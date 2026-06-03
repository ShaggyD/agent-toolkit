# agent-toolkit

Skills, tools, MCP servers, browser extensions, and UI themes for AI agents. Everything here was built for something specific, not as a demo. Provider-agnostic except for the hermes/ directory.

---

## Sections

### productivity/

Daily agent workflows.

| Artifact | What |
|----------|------|
| [agent-constitution-setup](productivity/agent-constitution-setup/) | Three documents (constitution, goals, strategy) that give an agent context on who you are and how you operate. Based on Allie Miller's framework. |

### development/

SDLC pipeline in 7 ordered phases, adapted from Addy Osmani's agent-skills framework.

| Artifact | What |
|----------|------|
| [sdlc-1-spec-driven-development](development/sdlc-1-spec-driven-development/) | Define objective, assumptions, and boundaries before coding |
| [sdlc-2-planning-and-task-breakdown](development/sdlc-2-planning-and-task-breakdown/) | Convert specs into dependency-aware plans |
| [sdlc-3-incremental-implementation](development/sdlc-3-incremental-implementation/) | Build in thin, testable vertical slices |
| [sdlc-4-test-driven-development](development/sdlc-4-test-driven-development/) | Red-Green-Refactor and reproduction-first bug fixes |
| [sdlc-5-code-review-and-quality](development/sdlc-5-code-review-and-quality/) | Five-axis review gates before merge |
| [sdlc-6-code-simplification](development/sdlc-6-code-simplification/) | Reduce complexity without behavior changes |
| [sdlc-7-shipping-and-launch](development/sdlc-7-shipping-and-launch/) | Rollout, monitoring, and rollback discipline |

### browser/

| Artifact | What |
|----------|------|
| [browser-automation](browser/browser-automation/) | Browser automation using agent-browser CLI with a stealth Chrome extension that bypasses Cloudflare and LinkedIn WAFs |

### autonomous-agents/

| Artifact | What |
|----------|------|
| [pi-agent](autonomous-agents/pi-agent/) | Stateful RPC control for remote coding agents (pi --mode rpc) |

### tools/

Standalone CLIs.

| Artifact | What |
|----------|------|
| [karakeep](tools/karakeep/) | Full CRUD CLI for Karakeep self-hosted bookmarking with optional Obsidian sync. Single Python file, zero dependencies |
| [opencode-analyzer](tools/opencode-analyzer/) | OpenCode cost analysis with daily, weekly, and monthly breakdowns |
| [email-triage](tools/email-triage/) | Two-layer Gmail pipeline. Zero-LLM noise archiver plus LLM-powered daily reviewer |

### mcp/

MCP servers.

| Artifact | What |
|----------|------|
| [stealth-browser](mcp/stealth-browser/) | MCP server with 10 browser automation tools that bypass Cloudflare and LinkedIn. Uses agent-browser with anti-detection flags and bundled stealth extension |

### extensions/

Browser extensions.

| Artifact | What |
|----------|------|
| [stealth-extension](extensions/stealth-extension/) | Manifest V3 Chrome extension that patches browser fingerprint vectors at document_start, before any page scripts run |

### themes/

Dashboard themes.

| Artifact | What |
|----------|------|
| [hermes-dashboard](themes/hermes-dashboard/) | Two themes for the Hermes Agent dashboard: Clean WebUI and Gruvbox Dark |

### hermes/

Platform-specific tooling for Hermes Agent.

| Artifact | What |
|----------|------|
| [pi-agent](hermes/pi-agent/) | Hermes-native tool plugin for controlling pi --mode rpc sessions |

### references/

Shared checklists imported from addyosmani/agent-skills.

- security-checklist.md
- performance-checklist.md
- accessibility-checklist.md
- testing-patterns.md

---

## Usage

```
git clone git@github.com:ShaggyD/agent-toolkit.git ~/agent-toolkit

# Hermes: symlink for skill discovery
ln -sf ~/agent-toolkit ~/.hermes/skills

# Load a skill
hermes -s browser-automation

# Register an MCP server
hermes mcp add stealth-browser --command "python3 path/to/mcp/stealth-browser/assets/mcp_server.py"

# Install a CLI tool
cp tools/karakeep/kk ~/.local/bin/
```

---

## License

MIT - use freely, adapt openly, attribute where meaningful.

Attribution:

- SDLC skills adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)
- Shared checklists from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)
- Constitution framework by Allie Miller via Silicon Valley Girl podcast
- Browser automation built with agent-browser CLI (Vercel Labs)
- File-size-gatekeeper inspired by Andrew's OpenClaw Blueprint Series

---

Maintained by Dustin "Dusty" Chadwick
