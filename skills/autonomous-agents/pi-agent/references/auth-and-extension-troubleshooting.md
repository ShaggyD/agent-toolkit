# Pi Auth + Extension Troubleshooting

## 1) Symptom: prompt fails with missing API key

Error pattern:

- `No API key found for opencode-go`
- `No API key found for unknown`

### Fix order

1. Confirm provider/model defaults in `~/.pi/agent/settings.json`.
2. Ensure credentials are available via:
   - `~/.pi/agent/auth.json` entries for `opencode-go` and `opencode`, or
   - `OPENCODE_API_KEY` exported in the spawned process environment.
3. Re-test with a minimal prompt in RPC mode.

## 2) Symptom: extension load blocks CLI startup

Error pattern:

- `Failed to load extension ... pi-minimal-footer ... Cannot find module '@earendil-works/pi-coding-agent'`

### Fix

Remove the broken package from `~/.pi/agent/settings.json` `packages` list (or reinstall its missing dependency chain). For immediate recovery, removal is fastest and restores CLI startup.

## 3) Wrapper gotcha

A wrapper script may run even if interactive shell env is not loaded. Always pass explicit `env` into `subprocess.Popen(...)` for deterministic auth behavior.
