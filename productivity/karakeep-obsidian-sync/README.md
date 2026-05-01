# karakeep-obsidian-sync

Full CRUD CLI for [Karakeep](https://github.com/karakeep-app/karakeep) (self-hosted bookmarking)
with bidirectional sync to an Obsidian vault.

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
kk login https://hoarder.example.com ak2_your_api_key_here --vault ~/obsidian/my-vault/Web\ Clips
kk sync
```

See [SKILL.md](SKILL.md) for full command reference and details.
