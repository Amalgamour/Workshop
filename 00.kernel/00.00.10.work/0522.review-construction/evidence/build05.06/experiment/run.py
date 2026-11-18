#!/usr/bin/env python3
"""One unchanged-cycle record/read with a review-construction/2 envelope.

Copies the historical disposable book
0707.app-use-check/evidence/build05.01/runs/run1/books/A.after-prepare
to a directory outside D:\\Git\\lib-build. Does not edit the cycle, the loop,
the door, the app, or that historical book. Saves outputs beside this file.
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

ROOT = Path(r"D:\Git\lib-build")
PY = Path(sys.executable)
CYCLE = ROOT / "labs" / "prime-cycle-pass03" / "prime_cycle.py"
CONSTRUCT = ROOT / "labs" / "review-construction-pass03" / "construct.py"
SOURCE = (
    ROOT
    / "00.kernel"
    / "00.00.10.work"
    / "0707.app-use-check"
    / "evidence"
    / "build05.01"
    / "runs"
    / "run1"
    / "books"
    / "A.after-prepare"
)
OUT = Path(__file__).resolve().parent


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(obj) -> bytes:
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def source_row(path: str, data: bytes, kind: str, identity: dict) -> dict:
    digest = sha(data)
    return {
        "bind": False,
        "content_bytes": len(data),
        "content_sha256": digest,
        "identity": identity,
        "kind": kind,
        "logical_path": path,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": data.decode("utf-8"),
        "transport_bytes": len(data),
        "transport_sha256": digest,
    }


def call(tool: Path, args: list[str]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [str(PY), "-B", str(tool), *args],
        cwd=str(ROOT),
        capture_output=True,
        env=env,
    )


def save(name: str, proc: subprocess.CompletedProcess) -> None:
    (OUT / f"{name}.stdout").write_bytes(proc.stdout.replace(b"\r\n", b"\n"))
    (OUT / f"{name}.stderr").write_bytes(proc.stderr.replace(b"\r\n", b"\n"))
    (OUT / f"{name}.exit").write_bytes(f"{proc.returncode}\n".encode("ascii"))


def main() -> int:
    book = Path(tempfile.mkdtemp(prefix="0522-0506-cycle-"))
    finding = None
    try:
        shutil.copytree(SOURCE, book, dirs_exist_ok=True)
        page_path = book / "0519.desk-app" / "05.01.md"
        page_before = page_path.read_bytes()
        (OUT / "page-before.md").write_bytes(page_before)
        reg = json.loads((book / "registration.json").read_text(encoding="utf-8"))
        descriptor = json.loads((book / "descriptor.json").read_text(encoding="utf-8"))
        read_before = call(CYCLE, ["read", "--fixture-root", str(book), "--registration", "registration.json"])
        save("read-before", read_before)
        if read_before.returncode != 0:
            finding = "cycle read refused before record"
            return 2
        view = json.loads(read_before.stdout.decode("utf-8"))
        template = view.get("template")
        if not isinstance(template, dict) or not isinstance(template.get("binding"), dict):
            finding = "cycle read returned no decision template"
            return 2
        task_before = view.get("task_binding_sha256")
        judgment = json.loads(json.dumps(template["judgment"]))
        sections = judgment["sections"]
        sections["return_result"] = "SYNTHETIC return result for the 05.06 envelope experiment."
        sections["prime_finding"] = "SYNTHETIC finding for the 05.06 envelope experiment."
        sections["within_direction"] = "SYNTHETIC direction for the 05.06 envelope experiment."
        sections["next_bounded_action"] = "SYNTHETIC next action for the 05.06 envelope experiment."
        next_text = "SYNTHETIC next action for the 05.06 envelope experiment. This is not a release."
        judgment.update({
            "outcome": "continue",
            "disposition": "held",
            "pass_terminal": "open",
            "finding": "SYNTHETIC finding for the 05.06 envelope experiment.",
            "reasons": ["The envelope experiment records a held judgment and does not render the page."],
            "source_refs": [reg["assignment_path"]],
            "next_action": {
                "action_id": "synth-0506",
                "text": next_text,
                "authorized_in_grant": False,
            },
            "unresolved": [],
            "semantic_conflict": False,
            "design_fork": None,
            "holds": [],
            "answers": [],
        })
        judgment["goal"]["terminal"] = "open"
        judgment["goal"]["evidence"] = []
        member = view["member"]
        assignment = (book / reg["assignment_path"]).read_bytes()
        note = (book / reg["evidence"][0]["logical_path"]).read_bytes()
        returned = (book / descriptor["return_path"]).read_bytes()
        receipt = (book / descriptor["receipt_path"]).read_bytes()
        sources = [
            source_row(reg["assignment_path"], assignment, "page", {"schema": "page-bytes/1"}),
            source_row(
                reg["evidence"][0]["logical_path"],
                note,
                "supplied-text",
                {"schema": "supplied-text/1", "label": "SUPPLIED"},
            ),
            source_row(
                descriptor["return_path"],
                returned,
                "capture",
                {
                    "schema": "return-capture/1",
                    "member": member,
                    "submission_id": reg["submission_id"],
                    "receipt_sha256": sha(receipt),
                    "origin": {
                        "book": descriptor["origin"]["book"],
                        "page": descriptor["origin"]["page"],
                        "batch": descriptor["origin"]["batch"],
                    },
                },
            ),
        ]
        supplied_record = {
            "schema": "prime-review-record/1",
            "attribution": {
                "actor_label": "Grok-2 synthetic envelope experiment",
                "role": "prime",
                "evidence": "SYNTHETIC judgment for 0522/05.06. The actor label is not authentication.",
            },
            "sources": sources,
            "agreement": reg["agreement"],
            "judgment": {
                "outcome": "continue",
                "finding": judgment["finding"],
                "reasons": list(judgment["reasons"]),
                "semantic_conflict": False,
                "design_fork": None,
                "next_action": next_text,
                "sections": sections,
            },
            "holds": [],
            "answers": [],
            "review_passes": [],
            "gaps": [],
        }
        decision = {
            "schema": "prime-cycle-decision/3",
            "review_id": template["review_id"],
            "supersedes": template["supersedes"],
            "recovers": template["recovers"],
            "binding": template["binding"],
            "attribution": supplied_record["attribution"],
            "judgment": judgment,
            "supplied_record": supplied_record,
        }
        envelope = {
            "schema": "review-construction/2",
            "source_kind": reg["source_kind"],
            "page": reg["kernel_page"],
            "pass": reg["pass"],
            "target": reg["target"],
            "expect_sha256": sha(page_before),
            "permit_create": False,
            "review_identity": reg["review_identity"],
            "task": {"task_id": reg["task_id"], "assignment_path": reg["assignment_path"]},
            "evidence": reg["evidence"],
            "agreement": reg["agreement"],
            "receipt": {
                "placement": "n5nn-matching-line",
                "member": member,
                "page_local": None,
                "submission_id": reg["submission_id"],
                "receipt_path": descriptor["receipt_path"],
                "return_path": descriptor["return_path"],
                "manifest_path": descriptor["manifest_path"],
                "status": "complete",
                "label": reg["receipt_label"],
            },
            "record": supplied_record,
            "supplied_review_state": {
                "schema": "supplied-review-state/1",
                "source": "cycle decision judgment",
                "disposition": judgment["disposition"],
                "pass_terminal": judgment["pass_terminal"],
                "goal_terminal": judgment["goal"]["terminal"],
                "outcome": judgment["outcome"],
            },
        }
        (book / "decision.json").write_bytes(dump(decision))
        (book / "envelope.json").write_bytes(dump(envelope))
        (OUT / "decision.json").write_bytes(dump(decision))
        (OUT / "envelope.json").write_bytes(dump(envelope))
        recorded = call(
            CYCLE,
            [
                "record",
                "--fixture-root",
                str(book),
                "--registration",
                "registration.json",
                "--decision",
                "decision.json",
                "--envelope",
                "envelope.json",
            ],
        )
        save("record", recorded)
        if recorded.returncode == 2:
            finding = "cycle record refused the review-construction/2 envelope"
            return 2
        read_after = call(CYCLE, ["read", "--fixture-root", str(book), "--registration", "registration.json"])
        save("read-after", read_after)
        if read_after.returncode != 0:
            finding = "cycle read refused after record"
            return 2
        after = json.loads(read_after.stdout.decode("utf-8"))
        bound = call(CONSTRUCT, ["bind", "--fixture-root", str(book), "--input", "envelope.json"])
        save("bind", bound)
        page_after = page_path.read_bytes()
        (OUT / "page-after.md").write_bytes(page_after)
        candidate = None
        if bound.returncode == 0:
            candidate = json.loads(bound.stdout.decode("utf-8")).get("binding_sha256")
        latest = after.get("latest_review") or {}
        recorded_binding = latest.get("task_binding_sha256")
        equal = candidate is not None and candidate == task_before == recorded_binding
        if not equal:
            finding = "task binding from pass02 bind and pass03 bind differ, or record did not keep the read binding"
        summary = {
            "schema": "constructor-pass03-cycle-experiment/1",
            "source_book": "00.kernel/00.00.10.work/0707.app-use-check/evidence/build05.01/runs/run1/books/A.after-prepare",
            "read_before_exit": read_before.returncode,
            "record_exit": recorded.returncode,
            "read_after_exit": read_after.returncode,
            "bind_exit": bound.returncode,
            "task_binding_sha256_read_before": task_before,
            "task_binding_sha256_recorded": recorded_binding,
            "candidate_binding_sha256": candidate,
            "bindings_equal": equal,
            "page_before_sha256": sha(page_before),
            "page_after_sha256": sha(page_after),
            "page_bytes_unchanged": page_before == page_after,
            "finding": finding,
            "cycle_patched": False,
        }
        (OUT / "summary.json").write_bytes(dump(summary))
        print(json.dumps({k: summary[k] for k in ("record_exit", "bindings_equal", "finding", "page_bytes_unchanged")}))
        return 0 if equal and finding is None else 2
    finally:
        if finding and not (OUT / "summary.json").exists():
            (OUT / "summary.json").write_bytes(dump({
                "schema": "constructor-pass03-cycle-experiment/1",
                "finding": finding,
                "cycle_patched": False,
            }))
            print(finding)
        shutil.rmtree(book, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
