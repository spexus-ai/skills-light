# Interactive Skill Installation

This document is an instruction for Codex, Claude Code, OpenCode, and other agents that support `SKILL.md` packages. Follow it as an interactive workflow. Do not install every skill automatically.

## Required Behavior

1. Treat the repository containing this file as the source repository.
2. Inspect every direct child of `skills/` that contains a `SKILL.md` file.
3. Read each discovered `SKILL.md` frontmatter and enough of its body and bundled resources to understand:
   - its name and purpose;
   - when it should be used;
   - required tools, runtimes, services, or permissions;
   - files or project state it may create or change;
   - compatibility concerns for the current agent.
4. Ignore directories without `SKILL.md`. Do not treat README files, examples, or references as separate installable skills.
5. Present the discovered skills to the user as a numbered table with these columns:

   | Number | Skill | What it does | Requirements or cautions | Installation status |
   | --- | --- | --- | --- | --- |

6. Explain the list in the user's language and use plain language. Mention technical details only when they affect installation or use.
7. Ask which skills the user wants to install. Accept `all`, skill names, numbers, or a comma-separated selection. Ask even when the repository contains only one skill.
8. Do not copy, link, replace, or delete anything before the user answers.

Use this question or its translation:

> Which skills would you like to install? You can answer with `all`, skill names, or numbers from the table.

## Choose the Installation Target

Detect the current agent when possible. If the agent or scope is ambiguous, ask the user whether the selected skills should be installed for the current user or only for the current project.

Use these default destinations:

| Agent | User installation | Project installation |
| --- | --- | --- |
| Codex | `~/.agents/skills` | `<project-root>/.agents/skills` |
| Claude Code | `~/.claude/skills` | `<project-root>/.claude/skills` |
| OpenCode | `~/.config/opencode/skills` | `<project-root>/.opencode/skills` |

If the user requests installation for more than one agent, treat each destination separately and show the complete destination plan before writing. Do not assume that one agent's personal directory is read by another agent.

When the environment exposes a different configured skills directory, prefer that explicit configuration and tell the user which path will be used. In particular, Codex's native `$skill-installer` may manage local installations under `$CODEX_HOME/skills` or `~/.codex/skills`; use that destination when invoking the native installer instead of direct copying.

## Preflight Checks

For every selected skill:

1. Confirm that the source directory name matches the `name` in `SKILL.md`.
2. Confirm that `SKILL.md` contains non-empty `name` and `description` frontmatter fields.
3. Include the complete skill directory, not only `SKILL.md`. Preserve bundled `agents/`, `references/`, `scripts/`, assets, and other files.
4. Resolve the absolute source and destination paths.
5. Check whether the destination already exists.

Classify an existing destination as:

- `not installed`: the destination does not exist;
- `same version`: its files match the source;
- `different version`: the destination exists and differs;
- `invalid`: the destination exists but is not a valid skill directory.

If any destination is `different version` or `invalid`, show the affected files and ask the user to choose `update`, `skip`, or `cancel`. Never overwrite it silently. Before an approved replacement, create a timestamped backup beside the destination and report its path.

Prefer copying the complete directory over creating a symbolic link. Use a symbolic link only when the user explicitly asks for a repository-linked development installation and the current agent supports linked skill directories.

## Installation

After the user confirms the skill selection and any conflict decisions:

1. Create only the required destination parent directories.
2. Copy each selected skill directory to `<destination>/<skill-name>`.
3. Preserve executable permissions on bundled scripts.
4. Do not modify the source repository.
5. Do not install dependencies, start services, or change agent configuration unless the user separately approves those actions.
6. Stop on the first failed installation and report which skills succeeded, failed, and were not attempted.

An agent may use its native skill installer instead of copying when that installer can install the exact selected repository paths and preserves all bundled files. The same selection, conflict, approval, and verification rules still apply.

## Verification

After installation:

1. Confirm that every selected destination contains `SKILL.md` and all expected bundled files.
2. Re-read the installed frontmatter and confirm that the installed skill name matches its directory.
3. Report each selected skill as `installed`, `updated`, `already current`, `skipped`, or `failed`.
4. Show the absolute destination path for every installed or inspected skill.
5. Tell the user to start a new agent session if the current agent does not discover newly installed skills immediately.

End with a concise result table. Do not claim success for a skill that was not verified.

## Platform References

- [Codex skills](https://developers.openai.com/codex/skills/)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [OpenCode skills](https://opencode.ai/docs/skills/)
