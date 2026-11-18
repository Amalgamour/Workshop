#!/usr/bin/env python3
"""0707/05.03 pass03 probe runner (NONPRODUCTION). New run directory per execution; nothing deleted.

U1: verify_committed on a COPY of the real 05.01 A cycle record, plus synthetic tampers.
U2: mechanical() on COPIES of real 05.01 read views, with constructor pass04 `inspect`
    run read-only (pinned file, unchanged) on COPIED pages in a scratch root outside the checkout.
Exit status is nonzero if any required step fails (0510/06.08 V04).
usage: run_probe.py
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import secrets
import shutil
import subprocess
import sys
import traceback
from copy import deepcopy
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import loop_rules as L  # noqa: E402

CHECKOUT = Path(r"D:\Git\lib-build")
PAGE = CHECKOUT / "00.kernel" / "00.00.10.work" / "0707.app-use-check"
OLD = PAGE / "evidence" / "build05.01" / "runs" / "run1"
RUNS = PAGE / "evidence" / "design05.03" / "runs"
SCRATCH = Path(r"C:\Users\misg\AppData\Local\Temp\claude\D--Git-Librarian\313e7ce7-27d2-405b-881d-6a16a47199dc\scratchpad\0707-0503")
CONSTRUCT = CHECKOUT / "labs" / "review-construction-pass04" / "construct.py"
CONSTRUCT_PIN = ("6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20", 42582)
PAGE_REL = "0519.desk-app/05.01.md"


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    name = f"{stamp}-{secrets.token_hex(3)}"
    RUNS.mkdir(parents=True, exist_ok=True)
    run = RUNS / name
    run.mkdir()
    scratch = SCRATCH / name
    scratch.mkdir(parents=True)
    rows: list[dict] = []

    def step(label, fn):
        try:
            got = fn()
            rows.append({"step": label, **got})
        except Exception:  # noqa: BLE001 - keep every failure as evidence
            rows.append({"step": label, "ok": False, "error": traceback.format_exc()})

    # copies of inputs
    inputs = run / "inputs"
    inputs.mkdir()
    src = {
        "record.json": OLD / "books/A.after-render/cycle/05.01-r1/record.json",
        "COMMITTED.json": OLD / "books/A.after-render/cycle/05.01-r1/COMMITTED.json",
        "envelope.json": OLD / "books/A.after-render/cycle/05.01-r1/envelope.json",
        "registration.json": OLD / "books/A.after-render/registration.json",
        "A-read.stdout": OLD / "05-A-read.stdout", "B-read-before.stdout": OLD / "09-B-read-before-recover.stdout",
        "D-read.stdout": OLD / "19-D-read.stdout", "E-read.stdout": OLD / "25-E-read.stdout",
        "E-record.stdout": OLD / "22-E-record.stdout", "A-prepare.stdout": OLD / "02-A-prepare.stdout",
        "page-A-rendered.md": OLD / "books/A.after-render" / PAGE_REL, "page-B-pending.md": OLD / "books/B.after-record-stop" / PAGE_REL,
        "page-D-changed.md": OLD / "books/D.after" / PAGE_REL, "page-E-substantive.md": OLD / "books/E.after" / PAGE_REL,
    }
    for k, p in src.items():
        shutil.copyfile(p, inputs / k)
    (inputs / "SOURCES.json").write_text(json.dumps({k: {"from": str(p), "sha256": sha(p.read_bytes())} for k, p in src.items()}, indent=2) + "\n")
    rb = (inputs / "record.json").read_bytes()
    committed = json.loads((inputs / "COMMITTED.json").read_bytes())
    env1 = json.loads((inputs / "envelope.json").read_bytes())
    reg = json.loads((inputs / "registration.json").read_bytes())
    a_read = json.loads((inputs / "A-read.stdout").read_bytes())
    latest = a_read["current"]["latest_review"]
    record = json.loads(rb)
    env2 = L.envelope_v2(env1, record["decision"])

    # ---- U1
    def expect_ok(env, rec=rb, com=committed, lat=latest):
        out = L.verify_committed(rec, com, lat, env, reg)
        return {"ok": True, "result": out}

    def expect_refuse(code, env, rec=rb, com=committed, lat=latest):
        try:
            L.verify_committed(rec, com, lat, env, reg)
        except L.Refuse as exc:
            return {"ok": exc.code == code, "expected": code, "observed": exc.code, "detail": exc.detail}
        return {"ok": False, "expected": code, "observed": "accepted"}

    step("U1-real-/2-from-committed-decision", lambda: expect_ok(env2))
    step("U1-real-/1-legacy", lambda: expect_ok(env1))
    tam = deepcopy(env2); tam["supplied_review_state"]["disposition"] = "accepted"
    step("U1-tamper-disposition", lambda: expect_refuse("supplied-state", tam))
    tam2 = deepcopy(env2); tam2["supplied_review_state"]["goal_terminal"] = "completed"
    step("U1-tamper-goal-terminal", lambda: expect_refuse("supplied-state", tam2))
    step("U1-record-bytes-changed", lambda: expect_refuse("record-hash", env2, rec=rb + b" "))
    lat_other = dict(latest, record_sha256="0" * 64)
    step("U1-cycle-names-other-record", lambda: expect_refuse("record-hash", env2, lat=lat_other))
    wrong_id = deepcopy(env2); wrong_id["review_identity"] = "r2"
    step("U1-wrong-review-identity", lambda: expect_refuse("review-identity", wrong_id))
    lat_bind = dict(latest, task_binding_sha256="0" * 64)
    step("U1-wrong-binding", lambda: expect_refuse("binding", env2, lat=lat_bind))
    swapped = deepcopy(env2); swapped["record"] = dict(swapped["record"], gaps=["x"])
    step("U1-envelope-record-swapped", lambda: expect_refuse("envelope-record", swapped))
    retarget = deepcopy(env2); retarget["target"] = "0519.desk-app/05.02.md"
    step("U1-envelope-retargeted", lambda: expect_refuse("envelope-target", retarget))

    # ---- U2: pass04 inspect (read-only) on copied pages outside the checkout
    data = CONSTRUCT.read_bytes()
    pin_ok = (sha(data), len(data)) == CONSTRUCT_PIN
    rows.append({"step": "U2-constructor-pin", "ok": pin_ok, "observed": [sha(data), len(data)]})
    binding = latest["task_binding_sha256"]
    inspected = {}
    for label in ("A-rendered", "B-pending", "D-changed", "E-substantive"):
        page_bytes = (inputs / f"page-{label}.md").read_bytes()
        for nl in ("LF", "CRLF"):
            body = page_bytes if nl == "LF" else page_bytes.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
            root = scratch / f"{label}-{nl}"
            root.mkdir()
            (root / "page.md").write_bytes(body)
            before = sha(body)
            argv = [sys.executable, "-B", str(CONSTRUCT), "inspect", "--fixture-root", str(root), "--target", "page.md", "--binding", binding]
            p = subprocess.run(argv, cwd=str(CHECKOUT), capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            (run / f"inspect-{label}-{nl}.stdout").write_bytes(p.stdout)
            (run / f"inspect-{label}-{nl}.stderr").write_bytes(p.stderr)
            unchanged = sha((root / "page.md").read_bytes()) == before and sorted(x.name for x in root.iterdir()) == ["page.md"]
            res = json.loads(p.stdout) if p.returncode == 0 else None
            inspected[(label, nl)] = res
            rows.append({"step": f"U2-inspect-{label}-{nl}", "ok": p.returncode == 0 and unchanged, "exit": p.returncode,
                         "state": res and res["state"], "binding_found": res and res["binding_sha256"], "writes_none": unchanged, "argv": argv})
    lf_eq_crlf = all((inspected[(l, "LF")] or {}).get("state") == (inspected[(l, "CRLF")] or {}).get("state")
                     for l in ("A-rendered", "B-pending", "D-changed", "E-substantive"))
    rows.append({"step": "U2-inspect-LF-equals-CRLF-state", "ok": lf_eq_crlf})

    def view_of(fname):
        return json.loads((inputs / fname).read_bytes())["view"]

    def expect_mech(label, view, insp, want, check=None):
        got = L.mechanical(view, insp, check)
        rows.append({"step": label, "ok": [got["state"], got["route"]] == want, "expected": want,
                     "observed": [got["state"], got["route"]], "mechanical": got,
                     "supplied_next_action": (view.get("next_action") or {}).get("text"),
                     "mechanical_text_is_not_supplied_text": got["text"] != (view.get("next_action") or {}).get("text")})

    expect_mech("U2-prepare-pending", view_of("A-prepare.stdout"), inspected[("B-pending", "LF")], ["awaiting-review", "record"])
    expect_mech("U2-prepare-substantive", view_of("A-prepare.stdout"), inspected[("E-substantive", "LF")], ["awaiting-review", "record-then-blocked"])
    expect_mech("U2-prepare-absent", view_of("A-prepare.stdout"), {"state": "absent"}, ["awaiting-review", "none-in-this-entry"])
    expect_mech("U2-B-interrupted", view_of("B-read-before.stdout"), inspected[("B-pending", "CRLF")], ["render-interrupted", "recover"])
    expect_mech("U2-D-target-changed", view_of("D-read.stdout"), inspected[("D-changed", "LF")], ["target-changed-since-record", "none-in-this-entry"])
    expect_mech("U2-E-before-render", view_of("E-record.stdout"), inspected[("E-substantive", "LF")], ["render-blocked", "none-in-this-entry"])
    expect_mech("U2-E-conflict", view_of("E-read.stdout"), inspected[("E-substantive", "CRLF")], ["existing-review-conflict", "none-in-this-entry"])
    expect_mech("U2-A-rendered", view_of("A-read.stdout"), inspected[("A-rendered", "LF")], ["rendered", "read"])
    synthetic = deepcopy(view_of("A-read.stdout"))
    synthetic["pass_state"], synthetic["render_state"] = "render-pending", "pending"  # SYNTHETIC: rendered.json removed (v2 test T7)
    expect_mech("U2-SYNTHETIC-marker-missing", synthetic, inspected[("A-rendered", "CRLF")], ["rendered-marker-missing", "none-in-this-entry"])
    expect_mech("U2-record-mismatch", view_of("A-read.stdout"), inspected[("A-rendered", "LF")], ["committed-record-mismatch", "none-in-this-entry"],
                L.Refuse("supplied-state", "SYNTHETIC tamper"))
    expect_mech("U2-unknown", {"pass_state": "weird"}, None, ["unknown-state", "none-in-this-entry"])

    failed = [r["step"] for r in rows if not r.get("ok")]
    summary = {"schema": "0707-0503-probe/1", "run": name, "interpreter": sys.executable, "version": sys.version,
               "steps": len(rows), "failed": failed, "aggregate": "pass" if not failed else "fail", "rows": rows}
    (run / "probe.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(name, summary["aggregate"], len(rows), "steps", "failed:", failed)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
