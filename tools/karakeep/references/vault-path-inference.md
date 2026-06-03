# Vault Path Inference Design

When the user configures `vault_path` (where bookmarks are stored as `.md` files), the tool
also needs to locate the daily notes directory for sync cross-references. Rather than
requiring two separate config values, `kk` infers the daily notes path from `vault_path`
using a simple heuristic.

## The Heuristic

```
If vault_path ends with:  .../003_Resources/Bookmarks
Then daily notes are at:  .../002_Journal/daily
```

Implementation (Python):

```python
vp = Path(vault_path).expanduser().resolve()
if vp.name == "Bookmarks" and vp.parent.name == "003_Resources":
    inferred = vp.parent.parent / "002_Journal" / "daily"
    if inferred.exists():
        return inferred
return None  # fallback — user must set daily_path explicitly
```

## Why This Works

This assumes the user follows a [PARA-like](https://fortelabs.com/blog/para/) vault structure:
- `003_Resources/` — reference material, templates, external knowledge
- `002_Journal/` — temporal notes (daily, weekly, monthly)
- `001_Inbox/` — unprocessed captures
- `000_Attachments/` — media, screenshots, assets

This is a common Obsidian vault convention. The tool doesn't enforce it — it only checks if
the inferred path actually exists. If it doesn't, daily cross-references are silently skipped
and the user can set `daily_path` explicitly.

## Explicit Override

Users can bypass inference entirely:

```bash
kk config --set daily_path=/absolute/path/to/daily-notes
```

Explicit `daily_path` always wins over inference.

## Design Principles

1. **Zero-config for common case** — PARA users get daily cross-refs without extra setup
2. **Silent skip for edge cases** — non-PARA vaults aren't forced to set a path
3. **Explicit override for everyone** — one command to point anywhere
4. **No hardcoded Dusty paths** — the default is gone, all paths derive from config
