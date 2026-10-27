"""Recorded Prime boot prototype, fixture only (0507.prime-support/05.07). Standard library only.

  python -B prime_boot.py prepare --request REQ.json --records ROOT --attempt ID
  python -B prime_boot.py check   --attempt DIR --answers ANSWERS.json
  python -B prime_boot.py judge   --attempt DIR --judgement JUDGEMENT.json
  python -B prime_boot.py show    --attempt DIR [--json]

Contract: 00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/CONTRACT.md. Every record is exclusive-create
in one attempt directory under an explicit external records root. Reads are fixed Git blobs at the requested commit,
pinned read-only tools, and live-worktree observations recorded apart. Nothing here installs, acknowledges, dispatches,
calls a model, accepts, seats or grants authority. Orientation is not authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

PINS = {
    "prime_support": "700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70",
    "clerk_adapter": "2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4",  # sibling of prime_support
    "check_book": "fc16d2f68a3645050b6766ce18ce55f8169a0e2bad52d3392b4d059c629073a4",
    "return_capture": "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac",
}
GIT_ALLOWED = {"rev-parse", "cat-file", "show", "status"}
REQUEST_KEYS = {"schema", "boot_id", "attempt", "previous_attempt", "workspace", "branch", "commit", "role", "model",
                "book", "role_record", "assignment_record", "registry", "tools", "members", "members_book", "packet",
                "limits"}
ANSWER_KEYS = {"O1": {"target", "citations", "conflicts_seen", "text"}, "O2": {"fields", "text"},
               "O3": {"citations", "text"}, "O4": {"citations", "text"}, "O6": {"citations", "text"}}
O2_FIELDS = {"release", "claim", "execution", "review"}
GRADES = {"pass", "gap", "wrong"}
ASSIGNMENT_KEYS = {"record", "schema", "desk", "book", "workflow_space", "current_work", "pack", "assignment_state",
                   "waits_on", "next", "updated"}
MAX_REFS, MAX_BYTES = 12, 131072
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
POINTER_RE = re.compile(r"contents in (\S+?)\.(?=\s|$)")
AUTHORITY = "none; orientation grants no new work authority"


class Refusal(Exception):
    pass


class StageFailure(Exception):
    pass


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def canonical(value) -> bytes:
    return (json.dumps(value, sort_keys=True, indent=1, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def strict_json(data: bytes, label: str):
    def pairs(seq):
        out = {}
        for key, value in seq:
            if key in out:
                raise StageFailure(f"{label}: duplicate key {key}")
            out[key] = value
        return out

    def constant(name):
        raise StageFailure(f"{label}: nonfinite number {name}")

    try:
        return json.loads(data.decode("utf-8"), object_pairs_hook=pairs, parse_constant=constant)
    except UnicodeDecodeError:
        raise StageFailure(f"{label}: not UTF-8") from None
    except json.JSONDecodeError as exc:
        raise StageFailure(f"{label}: invalid JSON ({exc.msg})") from None


def write_once(path: Path, data: bytes) -> None:
    with open(path, "xb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())


def inside_git(path: Path) -> bool:
    for ancestor in [path, *path.parents]:
        if (ancestor / ".git").exists():
            return True
    return False


def rel_ok(text) -> bool:
    if not isinstance(text, str) or not text or "\\" in text or text.startswith("/") or re.match(r"^[A-Za-z]:", text):
        return False
    return all(part not in ("", ".", "..") for part in text.split("/"))


def plain_file_sha(path: str) -> str | None:
    try:
        st = os.lstat(path)
    except OSError:
        return None
    if stat.S_ISLNK(st.st_mode) or (getattr(st, "st_file_attributes", 0) or 0) & 0x400 or not stat.S_ISREG(st.st_mode):
        return None
    with open(path, "rb") as handle:
        return sha256(handle.read())


# ---------- bounded external reads ----------

def git(workspace: str, *args: str, ok=(0,)) -> tuple[int, bytes]:
    if not args or args[0] not in GIT_ALLOWED:
        raise AssertionError(f"git subcommand not allowed: {args[:1]}")
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0", GIT_TERMINAL_PROMPT="0")
    proc = subprocess.run(["git", "-C", workspace, *args], capture_output=True, env=env, timeout=60)
    if proc.returncode not in ok:
        raise StageFailure(f"git {args[0]} failed: {proc.stderr.decode('utf-8', 'replace').strip()[:200]}")
    return proc.returncode, proc.stdout


def blob(workspace: str, commit: str, path: str) -> bytes | None:
    code, _ = git(workspace, "cat-file", "-e", f"{commit}:{path}", ok=(0, 1, 128))
    return git(workspace, "show", f"{commit}:{path}")[1] if code == 0 else None


def run_tool(path: str, pin: str, args: list[str]) -> dict:
    """Hash-check, then launch. A mismatch never launches."""
    digest = plain_file_sha(path)
    if digest != pin:
        raise StageFailure(f"tool {path} is not the pinned code (sha256 {digest})")
    proc = subprocess.run([sys.executable, "-I", "-B", path, *args], capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=120, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    return {"argv": [path, *args], "exit": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}


# ---------- prepare ----------

def validate_request(req) -> dict:
    if not isinstance(req, dict) or set(req) != REQUEST_KEYS:
        extra = sorted(set(req) - REQUEST_KEYS) if isinstance(req, dict) else []
        raise StageFailure("request keys are not prime-boot-request/1" + (f" (unknown {extra[0]})" if extra else ""))
    if req["schema"] != "prime-boot-request/1":
        raise StageFailure("unsupported request schema")
    for key in ("boot_id", "role", "model", "branch"):
        if not isinstance(req[key], str) or not LABEL.fullmatch(req[key]):
            raise StageFailure(f"request {key} is not a plain label")
    if type(req["attempt"]) is not int or req["attempt"] < 1:
        raise StageFailure("request attempt must be an integer >= 1")
    if not isinstance(req["commit"], str) or not HEX40.fullmatch(req["commit"]):
        raise StageFailure("request commit must be 40 lowercase hex")
    for key in ("workspace",):
        if not isinstance(req[key], str) or not os.path.isabs(req[key]):
            raise StageFailure(f"request {key} must be absolute")
    for key in ("book", "role_record", "assignment_record"):
        if not rel_ok(req[key]):
            raise StageFailure(f"request {key} is not a relative POSIX path")
    if req["previous_attempt"] is not None and (not isinstance(req["previous_attempt"], str) or not os.path.isabs(req["previous_attempt"])):
        raise StageFailure("previous_attempt must be null or absolute")
    reg = req["registry"]
    if not isinstance(reg, dict) or set(reg) != {"path", "sha256"} or not isinstance(reg["path"], str) \
            or not os.path.isabs(reg["path"]) or not isinstance(reg["sha256"], str) or not HEX64.fullmatch(reg["sha256"]):
        raise StageFailure("registry must be {path (absolute), sha256 (64 hex)}")
    tools = req["tools"]
    if not isinstance(tools, dict) or set(tools) != {"prime_support", "check_book", "return_capture"} \
            or not all(isinstance(v, str) and os.path.isabs(v) for v in tools.values()):
        raise StageFailure("tools must name prime_support, check_book and return_capture by absolute path")
    if not isinstance(req["members"], list) or not all(isinstance(m, str) and LABEL.fullmatch(m) for m in req["members"]):
        raise StageFailure("members must be a list of member folder names")
    if req["members"] and (not isinstance(req["members_book"], str) or not os.path.isabs(req["members_book"])):
        raise StageFailure("members_book must be absolute when members are named")
    if not req["members"] and req["members_book"] is not None:
        raise StageFailure("members_book must be null when no members are named")
    if not isinstance(req["packet"], list) or not all(rel_ok(p) for p in req["packet"]):
        raise StageFailure("packet must be a list of relative POSIX paths")
    if len(set(req["packet"])) != len(req["packet"]):
        raise StageFailure("packet lists a path twice")
    lim = req["limits"]
    if not isinstance(lim, dict) or set(lim) != {"max_refs", "max_bytes"} \
            or type(lim["max_refs"]) is not int or type(lim["max_bytes"]) is not int \
            or not 1 <= lim["max_refs"] <= MAX_REFS or not 1 <= lim["max_bytes"] <= MAX_BYTES:
        raise StageFailure(f"limits must be integers 1..{MAX_REFS} refs and 1..{MAX_BYTES} bytes")
    return req


def identities(req: dict) -> dict:
    """The required identities re-read for the stability check (PB-04)."""
    head = git(req["workspace"], "rev-parse", "--verify", "HEAD")[1].decode().strip()
    code, out = git(req["workspace"], "rev-parse", "--verify", "--quiet", f"refs/heads/{req['branch']}", ok=(0, 1))
    tools = {name: plain_file_sha(path) for name, path in req["tools"].items()}
    tools["clerk_adapter"] = plain_file_sha(str(Path(req["tools"]["prime_support"]).parent / "clerk_adapter.py"))
    return {"head": head, "branch_ref": out.decode().strip() if code == 0 else None,
            "registry_sha256": plain_file_sha(req["registry"]["path"]), "tools": tools}


def stage_links(req: dict, attempt_dir: Path) -> dict:
    prev = req["previous_attempt"]
    if prev is None:
        return {"previous_attempt": None}
    p = Path(prev)
    if p.resolve() == attempt_dir.resolve() or not (p / "00.intent.json").is_file():
        raise StageFailure("previous_attempt is not an existing attempt directory")
    intent_bytes = (p / "00.intent.json").read_bytes()
    intent = strict_json(intent_bytes, "previous intent")
    prev_req_raw = (p / "00.request.raw").read_bytes()
    try:
        prev_req = strict_json(prev_req_raw, "previous request")
        prev_n = prev_req.get("attempt") if isinstance(prev_req, dict) else None
    except StageFailure:
        prev_n = None
    if type(prev_n) is int and prev_n >= req["attempt"]:
        raise StageFailure(f"attempt {req['attempt']} does not follow previous attempt {prev_n}")
    return {"previous_attempt": str(p), "previous_attempt_id": intent.get("attempt_id"),
            "previous_intent_sha256": sha256(intent_bytes), "previous_attempt_number": prev_n,
            "previous_outcome_present": (p / "39.outcome.json").is_file()}


def stage_tools(req: dict) -> dict:
    observed = identities(req)["tools"]
    bad = {k: v for k, v in observed.items() if v != PINS[k]}
    if bad:
        raise StageFailure("tool pin mismatch: " + ", ".join(f"{k} {v}" for k, v in sorted(bad.items())))
    return {"tools": {k: {"path": (req["tools"].get(k) or str(Path(req["tools"]["prime_support"]).parent / "clerk_adapter.py")),
                          "sha256": v} for k, v in observed.items()}}


def stage_git(req: dict) -> dict:
    code, _ = git(req["workspace"], "cat-file", "-e", f"{req['commit']}^{{commit}}", ok=(0, 1, 128))
    if code != 0:
        raise StageFailure("requested commit does not exist in the workspace")
    ids = identities(req)
    dirty = git(req["workspace"], "status", "--porcelain=v1", "-z", "--untracked-files=all", "--", req["book"])[1]
    return {"requested_commit": req["commit"], "head": ids["head"], "branch": req["branch"],
            "branch_ref": ids["branch_ref"], "head_is_commit": ids["head"] == req["commit"],
            "branch_is_commit": ids["branch_ref"] == req["commit"],
            "dirty_paths": [e.decode("utf-8", "replace") for e in dirty.split(b"\0") if e],
            "reads": "committed blobs at requested_commit; worktree observed separately"}


def stage_book(req: dict) -> dict:
    entry_path = f"{req['book']}/00.md"
    entry = blob(req["workspace"], req["commit"], entry_path)
    if entry is None:
        raise StageFailure(f"{entry_path} is absent at the commit")
    pointers = POINTER_RE.findall(entry.decode("utf-8", "replace"))
    if len(pointers) != 1:
        raise StageFailure(f"{entry_path} has {len(pointers)} contents pointers; exactly one is required")
    contents = f"{req['book']}/{pointers[0]}"
    run = run_tool(req["tools"]["check_book"], PINS["check_book"],
                   ["--root", req["workspace"], "--revision", req["commit"], "--book", req["book"], "--json"])
    if run["exit"] not in (0, 1):
        raise StageFailure(f"contents checker refused (exit {run['exit']}): {run['stdout'].strip()[:300]}")
    report = strict_json(run["stdout"].encode("utf-8"), "contents checker report")
    return {"entry": entry_path, "entry_sha256": sha256(entry), "pointer": pointers[0], "contents": contents,
            "checker_exit": run["exit"], "checker_report": report,
            "findings": [f.get("kind") for f in report.get("findings", [])]}


def stage_records(req: dict) -> dict:
    out = {}
    for key in ("role_record", "assignment_record"):
        data = blob(req["workspace"], req["commit"], req[key])
        out[key] = {"path": req[key], "absent": data is None}
        if data is not None:
            out[key].update(sha256=sha256(data), kind="commit-blob", note="recorded text, not authority or current truth")
    data = blob(req["workspace"], req["commit"], req["assignment_record"])
    if data is not None:
        fields = {}
        for line in data.decode("utf-8", "replace").splitlines():
            key, sep, value = line.partition(": ")
            if sep:
                fields[key] = value
        out["assignment_fields"] = fields if set(fields) == ASSIGNMENT_KEYS else None
        out["assignment_parse"] = "v1" if out["assignment_fields"] else "unparsed (not the 0410 v1 key set)"
    return out


def stage_status(req: dict) -> dict:
    data = Path(req["registry"]["path"]).read_bytes()
    if sha256(data) != req["registry"]["sha256"]:
        raise StageFailure("registry bytes do not match the requested sha256")
    reg = strict_json(data, "registry")
    if isinstance(reg, dict) and any(isinstance(l, dict) and l.get("clerk_jobs") for l in reg.get("lanes", [])):
        raise StageFailure("unsupported: the registry has clerk_jobs; Clerk-job boot integration is deferred in this prototype")
    run = run_tool(req["tools"]["prime_support"], PINS["prime_support"], ["status", "--registry", req["registry"]["path"], "--json"])
    if run["exit"] not in (0, 1) or run["stderr"]:
        raise StageFailure(f"prime_support status failed (exit {run['exit']}): {(run['stdout'] + run['stderr']).strip()[:300]}")
    report = strict_json(run["stdout"].encode("utf-8"), "status report")
    scope = sorted({e["path"] for lane in report.get("lanes", []) for e in lane.get("files", []) if e.get("kind") != "page-folder"})
    return {"registry_sha256": sha256(data), "status_exit": run["exit"], "status": report, "scope_paths": scope,
            "conflicts": report.get("conflicts", []), "attention_advice": report.get("attention", []),
            "note": "status mixes committed and live labels as prime_support reports them; attention is advice only"}


def stage_members(req: dict) -> dict:
    results = []
    for member in req["members"]:
        run = run_tool(req["tools"]["return_capture"], PINS["return_capture"],
                       ["verify", "--book", req["members_book"], "--member", member])
        results.append({"member": member, "verify_exit": run["exit"], "verify_stdout": run["stdout"],
                        "integrity": "complete" if run["exit"] == 0 else "not verified",
                        "structured": "unavailable: return_inspect.py is unaccepted",
                        "scope": "capture integrity only; review or publication elsewhere is not asserted either way"})
    return {"members_book": req["members_book"], "members": results}


def stage_packet(req: dict, book: dict) -> dict:
    wanted = [book["entry"], book["contents"], req["role_record"], req["assignment_record"]]
    wanted += [p for p in req["packet"] if p not in wanted]
    refs, absences, omitted, total = [], [], [], 0
    for path in wanted:
        data = blob(req["workspace"], req["commit"], path)
        if data is None:
            absences.append({"id": f"A{len(absences) + 1:02d}", "path": path, "commit": req["commit"], "absent": True})
            continue
        digest = sha256(data)
        reason = None
        if len(refs) >= req["limits"]["max_refs"]:
            reason = "max_refs reached"
        elif total + len(data) > req["limits"]["max_bytes"]:
            reason = "max_bytes would be exceeded"
        else:
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                reason = "not UTF-8 text"
        if reason:
            omitted.append({"path": path, "commit": req["commit"], "sha256": digest, "bytes": len(data), "reason": reason})
            continue
        disk = Path(req["workspace"]) / path
        live_sha = plain_file_sha(str(disk)) if disk.exists() else None
        live = "absent" if not disk.exists() else ("same" if live_sha == digest else "differs")
        ref = {"id": f"R{len(refs) + 1:02d}", "path": path, "commit": req["commit"], "kind": "commit-blob",
               "sha256": digest, "bytes": len(data), "text": text, "live": live}
        if live == "differs":
            ref["live_sha256"] = live_sha
        refs.append(ref)
        total += len(data)
    return {"refs": refs, "absences": absences, "omitted": omitted, "raw_bytes": total, "limits": req["limits"]}


def prepare(request_path: str, records: str, attempt_id: str) -> int:
    root = Path(records)
    if not root.is_absolute() or not root.is_dir() or root.is_symlink() or inside_git(root.resolve()):
        raise Refusal("record store unusable: the records root must be an existing absolute plain directory outside "
                      "every Git working tree; nothing was recorded")
    if not LABEL.fullmatch(attempt_id or ""):
        raise Refusal("attempt id must be a plain label; nothing was recorded")
    attempt_dir = root / attempt_id
    try:
        os.mkdir(attempt_dir)
    except FileExistsError:
        raise Refusal(f"attempt {attempt_id} already exists; nothing was recorded") from None
    except OSError as exc:
        raise Refusal(f"record store unusable: {type(exc).__name__}: {exc.strerror}; nothing was recorded") from None
    try:
        raw = Path(request_path).read_bytes()
    except OSError as exc:
        raw = b""
        read_error = f"{type(exc).__name__}: {exc.strerror}"
    else:
        read_error = None
    write_once(attempt_dir / "00.request.raw", raw)
    write_once(attempt_dir / "00.intent.json", canonical({
        "schema": "prime-boot/1", "attempt_id": attempt_id, "request_path": str(request_path),
        "request_sha256": sha256(raw), "request_read_error": read_error, "started_at": now(),
        "tool": {"path": str(Path(__file__).resolve()), "sha256": sha256(Path(__file__).read_bytes())},
        "note": "intent recorded before any fallible preparation (PB-01)"}))
    stages = [("01", "request"), ("02", "links"), ("03", "tools"), ("04", "git"), ("05", "book"), ("06", "records"),
              ("07", "status"), ("08", "members"), ("09", "packet"), ("10", "stability")]
    results, req, before = {}, None, None
    for number, name in stages:
        try:
            if name == "request":
                if read_error:
                    raise StageFailure("request file could not be read: " + read_error)
                req = validate_request(strict_json(raw, "request"))
                value = {"boot_id": req["boot_id"], "attempt": req["attempt"], "role": req["role"], "model": req["model"],
                         "role_note": "role is a draft label for a fixture exercise, not a seated role"}
            elif name == "links":
                value = stage_links(req, attempt_dir)
            elif name == "tools":
                value = stage_tools(req)
                before = identities(req)
            elif name == "git":
                value = stage_git(req)
            elif name == "book":
                value = stage_book(req)
            elif name == "records":
                value = stage_records(req)
            elif name == "status":
                value = stage_status(req)
            elif name == "members":
                value = stage_members(req)
            elif name == "packet":
                value = stage_packet(req, results["book"])
            else:
                after = identities(req)
                changed = sorted(k for k in before if before[k] != after[k])
                value = {"before": before, "after": after, "stable": not changed, "changed": changed}
        except (StageFailure, OSError, subprocess.SubprocessError) as exc:
            detail = str(exc) if isinstance(exc, StageFailure) else f"{type(exc).__name__}: {exc}"
            write_once(attempt_dir / f"{number}.{name}.json", canonical({"stage": name, "status": "failed", "reason": detail}))
            write_once(attempt_dir / "19.prepare-outcome.json", canonical({
                "status": "failed", "stage": name, "reason": detail, "authority": AUTHORITY,
                "note": "a failed attempt is kept; retry with a new attempt that links this one"}))
            sys.stdout.write(f"attempt {attempt_dir}\nprepare failed at {name}: {detail}\n")
            return 2
        results[name] = value
        write_once(attempt_dir / f"{number}.{name}.json", canonical({"stage": name, "status": "ok", **value}))
    packet = results["packet"]
    reasons = []
    if not results["stability"]["stable"]:
        reasons.append("unstable: " + ", ".join(results["stability"]["changed"]))
    if packet["omitted"]:
        reasons.append(f"{len(packet['omitted'])} source(s) omitted by the caps")
    status = "partial" if reasons else "prepared"
    write_once(attempt_dir / "19.prepare-outcome.json", canonical({
        "status": status, "reasons": reasons, "refs": len(packet["refs"]), "absences": len(packet["absences"]),
        "omitted": len(packet["omitted"]), "authority": AUTHORITY}))
    sys.stdout.write(f"attempt {attempt_dir}\nprepare {status}{': ' + '; '.join(reasons) if reasons else ''}\n")
    return 0 if status == "prepared" else 1


# ---------- check ----------

def load_stage(attempt: Path, name: str) -> dict:
    return strict_json((attempt / name).read_bytes(), name)


def check_answers(attempt: Path, answers: dict) -> dict:
    packet = load_stage(attempt, "09.packet.json")
    status = load_stage(attempt, "07.status.json")
    ref_by_id = {r["id"]: r for r in packet["refs"]}
    ids = set(ref_by_id) | {a["id"] for a in packet["absences"]}
    scope = set(status["scope_paths"]) | {r["path"] for r in packet["refs"]}
    results = {}

    def cite(item, key, label):
        cites = item.get(key)
        if not isinstance(cites, list) or not all(isinstance(c, str) for c in cites):
            return [f"{label}: citations must be a list of packet ids"]
        return [f"{label}: {c} is not a packet ref or absence id" for c in cites if c not in ids]

    for q, keys in ANSWER_KEYS.items():
        item = answers.get(q)
        errs = []
        if not isinstance(item, dict) or set(item) != keys or not isinstance(item.get("text"), str):
            results[q] = {"status": "fail", "errors": [f"{q} must have exactly {sorted(keys)} with string text"]}
            continue
        if q != "O2":
            errs += cite(item, "citations", q)
        if q == "O1":
            target = item["target"]
            if not isinstance(target, str) or target not in scope:
                errs.append("O1 target is not inside the declared scope")
            elif not any(ref_by_id.get(c, {}).get("path") == target for c in item["citations"] if isinstance(c, str)):
                errs.append("O1 must cite a packet ref whose path is the target")
            seen = item["conflicts_seen"]
            if not isinstance(seen, list) or not all(type(i) is int for i in seen):
                errs.append("O1 conflicts_seen must be a list of conflict indices")
            elif sorted(set(seen)) != list(range(len(status["conflicts"]))):
                errs.append(f"O1 must acknowledge every reported conflict (0..{len(status['conflicts']) - 1})"
                            if status["conflicts"] else "O1 lists conflicts that were not reported")
        if q == "O2":
            fields = item["fields"]
            if not isinstance(fields, dict) or set(fields) != O2_FIELDS:
                errs.append(f"O2 fields must be exactly {sorted(O2_FIELDS)}")
            else:
                for name, f in fields.items():
                    if not isinstance(f, dict) or set(f) != {"value", "citation"} or not all(isinstance(v, str) for v in f.values()):
                        errs.append(f"O2 {name} must be {{value, citation}} strings")
                    elif f["citation"] not in ref_by_id:
                        errs.append(f"O2 {name}: {f['citation']} is not a packet ref")
                    elif not f["value"] or f["value"] not in ref_by_id[f["citation"]]["text"]:
                        errs.append(f"O2 {name}: value does not occur in {f['citation']}")
        results[q] = {"status": "fail" if errs else "ok", "errors": errs}
    o5 = answers.get("O5")
    if isinstance(o5, dict) and set(o5) == {"none_found", "text"} and o5["none_found"] is True and isinstance(o5["text"], str):
        results["O5"] = {"status": "ok", "errors": [], "note": "no unknown found in this bounded packet (PB-03)"}
    elif isinstance(o5, dict) and set(o5) == {"citations", "text"} and isinstance(o5["text"], str):
        errs = cite(o5, "citations", "O5")
        if not errs and not o5["citations"]:
            errs = ["O5 must cite at least one ref or absence, or say none_found"]
        results["O5"] = {"status": "fail" if errs else "ok", "errors": errs}
    else:
        results["O5"] = {"status": "fail", "errors": ["O5 must be {none_found: true, text} or {citations, text}"]}
    return {q: results[q] for q in sorted(results)}


def check(attempt_text: str, answers_path: str) -> int:
    attempt = Path(attempt_text)
    prep = load_stage(attempt, "19.prepare-outcome.json")
    if prep["status"] not in ("prepared", "partial"):
        raise Refusal(f"prepare outcome is {prep['status']}; nothing to check")
    raw = Path(answers_path).read_bytes()
    target = attempt / "20.answers.raw"
    if target.exists():
        if target.read_bytes() == raw:
            sys.stdout.write("already-recorded\n")
            return 0
        raise Refusal("conflict: different answers were already recorded for this attempt; start a new attempt")
    write_once(target, raw)
    try:
        doc = strict_json(raw, "answers")
        if not isinstance(doc, dict) or set(doc) != {"schema", "attempt_id", "answers"} or doc["schema"] != "prime-boot-answers/1" \
                or doc["attempt_id"] != attempt.name or not isinstance(doc["answers"], dict) \
                or set(doc["answers"]) != {"O1", "O2", "O3", "O4", "O5", "O6"}:
            raise StageFailure("answers must be prime-boot-answers/1 for this attempt with exactly O1..O6")
        results = check_answers(attempt, doc["answers"])
    except StageFailure as exc:
        write_once(attempt / "22.checks.json", canonical({"status": "failed", "reason": str(exc), "authority": AUTHORITY}))
        sys.stdout.write(f"checks failed: {exc}\n")
        return 1
    write_once(attempt / "21.answers.json", canonical(doc))
    ok = all(r["status"] == "ok" for r in results.values())
    write_once(attempt / "22.checks.json", canonical({"status": "ok" if ok else "failed", "results": results,
                                                       "note": "compute checks identities, scope and explicit fields only",
                                                       "authority": AUTHORITY}))
    sys.stdout.write(f"checks {'ok' if ok else 'failed'}\n" + "".join(
        f"{q} {r['status']}{': ' + '; '.join(r['errors']) if r['errors'] else ''}\n" for q, r in results.items()))
    return 0 if ok else 1


# ---------- judge ----------

def judge(attempt_text: str, judgement_path: str) -> int:
    attempt = Path(attempt_text)
    if not (attempt / "22.checks.json").is_file():
        raise Refusal("no checks recorded; a judgement needs checked answers")
    raw = Path(judgement_path).read_bytes()
    target = attempt / "30.judgement.raw"
    if target.exists():
        if target.read_bytes() == raw:
            sys.stdout.write("already-recorded\n")
            return 0
        raise Refusal("conflict: a different judgement was already recorded for this attempt")
    write_once(target, raw)
    doc = strict_json(raw, "judgement")
    qs = {"O1", "O2", "O3", "O4", "O5", "O6"}
    if not isinstance(doc, dict) or set(doc) != {"schema", "attempt_id", "reviewer", "grades", "reasons", "remediation"} \
            or doc["schema"] != "prime-boot-judgement/1" or doc["attempt_id"] != attempt.name \
            or not isinstance(doc["reviewer"], str) or not LABEL.fullmatch(doc["reviewer"]) \
            or not isinstance(doc["grades"], dict) or set(doc["grades"]) != qs or not all(g in GRADES for g in doc["grades"].values()) \
            or not isinstance(doc["reasons"], dict) or set(doc["reasons"]) != qs or not all(isinstance(r, str) for r in doc["reasons"].values()) \
            or not isinstance(doc["remediation"], list) or not all(
                isinstance(x, dict) and set(x) == {"kind", "detail"} and x["kind"] in ("reference", "question")
                and isinstance(x["detail"], str) for x in doc["remediation"]):
        raise Refusal("judgement is not prime-boot-judgement/1 for this attempt; the raw bytes are kept")
    write_once(attempt / "31.judgement.json", canonical(dict(doc, note="a supplied record from a named reviewer label; not authentication or authority")))
    prep = load_stage(attempt, "19.prepare-outcome.json")
    checks = load_stage(attempt, "22.checks.json")
    grades = set(doc["grades"].values())
    if prep["status"] == "prepared" and checks["status"] == "ok" and grades == {"pass"}:
        outcome = "oriented"
    elif prep["status"] in ("prepared", "partial") and checks["status"] == "ok" and "wrong" not in grades:
        outcome = "partial"
    else:
        outcome = "not-oriented"
    write_once(attempt / "39.outcome.json", canonical({
        "outcome": outcome, "prepare": prep["status"], "checks": checks["status"], "grades": doc["grades"],
        "remediation": doc["remediation"], "authority": AUTHORITY,
        "dependent_execution": "allowed only for already-released work" if outcome == "oriented" else "blocked",
        "read_only_investigation": "allowed and recorded separately"}))
    sys.stdout.write(f"outcome {outcome}\nauthority {AUTHORITY}\n")
    return 0 if outcome == "oriented" else 1


# ---------- show ----------

def show(attempt_text: str, as_json: bool) -> int:
    attempt = Path(attempt_text)
    if not (attempt / "00.intent.json").is_file():
        raise Refusal("not an attempt directory")
    files = sorted(p.name for p in attempt.iterdir())
    summary = {"attempt": str(attempt), "files": files}
    if (attempt / "39.outcome.json").is_file():
        summary["state"] = load_stage(attempt, "39.outcome.json")["outcome"]
    elif (attempt / "19.prepare-outcome.json").is_file():
        prep = load_stage(attempt, "19.prepare-outcome.json")["status"]
        summary["state"] = f"{prep}; not oriented (no judgement)" if prep != "failed" else "failed"
    else:
        stages = [f for f in files if re.match(r"^\d\d\.[a-z-]+\.json$", f) and not f.startswith("00.")]
        summary["state"] = f"interrupted after {stages[-1] if stages else '00.intent.json'}; not oriented"
    summary["authority"] = AUTHORITY
    sys.stdout.write(json.dumps(summary, indent=1) + "\n" if as_json else
                     f"attempt {attempt}\nstate {summary['state']}\nfiles {' '.join(files)}\nauthority {AUTHORITY}\n")
    return 0


def main(argv=None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    ap = argparse.ArgumentParser(prog="prime_boot.py")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--request", required=True)
    p.add_argument("--records", required=True)
    p.add_argument("--attempt", required=True)
    c = sub.add_parser("check")
    c.add_argument("--attempt", required=True)
    c.add_argument("--answers", required=True)
    j = sub.add_parser("judge")
    j.add_argument("--attempt", required=True)
    j.add_argument("--judgement", required=True)
    s = sub.add_parser("show")
    s.add_argument("--attempt", required=True)
    s.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        if args.command == "prepare":
            return prepare(args.request, args.records, args.attempt)
        if args.command == "check":
            return check(args.attempt, args.answers)
        if args.command == "judge":
            return judge(args.attempt, args.judgement)
        return show(args.attempt, args.json)
    except (Refusal, StageFailure) as exc:
        sys.stdout.write(f"refused: {exc}\n")
        return 2
    except OSError as exc:
        sys.stdout.write(f"refused: filesystem error: {type(exc).__name__}: {exc.strerror}\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
