# AGENTS.md - Agent Operating Guide

This file tells AI coding agents how to work with this repository. Read it before making changes.

---

## Repository Purpose

A collection of portable, provider-agnostic artifacts for AI agents - skills, tools, MCP servers, browser extensions, and UI themes. Each artifact is designed to work across different agent platforms without modification.

## Structure

```
agent-toolkit/
  AGENTS.md                     This file
  README.md                     Artifact index
  LICENSE                       MIT
  .gitignore                    Allowlist pattern
  <category>/
    <name>/
      SKILL.md                  Core instructions (skills, tools, MCP)
      references/               Deep-dive reference material (optional)
      assets/                   Binaries, scripts, configs (optional)
      templates/                Template files (optional)
  hermes/                       Platform-specific content
```

### Category Index

| Directory | Purpose |
|-----------|---------|
| `productivity/` | Skill docs (SKILL.md) - Hermes discovers automatically |
| `development/` | Skill docs (SKILL.md) - Hermes discovers automatically |
| `browser/` | Skill docs (SKILL.md) - Hermes discovers automatically |
| `autonomous-agents/` | Skill docs (SKILL.md) - Hermes discovers automatically |
| `tools/` | Standalone CLIs + SKILL.md docs |
| `mcp/` | MCP servers + SKILL.md docs |
| `extensions/` | Browser extension assets |
| `themes/` | Dashboard theme configs |
| `references/` | Shared reference docs |
| `hermes/` | Platform-specific tooling and scripts |

### Conventions

- Category directories are flat, single-level.
- Name directories are kebab-case, descriptive, unique.
- SKILL.md is the primary instruction file. Reference material over ~18000 characters should be split into references/.
- Outside hermes/, do not reference specific agent platforms (Hermes, Claude, Codex, ChatGPT). Use "the agent" or "the user's AI agent."
- Binaries (e.g., kk in tools/karakeep/) are committed alongside their SKILL.md.
- MCP servers live in mcp/<name>/ with SKILL.md + assets/mcp_server.py.
- Browser extensions live in extensions/<name>/ with manifest.json and JS files.

## Editing

### Before

1. Read this file.
2. Read README.md for the full artifact index.
3. Check .gitignore - new files need allowlist entries.
4. Check file sizes - SKILL.md should stay under 18000 characters.

### During

- Preserve YAML frontmatter on SKILL.md (name, description, version, author, tags).
- Keep provider-agnostic language outside hermes/.
- Keep README.md in sync with the artifact index.
- Use relative links where possible.

### After

- [ ] git status shows only intended changes
- [ ] New files have allowlist entries in .gitignore
- [ ] SKILL.md is under 18000 characters
- [ ] README.md includes the artifact if it's new
- [ ] Internal links are valid
- [ ] YAML frontmatter is present on new SKILL.md
- [ ] No platform-specific language outside hermes/

## Git

- Commits: conventional prefixes (feat:, fix:, docs:, chore:).
- Direct commits to main are fine for single-artifact changes. Feature branches for repo-wide restructuring.
- Only explicitly allowlisted artifacts (those with ! entries in .gitignore) are tracked.

---

Maintained by Dustin "Dusty" Chadwick
