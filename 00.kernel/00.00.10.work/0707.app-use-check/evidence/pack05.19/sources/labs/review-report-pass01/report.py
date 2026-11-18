#!/usr/bin/env python3
"""Read-only projection of one selected workbook review.

The command calls the pinned librarian review-loop inspect, read, and recover
doors. Attention is taken from record.json only after the journal hash matches
and the judgment matches the core. This process does not record or publish.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "review-report/1"
CORE_SCHEMA = "workbook-review-result/1"
JOURNAL_SCHEMA = "workbook-review-journal/1"
REPARSE = 0x400
PASS = re.compile(r"^05\.\d\d$")
ENVELOPE = (
    "accepted",
    "approved",
    "authority",
    "closes_work",
    "releases_action",
    "task_association",
)
INTERFACE_GAP = (
    "inspect, read, and recover do not return record.attention or "
    "prime_review_effective. Those fields are read from record.json only after "
    "the journal record_sha256 matches and the judgment matches the core."
)
PROPOSED = (
    "Add attention and prime_review_effective from the journal-checked record "
    "to inspect, read, and recover."
)
CLAIM_LIMIT = (
    "The selected record has no structured claim, case, run, or result rows. "
    "Prose in tests_note is not parsed into a pass."
)
HISTORICAL = (
    "The stored render is the historical published bytes. This projection is a "
    "separate reader view and does not replace rendered.md."
)
PINS = {
    "app/librarian.py": (12204, "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"),
    "app/review_loop_tools_v7.py": (10291, "93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d"),
    "app/review-loop-v7.json": (3515, "bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8"),
    "app/review_loop_tools_v6.py": (9175, "e2a5df36efe29f9dad8abd8fa0f842fd98941d58ca1eb3cd4be5227e20420a94"),
    "app/review-loop-v6.json": (2743, "c7f95d16f91644c6465fd3483e3db4d6fb9b9115aa6e20fc09a194fc5bb1f0aa"),
    "app/review_loop_tools_v5.py": (7875, "b1192daf5d265c66f10adfe2125ff0c92a08ccd3c797d229698ecc20e2fdeed9"),
    "app/review-loop-v5.json": (1964, "eaa9120bba2c7274f2218c875ec3ecfc84d291188557049240c30a1c2a430de3"),
    "app/review_loop_tools_v4.py": (13381, "0769179366a6c1659f38cb2c79c51981d5cb76fa8d48ee7325f9eaf00d14c296"),
    "app/review-loop-v4.json": (2519, "769f81321e19a9f3296020e3b0b4a4905ec1b3a66c1629bf53d9548b7182d723"),
    "labs/workbook-review-pass03/workbook.py": (19533, "9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c"),
    "labs/workbook-review-pass03/forms/workbook-review-v1.json": (4532, "4b8cf0e8c81cc421fd0212ae169ba1557998bf526c5f6d87ee170c9d038cbb0b"),
    "labs/workbook-review-pass02/workbook.py": (52574, "6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a"),
    "labs/workbook-review-pass02/forms/workbook-review-v1.json": (4532, "66b3f8f70f8e5d2f940296918767ff0e712e7e144378ad8653259e83d3284645"),
    "labs/workbook-review-pass01/workbook.py": (79131, "60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a"),
    "labs/workbook-review-pass01/forms/workbook-review-v1.json": (4532, "152b436bda8e19d15f252bb5208791c8eefd9a658789e2ab6e9789ffa362b49f"),
    "labs/return-access-pass01/return_access.py": (26561, "501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5"),
    "labs/review-loop-pass03/review_loop.py": (55474, "47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b"),
    "labs/review-construction-pass04/construct.py": (42582, "6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20"),
    "labs/prime-cycle-pass03/prime_cycle.py": (76045, "496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c"),
    "labs/prime-review-pass02/prime_review.py": (58560, "80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e"),
}


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def linked(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def same(left, right) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        if set(left) != set(right):
            return False
        return all(same(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same(a, b) for a, b in zip(left, right))
    return left == right


def parse_args(argv: list[str] | None) -> dict:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 8:
        raise Refuse("usage: report.py --code-root ABS --book ABS --source PAGE --pass 05.NN")
    values: dict[str, str] = {}
    index = 0
    while index < len(args):
        token = args[index]
        if token not in {"--code-root", "--book", "--source", "--pass"}:
            raise Refuse("unknown flag")
        if token in values or index + 1 >= len(args):
            raise Refuse("missing value")
        values[token] = args[index + 1]
        index += 2
    code_text = values["--code-root"]
    book_text = values["--book"]
    source = values["--source"]
    pass_id = values["--pass"]
    code_root = Path(code_text)
    book = Path(book_text)
    if not code_root.is_absolute() or ".." in code_root.parts or linked(code_root) or not code_root.is_dir():
        raise Refuse("code-root must be an absolute directory and was not followed when linked")
    if not book.is_absolute() or ".." in book.parts or linked(book) or not book.is_dir():
        raise Refuse("book must be an absolute directory and was not followed when linked")
    if source.strip() == "" or source.startswith("-") or "/" in source or "\\" in source or "\n" in source or "\r" in source:
        raise Refuse("source is a page id")
    if PASS.fullmatch(pass_id) is None or pass_id.startswith("-"):
        raise Refuse("pass is not 05.NN")
    return {"book": book_text, "code_root": code_root, "pass": pass_id, "source": source}


def check_pins(code_root: Path) -> None:
    for rel, (size, digest) in PINS.items():
        if "\\" in rel or rel.startswith("/") or any(part in {"", ".", ".."} for part in rel.split("/")):
            raise Refuse("pin path escapes")
        cursor = code_root
        for part in rel.split("/"):
            cursor = cursor / part
            if linked(cursor):
                raise Refuse(f"pin path is linked and was not followed: {rel}")
        if not cursor.is_file():
            raise Refuse(f"pin mismatch {rel}")
        data = cursor.read_bytes()
        if len(data) != size or sha256_bytes(data) != digest:
            raise Refuse(f"pin mismatch {rel}")


def core_call(code_root: Path, book: str, source: str, pass_id: str, command: str) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run(
        [
            sys.executable,
            "-B",
            str(code_root / "app" / "librarian.py"),
            "review-loop",
            command,
            "--book",
            book,
            "--source",
            source,
            "--pass",
            pass_id,
        ],
        cwd=str(code_root),
        env=env,
        capture_output=True,
        shell=False,
        check=False,
    )


def parse_core(proc: subprocess.CompletedProcess, command: str) -> dict | None:
    if type(proc.returncode) is not int:
        return None
    try:
        payload = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    if payload.get("schema") != CORE_SCHEMA or payload.get("command") != command:
        return None
    if payload.get("exit") != proc.returncode:
        return None
    return payload


def text_id(payload: dict, key: str) -> str | None:
    value = payload.get(key)
    return value if isinstance(value, str) else None


def list_field(value, recoverable: bool) -> dict:
    if not recoverable or not isinstance(value, list):
        return {"items": None, "state": "unknown"}
    if len(value) == 0:
        return {"items": [], "state": "none-supplied"}
    return {"items": value, "state": "supplied"}


def tests_passed_field(sections: dict | None, recoverable: bool) -> dict:
    blank = {
        "label": None,
        "proof_of_all_tests": False,
        "proof_of_requirements": False,
        "state": "unknown",
        "value": None,
    }
    if not recoverable or not isinstance(sections, dict) or "tests_passed" not in sections:
        return blank
    value = sections["tests_passed"]
    if value is None:
        return blank
    if type(value) is bool:
        return {
            "label": "supplied bounded assessment",
            "proof_of_all_tests": False,
            "proof_of_requirements": False,
            "state": "supplied",
            "value": value,
        }
    return blank


def note_field(sections: dict | None, recoverable: bool, key: str) -> dict:
    if not recoverable or not isinstance(sections, dict) or key not in sections:
        return {"state": "unknown", "text": None}
    value = sections[key]
    if value is None:
        return {"state": "unknown", "text": None}
    if isinstance(value, str):
        return {"state": "supplied", "text": value}
    return {"state": "unknown", "text": None}


def limits_field(sections: dict | None, recoverable: bool) -> dict:
    if not recoverable or not isinstance(sections, dict) or "limits" not in sections:
        return {"state": "unknown", "value": None}
    value = sections["limits"]
    if value is None:
        return {"state": "unknown", "value": None}
    return {"state": "supplied", "value": value}


def publication_class(has_review: bool, status: str | None, target_state: str | None, report_state: str) -> str:
    if report_state == "not-recorded":
        return "not-recorded"
    if not has_review:
        return "unknown"
    if status == "pointer-pending" or target_state == "pointer-pending":
        return "blocked"
    if status == "recorded" or status is None:
        return "recorded"
    if status == "published" and target_state in {"verified", "section-verified"}:
        return "complete"
    if status == "published" and target_state in {"missing", "bytes-changed", "marker-missing", "heading-unreadable"}:
        return "partial"
    return "unknown"


def artifacts_of(inspect: dict | None) -> dict:
    empty = {
        "bytes": None,
        "count": None,
        "hash_match": None,
        "hash_mismatch": None,
        "measurement": None,
        "missing": None,
        "not_verified": None,
        "rows": None,
        "measured_by": "accepted-intake",
    }
    if not isinstance(inspect, dict):
        return empty
    form = inspect.get("form") if isinstance(inspect.get("form"), dict) else {}
    bindings = form.get("bindings") if isinstance(form.get("bindings"), dict) else {}
    rows = bindings.get("rows") if isinstance(bindings.get("rows"), list) else []
    kept = []
    total = 0
    matched = 0
    mismatched = 0
    unverified = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        item = {
            "bytes": row.get("bytes") if isinstance(row.get("bytes"), int) and type(row.get("bytes")) is int else None,
            "declared_bytes": row.get("declared_bytes") if type(row.get("declared_bytes")) is int else None,
            "declared_sha256": row.get("declared_sha256") if isinstance(row.get("declared_sha256"), str) else None,
            "path": row.get("path") if isinstance(row.get("path"), str) else None,
            "role": row.get("role") if isinstance(row.get("role"), str) else None,
            "root": row.get("root") if isinstance(row.get("root"), str) else None,
            "sha256": row.get("sha256") if isinstance(row.get("sha256"), str) else None,
        }
        kept.append(item)
        if type(row.get("bytes")) is int:
            total += row["bytes"]
        if not isinstance(row.get("declared_sha256"), str):
            unverified += 1
        elif row.get("declared_sha256") == row.get("sha256") and type(row.get("declared_bytes")) is int and row.get("declared_bytes") == row.get("bytes"):
            matched += 1
        else:
            mismatched += 1
    missing = []
    findings = inspect.get("findings") if isinstance(inspect.get("findings"), list) else []
    for finding in findings:
        if isinstance(finding, dict) and finding.get("code") in {"artifact-missing", "declared-file-missing"}:
            missing.append({
                "code": finding.get("code"),
                "path": finding.get("path") if isinstance(finding.get("path"), str) else None,
            })
    measurement = inspect.get("measurement") if isinstance(inspect.get("measurement"), str) else None
    return {
        "bytes": total,
        "count": len(kept),
        "hash_match": matched,
        "hash_mismatch": mismatched,
        "measurement": measurement,
        "missing": missing,
        "not_verified": unverified,
        "rows": kept,
        "measured_by": "accepted-intake",
    }


def evidence_of(artifacts: dict) -> dict:
    missing = artifacts.get("missing")
    if isinstance(missing, list) and missing:
        return {"missing": missing, "state": "missing-referenced"}
    return {"missing": [], "state": "not-recorded"}


def claims_of() -> dict:
    return {"limit": CLAIM_LIMIT, "rows": [], "state": "not-recorded"}


def render_coverage(record: dict | None, recoverable: bool, page: str | None, pass_id: str | None, review_id: str | None, rendered_ok) -> dict:
    body = {
        "historical_note": HISTORICAL,
        "omitted": [],
        "path": None,
        "rendered_ok": rendered_ok if type(rendered_ok) is bool else None,
        "shows_attention_lines": None,
        "shows_tests_note": None,
        "shows_tests_passed": None,
        "stored_render_bytes": None,
        "tests_passed_line": None,
    }
    if isinstance(page, str) and isinstance(pass_id, str) and isinstance(review_id, str):
        body["path"] = f"workbook-review/{page}/{pass_id}/reviews/{review_id}/rendered.md"
    if not recoverable or not isinstance(record, dict) or not isinstance(record.get("rendered"), str):
        return body
    render = record["rendered"]
    body["stored_render_bytes"] = len(render.encode("utf-8"))
    found = [
        line for line in render.split("\n")
        if line in {"tests_passed: true", "tests_passed: false", "tests_passed: none supplied"}
    ]
    body["tests_passed_line"] = found[0] if len(found) == 1 else None
    body["shows_tests_passed"] = body["tests_passed_line"] is not None
    sections = record.get("judgment", {}).get("sections") if isinstance(record.get("judgment"), dict) else {}
    note = sections.get("tests_note") if isinstance(sections, dict) else None
    if isinstance(note, str):
        body["shows_tests_note"] = note in render
        if note not in render:
            body["omitted"].append("tests_note")
    limits = sections.get("limits") if isinstance(sections, dict) else None
    if isinstance(limits, str) and limits not in render:
        body["omitted"].append("limits")
    attention = record.get("attention") if isinstance(record.get("attention"), list) else None
    if isinstance(attention, list):
        shown = all(isinstance(line, str) and line in render for line in attention)
        body["shows_attention_lines"] = shown
        if attention and not shown:
            body["omitted"].append("attention")
    judgment = record.get("judgment") if isinstance(record.get("judgment"), dict) else {}
    gaps = judgment.get("gaps") if isinstance(judgment.get("gaps"), list) else []
    if any(isinstance(gap, str) and gap not in render for gap in gaps):
        body["omitted"].append("gaps")
    return body


def read_regular(path: Path) -> bytes | None:
    if linked(path) or not path.is_file():
        return None
    parent = path.parent
    if linked(parent):
        return None
    try:
        return path.read_bytes()
    except OSError:
        return None


def load_json(data: bytes) -> dict | None:
    if data.startswith(b"\xef\xbb\xbf") or b"\r" in data:
        return None
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def base_report(options: dict, state: str, exit_code: int) -> dict:
    return {
        "accepted": None,
        "action_released": None,
        "answers": {"items": None, "state": "unknown"},
        "approved": None,
        "artifacts": artifacts_of(None),
        "attention": {"lines": None, "lines_state": "unknown", "source": None, "state": "unknown"},
        "authority": None,
        "book": options.get("book"),
        "claims": claims_of(),
        "closes_work": None,
        "code_root": str(options.get("code_root")) if options.get("code_root") is not None else None,
        "core": {"inspect_exit": None, "read_exit": None, "recover_exit": None},
        "custody": None,
        "director_text": {"state": "unknown", "text": None},
        "disposition": None,
        "eligible_for_custody_completion": None,
        "evidence_index": {"missing": [], "state": "not-recorded"},
        "exit": exit_code,
        "finding": None,
        "findings": {"items": None, "state": "unknown"},
        "gaps": {"items": None, "state": "unknown"},
        "goal_terminal": None,
        "pass_terminal": None,
        "holds": {"items": None, "state": "unknown"},
        "identity": {
            "inspect_current": None,
            "interface_gap": INTERFACE_GAP,
            "journal_current": None,
            "judgment_matches_core": None,
            "read_review_id": None,
            "record_matches_journal": None,
            "record_sha256": None,
            "recover_review_id": None,
            "selected_by": "none",
        },
        "instance_id": None,
        "intake_findings": None,
        "interface_gap": INTERFACE_GAP,
        "judgment_recorded": False,
        "judgment_recoverable": False,
        "limits": {"state": "unknown", "value": None},
        "next_action": None,
        "operation": None,
        "pass": options.get("pass"),
        "prime_review_effective": None,
        "proposed_core_exposure": PROPOSED,
        "publication": {"class": "unknown", "rendered_sha256": None, "review_id": None, "status": None, "target_state": None},
        "reasons": {"items": None, "state": "unknown"},
        "releases_action": None,
        "render_coverage": render_coverage(None, False, None, None, None, None),
        "review_id": None,
        "schema": SCHEMA,
        "sections": None,
        "source": options.get("source"),
        "stale": None,
        "state": state,
        "successor_of": None,
        "task_association": None,
        "tests_note": {"state": "unknown", "text": None},
        "tests_passed": tests_passed_field(None, False),
        "unknowns": None,
        "work_complete": None,
    }


def apply_envelope(report: dict, inspect: dict, read: dict, recover: dict) -> bool:
    if any(key not in inspect for key in ENVELOPE):
        return False
    for other in (read, recover):
        if any(not same(inspect.get(key), other.get(key)) for key in ENVELOPE):
            return False
    for key in ENVELOPE:
        report[key] = inspect[key]
    report["action_released"] = inspect["releases_action"]
    return True


def apply_intake(report: dict, inspect: dict) -> None:
    report["artifacts"] = artifacts_of(inspect)
    report["evidence_index"] = evidence_of(report["artifacts"])
    report["instance_id"] = inspect.get("instance_id") if isinstance(inspect.get("instance_id"), str) else None
    findings = inspect.get("findings")
    report["intake_findings"] = findings if isinstance(findings, list) else None
    unknowns = inspect.get("unknowns")
    report["unknowns"] = unknowns if isinstance(unknowns, list) else None


def apply_publication(report: dict, inspect: dict, recover: dict, has_review: bool) -> None:
    publication = inspect.get("publication") if isinstance(inspect.get("publication"), dict) else {}
    status = publication.get("status") if isinstance(publication.get("status"), str) else None
    target_state = recover.get("target_state") if isinstance(recover.get("target_state"), str) else None
    rendered = publication.get("rendered_sha256") if isinstance(publication.get("rendered_sha256"), str) else None
    review_id = publication.get("review_id") if isinstance(publication.get("review_id"), str) else None
    report["publication"] = {
        "class": publication_class(has_review, status, target_state, report["state"]),
        "rendered_sha256": rendered,
        "review_id": review_id,
        "status": status,
        "target_state": target_state,
    }


def show_judgment(report: dict, record: dict, recover: dict) -> None:
    judgment = record.get("judgment") if isinstance(record.get("judgment"), dict) else {}
    sections = judgment.get("sections") if isinstance(judgment.get("sections"), dict) else {}
    report["judgment_recoverable"] = True
    report["judgment_recorded"] = True
    report["operation"] = judgment.get("operation") if isinstance(judgment.get("operation"), str) else None
    report["disposition"] = judgment.get("disposition") if isinstance(judgment.get("disposition"), str) else None
    report["finding"] = judgment.get("finding") if isinstance(judgment.get("finding"), str) else None
    report["next_action"] = judgment.get("next_action") if isinstance(judgment.get("next_action"), str) else None
    report["goal_terminal"] = judgment.get("goal_terminal") if isinstance(judgment.get("goal_terminal"), str) else None
    report["pass_terminal"] = judgment.get("pass_terminal") if isinstance(judgment.get("pass_terminal"), str) else None
    report["reasons"] = list_field(judgment.get("reasons"), True)
    report["findings"] = list_field(judgment.get("findings"), True)
    report["holds"] = list_field(record.get("holds"), True)
    report["gaps"] = list_field(judgment.get("gaps"), True)
    report["answers"] = list_field(judgment.get("answers"), True)
    report["sections"] = sections if isinstance(sections, dict) else None
    report["tests_passed"] = tests_passed_field(sections, True)
    report["tests_note"] = note_field(sections, True, "tests_note")
    report["limits"] = limits_field(sections, True)
    if "attention" not in record or not isinstance(record.get("attention"), list) or any(not isinstance(line, str) for line in record.get("attention", [])):
        report["attention"] = {"lines": None, "lines_state": "unknown", "source": None, "state": "unknown"}
    elif len(record["attention"]) == 0:
        report["attention"] = {"lines": [], "lines_state": "none-supplied", "source": "journal-checked-record", "state": "measured"}
    else:
        report["attention"] = {
            "lines": list(record["attention"]),
            "lines_state": "supplied",
            "source": "journal-checked-record",
            "state": "measured",
        }
    if "prime_review_effective" in record and (record.get("prime_review_effective") is None or isinstance(record.get("prime_review_effective"), str)):
        report["prime_review_effective"] = record.get("prime_review_effective")
    if isinstance(record.get("custody"), str):
        report["custody"] = record["custody"]
    elif "custody" in record and record.get("custody") is None:
        report["custody"] = None
    director = record.get("director_text")
    if isinstance(director, str):
        report["director_text"] = {"state": "supplied", "text": director}
    elif director is None:
        report["director_text"] = {"state": "none-measured", "text": None}
    if "successor_of" in record:
        report["successor_of"] = record.get("successor_of") if isinstance(record.get("successor_of"), str) or record.get("successor_of") is None else None
    eligible = record.get("eligible_for_custody_completion")
    if type(eligible) is bool:
        report["eligible_for_custody_completion"] = eligible
        report["work_complete"] = eligible
    rendered_ok = recover.get("rendered_ok") if type(recover.get("rendered_ok")) is bool else None
    report["render_coverage"] = render_coverage(
        record,
        True,
        report["source"],
        report["pass"],
        report["review_id"],
        rendered_ok,
    )
    stale_flags = [recover.get("stale") is True]
    report["stale"] = True if any(stale_flags) else False


def checked_record(book: str, page: str, pass_id: str, review_id: str, expected: str, inspect: dict, recover: dict) -> tuple[dict | None, str]:
    root = Path(book) / "workbook-review" / page / pass_id
    journal_bytes = read_regular(root / "journal.json")
    if journal_bytes is None:
        return None, "journal-unreadable"
    journal = load_json(journal_bytes)
    if journal is None or journal.get("schema") != JOURNAL_SCHEMA or journal.get("current") != review_id:
        return None, "journal-mismatch"
    rows = journal.get("reviews") if isinstance(journal.get("reviews"), list) else []
    record_sha = None
    for item in rows:
        if isinstance(item, dict) and item.get("review_id") == review_id and isinstance(item.get("record_sha256"), str):
            record_sha = item["record_sha256"]
    if record_sha != expected and not isinstance(record_sha, str):
        return None, "journal-mismatch"
    data = read_regular(root / "reviews" / review_id / "record.json")
    if data is None or sha256_bytes(data) != record_sha:
        return None, "record-mismatch"
    record = load_json(data)
    if record is None or not isinstance(record.get("judgment"), dict):
        return None, "record-mismatch"
    if not same(record.get("judgment"), recover.get("judgment")) or not same(record.get("judgment"), inspect.get("judgment")):
        return None, "judgment-mismatch"
    if not same(record.get("custody"), recover.get("custody")):
        return None, "judgment-mismatch"
    return record, "ok"


def journal_expected(book: str, page: str, pass_id: str, review_id: str) -> tuple[str | None, str | None, str]:
    data = read_regular(Path(book) / "workbook-review" / page / pass_id / "journal.json")
    if data is None:
        return None, None, "missing"
    journal = load_json(data)
    if journal is None or journal.get("schema") != JOURNAL_SCHEMA:
        return None, None, "bad"
    current = journal.get("current") if isinstance(journal.get("current"), str) else None
    rows = journal.get("reviews") if isinstance(journal.get("reviews"), list) else []
    digest = None
    for item in rows:
        if isinstance(item, dict) and item.get("review_id") == review_id and isinstance(item.get("record_sha256"), str):
            digest = item["record_sha256"]
    return current, digest, "ok"


def observe(options: dict) -> dict:
    code_root = options["code_root"]
    book = options["book"]
    source = options["source"]
    pass_id = options["pass"]
    procs = {name: core_call(code_root, book, source, pass_id, name) for name in ("inspect", "read", "recover")}
    parsed = {name: parse_core(proc, name) for name, proc in procs.items()}
    if any(parsed[name] is None for name in parsed):
        report = base_report(options, "refused", 2)
        report["core"] = {
            "inspect_exit": procs["inspect"].returncode if type(procs["inspect"].returncode) is int else None,
            "read_exit": procs["read"].returncode if type(procs["read"].returncode) is int else None,
            "recover_exit": procs["recover"].returncode if type(procs["recover"].returncode) is int else None,
        }
        return report
    inspect, read, recover = parsed["inspect"], parsed["read"], parsed["recover"]
    report = base_report(options, "identity-mismatch", 1)
    report["core"] = {
        "inspect_exit": inspect["exit"],
        "read_exit": read["exit"],
        "recover_exit": recover["exit"],
    }
    if inspect.get("page") != source or inspect.get("pass") != pass_id or not same(inspect.get("instance_id"), read.get("instance_id")) or not same(inspect.get("instance_id"), recover.get("instance_id")):
        apply_intake(report, inspect)
        report["identity"]["selected_by"] = "mismatch"
        return report
    if not apply_envelope(report, inspect, read, recover):
        apply_intake(report, inspect)
        report["identity"]["selected_by"] = "mismatch"
        return report
    apply_intake(report, inspect)
    inspect_id = text_id(inspect, "current")
    read_id = text_id(read, "review_id")
    recover_id = text_id(recover, "review_id")
    report["identity"]["inspect_current"] = inspect_id
    report["identity"]["read_review_id"] = read_id
    report["identity"]["recover_review_id"] = recover_id
    no_judgment = (
        read.get("exit") == 2
        and recover.get("exit") == 2
        and read.get("correction") == "No recorded judgment."
        and recover.get("correction") == "No recorded judgment."
        and read_id is None
        and recover_id is None
    )
    if inspect_id is None and read_id is None and recover_id is None:
        report["state"] = "not-recorded"
        report["exit"] = 1
        report["stale"] = None
        report["identity"]["selected_by"] = "none"
        apply_publication(report, inspect, recover, False)
        return report
    if no_judgment and isinstance(inspect_id, str):
        current, digest, journal_state = journal_expected(book, source, pass_id, inspect_id)
        report["state"] = "held"
        report["exit"] = 1
        report["stale"] = True
        report["review_id"] = inspect_id
        report["judgment_recorded"] = current == inspect_id
        report["identity"]["journal_current"] = current
        report["identity"]["record_sha256"] = digest
        report["identity"]["record_matches_journal"] = False
        report["identity"]["selected_by"] = "journal-current" if journal_state == "ok" and current == inspect_id else "none"
        report["attention"] = {"lines": None, "lines_state": "unknown", "source": None, "state": "not-exposed"}
        apply_publication(report, inspect, recover, True)
        return report
    if not (isinstance(inspect_id, str) and inspect_id == read_id == recover_id):
        report["identity"]["selected_by"] = "mismatch"
        apply_publication(report, inspect, recover, False)
        return report
    current, digest, journal_state = journal_expected(book, source, pass_id, inspect_id)
    report["review_id"] = inspect_id
    report["identity"]["journal_current"] = current
    report["identity"]["record_sha256"] = digest
    report["judgment_recorded"] = current == inspect_id
    if journal_state != "ok" or current != inspect_id or not isinstance(digest, str):
        report["identity"]["selected_by"] = "mismatch"
        report["identity"]["record_matches_journal"] = False
        apply_publication(report, inspect, recover, True)
        return report
    record, why = checked_record(book, source, pass_id, inspect_id, digest, inspect, recover)
    if record is None or why != "ok":
        report["attention"] = {"lines": None, "lines_state": "unknown", "source": None, "state": "not-exposed"}
        report["exit"] = 1
        if why == "record-mismatch":
            report["state"] = "held"
            report["stale"] = True
            report["identity"]["selected_by"] = "journal-current"
            report["identity"]["record_matches_journal"] = False
            report["identity"]["judgment_matches_core"] = False
        else:
            report["state"] = "identity-mismatch"
            report["identity"]["selected_by"] = "mismatch"
            report["identity"]["record_matches_journal"] = why == "judgment-mismatch"
            report["identity"]["judgment_matches_core"] = False
        apply_publication(report, inspect, recover, True)
        report["render_coverage"] = render_coverage(None, False, source, pass_id, inspect_id, recover.get("rendered_ok") if type(recover.get("rendered_ok")) is bool else None)
        return report
    report["identity"]["record_matches_journal"] = True
    report["identity"]["judgment_matches_core"] = True
    report["identity"]["selected_by"] = "journal-current"
    show_judgment(report, record, recover)
    inspect_stale = inspect.get("stale") is True
    read_stale = read.get("stale") is True
    recover_stale = recover.get("stale") is True
    report["stale"] = inspect_stale or read_stale or recover_stale
    report["state"] = "stale" if report["stale"] else "readable"
    report["exit"] = 1 if report["stale"] else 0
    apply_publication(report, inspect, recover, True)
    return report


def word(value) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "unknown"
    return str(value)


def projection_of(report: dict) -> str:
    lines = [
        f"state: {report['state']}",
        f"review_id: {word(report['review_id'])}",
        f"publication_class: {report['publication']['class']}",
        f"publication_status: {word(report['publication']['status'])}",
        f"publication_review_id: {word(report['publication']['review_id'])}",
        f"target_state: {word(report['publication']['target_state'])}",
        f"stale: {word(report['stale'])}",
        f"custody: {word(report['custody'])}",
        f"operation: {word(report['operation'])}",
        f"disposition: {word(report['disposition'])}",
        f"goal_terminal: {word(report['goal_terminal'])}",
        f"pass_terminal: {word(report['pass_terminal'])}",
        f"work_complete: {word(report['work_complete'])}",
        f"action_released: {word(report['action_released'])}",
        f"authority: {word(report['authority'])}",
        f"task_association: {word(report['task_association'])}",
        f"closes_work: {word(report['closes_work'])}",
        f"releases_action: {word(report['releases_action'])}",
        f"finding: {word(report['finding'])}",
        f"tests_passed: {word(report['tests_passed']['value']) if report['tests_passed']['state'] == 'supplied' else 'unknown'}",
        f"tests_passed_label: {word(report['tests_passed']['label'])}",
        f"tests_note: {report['tests_note']['text'] if report['tests_note']['state'] == 'supplied' else 'unknown'}",
        "limits: " + (
            report["limits"]["value"] if report["limits"]["state"] == "supplied" and isinstance(report["limits"]["value"], str)
            else "unknown" if report["limits"]["state"] != "supplied"
            else json.dumps(report["limits"]["value"], sort_keys=True)
        ),
        f"attention_state: {report['attention']['state']}",
    ]
    if report["attention"]["lines_state"] == "supplied" and isinstance(report["attention"]["lines"], list):
        lines.append("attention:")
        lines.extend(f"- {line}" for line in report["attention"]["lines"])
    elif report["attention"]["lines_state"] == "none-supplied":
        lines.append("attention: none supplied")
    elif report["attention"]["state"] == "not-exposed":
        lines.append("attention: not exposed")
    else:
        lines.append("attention: unknown")
    lines.append(f"prime_review_effective: {word(report['prime_review_effective']) if report['judgment_recoverable'] else 'unknown'}")
    if report["judgment_recoverable"] and report["prime_review_effective"] is None:
        lines[-1] = "prime_review_effective: none supplied"
    lines.extend([
        f"next_action: {word(report['next_action'])}",
        "director_words: " + (
            report["director_text"]["text"] if report["director_text"]["state"] == "supplied"
            else "none measured" if report["director_text"]["state"] == "none-measured"
            else "unknown"
        ),
    ])
    holds = report["holds"]
    if holds["state"] == "none-supplied":
        lines.append("holds: none supplied")
    elif holds["state"] == "supplied":
        lines.append("holds:")
        for item in holds["items"]:
            if isinstance(item, dict):
                lines.append(f"- {item.get('hold_id')} {item.get('kind')} {item.get('finding_id')}")
            else:
                lines.append("- unknown")
    else:
        lines.append("holds: unknown")
    lines.extend([
        "claims: not-recorded",
        f"evidence_index: {report['evidence_index']['state']}",
        f"artifact_measured_by: {report['artifacts']['measured_by']}",
        f"artifact_count: {word(report['artifacts']['count'])}",
        f"artifact_bytes: {word(report['artifacts']['bytes'])}",
        f"artifact_hash_match: {word(report['artifacts']['hash_match'])}",
        f"artifact_hash_mismatch: {word(report['artifacts']['hash_mismatch'])}",
        f"artifact_missing: {word(len(report['artifacts']['missing']) if isinstance(report['artifacts']['missing'], list) else None)}",
        f"artifact_not_verified: {word(report['artifacts']['not_verified'])}",
        f"measurement: {word(report['artifacts']['measurement'])}",
        "",
        "Detailed projection",
        f"successor_of: {word(report['successor_of']) if report['judgment_recoverable'] else 'unknown'}",
    ])
    if report["judgment_recoverable"] and report["successor_of"] is None:
        lines[-1] = "successor_of: none supplied"
    lines.append("reasons:")
    if report["reasons"]["state"] == "supplied":
        lines.extend(f"- {item}" for item in report["reasons"]["items"])
    else:
        lines.append(report["reasons"]["state"])
    lines.append("judgment_findings:")
    if report["findings"]["state"] == "supplied":
        for item in report["findings"]["items"]:
            if isinstance(item, dict):
                lines.append(f"- {item.get('finding_id')} {item.get('disposition')}: {item.get('text')}")
    else:
        lines.append(report["findings"]["state"])
    lines.append("intake_findings:")
    if isinstance(report["intake_findings"], list) and report["intake_findings"]:
        for item in report["intake_findings"]:
            if isinstance(item, dict):
                lines.append(f"- {item.get('code')} {item.get('path')}")
    elif isinstance(report["intake_findings"], list):
        lines.append("none supplied")
    else:
        lines.append("unknown")
    lines.append("gaps:")
    if report["gaps"]["state"] == "supplied":
        lines.extend(f"- {item}" for item in report["gaps"]["items"])
    else:
        lines.append(report["gaps"]["state"])
    lines.append("selected_replies:")
    if report["answers"]["state"] == "supplied":
        for item in report["answers"]["items"]:
            if isinstance(item, dict):
                lines.append(f"- {item.get('reply')}")
                lines.append(f"  question_id: {item.get('question_id')}")
                lines.append(f"  question_revision: {item.get('question_revision')}")
                lines.append(f"  question_sha256: {item.get('question_sha256')}")
    elif report["answers"]["state"] == "none-supplied":
        lines.append("none supplied")
    else:
        lines.append("unknown")
    lines.append("sections:")
    if isinstance(report["sections"], dict):
        for key in sorted(report["sections"]):
            value = report["sections"][key]
            if value is not None:
                lines.append(f"- {key}: {json.dumps(value, ensure_ascii=False, sort_keys=True)}")
        if all(value is None for value in report["sections"].values()):
            lines.append("unknown")
    else:
        lines.append("unknown")
    lines.append("artifact_rows:")
    rows = report["artifacts"]["rows"]
    if isinstance(rows, list):
        for row in rows:
            lines.append(f"- {row.get('role')} {row.get('path')} {row.get('sha256')} {row.get('bytes')}")
        if not rows:
            lines.append("none supplied")
    else:
        lines.append("unknown")
    coverage = report["render_coverage"]
    lines.append(f"render_path: {word(coverage['path'])}")
    lines.append(f"render_tests_passed_line: {word(coverage['tests_passed_line'])}")
    lines.append("render_omits: " + (", ".join(coverage["omitted"]) if coverage["omitted"] else "none"))
    lines.append(coverage["historical_note"])
    lines.append(report["interface_gap"])
    lines.append(report["proposed_core_exposure"])
    return "\n".join(lines) + "\n"


def finish(report: dict) -> dict:
    report["projection"] = projection_of(report)
    report["publication"]["class"] = publication_class(
        report["review_id"] is not None and report["state"] != "not-recorded",
        report["publication"]["status"],
        report["publication"]["target_state"],
        report["state"],
    )
    return report


def emit(report: dict) -> None:
    raw = (json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    sys.stdout.buffer.write(raw)


def main(argv: list[str] | None = None) -> int:
    blank = {"book": None, "code_root": None, "pass": None, "source": None}
    try:
        options = parse_args(argv)
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        emit(finish(base_report(blank, "refused", 2)))
        return 2
    try:
        check_pins(options["code_root"])
    except Refuse as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        emit(finish(base_report(options, "refused", 2)))
        return 2
    report = finish(observe(options))
    if report["exit"] == 2:
        print("refused: core stdout is not one workbook-review-result/1 object", file=sys.stderr)
    emit(report)
    return int(report["exit"])


if __name__ == "__main__":
    sys.exit(main())
