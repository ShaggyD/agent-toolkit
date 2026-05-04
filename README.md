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

### [file-size-gatekeeper](productivity/file-size-gatekeeper/)

Prevent the "18,000 character trap" — silent context-window degradation caused by bloated skill files, config, and reference docs.

| | |
|---|---|
| **Author** | Capricorn (via Dustin Chadwick) |
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
│   └── file-size-gatekeeper/
├── development/
│   ├── sdlc-1-spec-driven-development/
│   ├── sdlc-2-planning-and-task-breakdown/
│   ├── sdlc-3-incremental-implementation/
│   ├── sdlc-4-test-driven-development/
│   ├── sdlc-5-code-review-and-quality/
│   ├── sdlc-6-code-simplification/
│   └── sdlc-7-shipping-and-launch/
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
hermes -s agent-constitution-setup
# or in-session:  /skill agent-constitution-setup
```

For non-Hermes agents, read the `SKILL.md` file directly and feed it as system context.

---

## License

MIT — use freely, adapt openly, attribute where meaningful.

**Attribution notes:**
- [agent-constitution-setup](productivity/agent-constitution-setup/) builds on [Allie Miller's framework](https://www.youtube.com/watch?v=YfRkj9kmQf0)
- [file-size-gatekeeper](productivity/file-size-gatekeeper/) is inspired by [Andrew's OpenClaw Blueprint Series](https://youtu.be/5ec5mh41oig)
- [development/sdlc-*](development/) skills are inspired by [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT) and [Agent Skills](https://addyosmani.com/blog/agent-skills/), then modified to match Dustin Chadwick's personal engineering principles for depth, review discipline, and execution preferences
- [references/*](references/) checklists are imported from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT)

---

*Maintained by [Dustin "Dusty" Chadwick](https://github.com/ShaggyD)*
