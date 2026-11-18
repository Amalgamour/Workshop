#!/usr/bin/env python3
"""Faithful N5 replay of the real 0522/05.13 return on a disposable copy (0707/05.17 lab).

The copy root has the production layout: the v7-pinned code (verified against the v7 pins), every top-level
.md of 0522.review-construction (hash recorded; 05.13.md verified against its live hash taken at run start),
the declared submission and manifest (verified against the 05.13 pointer), and the 29 manifest rows (verified
against the manifest). The live checkout is only READ.

Runs, each a NEW process, on the SAME copy (intake_id includes the book path):
  A  actual app entry: app/librarian.py review-loop prepare (code root = live, read only; book = copy)
  U1 unpatched pass03 (n7compat2 without --patch), code root = copy
  P  patched pass02 (n7compat2 --patch), code root = copy
  U2 unpatched again (detects any state drift caused by the runs)
Compares intake_id, measurement, binding rows, finding codes, cuts; hashes every copied file before and after.
usage: n5_replay.py --room NEW-DIR (outside the checkout) --out FILE
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
LAB = LIVE / "labs/n7-intake-compat-pass02"
BOOK_REL = "00.kernel/00.00.10.work"
PAGE = f"{BOOK_REL}/0522.review-construction"
SRC, PASS = "0522.review-construction", "05.13"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
LINE = re.compile(r"^(Submission|Artifact manifest): (\S+) sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--room", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    room = Path(a.room)
    if str(room.resolve()).lower().startswith(str(LIVE).lower()):
        sys.exit("refused: room inside the checkout")
    repo = room / "repo"
    repo.mkdir(parents=True, exist_ok=False)
    copied = []

    def put(rel, want_sha=None, want_bytes=None):
        data = (LIVE / rel).read_bytes()
        if want_sha is not None and (sha(data) != want_sha or (want_bytes is not None and len(data) != want_bytes)):
            raise SystemExit(f"refused: {rel} does not match its pin")
        dst = repo / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        copied.append({"path": rel, "sha256": sha(data), "bytes": len(data), "verified": want_sha is not None})

    v7 = json.loads((LIVE / "app/review-loop-v7.json").read_bytes())
    put("app/review-loop-v7.json")
    for item in v7["tools"].values():
        put(item["path"], item["sha256"], item["bytes"])
    pack_md = (LIVE / PAGE / "05.13.md").read_bytes()
    for p in sorted((LIVE / PAGE).glob("*.md")):
        put(f"{PAGE}/{p.name}")
    declared = {}
    block = pack_md.decode("utf-8").split("## Return pointer", 1)[1].split("\n## ", 1)[0]
    for line in block.splitlines():
        m = LINE.match(line.strip())
        if m:
            declared[m.group(1)] = (m.group(2), m.group(3), int(m.group(4)))
    for role in ("Submission", "Artifact manifest"):
        put(*declared[role])
    man = json.loads((LIVE / declared["Artifact manifest"][0]).read_bytes())
    for row in man["files"]:
        if not (repo / row["path"]).exists():
            put(row["path"], row["sha256"], row["bytes"])
    before = {c["path"]: sha((repo / c["path"]).read_bytes()) for c in copied}
    tree_before = sorted(str(p.relative_to(repo)).replace("\\", "/") for p in repo.rglob("*") if p.is_file())

    book = repo / BOOK_REL
    runs = {}

    def run(name, argv):
        p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, timeout=600, env=ENV, cwd=str(LIVE))
        (room / f"{name}.stdout").write_bytes(p.stdout)
        (room / f"{name}.stderr").write_bytes(p.stderr)
        body = json.loads(p.stdout.decode("utf-8")) if p.stdout.strip() else {}
        rows = sorted(json.dumps(r, sort_keys=True) for r in ((body.get("form") or {}).get("bindings") or {}).get("rows") or [])
        runs[name] = {"argv": [str(x) for x in argv], "exit": p.returncode, "intake_id": body.get("intake_id"), "measurement": body.get("measurement"),
                      "kind": body.get("kind"), "destination": body.get("destination"), "custody": body.get("custody"),
                      "finding_codes": sorted(f.get("code") for f in body.get("findings") or []),
                      "rows_sha": sha("\n".join(rows).encode()), "row_count": len(rows),
                      "roles": sorted({json.loads(r).get("role") for r in rows}),
                      "submission_path": next((json.loads(r).get("path") for r in rows if json.loads(r).get("role") == "submission"), None),
                      "manifest_path": next((json.loads(r).get("path") for r in rows if json.loads(r).get("role") == "artifact-manifest"), None),
                      "cuts_sha": sha(json.dumps(body.get("cuts"), sort_keys=True).encode()),
                      "stderr_tail": p.stderr.decode("utf-8", "replace")[-200:]}
        print(name, json.dumps({k: runs[name][k] for k in ("exit", "intake_id", "measurement", "row_count", "finding_codes")})[:300])

    common = ["prepare", "--book", book, "--source", SRC, "--pass", PASS]
    run("A-app", [LIVE / "app/librarian.py", "review-loop", *common])
    run("U1-unpatched", [LAB / "n7compat2.py", "--repo-root", repo, *common])
    run("P-patched", [LAB / "n7compat2.py", "--patch", "--repo-root", repo, *common])
    run("U2-unpatched", [LAB / "n7compat2.py", "--repo-root", repo, *common])

    after = {c["path"]: sha((repo / c["path"]).read_bytes()) for c in copied}
    tree_after = sorted(str(p.relative_to(repo)).replace("\\", "/") for p in repo.rglob("*") if p.is_file())
    keys = ("exit", "intake_id", "measurement", "kind", "destination", "custody", "finding_codes", "rows_sha", "row_count", "cuts_sha")
    diffs = {k: {n: runs[n][k] for n in runs} for k in keys if len({json.dumps(runs[n][k]) for n in ("U1-unpatched", "P-patched", "U2-unpatched")}) > 1}
    result = {"schema": "n5-replay/1", "room": str(room), "source": f"{SRC} {PASS}", "pack_md_sha256": sha(pack_md), "declared": declared,
              "manifest_rows": len(man["files"]), "copied": len(copied), "runs": runs,
              "unpatched_vs_patched_identical": not diffs, "differences": diffs,
              "app_vs_unpatched_intake_id_equal": runs["A-app"]["intake_id"] == runs["U1-unpatched"]["intake_id"],
              "copied_bytes_unchanged": before == after, "files_added_by_runs": sorted(set(tree_after) - set(tree_before))}
    Path(a.out).write_text(json.dumps(result, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print("identical:", result["unpatched_vs_patched_identical"], "app==U1 id:", result["app_vs_unpatched_intake_id_equal"],
          "bytes unchanged:", result["copied_bytes_unchanged"], "added:", len(result["files_added_by_runs"]))
    return 0 if result["unpatched_vs_patched_identical"] and result["copied_bytes_unchanged"] else 1


if __name__ == "__main__":
    sys.exit(main())
