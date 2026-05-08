from __future__ import annotations

import json
import shutil
import subprocess
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Deque, Dict, Optional

from hermes_constants import get_hermes_home
from tools.registry import registry


PI_RPC_SCHEMA: Dict[str, Any] = {
    "name": "pi_agent",
    "description": (
        "Stateful controller for pi --mode rpc sessions bound to project directories. "
        "Use action='start' to open a session, action='send' to send prompts/commands, "
        "action='poll' to fetch new events, action='wait' to wait for turn completion, "
        "action='list' to view sessions, and action='stop' to terminate a session."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["start", "resume", "send", "poll", "wait", "stop", "list", "prune"],
                "description": "Action to perform",
            },
            "session_id": {
                "type": "string",
                "description": "Required for send/poll/wait/stop",
            },
            "workdir": {
                "type": "string",
                "description": "Project directory where pi session should run (start only)",
            },
            "pi_session_path": {
                "type": "string",
                "description": "Optional pi --session path to resume exact prior pi conversation (start only)",
            },
            "provider": {
                "type": "string",
                "description": "Optional --provider override for pi start",
            },
            "model": {
                "type": "string",
                "description": "Optional --model override for pi start",
            },
            "message": {
                "type": "string",
                "description": "Prompt text for action='send'",
            },
            "command": {
                "type": "object",
                "description": "Raw RPC command object for action='send' (alternative to message)",
            },
            "request_id": {
                "type": "string",
                "description": "Optional correlation id for send/wait",
            },
            "offset": {
                "type": "integer",
                "description": "For poll: first event index to return (default: session cursor)",
            },
            "limit": {
                "type": "integer",
                "description": "For poll: max events to return (default 100, max 500)",
            },
            "timeout_seconds": {
                "type": "integer",
                "description": "For wait: max seconds to block (default 60, max 600)",
            },
            "until_event": {
                "type": "string",
                "description": "For wait: event type to stop on (default: turn_end)",
            },
            "max_age_days": {
                "type": "integer",
                "description": "For prune: remove detached sessions older than this many days (default 7)",
            },
        },
        "required": ["action"],
    },
}


@dataclass
class PiRpcSession:
    proc: Optional[subprocess.Popen]
    workdir: Optional[str]
    cmd: list[str]
    created_at: float = field(default_factory=time.time)
    events: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=4000))
    event_count: int = 0
    cursor: int = 1
    lock: threading.Lock = field(default_factory=threading.Lock)
    session_file: Optional[str] = None
    detached: bool = False


_SESSIONS: Dict[str, PiRpcSession] = {}
_STATE_PATH = get_hermes_home() / "state" / "pi_agent_sessions.json"


def _persist_sessions() -> None:
    _STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "sessions": {
            sid: {
                "workdir": s.workdir,
                "cmd": s.cmd,
                "created_at": s.created_at,
                "session_file": s.session_file,
                "detached": s.detached,
                "running": (s.proc.poll() is None) if s.proc else False,
                "exit_code": s.proc.poll() if s.proc else None,
                "events_seen": s.event_count,
            }
            for sid, s in _SESSIONS.items()
        }
    }
    tmp = _STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    tmp.replace(_STATE_PATH)


def _load_sessions() -> None:
    if not _STATE_PATH.exists():
        return
    try:
        payload = json.loads(_STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return
    for sid, raw in (payload.get("sessions") or {}).items():
        _SESSIONS[sid] = PiRpcSession(
            proc=None,
            workdir=raw.get("workdir"),
            cmd=list(raw.get("cmd") or ["pi", "--mode", "rpc"]),
            created_at=float(raw.get("created_at") or time.time()),
            session_file=raw.get("session_file"),
            detached=True,
        )


def _reader_loop(session_id: str, stream_name: str, stream) -> None:
    while True:
        line = stream.readline()
        if line == "":
            break
        line = line.rstrip("\n")
        if not line:
            continue
        payload: Dict[str, Any]
        try:
            payload = json.loads(line)
        except Exception:
            payload = {"type": "raw", "stream": stream_name, "line": line}

        s = _SESSIONS.get(session_id)
        if s is None:
            break
        with s.lock:
            s.event_count += 1
            idx = s.event_count
            payload = {"index": idx, **payload}
            s.events.append(payload)
            if payload.get("type") == "response" and payload.get("command") == "get_state":
                sf = payload.get("data", {}).get("sessionFile")
                if isinstance(sf, str) and sf:
                    s.session_file = sf
        _persist_sessions()


def _check_pi_available() -> bool:
    return shutil.which("pi") is not None


def _is_live(s: PiRpcSession) -> bool:
    return bool(s.proc and s.proc.poll() is None and not s.detached)


def _start_session(args: Dict[str, Any]) -> Dict[str, Any]:
    workdir = args.get("workdir")
    pi_session_path = args.get("pi_session_path")
    provider = args.get("provider")
    model = args.get("model")

    cmd = ["pi", "--mode", "rpc"]
    if pi_session_path:
        cmd += ["--session", str(pi_session_path)]
    if provider:
        cmd += ["--provider", str(provider)]
    if model:
        cmd += ["--model", str(model)]

    proc = subprocess.Popen(
        cmd,
        cwd=workdir or None,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )

    if not proc.stdin or not proc.stdout or not proc.stderr:
        return {"success": False, "error": "Failed to initialize pi stdio streams"}

    sid = f"pi_agent_{uuid.uuid4().hex[:10]}"
    session = PiRpcSession(proc=proc, workdir=workdir, cmd=cmd)
    _SESSIONS[sid] = session

    t_out = threading.Thread(target=_reader_loop, args=(sid, "stdout", proc.stdout), daemon=True)
    t_err = threading.Thread(target=_reader_loop, args=(sid, "stderr", proc.stderr), daemon=True)
    t_out.start()
    t_err.start()

    proc.stdin.write(json.dumps({"type": "get_state"}) + "\n")
    proc.stdin.flush()
    _persist_sessions()

    return {
        "success": True,
        "session_id": sid,
        "pid": proc.pid,
        "workdir": workdir,
        "cmd": cmd,
        "message": "pi rpc session started",
    }


def _resume_session(args: Dict[str, Any]) -> Dict[str, Any]:
    sid = args.get("session_id")
    if not sid or sid not in _SESSIONS:
        return {"success": False, "error": "session_id not found"}
    old = _SESSIONS[sid]
    if not old.detached and _is_live(old):
        return {"success": True, "session_id": sid, "message": "session already live"}

    if not old.session_file:
        # Fallback: no persisted session file (e.g. minimal output env/test harness).
        # Start a fresh live rpc process in the same workdir.
        started = _start_session(
            {
                "workdir": args.get("workdir") or old.workdir,
                "provider": args.get("provider"),
                "model": args.get("model"),
            }
        )
        if not started.get("success"):
            return started
        started["resumed_from"] = sid
        started["warning"] = "resumed without session_file; started a fresh rpc process"
        return started

    started = _start_session(
        {
            "workdir": args.get("workdir") or old.workdir,
            "pi_session_path": old.session_file,
            "provider": args.get("provider"),
            "model": args.get("model"),
        }
    )
    if not started.get("success"):
        return started
    new_sid = started["session_id"]
    new_s = _SESSIONS[new_sid]
    new_s.cursor = max(old.cursor, 1)
    started["resumed_from"] = sid
    return started


def _send(args: Dict[str, Any]) -> Dict[str, Any]:
    sid = args.get("session_id")
    if not sid or sid not in _SESSIONS:
        return {"success": False, "error": "session_id not found"}
    s = _SESSIONS[sid]

    if not _is_live(s):
        return {"success": False, "error": "session is not live (detached or stopped)"}

    cmd_obj = args.get("command")
    if cmd_obj is None:
        message = args.get("message")
        if not message:
            return {"success": False, "error": "Provide message or command for action=send"}
        cmd_obj = {"type": "prompt", "message": str(message)}

    if not isinstance(cmd_obj, dict):
        return {"success": False, "error": "command must be a JSON object"}

    request_id = str(args.get("request_id") or uuid.uuid4().hex)
    cmd_obj.setdefault("request_id", request_id)

    assert s.proc and s.proc.stdin is not None
    s.proc.stdin.write(json.dumps(cmd_obj) + "\n")
    s.proc.stdin.flush()
    return {"success": True, "session_id": sid, "request_id": request_id, "sent": cmd_obj}


def _poll(args: Dict[str, Any]) -> Dict[str, Any]:
    sid = args.get("session_id")
    if not sid or sid not in _SESSIONS:
        return {"success": False, "error": "session_id not found"}

    s = _SESSIONS[sid]
    limit = min(max(int(args.get("limit", 100)), 1), 500)
    offset = args.get("offset")

    with s.lock:
        evts = list(s.events)
        start_idx = int(offset) if offset is not None else s.cursor
        filtered = [e for e in evts if int(e.get("index", 0)) >= start_idx]
        out = filtered[:limit]
        next_offset = (out[-1]["index"] + 1) if out else start_idx
        if offset is None:
            s.cursor = next_offset

    return {
        "success": True,
        "session_id": sid,
        "detached": s.detached,
        "running": _is_live(s),
        "exit_code": s.proc.poll() if s.proc else None,
        "session_file": s.session_file,
        "events": out,
        "returned": len(out),
        "next_offset": next_offset,
        "total_seen": s.event_count,
    }


def _wait(args: Dict[str, Any]) -> Dict[str, Any]:
    sid = args.get("session_id")
    if not sid or sid not in _SESSIONS:
        return {"success": False, "error": "session_id not found"}
    s = _SESSIONS[sid]
    timeout = min(max(int(args.get("timeout_seconds", 60)), 1), 600)
    until_event = str(args.get("until_event") or "turn_end")
    request_id = args.get("request_id")

    deadline = time.time() + timeout
    start_offset = int(args.get("offset") or s.cursor)
    current = start_offset
    matched: list[Dict[str, Any]] = []

    while time.time() < deadline:
        polled = _poll({"session_id": sid, "offset": current, "limit": 500})
        if not polled.get("success"):
            return polled
        events = polled.get("events", [])
        for evt in events:
            if request_id and evt.get("request_id") != request_id:
                continue
            matched.append(evt)
            if evt.get("type") == until_event:
                s.cursor = int(evt.get("index", current)) + 1
                return {
                    "success": True,
                    "session_id": sid,
                    "request_id": request_id,
                    "matched_event": evt,
                    "events": matched,
                    "next_offset": s.cursor,
                    "timed_out": False,
                }

        current = int(polled.get("next_offset", current))
        if s.proc and s.proc.poll() is not None and not events:
            break
        time.sleep(0.1)

    s.cursor = current
    return {
        "success": True,
        "session_id": sid,
        "request_id": request_id,
        "events": matched,
        "next_offset": current,
        "timed_out": True,
    }


def _stop(args: Dict[str, Any]) -> Dict[str, Any]:
    sid = args.get("session_id")
    if not sid or sid not in _SESSIONS:
        return {"success": False, "error": "session_id not found"}

    s = _SESSIONS[sid]
    if s.proc and s.proc.poll() is None:
        s.proc.terminate()
        try:
            s.proc.wait(timeout=3)
        except subprocess.TimeoutExpired:
            s.proc.kill()

    code = s.proc.poll() if s.proc else None
    del _SESSIONS[sid]
    _persist_sessions()
    return {"success": True, "session_id": sid, "exit_code": code}


def _list_sessions() -> Dict[str, Any]:
    items = []
    for sid, s in _SESSIONS.items():
        items.append(
            {
                "session_id": sid,
                "pid": s.proc.pid if s.proc else None,
                "running": _is_live(s),
                "exit_code": s.proc.poll() if s.proc else None,
                "workdir": s.workdir,
                "session_file": s.session_file,
                "events_seen": s.event_count,
                "created_at": s.created_at,
                "detached": s.detached,
            }
        )
    return {"success": True, "sessions": items, "count": len(items)}


def _prune_sessions(args: Dict[str, Any]) -> Dict[str, Any]:
    max_age_days = max(int(args.get("max_age_days", 7)), 0)
    cutoff = time.time() - (max_age_days * 86400)
    removed: list[str] = []
    for sid in list(_SESSIONS.keys()):
        s = _SESSIONS[sid]
        if not s.detached:
            continue
        if s.created_at > cutoff:
            continue
        del _SESSIONS[sid]
        removed.append(sid)
    _persist_sessions()
    return {
        "success": True,
        "removed": removed,
        "removed_count": len(removed),
        "max_age_days": max_age_days,
    }


def pi_agent(args: Dict[str, Any], **kwargs) -> str:
    action = (args or {}).get("action", "").strip().lower()

    try:
        if action == "start":
            result = _start_session(args)
        elif action == "resume":
            result = _resume_session(args)
        elif action == "send":
            result = _send(args)
        elif action == "poll":
            result = _poll(args)
        elif action == "wait":
            result = _wait(args)
        elif action == "stop":
            result = _stop(args)
        elif action == "list":
            result = _list_sessions()
        elif action == "prune":
            result = _prune_sessions(args)
        else:
            result = {
                "success": False,
                "error": "Invalid action. Use one of: start, resume, send, poll, wait, stop, list, prune",
            }
    except Exception as e:
        result = {"success": False, "error": str(e)}

    return json.dumps(result)


_load_sessions()

registry.register(
    name="pi_agent",
    toolset="terminal",
    schema=PI_RPC_SCHEMA,
    handler=pi_agent,
    check_fn=_check_pi_available,
    requires_env=[],
    emoji="🤖",
)
