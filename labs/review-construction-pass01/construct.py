#!/usr/bin/env python3
"""Render a full Prime assessment into a workflow review section.

Preview writes nothing. Apply writes only inside a disposable fixture root
outside D:\\Git\\lib-build. Judgment words come from a supplied prime-review
record. This tool does not accept, release, close, allocate, or establish custody.

Compare-then-rename narrows a stale write. It is not proof of race freedom.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(r"D:\Git\lib-build")
TOOL = ROOT / "labs" / "prime-review-pass01" / "prime_review.py"
TOOL_SHA256 = "805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0"
TOOL_BYTES = 58324

SCHEMA = "review-construction/1"
HEADING_EM = "## Review — Codex Prime"
HEADING_HYPHEN = "## Review - Codex Prime"
HEADINGS = (HEADING_EM, HEADING_HYPHEN)
NEXT_HEADING = re.compile(r"^## [^#]")
N5_PAGE = re.compile(
    r"^00\.kernel/00\.00\.10\.work/([0-9])5(\d\d)\.([a-z0-9][a-z0-9-]*)/(05\.\d\d)\.md$"
)
N7_PAGE = re.compile(
    r"^00\.kernel/00\.00\.10\.work/([0-9])7(\d\d)\.([a-z0-9][a-z0-9-]*)/(05\.\d\d)\.pack\.md$"
)
BOOK = "00.00.10.work"
IDENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
KINDS = {"N5NN", "N7NN"}
LABELS = {"synthetic", "supplied"}
STATUSES = {"complete", "reserved", "incomplete", "refused"}
ENVELOPE_KEYS = {
    "schema",
    "source_kind",
    "page",
    "pass",
    "target",
    "expect_sha256",
    "permit_create",
    "review_identity",
    "task",
    "evidence",
    "agreement",
    "receipt",
    "record",
}
TASK_KEYS = {"task_id", "assignment_path"}
EVIDENCE_KEYS = {"logical_path", "label"}
AGREEMENT_KEYS = {
    "goal",
    "scope",
    "prime_discretion",
    "director_required",
    "finish_criteria",
    "recorded_decisions",
}
RECEIPT_KEYS = {
    "placement",
    "member",
    "page_local",
    "submission_id",
    "receipt_path",
    "return_path",
    "manifest_path",
    "status",
    "label",
}
RACE = "compare-then-rename narrows a stale write and is not proof of race freedom"


class Refusal(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def need(cond: bool, message: str) -> None:
    if not cond:
        raise Refusal(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(obj) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def exact(obj, keys: set[str], where: str) -> None:
    need(isinstance(obj, dict), f"{where} must be an object")
    unknown = sorted(set(obj) - keys)
    missing = sorted(keys - set(obj))
    if unknown:
        raise Refusal(f"unknown key {unknown[0]} at {where}")
    if missing:
        raise Refusal(f"missing key {missing[0]} at {where}")


def ident(value, where: str) -> str:
    need(isinstance(value, str) and IDENT.fullmatch(value) is not None, f"bad id {where}")
    return value


def logical_path(value: str) -> str:
    need(isinstance(value, str), "unsafe path")
    need("\\" not in value and not value.startswith("/") and not value.startswith("//"), "unsafe path")
    need(re.match(r"^[A-Za-z]:", value) is None, "unsafe path")
    parts = value.split("/")
    need(parts and all(part not in ("", ".", "..") for part in parts), "unsafe path")
    need(len(value) <= 240, "unsafe path")
    return value


def is_inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def fixture_root(text: str) -> Path:
    need(isinstance(text, str) and text.strip() != "", "fixture root is empty")
    need(not text.startswith("\\\\") and not text.startswith("//"), "UNC path fixture root")
    path = Path(text)
    need(path.is_absolute(), "fixture root must be absolute")
    need(".." not in path.parts, "unsafe path fixture root")
    need(path.exists(), "fixture root is missing")
    info = path.lstat()
    need(not stat.S_ISLNK(info.st_mode), "fixture root is a symlink")
    need(stat.S_ISDIR(info.st_mode), "fixture root is not a directory")
    if is_inside(path, ROOT) or is_inside(ROOT, path):
        raise Refusal("fixture root must stay outside D:\\Git\\lib-build")
    return path


def under(root: Path, text: str, where: str) -> Path:
    need(isinstance(text, str) and text.strip() != "", f"empty path {where}")
    need(not text.startswith("\\\\") and not text.startswith("//"), f"UNC path {where}")
    path = Path(text)
    if path.is_absolute():
        need(".." not in path.parts, f"unsafe path {where}")
        resolved = path.resolve()
    else:
        logical_path(text)
        resolved = (root / Path(text)).resolve()
    need(is_inside(resolved, root.resolve()), f"path escapes fixture root {where}")
    return resolved


def read_regular(path: Path, where: str) -> bytes:
    need(path.exists(), f"missing file {where}")
    info = path.lstat()
    need(not stat.S_ISLNK(info.st_mode), f"symlink refused {where}")
    need(stat.S_ISREG(info.st_mode), f"not a regular file {where}")
    return path.read_bytes()


def load_json(data: bytes, where: str):
    if data.startswith(b"\xef\xbb\xbf"):
        raise Refusal(f"unsupported format: BOM {where}")
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refusal(f"unsupported format: not utf-8 {where}") from None

    def pairs(seq):
        out = {}
        for key, item in seq:
            need(key not in out, f"duplicate key {key} at {where}")
            out[key] = item
        return out

    try:
        return json.loads(text, object_pairs_hook=pairs)
    except json.JSONDecodeError as exc:
        raise Refusal(f"invalid JSON {where} ({exc.msg})") from None


def newline_of(data: bytes) -> bytes:
    if b"\x00" in data:
        raise Refusal("unsupported format: NUL")
    if data.startswith(b"\xef\xbb\xbf"):
        raise Refusal("unsupported format: BOM")
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refusal("unsupported format: not utf-8") from None
    bare = data.replace(b"\r\n", b"")
    if b"\r" in bare or (b"\n" in bare and b"\r" in data):
        raise Refusal("unsupported format: mixed newlines")
    if b"\r\n" in data:
        return b"\r\n"
    return b"\n"


def split_lines(data: bytes, sep: bytes) -> list[bytes]:
    pieces = data.split(sep)
    if data.endswith(sep):
        need(pieces[-1] == b"", "internal split")
        pieces = pieces[:-1]
    return pieces


def join_lines(lines: list[bytes], sep: bytes, trailing: bool) -> bytes:
    if not lines:
        return b""
    out = sep.join(lines)
    if trailing:
        out += sep
    return out


def derive_address(spec: dict) -> dict:
    kind = spec["source_kind"]
    page = spec["page"]
    pass_id = spec["pass"]
    if kind == "N5NN":
        match = N5_PAGE.fullmatch(page)
        need(match is not None, "page does not match N5NN")
        space, nn, subject, page_pass = match.groups()
        need(page_pass == pass_id, "pass does not match page")
        page_id = f"{space}5{nn}.{subject}"
        destination = f"{page_id}/{pass_id}.md"
        member = f"{space}1{nn}.{subject}"
        need(spec["target_text"] == destination, "target is not the derived review destination")
        need(spec["receipt"]["member"] == member, "member is not the derived matching line")
        return {
            "book": BOOK,
            "page": page_id,
            "pass": pass_id,
            "member": member,
            "destination": destination,
        }
    match = N7_PAGE.fullmatch(page)
    need(match is not None, "page does not match N7NN")
    space, nn, subject, page_pass = match.groups()
    need(page_pass == pass_id, "pass does not match page")
    page_id = f"{space}7{nn}.{subject}"
    tail = pass_id.split(".", 1)[1]
    destination = f"{page_id}/06.{tail}.review.md"
    need(spec["target_text"] == destination, "target is not the derived review destination")
    need(spec["receipt"]["page_local"] == f"05.{tail}.return.md", "page_local is not the N7NN return tail")
    need(spec["receipt"]["member"] is None, "N7NN must not use an N1NN member")
    return {
        "book": BOOK,
        "page": page_id,
        "pass": pass_id,
        "member": None,
        "destination": destination,
    }


def enforce_origin(spec: dict, address: dict) -> None:
    sources = spec["record"].get("sources") if isinstance(spec["record"], dict) else None
    need(isinstance(sources, list), "record sources are missing")
    if spec["source_kind"] == "N7NN":
        for item in sources:
            need(isinstance(item, dict), "record source must be an object")
            need(item.get("kind") != "capture", "N7NN must not use an N1NN capture member")
        return
    returned = None
    for item in sources:
        if isinstance(item, dict) and item.get("logical_path") == spec["receipt"]["return_path"]:
            need(returned is None, "duplicate record source")
            returned = item
    need(isinstance(returned, dict), "N5NN return source is not a capture")
    need(returned.get("kind") == "capture", "N5NN return source is not a capture")
    identity = returned.get("identity")
    need(isinstance(identity, dict), "capture identity is missing")
    need(identity.get("schema") == "return-capture/1", "capture identity schema mismatch")
    need(identity.get("member") == address["member"], "capture member is not the derived matching line")
    need(identity.get("submission_id") == spec["receipt"]["submission_id"], "receipt submission mismatch")
    origin = identity.get("origin")
    need(
        isinstance(origin, dict)
        and origin.get("book") == address["book"]
        and origin.get("page") == address["page"]
        and origin.get("batch") == address["pass"],
        "origin does not match the source",
    )


def parse_envelope(raw: dict) -> dict:
    exact(raw, ENVELOPE_KEYS, "envelope")
    need(raw["schema"] == SCHEMA, "bad schema")
    kind = raw["source_kind"]
    need(kind in KINDS, f"unsupported source kind {kind}")
    pass_id = raw["pass"]
    need(isinstance(pass_id, str) and re.fullmatch(r"05\.\d\d", pass_id) is not None, "bad pass")
    expect = raw["expect_sha256"]
    need(expect == "absent" or (isinstance(expect, str) and HEX64.fullmatch(expect) is not None), "bad expect_sha256")
    need(isinstance(raw["permit_create"], bool), "bad type permit_create")
    ident(raw["review_identity"], "review_identity")
    exact(raw["task"], TASK_KEYS, "task")
    ident(raw["task"]["task_id"], "task_id")
    logical_path(raw["task"]["assignment_path"])
    evidence = raw["evidence"]
    need(isinstance(evidence, list), "bad type evidence")
    seen = []
    for index, item in enumerate(evidence):
        exact(item, EVIDENCE_KEYS, f"evidence[{index}]")
        logical_path(item["logical_path"])
        need(item["label"] in LABELS, "bad evidence label")
        seen.append(item["logical_path"])
    need(len(seen) == len(set(seen)), "duplicate evidence path")
    exact(raw["agreement"], AGREEMENT_KEYS, "agreement")
    exact(raw["receipt"], RECEIPT_KEYS, "receipt")
    receipt = raw["receipt"]
    need(receipt["label"] in LABELS, "bad receipt label")
    need(receipt["status"] in STATUSES, "bad receipt status")
    ident(receipt["submission_id"], "submission_id")
    for key in ("receipt_path", "return_path", "manifest_path"):
        logical_path(receipt[key])
    assignment = raw["task"]["assignment_path"]
    need(assignment not in seen, "assignment path is duplicated in evidence")
    need(receipt["return_path"] not in seen, "return path is duplicated in evidence")
    need(receipt["return_path"] != assignment, "return path duplicates the assignment")
    if kind == "N5NN":
        need(receipt["placement"] == "n5nn-matching-line", "N5NN placement must be n5nn-matching-line")
        need(receipt["page_local"] is None, "N5NN page_local must be null")
    else:
        need(receipt["placement"] == "n7nn-page-local", "N7NN placement must be n7nn-page-local")
        need(receipt["member"] is None, "N7NN must not use an N1NN member")
        need(isinstance(receipt["page_local"], str), "bad page_local")
    need(isinstance(raw["record"], dict), "record must be an object")
    need(raw["page"] == raw["page"], "bad page")
    need(isinstance(raw["page"], str), "bad page")
    logical_path(raw["target"])
    spec = {
        "source_kind": kind,
        "page": raw["page"],
        "pass": pass_id,
        "target_text": raw["target"],
        "expect_sha256": expect,
        "permit_create": raw["permit_create"],
        "review_identity": raw["review_identity"],
        "task_id": raw["task"]["task_id"],
        "assignment_path": assignment,
        "evidence": evidence,
        "agreement": raw["agreement"],
        "receipt": receipt,
        "record": raw["record"],
    }
    address = derive_address(spec)
    enforce_origin(spec, address)
    spec["address"] = address
    return spec


def pin_tool() -> None:
    data = TOOL.read_bytes()
    need(len(data) == TOOL_BYTES and sha256_bytes(data) == TOOL_SHA256, "prime_review.py pin mismatch")


def measure(root: Path, spec: dict) -> dict:
    assignment = read_regular(under(root, spec["assignment_path"], "assignment"), "assignment")
    evidence_rows = []
    for item in spec["evidence"]:
        blob = read_regular(under(root, item["logical_path"], item["logical_path"]), item["logical_path"])
        evidence_rows.append({
            "bytes": len(blob),
            "label": item["label"],
            "logical_path": item["logical_path"],
            "sha256": sha256_bytes(blob),
        })
    evidence_rows.sort(key=lambda row: row["logical_path"])
    receipt_blob = read_regular(under(root, spec["receipt"]["receipt_path"], "receipt"), "receipt")
    return_blob = read_regular(under(root, spec["receipt"]["return_path"], "return"), "return")
    manifest_blob = read_regular(under(root, spec["receipt"]["manifest_path"], "manifest"), "manifest")
    agreement_sha = sha256_bytes(canonical(spec["agreement"]))
    receipt = spec["receipt"]
    address = spec["address"]
    binding = {
        "schema": "review-task-binding/2",
        "source": {
            "book": address["book"],
            "page": address["page"],
            "pass": address["pass"],
        },
        "task_id": spec["task_id"],
        "assignment_path": spec["assignment_path"],
        "assignment_sha256": sha256_bytes(assignment),
        "assignment_bytes": len(assignment),
        "evidence": evidence_rows,
        "agreement_sha256": agreement_sha,
        "receipt": {
            "placement": receipt["placement"],
            "member": receipt["member"],
            "page_local": receipt["page_local"],
            "submission_id": receipt["submission_id"],
            "status": receipt["status"],
            "label": receipt["label"],
            "receipt_sha256": sha256_bytes(receipt_blob),
            "receipt_bytes": len(receipt_blob),
            "return_sha256": sha256_bytes(return_blob),
            "return_bytes": len(return_blob),
            "manifest_sha256": sha256_bytes(manifest_blob),
            "manifest_bytes": len(manifest_blob),
        },
    }
    return {
        "assignment": assignment,
        "binding": binding,
        "binding_sha256": sha256_bytes(canonical(binding)),
        "agreement_sha256": agreement_sha,
    }


def align_record(spec: dict, measured: dict) -> None:
    record = spec["record"]
    need(record.get("agreement") == spec["agreement"], "agreement does not match the record")
    sources = record.get("sources")
    need(isinstance(sources, list), "record sources are missing")
    by_path = {}
    for source in sources:
        need(isinstance(source, dict), "record source must be an object")
        path = source.get("logical_path")
        need(isinstance(path, str), "record source path is missing")
        need(path not in by_path, "duplicate record source")
        by_path[path] = source
    declared = {spec["assignment_path"], spec["receipt"]["return_path"]}
    declared.update(item["logical_path"] for item in spec["evidence"])
    need(set(by_path) == declared, "record sources do not match the declared inputs")
    assignment = by_path[spec["assignment_path"]]
    need(assignment.get("kind") == "page", "assignment source is not a page")
    need(assignment.get("content_sha256") == measured["binding"]["assignment_sha256"], "assignment hash mismatch")
    need(assignment.get("content_bytes") == measured["binding"]["assignment_bytes"], "assignment length mismatch")
    for row in measured["binding"]["evidence"]:
        source = by_path[row["logical_path"]]
        need(source.get("content_sha256") == row["sha256"], f"evidence hash mismatch {row['logical_path']}")
        need(source.get("content_bytes") == row["bytes"], f"evidence length mismatch {row['logical_path']}")
    returned = by_path[spec["receipt"]["return_path"]]
    receipt = measured["binding"]["receipt"]
    need(returned.get("content_sha256") == receipt["return_sha256"], "return hash mismatch")
    need(returned.get("content_bytes") == receipt["return_bytes"], "return length mismatch")
    if spec["source_kind"] == "N5NN":
        need(returned.get("kind") == "capture", "N5NN return source is not a capture")
        identity = returned.get("identity")
        need(isinstance(identity, dict), "capture identity is missing")
        need(identity.get("schema") == "return-capture/1", "capture identity schema mismatch")
        need(identity.get("member") == spec["receipt"]["member"], "receipt member mismatch")
        need(identity.get("submission_id") == spec["receipt"]["submission_id"], "receipt submission mismatch")
        need(identity.get("receipt_sha256") == receipt["receipt_sha256"], "receipt hash mismatch")
    else:
        need(all(item.get("kind") != "capture" for item in sources), "N7NN must not use an N1NN capture member")


def call_prime_review(record: dict) -> tuple[dict, int, bytes]:
    pin_tool()
    payload = (json.dumps(record, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    handle = tempfile.NamedTemporaryFile(prefix="review-record-", suffix=".json", delete=False)
    path = Path(handle.name)
    try:
        handle.write(payload)
        handle.close()
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        proc = subprocess.run(
            [sys.executable, "-B", str(TOOL), "report", "--input", str(path), "--json"],
            cwd=str(ROOT),
            capture_output=True,
            env=env,
        )
    finally:
        try:
            path.unlink()
        except OSError:
            pass
    if proc.returncode not in (0, 1):
        detail = proc.stderr.decode("utf-8", errors="replace").strip()
        raise Refusal(detail or "prime_review refused the record")
    try:
        report = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Refusal("prime_review returned no report") from exc
    need(isinstance(report, dict) and isinstance(report.get("markdown"), str), "prime_review returned no report")
    return report, proc.returncode, payload


def line_of(label: str, value) -> str:
    if value is None:
        return f"{label}: none supplied"
    return f"{label}: {value}"


def block(title: str, text) -> list[str]:
    if text is None:
        return [f"{title}: none supplied", ""]
    return [f"{title}:", text, ""]


def nest_report(markdown: str) -> str:
    """Keep the report wording and move its headings below the page review section."""
    nested = []
    for line in markdown.split("\n"):
        nested.append("##" + line if line.startswith("#") else line)
    return "\n".join(nested)


def render_review(spec: dict, measured: dict, report: dict, record_sha: str) -> str:
    receipt = measured["binding"]["receipt"]
    sections = report["sections"]
    lines = [
        "authority: none",
        "closes_work: false",
        "releases_action: false",
        "authenticates_actor: false",
        f"task_binding: {measured['binding_sha256']}",
        f"record_sha256: {record_sha}",
        f"agreement_sha256: {measured['agreement_sha256']}",
        f"support: support/{spec['review_identity']}/record.json",
        "receipt_check: supplied-bytes-match",
        "custody: not-established",
        "allocated: false",
        f"placement: {receipt['placement']}",
        line_of("member", receipt["member"]),
        line_of("page_local", receipt["page_local"]),
        f"declared_status: {receipt['status']}",
        f"receipt_label: {receipt['label']}",
        f"receipt_sha256: {receipt['receipt_sha256']}",
        f"return_sha256: {receipt['return_sha256']}",
        f"manifest_sha256: {receipt['manifest_sha256']}",
        "This constructor did not allocate a member and did not establish custody.",
        "",
        "### Judgment",
        line_of("outcome", report.get("supplied_outcome")),
        line_of("effective", report.get("effective")),
        line_of("finding", report.get("finding")),
        line_of("semantic_conflict", report.get("supplied_semantic_conflict")),
        "",
        "### Reasons",
    ]
    reasons = report.get("reasons") or []
    if reasons:
        for reason in reasons:
            lines.append(f"- {reason}")
    else:
        lines.append("none supplied")
    lines.append("")
    fork = spec["record"]["judgment"]["design_fork"] if isinstance(spec["record"].get("judgment"), dict) else None
    lines.append("### Dissent")
    if not isinstance(fork, dict):
        lines.append("none supplied")
    else:
        lines.append(f"id: {fork.get('id')}")
        lines.append(fork.get("text") if isinstance(fork.get("text"), str) else "none supplied")
    lines.append("")
    lines.append("### Director replies")
    answers = report.get("answers") or []
    if not answers:
        lines.append("none supplied")
        lines.append("")
    else:
        for answer in answers:
            lines.append(f"id: {answer.get('answer_id')}")
            lines.append(f"role: {answer.get('role')}")
            lines.append(line_of("disposition", answer.get("disposition")))
            lines.append("reply:")
            lines.append(answer.get("reply") if isinstance(answer.get("reply"), str) else "")
            lines.append("")
    lines.extend(block("Next action", report.get("next_action")))
    if report.get("next_action") is not None:
        lines.insert(-1, "This line is not a release.")
    lines.append("### Agreement")
    agreement = spec["agreement"]
    for key in ("goal", "scope", "prime_discretion", "director_required"):
        lines.append(line_of(key, agreement.get(key)))
    criteria = agreement.get("finish_criteria") or []
    lines.append("finish_criteria:")
    if not criteria:
        lines.append("none supplied")
    else:
        for item in criteria:
            lines.append(f"- {item.get('id')}: {item.get('text')}")
    decisions = agreement.get("recorded_decisions") or []
    lines.append("recorded_decisions:")
    if not decisions:
        lines.append("none supplied")
    else:
        for item in decisions:
            lines.append(f"- {item.get('id')}: {item.get('text')}")
    lines.append("")
    lines.append("### Findings")
    account = sections.get("findings_account") if isinstance(sections, dict) else None
    if not account:
        lines.append("Findings account: none supplied")
    else:
        for item in account:
            lines.append(f"- {item.get('finding_id')} {item.get('status')}")
    lines.append("")
    lines.append("### Checks")
    tests_passed = sections.get("tests_passed") if isinstance(sections, dict) else None
    if tests_passed is True:
        lines.append("tests_passed: true")
    elif tests_passed is False:
        lines.append("tests_passed: false")
    else:
        lines.append("tests_passed: none supplied")
    note = sections.get("tests_note") if isinstance(sections, dict) else None
    if note is None:
        lines.append("tests_note: none supplied")
    else:
        lines.append("tests_note:")
        lines.append(note)
    lines.append("")
    lines.append("### Prime review report")
    lines.append(nest_report(report["markdown"].rstrip("\n")))
    lines.append("")
    lines.append(f"Typed record sha256: {record_sha}")
    lines.append("Fields prime_review accepted are in that record. Unknown fields are refused and are not dropped.")
    lines.append("")
    text = "\n".join(lines)
    if "\r" in text:
        raise Refusal("unsupported format: CR in rendered review")
    for line in text.split("\n"):
        if NEXT_HEADING.match(line):
            raise Refusal("unsupported format: rendered review contains a page heading")
    if not text.endswith("\n"):
        text += "\n"
    return text


def encode_body(text: str, sep: bytes) -> bytes:
    raw = text.encode("utf-8")
    if not raw.endswith(b"\n"):
        raw += b"\n"
    if sep == b"\r\n":
        raw = raw.replace(b"\n", b"\r\n")
    return raw


def locate(data: bytes, sep: bytes) -> tuple[bytes, bytes, bytes]:
    lines = split_lines(data, sep)
    ends = data.endswith(sep)
    indexes = []
    for index, line in enumerate(lines):
        try:
            text = line.decode("utf-8")
        except UnicodeDecodeError:
            raise Refusal("unsupported format: not utf-8") from None
        if text in HEADINGS:
            indexes.append(index)
    need(len(indexes) != 0, "missing review heading")
    need(len(indexes) == 1, "duplicate review heading")
    start = indexes[0] + 1
    end = len(lines)
    for index in range(start, len(lines)):
        text = lines[index].decode("utf-8")
        if NEXT_HEADING.match(text):
            end = index
            break
    prefix_trailing = bool(start) and (start < len(lines) or ends)
    prefix = join_lines(lines[:start], sep, trailing=prefix_trailing)
    current = join_lines(lines[start:end], sep, trailing=end < len(lines) or ends)
    suffix = join_lines(lines[end:], sep, trailing=ends if lines[end:] else False)
    need(prefix + current + suffix == data, "internal splice mismatch")
    return prefix, current, suffix


def exclusive_write(path: Path, payload: bytes) -> None:
    need(not os.path.lexists(path), f"temporary name {path.name} is present")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    try:
        fd = os.open(str(path), flags)
    except FileExistsError:
        raise Refusal(f"temporary name {path.name} is present") from None
    except OSError as exc:
        raise Refusal(f"cannot create {path.name}: {exc.errno}") from None
    try:
        os.write(fd, payload)
        os.fsync(fd)
    except OSError:
        raise Refusal(f"partial file retained: {path}") from None
    finally:
        os.close(fd)


def write_support(root: Path, spec: dict, measured: dict, record_bytes: bytes) -> None:
    folder = root / "support" / spec["review_identity"]
    record_path = folder / "record.json"
    binding_path = folder / "binding.json"
    binding_bytes = (json.dumps({
        "schema": "review-task-binding/2",
        "binding_sha256": measured["binding_sha256"],
        "binding": measured["binding"],
        "target_read": False,
    }, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    planned = ((record_path, record_bytes), (binding_path, binding_bytes))
    for path, payload in planned:
        if os.path.lexists(path):
            need(read_regular(path, path.name) == payload, f"support record conflicts {path.name}")
    folder.mkdir(parents=True, exist_ok=True)
    for path, payload in planned:
        if os.path.lexists(path):
            continue
        exclusive_write(path, payload)


def save_partial(root: Path, spec: dict, review_sha: str, body: bytes) -> Path:
    folder = root / "partial"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{spec['review_identity']}-{review_sha[:12]}.md"
    if path.exists():
        return path
    exclusive_write(path, body)
    return path


def install(target: Path, payload: bytes, before: bytes | None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + ".review-construct.tmp")
    exclusive_write(temporary, payload)
    if before is None:
        try:
            os.rename(temporary, target)
        except OSError:
            raise Refusal("target appeared during construction; temporary kept, target untouched") from None
        return
    current = read_regular(target, "target")
    if sha256_bytes(current) != sha256_bytes(before):
        raise Refusal("target changed during construction; temporary kept, target untouched")
    os.replace(temporary, target)


def result_object(spec, measured, report, code, record_sha, review, review_sha, before, after, name, written) -> dict:
    receipt = measured["binding"]["receipt"]
    return {
        "schema": "review-construction-result/1",
        "result": name,
        "written": written,
        "source_kind": spec["source_kind"],
        "page": spec["page"],
        "pass": spec["pass"],
        "binding_sha256": measured["binding_sha256"],
        "agreement_sha256": measured["agreement_sha256"],
        "record_sha256": record_sha,
        "review_sha256": review_sha,
        "target_sha256_before": before,
        "target_sha256_after": after,
        "prime_review_exit": code,
        "effective": report.get("effective"),
        "supplied_outcome": report.get("supplied_outcome"),
        "receipt_check": "supplied-bytes-match",
        "custody": "not-established",
        "placement": receipt["placement"],
        "member": receipt["member"],
        "allocated": False,
        "race_limitation": RACE,
        "review": review,
    }


def prepare(root: Path, spec: dict) -> tuple[dict, dict, int, bytes, str]:
    measured = measure(root, spec)
    align_record(spec, measured)
    report, code, record_bytes = call_prime_review(spec["record"])
    return measured, report, code, record_bytes, sha256_bytes(record_bytes)


def compose(root: Path, rel: str, mode: str) -> dict:
    spec = parse_envelope(load_json(read_regular(under(root, rel, "input"), "input"), "input"))
    target = under(root, spec["target_text"], "target")
    need(target != under(root, rel, "input"), "target must not be the input file")
    measured, report, code, record_bytes, record_sha = prepare(root, spec)
    review = render_review(spec, measured, report, record_sha)
    review_sha = sha256_bytes(review.encode("utf-8"))
    expect = spec["expect_sha256"]
    if expect == "absent":
        need(not os.path.lexists(target), "target exists; expected absent")
        need(spec["permit_create"] is True, "absent target requires permit_create")
        body = encode_body(review, b"\n")
        payload = (HEADING_EM + "\n").encode("utf-8") + body
        after = sha256_bytes(payload)
        if mode == "apply":
            write_support(root, spec, measured, record_bytes)
            install(target, payload, None)
        return result_object(
            spec, measured, report, code, record_sha, review, review_sha,
            None, after, "applied" if mode == "apply" else "preview", mode == "apply",
        )
    before_bytes = read_regular(target, "target")
    before = sha256_bytes(before_bytes)
    need(before == expect, f"target sha256 {before} is not the expected {expect}")
    sep = newline_of(before_bytes)
    prefix, current, suffix = locate(before_bytes, sep)
    body = encode_body(review, sep)
    if current == body:
        if mode == "apply":
            write_support(root, spec, measured, record_bytes)
        return result_object(
            spec, measured, report, code, record_sha, review, review_sha,
            before, before, "idempotent", False,
        )
    try:
        stripped = current.decode("utf-8").strip()
    except UnicodeDecodeError:
        raise Refusal("unsupported format: not utf-8") from None
    if stripped not in {"PENDING", "PENDING."}:
        if mode == "apply":
            saved = save_partial(root, spec, review_sha, body)
            raise Refusal(
                "existing review conflicts; a successor process is required and this review was not overwritten"
                f" partial evidence: {saved}"
            )
        raise Refusal(
            "existing review conflicts; a successor process is required and this review was not overwritten"
        )
    payload = prefix + body + suffix
    need(payload.startswith(prefix) and payload.endswith(suffix), "construction changed bytes outside its section")
    after = sha256_bytes(payload)
    if mode == "apply":
        write_support(root, spec, measured, record_bytes)
        install(target, payload, before_bytes)
        need(sha256_bytes(read_regular(target, "target")) == after, "target hash changed after rename")
    return result_object(
        spec, measured, report, code, record_sha, review, review_sha,
        before, after, "applied" if mode == "apply" else "preview", mode == "apply",
    )


def command_bind(root: Path, rel: str) -> dict:
    spec = parse_envelope(load_json(read_regular(under(root, rel, "input"), "input"), "input"))
    measured = measure(root, spec)
    return {
        "schema": "review-task-binding/2",
        "binding_sha256": measured["binding_sha256"],
        "binding": measured["binding"],
        "target_read": False,
    }


def command_show(root: Path, rel: str) -> dict:
    target = under(root, rel, "target")
    data = read_regular(target, "target")
    sep = newline_of(data)
    _prefix, current, _suffix = locate(data, sep)
    text = current.decode("utf-8")
    match = re.search(r"(?m)^task_binding: ([0-9a-f]{64})$", text)
    need(match is not None, "rendered review has no task binding")
    return {
        "schema": "review-construction-show/1",
        "binding_sha256": match.group(1),
        "section_sha256": sha256_bytes(current),
        "section": text,
    }


def emit(payload: dict) -> None:
    data = (json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        buffer.write(data)
    else:
        sys.stdout.write(data.decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(prog="construct.py")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("preview", "apply", "bind"):
        command = sub.add_parser(name)
        command.add_argument("--fixture-root", required=True)
        command.add_argument("--input", required=True)
    show = sub.add_parser("show")
    show.add_argument("--fixture-root", required=True)
    show.add_argument("--target", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 2
    try:
        root = fixture_root(args.fixture_root)
        if args.command == "bind":
            emit(command_bind(root, args.input))
        elif args.command == "show":
            emit(command_show(root, args.target))
        else:
            emit(compose(root, args.input, args.command))
    except Refusal as exc:
        print(f"refused: {exc.message}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
