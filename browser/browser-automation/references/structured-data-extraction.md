# Extracting Structured Data from JS-Rendered Pages

When API documentation and pricing pages render their content via JavaScript, `curl` and `wget` return empty or incomplete HTML. Use `agent-browser eval "document.body.innerText"` to extract the rendered text content instead.

## Pattern

```bash
# 1. Close any stale daemon
agent-browser close 2>/dev/null

# 2. Open the target page (with container/VM sandbox flags)
agent-browser --args "--no-sandbox,--disable-gpu,--disable-dev-shm-usage" open "https://example.com/pricing"

# 3. Extract all rendered text
agent-browser eval "document.body.innerText"
```

The output is a single string of all visible text on the page. Pipe through `grep` to extract the specific data you need.

## Extracting Pricing Tables

### Format-agnostic approach
Most pricing pages use a consistent pattern: model name adjacent to dollar amounts. Extract with:

```bash
agent-browser eval "document.body.innerText" | grep -iP 'model|input|output|\$[0-9]+\.[0-9]+|cache'
```

### Known provider techniques

**OpenAI** (`openai.com/api/pricing/`)
- Model names as headings, followed by Input/Cached/Output labeled sections
- Pattern: `"Model Name\n...Input: $X.XX / 1M tokens\nCached input: $X.XX / 1M tokens\nOutput: $X.XX / 1M tokens"`

**Anthropic** (`docs.anthropic.com/en/docs/about-claude/pricing`)
- Table format with columns: Model, Base Input Tokens, 5m Cache Writes, 1h Cache Writes, Cache Hits, Output Tokens
- Cache writes = 1.25x or 2x base. Cache hits = 0.1x base.
- Extract the full text and parse the table structure

**DeepSeek** (`api-docs.deepseek.com/quick_start/pricing`)
- Server-side rendered — `curl` works for this one
- Two-column table: Flash (column 1) and Pro (column 2)
- Pro prices shown with current discount and post-promotion permanent price in same cell
- Format: `$current (discount_note)$permanent`

**Kimi/Moonshot** (`platform.kimi.com/docs/pricing/chat`)
- Chinese-language site. Navigate via snapshot interaction:
  ```bash
  agent-browser snapshot -i                    # find link refs
  agent-browser click @e41                     # click "Kimi K2.6" link
  agent-browser eval "document.body.innerText"  # get the table
  ```
- Pricing in CNY (¥). Convert ~¥7.2 = $1 USD

## Navigation Tricks

If the data you need is behind a click (expandable section, tab, or sub-page):

1. **Snapshot to find interactive elements:** `agent-browser snapshot -i` shows refs like `[ref=e41]` for links and buttons
2. **Click to navigate:** `agent-browser click @e41`
3. **Wait for render:** The page needs a moment after clicking — use `sleep 2` between commands in a batch
4. **Re-eval for the new content:** `agent-browser eval "document.body.innerText"` now returns the clicked-through page

## Caveats

- **Daemon collision:** Always close the daemon first with `agent-browser close 2>/dev/null` before starting a new session with different args
- **Long text output:** `eval` returns the full page text. For very long pages, pipe through `head` to inspect structure first
- **WAF blocking:** Some sites (Cloudflare, Akamai) block headless Chrome. The agent-browser team mitigates this but it's not perfect. If you get an empty response or "Access Denied," try `curl` with realistic headers as fallback
- **Table parsing:** The output is plain text without table borders. You may need to reconstruct table structure from repeated patterns. Model names followed by dollar amounts is the most reliable signal
