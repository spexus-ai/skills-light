# Skills Light

Lightweight Agent Skills for Codex, Claude Code, OpenCode, and other compatible agents. The skills work with local files and do not require MCP services.

## Repository layout

```text
skills-light/
├── INSTALL.md
├── skills/
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── agents/
│       ├── references/
│       └── scripts/
├── LICENSE
└── README.md
```

Each skill is self-contained under `skills/<skill-name>/`. Add future skills as sibling directories; do not place skill runtime data in this repository.

## Available skills

| Skill | Description |
|---|---|
| [`progressive-specification-dialogue`](skills/progressive-specification-dialogue/) | Shapes a clear epic through progressive dialogue, local Markdown artifacts, and independent reviews. Stores runtime documents under the target project's `.spexus/` directory. |
| [`progressive-system-design-dialogue`](skills/progressive-system-design-dialogue/) | Designs and verifies architecture changes through local evidence ledgers, Graphify C4 projections, before/after diffs, and interactive UI. Does not require Spexus MCP. |
| [`lint-fix-planner`](skills/lint-fix-planner/) | Runs and triages linter reports, applies safe fixes, and prepares risk-aware remediation plans. |

## Installation

Clone the repository, then ask Codex, Claude Code, OpenCode, or another compatible agent to follow the interactive installer instructions:

```bash
git clone git@github.com:spexus-ai/skills-light.git
```

See [INSTALL.md](INSTALL.md). The agent will analyze all available skills, explain them, ask which ones to install, choose the correct destination for the active agent, and verify the result. It must not install or overwrite skills before receiving the user's selection and any required conflict approval.

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` with valid `name` and `description` frontmatter.
2. Add only the resources the skill needs, typically `agents/`, `references/`, or `scripts/`.
3. Keep runtime artifacts outside this repository and document their target location in the skill.
4. Validate the directory name and `SKILL.md` frontmatter against the Agent Skills format. When Codex is available, also run the `skill-creator` validation script.
5. Add the skill to the table above.

## License

This repository is licensed under the [GNU General Public License v3.0](LICENSE).
