# agent-toolkit

Skills, tools, MCP servers, browser extensions, and UI themes for AI agents. Everything here was built for something specific, not as a demo. Provider-agnostic except for the hermes/ directory.

---

## Sections

### productivity/

<table>
<tr><td nowrap><a href="productivity/agent-constitution-setup/">agent-constitution-setup</a></td><td>Agents drift when they don't know who you are or what you value. These three documents (constitution, goals, strategy) give them that anchor based on <a href="https://www.youtube.com/watch?v=YfRkj9kmQf0">Allie Miller's framework from the Silicon Valley Girl podcast</a> (hosted by Marina Mogilko). The result is an agent that acts consistent with your intent instead of guessing.</td></tr>
</table>

### development/

SDLC pipeline in 7 ordered phases, adapted from <a href="https://github.com/addyosmani/agent-skills">addyosmani/agent-skills</a> (MIT).

<table>
<tr><td nowrap><a href="development/sdlc-1-spec-driven-development/">sdlc-1-spec-driven-development</a></td><td>Most bugs come from unclear requirements. This phase forces you to write down objective, assumptions, and boundaries before any code gets written. Catches ambiguity early when it's cheap to fix.</td></tr>
<tr><td nowrap><a href="development/sdlc-2-planning-and-task-breakdown/">sdlc-2-planning-and-task-breakdown</a></td><td>A spec without a plan leads to messy execution. Breaks specs into ordered, dependency-aware tasks so nothing gets built before its prerequisites are ready.</td></tr>
<tr><td nowrap><a href="development/sdlc-3-incremental-implementation/">sdlc-3-incremental-implementation</a></td><td>Big bang merges break things and hide who broke what. Builds in thin, testable vertical slices so each piece works before the next one starts.</td></tr>
<tr><td nowrap><a href="development/sdlc-4-test-driven-development/">sdlc-4-test-driven-development</a></td><td>Writing tests after the code means tests that pass against broken logic. Red-Green-Refactor and reproduction-first bug fixes keep the test suite honest and the code correct.</td></tr>
<tr><td nowrap><a href="development/sdlc-5-code-review-and-quality/">sdlc-5-code-review-and-quality</a></td><td>Merging without review lets bad patterns compound. Five-axis review gates (correctness, security, performance, style, test coverage) catch what the author missed.</td></tr>
<tr><td nowrap><a href="development/sdlc-6-code-simplification/">sdlc-6-code-simplification</a></td><td>Code that works but is hard to understand is technical debt waiting to compound. Reduces complexity without changing behavior so the next person can reason about it.</td></tr>
<tr><td nowrap><a href="development/sdlc-7-shipping-and-launch/">sdlc-7-shipping-and-launch</a></td><td>A clean merge doesn't mean a clean deploy. Rollout, monitoring, and rollback discipline ensure the launch doesn't become the incident.</td></tr>
</table>

### browser/

<table>
<tr><td nowrap><a href="browser/browser-automation/">browser-automation</a></td><td>Standard headless browsers get blocked by Cloudflare and LinkedIn immediately. This combines <a href="https://github.com/vercel/agent-browser">agent-browser CLI (Vercel Labs)</a> with a stealth Chrome extension that patches browser fingerprint vectors at document_start, before any page scripts run. Gets through WAFs that normally stop automated browsing cold.</td></tr>
</table>

### autonomous-agents/

<table>
<tr><td nowrap><a href="autonomous-agents/pi-agent/">pi-agent</a></td><td>Remote coding agents lose state when sessions break or auth expires. This skill covers session lifecycle, RPC control, response extraction, and failure recovery for pi --mode rpc. Keeps agents connected and working reliably across restarts.</td></tr>
</table>

### tools/

<table>
<tr><td nowrap><a href="tools/karakeep/">karakeep</a></td><td>Most bookmarking tools are either SaaS or require heavy setup with databases and config. This is a single Python file with zero dependencies that gives you full CRUD on Karakeep and optionally syncs to Obsidian. Ready to use the second you download it.</td></tr>
<tr><td nowrap><a href="tools/opencode-analyzer/">opencode-analyzer</a></td><td>OpenCode costs add up fast and the CLI doesn't tell you what you're actually spending. This breaks down usage by day, week, and month with comparisons to OpenRouter equivalents. You see budget drift before it becomes a surprise bill.</td></tr>
<tr><td nowrap><a href="tools/email-triage/">email-triage</a></td><td>Gmail piles up noise faster than you can triage it. This splits the problem in two: a zero-LLM archiver that filters noise instantly without spending tokens, then an LLM-powered reviewer that surfaces only the signal. Noise is gone before you even see it.</td></tr>
</table>

### mcp/

<table>
<tr><td nowrap><a href="mcp/stealth-browser/">stealth-browser</a></td><td>Browser automation MCP servers hit the same WAF blocks as everything else. This one wraps <a href="https://github.com/vercel/agent-browser">agent-browser CLI (Vercel Labs)</a> with anti-detection flags and a stealth extension bundled inline with no external dependency. Exposes 10 tools (navigate, click, eval, screenshot, and more) that work through Cloudflare and LinkedIn.</td></tr>
</table>

### extensions/

<table>
<tr><td nowrap><a href="extensions/stealth-extension/">stealth-extension</a></td><td>Most stealth extensions load too late when fingerprint signals are already exposed. This one runs at document_start, before any page script executes, and patches navigator.webdriver, plugins, languages, and Permissions API. By the time the page loads, your browser looks native.</td></tr>
</table>

### themes/

<table>
<tr><td nowrap><a href="themes/hermes-dashboard/">hermes-dashboard</a></td><td>The default Hermes dashboard gets the job done but doesn't suit every environment. Two themes let you pick: Clean WebUI for a bright, minimal workspace or Gruvbox Dark for warm-toned low-light sessions. Drop them in and the dashboard matches your setup.</td></tr>
</table>

### hermes/

<table>
<tr><td nowrap><a href="hermes/pi-agent/">pi-agent</a></td><td>Using pi RPC from Hermes meant manually managing sessions and parsing raw responses. This plugin wraps the full lifecycle (start, send, poll, stop) as native Hermes tools. Tested against the actual pi protocol so it handles edge cases and auth failures cleanly.</td></tr>
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
- Constitution framework by <a href="https://www.youtube.com/watch?v=YfRkj9kmQf0">Allie Miller via Silicon Valley Girl podcast</a> (hosted by Marina Mogilko)
- Browser automation built with <a href="https://github.com/vercel/agent-browser">agent-browser CLI (Vercel Labs)</a>
- File-size-gatekeeper inspired by <a href="https://youtu.be/5ec5mh41oig">Andrew's OpenClaw Blueprint Series</a>

---

Maintained by Dustin "Dusty" Chadwick
