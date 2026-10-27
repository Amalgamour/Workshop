"""Pinned historical and current checks, read-only, with a checkout fingerprint before and after.
python -B -W error demos.py <lab-copy> <repo> <out-dir>"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

LAB, REPO, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS="0", PYTHONDONTWRITEBYTECODE="1")


def fingerprint():
    g = lambda *a: subprocess.run(["git", "-C", str(REPO), *a], env=ENV, capture_output=True, check=True).stdout
    return {"head": g("rev-parse", "HEAD").decode().strip(),
            "index_sha256": hashlib.sha256((REPO / ".git" / "index").read_bytes()).hexdigest(),
            "status_sha256": hashlib.sha256(g("status", "--porcelain=v1", "-uall")).hexdigest(),
            "refs_sha256": hashlib.sha256(g("for-each-ref", "--format=%(refname) %(objectname)")).hexdigest()}


RUNS = [("a5853b7-selected", "a5853b7", []),
        ("a5853b7-candidate-01.002", "a5853b7", ["--contents", "0011.contents/01.002.md"]),
        ("15b9cceb-selected", "15b9cceb3438b8a91acfd8d3155b9b0d5fce29ae", []),
        ("head-d3bcdab-selected", "d3bcdabd431bd0ca2bd5250da46f69b79879de89", [])]
before = fingerprint()
summary = []
for name, rev, extra in RUNS:
    r = subprocess.run([sys.executable, "-B", "-W", "error", str(LAB / "check_book.py"), "--root", str(REPO),
                        "--revision", rev, "--book", "00.kernel/00.00.10.work", "--json", *extra],
                       cwd=str(OUT), env=ENV, capture_output=True, timeout=120)
    (OUT / f"demo-{name}.json").write_bytes(r.stdout)
    rep = json.loads(r.stdout)
    line = {"run": name, "exit": r.returncode, "stderr": r.stderr.decode(), "commit": rep.get("commit"),
            "contents": rep.get("contents_path"), "contents_sha256": rep.get("contents_sha256"),
            "other_books": rep.get("counts", {}).get("other_books"),
            "findings": [f"{f['kind']} {f.get('item', '')}".strip() for f in rep.get("findings", [])]}
    summary.append(line)
    print(json.dumps(line))
after = fingerprint()
result = {"before": before, "after": after, "unchanged": before == after, "runs": summary}
(OUT / "demos-summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print("checkout unchanged:", before == after)
