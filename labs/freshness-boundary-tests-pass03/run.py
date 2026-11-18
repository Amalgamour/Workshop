#!/usr/bin/env python3
"""Freshness-boundary tests, execution-proof v2 adapter (0707/05.25). NONPRODUCTION.

Cases (34; 32 required), fixtures, judges and expectations: the UNCHANGED hash-pinned
labs/freshness-boundary-tests-pass01/run.py + judges.py (pack05.25 freeze). Replaced ONLY:
  1. identity: identity3.resolve (explicit harness-inputs/3 or labelled legacy for the two baselines; door fields);
  2. the gate before any case: identity3.execution_proof for the declared workbook, open entry and reporter.
     Only class 'executed' (audit-traced run/exec of the declared file by the probe command) passes; every other
     class refuses (exit 2) and is reported by name.
usage: run.py --candidate ROOT --identity INPUTS.json --rooms NEW-DIR --out RESULT.json [--cases ID,ID]
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
LIVE = Path(r"D:\Git\lib-build")
PACK25 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.25/source-manifest.json"
P1 = "labs/freshness-boundary-tests-pass01"
sys.path.insert(0, str(HERE))
import identity3 as I  # noqa: E402


def load_pass01():
    rows = {r["path"]: r for r in json.loads(PACK25.read_bytes())["files"]}
    for rel in (f"{P1}/run.py", f"{P1}/judges.py"):
        if hashlib.sha256((LIVE / rel).read_bytes()).hexdigest() != rows[rel]["sha256"]:
            raise SystemExit(f"refused: {rel} differs from its pack05.25 freeze")
    spec = importlib.util.spec_from_file_location("fbt_pass01_run", LIVE / P1 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fbt_pass01_run"] = mod
    spec.loader.exec_module(mod)
    return mod


R1 = load_pass01()
STATE = {}


def probes(R, ident):
    def wb(root, env):
        R.n5_book(root, "0587.fbt-probe")
        return I.run([root / ident["entry"], "review-loop", "prepare", "--book", root / R.BOOK, "--source", "0587.fbt-probe", "--pass", "05.01"], root, env)

    def op(root, env):
        R.write(root / R.BOOK / "0787.fbt-probe/05.01.pack.md", R.pack_text("normal").replace("POINTER-SLOT", "PENDING."))
        return I.run([root / ident["open_entry"], "open", "--book", root / R.BOOK, "--source", "0787.fbt-probe", "--pass", "05.01"], root, env)

    def rp(root, env):
        R.n5_book(root, "0587.fbt-probe")
        return I.run([root / ident["entry"], "review-report", "--book", root / R.BOOK, "--source", "0587.fbt-probe", "--pass", "05.01"], root, env)
    return {"workbook": wb, "open": op, "reporter": rp}


def gate(ident: dict, cand: Path, proof_rooms: Path) -> dict:
    p = probes(R1, ident)
    proof_rooms.mkdir(parents=True, exist_ok=False)
    out = {}
    for role, key in (("workbook", "workbook_entry"), ("open", "open_entry"), ("reporter", "reporter_entry")):
        tgt = ident.get(key)
        if tgt is None:
            continue
        out[role] = I.execution_proof(cand, ident, tgt, p[role], proof_rooms, role)
        if role == "open" and out[role].get("control", {}).get("exit") != 0:
            raise I.Refused(f"declared open entry {tgt} is not executable on a new root (control exit {out[role].get('control', {}).get('exit')})")
        if not out[role]["executed"]:
            raise I.Refused(f"declared {role} {tgt}: proof class '{out[role]['class']}' (only 'executed' passes)")
    return out


def verify(identity_doc, root: Path) -> dict:
    try:
        ident = I.resolve(identity_doc, root, R1.load_inputs_check().shape_problems)
        I.I2.verify_dependencies(identity_doc)
        STATE["ident"] = ident
        STATE["proof"] = gate(ident, root, STATE["proof_rooms"])
    except I.Refused as exc:
        STATE["refused"] = str(exc)
        raise R1.Refused(str(exc))
    R1.ENTRY = ident["entry"]
    return {"kind": ident["kind"], "candidate_json_sha256": ident["candidate_json_sha256"], "open_entry": ident["open_entry"], "files": ident["files"]}


def main() -> int:
    args = sys.argv[1:]
    out = Path(args[args.index("--out") + 1])
    rooms = Path(args[args.index("--rooms") + 1])
    STATE["proof_rooms"] = rooms.with_name(rooms.name + "-proof")
    R1.verify = verify
    code = R1.main()
    doc = json.loads(out.read_text(encoding="utf-8"))
    ident = STATE.get("ident") or {}
    doc.update({"adapter": "freshness-boundary-tests-pass03 (0707/05.25): cases/judges/expectations = pinned pass01; proof v2",
                "identity_mode": ident.get("mode"), "workbook_entry": ident.get("workbook_entry"),
                "execution_proof": STATE.get("proof"), "identity_refusal": STATE.get("refused")})
    out.write_text(json.dumps(doc, indent=1, default=str) + "\n", encoding="utf-8")
    print("identity:", ident.get("mode"), ident.get("workbook_entry"), "| proof:", {k: v["class"] for k, v in (STATE.get("proof") or {}).items()})
    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(3)
