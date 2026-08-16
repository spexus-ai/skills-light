# Prompt Templates

Use these templates when turning lint findings into executable work.

## Auto-Fix Prompt

```text
Apply the safe lint fixes in this bounded scope.

Scope:
- Files: <files>
- Issue types: <issue types>

Constraints:
- Keep behavior unchanged.
- Do not broaden lint exclusions.
- Make only mechanical fixes.
- Do not perform structural refactoring unless the refactor coverage gate has passed.

Verification:
- Run <command>

Return:
- Files changed
- What was fixed
- Verification result
```

## Local Refactor Prompt

```text
Fix the lint findings in this local refactor slice.

Goal:
- Reduce <linters> findings in <files>

Constraints:
- Keep API behavior unchanged.
- Prefer helper extraction, early returns, and response normalization.
- Do not touch files outside the listed scope.
- Before changing code, confirm targeted coverage is at least 30% and happy path behavior is covered.
- For nested `if` refactors, confirm every branch is covered by tests before changing branch structure.

Verification:
- Run <lint command>
- Run <targeted tests>
- Report before/after coverage for the affected scope when tooling supports it.

Return:
- Files changed
- Refactor summary
- Remaining lint findings in scope
```

## High-Risk Delegated Prompt

```text
Fix the high-risk lint findings in this bounded slice.

Scope:
- Files: <files>
- Main issues: <linters and examples>

Required approach:
- Preserve behavior and contracts.
- Before changing code, analyze the exact code path being refactored.
- Confirm targeted coverage is at least 60% for the changed area.
- Confirm critical paths and important domain paths are covered.
- If any important test gap remains, stop and report the gap instead of refactoring.
- Refactor incrementally.
- Add or update targeted tests if needed.
- Keep the write scope disjoint from other agents.

Verification:
- Run <lint command limited to scope>
- Run <targeted test command>

Final response must include:
- Files changed
- Risky areas reviewed
- Verification results
- Any remaining findings or blockers
```

## Final Remediation Plan

```text
Lint remediation plan

Current status:
- Lint command: <command>
- Report path: <path>
- Total findings: <count>
- Coverage gate: <passed|failed|not applicable>, <evidence>

Noise / exclusions:
- <decision>

Auto-fixes already applied:
- <list>

Remaining tasks:
1. <title>
   Risk: <low|medium|high>
   Files: <files>
   Issue types: <types>
   Coverage gate: <required threshold, covered paths, gaps>
   Why not auto-fix: <reason>
   Prompt: <execution prompt>
   Verification: <commands>
```
