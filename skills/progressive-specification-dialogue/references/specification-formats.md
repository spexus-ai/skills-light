# Specification Formats

Read this file before drafting or changing user stories, requirements, or acceptance criteria.

## Contents

- Language Contract
- User Stories
- Requirements: EARS And INCOSE
- Acceptance Criteria: Gherkin
- Traceability
- Quality Gate

## Language Contract

Keep the skill source, instructions, and bundled examples in English. Write runtime specification artifacts in the user's current dialogue language unless the user explicitly requests another artifact language.

At runtime, localize:

- user-story titles and statements;
- requirement titles, statements, and EARS keywords;
- acceptance-criterion titles, traceability labels, feature and scenario names, and Gherkin keywords;
- artifact headings, explanations, errors, constraints, and examples.

Keep identifier prefixes `US`, `REQ`, and `AC` unchanged because they are language-neutral references.

For non-English Gherkin, use the official localized dialect and include `# language: <dialect-code>` when supported. If the correct dialect is uncertain, verify it or ask the user; do not silently mix English keywords into a localized runtime artifact.

## User Stories

Use the role-capability-benefit structure and translate it into the runtime artifact language:

```text
As a <role>, I want <capability>, so that <benefit>.
```

Keep one stable user job per user story. Do not place requirements or acceptance scenarios inside the user-story sentence.

## Requirements: EARS And INCOSE

Write each requirement as one valid EARS pattern. Translate the keywords while preserving their semantic roles and order.

| Pattern | Structure |
|---|---|
| Ubiquitous | `THE <system> SHALL <response>` |
| Event-driven | `WHEN <trigger>, THE <system> SHALL <response>` |
| State-driven | `WHILE <state>, THE <system> SHALL <response>` |
| Unwanted event | `IF <condition>, THEN THE <system> SHALL <response>` |
| Optional feature | `WHERE <option>, THE <system> SHALL <response>` |

For complex requirements, preserve this order after translation:

```text
WHERE -> WHILE -> WHEN/IF -> THE SYSTEM -> SHALL
```

Use this structural shape, translated at runtime:

```markdown
##### US-001-REQ-001 — Short title

WHEN an employee submits a valid vacation request, THE system SHALL store the request with status "Pending approval".
```

Apply INCOSE-style quality checks to every requirement:

- use active voice and name the responsible system;
- express one required behavior;
- use explicit triggers, states, inputs, outputs, and thresholds;
- avoid vague terms, escape clauses, ambiguous pronouns, and undefined absolutes;
- state observable behavior rather than an implementation technique;
- use consistent domain terminology;
- keep the requirement feasible and verifiable.

Rewrite noncompliant user wording into a compliant requirement without changing product intent. Record material interpretation as provisional until the user confirms it.

## Acceptance Criteria: Gherkin

Write acceptance criteria as separate observable Gherkin scenarios in the runtime artifact language. Use one primary behavior per scenario.

Use this structural shape, translated at runtime:

````markdown
##### US-001-AC-001 — Valid request is submitted for approval

Verifies: US-001-REQ-001

```gherkin
Scenario: Submit a valid vacation request
  Given the employee is authenticated
  And valid vacation dates are entered
  When the employee submits the request
  Then the system stores it with status "Pending approval"
  And shows the stored request to the employee
```
````

Order scenarios as:

1. happy path;
2. additional valid variants;
3. negative scenarios and visible failures;
4. boundary and edge cases.

Do not hide multiple unrelated behaviors inside one scenario. Do not describe internal implementation steps unless they are observable contract requirements.

## Traceability

- Give every user story, requirement, and acceptance criterion a stable identifier.
- Use fully scoped identifiers such as `US-001-REQ-001` and `US-001-AC-001`.
- Add `Verifies: <requirement IDs>`, translated at runtime, to every acceptance criterion.
- Give every requirement at least one acceptance criterion before readiness, or record why it is intentionally unverifiable.
- When one scenario verifies multiple requirements, list each identifier explicitly.
- Never renumber identifiers after they are referenced; mark removed items obsolete instead.

## Quality Gate

Before marking an epic ready, verify:

- the complete runtime epic uses the user's language consistently;
- every user story follows the translated role-capability-benefit structure;
- every requirement follows a translated EARS pattern and passes INCOSE-style checks;
- every acceptance criterion uses valid localized Gherkin;
- positive, negative, and edge scenarios are covered where relevant;
- requirement-to-acceptance traceability is complete;
- no scenario contradicts its requirement or project steering.
