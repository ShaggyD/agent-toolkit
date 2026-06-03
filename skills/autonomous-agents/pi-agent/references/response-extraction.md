# Extracting pi's Final Text Response

When pi finishes a multi-turn research loop, the final assistant response text lives in the **session JSONL file**, not cleanly in the `wait()` return value.

## The Problem

`wait()` with `until_event="turn_end"` returns the matched event, but for complex prompts (where pi does 5–12 tool-calling turns before producing text), the response bundles all streaming deltas — often 400K–800K+ chars of thinking fragments, partial tool calls, and the actual text content jammed together. This gets truncated in tool output and is hard to parse.

## The Solution: Session File Extraction

Pi writes every event to a session JSONL file at:
```
~/.pi/agent/sessions/<project-dir-fingerprint>/<timestamp>_<uuid>.jsonl
```

The **last line** of this file contains the assistant's final message, including the complete `text` content block alongside the `thinking` block.

### One-liner extraction

```python
import json

with open(session_path) as f:
    lines = f.readlines()
    last = json.loads(lines[-1])
    msg = last.get('message', {})
    for c in msg.get('content', []):
        if c.get('type') == 'text':
            print(c['text'])
```

### Bash equivalent

```bash
python3 -c "
import json, sys
with open('$SESSION_PATH') as f:
    last = json.loads(f.readlines()[-1])
    for c in last['message']['content']:
        if c.get('type') == 'text':
            print(c['text'])
"
```

## Session file path patterns

Pi stores sessions under `~/.pi/agent/sessions/<directory-fingerprint>/<timestamp>_<uuid>.jsonl`.

The directory fingerprint is derived from the project path. For example, a session in `/home/dchadwick/dev/thoughtspace` gets stored at:
```
~/.pi/agent/sessions/--home-dchadwick-dev-thoughtspace--/<timestamp>_<uuid>.jsonl
```

You can find the exact path from `poll()` or `wait()` output which includes `"session_file": "<full-path>"` once the session has started flushing.

## Real-world data point (May 2026)

A project review prompt (which read ~60 files, ran tests + lint, explored the directory tree, and examined git history) produced:

| Metric | Value |
|--------|-------|
| Session file size | 92,031 bytes |
| Lines in session file | 63 |
| Final text response | 6,191 chars, ~1,200 words |
| Wait() return size | 421K–803K chars (truncated) |
| Total elapsed | ~2 minutes |
| pi tool-calling turns | 9 |

Use this as a calibration: for deep analysis prompts, allocate 3+ minutes and extract from the session file, not `wait()`.

## Structure of the last event

```json
{
  "type": "message",
  "message": {
    "role": "assistant",
    "content": [
      {"type": "thinking", "thinking": "..."},
      {"type": "text", "text": "Here's the full review:\n\n## 1. ..."}
    ]
  }
}
```

The `thinking` block comes first, then `text`. Skip the thinking block to get just the answer.
