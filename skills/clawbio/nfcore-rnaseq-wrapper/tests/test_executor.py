from __future__ import annotations

from pathlib import Path
import subprocess
import sys

import pytest

_SKILL_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_SKILL_DIR))


def _purge_foreign_modules(*names: str) -> None:
    for name in names:
        module = sys.modules.get(name)
        module_file = Path(getattr(module, "__file__", "") or "")
        if module is not None and _SKILL_DIR not in module_file.parents and module_file != _SKILL_DIR / f"{name}.py":
            sys.modules.pop(name, None)


def _purge_local_modules(*names: str) -> None:
    for name in names:
        module = sys.modules.get(name)
        module_file = Path(getattr(module, "__file__", "") or "")
        if module is not None and (module_file == _SKILL_DIR / f"{name}.py" or _SKILL_DIR in module_file.parents):
            sys.modules.pop(name, None)


def _remove_skill_dir_from_sys_path() -> None:
    while str(_SKILL_DIR) in sys.path:
        sys.path.remove(str(_SKILL_DIR))


_purge_foreign_modules("errors", "executor")

from errors import SkillError
import executor as executor_module
from executor import execute_nextflow

_purge_local_modules("errors", "executor")
_remove_skill_dir_from_sys_path()


class _MockProc:
    def __init__(self, returncode: int = 0, timeout_on_first_wait: bool = False):
        self._rc = returncode
        self._timeout_on_first = timeout_on_first_wait
        self._wait_calls = 0
        self.killed = False
        self.pid = 1234

    def wait(self, timeout=None):
        self._wait_calls += 1
        if self._timeout_on_first and self._wait_calls == 1:
            raise subprocess.TimeoutExpired(cmd=["nextflow"], timeout=timeout or 1)
        return self._rc

    def kill(self):
        self.killed = True


def test_execute_nextflow_creates_log_files_on_success(tmp_path, monkeypatch):
    proc = _MockProc(returncode=0)
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: proc)
    result = execute_nextflow(["nextflow", "run", "test"], cwd=tmp_path, output_dir=tmp_path, timeout_seconds=60)
    assert result["exit_code"] == 0
    assert Path(result["stdout_path"]).name == "stdout.txt"
    assert Path(result["stderr_path"]).name == "stderr.txt"
    assert (tmp_path / "logs" / "stdout.txt").exists()
    assert (tmp_path / "logs" / "stderr.txt").exists()


def test_execute_nextflow_raises_on_nonzero_exit_and_keeps_logs(tmp_path, monkeypatch):
    proc = _MockProc(returncode=1)
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: proc)
    with pytest.raises(SkillError) as exc:
        execute_nextflow(["nextflow", "run", "test"], cwd=tmp_path, output_dir=tmp_path, timeout_seconds=60)
    assert exc.value.error_code == "EXECUTION_FAILED"
    assert exc.value.details["exit_code"] == 1
    assert (tmp_path / "logs" / "stdout.txt").exists()
    assert (tmp_path / "logs" / "stderr.txt").exists()


def test_execute_nextflow_starts_new_session_on_posix(tmp_path, monkeypatch):
    proc = _MockProc(returncode=0)
    popen_kwargs = {}

    def fake_popen(*args, **kwargs):
        popen_kwargs.update(kwargs)
        return proc

    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    execute_nextflow(["nextflow", "run", "test"], cwd=tmp_path, output_dir=tmp_path, timeout_seconds=60)
    assert popen_kwargs["start_new_session"] is True


def test_execute_nextflow_terminates_process_group_on_posix_timeout(tmp_path, monkeypatch):
    proc = _MockProc(returncode=0, timeout_on_first_wait=True)
    pgid = 5678
    signals_sent: list[tuple[int, int]] = []

    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: proc)
    monkeypatch.setattr(executor_module.os, "getpgid", lambda pid: pgid)
    monkeypatch.setattr(executor_module.os, "killpg", lambda sent_pgid, sig: signals_sent.append((sent_pgid, sig)))

    with pytest.raises(SkillError):
        execute_nextflow(["nextflow", "run", "test"], cwd=tmp_path, output_dir=tmp_path, timeout_seconds=1)

    assert signals_sent
    assert all(sent_pgid == pgid for sent_pgid, _ in signals_sent)
    assert proc.killed is False


def test_execute_nextflow_cleans_up_empty_logs_on_popen_failure(tmp_path, monkeypatch):
    def raise_os_error(*args, **kwargs):
        raise OSError("nextflow: command not found")

    monkeypatch.setattr(subprocess, "Popen", raise_os_error)
    with pytest.raises(SkillError) as exc:
        execute_nextflow(["nextflow", "run", "test"], cwd=tmp_path, output_dir=tmp_path, timeout_seconds=60)
    assert exc.value.error_code == "EXECUTION_FAILED"
    assert not (tmp_path / "logs" / "stdout.txt").exists()
    assert not (tmp_path / "logs" / "stderr.txt").exists()


def test_execute_nextflow_timeout_error_reports_timeout_seconds(tmp_path, monkeypatch):
    proc = _MockProc(returncode=0, timeout_on_first_wait=True)
    monkeypatch.setattr(sys, "platform", "win32")
    monkeypatch.setattr(subprocess, "Popen", lambda *a, **kw: proc)
    monkeypatch.setattr(subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a[0], 0))
    with pytest.raises(SkillError) as exc:
        execute_nextflow(["nextflow", "run", "test"], cwd=tmp_path, output_dir=tmp_path, timeout_seconds=7)
    assert exc.value.details["timeout_seconds"] == 7


def test_terminate_process_tree_falls_back_to_sigkill_when_sigterm_times_out(monkeypatch):
    """_terminate_process_tree must send SIGKILL when SIGTERM's wait() times out."""
    import signal as signal_module

    signals_sent: list[int] = []
    wait_calls = [0]

    class _SlowProc:
        def __init__(self):
            self.pid = 9999
            self.killed = False

        def wait(self, timeout=None):
            wait_calls[0] += 1
            # First wait (grace period after SIGTERM) times out.
            # Second wait (after SIGKILL) completes immediately.
            if wait_calls[0] == 1:
                raise subprocess.TimeoutExpired(cmd=["nextflow"], timeout=timeout or 1)
            return -signal_module.SIGKILL

        def kill(self):
            self.killed = True

    proc = _SlowProc()
    pgid = 9999

    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setattr(executor_module.os, "getpgid", lambda pid: pgid)
    monkeypatch.setattr(
        executor_module.os,
        "killpg",
        lambda sent_pgid, sig: signals_sent.append(sig),
    )

    executor_module._terminate_process_tree(proc)

    # SIGTERM must be sent first, then SIGKILL as the fallback — order matters.
    assert signals_sent == [signal_module.SIGTERM, signal_module.SIGKILL], (
        f"Expected [SIGTERM, SIGKILL], got {signals_sent}"
    )
    # proc.kill() (last-resort fallback) must NOT have been called —
    # killpg(SIGKILL) should have succeeded.
    assert proc.killed is False
