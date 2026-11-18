#!/usr/bin/env python3
"""Successor overlay for the 05.13 return-intake repair.

Pass02 stays byte-for-byte. This file loads it and replaces pointer parsing,
declared-path resolution, and validator source identity. Freshness, ownership,
and cycle paths stay on the pass02 functions.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
PASS02_REL = "labs/workbook-review-pass02/workbook.py"
PASS02_SHA = "6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a"
PASS02_BYTES = 52574
FORM_REL = "labs/workbook-review-pass03/forms/workbook-review-v1.json"
FIELD_RE = re.compile(
    r"^(Submission|Artifact manifest|Verification): (\S+) sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.(.*)$"
)
COUNT_RE = re.compile(
    r"^(Artifact manifest): (\S+) sha256 ([0-9a-f]{64}), ([0-9]+) bytes, ([0-9]+) files\.(.*)$"
)
COUNT_TAILS = {"", " Excludes itself.", " Excludes itself and this page."}
VER_RE = re.compile(r"^Verification: `([^`]+)`$")
SCHEMA_RE = re.compile(r"^Schema: `([^`]+)`$")
HASH_RE = re.compile(r"^sha256: `([0-9a-f]{64})`$")
BYTES_RE = re.compile(r"^bytes: ([0-9]+)$")
LABEL_CODE = {
    "Submission": "ambiguous-submission",
    "Artifact manifest": "ambiguous-manifest",
    "Verification": "ambiguous-verification",
}
EMIT_ROLES = {"return", "artifact", "submission", "verification"}
LIMIT = "The lines are a declaration, not a successful verification run."


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_pass02():
    path = REPO / PASS02_REL
    data = path.read_bytes()
    if len(data) != PASS02_BYTES or hashlib.sha256(data).hexdigest() != PASS02_SHA:
        refuse_boot("pass02 workbook pin mismatch")
    spec = importlib.util.spec_from_file_location("workbook_review_pass02", path)
    if spec is None or spec.loader is None:
        refuse_boot("pass02 workbook did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p2 = load_pass02()
wb = p2.wb
_original_build = p2.build_intake


def accept_field(fields: dict, ambiguous: set, findings: list, label: str, value: dict) -> None:
    if label in ambiguous or fields[label] is not None:
        ambiguous.add(label)
        fields[label] = None
        findings.append({"code": LABEL_CODE[label], "path": None})
        return
    fields[label] = value


def parse_pointer(body: str | None) -> dict:
    findings = []
    parsed = {
        "findings": findings,
        "manifest": None,
        "state": "absent",
        "submission": None,
        "verification": None,
    }
    if body is None:
        findings.append({"code": "return-pointer-absent", "path": None})
        return parsed
    stripped = body.strip()
    if stripped == "":
        findings.append({"code": "return-pointer-empty", "path": None})
        parsed["state"] = "empty"
        return parsed
    if stripped == "PENDING.":
        findings.append({"code": "return-pending", "path": None})
        parsed["state"] = "pending"
        return parsed
    fields = {"Submission": None, "Artifact manifest": None, "Verification": None}
    ambiguous = set()
    for raw_line in body.split("\n"):
        line = raw_line.strip()
        if line == "" or line.startswith("Invocation/claim:"):
            continue
        counted = COUNT_RE.fullmatch(line)
        if counted and counted.group(6) in COUNT_TAILS:
            accept_field(fields, ambiguous, findings, counted.group(1), {
                "bytes": int(counted.group(4)),
                "file_count": int(counted.group(5)),
                "path": counted.group(2),
                "sha256": counted.group(3),
            })
            continue
        match = FIELD_RE.fullmatch(line)
        if match and p2.suffix_ok(match.group(5)):
            accept_field(fields, ambiguous, findings, match.group(1), {
                "bytes": int(match.group(4)),
                "path": match.group(2),
                "sha256": match.group(3),
            })
            continue
        findings.append({"code": "unparsed-return-line", "path": None, "text": line[:180]})
    parsed["submission"] = fields["Submission"]
    parsed["manifest"] = fields["Artifact manifest"]
    parsed["verification"] = fields["Verification"]
    parsed["state"] = "ambiguous" if ambiguous else "parsed"
    if parsed["submission"] is None and "Submission" not in ambiguous:
        findings.append({"code": "submission-not-declared", "path": None})
    return parsed


def locate_declared(book: Path, rel: str, page: str | None = None):
    page_id = page if isinstance(page, str) else getattr(p2, "_resolve_page", None)
    found = []
    seen = {}

    def consider(root_name: str, root: Path, rel_path: str) -> None:
        path = root / rel_path
        if wb.is_link(path) or not path.is_file():
            return
        try:
            resolved = path.resolve()
        except OSError:
            return
        if not wb.inside(resolved, root.resolve()):
            return
        key = os.path.normcase(os.path.abspath(resolved))
        item = {"file": path, "path": rel_path, "root": root_name}
        previous = seen.get(key)
        if previous is not None:
            if previous["root"] == "book" or root_name != "book":
                return
            found.remove(previous)
        seen[key] = item
        found.append(item)

    consider("book", book, rel)
    if rel.startswith(p2.WORK_PREFIX):
        consider("book", book, rel[len(p2.WORK_PREFIX):])
    if isinstance(page_id, str) and page_id != "":
        prefix = page_id + "/"
        if not rel.startswith(prefix) and not rel.startswith(p2.WORK_PREFIX):
            consider("book", book, prefix + rel)
    consider("code", wb.REPO, rel)
    if len(found) > 1:
        return None, "ambiguous"
    if len(found) == 1:
        return found[0], "one"
    return None, "missing"


def measure_declared(book: Path, spec: dict | None, role: str, rows: list, findings: list) -> dict | None:
    if not isinstance(spec, dict):
        return None
    rel = spec.get("path")
    if not isinstance(rel, str):
        findings.append({"code": "malformed-declared-path", "path": None})
        return {"incomplete": True}
    try:
        wb.logical(rel, role)
    except wb.Refusal:
        findings.append({"code": "malformed-declared-path", "path": None})
        return {"incomplete": True}
    located, how = locate_declared(book, rel)
    if how == "ambiguous":
        findings.append({"code": "ambiguous-declared-root", "path": rel})
        return {"incomplete": True}
    if how == "missing":
        code = "artifact-missing" if role == "artifact" else "declared-file-missing"
        findings.append({"code": code, "path": rel})
        return {"incomplete": True}
    data = located["file"].read_bytes()
    digest = wb.sha256_bytes(data)
    mismatch = digest != spec.get("sha256") or len(data) != spec.get("bytes")
    if mismatch:
        code = "artifact-hash-mismatch" if role == "artifact" else "declared-hash-mismatch"
        findings.append({
            "code": code,
            "measured_bytes": len(data),
            "measured_sha256": digest,
            "path": rel,
        })
    declared_sha = spec.get("sha256") if isinstance(spec.get("sha256"), str) else None
    declared_bytes = spec.get("bytes") if isinstance(spec.get("bytes"), int) else None
    row = {
        "bytes": len(data),
        "declared_bytes": declared_bytes,
        "declared_path": rel,
        "declared_sha256": declared_sha,
        "path": located["path"],
        "role": role,
        "root": located["root"],
        "sha256": digest,
    }
    key = (row["root"], row["role"], row["path"])
    existing = next(
        (item for item in rows if (item.get("root"), item.get("role"), item.get("path")) == key),
        None,
    )
    conflict = False
    if existing is not None:
        if existing.get("declared_sha256") != declared_sha or existing.get("declared_bytes") != declared_bytes:
            findings.append({"code": "source-identity-conflict", "path": rel})
            conflict = True
    else:
        rows.append(row)
    incomplete = mismatch or conflict
    if role == "artifact-manifest" and isinstance(spec.get("file_count"), int):
        counted = len(wb.manifest_entries(data))
        if counted != spec["file_count"]:
            findings.append({
                "code": "manifest-count-mismatch",
                "declared_count": spec["file_count"],
                "measured_count": counted,
                "path": rel,
            })
            incomplete = True
    return {
        "bytes": len(data),
        "cut": wb.cut_text(data),
        "declared_path": rel,
        "incomplete": incomplete,
        "path": located["path"],
        "root": located["root"],
        "sha256": digest,
    }


def resolved_key(base: Path, rel: str) -> str:
    path = base / rel
    try:
        resolved = path.resolve()
    except OSError:
        resolved = path
    return os.path.normcase(os.path.abspath(resolved))


def thin_blocks(text: str) -> tuple[list[dict], bool]:
    raw = text.split("\n")
    found = []
    malformed = False
    index = 0
    while index < len(raw):
        line = raw[index].strip()
        ver = VER_RE.fullmatch(line)
        if ver is None:
            index += 1
            continue
        block = [line]
        nxt = index + 1
        while nxt < len(raw) and len(block) < 4:
            piece = raw[nxt].strip()
            if piece == "":
                break
            block.append(piece)
            nxt += 1
        if len(block) == 4:
            schema = SCHEMA_RE.fullmatch(block[1])
            digest = HASH_RE.fullmatch(block[2])
            size = BYTES_RE.fullmatch(block[3])
            if schema and digest and size and schema.group(1) != "":
                found.append({
                    "bytes": int(size.group(1)),
                    "path": ver.group(1),
                    "schema_name": schema.group(1),
                    "sha256": digest.group(1),
                })
                index = nxt
                continue
        malformed = True
        index += 1
    return found, malformed


def bind_declared_verification(book: Path, intake: dict) -> None:
    findings = intake.get("findings")
    rows = intake.get("rows")
    if not isinstance(findings, list) or not isinstance(rows, list):
        return
    if not any(isinstance(item, dict) and item.get("code") == "verification-not-measured" for item in findings):
        return
    sub = next((row for row in rows if row.get("role") == "submission"), None)
    if not isinstance(sub, dict) or not isinstance(sub.get("path"), str):
        return
    base = book if sub.get("root", "book") == "book" else wb.REPO
    blob = (base / sub["path"]).read_bytes()
    try:
        text = blob.decode("utf-8")
    except UnicodeDecodeError:
        return
    blocks, malformed = thin_blocks(text)
    if len(blocks) > 1:
        findings.append({"code": "ambiguous-verification", "path": None})
        intake["measurement"] = "incomplete"
        return
    if len(blocks) != 1:
        if malformed:
            findings.append({"code": "verification-declaration-malformed", "path": sub.get("declared_path")})
            intake["measurement"] = "incomplete"
        return
    spec = {"bytes": blocks[0]["bytes"], "path": blocks[0]["path"], "sha256": blocks[0]["sha256"]}
    try:
        wb.logical(spec["path"], "verification")
    except wb.Refusal:
        findings.append({"code": "verification-declaration-malformed", "path": sub.get("declared_path")})
        intake["measurement"] = "incomplete"
        return
    measured = measure_declared(book, spec, "verification", rows, findings)
    measured_ok = isinstance(measured, dict) and isinstance(measured.get("sha256"), str)
    if measured_ok:
        intake["findings"] = [
            item for item in intake["findings"]
            if not (isinstance(item, dict) and item.get("code") == "verification-not-measured")
        ]
        findings = intake["findings"]
    sources = ["submission-lines"]
    if measured_ok:
        ver_base = book if measured.get("root") == "book" else wb.REPO
        ver_key = resolved_key(ver_base, measured["path"])
        for row in rows:
            if row.get("role") != "artifact" or not isinstance(row.get("path"), str):
                continue
            row_base = book if row.get("root", "book") == "book" else wb.REPO
            if resolved_key(row_base, row["path"]) == ver_key:
                sources.append("artifact-index")
                break
    findings.append({
        "code": "verification-declared",
        "hash_match": bool(measured_ok and not measured.get("incomplete")),
        "limit": LIMIT,
        "measured": measured_ok,
        "path": spec["path"],
        "schema": blocks[0]["schema_name"],
        "sources": sources,
        "successful_run": False,
    })
    if not isinstance(measured, dict) or measured.get("incomplete"):
        intake["measurement"] = "incomplete"
    cuts = intake.get("cuts")
    if measured_ok and isinstance(cuts, list) and "cut" in measured:
        if not any(isinstance(item, dict) and item.get("role") == "verification" and item.get("path") == measured.get("path") for item in cuts):
            cuts.append({
                "path": measured["path"],
                "role": "verification",
                "root": measured["root"],
                **measured["cut"],
            })


def mark_conflicts(book: Path, intake: dict) -> None:
    rows = intake.get("rows")
    findings = intake.get("findings")
    if not isinstance(rows, list) or not isinstance(findings, list):
        return
    groups = {}
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            continue
        root = row.get("root", "book")
        base = book if root == "book" else wb.REPO
        groups.setdefault((root, resolved_key(base, row["path"])), []).append(row)
    for grouped in groups.values():
        if len(grouped) < 2:
            continue
        measured_sha = {row.get("sha256") for row in grouped}
        measured_size = {row.get("bytes") for row in grouped}
        declared_sha = [row.get("declared_sha256") for row in grouped if isinstance(row.get("declared_sha256"), str)]
        declared_size = [row.get("declared_bytes") for row in grouped if isinstance(row.get("declared_bytes"), int)]
        if len(measured_sha) > 1 or len(measured_size) > 1 or len(set(declared_sha)) > 1 or len(set(declared_size)) > 1:
            findings.append({"code": "source-identity-conflict", "path": grouped[0].get("path")})
            intake["measurement"] = "incomplete"


def rehash(intake: dict) -> None:
    body = {key: value for key, value in intake.items() if key not in {"intake_id", "cuts", "artifact_paths"}}
    intake["intake_id"] = wb.sha256_bytes(wb.canonical(body))


def build_intake(book: Path, source: str, pass_id: str) -> dict:
    previous = getattr(p2, "_resolve_page", None)
    p2._resolve_page = source
    try:
        intake = _original_build(book, source, pass_id)
        bind_declared_verification(book, intake)
        mark_conflicts(book, intake)
        rehash(intake)
        return intake
    finally:
        p2._resolve_page = previous


def source_rank(row: dict, capture: dict | None) -> int:
    role = row.get("role")
    if role == "assignment":
        return 0
    if role == "return" and capture is not None and row.get("path") == capture.get("return_path"):
        return 1
    if role == "return":
        return 2
    if role == "submission":
        return 3
    if role == "verification":
        return 4
    if role == "artifact":
        return 5
    return 6


def contradictory(rows: list[dict]) -> bool:
    measured_sha = {row.get("sha256") for row in rows}
    measured_size = {row.get("bytes") for row in rows}
    declared_sha = [row.get("declared_sha256") for row in rows if isinstance(row.get("declared_sha256"), str)]
    declared_size = [row.get("declared_bytes") for row in rows if isinstance(row.get("declared_bytes"), int)]
    return len(measured_sha) > 1 or len(measured_size) > 1 or len(set(declared_sha)) > 1 or len(set(declared_size)) > 1


def prime_record(intake: dict, judgment: dict, capture: dict | None) -> dict:
    sources = []
    bind = capture is None
    book = Path(intake["book"])
    selected = []
    for row in intake["rows"]:
        if row.get("root", "book") != "book":
            continue
        if capture is not None and row["role"] not in {"assignment", "artifact", "return"}:
            continue
        selected.append(row)
    groups = {}
    for row in selected:
        groups.setdefault(resolved_key(book, row["path"]), []).append(row)
    for grouped in groups.values():
        if contradictory(grouped):
            wb.refuse("source identity conflict")
        winner = sorted(grouped, key=lambda item: (source_rank(item, capture), item.get("path") or ""))[0]
        blob = (book / winner["path"]).read_bytes()
        if winner["role"] == "assignment":
            sources.append(wb.source_row(winner["path"], blob, "page", {"schema": "page-bytes/1"}, bind))
        elif winner["role"] == "return" and capture is not None and winner["path"] == capture["return_path"]:
            sources.append(wb.source_row(winner["path"], blob, "capture", capture["identity"], bind))
        elif winner["role"] in EMIT_ROLES:
            sources.append(wb.source_row(
                winner["path"], blob, "supplied-text", {"schema": "supplied-text/1", "label": "SUPPLIED"}, bind,
            ))
    if not sources and intake.get("assignment_path"):
        blob = (book / intake["assignment_path"]).read_bytes()
        sources.append(wb.source_row(intake["assignment_path"], blob, "page", {"schema": "page-bytes/1"}, bind))
    return {
        "agreement": intake["agreement"],
        "answers": judgment["answers"],
        "attribution": {
            "actor_label": "Codex Prime (supplied)",
            "evidence": "The actor label is not authentication.",
            "role": "prime",
        },
        "gaps": judgment["gaps"],
        "holds": judgment["holds"],
        "judgment": {
            "design_fork": judgment["design_fork"],
            "finding": judgment["finding"],
            "next_action": judgment["next_action"],
            "outcome": judgment["operation"],
            "reasons": judgment["reasons"],
            "sections": judgment["sections"],
            "semantic_conflict": judgment["semantic_conflict"],
        },
        "review_passes": judgment["review_passes"],
        "schema": "prime-review-record/1",
        "sources": sources,
    }


p2._resolve_page = None
p2.parse_pointer = parse_pointer
p2.locate_declared = locate_declared
p2.measure_declared = measure_declared
p2.build_intake = build_intake
p2.prime_record = prime_record
wb.parse_pointer = parse_pointer
wb.locate_declared = locate_declared
wb.measure_declared = measure_declared
wb.build_intake = build_intake
wb.prime_record = prime_record
wb.FORM_REL = FORM_REL
wb.PINS["form"] = (FORM_REL, None, None)


def main(argv: list[str] | None = None) -> int:
    return wb.main(argv)


if __name__ == "__main__":
    sys.exit(main())
