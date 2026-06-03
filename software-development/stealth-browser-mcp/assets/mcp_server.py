#!/usr/bin/env python3
"""
Stealth Browser MCP Server

Provides browser automation tools that bypass Cloudflare, LinkedIn, Indeed, and
other WAF-protected sites using agent-browser CLI with anti-detection flags
and a stealth extension that patches browser fingerprinting vectors.

The stealth extension and Chrome flags are bundled — no external skill dependency.
On startup the extension is extracted to a temp directory.

Requirements:
    - Python 3.10+
    - mcp package (pip install mcp)
    - agent-browser CLI (npm install -g agent-browser)

Installation:
    hermes mcp add stealth-browser --command "python /path/to/mcp_server.py"

    Or in config.yaml:
        mcp_servers:
          stealth-browser:
            command: python
            args: ["/path/to/mcp_server.py"]
            timeout: 120
"""

from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path
from typing import Any
from mcp.server.fastmcp import FastMCP

# ---------------------------------------------------------------------------
# Stealth Extension (bundled inline — self-contained)
# ---------------------------------------------------------------------------
# Patches navigator.webdriver, plugins, languages, permissions, chrome.runtime,
# webdriver flags, and screen metrics before any page scripts run.

STEALTH_EXTENSION_MANIFEST = json.dumps(
    {
        "name": "Hermes Stealth",
        "version": "1.0.0",
        "description": "Bypass bot detection by patching browser fingerprint vectors.",
        "manifest_version": 3,
        "content_scripts": [
            {
                "matches": ["<all_urls>"],
                "js": ["stealth.js"],
                "run_at": "document_start",
                "all_frames": True,
                "match_origin_as_fallback": True,
            }
        ],
        "permissions": [],
        "host_permissions": ["<all_urls>"],
    },
    indent=2,
)

STEALTH_EXTENSION_JS = r"""
// Hermes Stealth — patches browser fingerprint vectors at document_start
(function() {
    const DEFAULT_LANGUAGES = ['en-US', 'en'];
    const DEFAULT_PLUGINS = [
        { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
        { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
        { name: 'Native Client', filename: 'internal-nacl-plugin' },
        { name: 'Widevine Content Decryption Module', filename: 'widevinecdm' },
    ];

    // 1. Override navigator.webdriver
    const webdriverGetter = Object.getOwnPropertyDescriptor(
        Navigator.prototype, 'webdriver'
    );
    if (webdriverGetter) {
        Object.defineProperty(Navigator.prototype, 'webdriver', {
            get: () => undefined,
            configurable: true,
        });
    }
    // Also patch direct property if set
    if (navigator.webdriver !== undefined) {
        try {
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
                configurable: true,
            });
        } catch (_) {}
    }

    // 2. Override navigator.plugins
    try {
        Object.defineProperty(Navigator.prototype, 'plugins', {
            get: () => {
                const arr = [];
                for (const p of DEFAULT_PLUGINS) {
                    try {
                        const plugin = new Plugin(p.name, p.filename);
                        arr.push(plugin);
                    } catch (_) {}
                }
                arr.item = (i) => arr[i] || null;
                arr.namedItem = (n) => arr.find(p => p.name === n) || null;
                arr.length = arr.length || DEFAULT_PLUGINS.length;
                return arr;
            },
            configurable: true,
        });
    } catch (_) {}

    // 3. Override navigator.languages
    try {
        Object.defineProperty(Navigator.prototype, 'languages', {
            get: () => [...DEFAULT_LANGUAGES],
            configurable: true,
        });
    } catch (_) {}

    // 4. Override navigator.language
    try {
        Object.defineProperty(Navigator.prototype, 'language', {
            get: () => DEFAULT_LANGUAGES[0],
            configurable: true,
        });
    } catch (_) {}

    // 5. Override Permissions API (always prompt to avoid automated detection)
    if (navigator.permissions && navigator.permissions.query) {
        const origQuery = navigator.permissions.query.bind(navigator.permissions);
        navigator.permissions.query = (desc) => {
            if (desc && (desc.name === 'notifications' || desc.name === 'geolocation')) {
                return Promise.resolve({ state: 'prompt', onchange: null });
            }
            return origQuery(desc);
        };
    }

    // 6. Remove webdriver-related attributes from <html>
    try {
        document.documentElement.removeAttribute('webdriver');
    } catch (_) {}

    // 7. Patch chrome.runtime if accessible from content script
    try {
        if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.id) {
            // Keep it — legitimate extensions expose this
        }
    } catch (_) {}

    // 8. Mock screen metrics for consistency
    try {
        // Some headless detections check screen dimensions vs viewport
        if (screen.width === 800 && screen.height === 600) {
            Object.defineProperty(screen, 'width', { get: () => 1920, configurable: true });
            Object.defineProperty(screen, 'height', { get: () => 1080, configurable: true });
            Object.defineProperty(screen, 'availWidth', { get: () => 1920, configurable: true });
            Object.defineProperty(screen, 'availHeight', { get: () => 1040, configurable: true });
        }
    } catch (_) {}
})();
"""

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

STEALTH_EXTENSION_DIR: str | None = None  # set by _setup_extension()

# Default stealth Chrome flags
DEFAULT_CHROME_ARGS = [
    "--no-sandbox",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--disable-blink-features=AutomationControlled",
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-sync",
    "--disable-background-networking",
]

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/125.0.0.0 Safari/537.36"
)

# ---------------------------------------------------------------------------
# Setup helpers
# ---------------------------------------------------------------------------


def _setup_extension() -> str:
    """Write bundled stealth extension to a temp directory and return its path."""
    ext_dir = tempfile.mkdtemp(prefix="stealth_ext_")
    manifest_path = os.path.join(ext_dir, "manifest.json")
    js_path = os.path.join(ext_dir, "stealth.js")

    with open(manifest_path, "w") as f:
        f.write(STEALTH_EXTENSION_MANIFEST)
    # Strip leading newline from the JS constant
    js = STEALTH_EXTENSION_JS.lstrip("\n")
    with open(js_path, "w") as f:
        f.write(js)

    return ext_dir


def _find_agent_browser() -> str | None:
    """Locate agent-browser CLI on PATH or common install locations."""
    # Try PATH first
    exe = shutil.which("agent-browser")
    if exe:
        return exe

    # Check common npx locations
    npx = shutil.which("npx")
    if npx:
        return f"{npx} agent-browser"

    # Hermes bundled location
    hermes_home = os.environ.get("HERMES_HOME") or os.path.expanduser("~/.hermes")
    candidate = os.path.join(hermes_home, "hermes-agent", "node_modules", ".bin", "agent-browser")
    if os.path.isfile(candidate):
        return candidate

    return None


def _check_chromium() -> tuple[bool, str]:
    """Check if Chromium is available for agent-browser."""
    try:
        ab = _find_agent_browser()
        if not ab:
            return False, "agent-browser CLI not found. Install: npm install -g agent-browser"
        # Run agent-browser doctor to check deps
        if " " in ab:
            parts = ab.split()
            result = subprocess.run([*parts, "doctor"], capture_output=True, text=True, timeout=30)
        else:
            result = subprocess.run([ab, "doctor"], capture_output=True, text=True, timeout=30)
        stdout = (result.stdout or "") + (result.stderr or "")
        if "chromium is installed" in stdout.lower() or "chromium" in stdout.lower():
            return True, ""
        return False, "Chromium not found. Run: agent-browser install --with-deps"
    except FileNotFoundError:
        return False, "agent-browser CLI not found. Install: npm install -g agent-browser"
    except subprocess.TimeoutExpired:
        return False, "agent-browser doctor timed out"
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# Browser session manager
# ---------------------------------------------------------------------------

_browser_lock = threading.Lock()
_browser_session: str | None = None  # current session name
_browser_pid: int | None = None      # PID tracker for cleanup


def _run_ab(command: str, *args: str, timeout: int = 60) -> dict[str, Any]:
    """Execute an agent-browser command with stealth flags.

    Returns parsed dict with keys: success, data, error
    """
    global _browser_session

    agent_browser = _find_agent_browser()
    if not agent_browser:
        return {"success": False, "error": "agent-browser CLI not found. Install: npm install -g agent-browser"}

    # Build cmd: [agent-browser, --session <name>, --args "...", --user-agent "...", --extension "...", --json, command, ...args]
    if " " in agent_browser:
        cmd_parts = agent_browser.split()
    else:
        cmd_parts = [agent_browser]

    # Session
    if _browser_session:
        cmd_parts.extend(["--session", _browser_session])
    else:
        # Create new session name
        _browser_session = f"stealth_{int(time.time())}"
        cmd_parts.extend(["--session", _browser_session])

    # Stealth flags
    chrome_args = ",".join(DEFAULT_CHROME_ARGS)
    cmd_parts.extend([
        "--args", chrome_args,
        "--user-agent", DEFAULT_USER_AGENT,
    ])

    # Extension
    global STEALTH_EXTENSION_DIR
    if STEALTH_EXTENSION_DIR and os.path.isdir(STEALTH_EXTENSION_DIR):
        cmd_parts.extend(["--extension", STEALTH_EXTENSION_DIR])

    # JSON output + command
    cmd_parts.append("--json")
    cmd_parts.append(command)
    cmd_parts.extend(args)

    try:
        result = subprocess.run(
            cmd_parts,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()

        if result.returncode != 0:
            # close is a special case - it can fail if no daemon
            if command == "close":
                return {"success": True, "data": {"closed": True}}
            error_msg = stderr or stdout or f"Exit code {result.returncode}"
            return {"success": False, "error": error_msg}

        # Parse JSON output
        if stdout:
            try:
                raw = json.loads(stdout)
                # agent-browser --json wraps results in {"success":true,"data":...,"error":null}
                # Unwrap so tool handlers get the inner data directly
                inner_data = raw.get("data") if isinstance(raw, dict) else raw
                inner_success = raw.get("success", True) if isinstance(raw, dict) else True
                return {"success": inner_success, "data": inner_data}
            except json.JSONDecodeError:
                return {"success": True, "data": {"text": stdout}}
        return {"success": True, "data": {"text": stdout or "(empty)"}}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Command timed out after {timeout}s"}
    except FileNotFoundError:
        return {"success": False, "error": "agent-browser CLI not found"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _close_session() -> dict[str, Any]:
    """Close the current browser daemon."""
    global _browser_session
    if not _browser_session:
        return {"success": True, "data": {"closed": True, "note": "no active session"}}

    # Try close first, then session reset
    _run_ab("close", timeout=15)
    _browser_session = None
    return {"success": True, "data": {"closed": True}}


# ---------------------------------------------------------------------------
# MCP Server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    "Stealth Browser",
    instructions=(
        "Browser automation tools that bypass Cloudflare, LinkedIn, Indeed, and "
        "other WAF-protected sites. Uses agent-browser CLI with anti-detection "
        "Chrome flags and a stealth extension patching browser fingerprint vectors."
    ),
)


@mcp.tool(
    name="navigate",
    description="Navigate to a URL using the stealth browser. Opens a headless Chrome session with anti-detection patching.",
)
def navigate(url: str) -> str:
    """Open a URL in the stealth browser."""
    with _browser_lock:
        result = _run_ab("open", url)
    if result["success"]:
        data = result.get("data", {})
        title = data.get("title", "") if isinstance(data, dict) else ""
        # Also set a realistic viewport
        with _browser_lock:
            _run_ab("set", "viewport", "1920", "1080", timeout=10)
        return f"Navigated to {url}" + (f" — {title}" if title else "")
    return f"Navigation failed: {result.get('error', 'unknown error')}"


@mcp.tool(
    name="snapshot",
    description="Get the current page content as readable text. Returns the rendered text of the page.",
)
def snapshot() -> str:
    """Get the rendered page text content."""
    with _browser_lock:
        result = _run_ab("eval", "document.body.innerText")
    if result["success"]:
        data = result.get("data", {})
        if isinstance(data, dict):
            text = data.get("result", data.get("text", ""))
        else:
            text = str(data)
        # Truncate very long output
        if len(text) > 20000:
            text = text[:20000] + f"\n... [truncated {len(text) - 20000} more chars]"
        return text or "(empty page)"
    return f"Snapshot failed: {result.get('error', 'unknown error')}"


@mcp.tool(
    name="click",
    description="Click an element identified by its accessibility ref ID (e.g., '@e3', '@e12'). Get refs from snapshot first.",
)
def click(ref: str) -> str:
    """Click an element by ref."""
    with _browser_lock:
        result = _run_ab("click", ref)
    if result["success"]:
        return f"Clicked {ref}"
    return f"Click failed: {result.get('error', 'unknown error')}"


@mcp.tool(
    name="eval",
    description="Execute JavaScript in the page context and return the result. Use for extracting data, checking page state, or interacting with the DOM.",
)
def eval_js(script: str) -> str:
    """Execute JavaScript in the page."""
    with _browser_lock:
        result = _run_ab("eval", script)
    if result["success"]:
        data = result.get("data", {})
        if isinstance(data, dict):
            text = data.get("result", data.get("text", ""))
        else:
            text = str(data)
        if len(text) > 15000:
            text = text[:15000] + f"\n... [truncated {len(text) - 15000} more chars]"
        return text or "(empty result)"
    return f"Eval failed: {result.get('error', 'unknown error')}"


@mcp.tool(
    name="type",
    description="Type text into an input field identified by its ref ID (e.g., '@e3'). Clears the field first.",
)
def type_text(ref: str, text: str) -> str:
    """Type text into a field by ref."""
    with _browser_lock:
        result = _run_ab("fill", ref, text)
    if result["success"]:
        return f"Typed into {ref}"
    # Fallback: try type instead of fill
    with _browser_lock:
        result2 = _run_ab("type", ref, text)
    if result2["success"]:
        return f"Typed into {ref}"
    return f"Type failed: {result2.get('error', 'unknown error')}"


@mcp.tool(
    name="set_viewport",
    description="Set the browser viewport dimensions (width x height). Default is 1920x1080.",
)
def set_viewport(width: int = 1920, height: int = 1080) -> str:
    """Set the viewport size."""
    with _browser_lock:
        result = _run_ab("set", "viewport", str(width), str(height), timeout=10)
    if result["success"]:
        return f"Viewport set to {width}x{height}"
    return f"set_viewport failed: {result.get('error', 'unknown error')}"


@mcp.tool(
    name="screenshot",
    description="Take a screenshot of the current page. Returns a base64-encoded PNG image.",
)
def screenshot() -> str:
    """Take a page screenshot (base64 PNG)."""
    with _browser_lock:
        result = _run_ab("screenshot", "--full", timeout=30)
    if result["success"]:
        data = result.get("data", {})
        # Screenshots are saved to disk by agent-browser; the JSON might contain a path
        if isinstance(data, dict) and "result" in data:
            path = data["result"].strip()
            if os.path.isfile(path):
                with open(path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()
                try:
                    os.remove(path)
                except OSError:
                    pass
                return f"data:image/png;base64,{b64}"
        return str(data)
    return f"Screenshot failed: {result.get('error', 'unknown error')}"


@mcp.tool(
    name="close",
    description="Close the stealth browser session. Call this when you're done browsing to free resources.",
)
def close_browser() -> str:
    """Close the browser daemon."""
    with _browser_lock:
        result = _close_session()
    if result["success"]:
        return "Browser session closed"
    return f"Close failed: {result.get('error', 'unknown error')}"


@mcp.tool(
    name="status",
    description="Check if the stealth browser is installed and ready. Reports agent-browser and Chromium availability.",
)
def check_status() -> str:
    """Check browser installation status."""
    ab = _find_agent_browser()
    if not ab:
        return "❌ agent-browser not installed. Run: npm install -g agent-browser && agent-browser install --with-deps"

    chrom_ok, chrom_msg = _check_chromium()
    lines = [
        f"✅ agent-browser found: {ab}",
        f"{'✅' if chrom_ok else '❌'} Chromium: {'installed' if chrom_ok else chrom_msg}",
    ]
    if _browser_session:
        lines.append(f"🔵 Active session: {_browser_session}")
    else:
        lines.append("⚪ No active session")
    return "\n".join(lines)


@mcp.tool(
    name="install",
    description="Install or verify agent-browser and Chromium dependencies. Pass force=True to reinstall.",
)
def install_browser(force: bool = False) -> str:
    """Install/check agent-browser and Chromium."""
    ab = _find_agent_browser()
    if not ab or force:
        try:
            subprocess.run(
                ["npm", "install", "-g", "agent-browser"],
                capture_output=True, text=True, timeout=120,
            )
        except Exception as e:
            return f"npm install failed: {e}"

    # Install Chromium
    ab = _find_agent_browser()
    if not ab:
        return "agent-browser not found after install attempt"

    try:
        if " " in ab:
            parts = ab.split()
            result = subprocess.run(
                [*parts, "install", "--with-deps"],
                capture_output=True, text=True, timeout=300,
            )
        else:
            result = subprocess.run(
                [ab, "install", "--with-deps"],
                capture_output=True, text=True, timeout=300,
            )
        stdout = (result.stdout or "") + (result.stderr or "")
        if result.returncode != 0:
            return f"Install may have issues:\n{stdout[-1000:]}"
        return f"✅ agent-browser and Chromium ready.\n{stdout[-500:]}" if stdout else "✅ Ready"
    except subprocess.TimeoutExpired:
        return "Install timed out (this can take a while on first run). Check with `agent-browser doctor`."
    except Exception as e:
        return f"Install error: {e}"


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Initialize stealth extension and run the MCP server."""
    global STEALTH_EXTENSION_DIR

    # Set up bundled stealth extension
    STEALTH_EXTENSION_DIR = _setup_extension()

    # Quick check: skip doctor if env says so (avoids slowdown on every hermes start)
    if not os.environ.get("STEALTH_BROWSER_SKIP_CHECK"):
        ab = _find_agent_browser()
        if not ab:
            print(
                "⚠️  agent-browser not found. Install: npm install -g agent-browser",
                file=sys.stderr,
            )

    # Run stdio-based MCP server
    try:
        mcp.run(transport="stdio")
    finally:
        # Clean up temp extension dir
        if STEALTH_EXTENSION_DIR and os.path.isdir(STEALTH_EXTENSION_DIR):
            try:
                shutil.rmtree(STEALTH_EXTENSION_DIR, ignore_errors=True)
            except Exception:
                pass


if __name__ == "__main__":
    main()
