#!/usr/bin/env python3
"""0510/05.06 pass02: NONPRODUCTION prototype of the corrected reserved-review rules.

Pure functions. No file, Git, process or model access. Successor of the sealed
pass01 reserved_rules.py (unchanged). Differences, by Prime finding:
  C01 page-local custody: no N1NN member; the first return is the page's own
      05.NN.return.md, sealed by a proposed workflow transition (workflow_model.py).
  C02 four separate facts: return bytes, seal transition, recorded order, declared
      exposure. Hash dependency is reported as dependency, never as chronology.
  C03 newline-aware parse view; raw bytes hashed as received.
  C04 launch requires BOTH full producer verify (intact, expected digest) and the
      standalone handoff check (valid, same digest); each covers what the other does not.
  C05 the caller states the expected mode; reserved without a descriptor refuses.
"""

from __future__ import annotations

import hashlib
import json
import re

DESCRIPTOR_SCHEMA = "reserved-review/2"
FINDINGS_SCHEMA = "reserved-findings/1"
RECON_SCHEMA = "reserved-reconciliation/1"
PRODUCER_REPORT = "colab-support-report/2"
TRIGGERS = ("stuck", "pre-release-testing")
SESSIONS = ("new", "continuing", "unknown")
STATUSES = ("confirmed", "withdrawn", "different-conditions", "unresolved", "out-of-scope")
NEEDS_REASON = ("withdrawn", "different-conditions", "out-of-scope", "unresolved")
MODES = ("ordinary", "reserved")
FINDING_ID = re.compile(r"^R[0-9]{2}$")
UNIQUE_ID = re.compile(r"^U[0-9]{2}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
PASS_RE = re.compile(r"^05\.(0[1-9]|[1-9][0-9])$")
DESCRIPTOR_KEYS = {
    "schema", "investigation", "stage", "first_pass", "first_return", "trigger", "question",
    "artifact_cut", "environment", "requirements", "authority_limits", "builder_context",
    "unavailable", "reviewer_assignment", "builder_identity",
}
FIRST_RETURN_KEYS = {"pass", "return_sha256", "return_bytes", "package_digest", "seal_seq", "seal_transition_sha256"}


class Problem(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def need(cond: bool, code: str, detail: str) -> None:
    if not cond:
        raise Problem(code, detail)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


# ---------------------------------------------------------------- typed accessors (no TypeError escapes)
def obj(value, where: str, keys: set[str] | None = None) -> dict:
    need(isinstance(value, dict), "type", f"{where} is not an object")
    if keys is not None:
        need(set(value) == keys, "keys", f"{where} keys are not the declared set")
    return value


def text(value, where: str, allow_empty: bool = False) -> str:
    need(isinstance(value, str), "type", f"{where} is not text")
    need(allow_empty or value.strip() != "", "empty", f"{where} is empty")
    return value


def enum(value, choices, where: str) -> str:
    need(isinstance(value, str) and value in choices, "enum", f"{where} is not one of {', '.join(choices)}")
    return value


def hex64(value, where: str) -> str:
    need(isinstance(value, str) and HEX64.fullmatch(value) is not None, "hash", f"{where} is not a sha256")
    return value


def items(value, where: str) -> list:
    need(isinstance(value, list), "type", f"{where} is not a list")
    return value


def count(value, where: str) -> int:
    need(isinstance(value, int) and not isinstance(value, bool) and value >= 0, "type", f"{where} is not a count")
    return value


# ---------------------------------------------------------------- C03 parse view
def parse_view(raw: bytes) -> tuple[str, dict]:
    """Return (text for parsing, facts). The raw bytes are only hashed, never altered."""
    need(isinstance(raw, (bytes, bytearray)), "type", "return is not bytes")
    try:
        decoded = bytes(raw).decode("utf-8")
    except UnicodeDecodeError:
        raise Problem("encoding", "return is not UTF-8") from None
    bom = decoded.startswith("﻿")
    if bom:
        decoded = decoded[1:]
    crlf = decoded.count("\r\n")
    need("\r" not in decoded.replace("\r\n", ""), "line-endings", "return has a carriage return that is not part of CRLF")
    view = decoded.replace("\r\n", "\n")
    facts = {"raw_sha256": sha(bytes(raw)), "raw_bytes": len(raw), "bom": bom, "crlf_lines": crlf,
             "lf_only_lines": view.count("\n") - crlf}
    return view, facts


def strict_json(text_: str, where: str):
    def pairs_hook(pairs):
        keys = [k for k, _ in pairs]
        need(len(keys) == len(set(keys)), "json", f"{where} repeats a key")
        return dict(pairs)

    def constant(name):
        raise Problem("json", f"{where} has non-finite number {name}")

    try:
        return json.loads(text_, object_pairs_hook=pairs_hook, parse_constant=constant)
    except json.JSONDecodeError:
        raise Problem("json", f"{where} is not strict JSON") from None


def block(raw: bytes, name: str, where: str) -> tuple[dict, dict]:
    view, facts = parse_view(raw)
    found = re.findall(r"(?ms)^```" + re.escape(name) + r"[ \t]*\n(.*?)^```[ \t]*$", view)
    need(len(found) != 0, f"missing-{name}", f"{where} has no ```{name}``` block")
    need(len(found) == 1, f"duplicate-{name}", f"{where} has more than one ```{name}``` block")
    return obj(strict_json(found[0], f"{where} {name} block"), f"{where} {name} block"), facts


# ---------------------------------------------------------------- C04 verifier boundary
def verified_package(producer_report, handoff_result, expected_digest: str) -> dict:
    """Both verifiers must agree on the same expected digest; return the trusted claims."""
    hex64(expected_digest, "expected digest")
    rep = obj(producer_report, "producer verify report")
    need(rep.get("schema") == PRODUCER_REPORT and rep.get("command") == "verify", "producer-not-verified", "not a colab-support-report/2 verify output")
    need(rep.get("result") == "intact" and rep.get("findings") == [], "producer-not-intact", f"producer verify result is {rep.get('result')!r}")
    need(rep.get("digest") == expected_digest, "digest", "producer verify digest differs from the expected digest")
    hc = obj(handoff_result, "handoff check output")
    need(hc.get("result") == "valid" and isinstance(hc.get("trusted"), dict), "handoff-not-valid", f"handoff check result is {hc.get('result')!r}")
    trusted = hc["trusted"]
    need(trusted.get("digest") == expected_digest, "digest", "handoff trusted digest differs from the expected digest")
    need(trusted.get("investigation") == rep.get("investigation"), "identity-split", "the two verifiers name different investigations")
    items(trusted.get("source_map"), "trusted.source_map")
    return trusted


# ---------------------------------------------------------------- descriptor
def validate_descriptor(d) -> dict:
    obj(d, "descriptor", DESCRIPTOR_KEYS)
    need(d["schema"] == DESCRIPTOR_SCHEMA, "version", "descriptor schema is not reserved-review/2")
    inv = obj(d["investigation"], "descriptor.investigation", {"book", "page", "pass"})
    text(inv["book"], "investigation.book"), text(inv["page"], "investigation.page")
    need(isinstance(inv["pass"], str) and PASS_RE.fullmatch(inv["pass"]) is not None, "pass", "investigation.pass is not 05.NN")
    enum(d["stage"], ("independent", "informed"), "stage")
    t = obj(d["trigger"], "trigger")
    need(t.get("kind") in TRIGGERS if isinstance(t.get("kind"), str) else False, "no-trigger", "trigger kind must be stuck or pre-release-testing")
    need(isinstance(t.get("named_by"), str) and t["named_by"].strip() != "", "no-trigger", "trigger names no one")
    need(isinstance(t.get("statement"), str) and t["statement"].strip() != "", "no-trigger", "trigger statement is empty")
    text(d["question"], "question")
    cut = d["artifact_cut"]
    need(isinstance(cut, dict) and isinstance(cut.get("commit"), str) and cut["commit"] != "", "launch-unready", "artifact cut or commit was not supplied")
    for i, tgt in enumerate(items(cut.get("targets"), "artifact_cut.targets") or [None]):
        need(isinstance(tgt, dict) and isinstance(tgt.get("sha256"), str) and HEX64.fullmatch(tgt["sha256"]) is not None
             and isinstance(tgt.get("bytes"), int), "launch-unready", f"artifact cut target {i} hash or length was not supplied")
        text(tgt.get("id"), f"target {i} id"), text(tgt.get("path"), f"target {i} path")
    obj(d["environment"], "environment")
    need(isinstance(d["requirements"], list) and len(d["requirements"]) >= 1, "requirement-missing",
         "a reserved review names at least one requirement source")
    for key in ("requirements", "authority_limits", "builder_context", "unavailable"):
        for i, row in enumerate(items(d[key], key)):
            obj(row, f"{key}[{i}]")
            if key != "unavailable":
                text(row.get("path"), f"{key}[{i}].path"), hex64(row.get("sha256"), f"{key}[{i}].sha256")
    ra = obj(d["reviewer_assignment"], "reviewer_assignment", {"model", "family", "session", "prior_involvement"})
    enum(ra["session"], SESSIONS, "reviewer_assignment.session")
    for key in ("model", "family", "prior_involvement"):
        text(ra[key], f"reviewer_assignment.{key} (text or 'unknown')")
    bi = obj(d["builder_identity"], "builder_identity", {"model", "family"})
    text(bi["model"], "builder_identity.model"), text(bi["family"], "builder_identity.family")
    if d["stage"] == "independent":
        need(d["first_pass"] is None and d["first_return"] is None, "stage-order", "an independent stage names no first pass")
    else:
        need(isinstance(d["first_pass"], str) and PASS_RE.fullmatch(d["first_pass"]) is not None, "stage-order", "informed stage must name first_pass 05.NN")
        fr = obj(d["first_return"], "first_return", FIRST_RETURN_KEYS)
        need(fr["pass"] == d["first_pass"], "stage-order", "first_return.pass differs from first_pass")
        hex64(fr["return_sha256"], "first_return.return_sha256"), hex64(fr["package_digest"], "first_return.package_digest")
        hex64(fr["seal_transition_sha256"], "first_return.seal_transition_sha256")
        count(fr["return_bytes"], "first_return.return_bytes"), count(fr["seal_seq"], "first_return.seal_seq")
    return d


def find_descriptor(trusted: dict, desk: str = "00.kernel"):
    inv = trusted["investigation"]
    nn = inv["pass"].split(".")[1]
    path = f"{desk}/{inv['book']}/{inv['page']}/evidence/reserved05.{nn}.json"
    rows = [r for r in trusted["source_map"] if isinstance(r, dict) and r.get("source_path") == path]
    need(len(rows) <= 1, "descriptor", "the descriptor path appears more than once")
    if rows:
        need(rows[0].get("role") == "required", "descriptor", "the descriptor must be a required source")
    return rows[0] if rows else None, path


def cut_rows(cut: dict) -> list[tuple]:
    return sorted((t["id"], t["path"], t["sha256"], t["bytes"]) for t in cut["targets"])


# ---------------------------------------------------------------- C05 + launch (independent stage)
def launch(expect: str, trusted: dict, request: dict, binding: dict, descriptor_bytes: bytes | None) -> dict:
    enum(expect, MODES, "expected mode")
    if descriptor_bytes is None:
        need(expect == "ordinary", "reserved-expected-missing-descriptor",
             "the caller asked for reserved mode but the verified packet carries no descriptor")
        return {"result": "ordinary-confirmed", "checked": "no reserved rules apply"}
    need(expect == "reserved", "descriptor-in-ordinary-job", "the packet carries a reserved descriptor but the caller expected ordinary")
    d = validate_descriptor(strict_json(parse_view(descriptor_bytes)[0], "descriptor"))
    need(d["stage"] == "independent", "stage-order", "launch is for the independent stage; use stage for the informed stage")
    inv = trusted["investigation"]
    need(d["investigation"] == inv, "identity", "descriptor investigation differs from the verified packet")
    cut = d["artifact_cut"]
    tb = obj(binding, "binding")
    commits = {t["source"]["commit"] for t in items(tb.get("targets"), "binding.targets")}
    need(commits == {cut["commit"]}, "cut-mismatch", "descriptor commit differs from the packet binding")
    packaged = sorted((r["targets"][0], r["source_path"], r["sha256"], r["bytes"]) for r in trusted["source_map"] if r.get("role") == "target")
    need(cut_rows(cut) == packaged, "cut-mismatch", "descriptor targets differ from the packaged targets")
    present = {(r["source_path"], r["sha256"]) for r in trusted["source_map"]}
    paths = {r["source_path"] for r in trusted["source_map"]}
    shas = {r["sha256"] for r in trusted["source_map"]}
    for row in d["requirements"]:
        need((row["path"], row["sha256"]) in present, "requirement-missing", f"requirement {row['path']} is not in the packet")
    for row in d["authority_limits"]:
        need((row["path"], row["sha256"]) in present, "authority-missing", f"authority limit {row['path']} is not in the packet")
    withheld = {w.get("item") for w in items(obj(request, "request").get("withheld"), "request.withheld") if isinstance(w, dict)}
    for row in d["builder_context"]:
        need(row["path"] not in paths and row["sha256"] not in shas, "context-in-first-packet", f"declared builder context {row['path']} is in the first packet")
        need(row["path"] in withheld, "withhold-undeclared", f"builder context {row['path']} is not declared as withheld to the reviewer")
    ra = d["reviewer_assignment"]
    need(ra["session"] != "continuing", "not-fresh", "a continuing session cannot be the independent first pass")
    return {
        "result": "reserved-launch-ready-as-declared",
        "first_pass_label": "independent-fresh-declared" if ra["session"] == "new" else "independent-freshness-unknown",
        "same_family_declared": "unknown" if "unknown" in (ra["family"], d["builder_identity"]["family"]) else str(ra["family"] == d["builder_identity"]["family"]).lower(),
        "verified": ["producer verify intact at the expected digest", "handoff check valid at the same digest",
                     "declared builder context absent by path and bytes", "requirements and authority limits present", "cut bound"],
        "declared_only": ["reviewer session freshness, model and family", "that no undeclared context reached the reviewer"],
    }


# ---------------------------------------------------------------- C01/C02 transition chain (page-local record)
def verify_chain(transitions) -> list[dict]:
    prev = None
    for i, t in enumerate(items(transitions, "transitions")):
        obj(t, f"transition {i + 1}")
        need(t.get("seq") == i + 1, "chain", f"transition {i + 1} has seq {t.get('seq')!r}")
        need(t.get("prev") == prev, "chain", f"transition {i + 1} does not chain to its predecessor")
        body = {k: v for k, v in t.items() if k != "sha256"}
        need(t.get("sha256") == sha(canonical(body)), "chain", f"transition {i + 1} hash does not match its content")
        prev = t["sha256"]
    return transitions


def first(transitions: list[dict], action: str, pass_id: str):
    hits = [t for t in transitions if t.get("action") == action and t.get("pass") == pass_id]
    return hits[0] if len(hits) == 1 else (None if not hits else Problem("chain", f"{action} {pass_id} recorded twice"))


def stage(descriptor_bytes: bytes, first_descriptor_bytes: bytes, trusted2: dict, transitions, first_return_raw: bytes, expect: str = "reserved") -> dict:
    """Informed stage, before attaching pass 2. Every failure blocks that attach."""
    enum(expect, MODES, "expected mode")
    need(expect == "reserved", "descriptor-in-ordinary-job", "stage is a reserved-mode check")
    d2 = validate_descriptor(strict_json(parse_view(descriptor_bytes)[0], "descriptor"))
    d1 = validate_descriptor(strict_json(parse_view(first_descriptor_bytes)[0], "first descriptor"))
    need(d2["stage"] == "informed" and d1["stage"] == "independent", "stage-order", "need an independent first and an informed second descriptor")
    i1, i2 = d1["investigation"], d2["investigation"]
    need((i1["book"], i1["page"]) == (i2["book"], i2["page"]), "identity", "both stages must be one N7NN page")
    need(d2["first_pass"] == i1["pass"] and i2["pass"] > i1["pass"], "stage-order", "the informed pass must follow the named first pass")
    need(trusted2["investigation"] == i2, "identity", "informed descriptor differs from its verified packet")
    chain = verify_chain(transitions)
    fr = d2["first_return"]
    attach1 = first(chain, "attach", i1["pass"])
    seal1 = first(chain, "seal-return", i1["pass"])
    review1 = first(chain, "review", i1["pass"])
    openp2 = first(chain, "open-pass", i2["pass"])
    for t in (attach1, seal1, review1, openp2):
        if isinstance(t, Problem):
            raise t
    need(attach1 is not None and attach1.get("digest") == fr["package_digest"], "first-packet", "first packet digest is not the one recorded at attach")
    need(seal1 is not None, "first-not-sealed", "no page-local seal transition for the first return")
    need(seal1["seq"] == fr["seal_seq"] and seal1["sha256"] == fr["seal_transition_sha256"], "first-not-sealed", "descriptor names a different seal transition")
    need(seal1.get("return_sha256") == fr["return_sha256"] == sha(first_return_raw) and seal1.get("return_bytes") == len(first_return_raw),
         "first-not-sealed", "first return bytes differ from the sealed bytes")
    block(first_return_raw, "reserved-findings", "first return")
    need(review1 is not None and review1.get("route") == "request-next" and review1.get("next_pass") == i2["pass"], "stage-order",
         "the first review does not request this informed pass")
    need(openp2 is not None, "stage-order", "the informed pass slot was not opened after the first review")
    need(attach1["seq"] < seal1["seq"] < review1["seq"] < openp2["seq"], "stage-order", "recorded transitions are out of order")
    need(first(chain, "attach", i2["pass"]) is None, "stage-order", "the informed packet is already attached; check before attach")
    shas2 = {r["sha256"] for r in trusted2["source_map"]}
    need(fr["return_sha256"] in shas2, "dependency", "the informed packet does not carry the sealed first return bytes")
    need(cut_rows(d1["artifact_cut"]) == cut_rows(d2["artifact_cut"]) and d1["artifact_cut"]["commit"] == d2["artifact_cut"]["commit"],
         "target-changed", "artifact cut changed: a new comparison, not the same frozen observation")
    present = {(r["source_path"], r["sha256"]) for r in trusted2["source_map"]}
    return {
        "result": "informed-launch-ready-as-declared",
        "verified": {
            "return_identity": fr["return_sha256"],
            "seal_identity": {"seq": seal1["seq"], "transition_sha256": seal1["sha256"]},
            "recorded_order": [attach1["seq"], seal1["seq"], review1["seq"], openp2["seq"]],
            "dependency": "the informed packet carries the sealed first-return bytes and a descriptor naming the seal transition",
        },
        "not_proved": ["wall-clock time of sealing or preparation", "when any person or model saw builder context",
                       "that the transition record was not rewritten wholesale outside the tool (Git history is the durable anchor)"],
        "declared_exposure": {"first": d1["reviewer_assignment"], "second": d2["reviewer_assignment"]},
        "builder_context_not_supplied": [r["path"] for r in d2["builder_context"] if (r["path"], r["sha256"]) not in present],
        "condition_differences": sorted(k for k in set(d1["environment"]) | set(d2["environment"]) if d1["environment"].get(k) != d2["environment"].get(k)),
        "reviewer_assignment_changed": [k for k in ("model", "family", "session") if d1["reviewer_assignment"][k] != d2["reviewer_assignment"][k]],
    }


# ---------------------------------------------------------------- reconcile (unresolved and unique stay visible)
def reconcile(first_return_raw: bytes, second_return_raw: bytes) -> dict:
    f1, facts1 = block(first_return_raw, "reserved-findings", "first return")
    need(f1.get("schema") == FINDINGS_SCHEMA and f1.get("stage") == "independent", "version", "findings block is not reserved-findings/1 independent")
    ids = []
    for i, f in enumerate(items(f1.get("findings"), "findings")):
        obj(f, f"finding {i}")
        need(isinstance(f.get("id"), str) and FINDING_ID.fullmatch(f["id"]) is not None, "findings", f"finding {i} id is not R01..R99")
        need(f["id"] not in ids, "findings", f"finding id {f['id']} repeats")
        text(f.get("claim"), f"finding {f['id']} claim")
        ids.append(f["id"])
    r2, facts2 = block(second_return_raw, "reserved-reconciliation", "second return")
    need(r2.get("schema") == RECON_SCHEMA and r2.get("stage") == "informed", "version", "reconciliation block is not reserved-reconciliation/1 informed")
    seen: dict[str, dict] = {}
    for i, item in enumerate(items(r2.get("dispositions"), "dispositions")):
        obj(item, f"disposition {i}")
        fid = item.get("finding")
        need(isinstance(fid, str), "type", f"disposition {i} finding is not text")
        need(fid in ids, "unknown-finding", f"disposition names {fid}, which is not a first-pass finding")
        need(fid not in seen, "duplicate-disposition", f"{fid} is dispositioned twice")
        enum(item.get("status"), STATUSES, f"{fid} status")
        if item["status"] in NEEDS_REASON:
            text(item.get("reason"), f"{fid} {item['status']} reason")
        seen[fid] = item
    unique = []
    for i, u in enumerate(items(r2.get("unique", []), "unique")):
        obj(u, f"unique {i}")
        need(isinstance(u.get("id"), str) and UNIQUE_ID.fullmatch(u["id"]) is not None, "unique", f"unique {i} id is not U01..U99")
        need(u["id"] not in [x["id"] for x in unique], "unique", f"unique id {u['id']} repeats")
        enum(u.get("origin"), ("reviewer", "builder"), f"unique {u['id']} origin")
        text(u.get("observation"), f"unique {u['id']} observation")
        unique.append(u)
    agreements = [text(a, "agreement") for a in items(r2.get("agreements", []), "agreements")]
    disagreements = [text(a, "disagreement") for a in items(r2.get("disagreements", []), "disagreements")]
    missing = [i for i in ids if i not in seen]
    return {
        "result": "reconciled-as-declared" if not missing else "incomplete",
        "undispositioned": missing,
        "unresolved": [{"finding": k, "reason": v["reason"]} for k, v in seen.items() if v["status"] == "unresolved"],
        "dispositions": {k: v["status"] for k, v in seen.items()},
        "unique": unique,
        "agreements": agreements,
        "disagreements": disagreements,
        "raw": {"first": facts1, "second": facts2},
        "not_established": ["truth of any finding", "acceptance", "independence of the reviewers' errors"],
    }
