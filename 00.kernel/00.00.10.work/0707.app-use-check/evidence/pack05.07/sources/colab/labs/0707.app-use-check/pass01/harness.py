#!/usr/bin/env python3
"""0707 pass01: a thin recorder for walking the app's review-loop operator path.

It runs only `python -B app/librarian.py review-loop ...` in D:\\Git\\lib-build,
one subprocess per call, after a byte guard on the app door and the pinned tools.
It keeps raw stdout/stderr/exit/argv. It does not build judgments or interpret
results. Disposable books live outside the checkout. Lab code, not product code.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

CHECKOUT = Path(r"D:\Git\lib-build")
LIVE_BOOK = CHECKOUT / "00.kernel" / "00.00.10.work"
PAGE = LIVE_BOOK / "0707.app-use-check"
PACK = PAGE / "evidence" / "pack05.01"
EVIDENCE = PAGE / "evidence" / "build05.01"
LAB = Path(__file__).resolve().parent
BOOKS = Path(r"C:\Users\misg\AppData\Local\Temp\claude\D--Git-Librarian\313e7ce7-27d2-405b-881d-6a16a47199dc\scratchpad\0707-books")
MEMBER = "0182.desk-app-integration-design-0501"
GUARDED = [
    "app/librarian.py",
    "app/review_loop_tools_v2.py",
    "app/review-loop-v2.json",
    "labs/review-loop-pass02/review_loop.py",
    "labs/prime-cycle-pass03/prime_cycle.py",
    "labs/review-construction-pass02/construct.py",
    "labs/prime-review-pass01/prime_review.py",
    "labs/prime-review-pass02/prime_review.py",
    "labs/return-lines-pass01/return_lines.py",
    "labs/return-placement-pass01/return_placement.py",
    "labs/return-capture-pass01/return_inspect.py",
]

sys.dont_write_bytecode = True


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(payload) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def manifest() -> dict:
    body = json.loads((PACK / "source-manifest.json").read_text(encoding="utf-8"))
    return {row["path"]: row for row in body["files"]}


def inside(child: Path, parent: Path) -> bool:
    c = os.path.normcase(os.path.abspath(child))
    p = os.path.normcase(os.path.abspath(parent))
    return c == p or c.startswith(p.rstrip(os.sep) + os.sep)


def guard() -> dict:
    pins = manifest()
    rows = []
    for rel in GUARDED:
        data = (CHECKOUT / rel).read_bytes()
        pin = pins[rel]
        rows.append({"path": rel, "sha256": sha(data), "ok": sha(data) == pin["sha256"] and len(data) == pin["bytes"]})
    return {"ok": all(r["ok"] for r in rows), "rows": rows}


def tree(root: Path) -> dict[str, str]:
    found = {}
    if not root.exists():
        return found
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            item = Path(dirpath) / name
            found[item.relative_to(root).as_posix()] = sha(item.read_bytes())
    return found


def watched() -> dict:
    page = LIVE_BOOK / "0519.desk-app" / "05.01.md"
    return {
        "member": tree(LIVE_BOOK / MEMBER),
        "page_0519_0501": sha(page.read_bytes()),
        "layout_exists": os.path.lexists(LIVE_BOOK / "return-line-layout.json"),
    }


class Run:
    """One run directory of evidence; calls are numbered in order."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.out = EVIDENCE / "runs" / name
        self.books = BOOKS / name
        if self.out.exists() or self.books.exists():
            raise SystemExit(f"refused: run {name} exists; choose a new run name")
        self.out.mkdir(parents=True)
        self.books.mkdir(parents=True)
        self.log = self.out / "calls.jsonl"
        self.count = 0

    def book(self, case: str) -> Path:
        path = self.books / case
        path.mkdir()
        assert not inside(path, CHECKOUT)
        return path

    def call(self, case: str, label: str, args: list[str]) -> subprocess.CompletedProcess:
        before = guard()
        if not before["ok"]:
            self._record(case, label, args, None, before, None, note="guard failed before call; not run")
            raise SystemExit("guard failed: live app/core bytes differ from pack05.01 pins")
        argv = [sys.executable, "-B", "app/librarian.py", "review-loop", *args]
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        start = time.time()
        proc = subprocess.run(argv, cwd=str(CHECKOUT), capture_output=True, env=env, shell=False)
        took = round(time.time() - start, 3)
        after = guard()
        self.count += 1
        stem = f"{self.count:02d}-{case}-{label}"
        (self.out / f"{stem}.stdout").write_bytes(proc.stdout)
        (self.out / f"{stem}.stderr").write_bytes(proc.stderr)
        self._record(case, label, argv, proc, before, after, stem=stem, seconds=took)
        if not after["ok"]:
            raise SystemExit("guard failed after call")
        return proc

    def _record(self, case, label, argv, proc, before, after, *, stem=None, seconds=None, note=None) -> None:
        row = {
            "n": self.count,
            "case": case,
            "label": label,
            "argv": [str(a) for a in argv],
            "cwd": str(CHECKOUT),
            "exit": None if proc is None else proc.returncode,
            "stdout": None if stem is None else f"{stem}.stdout",
            "stdout_sha256": None if proc is None else sha(proc.stdout),
            "stderr": None if stem is None else f"{stem}.stderr",
            "stderr_sha256": None if proc is None else sha(proc.stderr),
            "seconds": seconds,
            "guard_before": before["ok"],
            "guard_after": None if after is None else after["ok"],
            "note": note,
        }
        with self.log.open("ab") as handle:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n")

    def keep_book(self, case: str, tag: str) -> None:
        """Copy the whole disposable book into evidence, as it stands now."""
        src = self.books / case
        dst = self.out / "books" / f"{case}.{tag}"
        shutil.copytree(src, dst)
        (self.out / "books" / f"{case}.{tag}.tree.json").write_bytes(dump(tree(src)))


def copy_member(book: Path) -> dict:
    """Copy 0182 from pack05.01 snapshot bytes and check the copy against the pins."""
    pins = manifest()
    src = PACK / "sources" / "00.kernel" / "00.00.10.work" / MEMBER
    shutil.copytree(src, book / MEMBER)
    rows = []
    for rel, pin in pins.items():
        prefix = f"00.kernel/00.00.10.work/{MEMBER}/"
        if rel.startswith(prefix):
            data = (book / MEMBER / rel[len(prefix):]).read_bytes()
            rows.append({"path": rel, "ok": sha(data) == pin["sha256"] and len(data) == pin["bytes"]})
    extra = set(tree(book / MEMBER)) - {r["path"][len(f"00.kernel/00.00.10.work/{MEMBER}/"):] for r in rows}
    return {"ok": bool(rows) and all(r["ok"] for r in rows) and not extra, "rows": rows, "extra": sorted(extra)}


def snapshot_bytes(rel: str) -> bytes:
    return (PACK / "sources" / rel).read_bytes()
