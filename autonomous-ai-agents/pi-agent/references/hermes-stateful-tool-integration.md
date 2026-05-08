# Hermes-native `pi_rpc` tool integration notes

## Why
A shell wrapper works, but a native Hermes tool gives stable lifecycle control across tool calls and keeps session state in one place.

## Current action surface (production)
- `start` — spawn `pi --mode rpc` (optional `workdir`, `provider`, `model`, `pi_session_path`)
- `send` — send `message` or raw `command`; supports correlation `request_id`
- `poll` — incremental event retrieval (`offset`, `limit`) with session cursor default
- `wait` — block until completion boundary (default `until_event=turn_end`) with timeout
- `list` — show live sessions and detached metadata sessions
- `resume` — start a new live process from a detached record (prefers saved `sessionFile`)
- `prune` — remove stale detached metadata records older than `max_age_days`
- `stop` — terminate process and remove session handle

## Proven integration steps
1. Create/update tool module: `~/.hermes/hermes-agent/tools/pi_rpc_tool.py`.
2. Register schema as `pi_rpc` with the action API above.
3. Persist session metadata to: `~/.hermes/state/pi_rpc_sessions.json`.
4. Expose in toolsets by adding `pi_rpc` to:
   - `_HERMES_CORE_TOOLS`
   - `terminal` toolset
5. Verify registration with `registry.get_entry("pi_rpc")`.
6. Test lifecycle: `start -> send -> wait/poll -> stop`.

## Restart semantics
- On Hermes process restart, stored sessions are reloaded as **detached** records.
- Detached sessions are listable (continuity context), but not writable (`send` fails) because stdio cannot be safely reattached.
- Use `resume` on a detached session to start a new live process:
  - preferred: resume with saved `sessionFile`
  - fallback: if `sessionFile` is missing, start fresh in the prior `workdir` and return a warning
- Use `prune` periodically to clean stale detached records (`max_age_days`, default 7).

## Testing evidence pattern
- Add focused tests under `tests/tools/test_pi_rpc_tool.py`.
- Also update `tests/tools/test_registry.py` expected builtin tool list to include `tools.pi_rpc_tool`.
- Run:
  - `python -m pytest tests/tools/test_pi_rpc_tool.py -q -o 'addopts='`
  - `python -m pytest tests/tools/test_pi_rpc_tool.py tests/tools/test_registry.py -q -o 'addopts='`

## Gotchas
- Tool changes require Hermes restart/new session to appear in active schemas.
- Immediate `poll` after `send` can be empty; not necessarily failure.
- In some environments, Pi may emit sparse/non-JSON output; `wait` can time out despite valid process lifecycle. Treat as runtime/provider quirk and verify via `stop`/`list` health checks.
- Keep auth source centralized in Pi (`~/.pi/agent/auth.json`) to avoid duplicate token plumbing.
