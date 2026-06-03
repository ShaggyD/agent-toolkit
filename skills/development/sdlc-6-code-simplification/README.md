# SDLC 6: Code Simplification

Simplify code by reducing complexity while preserving exact behavior. This skill sits across the SDLC as a refinement and quality gate — applying after implementation and review to ensure code is as clear as it is correct.

## Overview

The goal is not fewer lines — it's code that is easier to read, understand, modify, and debug. This skill covers five principles (preserve behavior exactly, follow project conventions, prefer clarity over cleverness, maintain balance, scope to what changed), the full simplification process (Chesterton's Fence → identify opportunities → apply incrementally → verify), and language-specific guidance for TypeScript, Python, and React/JSX.

## Attribution

**Author:** Addy Osmani ([@addyosmani](https://github.com/addyosmani))  
**Source:** [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — MIT licensed  
**Blog Post:** [Agent Skills](https://addyosmani.com/blog/agent-skills/)  

This skill is ported from Addy Osmani's agent-skills collection, adapted with normalized frontmatter and repository conventions. Inspired by open-source code simplification workflows.

## Use When

- After a feature is working and tests pass, but the implementation feels heavier than it needs to be
- During code review when readability or complexity issues are flagged
- When you encounter deeply nested logic, long functions, or unclear names
- When refactoring code written under time pressure

## Related Skills

- [file-size-gatekeeper](../../productivity/file-size-gatekeeper/) — complementary discipline for keeping files under the 18K threshold
