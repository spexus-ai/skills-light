# Flat Local Storage Model

Read this file before locating, creating, or writing an epic.

## Contents

- Allowed Runtime Tree
- Naming
- Epic Specification
- Decision Ledger
- Steering Documents
- Resume Rules
- Write Ownership
- Document Reporting

## Allowed Runtime Tree

Use the invocation directory as `<project-root>`. Allow only this structure:

```text
<project-root>/.spexus/
├── steering/
│   ├── project-organization.md
│   ├── architecture.md
│   └── <other-technical-topic>.md
└── epics/
    └── <dd-mm-yyyy>-<short-epic-description>/
        ├── epic.md
        └── decision-log.md
```

Do not create session directories, global state files, indexes, user-story directories, review files, scratch files, or final copies. Keep atomic-write temporary files inside the target directory and remove them immediately after replacement.

## Naming

- Epic directory: creation date in `dd-mm-yyyy`, a hyphen, then an ASCII lowercase kebab-case slug.
- Example: `17-07-2026-vacation-approval`.
- Treat the directory name as immutable.
- On same-day slug collision, append `-02`, `-03`, and so on.
- Steering file: ASCII lowercase kebab-case topic plus `.md`.
- Example: `project-organization.md`.

## Epic Specification

Use `epic.md` as the single evolving specification:

```markdown
<!-- PROGRESSIVE_SPEC_EPIC v1 -->
# Epic Title

- Status: draft
- Created at: ...
- Updated at: ...

## Goal
...

## Scope
### Included
...
### Excluded
...

## Users And Motivation
...

## User Stories

### US-001 — Short title
As a ..., I want ..., so that ...

#### Requirements
##### REQ-001 — Short title
...

#### Acceptance Criteria
##### AC-001 — Short title
...

## Constraints And Important Rules
...

## Success Evidence
...

## Exceptions And Visible Failures
...

## Technical Notes
...

## Steering References
- [Project organization](../../steering/project-organization.md)

## Out Of Scope
...

## Open Questions
...
```

Keep user-story, requirement, and acceptance identifiers stable after creation. Scope requirement and acceptance identifiers within their user story when ambiguity is possible, for example `US-001-REQ-001`.

## Decision Ledger

Use `decision-log.md` as the only ledger and process-state file:

```markdown
<!-- PROGRESSIVE_SPEC_DECISION_LOG v1 -->
# Decision Log

## Current State
- Project root: ...
- Epic directory: ...
- Phase: START
- Revision: 0
- Dialogue language: ...
- Status: active
- Updated at: ...
- Next question: ...

## Current Understanding
...

## Accepted Decisions
| ID | Date | Decision | Reason | Supersedes | Status |
|---|---|---|---|---|---|

## Open Questions
| Question | Why it matters | Status |
|---|---|---|

## Completeness
| Area | Score | Reason |
|---|---:|---|

## Independent Reviews
### <timestamp> — <review type>
- Reviewer: ...
- Input scope: ...
- Result: ...
- Main-agent disposition: ...
- Resulting action: ...

## Finalization
- User confirmation: pending
- Required reviews: incomplete
- Last validation: not run

## History
### <timestamp> — <phase>
- User input: ...
- Agent action: ...
- Decision: ...
- Files changed: ...
```

Update `Updated at` and increment `Revision` for every material ledger change. Re-read before writing. Never remove history or reviews; mark obsolete decisions as superseded.

## Steering Documents

Use one file per durable project-wide technical topic:

```markdown
<!-- PROGRESSIVE_SPEC_STEERING v1 -->
# Technical Topic

- Status: active
- Updated at: ...

## Decision
...

## Context
...

## Rules
...

## Consequences
...

## Related Epics
- [Epic title](../epics/17-07-2026-example/epic.md)
```

Create a steering file only when a concrete cross-epic or project-wide decision exists and the user approves it. Prefer a new topic file over an unrelated section in an existing file. Update an existing topic instead of duplicating it.

Common topics are examples, not mandatory files:

- `project-organization.md`
- `architecture.md`
- `technology-stack.md`
- `coding-standards.md`
- `data-storage.md`
- `integrations.md`
- `security.md`
- `testing-strategy.md`
- `deployment.md`

## Resume Rules

1. List directories under `.spexus/epics/`.
2. Match the request by explicit directory, title, goal, or clearly related ledger context.
3. Read both required epic files.
4. Read only steering documents relevant to the epic or current technical question.
5. If multiple epics plausibly match, ask the user to choose.
6. If the ledger phase is `DONE`, enter reentry review.
7. Never use modification time as the sole selection signal.

## Write Ownership

- Main agent: all file writes.
- User: product decisions, approval for steering changes, and final readiness confirmation.
- Subagents: read-only review responses returned to the main agent.
- Helper script: deterministic directory scaffolding and structural validation.

## Document Reporting

At completion or partial failure, report absolute clickable paths for every relevant steering file plus the epic specification and decision ledger. Report whether each was created, updated, or unchanged. Put this document list last.
