# Email Triage System

Two-layer Gmail triage for inbox-zero without the cognitive load.

## Quick Start

```bash
# 1. Set up Gmail API credentials
# (see references/gmail-api-setup.md)

# 2. Copy templates
mkdir -p ~/.config/email-janitor
cp templates/config.yaml ~/.config/email-janitor/config.yaml
cp templates/noise-senders.yaml ~/.config/email-janitor/noise-senders.yaml
cp templates/safe-senders.yaml ~/.config/email-janitor/safe-senders.yaml

# 3. Install deps
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

# 4. Test with dry-run
python janitor.py --dry-run

# 5. Add to cron (every 15 min)
crontab -e
# */15 * * * * /usr/bin/python3 /path/to/janitor.py >> ~/.config/email-janitor/logs/cron.log 2>&1
```

## Files

| File | Purpose |
|------|---------|
| `janitor.py` | Zero-LLM Gmail noise archiving CLI script |
| `SKILL.md` | Full skill documentation |
| `templates/config.yaml` | Janitor configuration template |
| `templates/noise-senders.yaml` | Noise-sender patterns (promotions, newsletters, social, services, security) |
| `templates/safe-senders.yaml` | Safe-sender allowlist template |
| `templates/reviewer-soul.md` | Reviewer agent profile template |
| `references/gmail-api-setup.md` | OAuth setup for Gmail API |
| `references/label-conventions.md` | Label hierarchy conventions |
| `references/troubleshooting.md` | Common issues and fixes |

## Architecture

**Layer 1 (The Janitor):** Zero-LLM cron job that batch-archives noise every 15 minutes using Gmail API pattern matching. Builds a growing noise-sender database.

**Layer 2 (The Reviewer):** Optional LLM-powered agent that reads Janitor logs, reviews remaining emails, and produces a daily triage brief with categories and action items.

## License

MIT
