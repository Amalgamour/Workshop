#!/usr/bin/env python3
"""Command record for 0521.return-placement/05.12.

This process follows evidence/build05.12/CONTRACT.md. It copies reviewed
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
    / "pack05.12"
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
OTHER = "0521.other-subject"
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
        if not path.is_file():
            continue
        data = path.read_bytes()
        if any(needle in data for needle in needles):
            found.append({"bytes": len(data), "path": path.relative_to(code).as_posix(), "sha256": sha(data)})
    return found


def snapshot(root: Path) -> list[dict]:
    rows = []
    if not root.exists():
        return rows
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            path = Path(dirpath) / name
            if path.is_symlink():
                continue
            data = path.read_bytes()
            rows.append({
                "bytes": len(data),
                "path": path.relative_to(root).as_posix(),
                "sha256": sha(data),
            })
    return rows


def member_names(book: Path) -> list[str]:
    names = []
    for child in book.iterdir():
        if child.is_dir() and re.match(r"^\d{4}\.", child.name):
            names.append(child.name)
    return sorted(names)


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
        "finding": (
            f"Supplied fixture judgment for {page}. This is not an independent semantic review."
        ),
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


def main() -> int:
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    root = Path(r"D:\librarian\temp\0521-0512") / stamp
    code = root / "code"
    book = root / "book"
    out = root / "out"
    inputs = root / "inputs"
    for path in (book, out, inputs, root / "backup", root / "staging", root / "retired", root / "audit", root / "plan"):
        path.mkdir(parents=True)
    if (code / "00.kernel").exists():
        raise RuntimeError("copy live path was created early")
    live_before = {
        "dispatcher": file_sha(REPO / "app" / "librarian.py"),
        "door": file_sha(DOOR_PAGE),
        "layout_exists": (LIVE_BOOK / "return-line-layout.json").exists(),
    }
    copy_closure(code)
    dispatcher = write_dispatcher(code)
    roots = fixed_roots(code)
    release_text = load_release_text(code / "labs" / "return-lines-pass02" / "return_lines.py")
    app = code / "app" / "librarian.py"
    guard = code / "labs" / "return-capture-guard-pass01" / "return_capture_guard.py"
    backend = code / "labs" / "return-lines-pass04" / "return_lines.py"
    clerk = code / "labs" / "clerk-handoff-pass02" / "clerk.py"
    readiness = code / "labs" / "return-readiness-pass02" / "readiness.py"
    live_backend = REPO / "labs" / "return-lines-pass04" / "return_lines.py"
    live_readiness = REPO / "labs" / "return-readiness-pass02" / "readiness.py"

    def tool(step: str, script: Path, args: list[str], cwd: Path, expect: set[int] | None) -> dict:
        return run(step, [str(PYTHON), "-B", str(script), *args], cwd, expect, out)

    hist = tool(
        "01-historical-reserve",
        guard,
        [
            "reserve", "--book", str(book), "--submission", "hist-0512", "--name", "historical-read",
            "--origin-book", "00.00.10.work", "--origin-page", "0504.app-entry", "--origin-batch", "05.08",
            "--expected-output", "final-report.md", "--expected-output", "piece.txt",
            "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", "historical-read-prep",
        ],
        code,
        {0},
    )
    hist_text = hist["stdout"].decode("utf-8", "replace")
    member = field_after(hist_text, "member ")
    if member is None or not (book / member).is_dir():
        problem("historical reserve did not print a member directory", "01-historical-reserve")
        member = ""
    if "line-pass protection: absent" not in hist_text:
        problem("undeclared reserve omitted the absent-protection line", "01-historical-reserve")
    members_after_hist = member_names(book)

    audit_path = root / "audit" / "audit.json"
    write_bytes(audit_path, dump({"files": [], "records": []}))
    plan_path = root / "plan" / "plan.json"
    tool(
        "02-plan",
        app,
        ["return-lines", "plan", "--book", str(book), "--audit", str(audit_path), "--out", str(plan_path)],
        code,
        {0},
    )
    if not plan_path.is_file():
        problem("plan did not write the plan file", "02-plan")
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
        "03-init",
        backend,
        [
            "init", "--book", str(book), "--name", "00.00.10.work",
            "--authorization", str(auth_path), "--audit", str(audit_path), "--plan", str(plan_path),
            "--backup", str(root / "backup"), "--staging", str(root / "staging"), "--retired", str(root / "retired"),
        ],
        code,
        {0},
    )
    layout_path = book / "return-line-layout.json"
    if not layout_path.is_file() or layout_path.read_bytes() != predicted_layout:
        problem("init did not write the predicted line-pass layout", "03-init")
    write_bytes(book / "0100.band.returns" / "01.md", DOOR_PAGE.read_bytes())
    paths = {
        "audit": str(audit_path),
        "auth": str(auth_path),
        "backup": str(root / "backup"),
        "plan": str(plan_path),
        "retired": str(root / "retired"),
        "staging": str(root / "staging"),
    }
    pages = {
        f"{N5}/05.01.md": source_page(
            f"{N5} 05.01",
            "File this disposable pass on its matching return line and review the filed bytes.",
            True,
        ),
        f"{N5}/05.02.md": source_page(
            f"{N5} 05.02",
            "File a second disposable pass on the same matching return line.",
            True,
        ),
        f"{N5}/05.03.md": source_page(
            f"{N5} 05.03",
            "File a probe pass on the same matching return line.",
            True,
        ),
        f"{N7}/05.01.pack.md": source_page(
            f"{N7} 05.01",
            "Keep this page-local pack on its own page.",
            False,
        ),
    }
    for rel, data in pages.items():
        write_bytes(book / Path(rel), data)
    returns = {}
    for key, text in {
        "05.01": "Disposable return body for 05.01.\n",
        "05.02": "Disposable return body for 05.02.\n",
        "05.03": "Disposable return body for 05.03.\n",
        "n7": "Disposable page-local return body.\n",
    }.items():
        path = inputs / f"{key}.return.md"
        write_bytes(path, text.encode("utf-8"))
        note = inputs / f"{key}.note.txt"
        write_bytes(note, f"fixture note {key}\n".encode("utf-8"))
        returns[key] = (path, note)

    def line(step: str, args: list[str], expect: set[int]) -> dict:
        return tool(step, app, ["return-lines", *args, *auth_flags(paths)], code, expect)

    def reserve(step: str, page: str, batch: str, submission: str) -> dict:
        return line(step, [
            "reserve", "--book", str(book), "--page", page, "--batch", batch,
            "--submission", submission, "--output", "note.txt",
            "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", FILING_RELEASE,
        ], {1})

    def capture(step: str, page: str, batch: str, submission: str, key: str, expect: set[int]) -> dict:
        return_file, note = returns[key]
        return line(step, [
            "capture", "--book", str(book), "--page", page, "--batch", batch,
            "--submission", submission, "--return-file", str(return_file),
            "--artifact", "note.txt", str(note),
        ], expect)

    reserve("04-reserve-0501", N5, "05.01", "s0512a")
    capture("05-capture-0501", N5, "05.01", "s0512a", "05.01", {0})
    receipt_0501 = book / N5_LINE / "05.01.custody" / "receipt.json"
    return_0501 = book / N5_LINE / "05.01.return.md"
    receipt_0501_sha = file_sha(receipt_0501)
    if receipt_0501_sha is None or not return_0501.is_file():
        problem("05.01 capture did not leave a receipt and return", "05-capture-0501")
    tool(
        "06-restart-verify-0501",
        app,
        ["return-lines", "verify", "--book", str(book), "--source", N5, "--pass", "05.01"],
        code,
        {0},
    )
    if file_sha(receipt_0501) != receipt_0501_sha:
        problem("restart verify changed the 05.01 receipt", "06-restart-verify-0501")
    reserve("07-reserve-0502", N5, "05.02", "s0512b")
    capture("08-capture-0502", N5, "05.02", "s0512b", "05.02", {0})
    reserve("09-reserve-n7", N7, "05.01", "s0512n7")
    capture("10-capture-n7", N7, "05.01", "s0512n7", "n7", {0})
    reserve("11-reserve-0503", N5, "05.03", "s0512c")
    capture("12-capture-0503", N5, "05.03", "s0512c", "05.03", {0})
    if (book / "0121.connected-local").exists():
        problem("N7 filing created 0121.connected-local", "10-capture-n7")
    for rel in (
        f"{N5_LINE}/05.01.return.md",
        f"{N5_LINE}/05.02.return.md",
        f"{N5_LINE}/05.03.return.md",
        f"{N7}/05.01.return.md",
    ):
        if not (book / Path(rel)).is_file():
            problem(f"missing filed return {rel}", "12-capture-0503")
    tool("13-status", app, ["return-lines", "status", "--book", str(book)], code, {0})
    for step, page, batch in (
        ("14-lookup-0501", N5, "05.01"),
        ("15-verify-0501", N5, "05.01"),
        ("16-lookup-0502", N5, "05.02"),
        ("17-verify-0502", N5, "05.02"),
        ("18-lookup-n7", N7, "05.01"),
        ("19-verify-n7", N7, "05.01"),
    ):
        command = "lookup" if "lookup" in step else "verify"
        result = tool(
            step, app,
            ["return-lines", command, "--book", str(book), "--source", page, "--pass", batch],
            code, {0},
        )
        body = leading_json(result["stdout"])
        if body is None or body.get("task_association") != "not-established":
            problem("task association was not the explicit not-established value", step)
        text = result["stdout"].decode("utf-8", "replace")
        if page == N7 and "0121.connected-local" in text:
            problem("N7 retrieval named 0121.connected-local", step)
        if page == N5 and N5_LINE not in text:
            problem("N5 retrieval did not name the matching line", step)
        if page == N7 and N7 not in text:
            problem("N7 retrieval did not name the page-local target", step)

    def review_cycle(prefix: str, page: str, batch: str, judgment_name: str) -> dict:
        action = "Prime reviews this integration return before any shared app substitution."
        judgment_path = inputs / judgment_name
        write_bytes(judgment_path, dump(judgment(page, action)))
        prepared = tool(
            f"{prefix}-prepare", app,
            ["review-loop", "prepare", "--book", str(book), "--source", page, "--pass", batch],
            code, {0},
        )
        formed = tool(
            f"{prefix}-form", app,
            ["review-loop", "form", "--book", str(book), "--source", page, "--pass", batch],
            code, {0},
        )
        form_body = leading_json(formed["stdout"])
        intake_ids = find_strings(form_body, "intake_id") if form_body else []
        intake = intake_ids[0] if intake_ids else ""
        if not re.fullmatch(r"[0-9a-f]{64}", intake):
            problem("form did not return an intake id", f"{prefix}-form")
        recorded = tool(
            f"{prefix}-record", app,
            ["review-loop", "record", "--book", str(book), "--source", page, "--pass", batch,
             "--intake", intake, "--judgment", str(judgment_path)],
            code, {0, 1},
        )
        record_body = leading_json(recorded["stdout"])
        review_ids = [
            item for item in (find_strings(record_body, "review_id") if record_body else [])
            if re.fullmatch(r"w[0-9a-f]{16}", item)
        ]
        review = review_ids[0] if review_ids else ""
        if review == "":
            problem("record did not return a review id", f"{prefix}-record")
        inspected = tool(
            f"{prefix}-inspect", app,
            ["review-loop", "inspect", "--book", str(book), "--source", page, "--pass", batch],
            code, {0},
        )
        write_bytes(out / f"{prefix}-inspect-saved.txt", inspected["stdout"])
        published = tool(
            f"{prefix}-publish", app,
            ["review-loop", "publish", "--book", str(book), "--source", page, "--pass", batch,
             "--review", review],
            code, {0, 1},
        )
        tool(
            f"{prefix}-read", app,
            ["review-loop", "read", "--book", str(book), "--source", page, "--pass", batch],
            code, {0, 1},
        )
        tool(
            f"{prefix}-recover", app,
            ["review-loop", "recover", "--book", str(book), "--source", page, "--pass", batch],
            code, {0, 1},
        )
        return {
            "inspect_bytes": len(inspected["stdout"]),
            "intake_id": intake,
            "prepare_exit": prepared["exit"],
            "publish_exit": published["exit"],
            "record_exit": recorded["exit"],
            "review_id": review,
            "mode": None if record_body is None else record_body.get("mode"),
            "unknowns": None if form_body is None else form_body.get("unknowns"),
        }

    review_n5 = review_cycle("20", N5, "05.01", "judgment-0501.json")
    review_n7 = review_cycle("21", N7, "05.01", "judgment-n7.json")
    if file_sha(receipt_0501) != receipt_0501_sha:
        problem("review changed the 05.01 receipt", "20-recover")

    sealed_0502 = (book / N5_LINE / "05.02.return.md").read_bytes() if (book / N5_LINE / "05.02.return.md").is_file() else b""
    write_bytes(returns["05.02"][0], b"Conflicting disposable return body for 05.02.\n")
    conflict = capture("22-conflict-0502", N5, "05.02", "s0512b", "05.02", {2})
    after_0502 = (book / N5_LINE / "05.02.return.md").read_bytes() if (book / N5_LINE / "05.02.return.md").is_file() else b""
    if after_0502 != sealed_0502:
        problem("conflicting retry changed the sealed 05.02 return", "22-conflict-0502")
    write_bytes(out / "22-first-failure.txt", conflict["stdout"] + b"\n" + conflict["stderr"])

    mismatch = tool(
        "23-mismatch-verify", app,
        ["return-lines", "verify", "--book", str(book), "--source", OTHER, "--pass", "05.01"],
        code, None,
    )
    mismatch_body = leading_json(mismatch["stdout"])
    if mismatch["exit"] == 0 and isinstance(mismatch_body, dict) and mismatch_body.get("state") == "complete":
        problem("a different source verified as the filed 05.01 receipt", "23-mismatch-verify")
    if file_sha(receipt_0501) != receipt_0501_sha:
        problem("mismatch verify changed the 05.01 receipt", "23-mismatch-verify")

    payload = book / N5_LINE / "05.03.custody" / "payload" / "0001.blob"
    receipt_0503 = book / N5_LINE / "05.03.custody" / "receipt.json"
    receipt_0503_sha = file_sha(receipt_0503)
    if payload.is_file():
        payload.write_bytes(payload.read_bytes() + b"changed-after-filing\n")
    else:
        problem("05.03 payload was absent before the change probe", "24-changed-artifact")
    changed = tool(
        "24-changed-artifact", app,
        ["return-lines", "verify", "--book", str(book), "--source", N5, "--pass", "05.03"],
        code, None,
    )
    write_bytes(out / "24-first-failure.txt", changed["stdout"] + b"\n" + changed["stderr"])
    if file_sha(receipt_0503) != receipt_0503_sha:
        problem("changed-artifact verify rewrote the 05.03 receipt", "24-changed-artifact")
    if changed["exit"] == 0:
        body = leading_json(changed["stdout"])
        if isinstance(body, dict) and body.get("state") == "complete":
            problem("changed artifact still verified complete", "24-changed-artifact")

    handoff = root / "handoff"
    instructions = handoff / "instructions"
    store = handoff / "store"
    source = handoff / "source"
    instructions.mkdir(parents=True)
    source.mkdir()
    report = b"final report fixture\n"
    piece = b"piece-body-0512\n"
    write_bytes(instructions / "task.txt", b"fixture task\n")
    write_bytes(source / "final-report.md", report)
    write_bytes(source / "piece.txt", piece)
    job = {
        "assignee": "fixture-builder",
        "expected_outputs": ["final-report.md", "piece.txt"],
        "instructions": {"path": "task.txt", "sha256": sha((instructions / "task.txt").read_bytes())},
        "job_id": "fixture-0512",
        "release": "fixture job label; not a release",
        "reviewer": "fixture-reviewer",
        "routed_by": "fixture-router",
    }
    job_path = handoff / "job.json"
    write_bytes(job_path, canonical(job))
    queued = tool(
        "25-clerk-queue", clerk,
        ["queue", "--store", str(store), "--job", str(job_path), "--instructions-base", str(instructions)],
        code, {0},
    )
    claimed = tool(
        "26-clerk-claim", clerk,
        ["claim", "--store", str(store), "--job", "fixture-0512", "--as", "fixture-builder",
         "--instructions-base", str(instructions)],
        code, {0},
    )
    token = field_after(claimed["stdout"].decode("utf-8", "replace"), "token ")
    outbox = store / "jobs" / "fixture-0512" / "outbox"
    if token:
        write_bytes(outbox / "final-report.md", report)
        write_bytes(outbox / "piece.txt", piece)
        returned = tool(
            "27-clerk-return", clerk,
            ["return", "--store", str(store), "--job", "fixture-0512", "--as", "fixture-builder",
             "--claim", token, "--delivery", "fixture-delivery", "--evidence", "transport line only"],
            code, {0},
        )
        event = field_after(returned["stdout"].decode("utf-8", "replace"), "event 0003.returned.json sha256=")
    else:
        problem("clerk claim did not print a token", "26-clerk-claim")
        event = None
        returned = {"exit": None}
    book_before_door = snapshot(book)
    members_before_door = member_names(book)
    door_result = {"exit": None, "reached_guard": False}
    if event and member:
        binding = {
            "artifact_base": str(outbox),
            "artifacts": [
                {"bytes": len(report), "clerk_path": "final-report.md", "logical": "final-report.md", "sha256": sha(report), "source": "final-report.md"},
                {"bytes": len(piece), "clerk_path": "piece.txt", "logical": "piece.txt", "sha256": sha(piece), "source": "piece.txt"},
            ],
            "assignee": "fixture-builder",
            "book": str(book),
            "clerk_store": str(store),
            "failure_log": str(handoff / "failure.log"),
            "instructions_base": str(instructions),
            "job_id": "fixture-0512",
            "member": member,
            "origin": {"batch": "05.08", "book": "00.00.10.work", "page": "0504.app-entry"},
            "record": str(handoff / "record"),
            "report": {"bytes": len(report), "clerk_path": "final-report.md", "sha256": sha(report), "source": "final-report.md"},
            "returned_event_sha256": event,
            "schema": "clerk-capture-handoff/1",
            "source_root": str(source),
            "submission_id": "hist-0512",
            "work_ref": "hist-0512-work-ref",
        }
        binding_path = handoff / "binding.json"
        write_bytes(binding_path, canonical(binding))
        door_run = tool(
            "28-capture-return", app,
            ["capture-return", "--binding", str(binding_path)],
            code, None,
        )
        door_text = door_run["stdout"].decode("utf-8", "replace")
        door_result = {
            "exit": door_run["exit"],
            "reached_guard": "writer_started: false" in door_text or "line-pass route" in door_text,
        }
        if (book / member / "receipt.json").exists():
            problem("capture-return wrote a receipt on the historical member", "28-capture-return")
        if member_names(book) != members_before_door:
            problem("capture-return allocated a member", "28-capture-return")
        if door_run["exit"] == 0:
            problem("capture-return succeeded on the declared book", "28-capture-return")
    else:
        problem("clerk ceremony did not reach a binding; layout refusal stays with the guard reserve", "27-clerk-return")

    members_before_guard = member_names(book)
    guard_refuse = tool(
        "29-guard-reserve-refused", guard,
        [
            "reserve", "--book", str(book), "--submission", "guard-refuse", "--name", "guard-refuse",
            "--origin-book", "00.00.10.work", "--origin-page", "0504.app-entry", "--origin-batch", "05.08",
            "--submitter", "Grok-2", "--reviewer", "Codex Prime", "--release", "declared-book refusal probe",
        ],
        code, {2},
    )
    guard_text = guard_refuse["stdout"].decode("utf-8", "replace")
    if "writer_started: false" not in guard_text or "result refused" not in guard_text:
        problem("declared reserve did not refuse before the writer", "29-guard-reserve-refused")
    if member_names(book) != members_before_guard:
        problem("declared reserve allocated a member", "29-guard-reserve-refused")
    if member:
        verify_hist = tool(
            "30-historical-verify", guard,
            ["verify", "--book", str(book), "--member", member],
            code, None,
        )
        verify_text = verify_hist["stdout"].decode("utf-8", "replace")
        if "Use the line-pass route" in verify_text or "writer_started: false" in verify_text:
            problem("historical verify was the declared-layout write refusal", "30-historical-verify")
    copy_ready = tool(
        "31-readiness-copy", readiness,
        ["--code-root", str(code), "--book", str(book), "--text"],
        code, {0},
    )
    live_ready = tool(
        "32-readiness-live", live_readiness,
        ["--code-root", str(REPO), "--book", str(LIVE_BOOK), "--text"],
        REPO, {0},
    )
    live_auth = dict(auth_body)
    live_auth["book_path"] = str(LIVE_BOOK)
    live_auth_path = root / "auth" / "live-book-authorization.json"
    write_bytes(live_auth_path, dump(live_auth))
    live_preflight = tool(
        "33-live-preflight", live_backend,
        ["preflight", "--book", str(LIVE_BOOK), "--authorization", str(live_auth_path),
         "--audit", str(audit_path), "--plan", str(plan_path), "--backup", paths["backup"],
         "--staging", paths["staging"], "--retired", paths["retired"]],
        REPO, {2},
    )
    live_text = live_preflight["stdout"].decode("utf-8", "replace") + live_preflight["stderr"].decode("utf-8", "replace")
    if "canonical" not in live_text and "fixture authorization cannot authorize" not in live_text:
        problem("live preflight did not name the canonical refusal", "33-live-preflight")
    live_after = {
        "dispatcher": file_sha(REPO / "app" / "librarian.py"),
        "door": file_sha(DOOR_PAGE),
        "layout_exists": (LIVE_BOOK / "return-line-layout.json").exists(),
    }
    if live_after != live_before:
        problem(f"live identity changed during the run: {live_after}", "33-live-preflight")
    if (code / "00.kernel").exists():
        problem("the copy created its own live-book directory", "33-live-preflight")

    copy_body = leading_json(copy_ready["stdout"]) or {}
    live_body = leading_json(live_ready["stdout"]) or {}
    report = {
        "book": str(book),
        "code": str(code),
        "commands": [{key: value for key, value in item.items() if key not in {"stdout", "stderr"}} for item in COMMANDS],
        "copy_live_path_created": (code / "00.kernel").exists(),
        "dispatcher": dispatcher,
        "door_result": door_result,
        "first_failure": FIRST,
        "fixed_repo_references": roots,
        "historical_member": member,
        "historical_members_after_prepare": members_after_hist,
        "init_exit": init["exit"],
        "layout_sha256": file_sha(layout_path),
        "live_after": live_after,
        "live_before": live_before,
        "n7_review_destination_exists": (book / N7 / "06.01.review.md").is_file(),
        "problems": PROBLEMS,
        "queued_exit": queued["exit"],
        "readiness_copy": {
            "coherent": copy_body.get("coherent"),
            "declared": copy_body.get("declared"),
            "final_check": copy_body.get("final_check"),
            "layout": copy_body.get("layout"),
            "routes": copy_body.get("routes"),
        },
        "readiness_live": {
            "coherent": live_body.get("coherent"),
            "declared": live_body.get("declared"),
            "final_check": live_body.get("final_check"),
            "layout": live_body.get("layout"),
            "routes": live_body.get("routes"),
        },
        "receipt_0501_sha256": receipt_0501_sha,
        "review_n5": review_n5,
        "review_n7": review_n7,
        "schema": "connected-return-review-run/0512",
        "stamp": stamp,
    }
    write_bytes(root / "run-report.json", dump(report))
    write_bytes(root / "code-manifest.json", dump({"files": snapshot(code), "schema": "connected-return-review-files/0512"}))
    write_bytes(root / "book-manifest.json", dump({"files": snapshot(book), "schema": "connected-return-review-files/0512"}))
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
