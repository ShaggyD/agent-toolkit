# SDLC 1: Spec-Driven Development

Write a structured specification before writing any code. This skill enforces the **Define** phase of the SDLC — surfacing assumptions, clarifying requirements, and producing a shared source of truth before implementation begins.

## Overview

This skill is the first step in the SDLC pipeline. Before any code is written, a spec must exist covering six core areas: objective, commands, project structure, code style, testing strategy, and boundaries. The workflow is gated — each phase (Specify → Plan → Tasks → Implement) requires human review before advancing.

## Attribution

**Author:** Addy Osmani ([@addyosmani](https://github.com/addyosmani))  
**Source:** [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — MIT licensed  
**Blog Post:** [Agent Skills](https://addyosmani.com/blog/agent-skills/)  

This skill is ported from Addy Osmani's agent-skills collection, adapted with normalized frontmatter and repository conventions. The workflow content is preserved verbatim.

## Use When

- Starting a new project or feature
- Requirements are ambiguous or incomplete
- The change touches multiple files or modules
- You're about to make an architectural decision
- The task would take more than 30 minutes to implement

## Next Steps

After this skill completes, proceed to:
- **SDLC 2** (`sdlc-2-planning-and-task-breakdown`) — break the spec into implementable tasks
- **SDLC 3** (`sdlc-3-incremental-implementation`) — implement in thin vertical slices
- **SDLC 4** (`sdlc-4-test-driven-development`) — write tests before code

## Related Skills

- [file-size-gatekeeper](../../productivity/file-size-gatekeeper/) — keeps skill files under the 18K character threshold
