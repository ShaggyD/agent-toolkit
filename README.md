# agent-toolkit

Skills, tools, MCP servers, browser extensions, and UI themes for AI agents. Built for developers who need practical, tested components instead of hello-world examples. Provider-agnostic except for the hermes/ directory.

All items follow a simple format: the problem that needed solving, what was built, and the outcome. Detail lives in each artifact's own docs.

---

## productivity/

Daily agent workflows.

#### [agent-constitution-setup](productivity/agent-constitution-setup/)
**Problem:** Agents drift when they don't know who you are or what you value.

**Built:** Three documents (constitution, goals, strategy) based on [Allie Miller's framework from the Silicon Valley Girl podcast](https://www.youtube.com/watch?v=YfRkj9kmQf0) (hosted by Marina Mogilko).

**Outcome:** The agent acts consistent with your intent instead of guessing.

#### [file-size-gatekeeper](productivity/file-size-gatekeeper/)
**Problem:** Files grow unchecked and silently degrade agent performance until you notice instructions being ignored.

**Built:** A skill that enforces file size discipline, audits bloated files, and encodes four techniques from [Andrew's OpenClaw Blueprint video](https://youtu.be/5ec5mh41oig) on the 18,000 character trap.

**Outcome:** Your agent actually reads every instruction because nothing gets truncated or pushed out of context.

#### [macos-task-scheduler](productivity/macos-task-scheduler/)
**Problem:** Setting up recurring tasks on macOS means wrestling with launchd plist syntax and remembering the right load/unload commands.

**Built:** A skill that handles launchd configuration, scheduling syntax, and task lifecycle (load, unload, start, stop) so you don't have to.

**Outcome:** Schedule scripts without touching XML or digging through man pages.

---

## development/

SDLC pipeline in 7 ordered phases.

#### [sdlc-1-spec-driven-development](development/sdlc-1-spec-driven-development/)
**Problem:** Most bugs come from unclear requirements.

**Built:** A phase that forces you to write down objective, assumptions, and boundaries before any code gets written.

**Outcome:** Catches ambiguity early when it's cheap to fix.

#### [sdlc-2-planning-and-task-breakdown](development/sdlc-2-planning-and-task-breakdown/)
**Problem:** A spec without a plan leads to messy execution.

**Built:** Breaks specs into ordered, dependency-aware tasks.

**Outcome:** Nothing gets built before its prerequisites are ready.

#### [sdlc-3-incremental-implementation](development/sdlc-3-incremental-implementation/)
**Problem:** Big bang merges break things and hide who broke what.

**Built:** Thin, testable vertical slices.

**Outcome:** Each piece works before the next one starts.

#### [sdlc-4-test-driven-development](development/sdlc-4-test-driven-development/)
**Problem:** Writing tests after the code means tests that pass against broken logic.

**Built:** Red-Green-Refactor and reproduction-first bug fixes.

**Outcome:** The test suite stays honest and the code stays correct.

#### [sdlc-5-code-review-and-quality](development/sdlc-5-code-review-and-quality/)
**Problem:** Merging without review lets bad patterns compound.

**Built:** Five-axis review gates (correctness, security, performance, style, test coverage).

**Outcome:** Catches what the author missed.

#### [sdlc-6-code-simplification](development/sdlc-6-code-simplification/)
**Problem:** Code that works but is hard to understand is technical debt waiting to compound.

**Built:** Systematic complexity reduction without behavior changes.

**Outcome:** The next person can reason about the code.

#### [sdlc-7-shipping-and-launch](development/sdlc-7-shipping-and-launch/)
**Problem:** A clean merge doesn't mean a clean deploy.

**Built:** Rollout, monitoring, and rollback discipline.

**Outcome:** The launch doesn't become the incident.

---

## browser/

#### [browser-automation](browser/browser-automation/)
**Problem:** Standard headless browsers get blocked by Cloudflare and LinkedIn immediately.

**Built:** [agent-browser CLI (Vercel Labs)](https://github.com/vercel/agent-browser) combined with a stealth Chrome extension that patches browser fingerprint vectors at document_start, before any page scripts run.

**Outcome:** Gets through WAFs that normally stop automated browsing cold.

---

## autonomous-agents/

#### [pi-agent](autonomous-agents/pi-agent/)
**Problem:** Remote coding agents lose state when sessions break or auth expires.

**Built:** A skill covering session lifecycle, RPC control, response extraction, and failure recovery for pi --mode rpc.

**Outcome:** Your coding agent survives terminal restarts, auth reconnects, and network blips without losing context.

---

## tools/

Standalone CLIs, each with their own docs.

#### [karakeep](tools/karakeep/)
**Problem:** Most bookmarking tools are either SaaS or require heavy setup with databases and config.

**Built:** A single Python file with zero dependencies that gives you full CRUD on Karakeep and optionally syncs to Obsidian.

**Outcome:** Ready to use the second you download it.

#### [opencode-analyzer](tools/opencode-analyzer/)
**Problem:** OpenCode costs add up fast and the CLI doesn't tell you what you're actually spending.

**Built:** Usage breakdowns by day, week, and month with comparisons to OpenRouter equivalents.

**Outcome:** You see budget drift before it becomes a surprise bill.

#### [email-triage](tools/email-triage/)
**Problem:** Gmail piles up noise faster than you can triage it.

**Built:** A two-layer pipeline: a zero-LLM archiver that filters noise instantly without spending tokens, and an LLM-powered reviewer that surfaces only the signal.

**Outcome:** Noise is gone before you even see it.

---

## mcp/

MCP servers for agent platforms.

#### [stealth-browser](mcp/stealth-browser/)
**Problem:** Browser automation MCP servers hit the same WAF blocks as everything else.

**Built:** Wraps [agent-browser CLI (Vercel Labs)](https://github.com/vercel/agent-browser) with anti-detection flags and a stealth extension bundled inline with no external dependency. Exposes 10 tools (navigate, click, eval, screenshot, and more).

**Outcome:** Works through Cloudflare and LinkedIn from any MCP-compatible agent.

---

## extensions/

#### [stealth-extension](extensions/stealth-extension/)
**Problem:** Most stealth extensions load too late when fingerprint signals are already exposed.

**Built:** A Manifest V3 extension that runs at document_start, before any page script executes, and patches navigator.webdriver, plugins, languages, and Permissions API.

**Outcome:** By the time the page loads, your browser looks native.

---

## themes/

#### [hermes-dashboard](themes/hermes-dashboard/)
**Problem:** Staring at a bright dashboard in a dark room gets old fast.

**Built:** Two themes: Clean WebUI for a bright, minimal workspace and Gruvbox Dark for warm-toned low-light sessions.

**Outcome:** Drop them in and the dashboard matches your environment instead of fighting it.

---

## hermes/

Platform-specific tooling for Hermes Agent.

#### [pi-agent](hermes/pi-agent/)
**Problem:** Using pi RPC from Hermes meant manually managing sessions and parsing raw responses.

**Built:** A plugin that wraps the full lifecycle (start, send, poll, stop) as native Hermes tools, tested against the actual pi protocol.

**Outcome:** Handles edge cases and auth failures cleanly without manual session wrangling.

---

## references/

Shared checklists.

- [security-checklist.md](references/security-checklist.md)
- [performance-checklist.md](references/performance-checklist.md)
- [accessibility-checklist.md](references/accessibility-checklist.md)
- [testing-patterns.md](references/testing-patterns.md)

---

## Usage

```bash
git clone git@github.com:ShaggyD/agent-toolkit.git ~/agent-toolkit

# For Hermes users: symlink for skill discovery
ln -sf ~/agent-toolkit ~/.hermes/skills

# Load a skill (hermes -s <name> or /skill <name>)
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

- SDLC skills and shared checklists adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)
- Constitution framework by [Allie Miller via Silicon Valley Girl podcast](https://www.youtube.com/watch?v=YfRkj9kmQf0) (hosted by Marina Mogilko)
- Browser automation built with [agent-browser CLI (Vercel Labs)](https://github.com/vercel/agent-browser)
- File-size-gatekeeper inspired by [Andrew's OpenClaw Blueprint Series](https://youtu.be/5ec5mh41oig)

---

Maintained by Dustin "Dusty" Chadwick
