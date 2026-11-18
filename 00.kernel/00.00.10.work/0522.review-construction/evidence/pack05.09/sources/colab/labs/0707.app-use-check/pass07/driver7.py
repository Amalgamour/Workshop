#!/usr/bin/env python3
"""0707/05.08 pass07: NONPRODUCTION driver for the SUPPLEMENTAL two-case matrix.

usage: driver7.py preflight --config ABS
       driver7.py run --config ABS --evidence ABS

Uses the pinned pass06 harness unchanged. In memory only, it replaces the harness's
matrix loader so that the real-candidate run executes cases7 (A22a, A22b) instead of
pass04's 33 cases; pass04 cases/fixtures are still hash-checked and the fixture
guard still applies. Writes SUPPLEMENT.json into the run directory: this is NOT the
original 33-case matrix and its aggregate is separate.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PASS06 = HERE.parent / "pass06"
CHECKOUT = Path(r"D:\Git\lib-build")
PACK = CHECKOUT / "00.kernel" / "00.00.10.work" / "0707.app-use-check" / "evidence" / "pack05.08" / "source-manifest.json"
PINNED = ["colab/labs/0707.app-use-check/pass06/harness6.py", "colab/labs/0707.app-use-check/pass06/guards6.py",
          "colab/labs/0707.app-use-check/pass04/cases.py", "colab/labs/0707.app-use-check/pass04/fixtures.py"]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def check_pins() -> dict:
    pins = {r["path"]: r for r in json.loads(PACK.read_text(encoding="utf-8"))["files"]}
    out = {}
    for rel in PINNED:
        got = sha((CHECKOUT / rel).read_bytes())
        if got != pins[rel]["sha256"]:
            raise SystemExit(f"refused: {rel} differs from its pack05.08 pin")
        out[rel] = got
    return out


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    baseline = check_pins()
    sys.path.insert(0, str(HERE))
    sys.path.insert(1, str(PASS06))
    H = importlib.import_module("harness6")
    if args[:1] == ["preflight"] and len(args) == 3 and args[1] == "--config":
        return H.main(["preflight", "--config", args[2]])
    if not (args[:1] == ["run"] and len(args) == 5 and args[1] == "--config" and args[3] == "--evidence"):
        print(__doc__, file=sys.stderr)
        return 2
    original = H.load_pass04
    supplemental = {"cases7.py": sha((HERE / "cases7.py").read_bytes()), "driver7.py": sha((HERE / "driver7.py").read_bytes())}

    def load_supplemental():
        _cases, fixtures, prov = original()  # hash-checks pass04 cases/fixtures and installs the fixture guard
        module = importlib.import_module("cases7")
        return module, fixtures, dict(prov, **{f"colab/labs/0707.app-use-check/pass07/{k}": v for k, v in supplemental.items()})

    H.load_pass04 = load_supplemental
    code, summary = H.run_matrix(args[2], "real", args[4])
    if summary.get("run"):
        run_dir = Path(summary["canonical_paths"]["run_dir"])
        record = {
            "schema": "0707-supplemental-run/1",
            "statement": "SUPPLEMENTAL two-case run (A22a, A22b). NOT the original 33-case matrix; its aggregate is separate from 0707/05.07's FAIL.",
            "matrix_identity": "0707-supplemental-a22/1",
            "cases": [r["id"] for r in summary["cases"]],
            "supplemental_sources": supplemental,
            "reused_baseline_pins": baseline,
            "harness_summary_matrix_field": summary["matrix"],
            "note": "harness6 labels the run 'real' because it uses the real candidate config; the driver replaced only the matrix loader, in memory",
            "full_command": [sys.executable, "-I", "-B", str(HERE / "driver7.py"), *args],
            "aggregate": summary["aggregate"], "exit": code,
        }
        (run_dir / "SUPPLEMENT.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    print(summary.get("run"), summary["aggregate"], f"exit {code}", *summary.get("reasons", []))
    return code


if __name__ == "__main__":
    sys.exit(main())
