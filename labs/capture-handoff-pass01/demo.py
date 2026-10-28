"""Show one fixture handoff and an identical retry. Custody is not acceptance.

The demo queues, claims, returns, and reserves only as fixture setup. The
adapter call does not. Temporary directories are outside the checkout and are
removed afterward.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "labs" / "capture-handoff-pass01"))
import handoff  # noqa: E402


REPORT = b"final report body\n"
PIECE = b"piece-body-0517\n"
EVIDENCE = "transport line only"
JOB_ID = "fixture-0517"
ASSIGNEE = "fixture-builder"


def outside_git(path: Path) -> None:
    current = path.resolve()
    while True:
        if (current / ".git").exists():
            raise SystemExit(f"demo directory is inside a Git working tree: {path}")
        if current.parent == current:
            return
        current = current.parent


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
        raise SystemExit(f"demo setup failed: {relative} {args[0]}\n{out}{err}")
    return out


def canonical(value) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (text + "\n").encode("utf-8")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def field(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    raise SystemExit(f"demo setup missed {prefix!r}\n{text}")


def main() -> int:
    parent = Path(tempfile.gettempdir())
    outside_git(parent)
    root = Path(tempfile.mkdtemp(prefix="handoff0517-demo-", dir=str(parent)))
    outside_git(root)
    try:
        instructions = root / "instructions"
        instructions.mkdir()
        (instructions / "task.txt").write_bytes(b"fixture task\n")
        task_sha = digest((instructions / "task.txt").read_bytes())
        store = root / "store"
        book = root / "book"
        book.mkdir()
        source = root / "source"
        source.mkdir()
        job = {
            "assignee": ASSIGNEE,
            "expected_outputs": ["final-report.md", "piece.txt"],
            "instructions": {"path": "task.txt", "sha256": task_sha},
            "job_id": JOB_ID,
            "release": "fixture job label; not a release",
            "reviewer": "fixture-reviewer",
            "routed_by": "fixture-router",
        }
        job_path = root / "job.json"
        job_path.write_bytes(canonical(job))
        run_tool(
            "labs/clerk-handoff-pass02/clerk.py",
            ["queue", "--store", str(store), "--job", str(job_path), "--instructions-base", str(instructions)],
        )
        claimed = run_tool(
            "labs/clerk-handoff-pass02/clerk.py",
            ["claim", "--store", str(store), "--job", JOB_ID, "--as", ASSIGNEE, "--instructions-base", str(instructions)],
        )
        token = field(claimed, "token ")
        outbox = store / "jobs" / JOB_ID / "outbox"
        (outbox / "final-report.md").write_bytes(REPORT)
        (outbox / "piece.txt").write_bytes(PIECE)
        (source / "final-report.md").write_bytes(REPORT)
        (source / "piece.txt").write_bytes(PIECE)
        returned = run_tool(
            "labs/clerk-handoff-pass02/clerk.py",
            [
                "return", "--store", str(store), "--job", JOB_ID, "--as", ASSIGNEE,
                "--claim", token, "--delivery", "fixture-delivery", "--evidence", EVIDENCE,
            ],
        )
        event = field(returned, "event 0003.returned.json sha256=")
        reserved = run_tool(
            "labs/return-capture-pass01/return_capture.py",
            [
                "reserve", "--book", str(book), "--submission", "fixture-demo",
                "--name", "demo", "--origin-book", "00.00.10.work",
                "--origin-page", "0504.app-entry", "--origin-batch", "05.17",
                "--expected-output", "final-report.md", "--expected-output", "piece.txt",
                "--submitter", "Fixture Submitter", "--reviewer", "Fixture Reviewer",
                "--release", "fixture reservation; not a release",
            ],
        )
        member = field(reserved, "member ")
        binding = {
            "schema": "clerk-capture-handoff/1",
            "clerk_store": str(store),
            "job_id": JOB_ID,
            "instructions_base": str(instructions),
            "returned_event_sha256": event,
            "assignee": ASSIGNEE,
            "work_ref": "demo-work-ref",
            "origin": {"batch": "05.17", "book": "00.00.10.work", "page": "0504.app-entry"},
            "book": str(book),
            "submission_id": "fixture-demo",
            "member": member,
            "source_root": str(source),
            "artifact_base": str(outbox),
            "report": {
                "clerk_path": "final-report.md",
                "source": "final-report.md",
                "sha256": digest(REPORT),
                "bytes": len(REPORT),
            },
            "artifacts": [
                {
                    "clerk_path": "final-report.md",
                    "source": "final-report.md",
                    "logical": "final-report.md",
                    "sha256": digest(REPORT),
                    "bytes": len(REPORT),
                },
                {
                    "clerk_path": "piece.txt",
                    "source": "piece.txt",
                    "logical": "piece.txt",
                    "sha256": digest(PIECE),
                    "bytes": len(PIECE),
                },
            ],
            "record": str(root / "handoff-record"),
            "failure_log": str(root / "failure.log"),
        }
        binding_path = root / "binding.json"
        binding_path.write_bytes(canonical(binding))
        print("demo first")
        first = handoff.perform(str(binding_path))
        if first != 0:
            return first
        returned_file = (book / member / "return.md").read_bytes()
        if returned_file != REPORT or EVIDENCE.encode("utf-8") in returned_file:
            print("demo report bytes are not the returned artifact")
            return 2
        print("demo retry")
        second = handoff.perform(str(binding_path))
        if second != 0:
            return second
        if (root / "failure.log").exists():
            print("demo failure log exists after custody")
            return 2
        print("demo failure-log absent")
        print("demo custody only; not review, acceptance, or closure")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
