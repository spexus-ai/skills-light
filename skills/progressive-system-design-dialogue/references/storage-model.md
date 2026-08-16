# Flat Local Architecture Storage Model

Read this file before locating, creating, or writing an architecture design.

## Allowed Runtime Tree

Use the invocation directory as `<project-root>`. Keep skill-owned state only in this layout:

```text
<project-root>/.spexus/
├── steering/
│   └── <technical-topic>.md
└── architecture/
    └── <dd-mm-yyyy>-<short-change-description>/
        ├── architecture.md
        └── decision-log.md
```

Do not create session directories, global active-state files, indexes, scratch notes, review files, or final copies. Keep temporary atomic-write files in the target directory and remove them immediately.

Graphify owns its graph and HTML outputs. Do not copy them into `.spexus/`. Record their absolute paths, source revision, contract path, and build time in the design ledger. Typical locations are `graphify-out/`, `architecture/graphify-out/`, or a user-selected snapshot directory.

## Naming

- Design directory: creation date in `dd-mm-yyyy`, then an ASCII lowercase kebab-case slug. Example: `29-07-2026-scoped-rbac`.
- Treat the directory name as immutable. On a same-day collision, append `-02`, `-03`, and so on.
- Steering file: ASCII lowercase kebab-case topic plus `.md`.
- Create only steering documents that describe a durable cross-design or project-wide decision and only after explicit user approval.

## Architecture Design

Use `architecture.md` as the coherent current design:

```markdown
<!-- PROGRESSIVE_SYSTEM_DESIGN v1 -->
# Architecture Change Title

- Status: draft
- Created at: ...
- Updated at: ...

## Change Goal And Non-Goals
...

## Evidence Baseline
- Revision: ...
- C4 contract: ...
- Code graph: ...
- C4 projection and UI: ...

## Current Architecture
### Facts
...
### Inferences And Unknowns
...

## Impact And Expected Graph Delta
| Component or relation | Lifecycle | Expected proof | Owner/consumer |
|---|---|---|---|

## Selected Design
...

## Contracts, Data, Trust, And Failure Behavior
...

## Migration, Rollout, And Rollback
...

## Verification Plan
### Graph Evidence
...
### Behavioral And Operational Evidence
...

## Risks And Open Questions
...

## Steering References
...
```

## Decision Ledger

Use `decision-log.md` as the only process-state and history ledger:

```markdown
<!-- PROGRESSIVE_SYSTEM_DESIGN_LEDGER v1 -->
# Architecture Decision Ledger

## Current State
- Project root: ...
- Design directory: ...
- Phase: START
- Revision: 0
- Dialogue language: ...
- Status: active
- Updated at: ...
- Next action: ...

## Evidence Baseline
| Repository/component | Revision | Clean | C4 contract | Graph/UI path | Collected at |
|---|---|---|---|---|---|

## Evidence Index
| Claim | Fact / inference / proposal / unknown | Source | Confidence | Conclusion |
|---|---|---|---|---|

## Expected C4 Delta
| Level | Node or relation | Expected lifecycle | Required evidence | Status |
|---|---|---|---|---|

## Validation And UI
| Check or artifact | Revision | Result/path | Status |
|---|---|---|---|

## Accepted Decisions
| ID | Date | Decision | Evidence | Confidence | Supersedes | Status |
|---|---|---|---|---|---|---|

## Open Questions And Risks
| Item | Why it matters | Owner | Status |
|---|---|---|---|

## Independent Reviews
...

## Finalization
- User confirmation: pending
- Required reviews: incomplete
- Baseline comparison: not run
- Last validation: not run

## History
### <timestamp> — <phase>
- Evidence or user input: ...
- Agent action: ...
- Decision: ...
- Files changed: ...
```

Update the timestamp and increment `Revision` on every material ledger change. Never delete history or reviewer output; mark obsolete entries as superseded.

## Resume Rules

1. List directories in `.spexus/architecture/`.
2. Match an explicit directory, title, change goal, or clearly related ledger.
3. Read both required files and only steering documents relevant to the current design question.
4. Ask the user to choose when several designs plausibly match.
5. Enter reentry review when the phase is `DONE`.
6. Never select solely by modification time.

## Write Ownership

- Main agent: all runtime writes.
- User: material architecture decisions, C4/steering approval, and readiness confirmation.
- Independent reviewers: read-only response text returned to the main agent.

At completion or partial failure, report absolute clickable paths for every relevant document and generated Graphify artifact, along with its status.
