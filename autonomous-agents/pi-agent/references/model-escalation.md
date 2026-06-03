# Model Escalation Workflow for Pi Agent

## When to escalate

When pi-agent is running a complex task (multi-turn research, git operations, test runs) on a weaker model and either:
- The user explicitly instructs you to escalate on barrier (e.g., "escalate to Codex 5.3 if stuck")
- The agent has been producing unusable output or failing at simple tasks for 3+ minutes
- You're in a time-sensitive scenario where faster reasoning matters

## How to escalate mid-session

Pi agent supports switching the model at runtime without restarting the session. The session state is preserved.

### Check current model

First confirm what model is active, and also check what models are available:

```bash
# Check what's active
get_state via pi_agent

# List available models
opencode models
```

The response includes `model.id`, `model.name`, `model.api`, `model.provider`.

### Switch to a stronger model

Send a `set_model` command:

```json
{"type": "set_model", "provider": "opencode-go", "model": "deepseek-v4-pro"}
```

Available escalation targets vary by subscription. **Always check with `opencode models` first.** Common `opencode-go` options:
- `deepseek-v4-pro` — stronger reasoning than flash
- `kimi-k2.6` — strong reasoning model
- `minimax-m2.7` — high quality general model
- `glm-5.1` — alternative high-quality model
- `qwen3.6-plus` — large context window

If the user requests a specific subscription model (e.g. "OpenAI Codex 5.3") that doesn't appear in `opencode models`, it's not available — tell them rather than failing silently.

### Verify the switch

Send another `get_state` and confirm `model.id` changed.

### Downgrade back after breakthrough

Once the barrier is broken (complex task done), switch back to the original model:

```json
{"type": "set_model", "provider": "opencode-go", "model": "deepseek-v4-flash"}
```

## Complete lifecycle

```
1. Send task prompt                       → send({message: "..."})
2. Wait for completion or detect barrier  → wait(turn_end)
3. Check if stuck (no progress)           → poll(limit=5)
4. Check available models                 → opencode models
5. Escalate: set_model to stronger model
6. Re-send the problematic prompt
7. Wait for breakthrough
8. Downgrade: set_model back to original
9. Continue with remaining work
```

## Switching to a different provider (not opencode-go)

The user may request a model from a different provider, e.g. "OpenAI Codex 5.3 codex" or "5.3-codex via openai-codex subscription." The `set_model` command takes a `provider` field:

```json
{"type": "set_model", "provider": "openai-codex", "model": "5.3-codex"}
```

### Available providers for pi agent

Pi supports multiple providers. Check what's configured on this machine:

```bash
# List providers and their auth status
cat ~/.pi/agent/auth.json 2>/dev/null || echo "No auth.json found"
# Pi's own provider listing
pi providers list 2>/dev/null || echo "No pi providers command available"
```

Common provider strings:
- `"opencode-go"` — default, uses your OpenCode subscription
- `"openai-codex"` — separate OpenAI Codex subscription (NOT the same as opencode-go)
- `"anthropic"` — Claude models
- `"google"` — Gemini models

### OpenAI Codex specifically

The `openai-codex` provider uses the OpenAI Codex API (chatgpt.com/backend-api). It is a **different subscription** from `opencode-go`:

```json
{"type": "set_model", "provider": "openai-codex", "model": "5.3-codex"}
```

Known available model strings for openai-codex:
- `"5.3-codex"` — strongest available
- `"5.3-codex-spark"` — slightly weaker/cheaper variant
- `"5.2-codex"` — previous generation

### Auth failure: "No API key found for <provider>"

If `set_model` succeeds but prompting fails with:

**`No API key found for openai-codex.`**

This means the provider exists but has no credentials configured. **This is an auth problem, not a transport or model problem.** The provider is recognized but not authenticated.

**What to do when this happens:**
1. **Tell the user clearly** — don't silently fall back. Say: "openai-codex doesn't have credentials configured on this machine."
2. **Escalate via available means instead** — check what other providers have keys:
   ```bash
   cat ~/.pi/agent/auth.json 2>/dev/null | python3 -m json.tool
   ```
3. **Fall back to direct work** — if no alternative strong provider has keys, ask the user if you should proceed directly with terminal/code tools instead.
4. **Do NOT keep trying pi prompts** — a missing API key will fail every time. Move on.

### Auth configuration locations

Credentials live in two places depending on the provider:

| Provider | Credential location |
|----------|-------------------|
| `opencode-go` | `OPENCODE_API_KEY` env var or `~/.pi/agent/auth.json` |
| `openai-codex` | Only `~/.pi/agent/auth.json` (not env var) |
| Others | `~/.pi/agent/auth.json` or pi login |

To configure a missing provider:
```bash
# Interactive login flow
pi /login

# Or manually add to auth.json
# {"openai-codex": {"type": "api_key", "key": "sk-..."}}
```

### Complete multi-provider escalation lifecycle

```
1. Send task prompt                          → send({message: "..."})
2. Wait for completion or detect barrier     → wait(turn_end)
3. Check if stuck (no progress)              → poll(limit=5)
4. If stuck, try escalation:
   a. set_model to stronger model in same provider:
      → {"type": "set_model", "provider": "opencode-go", "model": "deepseek-v4-pro"}
   b. If user requested specific provider (e.g. openai-codex), try that:
      → {"type": "set_model", "provider": "openai-codex", "model": "5.3-codex"}
   c. If provider has no API key → tell user, fall back to direct work
5. Re-send the problematic prompt
6. Wait for breakthrough
7. Downgrade back to original model:
   → {"type": "set_model", "provider": "opencode-go", "model": "deepseek-v4-flash"}
8. Continue with remaining work
```

## What NOT to do

- **Do not kill the pi agent and take over directly** — the user explicitly instructed you to use pi agent and escalate. Killing the session violates the workflow.
- **Do not poll() for speed assessment** — intermediate events show streaming garbage. Use `wait(turn_end)` and check elapsed time instead.
- **Do not assume model names exist** — always check `opencode models` before attempting set_model.
- **Do not run git operations yourself via terminal** when pi agent is available. Hand staging, committing, and pushing to pi with a structured prompt.
- **Do not keep retrying a provider that has no API key configured** — it will fail every single time. Tell the user, check what providers work, and move on.
- **Do not confuse `openai-codex` (ChatGPT Codex API) with `opencode-go` (OpenCode subscription)** — they are separate subscriptions with separate credentials. Failing on one does not mean the other is broken.

## When all escalation paths are exhausted

This session proved a real scenario: pi agent on `deepseek-v4-flash` was too slow for multi-turn deep code analysis (exploring file structure, running tests, reading source). The user-specified escalation model (`openai-codex`) had no credentials on this machine. Other available models (qwen, kimi, glm) are not Codex and don't match the user's request.

### Decision tree when escalation is blocked

```
User says "escalate to model X at barriers"
  ↓
Check if model/provider exists → opencode models / pi --models "*"
  ├── Provider exists, has credentials → set_model and re-send prompt
  └── Provider doesn't exist OR has no credentials:
       ├── Tell the user clearly which provider is missing and why
       ├── Check available providers for alternatives
       │   ├── Stronger model in same provider available? → escalate within provider
       │   └── No strong alternative available → report to user
       └── Fall back to DIRECT WORK using terminal/file/tools
           (This is OK when escalation is genuinely impossible)
```

### When to fall back to direct work

Doing the work directly — reading files with terminal, writing code with write_file, running tests — is the correct fallback when:

1. **Pi agent is too slow** on the available model (deepseek-v4-flash goes turn-by-turn through files)
2. **The escalation path has no credentials** (openai-codex not configured)
3. **The task is well-understood** — you know what files to edit and what tests to write

This is NOT the same as killing the agent arbitrarily. It's accepting that the escalation path specified by the user doesn't exist and making pragmatic progress.

### How to communicate the fallback to the user

```
"I started pi agent but the available model (deepseek-v4-flash) is slow at
deep code analysis. I tried to escalate to {user-specified model} but it's
not configured — {provider} has no credentials on this machine. I'll proceed
directly with terminal/file tools to make progress."
```

### Example from this session

The thoughtspace repo needed: audit test coverage gaps, write test files, fix lint warnings, commit and push. The pi agent on deepseek was exploring file-by-file. OpenAI Codex wasn't configured. The pragmatic path was:

1. Stop the stuck pi session
2. Run `find ... __tests__/` to find covered vs uncovered files
3. Write the 3 highest-value test files directly
4. Run full test suite (200 all green)
5. Commit and push
