---
name: agent-constitution-setup
description: "Build three essential docs for AI agent context: personal constitution, goals, and business strategy. Based on Allie Miller's framework."
version: 1.0.0
author: Dusty + Capricorn
license: MIT
metadata:
  hermes:
    tags: [agent-setup, onboarding, constitution, productivity, personalization]
    source: "Allie Miller on Silicon Valley Girl with Marina Mogilko — https://www.youtube.com/watch?v=YfRkj9kmQf0"
    related_skills: [hermes-agent, incremental-onboarding]
---

# Agent Constitution Setup

Build three documents that give AI agents deep context about who you are, where you're going, and what you're building. Framework developed by AI advisor Allie Miller: without these files, every AI interaction starts from a blank slate. With them, the agent operates from your actual context.

## The Three Files

### 1. Personal Constitution (timeless)
**What it is:** Your core values, decision-making framework, personality, and operating principles. Not tied to any year or week — this is the "who you are at your core" doc.

**Why it matters:** Without it, the agent has no compass for how you make decisions, what tradeoffs you'd make, or how to communicate with you. Every response is generic instead of *you*.

**How to build it:**
- Use scenarios, not direct questions. Give the user situations and ask their gut reaction. Examples: shipping imperfect work, pushing back on bad ideas, handling credit, deep work interruptions.
- Cross-reference with personality test results if available (MBTI, Big Five, Enneagram). Look for tensions between traits — the edges are where the constitution gets sharp.
- Include both strengths AND acknowledged weaknesses. A constitution that only flatters is useless.
- Iterate: draft, ask what doesn't sit right, rewrite. The user should feel slightly exposed — that's how you know it's real.

**Format:** Plain markdown, one heading. Saved to `~/.hermes/references/constitution.md`.

### 2. Goals Document (time-bound)
**What it is:** Annual/quarterly/monthly goals, habits to build, habits to kick, specific inputs/outputs to manage.

**Why it matters:** Turns the agent from a dumb tool into something that proactively aligns with your trajectory. At minimum, the agent should know what you're optimizing for and what you're trying to change.

**How to build it:**
- Ask one category at a time: professional wins, personal routines, energy leaks.
- Focus on feelings first ("by December I want to feel like I finally ____"), then translate to specifics.
- Keep it lean. If it's longer than a screen, it won't get used.

**Format:** Plain markdown with sections. Saved to `~/.hermes/references/goals-YYYY.md`.

### 3. Core Business Strategy (contextual)
**What it is:** What your business is, who you serve, who you don't serve, value proposition, and — critically — the things NOT on your website or LinkedIn. The failed podcast, the org that retreats to safety, the patterns that explain decisions.

**Why it matters:** Without it, the agent treats everything as equally important. With it, the agent knows what to say no to and why certain things failed before.

**How to build it:**
- Separate day job from side projects — different strategies, different audiences.
- Ask directly: "What's something true about this that you'd never put on a public slide deck?" That answer IS the strategy doc.
- Capture constraints, not just aspirations. Real strategy lives in the friction.

**Format:** Plain markdown with sections. Saved to `~/.hermes/references/business-strategy.md`.

## Integration with Hermes

After building all three docs:

1. **Condense the constitution** into 3-5 bullet points and save to memory so it's injected into every turn.
2. **Reference the files** from memory: `Reference docs: ~/.hermes/references/constitution.md, ... Load these for context when planning, prioritizing, or making recommendations.`
3. **Consolidate user profile** — merge fragmented onboarding entries into denser blocks. The goal is <85% memory capacity with all three docs referenced.
4. **Load the docs explicitly** during planning sessions, weekly reviews, or any task where alignment matters.

## Interviewing Tips

- **One question at a time.** Don't dump categories. Let each answer breathe.
- **Scenarios beat abstractions.** "Here's a situation, what do you do?" surfaces real values faster than "what are your values?"
- **Push back on the draft.** If the user says "that doesn't sit right," dig into why. The rewrites are where the real self-knowledge emerges.
- **Save drafts.** Users will want to return and refine. These are living documents, not one-and-done.

## Pitfalls

- **Don't over-consolidate memory.** Cramming everything into one 1,300-char entry creates a wall of text the model skims. Concise bullets with file pointers work better.
- **Don't interview like a form.** If the user gives you a personality test result, use it. Cross-reference traits against what you've observed.
- **Constitutions are NOT goals.** If an entry could reasonably change next year, it belongs in the goals doc, not the constitution.
- **The third doc hurts.** If the business strategy doc is just marketing copy, you didn't go deep enough. The real strategy is what you'd tell a trusted advisor, not a customer.

## Attribution

**Framework by Allie Miller** — AI advisor to OpenAI, Google, Anthropic, and Fortune 500 leaders. One of the top voices in enterprise AI.

**Source:** ["Silicon Valley Girl" with Marina Mogilko](https://www.youtube.com/watch?v=YfRkj9kmQf0) — Allie Miller on building proactive AI agents, skills, and the three essential files every agent user needs.

**Key quote:** "Three documents that I would start with: the first is your personal constitution. This has nothing to do with what year it is, what you did last week — everything about this document is just who you are at your core."

**Allie's links:**
- YouTube interview: https://www.youtube.com/watch?v=YfRkj9kmQf0
- Silicon Valley Girl (Marina Mogilko): https://www.youtube.com/@SiliconValleyGirl
