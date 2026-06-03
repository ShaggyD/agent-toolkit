# Model Capability Discovery

How to determine which models support a specific capability (vision, audio, long context, etc.) and compare costs — before starting a pi-agent session or delegating a task.

## Why

The user prefers cost-effective model selection: try the cheapest capable model first, escalate to more expensive ones only if it struggles. You need to know which models have the capability AND what they cost before you can make that choice.

## Discovery workflow

### 1. List available models

```bash
opencode models
```

This shows all models available under the configured provider (e.g. `opencode-go/`). Each entry includes:
- Model name (e.g. `qwen3.6-plus`, `kimi-k2.6`, `mimo-v2-omni`)
- Provider prefix (e.g. `opencode-go/`)
- Cost per token (input/output)

### 2. Test capability

For each model you want to test, send it a prompt that requires the capability:

**Vision test:**
```bash
opencode run "Describe this image in detail: https://i.imgur.com/r2Bt8eD.jpeg" --model opencode-go/qwen3.6-plus --thinking
```

Check:
- Does it access the image URL successfully?
- Does the description match what's actually in the image?
- Is the transcription/recognition quality acceptable?

**Audio test (if available):**
```bash
opencode run "Transcribe this audio: file:///path/to/audio.wav" --model opencode-go/mimo-v2-omni --thinking
```

### 3. Compare costs

From the `opencode models` output, note:
- Input cost per 1K tokens
- Output cost per 1K tokens
- Minimum commitment (some models have a minimum before returning)

The user's cost tolerance: prefer models ≤ $0.30/M input for bulk work; only escalate to $1+/M models when quality demands it.

### 4. Pick the cheapest capable model

```text
Rule: best capability-to-cost ratio. If the $0.20 model handles the task, use it. 
Only escalate if it struggles on quality (transcription accuracy, detail extraction, etc.).
```

## Known model capabilities (opencode-go provider)

| Model | Vision | Cost (approx) | Notes |
|-------|--------|--------------|-------|
| `qwen3.6-plus` | ✅ Works | $0.20/M | Best value — use as default vision model |
| `kimi-k2.6` | ✅ Works | ~$0.30/M | Strong reasoning, good transcription |
| `kimi-k2.5` | ✅ Works | ~$0.25/M | Good transcription |
| `mimo-v2-omni` | ✅ Works | Higher | Fallback only when cheap models struggle |
| `glm-5.1` | ❌ No vision | — | Can't see image attachments |
| `minimax-m2.5` | ❌ No vision | — | No image support |
| `deepseek-v4-flash` (default) | No vision | Free* | Text-only; use for metadata/summarization |

*Default model via OpenCode Go API — effectively free for the user.

## When to use this

- Before starting a pi-agent session that needs vision/transcription
- When the user asks you to keep costs low
- When you're unsure whether a cheaper model can handle the task
- After a model fails on a capability — test the next model up

## Pitfalls

- **Costs are per-provider.** The `opencode models` output shows opencode-go pricing. Other providers (Anthropic, OpenAI) have different cost structures.
- **Capabilities change.** Models get updated. Re-test if a previously-working model stops handling a task.
- **Quality is task-dependent.** A model may handle simple vision but fail on dense transcription (e.g. small text in a screenshot). Test with realistic input.
- **`.dev` TLD services (model.dev, pi.dev) may be unreachable** from this machine due to DNS resolution issues. Use the opencode-provided model list and direct testing instead.
