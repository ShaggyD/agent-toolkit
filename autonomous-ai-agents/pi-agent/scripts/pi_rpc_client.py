#!/usr/bin/env python3
"""Minimal pi RPC client for durable multi-turn sessions.

Usage examples:
  python pi_rpc_client.py --self-check
  python pi_rpc_client.py --workdir ~/code/my-project --prompt "Audit this repo"
  python pi_rpc_client.py --session /path/to/session.jsonl --workdir ~/code/my-project --prompt "Continue"
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import threading
import queue
from typing import Any, Dict, Optional


class PiRpcClient:
    def __init__(self, session_path: Optional[str] = None, workdir: Optional[str] = None):
        cmd = ["pi", "--mode", "rpc"]
        if session_path:
            cmd += ["--session", session_path]

        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=workdir,
        )

        if not self.proc.stdin or not self.proc.stdout:
            raise RuntimeError("Failed to open pi RPC stdio")

        self._q: "queue.Queue[Dict[str, Any]]" = queue.Queue()
        self._reader = threading.Thread(target=self._read_loop, daemon=True)
        self._reader.start()

    def _read_loop(self) -> None:
        assert self.proc.stdout is not None
        for line in self.proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                self._q.put(json.loads(line))
            except json.JSONDecodeError:
                # Ignore non-JSON noise safely
                continue

    def send(self, payload: Dict[str, Any]) -> None:
        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps(payload) + "\n")
        self.proc.stdin.flush()

    def recv_until_response(self, command: str, timeout_s: float = 60.0) -> Dict[str, Any]:
        """Collect events until response for a given command arrives."""
        import time

        deadline = time.time() + timeout_s
        while time.time() < deadline:
            try:
                evt = self._q.get(timeout=0.2)
            except queue.Empty:
                continue
            if evt.get("type") == "response" and evt.get("command") == command:
                return evt
        raise TimeoutError(f"Timed out waiting for response to command={command}")

    def get_state(self) -> Dict[str, Any]:
        self.send({"type": "get_state"})
        return self.recv_until_response("get_state")

    def prompt(self, text: str) -> Dict[str, Any]:
        self.send({"type": "prompt", "message": text})
        return self.recv_until_response("prompt", timeout_s=300.0)

    def close(self) -> None:
        if self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()


def run_self_check() -> int:
    p = subprocess.run(["pi", "--mode", "rpc", "--help"], capture_output=True, text=True)
    if p.returncode != 0:
        print("SELF_CHECK_FAIL: pi rpc help failed", file=sys.stderr)
        print(p.stderr, file=sys.stderr)
        return p.returncode
    print("SELF_CHECK_OK")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--session", default=None, help="Path to existing pi session JSONL")
    ap.add_argument("--workdir", default=None, help="Project directory to start pi in")
    ap.add_argument("--prompt", default=None, help="Prompt to send")
    ap.add_argument("--self-check", action="store_true", help="Run basic installation check")
    args = ap.parse_args()

    if args.self_check:
        return run_self_check()

    client = PiRpcClient(session_path=args.session, workdir=args.workdir)
    try:
        state = client.get_state()
        session_file = state.get("data", {}).get("sessionFile")
        print(json.dumps({"sessionFile": session_file}, indent=2))

        if args.prompt:
            resp = client.prompt(args.prompt)
            print(json.dumps(resp, indent=2))
    finally:
        client.close()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
