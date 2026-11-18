#!/usr/bin/env python3
"""review-entry integration lab library (0707/05.18). NONPRODUCTION.

Builds disposable candidate roots with the production layout and runs the REAL on-disk app entry
(<root>/app/librarian.py review-loop ...) in new processes. The live checkout is only READ.

Root layout (each fixture gets its own root, because the lifecycle writes):
  app/*            every top-level file of the live app/ (production bytes, hash recorded), then
  app/librarian.py SELECTED dispatcher: live v7 bytes or the candidate v8 bytes (select())
  app/review_loop_tools_v8.py           candidate door (production proposal bytes)
  app/review-loop-v8.json               LAB declaration (adapter/review-loop-v8.lab.json): pins the adapter pass04
  labs/workbook-review-pass04/workbook.py  LAB ADAPTER bytes (one line differs from the candidate)
  labs/...         every tool the v8 declaration pins (verified against the pin)
  00.kernel/00.00.10.work/<page>/...    the fixture source set (verified, see build_fixture)
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
LAB = LIVE / "labs/review-entry-integration-pass01"
CAND = LAB / "candidate"
ADAPT = LAB / "adapter"
BOOK_REL = "00.kernel/00.00.10.work"
PACK18 = LIVE / BOOK_REL / "0707.app-use-check/evidence/pack05.18"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
N7COMPAT2 = LIVE / "labs/n7-intake-compat-pass02/n7compat2.py"   # the explicit 05.17 root adapter (baseline B)

FIXTURES = {
    "n5-0522": {"page": "0522.review-construction", "pass": "05.13", "pointer": "05.13.md", "kind": "N5NN", "declared": 29},
    "n5-0512": {"page": "0512.prime-review", "pass": "05.06", "pointer": "05.06.md", "kind": "N5NN", "declared": 14},
    "n7-0515": {"page": "0707.app-use-check", "pass": "05.15", "pointer": "05.15.pack.md", "kind": "N7NN", "declared": 26},
    "n7-0517": {"page": "0707.app-use-check", "pass": "05.17", "pointer": "05.17.pack.md", "kind": "N7NN", "declared": 33},
}
N5_LINE = re.compile(r"^(Submission|Artifact manifest): (\S+) sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.")
N7_RET = re.compile(r"^Returned: (\S+) \([^()]*\), sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.$")
N7_MAN = re.compile(r"^Artifact manifest: ([^,\s]+), sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.$")


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha_file(p: Path) -> str:
    return sha(Path(p).read_bytes())


def pack18() -> dict:
    m = json.loads((PACK18 / "source-manifest.json").read_text(encoding="utf-8"))
    return {f["path"]: f for f in m["files"]}


def refuse_inside(p: Path) -> None:
    if str(Path(p).resolve()).lower().startswith(str(LIVE).lower()):
        sys.exit(f"refused: {p} is inside the live checkout")


class Root:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.copied: list[dict] = []

    def put_bytes(self, rel: str, data: bytes, source: str, verified: str):
        dst = self.path / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        self.copied.append({"path": rel, "sha256": sha(data), "bytes": len(data), "source": source, "verified": verified})

    def put_live(self, rel: str, want_sha: str | None = None, want_bytes: int | None = None, verified: str = "hash-recorded"):
        data = (LIVE / rel).read_bytes()
        if want_sha is not None:
            if sha(data) != want_sha or (want_bytes is not None and len(data) != want_bytes):
                raise SystemExit(f"refused: live {rel} does not match its pin")
        self.put_bytes(rel, data, "live", verified)


def build_code(root: Root) -> None:
    """Production app files, the pinned labs, then the candidate overlay with the LAB declaration."""
    for p in sorted((LIVE / "app").iterdir()):
        if p.is_file():
            root.put_live(f"app/{p.name}")
    lab_decl = json.loads((ADAPT / "review-loop-v8.lab.json").read_bytes())
    for name, item in lab_decl["tools"].items():
        if item["path"] == "labs/workbook-review-pass04/workbook.py" or item["path"].startswith("app/"):
            continue
        root.put_live(item["path"], item["sha256"], item["bytes"], "v8-pin")
    root.put_bytes("app/review_loop_tools_v8.py", (CAND / "app/review_loop_tools_v8.py").read_bytes(), "candidate", "candidate")
    root.put_bytes("app/review-loop-v8.json", (ADAPT / "review-loop-v8.lab.json").read_bytes(), "adapter", "adapter")
    root.put_bytes("labs/workbook-review-pass04/workbook.py", (ADAPT / "workbook-pass04.lab.py").read_bytes(), "adapter", "adapter")
    for name, item in lab_decl["tools"].items():         # every pin must hold in the root
        data = (root.path / item["path"]).read_bytes()
        if sha(data) != item["sha256"] or len(data) != item["bytes"]:
            raise SystemExit(f"refused: root pin {name} does not hold")


def select(root: Path, which: str) -> str:
    """Write the selected dispatcher bytes into the root: 'v7' = live production bytes, 'v8' = candidate."""
    src = LIVE / "app/librarian.py" if which == "v7" else CAND / "app/librarian.py"
    data = src.read_bytes()
    (Path(root) / "app/librarian.py").write_bytes(data)
    return sha(data)


def declared_from_pointer(text: str, page_rel: str, kind: str) -> dict:
    """Builder-side only (which files to copy); selected by the fixture's KNOWN kind. The first run of this
    builder tried the N5 pattern first on an N7 page and hit the very comma collision (kept in the notes)."""
    block = text.split("## Return pointer", 1)[1].split("\n## ", 1)[0]
    out = {}
    for line in block.splitlines():
        line = line.strip()
        if kind == "N5NN":
            m = N5_LINE.match(line)
            if m:
                out[m.group(1)] = (m.group(2), m.group(3), int(m.group(4)))
            continue
        m = N7_RET.match(line)
        if m:
            out["Submission"] = (f"{page_rel}/{m.group(1)}", m.group(2), int(m.group(3)))
            continue
        m = N7_MAN.match(line)
        if m:
            out["Artifact manifest"] = (f"{page_rel}/{m.group(1)}", m.group(2), int(m.group(3)))
    return out


def build_fixture(root: Root, key: str, omit: tuple[str, ...] = ()) -> dict:
    """The source set: page top-level .md (pack05.18 snapshot when frozen, else live with hash recorded),
    the declared submission and manifest (verified against the pointer), every manifest row (verified)."""
    fx = FIXTURES[key]
    page_rel = f"{BOOK_REL}/{fx['page']}"
    frozen = pack18()
    for p in sorted((LIVE / page_rel).glob("*.md")):
        if p.name.startswith(("05.18.", "06.18.")) or p.name in omit:
            continue                                     # this pass's own files are not source data
        rel = f"{page_rel}/{p.name}"
        if rel in frozen:
            data = (PACK18 / frozen[rel]["snapshot"]).read_bytes()
            if sha(data) != frozen[rel]["sha256"]:
                raise SystemExit(f"refused: snapshot {rel}")
            root.put_bytes(rel, data, "pack05.18-snapshot", "pack05.18")
        else:
            root.put_live(rel)
    pointer = (root.path / page_rel / fx["pointer"]).read_text(encoding="utf-8")
    declared = declared_from_pointer(pointer, page_rel, fx["kind"])
    for role in ("Submission", "Artifact manifest"):
        rel, h, n = declared[role]
        if not (root.path / rel).exists():
            root.put_live(rel, h, n, "pointer")
        elif sha_file(root.path / rel) != h:
            raise SystemExit(f"refused: declared {role} differs")
    man = json.loads((root.path / declared["Artifact manifest"][0]).read_bytes())
    for row in man["files"]:
        if not (root.path / row["path"]).exists():
            root.put_live(row["path"], row["sha256"], row["bytes"], "manifest-row")
        elif sha_file(root.path / row["path"]) != row["sha256"]:
            raise SystemExit(f"refused: manifest row {row['path']} differs in the root")
    return {"declared": {k: list(v) for k, v in declared.items()}, "manifest_rows": [r["path"] for r in man["files"]],
            "manifest_sha": {r["path"]: r["sha256"] for r in man["files"]}}


def make_root(path: Path, key: str, omit: tuple[str, ...] = (), dispatcher: str = "v8") -> tuple[Root, dict]:
    refuse_inside(path)
    path.mkdir(parents=True, exist_ok=False)
    r = Root(path)
    build_code(r)
    info = build_fixture(r, key, omit)
    info["dispatcher_sha"] = select(path, dispatcher)
    (path / "ROOT-INDEX.json").write_text(json.dumps({"schema": "rie-root/1", "fixture": key, "omit": list(omit), "copied": r.copied,
                                                      "declared": info["declared"]}, indent=1) + "\n", encoding="utf-8")
    return r, info


def run(argv: list, cwd: Path, timeout=600) -> dict:
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, env=ENV, timeout=timeout, cwd=str(cwd))
    try:
        body = json.loads(p.stdout.decode("utf-8"))
    except Exception:
        body = None
    return {"argv": [str(x) for x in argv], "exit": p.returncode, "stdout": p.stdout.decode("utf-8", "replace"),
            "stderr": p.stderr.decode("utf-8", "replace"), "body": body}


def app(root: Path, *args) -> dict:
    """The REAL on-disk entry of the root: <root>/app/librarian.py review-loop ..."""
    return run([Path(root) / "app/librarian.py", "review-loop", *args], cwd=Path(root))


def baseline(root: Path, *args) -> dict:
    """Faithful v7 baseline: pinned pass03 via the explicit 05.17 root adapter (no grammar patch)."""
    return run([N7COMPAT2, "--repo-root", Path(root), *args], cwd=Path(root))


def wb_args(root: Path, key: str, cmd: str, *extra) -> list:
    fx = FIXTURES[key]
    return [cmd, "--book", str(Path(root) / BOOK_REL), "--source", fx["page"], "--pass", fx["pass"], *extra]


def rows_of(body) -> list:
    if not isinstance(body, dict):
        return []
    form = body.get("form") if isinstance(body.get("form"), dict) else body
    rows = ((form or {}).get("bindings") or {}).get("rows")
    return rows if isinstance(rows, list) else []


def summary(res: dict) -> dict:
    b = res.get("body") if isinstance(res.get("body"), dict) else {}
    rows = rows_of(b)
    return {"exit": res["exit"], "intake_id": b.get("intake_id"), "measurement": b.get("measurement"), "kind": b.get("kind"),
            "destination": b.get("destination"), "custody": b.get("custody"), "stale": b.get("stale"),
            "finding_codes": sorted(f.get("code") for f in b.get("findings") or [] if isinstance(f, dict)),
            "row_count": len(rows), "rows_sha": sha(json.dumps(sorted(json.dumps(r, sort_keys=True) for r in rows)).encode()),
            "cuts_sha": sha(json.dumps(b.get("cuts"), sort_keys=True).encode()), "stderr_tail": res["stderr"][-240:]}


def tree_hashes(root: Path, sub: str = BOOK_REL) -> dict:
    base = Path(root) / sub
    return {str(p.relative_to(base)).replace("\\", "/"): sha_file(p) for p in sorted(base.rglob("*")) if p.is_file()}


def save(res: dict, ev: Path, name: str) -> None:
    ev.mkdir(parents=True, exist_ok=True)
    (ev / f"{name}.stdout").write_text(res["stdout"], encoding="utf-8")
    (ev / f"{name}.stderr").write_text(res["stderr"], encoding="utf-8")
    (ev / f"{name}.argv.json").write_text(json.dumps({"argv": res["argv"], "exit": res["exit"]}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--room", required=True)
    ap.add_argument("--fixture", required=True, choices=sorted(FIXTURES))
    ap.add_argument("--omit", action="append", default=[])
    ap.add_argument("--dispatcher", default="v8", choices=("v7", "v8"))
    a = ap.parse_args()
    r, info = make_root(Path(a.room), a.fixture, tuple(a.omit), a.dispatcher)
    print(json.dumps({"root": a.room, "files": len(r.copied), "declared": info["declared"]}))
