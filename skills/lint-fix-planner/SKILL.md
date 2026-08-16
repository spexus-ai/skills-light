---
name: lint-fix-planner
description: Run a project linter, capture and analyze its report, separate lint noise from real work, auto-fix small safe issues, enforce pre-refactor test coverage gates, and produce an interactive remediation plan with concrete follow-up prompts. Use when the user asks to run `golangci-lint`, ESLint, Ruff, or another linter; to triage a lint report; to classify warnings into quick fixes vs refactors; to check coverage before lint-driven refactoring; to propose exclusions; or to delegate larger lint cleanup tasks to subagents.
---

# Lint Fix Planner

Execute a linter remediation workflow end to end: run the linter, save the report, summarize it, present an interactive triage, apply safe fixes, and turn the remaining work into bounded implementation prompts.

## Workflow

1. Establish the lint command.
If the user already gave the command, use it. Otherwise inspect the repo for the canonical entrypoint:
- `Makefile`
- package scripts
- CI config
- tool config such as `.golangci.yml`, `eslint.config.*`, `pyproject.toml`

2. Capture a report artifact.
Prefer a file-backed report so the analysis is reproducible. Use a timestamped path under the repo, for example:

```bash
mkdir -p artifacts/lint
<lint-command> | tee artifacts/lint/linter-report-$(date -u +%Y%m%dT%H%M%SZ).txt
```

If the command returns non-zero because issues were found, keep going. Stop only for execution failures such as a missing binary, broken config, or a crash.

3. Summarize the report with the bundled script.
Run:

```bash
python3 scripts/summarize_lint_report.py <report-path> --format markdown
python3 scripts/summarize_lint_report.py <report-path> --format json
```

Use the script output as the baseline summary. If the report format is unsupported, fall back to manual triage.

4. Classify findings into four buckets.

- `Noise / policy`
  Path-based or test/example/docs-only warnings that might belong in exclusions rather than code changes.
- `Safe auto-fix`
  Small, low-risk changes you can make directly in the current thread without design discussion.
- `Local refactor`
  Single-file or single-function cleanup such as extracting helpers, flattening conditionals, or fixing duplication.
- `High-risk refactor`
  Auth, permissions, search, repository, concurrency, or cross-file service logic where behavioral regressions are plausible.

5. Run the pre-refactor test coverage gate before proposing code changes.
Before changing or refactoring production code, establish whether the modified code has enough test coverage for the intended risk level. Inspect repo scripts, CI, and language tooling for a standard test and coverage command. Prefer targeted package/module coverage for the affected code over only project-wide coverage.

Record:
- coverage command and test command used
- current coverage percentage for the affected package/module/file/function when available
- covered happy paths, critical paths, and branch conditions relevant to the lint finding
- uncovered behavior gaps that must be closed before refactoring

If coverage cannot be measured with the project tooling, treat that as a test gap. Do not proceed with refactoring until the user explicitly accepts a task to add coverage first or chooses a targeted suppression/exclusion instead.

6. Present an interactive remediation brief before editing.
The brief must be short and decision-oriented. Always include:
- lint command
- report path
- coverage gate verdict for refactor candidates
- total issues by linter
- top noisy paths
- top high-risk files
- what you recommend fixing now vs excluding vs delegating

Offer concrete options, for example:
- `A` tighten exclusions only
- `B` apply safe auto-fixes now
- `C` generate prompts/tasks for larger work
- `D` apply safe fixes and delegate selected larger slices

If the user already gave a strong instruction, skip the option menu and execute the obvious path.

For metric-driven refactors, run a before/after report. If complexity is only moved into a helper and lint totals do not improve, prefer a targeted suppression over abstraction.

7. Apply safe fixes yourself.
Safe fixes are usually:
- `errcheck` on obvious cleanup paths
- `unused`
- trivial `staticcheck` rewrites
- formatting-adjacent simplifications
- test-only cleanup when tests are intentionally in scope

Do not silently perform large refactors under the label of auto-fix.

8. Turn larger work into prompt-plan tasks.
For anything not safe to fix immediately, produce bounded tasks with:
- objective
- target files
- issue types
- pre-refactor coverage gate and required gap closure
- constraints
- required verification
- explicit non-goals

Use the templates in `references/prompt-templates.md`.

9. Delegate only when appropriate.
If subagent tools are available and the user wants delegation, spawn subagents only for bounded, non-overlapping slices. Good candidates:
- one package with local complexity cleanup
- one handler file family
- one MCP tool set
- one test-only cleanup slice

Keep the critical path local. Do not delegate the immediate blocking analysis step.

10. Gate metric-driven refactors.
When the task is to find the next refactor candidate or clean up metric linters (`dupl`, `funlen`, `gocognit`, `gocyclo`, `cyclop`, `nestif`), use this stricter flow:

1. Save a baseline lint report before any refactor.
2. Spawn a subagent to identify candidate files/functions from the baseline report and code context. The subagent must not edit files.
3. Analyze the subagent signals locally and classify candidates using the same buckets above: `Noise / policy`, `Safe auto-fix`, `Local refactor`, `High-risk refactor`.
4. Apply the pre-refactor test coverage gate to the leading candidate. Do not refactor when the gate fails; create a test-gap task first.
5. Apply the Refactor ROI / Metric Conservation check to the leading candidate before proposing code changes.
6. Ask the user to confirm the verdict: either the ROI is worth refactoring, the first task is closing coverage gaps, or the right action is a targeted suppression/exclusion.
7. If the user confirms refactoring and the coverage gate passes, spawn a worker subagent to implement the bounded change. Give it exact files, non-goals, expected tests, required coverage evidence, and required final output.
8. After the worker returns, review the diff locally and run a control lint command against the changed scope or full lint command. Compare with the baseline report and state whether the refactor improved, preserved, or worsened the lint situation.
9. If the refactor only relocates complexity, or introduces an equivalent/new warning, do not keep it by default. Report the result and recommend reverting to the simpler code plus targeted suppression unless the user explicitly chooses otherwise.

11. End with a prompt-plan artifact.
Always produce a final remediation plan that the user can approve or execute. The plan must contain:
- current lint status
- coverage gate status for any refactor tasks
- exclusions/noise decisions
- auto-fixes applied
- remaining tasks, ordered by risk
- ready-to-run prompts for delegated or future work

## Classification Rules

Use these heuristics consistently.

### Noise / policy

Treat as exclusion candidates, not automatic code work, when most of these are true:
- generated or documentation-oriented code
- examples or benchmarks
- tests that the team does not want under strict lint policy
- files already intentionally excluded elsewhere
- warnings dominated by style/metric linters rather than correctness linters

Do not silently add exclusions for production code. Present the tradeoff first.

### Safe auto-fix

Apply directly when all are true:
- the change is mechanical
- the affected behavior is obvious
- the edit is small and local
- verification is cheap

Examples:
- add missing error checks on cleanup calls
- replace `WriteString(fmt.Sprintf(...))` with `fmt.Fprintf(...)`
- remove unused helpers
- simplify obviously equivalent branches suggested by `staticcheck`

### Local refactor

Create a task or fix locally if the scope is contained:
- one file or one function cluster
- one linter family dominates
- there is a clear extraction or simplification path
- tests already cover the behavior
- affected code has at least 30% targeted coverage
- happy path behavior for the modified code is covered

Examples:
- `funlen`, `nestif`, `cyclop` in a single handler
- `dupl` across a few resolver helpers

### Pre-Refactor Test Coverage Gates

Apply these gates before any code change that modifies behavior structure, control flow, or abstractions.

- General rule: before changing or refactoring code, verify that the modified code has sufficient tests for the intended risk. If it does not, first create a test-gap task or add tests in a separate step.
- Low-risk refactor: require at least 30% targeted coverage for the affected package/module/file when measurable, and require happy path coverage for the modified behavior.
- Nested `if` refactor: require tests that cover every branch of the nested conditional tree before flattening, extracting, or reordering the branches.
- High-risk refactor: require local analysis of the exact code path being changed; targeted coverage for the changed area must be at least 60%; critical paths and important domain paths must be covered.
- High-risk blockers: if any important gap remains in the tests, do not start the refactor. Close all identified test gaps first, then rerun the coverage gate.
- Coverage evidence: prefer branch/path-specific tests over aggregate percentages. A package with acceptable total coverage still fails the gate when the branch or error path being changed is untested.
- Baseline protection: run the relevant tests before refactoring and after refactoring. If baseline tests already fail, stop and report the blocker unless the user's task is explicitly to fix those tests.

### Refactor ROI / Metric Conservation

Do not keep an abstraction merely because it reduces a metric on the original function.

Before accepting a refactor for `dupl`, `gocognit`, `gocyclo`, `funlen`, or `nestif`, compare the before/after lint report and, when useful, absolute complexity for the affected functions.

Prefer `//nolint:<linter>` or a narrow config exclusion when all are true:
- the duplicated code is short, boring, and domain-explicit
- the entities have different repositories, errors, permissions, or lifecycle semantics
- extracting a shared helper moves complexity into callbacks, config, or generics
- the total lint count does not improve, or another equivalent warning replaces the original
- readers would need to jump across more files to understand the same behavior

Accept the refactor only when it improves at least one of:
- total lint issue count
- absolute complexity across the whole affected path, not only wrapper functions
- behavior safety through clearer boundaries
- meaningful duplication without hiding domain differences

If the refactor only relocates complexity, record the experiment and revert to the simpler code with a targeted suppression comment explaining why the duplication is intentional.

### High-risk refactor

Escalate to a dedicated task or subagent when any of these are true:
- touches auth, permissions, query logic, search, repositories, transactions, or orchestration
- multiple functions/files need coordinated changes
- the main issue is `gocognit`, `cyclop`, or `dupl` in business logic
- the fix might change branching, data flow, or error semantics

Before implementation, high-risk refactors must pass the high-risk coverage gate. If targeted coverage is below 60%, or critical paths are not covered, produce a test-gap task instead of a refactor task.

Examples:
- permission evaluation
- scope resolution
- search option parsing
- repository ordering and filtering logic

## Subagent Delegation

Use subagents only if the user asked for delegation, or if invoking this skill explicitly implies delegated execution for larger tasks.

Before spawning:
- keep one blocking task local
- split work by disjoint write scope
- give each agent one bounded slice
- require the agent to report changed files and verification results

Prompt structure:
- goal
- files in scope
- lint issue types to fix
- coverage gate status and required test-gap closure
- constraints on behavior
- verification command
- required final output

Use the templates in `references/prompt-templates.md`.

## Final Output Format

Return the result in this order.

### 1. Lint Brief
- command used
- report path
- total findings
- issue distribution
- notable hotspots
- coverage gate verdicts for refactor candidates

### 2. Actions Taken
- exclusions changed or proposed
- safe fixes applied
- verification run

### 3. Prompt-Plan
For each remaining task include:
- `Title`
- `Risk`: low, medium, high
- `Why it is not auto-fix`
- `Files`
- `Issue types`
- `Execution prompt`
- `Verification`

## Resources

### `scripts/summarize_lint_report.py`

Parse common lint report lines, count issues by linter and path, and classify them into:
- `noise_candidate`
- `auto_fix_candidate`
- `local_refactor`
- `high_risk_refactor`

Prefer this script over hand-built counting.

### `references/prompt-templates.md`

Contains reusable prompt templates for:
- auto-fix execution plans
- local refactor tasks
- high-risk delegated tasks
- final remediation plan output
