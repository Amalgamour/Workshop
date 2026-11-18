"""Reproduce G01 and G02 against frozen pass03. Disposable fixtures only."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
PASS03 = ROOT / "labs" / "review-construction-pass03" / "construct.py"
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
OUT = Path(__file__).resolve().parent
BINDING = "ab" * 32
RECORD = "cd" * 32


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load():
    spec = importlib.util.spec_from_file_location("construct_pass03_reproduce", PASS03)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rendered(module):
    spec = {
        "review_identity": "r1",
        "envelope_schema": "review-construction/1",
        "supplied_review_state": None,
        "agreement": {
            "goal": "Review the synthetic copy.",
            "scope": "The synthetic copy only.",
            "prime_discretion": "Prime may replace this text.",
            "director_required": "A live review is not in this fixture.",
            "finish_criteria": None,
            "recorded_decisions": None,
        },
        "record": {"judgment": {"design_fork": None}},
    }
    measured = {
        "binding_sha256": BINDING,
        "agreement_sha256": RECORD,
        "binding": {
            "receipt": {
                "placement": "n5nn-matching-line",
                "member": "0199.synth-lab",
                "page_local": None,
                "status": "complete",
                "label": "synthetic",
                "receipt_sha256": "11" * 32,
                "return_sha256": "22" * 32,
                "manifest_sha256": "33" * 32,
            }
        },
    }
    report = {
        "supplied_outcome": "continue",
        "effective": "attention",
        "finding": "sample finding",
        "supplied_semantic_conflict": False,
        "reasons": ["one reason"],
        "answers": [],
        "next_action": "look again",
        "sections": {"findings_account": None, "tests_passed": None, "tests_note": None},
        "markdown": "# Report\nbody\n",
    }
    return module.render_review(spec, measured, report, RECORD)


def page(sep: bytes, body: bytes) -> bytes:
    prefix = b"# Page" + sep + sep + b"## Review - Codex Prime" + sep
    suffix = b"## Later" + sep + b"outside" + sep
    return prefix + body + suffix


RAW_FIXTURES = {
    "g01-section-lf.txt",
    "g01-section-crlf.txt",
    "g01-page-lf.md",
    "g01-page-crlf.md",
}


def store(name: str, data: bytes) -> None:
    if name not in RAW_FIXTURES:
        data = data.replace(b"\r\n", b"\n")
        if b"\r" in data:
            raise SystemExit(f"bare cr in {name}")
    (OUT / name).write_bytes(data)


def run_cli(root: Path, args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(PY), "-B", str(PASS03), *args],
        cwd=ROOT,
        capture_output=True,
    )


def main() -> int:
    before = PASS03.read_bytes()
    module = load()
    text = rendered(module)
    if "\r" in text or f"task_binding: {BINDING}\n" not in text:
        raise SystemExit("renderer did not emit the LF binding line")
    body_lf = module.encode_body(text, b"\n")
    body_crlf = module.encode_body(text, b"\r\n")
    lf = page(b"\n", body_lf)
    crlf = page(b"\r\n", body_crlf)
    store("g01-section-lf.txt", body_lf)
    store("g01-section-crlf.txt", body_crlf)
    store("g01-page-lf.md", lf)
    store("g01-page-crlf.md", crlf)

    findings = []
    with tempfile.TemporaryDirectory(prefix="0522-0507-g01-") as tmp:
        root = Path(tmp)
        (root / "lf.md").write_bytes(lf)
        (root / "crlf.md").write_bytes(crlf)
        rows = {}
        for name in ("lf.md", "crlf.md"):
            target = root / name
            digest_before = digest(target.read_bytes())
            proc = run_cli(
                root,
                ["inspect", "--fixture-root", str(root), "--target", name, "--binding", BINDING],
            )
            digest_after = digest(target.read_bytes())
            store(f"g01-{name}.stdout", proc.stdout)
            store(f"g01-{name}.stderr", proc.stderr)
            (OUT / f"g01-{name}.exit").write_bytes(f"{proc.returncode}\n".encode("ascii"))
            shown = run_cli(root, ["show", "--fixture-root", str(root), "--target", name])
            store(f"g01-show-{name}.stdout", shown.stdout)
            store(f"g01-show-{name}.stderr", shown.stderr)
            (OUT / f"g01-show-{name}.exit").write_bytes(f"{shown.returncode}\n".encode("ascii"))
            payload = json.loads(proc.stdout.decode("utf-8")) if proc.returncode == 0 else None
            rows[name] = {
                "exit": proc.returncode,
                "state": None if payload is None else payload.get("state"),
                "binding_sha256": None if payload is None else payload.get("binding_sha256"),
                "page_unchanged": digest_before == digest_after,
                "show_exit": shown.returncode,
            }
        if rows["lf.md"]["state"] != "constructed-same-binding" or rows["lf.md"]["binding_sha256"] != BINDING:
            findings.append("G01 LF did not classify constructed-same-binding")
        if rows["crlf.md"]["state"] != "existing-review" or rows["crlf.md"]["binding_sha256"] is not None:
            findings.append("G01 CRLF did not classify existing-review with a null binding")
        if not rows["lf.md"]["page_unchanged"] or not rows["crlf.md"]["page_unchanged"]:
            findings.append("G01 inspect wrote the target")
        g01 = rows

    envelope = {key: None for key in module.ENVELOPE_KEYS}
    envelope["schema"] = "review-construction/2"
    envelope["supplied_review_state"] = {
        "schema": "supplied-review-state/1",
        "source": "cycle decision judgment",
        "disposition": [],
        "pass_terminal": "open",
        "goal_terminal": "open",
        "outcome": "continue",
    }
    raw_envelope = (json.dumps(envelope, indent=2) + "\n").encode("utf-8")
    store("g02-envelope.json", raw_envelope)
    target_bytes = b"# Page\n\n## Review - Codex Prime\nPENDING.\n"
    with tempfile.TemporaryDirectory(prefix="0522-0507-g02-") as tmp:
        root = Path(tmp)
        (root / "envelope.json").write_bytes(raw_envelope)
        (root / "page.md").write_bytes(target_bytes)
        before_tree = sorted(path.name for path in root.iterdir())
        proc = run_cli(root, ["preview", "--fixture-root", str(root), "--input", "envelope.json"])
        after_tree = sorted(path.name for path in root.iterdir())
        after_target = (root / "page.md").read_bytes()
        store("g02.stdout", proc.stdout)
        store("g02.stderr", proc.stderr)
        (OUT / "g02.exit").write_bytes(f"{proc.returncode}\n".encode("ascii"))
        stderr = proc.stderr.decode("utf-8", errors="replace")
        g02 = {
            "exit": proc.returncode,
            "traceback": "Traceback (most recent call last):" in stderr and "TypeError:" in stderr,
            "target_unchanged": after_target == target_bytes,
            "tree_before": before_tree,
            "tree_after": after_tree,
        }
        if proc.returncode != 1 or not g02["traceback"] or not g02["target_unchanged"] or before_tree != after_tree:
            findings.append("G02 did not exit 1 with TypeError and an unchanged fixture")

    after = PASS03.read_bytes()
    summary = {
        "schema": "constructor-pass04-reproduction/1",
        "pass03_sha256": digest(before),
        "pass03_bytes": len(before),
        "pass03_unchanged": before == after,
        "binding": BINDING,
        "g01": g01,
        "g02": g02,
        "findings": findings,
        "stored_newlines": "lf",
        "runner_newlines": "crlf-normalized-to-lf",
        "fixture_bytes": "raw",
    }
    store("summary.json", (json.dumps(summary, indent=2) + "\n").encode("utf-8"))
    print(json.dumps({"findings": findings, "g01": g01, "g02_exit": g02["exit"], "g02_traceback": g02["traceback"]}))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
