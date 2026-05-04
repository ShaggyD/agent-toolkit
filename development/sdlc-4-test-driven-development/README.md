# SDLC 4: Test-Driven Development

Write a failing test before writing the code that makes it pass. This skill enforces the **Verify** phase of the SDLC — proving code works through the Red-Green-Refactor cycle.

## Overview

Tests are proof — "seems right" is not done. This skill covers the full TDD cycle (Red → Green → Refactor), the Prove-It Pattern for bug fixes (reproduce with a test before fixing), the test pyramid (80/15/5 unit/integration/e2e), the Beyoncé Rule, DAMP over DRY in tests, and state-based over interaction-based testing. It also covers browser testing with DevTools and subagent delegation for complex bug reproductions.

## Attribution

**Author:** Addy Osmani ([@addyosmani](https://github.com/addyosmani))  
**Source:** [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — MIT licensed  
**Blog Post:** [Agent Skills](https://addyosmani.com/blog/agent-skills/)  

This skill is ported from Addy Osmani's agent-skills collection, adapted with normalized frontmatter and repository conventions. The workflow content is preserved verbatim.

## Use When

- Implementing any new logic or behavior
- Fixing any bug (always start with a reproduction test)
- Modifying existing functionality
- Adding edge case handling
- Any change that could break existing behavior

## Prerequisites

This skill is typically used alongside **SDLC 3** (`sdlc-3-incremental-implementation`) — each increment should include its tests.

## Next Steps

After tests pass:
- **SDLC 5** (`sdlc-5-code-review-and-quality`) — review before merging
- **SDLC 6** (`sdlc-6-code-simplification`) — clean up after tests are green
