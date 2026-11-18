"""Placement, canonical JSON, and input checks for desk-core/1.

N5NN maps to N1NN by the same NN and subject. N7NN stays on its page.
Any other band is refused. This module does not scan a book or allocate a slot.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass

PAGE_RE = re.compile(r"^0[0-9]{3}$")
SUBJECT_RE = re.compile(r"^[a-z0-9]+(?:[.-][a-z0-9]+)*$")
PASS_RE = re.compile(r"^(?:0[1-9]|[1-9][0-9])$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,40}$")

MARKER = "<!-- desk-core:"
LIMITS = (
    "no OS user isolation",
    "actor labels are not authentication",
    "file locks and rename are not a proof of race freedom",
    "a receipt is not a review and a review is not acceptance",
    "this tool does not launch a model or migrate the live book",
)


class Refused(Exception):
    def __init__(self, code: str, message: str, **extra: object) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.extra = extra


@dataclass(frozen=True)
class Placement:
    page: str
    subject: str
    pass_id: str
    kind: str
    source_name: str
    return_name: str | None

    @property
    def face_name(self) -> str:
        if self.kind == "N7NN":
            return f"05.{self.pass_id}.pack.md"
        return f"05.{self.pass_id}.md"

    @property
    def custody_name(self) -> str:
        if self.kind == "N7NN":
            return self.source_name
        if self.return_name is None:
            raise Refused("placement", "N5NN return line is missing")
        return self.return_name


def canonical(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _reject_constant(_name: str) -> object:
    raise Refused("json", "json contains a non-standard constant")


def loads(data: bytes, label: str) -> object:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise Refused("utf-8", f"{label} is not utf-8") from exc

    def pairs(seq: list[tuple[str, object]]) -> dict[str, object]:
        obj: dict[str, object] = {}
        for key, item in seq:
            if key in obj:
                raise Refused("duplicate-key", f"{label} repeats {key}")
            obj[key] = item
        return obj

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=_reject_constant)
    except Refused:
        raise
    except json.JSONDecodeError as exc:
        raise Refused("json", f"{label} is not json: {exc.msg}") from exc


def require_object(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise Refused("type", f"{label} must be an object")
    return value


def exact_keys(value: dict[str, object], keys: set[str], label: str) -> None:
    if set(value) != keys:
        missing = sorted(keys - set(value))
        extra = sorted(set(value) - keys)
        raise Refused("keys", f"{label} keys mismatch", missing=missing, extra=extra)


def one_line(value: object, label: str, limit: int) -> str:
    if type(value) is not str or value == "" or len(value) > limit:
        raise Refused("text", f"{label} must be one non-empty line")
    if "\n" in value or "\r" in value or "\x00" in value:
        raise Refused("text", f"{label} must be one line")
    return value


def prose(value: object, label: str, limit: int, empty_ok: bool = False) -> str:
    if type(value) is not str or len(value) > limit:
        raise Refused("text", f"{label} length is refused")
    if value == "" and not empty_ok:
        raise Refused("text", f"{label} is empty")
    if "\r" in value or "\x00" in value or MARKER in value:
        raise Refused("text", f"{label} contains a forbidden character")
    return value


def string_list(value: object, label: str, empty_ok: bool, limit: int = 32) -> list[str]:
    if type(value) is not list or len(value) > limit:
        raise Refused("list", f"{label} must be a short list")
    if value == [] and not empty_ok:
        raise Refused("list", f"{label} is empty")
    out: list[str] = []
    for item in value:
        out.append(one_line(item, label, 400))
    return out


def place(page: object, subject: object, pass_id: object) -> Placement:
    page_s = one_line(page, "page", 4)
    subject_s = one_line(subject, "subject", 80)
    pass_s = one_line(pass_id, "pass", 2)
    if not PAGE_RE.fullmatch(page_s):
        raise Refused(
            "undeclared-source-shape",
            "page must be four digits beginning with 0; other shapes are not routed",
        )
    if not SUBJECT_RE.fullmatch(subject_s):
        raise Refused("subject", "subject characters are refused")
    if not PASS_RE.fullmatch(pass_s):
        raise Refused("pass", "pass must be 01 through 99")
    band = page_s[1]
    source_name = f"{page_s}.{subject_s}"
    if band == "5":
        return_name = f"01{page_s[2:]}.{subject_s}"
        return Placement(page_s, subject_s, pass_s, "N5NN", source_name, return_name)
    if band == "7":
        return Placement(page_s, subject_s, pass_s, "N7NN", source_name, None)
    raise Refused(
        "undeclared-source-kind",
        f"band {band} is not N5NN or N7NN; no return line was allocated",
        band=band,
    )


def evidence_rows(value: object) -> list[dict[str, object]]:
    if type(value) is not list or len(value) > 32:
        raise Refused("evidence", "bound_evidence must be a short list")
    rows: list[dict[str, object]] = []
    names: set[str] = set()
    for item in value:
        obj = require_object(item, "evidence")
        exact_keys(obj, {"name", "sha256", "bytes"}, "evidence")
        name = one_line(obj["name"], "evidence name", 80)
        if not SUBJECT_RE.fullmatch(name):
            raise Refused("evidence", "evidence name is refused")
        if name in names:
            raise Refused("evidence", "evidence name repeats")
        names.add(name)
        digest = one_line(obj["sha256"], "evidence sha256", 64)
        if not HEX64_RE.fullmatch(digest):
            raise Refused("evidence", "evidence sha256 is refused")
        size = obj["bytes"]
        if type(size) is not int or isinstance(size, bool) or size < 0 or size > 50_000_000:
            raise Refused("evidence", "evidence bytes are refused")
        rows.append({"name": name, "sha256": digest, "bytes": size})
    rows.sort(key=lambda row: str(row["name"]))
    return rows


def task_binding(fields: dict[str, object]) -> str:
    body = {
        "schema": "desk-core-task-binding/1",
        "title": fields["title"],
        "body": fields["body"],
        "expected_outputs": fields["expected_outputs"],
        "scope": fields["scope"],
        "agreement": fields["agreement"],
        "bound_evidence": fields["bound_evidence"],
    }
    return sha256(canonical(body))


def agreement_sha(agreement: str) -> str:
    return sha256(agreement.encode("utf-8"))


def evidence_sha(rows: list[dict[str, object]]) -> str:
    return sha256(canonical(rows))


def review_binding(task_sha: str, receipt_sha: str, agree_sha: str, evid_sha: str, identity: str) -> str:
    body = {
        "schema": "desk-core-review-binding/1",
        "task_binding_sha256": task_sha,
        "receipt_sha256": receipt_sha,
        "agreement_sha256": agree_sha,
        "evidence_sha256": evid_sha,
        "review_identity": identity,
    }
    return sha256(canonical(body))
