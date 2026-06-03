# Using Pi Agent for Git Commit Organization

When pi agent is active in a repo and there are uncommitted changes, use it to organize commits into logical blocks rather than doing it manually.

## Pattern

```
send → wait(turn_end) → poll(offset=latest, limit=final_output)
```

Don't send one file at a time. Give pi agent the full picture:

1. **Describe what changed** — summarize the diff categories (config changes, test removals, test updates, etc.)
2. **Specify the commit plan** — list the logical commit blocks in order
3. **Let pi execute** — it will review the diff, stage files, and commit each block sequentially
4. **Handle the straggler** — package-lock.json changes often need a separate final commit

## Example prompt shape

```
Review the current git diff. Organize the changes into logical commit blocks:

1. [Category 1] — files: [paths] — message: "..."
2. [Category 2] — files: [paths] — message: "..."
3. [Category 3] — files: [paths] — message: "..."

Do them in order. Do NOT commit package-lock.json — I'll handle that.
```

## Why this works

Pi agent can see the full diff and make judgment calls about which changes belong together. It handles staging, committing, and sequencing without you needing to track which files were touched by which change.

## Always run tests after changes

After pi agent commits, run `npm test` (or the project's test command) to verify nothing broke. If tests fail, hand the failure output back to pi agent for fixing — don't patch manually. The user explicitly requires this validation step.

## Pitfalls

- **Don't micromanage the diff.** Tell pi what to commit and let it figure out the file lists. It has access to `git diff --stat` and `git diff`.
- **Do exclude generated files.** package-lock.json, coverage reports, and build artifacts shouldn't be in the same commits as source changes.
- **Force push after rebase.** If the branch was rebased, `git push` will be rejected as non-fast-forward. Use `git push --force-with-lease` and confirm with the user.
- **Always test after commit.** Run the test suite before pushing. Failing CI after push means rework — catch it locally.
- **Commit in named, atomic blocks.** One commit per concern. Not one giant commit. The user explicitly prefers this over a single blob commit. Good structure: "chore: config cleanup" → "test: remove obsolete tests" → "test: update screen tests" → "chore: lockfile".
