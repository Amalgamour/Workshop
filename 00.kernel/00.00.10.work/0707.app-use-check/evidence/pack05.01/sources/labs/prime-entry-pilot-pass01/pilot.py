#!/usr/bin/env python3
"""Disposable first-use pilot for the pinned review-loop app entry.

Copies live member 0182 into a book outside D:\\Git\\lib-build. Reads the live
page. Writes neither. The supplied judgment is synthetic. It is not acceptance
and it is not a review of the 0519 design.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
PY = Path(sys.executable)
LIBRARIAN = ROOT / "app" / "librarian.py"
LAB = Path(__file__).resolve().parent
LIVE_BOOK = ROOT / "00.kernel" / "00.00.10.work"
LIVE_MEMBER = LIVE_BOOK / "0182.desk-app-integration-design-0501"
LIVE_PAGE = LIVE_BOOK / "0519.desk-app" / "05.01.md"
LAYOUT = LIVE_BOOK / "return-line-layout.json"
EVIDENCE = LIVE_BOOK / "0522.review-construction" / "evidence" / "build05.05"
MEMBER_NAME = "0182.desk-app-integration-design-0501"
DERIVED_MEMBER = "0119.desk-app"
PAGE_REL = "0519.desk-app/05.01.md"
ASSIGNMENT = b"Synthetic assignment. The copied return is the material.\n"
NOTE = b"Copied return bytes are the evidence file.\n"
PENDING_PAGE = (
    "Intro OUTSIDE-\u0394-TOKEN\n\n"
    "## Return pointer\n"
    "PENDING.\n\n"
    "## Review - Codex Prime\n"
    "PENDING.\n"
    "## Notes\n"
    "TAIL-\u0394-TOKEN\n"
).encode("utf-8")
SECTION_KEYS = [
    "return_result", "prime_finding", "within_direction", "next_bounded_action",
    "for_model", "issue", "consequences", "options", "recommendation", "question",
    "affected", "proposed_plan", "exploration", "assumptions", "open_questions",
    "outcome_evidence", "limits", "tests_note", "tests_passed", "learning",
    "preservation", "remaining_choices", "findings_account", "finish_assessments",
]

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"


class PilotError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def load_json(path: Path) -> dict:
    body = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(body, dict):
        raise PilotError(f"{path.name} is not an object")
    return body


def inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def fingerprint(path: Path) -> dict[str, str]:
    found: dict[str, str] = {}
    if path.is_file():
        found[path.name] = sha(path.read_bytes())
        return found
    for dirpath, dirnames, filenames in os.walk(path):
        dirnames[:] = sorted(name for name in dirnames if not (Path(dirpath) / name).is_symlink())
        for name in sorted(filenames):
            item = Path(dirpath) / name
            if item.is_symlink() or not item.is_file():
                continue
            found[item.relative_to(path).as_posix()] = sha(item.read_bytes())
    return found


def app(destination: Path, name: str, args: list[str], transcript: list[dict]) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [str(PY), "-B", str(LIBRARIAN), "review-loop", *args],
        cwd=str(ROOT),
        capture_output=True,
        env=env,
        shell=False,
    )
    (destination / f"{name}.stdout").write_bytes(proc.stdout)
    (destination / f"{name}.stderr").write_bytes(proc.stderr)
    transcript.append({
        "name": name,
        "args": ["review-loop", *args],
        "exit": proc.returncode,
    })
    return proc


def as_json(proc: subprocess.CompletedProcess, name: str) -> dict:
    try:
        body = json.loads(proc.stdout.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise PilotError(
            f"{name} stdout is not json (exit {proc.returncode}): "
            + proc.stderr.decode("utf-8", "replace")[:800]
        ) from exc
    if not isinstance(body, dict):
        raise PilotError(f"{name} stdout is not an object")
    return body


def source_row(path: str, data: bytes, kind: str, identity: dict) -> dict:
    digest = sha(data)
    return {
        "bind": False,
        "content_bytes": len(data),
        "content_sha256": digest,
        "identity": identity,
        "kind": kind,
        "logical_path": path,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": data.decode("utf-8"),
        "transport_bytes": len(data),
        "transport_sha256": digest,
    }


def sections_of(words: dict) -> dict:
    body = {key: None for key in SECTION_KEYS}
    supplied = words["record_judgment"]["sections_text"]
    for key, value in supplied.items():
        if key not in body:
            raise PilotError(f"supplied section {key} is not a review section")
        body[key] = value
    return body


def build_decision(book: Path, template: dict, words: dict, descriptor: dict) -> dict:
    record_judgment = {
        "outcome": words["record_judgment"]["outcome"],
        "finding": words["record_judgment"]["finding"],
        "reasons": list(words["record_judgment"]["reasons"]),
        "semantic_conflict": words["record_judgment"]["semantic_conflict"],
        "design_fork": words["record_judgment"]["design_fork"],
        "next_action": words["record_judgment"]["next_action"],
        "sections": sections_of(words),
    }
    goal = template["judgment"]["goal"]
    judgment = {
        "outcome": record_judgment["outcome"],
        "disposition": "accepted",
        "pass_terminal": "open",
        "goal": {
            "terminal": "open",
            "goal_id": goal["goal_id"],
            "goal_sha256": goal["goal_sha256"],
            "evidence": [],
        },
        "finding": record_judgment["finding"],
        "reasons": list(record_judgment["reasons"]),
        "source_refs": ["assignment.txt"],
        "next_action": {
            "action_id": "hand-template",
            "text": record_judgment["next_action"],
            "authorized_in_grant": False,
        },
        "unresolved": [],
        "semantic_conflict": record_judgment["semantic_conflict"],
        "design_fork": record_judgment["design_fork"],
        "holds": [],
        "answers": [],
        "sections": record_judgment["sections"],
    }
    return_path = descriptor["return_path"]
    receipt_path = descriptor["receipt_path"]
    return_bytes = (book / return_path).read_bytes()
    receipt_bytes = (book / receipt_path).read_bytes()
    registration = load_json(book / "registration.json")
    record = {
        "schema": "prime-review-record/1",
        "attribution": words["attribution"],
        "sources": [
            source_row("assignment.txt", (book / "assignment.txt").read_bytes(), "page", {"schema": "page-bytes/1"}),
            source_row(
                "note.md",
                (book / "note.md").read_bytes(),
                "supplied-text",
                {"schema": "supplied-text/1", "label": "SUPPLIED"},
            ),
            source_row(
                return_path,
                return_bytes,
                "capture",
                {
                    "schema": "return-capture/1",
                    "member": DERIVED_MEMBER,
                    "submission_id": "claude-0519-0501",
                    "receipt_sha256": sha(receipt_bytes),
                    "origin": {"book": "00.00.10.work", "page": "0519.desk-app", "batch": "05.01"},
                },
            ),
        ],
        "agreement": registration["agreement"],
        "holds": [],
        "answers": [],
        "review_passes": [],
        "gaps": [],
        "judgment": record_judgment,
    }
    decision = deepcopy(template)
    decision["attribution"] = words["attribution"]
    decision["judgment"] = judgment
    decision["supplied_record"] = record
    return decision


def make_book(page: bytes) -> Path:
    book = Path(tempfile.mkdtemp(prefix="pilot0505-"))
    if inside(book, ROOT) or inside(ROOT, book):
        shutil.rmtree(book, ignore_errors=True)
        raise PilotError("disposable book must stay outside D:\\Git\\lib-build")
    shutil.copytree(LIVE_MEMBER, book / MEMBER_NAME)
    copied = fingerprint(book / MEMBER_NAME)
    live = fingerprint(LIVE_MEMBER)
    if copied != live:
        raise PilotError("copied member does not match the live member")
    target = book / PAGE_REL
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(page)
    (book / "assignment.txt").write_bytes(ASSIGNMENT)
    (book / "note.md").write_bytes(NOTE)
    return book


def plant_request(book: Path, descriptor: dict) -> bytes:
    raw = dump(descriptor)
    (book / "descriptor.json").write_bytes(raw)
    (book / "registration.json").write_bytes((LAB / "example-registration.json").read_bytes())
    (book / "request.json").write_bytes((LAB / "example-request.json").read_bytes())
    return raw


def describe(destination: Path, book: Path, name: str, transcript: list[dict]) -> dict:
    proc = app(
        destination,
        name,
        ["describe-legacy", "--book", str(book), "--member", MEMBER_NAME],
        transcript,
    )
    body = as_json(proc, name)
    if proc.returncode != 0:
        raise PilotError(f"{name} exit {proc.returncode}")
    descriptor = body.get("descriptor")
    if not isinstance(descriptor, dict):
        raise PilotError(f"{name} did not return a descriptor")
    if body.get("state") != "complete":
        raise PilotError(f"{name} state is {body.get('state')}")
    if descriptor.get("custody_format") != "legacy-in-place/1":
        raise PilotError("copied member is not legacy-in-place/1")
    if descriptor.get("placement", {}).get("status") != "pending":
        raise PilotError("copied member placement is not pending")
    if descriptor.get("placement", {}).get("intended_target_page") != DERIVED_MEMBER:
        raise PilotError("intended line is not 0119.desk-app")
    if descriptor.get("submission_id") != "claude-0519-0501":
        raise PilotError("submission_id changed")
    origin = descriptor.get("origin")
    if origin != {"book": "00.00.10.work", "page": "0519.desk-app", "batch": "05.01"}:
        raise PilotError("origin changed")
    if body.get("task_association") != "not-established":
        raise PilotError("task association was claimed from custody records")
    if body.get("accepted") is not False or body.get("filing_claimed") is not False:
        raise PilotError("describe-legacy claimed acceptance or filing")
    return body


def prepare_record(destination: Path, book: Path, prefix: str, transcript: list[dict], words: dict) -> dict:
    prepared_proc = app(
        destination,
        f"{prefix}-prepare",
        ["prepare", "--fixture-root", str(book), "--request", "request.json"],
        transcript,
    )
    prepared = as_json(prepared_proc, f"{prefix}-prepare")
    if prepared_proc.returncode != 0:
        raise PilotError(prepared.get("rule") or prepared_proc.stderr.decode("utf-8", "replace")[:800])
    if prepared.get("full_success") is not False:
        raise PilotError("prepare claimed full_success")
    template = prepared.get("view", {}).get("template") if isinstance(prepared.get("view"), dict) else None
    if not isinstance(template, dict):
        raise PilotError("prepare did not offer a template: " + str(prepared.get("pass_state")))
    observation = prepared.get("observation") if isinstance(prepared.get("observation"), dict) else {}
    if observation.get("member") != DERIVED_MEMBER or observation.get("custody_member") != MEMBER_NAME:
        raise PilotError("prepare did not keep the derived line and the custody member apart")
    if observation.get("task_association") != "not-established":
        raise PilotError("prepare claimed task association")
    (destination / f"{prefix}-prepare-template.json").write_bytes(dump(template))
    descriptor = load_json(book / "descriptor.json")
    decision = build_decision(book, template, words, descriptor)
    (book / "decision.json").write_bytes(dump(decision))
    (destination / f"{prefix}-decision.json").write_bytes((book / "decision.json").read_bytes())
    recorded_proc = app(
        destination,
        f"{prefix}-record",
        ["record", "--fixture-root", str(book), "--request", "request.json", "--decision", "decision.json"],
        transcript,
    )
    recorded = as_json(recorded_proc, f"{prefix}-record")
    if recorded_proc.returncode != 0:
        raise PilotError(recorded.get("rule") or recorded_proc.stderr.decode("utf-8", "replace")[:800])
    if recorded.get("accepted") is not False:
        raise PilotError("record claimed accepted")
    return {"prepared": prepared, "recorded": recorded, "template": template}


def check_destination(text: str) -> Path:
    if not isinstance(text, str) or text.strip() == "":
        raise PilotError("destination is empty")
    if text.startswith("\\\\") or text.startswith("//"):
        raise PilotError("UNC path destination")
    dest = Path(text)
    if not dest.is_absolute() or ".." in dest.parts:
        raise PilotError("destination must be an absolute path without ..")
    if dest.exists():
        raise PilotError("destination exists and was not replaced")
    if not dest.parent.is_dir():
        raise PilotError("destination parent is absent")
    if not inside(dest, EVIDENCE) or os.path.normcase(os.path.abspath(dest)) == os.path.normcase(os.path.abspath(EVIDENCE)):
        raise PilotError("destination must be a new directory under evidence/build05.05")
    return dest


def run_pilot(destination: Path) -> dict:
    destination.mkdir()
    transcript: list[dict] = []
    before_member = fingerprint(LIVE_MEMBER)
    before_page = sha(LIVE_PAGE.read_bytes())
    layout_before = os.path.lexists(LAYOUT)
    words = load_json(LAB / "supplied-judgment.json")
    success = conflict = None
    try:
        success = make_book(PENDING_PAGE)
        described = describe(destination, success, "describe-legacy", transcript)
        descriptor_bytes = plant_request(success, described["descriptor"])
        (destination / "descriptor.json").write_bytes(descriptor_bytes)
        (destination / "registration.json").write_bytes((success / "registration.json").read_bytes())
        (destination / "request.json").write_bytes((success / "request.json").read_bytes())
        (destination / "real-decision-template.json").write_bytes((LAB / "real-decision-template.json").read_bytes())
        (destination / "supplied-judgment.json").write_bytes((LAB / "supplied-judgment.json").read_bytes())
        success_steps = prepare_record(destination, success, "success", transcript, words)
        (destination / "prepare-template.json").write_bytes(dump(success_steps["template"]))
        rendered_proc = app(
            destination,
            "success-render",
            ["render", "--fixture-root", str(success), "--request", "request.json"],
            transcript,
        )
        rendered = as_json(rendered_proc, "success-render")
        if rendered_proc.returncode != 0 or rendered.get("full_success") is not True:
            raise PilotError(rendered.get("rule") or "success render did not complete")
        if rendered.get("accepted") is not False or rendered.get("custody") != "not-established":
            raise PilotError("render claimed acceptance or custody")
        observed = rendered.get("observation") if isinstance(rendered.get("observation"), dict) else {}
        if observed.get("filing_claimed") is not False:
            raise PilotError("render claimed filing")
        read_proc = app(
            destination,
            "success-read",
            ["read", "--fixture-root", str(success), "--request", "request.json"],
            transcript,
        )
        read_back = as_json(read_proc, "success-read")
        if read_proc.returncode != 0 or read_back.get("pass_state") != "reviewed":
            raise PilotError("new-process read did not report reviewed")
        if read_back.get("full_success") is not True or read_back.get("accepted") is not False:
            raise PilotError("read claimed the wrong success flags")
        if read_back.get("observation", {}).get("task_association") != "not-established":
            raise PilotError("read claimed task association")
        page = (success / PAGE_REL).read_bytes()
        text = page.decode("utf-8")
        if "OUTSIDE-\u0394-TOKEN" not in text or "TAIL-\u0394-TOKEN" not in text:
            raise PilotError("render rewrote text outside the review section")
        if words["record_judgment"]["finding"] not in text:
            raise PilotError("rendered page does not show the supplied finding")
        if (success / "descriptor.json").read_bytes() != descriptor_bytes:
            raise PilotError("descriptor bytes changed after render")
        (destination / "sample-review.md").write_bytes(page)

        live_page = LIVE_PAGE.read_bytes()
        conflict = make_book(live_page)
        conflict_described = describe(destination, conflict, "conflict-describe", transcript)
        plant_request(conflict, conflict_described["descriptor"])
        prepare_record(destination, conflict, "conflict", transcript, words)
        conflict_proc = app(
            destination,
            "conflict-render",
            ["render", "--fixture-root", str(conflict), "--request", "request.json"],
            transcript,
        )
        conflict_body = as_json(conflict_proc, "conflict-render")
        render = conflict_body.get("render") if isinstance(conflict_body.get("render"), dict) else {}
        if conflict_proc.returncode != 2 or render.get("result") != "render-conflict":
            raise PilotError("substantive page was not a render-conflict")
        if (conflict / PAGE_REL).read_bytes() != live_page:
            raise PilotError("render-conflict changed the substantive page")
        partials = list((conflict / "partial").glob("*.md")) if (conflict / "partial").is_dir() else []
        if len(partials) != 1:
            raise PilotError(f"expected one partial, found {len(partials)}")
        (destination / "conflict-page.md").write_bytes(live_page)
        if LIVE_PAGE.read_bytes() != live_page:
            raise PilotError("live page bytes changed")
    finally:
        if success is not None:
            shutil.rmtree(success, ignore_errors=True)
        if conflict is not None:
            shutil.rmtree(conflict, ignore_errors=True)

    after_member = fingerprint(LIVE_MEMBER)
    after_page = sha(LIVE_PAGE.read_bytes())
    layout_after = os.path.lexists(LAYOUT)
    unchanged = before_member == after_member and before_page == after_page and layout_before is False and layout_after is False
    summary = {
        "schema": "review-loop-pilot-demo/1",
        "accepted": False,
        "custody": "not-established",
        "filing_claimed": False,
        "task_association": "not-established",
        "full_success": True,
        "live_review_completed": False,
        "source_member": MEMBER_NAME,
        "intended_member": DERIVED_MEMBER,
        "submission_id": "claude-0519-0501",
        "origin": {"book": "00.00.10.work", "page": "0519.desk-app", "batch": "05.01"},
        "fingerprints_unchanged": unchanged,
        "layout_created": layout_after and not layout_before,
        "conflict_result": "render-conflict",
        "conflict_page_unchanged": True,
        "partial_count": 1,
        "successor_renderer": False,
        "supplied_judgment": True,
        "note": "Mechanical demonstration on a disposable copy. This is not Prime's judgment and it is not a live review.",
    }
    (destination / "summary.json").write_bytes(dump(summary))
    (destination / "fingerprints.json").write_bytes(dump({
        "member_before": before_member,
        "member_after": after_member,
        "page_before": before_page,
        "page_after": after_page,
        "layout_before": layout_before,
        "layout_after": layout_after,
    }))
    (destination / "commands.json").write_bytes(dump({"steps": transcript}))
    if not unchanged:
        raise PilotError("watched live files changed during the pilot")
    return summary


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] != ["--destination"] or len(args) != 2:
        print("refused: pass --destination ABS for a new directory under evidence/build05.05", file=sys.stderr)
        return 2
    try:
        destination = check_destination(args[1])
        summary = run_pilot(destination)
    except PilotError as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2
    print("pilot-demo")
    print(f"destination: {destination}")
    print(f"read full_success: {summary['full_success']}")
    print(f"accepted: {summary['accepted']}")
    print(f"conflict: {summary['conflict_result']}")
    print(f"fingerprints_unchanged: {summary['fingerprints_unchanged']}")
    print("live_review_completed: false")
    return 0


if __name__ == "__main__":
    sys.exit(main())
