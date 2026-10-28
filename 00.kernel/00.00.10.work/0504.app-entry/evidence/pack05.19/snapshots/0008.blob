#!/usr/bin/env python3
"""Fixture-only connection from one Clerk claim to one worker delivery.

The caller supplies the claim, the link, the actor, and the container.
This module does not queue, choose a route, call a model, or invoke a reviewer.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import stat
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

INSPECTION_SCHEMA = "clerk-handoff-inspection/2"
SEAM_SCHEMA = "librarian-clerk-seam"
LINK_SCHEMA = "librarian-clerk-link"
SEAM_KEYS = ("schema", "version", "clerk_path", "clerk_sha256")
LINK_KEYS = (
    "schema",
    "version",
    "delivery_id",
    "clerk_store",
    "clerk_job_id",
    "bridge_job",
    "bridge_job_sha256",
)
INTERRUPTS = ("before-launch", "before-copy", "before-return", "before-report")
IO_FAULTS = ("create", "write", "flush", "fsync", "read-back", "clerk-oserror", "clerk-timeout")
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
NAME = __import__("re").compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
HEX64 = __import__("re").compile(r"^[0-9a-f]{64}$")
TOKEN = __import__("re").compile(r"^[0-9a-f]{32}$")


class SeamResult:
    def __init__(self, code: int, text: str) -> None:
        self.code = code
        self.text = text if text.endswith("\n") else text + "\n"


class _CopyFault:
    def __init__(self, boundary: str, wrote: str, extra: str) -> None:
        self.boundary = boundary
        self.wrote = wrote
        self.extra = extra


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _linked(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def _lexists(path: Path) -> bool:
    return os.path.lexists(path)


def _pairs(context, pairs: list) -> dict:
    found = {}
    for key, value in pairs:
        if key in found:
            context.stop(f"repeats a key: {key}")
        found[key] = value
    return found


def _load_json(context, path: Path, kind: str) -> dict:
    if _linked(path) or not path.is_file():
        context.stop(f"{kind} is missing")
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeError:
        context.stop(f"{kind} is not utf-8")
    if text.startswith("\ufeff") or "\r" in text:
        context.stop(f"{kind} is not lf json")
    try:
        value = json.loads(text, object_pairs_hook=lambda pairs: _pairs(context, pairs))
    except context.Stop:
        raise
    except json.JSONDecodeError:
        context.stop(f"{kind} is not json")
    if not isinstance(value, dict):
        context.stop(f"{kind} is not an object")
    return value


def _exact(context, value: dict, keys: tuple[str, ...], kind: str) -> None:
    missing = [key for key in keys if key not in value]
    if missing:
        context.stop(f"{kind} misses keys: {', '.join(missing)}")
    unknown = [key for key in value if key not in keys]
    if unknown:
        context.stop(f"{kind} has an unknown key: {unknown[0]}")


def _version(context, value: dict, kind: str) -> None:
    got = value.get("version")
    if isinstance(got, bool) or not isinstance(got, int) or got != 1:
        context.stop(f"{kind} version is not 1")


def _simple_name(name: object) -> bool:
    return isinstance(name, str) and bool(NAME.fullmatch(name)) and name not in (".", "..")


def _load_bridge(code_root: Path):
    path = code_root / "app" / "worker_bridge.py"
    spec = importlib.util.spec_from_file_location("librarian_clerk_seam_bridge", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _pin_clerk(context, code_root: Path) -> Path:
    declaration = _load_json(context, code_root / "app" / "clerk-seam.json", "clerk seam declaration")
    _exact(context, declaration, SEAM_KEYS, "clerk seam declaration")
    _version(context, declaration, "clerk seam declaration")
    if declaration["schema"] != SEAM_SCHEMA:
        context.stop("clerk seam schema is not librarian-clerk-seam")
    rel = declaration["clerk_path"]
    digest = declaration["clerk_sha256"]
    if not isinstance(rel, str) or not isinstance(digest, str) or not HEX64.fullmatch(digest):
        context.stop("clerk pin is not a path and a sha256")
    clerk = context.resolve_under(code_root, rel)
    if _linked(clerk) or not clerk.is_file():
        context.stop("pinned clerk is missing")
    if _sha256(clerk.read_bytes()) != digest:
        context.stop("clerk pin does not match")
    return clerk


def _prepare(context, code_root: Path, root: Path, explicit: str | None) -> Path:
    config = context.load_config(code_root / "app" / "development-workspace.json")
    if context.is_filesystem_root(root):
        context.stop("fixture container is a filesystem root")
    if context.overlaps_live(root, code_root, config):
        context.stop("fixture root is the live workspace")
    container = context.select_container(root, code_root, explicit)
    context.guard_workspace_path(root, code_root)
    context.validate_context(root, config, execute=False, runner_root=code_root)
    return container


def _run_clerk(clerk: Path, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["GIT_OPTIONAL_LOCKS"] = "0"
    env["GIT_TERMINAL_PROMPT"] = "0"
    return subprocess.run(
        [sys.executable, "-B", str(clerk), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        timeout=60,
        check=False,
    )


def _document(context, proc: subprocess.CompletedProcess[bytes]) -> dict:
    if b"Traceback" in proc.stdout or b"Traceback" in proc.stderr:
        context.stop("clerk inspection raised")
    try:
        text = proc.stdout.decode("utf-8")
    except UnicodeError:
        context.stop("clerk inspection is not utf-8")
    try:
        value = json.loads(text, object_pairs_hook=lambda pairs: _pairs(context, pairs))
    except context.Stop:
        raise
    except json.JSONDecodeError:
        context.stop("clerk inspection is not json")
    if not isinstance(value, dict) or value.get("schema") != INSPECTION_SCHEMA:
        context.stop("clerk inspection schema is not clerk-handoff-inspection/2")
    return value


def _details(document: dict) -> str:
    problems = document.get("problems")
    if not isinstance(problems, list):
        return ""
    parts = []
    for item in problems:
        if isinstance(item, dict) and isinstance(item.get("detail"), str) and item["detail"]:
            parts.append(item["detail"])
    return "; ".join(parts)


def _attention(code: int, boundary: str, wrote: str, job_id: str, delivery: str, extra: str = "") -> SeamResult:
    lines = [
        "seam: attention",
        f"boundary: {boundary}",
        f"clerk_job: {job_id}",
        f"delivery_id: {delivery}",
        f"this-call-wrote: {wrote}",
        "review: not performed",
        "acceptance: not performed",
    ]
    if extra:
        lines.append(extra.rstrip("\n"))
    return SeamResult(code, "\n".join(lines))


def _show(context, clerk: Path, store: str, job_id: str, base: str) -> dict:
    proc = _run_clerk(
        clerk,
        ["show", "--store", store, "--job", job_id, "--instructions-base", base, "--json"],
    )
    return _document(context, proc)


def _resume(context, clerk: Path, store: str, job_id: str, actor: str, base: str, token: str, instruction_sha: str, delivery_exists: bool) -> SeamResult | None:
    proc = _run_clerk(
        clerk,
        ["claim", "--store", store, "--job", job_id, "--as", actor, "--instructions-base", base, "--resume"],
    )
    text = proc.stdout.decode("utf-8", "replace")
    if b"Traceback" in proc.stderr or "Traceback" in text:
        context.stop("clerk resume raised")
    lines = [line for line in text.splitlines() if line and not line.startswith("result ")]
    if proc.returncode != 0 or lines != [
        "resume " + job_id,
        "token " + token,
        "instructions-usable sha256=" + instruction_sha,
    ]:
        if delivery_exists:
            detail = text.strip() or proc.stderr.decode("utf-8", "replace").strip()
            return _attention(4, "stale instructions after delivery", "nothing", job_id, "", detail)
        context.stop("claim resume was refused")
    if not TOKEN.fullmatch(token):
        context.stop("claim token is not the public resume token")
    return None


def _outputs(context, job: dict) -> list[str]:
    names = job.get("expected_outputs")
    if not isinstance(names, list) or not names:
        context.stop("expected outputs are missing")
    clean = []
    for name in names:
        if not _simple_name(name):
            context.stop("expected output is not a file name")
        clean.append(name)
    if len(set(clean)) != len(clean):
        context.stop("expected output is repeated")
    return clean


def _instruction_sha(context, job: dict) -> str:
    instructions = job.get("instructions")
    if not isinstance(instructions, dict):
        context.stop("clerk instructions are missing")
    digest = instructions.get("sha256")
    if not isinstance(digest, str) or not HEX64.fullmatch(digest):
        context.stop("clerk instruction hash is missing")
    return digest


def _declared_matches(context, code_root: Path, root: Path, bridge_job: dict, instruction_sha: str) -> bool:
    inputs = bridge_job.get("inputs")
    if not isinstance(inputs, list) or not inputs:
        context.stop("bridge job inputs are missing")
    item = inputs[0]
    if not isinstance(item, dict) or item.get("sha256") != instruction_sha:
        return False
    path = item.get("path")
    if not isinstance(path, str):
        return False
    declared = context.resolve_under(root, "bridge/declared/" + path)
    context.guard_workspace_path(declared, code_root)
    if _linked(declared) or not declared.is_file():
        return False
    data = declared.read_bytes()
    size = item.get("bytes")
    return _sha256(data) == instruction_sha and size == len(data)


def _delivery_exists(root: Path, delivery: str) -> bool:
    prov = root / "bridge" / "provenance" / f"{delivery}.json"
    store = root / "bridge" / "store" / delivery
    return _lexists(prov) or _lexists(store)


def _bind(context, worker_bridge, canon, root: Path, job_bytes: bytes, link: dict, delivery: str) -> dict | None:
    prov_path = root / "bridge" / "provenance" / f"{delivery}.json"
    if not _lexists(prov_path):
        return None
    if _linked(prov_path) or not prov_path.is_file():
        context.stop("provenance is not a file")
    provenance = worker_bridge._load_provenance(context, canon, prov_path)
    if link["bridge_job_sha256"] != provenance["job_sha256"]:
        context.stop("link bridge_job_sha256 does not match the original provenance")
    if _sha256(job_bytes) != provenance["job_sha256"]:
        context.stop("job bytes do not match the original provenance")
    return provenance


def _artifact_map(context, stored: dict, expected: list[str]) -> dict[str, dict]:
    artifacts = stored.get("artifacts")
    if not isinstance(artifacts, list):
        context.stop("stored receipt artifacts are missing")
    found = {}
    for item in artifacts:
        if not isinstance(item, dict) or not _simple_name(item.get("path")):
            context.stop("stored receipt artifact name is not a file name")
        digest = item.get("sha256")
        if not isinstance(digest, str) or not HEX64.fullmatch(digest):
            context.stop("stored receipt artifact hash is missing")
        if item["path"] in found:
            context.stop("stored receipt artifact is repeated")
        found[item["path"]] = item
    if set(found) != set(expected):
        context.stop("stored receipt artifacts do not match expected outputs")
    return found


def _exc_line(exc: BaseException) -> str:
    text = str(exc).replace("\r", " ").replace("\n", " ")
    if len(text) > 200:
        text = text[:200]
    return text


def _io_attention(phase: str, dest: Path, exc: BaseException, payload: bytes) -> _CopyFault:
    boundary = {
        "create": "outbox create failed",
        "write": "outbox write failed",
        "flush": "outbox flush failed",
        "fsync": "outbox fsync failed",
        "read-back": "outbox read-back failed",
    }[phase]
    lines = [
        f"phase: {phase}",
        f"attempted: {dest.name}",
        f"exception: {type(exc).__name__}",
        "detail: " + _exc_line(exc),
    ]
    wrote = "uncertain outbox"
    if not _lexists(dest):
        wrote = "nothing"
        lines.append("retained: absent")
    elif _linked(dest):
        wrote = "occupied outbox path"
        lines.append(f"retained: {dest}")
    else:
        try:
            plain = dest.is_file()
            data = dest.read_bytes() if plain else None
        except OSError as read_exc:
            lines.append(f"retained: {dest}")
            lines.append("retained-bytes: unreadable")
            lines.append(f"read-error: {type(read_exc).__name__}")
        else:
            if not plain or data is None:
                wrote = "occupied outbox path"
                lines.append(f"retained: {dest}")
            else:
                if data == payload:
                    wrote = "outbox copy"
                elif len(data) == 0:
                    wrote = "empty outbox file"
                else:
                    wrote = "partial outbox"
                lines.append(f"retained: {dest}")
                lines.append(f"retained-bytes: {len(data)}")
                lines.append(f"retained-sha256: {_sha256(data)}")
    lines.append("recovery: explicit recovery is required")
    return _CopyFault(boundary, wrote, "\n".join(lines))


def _return_uncertain(job_id: str, delivery: str, outbox: Path, expected: list[str], exc: BaseException) -> SeamResult:
    lines = [
        "phase: clerk-return",
        "attempted: clerk return",
        f"exception: {type(exc).__name__}",
        "detail: " + _exc_line(exc),
    ]
    for name in expected:
        path = outbox / name
        lines.append(f"retained: {path}")
        if _linked(path):
            lines.append("retained-bytes: linked")
            continue
        try:
            if not path.is_file():
                lines.append("retained-bytes: absent")
                continue
            data = path.read_bytes()
        except OSError as read_exc:
            lines.append("retained-bytes: unreadable")
            lines.append(f"read-error: {type(read_exc).__name__}")
        else:
            lines.append(f"retained-bytes: {len(data)}")
            lines.append(f"retained-sha256: {_sha256(data)}")
    lines.append("recovery: explicit recovery is required")
    lines.append("return-report: uncertain; a Clerk event may already exist")
    return _attention(4, "clerk return is uncertain", "outbox copy", job_id, delivery, "\n".join(lines))


def _worker_result(report, boundary: str) -> SeamResult:
    text = (
        "seam: attention\n"
        f"boundary: {boundary}\n"
        "this-call-wrote: nothing\n"
        "review: not performed\n"
        "acceptance: not performed\n"
        + report.text
    )
    return SeamResult(report.code, text)


def _copy_outputs(context, container: Path, store: Path, job_id: str, output_root: Path, expected: list[str], artifacts: dict[str, dict], io_fault: str | None = None) -> str | _CopyFault:
    outbox = store / "jobs" / job_id / "outbox"
    if _linked(outbox) or not outbox.is_dir():
        return "outbox is not a plain directory"
    if not context.is_inside(outbox, container) or not context.is_inside(outbox, store):
        context.stop("outbox leaves the designated container")
    wrote = False
    for name in expected:
        source = output_root / name
        if not context.is_inside(source, output_root):
            context.stop("artifact path escapes the worker output")
        payload = source.read_bytes()
        if _sha256(payload) != artifacts[name]["sha256"]:
            return "bridge output does not match the receipt"
        dest = outbox / name
        if _lexists(dest):
            try:
                linked = _linked(dest)
                plain = dest.is_file()
                nlink = dest.stat().st_nlink
            except OSError as exc:
                return _io_attention("read-back", dest, exc, payload)
            if linked or not plain or nlink != 1:
                return "outbox path is occupied"
            try:
                existing = dest.read_bytes()
            except OSError as exc:
                return _io_attention("read-back", dest, exc, payload)
            if existing != payload:
                return "outbox bytes differ"
            continue
        if not context.is_inside(dest, outbox):
            context.stop("outbox name escapes the outbox")
        phase = "create"
        try:
            if io_fault == "create":
                raise OSError("injected outbox create failure")
            with open(dest, "xb") as handle:
                phase = "write"
                if io_fault == "write":
                    part = payload[:3] if len(payload) >= 3 else payload
                    handle.write(part)
                    handle.flush()
                    raise OSError("injected outbox write failure after partial bytes")
                handle.write(payload)
                phase = "flush"
                if io_fault == "flush":
                    raise OSError("injected outbox flush failure")
                handle.flush()
                phase = "fsync"
                if io_fault == "fsync":
                    raise OSError("injected outbox fsync failure")
                os.fsync(handle.fileno())
        except FileExistsError:
            try:
                if _linked(dest) or not dest.is_file() or dest.read_bytes() != payload:
                    return "outbox path is occupied"
            except OSError as exc:
                return _io_attention("read-back", dest, exc, payload)
            continue
        except OSError as exc:
            return _io_attention(phase, dest, exc, payload)
        try:
            if io_fault == "read-back":
                raise OSError("injected outbox read-back failure")
            copied = dest.read_bytes()
            nlink = dest.stat().st_nlink
        except OSError as exc:
            return _io_attention("read-back", dest, exc, payload)
        if copied != payload or nlink != 1:
            return "outbox copy does not match the receipt"
        wrote = True
    return "copied" if wrote else "already"


def _evidence(delivery: str, request_sha: str, receipt_sha: str, expected: list[str], artifacts: dict[str, dict]) -> str:
    parts = [f"bridge delivery {delivery} request {request_sha} receipt {receipt_sha}"]
    for name in expected:
        source = f"bridge/delivery/{delivery}/output/{name}"
        parts.append(f"artifact {name} {artifacts[name]['sha256']} source {source}")
    return " ".join(parts)


def _success(job_id: str, delivery: str, expected: list[str], artifacts: dict[str, dict], copy_state: str, clerk_line: str, reviewer: str) -> SeamResult:
    place = "copied to clerk outbox" if copy_state == "copied" else "already in clerk outbox"
    lines = [
        f"clerk_job: {job_id}",
        f"delivery_id: {delivery}",
        "transport: delivered",
        "collection: collected",
    ]
    for name in expected:
        lines.append(f"artifact: {name} sha256 {artifacts[name]['sha256']} {place}")
    lines.extend(
        [
            f"clerk: {clerk_line}",
            f"reviewer: {reviewer} (inbox projection; not invoked)",
            "review: not performed",
            "acceptance: not performed",
        ]
    )
    return SeamResult(0, "\n".join(lines))


def perform(
    context,
    code_root: Path,
    root: Path,
    *,
    link_rel: str,
    actor: str,
    instructions_base: str,
    explicit: str | None = None,
    interrupt: str | None = None,
    io_fault: str | None = None,
) -> SeamResult:
    """Run clerk-deliver. Refusals raise context.Stop. interrupt and io_fault are not CLI flags."""
    if interrupt not in (None, *INTERRUPTS):
        context.stop("unknown interrupt")
    if io_fault not in (None, *IO_FAULTS):
        context.stop("unknown io fault")
    if not isinstance(actor, str) or actor.strip() == "":
        context.stop("actor is missing")
    if not isinstance(instructions_base, str) or instructions_base.strip() == "":
        context.stop("instructions base is missing")
    base = Path(instructions_base)
    if _linked(base) or not base.is_dir():
        context.stop("instructions base is missing")
    base_text = str(base.resolve())
    container = _prepare(context, code_root, root, explicit)
    clerk = _pin_clerk(context, code_root)
    link_path = context.resolve_under(root, link_rel)
    context.guard_workspace_path(link_path, code_root)
    link = _load_json(context, link_path, "link")
    _exact(context, link, LINK_KEYS, "link")
    _version(context, link, "link")
    if link["schema"] != LINK_SCHEMA:
        context.stop("link schema is not librarian-clerk-link")
    delivery = link["delivery_id"]
    job_id = link["clerk_job_id"]
    if not _simple_name(delivery) or link_path.stem != delivery:
        context.stop("link delivery does not match its file name")
    if not _simple_name(job_id):
        context.stop("link job id is not a file name")
    if not isinstance(link["bridge_job"], str) or not isinstance(link["bridge_job_sha256"], str):
        context.stop("link bridge job is missing")
    if not HEX64.fullmatch(link["bridge_job_sha256"]):
        context.stop("link bridge_job_sha256 is not sha256")
    if not isinstance(link["clerk_store"], str) or not os.path.isabs(link["clerk_store"]):
        context.stop("clerk store must be absolute")
    store = Path(link["clerk_store"])
    if _linked(store) or not store.is_dir():
        context.stop("clerk store is not a plain directory")
    if context.is_inside(store, root) or context.is_inside(root, store):
        context.stop("clerk store overlaps the fixture root")
    if not context.is_inside(store, container):
        context.stop("clerk store is outside the designated container")
    job_path = context.resolve_under(root, link["bridge_job"])
    context.guard_workspace_path(job_path, code_root)
    if _linked(job_path) or not job_path.is_file():
        context.stop("bridge job is missing")
    job_bytes = job_path.read_bytes()
    if _sha256(job_bytes) != link["bridge_job_sha256"]:
        context.stop("bridge job bytes do not match the link")
    worker_bridge = _load_bridge(code_root)
    bridge_config = worker_bridge.load_bridge_config(context, code_root)
    _adapter, canon, envelope, ids, _lab = worker_bridge.pin_and_import(context, code_root, bridge_config)
    bridge_job = worker_bridge._load_job(context, envelope, job_path)
    worker_bridge._check_delivery(context, ids, bridge_job["delivery_id"])
    if bridge_job["delivery_id"] != delivery:
        context.stop("bridge delivery does not match the link")
    if bridge_job["job_id"] != job_id:
        context.stop("bridge job does not match the link")
    document = _show(context, clerk, str(store.resolve()), job_id, base_text)
    if document.get("job_id") != job_id:
        context.stop("inspection job does not match the link")
    state = document.get("state")
    exists = _delivery_exists(root, delivery)
    detail = _details(document)
    checks = document.get("checks") if isinstance(document.get("checks"), dict) else {}
    if state == "queued":
        context.stop("claim first")
    if state not in ("claimed", "returned"):
        completion = checks.get("completion")
        if completion in ("partial", "missing-event", "missing-witness", "mismatch") or exists:
            return _attention(4, "damaged completion", "nothing", job_id, delivery, detail)
        context.stop(detail or "clerk inspection refused")
    job = document.get("job")
    claim = document.get("claim")
    if not isinstance(job, dict) or not isinstance(claim, dict):
        context.stop("clerk inspection has no claim")
    if job.get("job_id") != job_id or job.get("assignee") != actor or claim.get("by") != actor:
        context.stop("actor is not the assignee")
    reviewer = job.get("reviewer")
    if not isinstance(reviewer, str) or reviewer.strip() == "":
        context.stop("reviewer is missing")
    token = claim.get("token")
    if not isinstance(token, str) or not TOKEN.fullmatch(token):
        context.stop("claim token is missing")
    if state == "returned":
        returned = document.get("returned")
        if not isinstance(returned, dict) or returned.get("delivery") != delivery or returned.get("by") != actor:
            context.stop("conflicting delivery")
        if checks.get("artifacts") == "changed":
            return _attention(4, "outbox artifact changed", "nothing", job_id, delivery, detail)
        if checks.get("completion") != "ok" or checks.get("events") != "ok":
            return _attention(4, "damaged completion", "nothing", job_id, delivery, detail)
    elif checks.get("events") != "ok":
        if exists:
            return _attention(4, "damaged completion", "nothing", job_id, delivery, detail)
        context.stop(detail or "clerk claim is incomplete")
    expected = _outputs(context, job)
    instruction_sha = _instruction_sha(context, job)
    usable = checks.get("instructions") == "usable" and _declared_matches(
        context, code_root, root, bridge_job, instruction_sha
    )
    if not usable:
        if exists or state == "returned":
            return _attention(4, "stale instructions after delivery", "nothing", job_id, delivery, detail)
        context.stop("stale instructions")
    if state == "claimed":
        resumed = _resume(
            context, clerk, str(store.resolve()), job_id, actor, base_text, token, instruction_sha, exists
        )
        if resumed is not None:
            return resumed
    if exists:
        _bind(context, worker_bridge, canon, root, job_bytes, link, delivery)
        report = worker_bridge.perform(
            context, "bridge-status", code_root, root, delivery=delivery, explicit=explicit
        )
    else:
        if interrupt == "before-launch":
            return _attention(4, "interrupted before launch", "nothing", job_id, delivery)
        report = worker_bridge.perform(
            context,
            "bridge-test",
            code_root,
            root,
            job_rel=link["bridge_job"],
            explicit=explicit,
        )
    if report.code == 3:
        return _worker_result(report, "worker result is not a collected done")
    if report.code != 0:
        return _worker_result(report, "worker result is uncertain")
    provenance = _bind(context, worker_bridge, canon, root, job_bytes, link, delivery)
    if provenance is None:
        return _attention(4, "missing provenance", "nothing", job_id, delivery)
    env = worker_bridge._correlate(context, code_root, root, container, canon, provenance, delivery)
    receipt_path = root / "bridge" / "store" / delivery / "receipt.json"
    stored = worker_bridge._read_stored_receipt(context, canon, receipt_path, provenance, env, delivery)
    if stored is None:
        return _attention(4, "missing receipt", "nothing", job_id, delivery)
    transport = stored.get("transport")
    collection = stored.get("collection")
    claimed = stored.get("claimed_outcome")
    if transport == "delivered" and collection == "uncollected":
        return _attention(3, "worker result is not a collected done", "nothing", job_id, delivery)
    if claimed == "failed" and collection == "collected":
        return _attention(3, "worker result is not a collected done", "nothing", job_id, delivery)
    if not (transport == "delivered" and collection == "collected" and claimed == "done"):
        return _attention(4, "worker result is uncertain", "nothing", job_id, delivery)
    artifacts = _artifact_map(context, stored, expected)
    output_root = context.resolve_under(root, provenance["output_root"])
    context.guard_workspace_path(output_root, code_root)
    for name in expected:
        source = output_root / name
        if _linked(source) or not source.is_file():
            return _attention(4, "bridge output is missing", "nothing", job_id, delivery)
        payload = source.read_bytes()
        size = artifacts[name].get("bytes")
        if _sha256(payload) != artifacts[name]["sha256"] or (isinstance(size, int) and not isinstance(size, bool) and size != len(payload)):
            return _attention(4, "bridge output does not match the receipt", "nothing", job_id, delivery)
    if interrupt == "before-copy":
        return _attention(4, "interrupted before copy", "nothing", job_id, delivery)
    copy_state = _copy_outputs(
        context, container, store, job_id, output_root, expected, artifacts, io_fault
    )
    if isinstance(copy_state, _CopyFault):
        return _attention(4, copy_state.boundary, copy_state.wrote, job_id, delivery, copy_state.extra)
    if copy_state not in ("copied", "already"):
        wrote = "outbox copy" if copy_state == "outbox copy does not match the receipt" else "nothing"
        return _attention(4, copy_state, wrote, job_id, delivery)
    if interrupt == "before-return":
        return _attention(4, "interrupted before return", "outbox copy", job_id, delivery)
    receipt_sha = _sha256(receipt_path.read_bytes())
    evidence = _evidence(delivery, provenance["request_sha256"], receipt_sha, expected, artifacts)
    outbox = store / "jobs" / job_id / "outbox"
    try:
        returned = _run_clerk(
            clerk,
            [
                "return",
                "--store",
                str(store.resolve()),
                "--job",
                job_id,
                "--as",
                actor,
                "--claim",
                token,
                "--delivery",
                delivery,
                "--evidence",
                evidence,
            ],
        )
        if io_fault == "clerk-timeout":
            raise subprocess.TimeoutExpired([sys.executable, "-B", str(clerk)], 60)
        if io_fault == "clerk-oserror":
            raise OSError("injected clerk process failure")
    except subprocess.TimeoutExpired as exc:
        return _return_uncertain(job_id, delivery, outbox, expected, exc)
    except OSError as exc:
        return _return_uncertain(job_id, delivery, outbox, expected, exc)
    text = returned.stdout.decode("utf-8", "replace")
    if b"Traceback" in returned.stderr or "Traceback" in text:
        return _attention(4, "clerk return raised", "outbox copy", job_id, delivery, text)
    lines = [line for line in text.splitlines() if line]
    clerk_line = ""
    if returned.returncode == 0:
        if f"returned {job_id}" in lines:
            clerk_line = "returned"
        elif f"already-recorded {job_id}" in lines:
            clerk_line = "already-recorded"
    if not clerk_line:
        return _attention(4, "clerk return was refused", "outbox copy", job_id, delivery, text.strip())
    if interrupt == "before-report":
        return _attention(4, "interrupted before report", "clerk return", job_id, delivery)
    return _success(job_id, delivery, expected, artifacts, copy_state, clerk_line, reviewer)
