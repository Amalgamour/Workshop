#!/usr/bin/env python3
"""0707/05.20 historical replay and N5 copied-book probe. NONPRODUCTION. My prototype tests.
R1 real N7 0707/05.15 and 05.17 (pack05.19 snapshots + hash-verified rows, via lcd) through the overlay: the local pair
   matches, chronology is reported 'unverified' (no open record exists for history; nothing inferred from mtime).
R2 N5 copied-book probe (UNCHANGED N5 behavior, documented): an N5 record copied into another book instance still reads
   current under BOTH pass04 and the overlay; the overlay deliberately does not change N5.
usage: replay_history.py --rooms NEW-DIR --out FILE
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB))
import run_matrix as M  # noqa: E402
from run_matrix import lcd, rie, lifecycle, B, codes  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rie.refuse_inside(rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    jf = rooms / "lab-judgment.json"
    jf.write_text(json.dumps(lifecycle.JUDGMENT, indent=1) + "\n", encoding="utf-8")
    out = {}
    r, _ = lcd.make_root(rooms / "R1", ["n7-0515", "n7-0517"], dispatcher="v8")
    root = r.path
    (root / "labs/n7-local-lifecycle-pass01").mkdir(parents=True, exist_ok=True)
    (root / "labs/n7-local-lifecycle-pass01/workbook.py").write_bytes(M.OVL_BYTES)
    for key in ("n7-0515", "n7-0517"):
        fx = lcd.FIX[key]
        M.use(root, "OVL")
        p = M.cmd(root, fx["page"], fx["pass"], "prepare")
        M.use(root, "P04")
        q = M.cmd(root, fx["page"], fx["pass"], "prepare")
        ex = B(p).get("exchange") or {}
        out[key] = {"state": ex.get("state"), "chronology": ex.get("chronology"), "n1_custody": ex.get("n1_custody"),
                    "measurement": B(p).get("measurement"), "codes": codes(p),
                    "artifact_rows_overlay": len({x.get("path") for x in rie.rows_of(B(p)) if x.get("role") == "artifact"}),
                    "artifact_rows_pass04": len({x.get("path") for x in rie.rows_of(B(q)) if x.get("role") == "artifact"})}
        print(key, json.dumps(out[key])[:300])
    out["R1_ok"] = all(out[k]["state"] == "matched" and out[k]["chronology"] == "unverified" and out[k]["measurement"] == "complete"
                       and out[k]["artifact_rows_overlay"] == out[k]["artifact_rows_pass04"] for k in ("n7-0515", "n7-0517"))
    # R2 N5 copied-book probe
    root = M.new_root(rooms / "R2-bookA")
    pdir = root / M.BOOK / M.N5PAGE
    evd = pdir / "evidence/b"
    a_ = M.write(evd / "artifact.md", "LAB N5 artifact\n")
    s_ = M.write(evd / "submission.md", "LAB N5 submission\n")
    man = M.write(evd / "artifact-manifest.json", json.dumps({"files": [{"path": f"{M.BOOK}/{M.N5PAGE}/evidence/b/artifact.md", "bytes": len(a_), "sha256": M.sha(a_)}]}) + "\n")
    M.write(pdir / "05.01.md", f"# 05.01 SYNTHETIC N5 pack\n\n## Goal\nLAB-ONLY.\n\n## Return pointer\nSubmission: {M.BOOK}/{M.N5PAGE}/evidence/b/submission.md sha256 {M.sha(s_)}, {len(s_)} bytes.\n"
                                 f"Artifact manifest: {M.BOOK}/{M.N5PAGE}/evidence/b/artifact-manifest.json sha256 {M.sha(man)}, {len(man)} bytes.\n\n## Review - Codex Prime\nPENDING.\n")
    p = M.cmd(root, M.N5PAGE, "05.01", "prepare")
    M.cmd(root, M.N5PAGE, "05.01", "record", "--intake", B(p).get("intake_id"), "--judgment", str(jf))
    shutil.copytree(root, rooms / "R2-bookB")
    rootB = rooms / "R2-bookB"
    res = {}
    for which in ("OVL", "P04"):
        M.use(rootB, which)
        rd = M.cmd(rootB, M.N5PAGE, "05.01", "read")
        res[which] = {"exit": rd["exit"], "stale": B(rd).get("stale")}
    out["R2_n5_copied_book"] = res
    out["R2_same_under_both"] = res["OVL"] == res["P04"]
    print("R2", json.dumps(res))
    Path(a.out).write_text(json.dumps({"schema": "n7-local-replay/0", "rooms": str(rooms), "results": out}, indent=1) + "\n", encoding="utf-8")
    return 0 if out["R1_ok"] and out["R2_same_under_both"] else 1


if __name__ == "__main__":
    sys.exit(main())
