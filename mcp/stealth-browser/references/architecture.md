# Stealth Browser MCP — Architecture

## Design

The MCP server wraps `agent-browser` CLI (a Rust binary) as a persistent browser daemon. Each tool call translates to an `agent-browser --json <command>` subprocess invocation against the same daemon session.

```
┌──────────────┐   JSON-RPC 2.0    ┌──────────────────────┐   subprocess    ┌──────────────┐
│  Hermes Agent │ ←─── stdio ─────→ │  mcp_server.py      │ ──────────────→ │ agent-browser│
│  (LLM + tools)│                   │  (FastMCP, Python)   │ ←────────────── │  (Rust, daemon)
└──────────────┘                   └──────────────────────┘                 └──────────────┘
                                           │
                                     ┌─────┴──────┐
                                     │  stealth/   │
                                     │  extension  │
                                     │  (tmp dir)  │
                                     └─────────────┘
```

## Daemon Lifecycle

- **Session start:** First `navigate` call creates a session with a timestamp-based name (`stealth_<epoch>`). The daemon persists in the background.
- **Reuse:** Subsequent calls (`snapshot`, `click`, `eval`) reuse the same session name — agent-browser connects to the running daemon automatically.
- **Cleanup:** `close` sends `agent-browser close`, which kills the daemon. The MCP process itself stays alive (it can start a new session on the next `navigate`).
- **Orphan handling:** If the MCP server exits without calling `close`, the daemon becomes orphaned. `agent-browser close --all` cleans them up. On next `navigate`, the MCP server creates a new session name.

## Thread Safety

A `threading.Lock` guards all agent-browser calls. Only one tool call executes at a time per MCP server instance. This prevents interleaved subprocess writes to the same daemon socket.

## agent-browser JSON Response Protocol

Every agent-browser command with `--json` returns:

```json
{
  "success": true,
  "data": { <command-specific result> },
  "error": null
}
```

Or on failure:

```json
{
  "success": false,
  "data": null,
  "error": "error message"
}
```

**Critical parsing detail:** The `_run_ab()` function must **unwrap** the outer response — return `data.get("success")` as its own success field and `data.get("data")` as the inner payload. Failing to unwrap means tool handlers look for their expected keys (e.g., `result` for eval) at the wrong nesting level.

The unwrap pattern:

```python
raw = json.loads(stdout)
inner_data = raw.get("data") if isinstance(raw, dict) else raw
inner_success = raw.get("success", True) if isinstance(raw, dict) else True
return {"success": inner_success, "data": inner_data}
```

## Command Output by Type

| Command | `data` shape on success |
|---------|------------------------|
| `open <url>` | `{"title": "...", "url": "..."}` |
| `eval <js>` | `{"origin": "...", "result": "<evaluated JS>"}` |
| `click <ref>` | `{"result": "..."}` |
| `snapshot` | Snapshot text in `result` or implicit |
| `set viewport W H` | `{"result": "..."}` |
| `screenshot --full` | Path to PNG file on disk |
| `--json` + close | `{"closed": true}` |

## Stealth Extension

Bundled inline as Python string constants in `mcp_server.py`:
- `STEALTH_EXTENSION_MANIFEST` — Chrome extension manifest (manifest v3)
- `STEALTH_EXTENSION_JS` — content script patching at `document_start`

On startup, `_setup_extension()` extracts these to a `tempfile.mkdtemp()` directory. The directory is cleaned up in `main()`'s `finally` block.

Vectors patched:
1. `navigator.webdriver` → `undefined`
2. `navigator.plugins` → Array of 4 real plugin names
3. `navigator.languages` → `["en-US", "en"]`
4. `navigator.language` → `"en-US"`
5. `navigator.permissions.query` → Always returns `prompt` for notifications/geolocation
6. `<html webdriver>` attribute removed
7. Screen dimensions overridden if detecting 800×600 (default headless)

## Common Issues

### Eval returns empty/missing result
Check the JSON unwrap in `_run_ab()`. If `data.get("result")` returns `""`, the unwrap may be returning the outer wrapper instead of the inner payload. See "agent-browser JSON Response Protocol" above.

### `--args` or `--extension` ignored
Agent-browser prints: `⚠ --extension, --args, --user-agent ignored: daemon already running`. Close the daemon first with `agent-browser close --all` before retrying with different flags. The MCP server always passes these on every call, so this only happens if external agent-browser commands are mixed in.

### Daemon won't start ("No usable sandbox")
The `--no-sandbox` flag is in `DEFAULT_CHROME_ARGS`. If it's removed or Chrome version changes, add it back. Verify with `agent-browser doctor`.

### MCP server exits immediately (no tools)
Check stderr for `NameError: name 'FastMCP' is not defined` — the `from mcp.server.fastmcp import FastMCP` import failed. Install with `pip install mcp`.
