#!/usr/bin/env python3
"""Explicit candidate identity reader for test equipment (0707/05.24; contract 0420/06.57). NONPRODUCTION.

Schema harness-inputs/3 = harness-inputs/2 plus an explicit candidate execution identity:
  candidate.schema          "candidate-identity/1"
  candidate.entry           the actual on-disk entry (must be "app/librarian.py")
  candidate.workbook_entry  the workbook that prepare/read/report actually execute (a declared file)
  candidate.open_entry      optional; a declared file, executable on a new root
  candidate.reporter_entry  optional; a declared file executed by 'review-report'
  candidate.files[]         {path, sha256, bytes, role}  role in ROLES; every executable dependency/adapter it uses
  candidate.lab_differences [{path, differs}]
Metadata paths are UNTRUSTED: relative POSIX, no '..', no drive, no backslash, no leading '/', unique, a regular
non-link file inside the root, hash+length equal. Unsupported schema refuses. A pending candidate refuses.

LEGACY (labelled): harness-inputs/2 is read ONLY for the two frozen baselines (CANDIDATE.json hash allowlist); their
workbook is then found by the old review_loop_tools_vN.py discovery, labelled 'legacy-discovery'. Any other
harness-inputs/2 refuses with its real reasons. Old manifests are never migrated or repinned.

EXECUTION PROOF: a declaration alone does not establish what runs. tamper_proof() PREPENDS a SystemExit with a nonce to
the declared target in a NEW disposable copy and compares a fixed probe against an untampered control copy. Identical
(exit, stdout) => the target is NOT executed => DECOY. Only disposable copies are ever changed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import uuid
from pathlib import Path

ENTRY = "app/librarian.py"
ROLES = {"entry", "workbook", "open", "reporter", "dependency", "adapter", "declaration", "data"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
LEGACY_BASELINES = {   # CANDIDATE.json sha256 of the two frozen baselines built by pass01 make_candidate.py
    "172ec4e9f22bb7a2c921915703a5e8e67ac2f58222f4a331fad5b6ae57b6f9af": "proto-l",
    "062a3c8da7c3e55e84ffa579d106c7ad07e2ef4011c513421584a151a5cc1b2a": "staged-g",
}
LIVE = Path(r"D:\Git\lib-build")


class Refused(Exception):
    pass


def sha_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def path_problem(p) -> str | None:
    if not isinstance(p, str) or not p:
        return "not a non-empty string"
    if "\\" in p or p.startswith("/") or re.match(r"^[A-Za-z]:", p) or "\x00" in p:
        return "not a relative POSIX path"
    parts = p.split("/")
    if any(x in ("", ".", "..") for x in parts):
        return "contains an empty, '.' or '..' segment"
    return None


def contained_file(root: Path, rel: str) -> Path:
    p = root / rel
    try:
        p.resolve().relative_to(root.resolve())
    except ValueError:
        raise Refused(f"{rel}: resolves outside the candidate root")
    if p.is_symlink() or (p.exists() and not p.is_file()):
        raise Refused(f"{rel}: not a regular file")
    return p


# ------------------------------------------------------------------ shapes
def v3_problems(cand) -> list:
    out = []
    if not isinstance(cand, dict):
        return ["candidate is not an object"]
    if cand.get("schema") != "candidate-identity/1":
        out.append(f"candidate.schema {cand.get('schema')!r} is not supported (need candidate-identity/1)")
    for k in ("name", "kind"):
        if not isinstance(cand.get(k), str) or not cand[k]:
            out.append(f"candidate.{k} missing")
    if cand.get("entry") != ENTRY:
        out.append(f"candidate.entry must be {ENTRY!r} (got {cand.get('entry')!r})")
    if not isinstance(cand.get("candidate_json_sha256"), str) or not HEX64.match(cand["candidate_json_sha256"]):
        out.append("candidate.candidate_json_sha256 bad")
    files = cand.get("files")
    if not isinstance(files, list) or not files:
        return out + [f"candidate.files is not a non-empty list (got {type(files).__name__})"]
    seen, roles = set(), {}
    for i, f in enumerate(files):
        w = f"candidate.files[{i}]"
        if not isinstance(f, dict):
            out.append(f"{w}: not an object")
            continue
        pp = path_problem(f.get("path"))
        if pp:
            out.append(f"{w}: path {f.get('path')!r} {pp}")
            continue
        if f["path"] in seen:
            out.append(f"{w}: duplicate path {f['path']}")
        seen.add(f["path"])
        if not isinstance(f.get("sha256"), str) or not HEX64.match(f["sha256"]):
            out.append(f"{w}: bad sha256")
        if type(f.get("bytes")) is not int or f["bytes"] < 0:
            out.append(f"{w}: bad bytes")
        if f.get("role") not in ROLES:
            out.append(f"{w}: unknown role {f.get('role')!r}")
        roles.setdefault(f.get("role"), []).append(f["path"])
    for key, role, need in (("entry", "entry", True), ("workbook_entry", "workbook", True), ("open_entry", "open", False),
                            ("reporter_entry", "reporter", False)):
        v = cand.get(key)
        if v is None and not need:
            if roles.get(role):
                out.append(f"files declare role {role!r} but candidate.{key} is null")
            continue
        pp = path_problem(v)
        if pp:
            out.append(f"candidate.{key} {v!r} {pp}")
        elif v not in seen:
            out.append(f"candidate.{key} {v!r} is not a declared file")
        elif key in ("open_entry", "reporter_entry") and v == cand.get("workbook_entry") and not roles.get(role):
            pass                     # the workbook may also be the open/reporter entry (as in proto-l and the 05.17 candidate)
        elif roles.get(role) != [v]:
            out.append(f"candidate.{key}: exactly one file must carry role {role!r} and it must be {v!r} (got {roles.get(role)})")
    if not isinstance(cand.get("lab_differences"), list):
        out.append("candidate.lab_differences is not a list")
    return out


# ------------------------------------------------------------------ resolution
def legacy_workbook(root: Path) -> str:
    """LEGACY DISCOVERY (labelled): the old review_loop_tools_vN.py filename rule, for the two frozen baselines only."""
    disp = (root / ENTRY).read_text(encoding="utf-8")
    for v in range(20, 3, -1):
        if f"review_loop_tools_v{v}.py" in disp:
            return json.loads((root / f"app/review-loop-v{v}.json").read_bytes())["tools"]["workbook"]["path"]
    raise Refused("legacy discovery found no review_loop_tools_vN.py in the dispatcher")


def resolve(inputs, root: Path, shape_v2) -> dict:
    """shape_v2: the frozen pass02 inputs_check.shape_problems (for the shared top-level shape)."""
    if not isinstance(inputs, dict):
        raise Refused("inputs is not an object")
    schema = inputs.get("schema")
    cand = inputs.get("candidate")
    if cand == "PENDING":
        raise Refused("candidate is PENDING: nothing to run until Prime freezes an explicit identity")
    try:
        root.resolve().relative_to(LIVE.resolve())
        raise Refused("candidate root is inside the live repo; refusing root substitution")
    except ValueError:
        pass
    if not (root / "CANDIDATE.json").is_file():
        raise Refused("candidate root has no CANDIDATE.json")
    cj = sha_file(root / "CANDIDATE.json")
    if schema == "harness-inputs/2":
        probs = shape_v2(inputs)
        if cj not in LEGACY_BASELINES:
            why = ["harness-inputs/2 is read only for the two frozen baselines; this candidate needs an explicit harness-inputs/3 identity"]
            if isinstance(cand, dict):
                paths = {f.get("path") for f in cand.get("files") or [] if isinstance(f, dict)}
                if cand.get("open_entry") and cand["open_entry"] not in paths:
                    why.append(f"open_entry {cand['open_entry']} is not a declared file")
                why.append("no workbook_entry is declared")
            raise Refused("; ".join(why + probs[:5]))
        if probs:
            raise Refused("legacy inputs malformed: " + "; ".join(probs[:8]))
        if cand["candidate_json_sha256"] != cj:
            raise Refused("CANDIDATE.json differs from the declared identity")
        files = [dict(f) for f in cand["files"]]
        ident = {"mode": "legacy-discovery", "kind": LEGACY_BASELINES[cj], "entry": ENTRY, "open_entry": cand.get("open_entry"),
                 "reporter_entry": None, "files": files, "candidate_json_sha256": cj}
        _bytes(root, files)
        ident["workbook_entry"] = legacy_workbook(root)
        if ident["workbook_entry"] not in {f["path"] for f in files}:
            raise Refused(f"legacy-discovered workbook {ident['workbook_entry']} is not a declared file")
        return ident
    if schema != "harness-inputs/3":
        raise Refused(f"unsupported inputs schema {schema!r}")
    top = dict(inputs, schema="harness-inputs/2", candidate={k: v for k, v in cand.items() if k in
              ("name", "kind", "candidate_json_sha256", "files", "open_entry", "lab_differences")} if isinstance(cand, dict) else cand)
    if isinstance(cand, dict) and isinstance(cand.get("files"), list):
        top["candidate"]["files"] = [{k: v for k, v in f.items() if k in ("path", "sha256", "bytes")} if isinstance(f, dict) else f
                                     for f in cand["files"]]
    probs = v3_problems(cand) + [p for p in shape_v2(top) if not p.startswith("candidate.")]
    if probs:
        raise Refused("explicit identity malformed: " + "; ".join(probs[:10]))
    if cand["candidate_json_sha256"] != cj:
        raise Refused("CANDIDATE.json differs from the declared identity")
    _bytes(root, cand["files"])
    return {"mode": "explicit", "kind": cand["kind"], "entry": cand["entry"], "workbook_entry": cand["workbook_entry"],
            "open_entry": cand.get("open_entry"), "reporter_entry": cand.get("reporter_entry"),
            "files": [{k: f[k] for k in ("path", "sha256", "bytes")} | {"role": f["role"]} for f in cand["files"]], "candidate_json_sha256": cj}


def _bytes(root: Path, files: list) -> None:
    for f in files:
        p = contained_file(root, f["path"])
        if not p.is_file():
            raise Refused(f"declared file absent: {f['path']}")
        if p.stat().st_size != f["bytes"] or sha_file(p) != f["sha256"]:
            raise Refused(f"declared file differs: {f['path']}")


def verify_dependencies(inputs) -> None:
    for d in inputs.get("dependencies") or []:
        if isinstance(d, dict) and d.get("status") == "accepted":
            for f in list(d.get("files") or []) + [d.get("review_ref")]:
                p = LIVE / f["path"]
                if not p.is_file() or p.stat().st_size != f["bytes"] or sha_file(p) != f["sha256"]:
                    raise Refused(f"accepted dependency {d.get('id')} differs: {f['path']}")


# ------------------------------------------------------------------ execution proof (controlled tamper, disposable only)
def _norm(text: str, root: Path) -> str:
    out = text
    for r in {str(root), str(root.resolve())}:
        for s in {r, r.replace("\\", "/"), r.replace("\\", "\\\\"), r.replace("/", "\\"), r.replace("/", "\\").replace("\\", "\\\\")}:
            out = out.replace(s, "<ROOT>")
    return out


def tamper_proof(cand_root: Path, ident: dict, target: str, probe, rooms: Path, tag: str) -> dict:
    """probe(root) -> {'exit', 'stdout', 'stderr'}; runs on a NEW copy. The target is tampered only in its own NEW copy."""
    if target not in {f["path"] for f in ident["files"]}:
        raise Refused(f"tamper target {target} is not a declared file")
    nonce = uuid.uuid4().hex[:12]
    # old-combined-run01/02 (kept): rooms at DIFFERENT paths always differ (paths and path-derived instance/intake ids
    # in the output), so a decoy looked executed. All three runs now use the SAME absolute path P; each finished room is
    # renamed aside (never deleted). Two controls must agree, else the probe is inconclusive (fail closed).
    rooms.mkdir(parents=True, exist_ok=True)
    stable = rooms / f"{tag}-run"
    runs = []
    for label in ("control-1", "control-2", "tamper"):
        shutil.copytree(cand_root, stable)
        if label == "tamper":
            f = stable / target
            # smoke-01 (kept): APPENDING never ran in a script that exits inside main(); PREPEND so any load fails.
            f.write_bytes(f"raise SystemExit('LAB-TAMPER-{nonce}')\n".encode() + f.read_bytes())
        res = probe(stable)
        runs.append((label, res, _norm(res["stdout"], stable)))
        stable.rename(rooms / f"{tag}-{label}")
    (_, c, cn), (_, c2, cn2), (_, t, tn) = runs
    deterministic = (c["exit"], cn) == (c2["exit"], cn2)
    executed = deterministic and (c["exit"], cn) != (t["exit"], tn)
    err = t["stderr"]
    if not deterministic:
        evidence = "inconclusive: two untampered controls at the same path disagree (probe nondeterministic)"
    elif not executed:
        evidence = "none: probe output identical to the control"
    elif nonce in err:
        evidence = "executed: the tamper nonce surfaced (the target ran)"
    elif "SyntaxError" in err and "__future__" in err:
        evidence = "loaded: the target was compiled by the chain (prepended line broke its __future__ import)"
    elif target in err.replace("\\", "/"):
        evidence = "checked: the chain refused naming this target (e.g. a pin check); a check of these bytes, not proof they run"
    else:
        evidence = "changed: probe output differs, but the stderr does not name the target"
    return {"target": target, "nonce": nonce, "evidence": evidence,
            "control": {"exit": c["exit"], "stdout_sha256": hashlib.sha256(c["stdout"].encode()).hexdigest(),
                        "normalized_stdout_sha256": hashlib.sha256(cn.encode()).hexdigest(), "stderr_tail": c["stderr"][-300:]},
            "tampered": {"exit": t["exit"], "stdout_sha256": hashlib.sha256(t["stdout"].encode()).hexdigest(),
                         "normalized_stdout_sha256": hashlib.sha256(tn.encode()).hexdigest(),
                         "nonce_in_stderr": nonce in t["stderr"], "stderr_tail": t["stderr"][-200:]},
            "deterministic_control": deterministic, "executed": executed,
            "verdict": "executed" if executed else ("INCONCLUSIVE (not proven executed)" if not deterministic else "DECOY (declared target not executed)"),
            "rooms": [str(rooms / f"{tag}-{x}") for x in ("control-1", "control-2", "tamper")], "stable_path": str(stable)}
