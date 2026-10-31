"""Check whether a declared Colab delivery supports its stated method.

The checker hashes declared bytes and evaluates a recorded smoke object.
It does not execute command text, decide truth, authorize work, or repair inputs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
from pathlib import Path


SCHEMA_REQUEST = "colab-readiness-request/1"
SCHEMA_REPORT = "colab-readiness/1"
LABEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")
DRIVE = re.compile(r"^[A-Za-z]:")
REPARSE = 0x400
REQUEST_LIMIT = 1048576

REQUEST_KEYS = {
    "schema",
    "purpose",
    "surface",
    "delivery_root",
    "output",
    "transport",
    "entry_points",
    "dependencies",
    "evidence",
    "references",
    "withholds",
    "smoke",
    "failure_policy",
    "independent_checks",
    "bounds",
}
PURPOSE_KEYS = {"statement", "mode", "question", "role", "method", "finish_boundary"}
SURFACE_KEYS = {
    "kind",
    "os",
    "interpreter",
    "network",
    "install",
    "secrets",
    "read_roots",
    "write_roots",
}
TRANSPORT_KEYS = {"path", "sha256", "bytes"}
ENTRY_KEYS = {"id", "path"}
DEPENDENCY_KEYS = {
    "id",
    "path",
    "sha256",
    "bytes",
    "role",
    "required",
    "needed_by",
    "invokes",
    "supply",
    "condition",
    "withhold_reason",
}
EVIDENCE_KEYS = {"category", "applicability", "reason", "refs"}
REFERENCE_KEYS = {"id", "format", "path", "follow_nested"}
WITHHOLD_KEYS = {"path", "reason"}
SMOKE_KEYS = {
    "status",
    "reason",
    "command",
    "child_exit",
    "wrapper_exit",
    "expected_state",
    "observed_state",
    "cutoff",
    "in_flight",
    "manual_fallback",
    "label",
    "page_sha256",
    "receipt_sha256",
    "pass_state_before",
    "pass_state_after",
    "custody",
    "judgment_label",
    "journal_operations",
}
POLICY_KEYS = {
    "declared",
    "retain_first_failure",
    "diagnostic",
    "dependency_check",
    "manual_fallback",
}
CHECK_KEYS = {"id", "text", "status"}
BOUNDS_KEYS = {"max_files", "max_file_bytes", "max_total_bytes"}
CONDITION_KEYS = {"text", "exercised"}
CATEGORIES = (
    "task-criteria",
    "director-constraints",
    "return-work-custody",
    "contract-code",
    "tests-evidence",
    "source-index",
    "capabilities",
    "fallback",
    "return-route",
)
ROLES = {
    "subject-runtime",
    "reviewer-assistance",
    "shared-subject-and-assistance",
    "source-under-review",
    "fixture",
    "evaluator-only",
}
SUPPLIES = {"supplied", "withheld", "unavailable", "preinstalled-verified"}
KNOWN_FORMATS = {
    "artifact-manifest/1",
    "prime-pack-sources/1",
    "review-packet-manifest/1",
    "colab-readiness-references/1",
}
MODES = {"return-review", "read-only"}
ACCESS = {"denied", "allowed", "unknown"}
SMOKE_STATUS = {"passed", "failed", "not-applicable", "not-run", "partial"}
LABELS = {"synthetic", "historical", "none"}
CHECK_STATUS = {"present", "absent", "not-established"}
BOUND_CAPS = {"max_files": 100000, "max_file_bytes": 20000000, "max_total_bytes": 50000000}
REPORT_KEYS = {
    "schema",
    "assembly",
    "mode",
    "transport_valid",
    "runtime_dependencies_resolved",
    "evidence_references_resolved",
    "minimum_evidence_satisfied",
    "smoke_result",
    "ready_for_declared_method",
    "semantic_sufficiency",
    "independent_proof",
    "exit_layers_differ",
    "surface_authorization",
    "shared_component",
    "facets",
    "limits",
    "problems",
}


class Refuse(Exception):
    pass


class Bound(Exception):
    pass


def canonical(value) -> bytes:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False)
    return (text + "\n").encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pairs(seq):
    out = {}
    for key, value in seq:
        if key in out:
            raise Refuse(f"duplicate JSON key {key}")
        out[key] = value
    return out


def reject_constant(name):
    raise Refuse(f"nonfinite JSON {name}")


def strict_json(data: bytes, label: str):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise Refuse(f"{label} is not UTF-8") from None
    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=reject_constant)
    except Refuse:
        raise
    except json.JSONDecodeError as exc:
        raise Refuse(f"{label} is not JSON ({exc.msg})") from None


def exact(value, keys: set[str], where: str) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        raise Refuse(f"{where} keys are not the contract set")
    return value


def prose(value, where: str) -> str:
    if not isinstance(value, str) or value.strip() == "":
        raise Refuse(f"{where} must be text")
    return value


def label(value, where: str) -> str:
    if not isinstance(value, str) or LABEL.fullmatch(value) is None:
        raise Refuse(f"{where} must be a label")
    return value


def flag(value, where: str) -> bool:
    if type(value) is not bool:
        raise Refuse(f"{where} must be boolean")
    return value


def whole(value, where: str, cap: int) -> int:
    if type(value) is not int or isinstance(value, bool) or not 1 <= value <= cap:
        raise Refuse(f"{where} is outside 1..{cap}")
    return value


def optional_hash(value, where: str):
    if value is None:
        return None
    if not isinstance(value, str) or HEX64.fullmatch(value) is None:
        raise Refuse(f"{where} must be 64 lowercase hex or null")
    return value


def optional_size(value, where: str):
    if value is None:
        return None
    if type(value) is not int or isinstance(value, bool) or value < 0:
        raise Refuse(f"{where} must be a non-negative integer or null")
    return value


def optional_text(value, where: str):
    if value is None:
        return None
    if not isinstance(value, str):
        raise Refuse(f"{where} must be a string or null")
    return value


def string_list(value, where: str) -> list:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise Refuse(f"{where} must be a list of strings")
    return value


def id_list(value, where: str, known: set[str] | None = None) -> list:
    if not isinstance(value, list):
        raise Refuse(f"{where} must be a list")
    out = []
    for item in value:
        out.append(label(item, where))
    if known is not None:
        missing = [item for item in out if item not in known]
        if missing:
            raise Refuse(f"{where} names an unknown id")
    return out


def relative_problem(value: str) -> str | None:
    if not isinstance(value, str) or value == "" or "\\" in value or value.startswith("/") or DRIVE.match(value):
        return "unsafe"
    if any(part in ("", ".", "..") for part in value.split("/")):
        return "unsafe"
    return None


def require_relative(value, where: str) -> str:
    if relative_problem(value):
        raise Refuse(f"{where} is not a contained relative path")
    return value


def is_link(path: Path) -> bool:
    try:
        info = os.lstat(path)
    except OSError:
        return False
    attrs = getattr(info, "st_file_attributes", 0) or 0
    return stat.S_ISLNK(info.st_mode) or bool(attrs & REPARSE)


def absolute_directory(text, where: str, must_exist: bool) -> Path:
    if not isinstance(text, str) or not os.path.isabs(text) or text.startswith(("\\\\", "//")):
        raise Refuse(f"{where} must be an absolute local path")
    path = Path(os.path.abspath(text))
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current = current / part
        if os.path.lexists(current) and is_link(current):
            raise Refuse(f"{where} passes through a link")
    if must_exist:
        if not path.is_dir() or is_link(path):
            raise Refuse(f"{where} must be an existing plain directory")
    return path


def contained(root: Path, rel: str) -> Path:
    current = root
    if is_link(root):
        raise Refuse("delivery root is a link")
    for part in rel.split("/"):
        current = current / part
        if os.path.lexists(current) and is_link(current):
            raise Refuse(f"link: {rel}")
    try:
        inside = os.path.commonpath(
            [os.path.normcase(str(root)), os.path.normcase(str(current))]
        ) == os.path.normcase(str(root))
    except ValueError:
        inside = False
    if not inside:
        raise Refuse(f"path escape: {rel}")
    return current


class Budget:
    def __init__(self, bounds: dict):
        self.max_files = bounds["max_files"]
        self.max_file_bytes = bounds["max_file_bytes"]
        self.max_total_bytes = bounds["max_total_bytes"]
        self.files = 0
        self.total = 0
        self.cache: dict[str, bytes] = {}

    def read(self, path: Path) -> bytes | None:
        key = os.path.normcase(os.path.abspath(path))
        if key in self.cache:
            return self.cache[key]
        if not os.path.lexists(path):
            return None
        if is_link(path):
            raise Refuse(f"link: {path.name}")
        if not stat.S_ISREG(os.lstat(path).st_mode):
            return None
        size = os.lstat(path).st_size
        if size > self.max_file_bytes or self.files + 1 > self.max_files or self.total + size > self.max_total_bytes:
            raise Bound(
                f"bound crossed at {path.name}: files {self.files}, bytes {self.total}, next {size}"
            )
        data = path.read_bytes()
        if len(data) != size:
            raise Bound(f"file changed while reading: {path.name}")
        self.files += 1
        self.total += len(data)
        self.cache[key] = data
        return data


def load_request(path_text: str) -> dict:
    if not isinstance(path_text, str) or not os.path.isabs(path_text):
        raise Refuse("request must be an absolute path")
    path = Path(os.path.abspath(path_text))
    if is_link(path) or not path.is_file():
        raise Refuse("request must be a regular file")
    if path.stat().st_size > REQUEST_LIMIT:
        raise Refuse("request is over the 1 MiB bound")
    body = strict_json(path.read_bytes(), "request")
    return exact(body, REQUEST_KEYS, "request")


def validate(request: dict) -> None:
    if request["schema"] != SCHEMA_REQUEST:
        raise Refuse("unsupported request schema")
    purpose = exact(request["purpose"], PURPOSE_KEYS, "purpose")
    for key in PURPOSE_KEYS - {"mode"}:
        prose(purpose[key], f"purpose.{key}")
    if purpose["mode"] not in MODES:
        raise Refuse("purpose.mode is not return-review or read-only")
    surface = exact(request["surface"], SURFACE_KEYS, "surface")
    for key in ("kind", "os", "interpreter", "secrets"):
        prose(surface[key], f"surface.{key}")
    if surface["network"] not in ACCESS or surface["install"] not in ACCESS:
        raise Refuse("surface network and install must be denied, allowed, or unknown")
    for key in ("read_roots", "write_roots"):
        roots = surface[key]
        if not isinstance(roots, list):
            raise Refuse(f"surface.{key} must be a list")
        for item in roots:
            if not isinstance(item, str) or not os.path.isabs(item) or item.startswith(("\\\\", "//")):
                raise Refuse(f"surface.{key} must contain absolute local paths")
    absolute_directory(request["delivery_root"], "delivery_root", True)
    output = absolute_directory(request["output"], "output", False)
    if output.exists():
        raise Refuse("output exists")
    if not output.parent.is_dir() or is_link(output.parent):
        raise Refuse("output parent must be an existing plain directory")
    if os.path.normcase(str(output)) == os.path.normcase(str(Path(request["delivery_root"]))):
        raise Refuse("output must not be the delivery root")

    transport = request["transport"]
    if not isinstance(transport, list) or not transport:
        raise Refuse("transport must be a non-empty list")
    seen_paths = set()
    for index, row in enumerate(transport):
        exact(row, TRANSPORT_KEYS, f"transport[{index}]")
        require_relative(row["path"], f"transport[{index}].path")
        if HEX64.fullmatch(row["sha256"] or "") is None:
            raise Refuse(f"transport[{index}].sha256 must be 64 lowercase hex")
        if type(row["bytes"]) is not int or row["bytes"] < 0:
            raise Refuse(f"transport[{index}].bytes must be a non-negative integer")
        if row["path"] in seen_paths:
            raise Refuse(f"duplicate transport path {row['path']}")
        seen_paths.add(row["path"])

    entries = request["entry_points"]
    if not isinstance(entries, list) or not entries:
        raise Refuse("entry_points must be a non-empty list")
    seen_ids = set()
    for index, row in enumerate(entries):
        exact(row, ENTRY_KEYS, f"entry_points[{index}]")
        label(row["id"], f"entry_points[{index}].id")
        require_relative(row["path"], f"entry_points[{index}].path")
        if row["path"] not in seen_paths:
            raise Refuse(f"entry point {row['id']} is not a transport path")
        if row["id"] in seen_ids:
            raise Refuse(f"duplicate entry id {row['id']}")
        seen_ids.add(row["id"])

    dependencies = request["dependencies"]
    if not isinstance(dependencies, list):
        raise Refuse("dependencies must be a list")
    dep_ids = []
    for index, row in enumerate(dependencies):
        exact(row, DEPENDENCY_KEYS, f"dependencies[{index}]")
        label(row["id"], f"dependencies[{index}].id")
        require_relative(row["path"], f"dependencies[{index}].path")
        optional_hash(row["sha256"], f"dependencies[{index}].sha256")
        optional_size(row["bytes"], f"dependencies[{index}].bytes")
        if row["role"] not in ROLES:
            raise Refuse(f"dependencies[{index}].role is unknown")
        flag(row["required"], f"dependencies[{index}].required")
        if row["supply"] not in SUPPLIES:
            raise Refuse(f"dependencies[{index}].supply is unknown")
        if row["condition"] is not None:
            exact(row["condition"], CONDITION_KEYS, f"dependencies[{index}].condition")
            prose(row["condition"]["text"], f"dependencies[{index}].condition.text")
            flag(row["condition"]["exercised"], f"dependencies[{index}].condition.exercised")
        optional_text(row["withhold_reason"], f"dependencies[{index}].withhold_reason")
        if row["id"] in dep_ids:
            raise Refuse(f"duplicate dependency id {row['id']}")
        dep_ids.append(row["id"])
    known = set(dep_ids)
    for index, row in enumerate(dependencies):
        id_list(row["needed_by"], f"dependencies[{index}].needed_by", known)
        id_list(row["invokes"], f"dependencies[{index}].invokes", known)

    evidence = request["evidence"]
    if not isinstance(evidence, list):
        raise Refuse("evidence must be a list")
    found = []
    for index, row in enumerate(evidence):
        exact(row, EVIDENCE_KEYS, f"evidence[{index}]")
        if row["category"] not in CATEGORIES:
            raise Refuse(f"evidence[{index}].category is unknown")
        if row["applicability"] not in {"required", "not-applicable"}:
            raise Refuse(f"evidence[{index}].applicability is unknown")
        prose(row["reason"], f"evidence[{index}].reason")
        if not isinstance(row["refs"], list) or any(not isinstance(item, str) for item in row["refs"]):
            raise Refuse(f"evidence[{index}].refs must be a list of strings")
        if row["applicability"] == "required" and not row["refs"]:
            raise Refuse(f"evidence[{index}] required category has no refs")
        if row["applicability"] == "not-applicable" and row["refs"]:
            raise Refuse(f"evidence[{index}] not-applicable category has refs")
        found.append(row["category"])
    if found != list(CATEGORIES) and sorted(found) != sorted(CATEGORIES):
        raise Refuse("evidence categories are not the nine required names")
    if len(found) != len(set(found)):
        raise Refuse("evidence category is repeated")

    references = request["references"]
    if not isinstance(references, list):
        raise Refuse("references must be a list")
    ref_ids = []
    for index, row in enumerate(references):
        exact(row, REFERENCE_KEYS, f"references[{index}]")
        label(row["id"], f"references[{index}].id")
        if not isinstance(row["format"], str) or row["format"].strip() == "":
            raise Refuse(f"references[{index}].format must be text")
        require_relative(row["path"], f"references[{index}].path")
        flag(row["follow_nested"], f"references[{index}].follow_nested")
        if row["id"] in ref_ids:
            raise Refuse(f"duplicate reference id {row['id']}")
        ref_ids.append(row["id"])
    known_refs = set(ref_ids)
    for index, row in enumerate(evidence):
        if any(item not in known_refs for item in row["refs"]):
            raise Refuse(f"evidence[{index}] names an unknown reference")

    withholds = request["withholds"]
    if not isinstance(withholds, list):
        raise Refuse("withholds must be a list")
    for index, row in enumerate(withholds):
        exact(row, WITHHOLD_KEYS, f"withholds[{index}]")
        require_relative(row["path"], f"withholds[{index}].path")
        prose(row["reason"], f"withholds[{index}].reason")

    smoke = exact(request["smoke"], SMOKE_KEYS, "smoke")
    if smoke["status"] not in SMOKE_STATUS:
        raise Refuse("smoke.status is unknown")
    if smoke["label"] not in LABELS:
        raise Refuse("smoke.label is unknown")
    prose(smoke["reason"], "smoke.reason")
    if smoke["command"] is not None and not isinstance(smoke["command"], str):
        raise Refuse("smoke.command must be a string or null")
    for key in ("child_exit", "wrapper_exit"):
        if smoke[key] is not None and type(smoke[key]) is not int:
            raise Refuse(f"smoke.{key} must be an integer or null")
    for key in (
        "expected_state",
        "observed_state",
        "pass_state_before",
        "pass_state_after",
        "custody",
        "judgment_label",
    ):
        optional_text(smoke[key], f"smoke.{key}")
    if not isinstance(smoke["cutoff"], str):
        raise Refuse("smoke.cutoff must be a string")
    string_list(smoke["in_flight"], "smoke.in_flight")
    string_list(smoke["journal_operations"], "smoke.journal_operations")
    flag(smoke["manual_fallback"], "smoke.manual_fallback")
    for key in ("page_sha256", "receipt_sha256"):
        optional_hash(smoke[key], f"smoke.{key}")

    policy = exact(request["failure_policy"], POLICY_KEYS, "failure_policy")
    flag(policy["declared"], "failure_policy.declared")
    flag(policy["retain_first_failure"], "failure_policy.retain_first_failure")
    for key in ("diagnostic", "dependency_check", "manual_fallback"):
        if not isinstance(policy[key], str):
            raise Refuse(f"failure_policy.{key} must be a string")

    checks = request["independent_checks"]
    if not isinstance(checks, list):
        raise Refuse("independent_checks must be a list")
    seen_checks = set()
    for index, row in enumerate(checks):
        exact(row, CHECK_KEYS, f"independent_checks[{index}]")
        label(row["id"], f"independent_checks[{index}].id")
        prose(row["text"], f"independent_checks[{index}].text")
        if row["status"] not in CHECK_STATUS:
            raise Refuse(f"independent_checks[{index}].status is unknown")
        if row["id"] in seen_checks:
            raise Refuse(f"duplicate independent check {row['id']}")
        seen_checks.add(row["id"])

    bounds = exact(request["bounds"], BOUNDS_KEYS, "bounds")
    for key, cap in BOUND_CAPS.items():
        whole(bounds[key], f"bounds.{key}", cap)


def blank_report(mode: str) -> dict:
    return {
        "schema": SCHEMA_REPORT,
        "assembly": "partial",
        "mode": mode,
        "transport_valid": False,
        "runtime_dependencies_resolved": False,
        "evidence_references_resolved": False,
        "minimum_evidence_satisfied": False,
        "smoke_result": "not-run",
        "ready_for_declared_method": False,
        "semantic_sufficiency": "not-established",
        "independent_proof": "not-established",
        "exit_layers_differ": None,
        "surface_authorization": "not-established",
        "shared_component": False,
        "facets": {
            "transport": {"rows": [], "problems": []},
            "runtime": {"closure": [], "entries": [], "rows": [], "problems": []},
            "evidence": {"references": [], "problems": []},
            "minimum": {"categories": [], "problems": []},
            "smoke": {
                "command_executed": False,
                "problems": [],
                "final_stage": None,
                "success_exit": None,
                "child_exit": None,
                "wrapper_exit": None,
            },
            "ready": {"problems": []},
        },
        "limits": [],
        "problems": [],
    }


def file_matches(budget: Budget, path: Path, digest: str, size: int) -> tuple[bool, str | None]:
    data = budget.read(path)
    if data is None:
        return False, "missing"
    if len(data) != size or sha256(data) != digest:
        return False, "changed"
    return True, None


def manifests_of(data: bytes):
    try:
        value = strict_json(data, "manifest")
    except Refuse:
        return None
    if isinstance(value, dict) and isinstance(value.get("schema"), str):
        return value
    return None


def row_identity(row: dict) -> tuple[bool, str, str, int]:
    path = row.get("path")
    digest = row.get("sha256")
    size = row.get("bytes")
    ok = (
        isinstance(path, str)
        and relative_problem(path) is None
        and isinstance(digest, str)
        and HEX64.fullmatch(digest) is not None
        and type(size) is int
        and size >= 0
    )
    return ok, path if isinstance(path, str) else "", digest if isinstance(digest, str) else "", size if type(size) is int else -1


def check_rows(
    budget: Budget,
    base: Path,
    rows: list,
    follow: bool,
    depth: int,
    problems: list,
    members: list,
) -> bool:
    if not isinstance(rows, list):
        problems.append("rows are not a list")
        return False
    seen = set()
    ok = True
    for row in rows:
        if not isinstance(row, dict):
            problems.append("row is not an object")
            ok = False
            continue
        good, rel, digest, size = row_identity(row)
        if not good:
            problems.append("row fields are incomplete or unsafe")
            ok = False
            continue
        if rel in seen:
            problems.append(f"duplicate row path {rel}")
            ok = False
            continue
        seen.add(rel)
        target = base
        escaped = False
        for part in rel.split("/"):
            target = target / part
            if os.path.lexists(target) and is_link(target):
                problems.append(f"link: {rel}")
                ok = False
                escaped = True
                break
        if escaped:
            continue
        matched, reason = file_matches(budget, target, digest, size)
        if not matched:
            problems.append(f"{reason}: {rel}")
            ok = False
            continue
        descended = False
        if follow:
            opened = budget.cache[os.path.normcase(os.path.abspath(target))]
            nested = manifests_of(opened)
            if nested is not None and nested.get("schema") in KNOWN_FORMATS:
                descended = True
                schema = nested.get("schema")
                if depth >= 4:
                    problems.append("nested reference depth exceeded")
                    ok = False
                elif not descend(
                    budget,
                    target.parent if schema == "prime-pack-sources/1" else base,
                    nested,
                    True,
                    depth + 1,
                    problems,
                    schema,
                    target,
                    members,
                ):
                    ok = False
        if not descended:
            members.append(rel)
    return ok


def descend(
    budget,
    delivery,
    value,
    follow,
    depth,
    problems,
    schema,
    manifest_path: Path,
    members: list,
) -> bool:
    if schema == "artifact-manifest/1":
        return check_rows(budget, delivery, value.get("artifacts"), follow, depth, problems, members)
    if schema == "colab-readiness-references/1":
        return check_rows(budget, delivery, value.get("items"), follow, depth, problems, members)
    if schema == "review-packet-manifest/1":
        return check_rows(budget, manifest_path.parent, value.get("files"), follow, depth, problems, members)
    if schema == "prime-pack-sources/1":
        sources = value.get("sources")
        if not isinstance(sources, list):
            problems.append("sources are not a list")
            return False
        ok = True
        seen = set()
        for row in sources:
            if not isinstance(row, dict):
                problems.append("source row is not an object")
                ok = False
                continue
            snapshot = row.get("snapshot")
            digest = row.get("sha256")
            size = row.get("bytes")
            good = (
                isinstance(snapshot, str)
                and relative_problem(snapshot) is None
                and isinstance(digest, str)
                and HEX64.fullmatch(digest) is not None
                and type(size) is int
                and size >= 0
            )
            if not good:
                problems.append("snapshot row is incomplete or unsafe")
                ok = False
                continue
            if snapshot in seen:
                problems.append(f"duplicate snapshot {snapshot}")
                ok = False
                continue
            seen.add(snapshot)
            target = manifest_path.parent
            escaped = False
            for part in snapshot.split("/"):
                target = target / part
                if os.path.lexists(target) and is_link(target):
                    problems.append(f"link: {snapshot}")
                    ok = False
                    escaped = True
                    break
            if escaped:
                continue
            matched, reason = file_matches(budget, target, digest, size)
            if not matched:
                problems.append(f"{reason}: {snapshot}")
                ok = False
                continue
            descended = False
            if follow:
                opened = budget.cache[os.path.normcase(os.path.abspath(target))]
                nested = manifests_of(opened)
                if nested is not None and nested.get("schema") in KNOWN_FORMATS:
                    descended = True
                    child_schema = nested.get("schema")
                    if depth >= 4:
                        problems.append("nested reference depth exceeded")
                        ok = False
                    elif not descend(
                        budget,
                        delivery,
                        nested,
                        True,
                        depth + 1,
                        problems,
                        child_schema,
                        target,
                        members,
                    ):
                        ok = False
            if not descended:
                members.append(snapshot)
        return ok
    problems.append(f"unsupported schema {schema}")
    return False


def closure_of(entries: list, dependencies: list) -> set[str]:
    selected = set()
    for entry in entries:
        for dep in dependencies:
            if dep["path"] == entry["path"]:
                selected.add(dep["id"])
    changed = True
    while changed:
        changed = False
        for dep in dependencies:
            if dep["id"] in selected:
                for name in dep["invokes"]:
                    if name not in selected:
                        selected.add(name)
                        changed = True
            elif any(name in selected for name in dep["needed_by"]):
                selected.add(dep["id"])
                changed = True
    return selected


def invoke_cycles(selected: set[str], dependencies: list) -> list[str]:
    invokes = {dep["id"]: list(dep["invokes"]) for dep in dependencies}
    color = {name: 0 for name in selected}
    found = []

    def walk(name: str, stack: list[str]) -> None:
        color[name] = 1
        stack.append(name)
        for nxt in invokes.get(name, []):
            if nxt not in color:
                continue
            if color[nxt] == 1:
                found.append(" -> ".join(stack[stack.index(nxt):] + [nxt]))
            elif color[nxt] == 0:
                walk(nxt, stack)
        stack.pop()
        color[name] = 2

    for name in sorted(selected):
        if color[name] == 0:
            walk(name, [])
    return found


def subsequence(items: list[str], wanted: tuple[str, ...]) -> bool:
    index = 0
    for item in items:
        if index < len(wanted) and item == wanted[index]:
            index += 1
    return index == len(wanted)


def evaluate(request: dict) -> dict:
    report = blank_report(request["purpose"]["mode"])
    budget = Budget(request["bounds"])
    root = Path(os.path.abspath(request["delivery_root"]))
    try:
        evaluate_into(request, report, budget, root)
        report["assembly"] = "complete"
    except Bound as exc:
        report["assembly"] = "partial"
        report["problems"].append(str(exc))
        report["ready_for_declared_method"] = False
        if report["smoke_result"] not in SMOKE_STATUS:
            report["smoke_result"] = "not-run"
    finish_limits(request, report)
    return report


def evaluate_into(request: dict, report: dict, budget: Budget, root: Path) -> None:
    transport_rows = []
    transport_ok = {}
    by_path = {}
    for row in request["transport"]:
        by_path[row["path"]] = row
        try:
            path = contained(root, row["path"])
        except Refuse as exc:
            raise Refuse(str(exc)) from None
        if os.path.lexists(path) and is_link(path):
            raise Refuse(f"link: {row['path']}")
        matched, reason = file_matches(budget, path, row["sha256"], row["bytes"])
        transport_ok[row["path"]] = matched
        transport_rows.append({"path": row["path"], "match": matched, "problem": reason})
        if reason:
            report["facets"]["transport"]["problems"].append(f"{reason}: {row['path']}")
    report["facets"]["transport"]["rows"] = transport_rows
    report["transport_valid"] = all(item["match"] for item in transport_rows)

    dependencies = request["dependencies"]
    selected = closure_of(request["entry_points"], dependencies)
    report["facets"]["runtime"]["closure"] = sorted(selected)
    cycles = invoke_cycles(selected, dependencies)
    runtime_problems = report["facets"]["runtime"]["problems"]
    for cycle in cycles:
        runtime_problems.append(f"dependency cycle: {cycle}")
    accounted_paths = {dep["path"] for dep in dependencies}
    entry_rows = []
    for entry in request["entry_points"]:
        accounted = entry["path"] in accounted_paths
        entry_rows.append({"id": entry["id"], "path": entry["path"], "accounted": accounted})
        if not accounted:
            runtime_problems.append(f"entry point has no dependency record: {entry['id']}")
    report["facets"]["runtime"]["entries"] = entry_rows
    withheld = {row["path"] for row in request["withholds"]}
    hard = bool(cycles) or any(not row["accounted"] for row in entry_rows)
    unknown = False
    rows = []
    for dep in dependencies:
        in_closure = dep["id"] in selected
        problems = []
        state = "not-in-closure"
        if dep["role"] == "shared-subject-and-assistance":
            report["shared_component"] = True
        if dep["required"] and not in_closure:
            problems.append("required dependency is outside the entry closure")
            hard = True
            state = "outside"
        if dep["supply"] == "supplied":
            if dep["sha256"] is None or dep["bytes"] is None:
                problems.append("null source binding")
                hard = True
                state = "null-binding"
            else:
                carried = by_path.get(dep["path"])
                if carried is None or carried["sha256"] != dep["sha256"] or carried["bytes"] != dep["bytes"]:
                    problems.append("dependency bytes are not the transported file")
                    hard = True
                    state = "untransported"
                elif not transport_ok.get(dep["path"], False):
                    problems.append("transported file does not match")
                    hard = True
                    state = "mismatch"
                elif state == "not-in-closure":
                    state = "supplied"
        elif dep["supply"] == "withheld":
            if dep["path"] not in withheld or not dep["withhold_reason"]:
                problems.append("withheld dependency is not listed with a reason")
                hard = True
                state = "withhold-unlisted"
            elif dep["required"]:
                problems.append("required dependency is withheld")
                hard = True
                state = "withheld"
            else:
                state = "withheld-optional"
        elif dep["supply"] == "unavailable":
            if dep["required"]:
                problems.append("required dependency is unavailable")
                hard = True
                state = "unavailable"
            else:
                state = "unavailable-optional"
        elif dep["supply"] == "preinstalled-verified" and (in_closure or dep["required"]):
            problems.append("preinstalled dependency was not measured")
            unknown = True
            state = "unknown"
        if dep["required"] and isinstance(dep["condition"], dict) and dep["condition"]["exercised"] is False:
            problems.append("required condition was not exercised")
            hard = True
            state = "condition-not-exercised"
        for item in problems:
            runtime_problems.append(f"{dep['id']}: {item}")
        rows.append(
            {
                "id": dep["id"],
                "state": state,
                "problem": "; ".join(problems) if problems else None,
                "in_closure": in_closure,
            }
        )
    report["facets"]["runtime"]["rows"] = rows
    if hard:
        report["runtime_dependencies_resolved"] = False
    elif unknown:
        report["runtime_dependencies_resolved"] = "unknown"
    else:
        report["runtime_dependencies_resolved"] = True

    evidence_problems = report["facets"]["evidence"]["problems"]
    unsupported = False
    evidence_ok = True
    ref_ok = {}
    ref_members = {}
    for ref in request["references"]:
        item_problems = []
        if ref["format"] not in KNOWN_FORMATS:
            item_problems.append(f"unsupported format {ref['format']}")
            unsupported = True
            evidence_ok = False
            ref_ok[ref["id"]] = False
            ref_members[ref["id"]] = []
            report["facets"]["evidence"]["references"].append(
                {"id": ref["id"], "resolved": False, "members": [], "problems": item_problems}
            )
            continue
        try:
            path = contained(root, ref["path"])
        except Refuse as exc:
            item_problems.append(str(exc))
            evidence_ok = False
            ref_ok[ref["id"]] = False
            ref_members[ref["id"]] = []
            report["facets"]["evidence"]["references"].append(
                {"id": ref["id"], "resolved": False, "members": [], "problems": item_problems}
            )
            continue
        if os.path.lexists(path) and is_link(path):
            item_problems.append(f"link: {ref['path']}")
            evidence_ok = False
            ref_ok[ref["id"]] = False
            ref_members[ref["id"]] = []
            report["facets"]["evidence"]["references"].append(
                {"id": ref["id"], "resolved": False, "members": [], "problems": item_problems}
            )
            continue
        data = budget.read(path)
        members = []
        if data is None:
            item_problems.append("missing")
            evidence_ok = False
            ref_ok[ref["id"]] = False
        else:
            carried = by_path.get(ref["path"])
            actual = sha256(data)
            if carried is None:
                item_problems.append("reference root is not transported")
                evidence_ok = False
                ref_ok[ref["id"]] = False
            elif carried["sha256"] != actual or carried["bytes"] != len(data):
                item_problems.append("reference root does not match the transported declaration")
                evidence_ok = False
                ref_ok[ref["id"]] = False
            else:
                value = manifests_of(data)
                if not isinstance(value, dict) or value.get("schema") != ref["format"]:
                    item_problems.append("manifest schema does not match the declared format")
                    evidence_ok = False
                    ref_ok[ref["id"]] = False
                else:
                    resolved = descend(
                        budget,
                        root,
                        value,
                        ref["follow_nested"],
                        1,
                        item_problems,
                        ref["format"],
                        path,
                        members,
                    )
                    ref_ok[ref["id"]] = resolved and not item_problems
                    evidence_ok = evidence_ok and ref_ok[ref["id"]]
        ref_members[ref["id"]] = members
        evidence_problems.extend(f"{ref['id']}: {item}" for item in item_problems)
        report["facets"]["evidence"]["references"].append(
            {
                "id": ref["id"],
                "resolved": ref_ok[ref["id"]],
                "members": members,
                "problems": item_problems,
            }
        )
    if unsupported:
        report["evidence_references_resolved"] = "unsupported"
    elif evidence_ok:
        report["evidence_references_resolved"] = True
    else:
        report["evidence_references_resolved"] = False

    minimum_ok = True
    for row in request["evidence"]:
        problems = []
        members = []
        if row["applicability"] == "required":
            for ref_id in row["refs"]:
                if not ref_ok.get(ref_id, False):
                    problems.append(f"ref {ref_id} did not resolve")
                else:
                    members.extend(ref_members.get(ref_id, []))
            if not problems and not members:
                problems.append("resolved no evidence material")
        if problems:
            minimum_ok = False
        report["facets"]["minimum"]["categories"].append(
            {
                "category": row["category"],
                "applicability": row["applicability"],
                "satisfied": not problems,
                "members": sorted(set(members)),
                "problems": problems,
            }
        )
        report["facets"]["minimum"]["problems"].extend(
            f"{row['category']}: {item}" for item in problems
        )
    report["minimum_evidence_satisfied"] = minimum_ok
    report["semantic_sufficiency"] = "not-established"

    smoke = request["smoke"]
    smoke_problems = []
    result = smoke["status"]
    child = smoke["child_exit"]
    wrapper = smoke["wrapper_exit"]
    if child is None and wrapper is None:
        report["exit_layers_differ"] = False
    elif type(child) is int and type(wrapper) is int:
        report["exit_layers_differ"] = child != wrapper
    else:
        report["exit_layers_differ"] = None
    if request["purpose"]["mode"] == "read-only":
        result, smoke_problems = read_only_smoke(smoke, report["exit_layers_differ"])
    else:
        result, smoke_problems = return_review_smoke(smoke, report["exit_layers_differ"])
    report["smoke_result"] = result
    report["facets"]["smoke"]["problems"] = smoke_problems
    report["facets"]["smoke"]["command_executed"] = False
    if request["purpose"]["mode"] == "return-review":
        report["facets"]["smoke"]["final_stage"] = "reviewed-reread"
        report["facets"]["smoke"]["success_exit"] = 0
    report["facets"]["smoke"]["child_exit"] = smoke["child_exit"]
    report["facets"]["smoke"]["wrapper_exit"] = smoke["wrapper_exit"]

    ready_problems = []
    policy = request["failure_policy"]
    if report["transport_valid"] is not True:
        ready_problems.append("transport is not valid")
    if report["runtime_dependencies_resolved"] is not True:
        ready_problems.append("runtime dependencies are not resolved")
    if report["evidence_references_resolved"] is not True:
        ready_problems.append("evidence references are not resolved")
    if report["minimum_evidence_satisfied"] is not True:
        ready_problems.append("minimum evidence is not satisfied")
    if request["purpose"]["mode"] == "read-only":
        if report["smoke_result"] != "not-applicable":
            ready_problems.append("read-only smoke is not not-applicable")
    elif report["smoke_result"] != "passed":
        ready_problems.append("smoke did not pass")
    if not policy["declared"] or not policy["retain_first_failure"]:
        ready_problems.append("failure policy is not declared to retain the first failure")
    for key in ("diagnostic", "dependency_check", "manual_fallback"):
        if policy[key].strip() == "":
            ready_problems.append(f"failure policy {key} is empty")
    surface = request["surface"]
    if surface["network"] != "denied" or surface["install"] != "denied":
        ready_problems.append("network or install is not denied; authorization is not established")
    if report["exit_layers_differ"] is not False:
        ready_problems.append("child and wrapper exits are not both recorded as equal")
    report["facets"]["ready"]["problems"] = ready_problems
    report["ready_for_declared_method"] = not ready_problems
    report["problems"] = list(
        dict.fromkeys(
            report["facets"]["transport"]["problems"]
            + report["facets"]["runtime"]["problems"]
            + report["facets"]["evidence"]["problems"]
            + report["facets"]["minimum"]["problems"]
            + smoke_problems
            + ready_problems
        )
    )


def read_only_smoke(smoke: dict, layers) -> tuple[str, list[str]]:
    problems = []
    if smoke["status"] != "not-applicable":
        problems.append("read-only smoke must be not-applicable")
    if smoke["label"] != "none":
        problems.append("read-only smoke label must be none")
    if smoke["manual_fallback"]:
        problems.append("manual fallback is not a read-only result")
    if smoke["in_flight"] or smoke["journal_operations"]:
        problems.append("read-only smoke records execution events")
    if smoke["child_exit"] is not None or smoke["wrapper_exit"] is not None:
        problems.append("read-only smoke records an exit")
    for key in ("page_sha256", "receipt_sha256", "pass_state_before", "pass_state_after", "custody", "judgment_label", "expected_state", "observed_state"):
        if smoke[key] is not None:
            problems.append(f"read-only smoke sets {key}")
    if layers not in (False, None):
        problems.append("exit layers differ")
    if problems:
        return "failed", problems
    return "not-applicable", []


def return_review_smoke(smoke: dict, layers) -> tuple[str, list[str]]:
    status = smoke["status"]
    if status == "not-run":
        return "not-run", []
    if status == "not-applicable":
        return "failed", ["return-review smoke cannot be not-applicable"]
    if status in {"failed", "partial"}:
        problems = []
        if smoke["manual_fallback"] and status == "passed":
            problems.append("manual fallback is not assisted success")
        if layers is True and status == "passed":
            return "partial", ["child exit differs from wrapper exit"]
        return status, problems
    problems = []
    if smoke["manual_fallback"]:
        problems.append("manual fallback is not assisted success")
    if smoke["label"] not in {"synthetic", "historical"} or smoke["judgment_label"] != smoke["label"]:
        problems.append("judgment label does not match the smoke label")
    if smoke["page_sha256"] is None or smoke["receipt_sha256"] is None:
        problems.append("page or receipt hash is missing")
    if smoke["pass_state_before"] != "awaiting-review" or smoke["pass_state_after"] != "reviewed":
        problems.append("pass states are not awaiting-review then reviewed")
    if smoke["custody"] != "complete":
        problems.append("custody is not complete")
    if smoke["expected_state"] != smoke["observed_state"] or not smoke["observed_state"]:
        problems.append("expected state does not equal observed state")
    if smoke["observed_state"] in {"no-return", "observation-failed"}:
        problems.append("unusable observed state cannot satisfy a passed smoke")
    if smoke["in_flight"]:
        problems.append("operations were still in flight")
    if type(smoke["child_exit"]) is not int:
        problems.append("child exit is missing")
    if type(smoke["wrapper_exit"]) is not int:
        problems.append("wrapper exit is missing")
    if smoke["cutoff"].strip() == "":
        problems.append("cutoff is empty")
    if not subsequence(smoke["journal_operations"], ("read", "record", "read")):
        problems.append("journal operations do not contain read, record, read")
    if smoke["command"] is None:
        problems.append("smoke command text is missing")
    elif smoke["command"].strip() == "":
        problems.append("smoke command text is empty")
    if (
        layers is not True
        and type(smoke["child_exit"]) is int
        and type(smoke["wrapper_exit"]) is int
        and (smoke["child_exit"] != 0 or smoke["wrapper_exit"] != 0)
    ):
        problems.append(
            "reviewed-reread exits are not the successful exit 0"
            f"; child {smoke['child_exit']}; wrapper {smoke['wrapper_exit']}"
        )
    if layers is True:
        return "partial", problems + ["child exit differs from wrapper exit"]
    if problems:
        return "failed", problems
    return "passed", []


def finish_limits(request: dict, report: dict) -> None:
    limits = [
        "semantic sufficiency is not established",
        "independent proof is not established",
        "surface authorization is not established",
        "command text was not executed",
        "the checker validated a supplied smoke record and did not execute or authenticate it",
        "tokens, cost, and clocks are unknown",
    ]
    if not request["independent_checks"]:
        limits.append("independent checks are empty")
    else:
        limits.append("listed independent checks do not establish independent proof")
    if report["shared_component"]:
        limits.append("a shared subject and assistance component is present; its own output is not proof")
    if report["assembly"] == "partial":
        limits.append("the report stopped at a bound and kept the partial result")
    report["limits"] = limits


def render(report: dict) -> str:
    def yn(value) -> str:
        if value is True:
            return "true"
        if value is False:
            return "false"
        return str(value)

    lines = [
        "# Readiness",
        "",
        f"Assembly: {report['assembly']}. Mode: {report['mode']}.",
        "This report does not establish semantic sufficiency, acceptance, or authorization.",
        "",
        "## Transport",
        "",
        f"transport_valid: {yn(report['transport_valid'])}",
    ]
    for row in report["facets"]["transport"]["rows"]:
        lines.append(f"- {row['path']}: match {yn(row['match'])}; problem {row['problem']}")
    for item in report["facets"]["transport"]["problems"]:
        lines.append(f"- problem: {item}")
    lines += ["", "## Runtime dependencies", "", f"runtime_dependencies_resolved: {yn(report['runtime_dependencies_resolved'])}"]
    lines.append("closure: " + (", ".join(report["facets"]["runtime"]["closure"]) or "(empty)"))
    for row in report["facets"]["runtime"]["entries"]:
        lines.append(f"- entry {row['id']}: accounted {yn(row['accounted'])}")
    for row in report["facets"]["runtime"]["rows"]:
        lines.append(f"- {row['id']}: {row['state']}; problem {row['problem']}")
    for item in report["facets"]["runtime"]["problems"]:
        lines.append(f"- problem: {item}")
    lines += ["", "## Evidence references", "", f"evidence_references_resolved: {yn(report['evidence_references_resolved'])}"]
    for row in report["facets"]["evidence"]["references"]:
        lines.append(
            f"- {row['id']}: resolved {yn(row['resolved'])}; members {len(row.get('members', []))}"
        )
        for item in row["problems"]:
            lines.append(f"  - {item}")
    lines += ["", "## Minimum evidence", "", f"minimum_evidence_satisfied: {yn(report['minimum_evidence_satisfied'])}"]
    lines.append("semantic_sufficiency: not-established")
    for row in report["facets"]["minimum"]["categories"]:
        lines.append(
            f"- {row['category']}: {row['applicability']}; satisfied {yn(row['satisfied'])}; members {len(row.get('members', []))}"
        )
    lines += ["", "## Smoke", "", f"smoke_result: {report['smoke_result']}"]
    lines.append(f"final_stage: {report['facets']['smoke'].get('final_stage')}")
    lines.append(f"child_exit: {report['facets']['smoke'].get('child_exit')}")
    lines.append(f"wrapper_exit: {report['facets']['smoke'].get('wrapper_exit')}")
    lines.append(f"exit_layers_differ: {yn(report['exit_layers_differ'])}")
    lines.append("command_executed: false")
    for item in report["facets"]["smoke"]["problems"]:
        lines.append(f"- problem: {item}")
    lines += [
        "",
        "## Ready for declared method",
        "",
        f"ready_for_declared_method: {yn(report['ready_for_declared_method'])}",
        "surface_authorization: not-established",
        f"independent_proof: {report['independent_proof']}",
        f"shared_component: {yn(report['shared_component'])}",
    ]
    for item in report["facets"]["ready"]["problems"]:
        lines.append(f"- problem: {item}")
    lines += ["", "## Limits", ""]
    for item in report["limits"]:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


def exclusive_write(path: Path, data: bytes) -> None:
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_BINARY"):
        flags |= os.O_BINARY
    fd = os.open(str(path), flags)
    try:
        view = memoryview(data)
        while view:
            written = os.write(fd, view)
            if written <= 0:
                raise OSError("short write")
            view = view[written:]
    finally:
        os.close(fd)


def emit(output: Path, report: dict) -> None:
    if set(report) != REPORT_KEYS:
        raise Refuse("report keys drifted from the contract")
    exclusive_write(output / "readiness.json", canonical(report))
    exclusive_write(output / "READINESS.md", render(report).encode("utf-8"))


def preflight(request: dict) -> None:
    root = Path(os.path.abspath(request["delivery_root"]))
    for row in request["transport"]:
        contained(root, row["path"])
    for row in request["references"]:
        if row["format"] in KNOWN_FORMATS:
            contained(root, row["path"])


def check(request_path: str) -> int:
    try:
        request = load_request(request_path)
        validate(request)
        preflight(request)
    except Refuse as exc:
        sys.stderr.write(str(exc).rstrip() + "\n")
        return 2
    output = Path(os.path.abspath(request["output"]))
    try:
        os.mkdir(output)
    except FileExistsError:
        sys.stderr.write("output exists\n")
        return 2
    try:
        report = evaluate(request)
    except Refuse as exc:
        report = blank_report(request["purpose"]["mode"])
        report["problems"].append(str(exc))
        report["limits"] = ["the check stopped on an unsafe path and kept this partial report"]
        try:
            emit(output, report)
        except OSError:
            sys.stderr.write(str(exc).rstrip() + "\n")
            return 2
        sys.stdout.write(
            f"colab-readiness assembly=partial ready=false transport=false runtime=false evidence=false minimum=false smoke=not-run\n"
        )
        sys.stderr.write(str(exc).rstrip() + "\n")
        return 2
    try:
        emit(output, report)
    except OSError as exc:
        sys.stderr.write(f"write failed: {exc}\n")
        return 2
    code = 0 if report["assembly"] == "complete" else 2
    sys.stdout.write(
        "colab-readiness assembly={assembly} ready={ready} transport={transport} runtime={runtime} evidence={evidence} minimum={minimum} smoke={smoke}\n".format(
            assembly=report["assembly"],
            ready=str(report["ready_for_declared_method"]).lower(),
            transport=str(report["transport_valid"]).lower(),
            runtime=report["runtime_dependencies_resolved"] if isinstance(report["runtime_dependencies_resolved"], str) else str(report["runtime_dependencies_resolved"]).lower(),
            evidence=report["evidence_references_resolved"] if isinstance(report["evidence_references_resolved"], str) else str(report["evidence_references_resolved"]).lower(),
            minimum=str(report["minimum_evidence_satisfied"]).lower(),
            smoke=report["smoke_result"],
        )
    )
    return code


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="colab_readiness.py")
    sub = parser.add_subparsers(dest="command", required=True)
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--request", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return 2 if code in (None, 0) else int(code)
    if args.command != "check":
        sys.stderr.write("unknown command\n")
        return 2
    return check(args.request)


if __name__ == "__main__":
    sys.exit(main())
