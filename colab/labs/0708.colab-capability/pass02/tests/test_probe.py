"""Harness for the pass02 probe. Temporary directories belong to this harness."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

PROBE = Path(__file__).resolve().parents[1] / "probe.py"
PY = sys.executable


def load_probe():
    spec = importlib.util.spec_from_file_location("pass02_probe", PROBE)
    if spec is None or spec.loader is None:
        raise RuntimeError("probe module is not loadable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROBE_MODULE = load_probe()


def tree_digest(root: Path) -> str:
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        data = path.read_bytes()
        rel = path.relative_to(root).as_posix()
        rows.append(f"{hashlib.sha256(data).hexdigest()} {len(data)} {rel}")
    blob = ("\n".join(rows) + ("\n" if rows else "")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()


def invoke(args: list[str], cwd: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [PY, "-B", str(PROBE), *args],
        cwd=str(cwd),
        capture_output=True,
        check=False,
        shell=False,
        env=env,
    )


class ProbeCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.evidence = self.root / "evidence"
        self.scratch = self.root / "scratch"
        self.evidence.mkdir()
        self.scratch.mkdir()

    def args(self, run_id: str | None, mode: str, extra: list[str] | None = None) -> list[str]:
        argv = [
            "run",
            "--evidence-root",
            str(self.evidence),
            "--scratch-root",
            str(self.scratch),
            "--mode",
            mode,
        ]
        if run_id is not None:
            argv.extend(["--run-id", run_id])
        if extra:
            argv.extend(extra)
        return argv

    def run_mode(self, run_id: str | None, mode: str, extra: list[str] | None = None) -> subprocess.CompletedProcess:
        return invoke(self.args(run_id, mode, extra), self.root)

    def status(self, run_id: str) -> dict:
        return json.loads((self.evidence / run_id / "status.json").read_text(encoding="utf-8"))

    def test_ok_two_slots_and_first_unchanged(self) -> None:
        first = self.run_mode("ok-1", "ok")
        self.assertEqual(first.returncode, 0, first.stderr)
        digest = tree_digest(self.evidence / "ok-1")
        scratch_digest = tree_digest(self.scratch / "ok-1")
        second = self.run_mode("ok-2", "ok")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(tree_digest(self.evidence / "ok-1"), digest)
        self.assertEqual(tree_digest(self.scratch / "ok-1"), scratch_digest)
        self.assertEqual(self.status("ok-1")["status"], "complete")
        self.assertEqual(self.status("ok-1")["interruption"], "none")
        self.assertEqual(self.status("ok-2")["status"], "complete")
        self.assertEqual((self.scratch / "ok-1" / "child-out.txt").read_bytes(), b"minimal-ok\n")
        self.assertEqual((self.scratch / "ok-2" / "child-out.txt").read_bytes(), b"minimal-ok\n")
        self.assertFalse((self.evidence / "ok-1" / "status.json.tmp").exists())

    def test_fail_partial_kept_and_later_ok_leaves_it(self) -> None:
        failed = self.run_mode("fail-1", "fail")
        self.assertEqual(failed.returncode, 1, failed.stderr)
        body = self.status("fail-1")
        self.assertEqual(body["status"], "failed")
        self.assertEqual(body["interruption"], "caught-failure")
        self.assertEqual(body["child_exit"], 1)
        self.assertEqual((self.scratch / "fail-1" / "partial.txt").read_bytes(), b"partial-output\n")
        evidence_digest = tree_digest(self.evidence / "fail-1")
        scratch_digest = tree_digest(self.scratch / "fail-1")
        later = self.run_mode("ok-after", "ok")
        self.assertEqual(later.returncode, 0, later.stderr)
        self.assertEqual(tree_digest(self.evidence / "fail-1"), evidence_digest)
        self.assertEqual(tree_digest(self.scratch / "fail-1"), scratch_digest)
        self.assertEqual(self.status("fail-1")["status"], "failed")
        self.assertEqual(self.status("ok-after")["status"], "complete")

    def test_occupied_evidence_refuses_without_scratch(self) -> None:
        slot = self.evidence / "occupied-seed"
        slot.mkdir()
        marker = slot / "marker.txt"
        marker.write_bytes(b"keep-me\n")
        before = marker.read_bytes()
        result = self.run_mode("occupied-seed", "ok")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertIn(b"occupied evidence destination", result.stderr)
        self.assertEqual(marker.read_bytes(), before)
        self.assertEqual([path.name for path in slot.iterdir()], ["marker.txt"])
        self.assertFalse((self.scratch / "occupied-seed").exists())

    def test_occupied_scratch_records_failure_and_keeps_marker(self) -> None:
        slot = self.scratch / "scratch-taken"
        slot.mkdir()
        marker = slot / "marker.txt"
        marker.write_bytes(b"scratch-keep\n")
        before = tree_digest(slot)
        result = self.run_mode("scratch-taken", "ok")
        self.assertEqual(result.returncode, 1, result.stderr)
        body = self.status("scratch-taken")
        self.assertEqual(body["status"], "failed")
        self.assertEqual(body["interruption"], "caught-failure")
        self.assertEqual(body["detail"], "occupied scratch destination")
        self.assertEqual(tree_digest(slot), before)
        self.assertEqual(marker.read_bytes(), b"scratch-keep\n")
        self.assertFalse((self.evidence / "scratch-taken" / "child.stdout").exists())

    def test_killed_hold_stays_running(self) -> None:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.Popen(
            [PY, "-B", str(PROBE), *self.args("hold-killed", "hold", ["--hold-seconds", "30"])],
            cwd=str(self.root),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            shell=False,
        )
        status_path = self.evidence / "hold-killed" / "status.json"
        scratch_slot = self.scratch / "hold-killed"
        observed = None
        deadline = time.time() + 10
        try:
            while time.time() < deadline:
                if status_path.is_file() and scratch_slot.is_dir():
                    try:
                        observed = json.loads(status_path.read_text(encoding="utf-8"))
                    except json.JSONDecodeError:
                        time.sleep(0.05)
                        continue
                    if observed.get("status") == "running":
                        break
                time.sleep(0.05)
            self.assertIsNotNone(observed)
            self.assertEqual(observed["status"], "running")
            self.assertIsNone(observed["interruption"])
            proc.kill()
        finally:
            if proc.poll() is None:
                proc.kill()
            proc.communicate(timeout=10)
        left = json.loads(status_path.read_text(encoding="utf-8"))
        self.assertEqual(left["status"], "running")
        self.assertIsNone(left["interruption"])
        digest = tree_digest(self.evidence / "hold-killed")
        scratch_digest = tree_digest(self.scratch / "hold-killed")
        later = self.run_mode("ok-after-kill", "ok")
        self.assertEqual(later.returncode, 0, later.stderr)
        self.assertEqual(tree_digest(self.evidence / "hold-killed"), digest)
        self.assertEqual(tree_digest(self.scratch / "hold-killed"), scratch_digest)
        self.assertEqual(self.status("hold-killed")["status"], "running")

    def test_omitted_run_id_makes_two_slots(self) -> None:
        first = self.run_mode(None, "ok")
        second = self.run_mode(None, "ok")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        names = sorted(path.name for path in self.evidence.iterdir())
        self.assertEqual(len(names), 2)
        self.assertNotEqual(names[0], names[1])
        for name in names:
            self.assertEqual(self.status(name)["status"], "complete")

    def test_same_id_race_admits_one(self) -> None:
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        command = [PY, "-B", str(PROBE), *self.args("race-1", "ok")]
        procs = [
            subprocess.Popen(
                command,
                cwd=str(self.root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                shell=False,
            )
            for _ in range(2)
        ]
        outputs = []
        for proc in procs:
            stdout, stderr = proc.communicate(timeout=20)
            outputs.append((proc.returncode, stdout, stderr))
        codes = sorted(item[0] for item in outputs)
        self.assertEqual(codes, [0, 2], outputs)
        slots = [path for path in self.evidence.iterdir() if path.is_dir()]
        self.assertEqual([path.name for path in slots], ["race-1"])
        self.assertEqual(self.status("race-1")["status"], "complete")
        self.assertEqual(self.status("race-1")["interruption"], "none")
        refused = [item for item in outputs if item[0] == 2]
        self.assertIn(b"occupied evidence destination", refused[0][2])
        self.assertTrue((self.scratch / "race-1" / "child-out.txt").is_file())

    def test_preview_pin_mismatch_does_not_spawn(self) -> None:
        producer = self.root / "producer.py"
        request = self.root / "request.json"
        config = self.root / "config.json"
        producer.write_bytes(b"not-the-producer\n")
        request.write_bytes(b"{}\n")
        config.write_bytes(b"{}\n")
        before = producer.read_bytes()
        result = self.run_mode(
            "pin-miss",
            "preview",
            ["--request", str(request), "--config", str(config), "--producer", str(producer)],
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        body = self.status("pin-miss")
        self.assertEqual(body["status"], "failed")
        self.assertEqual(body["interruption"], "caught-failure")
        self.assertEqual(body["detail"], "producer pin mismatch")
        self.assertFalse((self.evidence / "pin-miss" / "child.stdout").exists())
        self.assertEqual(producer.read_bytes(), before)
        inputs = json.loads((self.evidence / "pin-miss" / "inputs.json").read_text(encoding="utf-8"))
        producer_row = [row for row in inputs["files"] if row["role"] == "producer"][0]
        self.assertFalse(producer_row["pin_match"])

    def test_missing_root_is_not_created(self) -> None:
        missing = self.root / "missing-evidence"
        result = invoke(
            [
                "run",
                "--evidence-root",
                str(missing),
                "--scratch-root",
                str(self.scratch),
                "--run-id",
                "nope",
                "--mode",
                "ok",
            ],
            self.root,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse(missing.exists())
        self.assertFalse((self.scratch / "nope").exists())

    def test_relative_root_refused(self) -> None:
        result = invoke(
            [
                "run",
                "--evidence-root",
                "evidence",
                "--scratch-root",
                str(self.scratch),
                "--run-id",
                "rel",
                "--mode",
                "ok",
            ],
            self.root,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse((self.root / "evidence" / "rel").exists())

    def test_nested_roots_refused(self) -> None:
        nested = self.evidence / "nested-scratch"
        nested.mkdir()
        result = invoke(
            [
                "run",
                "--evidence-root",
                str(self.evidence),
                "--scratch-root",
                str(nested),
                "--run-id",
                "nest",
                "--mode",
                "ok",
            ],
            self.root,
        )
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse((self.evidence / "nest").exists())

    def test_slash_run_id_refused(self) -> None:
        result = self.run_mode("ok/1", "ok")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(list(self.evidence.iterdir()), [])
        self.assertEqual(list(self.scratch.iterdir()), [])

    def test_tool_args_on_ok_refused(self) -> None:
        request = self.root / "request.json"
        request.write_bytes(b"{}\n")
        result = self.run_mode("ok-extra", "ok", ["--request", str(request)])
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertFalse((self.evidence / "ok-extra").exists())

    def test_source_has_no_destructive_paths(self) -> None:
        text = PROBE.read_text(encoding="utf-8")
        for banned in ("rmtree", "shutil", "build05.01", "0708-colab-capability", "pass01"):
            self.assertNotIn(banned, text)
        self.assertNotIn('os.environ["TEMP"]', text)
        self.assertEqual(
            PROBE_MODULE.PRODUCER_SHA256,
            "2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b",
        )
        self.assertEqual(PROBE_MODULE.PRODUCER_BYTES, 53892)

    def test_decide_ok_requires_both_checks(self) -> None:
        good = PROBE_MODULE.decide_ok("sample", 0, b"minimal-ok\n")
        self.assertEqual(good["status"], "complete")
        self.assertEqual(good["interruption"], "none")
        bad_exit = PROBE_MODULE.decide_ok("sample", 1, b"minimal-ok\n")
        self.assertEqual(bad_exit["status"], "failed")
        bad_bytes = PROBE_MODULE.decide_ok("sample", 0, b"other\n")
        self.assertEqual(bad_bytes["status"], "failed")
        self.assertEqual(bad_bytes["interruption"], "caught-failure")
        failed = PROBE_MODULE.decide_fail("sample", 1, b"partial-output\n")
        self.assertEqual(failed["status"], "failed")
        self.assertNotEqual(failed["status"], "complete")

    def test_accept_preview_requires_digest(self) -> None:
        good = {
            "command": "preview",
            "digest": "a" * 64,
            "result": "preview",
            "schema": "colab-support-report/2",
        }
        raw = (json.dumps(good) + "\n").encode("utf-8")
        matched, _detail, digest = PROBE_MODULE.accept_preview(raw, 0)
        self.assertTrue(matched)
        self.assertEqual(digest, "a" * 64)
        matched, detail, _digest = PROBE_MODULE.accept_preview(raw, 2)
        self.assertFalse(matched)
        self.assertIn("preview exit 2", detail)
        broken = dict(good)
        broken["digest"] = "SHORT"
        raw_broken = json.dumps(broken).encode("utf-8")
        matched, detail, _digest = PROBE_MODULE.accept_preview(raw_broken, 0)
        self.assertFalse(matched)
        self.assertIn("digest", detail)

    def test_preview_missing_request_creates_nothing(self) -> None:
        result = self.run_mode("preview-missing", "preview")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertEqual(list(self.evidence.iterdir()), [])
        self.assertEqual(list(self.scratch.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
