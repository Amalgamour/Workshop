#!/usr/bin/env python3
"""Fixture-only Clerk-to-worker seam. Queue and claim here are setup, not the command.

Expected refusals are counted apart from passes. These checks are not a sandbox.
The Clerk lab and the bridge lab are not edited.
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
import traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PY = sys.executable
LIBRARIAN = REPO / "app" / "librarian.py"
CLERK = REPO / "labs" / "clerk-handoff-pass02" / "clerk.py"
EXAMPLE = REPO / "00.kernel/00.00.10.work/0506.clerk-handoff/evidence/design05.03/examples"
EXAMPLE_TASK = EXAMPLE / "router/instructions/task.md"
EXAMPLE_JOB = EXAMPLE / "fixture/bridge/job.json"
EXAMPLE_CLERK = EXAMPLE / "router/clerk-job.json"
WORK_REF = "00.kernel/00.00.10.work/0504.app-entry/05.01.md"
RECORD = "00.kernel/00.00.10.work/0401.goal/06.01.md"
SCHEMA = "00.kernel/00.00.10.work/0410.imports/01.md#assignment-record version 1"
TASK_SHA = "6c913091d80948e3be49fa384b023ee3c43762599f3f61b47db885b4f846fe66"
JOB_SHA = "4d57cdb9ea210bfaedf4bdf6974c723735abcf431cb16b3ec946222fab05e1cf"
RESULT_SHA = "0c07187ea6d064441225b3cba26a7b1e8bc702fcf332b457dae8e26892ba68a6"
BEFORE_LIBRARIAN = "fe31aae774ccc2cfa37839c2e423e0e58240e594e364888b323a5308ba0ab452"
BEFORE_README = "6237ddf4b8d0a7403e4ca4d3969b720ac89edfac0912965d1d6886e01a87e04f"
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
GUARDS = (
    "app/context.py",
    "app/worker_bridge.py",
    "app/worker-bridge.json",
    "app/development-workspace.json",
    "app/librarian.py",
    "app/README.md",
    "app/clerk_seam.py",
    "app/clerk-seam.json",
    "app/prime_tools.py",
    "app/prime-tools.json",
    "app/tests/test_entry.py",
    "app/tests/test_worker_bridge.py",
    "app/tests/test_prime_tools.py",
    "labs/clerk-handoff-pass02/clerk.py",
    "labs/worker-bridge-pass01/fixtures/worker_fixture.py",
    "labs/worker-bridge-pass01/profiles.json",
    "00.kernel/00.00.10.work/0504.app-entry/05.10.md",
    "00.kernel/00.00.10.work/0504.app-entry/06.10.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/CONTRACT.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/before/app/librarian.py",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/before/app/README.md",
)

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


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
OPEN: list[World] = []
JUNCTIONS: list[Path] = []
FOREIGN: Path | None = None
_LOADS = 0


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snap(paths: tuple[str, ...]) -> dict[str, str]:
    return {rel: sha(REPO / rel) for rel in paths}


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def show(proc: subprocess.CompletedProcess[str]) -> str:
    return f"exit {proc.returncode}\nstdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"


def foreign() -> Path:
    global FOREIGN
    if FOREIGN is None:
        FOREIGN = Path(tempfile.mkdtemp(prefix="librarian-0510-cwd-"))
        (FOREIGN / "note.txt").write_bytes(b"do-not-read\n")
    return FOREIGN


def run(args: list[str], timeout: float = 60, librarian: Path = LIBRARIAN) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(
        [PY, "-B", str(librarian), *args],
        cwd=str(foreign()),
        env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    SUITE.log.append(f"$ {' '.join(str(part) for part in proc.args)}")
    SUITE.log.append(f"cwd: {foreign()}")
    SUITE.log.append(f"exit: {proc.returncode}")
    SUITE.log.append(proc.stdout)
    SUITE.log.append(proc.stderr)
    return proc


def load_module(path: Path, prefix: str):
    global _LOADS
    _LOADS += 1
    spec = importlib.util.spec_from_file_location(f"{prefix}_{_LOADS}", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fields(text: str) -> dict[str, str]:
    found = {}
    for line in text.splitlines():
        key, sep, value = line.partition(": ")
        if sep:
            found[key] = value
    return found


def section(text: str, name: str) -> list[str]:
    lines = text.splitlines()
    start = lines.index("section " + name) + 1
    end = start
    while end < len(lines) and not lines[end].startswith("section ") and not lines[end].startswith("result "):
        end += 1
    return lines[start:end]


def record_text(state: str) -> bytes:
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
    order = (
        "record", "schema", "desk", "book", "workflow_space", "current_work",
        "pack", "assignment_state", "waits_on", "next", "updated",
    )
    return "".join(f"{key}: {values[key]}\n" for key in order).encode("utf-8")


def launches(root: Path, delivery: str = "bridge-0001") -> list[str]:
    path = root / f"bridge/delivery/{delivery}/output/launches.log"
    if not path.is_file():
        return []
    return path.read_text(encoding="utf-8").splitlines()


def event_map(store: Path, job: str = "clerk-0001") -> dict[str, str]:
    job_dir = store / "jobs" / job
    found = {}
    if not job_dir.exists():
        return found
    for dirpath, dirnames, filenames in os.walk(job_dir):
        kept = []
        for name in dirnames:
            path = Path(dirpath) / name
            rel = str(path.relative_to(job_dir))
            if is_reparse(path):
                found[rel] = "reparse-dir"
            else:
                kept.append(name)
        dirnames[:] = kept
        for name in filenames:
            path = Path(dirpath) / name
            rel = str(path.relative_to(job_dir))
            found[rel] = "reparse" if is_reparse(path) else sha(path)
    return found


def json_events(store: Path, job: str = "clerk-0001") -> dict[str, str]:
    job_dir = store / "jobs" / job
    found = {}
    for name in ("0001.queued.json", "0002.claimed.json", "0003.returned.json", "0003.witness.json"):
        path = job_dir / name
        if path.is_file() and not is_reparse(path):
            found[name] = sha(path)
    return found


class World:
    def __init__(
        self,
        backend: str | None = None,
        timeout_s: int | None = None,
        home: Path | None = None,
        container: Path | None = None,
        fixture: Path | None = None,
        store: Path | None = None,
    ) -> None:
        if home is None:
            self.home = Path(tempfile.mkdtemp(prefix="seam0510-"))
            self.container = self.home / "container"
            self.root = self.container / "fixture"
            self.store = self.container / "clerk-store"
            self.cleanup = self.home
        else:
            self.home = Path(home)
            self.container = Path(container)
            self.root = Path(fixture)
            self.store = Path(store)
            self.cleanup = self.home
        self.instructions = self.home / "router" / "instructions"
        self.outside = self.home / "outside.txt"
        self.outside_bytes = b"outside-sentinel\n"
        self.link_rel = "clerk-link/bridge-0001.json"
        OPEN.append(self)
        self._plant(backend, timeout_s)

    def _plant(self, backend: str | None, timeout_s: int | None) -> None:
        self.home.mkdir(parents=True, exist_ok=True)
        self.instructions.mkdir(parents=True, exist_ok=True)
        (self.root / "00.kernel/00.00.10.work/0401.goal").mkdir(parents=True, exist_ok=True)
        (self.root / "00.kernel/00.00.01.law").mkdir(parents=True, exist_ok=True)
        (self.root / "00.kernel/00.00.10.work/0504.app-entry").mkdir(parents=True, exist_ok=True)
        (self.root / RECORD).write_bytes(record_text("released"))
        (self.root / WORK_REF).write_bytes(b"fixture work item\n")
        task = EXAMPLE_TASK.read_bytes()
        if hashlib.sha256(task).hexdigest() != TASK_SHA:
            raise AssertionError("design task.md hash drifted")
        (self.instructions / "task.md").write_bytes(task)
        declared = self.root / "bridge/declared"
        declared.mkdir(parents=True, exist_ok=True)
        (declared / "task.md").write_bytes(task)
        (self.root / "clerk-link").mkdir(parents=True, exist_ok=True)
        if backend is None and timeout_s is None:
            job = EXAMPLE_JOB.read_bytes()
            if hashlib.sha256(job).hexdigest() != JOB_SHA:
                raise AssertionError("design job.json hash drifted")
            (self.root / "bridge/job.json").write_bytes(job)
        else:
            job_value = json.loads(EXAMPLE_JOB.read_text(encoding="utf-8"))
            if backend is not None:
                job_value["backend"] = backend
            if timeout_s is not None:
                job_value["limits"]["timeout_s"] = timeout_s
            (self.root / "bridge/job.json").write_bytes((json.dumps(job_value, indent=2) + "\n").encode("utf-8"))
        self.outside.write_bytes(self.outside_bytes)

    def assert_held(self) -> None:
        if self.outside.read_bytes() != self.outside_bytes:
            raise AssertionError("outside sentinel changed")

    def close(self) -> None:
        if self.cleanup.exists():
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(self.cleanup)], capture_output=True, text=True)

    def clerk(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        proc = subprocess.run(
            [PY, "-B", str(CLERK), *args],
            cwd=str(foreign()),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=60,
        )
        SUITE.log.append(f"$ clerk {' '.join(args)}")
        SUITE.log.append(f"exit: {proc.returncode}")
        SUITE.log.append(proc.stdout)
        SUITE.log.append(proc.stderr)
        if check and proc.returncode != 0:
            raise AssertionError(show(proc))
        return proc

    def write_link(self, **overrides: object) -> None:
        job_bytes = (self.root / "bridge/job.json").read_bytes()
        link = {
            "schema": "librarian-clerk-link",
            "version": 1,
            "delivery_id": "bridge-0001",
            "clerk_store": str(self.store.resolve()),
            "clerk_job_id": "clerk-0001",
            "bridge_job": "bridge/job.json",
            "bridge_job_sha256": hashlib.sha256(job_bytes).hexdigest(),
        }
        link.update(overrides)
        name = str(link["delivery_id"]) + ".json"
        path = self.root / "clerk-link" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes((json.dumps(link, indent=2) + "\n").encode("utf-8"))
        self.link_rel = "clerk-link/" + name

    def ready(self, claim: bool = True) -> subprocess.CompletedProcess[str] | None:
        self.write_link()
        job = self.home / "router" / "clerk-job.json"
        job.write_bytes(EXAMPLE_CLERK.read_bytes())
        self.clerk(
            "queue",
            "--store",
            str(self.store),
            "--job",
            str(job),
            "--instructions-base",
            str(self.instructions),
        )
        if not claim:
            return None
        return self.clerk(
            "claim",
            "--store",
            str(self.store),
            "--job",
            "clerk-0001",
            "--as",
            "fixture-worker",
            "--instructions-base",
            str(self.instructions),
        )

    def deliver(
        self,
        *extra: str,
        actor: str = "fixture-worker",
        link: str | None = None,
        container: bool = True,
        timeout: float = 60,
        librarian: Path = LIBRARIAN,
    ) -> subprocess.CompletedProcess[str]:
        args = ["clerk-deliver", "--root", str(self.root)]
        if container:
            args.extend(["--container", str(self.container)])
        args.extend(
            [
                "--link",
                link or self.link_rel,
                "--as",
                actor,
                "--instructions-base",
                str(self.instructions),
                *extra,
            ]
        )
        return run(args, timeout=timeout, librarian=librarian)

    def direct(self, interrupt: str | None = None, code_root: Path = REPO, io_fault: str | None = None) -> tuple[int, str, str]:
        context = load_module(code_root / "app" / "context.py", "seam_context")
        seam = load_module(code_root / "app" / "clerk_seam.py", "seam_module")
        try:
            result = seam.perform(
                context,
                code_root,
                self.root,
                link_rel=self.link_rel,
                actor="fixture-worker",
                instructions_base=str(self.instructions),
                explicit=str(self.container),
                interrupt=interrupt,
                io_fault=io_fault,
            )
        except context.Stop as exc:
            return 2, "", "stop: " + str(exc) + "\n"
        return result.code, result.text, ""

    def outbox(self, name: str = "result.json") -> Path:
        return self.store / "jobs" / "clerk-0001" / "outbox" / name

    def provenance(self) -> Path:
        return self.root / "bridge/provenance/bridge-0001.json"

    def receipt(self) -> Path:
        return self.root / "bridge/store/bridge-0001/receipt.json"


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


def expect_attention(name: str, proc: subprocess.CompletedProcess[str], code: int, snippet: str) -> None:
    if proc.returncode != code:
        raise AssertionError(show(proc))
    if "Traceback" in proc.stderr or "Traceback" in proc.stdout:
        raise AssertionError(show(proc))
    if proc.stderr.strip():
        raise AssertionError(show(proc))
    if "seam: attention" not in proc.stdout or snippet not in proc.stdout:
        raise AssertionError(show(proc))
    if "review: not performed" not in proc.stdout or "acceptance: not performed" not in proc.stdout:
        raise AssertionError(show(proc))
    SUITE.ok(name)


def expect_success(name: str, proc: subprocess.CompletedProcess[str], clerk_line: str, place: str) -> None:
    if proc.returncode != 0 or "Traceback" in proc.stdout or "Traceback" in proc.stderr:
        raise AssertionError(show(proc))
    got = fields(proc.stdout)
    if got.get("clerk_job") != "clerk-0001" or got.get("delivery_id") != "bridge-0001":
        raise AssertionError(show(proc))
    if got.get("transport") != "delivered" or got.get("collection") != "collected":
        raise AssertionError(show(proc))
    if got.get("clerk") != clerk_line or place not in proc.stdout or RESULT_SHA not in proc.stdout:
        raise AssertionError(show(proc))
    if "not invoked" not in proc.stdout or "review: not performed" not in proc.stdout:
        raise AssertionError(show(proc))
    if "acceptance: not performed" not in proc.stdout or "approval" in proc.stdout:
        raise AssertionError(show(proc))
    SUITE.ok(name)


def claim_token(proc: subprocess.CompletedProcess[str]) -> str:
    for line in proc.stdout.splitlines():
        if line.startswith("token "):
            return line.split(" ", 1)[1]
    raise AssertionError(show(proc))


def make_junction(link: Path, target: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssertionError(proc.stdout + proc.stderr)
    JUNCTIONS.append(link)


def clear_junctions() -> None:
    while JUNCTIONS:
        link = JUNCTIONS.pop()
        if os.path.lexists(link):
            os.rmdir(link)


def close_worlds() -> None:
    clear_junctions()
    held: Exception | None = None
    while OPEN:
        world = OPEN.pop()
        try:
            world.assert_held()
        except Exception as exc:
            held = exc
        world.close()
    if held is not None:
        raise held


def test_run_refused() -> None:
    proc = run(["run", "--root", str(REPO)])
    expect_stop("normal run is not activated", proc, "normal run is not activated")


def test_success_and_replay() -> None:
    world = World()
    world.ready()
    first = world.deliver()
    expect_success("A1 clerk-deliver returns the collected artifact", first, "returned", "copied to clerk outbox")
    if launches(world.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(world.root))
    if sha(world.outbox()) != RESULT_SHA:
        raise AssertionError(sha(world.outbox()))
    shown = world.clerk(
        "show",
        "--store",
        str(world.store),
        "--job",
        "clerk-0001",
        "--instructions-base",
        str(world.instructions),
        "--json",
    )
    document = json.loads(shown.stdout)
    if document.get("schema") != "clerk-handoff-inspection/2" or document.get("state") != "returned":
        raise AssertionError(shown.stdout)
    evidence = document["returned"]["evidence"]
    receipt_sha = sha(world.receipt())
    if "bridge-0001" not in evidence or receipt_sha not in evidence or RESULT_SHA not in evidence:
        raise AssertionError(evidence)
    if document["returned"]["delivery"] != "bridge-0001":
        raise AssertionError(shown.stdout)
    reviewer = world.clerk(
        "inbox",
        "--store",
        str(world.store),
        "--as",
        "codex-prime",
        "--instructions-base",
        str(world.instructions),
    )
    returned = section(reviewer.stdout, "returned")
    if not any("clerk-0001" in line and RESULT_SHA in line for line in returned):
        raise AssertionError(reviewer.stdout)
    for actor in ("fixture-worker", "other-label"):
        inbox = world.clerk(
            "inbox",
            "--store",
            str(world.store),
            "--as",
            actor,
            "--instructions-base",
            str(world.instructions),
        )
        if any(RESULT_SHA in line for line in section(inbox.stdout, "returned")):
            raise AssertionError(inbox.stdout)
    verified = world.clerk("verify", "--store", str(world.store), "--instructions-base", str(world.instructions))
    if "result ok" not in verified.stdout:
        raise AssertionError(verified.stdout)
    status = run(
        [
            "bridge-status",
            "--root",
            str(world.root),
            "--delivery",
            "bridge-0001",
            "--container",
            str(world.container),
        ]
    )
    if status.returncode != 0 or receipt_sha not in status.stdout:
        raise AssertionError(show(status))
    before = event_map(world.store)
    second = world.deliver()
    expect_success("A1 replay is already-recorded and launches nothing", second, "already-recorded", "already in clerk outbox")
    if launches(world.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(world.root))
    if event_map(world.store) != before:
        raise AssertionError("clerk bytes changed on replay")
    wrong = world.deliver(actor="someone-else")
    expect_stop("returned replay still checks the actor", wrong, "actor is not the assignee")
    if event_map(world.store) != before or launches(world.root) != ["bridge-0001 ok"]:
        raise AssertionError("actor refusal changed the stores")
    print(f"DEMO receipt {receipt_sha}")
    print(f"DEMO artifact {RESULT_SHA}")
    print("DEMO launches 1")
    print("DEMO replay already-recorded")
    SUITE.ok("A1 reviewer inbox, verify, and one launch")


def test_interrupts() -> None:
    launch = World()
    launch.ready()
    code, text, err = launch.direct("before-launch")
    if code != 4 or "interrupted before launch" not in text or err or "Traceback" in text:
        raise AssertionError(f"{code}\n{text}\n{err}")
    if launch.provenance().exists() or launches(launch.root):
        raise AssertionError("before-launch wrote a delivery")
    done = launch.deliver()
    expect_success("B1 a later call is the one launch", done, "returned", "copied to clerk outbox")
    if launches(launch.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(launch.root))

    copied = World()
    copied.ready()
    code, text, err = copied.direct("before-copy")
    if code != 4 or "interrupted before copy" not in text or copied.outbox().exists():
        raise AssertionError(f"{code}\n{text}\n{err}")
    if launches(copied.root) != ["bridge-0001 ok"] or not copied.receipt().is_file():
        raise AssertionError("before-copy did not keep the receipt")
    again = copied.deliver()
    expect_success("B3 repeat copies without a second launch", again, "returned", "copied to clerk outbox")
    if launches(copied.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(copied.root))

    held = World()
    held.ready()
    code, text, err = held.direct("before-return")
    if code != 4 or "interrupted before return" not in text or "this-call-wrote: outbox copy" not in text:
        raise AssertionError(f"{code}\n{text}\n{err}")
    if sha(held.outbox()) != RESULT_SHA or (held.store / "jobs/clerk-0001/0003.returned.json").exists():
        raise AssertionError("before-return did not stop before the Clerk return")
    finished = held.deliver()
    expect_success("B4 repeat returns the existing copy", finished, "returned", "already in clerk outbox")
    if launches(held.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(held.root))

    reported = World()
    reported.ready()
    code, text, err = reported.direct("before-report")
    if code != 4 or "interrupted before report" not in text or "this-call-wrote: clerk return" not in text:
        raise AssertionError(f"{code}\n{text}\n{err}")
    frozen = event_map(reported.store)
    if "0003.returned.json" not in frozen:
        raise AssertionError(frozen)
    replay = reported.deliver()
    expect_success("B5 repeat is already-recorded", replay, "already-recorded", "already in clerk outbox")
    if event_map(reported.store) != frozen or launches(reported.root) != ["bridge-0001 ok"]:
        raise AssertionError("before-report replay wrote again")
    SUITE.ok("in-process interruption hooks keep the partial stores")


def test_uncertain_then_recover() -> None:
    world = World()
    world.ready()
    context = load_module(REPO / "app" / "context.py", "seam_context")
    bridge = load_module(REPO / "app" / "worker_bridge.py", "seam_bridge")
    try:
        bridge.perform(
            context,
            "bridge-test",
            REPO,
            world.root,
            job_rel="bridge/job.json",
            explicit=str(world.container),
            crash_before_receipt=True,
        )
        raise AssertionError("crash hook returned a report")
    except context.Stop:
        raise
    except Exception as exc:
        if "simulated crash" not in str(exc):
            raise
    if world.receipt().exists() or launches(world.root) != ["bridge-0001 ok"]:
        raise AssertionError("crash hook did not leave an uncertain launch")
    uncertain = world.deliver()
    expect_attention("B2 uncertain launch is not a Clerk return", uncertain, 4, "worker result is uncertain")
    if launches(world.root) != ["bridge-0001 ok"] or world.outbox().exists():
        raise AssertionError("uncertain seam relaunched or copied")
    if (world.store / "jobs/clerk-0001/0003.returned.json").exists():
        raise AssertionError("uncertain seam returned the job")
    provenance = json.loads(world.provenance().read_text(encoding="utf-8"))
    recovery = {
        "schema": "librarian-bridge-recovery",
        "version": 1,
        "delivery_id": "bridge-0001",
        "request_sha256": provenance["request_sha256"],
        "reason": "interrupted receipt",
        "requester": "fixture test",
    }
    (world.root / "bridge/recover.json").write_bytes((json.dumps(recovery, indent=2) + "\n").encode("utf-8"))
    recovered = run(
        [
            "bridge-recover",
            "--root",
            str(world.root),
            "--delivery",
            "bridge-0001",
            "--recovery-request",
            "bridge/recover.json",
            "--container",
            str(world.container),
        ]
    )
    if recovered.returncode != 0 or "recovered: true" not in recovered.stdout:
        raise AssertionError(show(recovered))
    if launches(world.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(world.root))
    done = world.deliver()
    expect_success("B2 recover then deliver does not launch", done, "returned", "copied to clerk outbox")
    if launches(world.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(world.root))
    SUITE.ok("bridge-recover stays outside clerk-deliver")


def test_wrong_claim_and_link() -> None:
    queued = World()
    queued.ready(claim=False)
    expect_stop("A9 unclaimed job", queued.deliver(), "claim first")
    if queued.provenance().exists():
        raise AssertionError("queued refusal launched")

    wrong = World()
    wrong.ready()
    expect_stop("A9 wrong actor", wrong.deliver(actor="someone-else"), "actor is not the assignee")
    if wrong.provenance().exists():
        raise AssertionError("wrong actor launched")

    missing = World()
    missing.ready()
    expect_stop("A9 missing link", missing.deliver(link="clerk-link/missing.json"), "link is missing")

    mismatched = World()
    mismatched.ready()
    job_path = mismatched.root / "bridge/job.json"
    job_path.write_bytes(job_path.read_bytes().replace(b'"timeout_s": 30', b'"timeout_s": 31'))
    expect_stop("A9 link hash does not match the job", mismatched.deliver(), "bridge job bytes do not match the link")
    if mismatched.provenance().exists():
        raise AssertionError("hash mismatch launched")

    outside = World()
    outside.ready()
    other = outside.home / "other-store"
    other.mkdir()
    outside.write_link(clerk_store=str(other.resolve()))
    expect_stop("A9 store outside the container", outside.deliver(), "clerk store is outside the designated container")
    if outside.provenance().exists():
        raise AssertionError("outside store launched")

    other_job = World()
    other_job.ready()
    other_job.write_link(clerk_job_id="clerk-9999")
    expect_stop("A9 link job does not match the bridge job", other_job.deliver(), "bridge job does not match the link")


def test_stale_instructions() -> None:
    before = World()
    before.ready()
    (before.instructions / "task.md").write_bytes(b"changed instruction\n")
    expect_stop("A10 stale instructions before delivery", before.deliver(), "stale instructions")
    if before.provenance().exists() or (before.store / "jobs/clerk-0001/0003.returned.json").exists():
        raise AssertionError("stale refusal wrote a delivery or a return")

    after = World()
    after.ready()
    code, text, err = after.direct("before-copy")
    if code != 4 or not after.receipt().is_file():
        raise AssertionError(f"{code}\n{text}\n{err}")
    (after.instructions / "task.md").write_bytes(b"changed after delivery\n")
    stale = after.deliver()
    expect_attention("A10 stale instructions after delivery", stale, 4, "stale instructions after delivery")
    if after.outbox().exists() or launches(after.root) != ["bridge-0001 ok"]:
        raise AssertionError("stale after delivery copied or relaunched")
    if (after.store / "jobs/clerk-0001/0003.returned.json").exists():
        raise AssertionError("stale after delivery became a return")

    returned = World()
    returned.ready()
    done = returned.deliver()
    expect_success("A10 setup return", done, "returned", "copied to clerk outbox")
    frozen = json_events(returned.store)
    (returned.instructions / "task.md").write_bytes(b"changed after return\n")
    replay = returned.deliver()
    expect_attention("A10 returned replay still checks instructions", replay, 4, "stale instructions after delivery")
    if json_events(returned.store) != frozen or launches(returned.root) != ["bridge-0001 ok"]:
        raise AssertionError("stale replay wrote or relaunched")


def test_conflicts_and_bytes() -> None:
    conflict = World()
    claimed = conflict.ready()
    token = claim_token(claimed)
    conflict.outbox().parent.mkdir(parents=True, exist_ok=True)
    conflict.outbox().write_bytes(b'{"count":3}')
    conflict.clerk(
        "return",
        "--store",
        str(conflict.store),
        "--job",
        "clerk-0001",
        "--as",
        "fixture-worker",
        "--claim",
        token,
        "--delivery",
        "other-0001",
        "--evidence",
        "fixture setup delivery other-0001",
    )
    expect_stop("A11 Clerk returned under another delivery", conflict.deliver(), "conflicting delivery")
    if conflict.provenance().exists():
        raise AssertionError("conflicting delivery launched")

    rebound = World()
    rebound.ready()
    launched = run(
        [
            "bridge-test",
            "--root",
            str(rebound.root),
            "--job",
            "bridge/job.json",
            "--container",
            str(rebound.container),
        ]
    )
    if launched.returncode != 0:
        raise AssertionError(show(launched))
    job_path = rebound.root / "bridge/job.json"
    job_path.write_bytes(job_path.read_bytes().replace(b'"timeout_s": 30', b'"timeout_s": 29'))
    rebound.write_link()
    expect_stop(
        "A11 provenance job hash still binds the link",
        rebound.deliver(),
        "link bridge_job_sha256 does not match the original provenance",
    )
    if rebound.outbox().exists() or launches(rebound.root) != ["bridge-0001 ok"]:
        raise AssertionError("provenance conflict copied or relaunched")

    differ = World()
    differ.ready()
    code, text, err = differ.direct("before-copy")
    if code != 4:
        raise AssertionError(f"{code}\n{text}\n{err}")
    differ.outbox().write_bytes(b"different outbox bytes\n")
    occupied = differ.deliver()
    expect_attention("A7 different outbox bytes stay", occupied, 4, "outbox bytes differ")
    if differ.outbox().read_bytes() != b"different outbox bytes\n":
        raise AssertionError("outbox was overwritten")
    if (differ.store / "jobs/clerk-0001/0003.returned.json").exists():
        raise AssertionError("different outbox was returned")

    mutated = World()
    mutated.ready()
    code, text, err = mutated.direct("before-copy")
    if code != 4:
        raise AssertionError(f"{code}\n{text}\n{err}")
    output = mutated.root / "bridge/delivery/bridge-0001/output/result.json"
    output.write_bytes(b"mutated output\n")
    changed = mutated.deliver()
    expect_attention("A7 changed bridge output is not copied", changed, 4, "bridge output does not match the receipt")
    if mutated.outbox().exists() or launches(mutated.root) != ["bridge-0001 ok"]:
        raise AssertionError("mutated output was copied or relaunched")


def test_receipt_and_damage() -> None:
    malformed = World()
    malformed.ready()
    code, text, err = malformed.direct("before-copy")
    if code != 4:
        raise AssertionError(f"{code}\n{text}\n{err}")
    malformed.receipt().write_bytes(b"{not json\n")
    expect_stop("A8 malformed receipt is refused", malformed.deliver(), "stored receipt is not strict json")
    if malformed.outbox().exists() or launches(malformed.root) != ["bridge-0001 ok"]:
        raise AssertionError("malformed receipt was copied or relaunched")
    if malformed.receipt().read_bytes() != b"{not json\n":
        raise AssertionError("refusal rewrote the receipt")

    missing = World()
    missing.ready()
    code, text, err = missing.direct("before-copy")
    if code != 4:
        raise AssertionError(f"{code}\n{text}\n{err}")
    receipt = json.loads(missing.receipt().read_text(encoding="utf-8"))
    del receipt["request_sha256"]
    missing.receipt().write_bytes((json.dumps(receipt) + "\n").encode("utf-8"))
    expect_stop("A8 receipt without request_sha256 is refused", missing.deliver(), "stored receipt field is missing: request_sha256")
    if missing.outbox().exists():
        raise AssertionError("inconsistent receipt was copied")

    bare = World()
    bare.ready()
    os.rmdir(bare.outbox().parent)
    expect_stop("B1a claim without an outbox", bare.deliver(), "claim recorded but outbox is missing")
    if bare.provenance().exists() or bare.outbox().parent.exists():
        raise AssertionError("incomplete claim was repaired or launched")

    damaged = World()
    damaged.ready()
    done = damaged.deliver()
    expect_success("B5a setup return", done, "returned", "copied to clerk outbox")
    witness = damaged.store / "jobs/clerk-0001/0003.witness.json"
    returned = damaged.store / "jobs/clerk-0001/0003.returned.json"
    witness.unlink()
    expect_attention("B5a witness mismatch stays attention", damaged.deliver(), 4, "damaged completion")
    if witness.exists() or not returned.is_file() or launches(damaged.root) != ["bridge-0001 ok"]:
        raise AssertionError("damaged completion was repaired or relaunched")

    dirty = World()
    dirty.ready()
    done = dirty.deliver()
    expect_success("artifact-changed setup return", done, "returned", "copied to clerk outbox")
    frozen = json_events(dirty.store)
    dirty.outbox().write_bytes(b"changed after return\n")
    expect_attention("returned replay sees a changed outbox", dirty.deliver(), 4, "outbox artifact changed")
    if dirty.outbox().read_bytes() != b"changed after return\n" or json_events(dirty.store) != frozen:
        raise AssertionError("artifact-changed replay rewrote the record")
    if launches(dirty.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(dirty.root))


def test_worker_outcomes() -> None:
    uncollected = World(backend="fixture-missing-artifact")
    uncollected.ready()
    expect_attention("A13 uncollected is exit 3", uncollected.deliver(), 3, "worker result is not a collected done")
    if uncollected.outbox().exists() or launches(uncollected.root) != ["bridge-0001 missing-artifact"]:
        raise AssertionError("uncollected result was copied or relaunched")
    inbox = uncollected.clerk(
        "inbox",
        "--store",
        str(uncollected.store),
        "--as",
        "codex-prime",
        "--instructions-base",
        str(uncollected.instructions),
    )
    if section(inbox.stdout, "returned") != ["none"]:
        raise AssertionError(inbox.stdout)

    failed = World()
    failed.ready()
    code, text, err = failed.direct("before-copy")
    if code != 4:
        raise AssertionError(f"{code}\n{text}\n{err}")
    receipt = json.loads(failed.receipt().read_text(encoding="utf-8"))
    receipt["claimed_outcome"] = "failed"
    failed.receipt().write_bytes((json.dumps(receipt) + "\n").encode("utf-8"))
    expect_attention("A13 collected failed is exit 3", failed.deliver(), 3, "worker result is not a collected done")
    if failed.outbox().exists() or (failed.store / "jobs/clerk-0001/0003.returned.json").exists():
        raise AssertionError("failed result became a return")
    if launches(failed.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(failed.root))

    crashed = World(backend="fixture-crash")
    crashed.ready()
    expect_attention("A13 crash is exit 4", crashed.deliver(), 4, "worker result is uncertain")
    if crashed.outbox().exists() or launches(crashed.root) != ["bridge-0001 crash"]:
        raise AssertionError("crash was copied or relaunched")

    timeout = World(backend="fixture-sleep", timeout_s=1)
    timeout.ready()
    expect_attention("A13 timeout is exit 4", timeout.deliver(timeout=40), 4, "worker result is uncertain")
    if timeout.outbox().exists() or launches(timeout.root) != ["bridge-0001 sleep"]:
        raise AssertionError("timeout was copied or relaunched")
    inbox = timeout.clerk(
        "inbox",
        "--store",
        str(timeout.store),
        "--as",
        "codex-prime",
        "--instructions-base",
        str(timeout.instructions),
    )
    if section(inbox.stdout, "returned") != ["none"]:
        raise AssertionError(inbox.stdout)


def test_placement_and_pin() -> None:
    git = REPO / ".git"
    created = False
    try:
        if not os.path.lexists(git):
            git.write_bytes(b"seam-a12\n")
            created = True
        base = REPO / "app" / "scratch" / "seam-a12"
        if base.exists():
            subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(base)], capture_output=True, text=True)
        world = World(
            home=base,
            container=REPO / "app" / "scratch",
            fixture=base / "fixture",
            store=base / "store",
        )
        world.store.mkdir(parents=True, exist_ok=True)
        world.write_link()
        placed = world.deliver(container=False)
        expect_stop("A12 scratch store is inside Git", placed, "store resolves inside a Git working tree")
        if world.provenance().exists():
            raise AssertionError("git refusal launched")
    finally:
        if created and git.is_file():
            git.unlink()

    unknown = World()
    unknown.ready()
    expect_stop("A12 unknown flag", unknown.deliver("--not-a-seam-flag"), "unknown argument")
    expect_stop("A12 test flag is not a grant", unknown.deliver("--test"), "unknown argument")
    if unknown.provenance().exists():
        raise AssertionError("unknown flag launched")

    marker = Path(tempfile.mkdtemp(prefix="seam0510-marker-"))
    code_root = Path(tempfile.mkdtemp(prefix="seam0510-code-"))
    try:
        for rel in (
            "app/context.py",
            "app/librarian.py",
            "app/clerk_seam.py",
            "app/development-workspace.json",
            "00.kernel/00.00.01.law/0302.run/02.run.003.py",
        ):
            dest = code_root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((REPO / rel).read_bytes())
        digest = sha(CLERK)
        marker_file = marker / "ran.txt"
        script = (
            "from pathlib import Path\n"
            f"Path({str(marker_file)!r}).write_text('ran\\n', encoding='utf-8')\n"
        )
        (code_root / "app/marker_clerk.py").write_bytes(script.encode("utf-8"))
        declaration = {
            "schema": "librarian-clerk-seam",
            "version": 1,
            "clerk_path": "app/marker_clerk.py",
            "clerk_sha256": digest,
        }
        (code_root / "app/clerk-seam.json").write_bytes((json.dumps(declaration, indent=2) + "\n").encode("utf-8"))
        pinned = World()
        pinned.ready()
        refused = pinned.deliver(librarian=code_root / "app/librarian.py")
        expect_stop("A14 clerk pin mismatch starts no subprocess", refused, "clerk pin does not match")
        if marker_file.exists() or pinned.provenance().exists():
            raise AssertionError("pin mismatch executed the clerk path or launched")
    finally:
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(marker)], capture_output=True, text=True)
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(code_root)], capture_output=True, text=True)


def test_occupied_paths() -> None:
    linked = World()
    linked.ready()
    code, text, err = linked.direct("before-copy")
    if code != 4:
        raise AssertionError(f"{code}\n{text}\n{err}")
    target = linked.home / "junction-target"
    target.mkdir()
    (target / "sentinel.txt").write_bytes(b"keep\n")
    make_junction(linked.outbox(), target)
    occupied = linked.deliver()
    expect_attention("occupied junction stays", occupied, 4, "outbox path is occupied")
    if (target / "sentinel.txt").read_bytes() != b"keep\n":
        raise AssertionError("junction target was changed")
    if launches(linked.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(linked.root))

    hard = World()
    hard.ready()
    code, text, err = hard.direct("before-copy")
    if code != 4:
        raise AssertionError(f"{code}\n{text}\n{err}")
    other = hard.home / "hard-source.txt"
    other.write_bytes(b"hardlink bytes\n")
    proc = subprocess.run(["cmd", "/c", "mklink", "/H", str(hard.outbox()), str(other)], capture_output=True, text=True)
    if proc.returncode != 0:
        raise AssertionError(proc.stdout + proc.stderr)
    occupied = hard.deliver()
    expect_attention("occupied hardlink stays", occupied, 4, "outbox path is occupied")
    if other.read_bytes() != b"hardlink bytes\n" or hard.outbox().read_bytes() != b"hardlink bytes\n":
        raise AssertionError("hardlink was overwritten")

    soft = World()
    soft.ready()
    code, text, err = soft.direct("before-copy")
    if code != 4:
        raise AssertionError(f"{code}\n{text}\n{err}")
    source = soft.home / "soft-source.txt"
    source.write_bytes(b"symlink bytes\n")
    proc = subprocess.run(["cmd", "/c", "mklink", str(soft.outbox()), str(source)], capture_output=True, text=True)
    detail = proc.stdout + proc.stderr
    if proc.returncode != 0:
        if "1314" in detail or "privilege" in detail.casefold():
            SUITE.skip("dangling file symlink", "WinError 1314")
            return
        raise AssertionError(detail)
    try:
        occupied = soft.deliver()
        expect_attention("occupied symlink stays", occupied, 4, "outbox path is occupied")
        if source.read_bytes() != b"symlink bytes\n":
            raise AssertionError("symlink target was overwritten")
    finally:
        if os.path.lexists(soft.outbox()):
            os.remove(soft.outbox())


def attention_text(name: str, code: int, text: str, err: str, snippet: str) -> None:
    if code != 4 or err.strip() or "Traceback" in text or "Traceback" in err:
        raise AssertionError(f"{code}\n{text}\n{err}")
    if "seam: attention" not in text or snippet not in text:
        raise AssertionError(text)
    for line in (
        "clerk_job: clerk-0001",
        "delivery_id: bridge-0001",
        "review: not performed",
        "acceptance: not performed",
        "recovery: explicit recovery is required",
    ):
        if line not in text:
            raise AssertionError(text)
    SUITE.ok(name)


def test_io_failures() -> None:
    output_name = Path("bridge/delivery/bridge-0001/output/result.json")
    partial = World()
    partial.ready()
    before_events = json_events(partial.store)
    code, text, err = partial.direct(io_fault="write")
    attention_text("partial write returns attention", code, text, err, "outbox write failed")
    blob = partial.outbox().read_bytes()
    produced = (partial.root / output_name).read_bytes()
    if blob != produced[:3] or blob.hex() != "7b2263" or len(blob) != 3:
        raise AssertionError(blob.hex())
    if sha(partial.outbox()) != "ad5e54234e32e2b67092054d1de220fa5069dd2237c2ac771b5fe634df8e308b":
        raise AssertionError(sha(partial.outbox()))
    if "this-call-wrote: partial outbox" not in text or "retained-bytes: 3" not in text:
        raise AssertionError(text)
    if "this-call-wrote: nothing" in text or "transport: delivered" in text:
        raise AssertionError(text)
    if str(partial.outbox()) not in text or "phase: write" not in text:
        raise AssertionError(text)
    if json_events(partial.store) != before_events or launches(partial.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(partial.root))
    frozen = event_map(partial.store)
    again = partial.deliver()
    expect_attention("later call keeps the partial outbox", again, 4, "outbox bytes differ")
    if "this-call-wrote: nothing" not in again.stdout:
        raise AssertionError(again.stdout)
    if partial.outbox().read_bytes() != blob or launches(partial.root) != ["bridge-0001 ok"]:
        raise AssertionError("partial outbox changed or relaunched")
    if event_map(partial.store) != frozen or (partial.store / "jobs/clerk-0001/0003.returned.json").exists():
        raise AssertionError("later call wrote a Clerk return or changed bytes")

    created = World()
    created.ready()
    code, text, err = created.direct(io_fault="create")
    attention_text("create failure returns attention", code, text, err, "outbox create failed")
    if created.outbox().exists() or "retained: absent" not in text or "this-call-wrote: nothing" not in text:
        raise AssertionError(text)
    if launches(created.root) != ["bridge-0001 ok"] or not created.receipt().is_file():
        raise AssertionError("create failure did not keep the collected delivery")
    if (created.store / "jobs/clerk-0001/0003.returned.json").exists():
        raise AssertionError("create failure returned the job")
    copied = created.deliver()
    expect_success("later call copies after a failed create", copied, "returned", "copied to clerk outbox")
    if launches(created.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(created.root))

    def full_then_return(fault: str, snippet: str) -> None:
        world = World()
        world.ready()
        code, text, err = world.direct(io_fault=fault)
        attention_text(fault + " failure returns attention", code, text, err, snippet)
        if "this-call-wrote: nothing" in text or "transport: delivered" in text:
            raise AssertionError(text)
        if str(world.outbox()) not in text:
            raise AssertionError(text)
        produced = (world.root / output_name).read_bytes()
        if not world.outbox().is_file() or world.outbox().read_bytes() != produced or sha(world.outbox()) != RESULT_SHA:
            raise AssertionError("copy fault did not retain the outbox bytes")
        if launches(world.root) != ["bridge-0001 ok"]:
            raise AssertionError(launches(world.root))
        if (world.store / "jobs/clerk-0001/0003.returned.json").exists():
            raise AssertionError("copy fault returned the job")
        second = world.deliver()
        expect_success("later call returns after " + fault + " without a new launch", second, "returned", "already in clerk outbox")
        if launches(world.root) != ["bridge-0001 ok"] or world.outbox().read_bytes() != produced:
            raise AssertionError("later call relaunched or rewrote the outbox")

    full_then_return("flush", "outbox flush failed")
    full_then_return("fsync", "outbox fsync failed")
    full_then_return("read-back", "outbox read-back failed")

    def lost_return(fault: str) -> None:
        world = World()
        world.ready()
        code, text, err = world.direct(io_fault=fault)
        attention_text(fault + " stays uncertain", code, text, err, "clerk return is uncertain")
        if "return-report: uncertain; a Clerk event may already exist" not in text:
            raise AssertionError(text)
        if "transport: delivered" in text or "this-call-wrote: nothing" in text:
            raise AssertionError(text)
        if "this-call-wrote: outbox copy" not in text or "phase: clerk-return" not in text:
            raise AssertionError(text)
        if sha(world.outbox()) != RESULT_SHA or launches(world.root) != ["bridge-0001 ok"]:
            raise AssertionError(launches(world.root))
        if not (world.store / "jobs/clerk-0001/0003.returned.json").is_file():
            raise AssertionError("injected return did not exercise the Clerk process")
        frozen = event_map(world.store)
        second = world.deliver()
        expect_success("later call inspects " + fault + " and does not relaunch", second, "already-recorded", "already in clerk outbox")
        if launches(world.root) != ["bridge-0001 ok"] or event_map(world.store) != frozen:
            raise AssertionError("uncertain return relaunched or wrote again")

    lost_return("clerk-oserror")
    lost_return("clerk-timeout")

    bare = World()
    code, text, err = bare.direct(io_fault="not-a-phase")
    if code != 2 or text.strip() or "unknown io fault" not in err or "Traceback" in err or "Traceback" in text:
        raise AssertionError(f"{code}\n{text}\n{err}")
    if launches(bare.root) or bare.provenance().exists():
        raise AssertionError("unknown io fault launched")
    SUITE.refusal("unknown io fault is refused")


def test_concurrent() -> None:
    import threading

    world = World()
    world.ready()
    results: list[subprocess.CompletedProcess[str]] = []
    errors: list[BaseException] = []

    def go() -> None:
        try:
            results.append(world.deliver())
        except BaseException as exc:
            errors.append(exc)

    threads = [threading.Thread(target=go), threading.Thread(target=go)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    if errors:
        raise AssertionError(errors)
    for proc in results:
        if "Traceback" in proc.stdout or "Traceback" in proc.stderr:
            raise AssertionError(show(proc))
        if proc.returncode not in (0, 2, 4):
            raise AssertionError(show(proc))
    if not any(proc.returncode == 0 for proc in results):
        results.append(world.deliver())
    if launches(world.root) != ["bridge-0001 ok"]:
        raise AssertionError(launches(world.root))
    if not (world.store / "jobs/clerk-0001/0003.returned.json").is_file():
        raise AssertionError("concurrent calls did not return")
    frozen = event_map(world.store)
    later = world.deliver()
    expect_success("A15 later call is already-recorded", later, "already-recorded", "already in clerk outbox")
    if launches(world.root) != ["bridge-0001 ok"] or event_map(world.store) != frozen:
        raise AssertionError("concurrent replay launched or wrote")
    SUITE.ok("A15 one launch and one return")


def check(name: str, fn) -> None:
    try:
        fn()
    except Exception:
        SUITE.fail(name, traceback.format_exc())
    finally:
        try:
            close_worlds()
        except Exception:
            SUITE.fail(name + " cleanup", traceback.format_exc())


def main() -> None:
    before_lib = REPO / "00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/before/app/librarian.py"
    before_readme = REPO / "00.kernel/00.00.10.work/0504.app-entry/evidence/seam05.10/before/app/README.md"
    if sha(before_lib) != BEFORE_LIBRARIAN or sha(before_readme) != BEFORE_README:
        raise SystemExit("source-before bytes changed")
    if sha(REPO / "app/librarian.py") == BEFORE_LIBRARIAN:
        raise SystemExit("librarian.py has no clerk-deliver edit")
    before = snap(GUARDS)
    for name, fn in (
        ("run", test_run_refused),
        ("success", test_success_and_replay),
        ("interrupts", test_interrupts),
        ("recover", test_uncertain_then_recover),
        ("claim", test_wrong_claim_and_link),
        ("stale", test_stale_instructions),
        ("conflict", test_conflicts_and_bytes),
        ("receipt", test_receipt_and_damage),
        ("outcomes", test_worker_outcomes),
        ("placement", test_placement_and_pin),
        ("occupied", test_occupied_paths),
        ("io", test_io_failures),
        ("concurrent", test_concurrent),
    ):
        check(name, fn)
    after = snap(GUARDS)
    if before != after:
        changed = [key for key in before if before[key] != after.get(key)]
        SUITE.fail("guarded bytes changed during the suite", ", ".join(changed))
    else:
        SUITE.ok("guarded bytes were unchanged")
    pyc = [path for path in (REPO / "app").rglob("__pycache__") if "scratch" not in path.parts]
    pyc += list((REPO / "00.kernel").rglob("__pycache__"))
    if pyc:
        SUITE.fail("bytecode in a book or app", "\n".join(str(path) for path in pyc))
    else:
        SUITE.ok("no bytecode was written into the books or app")
    print(
        f"summary pass {len(SUITE.passed)} "
        f"expected-refusal {len(SUITE.refusals)} "
        f"skip {len(SUITE.skipped)} "
        f"fail {len(SUITE.failed)}"
    )
    if FOREIGN is not None:
        subprocess.run(["cmd", "/c", "rmdir", "/s", "/q", str(FOREIGN)], capture_output=True, text=True)
    if SUITE.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
