#!/usr/bin/env python3
"""Inputs-manifest shape validation for the harness successor (0707/05.22). NONPRODUCTION. Pure: no file reads.

shape_problems(inputs) returns a list of problems; the harness REFUSES (exit 2) on any. A malformed collection is
never read as an empty one. 'accepted' is declared evidence only: an accepted row must name a frozen Prime review
by path/sha256/bytes (review_ref), which the harness then checks against live bytes. The harness does not decide
that a review accepted anything; it checks that the declared reference exists unchanged.
"""

from __future__ import annotations

import re

SCHEMA = "harness-inputs/2"
KNOWN_DEPS = ("G", "L", "K", "I", "R", "W")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
JUDGMENT_IDS = ("j-0512-0509", "j-0522-0514", "j-0512-0510")


def _pin(x, where, out) -> bool:
    if not isinstance(x, dict):
        out.append(f"{where}: pin is not an object")
        return False
    ok = True
    if not isinstance(x.get("path"), str) or not x["path"] or x["path"].startswith(("/", "\\")) or ".." in x["path"].split("/"):
        out.append(f"{where}: bad path {x.get('path')!r}")
        ok = False
    if not isinstance(x.get("sha256"), str) or not HEX64.match(x["sha256"]):
        out.append(f"{where}: bad sha256")
        ok = False
    if type(x.get("bytes")) is not int or x["bytes"] < 0:
        out.append(f"{where}: bad bytes {x.get('bytes')!r}")
        ok = False
    return ok


def _pin_list(xs, where, out, allow_lab=False) -> None:
    if not isinstance(xs, list) or not xs:
        out.append(f"{where}: not a non-empty list (got {type(xs).__name__})")
        return
    seen = set()
    for i, x in enumerate(xs):
        if _pin(x, f"{where}[{i}]", out):
            if x["path"] in seen:
                out.append(f"{where}: duplicate path {x['path']}")
            seen.add(x["path"])
        if allow_lab and isinstance(x, dict) and "lab" in x and not isinstance(x["lab"], bool):
            out.append(f"{where}[{i}]: 'lab' is not boolean")


def shape_problems(inputs) -> list:
    out = []
    if not isinstance(inputs, dict):
        return [f"inputs is not an object (got {type(inputs).__name__})"]
    if inputs.get("schema") != SCHEMA:
        out.append(f"schema is not {SCHEMA}")
    # candidate
    cand = inputs.get("candidate")
    if cand != "PENDING":
        if not isinstance(cand, dict):
            out.append("candidate is neither 'PENDING' nor an object")
        else:
            for k in ("name", "kind"):
                if not isinstance(cand.get(k), str) or not cand[k]:
                    out.append(f"candidate.{k} missing")
            if not isinstance(cand.get("candidate_json_sha256"), str) or not HEX64.match(cand["candidate_json_sha256"]):
                out.append("candidate.candidate_json_sha256 bad")
            _pin_list(cand.get("files"), "candidate.files", out, allow_lab=True)
            if cand.get("open_entry") is not None and not isinstance(cand.get("open_entry"), str):
                out.append("candidate.open_entry is neither null nor a string")
            if not isinstance(cand.get("lab_differences"), list):
                out.append("candidate.lab_differences is not a list")
    # dependencies
    deps = inputs.get("dependencies")
    if not isinstance(deps, list):
        out.append(f"dependencies is not a list (got {type(deps).__name__})")
    elif not deps:
        out.append("dependencies is empty")
    else:
        seen = []
        for i, d in enumerate(deps):
            w = f"dependencies[{i}]"
            if not isinstance(d, dict):
                out.append(f"{w}: not an object")
                continue
            did = d.get("id")
            if did not in KNOWN_DEPS:
                out.append(f"{w}: unknown id {did!r}")
                continue
            w = f"dependency {did}"
            if did in seen:
                out.append(f"{w}: duplicate")
            seen.append(did)
            if d.get("required") is not True:
                out.append(f"{w}: 'required' must be the boolean true (got {d.get('required')!r})")
            st = d.get("status")
            if st not in ("accepted", "pending", "rejected"):
                out.append(f"{w}: unknown status {st!r}")
                continue
            if not isinstance(d.get("review"), str) or not d["review"]:
                out.append(f"{w}: no review note")
            if st == "accepted":
                _pin_list(d.get("files"), f"{w}.files", out)
                _pin(d.get("review_ref"), f"{w}.review_ref", out)
                if did == "R":
                    iface = d.get("interface")
                    if not isinstance(iface, dict) or iface.get("route") != "review-report":
                        out.append("dependency R: accepted row must declare interface.route 'review-report'")
            else:
                if d.get("files") != "PENDING":
                    out.append(f"{w}: {st} rows must say files 'PENDING' (got {type(d.get('files')).__name__})")
                if "review_ref" in d:
                    out.append(f"{w}: {st} rows carry no review_ref pin")
        missing = [x for x in KNOWN_DEPS if x not in seen]
        if missing:
            out.append(f"dependencies missing rows: {missing}")
    # fixtures and judgments
    _pin(inputs.get("fixture_source"), "fixture_source", out)
    js = inputs.get("judgments")
    if not isinstance(js, list):
        out.append(f"judgments is not a list (got {type(js).__name__})")
    else:
        ids = []
        for i, j in enumerate(js):
            if not isinstance(j, dict):
                out.append(f"judgments[{i}]: not an object")
                continue
            _pin(j, f"judgments[{i}]", out)
            ids.append(j.get("id"))
            if type(j.get("expected_sources")) is not int:
                out.append(f"judgments[{i}]: expected_sources is not an integer")
            for k in ("page", "pass"):
                if not isinstance(j.get(k), str):
                    out.append(f"judgments[{i}]: {k} missing")
        if sorted(x for x in ids if isinstance(x, str)) != sorted(JUDGMENT_IDS) or len(ids) != len(JUDGMENT_IDS):
            out.append(f"judgments must be exactly {list(JUDGMENT_IDS)} (got {ids})")
    return out
