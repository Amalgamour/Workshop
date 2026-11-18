#!/usr/bin/env python3
"""0709 pass02: active return-writer probes on disposable books (NONPRODUCTION).

H1 the unchanged sequential helper reserves in a line-pass-declared book.
H2 the unchanged helper capture (the app handoff backend) on a line-pass submission.
H3 the unchanged legacy readers on a line page.
Every tool runs unchanged as a subprocess after a pack05.02 pin check. Live is not touched.
usage: probe_writers.py --root ABS(new, outside checkout) --evidence ABS(new)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CHECKOUT = Path(r"D:\Git\lib-build")
PACK = CHECKOUT / "00.kernel/00.00.10.work/0709.return-migration-check/evidence/pack05.02/source-manifest.json"
RL = "labs/return-lines-pass01/return_lines.py"
RC = "labs/return-capture-pass01/return_capture.py"
RI = "labs/return-capture-pass01/return_inspect.py"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def tree(root: Path) -> dict:
    return {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in sorted(root.rglob("*")) if p.is_file()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--evidence", required=True)
    a = ap.parse_args()
    root, ev = Path(a.root), Path(a.evidence)
    if str(root).lower().startswith(str(CHECKOUT).lower()):
        raise SystemExit("refused: fixture root inside the checkout")
    root.mkdir(parents=True, exist_ok=False)
    ev.mkdir(parents=True, exist_ok=False)
    pins = {r["path"]: r for r in json.loads(PACK.read_text(encoding="utf-8"))["files"]}
    for rel in (RL, RC, RI):
        b = (CHECKOUT / rel).read_bytes()
        if (sha(b), len(b)) != (pins[rel]["sha256"], pins[rel]["bytes"]):
            raise SystemExit(f"refused: {rel} differs from its pack05.02 pin")
    steps = []

    def run(label: str, tool: str, args: list[str]) -> subprocess.CompletedProcess:
        argv = [sys.executable, "-B", str(CHECKOUT / tool), *args]
        p = subprocess.run(argv, cwd=str(CHECKOUT), capture_output=True, timeout=120, env=ENV)
        (ev / f"{label}.stdout").write_bytes(p.stdout)
        (ev / f"{label}.stderr").write_bytes(p.stderr)
        steps.append({"label": label, "argv": argv, "exit": p.returncode,
                      "stdout": p.stdout.decode("utf-8", "replace")[-1500:], "stderr": p.stderr.decode("utf-8", "replace")[-800:]})
        return p

    src = root / "src"
    src.mkdir()
    (src / "return.md").write_bytes(b"SYNTHETIC RETURN 0709/05.02 probe\n")
    (src / "note.md").write_bytes(b"SYNTHETIC NOTE\n")

    # H1
    b1 = root / "h1-book"
    b1.mkdir()
    run("h1-01-line-init", RL, ["init", "--book", str(b1), "--name", "00.00.10.work"])
    layout_before = (b1 / "return-line-layout.json").exists()
    run("h1-02-helper-reserve", RC, ["reserve", "--book", str(b1), "--submission", "probe-h1-helper", "--name", "alpha-0501",
                                     "--origin-book", "00.00.10.work", "--origin-page", "0501.alpha", "--origin-batch", "05.01",
                                     "--submitter", "probe", "--reviewer", "probe", "--release", "SYNTHETIC probe"])
    after_helper = sorted(e.name for e in b1.iterdir())
    run("h1-03-line-reserve", RL, ["reserve", "--book", str(b1), "--page", "0501.alpha", "--batch", "05.02",
                                   "--submission", "probe-h1-line", "--submitter", "probe", "--reviewer", "probe", "--release", "SYNTHETIC probe"])
    h1 = {"layout_declared_before_helper": layout_before, "book_after_helper": after_helper,
          "door_created_by_helper": (b1 / "0100.band.returns").is_dir(), "book_tree_end": tree(b1)}

    # H2 / H3
    b2 = root / "h2-book"
    b2.mkdir()
    run("h2-01-line-init", RL, ["init", "--book", str(b2), "--name", "00.00.10.work"])
    run("h2-02-line-reserve", RL, ["reserve", "--book", str(b2), "--page", "0504.app-entry", "--batch", "05.21",
                                   "--submission", "probe-h2-line", "--output", "note.md", "--submitter", "probe",
                                   "--reviewer", "probe", "--release", "SYNTHETIC probe"])
    run("h2-03-line-capture", RL, ["capture", "--book", str(b2), "--page", "0504.app-entry", "--batch", "05.21",
                                   "--submission", "probe-h2-line", "--return-file", str(src / "return.md"),
                                   "--artifact", "note.md", str(src / "note.md")])
    before = tree(b2)
    run("h2-04-helper-capture", RC, ["capture", "--book", str(b2), "--submission", "probe-h2-line",
                                     "--return-file", str(src / "return.md"), "--source-root", str(src)])
    run("h3-01-helper-verify-line", RC, ["verify", "--book", str(b2), "--member", "0104.app-entry"])
    run("h3-02-inspect-line", RI, ["inspect", "--book", str(b2), "--member", "0104.app-entry", "--json"])
    h2 = {"book_dirs": sorted(e.name for e in b2.iterdir()), "tree_unchanged_by_helper": before == tree(b2)}

    body = {"schema": "0709-writer-probe/1", "root": str(root), "steps": steps, "h1": h1, "h2": h2}
    (ev / "probe.json").write_text(json.dumps(body, indent=2) + "\n", encoding="utf-8")
    for s in steps:
        print(s["label"], "exit", s["exit"], "|", (s["stdout"] or s["stderr"]).strip().replace("\n", " / ")[:260])
    print("H1", json.dumps({k: v for k, v in h1.items() if k != "book_tree_end"}))
    print("H2", json.dumps(h2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
