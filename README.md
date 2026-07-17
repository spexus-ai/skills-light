# Skills Light

Lightweight Codex skills that work with local files and do not require MCP services.

## Repository layout

```text
skills-light/
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

## Installation

Clone the repository:

```bash
git clone git@github.com:spexus-ai/skills-light.git
```

Expose an individual skill to a project with a symbolic link:

```bash
mkdir -p /path/to/project/.codex/skills
ln -s /path/to/skills-light/skills/progressive-specification-dialogue \
  /path/to/project/.codex/skills/progressive-specification-dialogue
```

The repository remains the canonical source while the project-local link makes the skill discoverable by Codex.

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md` with valid `name` and `description` frontmatter.
2. Add only the resources the skill needs, typically `agents/`, `references/`, or `scripts/`.
3. Keep runtime artifacts outside this repository and document their target location in the skill.
4. Validate the skill with Codex's `skill-creator` validation script.
5. Add the skill to the table above.

## License

This repository is licensed under the [GNU General Public License v3.0](LICENSE).
