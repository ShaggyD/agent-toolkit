# Using `uv run --with` for Ad-Hoc Python Dependencies

Use `uv run --with <package>` when a CLI tool or script needs a Python package but shouldn't have permanent dependencies. This pattern is used by the `kk enrich` command to fetch YouTube transcripts without requiring `youtube-transcript-api` to be installed.

## How it works

```bash
uv run --with youtube-transcript-api python3 -c '
from youtube_transcript_api import YouTubeTranscriptApi
api = YouTubeTranscriptApi()
t = api.fetch("VIDEO_ID")
print(" ".join(s.text for s in t.snippets))
'
```

`uv` creates a temporary virtual environment, installs the package into it, runs the command, then discards it. No permanent install, no version conflicts.

## Best practices

1. **Always use `--with`** — without it, `uv run` uses the system Python which may not have the package.
2. **Pass code as a script or `-c` string** — inline code avoids needing a separate file.
3. **Capture stderr separately** from stdout, since `uv` prints package installation progress to stderr.
4. **Check `uv exists first`** — wrap in a `try/except FileNotFoundError` and fall back gracefully if `uv` isn't installed.
5. **Set reasonable timeouts** — `uv` can take a few seconds to install packages on first run (cached thereafter).
6. **Metadata prefix convention** — print machine-readable metadata on stdout before the actual output, then parse it from the parent process:

```python
print(f"LANGUAGE:{t.language}")
print(f"CHARS:{len(full_text)}")
print(full_text, end="")
```

## When to use this pattern

- **Optional enrichment features** — the CLI works without the dependency, but can do more with it.
- **Niche packages** that only apply to specific content types (YouTube transcripts, PDF extraction, image processing).
- **One-shot scripts** where installing the package permanently is overkill.
- **Environment-constrained systems** (externally-managed Python, no sudo, containers).

## When NOT to use this pattern

- Core functionality that the tool needs on every invocation.
- Packages with native extensions that take a long time to compile on first `uv run`.
- Offline environments where `uv` can't reach PyPI.

## Comparison with alternatives

| Approach | Deps installed? | Startup latency | Disk usage |
|----------|----------------|----------------|------------|
| `uv run --with` | No (discarded) | 2-5s first run, cached after | None |
| `pip install --user` | Yes | None after install | Permanent |
| Virtual env | Yes | Activate on use | ~50MB |
| System packages | Yes (apt) | None | ~50-200MB |
