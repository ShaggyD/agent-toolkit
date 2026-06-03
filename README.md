# agent-toolkit

A collection of portable skills, standalone tools, MCP servers, browser extensions, and UI themes for AI agents — built from real workflow needs, not templates.

**Provider-agnostic.** Every artifact works with Hermes, Claude, ChatGPT, Codex, or any agent that can read a SKILL.md and run a CLI. Platform-specific content lives in a single `hermes/` directory.

---

## What's Inside

| Layer | Category | Contents |
|-------|----------|----------|
| 📖 **Skills** | `productivity/` | Agent constitution setup, file-size gatekeeper, macOS task scheduler |
| 📖 **Skills** | `development/` | SDLC pipeline — spec, plan, implement, test, review, simplify, ship |
| 📖 **Skills** | `browser/` | Browser automation with Cloudflare/WAF bypass |
| 📖 **Skills** | `autonomous-agents/` | Pi agent orchestration patterns |
| 🔧 **Tools** | `tools/` | Standalone CLIs — bookmark sync (karakeep), cost analysis (opencode), email triage |
| 🔌 **MCP** | `mcp/` | Stealth browser MCP server — WAF-bypassing browser automation |
| 🌐 **Extensions** | `extensions/` | Chrome stealth extension — anti-bot-detection fingerprint patching |
| 🎨 **Themes** | `themes/` | Hermes dashboard themes — Clean WebUI and Gruvbox Dark |
| 🏛️ **Platform** | `hermes/` | Hermes-specific tool plugins and scripts |
| 📚 **References** | `references/` | Shared checklists — security, performance, accessibility, testing |

### Directory Map

```
agent-toolkit/
├── productivity/                   📖 Skill category
│   ├── agent-constitution-setup/     3-doc onboarding system
│   ├── file-size-gatekeeper/         Context window discipline
│   └── macos-task-scheduler/         launchd automation
├── development/                    📖 Skill category
│   └── sdlc-1-through-7/             7-phase SDLC pipeline
├── browser/                        📖 Skill category
│   └── browser-automation/           agent-browser + stealth extension
├── autonomous-agents/              📖 Skill category
│   └── pi-agent/                     Pi RPC orchestration patterns
├── tools/                          🔧 Standalone CLIs
│   ├── karakeep/                     Bookmark sync tool
│   ├── opencode-analyzer/            OpenCode cost analysis
│   └── email-triage/                 Gmail noise archiver + reviewer
├── mcp/                            🔌 MCP servers
│   └── stealth-browser/              Browser automation with WAF bypass
├── extensions/                     🌐 Browser extensions
│   └── stealth-extension/            Manifest V3 anti-detection extension
├── themes/                         🎨 UI themes
│   └── hermes-dashboard/             Clean WebUI + Gruvbox Dark
├── hermes/                         🏛️ Platform-specific
│   └── pi-agent/                     Hermes tool plugin for Pi RPC
├── references/                     📚 Shared docs
│   ├── security-checklist.md
│   ├── performance-checklist.md
│   ├── accessibility-checklist.md
│   └── testing-patterns.md
├── AGENTS.md                       Agent operating guide
├── README.md                       ← you are here
└── LICENSE                         MIT
```

## Installation

```bash
git clone git@github.com:ShaggyD/agent-toolkit.git ~/agent-toolkit

# Hermes users: symlink skills for discovery
ln -sf ~/agent-toolkit ~/.hermes/skills

# Or clone directly to Hermes skills dir
git clone git@github.com:ShaggyD/agent-toolkit.git ~/.hermes/skills
```

### Loading Skills

```bash
# Hermes
hermes -s browser-automation
# or in-session:  /skill browser-automation

# Other agents: read any SKILL.md directly as context
```

### Setting Up MCP Servers

```bash
hermes mcp add stealth-browser \
  --command "python3 /path/to/mcp/stealth-browser/assets/mcp_server.py"
```

### Using Tools

Tools are standalone — just add the directory to your PATH or copy binaries:

```bash
cp tools/karakeep/kk ~/.local/bin/
cp tools/opencode-analyzer/opencode-cost ~/.local/bin/
```

## Standout Artifacts

1. **SDLC Pipeline** — 7 ordered skills (spec → plan → implement → test → review → simplify → ship) for structured feature delivery. Adapted from Addy Osmani's open-source framework.

2. **Stealth Browser MCP** — MCP server wrapping agent-browser with anti-detection flags and a bundled content script that patches `navigator.webdriver`, `plugins`, `languages`, and permissions API. Bypasses Cloudflare, LinkedIn, and Indeed without paid proxies.

3. **Stealth Extension** — Manifest V3 Chrome extension loaded at `document_start` that patches browser fingerprint vectors before any page scripts run.

4. **Email Triage System** — Two-layer Gmail pipeline with a zero-LLM noise archiver and an LLM-powered daily reviewer. No database, no server, no LLM API keys for the Janitor layer.

5. **Pi Agent Orchestration** — Stateful RPC control patterns for remote coding agents. Auth, session lifecycle, response extraction, failure modes.

## License

MIT — use freely, adapt openly, attribute where meaningful.

**Attribution:**
- SDLC skills adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)
- Shared checklists imported from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)
- Constitution framework by Allie Miller via Silicon Valley Girl podcast
- File-size-gatekeeper inspired by Andrew's OpenClaw Blueprint Series
- Browser automation built with agent-browser CLI (Vercel Labs)
- Pi agent patterns documented from production usage

---

*Maintained by [Dustin "Dusty" Chadwick](https://github.com/ShaggyD)*
