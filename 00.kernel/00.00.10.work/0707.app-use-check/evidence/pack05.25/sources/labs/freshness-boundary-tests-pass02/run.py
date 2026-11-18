#!/usr/bin/env python3
"""Freshness-boundary tests, explicit-identity adapter (0707/05.24). NONPRODUCTION.

The 34 cases (32 required), fixtures, judges and expectations are the UNCHANGED, hash-pinned
labs/freshness-boundary-tests-pass01/run.py + judges.py (pack05.24 freeze). This adapter replaces ONLY:
  1. identity resolution: identity.resolve() (harness-inputs/3 explicit, or labelled legacy for the two baselines);
  2. an execution-proof gate BEFORE any case: controlled tamper of the declared workbook (and open/reporter entries
     when declared) in NEW disposable copies; a DECOY or a non-executable open entry refuses (exit 2).
usage: run.py --candidate ROOT --identity INPUTS.json --rooms NEW-DIR --out RESULT.json [--cases ID,ID]
exit: as pass01 (0 every required case passed, full run only; 1 otherwise; 2 refused; 3 crash)
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
PACK24 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.24/source-manifest.json"
P1 = "labs/freshness-boundary-tests-pass01"
sys.path.insert(0, str(HERE))
import identity as I  # noqa: E402


def load_pass01():
    rows = {r["path"]: r for r in json.loads(PACK24.read_bytes())["files"]}
    for rel in (f"{P1}/run.py", f"{P1}/judges.py"):
        if hashlib.sha256((LIVE / rel).read_bytes()).hexdigest() != rows[rel]["sha256"]:
            raise SystemExit(f"refused: {rel} differs from its pack05.24 freeze")
    spec = importlib.util.spec_from_file_location("fbt_pass01_run", LIVE / P1 / "run.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fbt_pass01_run"] = mod
    spec.loader.exec_module(mod)
    return mod


R1 = load_pass01()
STATE = {}


def probes(R, ident):
    def wb(root):
        R.n5_book(root, "0587.fbt-probe")
        return R.run([root / ident["entry"], "review-loop", "prepare", "--book", root / R.BOOK, "--source", "0587.fbt-probe", "--pass", "05.01"], root)

    def op(root):
        pd = root / R.BOOK / "0787.fbt-probe"
        R.write(pd / "05.01.pack.md", R.pack_text("normal").replace("POINTER-SLOT", "PENDING."))
        return R.run([root / ident["open_entry"], "open", "--book", root / R.BOOK, "--source", "0787.fbt-probe", "--pass", "05.01"], root)

    def rp(root):
        R.n5_book(root, "0587.fbt-probe")
        return R.run([root / ident["entry"], "review-report", "--book", root / R.BOOK, "--source", "0587.fbt-probe", "--pass", "05.01"], root)
    return wb, op, rp


def gate(ident: dict, cand: Path, proof_rooms: Path) -> dict:
    wb, op, rp = probes(R1, ident)
    proof_rooms.mkdir(parents=True, exist_ok=False)
    out = {"workbook": I.tamper_proof(cand, ident, ident["workbook_entry"], wb, proof_rooms, "workbook")}
    if not out["workbook"]["executed"]:
        raise I.Refused(f"declared workbook {ident['workbook_entry']}: {out['workbook']['verdict']} - {out['workbook']['evidence']}")
    if ident.get("open_entry"):
        out["open"] = I.tamper_proof(cand, ident, ident["open_entry"], op, proof_rooms, "open")
        if out["open"]["control"]["exit"] != 0:
            raise I.Refused(f"declared open entry {ident['open_entry']} is not executable on a new root (control exit {out['open']['control']['exit']})")
        if not out["open"]["executed"]:
            raise I.Refused(f"declared open entry {ident['open_entry']}: {out['open']['verdict']}")
    if ident.get("reporter_entry"):
        out["reporter"] = I.tamper_proof(cand, ident, ident["reporter_entry"], rp, proof_rooms, "reporter")
        if not out["reporter"]["executed"]:
            raise I.Refused(f"declared reporter entry {ident['reporter_entry']}: {out['reporter']['verdict']}")
    return out


def verify(identity_doc, root: Path) -> dict:
    try:
        ident = I.resolve(identity_doc, root, R1.load_inputs_check().shape_problems)
        I.verify_dependencies(identity_doc)
        STATE["ident"] = ident
        STATE["proof"] = gate(ident, root, STATE["proof_rooms"])
    except I.Refused as exc:
        STATE["refused"] = str(exc)
        raise R1.Refused(str(exc))
    R1.ENTRY = ident["entry"]
    return {"kind": ident["kind"], "candidate_json_sha256": ident["candidate_json_sha256"], "open_entry": ident["open_entry"],
            "files": ident["files"]}


def main() -> int:
    args = sys.argv[1:]
    out = Path(args[args.index("--out") + 1])
    rooms = Path(args[args.index("--rooms") + 1])
    STATE["proof_rooms"] = rooms.with_name(rooms.name + "-proof")
    R1.verify = verify
    code = R1.main()
    doc = json.loads(out.read_text(encoding="utf-8"))
    ident = STATE.get("ident") or {}
    doc.update({"adapter": "freshness-boundary-tests-pass02 (0707/05.24): cases/judges/expectations = pinned pass01",
                "identity_mode": ident.get("mode"), "workbook_entry": ident.get("workbook_entry"),
                "execution_proof": STATE.get("proof"), "identity_refusal": STATE.get("refused")})
    out.write_text(json.dumps(doc, indent=1, default=str) + "\n", encoding="utf-8")
    print("identity:", ident.get("mode"), ident.get("workbook_entry"), "| proof:",
          {k: v["verdict"] for k, v in (STATE.get("proof") or {}).items()})
    return code


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        sys.exit(3)
