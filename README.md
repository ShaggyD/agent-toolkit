# AGENT SKILLS

A collection of portable skill documents for AI agents — Hermes, Claude, ChatGPT, Codex, and others. Each skill gives an agent deep context about a specific task, workflow, or domain so it doesn't have to figure things out from scratch.

Skills are **provider-agnostic.** Export from one agent platform, import into another, they just work.

---

## Skills

### [agent-constitution-setup](productivity/agent-constitution-setup/)

Build the three essential onboarding docs that give any AI agent context about who you are and how you operate.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Framework** | [Allie Miller](https://www.youtube.com/watch?v=YfRkj9kmQf0) — Silicon Valley Girl podcast |
| **Category** | Productivity / Agent Onboarding |
| **Files** | 9 (SKILL.md + 5 reference docs + 3 templates) |

**What's inside:**
- `SKILL.md` — instructions for building all three docs
- `templates/generic-constitution.md` — blank template for values, principles, decision framework
- `templates/generic-goals.md` — blank template for annual/quarterly/monthly goals
- `templates/generic-strategy.md` — blank template for business positioning
- `references/example-dusty-*.md` — real-world examples from the author's own setup
- `references/hermes-integration.md` — how to wire into Hermes Agent specifically
- `references/agent-service-standards.md` — quality standards for agent interactions

**The three docs:**
1. **Constitution** — timeless personal values, principles, communication style, decision framework
2. **Goals** — annual/quarterly targets, habits to build, measurable outcomes
3. **Strategy** — business positioning, who you serve, value proposition

---

### [karakeep-obsidian-sync](productivity/karakeep-obsidian-sync/)

Full CRUD CLI for [Karakeep](https://github.com/karakeep-app/karakeep) (self-hosted bookmarking) with optional Obsidian vault sync.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Category** | Productivity / Bookmarking |
| **Files** | 6 (binary CLI + SKILL.md + 3 reference docs + README) |

**What's inside:**
- `kk` — standalone binary (Python, zero external deps) — just copy to `~/.local/bin/`
- `SKILL.md` — full command reference, configuration, and AI agent instructions
- `references/karakeep-api.md` — API endpoint reference for the Karakeep server
- `references/uv-adhoc-deps.md` — dependency management notes
- `references/vault-path-inference.md` — how the tool finds your vault path
- `README.md` — quick-start guide

**Usage:**
```bash
cp kk ~/.local/bin/
kk login https://hoarder.example.com your_api_key
kk sync
```

Synced bookmarks land in your Obsidian vault at `003_Resources/Bookmarks/` with an index dashboard, daily note cross-refs, and backlinks.

---

### [macos-task-scheduler](productivity/macos-task-scheduler/)

Schedule recurring tasks on macOS using launchd plists. Covers configuration, scheduling syntax, and task lifecycle.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Category** | Productivity / Automation |
| **Files** | 1 (SKILL.md) |

---

### [hermes-dashboard-themes](productivity/hermes-dashboard-themes/)

Two hand-crafted themes for the Hermes Agent web dashboard: **Clean WebUI** (white canvas, blue accents) and **Gruvbox Dark** (warm earthy dark mode). Both include readability-focused improvements over the defaults — visible borders, sidebar background, proper heading hierarchy, and wrapping Kanban columns.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Category** | Productivity / Dashboard |
| **Files** | 4 (README.md + screenshot + 2 reference YAMLs) |

**Installation:**
```bash
cp references/*.yaml ~/.hermes/dashboard-themes/
# Reload dashboard, pick theme from bottom-left picker
```

---

### [opencode-analyzer](productivity/opencode-analyzer/)

OpenCode cost analyzer with detailed daily/weekly/monthly breakdowns. Shows actual spending vs OpenRouter equivalents, plus same-token model comparisons.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Category** | Productivity / Analysis |
| **Files** | 4 (SKILL.md + binary CLI + plugins/README.md) |
|---

### [email-triage-system](productivity/email-triage-system/)

Two-layer Gmail triage pipeline — zero-LLM noise archiving (Janitor) + LLM-powered daily review (Reviewer) — keeps your inbox clean with minimal config.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Category** | Productivity / Email Management |
| **Files** | 10 (janitor.py + SKILL.md + README.md + 4 templates + 3 reference docs) |

**What's inside:**
- `janitor.py` — zero-LLM Gmail noise archiving CLI script
- `SKILL.md` — full system architecture, setup, and usage
- `templates/config.yaml` — externalized Janitor configuration
- `templates/noise-senders.yaml` — noise-sender patterns (promotions, newsletters, social, services, security)
- `templates/safe-senders.yaml` — safe-sender allowlist template
- `templates/reviewer-soul.md` — Reviewer agent profile template
- `references/gmail-api-setup.md` — OAuth setup for Gmail API
- `references/label-conventions.md` — label hierarchy conventions
- `references/troubleshooting.md` — common issues and fixes

The system requires only Gmail API credentials and a cron entry. No database, no server, no LLM API keys for the Janitor layer.

---

### [file-size-gatekeeper](productivity/file-size-gatekeeper/)

Prevent the "18,000 character trap" — silent context-window degradation caused by bloated skill files, config, and reference docs.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Inspired by** | [Andrew's OpenClaw Blueprint Series](https://youtu.be/5ec5mh41oig) — Video 2 of 8 |
| **Category** | Productivity / Housekeeping |
| **Files** | 1 (SKILL.md) |

**The problem:** Large files silently consume context window space. When a SKILL.md exceeds 17,000 characters, it starts crowding out conversation and tool outputs. The agent doesn't crash — it just gets *gradually worse* until you notice it's "ignoring" instructions buried 12k chars deep.

**The solution:** Enforce file size discipline with clear thresholds:

| Threshold | Action |
|---|---|
| **< 10,000 chars** | ✅ Safe |
| **10,000 – 17,000 chars** | 👀 Caution — review on next edit |
| **> 17,000 chars** | ⚠️ Flag for condense or split |
| **> 18,000 chars** | 🚩 Must condense or split |

**What it monitors:** `SKILL.md` files, `.env`, `SOUL.md`, `config.yaml`, and all reference docs.

The skill includes an on-demand audit command, a condensing workflow, and an optional nightly cron job.

---

## Software Development Skills

### [browser-automation](software-development/browser-automation/)

Browser automation via agent-browser CLI (Vercel Labs) with stealth anti-detection extension. Headless Chrome navigation with Cloudflare/WAF bypass, snapshot-ref interaction, JavaScript eval extraction, and batch flows.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Category** | Software Development / Browser Automation |
| **Files** | 9 (SKILL.md + 4 reference docs + stealth extension with 2 files) |

**What's inside:**
- `SKILL.md` — full command reference, session management, Quick Start patterns, Cloudflare/WAF bypass with stealth extension
- `assets/stealth-extension/` — Chrome extension that patches `navigator.webdriver`, plugins, and languages at page start to bypass bot detection
- `references/waf-protected-site-scraping.md` — extraction patterns for AI pricing pages, SaaS portals, e-commerce, and web app testing
- `references/employer-direct-job-scraping.md` — ATS portal patterns (BambooHR, Paylocity, Workday, ADP, Greenhouse, Lever)
- `references/structured-data-extraction.md` — extracting JSON-LD, tables, and structured data from JS-rendered pages
- `references/search-snippet-extraction.md` — Google search snippet fallback for CAPTCHA-blocked sites

---

## Autonomous AI Agent Skills

### [pi-agent](autonomous-ai-agents/pi-agent/)

Run Pi coding-agent workflows through RPC with persistent, resumable sessions and Hermes-native stateful control patterns.

| | |
|---|---|
| **Author** | Dustin Chadwick ([@ShaggyD](https://github.com/ShaggyD)) |
| **Category** | Autonomous AI Agents / RPC Orchestration |
| **Files** | 9 (SKILL.md + 4 reference docs + 1 script + 2 tool files + 1 test) |

**What's inside:**
- `SKILL.md` — operational workflow and action surface for stateful Pi RPC control
- `references/hermes-stateful-tool-integration.md` — Hermes tool wiring, lifecycle patterns, restart semantics
- `references/auth-and-extension-troubleshooting.md` — auth + startup troubleshooting playbook
- `references/response-extraction.md` — extracting text responses from RPC turn events
- `references/rpc-pitfalls.md` — common failure modes and fast triage
- `scripts/pi_agent_client.py` — minimal CLI RPC helper script
- `tools/pi_agent_tool.py` — Hermes-native `pi_agent` tool (🤖) for stateful Pi RPC sessions
- `tools/test_pi_agent_tool.py` — pytest suite for the tool

---

## Development / SDLC Skills

### SDLC Core Pipeline (ported)

These seven skills are adapted from Addy Osmani's [agent-skills](https://github.com/addyosmani/agent-skills) project (MIT), described in his [Agent Skills](https://addyosmani.com/blog/agent-skills/) blog post, and organized with an ordered `sdlc-<n>-` prefix.

**Default policy:** Use **SDLC 1–6 as required phases when those skills exist in the environment**. Treat **SDLC 7 as optional**, based on release/deployment scope.

| Step | Skill | Purpose |
|---|---|---|
| 1 | [sdlc-1-spec-driven-development](development/sdlc-1-spec-driven-development/) | Define objective, assumptions, success criteria, and boundaries before coding |
| 2 | [sdlc-2-planning-and-task-breakdown](development/sdlc-2-planning-and-task-breakdown/) | Convert specs into dependency-aware plans and actionable tasks |
| 3 | [sdlc-3-incremental-implementation](development/sdlc-3-incremental-implementation/) | Build in thin, testable vertical slices |
| 4 | [sdlc-4-test-driven-development](development/sdlc-4-test-driven-development/) | Prove behavior with Red-Green-Refactor and reproduction-first bug fixes |
| 5 | [sdlc-5-code-review-and-quality](development/sdlc-5-code-review-and-quality/) | Apply five-axis review gates before merge |
| 6 | [sdlc-6-code-simplification](development/sdlc-6-code-simplification/) | Reduce complexity without behavior changes |
| 7 (Optional) | [sdlc-7-shipping-and-launch](development/sdlc-7-shipping-and-launch/) | Launch safely with rollout, monitoring, and rollback discipline |

Each SDLC skill includes:
- `SKILL.md` — the workflow
- `README.md` — usage notes, prerequisites, and attribution

### Shared References (imported)

The SDLC skills use shared checklists imported into [references/](references/):
- [security-checklist.md](references/security-checklist.md)
- [performance-checklist.md](references/performance-checklist.md)
- [accessibility-checklist.md](references/accessibility-checklist.md)
- [testing-patterns.md](references/testing-patterns.md)

---

## Repository Structure

```
AGENT_SKILLS/
├── README.md                    ← you are here
├── LICENSE                      ← MIT
├── .gitignore                   ← allowlist pattern (track only published skills)
├── productivity/
│   ├── agent-constitution-setup/
│   ├── karakeep-obsidian-sync/
│   ├── file-size-gatekeeper/
│   ├── macos-task-scheduler/
│   ├── opencode-analyzer/
│   ├── email-triage-system/
│   └── hermes-dashboard-themes/
├── software-development/
│   └── browser-automation/
├── development/
│   ├── sdlc-1-spec-driven-development/
│   ├── sdlc-2-planning-and-task-breakdown/
│   ├── sdlc-3-incremental-implementation/
│   ├── sdlc-4-test-driven-development/
│   ├── sdlc-5-code-review-and-quality/
│   ├── sdlc-6-code-simplification/
│   └── sdlc-7-shipping-and-launch/
├── autonomous-ai-agents/
│   └── pi-agent/
└── references/
    ├── security-checklist.md
    ├── performance-checklist.md
    ├── accessibility-checklist.md
    └── testing-patterns.md
```

**Why the `.gitignore` uses an allowlist:** The repository root doubles as a Hermes Agent skills directory. Hermes's built-in skills from the [Skills Hub](https://agentskills.io) are present on disk but are not part of this repo. Only explicitly published skills are tracked in git.

---

## Usage

Clone into your agent's skills directory:

```bash
git clone git@github.com:ShaggyD/AGENT_SKILLS.git ~/.hermes/skills
```

Then load a skill by name:

```bash
hermes -s browser-automation
# or in-session:  /skill browser-automation
```

For non-Hermes agents, read the `SKILL.md` file directly and feed it as system context.

---

## License

MIT — use freely, adapt openly, attribute where meaningful.

**Attribution notes:**
- [agent-constitution-setup](productivity/agent-constitution-setup/) builds on [Allie Miller's framework](https://www.youtube.com/watch?v=YfRkj9kmQf0)
- [file-size-gatekeeper](productivity/file-size-gatekeeper/) is inspired by [Andrew's OpenClaw Blueprint Series](https://youtu.be/5ec5mh41oig)
- [macos-task-scheduler](productivity/macos-task-scheduler/)
- [opencode-analyzer](productivity/opencode-analyzer/) is developed from the [AGENTIC_SKILLS](https://github.com/ShaggyD/AGENTIC_SKILLS) repository
- [browser-automation](software-development/browser-automation/) — built and tested with agent-browser CLI (Vercel Labs)
- [autonomous-ai-agents/pi-agent](autonomous-ai-agents/pi-agent/) documents Pi RPC orchestration patterns and Hermes-native stateful tool workflows
- [development/sdlc-*](development/) skills are inspired by [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT) and [Agent Skills](https://addyosmani.com/blog/agent-skills/), then modified to match Dustin Chadwick's personal engineering principles for depth, review discipline, and execution preferences
- [references/*](references/) checklists are imported from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)

---

*Maintained by [Dustin "Dusty" Chadwick](https://github.com/ShaggyD)*
