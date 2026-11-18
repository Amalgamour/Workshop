#!/usr/bin/env python3
"""0510/05.05 pass01: NONPRODUCTION prototype of the proposed reserved-review rules.

Pure functions over already-verified inputs. No file, Git, process or model access.
The proposed checker (CONTRACT.md) would obtain these inputs from:
  trusted   - handoff_check.py `trusted` output (digest-bound package claims)
  request   - package/colab-request.json bytes (bound by the digest)
  binding   - package/binding.json bytes (sha == trusted.binding_sha256)
  descriptor- the reserved-review/1 snapshot found through trusted.source_map
  returns   - exact captured return.md bytes (N1NN member, verified by the inspector)
Compute checks shape, presence, identity and order. It does not judge findings,
prove freshness, model identity or independence; those stay declared facts.
"""

from __future__ import annotations

import json
import re

DESCRIPTOR_SCHEMA = "reserved-review/1"
FINDINGS_SCHEMA = "reserved-findings/1"
RECON_SCHEMA = "reserved-reconciliation/1"
TRIGGERS = ("stuck", "pre-release-testing")
SESSIONS = ("new", "continuing", "unknown")
STATUSES = ("confirmed", "withdrawn", "different-conditions", "unresolved", "out-of-scope")
NEEDS_REASON = ("withdrawn", "different-conditions", "out-of-scope", "unresolved")
FINDING_ID = re.compile(r"^R[0-9]{2}$")
UNIQUE_ID = re.compile(r"^U[0-9]{2}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DESCRIPTOR_KEYS = {
    "schema", "investigation", "stage", "first_pass", "first_return", "trigger", "question",
    "artifact_cut", "environment", "requirements", "authority_limits", "builder_context",
    "unavailable", "reviewer_assignment", "builder_identity",
}


class Problem(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def need(cond: bool, code: str, detail: str) -> None:
    if not cond:
        raise Problem(code, detail)


def descriptor_path(investigation: dict, desk: str = "00.kernel") -> str:
    """Proposed fixed location: <desk>/<book>/<page>/evidence/reserved05.NN.json."""
    nn = investigation["pass"].split(".")[1]
    return f"{desk}/{investigation['book']}/{investigation['page']}/evidence/reserved05.{nn}.json"


def find_descriptor(trusted: dict, path: str) -> dict | None:
    rows = [r for r in trusted["source_map"] if r["source_path"] == path]
    if not rows:
        return None
    need(len(rows) == 1 and rows[0]["role"] == "required", "descriptor", "the descriptor must be one required source")
    return rows[0]


def strict(data: bytes, where: str):
    def no_dupes(pairs):
        keys = [k for k, _ in pairs]
        need(len(keys) == len(set(keys)), "json", f"{where} repeats a key")
        return dict(pairs)
    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=no_dupes,
                          parse_constant=lambda c: (_ for _ in ()).throw(Problem("json", f"{where} has {c}")))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise Problem("json", f"{where} is not strict UTF-8 JSON") from None


def validate_descriptor(d: dict) -> None:
    need(isinstance(d, dict) and set(d) == DESCRIPTOR_KEYS, "descriptor", "keys are not reserved-review/1")
    need(d["schema"] == DESCRIPTOR_SCHEMA, "version", "descriptor schema is not reserved-review/1")
    need(d["stage"] in ("independent", "informed"), "descriptor", "stage is not independent or informed")
    t = d["trigger"]
    need(isinstance(t, dict) and t.get("kind") in TRIGGERS, "no-trigger", "trigger kind must be stuck or pre-release-testing")
    need(isinstance(t.get("named_by"), str) and t["named_by"].strip(), "no-trigger", "trigger names no one")
    need(isinstance(t.get("statement"), str) and t["statement"].strip(), "no-trigger", "trigger statement is empty")
    ra = d["reviewer_assignment"]
    need(ra.get("session") in SESSIONS, "descriptor", "reviewer session must be new, continuing or unknown")
    for key in ("model", "family", "prior_involvement"):
        need(isinstance(ra.get(key), str) and ra[key].strip(), "descriptor", f"reviewer {key} must be text or 'unknown'")


def cut_rows(cut) -> list[tuple]:
    return sorted((t["id"], t["path"], t["sha256"], t["bytes"]) for t in cut["targets"])


def launch_check(trusted: dict, request: dict, binding: dict, descriptor: dict | None) -> dict:
    """Independent stage. Returns {result, first_pass_label, notes}; raises Problem on refusal."""
    if descriptor is None:
        return {"result": "ordinary", "notes": ["no reserved-review descriptor; nothing to check"]}
    validate_descriptor(descriptor)
    need(descriptor["stage"] == "independent", "stage-order", "launch-check is for the independent stage")
    need(descriptor["first_pass"] is None and descriptor["first_return"] is None, "stage-order", "an independent stage names no first pass")
    inv = trusted["investigation"]
    need({k: descriptor["investigation"][k] for k in ("book", "page", "pass")} == inv, "identity", "descriptor investigation differs from the package")
    cut = descriptor["artifact_cut"]
    need(cut is not None and cut.get("commit") and all(HEX64.fullmatch(str(t.get("sha256") or "")) for t in cut.get("targets") or [{}]),
         "launch-unready", "artifact cut commit or target hashes were not supplied")
    need(cut["commit"] == binding["targets"][0]["source"]["commit"], "cut-mismatch", "descriptor commit differs from the package binding")
    package_targets = sorted((r["targets"][0], r["source_path"], r["sha256"], r["bytes"]) for r in trusted["source_map"] if r["role"] == "target")
    need(cut_rows(cut) == package_targets, "cut-mismatch", "descriptor targets differ from the packaged targets")
    present = {(r["source_path"], r["sha256"]) for r in trusted["source_map"]}
    shas = {r["sha256"] for r in trusted["source_map"]}
    paths = {r["source_path"] for r in trusted["source_map"]}
    for req in descriptor["requirements"]:
        need((req["path"], req["sha256"]) in present, "requirement-missing", f"requirement {req['path']} is not in the packet")
    for lim in descriptor["authority_limits"]:
        need((lim["path"], lim["sha256"]) in present, "authority-missing", f"authority limit {lim['path']} is not in the packet")
    for ctx in descriptor["builder_context"]:
        need(ctx["path"] not in paths and ctx["sha256"] not in shas, "context-in-first-packet", f"builder context {ctx['path']} is in the first packet")
    withheld = {w["item"] for w in request["withheld"]}
    for ctx in descriptor["builder_context"]:
        need(ctx["path"] in withheld, "withhold-undeclared", f"builder context {ctx['path']} is not declared as withheld to the reviewer")
    ra = descriptor["reviewer_assignment"]
    need(ra["session"] != "continuing", "not-fresh", "a continuing session cannot be the independent first pass; run it as an ordinary informed Colab")
    label = "independent-fresh-declared" if ra["session"] == "new" else "independent-freshness-unknown"
    bi = descriptor["builder_identity"]
    same = "unknown" if "unknown" in (ra["family"], bi.get("family", "unknown")) else str(ra["family"] == bi["family"]).lower()
    return {"result": "launch-ready-as-declared", "first_pass_label": label, "same_family_declared": same,
            "notes": ["declared facts only: freshness, model and family are not authenticated"]}


def parse_block(text: bytes, name: str, where: str):
    body = text.decode("utf-8")
    blocks = re.findall(r"(?ms)^```" + re.escape(name) + r"[ \t]*\n(.*?)^```[ \t]*$", body)
    need(len(blocks) != 0, f"missing-{name}", f"{where} has no ```{name}``` block")
    need(len(blocks) == 1, f"duplicate-{name}", f"{where} has more than one ```{name}``` block")
    return strict(blocks[0].encode("utf-8"), f"{where} {name} block")


def first_findings(return_bytes: bytes) -> dict:
    block = parse_block(return_bytes, "reserved-findings", "first return")
    need(block.get("schema") == FINDINGS_SCHEMA and block.get("stage") == "independent", "version", "findings block is not reserved-findings/1 independent")
    ids = [f.get("id") for f in block.get("findings") or []]
    need(all(isinstance(i, str) and FINDING_ID.fullmatch(i) for i in ids) and len(ids) == len(set(ids)), "findings", "finding ids must be unique R01..R99")
    return block


def stage_check(first: dict, second: dict, trusted2: dict, first_capture: dict, first_return: bytes) -> dict:
    """Informed stage, before launching pass 2."""
    validate_descriptor(second)
    need(second["stage"] == "informed", "stage-order", "stage-check is for the informed stage")
    inv1, inv2 = first["investigation"], second["investigation"]
    need((inv1["book"], inv1["page"]) == (inv2["book"], inv2["page"]), "identity", "both stages must be one investigation page")
    need(second["first_pass"] == inv1["pass"] and inv2["pass"] > inv1["pass"], "stage-order", "the informed pass must follow the named first pass")
    need(first_capture.get("status") == "complete" and first_capture.get("origin") == {"book": inv1["book"], "page": inv1["page"], "batch": inv1["pass"]},
         "first-not-sealed", "the first return is not a complete capture for the first pass")
    fr = second["first_return"]
    need(fr is not None and fr["return_sha256"] == first_capture["return_sha256"], "first-not-sealed", "descriptor does not name the captured first return")
    import hashlib
    need(hashlib.sha256(first_return).hexdigest() == fr["return_sha256"], "first-not-sealed", "first return bytes differ from the capture")
    first_findings(first_return)
    shas2 = {r["sha256"] for r in trusted2["source_map"]}
    need(fr["return_sha256"] in shas2, "order", "the informed packet does not carry the sealed first return")
    need(cut_rows(first["artifact_cut"]) == cut_rows(second["artifact_cut"]) and first["artifact_cut"]["commit"] == second["artifact_cut"]["commit"],
         "target-changed", "the artifact cut changed; this is a new comparison, not the same frozen observation")
    present = {(r["source_path"], r["sha256"]) for r in trusted2["source_map"]}
    missing_ctx = [c["path"] for c in second["builder_context"] if (c["path"], c["sha256"]) not in present]
    env = sorted(k for k in set(first["environment"]) | set(second["environment"]) if first["environment"].get(k) != second["environment"].get(k))
    changed_reviewer = [k for k in ("model", "family", "session") if first["reviewer_assignment"][k] != second["reviewer_assignment"][k]]
    return {"result": "informed-launch-ready-as-declared", "builder_context_not_supplied": missing_ctx,
            "condition_differences": env, "reviewer_assignment_changed": changed_reviewer}


def reconcile(first_return: bytes, second_return: bytes) -> dict:
    findings = first_findings(first_return)
    recon = parse_block(second_return, "reserved-reconciliation", "second return")
    need(recon.get("schema") == RECON_SCHEMA and recon.get("stage") == "informed", "version", "reconciliation block is not reserved-reconciliation/1 informed")
    ids = [f["id"] for f in findings["findings"]]
    seen = {}
    for item in recon.get("dispositions") or []:
        fid = item.get("finding")
        need(fid in ids, "unknown-finding", f"disposition names {fid}, which is not a first-pass finding")
        need(fid not in seen, "duplicate-disposition", f"{fid} is dispositioned twice")
        need(item.get("status") in STATUSES, "status", f"{fid} status is not one of {', '.join(STATUSES)}")
        if item["status"] in NEEDS_REASON:
            need(isinstance(item.get("reason"), str) and item["reason"].strip(), "reason", f"{fid} {item['status']} needs a reason")
        seen[fid] = item["status"]
    uniques = [u.get("id") for u in recon.get("unique") or []]
    need(all(isinstance(u, str) and UNIQUE_ID.fullmatch(u) for u in uniques) and len(uniques) == len(set(uniques)), "unique", "unique ids must be U01..U99")
    missing = [i for i in ids if i not in seen]
    status = "reconciled-as-declared" if not missing else "incomplete"
    counts = {s: sum(1 for v in seen.values() if v == s) for s in STATUSES}
    return {"result": status, "undispositioned": missing, "counts": counts,
            "unique": uniques, "agreements": len(recon.get("agreements") or []), "disagreements": len(recon.get("disagreements") or []),
            "not_established": ["truth of any finding", "acceptance", "independence of the reviewers' errors"]}
