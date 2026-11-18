#!/usr/bin/env python3
"""0522/05.15 proof driver. Read-only on the live work book. Record and publish stay on disposable books.

usage: drive.py --stamp NEW-DIR
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.dont_write_bytecode = True
REPO = Path(r"D:\Git\lib-build")
PY = Path(r"C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe")
BOOK = REPO / "00.kernel" / "00.00.10.work"
LAB = REPO / "labs" / "review-entry-staging-pass02"
DOOR = REPO / "app" / "review_loop_tools_v9.py"
WORKBOOK = REPO / "labs" / "workbook-review-pass05" / "workbook.py"
DISPATCH = REPO / "app" / "librarian.py"
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
WRITE_COMMANDS = {"record", "publish", "recover"}
INCOMPLETE = "The artifact measurement is incomplete. The judgment was not recorded."
KNOWN_HISTORICAL = {"G7", "I4", "H2", "I6"}
FLAG_EXPECT = {
    "accepted": False,
    "approved": False,
    "authority": "none",
    "closes_work": False,
    "eligible_for_custody_completion": False,
    "published_work": False,
    "releases_action": False,
    "task_association": "not-established",
}
SECTION_KEYS = (
    "affected", "assumptions", "consequences", "exploration", "findings_account", "finish_assessments",
    "for_model", "issue", "learning", "limits", "next_bounded_action", "open_questions", "options",
    "outcome_evidence", "preservation", "prime_finding", "proposed_plan", "question", "recommendation",
    "remaining_choices", "return_result", "tests_note", "tests_passed", "within_direction",
)
FROZEN = (
    "app/librarian.py",
    "README.md",
    "app/README.md",
    "app/review_loop_tools_v4.py",
    "app/review-loop-v4.json",
    "app/review_loop_tools_v5.py",
    "app/review-loop-v5.json",
    "app/review_loop_tools_v6.py",
    "app/review-loop-v6.json",
    "app/review_loop_tools_v7.py",
    "app/review-loop-v7.json",
    "app/review_loop_tools_v8.py",
    "app/review-loop-v8.json",
    "labs/workbook-review-pass01/workbook.py",
    "labs/workbook-review-pass01/forms/workbook-review-v1.json",
    "labs/workbook-review-pass02/workbook.py",
    "labs/workbook-review-pass02/forms/workbook-review-v1.json",
    "labs/workbook-review-pass03/workbook.py",
    "labs/workbook-review-pass03/forms/workbook-review-v1.json",
    "labs/workbook-review-pass04/workbook.py",
    "labs/prime-cycle-pass03/prime_cycle.py",
    "labs/prime-review-pass02/prime_review.py",
    "labs/return-access-pass01/return_access.py",
    "labs/review-loop-pass03/review_loop.py",
    "labs/review-construction-pass04/construct.py",
)
STAGED = (
    "app/review_loop_tools_v9.py",
    "app/review-loop-v9.json",
    "labs/workbook-review-pass05/workbook.py",
)
PAGES = (
    "0522.review-construction",
    "0512.prime-review",
    "0707.app-use-check",
)
SOURCES = (
    ("0522.review-construction", "05.13", "N5", None),
    ("0512.prime-review", "05.06", "N5", None),
    ("0707.app-use-check", "05.15", "N7", 26),
    ("0707.app-use-check", "05.17", "N7", 33),
)
PROBLEMS: list[str] = []
FIRST: dict | None = None


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def problem(message: str, step: str) -> None:
    global FIRST
    PROBLEMS.append(f"{step}: {message}")
    if FIRST is None:
        FIRST = {"step": step, "message": message}
    print(f"PROBLEM {step}: {message}", flush=True)


def identity(path: Path) -> dict | None:
    if not path.is_file():
        return None
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": sha(data)}


def tree(root: Path) -> dict:
    found = {}
    if not root.exists():
        return found
    for path in root.rglob("*"):
        if path.is_file() and not path.is_symlink():
            data = path.read_bytes()
            found[path.relative_to(root).as_posix()] = {"bytes": len(data), "sha256": sha(data)}
    return found


def frozen_now() -> dict:
    return {rel: identity(REPO / rel) for rel in FROZEN}


def staged_now() -> dict:
    return {rel: identity(REPO / rel) for rel in STAGED}


def pages_now() -> dict:
    return {name: tree(BOOK / name) for name in PAGES}


def custody_now() -> dict:
    names = (
        "0122.review-construction",
        "0112.prime-review",
        "0122.review-construction/05.15.return.md",
        "0122.review-construction/05.14.return.md",
        "0122.review-construction/05.13.return.md",
        "0112.prime-review/05.06.return.md",
    )
    return {name: identity(BOOK / name) if (BOOK / name).is_file() else {"present": (BOOK / name).exists()} for name in names}


def dump(path: Path, body) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes((json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def run(args: list[str], cwd: Path, timeout: int = 300) -> dict:
    proc = subprocess.run(
        [str(PY), "-B", *args],
        cwd=str(cwd),
        env=ENV,
        capture_output=True,
        timeout=timeout,
    )
    return {
        "exit": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "replace"),
        "stderr": proc.stderr.decode("utf-8", "replace"),
    }


def parse_body(result: dict) -> dict | None:
    text = result["stdout"].strip()
    if text == "":
        return None
    try:
        value, _end = json.JSONDecoder().raw_decode(text)
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def bindings_of(body: dict | None):
    if not isinstance(body, dict):
        return None
    form = body.get("form")
    if not isinstance(form, dict):
        return None
    bindings = form.get("bindings")
    return bindings if isinstance(bindings, dict) else None


def rows_of(body: dict | None):
    bindings = bindings_of(body)
    if bindings is None:
        return None
    return bindings.get("rows")


def findings_of(body: dict | None, command: str):
    if not isinstance(body, dict):
        return None
    if command == "form":
        bindings = bindings_of(body)
        if bindings is None:
            return None
        return bindings.get("findings")
    return body.get("findings")


def artifact_count(body: dict | None) -> int | None:
    rows = rows_of(body)
    if not isinstance(rows, list):
        return None
    return sum(1 for row in rows if isinstance(row, dict) and row.get("role") == "artifact")


def notes_diagnostic(body: dict | None) -> bool:
    findings = [] if body is None else body.get("findings") or []
    return any(
        isinstance(item, dict) and item.get("code") == "unparsed-return-line" and str(item.get("text") or "").startswith("Notes:")
        for item in findings
    )


def canonical(stamp: Path, before_pages: dict, before_frozen: dict) -> dict:
    book = str(BOOK)
    (stamp / "canonical").mkdir(parents=True, exist_ok=True)
    out = {"sources": []}
    for source, pas, kind, expect in SOURCES:
        for command in ("prepare", "form"):
            result = run([str(DOOR), command, "--book", book, "--source", source, "--pass", pas], REPO, 300)
            body = parse_body(result)
            name = f"{source}-{pas}-{command}"
            (stamp / "canonical" / f"{name}.stdout.json").write_bytes(result["stdout"].encode("utf-8", "replace"))
            (stamp / "canonical" / f"{name}.stderr.txt").write_bytes(result["stderr"].encode("utf-8", "replace"))
            item = {
                "command": command,
                "exit": result["exit"],
                "source": source,
                "pass": pas,
                "kind": kind,
                "intake_id": None if body is None else body.get("intake_id"),
                "measurement": None if body is None else body.get("measurement"),
                "artifact_count": artifact_count(body),
                "finding_codes": sorted({f.get("code") for f in (body or {}).get("findings") or [] if isinstance(f, dict)}),
                "form_finding_codes": sorted({f.get("code") for f in (findings_of(body, "form") or []) if isinstance(f, dict)}),
                "notes_diagnostic": notes_diagnostic(body),
                "stderr_tail": result["stderr"][-240:],
                "json": body is not None,
            }
            if kind == "N5":
                current = run(
                    [str(DISPATCH), "review-loop", command, "--book", book, "--source", source, "--pass", pas],
                    REPO,
                    300,
                )
                current_body = parse_body(current)
                (stamp / "canonical" / f"{name}.v7.stdout.json").write_bytes(current["stdout"].encode("utf-8", "replace"))
                (stamp / "canonical" / f"{name}.v7.stderr.txt").write_bytes(current["stderr"].encode("utf-8", "replace"))
                same_rows = json.dumps(rows_of(body), sort_keys=True) == json.dumps(rows_of(current_body), sort_keys=True)
                same_findings = json.dumps(findings_of(body, command), sort_keys=True) == json.dumps(findings_of(current_body, command), sort_keys=True)
                same_id = body is not None and current_body is not None and body.get("intake_id") == current_body.get("intake_id")
                same_cuts = True
                if command == "prepare":
                    same_cuts = json.dumps(body.get("cuts") if body else None, sort_keys=True) == json.dumps(current_body.get("cuts") if current_body else None, sort_keys=True)
                same = same_rows and same_findings and same_id and same_cuts
                item["v7_exit"] = current["exit"]
                item["v7_intake_id"] = None if current_body is None else current_body.get("intake_id")
                item["matches_v7"] = same
                if not same:
                    problem(f"{source}/{pas} N5 {command} differs from librarian.py review-loop {command}", "canonical")
            if command == "prepare" and kind == "N7":
                count = artifact_count(body)
                item["expect_artifacts"] = expect
                if result["exit"] != 0 or body is None or body.get("measurement") != "complete" or count != expect or not notes_diagnostic(body):
                    problem(
                        f"{source}/{pas} N7 prepare exit {result['exit']} measurement {None if body is None else body.get('measurement')} artifacts {count} notes {notes_diagnostic(body)}",
                        "canonical",
                    )
            if result["exit"] != 0 or body is None:
                problem(f"{source}/{pas} {command} exit {result['exit']}", "canonical")
            out["sources"].append(item)
            print(f"canonical {source} {pas} {command} exit {result['exit']}", flush=True)
    after_pages = pages_now()
    after_frozen = frozen_now()
    out["pages_unchanged"] = after_pages == before_pages
    out["frozen_unchanged"] = after_frozen == before_frozen
    out["custody_after"] = custody_now()
    if after_pages != before_pages:
        changed = [name for name in PAGES if after_pages[name] != before_pages[name]]
        problem(f"live page bytes changed: {changed}", "canonical")
    if after_frozen != before_frozen:
        problem("frozen module bytes changed during canonical checks", "canonical")
    return out


def suite(stamp: Path, label: str, script: Path, timeout: int) -> dict:
    root = stamp / label
    out = stamp / f"{label}.json"
    result = run([str(script), "--root", str(root), "--out", str(out)], REPO, timeout)
    (stamp / f"{label}.stdout.txt").write_bytes(result["stdout"].encode("utf-8", "replace"))
    (stamp / f"{label}.stderr.txt").write_bytes(result["stderr"].encode("utf-8", "replace"))
    body = None
    if out.is_file():
        body = json.loads(out.read_text(encoding="utf-8"))
    summary = {
        "exit": result["exit"],
        "aggregate": None if body is None else body.get("aggregate"),
        "first_failure": None if body is None else body.get("first_failure"),
        "stderr_tail": result["stderr"][-400:],
        "failures": [],
    }
    if isinstance(body, dict):
        for row in body.get("rows") or []:
            if row.get("status") != "PASS":
                summary["failures"].append({"id": row.get("id"), "status": row.get("status"), "detail": row.get("detail")})
    print(f"suite {label} exit {result['exit']} {summary['aggregate']} first {summary['first_failure']}", flush=True)
    return summary


def copy_door(dest: Path) -> None:
    document = json.loads((REPO / "app/review-loop-v9.json").read_bytes())
    rels = ["app/review_loop_tools_v9.py", "app/review-loop-v9.json"]
    rels.extend(item["path"] for item in document["tools"].values())
    for rel in dict.fromkeys(rels):
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((REPO / rel).read_bytes())


def door_prepare(root: Path) -> dict:
    book = root / "empty-book"
    book.mkdir(parents=True, exist_ok=True)
    return run(
        [str(root / "app/review_loop_tools_v9.py"), "prepare", "--book", str(book), "--source", "0599.staging-n5", "--pass", "05.01"],
        root,
        120,
    )


def pin_cases(stamp: Path) -> dict:
    base = stamp / "pins"
    cases = {}

    def one(name: str, mutate, text: str) -> None:
        root = base / name
        copy_door(root)
        mutate(root)
        result = door_prepare(root)
        ok = result["exit"] == 2 and text in result["stderr"]
        cases[name] = {"exit": result["exit"], "expect": text, "ok": ok, "stderr_tail": result["stderr"][-300:]}
        if not ok:
            problem(f"{name} exit {result['exit']} stderr {result['stderr'][-180:]}", "pins")
        print(f"pin {name} exit {result['exit']} ok {ok}", flush=True)

    def tamper(rel: str):
        def mutate(root: Path) -> None:
            path = root / rel
            path.write_bytes(path.read_bytes() + b"\n# disposable tamper\n")
        return mutate

    def drop(rel: str):
        def mutate(root: Path) -> None:
            (root / rel).unlink()
        return mutate

    def bad_schema(root: Path) -> None:
        path = root / "app/review-loop-v9.json"
        document = json.loads(path.read_bytes())
        document["schema"] = "review-loop-pins/6"
        path.write_bytes((json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"))

    def bad_workbook_bytes(root: Path) -> None:
        path = root / "app/review-loop-v9.json"
        document = json.loads(path.read_bytes())
        document["tools"]["workbook"]["bytes"] = document["tools"]["workbook"]["bytes"] + 1
        path.write_bytes((json.dumps(document, indent=2, sort_keys=True) + "\n").encode("utf-8"))

    one("pass03-tamper", tamper("labs/workbook-review-pass03/workbook.py"), "pass03 pin mismatch")
    one("pass04-tamper", tamper("labs/workbook-review-pass04/workbook.py"), "pass04 pin mismatch")
    one("missing-prime-cycle", drop("labs/prime-cycle-pass03/prime_cycle.py"), "pinned tool is missing: labs/prime-cycle-pass03/prime_cycle.py")
    one("missing-declaration", drop("app/review-loop-v9.json"), "review loop declaration is missing")
    one("schema", bad_schema, "schema is not review-loop-pins/7")
    one("workbook-bytes", bad_workbook_bytes, "pinned tool hash does not match: labs/workbook-review-pass05/workbook.py")
    return cases


def write_page(folder: Path, name: str, body: str) -> None:
    path = folder / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body.encode("utf-8"))


def manifest_for(artifact_rel: str, artifact: bytes) -> bytes:
    body = {"files": [{"bytes": len(artifact), "path": artifact_rel, "sha256": sha(artifact)}]}
    return (json.dumps(body, indent=2, sort_keys=True) + "\n").encode("utf-8")


def judgment() -> dict:
    sections = {key: None for key in SECTION_KEYS}
    sections["findings_account"] = []
    sections["next_bounded_action"] = "Disposable staging only."
    sections["prime_finding"] = "Supplied test data. This is not an independent semantic review."
    sections["return_result"] = "The disposable record stored this judgment. This sentence is supplied test data."
    sections["tests_note"] = "Supplied test data."
    sections["tests_passed"] = None
    sections["within_direction"] = "The run stays on the disposable book."
    return {
        "answers": [],
        "design_fork": None,
        "disposition": "held",
        "finding": "Supplied test data for the 0522/05.15 disposable cycle.",
        "findings": [],
        "gaps": ["Supplied test data, not an independent review."],
        "goal_terminal": "open",
        "holds": [],
        "next_action": "Prime reviews the staged v9 declaration block. This sentence is supplied test data.",
        "operation": "continue",
        "pass_terminal": "open",
        "reasons": ["The judgment text is supplied test data."],
        "review_passes": [],
        "sections": sections,
        "semantic_conflict": None,
    }


def live_collision(rel: str) -> bool:
    return (REPO / rel).exists()


def call_book(book: Path, source: str, pas: str, command: str, extra: list[str] | None = None) -> dict:
    if str(book).lower().startswith(str(BOOK).lower()) and command in WRITE_COMMANDS:
        raise SystemExit(f"refused: {command} on the live book")
    args = [str(DOOR), command, "--book", str(book), "--source", source, "--pass", pas, *(extra or [])]
    result = run(args, REPO, 300)
    body = parse_body(result)
    return {"exit": result["exit"], "body": body, "stderr_tail": result["stderr"][-400:], "stdout": result["stdout"]}


def flags_ok(body: dict | None) -> bool:
    if not isinstance(body, dict):
        return False
    return all(body.get(key) == value for key, value in FLAG_EXPECT.items())


def build_n5(book: Path, source: str, review: str) -> Path:
    page = book / source
    submission = b"Disposable submission for the staging cycle.\n"
    note = b"Disposable artifact for the staging cycle.\n"
    sub_rel = f"{source}/evidence/submission.md"
    note_rel = f"{source}/evidence/note.md"
    man_rel = f"{source}/evidence/artifact-manifest.json"
    if any(live_collision(rel) for rel in (sub_rel, note_rel, man_rel, f"{source}/05.01.md")):
        raise SystemExit("refused: synthetic path collides with the live checkout")
    manifest = manifest_for(note_rel, note)
    pointer = (
        f"Submission: {sub_rel} sha256 {sha(submission)}, {len(submission)} bytes.\n"
        f"Artifact manifest: {man_rel} sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
    )
    text = (
        f"# 05.01 - {source}\n\n## Goal\n\nMeasure a disposable review cycle on an external book.\n\n"
        f"## Scope\n\nThis disposable book only.\n\n## Return pointer\n\n{pointer}\n## Review - Codex Prime\n{review}\n"
    )
    write_page(page, "05.01.md", text)
    write_page(page, "evidence/submission.md", submission.decode("utf-8"))
    write_page(page, "evidence/note.md", note.decode("utf-8"))
    (page / "evidence/artifact-manifest.json").write_bytes(manifest)
    return page / "05.01.md"


def build_n7(book: Path, source: str, malformed: bool = False) -> Path:
    page = book / source
    returned = b"Disposable N7 return for the staging cycle.\n"
    note = b"Disposable N7 artifact for the staging cycle.\n"
    ret_rel = f"{source}/evidence/return.md"
    note_rel = f"{source}/evidence/note.md"
    man_rel = f"{source}/evidence/artifact-manifest.json"
    if any(live_collision(rel) for rel in (ret_rel, note_rel, man_rel, f"{source}/05.01.pack.md", f"{source}/06.01.review.md")):
        raise SystemExit("refused: synthetic path collides with the live checkout")
    manifest = manifest_for(note_rel, note)
    if malformed:
        pointer = (
            f"Artifact manifest: {man_rel}, sha256 {sha(manifest)}, {len(manifest)} bytes. note\n"
            f"Returned: {ret_rel} (staging attribution), sha256 {sha(returned)}, {len(returned)} bytes.\n"
        )
    else:
        pointer = (
            f"Returned: {ret_rel} (staging attribution), sha256 {sha(returned)}, {len(returned)} bytes.\n"
            f"Artifact manifest: {man_rel}, sha256 {sha(manifest)}, {len(manifest)} bytes.\n"
        )
    text = (
        f"# 05.01 - {source}\n\n## Goal\n\nMeasure a disposable N7 review cycle on an external book.\n\n"
        f"## Scope\n\nThis disposable book only.\n\n## Return pointer\n\n{pointer}\n"
    )
    write_page(page, "05.01.pack.md", text)
    write_page(page, "evidence/return.md", returned.decode("utf-8"))
    write_page(page, "evidence/note.md", note.decode("utf-8"))
    (page / "evidence/artifact-manifest.json").write_bytes(manifest)
    return page / "05.01.pack.md"


def brief(step: dict) -> dict:
    body = step["body"] if isinstance(step["body"], dict) else {}
    judgment_body = body.get("judgment") if isinstance(body.get("judgment"), dict) else {}
    return {
        "exit": step["exit"],
        "measurement": body.get("measurement"),
        "mode": body.get("mode"),
        "custody": body.get("custody"),
        "published": body.get("published"),
        "recorded": body.get("recorded"),
        "review_id": body.get("review_id"),
        "next_action": body.get("next_action") or judgment_body.get("next_action"),
        "finding": judgment_body.get("finding"),
        "correction": body.get("correction"),
        "accepted": body.get("accepted"),
        "flags_ok": flags_ok(body) if step["body"] else False,
        "stderr_tail": step["stderr_tail"],
        "cycle": body.get("cycle"),
    }


def stored_cycle(book: Path, source: str, pas: str, review_id: str | None) -> dict | None:
    if not isinstance(review_id, str):
        return None
    path = book / "workbook-review" / source / pas / "reviews" / review_id / "record.json"
    if not path.is_file():
        return {"present": False}
    document = json.loads(path.read_bytes())
    cycle = document.get("cycle") if isinstance(document.get("cycle"), dict) else {}
    return {"called": cycle.get("called"), "committed": cycle.get("committed"), "mode": document.get("mode")}


def lifecycle(stamp: Path, judge_path: Path) -> dict:
    out = {}
    judge = json.loads(judge_path.read_bytes())
    expected_action = judge["next_action"]
    expected_finding = judge["finding"]

    def cycle(name: str, book: Path, source: str, pas: str, target: Path | None) -> None:
        before = None if target is None or not target.exists() else target.read_bytes()
        steps = {}
        prepared = call_book(book, source, pas, "prepare")
        steps["prepare"] = brief(prepared)
        formed = call_book(book, source, pas, "form")
        steps["form"] = brief(formed)
        intake_id = (prepared["body"] or {}).get("intake_id")
        recorded = call_book(book, source, pas, "record", ["--intake", str(intake_id), "--judgment", str(judge_path.resolve())])
        steps["record"] = brief(recorded)
        review_id = (recorded["body"] or {}).get("review_id")
        steps["stored_cycle"] = stored_cycle(book, source, pas, review_id if isinstance(review_id, str) else None)
        inspected = call_book(book, source, pas, "inspect")
        steps["inspect"] = brief(inspected)
        read1 = call_book(book, source, pas, "read")
        steps["read"] = brief(read1)
        published = call_book(book, source, pas, "publish", ["--review", str(review_id)])
        steps["publish"] = brief(published)
        read2 = call_book(book, source, pas, "read")
        steps["read-after"] = brief(read2)
        recovered = call_book(book, source, pas, "recover")
        steps["recover"] = brief(recovered)
        read3 = call_book(book, source, pas, "read")
        steps["read-again"] = brief(read3)
        recovered2 = call_book(book, source, pas, "recover")
        steps["recover-again"] = brief(recovered2)
        after = None if target is None or not target.exists() else target.read_bytes()
        actions = [steps[key].get("next_action") for key in ("record", "read", "publish", "read-after", "recover", "read-again", "recover-again")]
        findings = [steps[key].get("finding") for key in ("record", "read", "read-after", "recover", "read-again")]
        kept = all(item == expected_action for item in actions if item is not None) and all(item == expected_finding for item in findings if item is not None)
        if not kept:
            problem(f"{name} judgment or next action was not preserved", "lifecycle")
        if steps["record"]["exit"] != 0:
            problem(f"{name} record exit {steps['record']['exit']} {steps['record']['correction']}", "lifecycle")
        out[name] = {
            "steps": steps,
            "target_existed_before": before is not None,
            "target_exists_after": after is not None,
            "target_unchanged": before == after,
            "judgment_preserved": kept,
            "measurement": steps["prepare"].get("measurement"),
        }
        print(f"lifecycle {name} record {steps['record']['exit']} publish {steps['publish']['exit']} kept {kept}", flush=True)

    n5_book = stamp / "life-n5" / "book"
    n5_page = build_n5(n5_book, "0599.staging-n5", "PENDING.\n")
    n5_before = n5_page.read_bytes()
    cycle("n5", n5_book, "0599.staging-n5", "05.01", None)
    out["n5"]["assignment_sha_before"] = sha(n5_before)
    out["n5"]["assignment_sha_after"] = sha(n5_page.read_bytes())
    out["n5"]["assignment_unchanged"] = n5_page.read_bytes() == n5_before
    n7_book = stamp / "life-n7" / "book"
    build_n7(n7_book, "0799.staging-n7")
    review = n7_book / "0799.staging-n7" / "06.01.review.md"
    if review.exists():
        problem("N7 review file existed before the cycle", "lifecycle")
    cycle("n7", n7_book, "0799.staging-n7", "05.01", review)
    return out


def manual_director(stamp: Path) -> dict:
    book = stamp / "manual" / "book"
    page = build_n5(book, "0598.staging-manual", "Director response: keep this sentence.\n")
    before = page.read_bytes()
    prepared = call_book(book, "0598.staging-manual", "05.01", "prepare")
    intake_id = (prepared["body"] or {}).get("intake_id")
    judge_path = stamp / "judgment.json"
    recorded = call_book(book, "0598.staging-manual", "05.01", "record", ["--intake", str(intake_id), "--judgment", str(judge_path.resolve())])
    review_id = (recorded["body"] or {}).get("review_id")
    published = call_book(book, "0598.staging-manual", "05.01", "publish", ["--review", str(review_id)])
    after = page.read_bytes()
    ok = before == after and published["exit"] != 0 and "manual-review" in str((published["body"] or {}).get("correction"))
    if not ok:
        problem(f"manual director text changed or was not held: exit {published['exit']}", "manual")
    print(f"manual publish exit {published['exit']} held {ok}", flush=True)
    return {
        "bytes_unchanged": before == after,
        "publish_exit": published["exit"],
        "correction": None if published["body"] is None else published["body"].get("correction"),
        "published": None if published["body"] is None else published["body"].get("published"),
        "ok": ok,
    }


def hostile(stamp: Path) -> dict:
    out = {}
    copied = stamp / "hostile-root" / "workbook.py"
    copied.parent.mkdir(parents=True, exist_ok=True)
    copied.write_bytes(WORKBOOK.read_bytes())
    sentinel = copied.parent / "sentinel.txt"
    sentinel.write_bytes(b"sentinel-unchanged\n")
    result = run([str(copied), "prepare", "--book", str(stamp / "hostile-root" / "book"), "--source", "0599.staging-n5", "--pass", "05.01"], copied.parent, 60)
    out["copied-workbook"] = {
        "exit": result["exit"],
        "stderr_tail": result["stderr"][-240:],
        "sentinel_unchanged": sentinel.read_bytes() == b"sentinel-unchanged\n",
        "ok": result["exit"] == 2 and "not at its canonical root" in result["stderr"] and sentinel.read_bytes() == b"sentinel-unchanged\n",
    }
    if not out["copied-workbook"]["ok"]:
        problem(f"copied workbook exit {result['exit']}", "hostile")
    book = stamp / "hostile-stale" / "book"
    page = build_n7(book, "0798.staging-hostile")
    returned = book / "0798.staging-hostile" / "evidence" / "return.md"
    prepared = call_book(book, "0798.staging-hostile", "05.01", "prepare")
    intake_id = (prepared["body"] or {}).get("intake_id")
    before = page.read_bytes()
    returned.write_bytes(returned.read_bytes() + b"\naltered\n")
    altered = returned.read_bytes()
    recorded = call_book(
        book,
        "0798.staging-hostile",
        "05.01",
        "record",
        ["--intake", str(intake_id), "--judgment", str((stamp / "judgment.json").resolve())],
    )
    review = book / "0798.staging-hostile" / "06.01.review.md"
    ok = (
        recorded["exit"] == 2
        and (recorded["body"] or {}).get("correction") == INCOMPLETE
        and not review.exists()
        and returned.read_bytes() == altered
        and page.read_bytes() == before
    )
    out["changed-source"] = {
        "prepare_exit": prepared["exit"],
        "prepare_measurement": None if prepared["body"] is None else prepared["body"].get("measurement"),
        "record_exit": recorded["exit"],
        "correction": None if recorded["body"] is None else recorded["body"].get("correction"),
        "review_absent": not review.exists(),
        "altered_bytes_kept": returned.read_bytes() == altered,
        "pack_bytes_kept": page.read_bytes() == before,
        "ok": ok,
    }
    if not ok:
        problem(f"changed source record exit {recorded['exit']} correction {(recorded['body'] or {}).get('correction')}", "hostile")
    print(f"hostile copy {out['copied-workbook']['ok']} changed-source {ok}", flush=True)
    return out


def block_record(stamp: Path) -> dict:
    book = stamp / "block-record" / "book"
    page = build_n7(book, "0797.block-n7", malformed=True)
    before = page.read_bytes()
    prepared = call_book(book, "0797.block-n7", "05.01", "prepare")
    formed = call_book(book, "0797.block-n7", "05.01", "form")
    prepare_body = prepared["body"] or {}
    form_body = formed["body"] or {}
    form_findings = findings_of(form_body, "form") or []
    form_codes = [item.get("code") for item in form_findings if isinstance(item, dict)]
    rows = rows_of(prepare_body) or []
    intake_id = prepare_body.get("intake_id")
    recorded = call_book(
        book,
        "0797.block-n7",
        "05.01",
        "record",
        ["--intake", str(intake_id), "--judgment", str((stamp / "judgment.json").resolve())],
    )
    review = book / "0797.block-n7" / "06.01.review.md"
    record_body = recorded["body"] or {}
    ok = (
        prepared["exit"] == 0
        and prepare_body.get("measurement") == "incomplete"
        and "malformed-n7-declaration" in [item.get("code") for item in (prepare_body.get("findings") or [])]
        and formed["exit"] == 0
        and form_body.get("intake_id") == intake_id
        and "malformed-n7-declaration" in form_codes
        and not any(isinstance(row, dict) and row.get("role") == "submission" for row in rows)
        and recorded["exit"] == 2
        and record_body.get("correction") == INCOMPLETE
        and record_body.get("recorded") is False
        and record_body.get("accepted") is False
        and record_body.get("published") is not True
        and not review.exists()
        and page.read_bytes() == before
    )
    if not ok:
        problem(f"malformed record exit {recorded['exit']} correction {record_body.get('correction')}", "block")
    print(f"block prepare {prepare_body.get('measurement')} record {recorded['exit']} ok {ok}", flush=True)
    return {
        "prepare_exit": prepared["exit"],
        "measurement": prepare_body.get("measurement"),
        "form_exit": formed["exit"],
        "form_intake_matches": form_body.get("intake_id") == intake_id,
        "form_codes": form_codes,
        "record_exit": recorded["exit"],
        "correction": record_body.get("correction"),
        "recorded": record_body.get("recorded"),
        "accepted": record_body.get("accepted"),
        "published": record_body.get("published"),
        "review_absent": not review.exists(),
        "source_unchanged": page.read_bytes() == before,
        "ok": ok,
    }


def source_manifest() -> dict:
    pack = BOOK / "0522.review-construction" / "evidence" / "pack05.15"
    blob = (pack / "source-manifest.json").read_bytes()
    manifest = json.loads(blob)
    missing = []
    mismatches = []
    for row in manifest["files"]:
        live = REPO / row["path"]
        snap = pack / row["snapshot"]
        if not live.is_file() or not snap.is_file():
            missing.append(row["path"])
            continue
        live_bytes = live.read_bytes()
        snap_bytes = snap.read_bytes()
        if (
            len(live_bytes) != row["bytes"]
            or sha(live_bytes) != row["sha256"]
            or len(snap_bytes) != row["bytes"]
            or sha(snap_bytes) != row["sha256"]
            or live_bytes != snap_bytes
        ):
            mismatches.append(row["path"])
    return {
        "schema": manifest.get("schema"),
        "files": len(manifest["files"]),
        "missing": missing,
        "mismatches": mismatches,
        "manifest_bytes": len(blob),
        "manifest_sha256": sha(blob),
        "manifest_cr": blob.count(b"\r"),
    }


def classify_historical(summary: dict) -> dict:
    failed = {item["id"] for item in summary.get("failures") or []}
    unexpected = sorted(failed - KNOWN_HISTORICAL)
    errors = [item["id"] for item in summary.get("failures") or [] if item.get("status") == "ERROR"]
    summary["unexpected"] = unexpected
    summary["known_historical"] = sorted(failed & KNOWN_HISTORICAL)
    if unexpected or errors:
        problem(f"historical unexpected {unexpected} errors {errors}", "historical")
    return summary


def main() -> int:
    stamp_arg = sys.argv[sys.argv.index("--stamp") + 1]
    stamp = Path(stamp_arg)
    if str(stamp.resolve()).lower().startswith(str(REPO).lower()):
        raise SystemExit("refused: stamp inside the checkout")
    stamp.mkdir(parents=True, exist_ok=False)
    before_pages = pages_now()
    before_frozen = frozen_now()
    before_staged = staged_now()
    before_custody = custody_now()
    dump(stamp / "judgment.json", judgment())
    report = {
        "schema": "v9-n7-declaration-block-drive/0515",
        "started": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "stamp": str(stamp),
        "custody_before": before_custody,
        "canonical": canonical(stamp, before_pages, before_frozen),
        "cases_block": suite(stamp, "cases-block", LAB / "suite" / "tests" / "test_block.py", 300),
        "cases_v2": suite(stamp, "cases-v2", LAB / "suite" / "tests" / "test_n7v2.py", 900),
        "cases_17": suite(stamp, "cases-17", LAB / "suite" / "compat17" / "tests" / "test_n7.py", 900),
        "pins": pin_cases(stamp),
        "hostile": hostile(stamp),
        "manual": manual_director(stamp),
        "lifecycle": lifecycle(stamp, stamp / "judgment.json"),
        "block_record": block_record(stamp),
    }
    report["cases_17"] = classify_historical(report["cases_17"])
    if report["cases_block"]["exit"] != 0 or report["cases_block"]["failures"]:
        problem(f"block suite {report['cases_block']['aggregate']} first {report['cases_block']['first_failure']}", "block-suite")
    if report["cases_v2"]["exit"] != 0 or report["cases_v2"]["failures"]:
        problem(f"12-case suite {report['cases_v2']['aggregate']} first {report['cases_v2']['first_failure']}", "cases-v2")
    report["source_manifest_end"] = source_manifest()
    report["frozen_end"] = frozen_now()
    report["staged_end"] = staged_now()
    report["pages_end_unchanged"] = pages_now() == before_pages
    report["frozen_end_unchanged"] = report["frozen_end"] == before_frozen
    report["staged_end_unchanged"] = report["staged_end"] == before_staged
    report["custody_end"] = custody_now()
    if report["source_manifest_end"]["missing"] or report["source_manifest_end"]["mismatches"]:
        problem("source manifest mismatch at the end", "manifest")
    if not report["pages_end_unchanged"]:
        problem("live page bytes differ at the end", "manifest")
    if not report["frozen_end_unchanged"]:
        problem("frozen bytes differ at the end", "manifest")
    if not report["staged_end_unchanged"]:
        problem("staged bytes differ at the end", "manifest")
    report["problems"] = PROBLEMS
    report["first"] = FIRST
    dump(stamp / "report.json", report)
    print(json.dumps({"problems": len(PROBLEMS), "first": FIRST, "stamp": str(stamp)}, indent=2), flush=True)
    return 0 if not PROBLEMS else 1


if __name__ == "__main__":
    sys.exit(main())
