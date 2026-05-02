# AGENT SKILLS

A collection of reusable AI agent skills — portable Markdown documents that give AI agents (Claude, Hermes, ChatGPT, Codex, and others) deep context about who you are and how to operate.

Skills are provider-agnostic by design. Export them from one agent platform and import into another without rewriting.

**Author:** Dustin "Dusty" Chadwick ([@ShaggyD](https://github.com/ShaggyD))

## Skills

| Skill | Description |
|-------|-------------|
| [agent-constitution-setup](productivity/agent-constitution-setup/) | Build three essential docs for AI agent context: personal constitution, goals, and business strategy. Framework by [Allie Miller](https://www.youtube.com/watch?v=YfRkj9kmQf0). |
|| [karakeep-obsidian-sync](productivity/karakeep-obsidian-sync/) | Full CRUD CLI for Karakeep (self-hosted bookmarking). All commands standalone — Obsidian vault sync is optional. By [Dustin Chadwick](https://github.com/ShaggyD). |
|| [file-size-gatekeeper](productivity/file-size-gatekeeper/) | Prevent silent context-window pressure and the "18,000 character trap" by enforcing file size discipline. Inspired by [Andrew's OpenClaw Blueprint](https://youtu.be/5ec5mh41oig) (Video 2 of 8). |

## What Makes a Good Skill?

A skill is a folder containing:

- `SKILL.md` — instructions the agent loads at runtime (trigger conditions, step-by-step workflow, pitfalls)
- `templates/` — example files the agent can learn from or the user can copy
- `references/` — supporting docs the agent can pull in as needed
- `scripts/` — helper scripts the agent can execute

Skills accumulate over time. Each one represents something the agent learned, solved, or got corrected on — turned into a repeatable procedure.

## Usage

Clone into your agent's skills directory. For Hermes Agent:

```bash
git clone git@github.com:ShaggyD/AGENT_SKILLS.git ~/.hermes/skills-custom
```

Then import directly or reference from your agent's memory.

## License

MIT
