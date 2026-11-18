#!/usr/bin/env python3
"""#03 measured-context tests on the ACTUAL candidate pass04 (0707/05.18). NONPRODUCTION. Author tests.

One NEW root holds two fixtures (N5 0512/05.06 and N7 0707/05.15). The candidate pass04 (lab adapter bytes)
is imported from that root. A spy wraps pass04.PASS03_BUILD (the delegate inside build_intake) to record,
WHILE intake runs, the measured kind in pass04.KIND and how the one ambiguous string parses right then.
X1 sequential N5 -> N7 -> N5 -> N7: kind follows address_of; KIND is None between calls.
X2 the collision string `Artifact manifest: m.json, sha256 ...` means 'm.json,' under N5 and 'm.json' under N7,
   decided only by the measured context (no file named either exists in the root).
X3 an exception inside intake (injected into the delegate) still resets KIND; the next call is correct.
X4 the real intake results equal the matrix (rows bound for N7; N5 submission path unchanged).
usage: ctx_test.py --room NEW-DIR --out FILE
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import rie  # noqa: E402

H = "a" * 64
COLLISION = f"Submission: s.md sha256 {H}, 1 bytes.\nArtifact manifest: m.json, sha256 {H}, 9 bytes."


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--room", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    room = Path(a.room)
    rie.refuse_inside(room)
    room.mkdir(parents=True, exist_ok=False)
    r = rie.Root(room)
    rie.build_code(r)
    rie.build_fixture(r, "n5-0512")
    rie.build_fixture(r, "n7-0515")
    spec = importlib.util.spec_from_file_location("pass04_candidate_ctx", room / "labs/workbook-review-pass04/workbook.py")
    p4 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(p4)
    real_delegate = p4.PASS03_BUILD
    seen = []
    inject = {"raise": False}

    def spy(book, source, pass_id):
        kind = p4.KIND.get()
        col = p4.parse_pointer(COLLISION)
        seen.append({"source": source, "pass": pass_id, "kind_inside": kind,
                     "collision_manifest": (col["manifest"] or {}).get("path")})
        if inject["raise"]:
            raise RuntimeError("LAB fault injected inside intake")
        return real_delegate(book, source, pass_id)

    p4.PASS03_BUILD = spy                               # lab fault injection point (module global used by build_intake)
    book = room / rie.BOOK_REL
    rows = []
    calls = [("0512.prime-review", "05.06"), ("0707.app-use-check", "05.15"), ("0512.prime-review", "05.06"), ("0707.app-use-check", "05.15")]
    for src, pas in calls:
        intake = p4.build_intake(book, src, pas)
        rows.append({"source": src, "kind_after": p4.KIND.get(), "submission": next((x.get("path") for x in intake["rows"] if x.get("role") == "submission"), None),
                     "artifacts": len({x.get("path") for x in intake["rows"] if x.get("role") == "artifact"}), "intake_id": intake["intake_id"]})
    inject["raise"] = True
    raised = None
    try:
        p4.build_intake(book, "0707.app-use-check", "05.15")
    except RuntimeError as exc:
        raised = str(exc)
    after_exc = p4.KIND.get()
    inject["raise"] = False
    again = p4.build_intake(book, "0512.prime-review", "05.06")
    out = {
        "X1": {"ok": [s["kind_inside"] for s in seen[:4]] == ["N5NN", "N7NN", "N5NN", "N7NN"] and all(x["kind_after"] is None for x in rows), "seen": seen[:4], "rows": rows},
        "X2": {"ok": [s["collision_manifest"] for s in seen[:4]] == ["m.json,", "m.json", "m.json,", "m.json"]
               and not (book / "m.json").exists() and not (book / "m.json,").exists()},
        "X3": {"ok": raised is not None and after_exc is None and seen[4]["kind_inside"] == "N7NN" and seen[5]["kind_inside"] == "N5NN"
               and again["intake_id"] == rows[0]["intake_id"], "raised": raised, "kind_after_exception": after_exc},
        "X4": {"ok": rows[0]["intake_id"] == rows[2]["intake_id"] and rows[1]["intake_id"] == rows[3]["intake_id"] and rows[1]["artifacts"] == 26
               and rows[0]["submission"] == "0512.prime-review/evidence/build05.06/submission.md",   # ctx01 had an and/or precedence slip here
               "n7_artifacts": rows[1]["artifacts"], "n5_submission": rows[0]["submission"]},
    }
    agg = {k: v["ok"] for k, v in out.items()}
    Path(a.out).write_text(json.dumps({"schema": "rie-ctx/1", "room": str(room), "aggregate": agg, "cases": out}, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(agg))
    return 0 if all(agg.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
