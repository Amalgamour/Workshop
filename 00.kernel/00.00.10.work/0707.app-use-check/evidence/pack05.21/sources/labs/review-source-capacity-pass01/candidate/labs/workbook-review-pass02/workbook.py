#!/usr/bin/env python3
"""Successor overlay for the 05.12 workbook repair.

Pass01 stays byte-for-byte. This file loads it and replaces the functions named
by the 05.12 contract: ownership, pointer and root mapping, freshness, pre-publish
checks, and scoped cycle identity.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
PASS01_REL = "labs/workbook-review-pass01/workbook.py"
PASS01_SHA = "60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a"
PASS01_BYTES = 79131
FORM_REL = "labs/workbook-review-pass02/forms/workbook-review-v1.json"
WORK_PREFIX = "00.kernel/00.00.10.work/"
FIELD_RE = __import__("re").compile(
    r"^(Submission|Artifact manifest|Verification): (\S+) sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.(.*)$"
)
SHA_RE = __import__("re").compile(r"[0-9a-f]{64}")
LABELS = ("Submission:", "Artifact manifest:", "Verification:")


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_pass01():
    path = REPO / PASS01_REL
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if len(data) != PASS01_BYTES or digest != PASS01_SHA:
        refuse_boot("pass01 workbook pin mismatch")
    spec = importlib.util.spec_from_file_location("workbook_review_pass01", path)
    if spec is None or spec.loader is None:
        refuse_boot("pass01 workbook did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


wb = load_pass01()
_original_exclusive_write = wb.exclusive_write
wb.FORM_REL = FORM_REL
wb.PINS["form"] = (FORM_REL, None, None)
wb._active_book = None
wb._allowed_target = None


def work_book() -> Path:
    return (wb.REPO / "00.kernel" / "00.00.10.work").resolve()


def writable(path: Path) -> None:
    resolved = path.resolve()
    if os.path.normcase(str(resolved)) == os.path.normcase(str(work_book())):
        return
    if wb.inside(resolved, wb.REPO) or wb.inside(wb.REPO, resolved):
        wb.refuse("book is inside the checkout; record and publish are refused")


def relative_write(path: Path, book: Path) -> str:
    if wb.is_link(path) or wb.is_link(path.parent):
        wb.refuse("write target is linked and was not followed")
    parent = path.parent.resolve()
    resolved = parent / path.name
    if not wb.inside(resolved, book.resolve()):
        wb.refuse("write is outside the named book")
    rel = os.path.relpath(os.path.abspath(resolved), os.path.abspath(book.resolve()))
    text = rel.replace("\\", "/")
    if text.startswith("../") or text == ".." or "/../" in f"/{text}/":
        wb.refuse("write is outside the named book")
    return text


def exclusive_write(path: Path, payload: bytes) -> None:
    book = wb._active_book
    if not isinstance(book, Path):
        wb.refuse("write without an owned book")
    rel = relative_write(path, book)
    allowed = wb._allowed_target
    if rel != allowed and not rel.startswith("workbook-review/"):
        wb.refuse("write is outside the derived review scope")
    _original_exclusive_write(path, payload)


def section_between(text: str, heading: str) -> str | None:
    lines = text.split("\n")
    start = None
    for index, line in enumerate(lines):
        if line.rstrip("\r") == heading:
            start = index + 1
            break
    if start is None:
        return None
    end = len(lines)
    for index in range(start, len(lines)):
        if lines[index].rstrip("\r").startswith("## "):
            end = index
            break
    body = "\n".join(line.rstrip("\r") for line in lines[start:end]).strip("\n")
    return body


def suffix_ok(rest: str) -> bool:
    if rest == "":
        return True
    if not rest.startswith(" "):
        return False
    if any(label in rest for label in LABELS):
        return False
    if SHA_RE.search(rest):
        return False
    return True


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
        match = FIELD_RE.fullmatch(line)
        if match and suffix_ok(match.group(5)):
            label = match.group(1)
            value = {"bytes": int(match.group(4)), "path": match.group(2), "sha256": match.group(3)}
            if label in ambiguous or fields[label] is not None:
                ambiguous.add(label)
                fields[label] = None
                code = {
                    "Submission": "ambiguous-submission",
                    "Artifact manifest": "ambiguous-manifest",
                    "Verification": "ambiguous-verification",
                }[label]
                findings.append({"code": code, "path": None})
                continue
            fields[label] = value
            continue
        findings.append({"code": "unparsed-return-line", "path": None, "text": line[:180]})
    parsed["submission"] = fields["Submission"]
    parsed["manifest"] = fields["Artifact manifest"]
    parsed["verification"] = fields["Verification"]
    parsed["state"] = "ambiguous" if ambiguous else "parsed"
    if parsed["submission"] is None and "Submission" not in ambiguous:
        findings.append({"code": "submission-not-declared", "path": None})
    return parsed


def locate_declared(book: Path, rel: str):
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
    if rel.startswith(WORK_PREFIX):
        consider("book", book, rel[len(WORK_PREFIX):])
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
    row = {
        "bytes": len(data),
        "declared_path": rel,
        "path": located["path"],
        "role": role,
        "root": located["root"],
        "sha256": digest,
    }
    key = (row["root"], row["role"], row["path"])
    if not any((item.get("root"), item.get("role"), item.get("path")) == key for item in rows):
        rows.append(row)
    return {
        "bytes": len(data),
        "cut": wb.cut_text(data),
        "declared_path": rel,
        "incomplete": mismatch,
        "path": located["path"],
        "root": located["root"],
        "sha256": digest,
    }


def line_field(line: str) -> dict | None:
    match = FIELD_RE.fullmatch(line.strip())
    if match is None or not suffix_ok(match.group(5)):
        return None
    if match.group(1) != "Verification":
        return None
    return {"bytes": int(match.group(4)), "path": match.group(2), "sha256": match.group(3)}


def build_intake(book: Path, source: str, pass_id: str) -> dict:
    for key in ("return_access", "prime_review", "form"):
        wb.pin_file(key)
    address = wb.address_of(source, pass_id)
    findings = []
    if address["kind"] is None:
        instance = wb.sha256_bytes(wb.canonical({"book": str(book), "pass": pass_id, "source": source}))
        return {
            "agreement": {},
            "artifact_paths": [],
            "assignment_path": None,
            "book": str(book),
            "custody": "missing",
            "cuts": [],
            "descriptor_schema": None,
            "destination": None,
            "director_text": None,
            "findings": [{"code": "route-undeclared", "path": None}],
            "goal_statement": None,
            "instance_id": instance,
            "intake_id": instance,
            "kind": None,
            "lookup_exit": None,
            "measurement": "complete",
            "member": None,
            "missing": ["route"],
            "page": source,
            "pass": pass_id,
            "receipt_sha256": None,
            "return_path": None,
            "rows": [],
            "schema": "workbook-review-intake/1",
            "submission_id": None,
            "target_kind": None,
            "unknowns": ["route"],
        }
    assignment = wb.choose_assignment(book, address, findings)
    rows = []
    page_text = ""
    agreement = {
        "director_required": None,
        "finish_criteria": None,
        "goal": None,
        "prime_discretion": None,
        "recorded_decisions": None,
        "scope": None,
    }
    goal = None
    director = None
    if assignment is not None:
        data = wb.regular_file(book / assignment, "assignment")
        rows.append({
            "bytes": len(data),
            "declared_path": assignment,
            "path": assignment,
            "role": "assignment",
            "root": "book",
            "sha256": wb.sha256_bytes(data),
        })
        page_text = data.decode("utf-8", "replace")
        agreement, goal, director = wb.measured_agreement(page_text)
    if assignment is None and address["kind"] is not None:
        pointer = {"findings": [], "manifest": None, "state": "absent", "submission": None, "verification": None}
        for rel in address["assignment_candidates"]:
            candidate = book / rel
            if not candidate.is_file() or wb.is_link(candidate):
                continue
            text = candidate.read_bytes().decode("utf-8", "replace")
            parsed = parse_pointer(wb.pointer_block(text))
            pointer["findings"].extend(parsed["findings"])
            if parsed["state"] == "ambiguous":
                pointer["state"] = "ambiguous"
    else:
        pointer = parse_pointer(wb.pointer_block(page_text) if assignment else None)
    findings.extend(pointer["findings"])
    cuts = []
    incomplete = False
    if assignment is not None:
        cuts.append({"path": assignment, "role": "assignment", "root": "book", **wb.cut_text((book / assignment).read_bytes())})
    submission = measure_declared(book, pointer.get("submission"), "submission", rows, findings)
    verification_spec = pointer.get("verification")
    if submission is not None and submission.get("incomplete"):
        incomplete = True
    if submission is not None and submission.get("root") == "book" and "cut" in submission:
        sub_file = book / submission["path"]
        sub_text = sub_file.read_bytes().decode("utf-8", "replace")
        cuts.append({"path": submission["path"], "role": "submission", "root": "book", **submission["cut"]})
        if verification_spec is None:
            for line in sub_text.split("\n"):
                found = line_field(line)
                if found is not None:
                    verification_spec = found
                    break
        if verification_spec is None and "verification" in sub_text.lower():
            findings.append({"code": "verification-not-measured", "path": submission["declared_path"]})
        if submission.get("bytes", 0) < 400 and verification_spec is None:
            findings.append({"code": "thin-submission", "path": submission["declared_path"]})
    elif isinstance(submission, dict) and "cut" in submission:
        cuts.append({"path": submission["path"], "role": "submission", "root": submission["root"], **submission["cut"]})
    measured_verification = measure_declared(book, verification_spec, "verification", rows, findings)
    if measured_verification is not None:
        if measured_verification.get("incomplete"):
            incomplete = True
        elif "cut" in measured_verification:
            cuts.append({
                "path": measured_verification["path"],
                "role": "verification",
                "root": measured_verification["root"],
                **measured_verification["cut"],
            })
    manifest = measure_declared(book, pointer.get("manifest"), "artifact-manifest", rows, findings)
    extra = []
    artifact_cuts = []
    if manifest is not None:
        if manifest.get("incomplete"):
            incomplete = True
        if "path" in manifest and "root" in manifest:
            root_path = book if manifest["root"] == "book" else wb.REPO
            entries = wb.manifest_entries((root_path / manifest["path"]).read_bytes())
            if len(entries) > wb.MAX_INDEX:
                findings.append({"code": "index-context-bounded", "count": len(entries), "path": manifest["declared_path"]})
            for item in entries:
                rel = item.get("path")
                spec = {"bytes": item.get("bytes"), "path": rel, "sha256": item.get("sha256")}
                measured = measure_declared(book, spec, "artifact", rows, findings)
                if measured is None or measured.get("incomplete"):
                    incomplete = True
                if isinstance(measured, dict) and measured.get("path"):
                    extra.append({"declared_path": rel, "path": measured["path"], "root": measured["root"]})
                    if "cut" in measured:
                        artifact_cuts.append({
                            "path": measured["path"],
                            "role": "artifact",
                            "root": measured["root"],
                            **measured["cut"],
                        })
            cuts.extend(artifact_cuts[: wb.MAX_INDEX])
    lookup = wb.lookup_custody(book, source, pass_id)
    facts = wb.descriptor_facts(lookup)
    descriptor = facts["descriptor"]
    custody = "missing"
    receipt_sha = None
    descriptor_schema = None
    submission_id = None
    return_path = address["return_path"]
    if isinstance(descriptor, dict):
        descriptor_schema = descriptor.get("schema") if isinstance(descriptor.get("schema"), str) else None
        submission_id = descriptor.get("submission_id") if isinstance(descriptor.get("submission_id"), str) else None
        described = descriptor.get("return_path") if isinstance(descriptor.get("return_path"), str) else None
        if described and described != return_path:
            findings.append({"code": "return-path-disagreement", "path": described})
            return_path = None
        elif described:
            return_path = described
        if wb.filed_ready(book, facts):
            custody = "complete-descriptor"
            receipt_sha = descriptor.get("receipt_sha256")
        else:
            custody = "not-complete"
            findings.append({"code": "custody-not-complete", "path": None})
    else:
        findings.append({"code": "custody-missing", "path": address["member"]})
        for item in facts["missing"]:
            findings.append({"code": "lookup-missing", "path": None, "text": str(item)[:180]})
    if return_path is not None:
        candidate = book / return_path
        if candidate.is_file() and not wb.is_link(candidate):
            blob = candidate.read_bytes()
            rows.append({
                "bytes": len(blob),
                "declared_path": return_path,
                "path": return_path,
                "role": "return",
                "root": "book",
                "sha256": wb.sha256_bytes(blob),
            })
            cuts.append({"path": return_path, "role": "return", "root": "book", **wb.cut_text(blob)})
        else:
            findings.append({"code": "return-missing", "path": return_path})
            if custody != "complete-descriptor":
                return_path = None
    unknowns = []
    if agreement["goal"] is None:
        unknowns.append("agreement.goal")
    if agreement["scope"] is None:
        unknowns.append("agreement.scope")
    if agreement["recorded_decisions"] is None:
        unknowns.append("recorded_decisions")
    if custody != "complete-descriptor":
        unknowns.append("receipt")
    seen_return = any(row["role"] == "return" and row["path"] == return_path for row in rows)
    instance = wb.sha256_bytes(wb.canonical({"book": str(book), "pass": pass_id, "source": source}))
    intake = {
        "agreement": agreement,
        "assignment_path": assignment,
        "book": str(book),
        "custody": custody,
        "descriptor_schema": descriptor_schema,
        "destination": address["destination"],
        "director_text": director,
        "findings": findings,
        "goal_statement": goal,
        "instance_id": instance,
        "kind": address["kind"],
        "lookup_exit": lookup.get("exit"),
        "measurement": "incomplete" if incomplete else "complete",
        "member": address["member"],
        "missing": address["missing"],
        "page": source,
        "pass": pass_id,
        "receipt_sha256": receipt_sha,
        "return_path": return_path if seen_return else None,
        "rows": rows,
        "schema": "workbook-review-intake/1",
        "submission_id": submission_id,
        "target_kind": address["target_kind"],
        "unknowns": unknowns,
    }
    intake["intake_id"] = wb.sha256_bytes(wb.canonical({key: value for key, value in intake.items() if key != "intake_id"}))
    intake["cuts"] = cuts
    intake["artifact_paths"] = extra
    return intake


def prime_record(intake: dict, judgment: dict, capture: dict | None) -> dict:
    sources = []
    bind = capture is None
    book = Path(intake["book"])
    for row in intake["rows"]:
        if row.get("root", "book") != "book":
            continue
        if capture is not None and row["role"] not in {"assignment", "artifact", "return"}:
            continue
        blob = (book / row["path"]).read_bytes()
        if row["role"] == "assignment":
            sources.append(wb.source_row(row["path"], blob, "page", {"schema": "page-bytes/1"}, bind))
        elif row["role"] == "return" and capture is not None and row["path"] == capture["return_path"]:
            sources.append(wb.source_row(row["path"], blob, "capture", capture["identity"], bind))
        elif row["role"] in {"return", "artifact", "submission", "verification"}:
            sources.append(wb.source_row(row["path"], blob, "supplied-text", {"schema": "supplied-text/1", "label": "SUPPLIED"}, bind))
    if not sources and intake["assignment_path"]:
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


def cycle_paths(intake: dict, review_id: str) -> dict:
    base = f"{wb.STORE}/{intake['page']}/{intake['pass']}/{review_id}/cycle"
    return {
        "decision": f"{base}/decision.json",
        "descriptor": f"{base}/descriptor.json",
        "registration": f"{base}/registration.json",
        "request": f"{base}/request.json",
        "review_identity": review_id,
        "review_location": f"{wb.STORE}/{intake['page']}/{intake['pass']}/cycle-records",
    }


def write_cycle_inputs(book: Path, intake: dict, review_id: str) -> dict:
    descriptor = wb.descriptor_facts(wb.lookup_custody(book, intake["page"], intake["pass"]))["descriptor"]
    if not isinstance(descriptor, dict):
        wb.refuse("descriptor disappeared before the cycle call")
    paths = cycle_paths(intake, review_id)
    exclusive_write(book / paths["descriptor"], wb.pretty(descriptor))
    evidence = []
    for row in intake["rows"]:
        if row["role"] == "artifact" and row.get("root") == "book":
            evidence.append({"label": "supplied", "logical_path": row["path"]})
    kind = intake["kind"]
    if kind == "N5NN":
        kernel = f"00.kernel/00.00.10.work/{intake['page']}/{intake['pass']}.md"
        target = intake["assignment_path"]
    else:
        kernel = f"00.kernel/00.00.10.work/{intake['page']}/{intake['pass']}.pack.md"
        target = intake["destination"]
    if not isinstance(intake["goal_statement"], str) or intake["goal_statement"].strip() == "":
        wb.refuse("goal statement was not measured")
    if not isinstance(intake["submission_id"], str) or wb.IDENT.fullmatch(intake["submission_id"]) is None:
        wb.refuse("submission id is not a cycle label")
    registration = {
        "agreement": intake["agreement"],
        "assignment_path": intake["assignment_path"],
        "book": wb.BOOK_NAME,
        "bounds": {"max_output_bytes": 2097152},
        "descriptor_path": paths["descriptor"],
        "evidence": evidence,
        "goal": {
            "evidence": [],
            "goal_id": "g1",
            "statement": intake["goal_statement"],
            "terminal": "open",
        },
        "kernel_page": kernel,
        "page_id": intake["page"],
        "pass": intake["pass"],
        "receipt_label": "supplied",
        "review_identity": paths["review_identity"],
        "review_location": paths["review_location"],
        "schema": "prime-cycle-registration/2",
        "source_kind": kind,
        "submission_id": intake["submission_id"],
        "target": target,
        "task_id": "task-" + intake["pass"].replace(".", ""),
        "work_id": intake["page"],
    }
    if registration["assignment_path"] is None or registration["target"] is None:
        wb.refuse("assignment path was not measured")
    exclusive_write(book / paths["registration"], wb.pretty(registration))
    exclusive_write(book / paths["request"], wb.pretty({
        "registration_path": paths["registration"],
        "schema": "review-loop-request/1",
    }))
    return paths


def attempt_cycle(book: Path, intake: dict, judgment: dict, review_id: str) -> dict:
    wb.pin_file("review_loop")
    wb.pin_file("construct")
    wb.pin_file("prime_cycle")
    try:
        paths = write_cycle_inputs(book, intake, review_id)
    except wb.Refusal as exc:
        return {"called": False, "committed": False, "error": exc.message}
    loop = wb.pin_file("review_loop")
    code, view, err = wb.call_json(loop, ["prepare", "--fixture-root", str(book), "--request", paths["request"]])
    template = None
    if isinstance(view, dict):
        inner = view.get("view") if isinstance(view.get("view"), dict) else view
        if isinstance(inner, dict):
            template = inner.get("template")
    if code != 0 or not isinstance(template, dict):
        detail = err.strip() or (view.get("rule") if isinstance(view, dict) else None) or "cycle prepare did not return a template"
        return {"called": True, "committed": False, "error": str(detail)[:600], "prepare_exit": code, "request": paths["request"]}
    statement = intake["goal_statement"].encode("utf-8")
    cycle_judgment = {
        "answers": judgment["answers"],
        "design_fork": judgment["design_fork"],
        "disposition": judgment["disposition"],
        "finding": judgment["finding"],
        "goal": {
            "evidence": [intake["assignment_path"]] if judgment["operation"] == "complete" else [],
            "goal_id": "g1",
            "goal_sha256": wb.sha256_bytes(statement),
            "terminal": judgment["goal_terminal"],
        },
        "holds": judgment["holds"],
        "next_action": {"action_id": "next", "authorized_in_grant": None, "text": judgment["next_action"]},
        "outcome": judgment["operation"],
        "pass_terminal": judgment["pass_terminal"],
        "reasons": judgment["reasons"],
        "sections": judgment["sections"],
        "semantic_conflict": judgment["semantic_conflict"],
        "source_refs": [intake["assignment_path"]] if intake["assignment_path"] else [],
        "unresolved": list(judgment["gaps"]),
    }
    capture = wb.capture_identity(book, intake) if intake["kind"] == "N5NN" else None
    supplied = prime_record(intake, judgment, capture)
    decision = dict(template)
    cycle_review_id = f"{intake['pass']}-{review_id}"
    decision["review_id"] = cycle_review_id
    decision["attribution"] = supplied["attribution"]
    decision["judgment"] = cycle_judgment
    decision["supplied_record"] = supplied
    exclusive_write(book / paths["decision"], wb.pretty(decision))
    record_code, record_view, record_err = wb.call_json(
        loop,
        ["record", "--fixture-root", str(book), "--request", paths["request"], "--decision", paths["decision"]],
    )
    committed = isinstance(record_view, dict) and record_code in {0, 1}
    inner_result = None
    if isinstance(record_view, dict):
        nested = record_view.get("record") if isinstance(record_view.get("record"), dict) else record_view
        inner_result = nested.get("result") if isinstance(nested, dict) else None
    if inner_result not in {"recorded", "already-recorded"}:
        committed = False
    return {
        "called": True,
        "committed": committed,
        "cycle_record": f"{paths['review_location']}/{cycle_review_id}/record.json",
        "cycle_review_id": cycle_review_id,
        "error": None if committed else (record_err.strip() or str(inner_result) or "cycle record was not committed")[:600],
        "record_exit": record_code,
        "request": paths["request"],
        "result": inner_result,
        "review_id": review_id,
        "review_identity": review_id,
    }


def row_map(intake: dict | None) -> dict:
    if not isinstance(intake, dict):
        return {}
    found = {}
    for row in intake.get("rows") or []:
        if not isinstance(row, dict):
            continue
        key = (row.get("root", "book"), row.get("role"), row.get("path"))
        found[key] = row.get("sha256")
    return found


def own_write_matches(book: Path, journal: dict) -> str | None:
    if not isinstance(journal, dict):
        return None
    candidates = []
    publication = journal.get("publication")
    if isinstance(publication, dict):
        candidates.append(publication)
    attested = journal.get("published_target")
    if isinstance(attested, dict):
        candidates.append(attested)
    for item in candidates:
        if item.get("status") != "published":
            continue
        target = item.get("target")
        after = item.get("after_sha256")
        if not isinstance(target, str) or not isinstance(after, str):
            continue
        path = book / target
        if not path.is_file() or wb.is_link(path):
            continue
        if wb.sha256_bytes(path.read_bytes()) == after:
            return target
    return None


def source_changed(book: Path, stored: dict | None, live: dict, journal: dict) -> bool:
    if not isinstance(stored, dict):
        return False
    old = row_map(stored)
    new = row_map(live)
    if old == new:
        return False
    target = own_write_matches(book, journal)
    if target is None:
        return True
    def drop(mapping: dict) -> dict:
        return {key: value for key, value in mapping.items() if not (key[1] == "assignment" and key[2] == target)}
    return drop(old) != drop(new)


def journal_of(book: Path, intake: dict) -> dict:
    if not wb.journal_path(book, intake).is_file():
        return {"current": None, "reviews": []}
    return wb.load_journal(book, intake)


def do_prepare(book: Path, source: str, pass_id: str) -> dict:
    document = wb.load_form()
    intake = build_intake(book, source, pass_id)
    stored = wb.read_stored_intake(book, intake)
    journal = journal_of(book, intake)
    stale = source_changed(book, stored, intake, journal)
    exit_code = 2 if "route" in intake.get("missing", []) else 0
    return wb.result(
        "prepare",
        intake,
        exit_code,
        custody=intake["custody"],
        cuts=intake["cuts"],
        destination=intake["destination"],
        director_text=intake["director_text"],
        findings=intake["findings"],
        form=wb.form_view(intake, document),
        live_intake_id=intake["intake_id"],
        measurement=intake["measurement"],
        missing=list(intake.get("missing") or []),
        stale=stale,
        stored_intake_id=None if not isinstance(stored, dict) else stored.get("intake_id"),
        unknowns=intake["unknowns"],
    )


def rendering_holds(book: Path, intake: dict, review_id: str, record: dict, journal: dict) -> str | None:
    path = wb.record_path(book, intake, review_id)
    data = path.read_bytes()
    rows = journal.get("reviews") if isinstance(journal.get("reviews"), list) else []
    expected = None
    for item in rows:
        if isinstance(item, dict) and item.get("review_id") == review_id:
            expected = item.get("record_sha256")
    if not isinstance(expected, str) or wb.sha256_bytes(data) != expected:
        return "stored record does not match the journal"
    rendered_path = path.parent / "rendered.md"
    if not rendered_path.is_file():
        return "rendered text does not match the durable judgment"
    disk = rendered_path.read_text(encoding="utf-8")
    derived = wb.render_body(record)
    if disk != record.get("rendered") or disk != derived:
        return "rendered text does not match the durable judgment"
    return None


def do_record(book: Path, source: str, pass_id: str, intake_id: str, judgment_path: Path, successor: str | None) -> dict:
    writable(book)
    document = wb.load_form()
    intake = build_intake(book, source, pass_id)
    if intake["kind"] is None:
        return wb.result("record", intake, 2, correction="missing route", missing=["route"], recorded=False)
    raw = wb.regular_file(judgment_path, "judgment")
    try:
        judgment = wb.parse_judgment(raw, document)
    except wb.Refusal as exc:
        failed = wb.save_failed(book, intake, raw, exc.message)
        return wb.result("record", intake, 2, correction=exc.message, failed_input=failed, judgment=None, recorded=False)
    if intake.get("measurement") == "incomplete":
        failed = wb.save_failed(book, intake, raw, "artifact measurement is incomplete")
        return wb.result(
            "record",
            intake,
            2,
            correction="The artifact measurement is incomplete. The judgment was not recorded.",
            failed_input=failed,
            recorded=False,
        )
    stored = wb.read_stored_intake(book, intake)
    journal = journal_of(book, intake)
    if isinstance(stored, dict) and source_changed(book, stored, intake, journal):
        failed = wb.save_failed(book, intake, raw, "stored intake differs from the live measurement")
        return wb.result(
            "record",
            intake,
            2,
            correction="The stored intake was kept. This entry does not repin.",
            failed_input=failed,
            recorded=False,
            stale=True,
            stored_intake_id=stored.get("intake_id"),
        )
    expected_id = stored.get("intake_id") if isinstance(stored, dict) else intake["intake_id"]
    if intake_id != expected_id:
        failed = wb.save_failed(book, intake, raw, "intake id does not match the stored measurement")
        return wb.result(
            "record",
            intake,
            2,
            correction="The stored intake was kept. This entry does not repin." if isinstance(stored, dict) else "Prepare again and copy the intake id. The live bytes were not stored over an old intake.",
            failed_input=failed,
            recorded=False,
            stale=True,
        )
    if not isinstance(stored, dict):
        exclusive_write(
            wb.store_root(book, intake) / "intake.json",
            wb.pretty({key: value for key, value in intake.items() if key not in {"cuts", "artifact_paths"}}),
        )
    review_id = wb.review_id_for(expected_id, judgment)
    journal = wb.load_journal(book, intake) if wb.journal_path(book, intake).is_file() else journal
    existing = wb.record_path(book, intake, review_id)
    if existing.is_file():
        prior = wb.load_record(book, intake, review_id)
        if wb.canonical(prior.get("judgment")) == wb.canonical(judgment):
            return wb.result(
                "record",
                intake,
                0,
                already_recorded=True,
                judgment=prior["judgment"],
                mode=prior.get("mode"),
                next_action=judgment["next_action"],
                recorded=True,
                review_id=review_id,
            )
        failed = wb.save_failed(book, intake, raw, "a different body is already stored for this review id")
        return wb.result("record", intake, 2, correction="The stored review was kept.", failed_input=failed, recorded=False, review_id=review_id)
    current = journal.get("current")
    if isinstance(current, str) and successor != current:
        failed = wb.save_failed(book, intake, raw, "a current review exists")
        return wb.result(
            "record",
            intake,
            2,
            correction="Pass --successor with the current review id. The current record was kept.",
            current=current,
            failed_input=failed,
            recorded=False,
        )
    if successor is not None and current is None:
        failed = wb.save_failed(book, intake, raw, "no review to succeed")
        return wb.result("record", intake, 2, correction="Record the first review without --successor.", failed_input=failed, recorded=False)
    cycle = {"called": False, "committed": False, "error": None}
    if intake["custody"] == "complete-descriptor":
        cycle = attempt_cycle(book, intake, judgment, review_id)
    if judgment["operation"] == "complete" and not cycle.get("committed"):
        failed = wb.save_failed(book, intake, raw, "completion is ineligible until the cycle records the review")
        return wb.result(
            "record",
            intake,
            2,
            correction="operation complete was not recorded. Missing custody or a cycle refusal stays ineligible for completion.",
            cycle=cycle,
            failed_input=failed,
            recorded=False,
        )
    mode = "cycle-committed" if cycle.get("committed") else "preliminary"
    custody = "measured" if cycle.get("committed") else "missing"
    if intake["custody"] == "complete-descriptor" and not cycle.get("committed"):
        custody = "present-not-committed"
    attention = []
    effective = None
    prime_exit = None
    if not cycle.get("committed"):
        code, report, err = wb.call_prime(book, prime_record(intake, judgment, None))
        prime_exit = code
        if code == 2 or not isinstance(report, dict):
            failed = wb.save_failed(book, intake, raw, err.strip() or "prime_review refused the record")
            return wb.result("record", intake, 2, correction=err.strip() or "prime_review refused the record", failed_input=failed, recorded=False)
        effective = report.get("effective")
        attention = report.get("attention") if isinstance(report.get("attention"), list) else []
    account = judgment["sections"].get("findings_account")
    if judgment["findings"] and account is None:
        attention.append("findings_account is unknown")
    if isinstance(account, list):
        accounted = set()
        for item in account:
            if isinstance(item, dict) and isinstance(item.get("finding_id"), str):
                accounted.add(item["finding_id"])
        for item in judgment["findings"]:
            if item["finding_id"] not in accounted:
                failed = wb.save_failed(book, intake, raw, "finding not accounted")
                return wb.result("record", intake, 2, correction="A supplied finding is missing from findings_account. It was not dropped.", failed_input=failed, recorded=False)
    record = {
        "attention": attention,
        "custody": custody,
        "cycle": cycle,
        "cycle_error": cycle.get("error"),
        "director_text": intake["director_text"],
        "eligible_for_custody_completion": bool(cycle.get("committed") and judgment["operation"] == "complete"),
        "holds": judgment["holds"],
        "intake_id": expected_id,
        "judgment": judgment,
        "mode": mode,
        "next_action": judgment["next_action"],
        "prime_review_effective": effective,
        "prime_review_exit": prime_exit,
        "review_id": review_id,
        "schema": "workbook-review-record/1",
        "successor_of": successor,
    }
    record["rendered"] = wb.render_body(record)
    folder = wb.record_path(book, intake, review_id).parent
    exclusive_write(folder / "judgment.json", wb.pretty(judgment))
    exclusive_write(folder / "record.json", wb.pretty(record))
    exclusive_write(folder / "rendered.md", record["rendered"].encode("utf-8"))
    published_target = journal.get("published_target")
    journal.setdefault("reviews", []).append({
        "judgment_sha256": wb.sha256_bytes(wb.canonical(judgment)),
        "record_sha256": wb.sha256_bytes(wb.pretty(record)),
        "review_id": review_id,
    })
    journal["current"] = review_id
    journal["publication"] = {"review_id": review_id, "status": "recorded"}
    if isinstance(published_target, dict):
        journal["published_target"] = published_target
    journal["schema"] = "workbook-review-journal/1"
    wb.save_journal(book, intake, journal)
    return wb.result(
        "record",
        intake,
        0,
        attention=attention,
        custody=custody,
        director_text=intake["director_text"],
        eligible_for_custody_completion=record["eligible_for_custody_completion"],
        holds=judgment["holds"],
        cycle=cycle,
        judgment=judgment,
        mode=mode,
        next_action=judgment["next_action"],
        recorded=True,
        review_id=review_id,
    )


def freshness(book: Path, intake: dict) -> tuple[bool, dict | None, str | None]:
    journal = journal_of(book, intake)
    review_id = journal.get("current") if isinstance(journal.get("current"), str) else None
    checked = None
    if isinstance(review_id, str) and wb.record_path(book, intake, review_id).is_file():
        checked = wb.revalidate(book, intake, review_id)
    stored = wb.read_stored_intake(book, intake)
    stale = source_changed(book, stored, intake, journal) or bool(checked and checked.get("stale"))
    return stale, checked, review_id


def do_inspect(book: Path, source: str, pass_id: str) -> dict:
    intake = build_intake(book, source, pass_id)
    document = wb.load_form()
    journal = journal_of(book, intake)
    current = journal.get("current") if isinstance(journal.get("current"), str) else None
    record = None
    if current and wb.record_path(book, intake, current).is_file():
        record = wb.load_record(book, intake, current)
    stale, _checked, _review = freshness(book, intake)
    return wb.result(
        "inspect",
        intake,
        0,
        current=current,
        destination=intake["destination"],
        director_text=intake["director_text"],
        findings=intake["findings"],
        form=wb.form_view(intake, document),
        holds=record.get("holds") if isinstance(record, dict) else [],
        judgment=record.get("judgment") if isinstance(record, dict) else None,
        measurement=intake["measurement"],
        mode=record.get("mode") if isinstance(record, dict) else None,
        next_action=record.get("next_action") if isinstance(record, dict) else None,
        publication=journal.get("publication"),
        rendered=record.get("rendered") if isinstance(record, dict) else None,
        stale=stale,
        unknowns=intake["unknowns"],
    )


def do_publish(book: Path, source: str, pass_id: str, review_id: str) -> dict:
    writable(book)
    intake = build_intake(book, source, pass_id)
    if intake["kind"] is None:
        return wb.result("publish", intake, 2, correction="missing route", missing=["route"], published=False)
    stored = wb.read_stored_intake(book, intake)
    if not isinstance(stored, dict):
        return wb.result("publish", intake, 2, correction="No judgment is recorded.", published=False)
    journal = journal_of(book, intake)
    if source_changed(book, stored, intake, journal):
        record = wb.load_record(book, intake, review_id) if wb.record_path(book, intake, review_id).is_file() else None
        return wb.result(
            "publish",
            intake,
            1,
            correction="Publication is blocked because the selected source changed after intake.",
            judgment=None if record is None else record.get("judgment"),
            next_action=None if record is None else record.get("next_action"),
            published=False,
            review_id=review_id,
            stale=True,
        )
    if not wb.record_path(book, intake, review_id).is_file():
        return wb.result("publish", intake, 2, correction="That review id is not recorded.", published=False)
    if journal.get("current") != review_id:
        record = wb.load_record(book, intake, review_id)
        return wb.result(
            "publish",
            intake,
            1,
            correction="Publish names the latest review. An older review was not selected.",
            judgment=record.get("judgment"),
            next_action=record.get("next_action"),
            published=False,
            review_id=review_id,
        )
    record = wb.load_record(book, intake, review_id)
    mismatch = rendering_holds(book, intake, review_id, record, journal)
    if mismatch:
        return wb.result(
            "publish",
            intake,
            1,
            correction=mismatch,
            holds=record.get("holds"),
            judgment=record.get("judgment"),
            next_action=record.get("next_action"),
            published=False,
            review_id=review_id,
        )
    rendered = record.get("rendered")
    if not isinstance(rendered, str):
        return wb.result("publish", intake, 1, correction="rendered text does not match the durable judgment", judgment=record.get("judgment"), next_action=record.get("next_action"), published=False, review_id=review_id)
    if record.get("mode") == "cycle-committed":
        loop = wb.pin_file("review_loop")
        request = record.get("cycle", {}).get("request") if isinstance(record.get("cycle"), dict) else None
        if not isinstance(request, str):
            return wb.result("publish", intake, 1, correction="cycle request was not stored", judgment=record["judgment"], next_action=record["next_action"], published=False, review_id=review_id)
        target = book / intake["destination"]
        before = target.read_bytes() if target.is_file() else b""
        try:
            prefix, current, suffix, _sep = wb.locate_review(before)
        except wb.Refusal:
            prefix, current, suffix = b"", before, b""
        if current and not wb.vacant(current) and b"workbook-review-id:" not in current and b"task_binding:" not in current and b"authority: none" not in current:
            return wb.result("publish", intake, 1, correction="Existing manual review text was kept.", judgment=record["judgment"], next_action=record["next_action"], published=False, review_id=review_id)
        code, view, err = wb.call_json(loop, ["render", "--fixture-root", str(book), "--request", request])
        after = target.read_bytes() if target.is_file() else b""
        render = view.get("render") if isinstance(view, dict) and isinstance(view.get("render"), dict) else {}
        render_result = render.get("result")
        blocked = None
        if render_result not in {"rendered", "already-rendered"}:
            blocked = str(render.get("rule") or err.strip() or "cycle render did not publish the review")[:600]
        elif after == before and render_result != "already-rendered":
            blocked = "cycle render did not change the target"
        elif code not in {0, 1}:
            blocked = err.strip() or "cycle render refused"
        else:
            try:
                new_prefix, _new_current, new_suffix, _sep = wb.locate_review(after)
                if new_prefix != prefix or new_suffix != suffix:
                    blocked = "unauthorized-diff"
            except wb.Refusal as exc:
                blocked = exc.message
        if blocked:
            return wb.result("publish", intake, 1, correction=blocked, judgment=record["judgment"], next_action=record["next_action"], published=False, review_id=review_id)
        fresh = wb.load_journal(book, intake)
        publication = {
            "after_sha256": wb.sha256_bytes(after),
            "before_sha256": wb.sha256_bytes(before),
            "review_id": review_id,
            "status": "published",
            "target": intake["destination"],
        }
        fresh["publication"] = publication
        fresh["published_target"] = publication
        wb.save_journal(book, intake, fresh)
        return wb.result("publish", intake, 0, judgment=record["judgment"], next_action=record["next_action"], published=True, review_id=review_id, target=intake["destination"])
    try:
        outcome = wb.publish_target(book, intake, rendered, review_id)
    except wb.Refusal as exc:
        fresh = wb.load_journal(book, intake)
        status = fresh.get("publication", {}).get("status") if isinstance(fresh.get("publication"), dict) else None
        return wb.result(
            "publish",
            intake,
            1,
            correction=exc.message,
            holds=record["holds"],
            judgment=record["judgment"],
            next_action=record["next_action"],
            publication_status=status,
            published=False,
            review_id=review_id,
        )
    if outcome.get("blocked"):
        return wb.result("publish", intake, 1, correction=outcome["blocked"], holds=record["holds"], judgment=record["judgment"], next_action=record["next_action"], published=False, review_id=review_id)
    fresh = wb.load_journal(book, intake)
    after = outcome.get("after") or b""
    publication = {
        "after_sha256": wb.sha256_bytes(after),
        "before_sha256": None if outcome.get("before") is None else wb.sha256_bytes(outcome["before"]),
        "rendered_sha256": wb.sha256_bytes(rendered.encode("utf-8")),
        "review_id": review_id,
        "status": "published",
        "target": outcome.get("target"),
    }
    fresh["publication"] = publication
    fresh["published_target"] = publication
    wb.save_journal(book, intake, fresh)
    return wb.result("publish", intake, 0, judgment=record["judgment"], next_action=record["next_action"], published=True, review_id=review_id, target=outcome.get("target"))


def do_read(book: Path, source: str, pass_id: str, command: str) -> dict:
    writable(book)
    intake = build_intake(book, source, pass_id)
    if intake["kind"] is None:
        return wb.result(command, intake, 2, correction="missing route", judgment=None, missing=["route"])
    _stale, checked, review_id = freshness(book, intake)
    if not isinstance(review_id, str) or not wb.record_path(book, intake, review_id).is_file() or not isinstance(checked, dict):
        return wb.result(command, intake, 2, correction="No recorded judgment.", judgment=None)
    stale = _stale
    payload = dict(checked)
    payload["stale"] = stale
    exit_code = 0 if not stale else 1
    return wb.result(command, intake, exit_code, **payload)


def perform(args: list[str]) -> int:
    command, values = wb.parse_call(args)
    book = wb.book_dir(values["--book"])
    source = values["--source"]
    pass_id = values["--pass"]
    wb._active_book = book
    wb._allowed_target = None
    address = wb.address_of(source, pass_id)
    if address.get("kind"):
        wb._allowed_target = address.get("destination")
    if command == "prepare":
        payload = do_prepare(book, source, pass_id)
    elif command == "form":
        prepared = do_prepare(book, source, pass_id)
        payload = wb.result(
            "form",
            {"instance_id": prepared["instance_id"], "intake_id": prepared["intake_id"], "kind": prepared["kind"], "page": prepared["page"], "pass": prepared["pass"]},
            int(prepared["exit"]),
            form=prepared["form"],
            missing=["route"] if prepared["exit"] == 2 else [],
        )
    elif command == "inspect":
        payload = do_inspect(book, source, pass_id)
    elif command == "record":
        judgment = Path(values["--judgment"])
        if not judgment.is_absolute():
            wb.refuse("judgment path must be absolute")
        payload = do_record(book, source, pass_id, values["--intake"], judgment, values.get("--successor"))
    elif command == "publish":
        payload = do_publish(book, source, pass_id, values["--review"])
    else:
        payload = do_read(book, source, pass_id, command)
    wb.emit(payload)
    return int(payload["exit"])


wb.writable = writable
wb.exclusive_write = exclusive_write
wb.section_between = section_between
wb.parse_pointer = parse_pointer
wb.measure_declared = measure_declared
wb.build_intake = build_intake
wb.prime_record = prime_record
wb.cycle_paths = cycle_paths
wb.write_cycle_inputs = write_cycle_inputs
wb.attempt_cycle = attempt_cycle
wb.do_prepare = do_prepare
wb.do_record = do_record
wb.do_inspect = do_inspect
wb.do_publish = do_publish
wb.do_read = do_read
wb.perform = perform


def main(argv: list[str] | None = None) -> int:
    return wb.main(argv)


if __name__ == "__main__":
    sys.exit(main())
