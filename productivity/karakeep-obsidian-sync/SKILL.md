---
name: karakeep-obsidian-sync
description: Full CRUD CLI for Karakeep + bidirectional sync to any Obsidian vault
version: 1.1.0
author: Capricorn
metadata:
  hermes:
    tags: [karakeep, obsidian, bookmarking, sync, cli]
---

# Karakeep ↔ Obsidian Sync

Full CRUD CLI tool (`kk`) for managing a self-hosted Karakeep instance with bidirectional sync to an Obsidian vault. The vault path is configurable — works for any vault, not just the author's.

## CLI Tool: `kk`

Installed at `~/.local/bin/kk`. Minimal dependencies (stdlib only: `urllib`, `json`, `argparse`, `re`, `pathlib`).

### Commands

| Command | Description |
|---------|-------------|
| `kk login <url> <key> [--vault PATH]` | Configure connection + optional vault setup |
| `kk list [--limit N]` | List recent bookmarks |
| `kk get <id>` | View bookmark as JSON |
| `kk add <url>` | Save a URL bookmark |
| `kk text <content>` | Save a plain text bookmark |
| `kk note <id> [text]` | View/update a bookmark's note |
| `kk edit <id> --title= --note=` | Update title, note, archived, favourited |
| `kk tag <id> <tag>...` | Attach tags |
| `kk untag <id> <tag>...` | Detach tags |
| `kk delete <id>` | Delete a bookmark |
| `kk sync` | Pull new bookmarks → Obsidian vault |
| `kk push` | Push vault note changes → Karakeep |
| `kk config [--set key=val]` | Show or update configuration |

## Onboarding Flow

On first run (`kk login`), after verifying the API connection, the tool asks:

```
Set up Obsidian vault sync? [y/N]:
  Web Clips directory path [~/obsidian/personal-vault/Web Clips]:
  Run initial sync now? [Y/n]:
```

If `--vault PATH` is passed to `login`, the interactive prompt is skipped entirely — useful for scripting or headless setup.

The vault path can also be changed later with `kk config --set vault_path=/new/path`.

## Configuration

- **Config file:** `~/.config/kk/config.json`
- **State file:** `~/.config/kk/state.json` (sync cursor + push/update timestamps)
- **Key fields in config:**
  - `url` — Karakeep instance URL
  - `api_key` — API token
  - `vault_path` — Path to Obsidian Web Clips directory (default: `~/obsidian/personal-vault/Web Clips`)

## Note Format

Each synced bookmark becomes an `.md` file with YAML frontmatter:

```yaml
---
created: 2026-04-30 05:49
source: karakeep
karakeep_id: <full-bookmark-id>
source_url: <original-url>
author: <author>
publisher: <publisher>
tags: [tag1, tag2]
status: #status/0-new
---
```

- **link** → AI summary + URL + editable `## Notes` section
- **text** → full content body
- **asset** → file reference

Editing the `## Notes` section of a synced file and running `kk push` sends changes back to the bookmark's `note` field in Karakeep.

## Filename Convention

`YYYY-MM-DD-slugified-title.md`

## Automation

A daily cron job runs `kk sync` at 8 AM via Hermes Agent. Push is manual-only for safety.

## API Reference

See `references/karakeep-api.md` for the full endpoint reference, authentication details, and known quirks discovered through real-world use (User-Agent block, tag format, 204 handling).

## Pitfalls

- **User-Agent block:** Karakeep blocks Python's default `urllib` UA string. The tool sets `User-Agent: kk-cli/0.3`.
- **Empty DELETE responses:** API returns 204 No Content — tool handles empty body gracefully.
- **Full IDs required:** Always use full bookmark IDs (displayed by `kk list`). Truncated IDs return 404.
- **Tag format:** Tags use `{"tagName": "..."}` objects. The tool handles this internally.
- **Clearing a note:** `kk note <id> ""` clears a bookmark's note field.
- **API key stored in plaintext** at `~/.config/kk/config.json` — treat the config file as sensitive.
- **Filename collisions:** Bookmarks without a title or content map to `unknown-untitled.md` and may collide.
