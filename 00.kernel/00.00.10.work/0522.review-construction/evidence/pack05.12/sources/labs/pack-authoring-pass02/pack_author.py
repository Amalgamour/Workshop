#!/usr/bin/env python3
"""Successor authoring module for usable forms and review binding.

Pass01 stays untouched. This module loads it under a private name and
replaces the form, review, and derived-face seams. The form declaration
is the only field list.
"""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

HELP = "labs/pack-authoring-pass02/PRIME-USE.md"
FORM_REL = "labs/pack-authoring-pass02/forms/build-pack-v1.json"
FORM_SHA = "b3d18c26699674d7aa0607e491210664b31e90a63dba13860befb5409b0416ab"
FORM_BYTES = 19453
PREDECESSOR = "labs/pack-authoring-pass01/pack_author.py"
PREDECESSOR_SHA = "30908475162fe9b1a566018d217d26465151b1243bb3a8f391cb54254f3ba10c"
PREDECESSOR_BYTES = 67547
FORM_KINDS = ("intent", "item", "note", "disposition", "review")
CONSTRAINTS = {"max_chars", "note_id", "existing_item", "book_path", "hex64", "module_key"}
RESULT = "authoring-result/2"

base = None
DECLARATION = None


def refuse(message: str) -> None:
    raise base.Refuse(message)


def load_bytes(path: Path, expected: str, size: int, label: str) -> bytes:
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected or len(raw) != size:
        raise RuntimeError(f"{label} pin does not match")
    return raw


def load_base() -> object:
    path = Path(__file__).resolve().parents[1] / "pack-authoring-pass01" / "pack_author.py"
    load_bytes(path, PREDECESSOR_SHA, PREDECESSOR_BYTES, "pass01")
    spec = importlib.util.spec_from_file_location("pack_author_pass01_pinned", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_declaration() -> dict:
    path = Path(__file__).resolve().parent / "forms" / "build-pack-v1.json"
    raw = load_bytes(path, FORM_SHA, FORM_BYTES, "form")
    document = json.loads(raw.decode("utf-8"))
    if document.get("schema") != "authoring-forms/1" or document.get("form_id") != "build-pack-v1":
        raise RuntimeError("form declaration identity does not match")
    forms = document["forms"]
    if set(forms) != set(FORM_KINDS):
        raise RuntimeError("form declaration kinds do not match")
    for kind in FORM_KINDS:
        check_fields(forms[kind]["fields"])
    return document


def check_fields(fields: list) -> None:
    names = []
    for field in fields:
        if field["type"] not in {"string", "enum", "string-list", "object", "object-list"}:
            raise RuntimeError(f"undeclared field type {field['name']}")
        if field["presence"] not in {"required", "optional", "required-when"}:
            raise RuntimeError(f"undeclared presence {field['name']}")
        names.append(field["name"])
        constraints = field.get("constraints") or {}
        if set(constraints) - CONSTRAINTS:
            raise RuntimeError(f"undeclared constraint on {field['name']}")
        if "fields" in field:
            check_fields(field["fields"])
        if "item_fields" in field:
            check_fields(field["item_fields"])
    if len(names) != len(set(names)):
        raise RuntimeError("form declaration repeats a field")


def field_by_name(kind: str, name: str) -> dict:
    for field in DECLARATION["forms"][kind]["fields"]:
        if field["name"] == name:
            return field
    refuse(f"form {kind} has no field {name}")
    return {}


def json_type(value: object) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "list"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, (int, float)):
        return "number"
    return "value"


def expected_shape(field: dict) -> str:
    kind = field["type"]
    if kind == "string":
        return "a non-empty string" if field.get("empty") == "refused" else "a string"
    if kind == "enum":
        return "one of " + ", ".join(field["values"])
    if kind == "string-list":
        return "a list of strings"
    if kind == "object-list":
        return "a list of objects"
    return "an object"


def field_stop(name: str, state: str, expected: str, retained: str) -> None:
    refuse(
        f"typed-field: {name} state {state}; expected {expected}; retained input {retained}. Help: {HELP}"
    )


def when_active(field: dict, value: dict) -> bool:
    spec = field.get("when")
    if not spec:
        return False
    return value.get(spec["field"]) in spec["values"]


def apply_constraints(field: dict, text: str, label: str, retained: str, context: dict) -> None:
    constraints = field.get("constraints") or {}
    if "max_chars" in constraints and len(text) > constraints["max_chars"]:
        field_stop(label, "wrong-type", f"a string up to {constraints['max_chars']} characters", retained)
    if constraints.get("book_path"):
        base.relative_parts(text)
    if constraints.get("hex64") and not base.HEX_RE.fullmatch(text):
        field_stop(label, "wrong-type", "64 lowercase hex", retained)
    if constraints.get("module_key") and text.count(":") != 1:
        field_stop(label, "wrong-type", "REPOSITORY:PATH", retained)
    known_notes = context.get("note_ids")
    if constraints.get("note_id") and known_notes is not None and text not in known_notes:
        field_stop(label, "wrong-type", "a declared or draft note id", retained)
    if constraints.get("existing_item"):
        if not base.ITEM_RE.fullmatch(text) or text not in context.get("item_ids", set()):
            field_stop(label, "wrong-type", "an existing item id", retained)


def apply_value(field: dict, got: object, retained: str, context: dict, label: str) -> object:
    if got is None:
        if field.get("null") == "not-applicable":
            return None
        field_stop(label, "null", expected_shape(field), retained)
    kind = field["type"]
    if kind == "string":
        if not isinstance(got, str):
            field_stop(label, "wrong-type", expected_shape(field), retained)
        if got.strip() == "" and field.get("empty") == "refused":
            field_stop(label, "empty", expected_shape(field), retained)
        apply_constraints(field, got, label, retained, context)
        return got
    if kind == "enum":
        if not isinstance(got, str):
            field_stop(label, "wrong-type", expected_shape(field), retained)
        if got.strip() == "" and field.get("empty") == "refused":
            field_stop(label, "empty", expected_shape(field), retained)
        if got not in field["values"]:
            field_stop(label, "wrong-type", expected_shape(field), retained)
        return got
    if kind == "string-list":
        if not isinstance(got, list):
            field_stop(label, "wrong-type", expected_shape(field), retained)
        minimum = field["min_items"]
        maximum = field["max_items"]
        if len(got) == 0 and field.get("empty") == "refused":
            field_stop(label, "empty", expected_shape(field), retained)
        if len(got) < minimum or len(got) > maximum:
            field_stop(label, "wrong-type", f"a list of {minimum} to {maximum} strings", retained)
        out = []
        for item in got:
            if not isinstance(item, str):
                field_stop(label, "wrong-type", expected_shape(field), retained)
            if item.strip() == "":
                field_stop(label, "empty", "a list of non-empty strings", retained)
            apply_constraints(field, item, label, retained, context)
            out.append(item)
        return out
    if kind == "object":
        if not isinstance(got, dict):
            field_stop(label, "wrong-type", expected_shape(field), retained)
        if got == {} and field.get("empty") == "refused":
            field_stop(label, "empty", expected_shape(field), retained)
        return apply_fields(field["fields"], got, retained, context, label + ".")
    if kind == "object-list":
        if not isinstance(got, list):
            field_stop(label, "wrong-type", expected_shape(field), retained)
        if len(got) == 0 and field.get("empty") == "refused":
            field_stop(label, "empty", expected_shape(field), retained)
        if len(got) < field["min_items"] or len(got) > field["max_items"]:
            field_stop(label, "wrong-type", "a list of objects", retained)
        rows = []
        for item in got:
            if not isinstance(item, dict):
                field_stop(label, "wrong-type", expected_shape(field), retained)
            rows.append(apply_fields(field["item_fields"], item, retained, context, label + "."))
        return rows
    field_stop(label, "wrong-type", expected_shape(field), retained)
    return None


def apply_fields(fields: list, value: dict, retained: str, context: dict, prefix: str) -> dict:
    if not isinstance(value, dict):
        field_stop(prefix[:-1] or "input", "wrong-type", "an object", retained)
    allowed = {field["name"] for field in fields}
    extra = sorted(set(value) - allowed)
    if extra:
        field_stop(prefix + extra[0], "extra", "an absent field", retained)
    out = {}
    for field in fields:
        name = field["name"]
        label = prefix + name
        needed = field["presence"] == "required" or (
            field["presence"] == "required-when" and when_active(field, value)
        )
        if name not in value:
            if needed:
                field_stop(label, "absent", expected_shape(field), retained)
            out[name] = None
            continue
        if not needed and field.get("otherwise") == "absent":
            field_stop(label, "extra", "an absent field", retained)
        out[name] = apply_value(field, value[name], retained, context, label)
    return out


def apply_form(kind: str, value: dict, retained: str, context: dict | None = None) -> dict:
    if kind not in DECLARATION["forms"]:
        refuse("unknown form")
    parsed = apply_fields(DECLARATION["forms"][kind]["fields"], value, retained, context or {}, "")
    if kind == "item" and isinstance(parsed.get("relationship"), dict):
        parsed["relationship"]["state"] = "unresolved-not-in-set"
    return parsed


def parse_intent(value: dict, retained: str) -> dict:
    return apply_form("intent", value, retained)


def parse_item(value: dict, retained: str) -> dict:
    return apply_form("item", value, retained)


def parse_note(value: dict, retained: str) -> dict:
    parsed = apply_form("note", value, retained)
    if "mark" not in parsed:
        parsed["mark"] = None
    return parsed


def parse_review(value: dict, retained: str) -> dict:
    return apply_form("review", value, retained)


def check_note_refs(record: dict, item: dict, retained: str) -> None:
    field = field_by_name("item", "note_refs")
    if not (field.get("constraints") or {}).get("note_id"):
        return
    known = {note["id"] for note in record["declared_notes"]} | {note["id"] for note in record["draft_notes"]}
    for ref in item["note_refs"]:
        if ref not in known:
            field_stop("note_refs", "wrong-type", "a declared or draft note id", retained)


def project(kind: str) -> dict:
    spec = DECLARATION["forms"][kind]
    return {
        "schema": "authoring-form/1",
        "form_id": spec["id"],
        "declaration": FORM_REL,
        "declaration_sha256": FORM_SHA,
        "declaration_bytes": FORM_BYTES,
        "kind": kind,
        "meaning": spec["meaning"],
        "owners": DECLARATION["owners"],
        "fields": spec["fields"],
        "example_input": spec["example_input"],
        "correction_help": spec["correction_help"],
        "not_submitted": spec["not_submitted"],
    }


def needed_kind(record: dict | None) -> str | None:
    if record is None or base.intent_missing(record):
        return "intent"
    if not record["items"]:
        return "item"
    notes = list(record["declared_notes"]) + list(record["draft_notes"])
    if any(note["disposition"] == "unresolved" for note in notes):
        return "disposition"
    if record["review"] is None:
        return "review"
    return None


def draft_status(record: dict | None) -> dict:
    if record is None:
        return {"state": "absent", "pass": None, "review": "absent", "missing": ["intent"]}
    return {
        "state": record["state"],
        "pass": record["pass"],
        "review": "present" if record.get("review") else "absent",
        "missing": base.gaps(record),
    }


def form_body(kind: str | None, profile: dict, profile_id: str, sources: list, record: dict | None) -> dict:
    if kind is None:
        body = {
            "schema": "authoring-form/1",
            "form_id": None,
            "declaration": FORM_REL,
            "declaration_sha256": FORM_SHA,
            "declaration_bytes": FORM_BYTES,
            "kind": None,
            "meaning": "No meaning form is waiting.",
            "owners": DECLARATION["owners"],
            "fields": [],
            "example_input": None,
            "correction_help": {"route": HELP, "states": [], "example": None},
            "not_submitted": ["candidate_sha256", "final_sha256"],
        }
    else:
        body = project(kind)
    body["profile_id"] = profile_id
    body["source_home"] = profile["source_home"]
    body["work_home"] = profile["work_home"]
    body["sources"] = sources
    body["draft_status"] = draft_status(record)
    return body


def open_record(ctx: dict) -> dict | None:
    sessions = base.open_sessions(ctx["work_dir"], ctx["profile_id"])
    if len(sessions) > 1:
        refuse("ambiguous session")
    if not sessions:
        return None
    return sessions[0][1]


def command_form(ctx: dict) -> int:
    record = open_record(ctx)
    kind = ctx["flags"].get("kind")
    if kind is None:
        kind = needed_kind(record)
    elif kind not in FORM_KINDS:
        refuse("unknown form")
    sources = base.measure_sources(ctx["book"], ctx["profile"])
    body = form_body(kind, ctx["profile"], ctx["profile_id"], sources, record)
    if ctx["json"]:
        sys.stdout.write(base.canonical_json(body).decode("utf-8"))
    else:
        sys.stdout.write(f"authoring-form/1\nkind: {kind}\nform-id: {body['form_id']}\n")
    return 0


def require_open(ctx: dict):
    slot, record = ORIGINAL_REQUIRE(ctx)
    if "form_binding" not in record:
        refuse("pass01 record is preserved")
    return slot, record


def next_step(record: dict, live: bool) -> str:
    if live:
        return "Prime can inspect this draft. Freeze on the live checkout is refused. This is not the Prime pilot."
    missing = base.gaps(record)
    if any(item in missing for item in ("goal", "finish", "executor", "reviewer")) or any(
        item.startswith("scope.") for item in missing
    ):
        return "supply intent through the intent form"
    if any(item.startswith("disposition ") for item in missing):
        return "supply a disposition for each declared note"
    if "item" in missing:
        return "add an item"
    if "review" in missing:
        return "review with the candidate sha256 shown by inspect"
    if record["state"] != "frozen":
        return "freeze with the final sha256 shown by inspect; return readiness stays blocked"
    return "The prepared page is written. Return readiness stays blocked."


def review_face(review: dict | None) -> dict | None:
    if review is None:
        return None
    return {
        "assessment": review["assessment"],
        "unresolved_issues": review["unresolved_issues"],
        "stop_conditions": review["stop_conditions"],
    }


def candidate_digest(record: dict) -> str:
    current = record.get("review")
    if current is None:
        return base.digest(base.render(record).encode("utf-8"))
    previous = current.get("candidate_review")
    record["review"] = previous
    try:
        text = base.render(record)
    finally:
        record["review"] = current
    return base.digest(text.encode("utf-8"))


def public_review(review: dict | None) -> dict | None:
    if not review:
        return None
    return {
        "assessment": review.get("assessment"),
        "unresolved_issues": review.get("unresolved_issues"),
        "stop_conditions": review.get("stop_conditions"),
        "candidate_sha256": review.get("candidate_sha256"),
        "final_sha256": review.get("final_sha256"),
    }


def face_view(record: dict) -> dict:
    stored = record.get("derived_face") or {
        "status": "absent",
        "preserved": None,
        "history": False,
        "divergence": False,
    }
    return stored


def result_for(record: dict, slot: Path, command: str, live: bool) -> dict:
    text = base.render(record)
    final_sha = base.digest(text.encode("utf-8"))
    if record.get("review"):
        candidate = record["review"].get("candidate_sha256") or candidate_digest(record)
        final = final_sha
    else:
        candidate = final_sha
        final = None
    face = face_view(record)
    page = slot.parent.parent / f"{record['pass']}.md"
    page_bytes = page.read_bytes() if page.is_file() and not base.is_link(page) else None
    kind = needed_kind(record)
    return {
        "schema": RESULT,
        "command": command,
        "state": record["state"],
        "pass": record["pass"],
        "record": str(slot / "record.json"),
        "draft": str(slot / "draft.md"),
        "draft_sha256": final_sha,
        "candidate_sha256": candidate,
        "final_sha256": final,
        "draft_text": text,
        "selected_review": public_review(record.get("review")),
        "form_id": DECLARATION["form_id"],
        "form_sha256": FORM_SHA,
        "next_form": kind,
        "form": project(kind) if kind else None,
        "next": next_step(record, live),
        "missing": base.gaps(record),
        "return_intent": record["return_intent"],
        "derived_history": bool(face.get("history")),
        "derived_divergence": bool(face.get("divergence")),
        "derived_conflict": bool(face.get("divergence")),
        "derived_preserved": face.get("preserved"),
        "face_status": face.get("status"),
        "page": str(page) if page_bytes is not None else None,
        "page_matches_draft": page_bytes == text.encode("utf-8") if page_bytes is not None else False,
        "coverage": [
            {"id": note["id"], "disposition": note["disposition"]}
            for note in list(record["declared_notes"]) + list(record["draft_notes"])
        ],
    }


def inspect_face(slot: Path, record: dict) -> dict:
    text = base.render(record).encode("utf-8")
    face = slot / "draft.md"
    if not face.is_file() or base.is_link(face):
        return {"status": "absent", "preserved": None, "history": False, "divergence": False}
    disk = face.read_bytes()
    if disk == text:
        return {"status": "matches-record", "preserved": None, "history": False, "divergence": False}
    disk_sha = base.digest(disk)
    if record.get("previous_face_sha256") and disk_sha == record.get("previous_face_sha256"):
        return {"status": "ordinary-history", "preserved": None, "history": True, "divergence": False}
    return {"status": "divergence", "preserved": None, "history": False, "divergence": True}


def classify_face(slot: Path, record: dict, operation: str) -> bytes:
    text = base.render(record).encode("utf-8")
    face = slot / "draft.md"
    previous = record.get("canonical_face_sha256")
    history = False
    divergence = False
    preserved = None
    if face.is_file() and not base.is_link(face):
        current = face.read_bytes()
        if current != text:
            current_sha = base.digest(current)
            if previous is not None and current_sha == previous:
                history = True
                name = f"draft.md.history-{operation}"
            else:
                divergence = True
                name = f"draft.md.divergence-{operation}"
            dest = slot / name
            if not dest.exists():
                dest.write_bytes(current)
            preserved = name
    record["previous_face_sha256"] = previous
    record["canonical_face_sha256"] = base.digest(text)
    record["derived_face"] = {
        "status": "divergence" if divergence else ("history" if history else "matches-record"),
        "preserved": preserved,
        "history": history,
        "divergence": divergence,
    }
    return text


def finish(slot, record, op_id, command, request, as_json, live, code=0, stop=None) -> int:
    pending = classify_face(slot, record, op_id) if code == 0 else None
    result = result_for(record, slot, command, live)
    if stop:
        result["stop"] = stop
    base.store_operation(record, op_id, command, request, code, result)
    base.commit_record(slot / "record.json", record, op_id)
    if pending is not None:
        partial = slot / f"draft.md.partial-{op_id}"
        partial.write_bytes(pending)
        os.replace(partial, slot / "draft.md")
    return base.emit(result, code, as_json)


def command_start(ctx: dict) -> int:
    work_dir = ctx["work_dir"]
    sources = base.measure_sources(ctx["book"], ctx["profile"])
    set_path, set_info = base.measure_set(ctx["profile"], ctx["book"], ctx["pins"])
    intent = parse_intent(ctx["input"], ctx["retained"]) if ctx["input"] is not None else base.empty_intent()
    with base.WorkLock(work_dir):
        found = base.find_operation(work_dir, ctx["profile_id"], ctx["op_id"])
        replay = base.replay_or_conflict(found, ctx["request"], "start", ctx["json"])
        if replay is not None:
            return replay
        if base.open_sessions(work_dir, ctx["profile_id"]):
            refuse("an open session already exists")
        dependency = base.collect_dependencies(ctx["code_root"], ctx["pins"], set_path, ctx["profile"], [])
        dependency["set"] = set_info
        pass_name, slot = base.reserve_pass(work_dir)
        template_pin = base.PINS["labs/pack-authoring-pass01/template/build-pack-v1.json"]
        record = {
            "schema": base.SCHEMA,
            "profile_id": ctx["profile_id"],
            "book": str(ctx["book"]),
            "pass": pass_name,
            "work_home": ctx["profile"]["work_home"],
            "state": "drafting",
            "stamp": "draft",
            "intent": intent,
            "declared_notes": base.declared_note_rows(sources),
            "draft_notes": [],
            "items": [],
            "revisions": [],
            "review": None,
            "review_history": [],
            "sources": sources,
            "template_schema": {
                "path": "labs/pack-authoring-pass01/template/build-pack-v1.json",
                "sha256": template_pin[0],
                "bytes": template_pin[1],
            },
            "form_binding": {
                "path": FORM_REL,
                "sha256": FORM_SHA,
                "bytes": FORM_BYTES,
                "form_id": DECLARATION["form_id"],
            },
            "canonical_face_sha256": None,
            "previous_face_sha256": None,
            "derived_face": {
                "status": "absent",
                "preserved": None,
                "history": False,
                "divergence": False,
            },
            "dependency": dependency,
            "return_intent": base.return_intent(work_dir),
            "operations": {},
        }
        return finish(slot, record, ctx["op_id"], "start", ctx["request"], ctx["json"], ctx["live"])


def command_revise(ctx: dict) -> int:
    with base.WorkLock(ctx["work_dir"]):
        found = base.find_operation(ctx["work_dir"], ctx["profile_id"], ctx["op_id"])
        replay = base.replay_or_conflict(found, ctx["request"], "revise", ctx["json"])
        if replay is not None:
            return replay
        slot, record = require_open(ctx)
        target = ctx["flags"]["target"]
        sources, set_info, dependency = base.refresh_current(
            ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record
        )
        if target == "intent":
            record["intent"] = parse_intent(ctx["input"], ctx["retained"])
            base.invalidate_review(record, "intent")
        elif target == "item":
            item_id = ctx["flags"]["item"]
            if not base.ITEM_RE.fullmatch(item_id):
                refuse("item id must be NN")
            current = next((item for item in record["items"] if item["id"] == item_id), None)
            if current is None:
                refuse("item is not in the draft")
            revised = parse_item(ctx["input"], ctx["retained"])
            check_note_refs(record, revised, ctx["retained"])
            record["revisions"].append({"id": item_id, "revision": current["revision"], "item": current})
            revised["id"] = item_id
            revised["revision"] = current["revision"] + 1
            record["items"] = [revised if item["id"] == item_id else item for item in record["items"]]
            base.invalidate_review(record, "item")
            _sources, set_info, dependency = base.refresh_current(
                ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record
            )
        elif target == "disposition":
            note_id = ctx["flags"]["note"]
            note = next(
                (item for item in record["declared_notes"] + record["draft_notes"] if item["id"] == note_id),
                None,
            )
            if note is None:
                refuse("note is not in the draft")
            context = {"item_ids": {item["id"] for item in record["items"]}}
            parsed = apply_form("disposition", ctx["input"], ctx["retained"], context)
            note["disposition"] = parsed["disposition"]
            note["why"] = parsed.get("why")
            note["integrated_item"] = parsed.get("item") if parsed["disposition"] == "integrated" else None
            base.invalidate_review(record, "disposition")
        else:
            refuse("unknown revise target")
        apply_source_drift(record, sources, set_info, dependency)
        return finish(slot, record, ctx["op_id"], "revise", ctx["request"], ctx["json"], ctx["live"])


def command_review(ctx: dict) -> int:
    with base.WorkLock(ctx["work_dir"]):
        found = base.find_operation(ctx["work_dir"], ctx["profile_id"], ctx["op_id"])
        replay = base.replay_or_conflict(found, ctx["request"], "review", ctx["json"])
        if replay is not None:
            return replay
        slot, record = require_open(ctx)
        expect = ctx["flags"].get("draft")
        if not expect:
            refuse("candidate identity is required")
        supplied = parse_review(ctx["input"], ctx["retained"])
        sources, set_info, dependency = base.refresh_current(
            ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record
        )
        drift = apply_source_drift(record, sources, set_info, dependency)
        if drift:
            return finish(slot, record, ctx["op_id"], "review", ctx["request"], ctx["json"], ctx["live"], 2, drift)
        candidate_sha = base.digest(base.render(record).encode("utf-8"))
        if expect != candidate_sha:
            refuse(f"stale candidate; retained input {ctx['retained']}. Help: {HELP}")
        template_sha = next(item["sha256"] for item in sources if item["role"] == "template")
        record["review"] = {
            "assessment": supplied["assessment"],
            "unresolved_issues": supplied["unresolved_issues"],
            "stop_conditions": supplied["stop_conditions"],
            "candidate_sha256": candidate_sha,
            "candidate_review": review_face(record["review"]),
            "final_sha256": "",
            "draft_sha256": "",
            "template_sha256": template_sha,
            "source_digest": base.source_digest(sources),
            "set_sha256": set_info["sha256"],
            "form_sha256": FORM_SHA,
            "reviewer_supplied": True,
        }
        final_sha = base.digest(base.render(record).encode("utf-8"))
        record["review"]["final_sha256"] = final_sha
        record["review"]["draft_sha256"] = final_sha
        return finish(slot, record, ctx["op_id"], "review", ctx["request"], ctx["json"], ctx["live"])


def command_inspect(ctx: dict) -> int:
    sessions = base.open_sessions(ctx["work_dir"], ctx["profile_id"])
    frozen = [
        (slot, record)
        for slot, record in base.iter_records(ctx["work_dir"])
        if record.get("profile_id") == ctx["profile_id"] and record.get("state") == "frozen"
    ]
    if len(sessions) == 1:
        slot, record = sessions[0]
    elif not sessions and len(frozen) == 1:
        slot, record = frozen[0]
    elif not sessions and not frozen:
        refuse("no open session")
    else:
        refuse("ambiguous session")
    sources, set_info, dependency = base.refresh_current(
        ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record
    )
    record = dict(record)
    record["derived_face"] = inspect_face(slot, record)
    result = result_for(record, slot, "inspect", ctx["live"])
    result["live"] = base.live_view(record, sources, set_info)
    result["live_dependency"] = {"queries": dependency["queries"], "item_refs": dependency["item_refs"]}
    review = record.get("review")
    recomputed = candidate_digest(record) if review else result["candidate_sha256"]
    result["candidate_recomputed"] = recomputed
    result["review_valid"] = bool(
        review
        and not result["live"]["source_drift"]
        and not result["live"]["set_drift"]
        and review.get("final_sha256") == result["final_sha256"]
        and review.get("candidate_sha256") == recomputed
        and review.get("form_sha256") == FORM_SHA
        and (record.get("form_binding") or {}).get("sha256") == FORM_SHA
    )
    return base.emit(result, 0, ctx["json"])


def command_freeze(ctx: dict) -> int:
    if ctx["live"] or base.on_live_tree(ctx["book"]):
        refuse("freeze on the live checkout is outside this slice")
    with base.WorkLock(ctx["work_dir"]):
        found = base.find_operation(ctx["work_dir"], ctx["profile_id"], ctx["op_id"])
        replay = base.replay_or_conflict(found, ctx["request"], "freeze", ctx["json"])
        if replay is not None:
            return replay
        slot, record = require_open(ctx)
        page = ctx["work_dir"] / f"{record['pass']}.md"
        partial_page = ctx["work_dir"] / f"{record['pass']}.md.partial"
        if page.exists() or partial_page.exists():
            refuse("pass page is occupied")
        sources, set_info, dependency = base.refresh_current(
            ctx["code_root"], ctx["pins"], ctx["book"], ctx["profile"], record
        )
        drift = apply_source_drift(record, sources, set_info, dependency)
        if drift:
            return finish(slot, record, ctx["op_id"], "freeze", ctx["request"], ctx["json"], False, 2, drift)
        if base.intent_missing(record):
            refuse("intent is incomplete")
        if not record["items"]:
            refuse("draft has no item")
        coverage = base.coverage_blocks(record)
        if coverage:
            refuse(coverage)
        blocked = base.blocking_dependency(record, set_info["sha256"])
        if blocked:
            refuse(blocked)
        if record["review"] is None:
            refuse("review is absent")
        final_sha = base.digest(base.render(record).encode("utf-8"))
        review = record["review"]
        if ctx["flags"]["draft"] != final_sha or review.get("final_sha256") != final_sha:
            refuse("final document identity does not match")
        if review.get("candidate_sha256") != candidate_digest(record):
            base.invalidate_review(record, "candidate")
            return finish(
                slot, record, ctx["op_id"], "freeze", ctx["request"], ctx["json"], False, 2, "changed review target"
            )
        template_sha = next(item["sha256"] for item in sources if item["role"] == "template")
        if (
            review.get("source_digest") != base.source_digest(sources)
            or review.get("set_sha256") != set_info["sha256"]
            or review.get("template_sha256") != template_sha
            or review.get("form_sha256") != FORM_SHA
        ):
            base.invalidate_review(record, "review-target")
            return finish(
                slot, record, ctx["op_id"], "freeze", ctx["request"], ctx["json"], False, 2, "changed review target"
            )
        manifest_path, _manifest = base.write_snapshot(slot, record, ctx["book"])
        code, report = base.run_checker(ctx["code_root"], ctx["pins"], manifest_path)
        matched = (
            code == 0
            and isinstance(report, dict)
            and report.get("entries")
            and all(item.get("result") == "match" for item in report["entries"])
        )
        if not matched:
            record["checker"] = {"exit": code, "report": report if isinstance(report, dict) else None}
            return finish(
                slot,
                record,
                ctx["op_id"],
                "freeze",
                ctx["request"],
                ctx["json"],
                False,
                2,
                "pack check did not match the measured snapshot",
            )
        base.exclusive_bytes(page, base.render(record).encode("utf-8"))
        record["state"] = "frozen"
        record["stamp"] = "prepared"
        record["checker"] = {
            "exit": code,
            "manifest": str(manifest_path),
            "label": "measured-file",
            "form": "working-tree",
        }
        return finish(slot, record, ctx["op_id"], "freeze", ctx["request"], ctx["json"], False)


def apply_source_drift(record, sources, set_info, dependency):
    reason = ORIGINAL_APPLY(record, sources, set_info, dependency)
    binding = record.get("form_binding") or {}
    if binding.get("sha256") != FORM_SHA:
        reason = reason or "changed form"
        base.invalidate_review(record, "form")
    return reason


def parse_call(args: list[str]):
    if not args:
        refuse("missing authoring command")
    command = args[0]
    commands = set(base.COMMANDS) | {"form"}
    if command not in commands:
        refuse("unknown authoring command")
    allowed = {
        "form": {"--book", "--profile", "--kind", "--json"},
        "start": {"--book", "--profile", "--operation", "--input", "--json"},
        "add-note": {"--book", "--profile", "--operation", "--input", "--json"},
        "add-item": {"--book", "--profile", "--operation", "--input", "--json"},
        "revise": {"--book", "--profile", "--operation", "--target", "--input", "--item", "--note", "--json"},
        "inspect": {"--book", "--profile", "--json"},
        "review": {"--book", "--profile", "--operation", "--input", "--draft-sha256", "--json"},
        "freeze": {"--book", "--profile", "--operation", "--draft-sha256", "--json"},
    }[command]
    values: dict[str, str] = {}
    as_json = False
    index = 1
    while index < len(args):
        token = args[index]
        if token in base.BANNED or any(token.startswith(prefix + "=") for prefix in base.BANNED):
            refuse("caller tool override is refused")
        if token == "--json":
            if as_json:
                refuse("repeated --json")
            as_json = True
            index += 1
            continue
        if not token.startswith("--"):
            refuse("unknown argument")
        if token not in allowed:
            refuse("unknown argument")
        key = token[2:]
        if key in values:
            refuse(f"repeated {token}")
        if index + 1 >= len(args) or args[index + 1].startswith("--"):
            refuse(f"missing value for {token}")
        values[key] = args[index + 1]
        index += 2
    for name in ("book", "profile"):
        if name not in values:
            refuse(f"missing --{name}")
    if command not in ("inspect", "form") and "operation" not in values:
        refuse("missing --operation")
    if command in ("add-note", "add-item", "revise", "review") and "input" not in values:
        refuse("missing --input")
    if command == "revise" and "target" not in values:
        refuse("missing --target")
    if command == "revise" and values["target"] == "item" and "item" not in values:
        refuse("missing --item")
    if command == "revise" and values["target"] == "disposition" and "note" not in values:
        refuse("missing --note")
    if command == "review" and "draft-sha256" not in values:
        refuse("candidate identity is required")
    if command == "freeze" and "draft-sha256" not in values:
        refuse("missing --draft-sha256")
    if "draft-sha256" in values and not base.HEX_RE.fullmatch(values["draft-sha256"]):
        refuse("draft sha256 must be 64 lowercase hex")
    if "operation" in values and not base.OP_RE.fullmatch(values["operation"]):
        refuse("operation id is not a label")
    renamed = dict(values)
    if "draft-sha256" in renamed:
        renamed["draft"] = renamed.pop("draft-sha256")
    return command, renamed, as_json


def perform(args: list[str], code_root: Path, replace=os.replace) -> int:
    command, flags, as_json = parse_call(args)
    pins = base.load_pins(code_root)
    profile = base.load_profile(pins, flags["profile"])
    book = base.book_root(flags["book"], profile["book_policy"])
    if command == "freeze" and (base.on_live_tree(book) or base.inside(book, base.CHECKOUT)):
        refuse("freeze on the live checkout is outside this slice")
    work_dir = base.walk_book(book, profile["work_home"], "dir")
    retained = flags.get("input", "")
    document, raw = base.load_input(flags.get("input"))
    if command in ("add-note", "add-item", "revise", "review") and document is None:
        refuse("missing --input")
    op_id = flags.get("operation", "")
    request = base.request_sha(command, flags, raw) if command not in ("inspect", "form") else ""
    ctx = {
        "code_root": code_root,
        "pins": pins,
        "profile": profile,
        "profile_id": flags["profile"],
        "book": book,
        "work_dir": work_dir,
        "live": base.on_live_tree(book),
        "json": as_json,
        "op_id": op_id,
        "request": request,
        "input": document,
        "retained": retained,
        "flags": flags,
        "replace": replace,
    }
    if command == "form":
        return command_form(ctx)
    if command == "inspect":
        return command_inspect(ctx)
    if command == "start":
        return command_start(ctx)
    if command == "add-note":
        return base.command_add_note(ctx)
    if command == "add-item":
        return base.command_add_item(ctx)
    if command == "revise":
        return command_revise(ctx)
    if command == "review":
        return command_review(ctx)
    if command == "freeze":
        return command_freeze(ctx)
    refuse("unknown authoring command")
    return 2


def install() -> None:
    global ORIGINAL_REQUIRE, ORIGINAL_APPLY
    ORIGINAL_REQUIRE = base.require_open
    ORIGINAL_APPLY = base.apply_source_drift
    base.HELP = HELP
    base.parse_intent = parse_intent
    base.parse_item = parse_item
    base.parse_note = parse_note
    base.parse_review = parse_review
    base.check_note_refs = check_note_refs
    base.require_open = require_open
    base.finish = finish
    base.result_for = result_for
    base.next_step = next_step
    base.command_start = command_start
    base.command_revise = command_revise
    base.command_review = command_review
    base.command_inspect = command_inspect
    base.command_freeze = command_freeze
    base.apply_source_drift = apply_source_drift


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace", newline="\n")
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args, Path(__file__).resolve().parents[2])
    except base.Refuse as exc:
        print(f"stop: {exc}", file=sys.stderr)
        return 2
    except base.Partial as exc:
        print(f"partial: {exc}", file=sys.stderr)
        return 4


base = load_base()
DECLARATION = load_declaration()
install()


if __name__ == "__main__":
    sys.exit(main())
