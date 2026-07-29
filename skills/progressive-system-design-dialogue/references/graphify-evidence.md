# Graphify C4 Evidence Protocol

Read this file before collecting a baseline, generating a C4 view, changing a C4 contract, or comparing architecture snapshots.

## Preconditions

1. Record the project root and exact repository revision for every graph input.
2. Check whether an existing code graph is current enough for the question. Prefer a scoped graph query, path, explain, or impact operation before raw source search.
3. Confirm the C4 contract has stable IDs, declared boundaries, and implementation mappings before presenting a Component-level result.
4. Keep the same C4 contract for before/after projection whenever possible. If it differs, record the difference and label the comparison limited.
5. Do not overwrite a baseline. Copy or generate a separately named snapshot before any rebuild that updates Graphify output.

## Standard Commands

Use only commands supported by the installed Graphify version. Typical commands for a repository are:

```text
graphify query "<architecture question>"
graphify architecture sync
graphify architecture validate
graphify architecture dependencies
graphify architecture audit --suspect
graphify architecture impact <node-or-file>
graphify architecture html
```

For a workspace, use its declared model and paths, for example:

```text
graphify architecture workspace html \
  --model architecture/graphify.workspace.c4.json \
  --root . \
  --out architecture/graphify-out/architecture.json \
  --graph-out architecture/graphify-out/workspace-graph.json \
  --output architecture/graphify-out/architecture.html
```

Do not run an extraction or rebuild merely because an architecture question was asked. Rebuild only when the graph is missing, stale for the recorded revision, or the user approves a new baseline.

## Baseline Manifest

For each component or repository record:

- repository URL or local source identity;
- branch and commit SHA;
- clean/dirty status and whether dirty state is intentionally included;
- Graphify version and command used;
- C4 contract path and content revision;
- code graph, C4 projection, and HTML paths;
- collection timestamp and known extractor limitations.

For multi-repository systems, build one evidence graph per repository and then compose a workspace only through Graphify's supported workspace mechanism. Do not infer HTTP, queue, CLI, or datastore calls across repositories from shared names; declare them as contracts until an extractor can prove them.

## Interpretation

Report architecture findings in this order:

1. **Graph facts**: declared and observed relations, each with source evidence.
2. **Uncertainties**: unmapped code, ambiguous ownership, suspect resolution, stale graph, or absent extractor support.
3. **Decision**: a proposed component, boundary, dependency, or rule.
4. **Full-graph impact**: components, relations, consumers, rules, and verification work that change.

Classify evidence correctly:

- `EXTRACTED`: a direct source fact; it can support automated enforcement when its resolution is reliable.
- `INFERRED`: a derived resolution; use it as a design lead and verify it.
- `AMBIGUOUS`, name-only, or unknown resolution: queue for review; do not call it a confirmed violation.

Absence from a graph means only that the current extractor did not find it. Never phrase it as proof that the dependency does not exist.

## C4 UI Protocol

Generate an interactive C4 HTML view when Graphify supports it. Open or link the generated page through the current environment's browser capability.

- Begin a technical discussion at the complete Component graph.
- Use Context for actors/external systems and Container for deployment/runtime questions, then return to Component for technical decisions.
- Use highlight to focus a component and direct relationships without deleting full-system context.
- Descend to Code and inspect evidence before accepting a relationship claim.
- Record the exact HTML and projection paths in the ledger. The UI is a view of evidence, not evidence by itself.

## Historical Comparison

Create two named snapshots from comparable revisions. Compare their C4 projections with an architecture diff, for example:

```text
graphify architecture diff \
  --before <before>/architecture.json \
  --after <after>/architecture.json \
  --out <diff>/architecture-diff.json \
  --html <diff>/architecture-diff.html
```

Inspect lifecycle changes at Context, Container, Component, and Code levels. At Component level, verify every expected added, removed, or modified component and relationship. Descend to the evidence-bearing Code relation before declaring the delta satisfied. Record unexpected changes as risks, accepted exceptions, or design defects; never hide them by filtering the graph.

Graph diff does not verify runtime authorization, data correctness, latency, availability, rollout safety, or observability. Add test, security, migration, telemetry, and operational evidence to the verification plan separately.
