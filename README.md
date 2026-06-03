# agent-toolkit

A collection of portable skills, standalone tools, MCP servers, browser extensions, and UI themes for AI agents. Each piece was built for a real problem, not as a demo. Provider-agnostic where possible, with a single directory for platform-specific content.

---

## Sections

### [productivity/](productivity/)

Skills for daily agent workflows:

- **agent-constitution-setup** - Three documents (constitution, goals, strategy) that give an AI agent context about who you are and how you operate. Based on Allie Miller's framework (Silicon Valley Girl podcast). Includes templates and real-world examples.
- **file-size-gatekeeper** - Prevents context-window bloat by enforcing size limits on skill files, config, and reference docs. Includes on-demand audit commands and optional nightly cron job.
- **macos-task-scheduler** - Schedule recurring tasks on macOS using launchd plists.

### [development/](development/)

SDLC pipeline in 7 ordered phases, adapted from Addy Osmani's agent-skills framework (MIT):

1. **sdlc-1-spec-driven-development** - Define objective, assumptions, and boundaries before coding
2. **sdlc-2-planning-and-task-breakdown** - Convert specs into dependency-aware plans
3. **sdlc-3-incremental-implementation** - Build in thin, testable vertical slices
4. **sdlc-4-test-driven-development** - Red-Green-Refactor and reproduction-first bug fixes
5. **sdlc-5-code-review-and-quality** - Five-axis review gates before merge
6. **sdlc-6-code-simplification** - Reduce complexity without behavior changes
7. **sdlc-7-shipping-and-launch** (optional) - Rollout, monitoring, and rollback discipline

### [browser/](browser/)

- **browser-automation** - Browser automation via agent-browser CLI (Vercel Labs) with a stealth anti-detection Chrome extension. Capable of bypassing Cloudflare, LinkedIn, and other WAFs using headless Chrome with patched fingerprint vectors. The stealth extension (also available standalone under [extensions/](extensions/)) patches navigator.webdriver, plugins, languages, and permissions API at document_start.

### [autonomous-agents/](autonomous-agents/)

- **pi-agent** - Stateful RPC control patterns for remote coding agents (pi --mode rpc). Covers session lifecycle, auth, response extraction, and common failure modes.

### [tools/](tools/)

Standalone CLIs, each with their own SKILL.md:

- **karakeep** - Full CRUD CLI for Karakeep (self-hosted bookmarking) with optional Obsidian vault sync. Single-file Python binary, zero external dependencies.
- **opencode-analyzer** - OpenCode cost analysis with daily/weekly/monthly breakdowns. Shows actual spending vs OpenRouter equivalents.
- **email-triage** - Two-layer Gmail pipeline: zero-LLM noise archiver (Janitor) + LLM-powered daily reviewer. No database, no server, no API keys for the Janitor layer.

### [mcp/](mcp/)

- **stealth-browser** - MCP server providing browser automation tools that bypass Cloudflare and LinkedIn. Uses agent-browser with anti-detection flags and a bundled stealth extension (no external skill dependency). Exposes 10 tools: navigate, snapshot, click, eval, type, set_viewport, screenshot, close, status, install.

### [extensions/](extensions/)

- **stealth-extension** - Manifest V3 Chrome extension that patches browser fingerprint vectors at document_start, before any page scripts run. Pairs with the browser-automation skill and stealth-browser MCP server.

### [themes/](themes/)

- **hermes-dashboard** - Two themes for the Hermes Agent web dashboard: Clean WebUI (white canvas, blue accents) and Gruvbox Dark (warm earthy dark mode).

### [hermes/](hermes/)

Platform-specific tooling for Hermes Agent:

- **pi-agent** - Hermes-native tool plugin and test suite for controlling pi --mode rpc sessions.

### [references/](references/)

Shared checklists imported from addyosmani/agent-skills (MIT):

- security-checklist.md
- performance-checklist.md
- accessibility-checklist.md
- testing-patterns.md

---

## Usage

```bash
git clone git@github.com:ShaggyD/agent-toolkit.git ~/agent-toolkit

# Hermes: symlink for skill discovery
ln -sf ~/agent-toolkit ~/.hermes/skills

# Load a skill
hermes -s browser-automation
# or in-session:  /skill browser-automation

# Register an MCP server
hermes mcp add stealth-browser --command "python3 path/to/mcp/stealth-browser/assets/mcp_server.py"

# Install a CLI tool
cp tools/karakeep/kk ~/.local/bin/
```

---

## License

MIT - use freely, adapt openly, attribute where meaningful.

**Attribution:**

- SDLC skills adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)
- Shared checklists imported from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)
- Constitution framework by Allie Miller via Silicon Valley Girl podcast
- Browser automation built with agent-browser CLI (Vercel Labs)
- File-size-gatekeeper inspired by Andrew's OpenClaw Blueprint Series

---

Maintained by Dustin "Dusty" Chadwick
