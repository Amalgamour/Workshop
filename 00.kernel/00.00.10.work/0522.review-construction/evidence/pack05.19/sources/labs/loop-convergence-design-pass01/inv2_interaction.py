#!/usr/bin/env python3
"""Investigation II - parsing / first-review / render / selection interaction (0707/05.19). NONPRODUCTION.
My own hostile cases on disposable roots. Expected = what the FROZEN baseline does today (a documented failure
where the Director's decision requires otherwise); 'required' = what an accepted successor must do.

X1 A-01 end-to-end: the N7 manifest line gets a trailing ' note' and a self-consistent decoy 'artifact-manifest.json,'
   (listing 1 artifact) exists. Today: v8 binds the decoy, measures 'complete' with 1 artifact, records and PUBLISHES.
   Required (Director 2026-11-04): blocked intake, no record/publication.
X2 A-02 end-to-end: a Returned line with a hash in the attribution (refused) plus a second valid Returned line naming
   06.15.notes.md. Today: binds the second. Required: blocked.
X3 the frozen 0521 first-target successor workbook (labs/n7-first-review-pass01, executed read-only from live, on an
   external Colab N7 book): cannot parse the N7 pointer (pass02 lineage) -> incomplete. Composition proof.
X4 Colab N7 first review today: custody missing -> record preliminary, cycle not called; preliminary publish CREATES the
   absent 06.15.review.md. The frozen 0521 successor refuses exactly this ('a preliminary record does not create it').
X5 selection inventory (static, frozen manifests in pack05.19): returns that declare app/ or staged v8/pass04 files.
usage: inv2_interaction.py --rooms NEW-DIR --out FILE
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lcd  # noqa: E402
from lcd import rie  # noqa: E402

sys.path.insert(0, str(lcd.LIVE / "labs/review-entry-integration-pass01"))
import lifecycle  # noqa: E402

PAGE = "0707.app-use-check"
SUCCESSOR_0521 = lcd.LIVE / "labs/n7-first-review-pass01/workbook.py"


def set_pointer(root: Path, lines: list) -> None:
    pf = root / lcd.BOOK_REL / PAGE / "05.15.pack.md"
    t = pf.read_text(encoding="utf-8")
    head, rest = t.split("## Return pointer\n", 1)
    parts = rest.split("\n## ", 1)
    tail = ("\n## " + parts[1]) if len(parts) == 2 else ""
    pf.write_text(head + "## Return pointer\n" + "\n".join(lines) + "\n" + tail, encoding="utf-8")


def pointer_lines(root: Path) -> list:
    t = (root / lcd.BOOK_REL / PAGE / "05.15.pack.md").read_text(encoding="utf-8")
    return [x for x in t.split("## Return pointer\n", 1)[1].split("\n## ", 1)[0].splitlines() if x.strip()]


def loop(root: Path, jf: Path, publish: bool) -> dict:
    p = rie.app(root, *lcd.args(root, "n7-0515", "prepare"))
    rows = rie.rows_of(lcd.body(p))
    rec = rie.app(root, *lcd.args(root, "n7-0515", "record", "--intake", lcd.body(p).get("intake_id") or "none", "--judgment", str(jf)))
    pub = rie.app(root, *lcd.args(root, "n7-0515", "publish", "--review", lcd.body(rec).get("review_id") or "none")) if publish and rec["exit"] == 0 else None
    target = root / lcd.BOOK_REL / PAGE / "06.15.review.md"
    return {"measurement": lcd.body(p).get("measurement"), "codes": lcd.codes(p),
            "submission": [r.get("path") for r in rows if r.get("role") == "submission"],
            "manifest": [r.get("path") for r in rows if r.get("role") == "artifact-manifest"],
            "artifacts": len({r.get("path") for r in rows if r.get("role") == "artifact"}),
            "record_exit": rec["exit"], "mode": lcd.body(rec).get("mode"), "cycle": lcd.body(rec).get("cycle"),
            "publish_exit": None if pub is None else pub["exit"], "published": None if pub is None else lcd.body(pub).get("published"),
            "target_created": target.exists(), "publish_correction": None if pub is None else lcd.body(pub).get("correction")}


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

    def note(cid, today, required, observed, as_predicted, detail):
        out[cid] = {"expected_today": today, "required_after_successor": required, "observed": observed, "as_predicted": as_predicted, "detail": detail}
        print(f"{'AS-PREDICTED' if as_predicted else 'UNEXPECTED':12} {cid}: {observed}"[:250])

    # X1
    root, _ = lcd.make_root(rooms / "X1", ["n7-0515"], omit=("06.15.review.md",))
    root = root.path
    ev = root / lcd.BOOK_REL / PAGE / "evidence/design05.15"
    ret = root / lcd.BOOK_REL / PAGE / "05.15.return.md"
    decoy = ev / "artifact-manifest.json,"
    decoy.write_bytes(json.dumps({"files": [{"path": f"{lcd.BOOK_REL}/{PAGE}/05.15.return.md", "bytes": ret.stat().st_size,
                                             "sha256": hashlib.sha256(ret.read_bytes()).hexdigest()}]}).encode() + b"\n")
    db = decoy.read_bytes()
    lines = [x for x in pointer_lines(root) if not x.startswith("Artifact manifest:")]
    lines.insert(1, f"Artifact manifest: evidence/design05.15/artifact-manifest.json, sha256 {hashlib.sha256(db).hexdigest()}, {len(db)} bytes. note")
    set_pointer(root, lines)
    d = loop(root, jf, True)
    note("X1", "decoy bound, complete with 1 artifact, recorded, published", "intake blocked; nothing recorded or published",
         f"manifest {d['manifest']}, artifacts {d['artifacts']}, {d['measurement']}, record {d['record_exit']}, published {d['published']}",
         d["manifest"] == [f"{PAGE}/evidence/design05.15/artifact-manifest.json,"] and d["measurement"] == "complete" and d["published"] is True, d)

    # X2
    root, _ = lcd.make_root(rooms / "X2", ["n7-0515"], omit=("06.15.review.md",))
    root = root.path
    notes = root / lcd.BOOK_REL / PAGE / "06.15.notes.md"
    nb = notes.read_bytes()
    lines = pointer_lines(root)
    lines = [x.replace("(claude-opus-5-5, 2026-11-03)", f"(sha256 {'b' * 64})") if x.startswith("Returned:") else x for x in lines]
    lines.insert(1, f"Returned: 06.15.notes.md (second line), sha256 {hashlib.sha256(nb).hexdigest()}, {len(nb)} bytes.")
    set_pointer(root, lines)
    d = loop(root, jf, False)
    note("X2", "refused line ignored; submission = 06.15.notes.md; complete; recorded", "intake blocked",
         f"submission {d['submission']}, {d['measurement']}, codes {d['codes']}, record {d['record_exit']}",
         d["submission"] == [f"{PAGE}/06.15.notes.md"] and d["record_exit"] == 0, d)

    # X3
    root, _ = lcd.make_root(rooms / "X3", ["n7-0515"], omit=("06.15.review.md",), dispatcher="v7")
    root = root.path
    r = rie.run([SUCCESSOR_0521, *lcd.args(root, "n7-0515", "prepare")], cwd=rooms)
    b = lcd.body(r)
    rows = rie.rows_of(b)
    note("X3", "0521 successor (pass02 lineage) cannot parse the Colab N7 pointer -> incomplete", "a combined successor = N7 grammar + 0521 overlay on ONE chain",
         f"exit {r['exit']}, kind {b.get('kind')}, {b.get('measurement')}, codes {lcd.codes(r)}",
         b.get("kind") == "N7NN" and b.get("measurement") == "incomplete" and "submission-not-declared" in lcd.codes(r),
         {"exit": r["exit"], "stderr": r["stderr"][-300:], "rows": len(rows), "successor_sha256": hashlib.sha256(SUCCESSOR_0521.read_bytes()).hexdigest()})

    # X4
    root, _ = lcd.make_root(rooms / "X4", ["n7-0515"], omit=("06.15.review.md",))
    d = loop(root.path, jf, True)
    src = SUCCESSOR_0521.read_text(encoding="utf-8")
    refusal = "target file is absent; a preliminary record does not create it" in src
    note("X4", "custody missing -> preliminary, cycle not called; preliminary publish creates 06.15.review.md",
         "DECISION NEEDED: the frozen 0521 successor refuses this exact publish",
         f"mode {d['mode']}, cycle {d['cycle']}, publish {d['publish_exit']}, created {d['target_created']}; 0521 refusal text present {refusal}",
         d["mode"] == "preliminary" and not (d["cycle"] or {}).get("called") and d["target_created"] and refusal, d)

    # X5 static inventory
    fz = lcd.frozen()
    hits = []
    for rel in sorted(fz):
        if not rel.endswith("artifact-manifest.json"):
            continue
        try:
            doc = json.loads((lcd.PACK19 / fz[rel]["snapshot"]).read_bytes())
        except Exception:
            continue
        rows = doc.get("files") if isinstance(doc, dict) else None
        for row in rows or []:
            p = row.get("path") if isinstance(row, dict) else None
            if isinstance(p, str) and (p.startswith("app/") or p.startswith("labs/workbook-review-pass04/")):
                hits.append({"manifest": rel, "path": p, "sha256": row.get("sha256")})
    by = {}
    for h in hits:
        by.setdefault(h["manifest"], []).append(h["path"])
    dispatcher = sorted(m for m, ps in by.items() if "app/librarian.py" in ps)
    note("X5", "static: frozen manifests declaring app/ or staged pass04 files", "selection must not repin them; they show stale and stay preserved",
         f"{len(by)} manifests declare app/ or pass04 files; {len(dispatcher)} declare app/librarian.py: {dispatcher}", True, {"by_manifest": by})

    agg = {"as_predicted": sum(v["as_predicted"] for v in out.values()), "total": len(out)}
    Path(a.out).write_text(json.dumps({"schema": "lcd-inv2/1", "rooms": str(rooms), "aggregate": agg, "cases": out}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("aggregate", agg)
    return 0 if agg["as_predicted"] == agg["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
