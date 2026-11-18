"""Blind the outputs of one task across samples for human scoring.

Run: python -I -B tools/blind.py TASK OUT_DIR RUN_DIR [RUN_DIR ...]
Each RUN_DIR holds output.txt and record.json (see RECORD.md). Copies each output.txt to OUT_DIR/<random>.txt
in shuffled order and writes OUT_DIR/../<TASK>-blind-key.json beside OUT_DIR, not inside it. The judge opens
only OUT_DIR. The key maps blind ids back to runs and is opened only after every score sheet is final.
"""
import json
import secrets
import shutil
import sys
from pathlib import Path


def main(argv):
    if len(argv) < 3:
        print(__doc__, file=sys.stderr)
        return 2
    task, out, runs = argv[0], Path(argv[1]), [Path(a) for a in argv[2:]]
    out.mkdir(parents=True, exist_ok=False)
    order = runs[:]
    secrets.SystemRandom().shuffle(order)
    key = {}
    for run in order:
        bid = secrets.token_hex(4)
        shutil.copyfile(run / "output.txt", out / f"{bid}.txt")
        rec = json.loads((run / "record.json").read_text(encoding="utf-8"))
        key[bid] = {"run_dir": str(run), "run_id": rec.get("run_id"), "sample_id": rec.get("sample_id"), "output_sha256": rec.get("output_sha256")}
    (out.parent / f"{task}-blind-key.json").write_text(json.dumps({"task": task, "key": key}, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"{len(key)} outputs blinded into {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
