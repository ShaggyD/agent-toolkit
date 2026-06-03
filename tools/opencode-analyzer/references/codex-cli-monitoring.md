# Codex CLI Cost Monitoring

OpenAI Codex CLI (gpt-5.5, gpt-5.3-codex, etc.) has a separate cost tracking approach from OpenCode. Codex stores sessions as JSONL files under `~/.codex/sessions/YYYY/MM/DD/` and a logs database at `~/.codex/logs_2.sqlite`.

## Approach

A watchdog script at `~/.hermes/scripts/codex-usage-monitor.py` provides hourly cost estimation and threshold alerts.

### How it works

1. Parses Codex session JSONL files modified within the lookback window (5h or 168h)
2. Estimates tokens from response content (~4 chars/token)
3. Applies model pricing (gpt-5.5: $1.25/M input, $10.00/M output)
4. Compares against a prorated monthly budget (default $100/mo)
5. Only fires on first crossing of 50% threshold, then stays silent with daily-brief reminders

### Cron job setup

```bash
# Hourly watchdog (no_agent mode — pure script, no LLM)
hermes cron create \
  --name "Codex usage watchdog" \
  --script "codex-usage-monitor.py check-both" \
  --schedule "every 1h" \
  --no-agent true
```

### Daily brief integration

In the morning standup cron prompt, add a step:
```
Run `python3 ~/.hermes/scripts/codex-usage-monitor.py daily-brief`
and include output under a "💰 Codex Usage" section.
```

### Alert behavior

| State | Behavior |
|---|---|
| Usage under 50% | Silent — no output |
| First time over 50% | Alert fires to origin channel |
| Subsequent checks over 50% | Silent (already alerted) |
| Daily brief with active alert | One-liner reminder |
| Usage drops below 50% | State auto-clears |

State is tracked in `~/.hermes/state/codex_alert_state.json`.

### Manual commands

```bash
# Check both 5h and weekly windows
python3 ~/.hermes/scripts/codex-usage-monitor.py check-both

# Get daily brief status
python3 ~/.hermes/scripts/codex-usage-monitor.py daily-brief

# Reset alert state
python3 ~/.hermes/scripts/codex-usage-monitor.py reset
```

### Script location

`~/.hermes/scripts/codex-usage-monitor.py`

### Pitfalls

- This is an **estimate**, not actual OpenAI billing. Tokens are estimated from character count (~4 chars/token). Real usage may differ.
- Codex session files are only created per-turn. Idle periods generate no files. The script only counts what's on disk.
- If you clear your Codex sessions directory, the 5h window resets to zero.
- Model pricing should be updated if OpenAI changes rates.
- This monitors **Codex CLI** only. For **OpenCode** cost analysis, use the `opencode-cost` tool in this same skill.
