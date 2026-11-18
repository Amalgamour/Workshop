#!/usr/bin/env python3
"""Command record for 0521.return-placement/05.13.

This process follows evidence/build05.13/CONTRACT.md. It copies reviewed
tools, runs them on one disposable book, and writes the transcript under
the stamp. It does not select the shared app or write the live book.
"""

from __future__ import annotations

import datetime
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
LIVE_BOOK = REPO / "00.kernel" / "00.00.10.work"
PYTHON = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
MANIFEST = (
    LIVE_BOOK
    / "0521.return-placement"
    / "evidence"
    / "pack05.13"
    / "source-manifest.json"
)
EXPECTED_DISPATCHER = (
    "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9",
    12204,
)
DOOR_PAGE = LIVE_BOOK / "0100.band.returns" / "01.md"
N5 = "0521.connected-return-review"
N5_LINE = "0121.connected-return-review"
N7 = "0721.connected-local"
N7_REVIEW = f"{N7}/06.01.review.md"
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
OLD_RETURN = 'parent / "return_line_tools_v2.py"'
NEW_RETURN = 'parent / "return_line_tools_v3.py"'
OLD_HANDOFF = 'parent / "handoff_tools.py"'
NEW_HANDOFF = 'parent / "handoff_tools_v2.py"'
FILING_RELEASE = "synthetic fixture filing; not a Director release"
ORIGIN = ("00.00.10.work", "0504.app-entry", "05.08")
WITNESS_FILES = ("return.md", "receipt.json", "manifest.json", "payload/0001.blob")

PROBLEMS: list[str] = []
COMMANDS: list[dict] = []
FIRST: dict | None = None


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(body: dict) -> bytes:
    return (json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8")


def canonical(body: dict) -> bytes:
    text = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return (text + "\n").encode("utf-8")


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def problem(message: str, step: str | None = None) -> None:
    global FIRST
    line = message if step is None else f"{step}: {message}"
    PROBLEMS.append(line)
    if FIRST is None:
        FIRST = {"step": step, "message": message}


def note_exit(step: str, code: int, expected: set[int]) -> None:
    if code not in expected:
        problem(f"exit {code}, expected {sorted(expected)}", step)


def load_release_text(pass02: Path) -> str:
    spec = importlib.util.spec_from_file_location("return_lines_pass02_release", pass02)
    if spec is None or spec.loader is None:
        raise RuntimeError("pass02 did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    text = module.RELEASE_TEXT
    if not isinstance(text, str) or "05.04.md" not in text:
        raise RuntimeError("RELEASE_TEXT was not the recorded constant")
    return text


def copy_closure(code: Path) -> None:
    document = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for row in document["files"]:
        rel = row["path"]
        if not (rel.startswith("app/") or rel.startswith("labs/")):
            continue
        if rel in {"app/librarian.py", "app/README.md"}:
            continue
        source = REPO / Path(rel)
        data = source.read_bytes()
        if sha(data) != row["sha256"] or len(data) != row["bytes"]:
            raise RuntimeError(f"closure row drifted before copy: {rel}")
        write_bytes(code / Path(rel), data)


def write_dispatcher(code: Path) -> dict:
    source = (REPO / "app" / "librarian.py").read_bytes()
    if sha(source) != EXPECTED_DISPATCHER[0] or len(source) != EXPECTED_DISPATCHER[1]:
        raise RuntimeError("live dispatcher drifted before the copy")
    text = source.decode("utf-8")
    if text.count(OLD_RETURN) != 1 or text.count(OLD_HANDOFF) != 1:
        raise RuntimeError("substitution sites are not unique")
    if "review_loop_tools_v7.py" not in text or "authoring_tools_v2.py" not in text:
        raise RuntimeError("preserved branches are absent")
    changed = text.replace(OLD_RETURN, NEW_RETURN, 1).replace(OLD_HANDOFF, NEW_HANDOFF, 1)
    if changed.count(NEW_RETURN) != 1 or changed.count(OLD_RETURN) != 0:
        raise RuntimeError("return-lines substitution did not stick")
    if changed.count(NEW_HANDOFF) != 1 or changed.count(OLD_HANDOFF) != 0:
        raise RuntimeError("capture-return substitution did not stick")
    if changed.count("review_loop_tools_v7.py") != text.count("review_loop_tools_v7.py"):
        raise RuntimeError("review-loop branch changed")
    if changed.count("authoring_tools_v2.py") != text.count("authoring_tools_v2.py"):
        raise RuntimeError("authoring branch changed")
    data = changed.encode("utf-8")
    write_bytes(code / "app" / "librarian.py", data)
    return {
        "before_sha256": EXPECTED_DISPATCHER[0],
        "before_bytes": EXPECTED_DISPATCHER[1],
        "after_sha256": sha(data),
        "after_bytes": len(data),
    }


def fixed_roots(code: Path) -> list[dict]:
    needles = (b"D:\\Git\\lib-build", b"D:/Git/lib-build")
    found = []
    for path in sorted(code.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        data = path.read_bytes()
        if any(needle in data for needle in needles):
            found.append({"bytes": len(data), "path": path.relative_to(code).as_posix(), "sha256": sha(data)})
    return found


def file_sha(path: Path) -> str | None:
    if not path.is_file():
        return None
    return sha(path.read_bytes())


def run(step: str, argv: list[str], cwd: Path, expect: set[int] | None, out: Path) -> dict:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        argv,
        cwd=os.fspath(cwd),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
        check=False,
    )
    record = {
        "argv": argv,
        "cwd": str(cwd),
        "exit": proc.returncode,
        "stderr_bytes": len(proc.stderr),
        "stdout_bytes": len(proc.stdout),
        "step": step,
    }
    write_bytes(out / f"{step}.stdout", proc.stdout)
    write_bytes(out / f"{step}.stderr", proc.stderr)
    COMMANDS.append(record)
    if expect is not None:
        note_exit(step, proc.returncode, expect)
    record["stdout"] = proc.stdout
    record["stderr"] = proc.stderr
    return record


def leading_json(data: bytes) -> dict | None:
    if not data.strip():
        return None
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


def field_after(text: str, prefix: str) -> str | None:
    for line in text.splitlines():
        if prefix in line:
            return line.split(prefix, 1)[1].strip()
    return None


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


def judgment(page: str, action: str) -> dict:
    sections = {key: None for key in SECTION_KEYS}
    sections["return_result"] = (
        f"The disposable capture command wrote the {page} receipt. This sentence is supplied test data."
    )
    sections["prime_finding"] = "Supplied test data. This is not an independent semantic review."
    sections["within_direction"] = "The run stays on the disposable book."
    sections["next_bounded_action"] = action
    sections["tests_passed"] = None
    return {
        "answers": [],
        "design_fork": None,
        "disposition": "accepted",
        "finding": f"Supplied fixture judgment for {page}. This is not an independent semantic review.",
        "findings": [],
        "gaps": ["agreement fields other than the measured goal were not in the source heading"],
        "goal_terminal": "open",
        "holds": [],
        "next_action": action,
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


def auth_flags(paths: dict) -> list[str]:
    return [
        "--authorization", paths["auth"],
        "--audit", paths["audit"],
        "--plan", paths["plan"],
        "--backup", paths["backup"],
        "--staging", paths["staging"],
        "--retired", paths["retired"],
    ]


def band01(book: Path) -> list[str]:
    names = []
    for child in book.iterdir():
        if child.is_dir() and re.match(r"^01\d\d\.", child.name):
            names.append(child.name)
    return sorted(names)


def file_identity(path: Path) -> dict | None:
    if not path.is_file():
        return None
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def witness_identity(book: Path, member: str) -> dict:
    base = book / member
    return {rel: file_identity(base / rel) for rel in WITNESS_FILES}


def origin_args() -> list[str]:
    book_name, page, batch = ORIGIN
    return ["--origin-book", book_name, "--origin-page", page, "--origin-batch", batch]


def ready_projection(body: dict) -> dict:
    routes = {}
    raw = body.get("routes") if isinstance(body.get("routes"), dict) else {}
    for name, route in raw.items():
        if not isinstance(route, dict):
            continue
        routes[name] = {
            "selected_facade": route.get("selected_facade"),
            "selector": route.get("selector"),
            "state": route.get("state"),
            "successor_path": route.get("successor_path"),
            "successor_staged": route.get("successor_staged"),
        }
    decl = body.get("book_declaration") if isinstance(body.get("book_declaration"), dict) else {}
    layout = decl.get("layout") if isinstance(decl.get("layout"), dict) else {}
    return {
        "app_selection_applied": body.get("app_selection_applied"),
        "authority": body.get("authority"),
        "coherent": body.get("coherent"),
        "declared": decl.get("declared"),
        "final_check": body.get("final_check"),
        "layout_sha256": layout.get("sha256"),
        "layout_state": layout.get("state"),
        "routes": routes,
        "schema": body.get("schema"),
    }


def main() -> int:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    root = Path(r"D:\librarian\temp\0521-0513") / stamp
    code = root / "code"
    book = root / "book"
    out = root / "out"
    inputs = root / "inputs"
    for path in (
        book,
        out,
        inputs,
        root / "backup",
        root / "staging",
        root / "retired",
        root / "audit",
        root / "plan",
        root / "auth",
    ):
        path.mkdir(parents=True)
    if (code / "00.kernel").exists():
        raise RuntimeError("copy live path was created early")
    live_before = {
        "dispatcher": file_sha(REPO / "app" / "librarian.py"),
        "door": file_sha(DOOR_PAGE),
        "layout_exists": (LIVE_BOOK / "return-line-layout.json").exists(),
        "readme": file_sha(REPO / "app" / "README.md"),
    }
    copy_closure(code)
    dispatcher = write_dispatcher(code)
    roots = fixed_roots(code)
    release_text = load_release_text(code / "labs" / "return-lines-pass02" / "return_lines.py")
    app = code / "app" / "librarian.py"
    guard = code / "labs" / "return-capture-guard-pass01" / "return_capture_guard.py"
    reader = code / "labs" / "return-capture-pass01" / "return_capture.py"
    inspect_tool = code / "labs" / "return-capture-pass01" / "return_inspect.py"
    backend = code / "labs" / "return-lines-pass04" / "return_lines.py"
    clerk = code / "labs" / "clerk-handoff-pass02" / "clerk.py"
    readiness = code / "labs" / "return-readiness-pass02" / "readiness.py"
    live_backend = REPO / "labs" / "return-lines-pass04" / "return_lines.py"
    live_readiness = REPO / "labs" / "return-readiness-pass02" / "readiness.py"
    live_cycle = REPO / "labs" / "review-loop-pass03" / "review_loop.py"

    def tool(step: str, script: Path, args: list[str], cwd: Path, expect: set[int] | None) -> dict:
        return run(step, [str(PYTHON), "-B", str(script), *args], cwd, expect, out)

    def reserve_historical(step: str, submission: str, name: str, outputs: list[str]) -> str:
        args = [
            "reserve", "--book", str(book), "--submission", submission, "--name", name,
            *origin_args(),
            "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", name,
        ]
        for item in outputs:
            args.extend(["--expected-output", item])
        result = tool(step, guard, args, code, {0})
        text = result["stdout"].decode("utf-8", "replace")
        member = field_after(text, "member ")
        if member is None or not (book / member).is_dir():
            problem("historical reserve did not print a member directory", step)
            return ""
        if "line-pass protection: absent" not in text:
            problem("undeclared reserve omitted the absent-protection line", step)
        return member

    witness = reserve_historical(
        "01-witness-reserve", "hist-witness", "historical-witness", ["witness.txt"],
    )
    witness_source = inputs / "witness-source"
    witness_return = inputs / "witness-return.md"
    witness_payload = b"witness payload 0513\n"
    witness_return_bytes = b"Historical witness return 0513.\n"
    write_bytes(witness_source / "witness.txt", witness_payload)
    write_bytes(witness_return, witness_return_bytes)
    captured = tool(
        "02-witness-capture",
        guard,
        [
            "capture", "--book", str(book), "--submission", "hist-witness",
            "--return-file", str(witness_return), "--source-root", str(witness_source),
            "--artifact", "witness.txt|witness.txt",
        ],
        code,
        {0},
    )
    capture_text = captured["stdout"].decode("utf-8", "replace")
    if "result captured" not in capture_text:
        problem("historical capture did not report result captured", "02-witness-capture")
    if witness and (book / witness / "return.md").is_file():
        if (book / witness / "return.md").read_bytes() != witness_return_bytes:
            problem("captured return.md differs from the supplied return", "02-witness-capture")
        payload_path = book / witness / "payload" / "0001.blob"
        if not payload_path.is_file() or payload_path.read_bytes() != witness_payload:
            problem("captured payload differs from the supplied witness bytes", "02-witness-capture")
    before_mark = witness_identity(book, witness) if witness else {}

    def read_witness(prefix: str, expect_complete: bool) -> None:
        if not witness:
            problem("witness member is absent", prefix)
            return
        verified = tool(
            f"{prefix}-guard-verify", guard,
            ["verify", "--book", str(book), "--member", witness],
            code, {0} if expect_complete else None,
        )
        text = verified["stdout"].decode("utf-8", "replace")
        if expect_complete:
            if "result complete" not in text or "not approved" not in text:
                problem("guard verify did not report a complete unapproved read", f"{prefix}-guard-verify")
            if "writer_started: false" in text or "Use the line-pass route" in text:
                problem("guard verify was the declared-layout write refusal", f"{prefix}-guard-verify")
        direct = tool(
            f"{prefix}-reader-verify", reader,
            ["verify", "--book", str(book), "--member", witness],
            code, {0} if expect_complete else None,
        )
        direct_text = direct["stdout"].decode("utf-8", "replace")
        if expect_complete and "result complete" not in direct_text:
            problem("reader verify did not report result complete", f"{prefix}-reader-verify")
        inspected = tool(
            f"{prefix}-inspect", inspect_tool,
            ["inspect", "--book", str(book), "--member", witness, "--json"],
            code, {0} if expect_complete else None,
        )
        body = leading_json(inspected["stdout"])
        if expect_complete and (body is None or body.get("status") != "complete"):
            problem("inspect status was not complete", f"{prefix}-inspect")

    read_witness("03", True)
    missing = reserve_historical(
        "04-negative-reserve", "hist-missing", "historical-missing", ["missing.txt"],
    )
    eligible = reserve_historical(
        "05-eligible-reserve", "hist-eligible", "historical-eligible", ["return.md", "piece.txt"],
    )
    if witness and missing and eligible:
        if len({witness, missing, eligible}) != 3:
            problem("historical reserves did not allocate three distinct members", "05-eligible-reserve")

    handoff = root / "handoff"
    instructions = handoff / "instructions"
    store = handoff / "store"
    source = handoff / "source"
    instructions.mkdir(parents=True)
    source.mkdir()
    (handoff / "record").mkdir()
    eligible_return = b"Eligible handoff return 0513.\n"
    eligible_piece = b"eligible-piece-0513\n"
    write_bytes(source / "return.md", eligible_return)
    write_bytes(source / "piece.txt", eligible_piece)
    write_bytes(instructions / "task.txt", b"fixture task\n")
    job = {
        "assignee": "fixture-builder",
        "expected_outputs": ["return.md", "piece.txt"],
        "instructions": {"path": "task.txt", "sha256": sha((instructions / "task.txt").read_bytes())},
        "job_id": "fixture-0513",
        "release": "fixture job label; not a release",
        "reviewer": "fixture-reviewer",
        "routed_by": "fixture-router",
    }
    job_path = handoff / "job.json"
    write_bytes(job_path, canonical(job))
    queued = tool(
        "06-clerk-queue", clerk,
        ["queue", "--store", str(store), "--job", str(job_path), "--instructions-base", str(instructions)],
        code, {0},
    )
    claimed = tool(
        "07-clerk-claim", clerk,
        ["claim", "--store", str(store), "--job", "fixture-0513", "--as", "fixture-builder",
         "--instructions-base", str(instructions)],
        code, {0},
    )
    token = field_after(claimed["stdout"].decode("utf-8", "replace"), "token ")
    outbox = store / "jobs" / "fixture-0513" / "outbox"
    event = None
    if token:
        write_bytes(outbox / "return.md", eligible_return)
        write_bytes(outbox / "piece.txt", eligible_piece)
        returned = tool(
            "08-clerk-return", clerk,
            ["return", "--store", str(store), "--job", "fixture-0513", "--as", "fixture-builder",
             "--claim", token, "--delivery", "fixture-delivery", "--evidence", "transport line only"],
            code, {0},
        )
        event = field_after(returned["stdout"].decode("utf-8", "replace"), "event 0003.returned.json sha256=")
    else:
        problem("clerk claim did not print a token", "07-clerk-claim")
    precondition = {
        "eligible_member": eligible,
        "expected_outputs": ["return.md", "piece.txt"],
        "piece_sha256": sha(eligible_piece),
        "return_sha256": sha(eligible_return),
        "source_piece_matches": (source / "piece.txt").read_bytes() == eligible_piece,
        "source_return_matches": (source / "return.md").read_bytes() == eligible_return,
        "outbox_piece_matches": (outbox / "piece.txt").is_file() and (outbox / "piece.txt").read_bytes() == eligible_piece,
        "outbox_return_matches": (outbox / "return.md").is_file() and (outbox / "return.md").read_bytes() == eligible_return,
    }
    if not all(
        precondition[key]
        for key in (
            "source_piece_matches",
            "source_return_matches",
            "outbox_piece_matches",
            "outbox_return_matches",
        )
    ):
        problem("eligible payload bytes do not match across source and outbox", "08-clerk-return")

    audit_path = root / "audit" / "audit.json"
    write_bytes(audit_path, dump({"files": [], "records": []}))
    plan_path = root / "plan" / "plan.json"
    tool(
        "09-plan", app,
        ["return-lines", "plan", "--book", str(book), "--audit", str(audit_path), "--out", str(plan_path)],
        code, {0},
    )
    predicted_layout = dump({
        "allocation": "line-pass",
        "bands": {"5": "matched-workflow-return-line", "7": "page-local-colab"},
        "book": "00.00.10.work",
        "schema": "return-line-layout/1",
        "sequential_allocation": False,
    })
    auth_path = root / "auth" / "authorization.json"
    auth_body = {
        "audit_bytes": audit_path.stat().st_size,
        "audit_sha256": sha(audit_path.read_bytes()),
        "backup_root": str(root / "backup"),
        "book": "00.00.10.work",
        "book_path": str(book),
        "executor": "Codex Prime",
        "layout_sha256": sha(predicted_layout),
        "operations": ["capture", "init", "preflight", "reserve"],
        "plan_sha256": sha(plan_path.read_bytes()) if plan_path.is_file() else "",
        "release": release_text,
        "retired_root": str(root / "retired"),
        "schema": "return-line-authorization/1",
        "staging_root": str(root / "staging"),
        "synthetic": True,
    }
    write_bytes(auth_path, dump(auth_body))
    init = tool(
        "10-init", backend,
        [
            "init", "--book", str(book), "--name", "00.00.10.work",
            "--authorization", str(auth_path), "--audit", str(audit_path), "--plan", str(plan_path),
            "--backup", str(root / "backup"), "--staging", str(root / "staging"), "--retired", str(root / "retired"),
        ],
        code, {0},
    )
    layout_path = book / "return-line-layout.json"
    if not layout_path.is_file() or layout_path.read_bytes() != predicted_layout:
        problem("init did not write the predicted line-pass layout", "10-init")
    write_bytes(book / "0100.band.returns" / "01.md", DOOR_PAGE.read_bytes())
    paths = {
        "audit": str(audit_path),
        "auth": str(auth_path),
        "backup": str(root / "backup"),
        "plan": str(plan_path),
        "retired": str(root / "retired"),
        "staging": str(root / "staging"),
    }
    read_witness("11", True)
    after_mark = witness_identity(book, witness) if witness else {}
    if before_mark != after_mark:
        problem("declaration changed the positive witness bytes", "11-guard-verify")
    if missing:
        negative = tool(
            "12-negative-verify", guard,
            ["verify", "--book", str(book), "--member", missing],
            code, {2},
        )
        negative_text = negative["stdout"].decode("utf-8", "replace")
        if "missing return.md" not in negative_text or "result refused" not in negative_text:
            problem("negative verify did not report the missing return", "12-negative-verify")
        if "writer_started: false" in negative_text or "Use the line-pass route" in negative_text:
            problem("negative verify was the declared-layout write refusal", "12-negative-verify")
        if "result complete" in negative_text:
            problem("negative verify was reported as the positive complete read", "12-negative-verify")

    binding_path = handoff / "binding.json"
    failure_log = handoff / "failure.log"
    intent_path = handoff / "record" / "intent.json"
    members_before_door = band01(book)
    door_result = {"attempted": False, "exit": None, "guard_invoked": False, "writer_started": None}
    if event and eligible and precondition["outbox_piece_matches"]:
        binding = {
            "artifact_base": str(outbox),
            "artifacts": [
                {"bytes": len(eligible_return), "clerk_path": "return.md", "logical": "return.md", "sha256": sha(eligible_return), "source": "return.md"},
                {"bytes": len(eligible_piece), "clerk_path": "piece.txt", "logical": "piece.txt", "sha256": sha(eligible_piece), "source": "piece.txt"},
            ],
            "assignee": "fixture-builder",
            "book": str(book),
            "clerk_store": str(store),
            "failure_log": str(failure_log),
            "instructions_base": str(instructions),
            "job_id": "fixture-0513",
            "member": eligible,
            "origin": {"batch": "05.08", "book": "00.00.10.work", "page": "0504.app-entry"},
            "record": str(handoff / "record"),
            "report": {"bytes": len(eligible_return), "clerk_path": "return.md", "sha256": sha(eligible_return), "source": "return.md"},
            "returned_event_sha256": event,
            "schema": "clerk-capture-handoff/1",
            "source_root": str(source),
            "submission_id": "hist-eligible",
            "work_ref": "hist-eligible-work-ref",
        }
        write_bytes(binding_path, canonical(binding))
        door_run = tool(
            "13-capture-return", app,
            ["capture-return", "--binding", str(binding_path)],
            code, {2},
        )
        door_result["attempted"] = True
        door_result["exit"] = door_run["exit"]
        if (book / eligible / "receipt.json").exists():
            problem("capture-return wrote a receipt on the eligible member", "13-capture-return")
        if band01(book) != members_before_door:
            problem("capture-return allocated a member", "13-capture-return")
        if failure_log.is_file():
            failure_body = json.loads(failure_log.read_text(encoding="utf-8"))
            child = failure_body.get("capture") if isinstance(failure_body.get("capture"), dict) else {}
            child_text = child.get("stdout") if isinstance(child.get("stdout"), str) else ""
            door_result["guard_invoked"] = child.get("attempted") is True and "writer_started: false" in child_text
            door_result["writer_started"] = "writer_started: false" in child_text
            door_result["child_has_line_pass_refusal"] = "Use the line-pass route." in child_text
            if not door_result["guard_invoked"] or not door_result["child_has_line_pass_refusal"]:
                problem("capture-return did not retain the guard refusal before the writer", "13-capture-return")
            if "result captured" in child_text:
                problem("capture child reported completion", "13-capture-return")
        else:
            problem("capture-return did not retain a failure log", "13-capture-return")
        failure_hash = file_sha(failure_log)
        intent_hash = file_sha(intent_path)
        repeated = tool(
            "14-capture-return-repeat", app,
            ["capture-return", "--binding", str(binding_path)],
            code, {2},
        )
        repeat_text = repeated["stdout"].decode("utf-8", "replace")
        if file_sha(failure_log) != failure_hash or file_sha(intent_path) != intent_hash:
            problem("repeated capture-return changed the retained failure or intent", "14-capture-return-repeat")
        if "intent is retained" not in repeat_text:
            problem("repeated capture-return did not retain the prior intent", "14-capture-return-repeat")
        if "result ok" in repeat_text or "result captured" in repeat_text:
            problem("repeated capture-return reported completion", "14-capture-return-repeat")
        if band01(book) != members_before_door:
            problem("repeated capture-return allocated a member", "14-capture-return-repeat")
        if (book / eligible / "receipt.json").exists():
            problem("repeated capture-return wrote a receipt", "14-capture-return-repeat")
        door_result["failure_sha256"] = failure_hash
        door_result["intent_sha256"] = intent_hash
        door_result["repeat_exit"] = repeated["exit"]
    else:
        problem("eligible binding was not ready after the clerk return", "08-clerk-return")

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
        return tool(step, app, ["return-lines", *args, *auth_flags(paths)], code, expect)

    line("15-reserve-0501", [
        "reserve", "--book", str(book), "--page", N5, "--batch", "05.01",
        "--submission", "s0513a", "--output", "note.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", FILING_RELEASE,
    ], {1})
    line("16-capture-0501", [
        "capture", "--book", str(book), "--page", N5, "--batch", "05.01",
        "--submission", "s0513a", "--return-file", str(n5_return),
        "--artifact", "note.txt", str(n5_note),
    ], {0})
    receipt_0501 = book / N5_LINE / "05.01.custody" / "receipt.json"
    receipt_0501_sha = file_sha(receipt_0501)
    if receipt_0501_sha is None:
        problem("05.01 capture did not leave a receipt", "16-capture-0501")
    looked = tool(
        "17-lookup-0501", app,
        ["return-lines", "lookup", "--book", str(book), "--source", N5, "--pass", "05.01"],
        code, {0},
    )
    verified_n5 = tool(
        "18-verify-0501", app,
        ["return-lines", "verify", "--book", str(book), "--source", N5, "--pass", "05.01"],
        code, {0},
    )
    verify_body = leading_json(verified_n5["stdout"])
    if verify_body is None or verify_body.get("task_association") != "not-established":
        problem("N5 verify did not report task_association not-established", "18-verify-0501")
    if verify_body is None or verify_body.get("state") != "complete":
        problem("N5 verify state was not complete", "18-verify-0501")
    if N5_LINE not in looked["stdout"].decode("utf-8", "replace"):
        problem("N5 lookup did not name the matching line", "17-lookup-0501")

    action = "Prime reviews this integration return before any shared app substitution."
    judgment_path = inputs / "judgment-0501.json"
    write_bytes(judgment_path, dump(judgment(N5, action)))
    prepared = tool(
        "19-prepare", app,
        ["review-loop", "prepare", "--book", str(book), "--source", N5, "--pass", "05.01"],
        code, {0},
    )
    formed = tool(
        "19-form", app,
        ["review-loop", "form", "--book", str(book), "--source", N5, "--pass", "05.01"],
        code, {0},
    )
    form_body = leading_json(formed["stdout"])
    intake_ids = find_strings(form_body, "intake_id") if form_body else []
    intake = intake_ids[0] if intake_ids else ""
    if not re.fullmatch(r"[0-9a-f]{64}", intake):
        problem("form did not return an intake id", "19-form")
    recorded = tool(
        "19-record", app,
        ["review-loop", "record", "--book", str(book), "--source", N5, "--pass", "05.01",
         "--intake", intake, "--judgment", str(judgment_path)],
        code, {0},
    )
    record_body = leading_json(recorded["stdout"])
    review_ids = [
        item for item in (find_strings(record_body, "review_id") if record_body else [])
        if re.fullmatch(r"w[0-9a-f]{16}", item)
    ]
    review = review_ids[0] if review_ids else ""
    if review == "":
        problem("record did not return a review id", "19-record")
    if record_body is None or record_body.get("mode") != "cycle-committed":
        problem("N5 record mode was not cycle-committed", "19-record")
    inspected = tool(
        "19-inspect", app,
        ["review-loop", "inspect", "--book", str(book), "--source", N5, "--pass", "05.01"],
        code, {0},
    )
    write_bytes(out / "19-inspect-saved.txt", inspected["stdout"])
    published = tool(
        "19-publish", app,
        ["review-loop", "publish", "--book", str(book), "--source", N5, "--pass", "05.01", "--review", review],
        code, {0},
    )
    tool(
        "19-read", app,
        ["review-loop", "read", "--book", str(book), "--source", N5, "--pass", "05.01"],
        code, {0},
    )
    tool(
        "19-recover", app,
        ["review-loop", "recover", "--book", str(book), "--source", N5, "--pass", "05.01"],
        code, {0},
    )
    page_text = (book / N5 / "05.01.md").read_text(encoding="utf-8") if (book / N5 / "05.01.md").is_file() else ""
    if "closes_work: false" not in page_text or "releases_action: false" not in page_text:
        problem("N5 published page did not keep closes_work and releases_action false", "19-publish")
    if file_sha(receipt_0501) != receipt_0501_sha:
        problem("N5 review changed the 05.01 receipt", "19-recover")
    review_n5 = {
        "intake_id": intake,
        "mode": None if record_body is None else record_body.get("mode"),
        "prepare_exit": prepared["exit"],
        "publish_exit": published["exit"],
        "record_exit": recorded["exit"],
        "review_id": review,
    }

    line("20-reserve-n7", [
        "reserve", "--book", str(book), "--page", N7, "--batch", "05.01",
        "--submission", "s0513n7", "--output", "note.txt",
        "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", FILING_RELEASE,
    ], {1})
    line("21-capture-n7", [
        "capture", "--book", str(book), "--page", N7, "--batch", "05.01",
        "--submission", "s0513n7", "--return-file", str(n7_return),
        "--artifact", "note.txt", str(n7_note),
    ], {0})
    if (book / "0121.connected-local").exists():
        problem("N7 filing created 0121.connected-local", "21-capture-n7")
    n7_receipt = book / N7 / "05.01.custody" / "receipt.json"
    if not n7_receipt.is_file():
        problem("N7 capture did not leave a receipt", "21-capture-n7")
    tool(
        "22-verify-n7", app,
        ["return-lines", "verify", "--book", str(book), "--source", N7, "--pass", "05.01"],
        code, {0},
    )
    if (book / N7_REVIEW).exists():
        problem("the driver found a review target before N7 prepare", "23-prepare-n7")
    n7_judgment = inputs / "judgment-n7.json"
    write_bytes(n7_judgment, dump(judgment(N7, action)))
    n7_prepared = tool(
        "23-prepare-n7", app,
        ["review-loop", "prepare", "--book", str(book), "--source", N7, "--pass", "05.01"],
        code, {0},
    )
    n7_formed = tool(
        "23-form-n7", app,
        ["review-loop", "form", "--book", str(book), "--source", N7, "--pass", "05.01"],
        code, {0},
    )
    n7_form = leading_json(n7_formed["stdout"])
    n7_intake_ids = find_strings(n7_form, "intake_id") if n7_form else []
    n7_intake = n7_intake_ids[0] if n7_intake_ids else ""
    n7_recorded = tool(
        "23-record-n7", app,
        ["review-loop", "record", "--book", str(book), "--source", N7, "--pass", "05.01",
         "--intake", n7_intake, "--judgment", str(n7_judgment)],
        code, {0, 1},
    )
    n7_record = leading_json(n7_recorded["stdout"])
    n7_inspected = tool(
        "23-inspect-n7", app,
        ["review-loop", "inspect", "--book", str(book), "--source", N7, "--pass", "05.01"],
        code, {0},
    )
    inspect_text = n7_inspected["stdout"].decode("utf-8", "replace")
    if "cycle prepare did not return a template" not in inspect_text:
        problem("N7 inspect did not keep the template failure", "23-inspect-n7")
    if n7_record is not None and n7_record.get("mode") == "cycle-committed":
        problem("N7 record mode was cycle-committed", "23-record-n7")
    cycle_request = None
    for path in (book / "workbook-review" / N7).rglob("request.json"):
        if path.parent.name == "cycle":
            cycle_request = path
            break
    cycle_files = {}
    if cycle_request is None:
        problem("N7 record did not leave a cycle request", "23-record-n7")
        request_rel = ""
    else:
        request_rel = cycle_request.relative_to(book).as_posix()
        for name in ("request.json", "registration.json", "descriptor.json"):
            source_path = cycle_request.parent / name
            if source_path.is_file():
                data = source_path.read_bytes()
                write_bytes(out / f"n7-cycle-{name}", data)
                cycle_files[name] = {"bytes": len(data), "sha256": sha(data), "path": source_path.relative_to(book).as_posix()}
    if (book / N7_REVIEW).exists():
        problem("a review target existed before the raw cycle prepare", "24-cycle-prepare")
    cycle_run = tool(
        "24-cycle-prepare", live_cycle,
        ["prepare", "--fixture-root", str(book), "--request", request_rel],
        REPO, None,
    )
    cycle_body = leading_json(cycle_run["stdout"])
    cycle_view = cycle_body.get("view") if isinstance(cycle_body, dict) and isinstance(cycle_body.get("view"), dict) else {}
    registration = {}
    if cycle_request is not None and (cycle_request.parent / "registration.json").is_file():
        registration = json.loads((cycle_request.parent / "registration.json").read_text(encoding="utf-8"))
    review_target_exists = (book / N7_REVIEW).exists()
    template = cycle_view.get("template") if isinstance(cycle_view, dict) else None
    write_token = cycle_view.get("write_token") if isinstance(cycle_view, dict) else None
    seam = (
        cycle_run["exit"] == 0
        and template is None
        and write_token is None
        and registration.get("target") == N7_REVIEW
        and registration.get("source_kind") == "N7NN"
        and review_target_exists is False
    )
    if not seam:
        problem("the raw N7 prepare did not reproduce the absent-target template seam", "24-cycle-prepare")
    dependency_names = {
        "construct": REPO / "labs" / "review-construction-pass04" / "construct.py",
        "prime_cycle": REPO / "labs" / "prime-cycle-pass03" / "prime_cycle.py",
        "review_loop": live_cycle,
        "workbook_pass02": REPO / "labs" / "workbook-review-pass02" / "workbook.py",
    }
    diagnosis = {
        "binding_present": isinstance(cycle_view, dict) and cycle_view.get("binding") is not None,
        "classification": "implementation-seam" if seam else "unconfirmed",
        "cycle_error": "cycle prepare did not return a template",
        "dependencies": {
            name: {"bytes": path.stat().st_size, "sha256": sha(path.read_bytes())}
            for name, path in dependency_names.items()
        },
        "expected_schema": "prime-cycle-view/4",
        "functions": {
            "derive": "labs/prime-cycle-pass03/prime_cycle.py",
            "prepare": "labs/review-loop-pass03/review_loop.py",
            "write_cycle_inputs": "labs/workbook-review-pass02/workbook.py",
            "write_token_of": "labs/prime-cycle-pass03/prime_cycle.py",
        },
        "kernel_page": registration.get("kernel_page"),
        "prepare_exit": cycle_run["exit"],
        "prepare_stderr_bytes": cycle_run["stderr_bytes"],
        "request": request_rel,
        "review_target_exists_after_prepare": review_target_exists,
        "source_kind": registration.get("source_kind"),
        "target": registration.get("target"),
        "template": template,
        "view_schema": cycle_view.get("schema") if isinstance(cycle_view, dict) else None,
        "write_token": write_token,
        "caller_correction_demonstrated": False,
        "n7_cycle_success_claimed": False,
    }
    write_bytes(out / "n7-diagnosis.json", dump(diagnosis))
    n7_published = tool(
        "25-publish-n7", app,
        ["review-loop", "publish", "--book", str(book), "--source", N7, "--pass", "05.01",
         "--review", (find_strings(n7_record, "review_id") or [""])[0]],
        code, {0, 1},
    )
    tool(
        "25-read-n7", app,
        ["review-loop", "read", "--book", str(book), "--source", N7, "--pass", "05.01"],
        code, {0, 1},
    )
    tool(
        "25-recover-n7", app,
        ["review-loop", "recover", "--book", str(book), "--source", N7, "--pass", "05.01"],
        code, {0, 1},
    )
    review_n7 = {
        "intake_id": n7_intake,
        "mode": None if n7_record is None else n7_record.get("mode"),
        "prepare_exit": n7_prepared["exit"],
        "publish_exit": n7_published["exit"],
        "record_exit": n7_recorded["exit"],
        "review_destination_exists": (book / N7_REVIEW).is_file(),
    }

    copy_ready = tool(
        "26-readiness-copy", readiness,
        ["--code-root", str(code), "--book", str(book), "--text"],
        code, {0},
    )
    live_ready = tool(
        "27-readiness-live", live_readiness,
        ["--code-root", str(REPO), "--book", str(LIVE_BOOK), "--text"],
        REPO, {0},
    )
    live_auth = dict(auth_body)
    live_auth["book_path"] = str(LIVE_BOOK)
    live_auth_path = root / "auth" / "live-book-authorization.json"
    write_bytes(live_auth_path, dump(live_auth))
    live_preflight = tool(
        "28-live-preflight", live_backend,
        ["preflight", "--book", str(LIVE_BOOK), "--authorization", str(live_auth_path),
         "--audit", str(audit_path), "--plan", str(plan_path), "--backup", paths["backup"],
         "--staging", paths["staging"], "--retired", paths["retired"]],
        REPO, {2},
    )
    live_text = live_preflight["stdout"].decode("utf-8", "replace")
    if "fixture authorization cannot authorize the canonical book." not in live_text:
        problem("live preflight did not name the canonical refusal", "28-live-preflight")
    live_after = {
        "dispatcher": file_sha(REPO / "app" / "librarian.py"),
        "door": file_sha(DOOR_PAGE),
        "layout_exists": (LIVE_BOOK / "return-line-layout.json").exists(),
        "readme": file_sha(REPO / "app" / "README.md"),
    }
    if live_after != live_before:
        problem(f"live identity changed during the run: {live_after}", "28-live-preflight")
    if (code / "00.kernel").exists():
        problem("the copy created its own live-book directory", "28-live-preflight")
    if witness_identity(book, witness) != before_mark:
        problem("later commands changed the positive witness bytes", "28-live-preflight")

    report = {
        "schema": "connected-return-review-run/0513",
        "stamp": stamp,
        "book": str(book),
        "code": str(code),
        "commands": [{key: value for key, value in item.items() if key not in {"stdout", "stderr"}} for item in COMMANDS],
        "copy_live_path_created": (code / "00.kernel").exists(),
        "dispatcher": dispatcher,
        "door_result": door_result,
        "eligible_precondition": precondition,
        "first_failure": FIRST,
        "fixed_repo_references": roots,
        "historical_members": {"eligible": eligible, "negative": missing, "witness": witness},
        "init_exit": init["exit"],
        "layout_sha256": file_sha(layout_path),
        "live_after": live_after,
        "live_before": live_before,
        "n7_diagnosis": diagnosis,
        "n7_review_destination_exists": (book / N7_REVIEW).is_file(),
        "positive_witness": {"after_declaration": after_mark, "before_declaration": before_mark},
        "prior_failure_reproduced": False,
        "prior_failure_record": [
            "D:\\librarian\\temp\\0521-0512\\20261103T173827361432Z",
            "D:\\librarian\\temp\\0521-0512\\20261103T174140129061Z",
        ],
        "problems": PROBLEMS,
        "queued_exit": queued["exit"],
        "readiness_copy": ready_projection(leading_json(copy_ready["stdout"]) or {}),
        "readiness_live": ready_projection(leading_json(live_ready["stdout"]) or {}),
        "receipt_0501_sha256": receipt_0501_sha,
        "review_n5": review_n5,
        "review_n7": review_n7,
        "witness_identity_unchanged": before_mark == after_mark == witness_identity(book, witness),
    }
    write_bytes(root / "run-report.json", dump(report))
    sys.stdout.buffer.write(f"{root}\nproblems {len(PROBLEMS)}\n".encode("utf-8"))
    if FIRST is not None:
        sys.stdout.buffer.write((FIRST["message"] + "\n").encode("utf-8"))
    return 0 if not PROBLEMS else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        sys.stderr.buffer.write(f"driver stopped: {exc}\n".encode("utf-8"))
        raise SystemExit(1)
