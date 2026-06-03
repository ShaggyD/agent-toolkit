# Content Editing Feedback Loop

A repeatable workflow for collaborative web content editing using browser screenshots.

## When to use

You're editing HTML/CSS in a local project and the user wants to see visual results before locking in changes. This pattern avoids "trust me, it looks good" hand-waving and gives the user something real to react to.

## The loop

```
1. Edit source files (patch, write_file)
2. Commit (git add + commit) — keeps a clean rollback point
3. Reload browser → screenshot → deliver to user
4. Get feedback → goto step 1
```

## Step-by-step

### 1. Edit
Use `patch` or `write_file` to modify the source files. For HTML content changes (copy, structure), `patch` is preferred since it's targeted.

```bash
# Example: replacing a tagline in an HTML file
patch new_str="Strategy follows reality." \
      old_str="Strategy follows proof." \
      path=/home/dchadwick/codegrit-dev-site/index.html
```

### 2. Reload the browser

The browser daemon persists across commands (started with `agent-browser --args "..." open <url>`).

```bash
# Hard reload to pick up file changes
agent-browser eval "location.reload()"
```

Add a small sleep (1-2s) to let the page render, especially if it has animations or lazy-loaded assets.

### 3. Scroll to the changed section

Use `eval` with `scrollIntoView` to target the specific section you edited:

```bash
# Scroll to the flywheel section, offset for fixed headers
agent-browser eval \
  "document.getElementById('flywheel').scrollIntoView({behavior:'instant', block:'start'}); window.scrollBy(0, -80);"
```

### 4. Screenshot

Two modes:

- **Full page** (best for showing how the section fits in context):
  ```bash
  agent-browser screenshot --full
  ```
  Saves to `/home/dchadwick/.agent-browser/tmp/screenshots/screenshot-<timestamp>.png`

- **Viewport only** (best for tight sections):
  ```bash
  agent-browser screenshot
  ```

### 5. Deliver

Send the image to the user using `MEDIA:<path>` in your response:

```
MEDIA:/home/dchadwick/.agent-browser/tmp/screenshots/screenshot-1779640290794.png
```

### 6. Iterate

Get feedback → refine → commit → screenshot → deliver again. Each iteration deserves its own commit so you can roll back cleanly if a direction doesn't work.

## Tips

- **Commit before screenshotting.** If the user hates the change, `git revert` is one command.
- **Snapshot first if you're unsure what element IDs exist.** Use `agent-browser snapshot -i` to find the right `id` for `scrollIntoView`.
- **Anchor fragments work too.** Opening `http://localhost:8765/#flywheel` scrolls automatically, but `scrollIntoView` is more reliable after a reload.
- **Full-page screenshots are wide.** They capture the entire document height. The user sees everything above the fold plus the section you edited below — gives context.
- **Don't screenshot every minor change.** Batch edits into coherent groups before showing the user. One screenshot per round of feedback.
- **Daemon collision.** If a previous invocation crashed, run `agent-browser close` before retrying. The daemon holds the browser process — it won't auto-recover on error.
