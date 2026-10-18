import ctypes
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import test_checker as support
import init_manifest

checker = support.checker


def alive(pid):
    if os.name == "nt":
        from ctypes import wintypes as w
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.argtypes = [w.DWORD, w.BOOL, w.DWORD]
        kernel.OpenProcess.restype = w.HANDLE
        kernel.GetExitCodeProcess.argtypes = [w.HANDLE, ctypes.POINTER(w.DWORD)]
        kernel.CloseHandle.argtypes = [w.HANDLE]
        handle = kernel.OpenProcess(0x1000, False, pid)
        if not handle:
            return False
        try:
            code = w.DWORD()
            return bool(kernel.GetExitCodeProcess(handle, ctypes.byref(code))) and code.value == 259
        finally:
            kernel.CloseHandle(handle)
    try:
        os.kill(pid, 0)
        stat = Path("/proc") / str(pid) / "stat"
        return not stat.exists() or stat.read_text().split(")", 1)[1].split()[0] != "Z"
    except ProcessLookupError:
        return False


class CheckerLifecycleTests(unittest.TestCase):
    def setUp(self):
        workspace = support.SCRIPTS.parent / "work" / "checker-lifecycle-tests"
        workspace.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=workspace)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.pidfile = self.root / "family.json"
        self.pids = {}
        self.addCleanup(self.cleanup_family)
        self.family = self.root / "family.py"
        self.family.write_text(
            "from pathlib import Path\nimport json,os,subprocess,sys,time\n"
            "quiet=sys.argv[2]=='exit'\n"
            "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'],stdout=subprocess.DEVNULL if quiet else None,stderr=subprocess.DEVNULL if quiet else None)\n"
            "Path(sys.argv[1]).write_text(json.dumps({'direct':os.getpid(),'grandchild':p.pid}))\n"
            "if not quiet: time.sleep(30)\n", encoding="utf-8")

    def cleanup_family(self):
        if not self.pids and self.pidfile.exists():
            self.pids = json.loads(self.pidfile.read_text())
        for pid in self.pids.values():
            if alive(pid):
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"], capture_output=True)
                else:
                    try:
                        os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass

    def wait_family(self):
        deadline = time.monotonic() + 5
        while not self.pidfile.exists() and time.monotonic() < deadline:
            time.sleep(.02)
        self.assertTrue(self.pidfile.exists(), "owned command did not start")
        self.pids = json.loads(self.pidfile.read_text())
        return self.pids

    def assert_family_stopped(self):
        self.wait_family()
        deadline = time.monotonic() + 3
        while any(alive(p) for p in self.pids.values()) and time.monotonic() < deadline:
            time.sleep(.02)
        self.assertFalse({n: p for n, p in self.pids.items() if alive(p)})

    def test_timeout_stops_ordinary_descendants_and_reader(self):
        result = checker.run_declared_command([sys.executable, str(self.family), str(self.pidfile), "wait"], self.root, 1)
        self.assertTrue(result["timed_out"])
        self.assertFalse(result["reader_stalled"])
        self.assertFalse(result["cleanup_timed_out"])
        self.assert_family_stopped()

    def test_normal_completion_cleans_background_descendants(self):
        result = checker.run_declared_command([sys.executable, str(self.family), str(self.pidfile), "exit"], self.root, 5)
        self.assertEqual(result["returncode"], 0)
        self.assertFalse(result["reader_stalled"])
        self.assert_family_stopped()

    def cli(self, inject_interrupt=False):
        project = self.root / "project"
        (project / "src").mkdir(parents=True)
        (project / "src/app.py").write_text("pass", encoding="utf-8")
        manifest = init_manifest.manifest(project, "lite")
        for doc in manifest["documents"]:
            path = project / doc["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Synthetic fixture REQ-BOOTSTRAP-01 AT-BOOTSTRAP-01", encoding="utf-8")
        manifest["baseline"]["status"] = "complete"
        manifest["checks"][0].update(command=[sys.executable, str(self.family), str(self.pidfile), "wait"], timeout_seconds=10)
        (project / "engineering-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        args = ["--root", str(project), "--manifest", "engineering-manifest.json", "--mode", "baseline", "--run-checks"]
        if inject_interrupt:
            wrapper = self.root / "interrupt.py"
            wrapper.write_text(
                "import _thread,sys,threading,time\nfrom pathlib import Path\n"
                + f"sys.path.insert(0,{str(support.SCRIPTS)!r})\nimport check_project\n"
                + f"ready=Path({str(self.pidfile)!r})\n"
                + "def interrupt():\n while not ready.exists(): time.sleep(.02)\n _thread.interrupt_main()\n"
                + "threading.Thread(target=interrupt,daemon=True).start()\n"
                + f"raise SystemExit(check_project.main({args!r}))\n", encoding="utf-8")
            command = [sys.executable, str(wrapper)]
        else:
            command = [sys.executable, str(support.SCRIPTS / "check_project.py"), *args]
        env = os.environ.copy()
        env.pop("ENGINEERING_TASK_ID", None)
        env.pop("ENGINEERING_CONTROL_PLANE_APPROVED", None)
        parent = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        self.addCleanup(self.cleanup_parent, parent)
        return parent

    @staticmethod
    def cleanup_parent(parent):
        if parent.poll() is None:
            parent.kill()
        parent.communicate(timeout=5)

    def test_cli_cancellation_is_non_success_and_cleans_the_family(self):
        parent = self.cli(inject_interrupt=os.name == "nt")
        self.wait_family()
        if os.name != "nt":
            parent.send_signal(signal.SIGTERM)
        stdout, stderr = parent.communicate(timeout=6)
        self.assertEqual(parent.returncode, 130 if os.name == "nt" else 143, stderr)
        report = json.loads(stdout)
        self.assertFalse(report["required_checks_satisfied"])
        interrupted = next(c for c in report["checks"] if c["rule_id"] == "interrupted")
        self.assertFalse(interrupted["evidence"]["reader_stalled"])
        self.assert_family_stopped()

    def test_platform_native_parent_lifecycle(self):
        parent = self.cli()
        self.wait_family()
        if os.name == "nt":
            # Job handle close is an OS action; no Python finally can run here.
            parent.kill()
            parent.communicate(timeout=5)
        else:
            parent.send_signal(signal.SIGINT)
            stdout, stderr = parent.communicate(timeout=6)
            self.assertEqual(parent.returncode, 130, stderr)
            self.assertFalse(json.loads(stdout)["required_checks_satisfied"])
        self.assert_family_stopped()

    def test_signal_handlers_are_restored_after_cancellation(self):
        previous = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
        with self.assertRaises(checker.CheckCancelled):
            with checker.command_cancellation():
                signal.raise_signal(signal.SIGTERM)
        self.assertEqual(previous, {s: signal.getsignal(s) for s in previous})

    def test_failed_lifecycle_setup_does_not_run_command_code(self):
        marker = self.root / "must-not-run"
        command = [sys.executable, "-c", f"open({str(marker)!r},'w').write('ran')"]
        if os.name == "nt":
            target, attribute = checker._WindowsProcessJob, "attach_and_resume"
        else:
            target, attribute = checker.subprocess, "Popen"
        with patch.object(target, attribute, side_effect=OSError("fixture setup failure")):
            with self.assertRaises(OSError):
                checker.run_declared_command(command, self.root, 5)
        self.assertFalse(marker.exists())


if __name__ == "__main__":
    unittest.main()
