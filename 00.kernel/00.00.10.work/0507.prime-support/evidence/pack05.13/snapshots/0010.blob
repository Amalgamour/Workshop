"""Read one return member. The sibling helper is pinned and executed only on a hash match.

This module does not reserve, capture, repair, allocate, or write. Package
integrity comes from the helper's verify_member. Review, acceptance, seating,
and publication are outside the observation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import types
from pathlib import Path

HELPER_NAME = "return_capture.py"
HELPER_SHA256 = "8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac"
SCHEMA = "return-capture-inspection/1"
FILE_ATTRIBUTE_REPARSE_POINT = 0x400
EXIT = {
    "complete": 0,
    "reserved": 1,
    "missing": 1,
    "incomplete": 2,
    "refused": 2,
}
RESERVED_NAMES = {"01.md", "reservation.json"}


def sibling() -> Path:
    return Path(__file__).resolve().parent / HELPER_NAME


def encode(value) -> bytes:
    """Canonical JSON for a refusal that happens before the helper is executed."""
    text = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return (text + "\n").encode("utf-8")


def pin_bytes(path: Path) -> tuple[str | None, bytes | None]:
    """Hash the sibling before any of its code runs. Links are not followed."""
    if not os.path.lexists(path):
        return "helper is missing", None
    try:
        info = os.lstat(path)
    except OSError as exc:
        return f"helper is unreadable: {type(exc).__name__}: {exc.strerror or exc}", None
    attrs = getattr(info, "st_file_attributes", 0) or 0
    if attrs & FILE_ATTRIBUTE_REPARSE_POINT or stat.S_ISLNK(info.st_mode):
        return "helper is link", None
    if not stat.S_ISREG(info.st_mode):
        return "helper is not-regular", None
    if info.st_nlink != 1:
        return "helper is link-count", None
    try:
        data = path.read_bytes()
    except OSError as exc:
        return f"helper is unreadable: {type(exc).__name__}: {exc.strerror or exc}", None
    digest = hashlib.sha256(data).hexdigest()
    if digest != HELPER_SHA256:
        return f"helper hash mismatch: expected {HELPER_SHA256} actual {digest}", None
    return None, data


def load_helper():
    path = sibling()
    problem, data = pin_bytes(path)
    if problem or data is None:
        return None, problem or "helper is missing"
    module = types.ModuleType("return_capture_pinned")
    module.__file__ = str(path)
    exec(compile(data, str(path), "exec"), module.__dict__)
    return module, None


def refusal_problems(exc: BaseException) -> list[str]:
    lines = [line for line in str(exc).splitlines() if line and line != "result refused"]
    return lines or ["refused"]


def blank(book: str, member: str, status: str, problems: list[str]) -> dict:
    return {
        "schema": SCHEMA,
        "book": book,
        "member": member,
        "status": status,
        "problems": problems,
        "reservation": None,
        "capture": None,
    }


def display_book(text: str) -> str:
    if isinstance(text, str) and os.path.isabs(text):
        return os.path.abspath(text)
    return text if isinstance(text, str) else ""


def origin_view(origin: dict) -> dict:
    return {"book": origin["book"], "page": origin["page"], "batch": origin["batch"]}


def destination_view(destination: dict) -> dict:
    return {
        "member": destination["member"],
        "name": destination["name"],
        "path": destination["path"],
    }


def reservation_view(body: dict, digest: str) -> dict:
    return {
        "submission_id": body["submission_id"],
        "origin": origin_view(body["origin"]),
        "destination": destination_view(body["destination"]),
        "expected_outputs": list(body["expected_outputs"]),
        "submitter": body["submitter"],
        "reviewer": body["reviewer"],
        "release": body["release"],
        "supersedes": body["supersedes"],
        "reserved_at": body["reserved_at"],
        "reservation_sha256": digest,
    }


def read_reservation(module, member_path: Path, folder: str) -> tuple[dict | None, list[str]]:
    path = member_path / "reservation.json"
    if not os.path.lexists(path):
        return None, []
    try:
        data, value = module.load_json_file(path)
        body = module.parse_reservation(data, value)
    except module.Refusal as exc:
        return None, refusal_problems(exc)
    problems = []
    destination = body["destination"]
    match = module._MEMBER.fullmatch(folder)
    number = int(match.group(1))
    if destination["path"] != folder:
        problems.append("destination path does not match the member folder")
    if destination["member"] != f"{number:04d}" or destination["name"] != match.group(2):
        problems.append("destination identity does not match the member folder")
    if problems:
        return None, problems
    return reservation_view(body, module.sha256_bytes(data)), []


def capture_view(info: dict) -> dict:
    reservation = info["reservation"]
    manifest = info["manifest"]
    payloads = []
    for source, (_rel, digest) in zip(manifest["sources"], info["payloads"]):
        payloads.append(
            {
                "logical": source["logical"],
                "payload": source["payload"],
                "sha256": digest,
                "bytes": source["bytes"],
            }
        )
    return_meta = manifest["return"]
    return {
        "submission_id": reservation["submission_id"],
        "origin": origin_view(reservation["origin"]),
        "retrospective": manifest["retrospective"],
        "source_commit": manifest["source_commit"],
        "captured_at": manifest["captured_at"],
        "reservation_sha256": info["reservation_sha256"],
        "manifest_sha256": info["manifest_sha256"],
        "receipt_sha256": info["receipt_sha256"],
        "return": {
            "sha256": return_meta["sha256"],
            "bytes": return_meta["bytes"],
            "includes_prime_review": return_meta["includes_prime_review"],
        },
        "payloads": payloads,
    }


def reservation_from_info(info: dict) -> dict:
    """Project the reservation verify_member already accepted."""
    body = info["reservation"]
    return reservation_view(body, info["reservation_sha256"])


def reserved_shape(module, member_path: Path) -> bool:
    try:
        names = set(os.listdir(member_path))
    except OSError:
        return False
    if "reservation.json" not in names or not names <= RESERVED_NAMES:
        return False
    for name in names:
        if module.plain_file_problem(member_path / name):
            return False
    return module.capture_entries(member_path) == []


def inspect_loaded(module, book: str, member: str) -> dict:
    try:
        book_path = module.require_reader_book(book)
    except module.Refusal as exc:
        shown = display_book(book) if isinstance(book, str) else ""
        requested = member if isinstance(member, str) else ""
        return blank(shown, requested, "refused", refusal_problems(exc))
    book_text = str(book_path)
    member_text = member if isinstance(member, str) else ""
    match = module._MEMBER.fullmatch(member) if isinstance(member, str) else None
    if (
        not isinstance(member, str)
        or "/" in member
        or "\\" in member
        or match is None
        or module.id_problem(match.group(2), "member")
    ):
        return blank(book_text, member_text, "refused", ["member path is not a return member"])
    member_path = book_path / member
    if not module.within(member_path, book_path):
        return blank(book_text, member_text, "refused", ["member path is outside the book"])
    number = int(match.group(1))
    if not (module.MEMBER_MIN <= number <= module.MEMBER_MAX):
        return blank(book_text, member_text, "refused", ["member is outside the return band"])
    if not os.path.lexists(member_path):
        return blank(book_text, member_text, "missing", ["member is absent"])
    problem = module.plain_dir_problem(member_path)
    if problem:
        return blank(book_text, member_text, "refused", [f"member is {problem}"])
    try:
        module.reject_reparse_parents(member_path)
    except module.Refusal as exc:
        return blank(book_text, member_text, "refused", refusal_problems(exc))
    reservation, reservation_problems = read_reservation(module, member_path, member)
    try:
        info = module.verify_member(member_path)
    except module.Refusal as exc:
        problems = refusal_problems(exc)
        for item in reservation_problems:
            if item not in problems:
                problems.append(item)
        state, _info = module.assess(member_path)
        if (
            state == "absent"
            and reservation is not None
            and not reservation_problems
            and reserved_shape(module, member_path)
        ):
            observed = blank(book_text, member_text, "reserved", ["reservation only"])
            observed["reservation"] = reservation
            return observed
        if (
            state == "absent"
            and reservation is None
            and not reservation_problems
            and not os.path.lexists(member_path / "reservation.json")
            and module.capture_entries(member_path) == []
        ):
            return blank(book_text, member_text, "missing", ["empty member"])
        observed = blank(book_text, member_text, "incomplete", problems)
        if reservation is not None and not reservation_problems:
            observed["reservation"] = reservation
        return observed
    observed = blank(book_text, member_text, "complete", [])
    observed["reservation"] = reservation_from_info(info)
    observed["capture"] = capture_view(info)
    return observed


def inspect_member(book: str, member: str) -> tuple[dict, bytes]:
    module, problem = load_helper()
    if module is None:
        observed = blank(display_book(book), member if isinstance(member, str) else "", "refused", [problem])
        return observed, encode(observed)
    try:
        observed = inspect_loaded(module, book, member)
    except OSError as exc:
        observed = blank(
            display_book(book),
            member if isinstance(member, str) else "",
            "refused",
            [f"filesystem: {type(exc).__name__}: {exc.strerror or exc}"],
        )
        return observed, module.canonical(observed)
    return observed, module.canonical(observed)


def execute(argv: list[str]) -> tuple[int, bytes]:
    parser = argparse.ArgumentParser(prog="return_inspect.py")
    sub = parser.add_subparsers(dest="command", required=True)
    inspect_parser = sub.add_parser("inspect")
    inspect_parser.add_argument("--book", required=True)
    inspect_parser.add_argument("--member", required=True)
    inspect_parser.add_argument("--json", action="store_true", required=True)
    args = parser.parse_args(argv)
    observed, payload = inspect_member(args.book, args.member)
    return EXIT[observed["status"]], payload


def main(argv: list[str] | None = None) -> int:
    try:
        code, payload = execute(sys.argv[1:] if argv is None else argv)
    except SystemExit as exc:
        status = exc.code
        return 2 if status is None else int(status)
    sys.stdout.buffer.write(payload)
    return code


if __name__ == "__main__":
    sys.exit(main())
