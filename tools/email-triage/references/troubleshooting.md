# Troubleshooting

Common issues and fixes when setting up the email triage system.

---

## Janitor Issues

### "No module named googleapiclient"

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Gmail API returns 403 (Insufficient Permission)

1. Ensure OAuth scopes include `gmail.modify`:
   ```python
   SCOPES = [
       'https://www.googleapis.com/auth/gmail.modify',
       'https://www.googleapis.com/auth/gmail.labels',
   ]
   ```
2. Re-run the token generation flow
3. Delete the old token file first: `rm ~/.google/gmail-token.json`

### "Token has expired"

Tokens auto-refresh via the Google client library. If the refresh token itself has expired (6-month inactivity):

1. Delete `~/.google/gmail-token.json`
2. Re-run the OAuth flow

### Rate limiting (429 Too Many Requests)

The Janitor uses configurable rate limiting:
- Default: 5 requests/second
- Gmail quota: 250 quota units/user/second
- `modify()` = 10 units → max 25 modifies/second

If you hit rate limits:
1. Reduce `rate_limit_rps` in `config.yaml`
2. Add exponential backoff (built into the Janitor client)

### "Label not found" warnings

The Janitor reads labels dynamically from Gmail. If no label matches a domain:
- No label is applied (the email is still archived)
- Check if the label exists in Gmail under the expected name
- Labels are case-sensitive — `services/example.com` ≠ `Services/example.com`

### False positives (email archived that shouldn't have been)

1. Check the Janitor log to see which pattern matched
2. Add the sender to `safe-senders.yaml`
3. Run a dry-run to verify: `python janitor.py --dry-run`
4. Check if the subject-line pattern is too aggressive

### False negatives (noise not archived)

1. Check if the sender is in `safe-senders.yaml` (remove if needed)
2. Add the sender pattern to `noise-senders.yaml` under the appropriate category
3. Verify the pattern syntax matches what's in the email's from field
4. Run `python janitor.py --dry-run` to see if the new pattern catches it

---

## Reviewer Issues

### No Janitor logs found

The Reviewer checks for logs from the last 48 hours. If none exist:
- It warns and proceeds with a full inbox review
- Check that the Janitor cron is running: `crontab -l | grep janitor`
- Check Janitor log directory permissions

### Reviewer LLM hallucinations

- Pin the model version in the Reviewer profile config
- Include the categorization categories explicitly in the prompt
- Review the first week of outputs manually to calibrate

### Too many emails to review

Adjust the reviewer's approach:
- Increase Janitor's noise detection (add more patterns)
- Add the high-volume sender to noise-senders.yaml
- For conference/launch spikes, consider running Janitor more frequently

---

## Cron Issues

### Cron not running

```bash
# Check crontab
crontab -l

# Check cron logs (Ubuntu/Debian)
grep janitor /var/log/syslog | tail

# Check cron logs (macOS)
grep janitor /var/log/cron.log | tail
```

### Permission issues

The Janitor runs under your user account. Ensure:
- `~/.google/gmail-token.json` is readable
- `~/.config/email-janitor/` is writable
- The cron command uses the full path to Python: `/usr/bin/python3` or use `/usr/bin/env python3`

---

## OAuth / Auth Issues

### "Access blocked: The app hasn't been verified"

This is normal for personal projects. In the OAuth consent screen, add your email as a **Test User**. The warning disappears once you're signed in.

### "Error 400: redirect_uri_mismatch"

The OAuth flow uses `http://localhost:PORT` for the redirect URI. If you see this:
1. Make sure you're using Desktop Application credential type (not Web Application)
2. The `run_local_server()` method handles this automatically

### Token won't refresh

If the token file is corrupted or the refresh token expired:
```bash
rm ~/.google/gmail-token.json
# Re-run the OAuth flow
```

---

## Performance

### Janitor runs slowly

- Increase `batch_size` in config.yaml (max 100)
- Check network latency to Gmail API
- Rate limiting may be too conservative — increase `rate_limit_rps` if you're not hitting 429s

### Reviewer runs slowly

- Reduce the number of emails by improving Janitor's noise capture
- Consider a faster LLM model for categorization
- Increase Janitor frequency (every 10 min instead of 15)

---

## Storage

### Log directory growing too large

The Janitor produces one JSONL file per run. At 15-min intervals:
- ~96 files/day
- ~2,880 files/month
- Each file is typically 1-5 KB

Consider a log rotation cron:
```bash
0 0 * * 0 find ~/.config/email-janitor/logs -name "*.jsonl" -mtime +90 -delete
```
