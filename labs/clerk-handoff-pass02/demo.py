"""Seven-step file-backed handoff demonstration.

Each Clerk command is a separate process. The builder step writes count.py
with a script. It does not call a model. The store stays under --out.
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


CLERK = Path(__file__).resolve().with_name("clerk.py")
INSTRUCTION = b"Count lines containing at least one non-whitespace character.\n"
COUNT = (
    b"def count_lines(text):\n"
    b"    return sum(1 for line in text.splitlines() if line.strip())\n"
)


def refuse(message: str) -> None:
    print("demo refused: " + message)
    raise SystemExit(2)


def outside_git(path: Path) -> None:
    current = path
    while True:
        if os.path.lexists(current / ".git"):
            refuse("output path resolves inside a Git working tree")
        if current.parent == current:
            return
        current = current.parent


def run(args, steps, expect):
    proc = subprocess.run(
        [sys.executable, "-B", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    steps.append({
        "argv": [sys.executable, "-B", *args],
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    })
    if proc.returncode != expect:
        refuse(
            "step failed\n"
            + " ".join(args)
            + f"\nexit {proc.returncode}\n"
            + proc.stdout
            + proc.stderr
        )
    return proc


def sections(text: str):
    out = {"queued": [], "claimed": [], "returned": [], "incomplete": []}
    current = None
    for line in text.splitlines():
        if line.startswith("section "):
            current = line.split(" ", 1)[1]
            continue
        if line.startswith("result ") or current is None or line == "none":
            if line.startswith("result "):
                current = None
            continue
        out[current].append(line)
    return out


def require(condition, message, steps):
    if condition:
        return
    steps.append({"assertion": message})
    refuse(message)


def file_hashes(root: Path):
    rows = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(dirpath) / name
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            rows.append(f"{digest}  {path.relative_to(root).as_posix()}")
    return "\n".join(rows) + ("\n" if rows else "")


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[0] != "--out":
        refuse("usage: python -B demo.py --out <new absolute directory>")
    out = Path(argv[1])
    if not out.is_absolute():
        refuse("demo output path must be absolute")
    if out.exists():
        refuse("demo output path already exists")
    outside_git(out)
    out.mkdir()
    outside_git(out.resolve())
    steps = []
    try:
        router = (
            "import hashlib, json, pathlib, sys\n"
            "base, job_path = sys.argv[1:]\n"
            "text = " + repr(INSTRUCTION) + "\n"
            "path = pathlib.Path(base) / 'task.txt'\n"
            "path.parent.mkdir(parents=True)\n"
            "path.write_bytes(text)\n"
            "digest = hashlib.sha256(text).hexdigest()\n"
            "job = {\n"
            "  'assignee': 'builder-b',\n"
            "  'expected_outputs': ['count.py'],\n"
            "  'instructions': {'path': 'task.txt', 'sha256': digest},\n"
            "  'job_id': 'demo-0001',\n"
            "  'release': 'fixture release',\n"
            "  'reviewer': 'codex-prime',\n"
            "  'routed_by': 'router-fixture',\n"
            "}\n"
            "pathlib.Path(job_path).write_text(json.dumps(job), encoding='utf-8')\n"
            "print(digest)\n"
        )
        base = out / "base"
        job_path = out / "job.json"
        store = out / "store"
        routed = run(["-c", router, str(base), str(job_path)], steps, 0)
        digest = routed.stdout.strip()
        require(len(digest) == 64, "router did not print a sha256", steps)

        queued = run([
            str(CLERK), "queue", "--store", str(store), "--job", str(job_path),
            "--instructions-base", str(base),
        ], steps, 0)
        require("queued demo-0001" in queued.stdout, "queue did not record demo-0001", steps)

        builder_inbox = run([
            str(CLERK), "inbox", "--store", str(store), "--as", "builder-b",
            "--instructions-base", str(base),
        ], steps, 0)
        reviewer_inbox = run([
            str(CLERK), "inbox", "--store", str(store), "--as", "codex-prime",
            "--instructions-base", str(base),
        ], steps, 0)
        require(
            any(line.startswith("demo-0001") for line in sections(builder_inbox.stdout)["queued"]),
            "assignee inbox did not list the queued job",
            steps,
        )
        require("demo-0001" not in reviewer_inbox.stdout, "reviewer saw the job before return", steps)

        claimed = run([
            str(CLERK), "claim", "--store", str(store), "--job", "demo-0001",
            "--as", "builder-b", "--instructions-base", str(base),
        ], steps, 0)
        token = ""
        for line in claimed.stdout.splitlines():
            if line.startswith("token "):
                token = line.split(" ", 1)[1]
        require(len(token) == 32, "claim did not print a token", steps)
        second = run([
            str(CLERK), "claim", "--store", str(store), "--job", "demo-0001",
            "--as", "builder-b", "--instructions-base", str(base),
        ], steps, 2)
        require("already claimed" in second.stdout, "second claim was not refused", steps)
        stranger = run([
            str(CLERK), "claim", "--store", str(store), "--job", "demo-0001",
            "--as", "colab", "--instructions-base", str(base),
        ], steps, 2)
        require("not assignee" in stranger.stdout, "non-assignee claim was not refused", steps)

        writer = (
            "import pathlib, sys\n"
            "pathlib.Path(sys.argv[1]).write_bytes(" + repr(COUNT) + ")\n"
        )
        count_path = store / "jobs" / "demo-0001" / "outbox" / "count.py"
        run(["-c", writer, str(count_path)], steps, 0)
        count_sha = hashlib.sha256(count_path.read_bytes()).hexdigest()
        returned = run([
            str(CLERK), "return", "--store", str(store), "--job", "demo-0001",
            "--as", "builder-b", "--claim", token, "--delivery", "d-1",
            "--evidence", "scripted fixture wrote count.py",
        ], steps, 0)
        require("returned demo-0001" in returned.stdout, "return did not record the job", steps)
        require(count_sha in returned.stdout, "return did not record count.py's sha256", steps)

        reviewer = run([
            str(CLERK), "inbox", "--store", str(store), "--as", "codex-prime",
            "--instructions-base", str(base),
        ], steps, 0)
        builder_after = run([
            str(CLERK), "inbox", "--store", str(store), "--as", "builder-b",
            "--instructions-base", str(base),
        ], steps, 0)
        colab = run([
            str(CLERK), "inbox", "--store", str(store), "--as", "colab",
            "--instructions-base", str(base),
        ], steps, 0)
        require(
            any("demo-0001" in line and count_sha in line for line in sections(reviewer.stdout)["returned"]),
            "reviewer inbox did not list the returned artifact",
            steps,
        )
        require(sections(builder_after.stdout)["returned"] == [], "builder was offered the review", steps)
        require("demo-0001" not in colab.stdout, "colab was offered the review", steps)

        checked = run([
            str(CLERK), "verify", "--store", str(store), "--instructions-base", str(base),
        ], steps, 0)
        require("chain ok" in checked.stdout, "verify did not report the chain", steps)
        require(
            "states queued claimed returned" in checked.stdout,
            "verify did not report queued, claimed, and returned",
            steps,
        )

        tamper = "import pathlib, sys\npath = pathlib.Path(sys.argv[1])\npath.write_bytes(path.read_bytes() + b'# tampered\\n')\n"
        run(["-c", tamper, str(count_path)], steps, 0)
        shown = run([
            str(CLERK), "show", "--store", str(store), "--job", "demo-0001",
            "--instructions-base", str(base),
        ], steps, 1)
        require("artifact changed" in shown.stdout, "show did not report artifact changed", steps)
        require("not-returned-clean" in shown.stdout, "show presented a clean return", steps)
        tainted = run([
            str(CLERK), "inbox", "--store", str(store), "--as", "codex-prime",
        ], steps, 1)
        require("artifact changed" in tainted.stdout, "reviewer inbox did not report artifact changed", steps)
        findings = run([str(CLERK), "verify", "--store", str(store)], steps, 1)
        require("artifact changed" in findings.stdout, "verify did not report artifact changed", steps)
    except SystemExit:
        (out / "transcript.json").write_text(json.dumps(steps, indent=2) + "\n", encoding="utf-8")
        (out / "listing.txt").write_text(file_hashes(out), encoding="utf-8")
        raise
    (out / "transcript.json").write_text(json.dumps(steps, indent=2) + "\n", encoding="utf-8")
    (out / "listing.txt").write_text(file_hashes(out), encoding="utf-8")
    print("demo ok")
    print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
