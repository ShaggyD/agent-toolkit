# SDLC 3: Incremental Implementation

Build in thin vertical slices — implement one piece, test it, verify it, then expand. This skill enforces the **Build** phase of the SDLC, ensuring each increment leaves the system in a working, testable state.

## Overview

Avoid implementing an entire feature in one pass. Instead, use vertical slicing (one complete path through the stack per slice), contract-first slicing, or risk-first slicing. Each increment follows the cycle: Implement → Test → Verify → Commit → Next slice. Key rules include simplicity first, scope discipline, one thing at a time, feature flags for incomplete work, and rollback-friendly changes.

## Attribution

**Author:** Addy Osmani ([@addyosmani](https://github.com/addyosmani))  
**Source:** [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — MIT licensed  
**Blog Post:** [Agent Skills](https://addyosmani.com/blog/agent-skills/)  

This skill is ported from Addy Osmani's agent-skills collection, adapted with normalized frontmatter and repository conventions. The workflow content is preserved verbatim.

## Use When

- Implementing any multi-file change
- Building a new feature from a task breakdown
- Refactoring existing code
- Any time you're tempted to write more than ~100 lines before testing

## Prerequisites

This skill expects a completed task breakdown from **SDLC 2** (`sdlc-2-planning-and-task-breakdown`).

## Next Steps

After each increment, run:
- **SDLC 4** (`sdlc-4-test-driven-development`) — TDD cycle for each slice
- **SDLC 5** (`sdlc-5-code-review-and-quality`) — review before merging
