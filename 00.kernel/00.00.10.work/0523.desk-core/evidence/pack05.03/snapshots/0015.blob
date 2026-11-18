"""Deterministic face rendering and column-0 section splice.

User prose is indented, so a supplied line cannot open or close a section.
Only the review body, or another named section body, is replaced.
"""

from __future__ import annotations

from .identity import Refused

RELEASE = "## Release"
CLAIM = "## Claim"
POINTER = "## Return pointer"
REVIEW = "## Review - Codex Prime"
NOTE = "## Record note"

N5_HEADINGS = (RELEASE, CLAIM, POINTER, REVIEW, NOTE)
N7_HEADINGS = (RELEASE, CLAIM, POINTER, NOTE)

RECORD_NOTE = (
    "Constructed by desk-core/2. A receipt, a passing check, and a review are different.\n"
    "None of them is Director approval, seating, migration completion, or permission to launch a model.\n"
    "TAIL-SENTINEL\n"
)


def _indent(text: str, empty: str = "(none)") -> str:
    if text == "":
        return f"    {empty}\n"
    lines = text.split("\n")
    if lines and lines[-1] == "":
        lines = lines[:-1]
    return "".join(f"    {line}\n" for line in lines)


def _bullets(items: list[str], empty: str = "(none)") -> str:
    if not items:
        return empty + "\n"
    return "".join(f"- {item}\n" for item in items)


def _normalize(body: str) -> bytes:
    if body == "":
        body = "\n"
    if not body.endswith("\n"):
        body += "\n"
    if not body.endswith("\n\n"):
        body += "\n"
    return body.encode("utf-8")


def render_prefix(task: dict[str, object]) -> bytes:
    evidence = task["bound_evidence"]
    if not isinstance(evidence, list):
        raise Refused("evidence", "bound evidence is not a list")
    scope = task["scope"]
    if not isinstance(scope, dict):
        raise Refused("scope", "scope is not an object")
    outputs = task["expected_outputs"]
    if not isinstance(outputs, list):
        raise Refused("outputs", "expected outputs are not a list")
    lines = [
        f"# {task['title']}",
        "",
        "schema: desk-core-face/1",
        f"page: {task['page']}.{task['subject']}",
        f"pass: {task['pass']}",
        f"kind: {task['kind']}",
        "synthetic: true",
        f"task-binding: {task['task_binding_sha256']}",
        "note: constructed face; not acceptance and not a release",
        "",
        "## Assignment",
        _indent(str(task["body"])).rstrip("\n"),
        "",
        "## Expected outputs",
        _bullets([str(item) for item in outputs]).rstrip("\n"),
        "",
        "## Scope",
        "in:",
        _bullets([str(item) for item in scope["in"]]).rstrip("\n"),
        "out:",
        _bullets([str(item) for item in scope["out"]]).rstrip("\n"),
        "",
        "## Agreement",
        _indent(str(task["agreement"])).rstrip("\n"),
        "",
        "## Bound evidence",
    ]
    if evidence == []:
        lines.append("(none)")
    else:
        for row in evidence:
            if not isinstance(row, dict):
                raise Refused("evidence", "evidence row is not an object")
            lines.append(f"- {row['name']} {row['sha256']} {row['bytes']}")
    return ("\n".join(lines) + "\n\n").encode("utf-8")


def release_body(record: dict[str, object] | None) -> str:
    if record is None:
        return "PENDING.\n"
    return (
        f"who: {record['who']}\n"
        f"date: {record['date']}\n"
        "fabricated: false\n"
        "text:\n"
        f"{_indent(str(record['text']))}"
    )


def claim_body(record: dict[str, object] | None) -> str:
    if record is None:
        return "PENDING.\n"
    return (
        f"worker: {record['worker']}\n"
        f"date: {record['date']}\n"
        f"task-binding: {record['task_binding_sha256']}\n"
        "not-authentication: true\n"
        "text:\n"
        f"{_indent(str(record['text']))}"
    )


def pointer_body(record: dict[str, object] | None) -> str:
    if record is None:
        return "PENDING.\n"
    return (
        f"placement: {record['placement']}\n"
        f"custody: {record['custody']}\n"
        f"return-file: {record['return_file']}\n"
        f"receipt-sha256: {record['receipt_sha256']}\n"
        f"return-sha256: {record['return_sha256']}\n"
        "note: a pointer is not a review and not acceptance\n"
    )


def review_body(record: dict[str, object] | None) -> str:
    if record is None:
        return "PENDING.\n"
    questions = record["unresolved_questions"]
    findings = record["findings"]
    if not isinstance(questions, list) or not isinstance(findings, list):
        raise Refused("review", "review lists are not lists")
    action = record["next_action"]
    if not isinstance(action, dict):
        raise Refused("review", "next action is not an object")
    return (
        f"reviewer: {record['reviewer']}\n"
        f"review-identity: {record['review_identity']}\n"
        f"disposition: {record['disposition']}\n"
        f"review-binding: {record['review_binding_sha256']}\n"
        f"task-binding: {record['bound_task_binding_sha256']}\n"
        f"receipt-sha256: {record['bound_receipt_sha256']}\n"
        f"agreement-sha256: {record['bound_agreement_sha256']}\n"
        f"evidence-sha256: {record['bound_evidence_sha256']}\n"
        "stale: no\n"
        "findings:\n"
        f"{_bullets([str(item) for item in findings])}"
        "dissent:\n"
        f"{_indent(str(record['dissent']))}"
        "director-text:\n"
        f"{_indent(str(record['director_text']))}"
        "unresolved-questions:\n"
        f"{_bullets([str(item) for item in questions])}"
        "assessment:\n"
        f"{_indent(str(record['assessment']))}"
        "next-action:\n"
        f"actor: {action['actor']}\n"
        "action:\n"
        f"{_indent(str(action['action']))}"
        "note: this review is a supplied judgment. It is not Director approval, seating, migration completion, or permission to launch a model.\n"
    )


def render_face(task: dict[str, object], kind: str) -> bytes:
    parts = [
        render_prefix(task),
        _section(RELEASE, release_body(None)),
        _section(CLAIM, claim_body(None)),
        _section(POINTER, pointer_body(None)),
    ]
    if kind == "N5NN":
        parts.append(_section(REVIEW, review_body(None)))
    elif kind != "N7NN":
        raise Refused("placement", "face kind is undeclared")
    parts.append(_section(NOTE, RECORD_NOTE))
    return b"".join(parts)


def render_colab_review(record: dict[str, object]) -> bytes:
    body = review_body(record)
    return (
        f"# Review {record['review_identity']}\n\n"
        "schema: desk-core-face/1\n"
        "home: page-local 06 review tail\n"
        "not-acceptance: true\n\n"
        f"{body}"
    ).encode("utf-8")


def _section(heading: str, body: str) -> bytes:
    return heading.encode("utf-8") + b"\n" + _normalize(body)


def line_spans(data: bytes) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    while start <= len(data):
        end = data.find(b"\n", start)
        if end < 0:
            if start < len(data) or not spans:
                spans.append((start, len(data)))
            break
        spans.append((start, end))
        start = end + 1
        if start == len(data):
            break
    return spans


def section_span(data: bytes, heading: str) -> tuple[int, int]:
    token = heading.encode("utf-8")
    found: list[int] = []
    spans = line_spans(data)
    for index, (start, end) in enumerate(spans):
        if data[start:end] == token:
            found.append(index)
    if len(found) != 1:
        raise Refused("face", f"expected one {heading}", found=len(found))
    heading_index = found[0]
    _start, end = spans[heading_index]
    body_start = end + 1 if end < len(data) else end
    body_end = len(data)
    for start, _line_end in spans[heading_index + 1 :]:
        line = data[start : _line_end]
        if line.startswith(b"## "):
            body_end = start
            break
    return body_start, body_end


def section_body(data: bytes, heading: str) -> bytes:
    start, end = section_span(data, heading)
    return data[start:end]


def replace_body(data: bytes, heading: str, body: str) -> bytes:
    start, end = section_span(data, heading)
    return data[:start] + _normalize(body) + data[end:]


def split_before_release(data: bytes) -> tuple[bytes, bytes]:
    prefix_end, _body_end = section_span(data, RELEASE)
    # prefix includes the Release heading line; assignment bytes stop at the heading.
    heading_at = data.rfind(b"## Release\n", 0, prefix_end)
    if heading_at < 0:
        raise Refused("face", "Release heading is missing")
    return data[:heading_at], data[heading_at:]
