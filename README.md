# agent-toolkit

Skills, tools, MCP servers, and configuration for AI agents. Each piece was built for a real problem - not as a demo. Provider-agnostic where possible, with a single directory for platform-specific content.

---

## What's Inside

| Area | Directory | Contents |
|------|-----------|----------|
| Skills | `productivity/` | Agent onboarding, context discipline, task scheduling |
| Skills | `development/` | SDLC pipeline - spec through ship (7 phases) |
| Skills | `browser/` | Browser automation with Cloudflare/WAF bypass |
| Skills | `autonomous-agents/` | Pi agent orchestration patterns |
| Tools | `tools/` | Bookmark sync, cost analysis, email triage CLIs |
| MCP | `mcp/` | WAF-bypassing browser automation via MCP protocol |
| Extensions | `extensions/` | Chrome stealth extension for bot detection bypass |
| Themes | `themes/` | Hermes dashboard themes |
| Platform | `hermes/` | Hermes-specific tool plugins and scripts |
| References | `references/` | Shared checklists |

### Directory Map

```
agent-toolkit/
  productivity/                   Skills
    agent-constitution-setup/      3-doc onboarding system
    file-size-gatekeeper/          Context window discipline
    macos-task-scheduler/          launchd automation
  development/                    Skills
    sdlc-1-through-7/              7-phase SDLC pipeline
  browser/                        Skills
    browser-automation/            agent-browser + stealth extension
  autonomous-agents/              Skills
    pi-agent/                      Pi RPC orchestration
  tools/                          Standalone CLIs
    karakeep/                      Bookmark sync
    opencode-analyzer/             OpenCode cost analysis
    email-triage/                  Gmail noise archiver + reviewer
  mcp/                            MCP servers
    stealth-browser/               Browser automation with WAF bypass
  extensions/                     Browser extensions
    stealth-extension/             Manifest V3 anti-detection extension
  themes/                         UI themes
    hermes-dashboard/              Clean WebUI + Gruvbox Dark
  hermes/                         Platform-specific
    pi-agent/                      Hermes tool plugin for Pi RPC
  references/                     Shared docs
    security-checklist.md
    performance-checklist.md
    accessibility-checklist.md
    testing-patterns.md
  AGENTS.md                       Agent operating guide
  README.md                       This file
  LICENSE                         MIT
```

## Install

```bash
git clone git@github.com:ShaggyD/agent-toolkit.git ~/agent-toolkit

# Hermes: symlink for skill discovery
ln -sf ~/agent-toolkit ~/.hermes/skills

# Or clone directly to where Hermes looks
git clone git@github.com:ShaggyD/agent-toolkit.git ~/.hermes/skills
```

### Loading Skills

```bash
# Hermes
hermes -s browser-automation
# or in-session:  /skill browser-automation

# Other agents: read any SKILL.md as context
```

### MCP Servers

```bash
hermes mcp add stealth-browser \
  --command "python3 /path/to/mcp/stealth-browser/assets/mcp_server.py"
```

### Tools

Tools are standalone binaries:

```bash
cp tools/karakeep/kk ~/.local/bin/
cp tools/opencode-analyzer/opencode-cost ~/.local/bin/
```

## Highlighted Pieces

1. **SDLC Pipeline** - 7 ordered skills (spec, plan, implement, test, review, simplify, ship). Adapted from Addy Osmani's open-source framework.

2. **Stealth Browser MCP** - MCP server wrapping agent-browser with anti-detection flags and a bundled content script that patches navigator.webdriver, plugins, languages, and permissions API. Bypasses Cloudflare, LinkedIn, and Indeed without paid proxies.

3. **Stealth Extension** - Manifest V3 Chrome extension that patches browser fingerprint vectors at document_start, before page scripts run.

4. **Email Triage** - Two-layer Gmail pipeline: zero-LLM noise archiver (Janitor) + LLM-powered daily reviewer. No database, no server, no API keys for the Janitor layer.

5. **Pi Agent Orchestration** - Stateful RPC control patterns for remote coding agents. Covers auth, session lifecycle, response extraction, and failure modes.

## License

MIT - use freely, adapt openly, attribute where meaningful.

SDLC skills adapted from addyosani/agent-skills (MIT). Shared checklists imported from the same source. Constitution framework by Allie Miller (Silicon Valley Girl). Browser automation built with agent-browser CLI (Vercel Labs).

---

Maintained by Dustin "Dusty" Chadwick
