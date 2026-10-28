"""Read-only batch observation for one page (0508.return-capture/05.13).

Two channels: the pinned parse_source result, unchanged, and an inventory of
unfenced return headings. Custody is an optional live inspector read.
Nothing here accepts, closes, repairs a revision, or writes Git.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path

SCHEMA = "batch-observation/1"
DECLARATION_SCHEMA = "batch-review-declaration/1"
AUTHORITY = "none"
PARSER_SHA = "700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70"
ADAPTER_SHA = "2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4"
INSPECT_SHA = "947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b"
HELPER_SHA = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
PARSER_BYTES = 59791
ADAPTER_BYTES = 11774
INSPECT_BYTES = 11402
HELPER_BYTES = 45767
INSPECT_SCHEMA = "return-capture-inspection/1"
INSPECT_EXIT = {
    "complete": 0,
    "reserved": 1,
    "missing": 1,
    "incomplete": 2,
    "refused": 2,
}
SEP = " — "
POINTER_FORMS = {"return", "return-em", "return-pointer", "return-pointers", "return-archive-pointer"}
DISPOSITIONS = {"accepted", "held", "returned-for-correction"}
DECLARATION_KEYS = {
    "schema",
    "reviewed_member",
    "reviewed_receipt_sha256",
    "reviewed_disposition",
    "reviewer",
}
MEMBER_NAME = r"(\d{4}\.[A-Za-z0-9][A-Za-z0-9._-]{0,63})"
MEMBER_LINE = re.compile(rf"^Member: {MEMBER_NAME}$")
MEMBER_TOKEN = re.compile(rf"(?:^Member: |^Member |\. Member ){MEMBER_NAME}")
BACKTICK_MEMBER = re.compile(rf"`{MEMBER_NAME}`")
RECEIPT_LINE = re.compile(r"^Receipt: ([0-9a-f]{64})$")
ASSIGNMENT_LINE = re.compile(r"\b(\d{4}\.[A-Za-z0-9][A-Za-z0-9._-]{0,63}) captures\b")
PAGE_PATH = re.compile(
    r"^(?P<prefix>.+)/(?P<book>[^/]+)/(?P<page>\d{4}\.[A-Za-z0-9][A-Za-z0-9._-]*)/(?P<batch>05\.\d{2})\.md$"
)
LEGACY_HASH = re.compile(r"Reviewed return SHA-256: `?([0-9a-f]{64})`?")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")

LABS = Path(__file__).resolve().parent.parent
PARSER_PATH = LABS / "prime-support-pass01" / "prime_support.py"
ADAPTER_PATH = LABS / "prime-support-pass01" / "clerk_adapter.py"
INSPECT_PATH = LABS / "return-capture-pass01" / "return_inspect.py"
HELPER_PATH = LABS / "return-capture-pass01" / "return_capture.py"


class ObserveError(Exception):
    pass


def refuse(message: str) -> None:
    raise ObserveError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_bytes(path: Path) -> bytes:
    if not os.path.lexists(path):
        refuse(f"missing {path.name}")
    info = os.lstat(path)
    attrs = getattr(info, "st_file_attributes", 0) or 0
    if attrs & 0x400 or stat.S_ISLNK(info.st_mode):
        refuse(f"link: {path.name}")
    if not stat.S_ISREG(info.st_mode):
        refuse(f"not a regular file: {path.name}")
    return path.read_bytes()


def require_pinned(path: Path, digest: str, size: int, label: str) -> bytes:
    data = file_bytes(path)
    actual = sha256(data)
    if actual != digest or len(data) != size:
        refuse(f"{label} pin mismatch")
    return data


def load_parser(parser_path: Path | None = None, adapter_path: Path | None = None):
    parser_path = PARSER_PATH if parser_path is None else parser_path
    adapter_path = ADAPTER_PATH if adapter_path is None else adapter_path
    require_pinned(adapter_path, ADAPTER_SHA, ADAPTER_BYTES, "clerk adapter")
    require_pinned(parser_path, PARSER_SHA, PARSER_BYTES, "parser")
    spec = importlib.util.spec_from_file_location("prime_support_pinned_observe", parser_path)
    if spec is None or spec.loader is None:
        refuse("parser could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def require_custody_pins(
    inspect_path: Path | None = None,
    helper_path: Path | None = None,
) -> None:
    inspect_path = INSPECT_PATH if inspect_path is None else inspect_path
    helper_path = HELPER_PATH if helper_path is None else helper_path
    require_pinned(helper_path, HELPER_SHA, HELPER_BYTES, "helper")
    require_pinned(inspect_path, INSPECT_SHA, INSPECT_BYTES, "inspector")


def relative_problem(value: str) -> str | None:
    if not isinstance(value, str) or value == "" or len(value) > 4000:
        return "path is empty or too long"
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        return "path has control characters"
    if "\\" in value or value.startswith("/") or re.match(r"^[A-Za-z]:", value) or ":" in value:
        return "path is not a contained relative path"
    for part in value.split("/"):
        if part in ("", ".", "..") or part.endswith(".") or part.endswith(" "):
            return "path is not a contained relative path"
    return None


def require_relative(value: str) -> str:
    problem = relative_problem(value)
    if problem:
        refuse(problem)
    return value


def require_commit(value: str) -> str:
    if not isinstance(value, str) or HEX40.fullmatch(value) is None:
        refuse("commit must be 40 lowercase hex")
    return value


def run_git(repo: str, args: list[str]) -> subprocess.CompletedProcess[bytes]:
    allowed = False
    if args[:3] == ["rev-parse", "--verify", "--end-of-options"] and len(args) == 4:
        allowed = True
    elif args[:3] in (["cat-file", "-t", "--end-of-options"], ["cat-file", "blob", "--end-of-options"]):
        allowed = len(args) == 4
    if not allowed:
        refuse("git command is not a read")
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    return subprocess.run(
        ["git", "-C", repo, *args],
        capture_output=True,
        check=False,
        env=env,
    )


def verify_commit(repo: str, commit: str) -> None:
    probe = run_git(repo, ["rev-parse", "--verify", "--end-of-options", f"{commit}^{{commit}}"])
    if probe.returncode != 0:
        refuse("commit is not in this repository")
    found = probe.stdout.decode("utf-8", "replace").strip()
    if found != commit:
        refuse("commit is not in this repository")


def read_blob(repo: str, commit: str, relpath: str) -> bytes | None:
    """Return blob bytes, or None when that path is absent. Other failures refuse."""
    kind = run_git(repo, ["cat-file", "-t", "--end-of-options", f"{commit}:{relpath}"])
    if kind.returncode != 0:
        return None
    if kind.stdout.strip() != b"blob":
        refuse("git object is not a blob")
    blob = run_git(repo, ["cat-file", "blob", "--end-of-options", f"{commit}:{relpath}"])
    if blob.returncode != 0:
        refuse("git blob could not be read")
    return blob.stdout


def fence_open(line: str) -> str | None:
    stripped = line.lstrip(" ")
    if len(line) - len(stripped) > 3:
        return None
    match = re.match(r"^(`{3,}|~{3,})", stripped)
    return match.group(1) if match else None


def form_of(title: str) -> str | None:
    folded = title.casefold()
    if not (folded.startswith("return") or folded.startswith("review")):
        return None
    if title == "Return":
        return "return"
    if title.startswith("Return" + SEP):
        return "return-em"
    if title == "Return pointer":
        return "return-pointer"
    if title == "Return pointers":
        return "return-pointers"
    if title.startswith("Return archive pointer" + SEP) and title[len("Return archive pointer" + SEP):].strip():
        return "return-archive-pointer"
    if title == "Review":
        return "review"
    if title.startswith("Review" + SEP):
        return "review-em"
    if folded.startswith("return"):
        return "other-return-family"
    return "other-review-family"


def split_lines(data: bytes) -> tuple[str | None, list[str]]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return None, []
    return text, [line.rstrip("\r") for line in text.split("\n")]


def walk_headings(lines: list[str]) -> tuple[list[dict], list[dict]]:
    outside: list[dict] = []
    inside: list[dict] = []
    fence = None
    for number, line in enumerate(lines, start=1):
        if fence:
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                fence = None
            else:
                match = re.match(r"^(#{1,6}) (.*)$", line)
                if match:
                    form = form_of(match.group(2))
                    if form:
                        inside.append({"line": number, "title": match.group(2), "text": line, "form": form})
            continue
        opened = fence_open(line)
        if opened:
            fence = opened
            continue
        match = re.match(r"^(#{1,6}) (.*)$", line)
        if not match or len(match.group(1)) != 2:
            continue
        form = form_of(match.group(2))
        if form is None:
            continue
        outside.append(
            {
                "line": number,
                "level": 2,
                "title": match.group(2),
                "form": form,
                "fenced": False,
                "text": line,
            }
        )
    return outside, inside


def section_body(lines: list[str], start: int, stops: set[int]) -> list[tuple[int, str]]:
    body = []
    for number, line in enumerate(lines, start=1):
        if number <= start:
            continue
        if number in stops and re.match(r"^#{1,2} ", line):
            break
        body.append((number, line))
    return body


def receipt_after(line: str) -> str | None:
    index = line.find("Receipt")
    if index < 0:
        return None
    match = re.search(r"([0-9a-f]{64})", line[index:])
    return match.group(1) if match else None


def member_blocks(body: list[tuple[int, str]], archive: bool = False) -> tuple[list[dict], list[str]]:
    """Member lines inside a pointer. Release lines are quoted instructions and stay out."""
    members: list[dict] = []
    attention: list[str] = []
    current: dict | None = None
    fence = None

    def finish() -> None:
        nonlocal current
        if current is not None:
            members.append(current)
            current = None

    for number, line in body:
        if fence:
            stripped = line.strip()
            if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                fence = None
            continue
        opened = fence_open(line)
        if opened:
            fence = opened
            continue
        stripped = line.strip()
        if stripped.startswith("Release:") or stripped.startswith("Release and claim:"):
            continue
        found = MEMBER_TOKEN.search(stripped)
        if found:
            finish()
            current = {"name": found.group(1).rstrip("."), "line": number, "receipts": []}
        elif archive:
            for match in BACKTICK_MEMBER.finditer(stripped):
                finish()
                current = {"name": match.group(1).rstrip("."), "line": number, "receipts": []}
        receipt = receipt_after(stripped)
        if receipt:
            if current is None:
                if "unpaired-receipt" not in attention:
                    attention.append("unpaired-receipt")
            elif all(item["sha256"] != receipt for item in current["receipts"]):
                current["receipts"].append({"sha256": receipt, "line": number})
            continue
        if stripped.startswith("Member:") and found is None:
            attention.append("unparsed-member-line")
    finish()
    return members, attention


def how_named(form: str) -> str:
    if form == "return-archive-pointer":
        return "archive-pointer"
    if form in {"return", "return-em"}:
        return "recognized-return"
    return "pointer"


def raw_line(lines: list[str], prefix: str) -> str | None:
    for line in lines:
        if line.startswith(prefix):
            return line
    return None


def page_identity(relpath: str | None) -> dict | None:
    if not relpath:
        return None
    match = PAGE_PATH.fullmatch(relpath)
    if match is None:
        return None
    return {"book": match.group("book"), "page": match.group("page"), "batch": match.group("batch"), "prefix": match.group("prefix")}


def loads_strict(data: bytes, label: str):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        refuse(f"{label} is not utf-8")

    def pairs(seq):
        out = {}
        for key, value in seq:
            if key in out:
                refuse(f"{label} duplicate key {key}")
            out[key] = value
        return out

    def reject_constant(_value):
        raise ValueError("non-finite")

    try:
        return json.loads(text, object_pairs_hook=pairs, parse_constant=reject_constant)
    except ObserveError:
        raise
    except json.JSONDecodeError as exc:
        refuse(f"{label} is not json")


def read_declaration(path: str | None) -> dict | None:
    if path is None:
        return None
    body = loads_strict(file_bytes(Path(path)), "declaration")
    if not isinstance(body, dict) or not isinstance(body.get("schema"), str):
        refuse("declaration schema is missing")
    if body["schema"] != DECLARATION_SCHEMA:
        refuse(f"unknown declaration schema {body['schema']}")
    if set(body) != DECLARATION_KEYS:
        refuse("declaration keys are not the contract set")
    member = body["reviewed_member"]
    receipt = body["reviewed_receipt_sha256"]
    disposition = body["reviewed_disposition"]
    reviewer = body["reviewer"]
    if not isinstance(member, str) or MEMBER_LINE.fullmatch(f"Member: {member}") is None:
        refuse("declaration member is not usable")
    if not isinstance(receipt, str) or HEX64.fullmatch(receipt) is None:
        refuse("declaration receipt is not usable")
    if disposition not in DISPOSITIONS:
        refuse("declaration disposition is not usable")
    if not isinstance(reviewer, str) or reviewer == "" or len(reviewer) > 200:
        refuse("declaration reviewer is not usable")
    return {
        "schema": DECLARATION_SCHEMA,
        "reviewed_member": member,
        "reviewed_receipt_sha256": receipt,
        "reviewed_disposition": disposition,
        "reviewer": reviewer,
        "authority": "not authenticated",
    }


def legacy_hashes(review_text: str, revision_id: str | None, whole: str) -> list[dict]:
    found = []
    seen = set()
    for match in LEGACY_HASH.finditer(review_text):
        digest = match.group(1)
        if digest in seen:
            continue
        seen.add(digest)
        found.append(
            {
                "hash": digest,
                "equals_whole": digest == whole,
                "equals_revision": revision_id is not None and digest == revision_id,
            }
        )
    return found


def origins_equal(origin: dict, page: dict) -> bool:
    return (
        origin.get("book") == page["book"]
        and origin.get("page") == page["page"]
        and origin.get("batch") == page["batch"]
    )


def launch_inspect(book: str, member: str, inspect_path: Path) -> tuple[dict | None, int]:
    proc = subprocess.run(
        [sys.executable, "-B", str(inspect_path), "inspect", "--book", book, "--member", member, "--json"],
        capture_output=True,
        check=False,
    )
    try:
        observed = json.loads(proc.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, proc.returncode
    if not isinstance(observed, dict):
        return None, proc.returncode
    return observed, proc.returncode


def inspection_ok(observed: dict, member: str, code: int) -> bool:
    status = observed.get("status")
    return (
        observed.get("schema") == INSPECT_SCHEMA
        and status in INSPECT_EXIT
        and observed.get("member") == member
        and code == INSPECT_EXIT[status]
        and isinstance(observed.get("problems"), list)
    )


def classify(page: dict | None, observations: list[dict]) -> tuple[str | None, list[str]]:
    """Assign roles in place. Return the primary member, if there is exactly one."""
    matched = []
    for item in observations:
        inspection = item["inspection"]
        if item["how_named"] == "assignment-sentence" or inspection is None:
            continue
        if item["role"] != "complete":
            continue
        capture = inspection.get("capture") if isinstance(inspection, dict) else None
        if not isinstance(capture, dict):
            continue
        origin = capture.get("origin")
        retro = capture.get("retrospective")
        if page and isinstance(origin, dict) and retro is False and origins_equal(origin, page):
            matched.append(item)
    ambiguous = len(matched) > 1
    primary = None
    extra: list[str] = []
    if ambiguous:
        extra.append("multiple-primary-candidates")
    for item in observations:
        if item["how_named"] == "assignment-sentence":
            item["role"] = "assignment-mention"
            continue
        inspection = item["inspection"]
        if inspection is None:
            item["role"] = "not-observed" if item["role"] == "pending" else item["role"]
            continue
        if item["role"] == "observation-failed":
            continue
        status = item["role"]
        if status != "complete":
            continue
        capture = inspection.get("capture")
        if not isinstance(capture, dict) or not isinstance(capture.get("origin"), dict):
            item["role"] = "observation-failed"
            item["attention"].append("observation-failed")
            continue
        if type(capture.get("retrospective")) is not bool:
            item["role"] = "observation-failed"
            item["attention"].append("observation-failed")
            continue
        origin = capture["origin"]
        retro = capture["retrospective"]
        if page is None:
            item["role"] = "page-unidentified"
            extra.append("page-unidentified")
            continue
        if origin.get("book") != page["book"]:
            item["role"] = "cross-book-origin"
            extra.append("cross-book-origin")
            continue
        same = origins_equal(origin, page)
        if same and retro:
            item["role"] = "same-page-retrospective"
            continue
        if same and not retro:
            item["role"] = "ambiguous-primary-candidate" if ambiguous else "primary-current-candidate"
            if not ambiguous:
                primary = item["member"]
            continue
        if retro:
            item["role"] = "secondary-historical"
            continue
        item["role"] = "origin-mismatch"
        extra.append("origin-mismatch")
    if primary is None and len(matched) == 1 and not ambiguous:
        primary = matched[0]["member"]
    return primary, extra


def build_observation(
    data: bytes,
    source: dict,
    *,
    members_book: str | None,
    declaration: dict | None,
    parser_module,
    inspect_path: Path = INSPECT_PATH,
    git_repo: str | None = None,
    git_commit: str | None = None,
) -> dict:
    text, lines = split_lines(data)
    parsed = parser_module.parse_source(data, "page-return")
    legacy = {
        "tool": "labs/prime-support-pass01/prime_support.py",
        "sha256": PARSER_SHA,
        "sibling": "labs/prime-support-pass01/clerk_adapter.py",
        "sibling_sha256": ADAPTER_SHA,
        "kind": "page-return",
        "status": parsed["status"],
        "reason": parsed["reason"],
        "revision_id": parsed["revision_id"] if parsed["status"] == "ok" else None,
        "execution": parsed["execution"],
        "whole": parsed["whole"],
        "review": parsed["review"] if parsed["status"] == "ok" else None,
    }
    if parsed["status"] != "ok":
        legacy["revision_id"] = None
        legacy["review"] = None
    ambiguities: list[str] = []
    attention: list[str] = []
    if text is None:
        ambiguities.append("not-utf-8")
    if legacy["status"] == "unsupported" and str(legacy["reason"]).startswith("ambiguous heading"):
        ambiguities.append("legacy-ambiguous-heading")
    elif legacy["status"] == "unsupported" and legacy["reason"] == "duplicate heading":
        ambiguities.append("legacy-duplicate-heading")
    elif legacy["status"] == "no-return":
        ambiguities.append("legacy-no-return")
    elif legacy["status"] != "ok":
        ambiguities.append("legacy-unsupported")
    if legacy["status"] != "ok":
        ambiguities.append("legacy-revision-withheld")
    if legacy["execution"] == "unknown":
        ambiguities.append("legacy-execution-unknown")

    outside, inside = walk_headings(lines) if text is not None else ([], [])
    if inside:
        ambiguities.append("fenced-heading-ignored")
    stops = {item["line"] for item in outside}
    # Also stop a pointer body at any level-2 heading, including non-return titles.
    if text is not None:
        fence = None
        for number, line in enumerate(lines, start=1):
            if fence:
                stripped = line.strip()
                if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                    fence = None
                continue
            opened = fence_open(line)
            if opened:
                fence = opened
                continue
            if re.match(r"^#{1,2} ", line):
                stops.add(number)

    pointers = []
    review_sections = []
    for item in outside:
        body = section_body(lines, item["line"], stops)
        if item["form"] in {"review", "review-em"}:
            review_sections.append(
                {
                    "line": item["line"],
                    "title": item["title"],
                    "text_raw": "\n".join(line for _number, line in body).strip("\n"),
                }
            )
            continue
        if item["form"] not in POINTER_FORMS:
            ambiguities.append("unknown-return-heading")
            continue
        members, member_attention = member_blocks(body, archive=item["form"] == "return-archive-pointer")
        attention.extend(code for code in member_attention if code not in attention)
        first = next((line for _number, line in body if line.strip()), None)
        pointers.append(
            {
                "line": item["line"],
                "form": item["form"],
                "title": item["title"],
                "execution_raw": first,
                "members": members,
            }
        )
    if len(review_sections) > 1:
        ambiguities.append("multiple-review-sections")

    mentions = []
    if text is not None:
        fence = None
        for number, line in enumerate(lines, start=1):
            if fence:
                stripped = line.strip()
                if stripped and set(stripped) == {fence[0]} and len(stripped) >= len(fence):
                    fence = None
                continue
            opened = fence_open(line)
            if opened:
                fence = opened
                continue
            for match in ASSIGNMENT_LINE.finditer(line):
                mentions.append({"member": match.group(1), "line": number, "form": "assignment-sentence"})

    page = page_identity(source.get("path"))
    page_out = None if page is None else {"book": page["book"], "page": page["page"], "batch": page["batch"]}

    grouped: dict[str, dict] = {}
    order: list[str] = []

    def add_stated(name: str, how: str, receipts: list[dict]) -> None:
        if name not in grouped:
            grouped[name] = {
                "member": name,
                "how_named": how,
                "stated_receipts": [],
                "inspection": None,
                "exit": None,
                "role": "pending",
                "commit_receipt_sha256": None,
                "commit_receipt_present": None,
                "receipt_bytes_match": None,
                "attention": [],
            }
            order.append(name)
        item = grouped[name]
        if item["how_named"] == "assignment-sentence" and how != "assignment-sentence":
            item["how_named"] = how
        for receipt in receipts:
            digest = receipt["sha256"]
            if digest not in item["stated_receipts"]:
                item["stated_receipts"].append(digest)
        if len(item["stated_receipts"]) > 1:
            if "conflicting-stated-receipts" not in item["attention"]:
                item["attention"].append("conflicting-stated-receipts")
            if "conflicting-stated-receipts" not in attention:
                attention.append("conflicting-stated-receipts")

    for pointer in pointers:
        named = how_named(pointer["form"])
        for member in pointer["members"]:
            add_stated(member["name"], named, member["receipts"])
    pointer_names = set(order)
    for mention in mentions:
        if mention["member"] in pointer_names:
            continue
        add_stated(mention["member"], "assignment-sentence", [])
        if "assignment-mention-not-pointer" not in ambiguities:
            ambiguities.append("assignment-mention-not-pointer")

    basis = "not-observed"
    if members_book:
        basis = "live"
        for name in order:
            item = grouped[name]
            if item["how_named"] == "assignment-sentence":
                continue
            observed, code = launch_inspect(members_book, name, inspect_path)
            item["exit"] = code
            if observed is None or not inspection_ok(observed, name, code):
                item["role"] = "observation-failed"
                item["inspection"] = observed if isinstance(observed, dict) else None
                item["attention"].append("observation-failed")
                if "observation-failed" not in attention:
                    attention.append("observation-failed")
                continue
            item["inspection"] = observed
            item["role"] = observed["status"]
            if observed["status"] in {"missing", "incomplete", "reserved", "refused"}:
                code_name = f"custody-{observed['status']}"
                item["attention"].append(code_name)
                if code_name not in attention:
                    attention.append(code_name)
            capture = observed.get("capture")
            live_receipt = capture.get("receipt_sha256") if isinstance(capture, dict) else None
            if item["stated_receipts"] and isinstance(live_receipt, str) and live_receipt not in item["stated_receipts"]:
                item["attention"].append("stated-receipt-differs")
                if "stated-receipt-differs" not in attention:
                    attention.append("stated-receipt-differs")
            if (
                source["kind"] == "git-blob"
                and git_repo
                and git_commit
                and page is not None
            ):
                receipt_path = f"{page['prefix']}/{page['book']}/{name}/receipt.json"
                blob = read_blob(git_repo, git_commit, receipt_path)
                item["commit_receipt_present"] = blob is not None
                if blob is not None:
                    item["commit_receipt_sha256"] = sha256(blob)
                    if isinstance(live_receipt, str):
                        item["receipt_bytes_match"] = item["commit_receipt_sha256"] == live_receipt
    elif order:
        inspected = [name for name in order if grouped[name]["how_named"] != "assignment-sentence"]
        if inspected:
            ambiguities.append("custody-not-observed")

    observations = [grouped[name] for name in order]
    primary, role_codes = classify(page, observations)
    for code in role_codes:
        if code not in ambiguities and code not in attention:
            attention.append(code)

    review_text = review_sections[0]["text_raw"] if review_sections else ""
    hashes = legacy_hashes(review_text, legacy["revision_id"], legacy["whole"])
    if legacy["review"] and legacy["review"].get("legacy_whole"):
        digest = legacy["review"]["legacy_whole"]
        if all(item["hash"] != digest for item in hashes):
            hashes.append(
                {
                    "hash": digest,
                    "equals_whole": digest == legacy["whole"],
                    "equals_revision": legacy["revision_id"] is not None and digest == legacy["revision_id"],
                }
            )
    if any(not item["equals_whole"] and not item["equals_revision"] for item in hashes):
        attention.append("legacy-hash-not-current")
    if "Accepted" in review_text or (legacy["review"] and legacy["review"].get("disposition") and "Accepted" in str(legacy["review"]["disposition"])):
        ambiguities.append("quoted-accepted-unbound")
    if declaration is not None:
        attention.append("declaration-not-authenticated")

    header = raw_line(lines, "state: ") if text is not None else None
    tool_bytes = file_bytes(Path(__file__).resolve())
    return {
        "schema": SCHEMA,
        "tool": {
            "name": "batch-observation-pass01",
            "path": "labs/batch-observation-pass01/batch_observe.py",
            "sha256": sha256(tool_bytes),
        },
        "authority": AUTHORITY,
        "source": source,
        "page": page_out,
        "document": {"header_state_raw": header},
        "assignment": {
            "executor_raw": raw_line(lines, "Executor: ") if text is not None else None,
            "release_raw": (
                None
                if text is None
                else raw_line(lines, "Release: ") or raw_line(lines, "Release and claim: ")
            ),
            "claim_raw": raw_line(lines, "Claim: ") if text is not None else None,
        },
        "legacy": legacy,
        "channels": {
            "legacy": "parse_source page-return, unmodified",
            "inventory": "unfenced return-family headings and Member/Receipt blocks",
            "revision_repaired": False,
        },
        "sections": outside,
        "fenced_headings": [{"line": item["line"], "title": item["title"], "text": item["text"]} for item in inside],
        "pointers": pointers,
        "assignment_mentions": mentions,
        "custody": {
            "basis": basis,
            "members_book": members_book,
            "package_at_commit": "not-established",
            "primary": primary,
            "primary_rule": "origin book, page, and batch match this page and retrospective is false; more than one match stays ambiguous",
            "observations": observations,
        },
        "review": {
            "parser_object": legacy["review"],
            "sections": review_sections,
            "text_raw": review_text if review_sections else None,
            "legacy_hashes": hashes,
            "binding": "unbound",
            "typed_declaration": declaration,
        },
        "ambiguities": ambiguities,
        "attention": attention,
    }


def source_git(repo: str, commit: str, relpath: str) -> tuple[bytes, dict]:
    require_commit(commit)
    require_relative(relpath)
    if not os.path.isabs(repo) or not os.path.isdir(repo):
        refuse("repository must be an absolute directory")
    verify_commit(repo, commit)
    blob = read_blob(repo, commit, relpath)
    if blob is None:
        refuse("path is not a blob at this commit")
    return blob, {
        "kind": "git-blob",
        "repository": os.path.abspath(repo),
        "path": relpath,
        "commit": commit,
        "sha256": sha256(blob),
        "bytes": len(blob),
        "label": "git blob at the named commit",
    }


def source_live(repo: str, relpath: str) -> tuple[bytes, dict]:
    require_relative(relpath)
    if not os.path.isabs(repo) or not os.path.isdir(repo):
        refuse("repository must be an absolute directory")
    current = Path(os.path.abspath(repo))
    for part in relpath.split("/"):
        current = current / part
        if not os.path.lexists(current):
            refuse("live path is missing")
        info = os.lstat(current)
        attrs = getattr(info, "st_file_attributes", 0) or 0
        if attrs & 0x400 or stat.S_ISLNK(info.st_mode):
            refuse("live path is a link")
    if not stat.S_ISREG(os.lstat(current).st_mode):
        refuse("live path is not a file")
    data = current.read_bytes()
    return data, {
        "kind": "live-file",
        "repository": os.path.abspath(repo),
        "path": relpath,
        "commit": None,
        "sha256": sha256(data),
        "bytes": len(data),
        "label": "worktree file, not a git blob",
    }


def source_supplied(file_path: str, relpath: str | None) -> tuple[bytes, dict]:
    if relpath is not None:
        require_relative(relpath)
    data = file_bytes(Path(file_path))
    label_path = relpath if relpath is not None else Path(file_path).name
    return data, {
        "kind": "supplied-text",
        "repository": None,
        "path": label_path,
        "commit": None,
        "sha256": sha256(data),
        "bytes": len(data),
        "label": "supplied text, not a git blob",
    }


def observe(argv: list[str]) -> tuple[dict, int]:
    parser = argparse.ArgumentParser(prog="batch_observe.py", add_help=True)
    parser.error = lambda message: refuse(message)  # type: ignore[method-assign]
    sub = parser.add_subparsers(dest="command", required=True)
    observe_parser = sub.add_parser("observe")
    observe_parser.error = parser.error
    observe_parser.add_argument("--repo")
    observe_parser.add_argument("--commit")
    observe_parser.add_argument("--path")
    observe_parser.add_argument("--live", action="store_true")
    observe_parser.add_argument("--supplied")
    observe_parser.add_argument("--members-book")
    observe_parser.add_argument("--declaration")
    observe_parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.command != "observe" or not args.json:
        refuse("json output is required")
    modes = [args.commit is not None, args.live, args.supplied is not None]
    if sum(bool(item) for item in modes) != 1:
        refuse("choose one of commit, live, or supplied")
    if args.live and args.commit:
        refuse("live and commit are separate observations")
    declaration = read_declaration(args.declaration)
    if args.members_book:
        if not os.path.isabs(args.members_book):
            refuse("members book must be absolute")
        require_custody_pins()
    module = load_parser()
    inspect_path = INSPECT_PATH
    if args.supplied is not None:
        if args.commit or args.live or args.repo:
            refuse("supplied text is not a git blob")
        data, source = source_supplied(args.supplied, args.path)
        repo = None
        commit = None
    elif args.live:
        if not args.repo or not args.path or args.commit:
            refuse("live mode needs a repository and a path")
        data, source = source_live(args.repo, args.path)
        repo = None
        commit = None
    else:
        if not args.repo or not args.commit or not args.path:
            refuse("commit mode needs a repository, a commit, and a path")
        data, source = source_git(args.repo, args.commit, args.path)
        repo = os.path.abspath(args.repo)
        commit = args.commit
    document = build_observation(
        data,
        source,
        members_book=args.members_book,
        declaration=declaration,
        parser_module=module,
        inspect_path=inspect_path,
        git_repo=repo,
        git_commit=commit,
    )
    code = 1 if document["ambiguities"] or document["attention"] else 0
    return document, code


def encode(document: dict) -> bytes:
    return (json.dumps(document, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def execute(argv: list[str]) -> tuple[int, bytes, str]:
    try:
        document, code = observe(argv)
    except ObserveError as exc:
        return 2, b"", str(exc)
    return code, encode(document), ""


def main(argv: list[str] | None = None) -> int:
    code, payload, error = execute(sys.argv[1:] if argv is None else argv)
    if error:
        sys.stderr.buffer.write((error + "\n").encode("utf-8"))
    else:
        sys.stdout.buffer.write(payload)
    return code


if __name__ == "__main__":
    sys.exit(main())
