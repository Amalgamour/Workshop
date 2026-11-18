"""Replay the supported assignment, capture, review, and restart path.

This file is lab glue. It does not import the clerk, the handoff, the capture
helper, or the Prime cycle. Each step is a new process running the pinned CLI.
Judgment words are supplied here. They are not a model and they are not Prime.
Disposable trees stay in the process temp directory, outside D:\\Git\\lib-build.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
BOOK = "00.kernel/00.00.10.work"
LANE = "0599.loop-lab"
BATCH = "05.01"
PAGE = f"{BOOK}/{LANE}/{BATCH}.md"
PIECE = b"synthetic piece\n"
INSTRUCTION = b"Synthetic assignment: write piece.txt.\n"
EVIDENCE = "synthetic handback line"
QUESTION = "SUPPLIED question: should the synthetic piece stay one file?"
NEXT_ACTION = "Pack one bounded correction for the synthetic piece."
AGREEMENT = {
    "goal": "SUPPLIED lab goal.",
    "scope": "SUPPLIED lab scope: this disposable page only.",
    "prime_discretion": "Prime may accept a bounded repair inside this scope.",
    "director_required": "Any change of design or scope.",
    "finish_criteria": [{"id": "done", "text": "The disposable page goal is met."}],
    "recorded_decisions": [{
        "id": "D1",
        "text": "SUPPLIED lab release label.",
        "source_sha256": "0" * 64,
    }],
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def outside_git(path: Path) -> None:
    current = path.resolve()
    while True:
        if (current / ".git").exists():
            raise RuntimeError(f"fixture path is inside a Git working tree: {path}")
        if current.parent == current:
            return
        current = current.parent


def tool(relative: str, args: list[str], timeout: int = 180) -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    proc = subprocess.run(
        [sys.executable, "-B", str(ROOT / relative), *args],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        timeout=timeout,
    )
    return {
        "argv": [sys.executable, "-B", relative, *args],
        "exit": proc.returncode,
        "stdout": proc.stdout.replace(b"\r\n", b"\n").decode("utf-8", "replace"),
        "stderr": proc.stderr.replace(b"\r\n", b"\n").decode("utf-8", "replace"),
    }


def field(text: str, prefix: str) -> str:
    for line in text.splitlines():
        if line.startswith(prefix):
            return line[len(prefix):]
    raise RuntimeError(f"missing {prefix!r}\n{text}")


def page_text(member: str | None, receipt: str | None, extra: str = "") -> str:
    if member:
        pointer = (
            f"Execution: returned. Member {member}. Receipt sha256 {receipt}. "
            "Fresh verify: result complete."
        )
    else:
        pointer = "PENDING."
    return (
        "# 05 — Synthetic loop batch\n"
        "version: 001\nstate: draft\nFace: 05\nPPPP: 0599\nbook: 00.00.10.work\n\n"
        "## Assignment\nExecutor: synthetic builder. Reviewer: synthetic Prime.\n\n"
        f"## #01 — Synthetic task\nWrite piece.txt.{extra}\n\n"
        f"## Return pointer\n{pointer}\n\n"
        "## Review — Codex Prime\nPENDING.\n"
    )


class Desk:
    """One disposable repository, clerk store, and output root."""

    def __init__(self, name: str):
        parent = Path(tempfile.gettempdir())
        outside_git(parent)
        self.tmp = Path(tempfile.mkdtemp(prefix=f"deskloop-{name}-", dir=str(parent)))
        outside_git(self.tmp)
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        self.book = self.repo / BOOK
        self.book.mkdir(parents=True)
        self.store = self.tmp / "store"
        self.instructions = self.tmp / "instructions"
        self.instructions.mkdir()
        self.source = self.tmp / "source"
        self.source.mkdir()
        self.out = self.tmp / "out"
        self.out.mkdir()
        self.journal = self.tmp / "journal"
        self.trace: list[dict] = []
        subprocess.run(
            ["git", "-C", str(self.repo), "init", "-q", "-b", "main"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def close(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def call(self, label: str, relative: str, args: list[str], timeout: int = 180) -> dict:
        step = tool(relative, args, timeout)
        step["label"] = label
        self.trace.append(step)
        return step

    def write_job(self, job_id: str) -> Path:
        task = self.instructions / "task.txt"
        task.write_bytes(INSTRUCTION)
        job = {
            "assignee": "lab-builder",
            "expected_outputs": ["piece.txt"],
            "instructions": {"path": "task.txt", "sha256": sha256(INSTRUCTION)},
            "job_id": job_id,
            "release": "synthetic job label; not a release",
            "reviewer": "lab-reviewer",
            "routed_by": "desk-loop-replay-pass01",
        }
        path = self.tmp / "job.json"
        path.write_bytes(canonical(job))
        return path

    def queue_and_claim(self, job_id: str) -> str:
        job = self.write_job(job_id)
        queued = self.call(
            "clerk queue",
            "labs/clerk-handoff-pass02/clerk.py",
            ["queue", "--store", str(self.store), "--job", str(job), "--instructions-base", str(self.instructions)],
        )
        if queued["exit"] != 0:
            raise RuntimeError(queued["stdout"] + queued["stderr"])
        claimed = self.call(
            "clerk claim",
            "labs/clerk-handoff-pass02/clerk.py",
            ["claim", "--store", str(self.store), "--job", job_id, "--as", "lab-builder",
             "--instructions-base", str(self.instructions)],
        )
        if claimed["exit"] != 0:
            raise RuntimeError(claimed["stdout"] + claimed["stderr"])
        return field(claimed["stdout"], "token ")

    def put_piece(self, body: bytes = PIECE) -> None:
        outbox = self.store / "jobs" / self.job_id / "outbox"
        (outbox / "piece.txt").write_bytes(body)
        (self.source / "piece.txt").write_bytes(body)

    def clerk_return(self, token: str, delivery: str) -> dict:
        return self.call(
            "clerk return",
            "labs/clerk-handoff-pass02/clerk.py",
            ["return", "--store", str(self.store), "--job", self.job_id, "--as", "lab-builder",
             "--claim", token, "--delivery", delivery, "--evidence", EVIDENCE],
        )

    def reserve(self, submission: str, name: str) -> str:
        reserved = self.call(
            "return_capture reserve",
            "labs/return-capture-pass01/return_capture.py",
            ["reserve", "--book", str(self.book), "--submission", submission, "--name", name,
             "--origin-book", "00.00.10.work", "--origin-page", LANE, "--origin-batch", BATCH,
             "--expected-output", "piece.txt", "--submitter", "lab-builder", "--reviewer", "lab-reviewer",
             "--release", "synthetic reservation; not a release"],
        )
        if reserved["exit"] != 0:
            raise RuntimeError(reserved["stdout"] + reserved["stderr"])
        return field(reserved["stdout"], "member ")

    def bind_and_perform(self, submission: str, member: str, event: str) -> dict:
        binding = {
            "schema": "clerk-capture-handoff/1",
            "clerk_store": str(self.store),
            "job_id": self.job_id,
            "instructions_base": str(self.instructions),
            "returned_event_sha256": event,
            "assignee": "lab-builder",
            "work_ref": "synthetic-work-ref",
            "origin": {"batch": BATCH, "book": "00.00.10.work", "page": LANE},
            "book": str(self.book),
            "submission_id": submission,
            "member": member,
            "source_root": str(self.source),
            "artifact_base": str(self.store / "jobs" / self.job_id / "outbox"),
            "report": {
                "clerk_path": "piece.txt",
                "source": "piece.txt",
                "sha256": sha256(PIECE),
                "bytes": len(PIECE),
            },
            "artifacts": [{
                "clerk_path": "piece.txt",
                "source": "piece.txt",
                "logical": "piece.txt",
                "sha256": sha256(PIECE),
                "bytes": len(PIECE),
            }],
            "record": str(self.tmp / "handoff-record"),
            "failure_log": str(self.tmp / "failure.log"),
        }
        path = self.tmp / "binding.json"
        path.write_bytes(canonical(binding))
        self.binding = path
        return self.call(
            "handoff perform",
            "labs/capture-handoff-pass01/handoff.py",
            ["perform", "--binding", str(path)],
            timeout=180,
        )

    def write_page(self, text: str) -> None:
        path = self.repo / PAGE
        path.parent.mkdir(parents=True, exist_ok=True)
        (path.parent / "evidence").mkdir(exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        self.page = path

    def registration(self, member: str | None, work_id: str = "loop") -> Path:
        reg = {
            "schema": "prime-cycle-registration/1",
            "repository": str(self.repo),
            "book": BOOK,
            "book_label": "00.00.10.work",
            "source": {"kind": "live-file", "commit": None},
            "members_book": str(self.book),
            "output_root": str(self.out),
            "bounds": {"max_works": 16, "max_page_bytes": 262144, "max_output_bytes": 2097152},
            "works": [{
                "work_id": work_id,
                "page": PAGE,
                "pass": BATCH,
                "member": member,
                "goal": {"goal_id": "g1", "statement": "Write the synthetic piece."},
                "agreement": AGREEMENT,
                "review_location": f"{BOOK}/{LANE}/evidence/prime-cycle-reviews/{BATCH}",
            }],
        }
        path = self.tmp / "registration.json"
        path.write_bytes((json.dumps(reg, indent=1) + "\n").encode("utf-8"))
        self.reg = path
        return path

    def cycle(self, label: str, *args: str) -> dict:
        return self.call(
            label,
            "labs/prime-cycle-pass01/prime_cycle.py",
            [*args, "--journal-root", str(self.journal), "--caller", "Grok-2 lab (SUPPLIED)",
             "--note", "synthetic desk-loop replay"],
            timeout=180,
        )

    def read(self, label: str, templates: bool = False) -> dict:
        args = ["read", "--registration", str(self.reg), "--json"]
        if templates:
            args += ["--templates", str(self.out / "templates")]
        step = self.cycle(label, *args)
        view = None
        if step["stdout"].lstrip().startswith("{"):
            view = json.loads(step["stdout"])
        step["view"] = view
        return step

    def receipt_sha(self, member: str) -> str:
        return sha256((self.book / member / "receipt.json").read_bytes())


def supply(template: dict, kind: str) -> dict:
    """Fill a cycle template with supplied words. This is glue, not prime_cycle."""
    decision = json.loads(json.dumps(template))
    decision["attribution"] = {
        "actor_label": "Grok-2 lab (SUPPLIED)",
        "role": "prime",
        "evidence": "SUPPLIED by desk-loop-replay-pass01. The label is not authentication.",
    }
    judgment = decision["judgment"]
    page = decision["binding"]["page"]
    judgment.update(
        finding="SUPPLIED lab finding.",
        reasons=["SUPPLIED lab reason."],
        source_refs=[page],
        semantic_conflict=False,
        design_fork=None,
        unresolved=[],
        holds=[],
        answers=[],
    )
    sections = judgment["sections"]
    if kind == "held":
        judgment.update(
            outcome="continue",
            disposition="held",
            pass_terminal="open",
            next_action={"action_id": "pack-correction", "text": NEXT_ACTION, "authorized_in_grant": True},
        )
        judgment["goal"]["terminal"] = "open"
        sections.update(
            return_result="The synthetic pass returned.",
            prime_finding="Held inside the synthetic scope.",
            within_direction="Inside the supplied fixture grant.",
            next_bounded_action=NEXT_ACTION,
        )
    elif kind == "accepted":
        judgment.update(
            outcome="continue",
            disposition="accepted",
            pass_terminal="finished",
            next_action={"action_id": "pack-correction", "text": NEXT_ACTION, "authorized_in_grant": True},
        )
        judgment["goal"]["terminal"] = "open"
        sections.update(
            return_result="The synthetic pass returned.",
            prime_finding="SUPPLIED accept without a capture, used only to test the refusal.",
            within_direction="Inside the supplied fixture grant.",
            next_bounded_action=NEXT_ACTION,
        )
    elif kind == "question":
        digest = sha256(QUESTION.encode("utf-8"))
        judgment.update(
            outcome="director-input",
            disposition="held",
            pass_terminal="open",
            next_action=None,
            unresolved=[QUESTION],
            holds=[{
                "hold_id": "H1",
                "finding_id": f"{page}#F-01",
                "kind": "director-judgment",
                "question_id": "Q1",
                "question_revision": "r1",
                "question_sha256": digest,
                "dependent_scope": ["design-change"],
            }],
        )
        judgment["goal"]["terminal"] = "open"
        sections.update(
            issue="SUPPLIED design question.",
            consequences="Either choice changes the next synthetic pass.",
            options=["Keep one file.", "Split the piece."],
            recommendation="Keep one file.",
            question={"id": "Q1", "revision": "r1", "content_sha256": digest, "text": QUESTION},
            affected=[{"action_id": "design-change", "dependency": "the open design question"}],
        )
    else:
        raise RuntimeError(kind)
    return decision


def write_decision(desk: Desk, decision: dict, name: str) -> Path:
    path = desk.tmp / name
    path.write_bytes((json.dumps(decision, indent=1) + "\n").encode("utf-8"))
    return path


def work(view: dict) -> dict:
    return view["works"][0]


def case_loop() -> dict:
    """Capture, restart before review, record a held next action, then stale the page."""
    desk = Desk("loop")
    desk.job_id = "job-loop"
    try:
        token = desk.queue_and_claim(desk.job_id)
        shown = desk.call(
            "clerk show",
            "labs/clerk-handoff-pass02/clerk.py",
            ["show", "--store", str(desk.store), "--job", desk.job_id, "--json",
             "--instructions-base", str(desk.instructions)],
        )
        desk.put_piece()
        returned = desk.clerk_return(token, "delivery-loop")
        event = field(returned["stdout"], "event 0003.returned.json sha256=")
        member = desk.reserve("loop-happy", "loop-return")
        performed = desk.bind_and_perform("loop-happy", member, event)
        receipt = desk.receipt_sha(member)
        desk.write_page(page_text(member, receipt))
        desk.registration(member)
        before = desk.read("cycle read before review", templates=True)
        template = json.loads((desk.out / "templates" / "template-loop.json").read_text(encoding="utf-8"))
        decision = write_decision(desk, supply(template, "held"), "held.json")
        recorded = desk.cycle("cycle record held", "record", "--registration", str(desk.reg), "--decision", str(decision))
        after = desk.read("cycle read after review")
        desk.page.write_bytes(desk.page.read_bytes() + b"\nEdited after review.\n")
        stale = desk.read("cycle read after page edit")
        refused = desk.cycle(
            "cycle record stale template",
            "record", "--registration", str(desk.reg), "--decision", str(decision),
        )
        return {
            "trace": slim(desk.trace),
            "show": json.loads(shown["stdout"]) if shown["exit"] == 0 else shown["stdout"],
            "return_exit": returned["exit"],
            "handoff_exit": performed["exit"],
            "receipt": receipt,
            "before": work(before["view"]) if before.get("view") else None,
            "before_exit": before["exit"],
            "record_exit": recorded["exit"],
            "record_stdout": recorded["stdout"],
            "after": work(after["view"]) if after.get("view") else None,
            "after_exit": after["exit"],
            "stale": work(stale["view"]) if stale.get("view") else None,
            "stale_exit": stale["exit"],
            "stale_record_exit": refused["exit"],
            "stale_record_stdout": refused["stdout"],
            "elected": [item["view"]["elected"] for item in (before, after, stale) if item.get("view")],
        }
    finally:
        desk.close()


def case_missing() -> dict:
    desk = Desk("missing")
    desk.job_id = "job-missing"
    try:
        token = desk.queue_and_claim(desk.job_id)
        returned = desk.clerk_return_ready(token)
        shown = desk.call(
            "clerk show returned",
            "labs/clerk-handoff-pass02/clerk.py",
            ["show", "--store", str(desk.store), "--job", desk.job_id, "--json",
             "--instructions-base", str(desk.instructions)],
        )
        desk.write_page(page_text(None, None, " The worker says this assignment is done."))
        desk.registration(None)
        viewed = desk.read("cycle read with no capture", templates=True)
        template = json.loads((desk.out / "templates" / "template-loop.json").read_text(encoding="utf-8"))
        decision = write_decision(desk, supply(template, "accepted"), "accepted.json")
        refused = desk.cycle(
            "cycle record accepted without capture",
            "record", "--registration", str(desk.reg), "--decision", str(decision),
        )
        review_root = desk.repo / BOOK / LANE / "evidence" / "prime-cycle-reviews"
        return {
            "trace": slim(desk.trace),
            "clerk_state": json.loads(shown["stdout"]).get("state") if shown["exit"] == 0 else shown["stdout"],
            "return_exit": returned["exit"],
            "members": [p.name for p in desk.book.iterdir() if p.is_dir()],
            "view": work(viewed["view"]) if viewed.get("view") else None,
            "view_exit": viewed["exit"],
            "accept_exit": refused["exit"],
            "accept_stdout": refused["stdout"],
            "review_dirs": [p.name for p in review_root.iterdir()] if review_root.exists() else [],
        }
    finally:
        desk.close()


def case_repeat() -> dict:
    desk = Desk("repeat")
    desk.job_id = "job-repeat"
    try:
        token = desk.queue_and_claim(desk.job_id)
        desk.put_piece()
        first = desk.clerk_return(token, "delivery-repeat")
        event = field(first["stdout"], "event 0003.returned.json sha256=")
        event_path = desk.store / "jobs" / desk.job_id / "0003.returned.json"
        event_hash = sha256(event_path.read_bytes())
        member = desk.reserve("loop-repeat", "loop-repeat")
        performed = desk.bind_and_perform("loop-repeat", member, event)
        receipt_before = (desk.book / member / "receipt.json").read_bytes()
        completed = desk.tmp / "handoff-record" / "completed.json"
        completed_before = completed.read_bytes()
        again = desk.clerk_return(token, "delivery-repeat")
        retried = desk.call(
            "handoff perform retry",
            "labs/capture-handoff-pass01/handoff.py",
            ["perform", "--binding", str(desk.binding)],
        )
        (desk.store / "jobs" / desk.job_id / "outbox" / "piece.txt").write_bytes(b"changed piece\n")
        conflict = desk.clerk_return(token, "delivery-repeat")
        other = desk.tmp / "other-return.md"
        other.write_bytes(b"different return body\n")
        recapture = desk.call(
            "return_capture capture changed return",
            "labs/return-capture-pass01/return_capture.py",
            ["capture", "--book", str(desk.book), "--submission", "loop-repeat",
             "--return-file", str(other), "--source-root", str(desk.source),
             "--artifact", "piece.txt|piece.txt"],
        )
        return {
            "trace": slim(desk.trace),
            "first_exit": first["exit"],
            "handoff_exit": performed["exit"],
            "again_exit": again["exit"],
            "again_stdout": again["stdout"],
            "event_unchanged": sha256(event_path.read_bytes()) == event_hash,
            "retry_exit": retried["exit"],
            "retry_stdout": retried["stdout"],
            "completed_unchanged": completed.read_bytes() == completed_before,
            "conflict_exit": conflict["exit"],
            "conflict_stdout": conflict["stdout"],
            "event_unchanged_after_conflict": sha256(event_path.read_bytes()) == event_hash,
            "recapture_exit": recapture["exit"],
            "recapture_stdout": recapture["stdout"],
            "receipt_unchanged": (desk.book / member / "receipt.json").read_bytes() == receipt_before,
        }
    finally:
        desk.close()


def case_stale_instruction() -> dict:
    desk = Desk("stale")
    try:
        job = desk.write_job("job-stale")
        queued = desk.call(
            "clerk queue",
            "labs/clerk-handoff-pass02/clerk.py",
            ["queue", "--store", str(desk.store), "--job", str(job), "--instructions-base", str(desk.instructions)],
        )
        task = desk.instructions / "task.txt"
        task.write_bytes(INSTRUCTION + b"changed after queue\n")
        claimed = desk.call(
            "clerk claim stale instructions",
            "labs/clerk-handoff-pass02/clerk.py",
            ["claim", "--store", str(desk.store), "--job", "job-stale", "--as", "lab-builder",
             "--instructions-base", str(desk.instructions)],
        )
        claim_file = desk.store / "jobs" / "job-stale" / "0002.claimed.json"
        return {
            "trace": slim(desk.trace),
            "queue_exit": queued["exit"],
            "claim_exit": claimed["exit"],
            "claim_stdout": claimed["stdout"],
            "claim_written": claim_file.exists(),
        }
    finally:
        desk.close()


def case_unresolved() -> dict:
    desk = Desk("question")
    desk.job_id = "job-question"
    try:
        token = desk.queue_and_claim(desk.job_id)
        desk.put_piece()
        returned = desk.clerk_return(token, "delivery-question")
        event = field(returned["stdout"], "event 0003.returned.json sha256=")
        member = desk.reserve("loop-question", "loop-question")
        performed = desk.bind_and_perform("loop-question", member, event)
        desk.write_page(page_text(member, desk.receipt_sha(member)))
        desk.registration(member)
        first = desk.read("cycle read before question", templates=True)
        template = json.loads((desk.out / "templates" / "template-loop.json").read_text(encoding="utf-8"))
        decision = write_decision(desk, supply(template, "question"), "question.json")
        recorded = desk.cycle(
            "cycle record question",
            "record", "--registration", str(desk.reg), "--decision", str(decision),
        )
        second = desk.read("cycle read after question")
        return {
            "trace": slim(desk.trace),
            "handoff_exit": performed["exit"],
            "record_exit": recorded["exit"],
            "record_stdout": recorded["stdout"],
            "after": work(second["view"]) if second.get("view") else None,
            "after_text_has_question": QUESTION in (second["stdout"] if second.get("view") else ""),
            "after_exit": second["exit"],
            "elected": None if not second.get("view") else second["view"]["elected"],
        }
    finally:
        desk.close()


# The missing case returns before put_piece. Give it the same outbox write.
def _missing_return(self, token: str) -> dict:
    self.put_piece()
    return self.clerk_return(token, "delivery-missing")


Desk.clerk_return_ready = _missing_return  # type: ignore[attr-defined]


def slim(trace: list[dict]) -> list[dict]:
    """Keep exits and text. Drop parsed views, which are stored on the case."""
    out = []
    for step in trace:
        item = {key: step[key] for key in ("label", "exit", "stdout", "stderr", "argv")}
        out.append(item)
    return out


def checks_for(report: dict) -> list[dict]:
    found = []

    def add(name: str, ok: bool, detail: str) -> None:
        found.append({"name": name, "ok": bool(ok), "detail": detail})

    loop = report["loop"]
    before = loop["before"] or {}
    after = loop["after"] or {}
    stale = loop["stale"] or {}
    add("loop claim shows usable instructions",
        isinstance(loop["show"], dict) and str(loop["show"].get("checks", {}).get("instructions", "")).startswith("usable"),
        str(loop["show"])[:240])
    add("loop handoff captures", loop["handoff_exit"] == 0 and loop["return_exit"] == 0, str(loop["handoff_exit"]))
    add("restart before review is awaiting-review",
        before.get("pass_state") == "awaiting-review" and before.get("custody", {}).get("state") == "present"
        and before.get("next_action") is None and before.get("pass_terminal") == "unknown",
        json.dumps({"pass_state": before.get("pass_state"), "custody": before.get("custody", {}).get("state"),
                    "terminal": before.get("pass_terminal")}))
    add("held review recovers the next action",
        loop["record_stdout"].startswith("recorded") and after.get("pass_state") == "reviewed"
        and after.get("disposition") == "held" and after.get("pass_terminal") == "open"
        and after.get("goal_terminal") == "open"
        and (after.get("next_action") or {}).get("text") == NEXT_ACTION,
        json.dumps({"record": loop["record_stdout"][:180], "pass_state": after.get("pass_state"),
                    "next": (after.get("next_action") or {}).get("text")}))
    add("cycle elects nothing", loop["elected"] == [None, None, None], str(loop["elected"]))
    add("edited page makes the review stale",
        stale.get("pass_state") == "review-stale" and stale.get("next_action") is None
        and ((stale.get("historical") or {}).get("next_action") or {}).get("text") == NEXT_ACTION,
        json.dumps({"pass_state": stale.get("pass_state"), "historical": (stale.get("historical") or {}).get("reason")}))
    add("stale template is refused",
        loop["stale_record_exit"] == 2 and "source changed" in loop["stale_record_stdout"],
        loop["stale_record_stdout"][:300])

    missing = report["missing"]
    view = missing["view"] or {}
    capture_members = [name for name in missing["members"] if len(name) > 5 and name[:2] == "01" and name[2:4].isdigit() and name[4] == "."]
    add("returned clerk job is not a capture",
        missing["clerk_state"] == "returned" and missing["return_exit"] == 0 and capture_members == [],
        json.dumps({"state": missing["clerk_state"], "book_entries": missing["members"], "captures": capture_members}))
    add("missing capture does not look complete",
        view.get("pass_state") == "no-return" and view.get("pass_terminal") == "unknown"
        and view.get("goal_terminal") == "unknown" and view.get("latest_review") is None,
        json.dumps({"pass_state": view.get("pass_state"), "terminal": view.get("pass_terminal"),
                    "goal": view.get("goal_terminal")}))
    add("accepted review without a capture is refused",
        missing["accept_exit"] == 2 and "bound captured return" in missing["accept_stdout"] and missing["review_dirs"] == [],
        missing["accept_stdout"][:300])

    repeat = report["repeat"]
    add("identical clerk return writes nothing",
        repeat["again_exit"] == 0 and "already-recorded" in repeat["again_stdout"] and repeat["event_unchanged"],
        repeat["again_stdout"][:200])
    add("identical handoff retry keeps the receipt",
        repeat["retry_exit"] == 0 and repeat["completed_unchanged"] and repeat["receipt_unchanged"],
        repeat["retry_stdout"][:200])
    add("changed clerk bytes conflict and keep the event",
        repeat["conflict_exit"] == 2 and "delivery conflict" in repeat["conflict_stdout"]
        and repeat["event_unchanged_after_conflict"],
        repeat["conflict_stdout"][:200])
    add("changed capture bytes conflict and keep the receipt",
        repeat["recapture_exit"] == 2 and "conflict" in repeat["recapture_stdout"] and repeat["receipt_unchanged"],
        repeat["recapture_stdout"][:300])

    stale_job = report["stale_instruction"]
    add("stale instructions refuse the claim",
        stale_job["claim_exit"] == 2 and "instruction hash mismatch" in stale_job["claim_stdout"]
        and stale_job["claim_written"] is False,
        stale_job["claim_stdout"][:200])

    question = report["unresolved"]
    held = question["after"] or {}
    holds = held.get("holds") or []
    add("unresolved question remains after restart",
        question["record_stdout"].startswith("recorded") and question["after_text_has_question"]
        and holds and holds[0].get("status") == "unresolved" and QUESTION in held.get("unresolved", [])
        and held.get("pass_terminal") == "open" and held.get("goal_terminal") == "open"
        and question["elected"] is None,
        json.dumps({"record": question["record_stdout"][:160], "hold": holds[:1], "unresolved": held.get("unresolved")}))
    return found


def run_all() -> dict:
    report = {
        "schema": "desk-loop-replay/1",
        "label": "synthetic supplied judgments; disposable books; no model",
        "loop": case_loop(),
        "missing": case_missing(),
        "repeat": case_repeat(),
        "stale_instruction": case_stale_instruction(),
        "unresolved": case_unresolved(),
    }
    report["checks"] = checks_for(report)
    report["ok"] = all(item["ok"] for item in report["checks"])
    return report


def main() -> int:
    transcript = None
    if "--transcript" in sys.argv:
        transcript = Path(sys.argv[sys.argv.index("--transcript") + 1])
    report = run_all()
    if transcript is not None:
        transcript.parent.mkdir(parents=True, exist_ok=True)
        transcript.write_bytes((json.dumps(report, indent=1) + "\n").encode("utf-8"))
    failed = [item for item in report["checks"] if not item["ok"]]
    for item in report["checks"]:
        print(("ok  " if item["ok"] else "BAD ") + item["name"])
    if failed:
        for item in failed:
            print(item["detail"])
        return 1
    print(f"checks {len(report['checks'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
