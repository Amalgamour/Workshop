#!/usr/bin/env python3
"""Draft Prime review reports and check declared holds.

Standard library only. Intelligence supplies the outcome and the words.
This module checks shape, source bindings, and declared holds.
It does not decide that an explanation is good or that a design conflicts.
It does not release work, close work, or prove who wrote a record.

  python -B prime_review.py report --input ABS [--root ABS] [--json]
  python -B prime_review.py guard --input ABS [--root ABS] [--json]
  python -B prime_review.py check-next --input ABS [--root ABS] [--json]
  python -B prime_review.py draft --input ABS --dest ABS --repo ABS --expect-sha256 HEX [--root ABS]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path

SCHEMA_RECORD = "prime-review-record/1"
SCHEMA_GUARD = "prime-review-guard/1"
SCHEMA_REPORT = "prime-review-report/1"
SCHEMA_GUARD_RESULT = "prime-review-guard-result/1"
MAX_DOC = 262144
MAX_LIST = 24
MAX_TEXT = 12000
REPARSE = 0x400
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
FINDING = re.compile(r"^[A-Za-z0-9][^#\r\n]{0,180}#[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
REV = re.compile(r"^[A-Za-z0-9._-]{1,64}$")
MEMBER = re.compile(r"^01[0-9]{2}\.[a-z0-9][a-z0-9.-]*$")
ROLES = {"prime", "director", "builder", "model", "unknown"}
OUTCOMES = {"continue", "director-input", "develop", "complete"}
LABELS = {"SYNTHETIC", "SUPPLIED", "DERIVED-FROM-RETAINED-SUMMARY"}
HOLD_KINDS = {"director-judgment", "design-conflict", "design-fork"}
BLOCKING = {
    "unresolved",
    "reconciliation-required",
    "stale",
    "ambiguous",
    "open-new-detail",
    "model-blocked",
}
RECORD_KEYS = {
    "schema",
    "attribution",
    "sources",
    "agreement",
    "judgment",
    "holds",
    "answers",
    "review_passes",
    "gaps",
}
SOURCE_KEYS = {
    "kind",
    "logical_path",
    "content_sha256",
    "content_bytes",
    "transport_sha256",
    "transport_bytes",
    "prior_content_sha256",
    "prior_transport_sha256",
    "record",
    "bind",
    "identity",
}
SECTION_KEYS = {
    "return_result",
    "prime_finding",
    "within_direction",
    "next_bounded_action",
    "for_model",
    "issue",
    "consequences",
    "options",
    "recommendation",
    "question",
    "affected",
    "proposed_plan",
    "exploration",
    "assumptions",
    "open_questions",
    "outcome_evidence",
    "limits",
    "tests_note",
    "tests_passed",
    "learning",
    "preservation",
    "remaining_choices",
    "findings_account",
    "finish_assessments",
}


class Refusal(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message


def need(cond: bool, message: str) -> None:
    if not cond:
        raise Refusal(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_reparse(info: os.stat_result) -> bool:
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def strict_json(data: bytes, label: str):
    if data.startswith(b"\xef\xbb\xbf"):
        raise Refusal(f"{label}: BOM")
    if len(data) > MAX_DOC:
        raise Refusal(f"{label}: input exceeds {MAX_DOC} bytes")

    def pairs(seq):
        out = {}
        for key, item in seq:
            need(key not in out, f"{label}: duplicate key {key}")
            out[key] = item
        return out

    def constant(name):
        raise Refusal(f"{label}: nonfinite number {name}")

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except UnicodeDecodeError:
        raise Refusal(f"{label}: not UTF-8") from None
    except json.JSONDecodeError as exc:
        raise Refusal(f"{label}: invalid JSON ({exc.msg})") from None


def exact(obj, keys: set[str], where: str) -> None:
    need(isinstance(obj, dict), f"{where} must be an object")
    unknown = sorted(set(obj) - keys)
    missing = sorted(keys - set(obj))
    if unknown:
        raise Refusal(f"unknown key {unknown[0]} at {where}")
    if missing:
        raise Refusal(f"missing key {missing[0]} at {where}")


def hex64(value, where: str) -> str:
    need(isinstance(value, str) and HEX64.fullmatch(value) is not None, f"bad hash {where}")
    return value


def hex64_or_null(value, where: str):
    if value is None:
        return None
    return hex64(value, where)


def ident(value, where: str) -> str:
    need(isinstance(value, str) and ID.fullmatch(value) is not None, f"bad id {where}")
    return value


def ident_or_null(value, where: str):
    if value is None:
        return None
    return ident(value, where)


def prose(value, where: str) -> str:
    need(isinstance(value, str) and value.strip() != "", f"empty text {where}")
    need(len(value) <= MAX_TEXT, f"text limit {where}")
    return value


def prose_or_null(value, where: str):
    if value is None:
        return None
    return prose(value, where)


def count(value, where: str) -> int:
    need(isinstance(value, int) and not isinstance(value, bool), f"bad type {where}")
    need(0 <= value <= MAX_DOC, f"limit {where}")
    return value


def as_list(value, where: str):
    need(isinstance(value, list), f"bad type {where}")
    need(len(value) <= MAX_LIST, f"limit {where}")
    return value


def logical_path(value: str) -> str:
    need(isinstance(value, str), "unsafe path")
    need("\\" not in value and not value.startswith("/") and not value.startswith("//"), "unsafe path")
    need(re.match(r"^[A-Za-z]:", value) is None, "unsafe path")
    parts = value.split("/")
    need(parts and all(part not in ("", ".", "..") for part in parts), "unsafe path")
    need(len(value) <= 240, "unsafe path")
    return value


def absolute_local(text: str, where: str) -> Path:
    need(isinstance(text, str), f"bad type {where}")
    need(not text.startswith("\\\\") and not text.startswith("//"), f"UNC path {where}")
    path = Path(text)
    need(path.is_absolute(), f"path must be absolute {where}")
    need(".." not in path.parts, f"unsafe path {where}")
    return path


def unique(ids: list[str], where: str) -> None:
    need(len(ids) == len(set(ids)), f"duplicate id at {where}")


def lstat_kind(path: Path):
    try:
        return path.lstat()
    except OSError as exc:
        raise Refusal(f"cannot stat {path.name}: {exc.errno}") from None


def refuse_link(info: os.stat_result, where: str) -> None:
    need(not is_reparse(info), f"symlink or junction {where}")


def read_regular(path: Path, where: str) -> bytes:
    info = lstat_kind(path)
    refuse_link(info, where)
    need(stat.S_ISREG(info.st_mode), f"not a regular file {where}")
    need(info.st_nlink == 1, f"hard link {where}")
    need(info.st_size <= MAX_DOC, f"{where}: input exceeds {MAX_DOC} bytes")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise Refusal(f"cannot read {where}: {exc.errno}") from None


def require_directory(path: Path, where: str) -> None:
    info = lstat_kind(path)
    refuse_link(info, where)
    need(stat.S_ISDIR(info.st_mode), f"not a directory {where}")


def inside(child: Path, parent: Path) -> bool:
    child_s = os.path.normcase(os.path.abspath(child))
    parent_s = os.path.normcase(os.path.abspath(parent))
    if child_s == parent_s:
        return True
    prefix = parent_s if parent_s.endswith(os.sep) else parent_s + os.sep
    return child_s.startswith(prefix)


def attribution(obj, where: str) -> dict:
    exact(obj, {"actor_label", "role", "evidence"}, where)
    role = obj["role"]
    need(role in ROLES, f"bad role {where}")
    return {
        "actor_label": prose(obj["actor_label"], f"{where}.actor_label"),
        "role": role,
        "evidence": prose(obj["evidence"], f"{where}.evidence"),
    }


def change_of(content: str, transport: str, prior_content, prior_transport) -> str:
    if prior_content is None and prior_transport is None:
        return "unspecified"
    need(
        isinstance(prior_content, str) and isinstance(prior_transport, str),
        "partial change binding",
    )
    prior_content = hex64(prior_content, "prior_content_sha256")
    prior_transport = hex64(prior_transport, "prior_transport_sha256")
    if prior_content != content:
        return "substantive"
    if prior_transport != transport:
        return "transport"
    return "unchanged"


def check_identity(kind: str, identity, content: str) -> dict:
    need(isinstance(identity, dict), "identity must be an object")
    if kind == "page":
        exact(identity, {"schema"}, "identity")
        need(identity["schema"] == "page-bytes/1", "bad identity schema")
        return {"schema": "page-bytes/1"}
    if kind == "return-revision":
        exact(identity, {"schema", "revision_id", "bytes_are_revision", "finding_ids"}, "identity")
        need(identity["schema"] == "prime-support-return/1", "bad identity schema")
        revision_id = hex64(identity["revision_id"], "revision_id")
        flag = identity["bytes_are_revision"]
        need(isinstance(flag, bool), "bad type identity.bytes_are_revision")
        if flag:
            need(revision_id == content, "revision_id does not match content")
        findings = as_list(identity["finding_ids"], "finding_ids")
        checked = [prose(item, "finding_id") for item in findings]
        for item in checked:
            need(FINDING.fullmatch(item) is not None, f"bad finding {item}")
        unique(checked, "finding_ids")
        return {
            "schema": "prime-support-return/1",
            "revision_id": revision_id,
            "bytes_are_revision": flag,
            "finding_ids": checked,
        }
    if kind == "capture":
        exact(identity, {"schema", "member", "submission_id", "receipt_sha256", "origin"}, "identity")
        need(identity["schema"] == "return-capture/1", "bad identity schema")
        member = identity["member"]
        need(isinstance(member, str) and MEMBER.fullmatch(member) is not None, "bad member")
        submission = ident(identity["submission_id"], "submission_id")
        origin = identity["origin"]
        exact(origin, {"book", "page", "batch"}, "origin")
        return {
            "schema": "return-capture/1",
            "member": member,
            "submission_id": submission,
            "receipt_sha256": hex64_or_null(identity["receipt_sha256"], "receipt_sha256"),
            "origin": {
                "book": ident(origin["book"], "origin.book"),
                "page": ident(origin["page"], "origin.page"),
                "batch": ident(origin["batch"], "origin.batch"),
            },
        }
    if kind == "observation":
        exact(identity, {"schema", "batch_id", "source_sha256", "label"}, "identity")
        need(identity["schema"] == "batch-observation/1", "bad identity schema")
        source_sha = hex64(identity["source_sha256"], "source_sha256")
        need(source_sha == content, "observation source_sha256 does not match content")
        label = identity["label"]
        need(label in LABELS, "bad observation label")
        return {
            "schema": "batch-observation/1",
            "batch_id": ident(identity["batch_id"], "batch_id"),
            "source_sha256": source_sha,
            "label": label,
        }
    if kind == "brief":
        exact(identity, {"schema", "brief_sha256"}, "identity")
        need(identity["schema"] == "prime-brief-input/1", "bad identity schema")
        brief = hex64(identity["brief_sha256"], "brief_sha256")
        need(brief == content, "brief_sha256 does not match content")
        return {"schema": "prime-brief-input/1", "brief_sha256": brief}
    if kind == "supplied-text":
        exact(identity, {"schema", "label"}, "identity")
        need(identity["schema"] == "supplied-text/1", "bad identity schema")
        label = identity["label"]
        need(label in LABELS, "bad supplied-text label")
        return {"schema": "supplied-text/1", "label": label}
    raise Refusal("bad source kind")


def bind_file(root: Path, source: dict) -> None:
    parts = source["logical_path"].split("/")
    current = root
    refuse_link(lstat_kind(current), "root")
    for part in parts[:-1]:
        current = current / part
        info = lstat_kind(current)
        refuse_link(info, part)
        need(stat.S_ISDIR(info.st_mode), f"not a directory {part}")
    candidate = current / parts[-1]
    need(inside(candidate, root), "path escapes root")
    data = read_regular(candidate, source["logical_path"])
    need(len(data) == source["transport_bytes"], "bound file length mismatch")
    need(sha256_bytes(data) == source["transport_sha256"], "bound file hash mismatch")


def parse_source(raw, index: int, root: Path | None) -> dict:
    where = f"sources[{index}]"
    exact(raw, SOURCE_KEYS, where)
    kind = raw["kind"]
    need(
        kind in {"page", "return-revision", "capture", "observation", "brief", "supplied-text"},
        "bad source kind",
    )
    content = hex64(raw["content_sha256"], f"{where}.content_sha256")
    transport = hex64(raw["transport_sha256"], f"{where}.transport_sha256")
    content_bytes = count(raw["content_bytes"], f"{where}.content_bytes")
    transport_bytes = count(raw["transport_bytes"], f"{where}.transport_bytes")
    if content == transport:
        need(content_bytes == transport_bytes, "transport length does not match content")
    record = raw["record"]
    if record is not None:
        need(isinstance(record, str), f"bad type {where}.record")
        need(len(record) <= MAX_TEXT, f"text limit {where}.record")
        encoded = record.encode("utf-8")
        need(len(encoded) == content_bytes, "record length does not match content_bytes")
        need(sha256_bytes(encoded) == content, "record hash does not match content_sha256")
    bind = raw["bind"]
    need(isinstance(bind, bool), f"bad type {where}.bind")
    change = change_of(content, transport, raw["prior_content_sha256"], raw["prior_transport_sha256"])
    if raw["prior_content_sha256"] is None and raw["prior_transport_sha256"] is None:
        prior_content = None
        prior_transport = None
    else:
        prior_content = hex64(raw["prior_content_sha256"], f"{where}.prior_content_sha256")
        prior_transport = hex64(raw["prior_transport_sha256"], f"{where}.prior_transport_sha256")
    source = {
        "kind": kind,
        "logical_path": logical_path(raw["logical_path"]),
        "content_sha256": content,
        "content_bytes": content_bytes,
        "transport_sha256": transport,
        "transport_bytes": transport_bytes,
        "prior_content_sha256": prior_content,
        "prior_transport_sha256": prior_transport,
        "change": change,
        "record": record,
        "bind": bind,
        "identity": check_identity(kind, raw["identity"], content),
    }
    if bind:
        need(root is not None, "bind requires --root")
        bind_file(root, source)
    return source


def criterion(raw, index: int) -> dict:
    exact(raw, {"id", "text"}, f"finish_criteria[{index}]")
    return {"id": ident(raw["id"], "finish_criteria.id"), "text": prose(raw["text"], "finish_criteria.text")}


def decision(raw, index: int) -> dict:
    exact(raw, {"id", "text", "source_sha256"}, f"recorded_decisions[{index}]")
    return {
        "id": ident(raw["id"], "recorded_decisions.id"),
        "text": prose(raw["text"], "recorded_decisions.text"),
        "source_sha256": hex64(raw["source_sha256"], "recorded_decisions.source_sha256"),
    }


def parse_agreement(raw) -> dict:
    exact(
        raw,
        {"goal", "scope", "prime_discretion", "director_required", "finish_criteria", "recorded_decisions"},
        "agreement",
    )
    criteria = raw["finish_criteria"]
    decisions = raw["recorded_decisions"]
    if criteria is not None:
        criteria = [criterion(item, index) for index, item in enumerate(as_list(criteria, "finish_criteria"))]
        unique([item["id"] for item in criteria], "finish_criteria")
    if decisions is not None:
        decisions = [decision(item, index) for index, item in enumerate(as_list(decisions, "recorded_decisions"))]
        unique([item["id"] for item in decisions], "recorded_decisions")
    return {
        "goal": prose_or_null(raw["goal"], "agreement.goal"),
        "scope": prose_or_null(raw["scope"], "agreement.scope"),
        "prime_discretion": prose_or_null(raw["prime_discretion"], "agreement.prime_discretion"),
        "director_required": prose_or_null(raw["director_required"], "agreement.director_required"),
        "finish_criteria": criteria,
        "recorded_decisions": decisions,
    }


def string_list(value, where: str):
    if value is None:
        return None
    return [prose(item, where) for item in as_list(value, where)]


def parse_for_model(value):
    if value is None:
        return None
    exact(value, {"model", "prompt"}, "for_model")
    model = prose(value["model"], "for_model.model")
    need("\n" not in model and "\r" not in model, "bad for_model.model")
    return {"model": model, "prompt": prose(value["prompt"], "for_model.prompt")}


def parse_question(value):
    if value is None:
        return None
    exact(value, {"id", "revision", "content_sha256", "text"}, "question")
    revision = value["revision"]
    need(isinstance(revision, str) and REV.fullmatch(revision) is not None, "bad question revision")
    return {
        "id": ident(value["id"], "question.id"),
        "revision": revision,
        "content_sha256": hex64(value["content_sha256"], "question.content_sha256"),
        "text": prose(value["text"], "question.text"),
    }


def parse_affected(value):
    if value is None:
        return None
    rows = []
    for index, item in enumerate(as_list(value, "affected")):
        exact(item, {"action_id", "dependency"}, f"affected[{index}]")
        rows.append({
            "action_id": ident(item["action_id"], "affected.action_id"),
            "dependency": prose(item["dependency"], "affected.dependency"),
        })
    unique([item["action_id"] for item in rows], "affected")
    return rows


def parse_plan(value):
    if value is None:
        return None
    exact(value, {"label", "text"}, "proposed_plan")
    need(value["label"] == "proposed-plan", "bad proposed_plan label")
    return {"label": "proposed-plan", "text": prose(value["text"], "proposed_plan.text")}


def parse_account(value):
    if value is None:
        return None
    rows = []
    for index, item in enumerate(as_list(value, "findings_account")):
        exact(item, {"finding_id", "status"}, f"findings_account[{index}]")
        finding = item["finding_id"]
        need(isinstance(finding, str) and FINDING.fullmatch(finding) is not None, f"bad finding {finding}")
        need(item["status"] in {"open", "accepted", "discarded", "unresolved"}, "bad finding status")
        rows.append({"finding_id": finding, "status": item["status"]})
    unique([item["finding_id"] for item in rows], "findings_account")
    return rows


def parse_assessments(value):
    if value is None:
        return None
    rows = []
    for index, item in enumerate(as_list(value, "finish_assessments")):
        exact(item, {"criterion_id", "assessment"}, f"finish_assessments[{index}]")
        need(item["assessment"] in {"met", "unmet", "unknown"}, "bad assessment")
        rows.append({
            "criterion_id": ident(item["criterion_id"], "finish_assessments.criterion_id"),
            "assessment": item["assessment"],
        })
    unique([item["criterion_id"] for item in rows], "finish_assessments")
    return rows


def parse_sections(raw) -> dict:
    exact(raw, SECTION_KEYS, "sections")
    tests_passed = raw["tests_passed"]
    need(tests_passed is None or isinstance(tests_passed, bool), "bad type tests_passed")
    return {
        "return_result": prose_or_null(raw["return_result"], "return_result"),
        "prime_finding": prose_or_null(raw["prime_finding"], "prime_finding"),
        "within_direction": prose_or_null(raw["within_direction"], "within_direction"),
        "next_bounded_action": prose_or_null(raw["next_bounded_action"], "next_bounded_action"),
        "for_model": parse_for_model(raw["for_model"]),
        "issue": prose_or_null(raw["issue"], "issue"),
        "consequences": prose_or_null(raw["consequences"], "consequences"),
        "options": string_list(raw["options"], "options"),
        "recommendation": prose_or_null(raw["recommendation"], "recommendation"),
        "question": parse_question(raw["question"]),
        "affected": parse_affected(raw["affected"]),
        "proposed_plan": parse_plan(raw["proposed_plan"]),
        "exploration": prose_or_null(raw["exploration"], "exploration"),
        "assumptions": string_list(raw["assumptions"], "assumptions"),
        "open_questions": string_list(raw["open_questions"], "open_questions"),
        "outcome_evidence": prose_or_null(raw["outcome_evidence"], "outcome_evidence"),
        "limits": prose_or_null(raw["limits"], "limits"),
        "tests_note": prose_or_null(raw["tests_note"], "tests_note"),
        "tests_passed": tests_passed,
        "learning": prose_or_null(raw["learning"], "learning"),
        "preservation": prose_or_null(raw["preservation"], "preservation"),
        "remaining_choices": string_list(raw["remaining_choices"], "remaining_choices"),
        "findings_account": parse_account(raw["findings_account"]),
        "finish_assessments": parse_assessments(raw["finish_assessments"]),
    }


def parse_judgment(raw) -> dict:
    exact(raw, {"outcome", "finding", "reasons", "semantic_conflict", "design_fork", "next_action", "sections"}, "judgment")
    outcome = raw["outcome"]
    need(outcome is None or outcome in OUTCOMES, "bad outcome")
    semantic = raw["semantic_conflict"]
    need(semantic is None or isinstance(semantic, bool), "bad type semantic_conflict")
    fork = raw["design_fork"]
    if fork is not None:
        exact(fork, {"id", "text"}, "design_fork")
        fork = {"id": ident(fork["id"], "design_fork.id"), "text": prose(fork["text"], "design_fork.text")}
    return {
        "outcome": outcome,
        "finding": prose_or_null(raw["finding"], "finding"),
        "reasons": string_list(raw["reasons"], "reasons"),
        "semantic_conflict": semantic,
        "design_fork": fork,
        "next_action": prose_or_null(raw["next_action"], "next_action"),
        "sections": parse_sections(raw["sections"]),
    }


def parse_hold(raw, index: int) -> dict:
    exact(
        raw,
        {
            "hold_id",
            "finding_id",
            "kind",
            "question_id",
            "question_revision",
            "question_sha256",
            "dependent_scope",
        },
        f"holds[{index}]",
    )
    need(raw["kind"] in HOLD_KINDS, "bad hold kind")
    revision = raw["question_revision"]
    need(isinstance(revision, str) and REV.fullmatch(revision) is not None, "bad question revision")
    finding = raw["finding_id"]
    need(isinstance(finding, str) and FINDING.fullmatch(finding) is not None, f"bad finding {finding}")
    scope = [ident(item, "dependent_scope") for item in as_list(raw["dependent_scope"], "dependent_scope")]
    unique(scope, "dependent_scope")
    return {
        "hold_id": ident(raw["hold_id"], "hold_id"),
        "finding_id": finding,
        "kind": raw["kind"],
        "question_id": ident(raw["question_id"], "question_id"),
        "question_revision": revision,
        "question_sha256": hex64(raw["question_sha256"], "question_sha256"),
        "dependent_scope": scope,
    }


def parse_answer(raw, index: int) -> dict:
    exact(
        raw,
        {
            "answer_id",
            "question_id",
            "question_revision",
            "question_sha256",
            "reply",
            "provenance",
            "disposition",
        },
        f"answers[{index}]",
    )
    revision = raw["question_revision"]
    need(isinstance(revision, str) and REV.fullmatch(revision) is not None, "bad question revision")
    reply = raw["reply"]
    need(isinstance(reply, str), "bad type reply")
    need(len(reply) <= MAX_TEXT, "text limit reply")
    disposition = raw["disposition"]
    need(disposition is None or disposition in {"brief-approval", "new-detail", "unresolved"}, "bad disposition")
    return {
        "answer_id": ident(raw["answer_id"], "answer_id"),
        "question_id": ident(raw["question_id"], "question_id"),
        "question_revision": revision,
        "question_sha256": hex64(raw["question_sha256"], "question_sha256"),
        "reply": reply,
        "provenance": attribution(raw["provenance"], f"answers[{index}].provenance"),
        "disposition": disposition,
    }


def parse_pass(raw, index: int) -> dict:
    exact(
        raw,
        {"pass_id", "finding_id", "review_record_sha256", "result", "prior_pass_id", "tool_retry"},
        f"review_passes[{index}]",
    )
    finding = raw["finding_id"]
    need(isinstance(finding, str) and FINDING.fullmatch(finding) is not None, f"bad finding {finding}")
    need(raw["result"] in {"unresolved", "resolved"}, "bad review result")
    need(isinstance(raw["tool_retry"], bool), "bad type tool_retry")
    return {
        "pass_id": ident(raw["pass_id"], "pass_id"),
        "finding_id": finding,
        "review_record_sha256": hex64_or_null(raw["review_record_sha256"], "review_record_sha256"),
        "result": raw["result"],
        "prior_pass_id": ident_or_null(raw["prior_pass_id"], "prior_pass_id"),
        "tool_retry": raw["tool_retry"],
    }


def parse_record(raw, root: Path | None) -> dict:
    exact(raw, RECORD_KEYS, "record")
    need(raw["schema"] == SCHEMA_RECORD, "bad schema")
    sources = as_list(raw["sources"], "sources")
    need(len(sources) >= 1, "missing sources")
    parsed_sources = [parse_source(item, index, root) for index, item in enumerate(sources)]
    unique([item["logical_path"] for item in parsed_sources], "sources")
    holds = [parse_hold(item, index) for index, item in enumerate(as_list(raw["holds"], "holds"))]
    unique([item["hold_id"] for item in holds], "holds")
    answers = [parse_answer(item, index) for index, item in enumerate(as_list(raw["answers"], "answers"))]
    unique([item["answer_id"] for item in answers], "answers")
    passes = [parse_pass(item, index) for index, item in enumerate(as_list(raw["review_passes"], "review_passes"))]
    unique([item["pass_id"] for item in passes], "review_passes")
    gaps = [prose(item, "gaps") for item in as_list(raw["gaps"], "gaps")]
    return {
        "schema": SCHEMA_RECORD,
        "attribution": attribution(raw["attribution"], "attribution"),
        "sources": parsed_sources,
        "agreement": parse_agreement(raw["agreement"]),
        "judgment": parse_judgment(raw["judgment"]),
        "holds": holds,
        "answers": answers,
        "review_passes": passes,
        "gaps": gaps,
    }


def question_needs_reconciliation(hold: dict, sources: list[dict]) -> bool:
    for source in sources:
        if source["change"] == "substantive" and hold["question_sha256"] == source["prior_content_sha256"]:
            return True
    return False


def derive_holds(record: dict, attention: list[str]) -> list[dict]:
    derived = []
    for hold in record["holds"]:
        exact_matches = []
        stale = []
        rehash = []
        for answer in record["answers"]:
            same_id = answer["question_id"] == hold["question_id"]
            same_rev = answer["question_revision"] == hold["question_revision"]
            same_hash = answer["question_sha256"] == hold["question_sha256"]
            if same_id and same_rev and same_hash:
                exact_matches.append(answer)
            elif same_id and same_rev and not same_hash:
                rehash.append(answer)
            elif same_id and not same_rev:
                stale.append(answer)
        status = "unresolved"
        bound_ids = [item["answer_id"] for item in exact_matches]
        if question_needs_reconciliation(hold, record["sources"]):
            status = "reconciliation-required"
            attention.append(f"source change needs reconciliation: {hold['hold_id']}")
        elif len(exact_matches) > 1:
            status = "ambiguous"
            attention.append(f"answer lineage is ambiguous: {hold['question_id']}")
        elif len(exact_matches) == 1:
            answer = exact_matches[0]
            role = answer["provenance"]["role"]
            disposition = answer["disposition"]
            if disposition == "new-detail":
                status = "open-new-detail"
                attention.append(f"answer is new detail and stays open: {answer['answer_id']}")
            elif disposition == "brief-approval" and role == "director" and answer["reply"].strip() != "":
                status = "reply-bound"
            elif disposition == "brief-approval" and role != "director":
                status = "model-blocked"
                attention.append(f"model cannot answer for the Director: {answer['answer_id']}")
            elif disposition == "brief-approval":
                status = "unresolved"
                attention.append(f"empty reply does not bind: {answer['answer_id']}")
            elif disposition is None:
                status = "unresolved"
                attention.append(f"disposition is unknown: {answer['answer_id']}")
            else:
                status = "unresolved"
        elif rehash:
            status = "reconciliation-required"
            attention.append(f"answer needs reconciliation: {rehash[0]['answer_id']}")
        elif stale:
            status = "stale"
            attention.append(f"answer is stale: {stale[0]['answer_id']}")
        derived.append({
            "hold_id": hold["hold_id"],
            "finding_id": hold["finding_id"],
            "kind": hold["kind"],
            "question_id": hold["question_id"],
            "question_revision": hold["question_revision"],
            "question_sha256": hold["question_sha256"],
            "dependent_scope": list(hold["dependent_scope"]),
            "status": status,
            "answer_ids": bound_ids,
        })
    return derived


def compute_elevation(passes: list[dict], attention: list[str]) -> list[dict]:
    known = {item["pass_id"] for item in passes}
    order = []
    grouped: dict[str, list[dict]] = {}
    for item in passes:
        grouped.setdefault(item["finding_id"], [])
        if item["finding_id"] not in order:
            order.append(item["finding_id"])
        grouped[item["finding_id"]].append(item)
    rows = []
    for finding in order:
        attempts = grouped[finding]
        countable = [
            item for item in attempts
            if item["result"] == "unresolved" and not item["tool_retry"] and item["review_record_sha256"] is not None
        ]
        retries = [item for item in attempts if item["tool_retry"]]
        dangling = any(item["prior_pass_id"] is not None and item["prior_pass_id"] not in known for item in attempts)
        elevate = False
        if dangling or (len(countable) >= 2 and not _chain(countable)):
            reason = "lineage is ambiguous"
            attention.append(f"elevation lineage is ambiguous: {finding}")
        elif len(countable) >= 2 and _chain(countable):
            elevate = True
            reason = "two linked unresolved reviews"
            attention.append(f"elevation indicated: {finding}")
        elif len(countable) == 0 and len(retries) >= 2:
            reason = "tool retries are not review passes"
        else:
            reason = "fewer than two linked unresolved reviews"
        rows.append({
            "finding_id": finding,
            "elevate": elevate,
            "reason": reason,
            "attempts": [
                {
                    "pass_id": item["pass_id"],
                    "result": item["result"],
                    "tool_retry": item["tool_retry"],
                    "review_record_sha256": item["review_record_sha256"],
                    "prior_pass_id": item["prior_pass_id"],
                }
                for item in attempts
            ],
        })
    return rows


def _chain(countable: list[dict]) -> bool:
    if countable[0]["prior_pass_id"] is not None:
        return False
    previous = countable[0]["pass_id"]
    for item in countable[1:]:
        if item["prior_pass_id"] != previous:
            return False
        previous = item["pass_id"]
    return True


def agreement_gaps(agreement: dict, attention: list[str]) -> list[str]:
    gaps = []
    for key in ("goal", "scope", "prime_discretion", "director_required", "finish_criteria", "recorded_decisions"):
        if agreement[key] is None:
            gaps.append(key)
            attention.append(f"agreement.{key} is unknown")
    return gaps


def require_text(value, code: str, attention: list[str]) -> bool:
    if value is None:
        attention.append(code)
        return False
    return True


def design_hold(holds: list[dict]) -> bool:
    return any(item["kind"] in {"design-conflict", "design-fork"} for item in holds)


def hold_is_open(holds: list[dict]) -> bool:
    return any(item["status"] != "reply-bound" for item in holds)


def complete_ready(record: dict, attention: list[str]) -> bool:
    sections = record["judgment"]["sections"]
    agreement = record["agreement"]
    ready = True
    for key, code in (
        ("outcome_evidence", "complete is missing outcome_evidence"),
        ("limits", "complete is missing limits"),
        ("tests_note", "complete is missing tests_note"),
        ("learning", "complete is missing learning"),
        ("preservation", "complete is missing preservation"),
    ):
        ready = require_text(sections[key], code, attention) and ready
    if sections["remaining_choices"] is None:
        attention.append("complete is missing remaining_choices")
        ready = False
    criteria = agreement["finish_criteria"] or []
    assessments = sections["finish_assessments"] or []
    if not criteria:
        attention.append("complete has no finish criterion")
        ready = False
    assessed = {item["criterion_id"]: item["assessment"] for item in assessments}
    known = {item["id"] for item in criteria}
    for item in assessments:
        if item["criterion_id"] not in known:
            raise Refusal(f"unknown criterion {item['criterion_id']}")
    for item in criteria:
        assessment = assessed.get(item["id"])
        if assessment is None:
            attention.append(f"finish criterion not assessed: {item['id']}")
            ready = False
        elif assessment == "unmet":
            attention.append(f"finish criterion unmet: {item['id']}")
            ready = False
        elif assessment == "unknown":
            attention.append(f"finish criterion unknown: {item['id']}")
            ready = False
    declared = set()
    for hold in record["holds"]:
        declared.add(hold["finding_id"])
    for item in record["review_passes"]:
        declared.add(item["finding_id"])
    account = sections["findings_account"] or []
    if not account:
        attention.append("complete has no accounted finding")
        ready = False
    accounted = {item["finding_id"] for item in account}
    for finding in sorted(declared):
        if finding not in accounted:
            attention.append(f"finding not accounted: {finding}")
            ready = False
    for item in account:
        if item["status"] in {"open", "unresolved"}:
            attention.append(f"finding unresolved: {item['finding_id']}")
            ready = False
    return ready


def collect_outcome_gaps(record: dict, attention: list[str]) -> None:
    judgment = record["judgment"]
    sections = judgment["sections"]
    outcome = judgment["outcome"]
    if outcome is None:
        attention.append("outcome is unknown")
    if judgment["finding"] is None:
        attention.append("finding is unknown")
    if not judgment["reasons"]:
        attention.append("reasons are unknown")
    if judgment["semantic_conflict"] is None:
        attention.append("semantic_conflict is unknown")
    elif judgment["semantic_conflict"] is True and not design_hold(record["holds"]):
        attention.append("semantic_conflict is true and no design hold declares a dependent scope")
    if outcome == "continue":
        require_text(sections["return_result"], "continue is missing return_result", attention)
        require_text(sections["prime_finding"], "continue is missing prime_finding", attention)
        require_text(sections["within_direction"], "continue is missing within_direction", attention)
        require_text(sections["next_bounded_action"], "continue is missing next_bounded_action", attention)
        require_text(judgment["next_action"], "continue is missing next_action", attention)
    elif outcome == "director-input":
        require_text(sections["issue"], "director-input is missing issue", attention)
        require_text(sections["consequences"], "director-input is missing consequences", attention)
        if not sections["options"]:
            attention.append("director-input is missing options")
        require_text(sections["recommendation"], "director-input is missing recommendation", attention)
        question = sections["question"]
        if question is None:
            attention.append("director-input is missing question")
        if not sections["affected"]:
            attention.append("director-input is missing affected work")
        if question is not None:
            matched = [
                hold for hold in record["holds"]
                if hold["question_id"] == question["id"]
                and hold["question_revision"] == question["revision"]
                and hold["question_sha256"] == question["content_sha256"]
            ]
            if not matched:
                attention.append("director-input question has no matching hold")
        covered = {action for hold in record["holds"] for action in hold["dependent_scope"]}
        for item in sections["affected"] or []:
            if item["action_id"] not in covered:
                attention.append(f"affected action has no hold scope: {item['action_id']}")
    elif outcome == "develop":
        require_text(sections["exploration"], "develop is missing exploration", attention)
        if not sections["assumptions"]:
            attention.append("develop is missing assumptions")
        if not sections["open_questions"]:
            attention.append("develop is missing open_questions")
    elif outcome == "complete":
        complete_ready(record, attention)


def _director_incomplete(attention: list[str]) -> bool:
    markers = (
        "director-input",
        "agreement.",
        "is unknown",
        "are unknown",
        "no design hold",
        "no matching hold",
        "no hold scope",
    )
    return any(any(marker in item for marker in markers) for item in attention)


def decide(record: dict, attention: list[str], holds: list[dict], elevation: list[dict]) -> str:
    outcome = record["judgment"]["outcome"]
    open_hold = len(holds) > 0 and hold_is_open(holds)
    elevated = any(item["elevate"] for item in elevation)
    if outcome == "continue" and open_hold:
        attention.append("hold overrides the continue label")
    dirty = bool(attention) or open_hold or elevated
    if not dirty and outcome == "continue":
        return "continue"
    if not dirty and outcome == "develop":
        return "develop"
    if not dirty and outcome == "complete":
        return "complete-as-supplied"
    if outcome == "director-input":
        if _director_incomplete(attention) or not holds:
            return "attention"
        return "hold"
    if outcome == "complete" and not open_hold and not elevated:
        return "not-closed"
    if open_hold or elevated:
        return "hold"
    if outcome == "complete":
        return "not-closed"
    return "attention"


def answer_rows(record: dict, holds: list[dict]) -> list[dict]:
    status_by_answer = {}
    for hold in holds:
        for answer_id in hold["answer_ids"]:
            status_by_answer[answer_id] = hold["status"]
    rows = []
    for answer in record["answers"]:
        binding = status_by_answer.get(answer["answer_id"], "unmatched")
        if binding == "unmatched":
            for hold in holds:
                if answer["question_id"] == hold["question_id"] and hold["status"] in {
                    "reconciliation-required",
                    "stale",
                    "ambiguous",
                    "open-new-detail",
                    "model-blocked",
                }:
                    binding = hold["status"]
                    break
        rows.append({
            "answer_id": answer["answer_id"],
            "question_id": answer["question_id"],
            "binding": binding,
            "reply": answer["reply"],
            "role": answer["provenance"]["role"],
            "disposition": answer["disposition"],
        })
    return rows


def add_block(lines: list[str], title: str, text: str | None) -> None:
    if text is None:
        return
    lines.append(f"## {title}")
    lines.append(text)
    lines.append("")


def add_items(lines: list[str], title: str, items) -> None:
    if not items:
        return
    lines.append(f"## {title}")
    for item in items:
        lines.append(item)
        lines.append("")


def render_markdown(report: dict) -> str:
    lines = [
        "# Prime review draft",
        f"schema: {SCHEMA_REPORT}",
        "authority: none",
        "closes_work: false",
        "releases_action: false",
        "authenticates_actor: false",
        f"permission: {report['permission']}",
        f"authorizes_task: false",
        "tasks_added: none",
        "",
        f"Supplied outcome: {report['supplied_outcome'] if report['supplied_outcome'] is not None else 'unknown'}",
        f"Effective: {report['effective']}",
        f"Supplied semantic_conflict: {report['supplied_semantic_conflict']}",
        "",
        "## Attribution",
        f"actor_label: {report['attribution']['actor_label']}",
        f"role: {report['attribution']['role']}",
        f"evidence: {report['attribution']['evidence']}",
        "This module does not prove that identity.",
        "",
    ]
    if report["attention"]:
        lines.append("## Attention")
        for item in report["attention"]:
            lines.append(f"- {item}")
        lines.append("")
    sections = report["sections"]
    add_block(lines, "Return and result", sections["return_result"])
    add_block(lines, "Prime finding", sections["prime_finding"] or report["finding"])
    add_block(lines, "Within direction", sections["within_direction"])
    add_block(lines, "Next bounded action", sections["next_bounded_action"])
    if report["next_action"] is not None:
        add_block(lines, "Supplied next action", report["next_action"] + "\nThis line is not a release.")
    add_block(lines, "Issue", sections["issue"])
    add_block(lines, "Consequences", sections["consequences"])
    add_items(lines, "Options", sections["options"])
    add_block(lines, "Recommendation", sections["recommendation"])
    question = sections["question"]
    if question is not None:
        lines.append("## Question")
        lines.append(f"id: {question['id']}")
        lines.append(f"revision: {question['revision']}")
        lines.append(f"content_sha256: {question['content_sha256']}")
        lines.append("text:")
        lines.append(question["text"])
        lines.append("")
    if sections["affected"]:
        lines.append("## Affected work")
        for item in sections["affected"]:
            lines.append(f"- {item['action_id']}: {item['dependency']}")
        lines.append("")
    plan = sections["proposed_plan"]
    if plan is not None:
        lines.append("## Proposed plan")
        lines.append(f"label: {plan['label']}")
        lines.append("This block is not executable.")
        lines.append(plan["text"])
        lines.append("")
    add_block(lines, "Exploration", sections["exploration"])
    add_items(lines, "Assumptions", sections["assumptions"])
    add_items(lines, "Open questions", sections["open_questions"])
    add_block(lines, "Agreed outcome evidence", sections["outcome_evidence"])
    add_block(lines, "Limits", sections["limits"])
    add_block(lines, "Tests", sections["tests_note"])
    if sections["tests_passed"] is True:
        lines.append("tests_passed: true")
        lines.append("Tests do not close this work.")
        lines.append("")
    elif sections["tests_passed"] is False:
        lines.append("tests_passed: false")
        lines.append("")
    add_block(lines, "Learning", sections["learning"])
    add_block(lines, "Preservation", sections["preservation"])
    add_items(lines, "Remaining choices", sections["remaining_choices"])
    if sections["findings_account"]:
        lines.append("## Findings account")
        for item in sections["findings_account"]:
            lines.append(f"- {item['finding_id']} {item['status']}")
        lines.append("")
    if sections["finish_assessments"]:
        lines.append("## Finish criteria")
        for item in sections["finish_assessments"]:
            lines.append(f"- {item['criterion_id']} {item['assessment']}")
        lines.append("")
    if report["holds"]:
        lines.append("## Holds")
        for hold in report["holds"]:
            lines.append(
                f"- {hold['hold_id']} {hold['kind']} status {hold['status']} "
                f"question {hold['question_id']} {hold['question_revision']} {hold['question_sha256']}"
            )
            lines.append(f"  scope: {', '.join(hold['dependent_scope']) if hold['dependent_scope'] else '(none)'}")
        lines.append("")
    if report["answers"]:
        lines.append("## Answers")
        for answer in report["answers"]:
            lines.append(f"id: {answer['answer_id']}")
            lines.append(f"binding: {answer['binding']}")
            lines.append(f"role: {answer['role']}")
            lines.append(f"disposition: {answer['disposition']}")
            lines.append("reply:")
            lines.append(answer["reply"])
            lines.append("")
    if report["elevation"]:
        lines.append("## Elevation")
        for row in report["elevation"]:
            lines.append(f"finding: {row['finding_id']}")
            lines.append(f"elevate: {str(row['elevate']).lower()}")
            lines.append(f"reason: {row['reason']}")
            lines.append("attempts:")
            for attempt in row["attempts"]:
                record = attempt["review_record_sha256"] if attempt["review_record_sha256"] is not None else "null"
                lines.append(
                    f"- {attempt['pass_id']} result {attempt['result']} "
                    f"tool_retry {str(attempt['tool_retry']).lower()} review_record {record}"
                )
            lines.append("")
    lines.append("## Sources")
    for source in report["sources"]:
        lines.append(
            f"- {source['kind']} `{source['logical_path']}` content {source['content_sha256']} "
            f"transport {source['transport_sha256']} change {source['change']}"
        )
    lines.append("")
    if report["gaps"]:
        lines.append("## Known gaps")
        for gap in report["gaps"]:
            lines.append(gap)
            lines.append("")
    prompt = report["prompt"]
    if prompt["emitted"]:
        lines.append(f"## For {prompt['model']}")
        lines.append(prompt["text"])
        lines.append("")
    elif prompt["reason"] == "withheld":
        lines.append("## For [model]")
        lines.append("withheld: no executable prompt is included.")
        lines.append("")
    text = "\n".join(lines)
    if not text.endswith("\n"):
        text += "\n"
    return text


def build_report(record: dict) -> dict:
    attention: list[str] = []
    gaps = agreement_gaps(record["agreement"], attention)
    holds = derive_holds(record, attention)
    elevation = compute_elevation(record["review_passes"], attention)
    before = len(attention)
    collect_outcome_gaps(record, attention)
    del before
    effective = decide(record, attention, holds, elevation)
    sections = record["judgment"]["sections"]
    for_model = sections["for_model"]
    emitted = effective == "continue" and for_model is not None
    if for_model is not None and not emitted:
        attention.append("for_model prompt withheld")
        if effective == "continue":
            effective = "attention"
    if any(item == "for_model prompt withheld" for item in attention) or effective in {"hold", "attention", "not-closed"}:
        permission = "withheld"
    else:
        permission = "recorded-only"
    prompt = (
        {"emitted": True, "model": for_model["model"], "text": for_model["prompt"], "reason": "supplied"}
        if emitted
        else {"emitted": False, "reason": "withheld" if for_model is not None else "not-supplied"}
    )
    semantic = record["judgment"]["semantic_conflict"]
    shown_sections = dict(sections)
    if not emitted:
        shown_sections["for_model"] = None
    report = {
        "schema": SCHEMA_REPORT,
        "authority": "none",
        "closes_work": False,
        "releases_action": False,
        "authenticates_actor": False,
        "tasks_added": [],
        "permission": permission,
        "supplied_outcome": record["judgment"]["outcome"],
        "effective": effective,
        "supplied_semantic_conflict": semantic if semantic is not None else "unknown",
        "attention": attention,
        "attribution": record["attribution"],
        "finding": record["judgment"]["finding"],
        "reasons": record["judgment"]["reasons"],
        "next_action": record["judgment"]["next_action"],
        "sections": shown_sections,
        "holds": holds,
        "answers": answer_rows(record, holds),
        "elevation": elevation,
        "sources": [
            {
                "kind": source["kind"],
                "logical_path": source["logical_path"],
                "content_sha256": source["content_sha256"],
                "transport_sha256": source["transport_sha256"],
                "change": source["change"],
                "identity_schema": source["identity"]["schema"],
            }
            for source in record["sources"]
        ],
        "agreement_gaps": gaps,
        "gaps": list(record["gaps"]),
        "prompt": prompt,
    }
    markdown = render_markdown(report)
    report["markdown"] = markdown
    report["markdown_sha256"] = sha256_bytes(markdown.encode("utf-8"))
    return report


def report_exit(report: dict) -> int:
    if report["attention"]:
        return 1
    if report["effective"] in {"continue", "develop", "complete-as-supplied"}:
        return 0
    return 1


def build_guard(review: dict, action: dict) -> dict:
    exact(action, {"action_id", "label", "grant_ref", "authorized_in_grant"}, "proposed_action")
    action_id = ident(action["action_id"], "action_id")
    label = prose(action["label"], "proposed_action.label")
    grant_ref = prose_or_null(action["grant_ref"], "grant_ref")
    authorized = action["authorized_in_grant"]
    need(authorized is None or isinstance(authorized, bool), "bad type authorized_in_grant")
    report = build_report(review)
    covering = [hold for hold in report["holds"] if action_id in hold["dependent_scope"]]
    others = [hold for hold in report["holds"] if action_id not in hold["dependent_scope"]]
    if authorized is False:
        result = "outside-declared-grant"
    elif authorized is None:
        result = "attention"
    elif not covering:
        result = "independent-of-holds"
    elif any(hold["status"] in BLOCKING for hold in covering):
        result = "blocked"
    elif all(hold["status"] == "reply-bound" for hold in covering):
        result = "not-released"
    else:
        result = "blocked"
    guard = {
        "schema": SCHEMA_GUARD_RESULT,
        "authority": "none",
        "releases_action": False,
        "authenticates_actor": False,
        "closes_work": False,
        "action_id": action_id,
        "label": label,
        "grant_ref": grant_ref,
        "authorized_in_grant": authorized if authorized is not None else "unknown",
        "result": result,
        "supplied_outcome": report["supplied_outcome"],
        "effective": report["effective"],
        "covering": covering,
        "other_holds": others,
        "elevation": report["elevation"],
        "review_attention": report["attention"],
        "permission": "withheld" if result != "independent-of-holds" else "not-blocked-by-these-holds",
    }
    lines = [
        "# Prime review guard",
        f"schema: {SCHEMA_GUARD_RESULT}",
        "authority: none",
        "releases_action: false",
        "closes_work: false",
        f"action: {action_id}",
        f"result: {result}",
        "This check does not release the action.",
        f"supplied_outcome: {report['supplied_outcome']}",
        f"effective: {report['effective']}",
    ]
    if covering:
        lines.append("covering:")
        for hold in covering:
            lines.append(f"- {hold['hold_id']} {hold['status']}")
    if others:
        lines.append("other_holds:")
        for hold in others:
            lines.append(f"- {hold['hold_id']} {hold['status']}")
    if report["elevation"]:
        for row in report["elevation"]:
            lines.append(f"elevation: {row['finding_id']} {str(row['elevate']).lower()} {row['reason']}")
    lines.append("")
    guard["markdown"] = "\n".join(lines)
    return guard


def guard_exit(guard: dict) -> int:
    if guard["result"] == "independent-of-holds":
        return 0
    return 1


def dump_json(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def load_input(path: Path) -> bytes:
    return read_regular(path, "input")


def optional_root(text: str | None) -> Path | None:
    if text is None:
        return None
    root = absolute_local(text, "root")
    require_directory(root, "root")
    return root


def report_from_bytes(data: bytes, root: Path | None) -> tuple[dict, int]:
    raw = strict_json(data, "input")
    record = parse_record(raw, root)
    report = build_report(record)
    return report, report_exit(report)


def guard_from_bytes(data: bytes, root: Path | None) -> tuple[dict, int]:
    raw = strict_json(data, "input")
    exact(raw, {"schema", "review", "proposed_action"}, "guard")
    need(raw["schema"] == SCHEMA_GUARD, "bad schema")
    review = parse_record(raw["review"], root)
    guard = build_guard(review, raw["proposed_action"])
    return guard, guard_exit(guard)


def _write_fd(fd: int, payload: bytes) -> None:
    os.write(fd, payload)


def write_draft(data: bytes, dest: Path, repo: Path, expect: str, root: Path | None) -> None:
    hex64(expect, "expect-sha256")
    require_directory(repo, "repo")
    need(dest.is_absolute(), "path must be absolute dest")
    need(not inside(dest, repo), "destination inside repository")
    parent = dest.parent
    require_directory(parent, "dest parent")
    try:
        info = dest.lstat()
    except FileNotFoundError:
        info = None
    if info is not None:
        raise Refusal("destination exists")
    report, _code = report_from_bytes(data, root)
    payload = report["markdown"].encode("utf-8")
    need(sha256_bytes(payload) == expect, "digest mismatch")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    try:
        fd = os.open(str(dest), flags)
    except FileExistsError:
        raise Refusal("destination exists") from None
    except OSError as exc:
        raise Refusal(f"cannot create destination: {exc.errno}") from None
    try:
        _write_fd(fd, payload)
    except OSError:
        raise Refusal("partial draft retained") from None
    finally:
        os.close(fd)


def write_out(text: str) -> None:
    """Write UTF-8 bytes when stdout has a buffer, so Windows does not insert CR."""
    data = text.encode("utf-8")
    buffer = getattr(sys.stdout, "buffer", None)
    if buffer is not None:
        buffer.write(data)
    else:
        sys.stdout.write(text)


def emit(payload: dict, code: int, as_json: bool) -> int:
    write_out(dump_json(payload) if as_json else payload["markdown"])
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="prime_review")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("report", "guard", "check-next"):
        command = sub.add_parser(name)
        command.add_argument("--input", required=True)
        command.add_argument("--root")
        command.add_argument("--json", action="store_true")
    draft = sub.add_parser("draft")
    draft.add_argument("--input", required=True)
    draft.add_argument("--dest", required=True)
    draft.add_argument("--repo", required=True)
    draft.add_argument("--expect-sha256", required=True)
    draft.add_argument("--root")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code) if exc.code is not None else 2
    try:
        incoming = absolute_local(args.input, "input")
        data = load_input(incoming)
        root = optional_root(getattr(args, "root", None))
        if args.command == "report":
            report, code = report_from_bytes(data, root)
            return emit(report, code, args.json)
        if args.command in {"guard", "check-next"}:
            guard, code = guard_from_bytes(data, root)
            return emit(guard, code, args.json)
        dest = absolute_local(args.dest, "dest")
        repo = absolute_local(args.repo, "repo")
        write_draft(data, dest, repo, args.expect_sha256, root)
    except Refusal as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    write_out("wrote\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
