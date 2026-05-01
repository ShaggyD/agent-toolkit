---
name: karakeep-obsidian-sync
description: Full CRUD CLI for Karakeep — standalone bookmarking tool with optional Obsidian vault sync
version: 0.5.0
author: Dustin Chadwick
metadata:
  hermes:
    tags: [karakeep, obsidian, bookmarking, sync, cli, crud]
---

# Karakeep ↔ Obsidian Sync

A CLI tool for [Karakeep](https://github.com/karakeep-app/karakeep) (self-hosted bookmarking). All CRUD commands work standalone — Obsidian vault sync is an optional add-on.

**Author:** Dustin "Dusty" Chadwick ([@ShaggyD](https://github.com/ShaggyD))

## CLI Tool: `kk`

Single-file Python script — zero external dependencies.

### Commands

| Command | Description |
|---------|-------------|
| `kk login <url> <key>` | Connect to a Karakeep instance |
| `kk logout` | Wipe saved config and state |
| `kk list [--limit N]` | List recent bookmarks |
| `kk get <id>` | View bookmark as JSON |
| `kk add <url>` | Save a URL bookmark |
| `kk text <content>` | Save a plain text bookmark |
| `kk note <id> [text]` | View/update a bookmark's note |
| `kk edit <id> --title= --note=` | Update title, note, archived, favourited |
| `kk tag <id> <tag>...` | Attach tags |
| `kk untag <id> <tag>...` | Detach tags |
| `kk delete <id>` | Delete a bookmark |
| `kk sync [--enrich]` | Pull new bookmarks → vault; use --enrich for transcripts/content |
| `kk push` | Push vault note changes → Karakeep (if configured) |
| `kk enrich <id>` | Fetch YouTube transcript or article content for a single bookmark |
| `kk config [--set key=val]` | Show or update configuration |

None of the CRUD commands (`list`, `get`, `add`, `text`, `note`, `edit`, `tag`, `untag`, `delete`) require a vault. Sync and push only work if `vault_path` is configured.

## Quick Start (standalone — no vault needed)

```bash
# Install
cp kk ~/.local/bin/ && chmod +x ~/.local/bin/kk

# Connect
kk login https://hoarder.example.com ak2_your_api_key_here

# Use
kk list
kk add https://example.com/article
kk note <id> "My thoughts on this"
```

## Optional: Obsidian Vault Sync

After login (or later), configure vault sync:

```bash
kk config --set vault_path=~/my-vault/003_Resources/Bookmarks
kk config --set daily_path=~/my-vault/002_Journal/daily   # optional
kk sync   # initial pull
```

The `login` command also offers an interactive vault setup prompt.

### What sync does

- Creates a `_Index.md` in your bookmark directory with Dataview-powered Recently Added and By Tag tables
- Each bookmark becomes a `.md` file with frontmatter (source, URL, tags, author)
- Backlinks point to `[[_Index|Bookmarks]]` (relative — works from any folder)
- Optional: appends a cross-reference to today's daily note if `daily_path` is configured

### What push does

Scans your vault for edited `## Notes` sections and pushes changes back to the bookmark's note field in Karakeep.

### Enrichment

Bookmarks can be enriched with additional content before saving to the vault:

| Type | Enrichment | How |
|------|-----------|-----|
| YouTube links | Full transcript (25K+ chars) | `youtube-transcript-api` via `uv run --with` |
| Article links | Readable text extraction | `curl` + Python's built-in `html.parser` |

**Commands:**
- `kk enrich <id>` — enrich a single bookmark and preview the result
- `kk sync --enrich` — sync new bookmarks and auto-enrich each one

Enrichment is best-effort. If fetching fails, the note is still saved with Karakeep's existing content.

The cron default is `kk sync` without `--enrich` because enrichment adds latency (transcript fetching, page downloads). Run with `--enrich` periodically or when you want deep content in new bookmarks.

### Vault path inference design

```json
{
  "url": "https://hoarder.example.com",
  "api_key": "ak2_...",
  "vault_path": "~/my-vault/003_Resources/Bookmarks",
  "daily_path": "~/my-vault/002_Journal/daily"
}
```

- `vault_path` — where synced bookmarks go as `.md` files (sync/push only)
### What push does

Scans your vault for edited `## Notes` sections and pushes changes back to the bookmark's note field in Karakeep.

### Enrichment

Bookmarks can be enriched with additional content before saving to the vault:

| Type | Enrichment | How |
|------|-----------|-----|
| YouTube links | Full transcript (25K+ chars) | `youtube-transcript-api` via `uv run --with` |
| Article links | Readable text extraction | `curl` + Python's built-in `html.parser` |

**Commands:**
- `kk enrich <id>` — enrich a single bookmark and preview the result
- `kk sync --enrich` — sync new bookmarks and auto-enrich each one

Enrichment is best-effort. If fetching fails, the note is still saved with Karakeep's existing content.

The cron default is `kk sync` without `--enrich` because enrichment adds latency (transcript fetching, page downloads). Run with `--enrich` periodically or when you want deep content in new bookmarks.

### Vault path inference design

When `daily_path` is not explicitly set, the tool infers it from `vault_path`
using a PARA-structure heuristic. See `references/vault-path-inference.md`.

### Automation (cron)

```cron
0 8 * * * /home/user/.local/bin/kk sync
```

No push cron by default — editing notes in your vault should be intentional.

## Note Format

```yaml
---
created: 2026-04-30 05:49
source: karakeep
karakeep_id: <full-bookmark-id>
source_url: <original-url>
author: <author>
publisher: <publisher>
tags: [tag1, tag2]
---
```

No personal tags or conventions are baked in. Notes link back to `[[_Index|Bookmarks]]` which works from any vault folder structure.

## Known Pitfalls

- **API key in plaintext** — stored at `~/.config/kk/config.json`. Recommended: `chmod 600 ~/.config/kk/config.json`
- **User-Agent block** — Karakeep blocks Python's default `urllib` UA. The tool sets `User-Agent: kk-cli/0.5`
- **Full IDs required** — use full bookmark IDs from `kk list`. Truncated IDs return 404
- **Tag format** — the API expects `{"tagName": "..."}` objects, not strings. Handled internally
- **Clearing a note:** `kk note <id> ""` clears a bookmark's note field
- **Filename collisions** — bookmarks without a title/content map to `unknown-untitled.md`
- **Python 3.7+ required** (for `pathlib` and `datetime.fromisoformat`)
- **Empty DELETE responses** — API returns 204 No Content. Tool handles empty body gracefully
