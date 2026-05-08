# Pi RPC Pitfalls Seen in Practice

## 1) Wrong prompt payload key

Symptom:
- Prompt command returns runtime error (example: `Cannot read properties of undefined (reading 'startsWith')`).

Cause:
- Sending `{"type":"prompt","prompt":"..."}` instead of `{"type":"prompt","message":"..."}`.

Fix:
- Use `message` as the payload key for prompt text.

## 2) Provider/auth missing despite valid RPC transport

Symptom:
- Prompt command returns:
  - `No API key found for unknown. Use /login or set an API key environment variable...`

Cause:
- RPC process is running correctly, but model provider auth is not configured in the environment/session.

Fix:
- Configure provider auth (`pi /login` or provider env vars such as `OPENCODE_API_KEY`).
- Verify by running a simple prompt after auth is set.

## 3) Wrong repository context

Symptom:
- Branch/diff output appears unrelated to intended project.

Cause:
- `pi --mode rpc` launched outside the target project directory.

Fix:
- Launch with explicit project cwd (e.g., `cd ~/dev/project && pi --mode rpc`) or set `cwd` in your client wrapper.

## Fast triage checklist

1. `pi --mode rpc --help` works.
2. `get_state` returns `sessionFile`.
3. Prompt payload uses `message` key.
4. Auth configured for selected provider/model.
5. Process cwd points to intended repo root.
