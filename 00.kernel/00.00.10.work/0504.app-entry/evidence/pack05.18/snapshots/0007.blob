"""Fixture proof for labs/capture-handoff-pass01/handoff.py.

Setup calls the pinned Clerk and capture CLIs. perform does not queue, claim,
return, or reserve. Stores and books are disposable directories outside the
checkout. Junctions are removed with os.rmdir before the tree is deleted.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import traceback
from pathlib import Path


sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "labs" / "capture-handoff-pass01"))
import handoff  # noqa: E402


REPORT = b"final report body\n"
PIECE = b"piece-body-0517\n"
EVIDENCE = "transport line only"
DELIVERY = "fixture-delivery"
JOB_ID = "fixture-0517"
ASSIGNEE = "fixture-builder"
REVIEWER = "fixture-reviewer"
CLERK = "labs/clerk-handoff-pass02/clerk.py"
CAPTURE = "labs/return-capture-pass01/return_capture.py"
FILES = {
    "final-report.md": REPORT,
    "piece.txt": PIECE,
}
COUNTS = {"pass": 0, "expected-refusal": 0, "skip": 0, "fail": 0}


def outside_git(path: Path) -> None:
    current = path.resolve()
    while True:
        if (current / ".git").exists():
            raise RuntimeError(f"path is inside a Git working tree: {path}")
        if current.parent == current:
            return
        current = current.parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (text + "\n").encode("utf-8")


def run_tool(relative: str, args: list[str]) -> str:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    proc = subprocess.run(
        [sys.executable, "-B", str(ROOT / relative), *args],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
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


def perform(path: str, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = handoff.perform(path, **kwargs)
    return code, buf.getvalue()


def remove_tree(root: Path, links: list[Path]) -> None:
    for link in links:
        if os.path.lexists(link):
            try:
                if stat.S_ISDIR(os.lstat(link).st_mode):
                    os.rmdir(link)
                else:
                    os.remove(link)
            except OSError:
                pass
    if root.exists():
        shutil.rmtree(root, ignore_errors=True)


def band_members(book: Path) -> list[str]:
    found = []
    if not book.exists():
        return found
    for name in os.listdir(book):
        if len(name) < 5 or not name[:4].isdigit() or name[4] != ".":
            continue
        number = int(name[:4])
        if 101 <= number <= 199:
            found.append(name)
    return sorted(found)


class World:
    def __init__(self, label: str) -> None:
        parent = Path(tempfile.gettempdir())
        outside_git(parent)
        self.root = Path(tempfile.mkdtemp(prefix=f"handoff0517-{label}-", dir=str(parent)))
        outside_git(self.root)
        self.links: list[Path] = []
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
        self.batch = "05.17"
        self.order = ["final-report.md", "piece.txt"]
        self.outbox = self.store / "jobs" / self.job_id / "outbox"
        self.token = ""

    def close(self) -> None:
        remove_tree(self.root, self.links)

    def queue_claim(self) -> None:
        job = {
            "assignee": ASSIGNEE,
            "expected_outputs": list(self.order),
            "instructions": {"path": "task.txt", "sha256": digest(self.task.read_bytes())},
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
        ])
        claimed = run_tool(CLERK, [
            "claim", "--store", str(self.store), "--job", self.job_id,
            "--as", ASSIGNEE, "--instructions-base", str(self.instructions),
        ])
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
        ])
        self.event = field(text, "event 0003.returned.json sha256=")
        for name, data in FILES.items():
            prefix = f"artifact {name} sha256="
            recorded = field(text, prefix)
            expect = f"{digest(data)} bytes={len(data)}"
            if recorded != expect:
                raise RuntimeError(f"artifact record {recorded} != {expect}")

    def do_reserve(self, outputs: list[str] | None = None, batch: str | None = None, submission: str | None = None) -> None:
        chosen = outputs or self.order
        sub = submission or self.submission
        origin_batch = batch or self.batch
        args = [
            "reserve", "--book", str(self.book), "--submission", sub,
            "--name", "handoff", "--origin-book", "00.00.10.work",
            "--origin-page", "0504.app-entry", "--origin-batch", origin_batch,
            "--submitter", "Fixture Submitter", "--reviewer", "Fixture Reviewer",
            "--release", "fixture reservation; not a release",
        ]
        for name in chosen:
            args.extend(["--expected-output", name])
        text = run_tool(CAPTURE, args)
        self.member = field(text, "member ")
        if submission is None:
            self.submission = sub

    def returned(self, outputs: list[str] | None = None, batch: str | None = None, submission: str | None = None) -> None:
        if outputs is not None:
            self.order = list(outputs)
        self.queue_claim()
        self.write_files()
        self.do_return()
        self.do_reserve(outputs=self.order, batch=batch, submission=submission)

    def binding(self, **overrides) -> str:
        artifacts = []
        for name in self.order:
            data = FILES[name]
            artifacts.append({
                "bytes": len(data),
                "clerk_path": name,
                "logical": name,
                "sha256": digest(data),
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
            "origin": {"batch": self.batch, "book": "00.00.10.work", "page": "0504.app-entry"},
            "record": str(self.record),
            "report": {
                "bytes": len(report),
                "clerk_path": "final-report.md",
                "sha256": digest(report),
                "source": "final-report.md",
            },
            "returned_event_sha256": self.event,
            "schema": "clerk-capture-handoff/1",
            "source_root": str(self.source),
            "submission_id": self.submission,
            "work_ref": self.work_ref,
        }
        for key, value in overrides.items():
            if key == "report" and isinstance(value, dict):
                body["report"].update(value)
            elif key == "origin" and isinstance(value, dict):
                body["origin"].update(value)
            else:
                body[key] = value
        self.binding_path.write_bytes(canonical(body))
        return str(self.binding_path)

    def job_names(self) -> list[str]:
        return sorted(os.listdir(self.store / "jobs" / self.job_id))

    def member_dir(self) -> Path:
        return self.book / self.member


def refusal(text: str) -> str:
    for line in text.splitlines():
        if line.startswith("refused: ") or line.startswith("attention: "):
            return line.split(": ", 1)[1]
    raise AssertionError("no refusal line\n" + text)


def assert_refused(code: int, text: str, message: str) -> str:
    if code != 2:
        raise AssertionError(f"exit {code}\n{text}")
    reason = refusal(text)
    if message not in reason:
        raise AssertionError(f"{reason}\n{text}")
    if "result refused" not in text and "result attention" not in text:
        raise AssertionError(text)
    return reason


def tree_digest(root: Path) -> str:
    hasher = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(dirpath) / name
            rel = path.relative_to(root).as_posix().encode("utf-8")
            hasher.update(rel)
            hasher.update(b"\0")
            hasher.update(digest(path.read_bytes()).encode("ascii"))
    return hasher.hexdigest()


def case_clean() -> tuple[str, str]:
    world = World("clean")
    calls = []
    real_launch = handoff.launch

    def wrapped(script, args, pins):
        calls.append((script, list(args)))
        return real_launch(script, args, pins)

    try:
        world.returned()
        path = world.binding()
        before_job = world.job_names()
        before_members = band_members(world.book)
        handoff.launch = wrapped
        code, text = perform(path)
        if code != 0 or "result ok" not in text:
            raise AssertionError(text)
        if "writes none" in text:
            raise AssertionError(text)
        return_file = (world.member_dir() / "return.md").read_bytes()
        if return_file != REPORT:
            raise AssertionError("return.md is not the report")
        if EVIDENCE.encode("utf-8") in return_file or DELIVERY.encode("utf-8") in return_file:
            raise AssertionError("transport text was copied into return.md")
        piece = (world.member_dir() / "payload" / "0002.blob").read_bytes()
        report_blob = (world.member_dir() / "payload" / "0001.blob").read_bytes()
        if report_blob != REPORT or piece != PIECE:
            raise AssertionError("payload bytes differ")
        completed = json.loads((world.record / "completed.json").read_bytes().decode("utf-8"))
        intent = json.loads((world.record / "intent.json").read_bytes().decode("utf-8"))
        if completed["work_ref"] != world.work_ref or completed["work_ref_role"] != "declared-label":
            raise AssertionError("work_ref was treated as more than a declared label")
        if intent["transport"]["evidence"] != EVIDENCE or intent["transport"]["delivery"] != DELIVERY:
            raise AssertionError("transport pair was not recorded on the intent")
        if world.failure_log.exists():
            raise AssertionError("clean handoff wrote a failure log")
        if world.job_names() != before_job or band_members(world.book) != before_members:
            raise AssertionError("adapter changed the job directory or allocated a member")
        commands = [args[0] for _script, args in calls]
        if commands != ["show", "inspect", "capture", "verify", "inspect"]:
            raise AssertionError(f"commands {commands}")
        capture_args = calls[2][1]
        if "--retrospective" in capture_args or "--source-commit" in capture_args:
            raise AssertionError("capture flags were set")
        if "--return-includes-prime-review" in capture_args:
            raise AssertionError("prime-review flag was set")
        receipt = field(text, "receipt ")
        first_tree = tree_digest(world.root)
        handoff.launch = real_launch
        code, retry = perform(path)
        if code != 0 or "writes none" not in retry or "result ok" not in retry:
            raise AssertionError(retry)
        if tree_digest(world.root) != first_tree:
            raise AssertionError("identical retry changed the tree")
        return "pass", f" event={world.event} receipt={receipt}"
    finally:
        handoff.launch = real_launch
        world.close()


def case_changed_event() -> tuple[str, str]:
    world = World("event")
    try:
        world.returned()
        path = world.binding()
        code, text = perform(path)
        if code != 0:
            raise AssertionError(text)
        completed = (world.record / "completed.json").read_bytes()
        receipt = (world.member_dir() / "receipt.json").read_bytes()
        original = world.event
        flipped = world.event[:-1] + ("0" if world.event[-1] != "0" else "1")
        world.event = flipped
        world.binding()
        code, text = perform(str(world.binding_path))
        reason = assert_refused(code, text, "returned event does not match the binding")
        if (world.record / "completed.json").read_bytes() != completed:
            raise AssertionError("completed record was overwritten")
        if (world.member_dir() / "receipt.json").read_bytes() != receipt:
            raise AssertionError("receipt changed")
        body = json.loads(world.binding_path.read_bytes().decode("utf-8"))
        body["returned_event_sha256"] = original
        body["work_ref"] = world.work_ref + "-other"
        world.binding_path.write_bytes(canonical(body))
        log_before = world.failure_log.read_bytes()
        code, text = perform(str(world.binding_path))
        reason2 = assert_refused(code, text, "completed handoff record does not match the binding")
        if (world.record / "completed.json").read_bytes() != completed:
            raise AssertionError("work_ref change overwrote the completed record")
        if world.failure_log.read_bytes() != log_before:
            raise AssertionError("second failure overwrote the failure log")
        return "expected-refusal", f": {reason}; {reason2}"
    finally:
        world.close()


def case_unrelated_report() -> tuple[str, str]:
    world = World("report")
    try:
        world.returned()
        world.binding(report={
            "clerk_path": "side-report.md",
            "source": "side-report.md",
            "sha256": digest(b"side\n"),
            "bytes": 5,
        })
        before = world.job_names()
        code, text = perform(str(world.binding_path))
        reason = assert_refused(code, text, "report is not a returned artifact")
        if (world.record / "intent.json").exists() or (world.member_dir() / "return.md").exists():
            raise AssertionError("unrelated report started a handoff")
        if world.job_names() != before:
            raise AssertionError("job directory changed")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_dirty() -> tuple[str, str]:
    world = World("dirty")
    try:
        world.returned()
        (world.outbox / "piece.txt").write_bytes(b"mutated-piece\n")
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "artifacts are changed")
        if (world.record / "intent.json").exists() or (world.member_dir() / "return.md").exists():
            raise AssertionError("dirty artifacts were captured")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_claimed() -> tuple[str, str]:
    world = World("claimed")
    try:
        world.queue_claim()
        world.do_reserve()
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "state is claimed")
        if (world.record / "intent.json").exists():
            raise AssertionError("claimed job created an intent")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_unusable() -> tuple[str, str]:
    world = World("unusable")
    try:
        world.returned()
        world.task.write_bytes(b"changed task\n")
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "instructions are unusable")
        if (world.record / "intent.json").exists():
            raise AssertionError("unusable instructions created an intent")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_not_checked() -> tuple[str, str]:
    document = {
        "schema": "clerk-handoff-inspection/2",
        "job_id": JOB_ID,
        "state": "returned",
        "returned": {
            "by": ASSIGNEE,
            "delivery": DELIVERY,
            "evidence": EVIDENCE,
            "artifacts": [],
            "event_sha256": "ab" * 32,
        },
        "checks": {
            "events": "ok",
            "completion": "ok",
            "artifacts": "ok",
            "instructions": "not-checked",
        },
        "problems": [],
    }
    parsed = {
        "job_id": JOB_ID,
        "returned_event_sha256": "ab" * 32,
        "assignee": ASSIGNEE,
    }
    try:
        handoff.load_returned(document, parsed)
    except handoff.Refuse as exc:
        if exc.message != "instructions are not-checked":
            raise AssertionError(exc.message)
        return "expected-refusal", f": {exc.message}"
    raise AssertionError("not-checked was accepted")


def case_wrong_origin() -> tuple[str, str]:
    world = World("origin")
    try:
        world.returned(batch="05.16")
        world.batch = "05.17"
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "origin does not match the reservation")
        if (world.record / "intent.json").exists():
            raise AssertionError("wrong origin created an intent")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_wrong_submission() -> tuple[str, str]:
    world = World("submission")
    try:
        world.returned(submission="fixture-reserved")
        world.submission = "fixture-binding"
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "submission does not match the reservation")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_wrong_order() -> tuple[str, str]:
    world = World("order")
    try:
        world.queue_claim()
        world.write_files()
        world.do_return()
        world.do_reserve(outputs=["piece.txt", "final-report.md"])
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "logical outputs do not match the reservation")
        if (world.member_dir() / "return.md").exists():
            raise AssertionError("wrong order captured")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_preexisting() -> tuple[str, str]:
    world = World("adopt")
    try:
        world.returned()
        path = world.binding()
        report = str(world.source / "final-report.md")
        run_tool(CAPTURE, [
            "capture", "--book", str(world.book), "--submission", world.submission,
            "--return-file", report, "--source-root", str(world.source),
            "--artifact", "final-report.md|final-report.md",
            "--artifact", "piece.txt|piece.txt",
        ])
        receipt = (world.member_dir() / "receipt.json").read_bytes()
        code, text = perform(path)
        reason = assert_refused(code, text, "complete capture has no completed handoff record")
        if (world.record / "completed.json").exists():
            raise AssertionError("preexisting capture was adopted")
        if (world.member_dir() / "receipt.json").read_bytes() != receipt:
            raise AssertionError("receipt changed")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_partial() -> tuple[str, str]:
    world = World("partial")
    try:
        world.returned()
        planted = world.member_dir() / "return.md"
        planted.write_bytes(b"partial-planted\n")
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "partial capture is retained")
        if planted.read_bytes() != b"partial-planted\n":
            raise AssertionError("planted return.md was removed")
        if (world.record / "intent.json").exists() or (world.member_dir() / "manifest.json").exists():
            raise AssertionError("partial member was repaired")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_hardlink() -> tuple[str, str]:
    world = World("hardlink")
    try:
        world.returned()
        os.link(world.source / "piece.txt", world.source / "piece-also.txt")
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "link-count: artifact source")
        if (world.record / "intent.json").exists():
            raise AssertionError("hardlink created an intent")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_junction() -> tuple[str, str]:
    world = World("junction")
    try:
        world.returned()
        link = world.root / "linked-source"
        proc = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(world.source)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.decode("utf-8", errors="replace"))
        world.links.append(link)
        world.binding(source_root=str(link))
        code, text = perform(str(world.binding_path))
        reason = assert_refused(code, text, f"link: {link}")
        if (world.source / "final-report.md").read_bytes() != REPORT:
            raise AssertionError("junction target was followed into a write")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_symlink() -> tuple[str, str]:
    world = World("symlink")
    link = None
    try:
        world.returned()
        target = world.root / "piece-target.txt"
        target.write_bytes(PIECE)
        link = world.source / "piece.txt"
        link.unlink()
        try:
            os.symlink(target, link)
        except OSError as exc:
            if getattr(exc, "winerror", None) == 1314:
                link.write_bytes(PIECE)
                return "skip", ": WinError 1314"
            raise
        world.links.append(link)
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "link:")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_bad_pins() -> tuple[str, str]:
    world = World("pins")
    seen = []
    try:
        world.instructions.mkdir(exist_ok=True)
        world.store.mkdir()
        world.member = "0101.pins"
        pins = handoff.default_pins()
        path, _digest = pins["capture"]
        pins["capture"] = (path, "ab" * 32)

        def hook(point):
            seen.append(point)
            return None

        code, text = perform(world.binding(), hook=hook, pins=pins)
        reason = assert_refused(code, text, "pin hash mismatch: capture")
        if seen:
            raise AssertionError(f"hook ran before the pin refusal: {seen}")
        log = json.loads(world.failure_log.read_bytes().decode("utf-8"))
        if log["schema"] != "clerk-capture-handoff-failure/1" or log["tool_stdout"] != []:
            raise AssertionError("pin refusal started a tool or skipped the log")
        first = world.failure_log.read_bytes()
        code, text = perform(str(world.binding_path), hook=hook, pins=pins)
        assert_refused(code, text, "pin hash mismatch: capture")
        if world.failure_log.read_bytes() != first:
            raise AssertionError("second pin failure overwrote the log")
        if "writes none" not in text or str(world.failure_log) not in text:
            raise AssertionError(text)
        if seen:
            raise AssertionError("second pin failure ran a hook")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_stop(point: str, label: str) -> tuple[str, str]:
    world = World(label)
    try:
        if point == "before-intent":
            world.store.mkdir()
            world.do_reserve()
            path = world.binding()
        else:
            world.returned()
            path = world.binding()
        before_job = world.job_names() if point != "before-intent" else []

        def hook(seen):
            if seen == point:
                return "stop"
            return None

        code, text = perform(path, hook=hook)
        reason = assert_refused(code, text, f"stopped {point}")
        completed = world.record / "completed.json"
        if completed.exists():
            raise AssertionError("stopped handoff wrote completed.json")
        if point == "before-intent":
            if (world.record / "intent.json").exists():
                raise AssertionError("before-intent stop wrote intent.json")
            log = json.loads(world.failure_log.read_bytes().decode("utf-8"))
            if log["tool_stdout"] != []:
                raise AssertionError("before-intent stop launched a tool")
            return "expected-refusal", f": {reason}"
        intent = (world.record / "intent.json").read_bytes()
        if point == "after-intent" and (world.member_dir() / "return.md").exists():
            raise AssertionError("after-intent stop captured")
        if point in ("after-capture", "before-final-record"):
            if (world.member_dir() / "return.md").read_bytes() != REPORT:
                raise AssertionError("capture did not keep the report")
        log_bytes = world.failure_log.read_bytes()
        code, text = perform(path)
        reason2 = assert_refused(
            code,
            text,
            "intent is retained" if point == "after-intent" else "complete capture has no completed handoff record",
        )
        if (world.record / "intent.json").read_bytes() != intent:
            raise AssertionError("retry changed the retained intent")
        if world.failure_log.read_bytes() != log_bytes:
            raise AssertionError("retry overwrote the failure log")
        if completed.exists():
            raise AssertionError("retry finished the record")
        if point != "before-intent" and world.job_names() != before_job:
            raise AssertionError("stop changed the job directory")
        return "expected-refusal", f": {reason}; {reason2}"
    finally:
        world.close()


def case_source_changed() -> tuple[str, str]:
    world = World("source")
    try:
        world.returned()
        path = world.binding()

        def hook(point):
            if point == "after-capture":
                (world.source / "piece.txt").write_bytes(b"changed-after-capture\n")
            return None

        code, text = perform(path, hook=hook)
        reason = assert_refused(code, text, "source bytes changed before the handoff record")
        if (world.record / "completed.json").exists():
            raise AssertionError("source change still wrote completed.json")
        if (world.member_dir() / "return.md").read_bytes() != REPORT:
            raise AssertionError("captured report changed with the later source")
        if (world.outbox / "piece.txt").read_bytes() != PIECE:
            raise AssertionError("outbox was rewritten")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_pin_changed() -> tuple[str, str]:
    world = World("pinlate")
    pins = handoff.default_pins()
    try:
        world.returned()
        path = world.binding()

        def hook(point):
            if point == "after-capture":
                script, _digest = pins["clerk"]
                pins["clerk"] = (script, "cd" * 32)
            return None

        code, text = perform(path, hook=hook, pins=pins)
        reason = assert_refused(code, text, "pin hash mismatch: clerk")
        if (world.record / "completed.json").exists():
            raise AssertionError("late pin change wrote completed.json")
        if not (world.record / "intent.json").exists():
            raise AssertionError("late pin change dropped the intent")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_compete() -> tuple[str, str]:
    world = World("compete")
    try:
        world.returned()
        path = world.binding()
        release = threading.Event()
        ready = threading.Event()
        winner = {}

        def hook(point):
            if point == "after-intent":
                ready.set()
                if not release.wait(60):
                    return "stop"
            return None

        def run_winner():
            code, text = handoff.execute(path, hook=hook)
            winner["code"] = code
            winner["text"] = text

        thread = threading.Thread(target=run_winner)
        thread.start()
        if not ready.wait(60):
            release.set()
            thread.join(30)
            raise AssertionError("winner did not reach after-intent")
        intent = (world.record / "intent.json").read_bytes()
        code, text = handoff.execute(path)
        reason = assert_refused(code, text, "intent is retained")
        if (world.record / "intent.json").read_bytes() != intent:
            raise AssertionError("loser overwrote intent.json")
        if (world.member_dir() / "return.md").exists():
            raise AssertionError("loser captured while the intent was unfinished")
        release.set()
        thread.join(120)
        if thread.is_alive():
            raise AssertionError("winner did not finish")
        if winner.get("code") != 0 or "result ok" not in winner.get("text", ""):
            raise AssertionError(winner.get("text", ""))
        if (world.record / "intent.json").read_bytes() != intent:
            raise AssertionError("winner rewrote intent.json")
        if not (world.record / "completed.json").exists():
            raise AssertionError("winner did not complete")
        if band_members(world.book) != [world.member]:
            raise AssertionError("compete allocated another member")
        return "expected-refusal", f": loser {reason}; winner result ok"
    finally:
        world.close()


def case_planted_intent() -> tuple[str, str]:
    world = World("planted")
    try:
        world.returned()
        world.record.mkdir()
        planted = world.record / "intent.json"
        planted.write_bytes(b"planted-intent\n")
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "intent is retained")
        if planted.read_bytes() != b"planted-intent\n":
            raise AssertionError("planted intent was overwritten")
        if (world.member_dir() / "return.md").exists() or (world.record / "completed.json").exists():
            raise AssertionError("planted intent captured")
        return "expected-refusal", f": {reason}"
    finally:
        world.close()


def case_git_store() -> tuple[str, str]:
    world = World("gitstore")
    store = ROOT / "labs" / "capture-handoff-pass01"
    before = sorted(os.listdir(store))
    calls = []
    real_launch = handoff.launch

    def wrapped(script, args, pins):
        calls.append(list(args))
        return real_launch(script, args, pins)

    try:
        world.store = store
        world.outbox = store / "jobs" / world.job_id / "outbox"
        world.do_reserve()
        handoff.launch = wrapped
        code, text = perform(world.binding())
        reason = assert_refused(code, text, "state is unknown")
        if len(calls) != 1 or calls[0][0] != "show" or calls[0][1] != "--store":
            raise AssertionError(f"git store calls {calls}")
        if os.path.normcase(calls[0][2]) != os.path.normcase(str(store)):
            raise AssertionError(f"git store path {calls[0]}")
        if (store / "jobs").exists() or sorted(os.listdir(store)) != before:
            raise AssertionError("git store test wrote into the checkout")
        if (world.record / "intent.json").exists():
            raise AssertionError("git store refusal created an intent")
        return "expected-refusal", f": {reason}"
    finally:
        handoff.launch = real_launch
        world.store = world.root / "store"
        world.close()


def raw_binding(world: World) -> dict:
    world.store.mkdir()
    world.do_reserve()
    world.event = "ab" * 32
    path = world.binding()
    return json.loads(Path(path).read_bytes().decode("utf-8"))


def case_malformed() -> tuple[str, str]:
    world = World("malformed")
    reasons = []
    try:
        base = raw_binding(world)

        def run_raw(raw: bytes) -> str:
            world.binding_path.write_bytes(raw)
            if world.failure_log.exists():
                world.failure_log.unlink()
            code, text = perform(str(world.binding_path))
            if code != 2 or "writes none" not in text or world.failure_log.exists():
                raise AssertionError(text)
            return assert_refused(code, text, "")

        text = canonical(base).decode("utf-8").rstrip("\n")
        raw = text[:-1] + ', "schema": "other"}\n'
        reasons.append(run_raw(raw.encode("utf-8")))
        if "repeats schema" not in reasons[-1]:
            raise AssertionError(reasons[-1])
        extra = dict(base)
        extra["hook"] = "stop"
        reasons.append(run_raw(canonical(extra)))
        if "unknown field hook" not in reasons[-1]:
            raise AssertionError(reasons[-1])
        missing = dict(base)
        del missing["instructions_base"]
        reasons.append(run_raw(canonical(missing)))
        if "misses instructions_base" not in reasons[-1]:
            raise AssertionError(reasons[-1])
        relative = dict(base)
        relative["clerk_store"] = "relative-store"
        reasons.append(run_raw(canonical(relative)))
        if "must be absolute" not in reasons[-1]:
            raise AssertionError(reasons[-1])
        mapped = json.loads(canonical(base).decode("utf-8"))
        mapped["report"]["source"] = "other-report.md"
        reasons.append(run_raw(canonical(mapped)))
        if "report source is not the clerk path" not in reasons[-1]:
            raise AssertionError(reasons[-1])
        flagged = json.loads(canonical(base).decode("utf-8"))
        flagged["report"]["bytes"] = True
        reasons.append(run_raw(canonical(flagged)))
        if "not an integer" not in reasons[-1]:
            raise AssertionError(reasons[-1])
        reasons.append(run_raw(canonical(base) + b"{}\n"))
        if "trailing data" not in reasons[-1]:
            raise AssertionError(reasons[-1])
        ambiguous = json.loads(canonical(base).decode("utf-8"))
        ambiguous["artifacts"][0]["logical"] = "other-name.md"
        reasons.append(run_raw(canonical(ambiguous)))
        if "ambiguous" not in reasons[-1]:
            raise AssertionError(reasons[-1])
        return "expected-refusal", ": " + "; ".join(reasons)
    finally:
        world.close()


def case_cli() -> tuple[str, str]:
    buf = io.StringIO()
    err = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(err):
        code = handoff.main(["perform", "--binding", r"D:\not-used.json", "--stop", "after-capture"])
    if code != 2 or "--stop" not in err.getvalue():
        raise AssertionError(f"cli exit {code} stdout {buf.getvalue()} stderr {err.getvalue()}")
    return "expected-refusal", ": cli rejects a fault switch"


def main() -> int:
    cases = [
        ("clean-and-identical-retry", case_clean),
        ("changed-event-and-work-ref", case_changed_event),
        ("unrelated-report", case_unrelated_report),
        ("dirty-artifacts", case_dirty),
        ("claimed-job", case_claimed),
        ("unusable-instructions", case_unusable),
        ("not-checked-instructions", case_not_checked),
        ("wrong-origin", case_wrong_origin),
        ("wrong-submission", case_wrong_submission),
        ("wrong-order", case_wrong_order),
        ("preexisting-complete", case_preexisting),
        ("partial-member", case_partial),
        ("hardlink", case_hardlink),
        ("junction", case_junction),
        ("file-symlink", case_symlink),
        ("bad-pins", case_bad_pins),
        ("stop-before-intent", lambda: case_stop("before-intent", "stop0")),
        ("stop-after-intent", lambda: case_stop("after-intent", "stop1")),
        ("stop-after-capture", lambda: case_stop("after-capture", "stop2")),
        ("stop-before-final-record", lambda: case_stop("before-final-record", "stop3")),
        ("source-changed-after-capture", case_source_changed),
        ("pin-changed-after-capture", case_pin_changed),
        ("competing-writers", case_compete),
        ("planted-intent", case_planted_intent),
        ("git-store", case_git_store),
        ("malformed-binding", case_malformed),
        ("cli-fault-switch", case_cli),
    ]
    for name, fn in cases:
        try:
            kind, detail = fn()
        except Exception as exc:
            COUNTS["fail"] += 1
            print(f"fail {name}: {type(exc).__name__}: {exc}")
            traceback.print_exc()
            print(
                f"summary pass {COUNTS['pass']} expected-refusal {COUNTS['expected-refusal']} "
                f"skip {COUNTS['skip']} fail {COUNTS['fail']}"
            )
            return 1
        COUNTS[kind] += 1
        print(f"{kind} {name}{detail}")
    print(
        f"summary pass {COUNTS['pass']} expected-refusal {COUNTS['expected-refusal']} "
        f"skip {COUNTS['skip']} fail 0"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
