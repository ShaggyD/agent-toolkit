# karakeep-obsidian-sync

Full CRUD CLI for [Karakeep](https://github.com/karakeep-app/karakeep) (self-hosted bookmarking) with bidirectional sync to an Obsidian vault.

## Problem

Most bookmarking tools are either SaaS (your data on someone else's server) or require heavy setup with databases, config files, and dependency chains. Getting bookmarks into your local notes usually means manual copy-paste or brittle integrations.

## Built

A single-file Python CLI with zero external dependencies. Gives you full CRUD on Karakeep (add, list, get, edit, delete, search, and tag bookmarks) plus optional Obsidian vault sync that creates proper notes with Dataview tables, daily note cross-refs, and backlinks.

## Outcome

Ready to use the second you download it. No pip install, no database setup, no config files to edit before your first command.

**Author:** Dustin "Dusty" Chadwick ([@ShaggyD](https://github.com/ShaggyD))

## Installation

```bash
cp kk ~/.local/bin/
chmod +x ~/.local/bin/kk
```

Zero external dependencies — uses only Python stdlib.

## Quick Start

```bash
kk login https://hoarder.example.com ak2_your_api_key_here
# Follow the interactive prompts, or:
kk login https://hoarder.example.com ak2_your_api_key_here --vault ~/obsidian/my-vault/003_Resources/Bookmarks
kk sync
```

## Vault Integration

Synced bookmarks land in `003_Resources/Bookmarks/` with:
- **Index dashboard** (`_Index.md`) — Dataview tables for Recently Added and By Tag
- **Daily note cross-ref** — sync appends a link to today's daily note
- **Backlinks** — each note links back to the index

See [SKILL.md](SKILL.md) for full command reference and configuration.
