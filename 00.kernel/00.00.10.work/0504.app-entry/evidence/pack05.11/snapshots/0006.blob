#!/usr/bin/env python3
"""Fixture-only glue between the development entry and the accepted worker bridge.

This module does not import the lab until the pinned file hashes match.
The import name is worker_bridge_pinned. sys.path is not changed.
Collection is not approval. Same-user Python is not a sandbox.
"""

from __future__ import annotations

import hashlib
import importlib
import importlib.util
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True

REQUEST_SCHEMA = "worker-bridge/request@1"
JOB_SCHEMA = "librarian-bridge-job"
PROVENANCE_SCHEMA = "librarian-bridge-provenance"
RECOVERY_SCHEMA = "librarian-bridge-recovery"
RECEIPT_SCHEMA = "worker-bridge/receipt@1"
CONFIG_SCHEMA = "librarian-worker-bridge"
PIN_NAMES = (
    "bridge/__init__.py",
    "bridge/canon.py",
    "bridge/ids.py",
    "bridge/envelope.py",
    "bridge/verify.py",
    "bridge/adapter.py",
    "profiles.json",
    "fixtures/worker_fixture.py",
)
CONFIG_KEYS = (
    "schema",
    "version",
    "_note",
    "bridge_dir",
    "files",
    "allowed_kinds",
    "container_subdir",
)
JOB_KEYS = (
    "schema",
    "version",
    "delivery_id",
    "job_id",
    "role",
    "work_ref",
    "backend",
    "inputs",
    "limits",
)
INPUT_KEYS = ("name", "path", "sha256", "bytes")
PROVENANCE_KEYS = (
    "schema",
    "version",
    "delivery_id",
    "job_id",
    "work_ref",
    "container",
    "job_sha256",
    "assignment_record",
    "assignment_sha256",
    "request_sha256",
    "input_root",
    "output_root",
    "store",
    "backend",
)
RECOVERY_KEYS = (
    "schema",
    "version",
    "delivery_id",
    "request_sha256",
    "reason",
    "requester",
)
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class Report:
    def __init__(self, code: int, text: str) -> None:
        self.code = code
        self.text = text


def _exact(context, value: dict, keys: tuple[str, ...], kind: str) -> None:
    missing = [key for key in keys if key not in value]
    if missing:
        context.stop(f"{kind} misses keys: {', '.join(missing)}")
    unknown = [key for key in value if key not in keys]
    if unknown:
        context.stop(f"{kind} has an unknown key: {unknown[0]}")


def _version(context, value: dict, kind: str) -> None:
    got = value["version"]
    if isinstance(got, bool) or not isinstance(got, int) or got != 1:
        context.stop(f"{kind} version is not 1")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(getattr(info, "st_file_attributes", 0) & REPARSE)


def _lexists(path: Path) -> bool:
    try:
        os.lstat(path)
    except FileNotFoundError:
        return False
    return True


def _ensure_plain_dir(context, path: Path, label: str) -> None:
    if _lexists(path):
        if _is_link(path) or not path.is_dir():
            context.stop(f"{label} is not a plain directory")
        return
    path.mkdir()


def _exclusive_dir(context, path: Path, label: str) -> None:
    if _lexists(path):
        context.stop(f"{label} is already present")
    try:
        os.mkdir(path)
    except FileExistsError:
        context.stop(f"{label} is already present")


def load_bridge_config(context, code_root: Path) -> dict:
    raw = context.load_json(code_root / "app" / "worker-bridge.json", kind="worker bridge config")
    _exact(context, raw, CONFIG_KEYS, "worker bridge config")
    if raw["schema"] != CONFIG_SCHEMA:
        context.stop("worker bridge config schema is not librarian-worker-bridge")
    _version(context, raw, "worker bridge config")
    if raw["container_subdir"] != "bridge":
        context.stop("worker bridge container subdir is not bridge")
    if not isinstance(raw["_note"], str):
        context.stop("worker bridge config field has the wrong type: _note")
    if not isinstance(raw["bridge_dir"], str) or raw["bridge_dir"].strip() == "":
        context.stop("bridge_dir is empty")
    files = raw["files"]
    if not isinstance(files, dict) or set(files) != set(PIN_NAMES):
        context.stop("worker bridge pins are not the eight accepted files")
    for name in PIN_NAMES:
        digest = files[name]
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            context.stop(f"pinned hash is not sha256: {name}")
    kinds = raw["allowed_kinds"]
    if (
        isinstance(kinds, bool)
        or not isinstance(kinds, list)
        or not kinds
        or any(not isinstance(item, str) or item.strip() == "" for item in kinds)
    ):
        context.stop("allowed_kinds is not a list of kinds")
    return raw


def pin_and_import(context, code_root: Path, bridge_config: dict):
    """Hash every pinned file, then import. A mismatch returns before import."""
    lab = context.resolve_under(code_root, bridge_config["bridge_dir"])
    for name in PIN_NAMES:
        path = context.resolve_under(lab, name)
        if not path.is_file() or _is_link(path):
            context.stop(f"pinned file is missing: {name}")
        got = _sha256(path.read_bytes())
        if got != bridge_config["files"][name]:
            context.stop(f"pinned file hash does not match: {name}")
    if "worker_bridge_pinned" not in sys.modules:
        init = lab / "bridge" / "__init__.py"
        spec = importlib.util.spec_from_file_location(
            "worker_bridge_pinned",
            init,
            submodule_search_locations=[str(lab / "bridge")],
        )
        if spec is None or spec.loader is None:
            context.stop("could not load the pinned bridge")
        package = importlib.util.module_from_spec(spec)
        sys.modules["worker_bridge_pinned"] = package
        spec.loader.exec_module(package)
    return (
        importlib.import_module("worker_bridge_pinned.adapter"),
        importlib.import_module("worker_bridge_pinned.canon"),
        importlib.import_module("worker_bridge_pinned.envelope"),
        importlib.import_module("worker_bridge_pinned.ids"),
        lab,
    )


def _load_profiles(context, canon, lab: Path) -> dict:
    raw = canon.strict_loads((lab / "profiles.json").read_bytes())
    if not isinstance(raw, dict):
        context.stop("profiles are not an object")
    profiles = {}
    for key, value in raw.items():
        if isinstance(key, str) and key.startswith("_"):
            continue
        if not isinstance(value, dict) or set(value) != {"kind", "argv"}:
            context.stop(f"profile is not kind and argv: {key}")
        if not isinstance(value["kind"], str) or value["kind"].strip() == "":
            context.stop(f"profile kind is empty: {key}")
        argv = value["argv"]
        if not isinstance(argv, list) or not argv or any(not isinstance(item, str) for item in argv):
            context.stop(f"profile argv is not a list of strings: {key}")
        profiles[key] = value
    return profiles


def _check_delivery(context, ids, delivery: str) -> str:
    try:
        return ids.check(delivery)
    except ids.IdentityError as exc:
        context.stop(str(exc))


def _load_job(context, envelope, path: Path) -> dict:
    job = context.load_json(path, kind="job")
    _exact(context, job, JOB_KEYS, "job")
    if job["schema"] != JOB_SCHEMA:
        context.stop("job schema is not librarian-bridge-job")
    _version(context, job, "job")
    for key in ("delivery_id", "job_id", "role", "work_ref", "backend"):
        got = job[key]
        if not isinstance(got, str) or got.strip() == "":
            context.stop(f"job field is empty: {key}")
    if not envelope.ID.match(job["job_id"]):
        context.stop("job_id is not a plain identifier")
    try:
        envelope.check_limits(job["limits"])
    except envelope.EnvelopeError as exc:
        context.stop(str(exc))
    inputs = job["inputs"]
    if not isinstance(inputs, list):
        context.stop("job inputs is not a list")
    names = set()
    for item in inputs:
        if not isinstance(item, dict):
            context.stop("an input is not an object")
        _exact(context, item, INPUT_KEYS, "input")
        if item["name"] in names:
            context.stop(f"input name repeated: {item['name']}")
        names.add(item["name"])
        if not isinstance(item["name"], str) or item["name"].strip() == "":
            context.stop("input name is empty")
        if not envelope.safe_rel(item["path"]):
            context.stop(f"input path is not a safe relative path: {item['path']!r}")
        digest = item["sha256"]
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            context.stop("input hash is not sha256")
        size = item["bytes"]
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            context.stop("input bytes is not a size")
    return job


def _profile(context, profiles: dict, allowed: list, backend: str) -> dict:
    profile = profiles.get(backend)
    if profile is None:
        context.stop(f"backend {backend!r} is not an allowlisted profile")
    if profile["kind"] not in allowed:
        context.stop("worker kind is not allowed")
    return profile


def _verify_declared(context, code_root: Path, root: Path, job: dict) -> None:
    for item in job["inputs"]:
        source = context.resolve_under(root, f"bridge/declared/{item['path']}")
        context.guard_workspace_path(source, code_root)
        if not source.is_file() or _is_link(source):
            context.stop(f"declared input is missing: {item['path']}")
        data = source.read_bytes()
        if len(data) != item["bytes"] or _sha256(data) != item["sha256"]:
            context.stop(f"input hash differs from the job: {item['path']}")


def _copy_inputs(context, code_root: Path, root: Path, job: dict, input_dir: Path) -> None:
    for item in job["inputs"]:
        source = context.resolve_under(root, f"bridge/declared/{item['path']}")
        context.guard_workspace_path(source, code_root)
        if not source.is_file() or _is_link(source):
            context.stop(f"declared input is missing: {item['path']}")
        data = source.read_bytes()
        if len(data) != item["bytes"] or _sha256(data) != item["sha256"]:
            context.stop(f"input hash differs from the job: {item['path']}")
        dest = input_dir.joinpath(*item["path"].split("/"))
        if not context.is_inside(dest, input_dir):
            context.stop("per-delivery input escapes its directory")
        if _lexists(dest):
            context.stop("per-delivery input is already present")
        _ensure_plain_dir(context, dest.parent, "per-delivery input directory")
        try:
            with open(dest, "xb") as handle:
                handle.write(data)
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError:
            context.stop("per-delivery input is already present")


def _write_exclusive(context, path: Path, data: bytes, label: str) -> None:
    if _lexists(path):
        context.stop(f"{label} is already present")
    try:
        with open(path, "xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        context.stop(f"{label} is already present")


def _stored_inside(context, fixture_root: Path, text: str, label: str) -> Path:
    if not isinstance(text, str) or text.strip() == "":
        context.stop(f"stored {label} is empty")
    try:
        resolved = Path(text).resolve()
    except OSError:
        context.stop(f"stored {label} escapes the container")
    if _is_link(Path(text)) or not context.is_inside(resolved, fixture_root.resolve()):
        context.stop(f"stored {label} escapes the container")
    return resolved


def _load_provenance(context, canon, path: Path) -> dict:
    if not path.is_file() or _is_link(path):
        context.stop("stored provenance is missing")
    try:
        raw = canon.strict_loads(path.read_bytes())
    except Exception:
        context.stop("stored provenance is not strict json")
    if not isinstance(raw, dict):
        context.stop("stored provenance is not an object")
    _exact(context, raw, PROVENANCE_KEYS, "provenance")
    if raw["schema"] != PROVENANCE_SCHEMA:
        context.stop("provenance schema is not librarian-bridge-provenance")
    _version(context, raw, "provenance")
    for key in (
        "delivery_id",
        "job_id",
        "work_ref",
        "container",
        "job_sha256",
        "assignment_record",
        "assignment_sha256",
        "request_sha256",
        "input_root",
        "output_root",
        "store",
        "backend",
    ):
        if not isinstance(raw[key], str) or raw[key].strip() == "":
            context.stop(f"provenance field is empty: {key}")
    return raw


def _correlate(context, code_root: Path, root: Path, container: Path, canon, provenance: dict, delivery: str) -> dict:
    if provenance["delivery_id"] != delivery:
        context.stop("provenance delivery does not match")
    if os.path.normcase(str(Path(provenance["container"]).resolve())) != os.path.normcase(str(Path(container).resolve())):
        context.stop("provenance container does not match the designated container")
    for label in ("input_root", "output_root", "store"):
        path = context.resolve_under(root, provenance[label])
        context.guard_workspace_path(path, code_root)
        if _is_link(path):
            context.stop(f"stored {label} is a link")
    request = context.resolve_under(root, provenance["store"] + "/" + delivery + "/request.json")
    context.guard_workspace_path(request, code_root)
    if not request.is_file() or _is_link(request):
        context.stop("stored request is missing")
    raw = request.read_bytes()
    if _sha256(raw) != provenance["request_sha256"]:
        context.stop("stored request does not match provenance")
    try:
        env = canon.strict_loads(raw)
    except Exception:
        context.stop("stored request is not strict json")
    if not isinstance(env, dict):
        context.stop("stored request is not an object")
    if env.get("delivery_id") != delivery or env.get("work_ref") != provenance["work_ref"]:
        context.stop("stored request does not match provenance")
    if env.get("job_id") != provenance["job_id"] or env.get("backend") != provenance["backend"]:
        context.stop("stored request does not match provenance")
    _stored_inside(context, root, env.get("input_root", ""), "input_root")
    _stored_inside(context, root, env.get("output_root", ""), "output_root")
    return env


def _require_stored_receipt(context, stored, provenance: dict, env: dict, delivery: str) -> None:
    """Refuse a persisted receipt whose identity does not match this delivery.

    The object must use the supported receipt schema. delivery_id, job_id,
    backend, and request_sha256 are mandatory strings. A missing request hash
    is not a match. A matching hash does not excuse a different delivery or job.
    Extra keys are left in place. This is not a signature or an approval.
    Call it only for a stored receipt, not for a transient status form.
    """
    if not isinstance(stored, dict):
        context.stop("stored receipt is not an object")
    if stored.get("schema") != RECEIPT_SCHEMA:
        context.stop("stored receipt schema is not worker-bridge/receipt@1")
    for key in ("delivery_id", "job_id", "request_sha256", "backend"):
        value = stored.get(key)
        if not isinstance(value, str) or value.strip() == "":
            context.stop(f"stored receipt field is missing: {key}")
    if (
        stored["delivery_id"] != delivery
        or stored["delivery_id"] != provenance["delivery_id"]
        or stored["delivery_id"] != env.get("delivery_id")
    ):
        context.stop("stored receipt delivery does not match")
    if stored["job_id"] != provenance["job_id"] or stored["job_id"] != env.get("job_id"):
        context.stop("stored receipt job does not match")
    if stored["backend"] != provenance["backend"] or stored["backend"] != env.get("backend"):
        context.stop("stored receipt backend does not match")
    if stored["request_sha256"] != provenance["request_sha256"]:
        context.stop("stored receipt does not match provenance")


def _read_stored_receipt(context, canon, receipt_file: Path, provenance: dict, env: dict, delivery: str):
    """Return the stored receipt when the file is present. Return None when it is absent.

    A link, a non-file, malformed JSON, or an inconsistent object refuses.
    The file is not written.
    """
    if not _lexists(receipt_file):
        return None
    if _is_link(receipt_file) or not receipt_file.is_file():
        context.stop("stored receipt is not a file")
    try:
        stored = canon.strict_loads(receipt_file.read_bytes())
    except Exception:
        context.stop("stored receipt is not strict json")
    _require_stored_receipt(context, stored, provenance, env, delivery)
    return stored


def _guard_reported_receipt(context, receipt, provenance: dict, env: dict, delivery: str, receipt_file: Path) -> None:
    """Apply the same identity check to the object about to be printed, when a receipt file exists."""
    if not _lexists(receipt_file):
        return
    _require_stored_receipt(context, receipt, provenance, env, delivery)


def _refuse_conflict(context, store_dir: Path, reason: str) -> None:
    message = reason
    if "this call did not launch" not in message:
        message += "; this call did not launch"
    if _lexists(store_dir / "launch.json"):
        message += "; a prior launch record remains"
    context.stop(message)


def _relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def exit_code(receipt: dict) -> int:
    state = receipt.get("state")
    transport = receipt.get("transport")
    if transport == "refused" or state == "refused":
        return 2
    if state in ("unknown", "uncertain", "accepted-not-launched") or transport in (
        "unknown",
        "uncertain",
        "timeout",
        "output-limit",
        "incomplete-output",
        "malformed",
        "crashed",
        "launch-failed",
    ):
        return 4
    if receipt.get("outcome_uncertain") is True:
        return 4
    collection = receipt.get("collection")
    claimed = receipt.get("claimed_outcome")
    if transport == "delivered" and collection == "collected" and claimed == "done":
        return 0
    if transport == "delivered" and collection == "uncollected":
        return 3
    if claimed == "failed" and collection == "collected":
        return 3
    return 4


def format_report(root: Path, receipt: dict, output_rel: str | None, receipt_path: Path | None) -> str:
    lines = [f"delivery_id: {receipt.get('delivery_id')}"]
    if receipt.get("worker_kind"):
        lines.append(f"worker_kind: {receipt['worker_kind']}")
    if receipt.get("state"):
        lines.append(f"state: {receipt['state']}")
    transport = receipt.get("transport") or receipt.get("state") or "unknown"
    if receipt.get("state") == "unknown":
        transport = "unknown"
    lines.append(f"transport: {transport}")
    claimed = receipt.get("claimed_outcome")
    lines.append("claimed_outcome: " + (claimed if isinstance(claimed, str) and claimed else "none"))
    collection = receipt.get("collection")
    if transport == "unknown" or receipt.get("state") == "unknown" or not isinstance(collection, str):
        collection = "not collected"
    lines.append(f"collection: {collection}")
    artifacts = receipt.get("artifacts") if isinstance(receipt.get("artifacts"), list) else []
    if artifacts and output_rel:
        for artifact in artifacts:
            lines.append(f"artifact: {output_rel}/{artifact['path']} sha256 {artifact['sha256']}")
    else:
        lines.append("artifact: none")
    if receipt_path is not None and receipt_path.is_file() and not _is_link(receipt_path):
        lines.append(f"receipt: {_relative(root, receipt_path)} sha256 {_sha256(receipt_path.read_bytes())}")
    else:
        lines.append("receipt: none")
    lines.append("review: not performed")
    lines.append("acceptance: not performed")
    if receipt.get("replayed") is True:
        lines.append("replayed: true")
    if receipt.get("recovered") is True:
        lines.append("recovered: true")
    cleanup = receipt.get("cleanup")
    if isinstance(cleanup, dict) and cleanup.get("retained"):
        lines.append("cleanup.retained: " + ", ".join(str(item) for item in cleanup["retained"]))
    reason = receipt.get("reason")
    if isinstance(reason, str) and reason and not (
        receipt.get("transport") == "delivered" and receipt.get("collection") == "collected"
    ):
        lines.append(f"reason: {reason}")
    return "\n".join(lines) + "\n"


def _report(context, root: Path, receipt: dict, output_rel: str | None, receipt_path: Path | None, store_dir: Path) -> Report:
    if receipt.get("transport") == "refused" or receipt.get("state") == "refused":
        _refuse_conflict(context, store_dir, str(receipt.get("reason") or "refused"))
    return Report(exit_code(receipt), format_report(root, receipt, output_rel, receipt_path))


def _prepare(context, code_root: Path, root: Path, explicit: str | None, execute: bool):
    config = context.load_config(code_root / "app" / "development-workspace.json")
    bridge_config = load_bridge_config(context, code_root)
    if context.is_filesystem_root(root):
        context.stop("fixture container is a filesystem root")
    if context.overlaps_live(root, code_root, config):
        context.stop("fixture root is the live workspace")
    container = context.select_container(root, code_root, explicit)
    context.guard_workspace_path(root, code_root)
    for relative in ("bridge", "bridge/declared", "bridge/delivery", "bridge/store", "bridge/provenance"):
        context.guard_workspace_path(context.resolve_under(root, relative), code_root)
    resolved = context.validate_context(root, config, execute=execute, runner_root=code_root)
    pinned = pin_and_import(context, code_root, bridge_config)
    return config, bridge_config, container, resolved, pinned


def _new_delivery(context, code_root, root, container, config, resolved, job, job_bytes, pinned, crash_before_receipt: bool) -> Report:
    adapter_mod, canon, envelope, ids, lab = pinned
    if job["work_ref"] != resolved.current_work:
        context.stop("work_ref is not the current work")
    profiles = _load_profiles(context, canon, lab)
    _profile(context, profiles, load_bridge_config(context, code_root)["allowed_kinds"], job["backend"])
    _verify_declared(context, code_root, root, job)
    delivery = job["delivery_id"]
    for relative in (
        f"bridge/delivery/{delivery}",
        f"bridge/delivery/{delivery}/input",
        f"bridge/delivery/{delivery}/output",
        f"bridge/store/{delivery}",
        f"bridge/provenance/{delivery}.json",
    ):
        if _lexists(context.resolve_under(root, relative)):
            if relative.startswith("bridge/store/"):
                context.stop("delivery store is already present; this call did not adopt it and did not launch")
            context.stop(f"{relative} is already present")
    tmp = context.resolve_under(root, f"bridge/provenance/{delivery}.json.tmp")
    if _lexists(tmp):
        context.stop("provenance temporary name is already present")
    _ensure_plain_dir(context, root / "bridge", "bridge")
    _ensure_plain_dir(context, root / "bridge" / "delivery", "bridge delivery")
    _ensure_plain_dir(context, root / "bridge" / "store", "bridge store")
    _ensure_plain_dir(context, root / "bridge" / "provenance", "bridge provenance")
    base = context.resolve_under(root, f"bridge/delivery/{delivery}")
    input_dir = base / "input"
    output_dir = base / "output"
    store_dir = context.resolve_under(root, f"bridge/store/{delivery}")
    _exclusive_dir(context, base, "per-delivery directory")
    _exclusive_dir(context, input_dir, "per-delivery input")
    _exclusive_dir(context, output_dir, "per-delivery output")
    _exclusive_dir(context, store_dir, "delivery store")
    _copy_inputs(context, code_root, root, job, input_dir)
    record_rel = config["assignment_record"].replace("\\", "/")
    record_path = context.resolve_under(root, record_rel)
    record_hash = _sha256(record_path.read_bytes())
    env = {
        "schema": REQUEST_SCHEMA,
        "delivery_id": delivery,
        "job_id": job["job_id"],
        "role": job["role"],
        "work_ref": job["work_ref"],
        "inputs": job["inputs"],
        "input_root": str(input_dir.resolve()),
        "output_root": str(output_dir.resolve()),
        "limits": job["limits"],
        "release": {"by": "fixture record", "ref": f"{record_rel} sha256 {record_hash}"},
        "backend": job["backend"],
    }
    try:
        request_sha = envelope.validate(env)
    except envelope.EnvelopeError as exc:
        context.stop(f"envelope: {exc}")
    provenance = {
        "schema": PROVENANCE_SCHEMA,
        "version": 1,
        "delivery_id": delivery,
        "job_id": job["job_id"],
        "work_ref": job["work_ref"],
        "container": str(container.resolve()),
        "job_sha256": _sha256(job_bytes),
        "assignment_record": record_rel,
        "assignment_sha256": record_hash,
        "request_sha256": request_sha,
        "input_root": f"bridge/delivery/{delivery}/input",
        "output_root": f"bridge/delivery/{delivery}/output",
        "store": "bridge/store",
        "backend": job["backend"],
    }
    prov_path = context.resolve_under(root, f"bridge/provenance/{delivery}.json")
    _write_exclusive(context, prov_path, canon.canonical(provenance), "provenance")
    adapter = adapter_mod.LocalProcessAdapter(root / "bridge" / "store", profiles, lab)
    receipt = adapter.deliver(env, _test_crash_before_receipt=crash_before_receipt)
    return _report(
        context,
        root,
        receipt,
        f"bridge/delivery/{delivery}/output",
        store_dir / "receipt.json",
        store_dir,
    )


def _replay(context, code_root, root, container, canon, job, job_bytes, pinned) -> Report:
    adapter_mod, canon_mod, _envelope, _ids, lab = pinned
    del canon_mod
    delivery = job["delivery_id"]
    store_dir = context.resolve_under(root, f"bridge/store/{delivery}")
    prov_path = context.resolve_under(root, f"bridge/provenance/{delivery}.json")
    if not (_lexists(prov_path) and (store_dir / "request.json").is_file()):
        context.stop("stored delivery does not match provenance; this call did not adopt it and did not launch")
    provenance = _load_provenance(context, canon, prov_path)
    if _sha256(job_bytes) != provenance["job_sha256"]:
        _refuse_conflict(
            context,
            store_dir,
            "delivery_id reused with a different request; use a new delivery_id",
        )
    env = _correlate(context, code_root, root, container, canon, provenance, delivery)
    receipt_file = store_dir / "receipt.json"
    _read_stored_receipt(context, canon, receipt_file, provenance, env, delivery)
    profiles = _load_profiles(context, canon, lab)
    adapter = adapter_mod.LocalProcessAdapter(root / "bridge" / "store", profiles, lab)
    receipt = adapter.deliver(env)
    _guard_reported_receipt(context, receipt, provenance, env, delivery, receipt_file)
    return _report(
        context,
        root,
        receipt,
        provenance["output_root"],
        receipt_file,
        store_dir,
    )


def _status(context, code_root, root, container, canon, ids, adapter_mod, lab, delivery: str) -> Report:
    _check_delivery(context, ids, delivery)
    store_dir = context.resolve_under(root, f"bridge/store/{delivery}")
    context.guard_workspace_path(store_dir, code_root)
    prov_path = context.resolve_under(root, f"bridge/provenance/{delivery}.json")
    output_rel = None
    if _lexists(prov_path) or _lexists(store_dir):
        if not prov_path.is_file():
            context.stop("stored delivery has no provenance; this call did not launch")
        provenance = _load_provenance(context, canon, prov_path)
        env = _correlate(context, code_root, root, container, canon, provenance, delivery)
        output_rel = provenance["output_root"]
        receipt_file = store_dir / "receipt.json"
        _read_stored_receipt(context, canon, receipt_file, provenance, env, delivery)
    else:
        provenance = None
        env = None
        receipt_file = store_dir / "receipt.json"
    profiles = _load_profiles(context, canon, lab)
    adapter = adapter_mod.LocalProcessAdapter(root / "bridge" / "store", profiles, lab)
    receipt = adapter.status(delivery)
    if provenance is not None and env is not None:
        _guard_reported_receipt(context, receipt, provenance, env, delivery, receipt_file)
    return _report(context, root, receipt, output_rel, receipt_file if receipt_file.is_file() else None, store_dir)


def _recover(context, code_root, root, container, canon, ids, adapter_mod, lab, delivery: str, recovery_path: Path) -> Report:
    _check_delivery(context, ids, delivery)
    request = context.load_json(recovery_path, kind="recovery request")
    _exact(context, request, RECOVERY_KEYS, "recovery request")
    if request["schema"] != RECOVERY_SCHEMA:
        context.stop("recovery request schema is not librarian-bridge-recovery")
    _version(context, request, "recovery request")
    for key in ("delivery_id", "request_sha256", "reason", "requester"):
        if not isinstance(request[key], str) or request[key].strip() == "":
            context.stop(f"recovery request field is empty: {key}")
    if request["delivery_id"] != delivery:
        context.stop("recovery request delivery does not match")
    digest = request["request_sha256"]
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        context.stop("recovery request hash is not sha256")
    store_dir = context.resolve_under(root, f"bridge/store/{delivery}")
    prov_path = context.resolve_under(root, f"bridge/provenance/{delivery}.json")
    if not prov_path.is_file():
        if not _lexists(store_dir):
            profiles = _load_profiles(context, canon, lab)
            adapter = adapter_mod.LocalProcessAdapter(root / "bridge" / "store", profiles, lab)
            receipt = adapter.recover(delivery)
            return _report(context, root, receipt, None, None, store_dir)
        context.stop("stored delivery has no provenance; this call did not launch")
    provenance = _load_provenance(context, canon, prov_path)
    env = _correlate(context, code_root, root, container, canon, provenance, delivery)
    if digest != provenance["request_sha256"] or digest != _sha256(canon.canonical(env)):
        context.stop("recovery request does not name the stored request; this call did not launch")
    receipt_file = store_dir / "receipt.json"
    _read_stored_receipt(context, canon, receipt_file, provenance, env, delivery)
    profiles = _load_profiles(context, canon, lab)
    adapter = adapter_mod.LocalProcessAdapter(root / "bridge" / "store", profiles, lab)
    receipt = adapter.recover(delivery)
    _guard_reported_receipt(context, receipt, provenance, env, delivery, receipt_file)
    return _report(
        context,
        root,
        receipt,
        provenance["output_root"],
        receipt_file if receipt_file.is_file() else None,
        store_dir,
    )


def perform(
    context,
    command: str,
    code_root: Path,
    root: Path,
    *,
    job_rel: str | None = None,
    delivery: str | None = None,
    recovery_rel: str | None = None,
    explicit: str | None = None,
    crash_before_receipt: bool = False,
) -> Report:
    """Run one bridge subcommand. Refusals raise context.Stop. The crash hook is not a CLI flag."""
    execute = command == "bridge-test"
    config, bridge_config, container, resolved, pinned = _prepare(context, code_root, root, explicit, execute)
    adapter_mod, canon, envelope, ids, lab = pinned
    del bridge_config
    if command == "bridge-test":
        if not isinstance(job_rel, str):
            context.stop("missing --job")
        job_path = context.resolve_under(root, job_rel)
        context.guard_workspace_path(job_path, code_root)
        if not job_path.is_file() or _is_link(job_path):
            context.stop("job is missing")
        job_bytes = job_path.read_bytes()
        job = _load_job(context, envelope, job_path)
        _check_delivery(context, ids, job["delivery_id"])
        store_dir = context.resolve_under(root, f"bridge/store/{job['delivery_id']}")
        prov_path = context.resolve_under(root, f"bridge/provenance/{job['delivery_id']}.json")
        if _lexists(prov_path) or _lexists(store_dir):
            if crash_before_receipt:
                context.stop("crash hook is only for a new delivery")
            return _replay(context, code_root, root, container, canon, job, job_bytes, pinned)
        return _new_delivery(
            context, code_root, root, container, config, resolved, job, job_bytes, pinned, crash_before_receipt
        )
    if command == "bridge-status":
        if not isinstance(delivery, str):
            context.stop("missing --delivery")
        return _status(context, code_root, root, container, canon, ids, adapter_mod, lab, delivery)
    if command == "bridge-recover":
        if not isinstance(delivery, str) or not isinstance(recovery_rel, str):
            context.stop("missing recovery request")
        recovery_path = context.resolve_under(root, recovery_rel)
        context.guard_workspace_path(recovery_path, code_root)
        if not recovery_path.is_file() or _is_link(recovery_path):
            context.stop("recovery request is missing")
        return _recover(
            context, code_root, root, container, canon, ids, adapter_mod, lab, delivery, recovery_path
        )
    context.stop("normal run is not activated")
