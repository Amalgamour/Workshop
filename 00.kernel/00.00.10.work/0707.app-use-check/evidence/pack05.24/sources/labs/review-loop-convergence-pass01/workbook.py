#!/usr/bin/env python3
"""One review-loop candidate workbook (0522/05.17, note 06.36).

Loads the pinned N5 instance workbook, which loads pass05. Does not import the
N7-local prototype. Re-expresses N7 exchange, open, and the pack-bound exemption
on this chain, and adds the two 06.37 freshness repairs.

Helper root is D:\\Git\\lib-build. A copied file fails the canonical path check.
instance_id stays path/page/pass. A same-path replacement clone is not detected.
"""

from __future__ import annotations

import contextvars
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
CANONICAL_FILE = REPO / "labs" / "review-loop-convergence-pass01" / "workbook.py"
INSTANCE_REL = "labs/review-instance-binding-pass01/workbook.py"
INSTANCE_SHA = "3f8118ccdc2c7afc4abdca2d52c3510864f159642ed06aee52a485709be55aba"
INSTANCE_BYTES = 5916
SUCCESSOR_REL = "labs/review-source-capacity-pass03/prime_review.py"
SUCCESSOR_SHA = "c15cbd2460200583cab0518e2ac16f4a95356a779edb4b1978dfb4afc2a3e7ab"
SUCCESSOR_BYTES = 6136
OPEN_NAME = "exchange-open.json"
POINTER_MARK = b"## Return pointer"
REVIEW_MARK = b"## Review"

COMPARE = contextvars.ContextVar("convergence_comparison_hold", default=None)
N7_RENDER = contextvars.ContextVar("convergence_n7_render", default=False)


def refuse_boot(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def load_instance():
    here = Path(__file__).resolve()
    if os.path.normcase(str(here)) != os.path.normcase(str(CANONICAL_FILE)):
        refuse_boot("convergence workbook is not at its canonical root")
    path = REPO / INSTANCE_REL
    data = path.read_bytes()
    if len(data) != INSTANCE_BYTES or hashlib.sha256(data).hexdigest() != INSTANCE_SHA:
        refuse_boot("instance workbook pin mismatch")
    spec = importlib.util.spec_from_file_location("workbook_review_instance_binding_pass01", path)
    if spec is None or spec.loader is None:
        refuse_boot("instance workbook did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inst = load_instance()
p5 = inst.p5
p4 = p5.p4
p3 = p5.p3
p2 = p3.p2
wb = p3.wb
BASE_BUILD = wb.build_intake
BASE_CHANGED = p2.source_changed
BASE_RESULT = wb.result
BASE_PERFORM = wb.perform
BASE_RENDER = wb.render_body
BASE_POINTER = wb.pointer_block


def _sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def _lines(blob: bytes) -> list[tuple[int, bytes]]:
    lines: list[tuple[int, bytes]] = []
    index = 0
    size = len(blob)
    while index < size:
        found = blob.find(b"\n", index)
        if found < 0:
            chunk = blob[index:]
            if chunk.endswith(b"\r"):
                chunk = chunk[:-1]
            lines.append((index, chunk))
            break
        chunk = blob[index:found]
        if chunk.endswith(b"\r"):
            chunk = chunk[:-1]
        lines.append((index, chunk))
        index = found + 1
    if not lines:
        lines.append((0, b""))
    return lines


def _is_pointer(text: bytes) -> bool:
    if not text.startswith(POINTER_MARK):
        return False
    return text[len(POINTER_MARK):].strip() == b""


def _is_review(text: bytes) -> bool:
    return text == REVIEW_MARK or text.startswith(REVIEW_MARK + b" ")


def classify_pack(blob: bytes) -> dict:
    """Exact unfenced headings. Ambiguous or missing structure has no bound hash."""
    fenced = False
    pointers: list[int] = []
    reviews: list[int] = []
    for start, text in _lines(blob):
        if text.strip().startswith(b"```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if _is_pointer(text):
            pointers.append(start)
        elif _is_review(text):
            reviews.append(start)
    status = "clear"
    if fenced:
        status = "ambiguous"
    elif not pointers or not reviews:
        status = "missing"
    elif len(pointers) != 1 or len(reviews) != 1 or reviews[0] <= pointers[0]:
        status = "ambiguous"
    full = _sha(blob)
    if status != "clear":
        return {"bound_sha256": None, "body_sha256": None, "sha256": full, "structure": status}
    return {
        "bound_sha256": _sha(blob[: reviews[0]]),
        "body_sha256": _sha(blob[: pointers[0]]),
        "sha256": full,
        "structure": "clear",
    }


def _pointer_body(blob: bytes) -> str | None:
    """Text between the one unfenced pointer heading and the one unfenced review heading."""
    fenced = False
    pointer_at = None
    review_at = None
    for start, text in _lines(blob):
        if text.strip().startswith(b"```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        if pointer_at is None and _is_pointer(text):
            newline = blob.find(b"\n", start)
            pointer_at = len(blob) if newline < 0 else newline + 1
        elif pointer_at is not None and _is_review(text):
            review_at = start
            break
    if pointer_at is None or review_at is None or review_at < pointer_at:
        return None
    return blob[pointer_at:review_at].decode("utf-8", "replace").strip("\n")


def pointer_block(text):
    """A fenced sample is not the declaration when the unfenced headings are clear.

    Pages with no fence keep the historical cutter. Ambiguous structure keeps it
    too: this function does not choose among several real headings.
    """
    if not isinstance(text, str) or "```" not in text:
        return BASE_POINTER(text)
    blob = text.encode("utf-8")
    if classify_pack(blob).get("structure") != "clear":
        return BASE_POINTER(text)
    body = _pointer_body(blob)
    if body is None:
        return BASE_POINTER(text)
    return body


wb.pointer_block = pointer_block


def _declared_places(book: Path, rel: str, page: str | None) -> list[dict]:
    page_id = page if isinstance(page, str) else getattr(p2, "_resolve_page", None)
    found: list[dict] = []
    seen: dict[str, dict] = {}

    def consider(root_name: str, root: Path, rel_path: str) -> None:
        path = root / rel_path
        if wb.is_link(path) or not path.is_file():
            return
        try:
            resolved = path.resolve()
        except OSError:
            return
        if not wb.inside(resolved, root.resolve()):
            return
        key = os.path.normcase(os.path.abspath(resolved))
        item = {"file": path, "path": rel_path, "root": root_name}
        previous = seen.get(key)
        if previous is not None:
            if previous["root"] == "book" or root_name != "book":
                return
            found.remove(previous)
        seen[key] = item
        found.append(item)

    consider("book", book, rel)
    if rel.startswith(p2.WORK_PREFIX):
        consider("book", book, rel[len(p2.WORK_PREFIX):])
    if isinstance(page_id, str) and page_id != "":
        prefix = page_id + "/"
        if not rel.startswith(prefix) and not rel.startswith(p2.WORK_PREFIX):
            consider("book", book, prefix + rel)
    consider("code", wb.REPO, rel)
    return found


BASE_LOCATE = p3.locate_declared


def locate_declared(book: Path, rel: str, page: str | None = None):
    """Equal book and helper-root bytes bind the book copy.

    The capacity candidate pointed REPO at a private tree, so a copied kernel
    page did not collide with the checkout. This helper root is the checkout.
    Two different files stay ambiguous. The same bytes bind the external book.
    """
    located, how = BASE_LOCATE(book, rel, page)
    if how != "ambiguous":
        return located, how
    found = _declared_places(book, rel, page)
    if len(found) != 2 or {item["root"] for item in found} != {"book", "code"}:
        return None, "ambiguous"
    book_item = next(item for item in found if item["root"] == "book")
    code_item = next(item for item in found if item["root"] == "code")
    try:
        if book_item["file"].read_bytes() != code_item["file"].read_bytes():
            return None, "ambiguous"
    except OSError:
        return None, "ambiguous"
    return book_item, "one"


p3.locate_declared = locate_declared
p2.locate_declared = locate_declared
wb.locate_declared = locate_declared


def _hex64(value) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(char in "0123456789abcdef" for char in value)


def install_capacity() -> None:
    successor = REPO / SUCCESSOR_REL
    original = wb.pin_file

    def pin_file(key: str) -> Path:
        if key != "prime_review":
            return original(key)
        if wb.is_link(successor) or not successor.is_file():
            wb.refuse("prime_review capacity pin is missing")
        data = successor.read_bytes()
        if len(data) != SUCCESSOR_BYTES or hashlib.sha256(data).hexdigest() != SUCCESSOR_SHA:
            wb.refuse("prime_review capacity pin mismatch")
        return successor

    wb.pin_file = pin_file


install_capacity()


def open_path(book: Path, page: str, pass_id: str) -> Path:
    return book / wb.STORE / page / pass_id / OPEN_NAME


def _read_open(path: Path):
    if not path.is_file() or wb.is_link(path):
        return None, False
    try:
        payload = json.loads(path.read_bytes().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None, True
    if not isinstance(payload, dict):
        return None, True
    return payload, True


def exchange_of(book: Path, intake: dict) -> dict:
    page, pass_id = intake["page"], intake["pass"]
    pack_rel, ret_rel = f"{page}/{pass_id}.pack.md", f"{page}/{pass_id}.return.md"
    pack, ret = book / pack_rel, book / ret_rel
    pack_ok = pack.is_file() and not wb.is_link(pack)
    ret_ok = ret.is_file() and not wb.is_link(ret)
    codes = {item.get("code") for item in intake.get("findings") or [] if isinstance(item, dict)}
    subs = sorted(
        row.get("path") for row in intake.get("rows") or [] if isinstance(row, dict) and row.get("role") == "submission"
    )
    if not pack_ok:
        legacy = intake.get("assignment_path") == f"{page}/{pass_id}.md"
        state = "assignment-not-pack" if legacy else ("orphan-return" if ret_ok else "pack-missing")
    elif "return-pending" in codes or "return-pointer-empty" in codes or "return-pointer-absent" in codes:
        state = "pointer-pending"
    elif subs != [ret_rel]:
        state = "return-not-local"
    else:
        state = "matched"
    pack_id = classify_pack(pack.read_bytes()) if pack_ok else None
    opened, present = _read_open(open_path(book, page, pass_id))
    chronology = "unverified"
    if present:
        body_hash = None if pack_id is None else pack_id.get("body_sha256")
        opened_hash = None if opened is None else opened.get("pack_body_sha256")
        if (
            opened is not None
            and _hex64(body_hash)
            and opened_hash == body_hash
            and opened.get("return_present") is False
        ):
            chronology = "recorded-before-return"
        else:
            chronology = "open-record-mismatch"
    pack_view = {"path": pack_rel, "present": pack_ok}
    if pack_id is not None:
        pack_view.update(pack_id)
    return {
        "schema": "n7-local-exchange/0",
        "route": "n7-local",
        "n1_custody": "not-applicable",
        "book": str(book.resolve()),
        "page": page,
        "pass": pass_id,
        "pack": pack_view,
        "return": {"path": ret_rel, "present": ret_ok, "sha256": _sha(ret.read_bytes()) if ret_ok else None},
        "declared_submission": subs,
        "destination": intake.get("destination"),
        "state": state,
        "unfiled_return_preserved": bool(ret_ok and state != "matched"),
        "chronology": chronology,
        "open_record": opened,
    }


def build_intake(book: Path, source: str, pass_id: str) -> dict:
    intake = BASE_BUILD(book, source, pass_id)
    N7_RENDER.set(intake.get("kind") == "N7NN")
    if intake.get("kind") != "N7NN":
        return intake
    exchange = exchange_of(book, intake)
    findings = [
        item for item in intake.get("findings") or []
        if not (isinstance(item, dict) and item.get("code") == "custody-missing")
    ]
    findings.append({"code": "n1-not-applicable", "path": None})
    if exchange["state"] != "matched":
        findings.append({"code": f"n7-exchange-{exchange['state']}", "path": exchange["return"]["path"]})
        intake["measurement"] = "incomplete"
    intake["findings"] = findings
    intake["exchange"] = exchange
    p3.rehash(intake)
    return intake


def _current_record(book: Path, live: dict, journal: dict) -> str | None:
    if not isinstance(journal, dict):
        return None
    current = journal.get("current")
    if not isinstance(current, str) or current == "":
        return None
    path = wb.record_path(book, live, current)
    if not path.is_file() or wb.is_link(path):
        return None
    return current


def comparison_hold(book: Path, stored, live: dict, journal: dict) -> dict | None:
    """Unknown applicability when a current review exists and comparison intake is unusable.

    A book with no current review is left to the predecessor. Invalid JSON raises
    through strict_json and is not turned into this hold.
    """
    current = _current_record(book, live, journal)
    if current is None or isinstance(stored, dict):
        return None
    path = wb.store_root(book, live) / "intake.json"
    if not path.is_file() or wb.is_link(path):
        reason = "comparison-intake-missing"
    else:
        payload = wb.strict_json(path.read_bytes(), "stored intake")
        if isinstance(payload, dict):
            return None
        reason = "comparison-intake-not-object"
    return {"reason": reason, "review_id": current, "state": "unknown"}


def _clear_bound(pack: dict) -> str | None:
    if pack.get("structure") != "clear":
        return None
    digest = pack.get("bound_sha256")
    if not _hex64(digest):
        return None
    return digest


def source_changed(book: Path, stored, live: dict, journal: dict) -> bool:
    inst.HOLD.set(None)
    COMPARE.set(None)
    hold = comparison_hold(book, stored, live, journal)
    if hold is not None:
        COMPARE.set(hold)
        return True
    if isinstance(live, dict) and live.get("kind") == "N7NN" and isinstance(stored, dict):
        if stored.get("book") != live.get("book"):
            return True
        old_pack = (stored.get("exchange") or {}).get("pack") or {}
        new_pack = (live.get("exchange") or {}).get("pack") or {}
        old_bound = _clear_bound(old_pack)
        new_bound = _clear_bound(new_pack)
        if old_bound is not None and old_bound == new_bound:
            old_rows = {key: value for key, value in p2.row_map(stored).items() if key[1] != "assignment"}
            new_rows = {key: value for key, value in p2.row_map(live).items() if key[1] != "assignment"}
            return old_rows != new_rows
    return BASE_CHANGED(book, stored, live, journal)


def render_body(record: dict) -> str:
    if (
        N7_RENDER.get()
        and isinstance(record, dict)
        and record.get("custody") == "missing"
        and record.get("mode") != "cycle-committed"
    ):
        record["custody"] = "not-applicable"
    return BASE_RENDER(record)


def result(command: str, intake, exit_code: int, **extra) -> dict:
    body = BASE_RESULT(command, intake, exit_code, **extra)
    if isinstance(intake, dict) and isinstance(intake.get("exchange"), dict) and "exchange" not in body:
        body = dict(body)
        body["exchange"] = intake["exchange"]
    hold = COMPARE.get()
    if hold is not None and "current_applicability" not in body:
        body = dict(body)
        body["current_applicability"] = hold
    if (
        command == "record"
        and isinstance(intake, dict)
        and intake.get("kind") == "N7NN"
        and body.get("custody") == "missing"
        and body.get("mode") != "cycle-committed"
    ):
        body = dict(body)
        body["custody"] = "not-applicable"
    return body


def _publish_block(values: dict[str, str]) -> dict | None:
    book = wb.book_dir(values["--book"])
    intake = build_intake(book, values["--source"], values["--pass"])
    journal = p2.journal_of(book, intake)
    stored = wb.read_stored_intake(book, intake)
    hold = comparison_hold(book, stored, intake, journal)
    if hold is None:
        return None
    COMPARE.set(hold)
    review_id = values.get("--review") or hold["review_id"]
    record = None
    path = wb.record_path(book, intake, review_id)
    if path.is_file() and not wb.is_link(path):
        record = wb.load_record(book, intake, review_id)
    judgment = record.get("judgment") if isinstance(record, dict) else None
    action = record.get("next_action") if isinstance(record, dict) else None
    return result(
        "publish",
        intake,
        1,
        correction="Publication is blocked because the comparison intake is missing or is not an object.",
        judgment=judgment,
        next_action=action,
        published=False,
        review_id=review_id,
        stale=True,
    )


def perform(args: list[str]) -> int:
    inst.HOLD.set(None)
    COMPARE.set(None)
    N7_RENDER.set(False)
    command, values = wb.parse_call(args)
    if command == "publish":
        blocked = _publish_block(values)
        if blocked is not None:
            wb.emit(blocked)
            return int(blocked["exit"])
    return BASE_PERFORM(args)


for _namespace in (p5, p4, p3, p2, wb):
    _namespace.build_intake = build_intake
p2.source_changed = source_changed
wb.render_body = render_body
wb.result = result
wb.perform = perform
p2.perform = perform


def _flag(args: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    index = 0
    while index < len(args):
        token = args[index]
        if token not in ("--book", "--source", "--pass") or index + 1 >= len(args) or token in values:
            wb.refuse("usage: open --book ABS --source PAGE --pass 05.NN")
        values[token] = args[index + 1]
        index += 2
    if set(values) != {"--book", "--source", "--pass"}:
        wb.refuse("usage: open --book ABS --source PAGE --pass 05.NN")
    return values


def do_open(args: list[str]) -> int:
    values = _flag(args)
    book = wb.book_dir(values["--book"])
    address = wb.address_of(values["--source"], values["--pass"])
    if address.get("kind") != "N7NN":
        wb.refuse("open is for N7 pages only")
    wb.writable(book)
    wb._active_book = book
    wb._allowed_target = None
    page, pass_id = values["--source"], values["--pass"]
    pack = book / f"{page}/{pass_id}.pack.md"
    ret = book / f"{page}/{pass_id}.return.md"
    if not pack.is_file() or wb.is_link(pack):
        wb.refuse("no pack to open")
    info = classify_pack(pack.read_bytes())
    target = open_path(book, page, pass_id)
    target.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "schema": "n7-local-open/0",
        "page": page,
        "pass": pass_id,
        "pack_path": f"{page}/{pass_id}.pack.md",
        "pack_body_sha256": info["body_sha256"],
        "pack_structure": info["structure"],
        "return_present": bool(ret.is_file() and not wb.is_link(ret)),
        "note": "observed by this command at this moment; not a historical timestamp",
    }
    wb.exclusive_write(target, wb.pretty(document))
    sys.stdout.buffer.write(wb.pretty(document))
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] == "open":
        try:
            return do_open(args[1:])
        except wb.Refusal as exc:
            print(f"refused: {exc.message}", file=sys.stderr)
            return 2
    return inst.main(argv)


if __name__ == "__main__":
    sys.exit(main())
