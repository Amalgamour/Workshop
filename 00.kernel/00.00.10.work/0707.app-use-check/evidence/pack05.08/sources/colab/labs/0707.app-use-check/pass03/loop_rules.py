#!/usr/bin/env python3
"""0707/05.03 pass03: NONPRODUCTION prototype of the remaining loop rules.

Pure functions over already-read bytes and parsed tool outputs. Not the loop.
  supplied_state_of   build supplied-review-state/1 from the committed cycle decision
  envelope_v2         review-construction/2 from a /1 envelope plus that state
  verify_committed    before render/recover: hash-verified record vs envelope (U1)
  mechanical          mechanical next, separate from supplied text (U2)
"""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy

SUPPLIED_SCHEMA = "supplied-review-state/1"
SUPPLIED_SOURCE = "cycle decision judgment"


class Refuse(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def need(cond: bool, code: str, detail: str) -> None:
    if not cond:
        raise Refuse(code, detail)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def supplied_state_of(decision: dict) -> dict:
    j = decision["judgment"]
    return {"schema": SUPPLIED_SCHEMA, "source": SUPPLIED_SOURCE, "disposition": j["disposition"],
            "pass_terminal": j["pass_terminal"], "goal_terminal": j["goal"]["terminal"], "outcome": j["outcome"]}


def envelope_v2(envelope_v1: dict, decision: dict) -> dict:
    need(envelope_v1.get("schema") == "review-construction/1", "envelope", "input is not a /1 envelope")
    e = deepcopy(envelope_v1)
    e["schema"] = "review-construction/2"
    e["supplied_review_state"] = supplied_state_of(decision)
    return e


def verify_committed(record_bytes: bytes, committed: dict, latest: dict, envelope: dict, reg: dict) -> dict:
    """All checks run before any constructor apply. Each failure is a distinct refusal; nothing is written."""
    digest = sha(record_bytes)
    need(isinstance(committed, dict) and committed.get("record_sha256") == digest, "record-hash", "record.json does not hash to COMMITTED.json")
    need(isinstance(latest, dict) and latest.get("record_sha256") == digest, "record-hash", "record.json is not the record the cycle read names")
    record = json.loads(record_bytes.decode("utf-8"))
    decision = record.get("decision") or {}
    expected_id = f"{reg['pass']}-{reg['review_identity']}"
    need(envelope.get("review_identity") == reg["review_identity"], "review-identity", "envelope review_identity differs from the registration")
    need(record.get("review_id") == decision.get("review_id") == latest.get("review_id") == expected_id, "review-identity",
         f"record, decision and cycle read do not all name {expected_id}")
    need((decision.get("binding") or {}).get("task_binding_sha256") == latest.get("task_binding_sha256"), "binding",
         "committed decision binding differs from the cycle read's task binding")
    need(envelope.get("record") == decision.get("supplied_record"), "envelope-record", "envelope record is not the committed supplied record")
    need((envelope.get("target"), envelope.get("pass")) == (reg["target"], reg["pass"]), "envelope-target", "envelope target or pass differs from the registration")
    schema = envelope.get("schema")
    if schema == "review-construction/2":
        need(envelope.get("supplied_review_state") == supplied_state_of(decision), "supplied-state",
             "envelope supplied_review_state differs from the hash-verified committed decision")
        state = "verified-against-committed-record"
    else:
        need(schema == "review-construction/1", "envelope", "unknown envelope schema")
        state = "legacy-/1-envelope: no supplied state is rendered"
    return {"record_sha256": digest, "review_id": expected_id, "supplied_state": state,
            "not_established": ["Director acceptance", "release", "authenticated identity"]}


ROUTES = {
    "record": "Supply the typed judgment, then record.",
    "record-then-blocked": "Recording preserves the judgment; rendering into this target will be refused.",
    "recover": "Run recover: it retries rendering the same committed review into the unchanged target.",
    "read": "Read the rendered review.",
    "none-in-this-entry": "No mechanical route in this entry; the committed judgment is kept.",
}


def mechanical(view: dict, inspection: dict | None, record_check: Refuse | None = None) -> dict:
    """Pure function of the cycle view, the read-only inspection and the record check. Never reads supplied text."""
    pass_state = view.get("pass_state")
    render_state = view.get("render_state")
    latest = view.get("latest_review") or {}
    current = (view.get("write_token") or {}).get("sha256")
    recorded = (latest.get("write_token") or {}).get("sha256")
    target = (inspection or {}).get("state")

    def out(state, route, blocker=None, extra=None):
        body = {"state": state, "blocker": blocker, "route": route, "text": ROUTES.get(route, ""), "target": target}
        if extra:
            body.update(extra)
        return body

    if record_check is not None:
        return out("committed-record-mismatch", "none-in-this-entry", record_check.code, {"detail": record_check.detail})
    if pass_state == "awaiting-review":
        if target == "pending":
            return out("awaiting-review", "record")
        if target in ("existing-review", "unsupported", "constructed-same-binding"):
            return out("awaiting-review", "record-then-blocked", f"target-{target}")
        if target == "absent":
            return out("awaiting-review", "none-in-this-entry", "target-absent",
                       {"detail": "record hashes the target and refuses when it is absent (review_loop.py 337)"})
        return out("unknown-state", "none-in-this-entry", "target-not-inspected")
    if render_state == "conflict":
        return out("existing-review-conflict", "none-in-this-entry", "existing-review")
    if render_state == "pending":
        if current is not None and current == recorded:
            if target == "pending":
                return out("render-interrupted", "recover")
            if target in ("existing-review", "unsupported"):
                return out("render-blocked", "none-in-this-entry", f"target-{target}",
                           {"detail": "the judgment is committed (B8); render would refuse and keep one partial"})
            return out("unknown-state", "none-in-this-entry", f"unchanged target classified {target}")
        if target == "constructed-same-binding" and (inspection or {}).get("binding_sha256") == latest.get("task_binding_sha256"):
            return out("rendered-marker-missing", "none-in-this-entry", "page-holds-this-binding",
                       {"detail": "recover refuses 'write token changed since read' (v2 test T7); a successor must confirm byte equality"})
        return out("target-changed-since-record", "none-in-this-entry", "write-token-changed")
    if pass_state == "reviewed" and render_state == "rendered":
        return out("rendered", "read")
    return out("unknown-state", "none-in-this-entry", f"pass {pass_state} render {render_state}")
