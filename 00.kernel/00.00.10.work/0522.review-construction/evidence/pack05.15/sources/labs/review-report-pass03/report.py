#!/usr/bin/env python3
"""Read-only projection of one selected workbook review.

Successor of review-report-pass02. File counts come from accepted intake
metadata. A content hash is not a physical file. This process does not
record or publish.
"""

from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

_PASS02 = Path(__file__).resolve().parents[1] / "review-report-pass02" / "report.py"
_SPEC = importlib.util.spec_from_file_location("review_report_pass02_for_pass03", _PASS02)
p2 = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(p2)

SCHEMA = "review-report/3"
SCOPE_ADDRESSED = "addressed-source-paths"
SCOPE_CONTENT = "content-sha256"
SCOPE_PHYSICAL = "verified-physical-files"
PROVENANCE_MEASURED = "current-measured"
PROVENANCE_PHYSICAL = "not-established"
ASSUMPTION_ADDRESSED = (
    "exact root string plus exact path string; no slash folding, no case folding, "
    "and no dot-segment resolution"
)
ASSUMPTION_CONTENT = "a 64-character lowercase sha256 proves content equality only"
REASON_ADDRESSED_MEASUREMENT = "measurement is not complete, so addressed-source identity is not established"
REASON_ADDRESSED_ROWS = "intake rows are absent, so addressed-source identity is not established"
REASON_ADDRESSED_MISSING = (
    "a row lacks a root string or a path string, so the addressed-source total "
    "is not completed from the other rows"
)
REASON_ADDRESSED_SIZE = "rows of one addressed source do not agree on one int byte size"
REASON_CONTENT_MEASUREMENT = "measurement is not complete, so content-blob identity is not established"
REASON_CONTENT_ROWS = "intake rows are absent, so content-blob identity is not established"
REASON_CONTENT_MISSING = (
    "a row lacks a 64-character lowercase sha256, so the content-blob total "
    "is not completed from the other rows"
)
REASON_CONTENT_SIZE = "rows of one content hash do not agree on one int byte size"
REASON_PHYSICAL = (
    "accepted intake metadata has no physical-file identity; a path and a content hash "
    "do not establish one"
)
OBSERVATION_LIMIT = p2.OBSERVATION_LIMIT
core_call = p2.core_call
checked_record = p2.checked_record
finish = p2.finish
_artifacts_of = p2.artifacts_of
_projection_of = p2.projection_of


def _unknown(scope: str, provenance: str, reason: str, assumption: str | None) -> dict:
    item = p2.unknown_counter(scope, provenance)
    item["reason"] = reason
    if assumption is not None:
        item["assumption"] = assumption
    return item


def _measured(scope: str, provenance: str, count: int, size, bytes_state: str, assumption: str, reason: str | None) -> dict:
    item = p2.counter(scope, provenance, count, "measured", size, bytes_state)
    item["assumption"] = assumption
    if reason is not None:
        item["reason"] = reason
    return item


def _sizes(groups: dict, order: list) -> tuple[list[int], bool]:
    pieces = []
    conflict = False
    for key in order:
        values = groups[key]
        if all(type(value) is int for value in values) and len(set(values)) == 1:
            pieces.append(values[0])
        else:
            conflict = True
    return pieces, conflict


def addressed_sources(rows, measurement) -> dict:
    if measurement != "complete":
        return _unknown(SCOPE_ADDRESSED, PROVENANCE_MEASURED, REASON_ADDRESSED_MEASUREMENT, ASSUMPTION_ADDRESSED)
    if not isinstance(rows, list):
        return _unknown(SCOPE_ADDRESSED, PROVENANCE_MEASURED, REASON_ADDRESSED_ROWS, ASSUMPTION_ADDRESSED)
    groups: dict[tuple[str, str], list] = {}
    order: list[tuple[str, str]] = []
    for row in rows:
        root = row.get("root") if isinstance(row, dict) else None
        path = row.get("path") if isinstance(row, dict) else None
        if not isinstance(root, str) or not isinstance(path, str):
            return _unknown(SCOPE_ADDRESSED, PROVENANCE_MEASURED, REASON_ADDRESSED_MISSING, ASSUMPTION_ADDRESSED)
        key = (root, path)
        if key not in groups:
            order.append(key)
            groups[key] = []
        groups[key].append(row.get("bytes"))
    pieces, conflict = _sizes(groups, order)
    if conflict:
        return _measured(
            SCOPE_ADDRESSED, PROVENANCE_MEASURED, len(order), None, "unknown",
            ASSUMPTION_ADDRESSED, REASON_ADDRESSED_SIZE,
        )
    return _measured(
        SCOPE_ADDRESSED, PROVENANCE_MEASURED, len(order), sum(pieces), "measured",
        ASSUMPTION_ADDRESSED, None,
    )


def content_blobs(rows, measurement) -> dict:
    if measurement != "complete":
        return _unknown(SCOPE_CONTENT, PROVENANCE_MEASURED, REASON_CONTENT_MEASUREMENT, ASSUMPTION_CONTENT)
    if not isinstance(rows, list):
        return _unknown(SCOPE_CONTENT, PROVENANCE_MEASURED, REASON_CONTENT_ROWS, ASSUMPTION_CONTENT)
    groups: dict[str, list] = {}
    order: list[str] = []
    for row in rows:
        digest = p2.sha_key(row.get("sha256")) if isinstance(row, dict) else None
        if digest is None:
            return _unknown(SCOPE_CONTENT, PROVENANCE_MEASURED, REASON_CONTENT_MISSING, ASSUMPTION_CONTENT)
        if digest not in groups:
            order.append(digest)
            groups[digest] = []
        groups[digest].append(row.get("bytes"))
    pieces, conflict = _sizes(groups, order)
    if conflict:
        return _measured(
            SCOPE_CONTENT, PROVENANCE_MEASURED, len(order), None, "unknown",
            ASSUMPTION_CONTENT, REASON_CONTENT_SIZE,
        )
    return _measured(
        SCOPE_CONTENT, PROVENANCE_MEASURED, len(order), sum(pieces), "measured",
        ASSUMPTION_CONTENT, None,
    )


def physical_files() -> dict:
    return {
        "bytes": None,
        "bytes_state": "unknown",
        "count": None,
        "count_state": "unknown",
        "provenance": PROVENANCE_PHYSICAL,
        "reason": REASON_PHYSICAL,
        "scope": SCOPE_PHYSICAL,
    }


def artifacts_of(inspect: dict | None) -> dict:
    body = _artifacts_of(inspect)
    body.pop("unique_files", None)
    measurement = body.get("measurement") if isinstance(body.get("measurement"), str) else None
    rows = body.get("rows") if isinstance(body.get("rows"), list) else None
    body["addressed_sources"] = addressed_sources(rows, measurement)
    body["content_blobs"] = content_blobs(rows, measurement)
    body["physical_files"] = physical_files()
    return body


def _identity_line(name: str, item) -> str:
    counter = item if isinstance(item, dict) else {}
    text = p2.counter_text(
        counter.get("count"),
        counter.get("count_state", "unknown"),
        counter.get("bytes"),
        counter.get("bytes_state", "unknown"),
        counter.get("provenance", "unknown"),
    )
    scope = counter.get("scope") if isinstance(counter.get("scope"), str) else "unknown"
    line = f"{name}: {text}, scope {scope}"
    reason = counter.get("reason")
    if isinstance(reason, str) and reason != "":
        line += f", reason {reason}"
    return line


def projection_of(report: dict) -> str:
    text = _projection_of(report)
    marker = "unique_files: count unknown, bytes unknown, provenance current-measured\n"
    artifacts = report.get("artifacts") if isinstance(report.get("artifacts"), dict) else {}
    replacement = "\n".join((
        _identity_line("addressed_sources", artifacts.get("addressed_sources")),
        _identity_line("content_blobs", artifacts.get("content_blobs")),
        _identity_line("physical_files", artifacts.get("physical_files")),
    )) + "\n"
    if marker not in text:
        raise RuntimeError("unique_files projection marker missing")
    return text.replace(marker, replacement, 1)


def _sync() -> None:
    p2.core_call = core_call


def observe(options: dict) -> dict:
    _sync()
    return p2.observe(options)


def main(argv: list[str] | None = None) -> int:
    _sync()
    return p2.main(argv)


p2.SCHEMA = SCHEMA
p2.artifacts_of = artifacts_of
p2.projection_of = projection_of


if __name__ == "__main__":
    sys.exit(main())
