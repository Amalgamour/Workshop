#!/usr/bin/env python3
"""0707 pass01: fill the prepare template with the SUPPLIED sample judgment.

Pure function of: the prepare template (from the app's stdout), the supplied
judgment file, the registration and the measured bytes in the disposable book.
Writes nothing itself; walk.py writes decision.json into the book.

PROVENANCE says where the operator learned each shape: the template, the
written docs, or code (pilot.py build_decision / prime_cycle.py check_judgment).
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

PROVENANCE = {
    "decision top-level keys": "template (prime-cycle-decision/3 offered by prepare)",
    "attribution {actor_label, role, evidence}": "template keys; values from PILOT supplied-judgment.json example",
    "judgment keys incl. 24 sections": "template",
    "judgment.outcome values": "code: prime_cycle.py check_judgment",
    "judgment.disposition values": "code: prime_cycle.py check_judgment",
    "judgment.pass_terminal / goal.terminal values and their coupling": "code: prime_cycle.py check_judgment",
    "judgment.next_action {action_id, text, authorized_in_grant}": "code: pilot.py build_decision; prime_cycle.py check_judgment",
    "judgment.source_refs content": "code: pilot.py build_decision (['assignment.txt'])",
    "supplied_record schema prime-review-record/1 and keys": "code: pilot.py build_decision",
    "supplied_record.sources rows (bind, content/transport hashes, record text, identity)": "code: pilot.py source_row",
    "capture identity {schema, member=derived line, submission_id, receipt_sha256, origin}": "code: pilot.py build_decision; PILOT.md names the derived member only",
    "supplied_record.judgment mirrors judgment (next_action as text)": "code: prime_cycle.py align_supplied",
    "supplied_record.agreement == registration.agreement": "code: pilot.py; prime_cycle.py align_supplied",
}
SOURCE_ROW_KEYS = "bind content_bytes content_sha256 identity kind logical_path prior_content_sha256 prior_transport_sha256 record transport_bytes transport_sha256"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_row(path: str, data: bytes, kind: str, identity: dict) -> dict:
    digest = sha(data)
    return {
        "bind": False,
        "content_bytes": len(data),
        "content_sha256": digest,
        "identity": identity,
        "kind": kind,
        "logical_path": path,
        "prior_content_sha256": None,
        "prior_transport_sha256": None,
        "record": data.decode("utf-8"),
        "transport_bytes": len(data),
        "transport_sha256": digest,
    }


def build(book: Path, template: dict, words: dict) -> dict:
    registration = json.loads((book / "registration.json").read_text(encoding="utf-8"))
    descriptor = json.loads((book / "descriptor.json").read_text(encoding="utf-8"))
    rj = words["record_judgment"]
    sections = {key: None for key in template["judgment"]["sections"]}
    for key, value in rj["sections_text"].items():
        if key not in sections:
            raise ValueError(f"section {key} is not offered by the template")
        sections[key] = value
    goal = template["judgment"]["goal"]
    judgment = deepcopy(template["judgment"])
    judgment.update({
        "outcome": rj["outcome"],
        "disposition": rj["disposition"],
        "pass_terminal": "open",
        "goal": {"terminal": "open", "goal_id": goal["goal_id"], "goal_sha256": goal["goal_sha256"], "evidence": []},
        "finding": rj["finding"],
        "reasons": list(rj["reasons"]),
        "source_refs": [registration["assignment_path"]],
        "next_action": {"action_id": rj["next_action_id"], "text": rj["next_action"], "authorized_in_grant": False},
        "unresolved": [],
        "semantic_conflict": rj["semantic_conflict"],
        "design_fork": rj["design_fork"],
        "holds": [],
        "answers": [],
        "sections": sections,
    })
    record_judgment = {
        "outcome": rj["outcome"],
        "finding": rj["finding"],
        "reasons": list(rj["reasons"]),
        "semantic_conflict": rj["semantic_conflict"],
        "design_fork": rj["design_fork"],
        "next_action": rj["next_action"],
        "sections": sections,
    }
    receipt = (book / descriptor["receipt_path"]).read_bytes()
    origin = descriptor["origin"]
    sources = [source_row(registration["assignment_path"], (book / registration["assignment_path"]).read_bytes(), "page", {"schema": "page-bytes/1"})]
    for item in registration["evidence"]:
        sources.append(source_row(item["logical_path"], (book / item["logical_path"]).read_bytes(), "supplied-text",
                                  {"schema": "supplied-text/1", "label": "SUPPLIED"}))
    sources.append(source_row(descriptor["return_path"], (book / descriptor["return_path"]).read_bytes(), "capture", {
        "schema": "return-capture/1",
        "member": descriptor["placement"]["intended_target_page"],
        "submission_id": descriptor["submission_id"],
        "receipt_sha256": sha(receipt),
        "origin": {"book": origin["book"], "page": origin["page"], "batch": origin["batch"]},
    }))
    record = {
        "schema": "prime-review-record/1",
        "attribution": words["attribution"],
        "sources": sources,
        "agreement": registration["agreement"],
        "holds": [],
        "answers": [],
        "review_passes": [],
        "gaps": [],
        "judgment": record_judgment,
    }
    decision = deepcopy(template)
    decision["attribution"] = words["attribution"]
    decision["judgment"] = judgment
    decision["supplied_record"] = record
    return decision
