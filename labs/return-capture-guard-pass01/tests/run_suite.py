#!/usr/bin/env python3
"""Disposable proof for the guarded legacy writer. Roots are kept."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LIVE = REPO / "00.kernel" / "00.00.10.work"
EVIDENCE = LIVE / "0521.return-placement" / "evidence" / "build05.08"
GUARD = REPO / "labs" / "return-capture-guard-pass01" / "return_capture_guard.py"
WRITER = REPO / "labs" / "return-capture-pass01" / "return_capture.py"
INSPECT = REPO / "labs" / "return-capture-pass01" / "return_inspect.py"
PASS04 = REPO / "labs" / "return-lines-pass04" / "return_lines.py"
ACCESS = REPO / "labs" / "return-access-pass01" / "return_access.py"
CLERK = REPO / "labs" / "clerk-handoff-pass02" / "clerk.py"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
sys.path.insert(0, str(REPO / "labs" / "return-capture-guard-pass01"))
import harness  # noqa: E402
import return_capture_guard as tool  # noqa: E402

LOG: list[dict] = []
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
ROOT = Path(r"D:\librarian\temp\0521-0508") / f"{STAMP}-suite"
RELEASE = "résumé — not a release"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(body: dict) -> bytes:
    return (json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def fail(message: str) -> None:
    (EVIDENCE / "first-failure.txt").write_bytes(f"{message}\n".encode("utf-8"))
    print("FAIL", message)
    raise SystemExit(1)


def run(script: Path, args: list[str]) -> tuple[int, str, bytes]:
    proc = subprocess.run(
        [str(PY), "-B", str(script), *args],
        cwd=str(REPO),
        env=ENV,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    text = proc.stdout.replace(b"\r\n", b"\n").decode("utf-8")
    LOG.append({
        "argv": [str(script), *args],
        "exit": proc.returncode,
        "stderr_bytes": len(proc.stderr),
        "stdout_sha256": sha(text.encode("utf-8")),
    })
    if proc.returncode not in {0, 1, 2}:
        fail(f"unexpected exit {proc.returncode} from {script.name} {args[:1]}")
    return proc.returncode, text, proc.stderr


def tree_rows(root: Path) -> list[str]:
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if not tool.is_reparse(os.path.join(dirpath, name))]
        for name in filenames:
            path = Path(dirpath) / name
            if tool.is_reparse(str(path)):
                continue
            data = path.read_bytes()
            rows.append(f"{path.relative_to(root).as_posix()} {len(data)} {sha(data)}")
    rows.sort()
    return rows


def tree_sha(root: Path) -> str:
    return sha(("\n".join(tree_rows(root)) + "\n").encode("utf-8"))


def layout_bytes(name: str) -> bytes:
    lines = tool.load_lines()
    return lines.dump(lines.layout_body(name))


def line_auth(book: Path) -> list[str]:
    """Parser labels for pass04. A doorless copy does not open or create them."""
    label = book.parent / "unused-auth-labels"
    names = (
        ("--authorization", "not-a-release.txt"),
        ("--audit", "not-an-audit.json"),
        ("--plan", "not-a-plan.json"),
        ("--backup", "not-a-backup"),
        ("--staging", "not-a-staging"),
        ("--retired", "not-a-retired"),
    )
    args: list[str] = []
    for flag, name in names:
        args.extend((flag, str(label / name)))
    return args


def reserve(script: Path, book: Path, submission: str, name: str) -> tuple[int, str]:
    code, text, err = run(script, [
        "reserve", "--book", str(book), "--submission", submission, "--name", name,
        "--origin-book", "00.00.10.work", "--origin-page", "0504.app-entry",
        "--origin-batch", "05.08", "--expected-output", "final-report.md",
        "--expected-output", "piece.txt", "--submitter", "Grok-2",
        "--reviewer", "Codex Prime", "--release", RELEASE,
    ])
    if err:
        fail(f"stderr on reserve {err[:200]!r}")
    return code, text


def field(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    fail(f"missing {prefix!r} in {text[:240]!r}")
    return ""


def main() -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    ROOT.mkdir(parents=True)
    if (LIVE / "return-line-layout.json").exists():
        fail("live layout already exists")
    print("work root", ROOT)

    unit = subprocess.run(
        [str(PY), "-B", str(REPO / "labs/return-capture-guard-pass01/tests/test_guard.py")],
        cwd=str(REPO), env=ENV, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
    )
    (EVIDENCE / "unit-stdout.txt").write_bytes(unit.stdout)
    (EVIDENCE / "unit-stderr.txt").write_bytes(unit.stderr)
    if unit.returncode != 0:
        fail(f"unit exit {unit.returncode}")

    legacy = ROOT / "legacy"
    book = legacy / "book"
    book.mkdir(parents=True)
    kept = "café — 保留\n".encode("utf-8")
    (book / "kept.txt").write_bytes(kept)
    code, text = reserve(GUARD, book, "legacy-0508", "legacy")
    if code != 0 or "result reserved" not in text.splitlines():
        fail(f"undeclared reserve {code} {text}")
    if "has not gained line-pass protection" not in text:
        fail("undeclared reserve omitted the protection sentence")
    member = field(text, "member ")
    reservation = (book / member / "reservation.json").read_bytes()
    if RELEASE.encode("utf-8") not in reservation:
        fail("reservation lost the non-ASCII release")
    code, again = reserve(GUARD, book, "legacy-0508", "legacy")
    if code != 0 or "result already-reserved" not in again.splitlines():
        fail(f"undeclared repeat {code} {again}")
    (book / "return-line-layout.json").write_bytes(layout_bytes("disposable-copy"))
    before = tree_sha(book)
    code, refused = reserve(GUARD, book, "legacy-0508", "legacy")
    if code != 2 or "result refused" not in refused.splitlines() or "already-reserved" in refused:
        fail(f"declared repeat {code} {refused}")
    if "writer_started: false" not in refused or tree_sha(book) != before:
        fail("declared repeat changed the book or started a success path")
    code, captured = run(GUARD, [
        "capture", "--book", str(book), "--submission", "legacy-0508",
        "--return-file", str(legacy / "missing-return.md"),
        "--source-root", str(legacy),
    ])[:2]
    if code != 2 or "result captured" in captured.splitlines() or tree_sha(book) != before:
        fail(f"declared capture of unfinished member {code} {captured}")
    if (book / member / "receipt.json").exists():
        fail("refused capture invented a receipt")

    done = ROOT / "completed"
    done_book = done / "book"
    source = done / "source"
    done_book.mkdir(parents=True)
    source.mkdir()
    report = "final café — report\n".encode("utf-8")
    piece = "piece-body-0508\n".encode("utf-8")
    (source / "final-report.md").write_bytes(report)
    (source / "piece.txt").write_bytes(piece)
    code, text = reserve(GUARD, done_book, "done-0508", "done")
    if code != 0:
        fail(f"completed-book reserve {code} {text}")
    done_member = field(text, "member ")
    code, text, err = run(GUARD, [
        "capture", "--book", str(done_book), "--submission", "done-0508",
        "--return-file", str(source / "final-report.md"), "--source-root", str(source),
        "--artifact", "final-report.md|final-report.md", "--artifact", "piece.txt|piece.txt",
    ])
    if err or code != 0 or "result captured" not in text.splitlines():
        fail(f"undeclared capture {code} {text} {err[:200]!r}")
    if "has not gained line-pass protection" not in text:
        fail("undeclared capture omitted the protection sentence")
    code, verified, err = run(GUARD, ["verify", "--book", str(done_book), "--member", done_member])
    if err or code != 0 or "result complete" not in verified.splitlines() or "not approved" not in verified.splitlines():
        fail(f"verify before declaration {code} {verified}")
    (done_book / "return-line-layout.json").write_bytes(layout_bytes("disposable-copy"))
    receipt = (done_book / done_member / "receipt.json").read_bytes()
    code, verified, err = run(GUARD, ["verify", "--book", str(done_book), "--member", done_member])
    if err or code != 0 or "result complete" not in verified.splitlines():
        fail(f"verify after declaration {code} {verified}")
    if (done_book / done_member / "receipt.json").read_bytes() != receipt:
        fail("verify rewrote the receipt")
    code, inspected, err = run(INSPECT, ["inspect", "--book", str(done_book), "--member", done_member, "--json"])
    if err or code != 0:
        fail(f"inspect {code} {inspected}")
    view = json.loads(inspected)
    if view.get("schema") != "return-capture-inspection/1" or view.get("status") != "complete":
        fail(f"inspect status {view.get('status')}")
    code, blocked, _err = run(GUARD, [
        "capture", "--book", str(done_book), "--submission", "done-0508",
        "--return-file", str(source / "final-report.md"), "--source-root", str(source),
        "--artifact", "final-report.md|final-report.md", "--artifact", "piece.txt|piece.txt",
    ])
    if code != 2 or (done_book / done_member / "receipt.json").read_bytes() != receipt:
        fail("capture after declaration changed the completed receipt")
    if "result captured" in blocked.splitlines():
        fail("declared capture reported success")

    bad = ROOT / "malformed" / "book"
    bad.mkdir(parents=True)
    (bad / "return-line-layout.json").write_bytes(b"{")
    code, text = reserve(GUARD, bad, "bad-0508", "bad")
    if code != 2 or "state: attention" not in text or (bad / "0100.band.returns").exists():
        fail(f"malformed layout allocated {code} {text}")
    clash = ROOT / "conflict" / "book"
    clash.mkdir(parents=True)
    body = json.loads(layout_bytes("disposable-copy").decode("utf-8"))
    (clash / "return-line-layout.json").write_bytes((json.dumps(body, separators=(",", ":")) + "\n").encode("utf-8"))
    code, text = reserve(GUARD, clash, "clash-0508", "clash")
    if code != 2 or "conflicts with the accepted line-pass declaration" not in text or (clash / "0100.band.returns").exists():
        fail(f"conflicting layout allocated {code} {text}")

    linked = ROOT / "linked" / "book"
    linked.mkdir(parents=True)
    source_layout = ROOT / "linked" / "source.json"
    source_layout.write_bytes(layout_bytes("disposable-copy"))
    os.link(source_layout, linked / "return-line-layout.json")
    code, text = reserve(GUARD, linked, "link-0508", "link")
    if code != 2 or "state: attention" not in text or (linked / "0100.band.returns").exists():
        fail(f"linked layout allocated {code} {text}")

    migrated = ROOT / "migrated" / "book"
    migrated.mkdir(parents=True)
    native = migrated / "0121.synthetic-filing"
    code, text, err = run(PASS04, ["init", "--book", str(migrated), "--name", "00.00.10.work", *line_auth(migrated)])
    if code != 0 or err:
        fail(f"pass04 init {code} {text} {err[:300]!r}")
    code, text, err = run(PASS04, [
        "reserve", "--book", str(migrated), "--page", "0521.synthetic-filing",
        "--batch", "05.01", "--submission", "line-0508", "--output", "note.md",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", "synthetic line filing",
        *line_auth(migrated),
    ])
    if code not in {0, 1} or err:
        fail(f"pass04 reserve {code} {text} {err[:300]!r}")
    note = migrated / "note.md"
    note.write_bytes("line filing\n".encode("utf-8"))
    code, text, err = run(PASS04, [
        "capture", "--book", str(migrated), "--page", "0521.synthetic-filing",
        "--batch", "05.01", "--submission", "line-0508", "--return-file", str(note),
        "--artifact", "note.md", str(note),
        *line_auth(migrated),
    ])
    if code != 0 or err:
        fail(f"pass04 capture {code} {text} {err[:400]!r}")
    if (migrated.parent / "unused-auth-labels").exists():
        fail("pass04 created an authorization path on the doorless copy")
    code, text, err = run(ACCESS, [
        "lookup", "--book", str(migrated), "--source", "0521.synthetic-filing", "--pass", "05.01",
    ])
    if code != 0 or err:
        fail(f"reader lookup {code} {text} {err[:300]!r}")
    looked = json.loads(text)
    if looked.get("state") != "complete":
        fail(f"reader state {looked.get('state')}")
    native_before = tree_sha(native)
    door_before = (migrated / "0100.band.returns").exists()
    code, text = reserve(GUARD, migrated, "legacy-on-line", "legacy-on-line")
    if code != 2 or "result refused" not in text.splitlines() or "line-pass route" not in text:
        fail(f"guard on migrated copy {code} {text}")
    if tree_sha(native) != native_before or (migrated / "0100.band.returns").exists() != door_before:
        fail("guard treated a native line path as a legacy write")

    historical = ROOT / "historical-declared" / "book"
    historical.mkdir(parents=True)
    (historical / "return-line-layout.json").write_bytes(layout_bytes("disposable-copy"))
    code, text, err = run(WRITER, [
        "reserve", "--book", str(historical), "--submission", "old-0508", "--name", "old",
        "--origin-book", "00.00.10.work", "--origin-page", "0504.app-entry",
        "--origin-batch", "05.08", "--submitter", "Grok-2", "--reviewer", "Codex Prime",
        "--release", "historical script",
    ])
    if err or code != 0 or "result reserved" not in text.splitlines():
        fail(f"historical writer on a declared copy {code} {text}")

    harness_book = handoff_case()
    report = {
        "accepted": False,
        "approved": False,
        "capture_slot": None,
        "committed": False,
        "custody": "pending",
        "guard_refused_declared_capture": True,
        "historical_writer_still_allocates": True,
        "live_layout_written": (LIVE / "return-line-layout.json").exists(),
        "published": False,
        "reader_state": looked.get("state"),
        "receipt": None,
        "schema": "return-capture-guard-suite/1",
        "seated": False,
        "sentinel_installed": False,
        "unit_exit": unit.returncode,
        "work_root": str(ROOT),
        "handoff_book": str(harness_book),
    }
    if report["live_layout_written"]:
        fail("live layout written")
    (ROOT / "suite-report.json").write_bytes(dump(report))
    (EVIDENCE / "suite-report.json").write_bytes(dump(report))
    (EVIDENCE / "commands.json").write_bytes(dump({"commands": LOG, "schema": "return-capture-guard-commands/1"}))
    (EVIDENCE / "first-failure.txt").write_bytes(b"No command failed in the official run.\n")
    print("OK", ROOT)


def handoff_case() -> Path:
    import io
    from contextlib import redirect_stdout

    base = ROOT / "handoff"
    instructions = base / "instructions"
    instructions.mkdir(parents=True)
    (instructions / "task.txt").write_bytes(b"fixture task\n")
    store = base / "store"
    book = base / "book"
    book.mkdir()
    source = base / "source"
    source.mkdir()
    report = "final café — report\n".encode("utf-8")
    piece = "piece-body-0508\n".encode("utf-8")
    (source / "final-report.md").write_bytes(report)
    (source / "piece.txt").write_bytes(piece)
    job = {
        "assignee": "fixture-builder",
        "expected_outputs": ["final-report.md", "piece.txt"],
        "instructions": {"path": "task.txt", "sha256": sha((instructions / "task.txt").read_bytes())},
        "job_id": "fixture-0508",
        "release": "fixture job label; not a release",
        "reviewer": "fixture-reviewer",
        "routed_by": "fixture-router",
    }
    job_path = base / "job.json"
    job_path.write_bytes(dump(job).replace(b"\n  ", b"").replace(b"\n", b"") if False else canonical(job))
    code, text, err = run(CLERK, ["queue", "--store", str(store), "--job", str(job_path), "--instructions-base", str(instructions)])
    if code != 0 or err:
        fail(f"clerk queue {code} {text} {err[:300]!r}")
    code, text, err = run(CLERK, [
        "claim", "--store", str(store), "--job", "fixture-0508", "--as", "fixture-builder",
        "--instructions-base", str(instructions),
    ])
    if code != 0 or err:
        fail(f"clerk claim {code} {text} {err[:300]!r}")
    token = field(text, "token ")
    outbox = store / "jobs" / "fixture-0508" / "outbox"
    (outbox / "final-report.md").write_bytes(report)
    (outbox / "piece.txt").write_bytes(piece)
    code, text, err = run(CLERK, [
        "return", "--store", str(store), "--job", "fixture-0508", "--as", "fixture-builder",
        "--claim", token, "--delivery", "fixture-delivery", "--evidence", "transport line only",
    ])
    if code != 0 or err:
        fail(f"clerk return {code} {text} {err[:300]!r}")
    event = field(text, "event 0003.returned.json sha256=")
    code, reserved = reserve(GUARD, book, "guard-0508", "guard-demo")
    if code != 0:
        fail(f"handoff reserve {code} {reserved}")
    member = field(reserved, "member ")
    (book / "return-line-layout.json").write_bytes(layout_bytes("disposable-copy"))
    before = tree_sha(book)
    binding = {
        "artifact_base": str(outbox),
        "artifacts": [
            {"bytes": len(report), "clerk_path": "final-report.md", "logical": "final-report.md", "sha256": sha(report), "source": "final-report.md"},
            {"bytes": len(piece), "clerk_path": "piece.txt", "logical": "piece.txt", "sha256": sha(piece), "source": "piece.txt"},
        ],
        "assignee": "fixture-builder",
        "book": str(book),
        "clerk_store": str(store),
        "failure_log": str(base / "failure.log"),
        "instructions_base": str(instructions),
        "job_id": "fixture-0508",
        "member": member,
        "origin": {"batch": "05.08", "book": "00.00.10.work", "page": "0504.app-entry"},
        "record": str(base / "handoff-record"),
        "report": {"bytes": len(report), "clerk_path": "final-report.md", "sha256": sha(report), "source": "final-report.md"},
        "returned_event_sha256": event,
        "schema": "clerk-capture-handoff/1",
        "source_root": str(source),
        "submission_id": "guard-0508",
        "work_ref": "guard-0508-work-ref",
    }
    binding_path = base / "binding.json"
    binding_path.write_bytes(canonical(binding))
    buf = io.StringIO()
    with redirect_stdout(buf):
        status = harness.perform(str(binding_path))
    first = buf.getvalue()
    (base / "perform-1.txt").write_bytes(first.encode("utf-8"))
    if status == 0 or "result ok" in first.splitlines():
        fail(f"handoff reported success\n{first}")
    if "result attention" not in first.splitlines() and "result refused" not in first.splitlines():
        fail(f"handoff did not block\n{first}")
    log_path = base / "failure.log"
    if not log_path.is_file():
        fail("failure log was not retained")
    log_bytes = log_path.read_bytes()
    payload = json.loads(log_bytes.decode("utf-8"))
    if payload.get("schema") != "clerk-capture-handoff-failure/1":
        fail("failure log schema")
    if tree_sha(book) != before or (book / member / "receipt.json").exists():
        fail("handoff capture changed the book")
    if report != (source / "final-report.md").read_bytes():
        fail("non-ASCII report bytes changed")
    buf = io.StringIO()
    with redirect_stdout(buf):
        status = harness.perform(str(binding_path))
    second = buf.getvalue()
    (base / "perform-2.txt").write_bytes(second.encode("utf-8"))
    if status == 0 or "result ok" in second.splitlines() or log_path.read_bytes() != log_bytes:
        fail("retry overwrote the failure log or succeeded")
    return book


def canonical(value: dict) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return (text + "\n").encode("utf-8")


if __name__ == "__main__":
    main()
