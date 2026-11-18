#!/usr/bin/env python3
"""Investigation I - source-list capacity seam and supplied-judgment preservation (0707/05.19).
NONPRODUCTION. My own hostile cases against FROZEN baseline tools on disposable roots (real v8 entry with the
disclosed 05.18 root adapter; record path = unchanged pass02/pass03 + pinned prime_review pass02).

C1 actual 0512/05.09 with Prime's EXACT retained judgment (prime-review05.09/core-review/judgment.json):
   expected (baseline) record refused 'limit sources'; no review stored; the supplied judgment kept in failed/.
C2 boundary on a synthetic N5 page: K book artifacts, K = 22 and 23 -> find the exact source count that refuses.
C3 composition: 40 artifacts all CODE-root -> not counted as sources (artifact count alone does not predict).
C4 prediction: actual 0707/05.17 (25 book artifacts, N7 parsed by v8) -> record refused the same way.
C5 control: actual 0522/05.14 (19 book artifacts) records preliminary (Prime's 06.31 success, on a copy).
Expected-vs-observed is recorded per case; a 'pass' means the baseline behaved as PREDICTED, not that it is fixed.
usage: inv1_capacity.py --rooms NEW-DIR --out FILE
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lcd  # noqa: E402
from lcd import rie  # noqa: E402

sys.path.insert(0, str(lcd.LIVE / "labs/review-entry-integration-pass01"))
import lifecycle  # noqa: E402

PRIME_JUDGMENT = lcd.LIVE / "00.kernel/00.00.10.work/0512.prime-review/evidence/prime-review05.09/core-review/judgment.json"


def store_files(root: Path, page: str, pas: str) -> list:
    base = root / lcd.BOOK_REL / "workbook-review" / page / pas
    return sorted(str(p.relative_to(base)).replace("\\", "/") for p in base.rglob("*") if p.is_file()) if base.exists() else []


def record_case(root: Path, key: str, judgment_file: Path) -> dict:
    p = rie.app(root, *lcd.args(root, key, "prepare"))
    iid = lcd.body(p).get("intake_id")
    rec = rie.app(root, *lcd.args(root, key, "record", "--intake", iid or "none", "--judgment", str(judgment_file)))
    fx = lcd.FIX[key] if isinstance(key, str) else key
    files = store_files(root, fx["page"], fx["pass"])
    failed = [f for f in files if f.startswith("failed/") and f.endswith(".json")]
    kept = None
    if failed:
        doc = json.loads((root / lcd.BOOK_REL / "workbook-review" / fx["page"] / fx["pass"] / failed[0]).read_bytes())
        supplied = json.loads(judgment_file.read_bytes())

        def find(o):
            if o == supplied:
                return True
            if isinstance(o, dict):
                return any(find(v) for v in o.values())
            if isinstance(o, list):
                return any(find(v) for v in o)
            return False
        kept = {"failed_file": failed[0], "supplied_judgment_found_intact": find(doc), "failed_keys": sorted(doc) if isinstance(doc, dict) else None}
    rb = lcd.body(rec)
    return {"prepare_exit": p["exit"], "measurement": lcd.body(p).get("measurement"), "book_sources": lcd.book_sources(p),
            "row_count": len(rie.rows_of(lcd.body(p))), "record_exit": rec["exit"], "recorded": rb.get("recorded"), "review_id": rb.get("review_id"),
            "correction": rb.get("correction"), "mode": rb.get("mode"), "stored": [f for f in files if f.startswith("reviews/")], "failed": kept,
            "record_stderr": rec["stderr"][-200:]}


def synth(root: Path, name: str, k: int, code_root: bool) -> dict:
    """A synthetic N5 page 0598.<name>/05.01.md declaring K artifacts (book- or code-root). LABELLED SYNTHETIC."""
    page = f"0598.{name}"
    pdir = root / lcd.BOOK_REL / page
    ev = pdir / "evidence/b"
    ev.mkdir(parents=True)
    rows = []
    for i in range(k):
        if code_root:
            rel = f"labs/capacity-lab-{name}/a{i:03d}.txt"
        else:
            rel = f"{lcd.BOOK_REL}/{page}/evidence/b/a{i:03d}.txt"
        f = root / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(f"SYNTHETIC artifact {i} for 0707/05.19 capacity lab\n".encode())
        rows.append({"path": rel, "bytes": f.stat().st_size, "sha256": hashlib.sha256(f.read_bytes()).hexdigest()})
    sub = ev / "submission.md"
    sub.write_bytes(b"SYNTHETIC submission for the 0707/05.19 capacity lab\n" + b"x" * 300 + b"\n")
    man = ev / "artifact-manifest.json"
    man.write_bytes(json.dumps({"files": rows}, indent=1).encode() + b"\n")
    sb, mb = sub.read_bytes(), man.read_bytes()
    pointer = (f"Submission: {lcd.BOOK_REL}/{page}/evidence/b/submission.md sha256 {hashlib.sha256(sb).hexdigest()}, {len(sb)} bytes.\n"
               f"Artifact manifest: {lcd.BOOK_REL}/{page}/evidence/b/artifact-manifest.json sha256 {hashlib.sha256(mb).hexdigest()}, {len(mb)} bytes.\n")
    (pdir / "05.01.md").write_text(f"# 05.01 SYNTHETIC capacity page\n\n## Goal\nLab only.\n\n## Return pointer\n{pointer}\n## Review - Codex Prime\nPENDING.\n", encoding="utf-8")
    return {"page": page, "pass": "05.01"}


def main() -> int:
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

    def note(cid, expected, observed, ok, detail):
        out[cid] = {"expected": expected, "observed": observed, "as_predicted": ok, "detail": detail}
        print(f"{'AS-PREDICTED' if ok else 'UNEXPECTED':12} {cid}: {observed}"[:240])

    root, _ = lcd.make_root(rooms / "C1", ["n5-0512-0509"])
    d = record_case(root.path, "n5-0512-0509", PRIME_JUDGMENT)
    note("C1", "complete prepare; record refused 'limit sources'; no review stored; Prime's exact judgment kept in failed/",
         f"measurement {d['measurement']}, book sources {d['book_sources']}, record exit {d['record_exit']} {d['correction']}",
         d["measurement"] == "complete" and d["record_exit"] == 2 and "limit sources" in str(d["correction"]) and not d["stored"]
         and bool(d["failed"]) and d["failed"]["supplied_judgment_found_intact"], d)

    root, _ = lcd.make_root(rooms / "C2", [])
    res = {}
    for k in (21, 22, 23):
        fx = synth(root.path, f"book{k}", k, False)
        res[k] = record_case(root.path, fx, jf)
    edge = {k: (v["book_sources"], v["record_exit"], v["correction"]) for k, v in res.items()}
    note("C2", "sources = K + 2 (assignment, submission); <= 24 records, 25 refuses",
         str(edge), res[22]["record_exit"] == 0 and res[23]["record_exit"] == 2 and "limit sources" in str(res[23]["correction"]), res)

    fx = synth(root.path, "code40", 40, True)
    d = record_case(root.path, fx, jf)
    note("C3", "40 code-root artifacts: complete, sources = 2, records preliminary",
         f"measurement {d['measurement']}, book sources {d['book_sources']}, record exit {d['record_exit']} mode {d['mode']}",
         d["measurement"] == "complete" and d["record_exit"] == 0, d)

    root, _ = lcd.make_root(rooms / "C4", ["n7-0517"])
    d = record_case(root.path, "n7-0517", jf)
    note("C4", "prediction: N7 0517 parsed complete by v8, record refused 'limit sources' (25 book artifacts)",
         f"measurement {d['measurement']}, book sources {d['book_sources']}, record exit {d['record_exit']} {d['correction']}",
         d["measurement"] == "complete" and d["record_exit"] == 2 and "limit sources" in str(d["correction"]), d)

    root, _ = lcd.make_root(rooms / "C5", ["n5-0522-0514"])
    d = record_case(root.path, "n5-0522-0514", jf)
    note("C5", "control: 0522/05.14 records preliminary (as Prime's live core run)",
         f"measurement {d['measurement']}, book sources {d['book_sources']}, record exit {d['record_exit']} mode {d['mode']}",
         d["record_exit"] == 0 and d["mode"] == "preliminary", d)

    agg = {"as_predicted": sum(v["as_predicted"] for v in out.values()), "total": len(out)}
    Path(a.out).write_text(json.dumps({"schema": "lcd-inv1/1", "rooms": str(rooms), "aggregate": agg, "cases": out}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("aggregate", agg)
    return 0 if agg["as_predicted"] == agg["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
