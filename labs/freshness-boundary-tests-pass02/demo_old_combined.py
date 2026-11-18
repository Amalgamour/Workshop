#!/usr/bin/env python3
"""Show the OLD combined candidate (Grok-1 0522/05.17, Prime's frozen external copy) is refused for its REAL identity
problems by the explicit-identity reader. NONPRODUCTION. The candidate's code and expectations are never edited.

  A  Prime's frozen harness-inputs/2 identity + the copy                -> refused (not a legacy baseline; open_entry not
                                                                           declared; no workbook_entry)
  B  an honest harness-inputs/3 identity of the copy AS IT STANDS        -> refused (declared workbook absent from root)
  C  TEST-SIDE ASSEMBLY (labelled): the copy plus the reviewed pass01 files placed at their declared relative paths,
     with an honest v3 identity                                          -> identity verifies, then the execution proof
     shows the declared workbook is a DECOY: the dispatcher runs D:\\Git\\lib-build's canonical copy -> refused
The assembly only places frozen reviewed bytes beside the unchanged candidate; it is not a repaired candidate.
usage: demo_old_combined.py --rooms NEW-DIR --out FILE
"""

import argparse
import copy
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import identity as I  # noqa: E402
import run as A  # noqa: E402

LIVE = I.LIVE
OLD_COPY = Path(r"D:\librarian\temp\prime-night-0517-0723\combined-copy")
OLD_V2 = LIVE / "00.kernel/00.00.10.work/0522.review-construction/evidence/prime-review05.17/combined-measured-inputs.json"
P = "labs/review-loop-convergence-pass01"
ASSEMBLE = {f"{P}/workbook.py": "workbook", f"{P}/review_loop_tools.py": "dependency", f"{P}/review_report_tools.py": "dependency",
            f"{P}/report.py": "dependency", f"{P}/review-loop.json": "declaration"}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def v3(root: Path, include_assembled: bool) -> dict:
    base = json.loads(OLD_V2.read_text(encoding="utf-8"))
    doc = copy.deepcopy(base)
    doc["schema"] = "harness-inputs/3"
    files = [{"path": "app/librarian.py", "role": "entry"}]
    rows = []
    for f in files + [{"path": p, "role": r} for p, r in ASSEMBLE.items()]:
        src = (root / f["path"]) if (root / f["path"]).is_file() else (LIVE / f["path"])   # B: hash the reviewed bytes it SHOULD hold
        b = src.read_bytes()
        rows.append({"path": f["path"], "sha256": sha(b), "bytes": len(b), "role": f["role"]})
    doc["candidate"] = {"schema": "candidate-identity/1", "name": "grok-0517-explicit (Claude test-side description)", "kind": "combined",
                        "entry": "app/librarian.py", "workbook_entry": f"{P}/workbook.py", "open_entry": f"{P}/workbook.py",
                        "reporter_entry": None, "candidate_json_sha256": sha((root / "CANDIDATE.json").read_bytes()), "files": rows,
                        "lab_differences": base["candidate"]["lab_differences"]}
    return doc


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    shape = A.R1.load_inputs_check().shape_problems
    out = {"schema": "old-combined-identity-demo/1", "copy": str(OLD_COPY),
           "copy_identity": {"CANDIDATE.json": sha((OLD_COPY / "CANDIDATE.json").read_bytes()), "app/librarian.py": sha((OLD_COPY / "app/librarian.py").read_bytes())}}
    ra = rooms / "A-copy"
    shutil.copytree(OLD_COPY, ra)
    try:
        I.resolve(json.loads(OLD_V2.read_text(encoding="utf-8")), ra, shape)
        out["A"] = {"refused": None, "ok": False}
    except I.Refused as exc:
        out["A"] = {"refused": str(exc), "ok": True}
    rb = rooms / "B-copy"
    shutil.copytree(OLD_COPY, rb)
    try:
        I.resolve(v3(rb, False), rb, shape)
        out["B"] = {"refused": None, "ok": False}
    except I.Refused as exc:
        out["B"] = {"refused": str(exc), "ok": "declared file absent" in str(exc)}
    rc = rooms / "C-assembled"
    shutil.copytree(OLD_COPY, rc)
    for rel in ASSEMBLE:
        (rc / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(LIVE / rel, rc / rel)
    doc = v3(rc, True)
    (rooms / "C-identity.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
    try:
        ident = I.resolve(doc, rc, shape)
        out["C"] = {"identity": "verified", "mode": ident["mode"]}
        wb, op, rp = A.probes(A.R1, ident)
        proof = {"workbook": I.tamper_proof(rc, ident, ident["workbook_entry"], wb, rooms / "C-proof", "workbook")}
        proof["open"] = I.tamper_proof(rc, ident, ident["open_entry"], op, rooms / "C-proof", "open")
        out["C"]["proof"] = proof
        try:
            A.gate(ident, rc, rooms / "C-gate")
            out["C"].update({"gate": "passed", "ok": False})
        except I.Refused as exc:
            out["C"].update({"gate": f"refused: {exc}", "ok": "DECOY" in str(exc)})
    except I.Refused as exc:
        out["C"] = {"identity": f"refused: {exc}", "ok": False}
    out["copy_unchanged"] = out["copy_identity"] == {"CANDIDATE.json": sha((OLD_COPY / "CANDIDATE.json").read_bytes()),
                                                     "app/librarian.py": sha((OLD_COPY / "app/librarian.py").read_bytes())}
    Path(a.out).write_text(json.dumps(out, indent=1, default=str) + "\n", encoding="utf-8")
    for k in ("A", "B", "C"):
        print(k, "OK " if out[k].get("ok") else "BAD", out[k].get("refused") or out[k].get("gate") or out[k].get("identity"))
    print("copy unchanged:", out["copy_unchanged"])
    return 0 if all(out[k].get("ok") for k in ("A", "B", "C")) and out["copy_unchanged"] else 1


if __name__ == "__main__":
    sys.exit(main())
