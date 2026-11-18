"""Book path guards and durable writes. Advisory locks are not race freedom."""

from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from .identity import LIMITS, Refused, canonical, loads, require_object, sha256

BOOK_SCHEMA = "desk-core-book/1"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _reject_symlink_chain(path: Path) -> None:
    current = path
    while True:
        if current.is_symlink():
            raise Refused("symlink", f"symlink refused: {current}")
        if current == current.parent:
            break
        current = current.parent


def outside_book(text: str) -> Path:
    raw = Path(text)
    if not raw.is_absolute():
        raise Refused("book-path", "book path must be absolute")
    _reject_symlink_chain(raw)
    resolved = raw.resolve(strict=False)
    repo = repo_root().resolve()
    try:
        resolved.relative_to(repo)
    except ValueError:
        inside = False
    else:
        inside = True
    if inside or "00.kernel" in resolved.parts and "00.00.10.work" in resolved.parts:
        raise Refused("live-book-refused", "book path is inside the Librarian checkout or a live work book")
    return resolved


def atomic_write(path: Path, data: bytes) -> None:
    if path.is_symlink():
        raise Refused("symlink", f"refusing to write through symlink {path.name}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    fd = os.open(tmp, os.O_CREAT | os.O_TRUNC | os.O_WRONLY, 0o644)
    try:
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)
    os.replace(tmp, path)


def exclusive_write(path: Path, data: bytes) -> None:
    if path.exists() or path.is_symlink():
        raise Refused("exists", f"{path.name} already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
    try:
        os.write(fd, data)
        os.fsync(fd)
    finally:
        os.close(fd)


def read_bytes(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise Refused("read", f"missing plain file {path.name}")
    return path.read_bytes()


def read_json(path: Path, label: str) -> dict[str, object]:
    value = loads(read_bytes(path), label)
    return require_object(value, label)


def write_json(path: Path, value: dict[str, object], exclusive: bool = False) -> None:
    data = json.dumps(value, indent=2, sort_keys=True).encode("utf-8") + b"\n"
    if exclusive:
        exclusive_write(path, data)
    else:
        atomic_write(path, data)


@contextmanager
def file_lock(path: Path) -> Iterator[None]:
    import fcntl

    path.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o644)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)


def header_body(label: str) -> dict[str, object]:
    return {
        "schema": BOOK_SCHEMA,
        "label": label,
        "synthetic": True,
        "task_ledger": False,
        "limits": list(LIMITS),
    }


def book_header(book: Path) -> dict[str, object]:
    header = book / "00.desk.json"
    if not book.is_dir() or header.is_symlink() or not header.is_file():
        raise Refused("book-missing", "disposable book header is missing")
    value = read_json(header, "00.desk.json")
    if value.get("schema") != BOOK_SCHEMA or value.get("task_ledger") is not False:
        raise Refused("book-schema", "book schema is not desk-core-book/1")
    return value


def open_book(text: str) -> Path:
    book = outside_book(text)
    book_header(book)
    return book


def digest_file(path: Path) -> str:
    return sha256(read_bytes(path))


def stable_id(value: dict[str, object]) -> str:
    return sha256(canonical(value))
