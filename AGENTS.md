# AGENTS.md — Agent Operating Guide

This file tells AI coding agents how to work with this repository. Read it before making changes.

---

## Repository Purpose

A collection of **portable, provider-agnostic skill documents** for AI agents. Skills give agents deep context about a specific task, workflow, or domain. They are designed to be exported from one agent platform and imported into another without modification.

## Canonical Structure

```
AGENT_SKILLS/
├── AGENTS.md                     ← this file
├── README.md                     ← skill index, must stay in sync
├── LICENSE                       ← MIT
├── .gitignore                    ← allowlist pattern
└── <category>/
    └── <skill-name>/
        ├── SKILL.md              ← core instructions (required)
        ├── references/           ← deep-dive reference material (optional)
        ├── templates/            ← template files (optional)
        └── ...                   ← binaries, configs, etc. (optional)
```

### Conventions

- **Category directories** are flat, single-level: `productivity/`, `devops/`, `design/`, etc. No nested subcategories.
- **Skill directories** are kebab-case, descriptive, and unique across categories.
- **`SKILL.md`** is the primary file an agent reads. It must be self-contained enough for the agent to do its job, but reference material exceeding ~18 000 characters should be split into `references/` (see [file-size-gatekeeper](productivity/file-size-gatekeeper/)).
- **Provider-agnostic language**: Do not reference Hermes, Claude, ChatGPT, Codex, or any specific agent platform in skill content unless the skill is explicitly about that platform. Use "the agent" or "the user's AI agent."
- **Binaries** (e.g., `kk` in `karakeep-obsidian-sync/`) are committed directly alongside `SKILL.md` when the skill ships a tool.

## Editing Rules

### Before You Edit

1. **Read this file.** (You just did. Good.)
2. **Read `README.md`** to understand the skill index layout. The index lists every skill with a table, author, description, category, and file count. Adding a new skill means adding an index entry.
3. **Check `.gitignore`.** Changes that introduce new files must add allowlist entries.
4. **Check file sizes.** SKILL.md should stay under 18 000 characters. If you're adding substantial content, split into `references/` or `templates/` instead.

### During Editing

- **Preserve the frontmatter** — each `SKILL.md` starts with YAML frontmatter (`name`, `description`, `version`, `author`, `tags`). Keep it accurate.
- **Don't break provider-agnosticism** — avoid platform-specific terminology unless the skill is platform-specific by design.
- **Keep `README.md` in sync** — the skill index table must include every published skill. Categories, names, descriptions, and file counts must match reality.
- **Don't refactor unrelated skills** — a change to one skill should not touch other skills unless the change is structural (e.g., renaming a category).
- **Use relative links** where possible between files in the repo.

### After Editing

Run this checklist before committing:

- [ ] `git status` shows only the intended changes (no stray file additions)
- [ ] New files have `!` allowlist entries in `.gitignore`
- [ ] `wc -c <path>/SKILL.md` < 18 000 for any modified or added skill
- [ ] `README.md` index includes the skill if it's new
- [ ] All internal links (e.g., `../karakeep-obsidian-sync/`) are valid
- [ ] YAML frontmatter is present and well-formed on any new `SKILL.md`
- [ ] No platform-specific language leaked into a general-purpose skill

## Git Workflow

- **Commits**: Use conventional commit prefixes: `feat:` for new skills, `fix:` for bug fixes, `docs:` for documentation, `chore:` for housekeeping.
- **Branching**: Direct commits to `main` are fine for single-skill changes. For repo-wide restructuring or multi-skill changes, use a feature branch.
- **The `.gitignore` allowlist**: The repo root doubles as a Hermes Agent skills directory. Hermes built-in skills live on disk but are not tracked. Only explicitly published skills (those with `!` entries in `.gitignore`) are committed. When adding a new tracked file, add the corresponding `!` line.

## Key Files at a Glance

| File | Purpose |
|---|---|
| `README.md` | Skill index — update when adding/removing skills |
| `AGENTS.md` | This file — agent operating guide |
| `.gitignore` | Allowlist for tracked skills |
| `productivity/<skill>/SKILL.md` | Core instruction file for a skill |
| `productivity/<skill>/references/` | Extended reference material for a skill |

---

*Questions an agent should ask itself before starting work: "Do I know where the skill index lives? Have I checked `.gitignore`? Is my edit provider-agnostic? Is this skill's SKILL.md under the size threshold?"*
