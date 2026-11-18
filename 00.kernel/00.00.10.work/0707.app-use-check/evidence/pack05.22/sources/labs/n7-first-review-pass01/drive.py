#!/usr/bin/env python3
"""Command record for 0521.return-placement/05.14.

This process follows evidence/build05.14/CONTRACT.md. It files one disposable
book with the pinned return-lines tool, then runs the staged N7 first-review
successor. It does not select the shared app, edit the active core, or rewrite
the known-failure stamp.
"""

from __future__ import annotations

import copy
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
PYTHON = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
LIVE_BOOK = REPO / "00.kernel" / "00.00.10.work"
DOOR_PAGE = LIVE_BOOK / "0100.band.returns" / "01.md"
LAB = REPO / "labs" / "n7-first-review-pass01"
WORKBOOK = LAB / "workbook.py"
LOOP = LAB / "review_loop.py"
CYCLE = LAB / "prime_cycle.py"
LINES = REPO / "labs" / "return-lines-pass04" / "return_lines.py"
ACCESS = REPO / "labs" / "return-access-pass01" / "return_access.py"
PASS02_LINES = REPO / "labs" / "return-lines-pass02" / "return_lines.py"
KNOWN = Path(r"D:\librarian\temp\0521-0514\known-failure")
SOURCE_STAMP = Path(r"D:\librarian\temp\0521-0513\20261103T214834952429Z")
N5 = "0521.connected-return-review"
N5_LINE = "0121.connected-return-review"
N7 = "0721.connected-local"
N7_REVIEW = f"{N7}/06.01.review.md"
LAYOUT_SHA = "2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804"
ACTION = "Prime remeasures the successor delta and decides whether to stage it into the shared cycle modules."
FINDING_N7 = "Supplied fixture judgment for 0721.connected-local. This is not an independent semantic review."
FINDING_N5 = "Supplied fixture judgment for 0521.connected-return-review. This is not an independent semantic review."
FILING_RELEASE = "synthetic fixture filing; not a Director release"
MANUAL = (
    "# Fixture page\n\n"
    "## Review - Codex Prime\n"
    "Director response: keep this sentence.\n"
).encode("utf-8")
SECTION_KEYS = (
    "affected",
    "assumptions",
    "consequences",
    "exploration",
    "findings_account",
    "finish_assessments",
    "for_model",
    "issue",
    "learning",
    "limits",
    "next_bounded_action",
    "open_questions",
    "options",
    "outcome_evidence",
    "preservation",
    "prime_finding",
    "proposed_plan",
    "question",
    "recommendation",
    "remaining_choices",
    "return_result",
    "tests_note",
    "tests_passed",
    "within_direction",
)
WATCH = (
    "labs/prime-cycle-pass03/prime_cycle.py",
    "labs/review-loop-pass03/review_loop.py",
    "labs/review-construction-pass02/construct.py",
    "labs/review-construction-pass04/construct.py",
    "labs/workbook-review-pass01/workbook.py",
    "labs/workbook-review-pass02/workbook.py",
    "labs/prime-review-pass01/prime_review.py",
    "labs/prime-review-pass02/prime_review.py",
    "labs/return-lines-pass01/return_lines.py",
    "labs/return-lines-pass02/return_lines.py",
    "labs/return-lines-pass04/return_lines.py",
    "labs/return-placement-pass01/return_placement.py",
    "labs/return-capture-pass01/return_inspect.py",
    "labs/return-access-pass01/return_access.py",
    "labs/connected-return-review-pass02/drive.py",
    "labs/n7-first-review-pass01/prime_cycle.py",
    "labs/n7-first-review-pass01/review_loop.py",
    "labs/n7-first-review-pass01/workbook.py",
    "labs/n7-first-review-pass01/drive.py",
    "app/librarian.py",
    "app/README.md",
    "00.kernel/00.00.10.work/0521.return-placement/05.14.md",
    "00.kernel/00.00.10.work/0521.return-placement/06.26.md",
    "00.kernel/00.00.10.work/0521.return-placement/06.27.md",
    "00.kernel/00.00.10.work/0521.return-placement/06.28.md",
    "00.kernel/00.00.10.work/0521.return-placement/evidence/build05.14/CONTRACT.md",
    "00.kernel/00.00.10.work/0521.return-placement/evidence/pack05.14/source-manifest.json",
)
SUCCESSOR_PINS = {
    "prime_cycle.py": ("b664c2c989a132108aa236ea6885e2503cf0dca266a12538ebe0b26cf9dba81d", 77501),
    "review_loop.py": ("fb0e1e32a33e25b0f36013fbca6231094fccda5f65491b8596320c8594c89fe4", 59229),
}

PROBLEMS: list[str] = []
COMMANDS: list[dict] = []
CASES: list[dict] = []
FIRST: dict | None = None
TOOLS = False
ENV = os.environ.copy()
ENV["PYTHONDONTWRITEBYTECODE"] = "1"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(body: dict) -> bytes:
    return (json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def identity(path: Path) -> dict | None:
    if not path.is_file():
        return None
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def problem(message: str, step: str | None = None) -> None:
    global FIRST
    line = message if step is None else f"{step}: {message}"
    PROBLEMS.append(line)
    if FIRST is None:
        FIRST = {"message": message, "step": step}


def writer_started_of(text: str) -> bool | None:
    for line in text.splitlines():
        if line == "writer_started: false":
            return False
        if line == "writer_started: true":
            return True
    return None


def leading_json(data: bytes) -> dict | None:
    try:
        value, _end = json.JSONDecoder().raw_decode(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def find_strings(value: object, key: str) -> list[str]:
    found = []
    if isinstance(value, dict):
        item = value.get(key)
        if isinstance(item, str):
            found.append(item)
        for child in value.values():
            found.extend(find_strings(child, key))
    elif isinstance(value, list):
        for child in value:
            found.extend(find_strings(child, key))
    return found


def source_page(title: str, goal: str, review_slot: bool) -> bytes:
    lines = [
        f"# {title}",
        "",
        "This page is handwritten fixture serialization.",
        "",
        "## Goal",
        "",
        goal,
        "",
    ]
    if review_slot:
        lines.extend(["## Review - Codex Prime", "PENDING.", ""])
    return ("\n".join(lines)).encode("utf-8")


def judgment(page: str, finding: str) -> dict:
    sections = {key: None for key in SECTION_KEYS}
    sections["return_result"] = (
        f"The disposable capture command wrote the {page} receipt. This sentence is supplied test data."
    )
    sections["prime_finding"] = "Supplied test data. This is not an independent semantic review."
    sections["within_direction"] = "The run stays on the disposable book."
    sections["next_bounded_action"] = ACTION
    return {
        "answers": [],
        "design_fork": None,
        "disposition": "accepted",
        "finding": finding,
        "findings": [],
        "gaps": ["agreement fields other than the measured goal were not in the source heading"],
        "goal_terminal": "open",
        "holds": [],
        "next_action": ACTION,
        "operation": "continue",
        "pass_terminal": "open",
        "reasons": [
            "The capture receipt was produced by the reviewed capture command.",
            "The judgment text is supplied test data.",
        ],
        "review_passes": [],
        "sections": sections,
        "semantic_conflict": None,
    }


def release_text() -> str:
    spec = importlib.util.spec_from_file_location("return_lines_pass02_release", PASS02_LINES)
    if spec is None or spec.loader is None:
        raise RuntimeError("pass02 did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    text = module.RELEASE_TEXT
    if not isinstance(text, str) or not text.startswith("Work in D:\\Git\\lib-build."):
        raise RuntimeError("pass02 release text did not load")
    return text


def predicted_layout() -> bytes:
    return dump({
        "allocation": "line-pass",
        "bands": {"5": "matched-workflow-return-line", "7": "page-local-colab"},
        "book": "00.00.10.work",
        "schema": "return-line-layout/1",
        "sequential_allocation": False,
    })


def watch_map() -> dict:
    found = {}
    for rel in WATCH:
        found[rel] = identity(REPO / rel)
    found["known-failure.json"] = identity(KNOWN / "known-failure.json")
    found["known-failure-prepare.stdout"] = identity(KNOWN / "prepare.stdout")
    found["known-failure-prepare.stderr"] = identity(KNOWN / "prepare.stderr")
    found["05.13-run-report.json"] = identity(SOURCE_STAMP / "run-report.json")
    return found


def preflight() -> None:
    layout = predicted_layout()
    if sha(layout) != LAYOUT_SHA or len(layout) != 216:
        problem("predicted layout hash does not match the contract", "preflight")
    sample = "The sealed field stored writer_started: false as a presence flag.\nwriter_started: false\n"
    if writer_started_of(sample) is not False:
        problem("writer_started parser did not return false for the exact line", "preflight")
    if writer_started_of("writer_started: false") is not False:
        problem("writer_started sample line was not false", "preflight")
    if writer_started_of("writer_started: true") is not True:
        problem("writer_started true line was not true", "preflight")
    if writer_started_of("prefix writer_started: false suffix") is not None:
        problem("writer_started substring was treated as a line", "preflight")
    for name, (digest, size) in SUCCESSOR_PINS.items():
        data = (LAB / name).read_bytes()
        if sha(data) != digest or len(data) != size or b"\r" in data:
            problem(f"successor pin does not match {name}", "preflight")
    workbook = WORKBOOK.read_bytes()
    if b"\r" in workbook or b"fb0e1e32a33e25b0f36013fbca6231094fccda5f65491b8596320c8594c89fe4" not in workbook:
        problem("workbook pin text does not name the review_loop hash", "preflight")
    if b"b664c2c989a132108aa236ea6885e2503cf0dca266a12538ebe0b26cf9dba81d" not in workbook:
        problem("workbook pin text does not name the prime_cycle hash", "preflight")
    if not (SOURCE_STAMP / "book" / N7_REVIEW).is_file():
        problem("05.13 stamp review file is absent", "preflight")
    if (LIVE_BOOK / "return-line-layout.json").exists():
        problem("live layout exists", "preflight")


def tool(step: str, script: Path, args: list[str], expect: set[int] | None, out: Path) -> dict:
    global TOOLS
    TOOLS = True
    proc = subprocess.run(
        [str(PYTHON), "-B", str(script), *args],
        cwd=str(REPO),
        capture_output=True,
        env=ENV,
    )
    write_bytes(out / f"{step}.stdout", proc.stdout)
    write_bytes(out / f"{step}.stderr", proc.stderr)
    COMMANDS.append({
        "exit": proc.returncode,
        "script": str(script.relative_to(REPO)).replace("\\", "/"),
        "step": step,
    })
    if expect is not None and proc.returncode not in expect:
        problem(f"exit {proc.returncode}, expected {sorted(expect)}", step)
    return {"exit": proc.returncode, "stderr": proc.stderr, "stdout": proc.stdout}


def auth_flags(paths: dict) -> list[str]:
    return [
        "--authorization", paths["auth"],
        "--audit", paths["audit"],
        "--plan", paths["plan"],
        "--backup", paths["backup"],
        "--staging", paths["staging"],
        "--retired", paths["retired"],
    ]


def add_case(name: str, ok: bool, detail: str, limit: str) -> None:
    CASES.append({"detail": detail, "limit": limit, "name": name, "ok": ok})
    if not ok:
        problem(detail, name)


def load_workbook():
    spec = importlib.util.spec_from_file_location("n7_workbook_driver", WORKBOOK)
    if spec is None or spec.loader is None:
        raise RuntimeError("successor workbook did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def arm(module, book: Path, source: str) -> None:
    module.wb._active_book = book
    address = module.wb.address_of(source, "05.01")
    module.wb._allowed_target = address.get("destination")


def view_of(payload: dict | None) -> dict:
    if not isinstance(payload, dict):
        return {}
    view = payload.get("view")
    return view if isinstance(view, dict) else {}


def token_of(payload: dict | None) -> dict | None:
    token = view_of(payload).get("write_token")
    if isinstance(token, dict):
        return token
    current = payload.get("current") if isinstance(payload, dict) else None
    if isinstance(current, dict) and isinstance(current.get("write_token"), dict):
        return current["write_token"]
    return None


def cycle_decision(module, template: dict, intake: dict, review_id: str, finding: str) -> dict:
    judgment_body = judgment(intake["page"], finding)
    statement = intake["goal_statement"].encode("utf-8")
    cycle_judgment = {
        "answers": judgment_body["answers"],
        "design_fork": judgment_body["design_fork"],
        "disposition": judgment_body["disposition"],
        "finding": judgment_body["finding"],
        "goal": {
            "evidence": [],
            "goal_id": "g1",
            "goal_sha256": module.wb.sha256_bytes(statement),
            "terminal": judgment_body["goal_terminal"],
        },
        "holds": judgment_body["holds"],
        "next_action": {"action_id": "next", "authorized_in_grant": None, "text": judgment_body["next_action"]},
        "outcome": judgment_body["operation"],
        "pass_terminal": judgment_body["pass_terminal"],
        "reasons": judgment_body["reasons"],
        "sections": judgment_body["sections"],
        "semantic_conflict": judgment_body["semantic_conflict"],
        "source_refs": [intake["assignment_path"]] if intake["assignment_path"] else [],
        "unresolved": list(judgment_body["gaps"]),
    }
    supplied = module.prime_record(intake, judgment_body, None)
    decision = copy.deepcopy(template)
    decision["review_id"] = f"{intake['pass']}-{review_id}"
    decision["attribution"] = supplied["attribution"]
    decision["judgment"] = cycle_judgment
    decision["supplied_record"] = supplied
    return decision


def direct_prepare(module, book: Path, source: str, review_id: str, out: Path, step: str) -> dict:
    arm(module, book, source)
    intake = module.build_intake(book, source, "05.01")
    paths = module.write_cycle_inputs(book, intake, review_id)
    result = tool(
        step,
        LOOP,
        ["prepare", "--fixture-root", str(book), "--request", paths["request"]],
        None,
        out,
    )
    return {"body": leading_json(result["stdout"]), "intake": intake, "paths": paths, "run": result}


def workbook_cycle(book: Path, source: str, finding: str, prefix: str, out: Path, inputs: Path) -> dict:
    judgment_path = inputs / f"judgment-{prefix}.json"
    write_bytes(judgment_path, dump(judgment(source, finding)))
    prepared = tool(
        f"{prefix}-prepare",
        WORKBOOK,
        ["prepare", "--book", str(book), "--source", source, "--pass", "05.01"],
        {0},
        out,
    )
    formed = tool(
        f"{prefix}-form",
        WORKBOOK,
        ["form", "--book", str(book), "--source", source, "--pass", "05.01"],
        {0},
        out,
    )
    form_body = leading_json(formed["stdout"])
    intake_ids = [item for item in find_strings(form_body, "intake_id") if len(item) == 64]
    intake = intake_ids[0] if intake_ids else ""
    if len(intake) != 64:
        problem("form did not return an intake id", f"{prefix}-form")
    recorded = tool(
        f"{prefix}-record",
        WORKBOOK,
        ["record", "--book", str(book), "--source", source, "--pass", "05.01", "--intake", intake, "--judgment", str(judgment_path)],
        None,
        out,
    )
    record_body = leading_json(recorded["stdout"])
    review_ids = [
        item for item in find_strings(record_body, "review_id")
        if len(item) == 17 and item.startswith("w")
    ]
    review = review_ids[0] if review_ids else ""
    return {
        "form_exit": formed["exit"],
        "intake_id": intake,
        "prepare_exit": prepared["exit"],
        "record": record_body,
        "record_exit": recorded["exit"],
        "review_id": review,
    }


def main() -> int:
    preflight()
    if PROBLEMS:
        print("\n".join(PROBLEMS), file=sys.stderr)
        return 2
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    root = Path(r"D:\librarian\temp\0521-0514") / stamp
    book = root / "book"
    out = root / "out"
    inputs = root / "inputs"
    for path in (book, out, inputs, root / "backup", root / "staging", root / "retired", root / "audit", root / "plan", root / "auth", root / "copies"):
        path.mkdir(parents=True)
    before = watch_map()
    head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "HEAD"], capture_output=True, text=True, env=ENV)
    branch = subprocess.run(["git", "-C", str(REPO), "branch", "--show-current"], capture_output=True, text=True, env=ENV)
    text = release_text()
    layout = predicted_layout()
    audit_path = root / "audit" / "audit.json"
    plan_path = root / "plan" / "plan.json"
    write_bytes(audit_path, dump({"files": [], "records": []}))
    tool("01-plan", LINES, ["plan", "--book", str(book), "--audit", str(audit_path), "--out", str(plan_path)], {0}, out)
    auth_path = root / "auth" / "authorization.json"
    write_bytes(auth_path, dump({
        "audit_bytes": audit_path.stat().st_size,
        "audit_sha256": sha(audit_path.read_bytes()),
        "backup_root": str(root / "backup"),
        "book": "00.00.10.work",
        "book_path": str(book),
        "executor": "Codex Prime",
        "layout_sha256": sha(layout),
        "operations": ["capture", "init", "preflight", "reserve"],
        "plan_sha256": sha(plan_path.read_bytes()) if plan_path.is_file() else "",
        "release": text,
        "retired_root": str(root / "retired"),
        "schema": "return-line-authorization/1",
        "staging_root": str(root / "staging"),
        "synthetic": True,
    }))
    paths = {
        "audit": str(audit_path),
        "auth": str(auth_path),
        "backup": str(root / "backup"),
        "plan": str(plan_path),
        "retired": str(root / "retired"),
        "staging": str(root / "staging"),
    }
    tool("02-init", LINES, ["init", "--book", str(book), "--name", "00.00.10.work", *auth_flags(paths)], {0}, out)
    layout_path = book / "return-line-layout.json"
    if not layout_path.is_file() or layout_path.read_bytes() != layout or sha(layout_path.read_bytes()) != LAYOUT_SHA:
        problem("init did not write the predicted layout", "02-init")
    write_bytes(book / "0100.band.returns" / "01.md", DOOR_PAGE.read_bytes())
    write_bytes(book / N5 / "05.01.md", source_page(
        f"{N5} 05.01",
        "File this disposable pass on its matching return line and review the filed bytes.",
        True,
    ))
    write_bytes(book / N7 / "05.01.pack.md", source_page(
        f"{N7} 05.01",
        "Keep this page-local pack on its own page.",
        False,
    ))
    n5_return = inputs / "05.01.return.md"
    n5_note = inputs / "05.01.note.txt"
    n7_return = inputs / "n7.return.md"
    n7_note = inputs / "n7.note.txt"
    write_bytes(n5_return, b"Disposable return body for 05.01.\n")
    write_bytes(n5_note, b"fixture note 05.01\n")
    write_bytes(n7_return, b"Disposable page-local return body.\n")
    write_bytes(n7_note, b"fixture note n7\n")

    def line(step: str, args: list[str], expect: set[int]) -> dict:
        return tool(step, LINES, [*args, *auth_flags(paths)], expect, out)

    line("03-reserve-n5", [
        "reserve", "--book", str(book), "--page", N5, "--batch", "05.01",
        "--submission", "s0514a", "--output", "note.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", FILING_RELEASE,
    ], {1})
    line("04-capture-n5", [
        "capture", "--book", str(book), "--page", N5, "--batch", "05.01",
        "--submission", "s0514a", "--return-file", str(n5_return),
        "--artifact", "note.txt", str(n5_note),
    ], {0})
    line("05-reserve-n7", [
        "reserve", "--book", str(book), "--page", N7, "--batch", "05.01",
        "--submission", "s0514n7", "--output", "note.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", FILING_RELEASE,
    ], {1})
    line("06-capture-n7", [
        "capture", "--book", str(book), "--page", N7, "--batch", "05.01",
        "--submission", "s0514n7", "--return-file", str(n7_return),
        "--artifact", "note.txt", str(n7_note),
    ], {0})
    if (book / "0121.connected-local").exists():
        problem("N7 filing created 0121.connected-local", "06-capture-n7")
    n5_receipt = book / N5_LINE / "05.01.custody" / "receipt.json"
    n7_receipt = book / N7 / "05.01.custody" / "receipt.json"
    n5_receipt_sha = identity(n5_receipt)
    n7_receipt_sha = identity(n7_receipt)
    if n5_receipt_sha is None or n7_receipt_sha is None:
        problem("capture did not leave both receipts", "06-capture-n7")
    verified_n7 = tool("07-verify-n7", ACCESS, ["verify", "--book", str(book), "--source", N7, "--pass", "05.01"], {0}, out)
    verified_n5 = tool("07-verify-n5", ACCESS, ["verify", "--book", str(book), "--source", N5, "--pass", "05.01"], {0}, out)
    for label, result in (("07-verify-n7", verified_n7), ("07-verify-n5", verified_n5)):
        body = leading_json(result["stdout"])
        if body is None or body.get("state") != "complete":
            problem("access verify state was not complete", label)
    if (book / N7_REVIEW).exists():
        problem("N7 review existed before the successor cycle", "08-n7-prepare")
    shutil.copytree(book, root / "copies" / "filed")

    n7 = workbook_cycle(book, N7, FINDING_N7, "08-n7", out, inputs)
    record_body = n7["record"] if isinstance(n7["record"], dict) else {}
    if n7["record_exit"] != 0 or record_body.get("mode") != "cycle-committed":
        problem(f"N7 record mode was {record_body.get('mode')}", "08-n7-record")
    if (book / N7_REVIEW).exists():
        problem("N7 review existed before authorized render", "08-n7-record")
    if record_body.get("closes_work") is True or record_body.get("releases_action") is True:
        problem("N7 record released work or action", "08-n7-record")
    review_id = n7["review_id"]
    # Record stores the body beside record.json, under reviews/{review_id}.
    rendered_path = book / "workbook-review" / N7 / "05.01" / "reviews" / review_id / "rendered.md"
    rendered_bytes = rendered_path.read_bytes() if rendered_path.is_file() else b""
    write_bytes(out / "n7-rendered.md", rendered_bytes)
    rendered_text = rendered_bytes.decode("utf-8", "replace")
    if FINDING_N7 not in rendered_text or ACTION not in rendered_text:
        problem("full rendered read did not contain the supplied finding and next action", "08-n7-rendered")
    if "authority: none" not in rendered_text or "closes_work: false" not in rendered_text or "releases_action: false" not in rendered_text:
        problem("rendered read did not keep the authority bounds", "08-n7-rendered")
    request_rel = ""
    request_path = book / "workbook-review" / N7 / "05.01" / review_id / "cycle" / "request.json"
    if request_path.is_file():
        request_rel = request_path.relative_to(book).as_posix()
    else:
        problem("N7 cycle request was not stored", "08-n7-record")
    read_before = tool("09-n7-cycle-read", LOOP, ["read", "--fixture-root", str(book), "--request", request_rel], {0}, out)
    token = token_of(leading_json(read_before["stdout"]))
    if token is None or token.get("state") != "absent-create" or token.get("sha256") is not None or token.get("path") != N7_REVIEW:
        problem("committed read did not keep the absent-create token", "09-n7-cycle-read")
    shutil.copytree(book, root / "copies" / "recorded")
    published = tool(
        "10-n7-publish",
        WORKBOOK,
        ["publish", "--book", str(book), "--source", N7, "--pass", "05.01", "--review", review_id],
        {0},
        out,
    )
    publish_body = leading_json(published["stdout"])
    page = book / N7_REVIEW
    page_bytes = page.read_bytes() if page.is_file() else b""
    page_text = page_bytes.decode("utf-8", "replace")
    write_bytes(out / "n7-review.md", page_bytes)
    created = (
        page.is_file()
        and publish_body is not None
        and publish_body.get("published") is True
        and FINDING_N7 in page_text
        and ACTION in page_text
        and "authority: none" in page_text
        and "closes_work: false" in page_text
        and "releases_action: false" in page_text
        and "authenticates_actor: false" in page_text
        and "task_binding: " in page_text
    )
    if not created:
        problem("authorized render did not create the bounded N7 review", "10-n7-publish")
    page_id = identity(page)
    if identity(n7_receipt) != n7_receipt_sha:
        problem("N7 review changed the capture receipt", "10-n7-publish")
    tool("11-n7-read", WORKBOOK, ["read", "--book", str(book), "--source", N7, "--pass", "05.01"], {0}, out)
    tool("11-n7-recover", WORKBOOK, ["recover", "--book", str(book), "--source", N7, "--pass", "05.01"], {0}, out)
    rendered_again = tool("11-n7-render", LOOP, ["render", "--fixture-root", str(book), "--request", request_rel], {0}, out)
    again_body = leading_json(rendered_again["stdout"])
    again_render = again_body.get("render") if isinstance(again_body, dict) else None
    if not isinstance(again_render, dict) or again_render.get("result") != "already-rendered":
        problem("new-process render did not report already-rendered", "11-n7-render")
    if identity(page) != page_id:
        problem("new-process render changed the review bytes", "11-n7-render")
    read_after = tool("11-n7-cycle-read", LOOP, ["read", "--fixture-root", str(book), "--request", request_rel], {0}, out)
    after_view = view_of(leading_json(read_after["stdout"]))
    if after_view.get("pass_state") != "reviewed" or after_view.get("render_state") != "rendered":
        problem("new-process read did not report the rendered review", "11-n7-cycle-read")
    live_token = token_of(leading_json(read_after["stdout"]))
    if not isinstance(live_token, dict) or "state" in live_token or live_token.get("sha256") != (page_id or {}).get("sha256"):
        problem("live token after create was not the file hash", "11-n7-cycle-read")
    add_case(
        "absent-target",
        bool(created and isinstance(token, dict) and token.get("state") == "absent-create"),
        "first N7 review was created only at authorized render" if created else "authorized render did not create the bounded review",
        "This case does not release the action, accept the pack, or cover a second review on the same page.",
    )

    n5 = workbook_cycle(book, N5, FINDING_N5, "12-n5", out, inputs)
    n5_body = n5["record"] if isinstance(n5["record"], dict) else {}
    if n5["record_exit"] != 0 or n5_body.get("mode") != "cycle-committed":
        problem(f"N5 record mode was {n5_body.get('mode')}", "12-n5-record")
    n5_request = book / "workbook-review" / N5 / "05.01" / n5["review_id"] / "cycle" / "request.json"
    n5_request_rel = n5_request.relative_to(book).as_posix() if n5_request.is_file() else ""
    n5_read = tool("12-n5-cycle-read", LOOP, ["read", "--fixture-root", str(book), "--request", n5_request_rel], {0}, out)
    n5_token = token_of(leading_json(n5_read["stdout"]))
    if not isinstance(n5_token, dict) or "state" in n5_token or not isinstance(n5_token.get("sha256"), str):
        problem("N5 token did not stay a present-file hash", "12-n5-cycle-read")
    tool(
        "12-n5-publish",
        WORKBOOK,
        ["publish", "--book", str(book), "--source", N5, "--pass", "05.01", "--review", n5["review_id"]],
        {0},
        out,
    )
    n5_page = (book / N5 / "05.01.md").read_text(encoding="utf-8") if (book / N5 / "05.01.md").is_file() else ""
    if "closes_work: false" not in n5_page or "releases_action: false" not in n5_page or "authority: none" not in n5_page:
        problem("N5 published page did not keep the authority bounds", "12-n5-publish")
    replay = tool(
        "13-n5-replay",
        WORKBOOK,
        ["record", "--book", str(book), "--source", N5, "--pass", "05.01", "--intake", n5["intake_id"], "--judgment", str(inputs / "judgment-12-n5.json")],
        {0},
        out,
    )
    replay_body = leading_json(replay["stdout"])
    replay_ok = (
        isinstance(replay_body, dict)
        and replay_body.get("already_recorded") is True
        and identity(n5_receipt) == n5_receipt_sha
        and isinstance(n5_token, dict)
        and "state" not in n5_token
    )
    if not replay_ok:
        problem("N5 replay changed the receipt or the token shape", "13-n5-replay")
    add_case(
        "n5-replay",
        replay_ok,
        "N5 replay stayed cycle-committed on the existing file hash",
        "cycle-committed is the tool mode. It is not acceptance.",
    )

    try:
        module = load_workbook()
    except Exception as exc:
        problem(f"{type(exc).__name__}: {exc}", "hostile")
        module = None
    filed = root / "copies" / "filed"
    recorded = root / "copies" / "recorded"

    try:
        def clone(name: str, source: Path) -> Path:
            dest = root / "copies" / name
            shutil.copytree(source, dest)
            return dest

        manual_book = clone("manual", filed)
        manual_path = manual_book / N7_REVIEW
        write_bytes(manual_path, MANUAL)
        before_manual = manual_path.read_bytes()
        manual = workbook_cycle(manual_book, N7, FINDING_N7, "14-manual", out, inputs)
        manual_published = tool(
            "14-manual-publish",
            WORKBOOK,
            ["publish", "--book", str(manual_book), "--source", N7, "--pass", "05.01", "--review", manual["review_id"]],
            None,
            out,
        )
        manual_body = leading_json(manual_published["stdout"])
        manual_ok = (
            manual_path.read_bytes() == before_manual
            and b"Director response: keep this sentence." in manual_path.read_bytes()
            and (manual_body or {}).get("published") is not True
        )
        add_case(
            "manual-director",
            manual_ok,
            "existing Director text was kept" if manual_ok else f"manual publish changed the file or published it: {(manual_body or {}).get('correction')}",
            "The kept text is fixture Director text. This run does not approve it.",
        )

        planted = b"planted after prepare\n"
        after_book = clone("after-prepare", filed)
        prepared_after = direct_prepare(module, after_book, N7, "w0514after01", out, "15-after-prepare")
        after_template = view_of(prepared_after["body"]).get("template")
        after_path = after_book / N7_REVIEW
        write_bytes(after_path, planted)
        after_decision = {}
        if isinstance(after_template, dict):
            after_decision = cycle_decision(module, after_template, prepared_after["intake"], "w0514after01", FINDING_N7)
            decision_path = after_book / prepared_after["paths"]["decision"]
            write_bytes(decision_path, dump(after_decision))
            refused = tool(
                "15-after-record",
                LOOP,
                ["record", "--fixture-root", str(after_book), "--request", prepared_after["paths"]["request"], "--decision", prepared_after["paths"]["decision"]],
                None,
                out,
            )
            rule = (leading_json(refused["stdout"]) or {}).get("rule") or refused["stderr"].decode("utf-8", "replace")
        else:
            refused = {"exit": prepared_after["run"]["exit"]}
            rule = "prepare did not return a template"
        after_ok = after_path.read_bytes() == planted and refused["exit"] != 0 and "target appeared after read" in rule
        add_case(
            "created-after-prepare",
            after_ok,
            "record refused a file that appeared after prepare" if after_ok else rule[:500],
            "The planted file was left in place.",
        )

        foreign_book = clone("foreign", filed)
        foreign = direct_prepare(module, foreign_book, N7, "w0514foreign", out, "16-foreign-prepare")
        foreign_reg = foreign_book / foreign["paths"]["registration"]
        foreign_body = json.loads(foreign_reg.read_text(encoding="utf-8"))
        foreign_body["target"] = f"{N7}/99.foreign.md"
        write_bytes(foreign_reg, dump(foreign_body))
        foreign_run = tool(
            "16-foreign-reread",
            LOOP,
            ["prepare", "--fixture-root", str(foreign_book), "--request", foreign["paths"]["request"]],
            None,
            out,
        )
        foreign_rule = (leading_json(foreign_run["stdout"]) or {}).get("rule") or foreign_run["stderr"].decode("utf-8", "replace")
        foreign_ok = (
            foreign_run["exit"] != 0
            and "derived review destination" in foreign_rule
            and not (foreign_book / N7_REVIEW).exists()
            and not (foreign_book / N7 / "99.foreign.md").exists()
        )
        add_case(
            "foreign-target",
            foreign_ok,
            "a foreign registration target was refused" if foreign_ok else foreign_rule[:500],
            "No output path other than the derived N7 review is accepted.",
        )

        malformed_book = clone("malformed", filed)
        malformed = direct_prepare(module, malformed_book, N7, "w0514malform", out, "17-malformed-prepare")
        malformed_reg = malformed_book / malformed["paths"]["registration"]
        malformed_body = json.loads(malformed_reg.read_text(encoding="utf-8"))
        malformed_body["target"] = f"{N7}/../06.01.review.md"
        write_bytes(malformed_reg, dump(malformed_body))
        malformed_run = tool(
            "17-malformed-reread",
            LOOP,
            ["prepare", "--fixture-root", str(malformed_book), "--request", malformed["paths"]["request"]],
            None,
            out,
        )
        malformed_rule = (leading_json(malformed_run["stdout"]) or {}).get("rule") or malformed_run["stderr"].decode("utf-8", "replace")
        malformed_ok = malformed_run["exit"] != 0 and not (malformed_book / N7_REVIEW).exists() and "unsafe path" in malformed_rule
        add_case(
            "malformed-target",
            malformed_ok,
            "a malformed target path was refused" if malformed_ok else malformed_rule[:500],
            "The refusal is the path check. It is not a new naming rule.",
        )

        token_book = clone("token-path", filed)
        token_prep = direct_prepare(module, token_book, N7, "w0514token01", out, "18-token-prepare")
        token_template = view_of(token_prep["body"]).get("template")
        token_rule = "prepare did not return a template"
        token_run = {"exit": token_prep["run"]["exit"]}
        if isinstance(token_template, dict):
            token_decision = cycle_decision(module, token_template, token_prep["intake"], "w0514token01", FINDING_N7)
            token_decision["binding"]["write_token"]["path"] = f"{N7}/99.foreign.md"
            write_bytes(token_book / token_prep["paths"]["decision"], dump(token_decision))
            token_run = tool(
                "18-token-record",
                LOOP,
                ["record", "--fixture-root", str(token_book), "--request", token_prep["paths"]["request"], "--decision", token_prep["paths"]["decision"]],
                None,
                out,
            )
            token_rule = (leading_json(token_run["stdout"]) or {}).get("rule") or token_run["stderr"].decode("utf-8", "replace")
        token_ok = (
            token_run["exit"] != 0
            and "derived destination" in token_rule
            and not (token_book / N7_REVIEW).exists()
            and not (token_book / N7 / "99.foreign.md").exists()
        )
        add_case(
            "decision-token-path",
            token_ok,
            "a decision token for another path was refused" if token_ok else token_rule[:500],
            "The bound path must equal the registration's derived destination.",
        )

        forge_book = clone("n5-forge", filed)
        forge = direct_prepare(module, forge_book, N5, "w0514n5forge", out, "19-n5-forge-prepare")
        forge_page = forge_book / N5 / "05.01.md"
        forge_template = view_of(forge["body"]).get("template")
        forge_rule = ""
        forge_record_exit = 0
        if isinstance(forge_template, dict):
            forge_decision = cycle_decision(module, forge_template, forge["intake"], "w0514n5forge", FINDING_N5)
            write_bytes(forge_book / forge["paths"]["decision"], dump(forge_decision))
        else:
            forge_rule = "prepare did not return a template while the N5 page existed"
        if forge_page.is_file():
            forge_page.unlink()
        forge_again = tool(
            "19-n5-forge-reread",
            LOOP,
            ["prepare", "--fixture-root", str(forge_book), "--request", forge["paths"]["request"]],
            None,
            out,
        )
        forge_token = token_of(leading_json(forge_again["stdout"]))
        if isinstance(forge_template, dict):
            forge_record = tool(
                "19-n5-forge-record",
                LOOP,
                ["record", "--fixture-root", str(forge_book), "--request", forge["paths"]["request"], "--decision", forge["paths"]["decision"]],
                None,
                out,
            )
            forge_rule = (leading_json(forge_record["stdout"]) or {}).get("rule") or forge_record["stderr"].decode("utf-8", "replace")
            forge_record_exit = forge_record["exit"]
        forge_ok = forge_token is None and forge_record_exit != 0 and not forge_page.exists()
        add_case(
            "forged-n5-absent-create",
            forge_ok,
            "N5 absence stayed a null token and created no file" if forge_ok else forge_rule[:500],
            "N5 does not receive the absent-create state.",
        )

        directory_book = clone("directory", recorded)
        directory_path = directory_book / N7_REVIEW
        directory_path.mkdir(parents=True)
        directory_run = tool(
            "20-directory-publish",
            WORKBOOK,
            ["publish", "--book", str(directory_book), "--source", N7, "--pass", "05.01", "--review", review_id],
            None,
            out,
        )
        directory_body = leading_json(directory_run["stdout"])
        directory_rule = (directory_body or {}).get("correction") or directory_run["stderr"].decode("utf-8", "replace")
        directory_ok = directory_path.is_dir() and not directory_path.is_file() and directory_run["exit"] != 0 and "not a regular file" in directory_rule
        add_case(
            "directory-target",
            directory_ok,
            "a directory at the destination was left in place" if directory_ok else directory_rule[:500],
            "The directory was not deleted and was not replaced.",
        )

        link_book = clone("link", recorded)
        link_path = link_book / N7_REVIEW
        link_target = link_book / "link-target.txt"
        write_bytes(link_target, b"link target bytes\n")
        link_case = {"ok": False, "detail": "", "skipped": False}
        try:
            os.symlink(link_target, link_path)
        except OSError as exc:
            winerror = getattr(exc, "winerror", None)
            link_case = {
                "detail": f"symlink skipped: WinError {winerror}" if winerror is not None else f"symlink skipped: {exc}",
                "ok": True,
                "skipped": True,
            }
        else:
            link_before = link_target.read_bytes()
            link_run = tool(
                "21-link-publish",
                WORKBOOK,
                ["publish", "--book", str(link_book), "--source", N7, "--pass", "05.01", "--review", review_id],
                None,
                out,
            )
            link_body = leading_json(link_run["stdout"])
            link_rule = (link_body or {}).get("correction") or link_run["stderr"].decode("utf-8", "replace")
            link_ok = link_path.is_symlink() and link_target.read_bytes() == link_before and link_run["exit"] != 0 and "not a regular file" in link_rule
            link_case = {"detail": "link target was refused and left in place" if link_ok else link_rule[:500], "ok": link_ok, "skipped": False}
        add_case("link-target", link_case["ok"], link_case["detail"], "A missing privilege is recorded as a skip. It is not a successful link proof.")

        temp_book = clone("temp", recorded)
        temp_path = temp_book / N7 / "06.01.review.md.review-construct.tmp"
        temp_bytes = b"partial construct\n"
        write_bytes(temp_path, temp_bytes)
        temp_run = tool(
            "22-temp-publish",
            WORKBOOK,
            ["publish", "--book", str(temp_book), "--source", N7, "--pass", "05.01", "--review", review_id],
            None,
            out,
        )
        temp_body = leading_json(temp_run["stdout"])
        temp_rule = (temp_body or {}).get("correction") or temp_run["stderr"].decode("utf-8", "replace")
        rendered_marker = list((temp_book / "workbook-review").rglob("rendered.json")) if (temp_book / "workbook-review").exists() else []
        temp_ok = (
            temp_path.read_bytes() == temp_bytes
            and not (temp_book / N7_REVIEW).exists()
            and temp_run["exit"] != 0
            and rendered_marker == []
            and "review-construct.tmp" in temp_rule
        )
        add_case(
            "interrupted-create",
            temp_ok,
            "the constructor temporary was kept and was not marked complete" if temp_ok else temp_rule[:500],
            "Exclusive create is O_EXCL plus rename. It is not a power-loss or multiwriter guarantee.",
        )

        changed_book = clone("return-changed", recorded)
        changed_return = changed_book / N7 / "05.01.return.md"
        changed_return.write_bytes(changed_return.read_bytes() + b"changed after record\n")
        changed_run = tool(
            "23-return-changed",
            WORKBOOK,
            ["publish", "--book", str(changed_book), "--source", N7, "--pass", "05.01", "--review", review_id],
            None,
            out,
        )
        changed_body = leading_json(changed_run["stdout"])
        changed_rule = (changed_body or {}).get("correction") or ""
        changed_ok = (
            changed_run["exit"] != 0
            and not (changed_book / N7_REVIEW).exists()
            and "source changed" in changed_rule
        )
        add_case(
            "return-changed-after-record",
            changed_ok,
            "publication stopped after the return bytes changed" if changed_ok else changed_rule[:500],
            "The changed return was left in place. The review file was not created.",
        )

    except Exception as exc:
        problem(f"{type(exc).__name__}: {exc}", "hostile")

    after = watch_map()
    changed_core = [rel for rel in WATCH if before.get(rel) != after.get(rel)]
    if changed_core:
        problem("watched bytes changed during the run: " + ", ".join(changed_core), "watch")
    if (LIVE_BOOK / "return-line-layout.json").exists():
        problem("live layout exists after the run", "watch")
    if not (SOURCE_STAMP / "book" / N7_REVIEW).is_file():
        problem("05.13 stamp review file changed", "watch")
    known_same = (
        before.get("known-failure.json") == after.get("known-failure.json")
        and before.get("known-failure-prepare.stdout") == after.get("known-failure-prepare.stdout")
        and before.get("05.13-run-report.json") == after.get("05.13-run-report.json")
    )
    if not known_same:
        problem("known failure or the 05.13 report changed", "watch")

    report = {
        "accepted": False,
        "action_released": False,
        "activated": False,
        "allocated_0184": False,
        "allocator": "not-used",
        "app_selected": False,
        "app_selection_applied": False,
        "approved": False,
        "authority": "not-assessed",
        "branch": branch.stdout.strip(),
        "capture_slot": None,
        "cases": CASES,
        "commands": COMMANDS,
        "committed": False,
        "contract_revised_after_commands": False,
        "custody": "pending",
        "date": "2026-11-03",
        "director_release": False,
        "driver_exit_problems": len(PROBLEMS),
        "executor": "Grok-2",
        "first": FIRST,
        "head": head.stdout.strip(),
        "known_failure": before.get("known-failure.json"),
        "retained_first_failure": {
            "cause": "prime_review report without --root refused N7 sources marked bind true",
            "stamp": "20261103T225239321284Z",
            "step": "08-n7-record",
        },
        "retained_measurement_miss": {
            "cause": "the driver read workbook-review/{page}/{pass}/{review_id}/rendered.md; record stores reviews/{review_id}/rendered.md",
            "stamp": "20261103T225847465645Z",
            "step": "08-n7-rendered",
        },
        "launcher_is_portable_copy": False,
        "layout_sha256": LAYOUT_SHA,
        "limits": [
            "Driver exit 0 is the empty problem list. It is Prime review on neither page.",
            "The supplied judgment disposition accepted is test data.",
            "N7 file creation is the authorized render of one derived review. It is not Director release.",
            "N5 cycle-committed is the tool mode. It is not acceptance.",
            "Exclusive create keeps a partial temporary. It does not guarantee power loss, multiwriter safety, or AR-01.",
            "The launcher loads pinned live tools. It is not a portable copy.",
            "Matching custody for 0121.return-placement stays pending.",
            "writer_started is the exact child line, and the sample line is false.",
        ],
        "live_layout_exists": False,
        "matching_line": "0121.return-placement",
        "n5_receipt": n5_receipt_sha,
        "n5_replay_ok": replay_ok,
        "n5_token_has_state": isinstance(n5_token, dict) and "state" in n5_token,
        "n7_page": page_id,
        "n7_receipt": n7_receipt_sha,
        "n7_rendered": identity(out / "n7-rendered.md"),
        "n7_review_created": created,
        "n7_review_id": review_id,
        "n7_token_before_render": token,
        "not_covered": [
            "power loss beyond the retained temporary",
            "multiwriter races",
            "AR-01",
            "live migration",
            "shared route selection",
            "a second review on the same N7 page",
        ],
        "problems": PROBLEMS,
        "published": False,
        "receipt": None,
        "reviewer": "Codex Prime",
        "schema": "n7-first-review-run/0514",
        "seated": False,
        "shared_runtime": {
            "construct_pass02": "labs/review-construction-pass02/construct.py",
            "construct_pass04": "labs/review-construction-pass04/construct.py",
            "prime_review_pass02": "labs/prime-review-pass02/prime_review.py",
            "return_access": "labs/return-access-pass01/return_access.py",
            "return_inspect": "labs/return-capture-pass01/return_inspect.py",
            "return_lines_pass01": "labs/return-lines-pass01/return_lines.py",
            "return_lines_pass04": "labs/return-lines-pass04/return_lines.py",
            "return_placement": "labs/return-placement-pass01/return_placement.py",
            "workbook_pass01": "labs/workbook-review-pass01/workbook.py",
        },
        "stamp": stamp,
        "watched_changed": changed_core,
        "work_complete": False,
        "writer_started": writer_started_of("writer_started: false"),
    }
    write_bytes(root / "run-report.json", dump(report))
    print(f"stamp {stamp}")
    print(f"problems {len(PROBLEMS)}")
    if FIRST is not None:
        print(f"first {FIRST['step']}: {FIRST['message']}")
    return 0 if not PROBLEMS else 1


if __name__ == "__main__":
    sys.exit(main())
