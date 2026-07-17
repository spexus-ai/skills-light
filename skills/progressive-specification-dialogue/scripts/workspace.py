#!/usr/bin/env python3
"""Create, inspect, and validate flat local epic specification workspaces."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime
from pathlib import Path


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
EPIC_DIR_RE = re.compile(r"^[0-9]{2}-[0-9]{2}-[0-9]{4}-[a-z0-9]+(?:-[a-z0-9]+)*(?:-[0-9]{2})?$")
PHASE_RE = re.compile(r"^- Phase: ([A-Z_]+)\s*$", re.MULTILINE)
REVISION_RE = re.compile(r"^- Revision: ([0-9]+)\s*$", re.MULTILINE)
ROOT_RE = re.compile(r"^- Project root: (.+)\s*$", re.MULTILINE)
EPIC_NAME_RE = re.compile(r"^- Epic directory: (.+)\s*$", re.MULTILINE)

EPIC_MARKER = "<!-- PROGRESSIVE_SPEC_EPIC v1 -->"
LOG_MARKER = "<!-- PROGRESSIVE_SPEC_DECISION_LOG v1 -->"
STEERING_MARKER = "<!-- PROGRESSIVE_SPEC_STEERING v1 -->"


class WorkspaceError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def ensure_real_directory(path: Path, create: bool = False) -> None:
    if path.is_symlink():
        raise WorkspaceError(f"refusing symbolic-link directory: {path}")
    if path.exists() and not path.is_dir():
        raise WorkspaceError(f"expected directory but found another file type: {path}")
    if create:
        path.mkdir(parents=True, exist_ok=True)


def resolve_paths(root_arg: str, create: bool = False) -> tuple[Path, Path, Path, Path]:
    root = Path(root_arg).resolve()
    if not root.is_dir():
        raise WorkspaceError(f"project root is not a directory: {root}")
    runtime = root / ".spexus"
    steering = runtime / "steering"
    epics = runtime / "epics"
    for path in (runtime, steering, epics):
        ensure_real_directory(path, create=create)
    return root, runtime, steering, epics


def assert_regular_file(path: Path) -> None:
    if path.is_symlink() or not path.is_file():
        raise WorkspaceError(f"missing or invalid regular file: {path}")


def atomic_text(path: Path, content: str) -> None:
    temp = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    try:
        with temp.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        temp.replace(path)
    finally:
        if temp.exists():
            temp.unlink()


def display_title(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def epic_template(title: str, created: str) -> str:
    return f"""{EPIC_MARKER}
# {title}

- Status: draft
- Created at: {created}
- Updated at: {created}

## Goal
Not framed yet.

## Scope

### Included
Undetermined.

### Excluded
Undetermined.

## Users And Motivation
Undetermined.

## User Stories
Undetermined.

## Constraints And Important Rules
Undetermined.

## Success Evidence
Undetermined.

## Exceptions And Visible Failures
Undetermined.

## Technical Notes
Undetermined.

## Steering References
None recorded.

## Out Of Scope
Undetermined.

## Open Questions
- What goal are we trying to achieve?
"""


def decision_log_template(root: Path, epic_name: str, created: str) -> str:
    return f"""{LOG_MARKER}
# Decision Log

## Current State
- Project root: {root}
- Epic directory: {epic_name}
- Phase: START
- Revision: 0
- Dialogue language: undetermined
- Status: active
- Updated at: {created}
- Next question: What goal are we trying to achieve?

## Current Understanding
No substantive decisions recorded.

## Accepted Decisions
| ID | Date | Decision | Reason | Supersedes | Status |
|---|---|---|---|---|---|

## Open Questions
| Question | Why it matters | Status |
|---|---|---|
| What goal are we trying to achieve? | Establish the desired outcome. | open |

## Completeness
| Area | Score | Reason |
|---|---:|---|
| Goal | 0/5 | Not assessed |
| User path | 0/5 | Not assessed |
| System behavior | 0/5 | Not assessed |
| Success checks | 0/5 | Not assessed |
| Constraints | 0/5 | Not assessed |
| Technical notes | 0/5 | Not assessed |
| Ownership | 0/5 | Not assessed |
| QA readiness | 0/5 | Not assessed |
| NFR classification | 0/5 | Not assessed |

## Independent Reviews
No reviews recorded.

## Finalization
- User confirmation: pending
- Required reviews: incomplete
- Last validation: not run

## History

### {created} — START
- User input: Epic workspace initialization requested.
- Agent action: Created epic.md and decision-log.md.
- Decision: No substantive decision yet.
- Files changed: epic.md, decision-log.md.
"""


def steering_template(topic: str, created: str) -> str:
    return f"""{STEERING_MARKER}
# {display_title(topic)}

- Status: draft
- Updated at: {created}

## Decision
Not recorded yet.

## Context
Not recorded yet.

## Rules
Not recorded yet.

## Consequences
Not recorded yet.

## Related Epics
None recorded.
"""


def next_epic_name(epics: Path, slug: str) -> str:
    date_prefix = datetime.now().astimezone().strftime("%d-%m-%Y")
    base = f"{date_prefix}-{slug}"
    if not (epics / base).exists():
        return base
    counter = 2
    while (epics / f"{base}-{counter:02d}").exists():
        counter += 1
    return f"{base}-{counter:02d}"


def create_epic(root_arg: str, slug: str) -> dict[str, object]:
    if not SLUG_RE.fullmatch(slug):
        raise WorkspaceError("epic slug must be ASCII lowercase kebab-case")
    root, runtime, steering, epics = resolve_paths(root_arg, create=True)
    epic_name = next_epic_name(epics, slug)
    epic_dir = epics / epic_name
    epic_dir.mkdir(mode=0o755)
    created = now_iso()
    atomic_text(epic_dir / "epic.md", epic_template(display_title(slug), created))
    atomic_text(epic_dir / "decision-log.md", decision_log_template(root, epic_name, created))
    return {
        "action": "created-epic",
        "root": str(root),
        "runtime_root": str(runtime),
        "epic": epic_name,
        "epic_dir": str(epic_dir),
        "epic_file": str(epic_dir / "epic.md"),
        "decision_log": str(epic_dir / "decision-log.md"),
        "steering_dir": str(steering),
    }


def create_steering(root_arg: str, topic: str) -> dict[str, object]:
    if not SLUG_RE.fullmatch(topic):
        raise WorkspaceError("steering topic must be ASCII lowercase kebab-case")
    root, runtime, steering, _ = resolve_paths(root_arg, create=True)
    target = steering / f"{topic}.md"
    if target.exists():
        assert_regular_file(target)
        return {
            "action": "existing-steering",
            "root": str(root),
            "runtime_root": str(runtime),
            "topic": topic,
            "file": str(target),
        }
    atomic_text(target, steering_template(topic, now_iso()))
    return {
        "action": "created-steering",
        "root": str(root),
        "runtime_root": str(runtime),
        "topic": topic,
        "file": str(target),
    }


def list_workspace(root_arg: str) -> dict[str, object]:
    root, runtime, steering, epics = resolve_paths(root_arg, create=False)
    steering_files: list[str] = []
    epic_names: list[str] = []
    if steering.exists():
        steering_files = sorted(path.name for path in steering.iterdir() if path.is_file() and not path.is_symlink())
    if epics.exists():
        epic_names = sorted(path.name for path in epics.iterdir() if path.is_dir() and not path.is_symlink())
    return {
        "action": "status",
        "root": str(root),
        "runtime_root": str(runtime),
        "exists": runtime.exists(),
        "steering": steering_files,
        "epics": epic_names,
    }


def validate_epic(root_arg: str, epic_name: str) -> dict[str, object]:
    if not EPIC_DIR_RE.fullmatch(epic_name):
        raise WorkspaceError("invalid epic directory name")
    root, runtime, steering, epics = resolve_paths(root_arg, create=False)
    epic_dir = epics / epic_name
    ensure_real_directory(epic_dir)
    if not epic_dir.exists():
        raise WorkspaceError(f"epic directory does not exist: {epic_dir}")

    expected = {"epic.md", "decision-log.md"}
    actual = {path.name for path in epic_dir.iterdir()}
    unexpected = sorted(actual - expected)
    missing = sorted(expected - actual)
    errors: list[str] = []
    if missing:
        errors.append(f"missing files: {', '.join(missing)}")
    if unexpected:
        errors.append(f"unexpected epic entries: {', '.join(unexpected)}")

    epic_file = epic_dir / "epic.md"
    log_file = epic_dir / "decision-log.md"
    for path, marker in ((epic_file, EPIC_MARKER), (log_file, LOG_MARKER)):
        if path.name in missing:
            continue
        if path.is_symlink() or not path.is_file():
            errors.append(f"invalid regular file: {path.name}")
            continue
        if marker not in path.read_text(encoding="utf-8"):
            errors.append(f"missing marker in {path.name}: {marker}")

    phase = None
    revision = None
    if log_file.is_file() and not log_file.is_symlink():
        log_text = log_file.read_text(encoding="utf-8")
        phase_match = PHASE_RE.search(log_text)
        revision_match = REVISION_RE.search(log_text)
        root_match = ROOT_RE.search(log_text)
        epic_match = EPIC_NAME_RE.search(log_text)
        phase = phase_match.group(1) if phase_match else None
        revision = int(revision_match.group(1)) if revision_match else None
        if phase is None:
            errors.append("decision-log.md lacks phase")
        if revision is None:
            errors.append("decision-log.md lacks numeric revision")
        if not root_match or Path(root_match.group(1)).resolve() != root:
            errors.append("decision-log.md project root differs from invocation root")
        if not epic_match or epic_match.group(1).strip() != epic_name:
            errors.append("decision-log.md epic directory differs from target")

    invalid_steering: list[str] = []
    if steering.exists():
        for path in steering.iterdir():
            if path.is_symlink() or not path.is_file() or path.suffix != ".md" or not SLUG_RE.fullmatch(path.stem):
                invalid_steering.append(path.name)
                continue
            if STEERING_MARKER not in path.read_text(encoding="utf-8"):
                invalid_steering.append(path.name)
    if invalid_steering:
        errors.append(f"invalid steering files: {', '.join(sorted(invalid_steering))}")

    if errors:
        raise WorkspaceError("; ".join(errors))
    return {
        "action": "validated",
        "root": str(root),
        "runtime_root": str(runtime),
        "epic": epic_name,
        "epic_dir": str(epic_dir),
        "epic_file": str(epic_file),
        "decision_log": str(log_file),
        "phase": phase,
        "revision": revision,
        "valid": True,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status")
    status.add_argument("--root", default=".")

    epic = subparsers.add_parser("create-epic")
    epic.add_argument("--root", default=".")
    epic.add_argument("--slug", required=True)

    steering = subparsers.add_parser("create-steering")
    steering.add_argument("--root", default=".")
    steering.add_argument("--topic", required=True)

    validate = subparsers.add_parser("validate")
    validate.add_argument("--root", default=".")
    validate.add_argument("--epic", required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "status":
            result = list_workspace(args.root)
        elif args.command == "create-epic":
            result = create_epic(args.root, args.slug)
        elif args.command == "create-steering":
            result = create_steering(args.root, args.topic)
        else:
            result = validate_epic(args.root, args.epic)
    except (OSError, WorkspaceError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, **result}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
