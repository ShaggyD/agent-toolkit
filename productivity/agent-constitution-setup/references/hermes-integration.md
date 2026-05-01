# Hermes Integration: Memory Consolidation & GitHub Publishing

## Memory Consolidation

After building the three docs, the user profile in Hermes will likely be bloated from onboarding Q&A. Audit and consolidate.

### Pattern

1. **Audit the profile:** Fragmented preferences (standup rules split across 3 entries, persona split across 4) are the #1 source of bloat.
2. **Drop onboarding crud:** Entries like "prefers Linux for installation" and "prefers onboarding questions one at a time" are useless post-onboarding.
3. **Merge by category:** One entry for persona/voice, one for communication protocols, one for identity details.
4. **Add doc pointers:** A single entry that lists the three files and tells the agent to load them for planning/prioritizing.

### Target

- 6 or fewer entries
- Below 85% capacity
- Constitution values condensed into 3-5 bullet points in the main identity entry
- File paths accessible for explicit loading

### What consolidation looks like

Typical starting point: 12-15 fragmented entries at ~90% capacity. After consolidation: 5-7 entries at ~80%. Onboarding entries removed. Persona, communication rules, and notification preferences merged into one block. Doc paths added as a single reference entry.

### Pitfalls

- **Don't over-condense.** A single 1,300-char wall of text gets skimmed. Concise bullets with file pointers work better.
- **Memory auto-save must survive.** If your agent platform has an auto-save preference for user-provided information, make sure the consolidation process doesn't override or lose it — otherwise the agent stops learning from corrections.

## GitHub Publishing

To publish skills to a personal GitHub repo from within the Hermes skills directory.

### Workflow

1. `git init` inside `~/.hermes/skills/`
2. Create a `.gitignore` that blocks everything except explicitly added skills:
   ```
   *
   !.gitignore
   !README.md
   !LICENSE
   !productivity/
   productivity/*
   !productivity/agent-constitution-setup/
   !productivity/agent-constitution-setup/**
   ```
3. Add each skill explicitly: `git add productivity/<skill-name>/`
4. Commit and push to remote

### Why whitelist over blacklist

The skills directory contains dozens of skills from the Hermes ecosystem. A blacklist approach fights entropy. The whitelist pattern ensures only your authored skills get committed.

### GH CLI setup

Use `gh repo edit` for metadata (description, topics, homepage). Use `gh api` and `git push` for license files. Commit LICENSE as a file, then set the license template via API for the sidebar badge.

### Attribution lesson

Credit the source (Allie Miller, podcast link, key quote) in the SKILL.md and README — but the repo description is about YOUR collection, not the source's framework. Keep "Framework by..." in the skill body, not the repo about.
