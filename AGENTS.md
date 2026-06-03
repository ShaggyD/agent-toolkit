# AGENTS.md — Agent Operating Guide

This file tells AI coding agents how to work with this repository. Read it before making changes.

---

## Repository Purpose

A collection of **portable, provider-agnostic artifacts for AI agents** — skills, tools, MCP servers, browser extensions, and UI themes. Each artifact is designed to be exported from one agent platform and imported into another without modification.

## Canonical Structure

```
agent-toolkit/
├── AGENTS.md                     ← this file
├── README.md                     ← artifact index
├── LICENSE                       ← MIT
├── .gitignore                    ← allowlist pattern
├── <category>/
│   └── <name>/
│       ├── SKILL.md              ← core instructions (skills, tools, MCP)
│       ├── references/           ← deep-dive reference material (optional)
│       ├── assets/               ← binaries, scripts, configs (optional)
│       └── templates/            ← template files (optional)
└── hermes/                       ← platform-specific content
```

### Category Types

| Category | Purpose | Hermes discovers? |
|----------|---------|-------------------|
| `productivity/` | Pure skill docs (SKILL.md) | ✅ Yes |
| `development/` | Pure skill docs (SKILL.md) | ✅ Yes |
| `browser/` | Pure skill docs (SKILL.md) | ✅ Yes |
| `autonomous-agents/` | Pure skill docs (SKILL.md) | ✅ Yes |
| `tools/` | Standalone CLIs + SKILL.md docs | ✅ Yes (SKILL.md loaded) |
| `mcp/` | MCP servers + SKILL.md docs | ✅ Yes (SKILL.md loaded) |
| `extensions/` | Browser extension assets | ❌ No SKILL.md |
| `themes/` | Dashboard theme configs | ❌ No SKILL.md |
| `references/` | Shared reference docs | ❌ No SKILL.md |
| `hermes/` | Platform-specific tooling | ✅ Yes |

### Conventions

- **Category directories** are flat, single-level: `productivity/`, `development/`, `tools/`, `mcp/`, etc.
- **Name directories** are kebab-case, descriptive, and unique.
- **`SKILL.md`** is the primary instruction file. It must be self-contained enough for the agent to do its job, but reference material exceeding ~18 000 characters should be split into `references/`.
- **Provider-agnostic language**: Do not reference Hermes, Claude, ChatGPT, Codex, or any specific agent platform in content outside `hermes/`. Use "the agent" or "the user's AI agent." The `hermes/` directory is the only exception.
- **Binaries** (e.g., `kk` in `tools/karakeep/`) are committed alongside their SKILL.md.
- **MCP servers** live in `mcp/<name>/` with `SKILL.md` + `assets/mcp_server.py`.
- **Browser extensions** live in `extensions/<name>/` with `manifest.json` and JS files.

## Editing Rules

### Before You Edit

1. **Read this file.** (You just did. Good.)
2. **Read `README.md`** to understand the full artifact index.
3. **Check `.gitignore`.** New files need allowlist entries.
4. **Check file sizes.** SKILL.md should stay under 18 000 characters.

### During Editing

- **Preserve the frontmatter** — each `SKILL.md` starts with YAML frontmatter (`name`, `description`, `version`, `author`, `tags`). Keep it accurate.
- **Don't break provider-agnosticism** — avoid platform-specific terminology outside `hermes/`.
- **Keep `README.md` in sync** — the artifact index must list every published item.
- **Don't refactor unrelated artifacts** — a change to one should not touch another unless structural.
- **Use relative links** where possible.

### After Editing

- [ ] `git status` shows only intended changes
- [ ] New files have `!` allowlist entries in `.gitignore`
- [ ] `wc -c <path>/SKILL.md` < 18 000 for any modified or new skill
- [ ] `README.md` includes the artifact if it's new
- [ ] All internal links are valid
- [ ] YAML frontmatter is present on new `SKILL.md`
- [ ] No platform-specific language leaked outside `hermes/`

## Git Workflow

- **Commits**: Use conventional commit prefixes: `feat:`, `fix:`, `docs:`, `chore:`.
- **Branching**: Direct commits to `main` for single-artifact changes. Feature branches for repo-wide restructuring.
- **The `.gitignore` allowlist**: Only explicitly published artifacts (those with `!` entries) are tracked. When adding a new tracked file, add the corresponding `!` line.

## Key Files at a Glance

| File | Purpose |
|---|---|
| `README.md` | Artifact index — update when adding/removing anything |
| `AGENTS.md` | This file — agent operating guide |
| `.gitignore` | Allowlist for tracked artifacts |

---

*Questions an agent should ask itself before starting work: "Have I checked `.gitignore`? Is my edit provider-agnostic? Is the SKILL.md under the size threshold?"*
