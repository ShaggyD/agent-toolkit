from __future__ import annotations

import importlib
import json
import time


class _FakeStdin:
    def __init__(self):
        self.writes: list[str] = []

    def write(self, s: str):
        self.writes.append(s)

    def flush(self):
        return None


class _FakeStream:
    def readline(self):
        return ""


class _FakePopen:
    _pid = 5000

    def __init__(self, *args, **kwargs):
        type(self)._pid += 1
        self.pid = type(self)._pid
        self.stdin = _FakeStdin()
        self.stdout = _FakeStream()
        self.stderr = _FakeStream()
        self._rc = None

    def poll(self):
        return self._rc

    def terminate(self):
        self._rc = -15

    def wait(self, timeout=None):
        if self._rc is None:
            self._rc = 0
        return self._rc

    def kill(self):
        self._rc = -9


class _FakeThread:
    def __init__(self, *args, **kwargs):
        pass

    def start(self):
        return None


def _reload_tool(monkeypatch, tmp_path):
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / ".hermes"))
    import tools.pi_agent_tool as mod

    return importlib.reload(mod)


def test_start_send_poll_stop_and_persistence(monkeypatch, tmp_path):
    mod = _reload_tool(monkeypatch, tmp_path)
    monkeypatch.setattr(mod.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(mod.threading, "Thread", _FakeThread)

    started = json.loads(mod.pi_agent({"action": "start", "workdir": "/tmp/project"}))
    assert started["success"] is True
    sid = started["session_id"]

    listed = json.loads(mod.pi_agent({"action": "list"}))
    assert listed["count"] == 1
    assert listed["sessions"][0]["session_id"] == sid
    assert listed["sessions"][0]["running"] is True

    sent = json.loads(mod.pi_agent({"action": "send", "session_id": sid, "message": "hello"}))
    assert sent["success"] is True
    assert sent["request_id"]
    assert sent["sent"]["request_id"] == sent["request_id"]

    polled = json.loads(mod.pi_agent({"action": "poll", "session_id": sid}))
    assert polled["success"] is True
    assert polled["next_offset"] >= 1

    state_file = tmp_path / ".hermes" / "state" / "pi_agent_sessions.json"
    assert state_file.exists()

    stopped = json.loads(mod.pi_agent({"action": "stop", "session_id": sid}))
    assert stopped["success"] is True


def test_wait_returns_on_matching_event(monkeypatch, tmp_path):
    mod = _reload_tool(monkeypatch, tmp_path)
    monkeypatch.setattr(mod.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(mod.threading, "Thread", _FakeThread)

    started = json.loads(mod.pi_agent({"action": "start"}))
    sid = started["session_id"]

    req = "req-123"
    s = mod._SESSIONS[sid]
    with s.lock:
        s.event_count += 1
        s.events.append({"index": s.event_count, "type": "response", "request_id": req})
        s.event_count += 1
        s.events.append({"index": s.event_count, "type": "turn_end", "request_id": req})

    waited = json.loads(
        mod.pi_agent(
            {
                "action": "wait",
                "session_id": sid,
                "request_id": req,
                "timeout_seconds": 1,
            }
        )
    )
    assert waited["success"] is True
    assert waited["timed_out"] is False
    assert waited["matched_event"]["type"] == "turn_end"


def test_reload_marks_sessions_detached(monkeypatch, tmp_path):
    mod = _reload_tool(monkeypatch, tmp_path)
    monkeypatch.setattr(mod.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(mod.threading, "Thread", _FakeThread)

    sid = json.loads(mod.pi_agent({"action": "start"}))["session_id"]

    # Simulate process restart by reloading the module; persisted sessions should
    # be available for list but marked detached.
    mod2 = importlib.reload(mod)
    listed = json.loads(mod2.pi_agent({"action": "list"}))
    assert listed["count"] == 1
    assert listed["sessions"][0]["session_id"] == sid
    assert listed["sessions"][0]["detached"] is True

    send_detached = json.loads(mod2.pi_agent({"action": "send", "session_id": sid, "message": "x"}))
    assert send_detached["success"] is False
    assert "detached" in send_detached["error"]


def test_resume_detached_session_starts_new_live_session(monkeypatch, tmp_path):
    mod = _reload_tool(monkeypatch, tmp_path)
    monkeypatch.setattr(mod.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(mod.threading, "Thread", _FakeThread)

    sid = json.loads(mod.pi_agent({"action": "start"}))["session_id"]
    mod2 = importlib.reload(mod)
    monkeypatch.setattr(mod2.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(mod2.threading, "Thread", _FakeThread)

    resumed = json.loads(mod2.pi_agent({"action": "resume", "session_id": sid}))
    assert resumed["success"] is True
    assert resumed["resumed_from"] == sid
    assert resumed["session_id"] != sid

    listed = json.loads(mod2.pi_agent({"action": "list"}))
    assert listed["count"] == 2
    live = [s for s in listed["sessions"] if s["session_id"] == resumed["session_id"]][0]
    assert live["running"] is True
    assert live["detached"] is False


def test_prune_removes_old_detached_sessions(monkeypatch, tmp_path):
    mod = _reload_tool(monkeypatch, tmp_path)
    monkeypatch.setattr(mod.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(mod.threading, "Thread", _FakeThread)

    sid = json.loads(mod.pi_agent({"action": "start"}))["session_id"]
    mod2 = importlib.reload(mod)
    monkeypatch.setattr(mod2.subprocess, "Popen", _FakePopen)
    monkeypatch.setattr(mod2.threading, "Thread", _FakeThread)

    # Make detached session old enough to be pruned.
    mod2._SESSIONS[sid].created_at = time.time() - (10 * 86400)
    pruned = json.loads(mod2.pi_agent({"action": "prune", "max_age_days": 7}))
    assert pruned["success"] is True
    assert pruned["removed_count"] == 1
    assert sid in pruned["removed"]

    listed = json.loads(mod2.pi_agent({"action": "list"}))
    assert listed["count"] == 0
