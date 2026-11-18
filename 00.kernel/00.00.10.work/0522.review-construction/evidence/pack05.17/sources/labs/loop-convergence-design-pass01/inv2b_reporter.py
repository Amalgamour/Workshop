#!/usr/bin/env python3
"""Investigation II-b - selection x reporter interaction (0707/05.19). NONPRODUCTION. My own hostile cases.

X6 a COMBINED dispatcher (current + accepted reporter hunk + v8 review-loop selection), written on disk in a
   disposable root next to the frozen reporter v3 connector/declaration -> expected: the reporter refuses
   (v3 pins app/librarian.py f1d23d45...). The review-loop route of the same file still runs v8.
X7 reporter parity: the frozen reporter dispatcher (f1d23d45..., labs/review-report-hardening-pass01/librarian.py)
   on a root whose N7 0707/05.15 review was recorded+published through the v8 candidate -> expected: the v3 reporter
   (pinned to pass03 observation) does not report that v8 record as current.
usage: inv2b_reporter.py --rooms NEW-DIR --out FILE
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

REPORTER_DISPATCHER = lcd.LIVE / "labs/review-report-hardening-pass01/librarian.py"
CANDIDATE_V8_DISPATCHER = rie.CAND / "app/librarian.py"


def combined_dispatcher() -> bytes:
    """Reporter-candidate dispatcher with the v8 review-loop selection line and its docstring line applied."""
    t = REPORTER_DISPATCHER.read_text(encoding="utf-8")
    a = "to the pinned v7 door."
    b = '"review_loop_tools_v7.py", "librarian_review_loop_tools_v7"'
    assert t.count(a) == 1 and t.count(b) == 1
    return t.replace(a, "to the pinned v8 door.").replace(b, '"review_loop_tools_v8.py", "librarian_review_loop_tools_v8"').encode("utf-8")


def add_reporter(root: Path) -> None:
    decl = json.loads((lcd.LIVE / "app/review-report-v3.json").read_bytes())
    for rel in ("app/review_report_tools_v3.py", "app/review-report-v3.json"):
        (root / rel).write_bytes((lcd.LIVE / rel).read_bytes())
    for rel, pin in decl["tools"].items():
        if rel == "app/librarian.py":
            continue
        data = (lcd.LIVE / rel).read_bytes()
        if hashlib.sha256(data).hexdigest() != pin["sha256"]:
            raise SystemExit(f"refused: live {rel} differs from reporter v3 pin")
        dst = root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            dst.write_bytes(data)
        elif dst.read_bytes() != data:
            raise SystemExit(f"refused: root already holds different bytes at {rel}")


def report(root: Path, key: str) -> dict:
    fx = lcd.FIX[key]
    return rie.run([root / "app/librarian.py", "review-report", "--book", str(root / lcd.BOOK_REL), "--source", fx["page"], "--pass", fx["pass"]], cwd=root)


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

    root, _ = lcd.make_root(rooms / "X6", ["n7-0515"], omit=("06.15.review.md",))
    root = root.path
    add_reporter(root)
    comb = combined_dispatcher()
    (root / "app/librarian.py").write_bytes(comb)
    r = report(root, "n7-0515")
    p = rie.app(root, *lcd.args(root, "n7-0515", "prepare"))
    out["X6"] = {"expected": "reporter v3 refuses the combined dispatcher; review-loop route still runs v8",
                 "combined_dispatcher_sha256": hashlib.sha256(comb).hexdigest(), "combined_bytes": len(comb),
                 "report_exit": r["exit"], "report_stderr": r["stderr"][-300:], "review_loop_measurement": lcd.body(p).get("measurement"),
                 "as_predicted": r["exit"] == 2 and "app/librarian.py" in r["stderr"] and lcd.body(p).get("measurement") == "complete"}
    print("X6", json.dumps(out["X6"])[:300])

    root, _ = lcd.make_root(rooms / "X7", ["n7-0515"], omit=("06.15.review.md",))
    root = root.path
    add_reporter(root)
    p = rie.app(root, *lcd.args(root, "n7-0515", "prepare"))
    rec = rie.app(root, *lcd.args(root, "n7-0515", "record", "--intake", lcd.body(p).get("intake_id"), "--judgment", str(jf)))
    pub = rie.app(root, *lcd.args(root, "n7-0515", "publish", "--review", lcd.body(rec).get("review_id") or "none"))
    (root / "app/librarian.py").write_bytes(REPORTER_DISPATCHER.read_bytes())        # select the reporter candidate (v7 review-loop)
    r = report(root, "n7-0515")
    rb = r["body"] if isinstance(r["body"], dict) else {}
    (rooms / "X7-report.stdout").write_text(r["stdout"], encoding="utf-8")
    flat = json.dumps(rb)
    out["X7"] = {"expected": "v3 reporter does not report the v8-recorded N7 review as current",
                 "v8_record": {"review_id": lcd.body(rec).get("review_id"), "publish_exit": pub["exit"]},
                 "report_exit": r["exit"], "report_stderr": r["stderr"][-300:],
                 "report_keys": sorted(rb)[:40], "stale": rb.get("stale"), "state": rb.get("state"),
                 "mentions_review_id": (lcd.body(rec).get("review_id") or "x") in flat, "measurement_in_report": rb.get("measurement")}
    out["X7"]["as_predicted"] = r["exit"] != 0 or rb.get("stale") is True or rb.get("state") not in (None, "current")
    print("X7", json.dumps(out["X7"])[:400])
    Path(a.out).write_text(json.dumps({"schema": "lcd-inv2b/1", "rooms": str(rooms), "cases": out}, indent=1) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
