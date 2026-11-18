"""Reproducible disposable demo. Writes a transcript and does not touch the live book.

    python3.11 -B -m app.desk_core.demo --transcript /absolute/transcript.txt
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from .bookio import repo_root


def _run(args: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, "-B", "-m", "app.desk_core", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout, proc.stderr


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="app.desk_core.demo")
    parser.add_argument("--transcript", required=True)
    args = parser.parse_args(argv)
    repo = repo_root()
    transcript = Path(args.transcript)
    if not transcript.is_absolute():
        raise SystemExit("transcript path must be absolute")
    lines: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "book"
        spec = {
            "page": "0523",
            "subject": "demo",
            "pass": "01",
            "title": "Synthetic demo task",
            "body": "Demonstrate the disposable N5NN loop.\n",
            "expected_outputs": ["return text"],
            "scope": {"in": ["disposable book"], "out": ["live work book"]},
            "agreement": "Synthetic demo agreement.\n",
            "bound_evidence": [
                {
                    "name": "pack",
                    "sha256": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                    "bytes": 4,
                }
            ],
            "synthetic": True,
        }
        (root / "task.json").write_text(json.dumps(spec), encoding="utf-8")
        steps = [
            ["pins"],
            ["init", "--book", str(book), "--label", "synthetic-demo"],
            ["record-task", "--book", str(book), "--input", str(root / "task.json")],
        ]
        binding = None
        for step in steps:
            code, out, err = _run(step, repo)
            lines.append(f"$ {' '.join(step)}\nexit {code}\n{out}{err}")
            if step[0] == "record-task":
                binding = json.loads(out)["task_binding_sha256"]
        register = {
            "page": "0523",
            "subject": "demo",
            "pass": "01",
            "synthetic": True,
            "release": {"who": "Director", "date": "2026-10-31", "text": "Synthetic demo release.\n"},
            "claim": {"worker": "synthetic-worker", "date": "2026-10-31", "text": "Synthetic demo claim.\n"},
        }
        (root / "register.json").write_text(json.dumps(register), encoding="utf-8")
        ret = {
            "page": "0523",
            "subject": "demo",
            "pass": "01",
            "worker": "synthetic-worker",
            "return_text": "Synthetic demo return.\n",
            "unresolved_questions": ["demo question"],
            "artifacts": [{"logical": "notes.md", "text": "demo notes\n"}],
            "synthetic": True,
            "task_binding_sha256": binding,
        }
        (root / "return.json").write_text(json.dumps(ret), encoding="utf-8")
        judgment = {
            "page": "0523",
            "subject": "demo",
            "pass": "01",
            "reviewer": "Codex Prime",
            "review_identity": "synthetic-demo-review",
            "disposition": "demo only; not acceptance",
            "findings": [],
            "dissent": "",
            "director_text": "Demo director text.\n",
            "unresolved_questions": ["demo question"],
            "assessment": "Demo assessment kept in full.\n",
            "next_action": {"actor": "director", "action": "Read the branch.\n"},
            "synthetic": True,
        }
        (root / "review.json").write_text(json.dumps(judgment), encoding="utf-8")
        more = [
            ["register", "--book", str(book), "--input", str(root / "register.json")],
            ["show", "--book", str(book), "--page", "0523", "--subject", "demo", "--pass", "01"],
            ["assert-done", "--book", str(book), "--page", "0523", "--subject", "demo", "--pass", "01", "--worker", "synthetic-worker"],
            ["show", "--book", str(book), "--page", "0523", "--subject", "demo", "--pass", "01"],
            ["submit-return", "--book", str(book), "--input", str(root / "return.json"), "--interrupt"],
            ["show", "--book", str(book), "--page", "0523", "--subject", "demo", "--pass", "01"],
            ["submit-return", "--book", str(book), "--input", str(root / "return.json")],
            ["submit-return", "--book", str(book), "--input", str(root / "return.json")],
            ["retrieve", "--book", str(book), "--page", "0523", "--subject", "demo", "--pass", "01"],
            ["review", "--book", str(book), "--input", str(root / "review.json")],
            ["recover", "--book", str(book), "--page", "0523", "--subject", "demo", "--pass", "01"],
            ["pending", "--book", str(book)],
        ]
        exits = []
        for step in more:
            code, out, err = _run(step, repo)
            exits.append(code)
            lines.append(f"$ {' '.join(step)}\nexit {code}\n{out}{err}")
        lines.append(
            "expected exits: register 0, show 0, assert-done 0, show 0, interrupt 3, "
            "partial show 0, submit 0, idempotent submit 0, retrieve 0, review 0, recover 0, pending 0\n"
            f"actual exits: {exits}\n"
        )
        if exits != [0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0]:
            transcript.write_text("".join(lines), encoding="utf-8")
            return 1
    transcript.parent.mkdir(parents=True, exist_ok=True)
    transcript.write_text("".join(lines), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
