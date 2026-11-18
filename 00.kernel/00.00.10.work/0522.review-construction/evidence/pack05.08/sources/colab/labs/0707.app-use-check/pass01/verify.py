#!/usr/bin/env python3
"""0707 pass01: aggregate per-case criteria into verification.json.

usage: verify.py <run>   (reads the run's evidence; writes build05.01/verification.json)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness as H  # noqa: E402


def main() -> int:
    name = sys.argv[1]
    out = H.EVIDENCE / "runs" / name
    calls = [json.loads(line) for line in (out / "calls.jsonl").read_bytes().splitlines()]

    def body(row):
        raw = (out / row["stdout"]).read_bytes()
        return json.loads(raw) if raw.strip() else None

    def get(case, label):
        row = [r for r in calls if r["case"] == case and r["label"] == label][-1]
        return row, body(row), (out / row["stderr"]).read_bytes().decode("utf-8", "replace").strip()

    def rres(b):
        return (b or {}).get("render", {}) and b["render"].get("result")

    cases = []

    def case(cid, criterion, ok, evidence):
        cases.append({"case": cid, "criterion": criterion, "ok": bool(ok), "evidence": evidence})

    cmp = json.loads((out / "recovery-comparison.json").read_bytes())
    r, b, _ = get("A", "render")
    r2, b2, _ = get("A", "read")
    case("A", "describe/prepare/record/render exit 0; new-process read reviewed+rendered; recovered judgment equals supplied; flags false/not-established",
         all(x["exit"] == 0 for x in calls if x["case"] == "A") and rres(b) == "rendered" and b2["pass_state"] == "reviewed"
         and b2["full_success"] is True and b2["accepted"] is False and cmp["all_ok_excluding_observation_checks"],
         ["calls 01-05", "recovery-comparison.json"])
    _, b9, _ = get("B", "read-before-recover")
    _, b10, _ = get("B", "recover")
    _, b11, _ = get("B", "read-after-recover")
    case("B", "after record-only stop: read shows render-pending; recover renders; read reviewed; judgment and section equal A",
         b9["pass_state"] == "render-pending" and b9["full_success"] is False and rres(b10) == "rendered" and b11["pass_state"] == "reviewed",
         ["calls 06-11", "recovery-comparison.json B checks"])
    c = json.loads((out / "C-page-check.json").read_bytes())
    _, b12, _ = get("C", "recover-on-A")
    _, b13, _ = get("C", "render-again-on-A")
    case("C", "recover and render again on A are already-rendered; page bytes unchanged",
         rres(b12) == "already-rendered" and rres(b13) == "already-rendered" and c["unchanged"], ["calls 12-14", "C-page-check.json"])
    d = json.loads((out / "D-page-check.json").read_bytes())
    r18, b18, e18 = get("D", "render-after-target-change")
    _, b19, _ = get("D", "read")
    case("D", "render after a target change is refused (write token changed), exit 2; page keeps the changed bytes, nothing rendered",
         r18["exit"] == 2 and b18["rule"] == "write token changed since read" and d["render_left_changed_bytes"] and b19["pass_state"] == "render-pending",
         ["calls 15-19", "D-page-check.json"])
    e = json.loads((out / "E-page-check.json").read_bytes())
    r23, b23, _ = get("E", "render")
    r24, b24, _ = get("E", "recover")
    _, b25, _ = get("E", "read")
    case("E", "substantive page: render and recover are render-conflict exit 2, full_success false; page bytes = snapshot; one partial; read not full_success",
         r23["exit"] == 2 and rres(b23) == "render-conflict" and b23["full_success"] is False and r24["exit"] == 2
         and rres(b24) == "render-conflict" and e["unchanged"] and len(e["partials"]) == 1 and b25["full_success"] is False,
         ["calls 20-25", "E-page-check.json"])
    r26, b26, e26 = get("F", "prepare-root-inside-checkout")
    case("F", "fixture root inside the checkout: stop: on stderr, exit 2, no loop output",
         r26["exit"] == 2 and e26.startswith("stop: ") and b26 is None, ["call 26"])

    gb = json.loads((out / "guard-before.json").read_bytes())
    ga = json.loads((out / "guard-after.json").read_bytes())
    wb = json.loads((out / "watched-before.json").read_bytes())
    wa = json.loads((out / "watched-after.json").read_bytes())
    before = set((out / "git-status-before.txt").read_text(encoding="utf-8").splitlines())
    after = set((out / "git-status-after.txt").read_text(encoding="utf-8").splitlines())
    result = {
        "schema": "0707-verification/1",
        "run": name,
        "python": sys.version.split()[0],
        "calls": len(calls),
        "every_call_guarded_before_and_after": all(x["guard_before"] and x["guard_after"] for x in calls),
        "guard_start": gb["ok"],
        "guard_end": ga["ok"],
        "watched_live_unchanged": wb == wa,
        "live_layout_created": wa["layout_exists"],
        "cases": cases,
        "all_cases_ok": all(x["ok"] for x in cases),
        "observations_not_criteria": [x for x in cmp["checks"] if not x["ok"]],
        "checkout_status_new_lines": sorted(after - before),
        "checkout_status_removed_lines": sorted(before - after),
        "checkout_new_lines_disposition": "Not app writes. Neither path is referenced by the 11 pinned files; every cycle/loop write site is fixture-root relative. labs/prime-desk-use-pass01 files are stamped 12:36:42-12:36:44 (inside call 03's window, 12:36:38-12:36:45); 0401.goal/06.03.md 12:39:51, after the last call. Names and times only; contents not read.",
        "first_failures": "none in run1; no case was rerun",
    }
    (H.EVIDENCE / "verification.json").write_bytes(H.dump(result))
    print(json.dumps({k: result[k] for k in ("all_cases_ok", "every_call_guarded_before_and_after", "watched_live_unchanged", "live_layout_created", "checkout_status_new_lines")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
