# SDLC 7 (Optional): Shipping and Launch

Ship with confidence — deploy safely with monitoring, rollback plans, and clear success criteria. This optional skill covers the **Ship** phase of the SDLC when release/production discipline is needed.

## Overview

Every launch should be reversible, observable, and incremental. This skill provides a comprehensive pre-launch checklist (code quality, security, performance, accessibility, infrastructure, documentation), feature flag strategy with lifecycle management, staged rollout with decision thresholds, monitoring and observability guidance, and rollback planning.

## Attribution

**Author:** Addy Osmani ([@addyosmani](https://github.com/addyosmani))  
**Source:** [github.com/addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — MIT licensed  
**Blog Post:** [Agent Skills](https://addyosmani.com/blog/agent-skills/)  

This skill is ported from Addy Osmani's agent-skills collection, adapted with normalized frontmatter and repository conventions. The workflow content is preserved verbatim.

## Use When

- Deploying a feature to production for the first time
- Releasing a significant change to users
- Migrating data or infrastructure
- Opening a beta or early access program
- Any deployment that carries risk (all of them)

## Prerequisites

Use this optional skill when preparing for release/deploy. It expects prior SDLC phases to be complete when applicable:
- **SDLC 1** (`sdlc-1-spec-driven-development`) — spec exists
- **SDLC 2** (`sdlc-2-planning-and-task-breakdown`) — plan exists
- **SDLC 3** (`sdlc-3-incremental-implementation`) — code is implemented
- **SDLC 4** (`sdlc-4-test-driven-development`) — tests pass
- **SDLC 5** (`sdlc-5-code-review-and-quality`) — review passed
