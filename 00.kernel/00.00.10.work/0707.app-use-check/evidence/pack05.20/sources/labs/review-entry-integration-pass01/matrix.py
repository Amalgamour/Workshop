#!/usr/bin/env python3
"""#03 actual-source replay matrix (0707/05.18). NONPRODUCTION.

For each fixture, ONE copy root (production layout), runs in new processes:
  W  real v7 entry  <root>/app/librarian.py (live v7 bytes selected)  - wrong-root REFERENCE, not the baseline
  B  faithful v7 baseline: pinned pass03 through the explicit 05.17 root adapter (n7compat2 --repo-root, no patch)
  C  real v8 entry  <root>/app/librarian.py (candidate bytes selected) - the candidate under test
  B2 baseline again after C (drift check)
prepare and form for each. Book bytes are hashed before and after. Every declared manifest row is checked
against the C rows (path, measured sha256 == manifest sha256).
usage: matrix.py --rooms NEW-DIR --out FILE
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rie  # noqa: E402


def norm(row: dict) -> str | None:
    p = row.get("path")
    if p is None:
        return None
    return f"{rie.BOOK_REL}/{p}" if row.get("root", "book") == "book" else p


def coverage(rows: list, info: dict) -> dict:
    by = {}
    for r in rows:
        by.setdefault(norm(r), []).append(r)
    missing, wrong, ok = [], [], []
    for path, want in info["manifest_sha"].items():
        got = by.get(path) or []
        shas = {r.get("sha256") for r in got}
        if not got:
            missing.append(path)
        elif shas != {want}:
            wrong.append({"path": path, "measured": sorted(str(s) for s in shas), "manifest": want})
        else:
            ok.append(path)
    roles = {}
    for r in rows:
        roles[r.get("role")] = roles.get(r.get("role"), 0) + 1
    decl = {}
    for role, (path, h, n) in info["declared"].items():
        got = by.get(path) or []
        decl[role] = {"path": path, "rows": len(got), "sha_ok": bool(got) and all(r.get("sha256") == h for r in got)}
    return {"manifest_rows": len(info["manifest_sha"]), "covered": len(ok), "missing": missing, "hash_mismatch": wrong,
            "roles": roles, "unique_paths": len(by), "declared": decl}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rooms", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--only", action="append")
    a = ap.parse_args()
    rooms = Path(a.rooms)
    rie.refuse_inside(rooms)
    rooms.mkdir(parents=True, exist_ok=False)
    result = {"schema": "rie-matrix/1", "rooms": str(rooms), "fixtures": {}}
    for key in a.only or list(rie.FIXTURES):
        root = rooms / key
        _, info = rie.make_root(root, key, dispatcher="v7")
        ev = rooms / f"{key}-evidence"
        before = rie.tree_hashes(root)
        steps = {}

        def go(name, res):
            rie.save(res, ev, name)
            steps[name] = rie.summary(res)
            steps[name]["_rows"] = rie.rows_of(res.get("body"))
            print(f"{key:8} {name:12} exit {res['exit']} {steps[name]['measurement']} {str(steps[name]['intake_id'])[:16]} rows {steps[name]['row_count']} {steps[name]['finding_codes']}"[:230])

        go("W-prepare", rie.app(root, *rie.wb_args(root, key, "prepare")))
        go("W-form", rie.app(root, *rie.wb_args(root, key, "form")))
        go("B-prepare", rie.baseline(root, *rie.wb_args(root, key, "prepare")))
        go("B-form", rie.baseline(root, *rie.wb_args(root, key, "form")))
        # D: the real v8 DOOR on disk (its own __file__, code root = this root) while the v7 dispatcher bytes are
        # still selected: same file state as B, so parser parity is not confounded by the dispatcher change.
        go("D-prepare", rie.run([root / "app/review_loop_tools_v8.py", *rie.wb_args(root, key, "prepare")], cwd=root))
        sel = rie.select(root, "v8")
        go("C-prepare", rie.app(root, *rie.wb_args(root, key, "prepare")))
        go("C-form", rie.app(root, *rie.wb_args(root, key, "form")))
        go("B2-prepare", rie.baseline(root, *rie.wb_args(root, key, "prepare")))
        after = rie.tree_hashes(root)
        fx = rie.FIXTURES[key]
        keys = ("exit", "intake_id", "measurement", "kind", "finding_codes", "rows_sha", "cuts_sha", "row_count")
        bc = {k: (steps["B-prepare"][k], steps["C-prepare"][k]) for k in keys if steps["B-prepare"][k] != steps["C-prepare"][k]}
        bb = {k: (steps["B-prepare"][k], steps["B2-prepare"][k]) for k in keys if steps["B-prepare"][k] != steps["B2-prepare"][k]}
        bw = {k: (steps["W-prepare"][k], steps["B-prepare"][k]) for k in keys if steps["W-prepare"][k] != steps["B-prepare"][k]}
        bd = {k: (steps["B-prepare"][k], steps["D-prepare"][k]) for k in keys if steps["B-prepare"][k] != steps["D-prepare"][k]}
        b2c = {k: (steps["B2-prepare"][k], steps["C-prepare"][k]) for k in keys if steps["B2-prepare"][k] != steps["C-prepare"][k]}
        brows = {json.dumps(r, sort_keys=True) for r in steps["B-prepare"]["_rows"]}
        crows = {json.dumps(r, sort_keys=True) for r in steps["C-prepare"]["_rows"]}
        gained = sorted((json.loads(r).get("role"), norm(json.loads(r))) for r in crows - brows)
        lost = sorted((json.loads(r).get("role"), norm(json.loads(r))) for r in brows - crows)
        cov = coverage(steps["C-prepare"]["_rows"], info)
        form_eq = steps["C-form"]["intake_id"] == steps["C-prepare"]["intake_id"]
        verdict = {}
        if fx["kind"] == "N5NN":
            verdict["n5_unchanged_B_vs_C"] = not bc
            verdict["n5_parity_same_state"] = not bd and not b2c      # B==D (v7 dispatcher bytes), B2==C (v8 bytes)
            verdict["selection_changed_measurement"] = bool(bb)
        else:
            verdict["n7_identity_changed"] = "intake_id" in bc
            verdict["n7_lost_rows"] = lost
        verdict["c_complete"] = steps["C-prepare"]["measurement"] == "complete"
        verdict["all_declared_covered"] = cov["covered"] == cov["manifest_rows"] and not cov["hash_mismatch"]
        verdict["book_bytes_unchanged"] = before == after
        verdict["baseline_stable"] = not bb
        for s in steps.values():
            s.pop("_rows", None)
        result["fixtures"][key] = {"fixture": fx, "root": str(root), "dispatcher_v8_sha": sel, "declared": info["declared"],
                                   "steps": steps, "B_vs_C": bc, "W_vs_B": bw, "B_vs_B2": bb, "B_vs_D": bd, "B2_vs_C": b2c, "gained_rows": gained, "lost_rows": lost,
                                   "coverage_C": cov, "form_intake_equal": form_eq, "verdict": verdict}
        print(key, json.dumps(verdict)[:300])
    Path(a.out).write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
