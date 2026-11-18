#!/usr/bin/env python3
"""0707 pass01: operator walk, one stage per invocation.

usage: walk.py <run> <stage>
Each stage is what an operator does next; every app call is a new process.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness as H  # noqa: E402

PAGE_REL = "0519.desk-app/05.01.md"
PILOT = "labs/prime-entry-pilot-pass01"
SYNTHETIC_PAGE = (
    "# SYNTHETIC PENDING target - 0707 pass01 lab\n"
    "Not the real 0519.desk-app/05.01 page. Disposable book only. OUTSIDE-0707-TOKEN\n\n"
    "## Return pointer\n"
    "PENDING.\n\n"
    "## Review - Codex Prime\n"
    "PENDING.\n"
    "## Notes\n"
    "TAIL-0707-TOKEN\n"
).encode("utf-8")
ASSIGNMENT = b"SYNTHETIC assignment for the 0707 lab: review the copied 0182 return in a disposable book.\n"
NOTE = b"SYNTHETIC note for the 0707 lab: the copied return bytes are the evidence file.\n"


def state_path(run: H.Run | str) -> Path:
    name = run if isinstance(run, str) else run.name
    return H.EVIDENCE / "runs" / name / "state.json"


def load_state(name: str) -> dict:
    return json.loads(state_path(name).read_text(encoding="utf-8"))


def save_state(name: str, state: dict) -> None:
    state_path(name).write_bytes(H.dump(state))


class Resume(H.Run):
    """Reopen an existing run directory to append calls."""

    def __init__(self, name: str) -> None:  # noqa: D401
        self.name = name
        self.out = H.EVIDENCE / "runs" / name
        self.books = H.BOOKS / name
        self.log = self.out / "calls.jsonl"
        self.count = sum(1 for _ in self.log.open("rb")) if self.log.exists() else 0


def setup_book(run: H.Run, case: str, page: bytes) -> Path:
    book = run.book(case)
    copied = H.copy_member(book)
    (run.out / f"{case}-member-copy-check.json").write_bytes(H.dump(copied))
    if not copied["ok"]:
        raise SystemExit("member copy does not match pack pins")
    target = book / PAGE_REL
    target.parent.mkdir(parents=True)
    target.write_bytes(page)
    (book / "assignment.txt").write_bytes(ASSIGNMENT)
    (book / "note.md").write_bytes(NOTE)
    return book


def describe_and_plant(run: H.Run, case: str, book: Path) -> dict:
    proc = run.call(case, "describe-legacy", ["describe-legacy", "--book", str(book), "--member", H.MEMBER])
    body = json.loads(proc.stdout.decode("utf-8"))
    descriptor = body["descriptor"]
    (book / "descriptor.json").write_bytes(H.dump(descriptor))
    (book / "registration.json").write_bytes(H.snapshot_bytes(f"{PILOT}/example-registration.json"))
    (book / "request.json").write_bytes(H.snapshot_bytes(f"{PILOT}/example-request.json"))
    return body


def stage_start(name: str) -> None:
    run = H.Run(name)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=str(H.CHECKOUT), capture_output=True)
    (run.out / "git-status-before.txt").write_bytes(status.stdout)
    (run.out / "watched-before.json").write_bytes(H.dump(H.watched()))
    (run.out / "guard-before.json").write_bytes(H.dump(H.guard()))
    save_state(name, {"run": name, "stages": ["start"]})


def stage_a1(name: str) -> None:
    run = Resume(name)
    book = setup_book(run, "A", SYNTHETIC_PAGE)
    describe_and_plant(run, "A", book)
    run.call("A", "prepare", ["prepare", "--fixture-root", str(book), "--request", "request.json"])
    run.keep_book("A", "after-prepare")


def last_stdout(run: H.Run, case: str, label: str) -> dict:
    rows = [json.loads(line) for line in run.log.read_bytes().splitlines()]
    row = [r for r in rows if r["case"] == case and r["label"] == label][-1]
    return json.loads((run.out / row["stdout"]).read_bytes().decode("utf-8"))


def fill_decision(run: H.Run, case: str, book: Path) -> None:
    import decide

    template = last_stdout(run, case, "prepare")["view"]["template"]
    words = json.loads((H.LAB / "supplied-judgment.json").read_text(encoding="utf-8"))
    decision = decide.build(book, template, words)
    raw = H.dump(decision)
    (book / "decision.json").write_bytes(raw)
    (run.out / f"{case}-decision.json").write_bytes(raw)
    (run.out / f"{case}-prepare-template.json").write_bytes(H.dump(template))
    (run.out / "decision-build.json").write_bytes(H.dump({"provenance": decide.PROVENANCE}))


def prepare_record(run: H.Run, case: str, book: Path) -> None:
    run.call(case, "prepare", ["prepare", "--fixture-root", str(book), "--request", "request.json"])
    fill_decision(run, case, book)
    run.call(case, "record", ["record", "--fixture-root", str(book), "--request", "request.json", "--decision", "decision.json"])


def args_of(command: str, book: Path) -> list[str]:
    return [command, "--fixture-root", str(book), "--request", "request.json"]


def stage_a2(name: str) -> None:
    run = Resume(name)
    book = run.books / "A"
    fill_decision(run, "A", book)
    run.call("A", "record", ["record", "--fixture-root", str(book), "--request", "request.json", "--decision", "decision.json"])
    run.keep_book("A", "after-record")
    run.call("A", "render", args_of("render", book))
    run.keep_book("A", "after-render")


def stage_a3(name: str) -> None:
    run = Resume(name)
    run.call("A", "read", args_of("read", run.books / "A"))


def stage_b1(name: str) -> None:
    run = Resume(name)
    book = setup_book(run, "B", SYNTHETIC_PAGE)
    describe_and_plant(run, "B", book)
    prepare_record(run, "B", book)
    run.keep_book("B", "after-record-stop")


def stage_b2(name: str) -> None:
    run = Resume(name)
    book = run.books / "B"
    run.call("B", "read-before-recover", args_of("read", book))
    run.call("B", "recover", args_of("recover", book))
    run.call("B", "read-after-recover", args_of("read", book))
    run.keep_book("B", "after-recover")


def stage_c1(name: str) -> None:
    run = Resume(name)
    book = run.books / "A"
    before = (book / PAGE_REL).read_bytes()
    run.call("C", "recover-on-A", args_of("recover", book))
    run.call("C", "render-again-on-A", args_of("render", book))
    run.call("C", "read-on-A", args_of("read", book))
    after = (book / PAGE_REL).read_bytes()
    (run.out / "C-page-check.json").write_bytes(H.dump({"before": H.sha(before), "after": H.sha(after), "unchanged": before == after}))


def stage_d1(name: str) -> None:
    run = Resume(name)
    book = setup_book(run, "D", SYNTHETIC_PAGE)
    describe_and_plant(run, "D", book)
    prepare_record(run, "D", book)
    target = book / PAGE_REL
    original = target.read_bytes()
    changed = original.replace(b"OUTSIDE-0707-TOKEN", b"OUTSIDE-0707-TOKEX")
    assert changed != original and len(changed) == len(original)
    target.write_bytes(changed)
    run.call("D", "render-after-target-change", args_of("render", book))
    run.call("D", "read", args_of("read", book))
    after = target.read_bytes()
    (run.out / "D-page-check.json").write_bytes(H.dump({
        "recorded_against": H.sha(original), "changed_to": H.sha(changed), "after_render": H.sha(after),
        "render_left_changed_bytes": after == changed,
    }))
    run.keep_book("D", "after")


def stage_e1(name: str) -> None:
    run = Resume(name)
    page = H.snapshot_bytes("00.kernel/00.00.10.work/0519.desk-app/05.01.md")
    book = setup_book(run, "E", page)
    describe_and_plant(run, "E", book)
    prepare_record(run, "E", book)
    run.call("E", "render", args_of("render", book))
    run.call("E", "recover", args_of("recover", book))
    run.call("E", "read", args_of("read", book))
    after = (book / PAGE_REL).read_bytes()
    (run.out / "E-page-check.json").write_bytes(H.dump({
        "snapshot": H.sha(page), "after": H.sha(after), "unchanged": after == page,
        "partials": sorted(p.name for p in (book / "partial").glob("*")) if (book / "partial").is_dir() else [],
    }))
    run.keep_book("E", "after")


def stage_f1(name: str) -> None:
    run = Resume(name)
    run.call("F", "prepare-root-inside-checkout", ["prepare", "--fixture-root", str(H.LAB), "--request", "request.json"])


def stage_end(name: str) -> None:
    run = Resume(name)
    status = subprocess.run(["git", "status", "--porcelain"], cwd=str(H.CHECKOUT), capture_output=True)
    (run.out / "git-status-after.txt").write_bytes(status.stdout)
    (run.out / "watched-after.json").write_bytes(H.dump(H.watched()))
    (run.out / "guard-after.json").write_bytes(H.dump(H.guard()))


STAGES = {
    "start": stage_start, "a1": stage_a1, "a2": stage_a2, "a3": stage_a3, "b1": stage_b1, "b2": stage_b2,
    "c1": stage_c1, "d1": stage_d1, "e1": stage_e1, "f1": stage_f1, "end": stage_end,
}


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[2] not in STAGES:
        print("usage: walk.py <run> <" + "|".join(STAGES) + ">", file=sys.stderr)
        return 2
    name, stage = sys.argv[1], sys.argv[2]
    STAGES[stage](name)
    if stage != "start":
        state = load_state(name)
        state["stages"].append(stage)
        save_state(name, state)
    return 0


if __name__ == "__main__":
    sys.exit(main())
