#!/usr/bin/env python3
"""Prepare, verify and take in N7NN-bound Colab investigation packages.

Standard library only. Preview writes nothing. Prepare writes one fresh external
output only after the recomputed digest matches. Verify only reads (it copies the
assembler's own file set into a temporary directory to run the pinned verify).
Intake delegates custody to the pinned return_capture helper and inspector.
Nothing here releases, reviews, accepts, seats or publishes work.

  python -B colab_support.py preview --request ABS --config ABS --json
  python -B colab_support.py prepare --request ABS --config ABS --output ABS --digest HEX --json
  python -B colab_support.py verify  --output ABS --config ABS --json
  python -B colab_support.py intake  --output ABS --config ABS --book ABS --member 01NN.slug \
      --return-file ABS --source-root ABS --artifact REL|LOGICAL [...] --json

The contract is 00.kernel/00.00.10.work/0510.colab-tools/evidence/n7nn05.02/CONTRACT.md.
"""

import argparse
import datetime
import hashlib
import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True

REQUEST_SCHEMA = "colab-request/1"
BINDING_SCHEMA = "colab-binding/1"
CONFIG_SCHEMA = "colab-config/1"
REPORT_SCHEMA = "colab-support-report/1"
VERIFICATION_SCHEMA = "colab-package-verification/1"
PROVENANCE_SCHEMA = "colab-intake-provenance/1"
DIGEST_DOMAIN = "colab-package-digest/1"
ASSEMBLY_REQUEST = "pack-assembly-request/1"
ASSEMBLY_TEMPLATE = "pack-assembly-draft/1"

# Accepted tools, by exact bytes. A mismatch never loads or launches.
PINS = {
    "assembler": ("75d49679cbf3e624a82573229ca8c7cd9b758799bc26b6f080111feb6eaa275c", 43928),
    "checker": ("9bbd9d57f3b7da43234ac2e6ae4ce40a0ab6af2f53c8135ecfb2ee0c8a6e322d", 21563),
    "helper": ("8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac", 45767),
    "inspector": ("947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b", 11402),
}

MAX_REQUEST_BYTES = 262144
MAX_TEXT = 16384
MAX_LINE = 512
MAX_TARGETS = 32
MAX_ITEMS = 64
MODES = ("open-design", "hostile-read", "diagnostic", "controlled-experiment")
ENV_KINDS = ("zip-only", "local-tools")
REPLY_STATUS = ("actual", "hypothetical-fixture")
UNAVAILABLE_KINDS = ("required-omission", "tool-limitation")
PAGE_RE = re.compile(r"^[0-9]{4}\.[a-z][a-z0-9-]*$")
PASS_RE = re.compile(r"^05\.[0-9]{2}$")
TARGET_ID_RE = re.compile(r"^T[0-9]{2}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
MEMBER_RE = re.compile(r"^01[0-9]{2}\.[a-z0-9][a-z0-9-]*$")
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+\S")
LOCAL_PATH_RE = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]|\\\\[A-Za-z0-9]|(?:^|[\s(\"'`])/[A-Za-z0-9_.~-]+/")
RETURN_HEADINGS = ("Hostile", "Factfind", "Overflow", "Unprompted", "Director replies")
ZIP_TIME = (1980, 1, 1, 0, 0, 0)
HOOKS = ("before-assembler", "after-assembler", "before-zip", "before-verification")

NOT_CHECKED = [
    "meaning: this tool does not say what any source or return means",
    "adequacy: it does not judge whether the question, method or cases are sufficient",
    "authenticity: labels and quoted replies are supplied text; they authenticate nobody",
    "permission: it releases, reviews, accepts, seats and publishes nothing",
    "design-findings: verify reports pack, input and tool defects only",
]
STATEMENTS = [
    "This package is a draft. Preparation is not a Director release.",
    "A verified package or receipt is custody, not review or acceptance.",
    "The investigation binding is supplied by Prime; it does not open a live investigation.",
    "Labels and quoted Director text do not authenticate anyone.",
]


class ColabError(Exception):
    def __init__(self, code, detail, kind="input-defect"):
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.kind = kind


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


# ---------------------------------------------------------------- strict input

def _pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ColabError("duplicate-key", f"duplicate key: {key}")
        obj[key] = value
    return obj


def _constant(name):
    raise ColabError("nonfinite", f"non-finite number: {name}")


def strict_json(raw, label):
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ColabError("bom", f"{label} has a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeError as exc:
        raise ColabError("encoding", f"{label} is not UTF-8") from exc
    start = len(text) - len(text.lstrip())
    try:
        value, end = json.JSONDecoder(object_pairs_hook=_pairs, parse_constant=_constant).raw_decode(text, start)
    except ColabError:
        raise
    except json.JSONDecodeError as exc:
        raise ColabError("json", f"{label} is not strict json: {exc.msg}") from exc
    if text[end:].strip():
        raise ColabError("json", f"{label} has trailing data")
    if not isinstance(value, dict):
        raise ColabError("json", f"{label} is not an object")
    return value


def exact_keys(value, keys, label):
    if not isinstance(value, dict):
        raise ColabError("type", f"{label} is not an object")
    extra = sorted(set(value) - set(keys))
    missing = sorted(set(keys) - set(value))
    if extra:
        raise ColabError("unknown-key", f"{label} has unknown key: {', '.join(extra)}")
    if missing:
        raise ColabError("missing-key", f"{label} is missing key: {', '.join(missing)}")
    return value


def scan_headings(value, label):
    fenced = False
    for line in value.split("\n"):
        probe = line.lstrip(" ")
        if probe.startswith("```") or probe.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced or probe.startswith(">"):
            continue
        if HEADING_RE.match(probe):
            raise ColabError("heading", f"{label} contains a structural heading")


def one_line(value, label, allow_hash=True):
    if not isinstance(value, str) or value == "":
        raise ColabError("type", f"{label} is empty or not a string")
    if len(value) > MAX_LINE:
        raise ColabError("limit", f"{label} is longer than {MAX_LINE} characters")
    if value != value.strip() or any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise ColabError("line", f"{label} is not a single clean line")
    if not allow_hash and "#" in value:
        raise ColabError("line", f"{label} contains '#', which the pinned assembler refuses")
    scan_headings(value, label)
    return value


def text_block(value, label):
    if not isinstance(value, str) or value.strip() == "":
        raise ColabError("type", f"{label} is empty or not a string")
    if len(value) > MAX_TEXT:
        raise ColabError("limit", f"{label} is longer than {MAX_TEXT} characters")
    if any((ord(ch) < 32 and ch not in "\n\t") or ord(ch) == 127 for ch in value):
        raise ColabError("control", f"{label} contains a control character")
    scan_headings(value, label)
    return value


def bounded_list(value, label, low, high):
    if not isinstance(value, list):
        raise ColabError("type", f"{label} is not a list")
    if len(value) < low or len(value) > high:
        raise ColabError("limit", f"{label} needs {low} to {high} items")
    return value


def is_int(value):
    return isinstance(value, int) and not isinstance(value, bool)


def declared_path(value, label):
    """The custody checker's canonical relative path rule, restated without loading it."""
    if not isinstance(value, str) or value == "":
        raise ColabError("path", f"{label} is empty")
    if unicodedata.normalize("NFC", value) != value:
        raise ColabError("path", f"{label} is not Unicode NFC")
    if any(ch in value for ch in "\\\0\n\r\t") or value.startswith("/") or re.match(r"^[A-Za-z]:", value):
        raise ColabError("path", f"{label} is not a canonical relative path")
    for part in value.split("/"):
        if part in ("", ".", "..") or part.endswith(" ") or part.endswith(".") or ":" in part:
            raise ColabError("path", f"{label} is not a canonical relative path")
    return value


# ---------------------------------------------------------------- binding

def validate_binding(binding):
    exact_keys(binding, ("schema", "investigation", "targets"), "binding")
    if binding["schema"] != BINDING_SCHEMA:
        raise ColabError("schema", "binding schema is not colab-binding/1")
    inv = exact_keys(binding["investigation"], ("book", "page", "pass"), "investigation")
    for key in ("book", "page", "pass"):
        if not isinstance(inv[key], str) or inv[key] == "":
            raise ColabError("type", f"investigation {key} is not a string")
    if "/" in inv["book"]:
        raise ColabError("path", "investigation book is not one path segment")
    if not PAGE_RE.fullmatch(inv["page"]):
        raise ColabError("page", "investigation page is not NNNN.name")
    number = int(inv["page"][:4])
    if not 701 <= number <= 799:
        raise ColabError(
            "origin-band",
            f"investigation origin {inv['page']} is not an N7NN investigation member (0701-0799)",
        )
    if not PASS_RE.fullmatch(inv["pass"]):
        raise ColabError("pass", "investigation pass is not 05.NN")
    if inv["pass"] == "05.00":
        raise ColabError("pass", "pass 05.00 is refused by the pinned assembler", "tool-limitation")
    targets = bounded_list(binding["targets"], "targets", 1, MAX_TARGETS)
    seen_ids = set()
    seen_bodies = set()
    for target in targets:
        exact_keys(target, ("id", "book", "page", "file", "section", "source"), "target")
        tid = target["id"]
        if not isinstance(tid, str) or not TARGET_ID_RE.fullmatch(tid):
            raise ColabError("target-id", "target id is not TNN")
        if tid in seen_ids:
            raise ColabError("duplicate-target", f"duplicate target id {tid}")
        seen_ids.add(tid)
        for key in ("book", "page", "file"):
            if not isinstance(target[key], str) or target[key] == "":
                raise ColabError("type", f"{tid} {key} is not a string")
        if "/" in target["book"]:
            raise ColabError("path", f"{tid} book is not one path segment")
        if not PAGE_RE.fullmatch(target["page"]):
            raise ColabError("page", f"{tid} page is not NNNN.name")
        declared_path(target["file"], f"{tid} file")
        section = target["section"]
        if section is not None:
            exact_keys(section, ("kind", "value", "occurrence"), f"{tid} section")
            if section["kind"] not in ("id", "heading"):
                raise ColabError("section", f"{tid} section kind is not id or heading")
            if not isinstance(section["value"], str) or section["value"] == "":
                raise ColabError("section", f"{tid} section value is empty")
            occ = section["occurrence"]
            if occ is not None and (not is_int(occ) or occ < 1):
                raise ColabError("section", f"{tid} occurrence is not null or an integer of at least 1")
            if section["kind"] == "id":
                raise ColabError(
                    "unsupported-section-id",
                    f"{tid} section kind id: interface v1 declares no section-id syntax",
                    "tool-limitation",
                )
            if "\n" in section["value"] or "\r" in section["value"] or not HEADING_RE.match(section["value"]):
                raise ColabError("section", f"{tid} heading value is not one Markdown heading line")
        source = exact_keys(target["source"], ("repository", "commit", "path", "sha256"), f"{tid} source")
        if not isinstance(source["repository"], str) or source["repository"] == "":
            raise ColabError("type", f"{tid} source repository is empty")
        if not isinstance(source["commit"], str) or not COMMIT_RE.fullmatch(source["commit"]):
            raise ColabError("commit", f"{tid} source commit is not 40 lowercase hex")
        if not isinstance(source["sha256"], str) or not SHA_RE.fullmatch(source["sha256"]):
            raise ColabError("sha256", f"{tid} source sha256 is not 64 lowercase hex")
        declared_path(source["path"], f"{tid} source path")
        tail = [target["book"], target["page"]] + target["file"].split("/")
        parts = source["path"].split("/")
        if parts[-len(tail):] != tail or len(parts) < len(tail):
            raise ColabError("path-mismatch", f"{tid} source path does not end in book/page/file")
        if target["book"] == inv["book"] and target["page"] == inv["page"]:
            raise ColabError("target-is-origin", f"{tid} names the investigation page itself; targets are subjects")
        body = json.dumps({k: target[k] for k in target if k != "id"}, sort_keys=True)
        if body in seen_bodies:
            raise ColabError("duplicate-target", f"{tid} duplicates another target exactly")
        seen_bodies.add(body)
    repos = {t["source"]["repository"] for t in targets}
    commits = {t["source"]["commit"] for t in targets}
    if len(repos) != 1 or len(commits) != 1:
        raise ColabError(
            "multi-commit",
            "targets span more than one repository or commit; the pinned assembler reads one revision",
            "tool-limitation",
        )
    return binding


# ---------------------------------------------------------------- request

def validate_request(doc):
    keys = (
        "schema", "binding", "title", "date", "author", "recipient", "reviewer", "mode", "scoring",
        "context", "question", "why", "built_state", "known_gaps", "method", "cases", "environment",
        "permissions", "stop", "prior_involvement", "required_sources", "withheld", "unavailable",
        "director_replies", "return_route",
    )
    exact_keys(doc, keys, "request")
    if doc["schema"] != REQUEST_SCHEMA:
        raise ColabError("schema", "request schema is not colab-request/1")
    validate_binding(doc["binding"])
    for key in ("title", "author", "recipient", "reviewer"):
        one_line(doc[key], key, allow_hash=False)
    date = doc["date"]
    if not isinstance(date, str) or not DATE_RE.fullmatch(date):
        raise ColabError("date", "date is not YYYY-MM-DD")
    try:
        datetime.date.fromisoformat(date)
    except ValueError as exc:
        raise ColabError("date", "date is not a calendar day") from exc
    if doc["mode"] not in MODES:
        raise ColabError("mode", "mode is not one of " + ", ".join(MODES))
    scoring = doc["scoring"]
    if not isinstance(scoring, dict) or "state" not in scoring:
        raise ColabError("scoring", "scoring is not explicit")
    if scoring["state"] == "unscored":
        exact_keys(scoring, ("state",), "scoring")
    elif scoring["state"] == "scored":
        if not isinstance(scoring.get("blind"), bool):
            raise ColabError("scoring", "scoring blind is not a boolean")
        if scoring["blind"]:
            # The request travels in the package, so a blind rubric lives only in evaluator sources.
            exact_keys(scoring, ("state", "blind", "evaluator_sources"), "blind scoring")
            ev = bounded_list(scoring["evaluator_sources"], "evaluator sources", 1, MAX_ITEMS)
            for path in ev:
                declared_path(path, "evaluator source")
            if len(set(ev)) != len(ev):
                raise ColabError("duplicate-source", "evaluator sources repeat a path")
        else:
            exact_keys(scoring, ("state", "blind", "rubric", "meaning"), "open scoring")
            text_block(scoring["rubric"], "scoring rubric")
            text_block(scoring["meaning"], "scoring meaning")
    else:
        raise ColabError("scoring", "scoring state is not unscored or scored")
    for key in ("context", "question", "why", "built_state", "method", "prior_involvement"):
        text_block(doc[key], key)
    for item in bounded_list(doc["known_gaps"], "known_gaps", 0, MAX_ITEMS):
        text_block(item, "known gap")
    cases = bounded_list(doc["cases"], "cases", 1, MAX_ITEMS)
    for index, case in enumerate(cases, start=1):
        exact_keys(case, ("id", "text"), "case")
        if case["id"] != f"C{index:02d}":
            raise ColabError("case-id", "case ids are not C01..CNN in order")
        text_block(case["text"], f"case {case['id']}")
    env = exact_keys(doc["environment"], ("kind", "read", "write", "execute", "network"), "environment")
    if env["kind"] not in ENV_KINDS:
        raise ColabError("environment", "environment kind is not zip-only or local-tools")
    for key in ("read", "write", "execute", "network"):
        one_line(env[key], f"environment {key}", allow_hash=(key != "write"))
    for key in ("permissions", "stop"):
        for item in bounded_list(doc[key], key, 1, MAX_ITEMS):
            one_line(item, key)
    target_paths = {t["source"]["path"] for t in doc["binding"]["targets"]}
    req_paths = []
    for item in bounded_list(doc["required_sources"], "required_sources", 0, MAX_ITEMS):
        exact_keys(item, ("path", "role"), "required source")
        declared_path(item["path"], "required source path")
        one_line(item["role"], "required source role")
        if item["path"] in target_paths:
            raise ColabError("duplicate-source", f"required source {item['path']} is already a target")
        req_paths.append(item["path"])
    folded = [p.casefold() for p in req_paths + sorted(target_paths)]
    if len(set(folded)) != len(folded):
        raise ColabError("duplicate-source", "required sources repeat a path or a case alias")
    for item in bounded_list(doc["withheld"], "withheld", 0, MAX_ITEMS):
        exact_keys(item, ("item", "reason"), "withheld")
        one_line(item["item"], "withheld item")
        one_line(item["reason"], "withheld reason")
    for item in bounded_list(doc["unavailable"], "unavailable", 0, MAX_ITEMS):
        exact_keys(item, ("item", "reason", "kind"), "unavailable")
        one_line(item["item"], "unavailable item")
        one_line(item["reason"], "unavailable reason")
        if item["kind"] not in UNAVAILABLE_KINDS:
            raise ColabError("unavailable", "unavailable kind is not required-omission or tool-limitation")
    for index, reply in enumerate(bounded_list(doc["director_replies"], "director_replies", 0, MAX_ITEMS), start=1):
        exact_keys(reply, ("id", "date", "source", "reply", "status"), "director reply")
        if reply["id"] != f"D{index:02d}":
            raise ColabError("reply-id", "director reply ids are not D01..DNN in order")
        one_line(reply["date"], "reply date")
        one_line(reply["source"], "reply source")
        if not isinstance(reply["reply"], str) or reply["reply"] == "" or "\0" in reply["reply"]:
            raise ColabError("reply", "director reply text is empty or has NUL")
        if len(reply["reply"]) > MAX_TEXT:
            raise ColabError("limit", "director reply is too long")
        if reply["status"] not in REPLY_STATUS:
            raise ColabError("reply", "director reply status is not actual or hypothetical-fixture")
    route = exact_keys(doc["return_route"], ("destination", "submission_hint"), "return_route")
    one_line(route["destination"], "return destination", allow_hash=False)
    one_line(route["submission_hint"], "submission hint")
    if scoring["state"] == "scored" and scoring["blind"]:
        ev = set(scoring["evaluator_sources"])
        if ev & (set(req_paths) | target_paths):
            raise ColabError("evaluator-overlap", "an evaluator source is also a candidate input")
    if env["kind"] == "zip-only":
        for label, value in recipient_texts(doc):
            if LOCAL_PATH_RE.search(value):
                raise ColabError(
                    "local-path",
                    f"{label} names a local path; a ZIP-only recipient needs included readable inputs",
                )
    return doc


def recipient_texts(doc):
    """Recipient-facing text. Director replies are quoted data and are not scanned."""
    yield "context", doc["context"]
    yield "question", doc["question"]
    yield "why", doc["why"]
    yield "built_state", doc["built_state"]
    yield "method", doc["method"]
    yield "prior_involvement", doc["prior_involvement"]
    for item in doc["known_gaps"]:
        yield "known gap", item
    for case in doc["cases"]:
        yield f"case {case['id']}", case["text"]
    for key in ("read", "write", "execute", "network"):
        yield f"environment {key}", doc["environment"][key]
    for key in ("permissions", "stop"):
        for item in doc[key]:
            yield key, item
    yield "return destination", doc["return_route"]["destination"]
    yield "submission hint", doc["return_route"]["submission_hint"]


# ---------------------------------------------------------------- config and pins

def require_absolute(value, label):
    if not isinstance(value, str) or not value or not os.path.isabs(value):
        raise ColabError("path", f"{label} must be an absolute path")
    return value


def read_file(path, label):
    require_absolute(path, label)
    probe = Path(path)
    try:
        if probe.is_symlink() or (hasattr(probe, "is_junction") and probe.is_junction()):
            raise ColabError("linked", f"{label} is linked and was not followed")
        if not probe.is_file():
            raise ColabError("missing", f"{label} is not a file")
        return probe.read_bytes()
    except OSError as exc:
        raise ColabError("unreadable", f"{label} could not be read: {exc.strerror or exc}") from exc


def load_config(path):
    raw = read_file(path, "config")
    cfg = strict_json(raw, "config")
    exact_keys(cfg, ("schema", "repositories", "python", "assembler", "checker", "helper", "inspector"), "config")
    if cfg["schema"] != CONFIG_SCHEMA:
        raise ColabError("schema", "config schema is not colab-config/1")
    repos = cfg["repositories"]
    if not isinstance(repos, dict) or not repos:
        raise ColabError("config", "config repositories is empty")
    for label, root in repos.items():
        one_line(label, "repository label")
        require_absolute(root, f"repository {label}")
    for key in ("python", "assembler", "checker", "helper", "inspector"):
        require_absolute(cfg[key], key)
    return cfg


def pinned_bytes(cfg, name):
    raw = read_file(cfg[name], name)
    want, size = PINS[name]
    if sha256(raw) != want or len(raw) != size:
        raise ColabError("pin", f"{name} does not match its pin {want[:8]}…", "tool-limitation")
    return raw


class Tools:
    """The pinned assembler module and, through its own loader, the pinned checker."""

    def __init__(self, cfg):
        pinned_bytes(cfg, "assembler")
        pinned_bytes(cfg, "checker")
        spec = importlib.util.spec_from_file_location("pack_assembly_pinned", cfg["assembler"])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if sha256(Path(cfg["assembler"]).read_bytes()) != PINS["assembler"][0]:
            raise ColabError("pin", "assembler changed while it was loaded", "tool-limitation")
        self.asm = module
        try:
            self.checker, self.checker_sha, self.checker_bytes = module.load_checker(cfg["checker"])
        except module.AssemblyError as exc:
            raise ColabError("pin", exc.detail, "tool-limitation") from exc


def run_tool(cfg, name, args):
    pinned_bytes(cfg, name)
    argv = [cfg["python"], "-B", cfg[name]] + args
    try:
        proc = subprocess.run(argv, capture_output=True, shell=False)
    except OSError as exc:
        raise ColabError("launch", f"{name} could not start: {exc.strerror or exc}", "tool-limitation") from exc
    return {
        "tool": name,
        "args": args,
        "exit": proc.returncode,
        "stdout": proc.stdout.decode("utf-8", "replace"),
        "stderr": proc.stderr.decode("utf-8", "replace"),
    }


# ---------------------------------------------------------------- sections

def heading_lines(data):
    """Yield (index, text, level, start, end) for headings outside fences."""
    out = []
    lines = []
    offset = 0
    for raw in data.split(b"\n"):
        lines.append((raw, offset))
        offset += len(raw) + 1
    fenced = False
    for index, (raw, start) in enumerate(lines):
        try:
            text = raw.decode("utf-8")
        except UnicodeError as exc:
            raise ColabError("encoding", "a sectioned target is not UTF-8") from exc
        if text.endswith("\r"):
            text = text[:-1]
        probe = text.lstrip(" ")
        if probe.startswith("```") or probe.startswith("~~~"):
            fenced = not fenced
            continue
        if fenced:
            continue
        match = HEADING_RE.match(text)
        if match:
            out.append((index, text, len(match.group(1)), start))
    return out, lines


def resolve_section(target, data):
    section = target["section"]
    if section is None:
        return {"target": target["id"], "kind": "whole-file", "sha256": sha256(data), "bytes": len(data)}
    heads, lines = heading_lines(data)
    matches = [h for h in heads if h[1] == section["value"]]
    occ = section["occurrence"]
    if not matches:
        raise ColabError("section-missing", f"{target['id']} heading not found: {section['value']}")
    if occ is None and len(matches) > 1:
        raise ColabError(
            "section-ambiguous",
            f"{target['id']} heading occurs {len(matches)} times; an explicit occurrence is required",
        )
    pick = occ or 1
    if pick > len(matches):
        raise ColabError("section-missing", f"{target['id']} heading occurrence {pick} does not exist")
    index, _text, level, start = matches[pick - 1]
    end_line = len(lines)
    for other in heads:
        if other[0] > index and other[2] <= level:
            end_line = other[0]
            break
    end = lines[end_line][1] if end_line < len(lines) else len(data)
    body = data[start:end]
    return {
        "target": target["id"],
        "kind": "heading",
        "value": section["value"],
        "occurrence": occ,
        "matches": len(matches),
        "line_start": index + 1,
        "line_end": end_line,
        "sha256": sha256(body),
        "bytes": len(body),
    }


# ---------------------------------------------------------------- rendering

def assembler_request(doc):
    """Adapter: the colab request as the accepted assembler's request. Deterministic."""
    binding = doc["binding"]
    inv = binding["investigation"]
    first = binding["targets"][0]["source"]
    paths = []
    for target in binding["targets"]:
        if target["source"]["path"] not in paths:
            paths.append(target["source"]["path"])
    paths.extend(item["path"] for item in doc["required_sources"])
    instructions = [{"nn": "01", "heading": "Read the entry first", "text": (
        "ENTRY.md is the self-contained brief: role, question, targets, reading order, environment, "
        "permissions and stop points. 06 holds the supplied reasons. RETURN-TEMPLATE.md is the return shape."
    )}, {"nn": "02", "heading": "Method", "text": doc["method"]}]
    for case in doc["cases"]:
        instructions.append({"nn": f"{len(instructions) + 1:02d}", "heading": f"Case {case['id']}", "text": case["text"]})
    instructions.append({"nn": f"{len(instructions) + 1:02d}", "heading": "Return", "text": (
        "Return one file in the RETURN-TEMPLATE.md shape to the destination named in ENTRY.md. "
        "Keep Hostile, Factfind, Overflow and Unprompted even when empty."
    )})
    items = [{"name": f"withheld {w['item']}", "detail": w["reason"]} for w in doc["withheld"]]
    items += [{"name": f"{u['kind']} {u['item']}", "detail": u["reason"]} for u in doc["unavailable"]]
    if not items:
        items = [{"name": "sources", "detail": "every selected source is included as a snapshot"}]
    request = {
        "schema": ASSEMBLY_REQUEST,
        "template": ASSEMBLY_TEMPLATE,
        "title": doc["title"],
        "date": doc["date"],
        "author": doc["author"],
        "origin": {"book": inv["book"], "page": inv["page"], "batch": inv["pass"]},
        "identity": {"book": inv["book"], "pppp": inv["page"][:4], "keyword": inv["page"][5:], "batch": inv["pass"]},
        "executor": doc["recipient"],
        "reviewer": doc["reviewer"],
        "goal": "Question: " + doc["question"] + "\nWhy: " + doc["why"],
        "scope": ["Recipient writes: " + doc["environment"]["write"]],
        "revision": first["commit"],
        "paths": paths,
        "instructions": instructions,
        "evidence": "One return file in the RETURN-TEMPLATE.md shape. A receipt of it is custody, not acceptance.",
        "dependencies": {"state": "supplied", "items": items},
        "return_destination": {"state": "supplied", "path": doc["return_route"]["destination"]},
        "repository_label": first["repository"],
    }
    return (json.dumps(request, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def lines_of(value):
    parts = value.split("\n")
    if parts and parts[-1] == "":
        parts.pop()
    return parts


def render_entry(doc, sources, sections, batch_file, sixty_file):
    binding = doc["binding"]
    inv = binding["investigation"]
    commit = binding["targets"][0]["source"]["commit"]
    repo = binding["targets"][0]["source"]["repository"]
    snap = {s["path"]: s["snapshot"] for s in sources}
    out = [
        f"# ENTRY — {doc['title']}",
        "",
        f"Investigation: book {inv['book']}, page {inv['page']}, pass {inv['pass']}.",
        f"Prepared by {doc['author']} on {doc['date']} for {doc['recipient']}. Reviewer: {doc['reviewer']}.",
        f"Every source here is the exact Git blob at {repo} commit {commit}.",
        "This entry is a draft brief. It releases, seats and authorizes nothing.",
        "",
        "## Role and mode",
        f"You are a Colab. Mode: {doc['mode']}.",
        "You may challenge the method and propose a better one. Your findings are yours; they do not change any page by themselves.",
        "",
        "## Question",
    ]
    out += lines_of(doc["question"])
    out += ["", "## Why this matters"] + lines_of(doc["why"])
    out += ["", "## Context"] + lines_of(doc["context"])
    out += ["", "## Built state"] + lines_of(doc["built_state"])
    out += ["", "## Known gaps"]
    if doc["known_gaps"]:
        for index, gap in enumerate(doc["known_gaps"], start=1):
            gap_lines = lines_of(gap)
            out.append(f"G{index:02d}. {gap_lines[0]}")
            out += gap_lines[1:]
    else:
        out.append("None supplied.")
    out += ["", "## Targets (the subjects of this investigation)"]
    by_id = {s["target"]: s for s in sections}
    for target in binding["targets"]:
        res = by_id[target["id"]]
        where = f"{target['book']}/{target['page']}/{target['file']}"
        if res["kind"] == "whole-file":
            scope = "whole named file (not the whole page)"
        else:
            scope = (
                f"section `{res['value']}` occurrence {res['occurrence'] or 1} of {res['matches']}, "
                f"lines {res['line_start']}-{res['line_end']}"
            )
        out.append(
            f"- {target['id']}: {where}; {scope}; blob {target['source']['sha256']}; "
            f"read `{snap[target['source']['path']]}`."
        )
    out += ["", "## Reading order", "1. This ENTRY.md.", f"2. `{batch_file}` (the draft batch: method and cases as #NN).",
            f"3. `{sixty_file}` (supplied purpose and reasons; no findings).", "4. The target snapshots, in target order."]
    if doc["required_sources"]:
        out.append("5. Required sources:")
        for item in doc["required_sources"]:
            out.append(f"   - `{snap[item['path']]}` = {item['path']} — {item['role']}")
    out.append(f"Last: `RETURN-TEMPLATE.md`. `source-manifest.json` lists every snapshot with its sha256.")
    out += ["", "## Supplied, withheld and unavailable",
            "Supplied: every file in this package. Anything not here and not listed below was not supplied; do not invent it."]
    if doc["withheld"]:
        out.append("Withheld on purpose:")
        for item in doc["withheld"]:
            out.append(f"- {item['item']}: {item['reason']}")
    else:
        out.append("Withheld on purpose: none.")
    omissions = [u for u in doc["unavailable"] if u["kind"] == "required-omission"]
    limits = [u for u in doc["unavailable"] if u["kind"] == "tool-limitation"]
    out.append("Required but unavailable (a pack gap, not a design finding):" if omissions else "Required but unavailable: none.")
    for item in omissions:
        out.append(f"- {item['item']}: {item['reason']}")
    out.append("Tool limitations (not design findings):" if limits else "Tool limitations declared: none.")
    for item in limits:
        out.append(f"- {item['item']}: {item['reason']}")
    env = doc["environment"]
    out += ["", "## Environment and capabilities", f"Kind: {env['kind']}.", f"Read: {env['read']}", f"Write: {env['write']}",
            f"Execute: {env['execute']}", f"Network: {env['network']}"]
    if env["kind"] == "zip-only":
        out.append("You have only this package. Paths in it are labels; they give no access to any local drive.")
    out += ["", "## Method"] + lines_of(doc["method"])
    out += ["", "## Cases"]
    for case in doc["cases"]:
        case_lines = lines_of(case["text"])
        out.append(f"{case['id']}. {case_lines[0]}")
        out += case_lines[1:]
    out += ["", "## Scoring"]
    scoring = doc["scoring"]
    if scoring["state"] == "unscored":
        out.append("Unscored. State the qualitative result. Do not invent a number.")
    elif scoring["blind"]:
        out.append("A formal scored method is declared. Its evaluator material is withheld from you by design and is not in this package.")
    else:
        out.append("Scored, not blind. Rubric:")
        out += lines_of(scoring["rubric"])
        out.append("What a score means:")
        out += lines_of(scoring["meaning"])
    out += ["", "## Permissions"] + [f"- {p}" for p in doc["permissions"]]
    out += ["", "## Stop and escalate"] + [f"- {s}" for s in doc["stop"]]
    out += ["", "## Prior involvement and shared context"] + lines_of(doc["prior_involvement"])
    out += ["", "## Director replies (quoted data)"]
    if doc["director_replies"]:
        for reply in doc["director_replies"]:
            label = "actual Director reply" if reply["status"] == "actual" else "HYPOTHETICAL FIXTURE, not a Director decision"
            out.append(f"{reply['id']} ({label}; {reply['date']}; {reply['source']}):")
            out.append("```text")
            out += [f"reply: {line}" for line in reply["reply"].split("\n")]
            out.append("```")
    else:
        out.append("None supplied.")
    out += ["", "## Return", f"Destination: {doc['return_route']['destination']}",
            f"Submission: {doc['return_route']['submission_hint']}",
            "Use RETURN-TEMPLATE.md. A receipt of your return is custody, not acceptance.", ""]
    return ("\n".join(out)).encode("utf-8")


def render_sixty(doc):
    inv = doc["binding"]["investigation"]
    out = [
        f"# 06 — Supplied purpose and reasons — {doc['title']}",
        "version: 001",
        f"Authorization: draft — {doc['date']}",
        f"who: {doc['author']}",
        "state: draft; supplied reasons only, no findings",
        "Face: 06",
        f"PPPP: {inv['page'][:4]}",
        f"book: {inv['book']}",
        f"keyword: {inv['page'][5:]}",
        "",
        "## Supplied purpose",
    ]
    out += lines_of(doc["question"]) + [""] + lines_of(doc["why"])
    out += ["", "## Supplied context"] + lines_of(doc["context"])
    out += ["", "## Supplied known gaps"]
    out += [f"G{i:02d}. {g}" for i, g in enumerate(doc["known_gaps"], start=1)] or ["None supplied."]
    out += ["", "## Director replies"]
    if doc["director_replies"]:
        for reply in doc["director_replies"]:
            out.append(f"{reply['id']} [{reply['status']}] {reply['date']} {reply['source']}")
            out.append("```text")
            out += [f"reply: {line}" for line in reply["reply"].split("\n")]
            out.append("```")
    else:
        out.append("None supplied.")
    out += ["", "## Findings",
            "None. This face holds supplied reasons only. Findings arrive in the captured return and in Prime's later dispositions.", ""]
    return ("\n".join(out)).encode("utf-8")


def render_template(doc):
    inv = doc["binding"]["investigation"]
    out = [
        f"# Return — {inv['book']}/{inv['page']} pass {inv['pass']}",
        "Return one file. Keep every heading. An empty section may say what you looked for and that nothing was found.",
        "",
        "## Identity",
        "Model, publisher or interface, session id if known, date. Prior involvement and shared context.",
        "",
        "## Inputs actually read",
        "The snapshot files you opened. Anything you could not open.",
        "",
        "## Answer",
        "The answer to the question, with evidence and a reasoned assessment. An honest unknown is a result.",
        "",
        "## Cases",
    ]
    out += [f"{case['id']}: result and evidence." for case in doc["cases"]]
    out += [
        "",
        "## Actual operations",
        "What you actually read, ran or changed. Mark anything self-reported and not observable by the reader.",
        "",
        "## Hostile",
        "The failing path; the first misleading sentence or row; a missing relationship; where a protective rule blocks legitimate work.",
        "",
        "## Factfind",
        "Numbered holes F01.. tied to an exact page, face or source, each with a test or observation.",
        "",
        "## Pack and tool defects",
        "Missing inputs and tool limits. These are not design findings.",
        "",
        "## Overflow",
        "Relevant discoveries outside the ask, parked.",
        "",
        "## Unprompted",
        "What to add, cut, refuse or investigate that was not asked, and why.",
        "",
        "## Director replies",
        "Exact attributed `reply:` lines from any Director exchange, or `none`. Keep proposals and hypothetical examples separate from actual decisions.",
    ]
    if doc["scoring"]["state"] == "scored":
        out += ["", "## Scoring", "The declared method, raw evidence and what the score means."]
    out += ["", "## Limits", "What this return does not establish.", ""]
    return ("\n".join(out)).encode("utf-8")


def make_zip(files):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_STORED) as archive:
        for name in sorted(files):
            info = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            info.create_system = 0
            info.external_attr = 0
            info.compress_type = zipfile.ZIP_STORED
            archive.writestr(info, files[name])
    return buffer.getvalue()


def length_prefix(part):
    if isinstance(part, str):
        part = part.encode("utf-8")
    return len(part).to_bytes(8, "big") + part


# ---------------------------------------------------------------- planning

def plan(request_raw, tools, read_sources, read_evaluator):
    """Pure planning. read_sources(commit, paths) -> (commit, sources with data)."""
    if len(request_raw) > MAX_REQUEST_BYTES:
        raise ColabError("limit", f"request is larger than {MAX_REQUEST_BYTES} bytes")
    doc = validate_request(strict_json(request_raw, "request"))
    asm = tools.asm
    asm_raw = assembler_request(doc)
    try:
        asm_req = asm.validate_request(asm.parse_json(asm_raw), tools.checker)
    except asm.AssemblyError as exc:
        raise ColabError("assembler-request", f"pinned assembler refuses the adapted request: {exc.detail}",
                         "tool-limitation") from exc
    binding = doc["binding"]
    commit = binding["targets"][0]["source"]["commit"]
    resolved, sources = read_sources(commit, asm_req["paths"])
    if resolved != commit:
        raise ColabError("commit", "the bound commit did not resolve to itself")
    by_path = {s["path"]: s for s in sources}
    sections = []
    for target in binding["targets"]:
        src = by_path[target["source"]["path"]]
        if src["sha256"] != target["source"]["sha256"]:
            # Report the fact; never adopt it. Prime decides whether to rebind.
            raise ColabError("stale-source", f"{target['id']} blob at the commit is {src['sha256']}, "
                             f"not the bound {target['source']['sha256']}; nothing was retargeted")
        sections.append(resolve_section(target, src["data"]))
    identities, planned, asm_digest = asm.plan_outputs(asm_raw, asm_req, commit, sources)
    receipt = asm.receipt_bytes({
        "request": asm_req, "planned": planned, "digest": asm_digest, "request_raw": asm_raw,
        "commit": commit, "sources": identities,
        "checker_sha256": tools.checker_sha, "checker_bytes": tools.checker_bytes,
    }, {"result": "pass", "rows_checked": len(sources)}, 0)
    inv = binding["investigation"]
    nn = inv["pass"][3:]
    batch_file = f"{inv['pass']}.md"
    sixty_file = f"06.{nn}.md"
    colab_files = [
        ("binding.json", canonical(binding)),
        ("colab-request.json", request_raw),
        ("ENTRY.md", render_entry(doc, identities, sections, batch_file, sixty_file)),
        (sixty_file, render_sixty(doc)),
        ("RETURN-TEMPLATE.md", render_template(doc)),
    ]
    package = {item["path"]: item["data"] for item in planned}
    package["completion-receipt.json"] = receipt
    for name, data in colab_files:
        if name in package:
            raise ColabError("collision", f"colab file {name} collides with an assembler file", "tool-limitation")
        package[name] = data
    evaluator = []
    scoring = doc["scoring"]
    if scoring["state"] == "scored" and scoring["blind"]:
        ev_commit, ev_sources = read_evaluator(commit, scoring["evaluator_sources"])
        candidate = {s["sha256"] for s in sources}
        for src in ev_sources:
            if src["sha256"] in candidate:
                raise ColabError("evaluator-overlap", f"evaluator source {src['path']} has the same bytes as a candidate input")
        manifest = {"schema": "prime-pack-sources/1", "commit": ev_commit, "sources": [
            {"path": s["path"], "sha256": s["sha256"], "bytes": s["bytes"], "snapshot": s["snapshot"]} for s in ev_sources]}
        evaluator = [("evaluator/source-manifest.json", canonical(manifest))]
        evaluator += [("evaluator/" + s["snapshot"], s["data"]) for s in ev_sources]
    zip_bytes = make_zip(package)
    digest = hashlib.sha256()
    for part in (DIGEST_DOMAIN, request_raw, canonical(binding), asm_digest):
        digest.update(length_prefix(part))
    for name, data in colab_files + evaluator:
        for part in (name, sha256(data), str(len(data))):
            digest.update(length_prefix(part))
    for part in (sha256(zip_bytes), str(len(zip_bytes))):
        digest.update(length_prefix(part))
    return {
        "doc": doc,
        "asm_raw": asm_raw,
        "asm_digest": asm_digest,
        "commit": commit,
        "sources": identities,
        "sections": sections,
        "package": package,
        "colab_files": colab_files,
        "evaluator": evaluator,
        "zip": zip_bytes,
        "digest": digest.hexdigest(),
    }


def git_reader(tools, root):
    def read(commit, paths):
        try:
            resolved, sources = tools.asm.load_sources(tools.checker, root, commit, paths)
        except tools.asm.AssemblyError as exc:
            raise ColabError("source", exc.detail) from exc
        return resolved, sources
    return read


def repo_root(cfg, doc):
    label = doc["binding"]["targets"][0]["source"]["repository"]
    if label not in cfg["repositories"]:
        raise ColabError("repository", f"repository label {label} has no local root in config")
    return cfg["repositories"][label]


def plan_from_git(request_path, cfg, tools):
    raw = read_file(request_path, "request")
    doc = validate_request(strict_json(raw, "request")) if len(raw) <= MAX_REQUEST_BYTES else None
    if doc is None:
        raise ColabError("limit", f"request is larger than {MAX_REQUEST_BYTES} bytes")
    reader = git_reader(tools, repo_root(cfg, doc))
    return plan(raw, tools, reader, reader)


# ---------------------------------------------------------------- reports

def report(command, result, findings=(), planned=None, **extra):
    body = {
        "schema": REPORT_SCHEMA,
        "command": command,
        "result": result,
        "digest": None,
        "investigation": None,
        "commit": None,
        "targets": [],
        "planned": [],
        "findings": list(findings),
        "statements": STATEMENTS,
        "not_checked": NOT_CHECKED,
    }
    if planned is not None:
        body["digest"] = planned["digest"]
        body["investigation"] = planned["doc"]["binding"]["investigation"]
        body["commit"] = planned["commit"]
        body["targets"] = planned["sections"]
        files = [("package/" + name, data) for name, data in sorted(planned["package"].items())]
        files += [(name, data) for name, data in planned["evaluator"]]
        files.append(("prepared-colab.zip", planned["zip"]))
        body["planned"] = [{"path": n, "sha256": sha256(d), "bytes": len(d)} for n, d in files]
    body.update(extra)
    return body


def finding(exc):
    return {"kind": exc.kind, "code": exc.code, "detail": exc.detail}


def preview(request_path, config_path):
    try:
        cfg = load_config(config_path)
        planned = plan_from_git(request_path, cfg, Tools(cfg))
    except ColabError as exc:
        return report("preview", "invalid", [finding(exc)]), 2
    return report("preview", "preview", planned=planned), 0


# ---------------------------------------------------------------- prepare

def kind_of(path):
    probe = Path(path)
    try:
        if probe.is_symlink() or (hasattr(probe, "is_junction") and probe.is_junction()):
            return "linked"
        if not os.path.lexists(path):
            return "missing"
        if probe.is_dir():
            return "dir"
        if probe.is_file():
            return "file"
    except OSError:
        return "unreadable"
    return "other"


def inside(child, parent):
    c = os.path.normcase(os.path.abspath(child))
    p = os.path.normcase(os.path.abspath(parent))
    return c == p or c.startswith(p.rstrip(os.sep) + os.sep)


def check_output(output, cfg):
    require_absolute(output, "output")
    parent = Path(output).parent
    if kind_of(parent) != "dir":
        raise ColabError("output", "output parent is not a real directory")
    for label, root in cfg["repositories"].items():
        if inside(output, root):
            raise ColabError("output", f"output is inside repository {label}")
    current = Path(output).absolute()
    while True:
        if kind_of(current / "00.kernel") in ("dir", "linked"):
            raise ColabError("output", "output is inside a book workspace")
        if current.parent == current:
            break
        current = current.parent
    kind = kind_of(output)
    if kind == "missing":
        return "fresh"
    if kind != "dir":
        raise ColabError("collision", "output exists and is not a directory")
    if not any(Path(output).iterdir()):
        return "fresh"
    return "occupied"


def write_new(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0)
    try:
        fd = os.open(path, flags)
    except FileExistsError as exc:
        raise ColabError("collision", f"refusing to overwrite {path.name}", "pack-defect") from exc
    try:
        view = memoryview(data)
        while view:
            view = view[os.write(fd, view):]
    finally:
        os.close(fd)


def written_list(output):
    root = Path(output)
    if not root.exists():
        return []
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())


def verification_body(planned):
    package = planned["package"]
    return {
        "schema": VERIFICATION_SCHEMA,
        "result": "prepared",
        "digest": planned["digest"],
        "assembler_digest": planned["asm_digest"],
        "repository": planned["doc"]["binding"]["targets"][0]["source"]["repository"],
        "commit": planned["commit"],
        "investigation": planned["doc"]["binding"]["investigation"],
        "binding_sha256": sha256(canonical(planned["doc"]["binding"])),
        "request_sha256": sha256(package["colab-request.json"]),
        "package_files": [{"path": n, "sha256": sha256(d), "bytes": len(d)} for n, d in sorted(package.items())],
        "zip": {"path": "prepared-colab.zip", "sha256": sha256(planned["zip"]), "bytes": len(planned["zip"]),
                "members": sorted(package)},
        "evaluator_files": [{"path": n, "sha256": sha256(d), "bytes": len(d)} for n, d in planned["evaluator"]],
        "sections": planned["sections"],
        "pins": {name: pin[0] for name, pin in sorted(PINS.items())},
        "statements": STATEMENTS,
    }


def prepare(request_path, config_path, output, supplied, hooks=None):
    hooks = hooks or {}
    try:
        cfg = load_config(config_path)
        tools = Tools(cfg)
        planned = plan_from_git(request_path, cfg, tools)
    except ColabError as exc:
        return report("prepare", "invalid", [finding(exc)], supplied_digest=supplied), 2
    if supplied != planned["digest"]:
        return report("prepare", "invalid", [{"kind": "input-defect", "code": "digest-mismatch",
                      "detail": "supplied digest does not match the recomputed plan"}],
                      planned=planned, supplied_digest=supplied), 2
    try:
        state = check_output(output, cfg)
    except ColabError as exc:
        return report("prepare", "invalid", [finding(exc)], planned=planned, supplied_digest=supplied), 2
    if state == "occupied":
        body, code = verify(output, config_path)
        if code == 0 and body.get("digest") == planned["digest"]:
            return report("prepare", "already-prepared", planned=planned, supplied_digest=supplied,
                          output=output, written=[]), 0
        detail = "output holds a different package" if code == 0 else "output holds a partial or damaged package"
        return report("prepare", "collision", [{"kind": "pack-defect", "code": "collision", "detail": detail}],
                      planned=planned, supplied_digest=supplied, output=output,
                      retained=written_list(output)), 2
    root = Path(output)
    try:
        root.mkdir(exist_ok=True)
        write_new(root / "assembler-request.json", planned["asm_raw"])
        if "before-assembler" in hooks:
            hooks["before-assembler"](root)
        run = run_tool(cfg, "assembler", [
            "assemble", "--request", str(root / "assembler-request.json"), "--repo", repo_root(cfg, planned["doc"]),
            "--checker", cfg["checker"], "--output", str(root / "package"), "--digest", planned["asm_digest"], "--json",
        ])
        write_new(root / "assembler-run.json", canonical(run))
        if run["exit"] != 0:
            raise ColabError("assembler", f"pinned assembler exit {run['exit']}", "tool-limitation")
        receipt = (root / "package" / "completion-receipt.json").read_bytes()
        if receipt != planned["package"]["completion-receipt.json"]:
            raise ColabError("assembler", "assembler receipt differs from the plan", "pack-defect")
        if "after-assembler" in hooks:
            hooks["after-assembler"](root)
        for name, data in planned["colab_files"]:
            write_new(root / "package" / name, data)
        for name, data in planned["evaluator"]:
            write_new(root / name, data)
        if "before-zip" in hooks:
            hooks["before-zip"](root)
        for name, data in planned["package"].items():
            if (root / "package" / name).read_bytes() != data:
                raise ColabError("drift", f"package/{name} differs from the plan before zipping", "pack-defect")
        write_new(root / "prepared-colab.zip", planned["zip"])
        if "before-verification" in hooks:
            hooks["before-verification"](root)
        write_new(root / "verification.json", canonical(verification_body(planned)))
    except ColabError as exc:
        return report("prepare", "partial", [finding(exc)], planned=planned, supplied_digest=supplied,
                      output=output, retained=written_list(output)), 2
    except OSError as exc:
        return report("prepare", "partial", [{"kind": "tool-limitation", "code": "io", "detail": str(exc)}],
                      planned=planned, supplied_digest=supplied, output=output, retained=written_list(output)), 2
    return report("prepare", "prepared", planned=planned, supplied_digest=supplied, output=output,
                  written=written_list(output)), 0


# ---------------------------------------------------------------- verify

def read_tree(root):
    files = {}
    for path in sorted(Path(root).rglob("*")):
        rel = path.relative_to(root).as_posix()
        kind = kind_of(path)
        if kind == "linked":
            raise ColabError("linked", f"{rel} is linked", "pack-defect")
        if kind == "file":
            files[rel] = path.read_bytes()
        elif kind != "dir":
            raise ColabError("unexpected", f"{rel} is not a plain file or directory", "pack-defect")
    return files


def package_reader(files, prefix=""):
    def read(commit, paths):
        manifest = strict_json(files[prefix + "source-manifest.json"], "source manifest")
        rows = manifest.get("sources")
        if not isinstance(rows, list) or [r.get("path") for r in rows] != list(paths):
            raise ColabError("manifest", "packaged manifest paths differ from the request plan", "pack-defect")
        sources = []
        for row in rows:
            name = prefix + row["snapshot"]
            if name not in files:
                raise ColabError("missing", f"{name} is missing", "pack-defect")
            sources.append({"path": row["path"], "sha256": sha256(files[name]), "bytes": len(files[name]),
                            "snapshot": row["snapshot"], "data": files[name]})
        return manifest.get("commit"), sources
    return read


def verify(output, config_path):
    findings = []
    try:
        cfg = load_config(config_path)
        tools = Tools(cfg)
        require_absolute(output, "output")
        if kind_of(output) != "dir":
            raise ColabError("missing", "output is not a directory", "pack-defect")
        tree = read_tree(output)
    except ColabError as exc:
        return report("verify", "invalid", [finding(exc)]), 2
    if "verification.json" not in tree:
        return report("verify", "partial", [{"kind": "pack-defect", "code": "not-completed",
                      "detail": "verification.json is absent"}], present=sorted(tree)), 1
    try:
        recorded = strict_json(tree["verification.json"], "verification")
        exact_keys(recorded, tuple(verification_body_keys()), "verification")
        package = {n[len("package/"):]: d for n, d in tree.items() if n.startswith("package/")}
        if "colab-request.json" not in package:
            raise ColabError("missing", "package/colab-request.json is missing", "pack-defect")
        files = dict(package)
        evaluator_tree = {n: d for n, d in tree.items() if n.startswith("evaluator/")}

        def read_evaluator(commit, paths):
            manifest = strict_json(evaluator_tree.get("evaluator/source-manifest.json", b"{}"), "evaluator manifest")
            rows = manifest.get("sources") or []
            if [r.get("path") for r in rows] != list(paths):
                raise ColabError("manifest", "evaluator manifest differs from the request", "pack-defect")
            out = []
            for row in rows:
                data = evaluator_tree.get("evaluator/" + row["snapshot"])
                if data is None:
                    raise ColabError("missing", f"evaluator/{row['snapshot']} is missing", "pack-defect")
                out.append({"path": row["path"], "sha256": sha256(data), "bytes": len(data),
                            "snapshot": row["snapshot"], "data": data})
            return manifest.get("commit"), out

        planned = plan(package["colab-request.json"], tools, package_reader(files), read_evaluator)
    except ColabError as exc:
        return report("verify", "mismatch", [finding(exc)]), 1
    expected = {"package/" + n: d for n, d in planned["package"].items()}
    expected.update(dict(planned["evaluator"]))
    expected["prepared-colab.zip"] = planned["zip"]
    expected["verification.json"] = canonical(verification_body(planned))
    side = {"assembler-request.json", "assembler-run.json"}
    for name in sorted(set(expected) | set(tree)):
        if name in side:
            continue
        if name not in tree:
            findings.append({"kind": "pack-defect", "code": "missing", "detail": f"{name} is missing"})
        elif name not in expected:
            findings.append({"kind": "pack-defect", "code": "extra", "detail": f"{name} is not part of the package"})
        elif tree[name] != expected[name]:
            findings.append({"kind": "pack-defect", "code": "differs", "detail": f"{name} differs from the recomputed plan"})
    if tree.get("assembler-request.json") not in (None, planned["asm_raw"]):
        findings.append({"kind": "pack-defect", "code": "differs", "detail": "assembler-request.json differs"})
    try:
        with zipfile.ZipFile(io.BytesIO(tree.get("prepared-colab.zip", b""))) as archive:
            members = {info.filename: archive.read(info.filename) for info in archive.infolist()}
        if members != planned["package"]:
            findings.append({"kind": "pack-defect", "code": "zip", "detail": "ZIP members differ from package/"})
    except (zipfile.BadZipFile, KeyError, OSError) as exc:
        findings.append({"kind": "pack-defect", "code": "zip", "detail": f"ZIP is unreadable: {exc}"})
    asm_run = None
    with tempfile.TemporaryDirectory(prefix="colab-verify-") as tmp:
        projection = Path(tmp) / "pack"
        names = [n for n in planned["package"] if n in ("request.snapshot", "source-manifest.json",
                 "completion-receipt.json", planned["doc"]["binding"]["investigation"]["pass"] + ".md")
                 or n.startswith("snapshots/")]
        for name in names:
            dest = projection.joinpath(*name.split("/"))
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(package.get(name, b""))
        try:
            asm_run = run_tool(cfg, "assembler", ["verify", "--pack", str(projection), "--checker", cfg["checker"], "--json"])
        except ColabError as exc:
            findings.append(finding(exc))
        if asm_run is not None:
            asm_run["args"] = ["verify", "--pack", "<temporary projection>", "--checker", "<pinned checker>", "--json"]
            asm_run["stdout"] = asm_run["stdout"].replace(str(projection), "<temporary projection>")
            if asm_run["exit"] != 0:
                findings.append({"kind": "pack-defect", "code": "assembler-verify",
                                 "detail": f"pinned assembler verify exit {asm_run['exit']}"})
    if findings:
        return report("verify", "mismatch", findings, planned=planned, assembler_verify=asm_run), 1
    return report("verify", "intact", planned=planned, assembler_verify=asm_run), 0


def verification_body_keys():
    return ("schema", "result", "digest", "assembler_digest", "repository", "commit", "investigation",
            "binding_sha256", "request_sha256", "package_files", "zip", "evaluator_files", "sections",
            "pins", "statements")


# ---------------------------------------------------------------- intake

def parse_inspection(run):
    try:
        body = strict_json(run["stdout"].encode("utf-8"), "inspector output")
    except ColabError as exc:
        raise ColabError("inspector", f"inspector output is not one JSON object: {exc.detail}", "tool-limitation") from exc
    if body.get("schema") != "return-capture-inspection/1":
        raise ColabError("inspector", "inspector output schema is not return-capture-inspection/1", "tool-limitation")
    return body


def heading_presence(data):
    found = {}
    text = data.decode("utf-8", "replace")
    for name in RETURN_HEADINGS:
        pattern = re.compile(r"^#{1,6}[ \t]+" + re.escape(name) + r"\b", re.MULTILINE)
        found[name] = bool(pattern.search(text))
    return found


def intake(output, config_path, book, member, return_file, source_root, artifacts):
    runs = []

    def done(result, code, findings=(), **extra):
        body = {
            "schema": PROVENANCE_SCHEMA,
            "result": result,
            "member": member,
            "findings": list(findings),
            "runs": runs,
            "statements": STATEMENTS + ["Intake edits no work page. Prime appends any pointer after review."],
        }
        body.update(extra)
        return body, code

    try:
        cfg = load_config(config_path)
        for path, label in ((book, "book"), (return_file, "return file"), (source_root, "source root")):
            require_absolute(path, label)
        if not isinstance(member, str) or not MEMBER_RE.fullmatch(member):
            raise ColabError("member", "member is not 01NN.slug")
        if not artifacts:
            raise ColabError("artifact", "at least one --artifact is required")
        for name in ("helper", "inspector"):
            pinned_bytes(cfg, name)
    except ColabError as exc:
        return done("invalid", 2, [finding(exc)])
    package, code = verify(output, config_path)
    if code != 0:
        return done("package-not-verified", 2, package["findings"])
    binding = strict_json((Path(output) / "package" / "binding.json").read_bytes(), "binding")
    inv = binding["investigation"]
    base = {
        "package_digest": package["digest"],
        "binding_sha256": sha256(canonical(binding)),
        "investigation": inv,
        "targets": [{"id": t["id"], "path": t["source"]["path"], "commit": t["source"]["commit"],
                     "sha256": t["source"]["sha256"], "section": t["section"]} for t in binding["targets"]],
    }
    try:
        first = run_tool(cfg, "inspector", ["inspect", "--book", book, "--member", member, "--json"])
        runs.append(first)
        seen = parse_inspection(first)
    except ColabError as exc:
        return done("invalid", 2, [finding(exc)], **base)
    if seen.get("status") not in ("reserved", "complete"):
        return done("not-reserved", 2, [{"kind": "input-defect", "code": "member",
                    "detail": f"member status is {seen.get('status')}"}], **base)
    reservation = seen.get("reservation") or {}
    origin = reservation.get("origin")
    want = {"book": inv["book"], "page": inv["page"], "batch": inv["pass"]}
    if origin != want:
        return done("wrong-origin", 2, [{"kind": "input-defect", "code": "wrong-origin",
                    "detail": f"reservation origin {origin} is not the investigation {want}"}], **base)
    submission = reservation.get("submission_id")
    capture_args = ["capture", "--book", book, "--submission", str(submission), "--return-file", return_file,
                    "--source-root", source_root]
    for item in artifacts:
        capture_args += ["--artifact", item]
    try:
        cap = run_tool(cfg, "helper", capture_args)
        runs.append(cap)
        ver = run_tool(cfg, "helper", ["verify", "--book", book, "--member", member])
        runs.append(ver)
        after_run = run_tool(cfg, "inspector", ["inspect", "--book", book, "--member", member, "--json"])
        runs.append(after_run)
        after = parse_inspection(after_run)
    except ColabError as exc:
        return done("attention", 1, [finding(exc)], **base)
    capture = after.get("capture") or {}
    replay = "already-captured" in cap["stdout"]
    presence = None
    try:
        presence = heading_presence(read_file(return_file, "return file"))
    except ColabError:
        presence = None
    extra = dict(base, submission=submission, capture=capture, return_headings=presence,
                 helper_capture="already-captured" if replay else ("captured" if cap["exit"] == 0 else "refused"))
    if cap["exit"] != 0 or ver["exit"] != 0 or after.get("status") != "complete":
        return done("attention", 1, [{"kind": "pack-defect", "code": "custody",
                    "detail": f"capture exit {cap['exit']}, verify exit {ver['exit']}, status {after.get('status')}"}],
                    **extra)
    receipt = capture.get("receipt_sha256")
    extra["pointer"] = (
        f"Member {member}. Receipt sha256 {receipt}. Verify exit 0: result complete; not approved; "
        f"not accepted; not published. Package digest {package['digest']}."
    )
    return done("already-captured" if replay else "captured", 0, **extra)


# ---------------------------------------------------------------- CLI

def emit(body):
    sys.stdout.buffer.write((json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def build_parser():
    parser = argparse.ArgumentParser(description="N7NN Colab package support. Drafts and custody only.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("preview", "prepare", "verify", "intake"):
        item = sub.add_parser(name)
        item.add_argument("--config", required=True)
        item.add_argument("--json", action="store_true", required=True)
        if name in ("preview", "prepare"):
            item.add_argument("--request", required=True)
        if name in ("prepare", "verify", "intake"):
            item.add_argument("--output", required=True)
        if name == "prepare":
            item.add_argument("--digest", required=True)
        if name == "intake":
            item.add_argument("--book", required=True)
            item.add_argument("--member", required=True)
            item.add_argument("--return-file", required=True)
            item.add_argument("--source-root", required=True)
            item.add_argument("--artifact", action="append", default=[])
    return parser


def main(argv=None):
    opts = build_parser().parse_args(argv)
    try:
        if opts.command == "preview":
            body, code = preview(opts.request, opts.config)
        elif opts.command == "prepare":
            body, code = prepare(opts.request, opts.config, opts.output, opts.digest)
        elif opts.command == "verify":
            body, code = verify(opts.output, opts.config)
        else:
            body, code = intake(opts.output, opts.config, opts.book, opts.member, opts.return_file,
                                opts.source_root, opts.artifact)
    except ColabError as exc:
        body, code = report(opts.command, "invalid", [finding(exc)]), 2
    emit(body)
    return code


if __name__ == "__main__":
    sys.exit(main())
