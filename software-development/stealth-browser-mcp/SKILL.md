---
name: stealth-browser-mcp
description: MCP server providing browser automation tools that bypass Cloudflare, LinkedIn, Indeed, and other WAF-protected sites using agent-browser with anti-detection stealth.
version: 1.0.0
author: Dustin Chadwick (@ShaggyD)
tags: [browser, automation, stealth, mcp, cloudflare, bypass, agent-browser, web-scraping]
license: MIT
---

# Stealth Browser MCP

An MCP (Model Context Protocol) server that provides browser automation tools with **built-in WAF/Cloudflare bypass**. Uses `agent-browser` CLI with anti-detection Chrome flags and a bundled stealth extension that patches browser fingerprint vectors (`navigator.webdriver`, `plugins`, `languages`, permissions API, etc.).

## How it works

The stealth extension + Chrome flags trick the site into thinking you're a real user on a real Chrome browser:

| Technique | What it does |
|-----------|-------------|
| `--disable-blink-features=AutomationControlled` | Removes Chrome's automation flag |
| Real Chrome 125 user agent | Masks headless browser identity |
| Stealth content script | Patches `navigator.webdriver` → `undefined`, adds plugins, fixes languages |
| Consistent viewport (1920×1080) | Avoids headless screen-size detection |
| Extension loaded at `document_start` | Patches fire before any page JS runs |

## Installation

### 1. Install dependencies

```bash
npm install -g agent-browser
agent-browser install --with-deps
```

### 2. Register the MCP server

```bash
# Find the server script
MCP_SERVER="$HOME/.hermes/skills/software-development/stealth-browser-mcp/assets/mcp_server.py"

# Register with the agent
hermes mcp add stealth-browser --command "python3 $MCP_SERVER"
```

Or add to `config.yaml`:

```yaml
mcp_servers:
  stealth-browser:
    command: python3
    args: ["~/.hermes/skills/software-development/stealth-browser-mcp/assets/mcp_server.py"]
    timeout: 120
```

### 3. Start a fresh session

```bash
hermes chat --reset
```

The stealth browser tools will appear in the agent's tool list automatically.

## Available Tools

| Tool | Description |
|------|-------------|
| `navigate` | Open a URL with full stealth protection |
| `snapshot` | Get page content as readable text |
| `click` | Click an element by accessibility ref ID (e.g., `@e3`) |
| `eval` | Execute JavaScript and return the result |
| `type` | Type text into a form field |
| `set_viewport` | Set viewport dimensions (default 1920×1080) |
| `screenshot` | Take a full-page screenshot (base64) |
| `close` | Close the browser session |
| `status` | Check if agent-browser and Chromium are installed |
| `install` | Install or verify agent-browser + Chromium deps |

## Usage

Once registered, the agent can use the tools naturally:

> "Navigate to https://www.linkedin.com/jobs/search/?keywords=admin&location=Remote"
> "Get the page text"
> "Click @e5 to see job details"
> "Check the stealth browser status"

### Typical workflow

1. `navigate` to the target URL
2. `snapshot` to see page content with element refs (shown as `@e1`, `@e2`, etc.)
3. `click` on elements to interact, expand, or navigate further
4. `eval` to extract structured data (pricing, job listings, search results)
5. `screenshot` for visual confirmation
6. `close` when done

## Job Search Example (LinkedIn, no login)

```python
# 1. Navigate to LinkedIn jobs
navigate("https://www.linkedin.com/jobs/search/?keywords=front+office+coordinator&location=American+Fork%2C+Utah&f_TPR=r604800")

# 2. Extract job listings
eval("""
JSON.stringify(
  Array.from(document.querySelectorAll('.job-card-container')).map(c => ({
    title: c.querySelector('.job-card-list__title')?.innerText?.trim(),
    company: c.querySelector('.job-card-container__company-name')?.innerText?.trim(),
    location: c.querySelector('.job-card-container__metadata-item')?.innerText?.trim(),
    link: c.querySelector('a')?.href
  }))
)
""")

# 3. Click into a specific job
click("@e3")

# 4. Get full description
snapshot()
```

## Self-Contained

The MCP server is fully self-contained — the stealth extension JS and manifest are bundled inline in the Python script. On startup, it extracts them to a temporary directory. No external skill or file dependencies.

## Requirements

- Python 3.10+
- `mcp` package (`pip install mcp`)
- `agent-browser` CLI + Chromium (`npm install -g agent-browser && agent-browser install --with-deps`)
