# agent-toolkit

Skills, tools, MCP servers, browser extensions, and UI themes for AI agents. Everything here was built for something specific, not as a demo. Provider-agnostic except for the hermes/ directory.

---

## Sections

### productivity/

Daily agent workflows.

<table>
<tr><td nowrap><a href="productivity/agent-constitution-setup/">agent-constitution-setup</a></td><td>Three documents (constitution, goals, strategy) that give an agent context on who you are and how you operate. Based on Allie Miller's framework from the Silicon Valley Girl podcast.</td></tr>
</table>

### development/

SDLC pipeline in 7 ordered phases, adapted from <a href="https://github.com/addyosmani/agent-skills">addyosmani/agent-skills</a> (MIT).

<table>
<tr><td nowrap><a href="development/sdlc-1-spec-driven-development/">sdlc-1-spec-driven-development</a></td><td>Define objective, assumptions, and boundaries before coding</td></tr>
<tr><td nowrap><a href="development/sdlc-2-planning-and-task-breakdown/">sdlc-2-planning-and-task-breakdown</a></td><td>Convert specs into dependency-aware plans</td></tr>
<tr><td nowrap><a href="development/sdlc-3-incremental-implementation/">sdlc-3-incremental-implementation</a></td><td>Build in thin, testable vertical slices</td></tr>
<tr><td nowrap><a href="development/sdlc-4-test-driven-development/">sdlc-4-test-driven-development</a></td><td>Red-Green-Refactor and reproduction-first bug fixes</td></tr>
<tr><td nowrap><a href="development/sdlc-5-code-review-and-quality/">sdlc-5-code-review-and-quality</a></td><td>Five-axis review gates before merge</td></tr>
<tr><td nowrap><a href="development/sdlc-6-code-simplification/">sdlc-6-code-simplification</a></td><td>Reduce complexity without behavior changes</td></tr>
<tr><td nowrap><a href="development/sdlc-7-shipping-and-launch/">sdlc-7-shipping-and-launch</a></td><td>Rollout, monitoring, and rollback discipline</td></tr>
</table>

### browser/

<table>
<tr><td nowrap><a href="browser/browser-automation/">browser-automation</a></td><td>Browser automation using <a href="https://github.com/vercel/agent-browser">agent-browser CLI (Vercel Labs)</a> with a stealth Chrome extension that bypasses Cloudflare and LinkedIn WAFs</td></tr>
</table>

### autonomous-agents/

<table>
<tr><td nowrap><a href="autonomous-agents/pi-agent/">pi-agent</a></td><td>Stateful RPC control for remote coding agents (pi --mode rpc)</td></tr>
</table>

### tools/

Standalone CLIs.

<table>
<tr><td nowrap><a href="tools/karakeep/">karakeep</a></td><td>Full CRUD CLI for Karakeep self-hosted bookmarking with optional Obsidian sync. Single Python file, zero dependencies</td></tr>
<tr><td nowrap><a href="tools/opencode-analyzer/">opencode-analyzer</a></td><td>OpenCode cost analysis with daily, weekly, and monthly breakdowns</td></tr>
<tr><td nowrap><a href="tools/email-triage/">email-triage</a></td><td>Two-layer Gmail pipeline. Zero-LLM noise archiver plus LLM-powered daily reviewer</td></tr>
</table>

### mcp/

<table>
<tr><td nowrap><a href="mcp/stealth-browser/">stealth-browser</a></td><td>MCP server with 10 browser automation tools that bypass Cloudflare and LinkedIn. Uses <a href="https://github.com/vercel/agent-browser">agent-browser CLI (Vercel Labs)</a> with anti-detection flags and bundled stealth extension</td></tr>
</table>

### extensions/

<table>
<tr><td nowrap><a href="extensions/stealth-extension/">stealth-extension</a></td><td>Manifest V3 Chrome extension that patches browser fingerprint vectors at document_start, before any page scripts run</td></tr>
</table>

### themes/

<table>
<tr><td nowrap><a href="themes/hermes-dashboard/">hermes-dashboard</a></td><td>Two themes for the Hermes Agent dashboard: Clean WebUI and Gruvbox Dark</td></tr>
</table>

### hermes/

Platform-specific tooling for Hermes Agent.

<table>
<tr><td nowrap><a href="hermes/pi-agent/">pi-agent</a></td><td>Hermes-native tool plugin for controlling pi --mode rpc sessions</td></tr>
</table>

### references/

Shared checklists imported from <a href="https://github.com/addyosmani/agent-skills">addyosmani/agent-skills</a> (MIT).

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

- SDLC skills adapted from <a href="https://github.com/addyosmani/agent-skills">addyosmani/agent-skills</a> (MIT)
- Shared checklists from <a href="https://github.com/addyosmani/agent-skills">addyosmani/agent-skills</a> (MIT)
- Constitution framework by Allie Miller via Silicon Valley Girl podcast
- Browser automation built with <a href="https://github.com/vercel/agent-browser">agent-browser CLI (Vercel Labs)</a>
- File-size-gatekeeper inspired by Andrew's OpenClaw Blueprint Series

---

Maintained by Dustin "Dusty" Chadwick
