"""Return-line routing and a fixture-only migration candidate.

Band 5 keeps the leading workflow-space digit and maps N5NN to N1NN.
Band 7 stays on its own page at any prefix. This tool reads the pinned
return-capture reader and does not call its sequential allocator. It does
not allocate a member and does not move a live capture.

Paths are checked with abspath. Symlinks are not followed.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import stat
import sys

ROUTE_SCHEMA = "return-placement-route/1"
RELOCATION_SCHEMA = "return-placement-relocation/1"
JOURNAL_SCHEMA = "return-placement-journal/1"
PLAN_SCHEMA = "return-placement-plan/1"
FILING_SCHEMA = "return-placement-filing-check/1"

DOOR = "0100.band.returns"
JOURNAL_NAME = "placement-journal.json"
REPARSE = 0x400
PAGE_RE_TEXT = r"^(\d{4})\.([A-Za-z0-9][A-Za-z0-9._-]{0,63})$"
ROOT_NAMES = ("01.md", "reservation.json", "manifest.json", "receipt.json", "return.md")
STATEMENT = "The sealed reservation destination was not rewritten."
MEMBER_DIR = r"^01(?:0[1-9]|[1-9][0-9])\..+"
READER_SHA256 = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
READER_BYTES = 45767
_READER = None

EXIT_OK = 0
EXIT_RECORDED = 1
EXIT_REFUSED = 2
EXIT_PARTIAL = 3


class PlacementError(Exception):
    def __init__(self, reason: str, exit_code: int = EXIT_REFUSED) -> None:
        super().__init__(reason)
        self.reason = reason
        self.exit_code = exit_code


def _norm(path: str) -> str:
    return os.path.normcase(os.path.normpath(path))


def _within(root_abs: str, path_abs: str) -> bool:
    try:
        common = os.path.commonpath([_norm(root_abs), _norm(path_abs)])
    except ValueError:
        return False
    return common == _norm(root_abs)


def _is_reparse(path: str) -> bool:
    try:
        st = os.lstat(path)
    except OSError:
        return False
    if stat.S_ISLNK(st.st_mode):
        return True
    attrs = getattr(st, "st_file_attributes", 0) or 0
    return bool(attrs & REPARSE)


def _require_no_reparse(root_abs: str, path_abs: str) -> None:
    if _is_reparse(root_abs):
        raise PlacementError("reparse point")
    rel = os.path.relpath(path_abs, root_abs)
    cur = root_abs
    if rel in (".", os.curdir):
        return
    for part in rel.split(os.sep):
        if part in ("", "."):
            continue
        cur = os.path.join(cur, part)
        if os.path.lexists(cur) and _is_reparse(cur):
            raise PlacementError("reparse point")


def require_inside(root_abs: str, path: str) -> str:
    abs_path = os.path.abspath(path)
    if not _within(root_abs, abs_path):
        raise PlacementError("path escapes fixture root")
    _require_no_reparse(root_abs, abs_path)
    return abs_path


def _posix(rel: str) -> str:
    return rel.replace("\\", "/")


def _join(root: str, rel: str) -> str:
    parts = [p for p in _posix(rel).split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        raise PlacementError("path escapes fixture root")
    return os.path.join(root, *parts) if parts else root


def _sha_file(path: str) -> tuple[str, int]:
    digest = hashlib.sha256()
    total = 0
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(65536)
            if not chunk:
                break
            digest.update(chunk)
            total += len(chunk)
    return digest.hexdigest(), total


def _sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_json(path: str) -> object:
    with open(path, "rb") as handle:
        return json.loads(handle.read().decode("utf-8"))


def _dump(obj: object) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8")


def _member_key(name: str) -> tuple:
    base = _posix(name).split("/")[-1]
    digits = base.split(".", 1)[0]
    number = int(digits) if len(digits) == 4 and digits.isdigit() else 10**9
    return (number, base, _posix(name))


def compute_route(origin: object) -> dict:
    """Return a return-placement-route/1 record or raise undeclared origin."""
    if not isinstance(origin, dict):
        raise PlacementError("undeclared origin")
    book = origin.get("book")
    page = origin.get("page")
    batch = origin.get("batch")
    if not isinstance(book, str) or not book or any(c in book for c in "/\\\n\r"):
        raise PlacementError("undeclared origin")
    if not isinstance(page, str) or not isinstance(batch, str):
        raise PlacementError("undeclared origin")
    import re
    page_m = re.fullmatch(PAGE_RE_TEXT, page)
    batch_m = re.fullmatch(r"^05\.(\d{2})$", batch)
    if page_m is None or batch_m is None:
        raise PlacementError("undeclared origin")
    page_number, subject = page_m.group(1), page_m.group(2)
    space = page_number[0]
    band = page_number[1]
    nn = page_number[2:]
    pass_nn = batch_m.group(1)
    if band == "5":
        target_number = f"{space}1{nn}"
        route_name = "matched-workflow-return-line"
        target_page = f"{target_number}.{subject}"
        pack_path = None
        review_path = None
    elif band == "7":
        target_number = page_number
        route_name = "page-local-colab"
        target_page = page
        pack_path = f"{target_page}/05.{pass_nn}.pack.md"
        review_path = f"{target_page}/06.{pass_nn}.review.md"
    else:
        raise PlacementError("undeclared origin")
    if target_number[0] != space or len(target_number) != 4:
        raise PlacementError("undeclared origin")
    if band == "5" and (target_number[1] != "1" or target_number[2:] != nn):
        raise PlacementError("undeclared origin")
    if band == "7" and target_page != page:
        raise PlacementError("undeclared origin")
    return {
        "schema": ROUTE_SCHEMA,
        "origin": {"batch": batch, "book": book, "page": page},
        "workflow_space": space,
        "page_number": page_number,
        "target_number": target_number,
        "subject": subject,
        "band": band,
        "route": route_name,
        "pass": batch,
        "target_page": target_page,
        "return_path": f"{target_page}/{batch}.return.md",
        "custody_dir": f"{target_page}/{batch}.custody",
        "pack_path": pack_path,
        "review_path": review_path,
        "sequential_allocation": False,
    }


def _reader():
    """Load the pinned return-capture reader. Do not call its allocator."""
    global _READER
    if _READER is not None:
        return _READER
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(here, "..", "return-capture-pass01", "return_capture.py"))
    if _is_reparse(path) or not os.path.isfile(path):
        raise PlacementError("pinned reader mismatch")
    digest, size = _sha_file(path)
    if digest != READER_SHA256 or size != READER_BYTES:
        raise PlacementError("pinned reader mismatch")
    spec = importlib.util.spec_from_file_location("return_capture_pinned", path)
    if spec is None or spec.loader is None:
        raise PlacementError("pinned reader mismatch")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _READER = module
    return module


def _assess_custody(member_abs: str) -> dict:
    """Read-only sealed-package check. A refusal is not a completed copy."""
    empty = {
        "custody_valid": False,
        "custody_reason": None,
        "reservation_sha256": None,
        "manifest_sha256": None,
        "receipt_sha256": None,
        "acceptance": None,
    }
    try:
        reader = _reader()
        info = reader.verify_member(reader.Path(member_abs))
    except PlacementError:
        raise
    except Exception as exc:
        reason = getattr(exc, "args", ("",))[0] if getattr(exc, "args", None) else ""
        if not isinstance(reason, str) or not reason.strip():
            reason = f"custody reader {type(exc).__name__}"
        else:
            reason = reason.strip().splitlines()[0]
        empty["custody_reason"] = reason
        return empty
    return {
        "custody_valid": True,
        "custody_reason": None,
        "reservation_sha256": info.get("reservation_sha256"),
        "manifest_sha256": info.get("manifest_sha256"),
        "receipt_sha256": info.get("receipt_sha256"),
        "acceptance": None,
    }


def _line_occupants(root_abs: str, target_number: str, target_page: str) -> list[str]:
    """Different-name directories on this exact number. A missing tail does not clear them."""
    prefix = target_number + "."
    found = []
    try:
        entries = list(os.scandir(root_abs))
    except OSError:
        return found
    for entry in entries:
        if not entry.name.startswith(prefix) or entry.name == target_page:
            continue
        try:
            if _is_reparse(entry.path) or entry.is_dir(follow_symlinks=False):
                found.append(entry.name)
        except OSError:
            continue
    found.sort()
    return found


def _overlay_route(route: dict, occupants: list[str], old_member: str, custody_valid: bool) -> dict:
    write = dict(route)
    write["final_return_path"] = route["return_path"]
    write["final_custody_dir"] = route["custody_dir"]
    write["occupants"] = list(occupants)
    write["staging_required"] = bool(occupants)
    write["retirement"] = "not performed"
    write["overwrite"] = False
    write["acceptance"] = None
    write["custody_valid"] = custody_valid
    write["line_adoption"] = False
    if occupants:
        base = f"staging/{old_member}"
        write["staging_root"] = base
        write["return_path"] = f"{base}/{route['pass']}.return.md"
        write["custody_dir"] = f"{base}/{route['pass']}.custody"
    else:
        write["staging_root"] = None
    return write


def _load_reservation(member_abs: str) -> tuple[dict | None, str | None]:
    path = os.path.join(member_abs, "reservation.json")
    if not os.path.lexists(path):
        return None, "missing reservation"
    if _is_reparse(path) or not os.path.isfile(path):
        return None, "unusable origin"
    try:
        body = _read_json(path)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None, "unusable origin"
    if not isinstance(body, dict):
        return None, "unusable origin"
    submission = body.get("submission_id")
    origin = body.get("origin")
    if not isinstance(submission, str) or not submission:
        return None, "unusable origin"
    if not isinstance(origin, dict):
        return None, "unusable origin"
    return body, None


def _scan_files(member_abs: str) -> list[dict]:
    rels: list[str] = []
    for name in ROOT_NAMES:
        path = os.path.join(member_abs, name)
        if os.path.lexists(path):
            rels.append(name)
    payload = os.path.join(member_abs, "payload")
    if os.path.lexists(payload):
        if _is_reparse(payload):
            raise PlacementError("reparse point")
        if not stat.S_ISDIR(os.lstat(payload).st_mode):
            raise PlacementError("payload is not a directory")
        for dirpath, dirnames, filenames in os.walk(payload, followlinks=False):
            kept = []
            for dirname in sorted(dirnames):
                child = os.path.join(dirpath, dirname)
                if _is_reparse(child):
                    raise PlacementError("reparse point")
                kept.append(dirname)
            dirnames[:] = kept
            for filename in sorted(filenames):
                child = os.path.join(dirpath, filename)
                rels.append(_posix(os.path.relpath(child, member_abs)))
    found = []
    for rel in rels:
        path = _join(member_abs, rel)
        if _is_reparse(path):
            raise PlacementError("reparse point")
        st = os.lstat(path)
        if not stat.S_ISREG(st.st_mode):
            raise PlacementError("not a regular file")
        if st.st_nlink > 1:
            raise PlacementError("hard link")
        digest, size = _sha_file(path)
        found.append({"rel": rel, "sha256": digest, "bytes": size})
    return found


def _identity(origin: dict, submission: str) -> dict:
    return {
        "batch": origin["batch"],
        "book": origin["book"],
        "page": origin["page"],
        "submission_id": submission,
    }


def _origin_key(identity: dict | None) -> tuple | None:
    if not identity:
        return None
    return (identity["book"], identity["page"], identity["batch"])


def _tail_action(root_abs: str, route: dict, source_files: list[dict]) -> str:
    returned = next((item for item in source_files if item["rel"] == "return.md"), None)
    if returned is None:
        return "absent"
    if route["route"] != "page-local-colab":
        return "copied"
    tail = require_inside(root_abs, _join(root_abs, route["return_path"]))
    if not os.path.lexists(tail):
        return "copied"
    if _is_reparse(tail) or not os.path.isfile(tail):
        raise PlacementError("occupied target")
    digest, size = _sha_file(tail)
    if digest == returned["sha256"] and size == returned["bytes"]:
        return "verified-equal"
    raise PlacementError("colab return differs")


def _expected_writes(root_abs: str, route: dict, source_files: list[dict], tail_action: str,
                     old_rel: str, identity: dict) -> list[dict]:
    custody = route["custody_dir"]
    ops = []
    copied = []
    for item in source_files:
        dest_rel = f"{custody}/{item['rel']}"
        ops.append({
            "dest": dest_rel,
            "sha256": item["sha256"],
            "bytes": item["bytes"],
            "role": "custody",
            "src": item["rel"],
        })
        copied.append({
            "bytes": item["bytes"],
            "path": f"{route['pass']}.custody/{item['rel']}",
            "sha256": item["sha256"],
        })
    if tail_action == "copied":
        returned = next(item for item in source_files if item["rel"] == "return.md")
        ops.append({
            "dest": route["return_path"],
            "sha256": returned["sha256"],
            "bytes": returned["bytes"],
            "role": "tail",
            "src": "return.md",
        })
        copied.append({
            "bytes": returned["bytes"],
            "path": f"{route['pass']}.return.md",
            "sha256": returned["sha256"],
        })
    will_adopt = bool(route.get("custody_valid")) and not route.get("staging_required") and tail_action not in {"absent", "conflict"}
    relocation = {
        "schema": RELOCATION_SCHEMA,
        "old_member_path": _posix(old_rel),
        "origin": route["origin"],
        "submission_id": identity["submission_id"],
        "route": route,
        "files": copied,
        "return_tail": {
            "action": tail_action,
            "path": route.get("final_return_path") or route["return_path"],
            "write_path": route["return_path"],
        },
        "reservation_destination_rewritten": False,
        "statement": STATEMENT,
        "acceptance": None,
        "approved": False,
        "accepted": False,
        "published": False,
        "custody_valid": bool(route.get("custody_valid")),
        "line_adoption": will_adopt,
        "staging_root": route.get("staging_root"),
        "retirement": "not performed",
        "overwrite": False,
    }
    payload = _dump(relocation)
    ops.append({
        "dest": f"{custody}/relocation.json",
        "sha256": _sha_bytes(payload),
        "bytes": len(payload),
        "role": "relocation",
        "src": None,
        "payload": payload,
    })
    for op in ops:
        require_inside(root_abs, _join(root_abs, op["dest"]))
    return ops


def _blank_item(prep: dict) -> dict:
    write = prep.get("write_route") or {}
    route = prep.get("route") or {}
    return {
        "source": prep["source"],
        "old_member": prep["old_member"],
        "status": prep["status"],
        "reason": prep.get("reason"),
        "identity": prep.get("identity"),
        "route": prep.get("route"),
        "source_files": prep.get("source_files") or [],
        "expected": prep.get("expected") or [],
        "written": [],
        "tail_action": prep.get("tail_action"),
        "replay": None,
        "custody_valid": prep.get("custody_valid"),
        "custody_reason": prep.get("custody_reason"),
        "acceptance": None,
        "approved": False,
        "accepted": False,
        "published": False,
        "line_adoption": False,
        "copy_progress": "none",
        "occupants": prep.get("occupants") or [],
        "staging_required": bool(prep.get("staging_required")),
        "final_return_path": route.get("return_path"),
        "write_return_path": write.get("return_path") or route.get("return_path"),
        "retirement": "not performed",
        "overwrite": False,
    }


def _journal_path(root_abs: str) -> str:
    return os.path.join(root_abs, JOURNAL_NAME)


def _save_journal(root_abs: str, journal: dict) -> None:
    path = _journal_path(root_abs)
    temporary = path + ".tmp"
    data = _dump(journal)
    with open(temporary, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def _load_journal(root_abs: str) -> dict | None:
    path = _journal_path(root_abs)
    if not os.path.lexists(path):
        return None
    if _is_reparse(path):
        raise PlacementError("reparse point")
    body = _read_json(path)
    if not isinstance(body, dict) or body.get("schema") != JOURNAL_SCHEMA:
        raise PlacementError("unusable journal")
    return body


def _recompute_complete(journal: dict) -> None:
    items = journal.get("items") or []
    sources = journal.get("sources") or []
    ok = {"placed", "verified-equal"}
    covered = {item["source"] for item in items if item.get("status") in ok}
    journal["complete"] = bool(sources) and covered == set(sources) and not journal.get("interrupted")


def _upsert(journal: dict, item: dict) -> None:
    items = journal["items"]
    for index, old in enumerate(items):
        if old["source"] == item["source"]:
            items[index] = item
            break
    else:
        items.append(item)
    items.sort(key=lambda entry: _member_key(entry["old_member"]))


def _check_root(root: str) -> str:
    root_abs = os.path.abspath(root)
    if not os.path.isdir(root_abs) or _is_reparse(root_abs):
        raise PlacementError("fixture root is not a directory")
    if os.path.isdir(os.path.join(root_abs, DOOR)) or _door_nested(root_abs):
        raise PlacementError("fixture root contains 0100.band.returns")
    return root_abs


def _door_nested(root_abs: str) -> bool:
    if os.path.isdir(os.path.join(root_abs, DOOR)):
        return True
    for dirpath, dirnames, _names in os.walk(root_abs, followlinks=False):
        if DOOR in dirnames:
            return True
        dirnames[:] = [name for name in dirnames if not _is_reparse(os.path.join(dirpath, name))]
    return False


def _prepare_one(root_abs: str, source_rel: str) -> dict:
    old_member = _posix(source_rel).split("/")[-1]
    prep = {
        "source": _posix(source_rel),
        "old_member": old_member,
        "status": "ready",
        "reason": None,
        "identity": None,
        "route": None,
        "source_files": [],
        "expected": [],
        "tail_action": None,
    }
    try:
        member_abs = require_inside(root_abs, _join(root_abs, source_rel))
        if not os.path.isdir(member_abs) or _is_reparse(member_abs):
            prep["status"] = "refused"
            prep["reason"] = "unresolved source"
            return prep
        try:
            files = _scan_files(member_abs)
        except PlacementError as exc:
            prep["status"] = "refused"
            prep["reason"] = exc.reason
            return prep
        body, problem = _load_reservation(member_abs)
        if problem:
            prep["status"] = "unresolved"
            prep["reason"] = problem
            return prep
        assert body is not None
        try:
            route = compute_route(body["origin"])
        except PlacementError as exc:
            prep["status"] = "refused"
            prep["reason"] = exc.reason
            return prep
        identity = _identity(route["origin"], body["submission_id"])
        prep["identity"] = identity
        prep["route"] = route
        prep["source_files"] = files
        custody = _assess_custody(member_abs)
        prep["custody_valid"] = custody["custody_valid"]
        prep["custody_reason"] = custody["custody_reason"]
        prep["reservation_sha256"] = custody["reservation_sha256"]
        prep["manifest_sha256"] = custody["manifest_sha256"]
        prep["receipt_sha256"] = custody["receipt_sha256"]
        occupants = _line_occupants(root_abs, route["target_number"], route["target_page"])
        prep["occupants"] = occupants
        prep["staging_required"] = bool(occupants)
        write_route = _overlay_route(route, occupants, old_member, custody["custody_valid"])
        prep["write_route"] = write_route
        try:
            if occupants and route["route"] == "page-local-colab":
                action = "copied" if any(item["rel"] == "return.md" for item in files) else "absent"
            else:
                action = _tail_action(root_abs, route, files)
        except PlacementError as exc:
            prep["status"] = "conflict"
            prep["reason"] = exc.reason
            prep["tail_action"] = "conflict"
            return prep
        prep["tail_action"] = action
        prep["expected"] = _expected_writes(root_abs, write_route, files, action, prep["source"], identity)
        return prep
    except PlacementError as exc:
        prep["status"] = "refused"
        prep["reason"] = exc.reason
        return prep


def _mark_duplicates(prepared: list[dict]) -> None:
    groups: dict[tuple, list[dict]] = {}
    for prep in prepared:
        key = _origin_key(prep.get("identity"))
        if key is None or prep["status"] != "ready":
            continue
        groups.setdefault(key, []).append(prep)
    for group in groups.values():
        if len(group) < 2:
            continue
        for prep in group:
            prep["status"] = "conflict"
            prep["reason"] = "duplicate origin pass"
            prep["expected"] = []
            prep["tail_action"] = None


def _same_files(left: list[dict], right: list[dict]) -> bool:
    def key(item: dict) -> tuple:
        return (item["rel"], item["sha256"], item["bytes"])
    return sorted(map(key, left)) == sorted(map(key, right))


def _public_expected(ops: list[dict]) -> list[dict]:
    return [
        {"bytes": op["bytes"], "dest": op["dest"], "role": op["role"], "sha256": op["sha256"]}
        for op in ops
    ]


def _occupied(root_abs: str, expected: list[dict], already: dict[str, dict]) -> str | None:
    for op in expected:
        prior = already.get(op["dest"])
        if prior and prior["sha256"] == op["sha256"] and prior["bytes"] == op["bytes"]:
            continue
        dest = _join(root_abs, op["dest"])
        if not os.path.lexists(dest):
            continue
        if _is_reparse(dest) or not os.path.isfile(dest):
            return "occupied target"
        digest, size = _sha_file(dest)
        if digest != op["sha256"] or size != op["bytes"]:
            return "occupied target"
    return None


def _write_op(root_abs: str, member_abs: str, op: dict) -> None:
    dest = require_inside(root_abs, _join(root_abs, op["dest"]))
    parent = os.path.dirname(dest)
    require_inside(root_abs, parent if os.path.isdir(parent) else os.path.dirname(parent) if parent else root_abs)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if os.path.lexists(dest):
        digest, size = _sha_file(dest)
        if digest == op["sha256"] and size == op["bytes"]:
            return
        raise PlacementError("occupied target")
    temporary = dest + ".partial"
    if op["role"] == "relocation":
        data = op["payload"]
    else:
        src = require_inside(root_abs, _join(member_abs, op["src"]))
        with open(src, "rb") as handle:
            data = handle.read()
        if _sha_bytes(data) != op["sha256"] or len(data) != op["bytes"]:
            raise PlacementError("hash mismatch")
    with open(temporary, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, dest)
    digest, size = _sha_file(dest)
    if digest != op["sha256"] or size != op["bytes"]:
        raise PlacementError("hash mismatch")


def _finish_status(prep: dict) -> str:
    if prep.get("tail_action") == "absent":
        return "incomplete"
    if not prep.get("custody_valid"):
        return "copied-incomplete"
    if prep.get("staging_required"):
        return "staged"
    if prep.get("tail_action") == "verified-equal":
        return "verified-equal"
    return "placed"


def _reason_for(status: str, prep: dict) -> str | None:
    if status == "incomplete":
        return "missing return"
    if status == "copied-incomplete":
        return prep.get("custody_reason") or "custody incomplete"
    if status == "staged":
        return "occupied line; staged; retirement not performed"
    if status == "verified-equal":
        return "existing return matches; not rewritten"
    if status == "placed":
        return None
    return prep.get("reason")


def _annotate_finish(item: dict, prep: dict) -> None:
    status = _finish_status(prep)
    item["status"] = status
    item["reason"] = _reason_for(status, prep)
    item["custody_valid"] = bool(prep.get("custody_valid"))
    item["custody_reason"] = prep.get("custody_reason")
    item["acceptance"] = None
    item["approved"] = False
    item["accepted"] = False
    item["published"] = False
    item["line_adoption"] = status in {"placed", "verified-equal"}
    item["retirement"] = "not performed"
    item["overwrite"] = False
    if status == "staged":
        item["copy_progress"] = "staged"
    elif status == "verified-equal":
        item["copy_progress"] = "verified-equal"
    elif status in {"placed", "incomplete", "copied-incomplete"}:
        item["copy_progress"] = "copied"
    else:
        item["copy_progress"] = "none"


def _verify_written(root_abs: str, written: list[dict]) -> str | None:
    for record in written:
        dest = _join(root_abs, record["dest"])
        if not os.path.isfile(dest) or _is_reparse(dest):
            return "hash mismatch"
        digest, size = _sha_file(dest)
        if digest != record["sha256"] or size != record["bytes"]:
            return "hash mismatch"
    return None


def _apply_prepared(root_abs: str, journal: dict, prepared: list[dict], interrupt_after: int | None) -> int:
    copies = 0
    refused_replay = False
    by_source = {item["source"]: item for item in journal["items"]}
    for prep in prepared:
        current = by_source.get(prep["source"])
        if current and current.get("status") in {"placed", "verified-equal", "incomplete", "copied-incomplete", "staged"}:
            if not _same_files(current.get("source_files") or [], prep.get("source_files") or []):
                current["replay"] = "refused"
                current["replay_reason"] = "changed content under the same identity"
                refused_replay = True
                _upsert(journal, current)
                _save_journal(root_abs, journal)
                continue
            if prep["status"] == "conflict":
                current["status"] = "conflict"
                current["reason"] = prep.get("reason")
                current["replay"] = "refused"
                refused_replay = True
                _upsert(journal, current)
                _recompute_complete(journal)
                _save_journal(root_abs, journal)
                continue
            problem = _verify_written(root_abs, current.get("written") or [])
            if problem:
                current["status"] = "mismatch"
                current["reason"] = problem
                journal["interrupted"] = False
                _recompute_complete(journal)
                _upsert(journal, current)
                _save_journal(root_abs, journal)
                return EXIT_REFUSED
            if current.get("status") in {"placed", "verified-equal"}:
                current["replay"] = "already-placed"
            else:
                current["replay"] = "already-recorded"
            _upsert(journal, current)
            by_source[prep["source"]] = current
            continue
        if prep["status"] != "ready":
            item = _blank_item(prep)
            item["written"] = []
            _upsert(journal, item)
            by_source[prep["source"]] = item
            journal["interrupted"] = False
            _recompute_complete(journal)
            _save_journal(root_abs, journal)
            continue
        if current and current.get("status") == "interrupted":
            if not _same_files(current.get("source_files") or [], prep.get("source_files") or []):
                current["status"] = "refused"
                current["reason"] = "changed content under the same identity"
                current["replay"] = "refused"
                refused_replay = True
                _upsert(journal, current)
                _save_journal(root_abs, journal)
                continue
            problem = _verify_written(root_abs, current.get("written") or [])
            if problem:
                current["status"] = "mismatch"
                current["reason"] = problem
                _recompute_complete(journal)
                _upsert(journal, current)
                _save_journal(root_abs, journal)
                return EXIT_REFUSED
            item = current
        else:
            item = _blank_item(prep)
            item["status"] = "interrupted"
            item["expected"] = _public_expected(prep["expected"])
        already = {record["dest"]: record for record in item.get("written") or []}
        problem = _occupied(root_abs, prep["expected"], already)
        if problem and not already:
            item["status"] = "conflict"
            item["reason"] = problem
            item["expected"] = []
            _upsert(journal, item)
            by_source[prep["source"]] = item
            _recompute_complete(journal)
            _save_journal(root_abs, journal)
            continue
        if problem:
            item["status"] = "conflict"
            item["reason"] = problem
            _upsert(journal, item)
            _recompute_complete(journal)
            _save_journal(root_abs, journal)
            continue
        member_abs = require_inside(root_abs, _join(root_abs, prep["source"]))
        stopped = False
        for op in prep["expected"]:
            prior = already.get(op["dest"])
            if prior:
                continue
            if interrupt_after is not None and copies >= interrupt_after:
                item["status"] = "interrupted"
                item["reason"] = "interrupted"
                journal["interrupted"] = True
                _upsert(journal, item)
                _recompute_complete(journal)
                _save_journal(root_abs, journal)
                stopped = True
                break
            dest = _join(root_abs, op["dest"])
            existed = os.path.isfile(dest) and not _is_reparse(dest)
            try:
                _write_op(root_abs, member_abs, op)
            except PlacementError as exc:
                item["status"] = "conflict" if exc.reason == "occupied target" else "mismatch"
                item["reason"] = exc.reason
                _upsert(journal, item)
                _recompute_complete(journal)
                _save_journal(root_abs, journal)
                return EXIT_REFUSED if exc.reason == "hash mismatch" else EXIT_RECORDED
            created = not existed
            record = {
                "bytes": op["bytes"],
                "created": created,
                "dest": op["dest"],
                "role": op["role"],
                "sha256": op["sha256"],
            }
            item.setdefault("written", []).append(record)
            already[op["dest"]] = record
            if created:
                copies += 1
            item["status"] = "interrupted"
            journal["interrupted"] = True
            _upsert(journal, item)
            by_source[prep["source"]] = item
            _recompute_complete(journal)
            _save_journal(root_abs, journal)
        if stopped:
            return EXIT_PARTIAL
        if interrupt_after is not None and copies >= interrupt_after and _work_remains(prepared, by_source, prep["source"]):
            _annotate_finish(item, prep)
            journal["interrupted"] = True
            _upsert(journal, item)
            _recompute_complete(journal)
            _save_journal(root_abs, journal)
            return EXIT_PARTIAL
        _annotate_finish(item, prep)
        item["replay"] = None
        _upsert(journal, item)
        by_source[prep["source"]] = item
        journal["interrupted"] = False
        _recompute_complete(journal)
        _save_journal(root_abs, journal)
    journal["interrupted"] = False
    _recompute_complete(journal)
    _save_journal(root_abs, journal)
    if refused_replay:
        return EXIT_REFUSED
    return _exit_for(journal)


def _work_remains(prepared: list[dict], by_source: dict, current_source: str) -> bool:
    seen = False
    for prep in prepared:
        if prep["source"] == current_source:
            seen = True
            continue
        if not seen:
            continue
        item = by_source.get(prep["source"])
        if item is None or item.get("status") == "interrupted":
            return True
    return False


def _exit_for(journal: dict) -> int:
    if journal.get("interrupted"):
        return EXIT_PARTIAL
    if journal.get("complete"):
        return EXIT_OK
    statuses = [item.get("status") for item in journal.get("items") or []]
    if statuses and all(status in {"refused", "mismatch"} for status in statuses):
        return EXIT_REFUSED
    return EXIT_RECORDED


def _result(root_abs: str, journal: dict, code: int) -> dict:
    return {
        "complete": bool(journal.get("complete")),
        "exit": code,
        "items": [
            {
                "old_member": item["old_member"],
                "acceptance": None,
                "approved": False,
                "accepted": False,
                "published": False,
                "copy_progress": item.get("copy_progress"),
                "custody_valid": item.get("custody_valid"),
                "line_adoption": bool(item.get("line_adoption")),
                "reason": item.get("reason"),
                "replay": item.get("replay"),
                "return_path": (item.get("route") or {}).get("return_path"),
                "status": item.get("status"),
            }
            for item in journal.get("items") or []
        ],
        "journal": _posix(os.path.relpath(_journal_path(root_abs), root_abs)),
    }


def apply_run(root: str, sources: list[str], interrupt_after: int | None = None) -> dict:
    if interrupt_after is not None and interrupt_after < 0:
        raise PlacementError("interrupt-after must be >= 0")
    root_abs = _check_root(root)
    rels = []
    for source in sources:
        abs_source = os.path.abspath(source)
        if not _within(root_abs, abs_source):
            raise PlacementError("path escapes fixture root")
        rels.append(_posix(os.path.relpath(abs_source, root_abs)))
    rels = sorted(set(rels), key=_member_key)
    journal = _load_journal(root_abs)
    if journal is None:
        journal = {
            "schema": JOURNAL_SCHEMA,
            "complete": False,
            "interrupted": False,
            "sources": rels,
            "items": [],
        }
        _save_journal(root_abs, journal)
    elif list(journal.get("sources") or []) != rels:
        raise PlacementError("journal sources differ")
    prepared = [_prepare_one(root_abs, rel) for rel in rels]
    _mark_duplicates(prepared)
    code = _apply_prepared(root_abs, journal, prepared, interrupt_after)
    journal = _load_journal(root_abs) or journal
    return _result(root_abs, journal, code)


def resume_run(root: str, interrupt_after: int | None = None) -> dict:
    root_abs = _check_root(root)
    journal = _load_journal(root_abs)
    if journal is None:
        raise PlacementError("missing journal")
    sources = [ _join(root_abs, rel) for rel in journal.get("sources") or [] ]
    return apply_run(root_abs, sources, interrupt_after)


def _prune_empty(root_abs: str, start_file: str) -> None:
    cur = os.path.dirname(start_file)
    while _within(root_abs, cur) and _norm(cur) != _norm(root_abs):
        try:
            if os.listdir(cur):
                return
            os.rmdir(cur)
        except OSError:
            return
        cur = os.path.dirname(cur)


def rollback_run(root: str) -> dict:
    root_abs = _check_root(root)
    journal = _load_journal(root_abs)
    if journal is None:
        raise PlacementError("missing journal")
    created = []
    for item in journal.get("items") or []:
        for record in item.get("written") or []:
            if record.get("created"):
                created.append(record)
    for record in created:
        dest = require_inside(root_abs, _join(root_abs, record["dest"]))
        if not os.path.lexists(dest):
            continue
        if _is_reparse(dest) or not os.path.isfile(dest):
            raise PlacementError("hash mismatch")
        digest, size = _sha_file(dest)
        if digest != record["sha256"] or size != record["bytes"]:
            raise PlacementError("hash mismatch")
    for record in created:
        dest = require_inside(root_abs, _join(root_abs, record["dest"]))
        if os.path.isfile(dest):
            os.remove(dest)
            _prune_empty(root_abs, dest)
    for item in journal.get("items") or []:
        item["written"] = [record for record in item.get("written") or [] if not record.get("created")]
        if item.get("status") in {"placed", "verified-equal", "incomplete", "copied-incomplete", "staged", "interrupted"}:
            item["status"] = "rolled-back"
            item["reason"] = "rolled back"
    journal["complete"] = False
    journal["interrupted"] = False
    journal["rolled_back"] = True
    _save_journal(root_abs, journal)
    return _result(root_abs, journal, EXIT_OK)


def lookup_run(root: str, member: str | None = None, page: str | None = None,
               batch: str | None = None, return_path: str | None = None) -> dict:
    if not any((member, page, batch, return_path)):
        raise PlacementError("lookup needs a member, page, batch, or return path")
    root_abs = _check_root(root)
    journal = _load_journal(root_abs)
    if journal is None:
        raise PlacementError("missing journal")
    want_return = _posix(return_path) if return_path else None
    found = []
    for item in journal.get("items") or []:
        identity = item.get("identity") or {}
        route = item.get("route") or {}
        if member and item.get("old_member") != member and item.get("source") != _posix(member):
            continue
        if page and identity.get("page") != page:
            continue
        if batch and identity.get("batch") != batch:
            continue
        paths = {
            _posix(route.get("return_path") or ""),
            _posix(item.get("final_return_path") or ""),
            _posix(item.get("write_return_path") or ""),
        }
        if want_return and want_return not in paths:
            continue
        if member or page or batch or want_return:
            if member and item.get("old_member") != member and item.get("source") != _posix(member):
                continue
            found.append(item)
    return {
        "schema": "return-placement-lookup/1",
        "complete": bool(journal.get("complete")),
        "count": len(found),
        "items": found,
    }


def filing_check(book: str, page: str) -> dict:
    import re
    match = re.fullmatch(PAGE_RE_TEXT, page)
    if match is None:
        raise PlacementError("undeclared origin")
    number = match.group(1)
    book_abs = os.path.abspath(book)
    if not os.path.isdir(book_abs) or _is_reparse(book_abs):
        raise PlacementError("book is not a directory")
    blockers = []
    prefix = number + "."
    with os.scandir(book_abs) as entries:
        for entry in entries:
            try:
                if _is_reparse(entry.path):
                    if entry.name.startswith(prefix):
                        blockers.append(entry.name)
                    continue
                if entry.is_dir(follow_symlinks=False) and entry.name.startswith(prefix) and entry.name != page:
                    blockers.append(entry.name)
            except OSError:
                continue
    blockers.sort()
    return {
        "schema": FILING_SCHEMA,
        "page": page,
        "number": number,
        "allowed": not blockers,
        "blockers": blockers,
        "creates": False,
    }


def _audit_member(path: str, names: set[str]) -> tuple[str | None, str | None]:
    norm = path.replace("\\", "/")
    for name in names:
        token = name + "/"
        index = norm.find(token)
        if index == 0 or (index > 0 and norm[index - 1] == "/"):
            return name, norm[index + len(token):]
    return None, None


def _guard_out(book: str, audit_path: str, out_path: str) -> str:
    import re
    book_abs = os.path.abspath(book)
    out_abs = os.path.abspath(out_path)
    audit_abs = os.path.abspath(audit_path)
    if _norm(out_abs) == _norm(audit_abs):
        raise PlacementError("refusing to overwrite the audit")
    if _within(book_abs, out_abs):
        rel = _posix(os.path.relpath(out_abs, book_abs))
        for part in rel.split("/"):
            if re.fullmatch(MEMBER_DIR, part):
                raise PlacementError("refusing to write inside a capture member")
    parent = os.path.dirname(out_abs)
    if parent and not os.path.isdir(parent):
        if _within(book_abs, parent):
            rel_parent = _posix(os.path.relpath(parent, book_abs))
            for part in rel_parent.split("/"):
                if re.fullmatch(MEMBER_DIR, part):
                    raise PlacementError("refusing to write inside a capture member")
        os.makedirs(parent, exist_ok=True)
    return out_abs


def build_plan(book: str, audit_path: str) -> dict:
    import re
    book_abs = os.path.abspath(book)
    audit_abs = os.path.abspath(audit_path)
    if not os.path.isdir(book_abs) or _is_reparse(book_abs):
        raise PlacementError("book is not a directory")
    if _is_reparse(audit_abs) or not os.path.isfile(audit_abs):
        raise PlacementError("audit is not a file")
    audit_sha, audit_size = _sha_file(audit_abs)
    audit = _read_json(audit_abs)
    if not isinstance(audit, dict) or not isinstance(audit.get("records"), list):
        raise PlacementError("unusable audit")
    if not isinstance(audit.get("files"), list):
        raise PlacementError("unusable audit")
    records = list(audit["records"])
    names = [record.get("old_member") for record in records if isinstance(record, dict)]
    name_set = {name for name in names if isinstance(name, str)}
    grouped: dict[str, list[dict]] = {name: [] for name in name_set}
    changes = []
    for entry in audit["files"]:
        if not isinstance(entry, dict) or not isinstance(entry.get("path"), str):
            continue
        member, rel = _audit_member(entry["path"], name_set)
        if member is None or rel is None:
            changes.append({
                "audit_bytes": entry.get("bytes"),
                "audit_path": entry["path"].replace("\\", "/"),
                "audit_sha256": entry.get("sha256"),
                "book_path": None,
                "kind": "unassigned",
                "live_bytes": None,
                "live_sha256": None,
            })
            continue
        grouped[member].append({
            "audit_bytes": entry.get("bytes"),
            "audit_path": entry["path"].replace("\\", "/"),
            "audit_sha256": entry.get("sha256"),
            "rel": rel,
        })
    directory_names = []
    with os.scandir(book_abs) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                directory_names.append(entry.name)
    directory_names.sort()
    live_members = [name for name in directory_names if re.fullmatch(MEMBER_DIR, name)]
    live_members.sort(key=_member_key)
    items = []
    unresolved = []
    for record in sorted((r for r in records if isinstance(r, dict)), key=lambda r: _member_key(str(r.get("old_member") or ""))):
        old = record.get("old_member")
        origin = record.get("origin")
        item = {
            "old_member": old,
            "origin": origin if isinstance(origin, dict) else None,
            "submission": record.get("submission"),
            "audit_route": record.get("route"),
            "audit_status": record.get("status"),
            "audit_target_return": record.get("target_return"),
            "has_receipt": record.get("has_receipt"),
            "verify_exit_pinned": record.get("verify_exit"),
            "verify_reexecuted": False,
            "route": None,
            "proposed_return_path": None,
            "proposed_custody_dir": None,
            "status": "unresolved",
            "files": [],
            "local_return": None,
            "number_neighbors": [],
            "verify_applies": False,
        }
        try:
            route = compute_route(origin)
        except PlacementError as exc:
            item["status"] = "refused" if exc.reason == "undeclared origin" else "unresolved"
            item["reason"] = exc.reason
            unresolved.append({"old_member": old, "reason": exc.reason})
            items.append(item)
            continue
        item["route"] = route
        item["proposed_return_path"] = route["return_path"]
        item["proposed_custody_dir"] = route["custody_dir"]
        if route["return_path"] != record.get("target_return") or route["route"] != record.get("route"):
            changes.append({
                "kind": "route-disagreement",
                "old_member": old,
                "audit_route": record.get("route"),
                "audit_target_return": record.get("target_return"),
                "computed_route": route["route"],
                "computed_return": route["return_path"],
            })
        member_dir = os.path.join(book_abs, old) if isinstance(old, str) else ""
        files_out = []
        matched = True
        present_rels = set()
        if not isinstance(old, str) or not os.path.isdir(member_dir):
            item["status"] = "unresolved"
            item["reason"] = "missing member"
            unresolved.append({"old_member": old, "reason": "missing member"})
            matched = False
        for audited in grouped.get(old, []):
            present_rels.add(audited["rel"])
            live_path = os.path.join(member_dir, *audited["rel"].split("/")) if member_dir else ""
            row = {
                "audit_bytes": audited["audit_bytes"],
                "audit_path": audited["audit_path"],
                "audit_sha256": audited["audit_sha256"],
                "book_path": f"{old}/{audited['rel']}" if isinstance(old, str) else None,
                "live_bytes": None,
                "live_sha256": None,
                "match": False,
            }
            if not live_path or not os.path.lexists(live_path) or _is_reparse(live_path) or not os.path.isfile(live_path):
                matched = False
                changes.append({
                    "audit_bytes": audited["audit_bytes"],
                    "audit_path": audited["audit_path"],
                    "audit_sha256": audited["audit_sha256"],
                    "book_path": row["book_path"],
                    "kind": "reparse" if live_path and os.path.lexists(live_path) and _is_reparse(live_path) else "missing",
                    "live_bytes": None,
                    "live_sha256": None,
                })
            else:
                digest, size = _sha_file(live_path)
                row["live_sha256"] = digest
                row["live_bytes"] = size
                row["match"] = digest == audited["audit_sha256"] and size == audited["audit_bytes"]
                if not row["match"]:
                    matched = False
                    changes.append({
                        "audit_bytes": audited["audit_bytes"],
                        "audit_path": audited["audit_path"],
                        "audit_sha256": audited["audit_sha256"],
                        "book_path": row["book_path"],
                        "kind": "changed",
                        "live_bytes": size,
                        "live_sha256": digest,
                    })
            files_out.append(row)
        if isinstance(old, str) and os.path.isdir(member_dir):
            for dirpath, dirnames, filenames in os.walk(member_dir, followlinks=False):
                kept = []
                for dirname in dirnames:
                    child = os.path.join(dirpath, dirname)
                    if _is_reparse(child):
                        rel = _posix(os.path.relpath(child, member_dir))
                        changes.append({
                            "audit_bytes": None,
                            "audit_path": None,
                            "audit_sha256": None,
                            "book_path": f"{old}/{rel}",
                            "kind": "reparse",
                            "live_bytes": None,
                            "live_sha256": None,
                        })
                        continue
                    kept.append(dirname)
                dirnames[:] = kept
                for filename in filenames:
                    child = os.path.join(dirpath, filename)
                    rel = _posix(os.path.relpath(child, member_dir))
                    if rel in present_rels:
                        continue
                    if _is_reparse(child) or not os.path.isfile(child):
                        changes.append({
                            "book_path": f"{old}/{rel}",
                            "kind": "reparse",
                            "audit_path": None,
                            "audit_sha256": None,
                            "audit_bytes": None,
                            "live_sha256": None,
                            "live_bytes": None,
                        })
                        continue
                    digest, size = _sha_file(child)
                    changes.append({
                        "audit_bytes": None,
                        "audit_path": None,
                        "audit_sha256": None,
                        "book_path": f"{old}/{rel}",
                        "kind": "extra",
                        "live_bytes": size,
                        "live_sha256": digest,
                    })
        item["files"] = files_out
        return_row = next((row for row in files_out if row.get("book_path") and str(row["book_path"]).endswith("/return.md")), None)
        if route["route"] == "page-local-colab":
            tail_rel = route["return_path"]
            tail_abs = os.path.join(book_abs, *tail_rel.split("/"))
            local = {
                "path": tail_rel,
                "present": False,
                "equal": False,
                "live_sha256": None,
                "live_bytes": None,
                "captured_return_sha256": None if return_row is None else return_row.get("live_sha256"),
                "captured_return_bytes": None if return_row is None else return_row.get("live_bytes"),
                "action": "verify-not-overwrite",
            }
            if os.path.lexists(tail_abs) and not _is_reparse(tail_abs) and os.path.isfile(tail_abs):
                digest, size = _sha_file(tail_abs)
                local["present"] = True
                local["live_sha256"] = digest
                local["live_bytes"] = size
                local["equal"] = (
                    return_row is not None
                    and digest == return_row.get("live_sha256")
                    and size == return_row.get("live_bytes")
                    and return_row.get("match") is True
                )
                if not local["equal"]:
                    changes.append({
                        "kind": "local-return-differs",
                        "book_path": tail_rel,
                        "live_sha256": digest,
                        "live_bytes": size,
                        "captured_return_sha256": local["captured_return_sha256"],
                        "old_member": old,
                    })
            elif return_row is not None and return_row.get("match"):
                local["action"] = "absent"
            item["local_return"] = local
        target_number = route["target_number"]
        occupants = sorted(
            name for name in directory_names
            if name.startswith(target_number + ".") and name != route["target_page"]
        )
        item["number_neighbors"] = occupants
        custody = {
            "custody_valid": False,
            "custody_reason": None,
            "reservation_sha256": None,
            "manifest_sha256": None,
            "receipt_sha256": None,
            "acceptance": None,
        }
        if isinstance(old, str) and member_dir and os.path.isdir(member_dir) and not _is_reparse(member_dir):
            custody = _assess_custody(member_dir)
            item["verify_reexecuted"] = True
        item["custody_valid"] = custody["custody_valid"]
        item["custody_reason"] = custody["custody_reason"]
        item["acceptance"] = None
        item["reservation_sha256"] = custody["reservation_sha256"]
        item["manifest_sha256"] = custody["manifest_sha256"]
        item["receipt_sha256"] = custody["receipt_sha256"]
        item["occupancy"] = {
            "adoption_blocked": bool(occupants) or not custody["custody_valid"],
            "line_adoption": False,
            "number": target_number,
            "occupants": occupants,
            "overwrite": False,
            "retirement": "not performed",
            "staging_required": bool(occupants),
            "target_page": route["target_page"],
        }
        if item.get("reason") == "missing member":
            items.append(item)
            continue
        if return_row is None:
            item["status"] = "incomplete"
            item["reason"] = "missing return"
        elif route["route"] == "page-local-colab" and item["local_return"]["present"] and not item["local_return"]["equal"]:
            item["status"] = "conflict"
            item["reason"] = "colab return differs"
        elif route["route"] == "page-local-colab" and item["local_return"]["present"] and item["local_return"]["equal"]:
            item["status"] = "verified-equal"
            item["reason"] = "existing return matches; not rewritten"
        elif not matched:
            item["status"] = "changed"
            item["reason"] = "bytes differ from the pinned audit"
        else:
            item["status"] = "planned"
            item["reason"] = None
        if item["status"] in {"planned", "verified-equal"} and not custody["custody_valid"]:
            item["status"] = "custody-invalid"
            item["reason"] = custody["custody_reason"] or "custody incomplete"
        item["occupancy"]["adoption_blocked"] = bool(occupants) or not custody["custody_valid"] or item["status"] not in {"planned", "verified-equal"}
        item["verify_applies"] = bool(matched and item["status"] in {"planned", "verified-equal", "incomplete"})
        if item["status"] == "incomplete":
            item["verify_applies"] = bool(matched)
        items.append(item)
    collisions = []
    raw_cross = audit.get("cross-source_collisions") or {}
    if raw_cross:
        collisions.append({"kind": "audit-cross-source", "value": raw_cross})
    by_return: dict[str, list[str]] = {}
    for item in items:
        path = item.get("proposed_return_path")
        if path:
            by_return.setdefault(path, []).append(item.get("old_member"))
    for path, members in sorted(by_return.items()):
        if len(members) > 1:
            collisions.append({"kind": "shared-return-path", "return_path": path, "old_members": members})
    for item in items:
        local = item.get("local_return")
        if local and local.get("present") and not local.get("equal"):
            collisions.append({
                "kind": "occupied-return",
                "return_path": local["path"],
                "old_member": item["old_member"],
            })
        elif item.get("proposed_return_path") and item.get("route", {}) and item["route"]["route"] != "page-local-colab":
            tail_abs = os.path.join(book_abs, *item["proposed_return_path"].split("/"))
            if os.path.lexists(tail_abs):
                collisions.append({
                    "kind": "occupied-return",
                    "return_path": item["proposed_return_path"],
                    "old_member": item["old_member"],
                })
    occupancy_conflicts = []
    by_target: dict[str, dict] = {}
    for item in items:
        occ = item.get("occupancy") or {}
        if not occ.get("occupants"):
            continue
        key = occ["target_page"]
        row = by_target.get(key)
        if row is None:
            row = {
                "kind": "occupied-line",
                "line_adoption": False,
                "number": occ["number"],
                "occupants": occ["occupants"],
                "overwrite": False,
                "retirement": "not performed",
                "sources": [],
                "staging_required": True,
                "target_page": key,
            }
            by_target[key] = row
            occupancy_conflicts.append(row)
        row["sources"].append(item.get("old_member"))
    for row in occupancy_conflicts:
        collisions.append({
            "kind": "occupied-line",
            "number": row["number"],
            "occupants": row["occupants"],
            "old_members": list(row["sources"]),
            "overwrite": False,
            "retirement": "not performed",
            "staging_required": True,
            "target_page": row["target_page"],
        })
    filing = filing_check(book_abs, "0121.return-placement")
    dirs_0184 = []
    with os.scandir(book_abs) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False) and entry.name.startswith("0184."):
                dirs_0184.append(entry.name)
    missing_audited = sorted(name for name in name_set if name not in set(live_members))
    extra_live = sorted((name for name in live_members if name not in name_set), key=_member_key)
    changes.sort(key=lambda row: (str(row.get("book_path") or ""), str(row.get("kind") or "")))
    return {
        "schema": PLAN_SCHEMA,
        "live_moves": False,
        "order": "ascending old member",
        "audit_schema": audit.get("schema"),
        "audit_sha256": audit_sha,
        "audit_bytes": audit_size,
        "rule_source": audit.get("rule_source"),
        "verify_reexecuted": True,
        "lowest_capture": items[0]["old_member"] if items else None,
        "item_count": len(items),
        "items": items,
        "changes_since_audit": changes,
        "unresolved": unresolved,
        "collisions": collisions,
        "occupancy_conflicts": occupancy_conflicts,
        "occupancy_conflict_count": len(occupancy_conflicts),
        "members_not_in_audit": extra_live,
        "audit_members_missing": missing_audited,
        "directories_0184": sorted(dirs_0184),
        "filing_0121": filing,
        "preconditions": [
            "Do not call return_capture.py reserve.",
            "Do not allocate 0184. 0184 is not a destination.",
            "0121.return-placement is unused until 0121.archive-resolution-0508 has been migrated and, after Prime acceptance, retired.",
            "Sequential reserve is not retired. Historical return-capture/1 reads stay available.",
            "This plan performs no live moves and does not create member directories.",
            "The pinned reader re-executed a read-only custody check on each present member. A matching file hash is not custody. custody_valid, copy progress, and acceptance are separate. Acceptance is null.",
            "An occupied target number is listed for staging. Retirement is not performed. The final page is not created beside another active name.",
        ],
    }


def verify_run(root: str) -> dict:
    root_abs = _check_root(root)
    journal = _load_journal(root_abs)
    if journal is None:
        raise PlacementError("missing journal")
    problems = []
    for item in journal.get("items") or []:
        problem = _verify_written(root_abs, item.get("written") or [])
        if problem:
            problems.append({"old_member": item.get("old_member"), "reason": problem})
    return {
        "schema": "return-placement-verify/1",
        "complete": bool(journal.get("complete")) and not problems,
        "problems": problems,
        "exit": EXIT_OK if journal.get("complete") and not problems else (EXIT_REFUSED if problems else EXIT_RECORDED),
    }


def _print(obj: object) -> None:
    sys.stdout.write(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute a return line and rehearse migration in a fixture.")
    sub = parser.add_subparsers(dest="command", required=True)
    route = sub.add_parser("route")
    route.add_argument("--book")
    route.add_argument("--page")
    route.add_argument("--batch")
    route.add_argument("--reservation")
    plan = sub.add_parser("plan")
    plan.add_argument("--book", required=True)
    plan.add_argument("--audit", required=True)
    plan.add_argument("--out", required=True)
    apply_p = sub.add_parser("apply")
    apply_p.add_argument("--root", required=True)
    apply_p.add_argument("--source", action="append", required=True)
    apply_p.add_argument("--interrupt-after", type=int)
    resume_p = sub.add_parser("resume")
    resume_p.add_argument("--root", required=True)
    resume_p.add_argument("--interrupt-after", type=int)
    roll = sub.add_parser("rollback")
    roll.add_argument("--root", required=True)
    look = sub.add_parser("lookup")
    look.add_argument("--root", required=True)
    look.add_argument("--member")
    look.add_argument("--page")
    look.add_argument("--batch")
    look.add_argument("--return")
    filing = sub.add_parser("filing-check")
    filing.add_argument("--book", required=True)
    filing.add_argument("--page", required=True)
    verify_p = sub.add_parser("verify")
    verify_p.add_argument("--root", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "route":
            if args.reservation:
                body = _read_json(os.path.abspath(args.reservation))
                if not isinstance(body, dict):
                    raise PlacementError("unusable origin")
                _print(compute_route(body.get("origin")))
            else:
                _print(compute_route({"book": args.book, "page": args.page, "batch": args.batch}))
            return EXIT_OK
        if args.command == "plan":
            body = build_plan(args.book, args.audit)
            out_abs = _guard_out(args.book, args.audit, args.out)
            data = _dump(body)
            temporary = out_abs + ".tmp"
            with open(temporary, "wb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, out_abs)
            _print({
                "bytes": len(data),
                "changes": len(body["changes_since_audit"]),
                "collisions": len(body["collisions"]),
                "exit": EXIT_OK,
                "occupancy_conflicts": body["occupancy_conflict_count"],
                "items": body["item_count"],
                "live_moves": False,
                "lowest_capture": body["lowest_capture"],
                "schema": PLAN_SCHEMA,
                "sha256": _sha_bytes(data),
                "unresolved": len(body["unresolved"]),
                "wrote": out_abs,
            })
            return EXIT_OK
        if args.command == "apply":
            result = apply_run(args.root, args.source, args.interrupt_after)
            _print(result)
            return int(result["exit"])
        if args.command == "resume":
            result = resume_run(args.root, args.interrupt_after)
            _print(result)
            return int(result["exit"])
        if args.command == "rollback":
            result = rollback_run(args.root)
            _print(result)
            return int(result["exit"])
        if args.command == "lookup":
            found = lookup_run(args.root, args.member, args.page, args.batch, getattr(args, "return"))
            _print(found)
            return EXIT_OK if found["count"] else EXIT_REFUSED
        if args.command == "filing-check":
            found = filing_check(args.book, args.page)
            _print(found)
            return EXIT_OK if found["allowed"] else EXIT_REFUSED
        if args.command == "verify":
            found = verify_run(args.root)
            _print(found)
            return int(found["exit"])
    except PlacementError as exc:
        sys.stderr.write(exc.reason + "\n")
        return exc.exit_code
    return EXIT_REFUSED


if __name__ == "__main__":
    sys.exit(main())
