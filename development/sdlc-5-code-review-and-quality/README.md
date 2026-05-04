# SDLC 5: Code Review and Quality

Multi-dimensional code review with quality gates. This skill enforces the **Review** phase of the SDLC — every change gets reviewed before merge, no exceptions.

## Overview

Review covers five axes: correctness, readability & simplicity, architecture, security, and performance. The skill provides a structured review process (understand context → review tests first → review implementation → categorize findings → verify verification), change sizing guidelines (~100 lines target), severity labels (Critical/Nit/Optional/FYI), and dead code hygiene. It also covers multi-model review patterns and handling disagreements.

## Attribution

**Author:** Addy Osmani ([@addyosmani](https://github.com/addyosmani))  
**Source:** [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — MIT licensed  
**Blog Post:** [Agent Skills](https://addyosmani.com/blog/agent-skills/)  

This skill is ported from Addy Osmani's agent-skills collection, adapted with normalized frontmatter and repository conventions. The workflow content is preserved verbatim.

## Use When

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)

## Prerequisites

This skill expects completed implementation from **SDLC 3** (`sdlc-3-incremental-implementation`) with tests from **SDLC 4** (`sdlc-4-test-driven-development`).

## Next Steps

After review passes:
- **SDLC 6** (`sdlc-6-code-simplification`) — simplify if needed before ship
- **SDLC 7** (`sdlc-7-shipping-and-launch`) — deploy to production
