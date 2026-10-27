#!/usr/bin/env python3
"""Fixture-only app-to-worker exchange. Expected refusals are counted apart from passes.

These checks are not an operating-system sandbox. The lab is not edited.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
LIBRARIAN = REPO / "app" / "librarian.py"
EXAMPLE = REPO / "00.kernel/00.00.10.work/0503.worker-bridge/evidence/design05.04/example"
WORK_REF = "00.kernel/00.00.10.work/0501.fixture/05.01.md"
RECORD = "00.kernel/00.00.10.work/0401.goal/06.01.md"
SCHEMA = "00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1"
INPUT_SHA = "f1f6c82d215ccf38a9d5eafce281febb2c971dc71ae7a15bbe0c1c81458d69c8"
RESULT_SHA = "0c07187ea6d064441225b3cba26a7b1e8bc702fcf332b457dae8e26892ba68a6"
JOB_SHA = "d888b53853a5ed77594643c46cfd5ec589197b4f77b80f5574d9db72d9f2eac5"
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
GUARDS = (
    "app/context.py",
    "app/development-workspace.json",
    "app/README.md",
    "README.md",
    "00.kernel/00.00.10.work/0401.goal/06.01.md",
    "00.kernel/00.live.md",
    "00.kernel/00.00.10.work/0504.app-entry/05.04.md",
    "labs/worker-bridge-pass01/bridge/__init__.py",
    "labs/worker-bridge-pass01/bridge/canon.py",
    "labs/worker-bridge-pass01/bridge/ids.py",
    "labs/worker-bridge-pass01/bridge/envelope.py",
    "labs/worker-bridge-pass01/bridge/verify.py",
    "labs/worker-bridge-pass01/bridge/adapter.py",
    "labs/worker-bridge-pass01/profiles.json",
    "labs/worker-bridge-pass01/fixtures/worker_fixture.py",
)
COPY_PATHS = (
    "app/librarian.py",
    "app/context.py",
    "app/worker_bridge.py",
    "app/worker-bridge.json",
    "app/development-workspace.json",
    "app/README.md",
    "labs/worker-bridge-pass01/bridge/__init__.py",
    "labs/worker-bridge-pass01/bridge/canon.py",
    "labs/worker-bridge-pass01/bridge/ids.py",
    "labs/worker-bridge-pass01/bridge/envelope.py",
    "labs/worker-bridge-pass01/bridge/verify.py",
    "labs/worker-bridge-pass01/bridge/adapter.py",
    "labs/worker-bridge-pass01/profiles.json",
    "labs/worker-bridge-pass01/fixtures/worker_fixture.py",
    "00.kernel/00.00.01.law/0302.run/02.run.003.py",
)


class Suite:
    def __init__(self) -> None:
        self.passed, self.refusals, self.skipped, self.failed, self.log = [], [], [], [], []

    def ok(self, name: str) -> None:
        self.passed.append(name)
        self.log.append(f"PASS {name}")
        print(f"PASS {name}", flush=True)

    def refusal(self, name: str) -> None:
        self.refusals.append(name)
        self.log.append(f"REFUSAL {name}")
        print(f"REFUSAL {name}", flush=True)

    def skip(self, name: str, detail: str) -> None:
        self.skipped.append(name)
        self.log.append(f"SKIP {name}: {detail}")
        print(f"SKIP {name}: {detail}", flush=True)

    def fail(self, name: str, detail: str) -> None:
        self.failed.append(name)
        self.log.append(f"FAIL {name}: {detail}")
        print(f"FAIL {name}: {detail}", flush=True)


SUITE = Suite()
FOREIGN = Path(tempfile.mkdtemp(prefix="librarian-0505-cwd-"))
(FOREIGN / "note.txt").write_bytes(b"do-not-read\n")
JUNCTIONS: list[Path] = []


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snap(paths: tuple[str, ...]) -> dict[str, str]:
    return {rel: sha(REPO / rel) for rel in paths}


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def show(proc: subprocess.CompletedProcess[str]) -> str:
    return f"exit {proc.returncode}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"


def run(args: list[str], cwd: Path | None = None, timeout: float = 40, librarian: Path = LIBRARIAN) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        [PY, "-B", str(librarian), *args],
        cwd=str(cwd or FOREIGN),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    SUITE.log.append(f"$ {' '.join(proc.args) if isinstance(proc.args, list) else proc.args}")
    SUITE.log.append(f"cwd: {cwd or FOREIGN}")
    SUITE.log.append(f"exit: {proc.returncode}")
    SUITE.log.append(proc.stdout)
    SUITE.log.append(proc.stderr)
    return proc


def fields(text: str) -> dict[str, str]:
    found = {}
    for line in text.splitlines():
        key, sep, value = line.partition(": ")
        if sep:
            found[key] = value
    return found


def record_text(state: str, **overrides: str) -> bytes:
    values = {
        "record": "current-assignment",
        "schema": SCHEMA,
        "desk": "00.kernel",
        "book": "00.00.10.work",
        "workflow_space": "0",
        "current_work": WORK_REF,
        "pack": WORK_REF,
        "assignment_state": state,
        "waits_on": "review",
        "next": "next step",
        "updated": "2026-10-26",
    }
    values.update(overrides)
    order = (
        "record", "schema", "desk", "book", "workflow_space", "current_work",
        "pack", "assignment_state", "waits_on", "next", "updated",
    )
    return "".join(f"{key}: {values[key]}\n" for key in order).encode("utf-8")


def plant(root: Path, state: str = "released", **overrides: str) -> None:
    (root / "00.kernel/00.00.10.work/0401.goal").mkdir(parents=True, exist_ok=True)
    (root / "00.kernel/00.00.01.law").mkdir(parents=True, exist_ok=True)
    (root / "00.kernel/00.00.10.work/0501.fixture").mkdir(parents=True, exist_ok=True)
    (root / RECORD).write_bytes(record_text(state, **overrides))
    (root / WORK_REF).write_bytes(b"fixture work item\n")
    declared = root / "bridge/declared"
    declared.mkdir(parents=True, exist_ok=True)
    (declared / "input.txt").write_bytes((EXAMPLE / "input.txt").read_bytes())


def write_job(root: Path, delivery: str = "bridge-0001", **overrides: object) -> None:
    job = json.loads((EXAMPLE / "job.json").read_text(encoding="utf-8"))
    job["delivery_id"] = delivery
    job.update(overrides)
    (root / "bridge/job.json").write_bytes((json.dumps(job, indent=2) + "\n").encode("utf-8"))


def write_example_job(root: Path) -> None:
    (root / "bridge").mkdir(parents=True, exist_ok=True)
    (root / "bridge/job.json").write_bytes((EXAMPLE / "job.json").read_bytes())


def bridge(root: Path, command: str, *args: str, container: str | None = None, timeout: float = 40, librarian: Path = LIBRARIAN):
    full = [command, "--root", str(root), *args]
    if container is not None:
        full.extend(["--container", container])
    return run(full, timeout=timeout, librarian=librarian)


def launches(root: Path, delivery: str = "bridge-0001") -> list[str]:
    path = root / f"bridge/delivery/{delivery}/output/launches.log"
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8").splitlines()


def expect_stop(name: str, proc: subprocess.CompletedProcess[str], snippet: str) -> None:
    bad = []
    if proc.returncode != 2:
        bad.append(f"exit {proc.returncode}")
    if "Traceback" in proc.stderr or "Traceback" in proc.stdout:
        bad.append("traceback")
    if not proc.stderr.startswith("stop:"):
        bad.append("stderr did not start with stop:")
    if snippet not in proc.stderr:
        bad.append(f"missing {snippet!r}")
    if proc.stdout.strip():
        bad.append("stdout was not empty")
    if bad:
        raise AssertionError("; ".join(bad) + "\n" + show(proc))
    SUITE.refusal(name)


def expect_outcome(name: str, proc: subprocess.CompletedProcess[str], code: int, **want: str) -> dict[str, str]:
    if proc.returncode != code:
        raise AssertionError(show(proc))
    if "Traceback" in proc.stderr or "Traceback" in proc.stdout:
        raise AssertionError(show(proc))
    got = fields(proc.stdout)
    for key, value in want.items():
        if got.get(key) != value:
            raise AssertionError(f"{key}: {got.get(key)!r} != {value!r}\n" + show(proc))
    if got.get("review") != "not performed" or got.get("acceptance") != "not performed":
        raise AssertionError(show(proc))
    if "approval" in proc.stdout:
        raise AssertionError(show(proc))
    SUITE.ok(name)
    return got


def make_junction(link: Path, target: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssertionError(proc.stdout + proc.stderr)
    JUNCTIONS.append(link)


def clear_junctions() -> None:
    for link in list(JUNCTIONS):
        if is_reparse(link):
            os.rmdir(link)
        JUNCTIONS.remove(link)


def fresh(name: str) -> Path:
    root = REPO / "app" / "scratch" / "bridge" / name
    clear_junctions()
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    return root


def copy_code(dest: Path) -> Path:
    for rel in COPY_PATHS:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, target)
    return dest / "app" / "librarian.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def receipt_hash(root: Path, delivery: str = "bridge-0001") -> str:
    return sha(root / f"bridge/store/{delivery}/receipt.json")


def test_pins_and_success() -> None:
    for rel, digest in {
        "labs/worker-bridge-pass01/bridge/__init__.py": "50f501a7eb4c1a8cef91317ca0dbc5222d63a9c2221ca9fdcbb90e5afc6cd7d1",
        "labs/worker-bridge-pass01/bridge/canon.py": "6c1a761db08b60b381c1ea6e5d9516a80f7ce7d389bdb42797e394d31488d60d",
        "labs/worker-bridge-pass01/bridge/ids.py": "8913d0c2c569a1c0b5748f3f4d597a9bc57a498fa6b952b817790c399356ed66",
        "labs/worker-bridge-pass01/bridge/envelope.py": "2b7b352b64a541a5f86a5b5abab2affddf82303a4bdb5c7246e20eb04b59a2d0",
        "labs/worker-bridge-pass01/bridge/verify.py": "8ffe8cac0f57399956f103da1d47a9d7a23faaed79682f4973b4cdeffc163f2f",
        "labs/worker-bridge-pass01/bridge/adapter.py": "27d683b494c13bd120d5099f863bb68ab96c6d458dd2a7641c0129122b89c9de",
        "labs/worker-bridge-pass01/profiles.json": "407804f5bb2ece553f61adef9bb424cfbfd33615b10dcd0144d734ea4fc6b59d",
        "labs/worker-bridge-pass01/fixtures/worker_fixture.py": "0d519c8b0eeb7106321748c88fed0dca0d855f2cc85a3904ada9aacc149d7cad",
    }.items():
        if sha(REPO / rel) != digest:
            raise AssertionError(rel)
    if sha(EXAMPLE / "input.txt") != INPUT_SHA or (EXAMPLE / "input.txt").stat().st_size != 22:
        raise AssertionError("example input changed")
    if sha(EXAMPLE / "expected-result.json") != RESULT_SHA:
        raise AssertionError("example result changed")
    if sha(EXAMPLE / "job.json") != JOB_SHA:
        raise AssertionError("example job changed")
    SUITE.ok("pinned lab and example bytes")

    root = fresh("success")
    plant(root)
    write_example_job(root)
    (root / "fixture.json").write_bytes(b'{"schema":"not-a-fixture"}\n')
    first = bridge(root, "bridge-test", "--job", "bridge/job.json")
    got = expect_outcome(
        "bridge-test collected the count",
        first,
        0,
        delivery_id="bridge-0001",
        worker_kind="protocol test worker",
        transport="delivered",
        claimed_outcome="done",
        collection="collected",
    )
    artifact = root / "bridge/delivery/bridge-0001/output/result.json"
    if artifact.read_bytes() != (EXAMPLE / "expected-result.json").read_bytes():
        raise AssertionError(artifact.read_bytes())
    if sha(artifact) != RESULT_SHA:
        raise AssertionError(sha(artifact))
    if got["artifact"] != f"bridge/delivery/bridge-0001/output/result.json sha256 {RESULT_SHA}":
        raise AssertionError(got["artifact"])
    if got["receipt"] != f"bridge/store/bridge-0001/receipt.json sha256 {receipt_hash(root)}":
        raise AssertionError(got["receipt"])
    if "replayed" in got:
        raise AssertionError("first delivery was marked replayed")
    if launches(root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(root))
    stored_request = (root / "bridge/store/bridge-0001/request.json").read_bytes()
    status = bridge(root, "bridge-status", "--delivery", "bridge-0001")
    status_fields = expect_outcome(
        "fresh-process status reads the receipt",
        status,
        0,
        transport="delivered",
        collection="collected",
        claimed_outcome="done",
    )
    if status_fields["receipt"] != got["receipt"]:
        raise AssertionError(status_fields["receipt"])
    if "replayed" in status_fields:
        raise AssertionError("status invented replayed")
    (root / RECORD).write_bytes(record_text("released", waits_on="later note"))
    before_output = sha(artifact)
    replay = bridge(root, "bridge-test", "--job", "bridge/job.json")
    replay_fields = expect_outcome("identical replay does not launch again", replay, 0, collection="collected")
    if replay_fields.get("replayed") != "true":
        raise AssertionError(show(replay))
    if replay_fields["receipt"] != got["receipt"]:
        raise AssertionError(replay_fields["receipt"])
    if launches(root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(root))
    if (root / "bridge/store/bridge-0001/request.json").read_bytes() != stored_request:
        raise AssertionError("replay rebuilt the request")
    if sha(artifact) != before_output:
        raise AssertionError("replay rewrote the artifact")
    output = root / "bridge/delivery/bridge-0001/output"
    shutil.rmtree(output)
    again = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_outcome("replay does not recreate the output directory", again, 0, collection="collected")
    if output.exists():
        raise AssertionError("output directory was recreated")
    if (root / "bridge/store/bridge-0001/request.json").read_bytes() != stored_request:
        raise AssertionError("request changed after the directory was removed")


def test_external_and_status_after_return() -> None:
    root = Path(tempfile.mkdtemp(prefix="librarian-0505-external-"))
    try:
        plant(root)
        write_example_job(root)
        first = bridge(root, "bridge-test", "--job", "bridge/job.json", container=str(root))
        got = expect_outcome("external container collected", first, 0, collection="collected", transport="delivered")
        status = bridge(root, "bridge-status", "--delivery", "bridge-0001", container=str(root))
        status_fields = expect_outcome("external fresh status", status, 0, collection="collected")
        if status_fields["receipt"] != got["receipt"]:
            raise AssertionError(status_fields["receipt"])
        replay = bridge(root, "bridge-test", "--job", "bridge/job.json", container=str(root))
        replay_fields = expect_outcome("external replay", replay, 0, collection="collected")
        if replay_fields.get("replayed") != "true" or launches(root) != ["bridge-0001 ok"]:
            raise AssertionError(show(replay) + str(launches(root)))
        other = "00.kernel/00.00.10.work/0501.fixture/05.02.md"
        (root / other).parent.mkdir(parents=True, exist_ok=True)
        (root / other).write_bytes(b"later work\n")
        (root / RECORD).write_bytes(record_text("accepted", current_work=other, pack=other))
        accepted = bridge(root, "bridge-status", "--delivery", "bridge-0001", container=str(root))
        accepted_fields = expect_outcome("status after accepted and current-work change", accepted, 0, collection="collected")
        if accepted_fields["receipt"] != got["receipt"]:
            raise AssertionError(accepted_fields["receipt"])
        (root / RECORD).write_bytes(record_text("returned", current_work=other, pack=other))
        returned = bridge(root, "bridge-status", "--delivery", "bridge-0001", container=str(root))
        returned_fields = expect_outcome("status after returned", returned, 0, collection="collected")
        if returned_fields["receipt"] != got["receipt"] or launches(root) != ["bridge-0001 ok"]:
            raise AssertionError(show(returned))
    finally:
        clear_junctions()
        shutil.rmtree(root, ignore_errors=True)


def test_failures() -> None:
    cases = (
        ("bad-hash", "fixture-bad-hash", 3, "delivered", "uncollected"),
        ("missing-artifact", "fixture-missing-artifact", 3, "delivered", "uncollected"),
        ("escape", "fixture-escape", 3, "delivered", "uncollected"),
        ("garbage", "fixture-garbage", 4, "malformed", "not attempted"),
        ("partial", "fixture-partial", 4, "malformed", "not attempted"),
        ("bad-shape", "fixture-bad-shape", 4, "malformed", "not attempted"),
        ("dup-keys", "fixture-dup-keys", 4, "malformed", "not attempted"),
        ("crash", "fixture-crash", 4, "crashed", "not attempted"),
    )
    for name, backend, code, transport, collection in cases:
        root = fresh(name)
        plant(root)
        write_job(root, backend=backend)
        proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
        expect_outcome(name, proc, code, transport=transport, collection=collection)
        if collection == "collected":
            raise AssertionError(name)

    root = fresh("flood")
    plant(root)
    write_job(root, backend="fixture-flood", limits={"timeout_s": 20, "max_stdout_bytes": 1000, "max_stderr_bytes": 1000})
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json", timeout=30)
    expect_outcome("output-limit", proc, 4, transport="output-limit", collection="not attempted")

    root = fresh("sleep")
    plant(root)
    write_job(root, backend="fixture-sleep", limits={"timeout_s": 1.5, "max_stdout_bytes": 100000, "max_stderr_bytes": 100000})
    started = time.monotonic()
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json", timeout=20)
    elapsed = time.monotonic() - started
    expect_outcome("timeout stays uncertain", proc, 4, transport="timeout", collection="not attempted")
    if elapsed > 8:
        raise AssertionError(f"timeout returned in {elapsed:.2f}s")
    replay = bridge(root, "bridge-test", "--job", "bridge/job.json", timeout=20)
    got = expect_outcome("timeout replay does not relaunch", replay, 4, transport="timeout")
    if got.get("replayed") != "true" or launches(root) != ["bridge-0001 sleep"]:
        raise AssertionError(show(replay) + str(launches(root)))

    root = fresh("pipes")
    plant(root)
    write_job(
        root,
        backend="fixture-inherit-pipes",
        limits={"timeout_s": 1.5, "max_stdout_bytes": 100000, "max_stderr_bytes": 100000},
    )
    started = time.monotonic()
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json", timeout=20)
    elapsed = time.monotonic() - started
    got = expect_outcome("inherited pipes stay incomplete", proc, 4, transport="incomplete-output", collection="not attempted")
    if "cleanup.retained" not in got or elapsed > 8:
        raise AssertionError(f"{elapsed:.2f}s\n" + show(proc))


def test_conflict_and_recovery() -> None:
    root = fresh("conflict")
    plant(root)
    write_example_job(root)
    first = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_outcome("conflict setup collected", first, 0, collection="collected")
    write_job(root, job_id="job-other")
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("conflicting delivery does not claim there was no launch", proc, "reused with a different request")
    if "this call did not launch" not in proc.stderr or "a prior launch record remains" not in proc.stderr:
        raise AssertionError(show(proc))
    if "never launched" in proc.stderr or "no launch" in proc.stderr or "refused before launch" in proc.stderr:
        raise AssertionError(show(proc))
    if launches(root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(root))

    root = fresh("interrupt")
    plant(root)
    write_example_job(root)
    context = load_module(REPO / "app/context.py", "librarian_context_bridge")
    bridge_mod = load_module(REPO / "app/worker_bridge.py", "librarian_worker_bridge_test")
    try:
        bridge_mod.perform(
            context,
            "bridge-test",
            REPO,
            root.resolve(),
            job_rel="bridge/job.json",
            crash_before_receipt=True,
        )
        raise AssertionError("crash hook returned a report")
    except Exception as exc:
        if "simulated crash" not in str(exc):
            raise
    if (root / "bridge/store/bridge-0001/receipt.json").exists():
        raise AssertionError("receipt existed after the crash hook")
    if launches(root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(root))
    status = bridge(root, "bridge-status", "--delivery", "bridge-0001")
    expect_outcome("interrupted receipt stays uncertain", status, 4, state="uncertain", collection="not collected")
    if "receipt: none" not in status.stdout:
        raise AssertionError(show(status))
    provenance = json.loads((root / "bridge/provenance/bridge-0001.json").read_text(encoding="utf-8"))
    recovery = {
        "schema": "librarian-bridge-recovery",
        "version": 1,
        "delivery_id": "bridge-0001",
        "request_sha256": provenance["request_sha256"],
        "reason": "interrupted receipt",
        "requester": "fixture test",
    }
    (root / "bridge/recover.json").write_bytes((json.dumps(recovery, indent=2) + "\n").encode("utf-8"))
    recovered = bridge(
        root,
        "bridge-recover",
        "--delivery",
        "bridge-0001",
        "--recovery-request",
        "bridge/recover.json",
    )
    got = expect_outcome("recover rebuilds the receipt without a launch", recovered, 0, collection="collected")
    if got.get("recovered") != "true" or launches(root) != ["bridge-0001 ok"]:
        raise AssertionError(show(recovered) + str(launches(root)))
    request_after = (root / "bridge/store/bridge-0001/request.json").read_bytes()
    second = bridge(
        root,
        "bridge-recover",
        "--delivery",
        "bridge-0001",
        "--recovery-request",
        "bridge/recover.json",
    )
    again = expect_outcome("second recover reads the stored receipt", second, 0, collection="collected")
    if again.get("recovered") != "true" or launches(root) != ["bridge-0001 ok"]:
        raise AssertionError(show(second))
    if (root / "bridge/store/bridge-0001/request.json").read_bytes() != request_after:
        raise AssertionError("recover rewrote the request")

    attempt = root / "bridge/store/bridge-0002"
    root2 = fresh("no-attempt")
    plant(root2)
    write_job(root2, delivery="bridge-0002")
    try:
        bridge_mod.perform(
            context,
            "bridge-test",
            REPO,
            root2.resolve(),
            job_rel="bridge/job.json",
            crash_before_receipt=True,
        )
    except Exception as exc:
        if "simulated crash" not in str(exc):
            raise
    shutil.rmtree(root2 / "bridge/store/bridge-0002/attempt")
    (root2 / "bridge/store/bridge-0002/receipt.json").unlink(missing_ok=True)
    provenance = json.loads((root2 / "bridge/provenance/bridge-0002.json").read_text(encoding="utf-8"))
    recovery["delivery_id"] = "bridge-0002"
    recovery["request_sha256"] = provenance["request_sha256"]
    (root2 / "bridge/recover.json").write_bytes((json.dumps(recovery) + "\n").encode("utf-8"))
    proc = bridge(root2, "bridge-recover", "--delivery", "bridge-0002", "--recovery-request", "bridge/recover.json")
    expect_outcome("launch without an attempt stays uncertain", proc, 4, collection="not collected")
    if (root2 / "bridge/store/bridge-0002/receipt.json").exists() or launches(root2, "bridge-0002") != ["bridge-0002 ok"]:
        raise AssertionError(show(proc))
    del attempt


def test_honesty_and_refusals() -> None:
    root = fresh("unknown")
    plant(root)
    proc = bridge(root, "bridge-status", "--delivery", "bridge-0099")
    got = expect_outcome("unknown delivery is not collected", proc, 4, state="unknown", transport="unknown", collection="not collected")
    if got.get("collection") == "collected":
        raise AssertionError(show(proc))

    root = fresh("accepted-not-launched")
    plant(root)
    write_example_job(root)
    expect_outcome("accepted-not-launched setup", bridge(root, "bridge-test", "--job", "bridge/job.json"), 0, collection="collected")
    store = root / "bridge/store/bridge-0001"
    (store / "receipt.json").unlink()
    (store / "launch.json").unlink()
    shutil.rmtree(store / "attempt")
    proc = bridge(root, "bridge-status", "--delivery", "bridge-0001")
    expect_outcome("accepted-not-launched stays not collected", proc, 4, state="accepted-not-launched", collection="not collected")

    root = fresh("bad-provenance")
    plant(root)
    write_example_job(root)
    expect_outcome("bad provenance setup", bridge(root, "bridge-test", "--job", "bridge/job.json"), 0, collection="collected")
    prov_path = root / "bridge/provenance/bridge-0001.json"
    before = prov_path.read_bytes()
    receipt_before = (root / "bridge/store/bridge-0001/receipt.json").read_bytes()
    raw = json.loads(before)
    raw["extra"] = "no"
    prov_path.write_bytes((json.dumps(raw) + "\n").encode("utf-8"))
    proc = bridge(root, "bridge-status", "--delivery", "bridge-0001")
    expect_stop("bad stored provenance", proc, "unknown key")
    if (root / "bridge/store/bridge-0001/receipt.json").read_bytes() != receipt_before:
        raise AssertionError("status rewrote the receipt")
    prov_path.write_bytes(before)
    raw = json.loads(before)
    raw["input_root"] = "../outside"
    prov_path.write_bytes(json.dumps(raw).encode("utf-8"))
    proc = bridge(root, "bridge-status", "--delivery", "bridge-0001")
    expect_stop("escaping stored path", proc, "path escapes the root")

    root = fresh("unreleased")
    plant(root, "accepted")
    write_example_job(root)
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("unreleased new work", proc, "assignment is not a fresh execution release")
    if (root / "bridge/store").exists():
        raise AssertionError("unreleased work wrote a store")

    root = fresh("backend")
    plant(root)
    write_job(root, backend="fixture-no-such")
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("unknown backend", proc, "not an allowlisted profile")
    if (root / "bridge/store").exists() or (root / "bridge/delivery").exists():
        raise AssertionError("unknown backend wrote delivery directories")

    root = fresh("work-ref")
    plant(root)
    write_job(root, work_ref="00.kernel/00.00.10.work/0501.fixture/other.md")
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("work_ref is not current work", proc, "work_ref is not the current work")

    root = fresh("limits")
    plant(root)
    write_job(root, limits={"timeout_s": -1, "max_stdout_bytes": 1000, "max_stderr_bytes": 1000})
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("bad limits", proc, "timeout_s")
    if (root / "bridge/delivery").exists():
        raise AssertionError("bad limits created a delivery directory")

    root = fresh("escape-job")
    plant(root)
    proc = bridge(root, "bridge-test", "--job", "../job.json")
    expect_stop("job path escape", proc, "path escapes the root")

    proc = run(["run", "--root", str(REPO)])
    expect_stop("normal run", proc, "normal run is not activated")
    proc = bridge(REPO, "bridge-test", "--job", "bridge/job.json")
    expect_stop("live workspace", proc, "fixture root is the live workspace")


def test_preplanted() -> None:
    root = fresh("pre-dir")
    plant(root)
    write_example_job(root)
    planted = root / "bridge/delivery/bridge-0001/output"
    planted.mkdir(parents=True)
    sentinel = planted / "keep.txt"
    sentinel.write_bytes(b"keep\n")
    before = sentinel.read_bytes()
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("pre-planted per-delivery directory", proc, "already present")
    if sentinel.read_bytes() != before or not planted.is_dir():
        raise AssertionError("pre-planted directory was removed or rewritten")
    if (root / "bridge/store/bridge-0001/launch.json").exists():
        raise AssertionError("pre-planted directory still launched")

    root = fresh("pre-link")
    plant(root)
    write_example_job(root)
    output = root / "bridge/delivery/bridge-0001/output"
    output.mkdir(parents=True)
    victim = root / "bridge/victim.txt"
    victim.write_bytes(b"victim-bytes\n")
    os.link(victim, output / "result.json")
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("pre-planted hard link", proc, "already present")
    if victim.read_bytes() != b"victim-bytes\n" or not (output / "result.json").exists():
        raise AssertionError("hard link was rewritten or removed")

    root = fresh("pre-store")
    plant(root)
    write_example_job(root)
    store = root / "bridge/store/bridge-0001"
    store.mkdir(parents=True)
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("pre-planted store", proc, "did not adopt")
    if list(store.iterdir()) or (root / "bridge/delivery/bridge-0001").exists():
        raise AssertionError("pre-planted store was adopted")

    root = fresh("pre-junction")
    plant(root)
    write_example_job(root)
    target = root / "bridge/junction-target"
    target.mkdir()
    (target / "keep.txt").write_bytes(b"junction-target\n")
    link = root / "bridge/delivery/bridge-0001"
    try:
        make_junction(link, target)
    except AssertionError as exc:
        SUITE.skip("pre-planted junction", str(exc))
        return
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("pre-planted junction", proc, "already present")
    if (target / "keep.txt").read_bytes() != b"junction-target\n" or not is_reparse(link):
        raise AssertionError("junction target changed")

    root = fresh("pre-symlink")
    plant(root)
    write_example_job(root)
    link = root / "bridge/delivery/bridge-0001"
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.symlink(root / "bridge/declared", link)
    except OSError as exc:
        SUITE.skip("pre-planted file symlink", f"WinError {exc.winerror}: {exc.strerror}" if getattr(exc, "winerror", None) else str(exc))
        return
    proc = bridge(root, "bridge-test", "--job", "bridge/job.json")
    expect_stop("pre-planted symlink", proc, "already present")


def test_isolated_copies() -> None:
    base = Path(tempfile.mkdtemp(prefix="librarian-0505-code-"))
    try:
        pin_root = base / "pin"
        librarian = copy_code(pin_root)
        adapter = pin_root / "labs/worker-bridge-pass01/bridge/adapter.py"
        adapter.write_bytes(b"this is not python\n")
        fixture = pin_root / "app/scratch/pin"
        plant(fixture)
        write_example_job(fixture)
        proc = bridge(fixture, "bridge-test", "--job", "bridge/job.json", librarian=librarian)
        expect_stop("pin mismatch before import", proc, "pinned file hash does not match")
        if "SyntaxError" in proc.stderr or "Traceback" in proc.stderr:
            raise AssertionError(show(proc))
        if (fixture / "bridge/store").exists():
            raise AssertionError("pin mismatch wrote a store")

        kind_root = base / "kind"
        librarian = copy_code(kind_root)
        config_path = kind_root / "app/worker-bridge.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["allowed_kinds"] = ["other kind"]
        config_path.write_bytes((json.dumps(config, indent=2) + "\n").encode("utf-8"))
        fixture = kind_root / "app/scratch/kind"
        plant(fixture)
        write_example_job(fixture)
        proc = bridge(fixture, "bridge-test", "--job", "bridge/job.json", librarian=librarian)
        expect_stop("wrong kind", proc, "worker kind is not allowed")
        if (fixture / "bridge/delivery").exists():
            raise AssertionError("wrong kind created a delivery")

        fail_root = base / "launch-failed"
        librarian = copy_code(fail_root)
        profiles_path = fail_root / "labs/worker-bridge-pass01/profiles.json"
        profiles = json.loads(profiles_path.read_text(encoding="utf-8"))
        profiles["fixture-ok"]["argv"] = ["missing-bridge-worker.exe"]
        profiles_path.write_bytes((json.dumps(profiles, indent=2) + "\n").encode("utf-8"))
        config_path = fail_root / "app/worker-bridge.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["files"]["profiles.json"] = sha(profiles_path)
        config_path.write_bytes((json.dumps(config, indent=2) + "\n").encode("utf-8"))
        fixture = fail_root / "app/scratch/launch"
        plant(fixture)
        write_example_job(fixture)
        proc = bridge(fixture, "bridge-test", "--job", "bridge/job.json", librarian=librarian)
        expect_outcome("launch-failed is not collected", proc, 4, transport="launch-failed", collection="not attempted")
        if launches(fixture):
            raise AssertionError(launches(fixture))
        if not (fixture / "bridge/store/bridge-0001/launch.json").is_file():
            raise AssertionError("launch-failed hid the launch record")
    finally:
        shutil.rmtree(base, ignore_errors=True)


def test_lab_suite() -> None:
    lab = Path(tempfile.mkdtemp(prefix="librarian-0505-lab-"))
    try:
        source = REPO / "labs/worker-bridge-pass01"
        for name in ("bridge", "fixtures", "tests"):
            shutil.copytree(source / name, lab / name)
        shutil.copy2(source / "profiles.json", lab / "profiles.json")
        count = 0
        for name in ("test_bridge.py", "test_pass02.py", "test_pass03.py"):
            proc = subprocess.run(
                [PY, "-B", str(lab / "tests" / name)],
                cwd=str(lab),
                env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180,
            )
            SUITE.log.append(f"LAB {name} exit {proc.returncode}")
            SUITE.log.append(proc.stdout[-2000:])
            SUITE.log.append(proc.stderr[-2000:])
            if proc.returncode != 0:
                raise AssertionError(f"{name} failed\n{proc.stdout[-1500:]}\n{proc.stderr[-1500:]}")
            count += proc.stderr.count("\n")  # unittest writes "Ran N tests" to stderr
            # The actual count is parsed below.
        text = "\n".join(SUITE.log)
        ran = 0
        for line in text.splitlines():
            if line.startswith("Ran "):
                ran += int(line.split()[1])
        if ran != 30:
            raise AssertionError(f"lab ran {ran} tests")
        SUITE.ok("accepted bridge 30 tests in an isolated copy")
        del count
    finally:
        shutil.rmtree(lab, ignore_errors=True)


def check(name: str, fn) -> None:
    try:
        fn()
    except Exception:
        SUITE.fail(name, traceback.format_exc())
    finally:
        clear_junctions()


def main() -> None:
    scratch = REPO / "app" / "scratch" / "bridge"
    if scratch.exists():
        shutil.rmtree(scratch)
    before = snap(GUARDS)
    for name, fn in (
        ("success", test_pins_and_success),
        ("external", test_external_and_status_after_return),
        ("failures", test_failures),
        ("recovery", test_conflict_and_recovery),
        ("refusals", test_honesty_and_refusals),
        ("preplanted", test_preplanted),
        ("isolated", test_isolated_copies),
        ("lab", test_lab_suite),
    ):
        check(name, fn)
    after = snap(GUARDS)
    if before != after:
        changed = [key for key in before if before[key] != after.get(key)]
        SUITE.fail("guarded bytes changed during the suite", ", ".join(changed))
    else:
        SUITE.ok("guarded bytes were unchanged")
    pyc = [p for p in (REPO / "app").rglob("__pycache__") if "scratch" not in p.parts]
    pyc += list((REPO / "00.kernel").rglob("__pycache__"))
    if pyc:
        SUITE.fail("bytecode in a book or app", "\n".join(str(p) for p in pyc))
    else:
        SUITE.ok("no bytecode was written into the books or app")
    print(
        f"summary pass {len(SUITE.passed)} "
        f"expected-refusal {len(SUITE.refusals)} "
        f"skip {len(SUITE.skipped)} "
        f"fail {len(SUITE.failed)}"
    )
    log = REPO / "app" / "scratch" / "bridge-test-log.txt"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("\n".join(SUITE.log) + "\n", encoding="utf-8", newline="\n")
    shutil.rmtree(FOREIGN, ignore_errors=True)
    if SUITE.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
