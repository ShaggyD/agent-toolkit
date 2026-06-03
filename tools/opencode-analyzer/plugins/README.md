# opencode-analyzer plugins

Optional plugin files that pair with the `opencode-analyzer` skill.

## What the plugin is intended to do

The cost-tracking plugin in this skill is intended to provide quick, in-app visibility for spend estimates by:

- Reading token usage from OpenCode's local DB
- Using actual provider cost when available
- Falling back to OpenRouter rates for free models
- Showing period summaries (today, yesterday, 7d, 30d)
- Showing daily/weekly/monthly averages and top-cost models

In runtimes where sidebar hooks are not available, use the stable command flow (`opencode-cost` and `/cost-report`) instead.

## Why this directory exists

OpenCode plugins are loaded from:

- `~/.config/opencode/plugins/` (global)
- `.opencode/plugins/` (project-local)

This repo directory is for storing/shareable plugin source, not for auto-loading.

## How to use a plugin from here

Copy a plugin into one of OpenCode's plugin directories, then restart OpenCode.

```bash
mkdir -p ~/.config/opencode/plugins
cp skills/opencode-analyzer/plugins/<plugin-file>.js ~/.config/opencode/plugins/
```

If needed, add npm plugin packages in `opencode.json` under `plugin`, or keep local file plugins in the directories above.

## Notes

- Keep plugin files small and focused.
- Prefer stable command-based integrations (`opencode-cost`, `/cost-report`) over sidebar UI until sidebar plugin APIs are confirmed in your runtime.
