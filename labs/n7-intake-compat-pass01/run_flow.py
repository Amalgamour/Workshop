#!/usr/bin/env python3
"""Recorded baseline / repaired runs on the disposable fixtures (0707/05.16 lab).

Each step is a NEW process; argv, exit, stdout and stderr are kept. Production files are hashed
(all 50 pack05.16 inputs) before and after. The live book is never passed as --book.
usage: run_flow.py --fixtures DIR --evidence NEW-DIR
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
LAB = LIVE / "labs/n7-intake-compat-pass01"
PACK16 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.16/source-manifest.json"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
SRC, PASS = "0707.app-use-check", "05.15"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prod_hashes() -> dict:
    m = json.loads(PACK16.read_text(encoding="utf-8"))
    return {f["path"]: sha((LIVE / f["path"]).read_bytes()) == f["sha256"] for f in m["files"]}


def summary(body: dict | None) -> dict:
    if not isinstance(body, dict):
        return {}
    rows = body.get("rows") or (body.get("intake") or {}).get("rows") or []
    out = {k: body.get(k) for k in ("command", "exit", "measurement", "custody", "stale", "state", "review_id", "intake_id", "live_intake_id",
                                     "publication_complete", "judgment_recorded", "destination", "next_action", "unknowns")}
    out["finding_codes"] = sorted({f.get("code") for f in body.get("findings") or [] if isinstance(f, dict)})
    out["roles"] = {}
    for r in rows:
        out["roles"][r.get("role")] = out["roles"].get(r.get("role"), 0) + 1
    out["submission_row"] = next(({k: r.get(k) for k in ("path", "root", "declared_sha256", "sha256", "bytes")} for r in rows if r.get("role") == "submission"), None)
    out["manifest_row"] = next(({k: r.get(k) for k in ("path", "root", "declared_sha256", "sha256")} for r in rows if r.get("role") == "artifact-manifest"), None)
    return {k: v for k, v in out.items() if v not in (None, {}, [])} | {"finding_codes": out["finding_codes"]}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fixtures", required=True)
    ap.add_argument("--evidence", required=True)
    a = ap.parse_args()
    fx, ev = Path(a.fixtures), Path(a.evidence)
    ev.mkdir(parents=True, exist_ok=False)
    before = prod_hashes()
    steps = []

    def step(name, argv):
        p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, timeout=600, env=ENV, cwd=str(LIVE))
        (ev / f"{name}.stdout").write_bytes(p.stdout)
        (ev / f"{name}.stderr").write_bytes(p.stderr)
        try:
            body = json.loads(p.stdout.decode("utf-8"))
        except Exception:
            body = None
        steps.append({"step": name, "argv": [str(x) for x in argv], "exit": p.returncode, "summary": summary(body),
                      "stderr_tail": p.stderr.decode("utf-8", "replace")[-300:]})
        print(f"{name:28} exit {p.returncode}  {json.dumps(summary(body), ensure_ascii=False)[:260]}")
        return p.returncode, body

    faithful = fx / "faithful/repo"
    norev = fx / "noreview/repo"
    fb = faithful / "00.kernel/00.00.10.work"
    nb = norev / "00.kernel/00.00.10.work"
    app = LIVE / "app/librarian.py"
    n7 = LAB / "n7compat.py"
    # Baseline A: the actual selected app entry, code root = live checkout (read only), book = disposable copy
    step("A-app-prepare", [app, "review-loop", "prepare", "--book", fb, "--source", SRC, "--pass", PASS])
    # Baseline B: unchanged pass03 with the faithful production layout (code root = the copy)
    step("B-faithful-prepare", [n7, "--repo-root", faithful, "prepare", "--book", fb, "--source", SRC, "--pass", PASS])
    # Repaired R: the lab parser in all three namespaces, same faithful layout
    rc, prep = step("R-faithful-prepare", [n7, "--patch", "--repo-root", faithful, "prepare", "--book", fb, "--source", SRC, "--pass", PASS])
    step("R-faithful-form", [n7, "--patch", "--repo-root", faithful, "form", "--book", fb, "--source", SRC, "--pass", PASS])
    judgment = {
        "finding": "LAB-ONLY SYNTHETIC judgment for the 0707/05.16 intake lab; not a real review of 0707/05.15.",
        "reasons": ["LAB-ONLY: exercises record, inspect, publish, read and recover on a disposable copy."],
        "operation": "continue", "disposition": "held", "pass_terminal": "open", "goal_terminal": "open",
        "next_action": "LAB-ONLY: no real action; Prime reviews the intake repair proposal.",
        "semantic_conflict": None, "design_fork": None, "findings": [], "holds": [], "answers": [], "review_passes": [], "gaps": ["LAB-ONLY: synthetic judgment"],
        "sections": {k: None for k in ("affected", "assumptions", "consequences", "exploration", "finish_assessments", "for_model", "issue", "learning", "limits",
                                       "open_questions", "options", "outcome_evidence", "preservation", "proposed_plan", "question", "recommendation",
                                       "remaining_choices", "within_direction")}
        | {"findings_account": [], "next_bounded_action": "LAB-ONLY: none.", "prime_finding": "LAB-ONLY synthetic.", "return_result": "LAB-ONLY synthetic.",
           "tests_note": "LAB-ONLY: no tests judged.", "tests_passed": None},
    }
    for label, root, book in (("faithful", faithful, fb), ("noreview", norev, nb)):
        jf = ev / f"judgment-{label}.json"
        jf.write_text(json.dumps(judgment, indent=1) + "\n", encoding="utf-8")
        rc, p = step(f"R-{label}-prepare2", [n7, "--patch", "--repo-root", root, "prepare", "--book", book, "--source", SRC, "--pass", PASS])
        iid = (p or {}).get("intake_id") or (p or {}).get("live_intake_id")
        rc, rec = step(f"R-{label}-record", [n7, "--patch", "--repo-root", root, "record", "--book", book, "--source", SRC, "--pass", PASS, "--intake", iid, "--judgment", jf])
        rc, ins = step(f"R-{label}-inspect", [n7, "--patch", "--repo-root", root, "inspect", "--book", book, "--source", SRC, "--pass", PASS])
        rid = (rec or {}).get("review_id") or (ins or {}).get("review_id")
        rendered = json.dumps(ins or {}, ensure_ascii=False)
        (ev / f"R-{label}-inspect.full-read.txt").write_text(rendered, encoding="utf-8")   # the full text kept for the human/model read
        step(f"R-{label}-publish", [n7, "--patch", "--repo-root", root, "publish", "--book", book, "--source", SRC, "--pass", PASS, "--review", rid or "none"])
        step(f"R-{label}-read", [n7, "--patch", "--repo-root", root, "read", "--book", book, "--source", SRC, "--pass", PASS])
        step(f"R-{label}-recover", [n7, "--patch", "--repo-root", root, "recover", "--book", book, "--source", SRC, "--pass", PASS])
    after = prod_hashes()
    body = {"schema": "n7-intake-runs/1", "steps": steps, "production_unchanged": before == after and all(after.values()),
            "production_files_checked": len(after)}
    (ev / "runs.json").write_text(json.dumps(body, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("production unchanged:", body["production_unchanged"], "files", len(after))
    return 0


if __name__ == "__main__":
    sys.exit(main())
