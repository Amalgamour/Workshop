#!/usr/bin/env python3
"""Fixture checks for the capture-return door.

Setup calls the pinned Clerk and capture CLIs. The door itself does not
queue, claim, return, or reserve. Stores and books are disposable directories
outside the checkout. Junctions are removed with os.rmdir before the tree
is deleted. A receipt is custody, not acceptance.
"""

from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path


sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "labs" / "capture-handoff-pass01"))
import handoff  # noqa: E402

PY = sys.executable
LIBRARIAN = REPO / "app" / "librarian.py"
HANDOFF = REPO / "labs" / "capture-handoff-pass01" / "handoff.py"
REPARSE = 0x400
REPORT = b"final report body\n"
PIECE = b"piece-body-0520\n"
EVIDENCE = "transport line only"
DELIVERY = "fixture-delivery"
JOB_ID = "fixture-0520"
ASSIGNEE = "fixture-builder"
REVIEWER = "fixture-reviewer"
CLERK = "labs/clerk-handoff-pass02/clerk.py"
CAPTURE = "labs/return-capture-pass01/return_capture.py"
FILES = {"final-report.md": REPORT, "piece.txt": PIECE}
NEEDED = (
    "app/librarian.py",
    "app/handoff_tools.py",
    "app/capture-handoff.json",
    "labs/capture-handoff-pass01/handoff.py",
    "labs/clerk-handoff-pass02/clerk.py",
    "labs/return-capture-pass01/return_capture.py",
    "labs/return-capture-pass01/return_inspect.py",
)
UNTOUCHED = NEEDED + (
    "app/README.md",
    "app/context.py",
    "app/clerk_seam.py",
    "app/clerk-seam.json",
    "app/tests/test_entry.py",
    "app/tests/test_handoff_tools.py",
    "00.kernel/00.00.10.work/0504.app-entry/05.20.md",
    "00.kernel/00.00.10.work/0149.capture-handoff-entry-0520/reservation.json",
    "00.kernel/00.00.10.work/0149.capture-handoff-entry-0520/01.md",
    "00.kernel/00.00.10.work/0504.app-entry/evidence/prime-review05.19/review.md",
)
CUSTODY = (b"result complete", b"not approved", b"not accepted", b"not published")


class Skip(Exception):
    pass


class Suite:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.refusals: list[str] = []
        self.skipped: list[str] = []
        self.failed: list[str] = []

    def ok(self, name: str) -> None:
        self.passed.append(name)
        print(f"pass {name}", flush=True)

    def refuse(self, name: str) -> None:
        self.refusals.append(name)
        print(f"expected-refusal {name}", flush=True)

    def skip(self, name: str) -> None:
        self.skipped.append(name)
        print(f"skip {name}", flush=True)

    def fail(self, name: str) -> None:
        self.failed.append(name)
        print(f"fail {name}", flush=True)


SUITE = Suite()
SNAPS: list[Path] = []
JUNCTIONS: list[Path] = []


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (text + "\n").encode("utf-8")


def outside_git(path: Path) -> None:
    current = path.resolve()
    while True:
        if (current / ".git").exists():
            raise RuntimeError(f"path is inside a Git working tree: {path}")
        if current.parent == current:
            return
        current = current.parent


def env_copy() -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return env


def run(argv: list[str], env: dict, cwd: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        argv,
        cwd=str(cwd or REPO),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
    )


def run_tool(relative: str, args: list[str], env: dict) -> str:
    proc = subprocess.run(
        [PY, "-B", str(REPO / relative), *args],
        cwd=str(REPO),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
        timeout=60,
    )
    out = proc.stdout.replace(b"\r\n", b"\n").decode("utf-8")
    err = proc.stderr.replace(b"\r\n", b"\n").decode("utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"{relative} {args[0]} exit {proc.returncode}\n{out}{err}")
    return out


def field(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    raise RuntimeError(f"missing {prefix!r}\n{text}")


def is_reparse(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def remove_tree(root: Path) -> None:
    if root.exists():
        shutil.rmtree(root, ignore_errors=True)


def snapshot(world_root: Path) -> Path:
    parent = world_root.parent
    outside_git(parent)
    dest = Path(tempfile.mkdtemp(prefix="handoff0520-snap-", dir=str(parent)))
    outside_git(dest)
    shutil.copytree(world_root, dest / "tree")
    SNAPS.append(dest)
    return dest


def restore(world_root: Path, snap: Path) -> None:
    shutil.rmtree(world_root)
    shutil.copytree(snap / "tree", world_root)


def tree_digest(root: Path) -> str:
    if not root.exists():
        return "absent"
    hasher = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(dirpath) / name
            if is_reparse(path):
                hasher.update(b"link\0")
                continue
            rel = path.relative_to(root).as_posix().encode("utf-8")
            hasher.update(rel)
            hasher.update(b"\0")
            hasher.update(path.read_bytes())
            hasher.update(b"\0")
    return hasher.hexdigest()


def emit(label: str, proc: subprocess.CompletedProcess[bytes]) -> None:
    tail_out = b"" if proc.stdout.endswith(b"\n") or proc.stdout == b"" else b"\n"
    tail_err = b"" if proc.stderr.endswith(b"\n") or proc.stderr == b"" else b"\n"
    blob = b"".join([
        f"--- {label} exit {proc.returncode}\n--- stdout\n".encode("utf-8"),
        proc.stdout,
        tail_out,
        b"--- stderr\n",
        proc.stderr,
        tail_err,
        b"--- end\n",
    ])
    sys.stdout.buffer.write(blob)
    sys.stdout.buffer.flush()


def lines_of(data: bytes) -> list[bytes]:
    text = data.replace(b"\r\n", b"\n")
    if text.endswith(b"\n"):
        text = text[:-1]
    if text == b"":
        return []
    return text.split(b"\n")


def assert_stop(proc: subprocess.CompletedProcess[bytes], message: str) -> None:
    text = proc.stderr.decode("utf-8").replace("\r\n", "\n")
    if proc.returncode != 2 or f"stop: {message}" not in text or proc.stdout != b"":
        raise AssertionError((proc.returncode, text, proc.stdout[:300]))


def run_app(binding: str, env: dict, librarian: Path | None = None) -> subprocess.CompletedProcess[bytes]:
    return run([PY, "-B", str(librarian or LIBRARIAN), "capture-return", "--binding", binding], env)


def run_direct(binding: str, env: dict) -> subprocess.CompletedProcess[bytes]:
    return run([PY, "-B", str(HANDOFF), "perform", "--binding", binding], env)


def make_junction(link: Path, target: Path) -> None:
    proc = subprocess.run(
        ["cmd", "/c", "mklink", "/J", str(link), str(target)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        shell=False,
    )
    if proc.returncode != 0:
        raise AssertionError(proc.stderr.decode("utf-8", "replace"))
    JUNCTIONS.append(link)


def copy_code(dest: Path) -> Path:
    for rel in NEEDED:
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / rel).read_bytes())
    return dest


def sentinel_bytes(path: Path) -> bytes:
    text = "from pathlib import Path\nPath(%r).write_text('ran', encoding='utf-8')\n" % str(path)
    return text.encode("utf-8")


def live_bytes() -> dict[str, bytes]:
    return {rel: (REPO / rel).read_bytes() for rel in UNTOUCHED}


class World:
    def __init__(self, label: str, env: dict) -> None:
        parent = Path(tempfile.gettempdir())
        outside_git(parent)
        self.root = Path(tempfile.mkdtemp(prefix=f"handoff0520-{label}-", dir=str(parent)))
        outside_git(self.root)
        self.env = env
        self.instructions = self.root / "instructions"
        self.instructions.mkdir()
        self.task = self.instructions / "task.txt"
        self.task.write_bytes(b"fixture task\n")
        self.store = self.root / "store"
        self.book = self.root / "book"
        self.book.mkdir()
        self.source = self.root / "source"
        self.source.mkdir()
        self.record = self.root / "handoff-record"
        self.failure_log = self.root / "failure.log"
        self.binding_path = self.root / "binding.json"
        self.job_id = JOB_ID
        self.submission = "fixture-" + label
        self.member = ""
        self.event = "0" * 64
        self.work_ref = "work-ref-" + label
        self.order = ["final-report.md", "piece.txt"]
        self.outbox = self.store / "jobs" / self.job_id / "outbox"
        self.token = ""

    def close(self) -> None:
        remove_tree(self.root)

    def queue_claim(self) -> None:
        job = {
            "assignee": ASSIGNEE,
            "expected_outputs": list(self.order),
            "instructions": {"path": "task.txt", "sha256": sha256(self.task.read_bytes())},
            "job_id": self.job_id,
            "release": "fixture job label; not a release",
            "reviewer": REVIEWER,
            "routed_by": "fixture-router",
        }
        job_path = self.root / "job.json"
        job_path.write_bytes(canonical(job))
        run_tool(CLERK, [
            "queue", "--store", str(self.store), "--job", str(job_path),
            "--instructions-base", str(self.instructions),
        ], self.env)
        claimed = run_tool(CLERK, [
            "claim", "--store", str(self.store), "--job", self.job_id,
            "--as", ASSIGNEE, "--instructions-base", str(self.instructions),
        ], self.env)
        self.token = field(claimed, "token ")

    def write_files(self) -> None:
        for name, data in FILES.items():
            (self.outbox / name).write_bytes(data)
            (self.source / name).write_bytes(data)

    def do_return(self) -> None:
        text = run_tool(CLERK, [
            "return", "--store", str(self.store), "--job", self.job_id,
            "--as", ASSIGNEE, "--claim", self.token, "--delivery", DELIVERY,
            "--evidence", EVIDENCE,
        ], self.env)
        self.event = field(text, "event 0003.returned.json sha256=")
        for name, data in FILES.items():
            recorded = field(text, f"artifact {name} sha256=")
            expect = f"{sha256(data)} bytes={len(data)}"
            if recorded != expect:
                raise RuntimeError(f"artifact record {recorded} != {expect}")

    def do_reserve(self) -> None:
        args = [
            "reserve", "--book", str(self.book), "--submission", self.submission,
            "--name", "handoff", "--origin-book", "00.00.10.work",
            "--origin-page", "0504.app-entry", "--origin-batch", "05.20",
            "--submitter", "Fixture Submitter", "--reviewer", "Fixture Reviewer",
            "--release", "fixture reservation; not a release",
        ]
        for name in self.order:
            args.extend(["--expected-output", name])
        text = run_tool(CAPTURE, args, self.env)
        self.member = field(text, "member ")

    def returned(self) -> None:
        self.queue_claim()
        self.write_files()
        self.do_return()
        self.do_reserve()

    def binding(self) -> str:
        artifacts = []
        for name in self.order:
            data = FILES[name]
            artifacts.append({
                "bytes": len(data),
                "clerk_path": name,
                "logical": name,
                "sha256": sha256(data),
                "source": name,
            })
        report = FILES["final-report.md"]
        body = {
            "artifact_base": str(self.outbox),
            "artifacts": artifacts,
            "assignee": ASSIGNEE,
            "book": str(self.book),
            "clerk_store": str(self.store),
            "failure_log": str(self.failure_log),
            "instructions_base": str(self.instructions),
            "job_id": self.job_id,
            "member": self.member,
            "origin": {"batch": "05.20", "book": "00.00.10.work", "page": "0504.app-entry"},
            "record": str(self.record),
            "report": {
                "bytes": len(report),
                "clerk_path": "final-report.md",
                "sha256": sha256(report),
                "source": "final-report.md",
            },
            "returned_event_sha256": self.event,
            "schema": "clerk-capture-handoff/1",
            "source_root": str(self.source),
            "submission_id": self.submission,
            "work_ref": self.work_ref,
        }
        self.binding_path.write_bytes(canonical(body))
        return str(self.binding_path)

    def member_dir(self) -> Path:
        return self.book / self.member


def member_digest(world: World) -> str:
    return tree_digest(world.member_dir())


def record_digest(world: World) -> str:
    return tree_digest(world.record)


def assert_same(app: subprocess.CompletedProcess[bytes], direct: subprocess.CompletedProcess[bytes]) -> None:
    if app.returncode != direct.returncode or app.stdout != direct.stdout or app.stderr != direct.stderr:
        raise AssertionError((app.returncode, direct.returncode, app.stdout, direct.stdout, app.stderr, direct.stderr))


def assert_complete_pair(app: subprocess.CompletedProcess[bytes], direct: subprocess.CompletedProcess[bytes]) -> None:
    if app.returncode != 0 or direct.returncode != 0 or app.stderr or direct.stderr:
        raise AssertionError((app.returncode, direct.returncode, app.stderr, direct.stderr, app.stdout, direct.stdout))
    left = lines_of(app.stdout)
    right = lines_of(direct.stdout)
    if len(left) != len(right):
        raise AssertionError((left, right))
    for one, other in zip(left, right):
        if one.startswith((b"manifest ", b"receipt ")):
            kind = one.split(b" ", 1)[0]
            if other.split(b" ", 1)[0] != kind:
                raise AssertionError((one, other))
            if len(one.split(b" ", 1)[1]) != 64 or len(other.split(b" ", 1)[1]) != 64:
                raise AssertionError((one, other))
            continue
        if one != other:
            raise AssertionError((one, other))
    for phrase in (b"result ok", *CUSTODY):
        if phrase not in app.stdout or phrase not in direct.stdout:
            raise AssertionError(app.stdout)
    if b"writes none" in app.stdout or b"writes none" in direct.stdout:
        raise AssertionError(app.stdout)


def assert_payload(world: World) -> None:
    member = world.member_dir()
    if (member / "return.md").read_bytes() != REPORT:
        raise AssertionError("return.md is not the report")
    blobs = member / "payload"
    if (blobs / "0001.blob").read_bytes() != REPORT or (blobs / "0002.blob").read_bytes() != PIECE:
        raise AssertionError(sorted(path.name for path in blobs.iterdir()))
    completed = json.loads((world.record / "completed.json").read_bytes().decode("utf-8"))
    if completed.get("work_ref") != world.work_ref or completed.get("work_ref_role") != "declared-label":
        raise AssertionError(completed)
    if not (world.record / "intent.json").is_file():
        raise AssertionError("intent.json is absent")
    if world.failure_log.exists():
        raise AssertionError("clean handoff wrote a failure log")


def flip_event(path: Path) -> None:
    body = json.loads(path.read_bytes().decode("utf-8"))
    event = body["returned_event_sha256"]
    body["returned_event_sha256"] = event[:-1] + ("0" if event[-1] != "0" else "1")
    path.write_bytes(canonical(body))


def load_door():
    name = "librarian_handoff_tools_under_test"
    sys.modules.pop(name, None)
    spec = importlib.util.spec_from_file_location(name, REPO / "app" / "handoff_tools.py")
    if spec is None or spec.loader is None:
        raise AssertionError("could not load handoff_tools")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def perform_bytes(module, args: list[str]) -> tuple[int, bytes, bytes]:
    out = io.BytesIO()
    err = io.BytesIO()
    held_out = io.TextIOWrapper(out, encoding="utf-8", newline="\n")
    held_err = io.TextIOWrapper(err, encoding="utf-8", newline="\n")
    old_out, old_err = sys.stdout, sys.stderr
    sys.stdout = held_out
    sys.stderr = held_err
    try:
        code = module.perform(args, REPO)
    finally:
        held_out.flush()
        held_err.flush()
        held_out.detach()
        held_err.detach()
        sys.stdout = old_out
        sys.stderr = old_err
    return code, out.getvalue(), err.getvalue()


def call_fake(module, fake, args: list[str]) -> tuple[int, bytes, bytes]:
    original = subprocess.run
    subprocess.run = fake
    try:
        return perform_bytes(module, args)
    finally:
        subprocess.run = original


def main() -> None:
    print("command python -B app/tests/test_handoff_tools.py", flush=True)
    print("repo D:/Git/lib-build", flush=True)
    print("python " + PY, flush=True)
    env = env_copy()
    before = live_bytes()
    report_hash = sha256(REPORT)
    print(f"report {report_hash} {len(REPORT)}", flush=True)
    temp_root = Path(tempfile.mkdtemp(prefix="handoff0520-door-", dir=str(Path(tempfile.gettempdir()))))
    outside_git(temp_root)
    try:
        def case_flow() -> None:
            world = World("flow", env)
            try:
                world.returned()
                path = world.binding()
                ready = snapshot(world.root)
                app = run_app(path, env)
                emit("complete-app", app)
                if app.returncode != 0:
                    raise AssertionError("app capture failed")
                assert_payload(world)
                app_return = sha256((world.member_dir() / "return.md").read_bytes())
                restore(world.root, ready)
                direct = run_direct(path, env)
                emit("complete-direct", direct)
                assert_complete_pair(app, direct)
                assert_payload(world)
                direct_return = sha256((world.member_dir() / "return.md").read_bytes())
                if app_return != direct_return or direct_return != report_hash:
                    raise AssertionError((app_return, direct_return, report_hash))
                print(f"complete-return {direct_return}", flush=True)
                done = snapshot(world.root)
                before_member = member_digest(world)
                before_record = record_digest(world)
                receipt = (world.member_dir() / "receipt.json").read_bytes()
                app_again = run_app(path, env)
                direct_again = run_direct(path, env)
                emit("repeat-app", app_again)
                emit("repeat-direct", direct_again)
                assert_same(app_again, direct_again)
                if app_again.returncode != 0 or b"writes none" not in app_again.stdout:
                    raise AssertionError(app_again.stdout)
                if b"result ok" not in app_again.stdout:
                    raise AssertionError(app_again.stdout)
                for phrase in CUSTODY:
                    if phrase not in app_again.stdout:
                        raise AssertionError(app_again.stdout)
                if member_digest(world) != before_member or record_digest(world) != before_record:
                    raise AssertionError("repeat changed durable bytes")
                if (world.member_dir() / "receipt.json").read_bytes() != receipt:
                    raise AssertionError("repeat changed the receipt")
                print(f"repeat-member {before_member}", flush=True)

                restore(world.root, done)
                flip_event(world.binding_path)
                event_snap = snapshot(world.root)
                member_before = member_digest(world)
                receipt_before = (world.member_dir() / "receipt.json").read_bytes()
                app_event = run_app(path, env)
                emit("changed-event-app", app_event)
                restore(world.root, event_snap)
                direct_event = run_direct(path, env)
                emit("changed-event-direct", direct_event)
                assert_same(app_event, direct_event)
                if app_event.returncode != 2 or b"returned event does not match the binding" not in app_event.stdout:
                    raise AssertionError(app_event.stdout)
                if b"result ok" in app_event.stdout:
                    raise AssertionError(app_event.stdout)
                if member_digest(world) != member_before:
                    raise AssertionError("changed event replaced the member")
                if (world.member_dir() / "receipt.json").read_bytes() != receipt_before:
                    raise AssertionError("changed event replaced the receipt")

                restore(world.root, done)
                source = world.source / "final-report.md"
                source.write_bytes(source.read_bytes() + b"x")
                payload_snap = snapshot(world.root)
                member_before = member_digest(world)
                receipt_before = (world.member_dir() / "receipt.json").read_bytes()
                app_payload = run_app(str(world.binding_path), env)
                emit("changed-payload-app", app_payload)
                restore(world.root, payload_snap)
                direct_payload = run_direct(str(world.binding_path), env)
                emit("changed-payload-direct", direct_payload)
                assert_same(app_payload, direct_payload)
                if app_payload.returncode != 2 or b"report source bytes are not the outbox bytes" not in app_payload.stdout:
                    raise AssertionError(app_payload.stdout)
                if member_digest(world) != member_before:
                    raise AssertionError("changed payload replaced the member")
                if (world.member_dir() / "receipt.json").read_bytes() != receipt_before:
                    raise AssertionError("changed payload replaced the receipt")
            finally:
                world.close()

        def case_partial() -> None:
            world = World("partial", env)
            try:
                world.returned()
                path = world.binding()

                def hook(point: str):
                    if point == "after-capture":
                        return "stop"
                    return None

                buf = io.StringIO()
                old = sys.stdout
                sys.stdout = buf
                try:
                    code = handoff.perform(path, hook=hook)
                finally:
                    sys.stdout = old
                text = buf.getvalue()
                print("--- partial-stop exit %s" % code, flush=True)
                sys.stdout.write(text)
                if not text.endswith("\n"):
                    sys.stdout.write("\n")
                sys.stdout.flush()
                if code != 2 or "stopped after-capture" not in text or "result attention" not in text:
                    raise AssertionError(text)
                if (world.record / "completed.json").exists():
                    raise AssertionError("stop wrote completed.json")
                if (world.member_dir() / "return.md").read_bytes() != REPORT:
                    raise AssertionError("partial return.md is not the report")
                receipt = (world.member_dir() / "receipt.json").read_bytes()
                log_before = world.failure_log.read_bytes()
                before_member = member_digest(world)
                before_record = record_digest(world)
                app = run_app(path, env)
                direct = run_direct(path, env)
                emit("partial-app", app)
                emit("partial-direct", direct)
                assert_same(app, direct)
                if app.returncode != 2:
                    raise AssertionError(app.returncode)
                if b"complete capture has no completed handoff record" not in app.stdout:
                    raise AssertionError(app.stdout)
                if b"result attention" not in app.stdout or b"result ok" in app.stdout:
                    raise AssertionError(app.stdout)
                if (world.record / "completed.json").exists():
                    raise AssertionError("forwarded partial wrote completed.json")
                if member_digest(world) != before_member or record_digest(world) != before_record:
                    raise AssertionError("forwarded partial changed durable bytes")
                if (world.member_dir() / "receipt.json").read_bytes() != receipt:
                    raise AssertionError("forwarded partial changed the receipt")
                if world.failure_log.read_bytes() != log_before:
                    raise AssertionError("forwarded partial changed the failure log")
                print(f"partial-receipt {sha256(receipt)} {len(receipt)}", flush=True)
            finally:
                world.close()

        def case_malformed() -> None:
            folder = Path(tempfile.mkdtemp(prefix="handoff0520-bad-", dir=str(temp_root)))
            outside_git(folder)
            binding = folder / "binding.json"
            binding.write_bytes(b"{not json\n")
            app = run_app(str(binding), env)
            direct = run_direct(str(binding), env)
            emit("malformed-app", app)
            emit("malformed-direct", direct)
            assert_same(app, direct)
            if app.returncode != 2 or b"binding is not strict json" not in app.stdout:
                raise AssertionError(app.stdout)
            if (folder / "failure.log").exists() or (folder / "store").exists():
                raise AssertionError("malformed binding launched custody tools")

        def case_relative() -> None:
            proc = run([PY, "-B", str(LIBRARIAN), "capture-return", "--binding", "binding.json"], env)
            assert_stop(proc, "binding path must be absolute")

        def case_missing() -> None:
            missing = temp_root / "missing-binding.json"
            proc = run_app(str(missing), env)
            assert_stop(proc, "binding path is not a plain file")

        def case_linked() -> None:
            target = temp_root / "link-target"
            target.mkdir()
            (target / "binding.json").write_bytes(b"{}\n")
            link = temp_root / "link-binding"
            make_junction(link, target)
            proc = run_app(str(link), env)
            assert_stop(proc, "binding path is linked and was not followed")

        def case_override() -> None:
            present = temp_root / "override-binding.json"
            present.write_bytes(b"{}\n")
            proc = run([
                PY, "-B", str(LIBRARIAN), "capture-return",
                "--binding", str(present), "--handoff", str(HANDOFF),
            ], env)
            assert_stop(proc, "caller tool override is refused")

        def case_timeout_flag() -> None:
            present = temp_root / "timeout-binding.json"
            present.write_bytes(b"{}\n")
            proc = run([
                PY, "-B", str(LIBRARIAN), "capture-return",
                "--binding", str(present), "--timeout", "1",
            ], env)
            assert_stop(proc, "caller timeout is refused")

        def case_unknown_flag() -> None:
            present = temp_root / "unknown-binding.json"
            present.write_bytes(b"{}\n")
            proc = run([
                PY, "-B", str(LIBRARIAN), "capture-return",
                "--binding", str(present), "--model",
            ], env)
            assert_stop(proc, "unsupported argument")

        def case_repeated() -> None:
            present = temp_root / "repeat-binding.json"
            present.write_bytes(b"{}\n")
            proc = run([
                PY, "-B", str(LIBRARIAN), "capture-return",
                "--binding", str(present), "--binding", str(present),
            ], env)
            assert_stop(proc, "repeated --binding")

        def case_normal_run() -> None:
            proc = run([PY, "-B", str(LIBRARIAN), "run"], env)
            assert_stop(proc, "normal run is not activated")

        def case_unknown_child() -> None:
            present = temp_root / "child-binding.json"
            present.write_bytes(b"{}\n")
            module = load_door()
            calls = []

            def fake(argv, **kwargs):
                calls.append((list(argv), dict(kwargs)))
                return subprocess.CompletedProcess(argv, 1, b"partial-bytes", b"")

            code, out, err = call_fake(module, fake, ["--binding", str(present)])
            if len(calls) != 1 or "timeout" in calls[0][1] or calls[0][1].get("shell") is not False:
                raise AssertionError(calls)
            if calls[0][0][1:4] != ["-B", str(HANDOFF), "perform"]:
                raise AssertionError(calls[0][0])
            if code != 1 or out != b"partial-bytes" or b"writes none" in err:
                raise AssertionError((code, out, err))
            if b"inspect retained state" not in err or b"does not retry" not in err:
                raise AssertionError(err)
            print(f"unknown-exit stderr {err.decode('utf-8').rstrip()}", flush=True)

        def case_missing_exit() -> None:
            present = temp_root / "missing-exit-binding.json"
            present.write_bytes(b"{}\n")
            module = load_door()
            calls = []

            def fake(argv, **kwargs):
                calls.append(1)
                return subprocess.CompletedProcess(argv, None, b"", b"")

            code, out, err = call_fake(module, fake, ["--binding", str(present)])
            if calls != [1] or code == 0 or out != b"" or b"writes none" in err:
                raise AssertionError((calls, code, out, err))
            if b"inspect retained state" not in err or b"does not retry" not in err:
                raise AssertionError(err)

        def case_known_forward() -> None:
            present = temp_root / "known-binding.json"
            present.write_bytes(b"{}\n")
            module = load_door()

            def fake(argv, **kwargs):
                return subprocess.CompletedProcess(argv, 2, b"refused: sample\nwrites none\nresult refused\n", b"")

            code, out, err = call_fake(module, fake, ["--binding", str(present)])
            if code != 2 or err != b"" or b"writes none\n" not in out:
                raise AssertionError((code, out, err))
            if b"inspect retained state" in err:
                raise AssertionError(err)

        def case_start_failed() -> None:
            present = temp_root / "start-binding.json"
            present.write_bytes(b"{}\n")
            module = load_door()

            def fake(argv, **kwargs):
                raise OSError("denied")

            try:
                call_fake(module, fake, ["--binding", str(present)])
            except module.Refuse as exc:
                if "writes none" in str(exc) or "failed to start" not in str(exc):
                    raise AssertionError(str(exc))
            else:
                raise AssertionError("start failure returned")

        def pin_stop(name: str, mutate, message: str) -> None:
            code = copy_code(temp_root / name)
            ran = temp_root / (name + "-ran.txt")
            mutate(code, ran)
            present = temp_root / (name + "-binding.json")
            present.write_bytes(b"{}\n")
            proc = run_app(str(present), env, code / "app" / "librarian.py")
            assert_stop(proc, message)
            if ran.exists():
                raise AssertionError(name + " launched")

        def case_decl_hash() -> None:
            def mutate(code: Path, ran: Path) -> None:
                path = code / "app" / "capture-handoff.json"
                document = json.loads(path.read_text(encoding="utf-8"))
                document["tools"]["handoff"]["sha256"] = "0" * 64
                path.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
                (code / "labs" / "capture-handoff-pass01" / "handoff.py").write_bytes(sentinel_bytes(ran))

            pin_stop("decl-hash", mutate, "capture handoff declaration does not match the pinned tools")

        def case_decl_unknown() -> None:
            def mutate(code: Path, ran: Path) -> None:
                path = code / "app" / "capture-handoff.json"
                document = json.loads(path.read_text(encoding="utf-8"))
                document["extra"] = 1
                path.write_bytes((json.dumps(document, indent=2) + "\n").encode("utf-8"))
                (code / "labs" / "capture-handoff-pass01" / "handoff.py").write_bytes(sentinel_bytes(ran))

            pin_stop("decl-unknown", mutate, "capture handoff declaration has an unknown field: extra")

        def case_decl_repeat() -> None:
            def mutate(code: Path, ran: Path) -> None:
                raw = b'{"schema":"librarian-capture-handoff","schema":"librarian-capture-handoff"}\n'
                (code / "app" / "capture-handoff.json").write_bytes(raw)
                (code / "labs" / "capture-handoff-pass01" / "handoff.py").write_bytes(sentinel_bytes(ran))

            pin_stop("decl-repeat", mutate, "capture handoff declaration repeats schema")

        def case_tool_bytes() -> None:
            def mutate(code: Path, ran: Path) -> None:
                (code / "labs" / "capture-handoff-pass01" / "handoff.py").write_bytes(sentinel_bytes(ran))

            pin_stop("tool-bytes", mutate, "pinned tool hash does not match: handoff")

        def case_tool_junction() -> None:
            code = copy_code(temp_root / "pin-junction")
            lab = code / "labs" / "capture-handoff-pass01"
            outside = temp_root / "outside-handoff"
            shutil.copytree(lab, outside)
            shutil.rmtree(lab)
            make_junction(lab, outside)
            ran = temp_root / "junction-ran.txt"
            (outside / "handoff.py").write_bytes(sentinel_bytes(ran))
            present = temp_root / "junction-binding.json"
            present.write_bytes(b"{}\n")
            proc = run_app(str(present), env, code / "app" / "librarian.py")
            assert_stop(proc, "tool path is linked and was not followed")
            if ran.exists():
                raise AssertionError("junction was followed")

        def case_file_symlink() -> None:
            code = copy_code(temp_root / "pin-symlink")
            tool = code / "labs" / "capture-handoff-pass01" / "handoff.py"
            outside = temp_root / "linked-handoff.py"
            outside.write_bytes(tool.read_bytes())
            tool.unlink()
            try:
                os.symlink(outside, tool)
            except OSError as exc:
                if getattr(exc, "winerror", None) == 1314:
                    raise Skip("file symlink privilege WinError 1314") from exc
                raise
            present = temp_root / "symlink-binding.json"
            present.write_bytes(b"{}\n")
            proc = run_app(str(present), env, code / "app" / "librarian.py")
            assert_stop(proc, "tool path is linked and was not followed")

        checks = [
            ("complete-and-repeat", "pass", case_flow),
            ("partial-forwarded", "pass", case_partial),
            ("malformed-binding", "refuse", case_malformed),
            ("relative-binding", "refuse", case_relative),
            ("missing-binding", "refuse", case_missing),
            ("linked-binding", "refuse", case_linked),
            ("tool-override", "refuse", case_override),
            ("caller-timeout", "refuse", case_timeout_flag),
            ("unknown-flag", "refuse", case_unknown_flag),
            ("repeated-binding", "refuse", case_repeated),
            ("normal-run", "refuse", case_normal_run),
            ("unknown-exit", "pass", case_unknown_child),
            ("missing-exit", "pass", case_missing_exit),
            ("known-exit-forwarded", "pass", case_known_forward),
            ("start-failed", "refuse", case_start_failed),
            ("declaration-hash", "refuse", case_decl_hash),
            ("declaration-unknown", "refuse", case_decl_unknown),
            ("declaration-repeat", "refuse", case_decl_repeat),
            ("tool-bytes", "refuse", case_tool_bytes),
            ("tool-junction", "refuse", case_tool_junction),
            ("file-symlink", "refuse", case_file_symlink),
        ]
        for name, kind, fn in checks:
            try:
                fn()
            except Skip as exc:
                SUITE.skip(f"{name} {exc}")
                continue
            except Exception:
                SUITE.fail(name)
                traceback.print_exc()
                continue
            if kind == "pass":
                SUITE.ok(name)
            else:
                SUITE.refuse(name)
        after = live_bytes()
        if after != before:
            changed = [rel for rel in UNTOUCHED if after[rel] != before[rel]]
            SUITE.fail("untouched")
            print("changed " + " ".join(changed), flush=True)
        else:
            SUITE.ok("untouched")
    finally:
        for link in reversed(JUNCTIONS):
            if os.path.lexists(link):
                try:
                    os.rmdir(link)
                except OSError:
                    pass
        for snap in SNAPS:
            remove_tree(snap)
        remove_tree(temp_root)
    print(
        f"summary pass {len(SUITE.passed)} expected-refusal {len(SUITE.refusals)} "
        f"skip {len(SUITE.skipped)} fail {len(SUITE.failed)}",
        flush=True,
    )
    if SUITE.failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
