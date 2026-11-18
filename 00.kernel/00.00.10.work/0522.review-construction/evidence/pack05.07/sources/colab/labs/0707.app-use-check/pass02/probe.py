#!/usr/bin/env python3
"""0707 pass02: bounded design probes on CURRENT code (nonproduction lab).

usage: probe.py <run>
P1  construct.py show on six target shapes (read-only; pinned file run directly)
P2  app review-loop prepare on the same shapes
P3  app describe/prepare/record/render/read with recorded_decisions [] and a
    SYNTHETIC correction-required disposition

Writes only: evidence/build05.02/probes/<run>/ and disposable books under the
scratchpad. Guards the pinned code against pack05.02 before and after each call.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

CHECKOUT = Path(r"D:\Git\lib-build")
PAGE = CHECKOUT / "00.kernel" / "00.00.10.work" / "0707.app-use-check"
PACK2 = PAGE / "evidence" / "pack05.02"
PACK1 = PAGE / "evidence" / "pack05.01"
OLD = PAGE / "evidence" / "build05.01" / "runs" / "run1"
EVIDENCE = PAGE / "evidence" / "build05.02" / "probes"
LAB = Path(__file__).resolve().parent
BOOKS = Path(r"C:\Users\misg\AppData\Local\Temp\claude\D--Git-Librarian\313e7ce7-27d2-405b-881d-6a16a47199dc\scratchpad\0707-0502-books")
MEMBER = "0182.desk-app-integration-design-0501"
PAGE_REL = "0519.desk-app/05.01.md"
GUARDED = [
    "app/librarian.py", "app/review_loop_tools_v2.py", "app/review-loop-v2.json",
    "labs/review-loop-pass02/review_loop.py", "labs/prime-cycle-pass03/prime_cycle.py",
    "labs/review-construction-pass02/construct.py", "labs/prime-review-pass01/prime_review.py",
    "labs/prime-review-pass02/prime_review.py", "labs/return-lines-pass01/return_lines.py",
    "labs/return-placement-pass01/return_placement.py", "labs/return-capture-pass01/return_inspect.py",
    "labs/return-capture-pass01/return_capture.py",
]
PENDING = (
    "# SYNTHETIC PENDING target - 0707 pass02 probe\nOUTSIDE-0502-TOKEN\n\n"
    "## Return pointer\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n## Notes\nTAIL-0502-TOKEN\n"
).encode("utf-8")
NO_HEADING = b"# SYNTHETIC page without a review heading - 0707 pass02 probe\n\n## Return pointer\nPENDING.\n"
DUPLICATE = (
    "# SYNTHETIC page with two review headings - 0707 pass02 probe\n\n"
    "## Review - Codex Prime\nPENDING.\n\n## Review - Codex Prime\nPENDING.\n"
).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(payload) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def pins(pack: Path) -> dict:
    body = json.loads((pack / "source-manifest.json").read_text(encoding="utf-8"))
    return {row["path"]: row for row in body["files"]}


P2PINS = pins(PACK2)
P1PINS = pins(PACK1)


def guard() -> bool:
    for rel in GUARDED:
        data = (CHECKOUT / rel).read_bytes()
        if sha(data) != P2PINS[rel]["sha256"] or len(data) != P2PINS[rel]["bytes"]:
            return False
    return True


def snap1(rel: str) -> bytes:
    data = (PACK1 / "sources" / rel).read_bytes()
    pin = P1PINS[rel]
    assert sha(data) == pin["sha256"] and len(data) == pin["bytes"], rel
    return data


class Run:
    def __init__(self, name: str) -> None:
        self.out = EVIDENCE / name
        self.books = BOOKS / name
        if self.out.exists() or self.books.exists():
            raise SystemExit(f"refused: run {name} exists")
        self.out.mkdir(parents=True)
        self.books.mkdir(parents=True)
        self.n = 0

    def call(self, probe: str, label: str, argv: list[str]) -> subprocess.CompletedProcess:
        if not guard():
            raise SystemExit("guard failed before call")
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        full = [sys.executable, "-B", *argv]
        proc = subprocess.run(full, cwd=str(CHECKOUT), capture_output=True, env=env, shell=False)
        ok_after = guard()
        self.n += 1
        stem = f"{self.n:02d}-{probe}-{label}"
        (self.out / f"{stem}.stdout").write_bytes(proc.stdout)
        (self.out / f"{stem}.stderr").write_bytes(proc.stderr)
        row = {"n": self.n, "probe": probe, "label": label, "argv": full, "cwd": str(CHECKOUT),
               "exit": proc.returncode, "stdout_sha256": sha(proc.stdout), "stderr_sha256": sha(proc.stderr),
               "guard_before": True, "guard_after": ok_after}
        with (self.out / "calls.jsonl").open("ab") as handle:
            handle.write(json.dumps(row, sort_keys=True).encode("utf-8") + b"\n")
        if not ok_after:
            raise SystemExit("guard failed after call")
        return proc


def shapes() -> dict[str, bytes | None]:
    return {
        "pending": PENDING,
        "substantive": snap1("00.kernel/00.00.10.work/0519.desk-app/05.01.md"),
        "rendered-other": (OLD / "books" / "A.after-render" / PAGE_REL).read_bytes(),
        "no-heading": NO_HEADING,
        "duplicate-heading": DUPLICATE,
        "absent": None,
    }


def make_book(run: Run, name: str, page: bytes | None, registration: bytes) -> Path:
    book = run.books / name
    book.mkdir()
    src = PACK1 / "sources" / "00.kernel" / "00.00.10.work" / MEMBER
    shutil.copytree(src, book / MEMBER)
    for rel, pin in P1PINS.items():
        prefix = f"00.kernel/00.00.10.work/{MEMBER}/"
        if rel.startswith(prefix):
            assert sha((book / MEMBER / rel[len(prefix):]).read_bytes()) == pin["sha256"], rel
    if page is not None:
        (book / PAGE_REL).parent.mkdir(parents=True)
        (book / PAGE_REL).write_bytes(page)
    (book / "assignment.txt").write_bytes(b"SYNTHETIC assignment for the 0707 pass02 probe.\n")
    (book / "note.md").write_bytes(b"SYNTHETIC note for the 0707 pass02 probe.\n")
    (book / "registration.json").write_bytes(registration)
    (book / "request.json").write_bytes(snap1("labs/prime-entry-pilot-pass01/example-request.json"))
    return book


def app(command: str, *pairs: str) -> list[str]:
    return ["app/librarian.py", "review-loop", command, *pairs]


def main() -> int:
    run = Run(sys.argv[1])
    example_reg = snap1("labs/prime-entry-pilot-pass01/example-registration.json")

    # descriptor once, from a real describe-legacy on a fresh copy
    first = make_book(run, "describe", PENDING, example_reg)
    proc = run.call("P0", "describe-legacy", app("describe-legacy", "--book", str(first), "--member", MEMBER))
    descriptor = dump(json.loads(proc.stdout.decode("utf-8"))["descriptor"])
    (run.out / "descriptor.json").write_bytes(descriptor)

    # P1: constructor show, read-only
    p1 = run.books / "p1"
    p1.mkdir()
    for name, page in shapes().items():
        if page is not None:
            (p1 / name).mkdir()
            (p1 / name / "page.md").write_bytes(page)
        run.call("P1", name, ["labs/review-construction-pass02/construct.py", "show",
                              "--fixture-root", str(p1), "--target", f"{name}/page.md"])

    # P2: app prepare per shape
    for name, page in shapes().items():
        book = make_book(run, f"p2-{name}", page, example_reg)
        (book / "descriptor.json").write_bytes(descriptor)
        run.call("P2", name, app("prepare", "--fixture-root", str(book), "--request", "request.json"))

    # P3: clean agreement + SYNTHETIC correction-required, full path
    reg = json.loads(example_reg)
    reg["agreement"]["recorded_decisions"] = []
    reg["agreement"]["prime_discretion"] = "SYNTHETIC probe: no Director decision is recorded for this fixture."
    clean = dump(reg)
    (run.out / "P3-registration.json").write_bytes(clean)
    book = make_book(run, "p3", PENDING, clean)
    proc = run.call("P3", "describe-legacy", app("describe-legacy", "--book", str(book), "--member", MEMBER))
    (book / "descriptor.json").write_bytes(dump(json.loads(proc.stdout.decode("utf-8"))["descriptor"]))
    proc = run.call("P3", "prepare", app("prepare", "--fixture-root", str(book), "--request", "request.json"))
    template = json.loads(proc.stdout.decode("utf-8"))["view"]["template"]
    decide_path = CHECKOUT / "colab/labs/0707.app-use-check/pass01/decide.py"
    assert sha(decide_path.read_bytes()) == P2PINS["colab/labs/0707.app-use-check/pass01/decide.py"]["sha256"]
    spec = importlib.util.spec_from_file_location("pass01_decide", decide_path)
    decide = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(decide)
    words = json.loads((LAB / "fixtures" / "supplied-correction-required.json").read_text(encoding="utf-8"))
    decision = dump(decide.build(book, template, words))
    (book / "decision.json").write_bytes(decision)
    (run.out / "P3-decision.json").write_bytes(decision)
    run.call("P3", "record", app("record", "--fixture-root", str(book), "--request", "request.json", "--decision", "decision.json"))
    run.call("P3", "render", app("render", "--fixture-root", str(book), "--request", "request.json"))
    run.call("P3", "read", app("read", "--fixture-root", str(book), "--request", "request.json"))
    (run.out / "P3-page-after.md").write_bytes((book / PAGE_REL).read_bytes())
    (run.out / "P3-REVIEW.md").write_bytes((book / "cycle" / "05.01-r1" / "REVIEW.md").read_bytes())
    return 0


if __name__ == "__main__":
    sys.exit(main())
