"""Delivery identity and control-plane path containment (05.02 #02). Containment, not authentication.

Windows identifier rules for a delivery_id (it becomes a folder name under the store):
  - a str of 1 to 64 characters;
  - lowercase ASCII letters, digits, '.', '_' and '-' only, so two ids can never name the same folder on a
    case-insensitive file system;
  - starts and ends with a letter or digit, so there is no leading dot and no trailing dot or space (Windows
    silently drops those, which would alias two ids);
  - no '..' anywhere;
  - the part before the first '.' is not a reserved device name (con, prn, aux, nul, com1-com9, lpt1-lpt9).
A path separator, drive letter, colon, absolute path or traversal therefore cannot be an id.
"""
import os, re, stat
from pathlib import Path

PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9._-]{0,62}[a-z0-9])?$")
RESERVED = {"con", "prn", "aux", "nul"} | {f"com{i}" for i in range(1, 10)} | {f"lpt{i}" for i in range(1, 10)}
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class IdentityError(Exception):
    pass


def check(delivery_id):
    if not isinstance(delivery_id, str):
        raise IdentityError(f"delivery_id is not text ({type(delivery_id).__name__})")
    if not PATTERN.match(delivery_id) or ".." in delivery_id:
        raise IdentityError(f"delivery_id {delivery_id!r} breaks the identifier rules (lowercase a-z 0-9 . _ -, 1-64 chars, "
                            "letter or digit at both ends, no '..')")
    if delivery_id.split(".")[0] in RESERVED:
        raise IdentityError(f"delivery_id {delivery_id!r} is a reserved Windows device name")
    return delivery_id


def _is_link(p):
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & REPARSE)


def store_dir(store, delivery_id):
    """The per-delivery folder, after the id rules and a resolved-containment check. Touches nothing."""
    check(delivery_id)
    root = Path(store).resolve()
    d = root / delivery_id
    if _is_link(d):
        raise IdentityError(f"the delivery folder {delivery_id!r} is a link or reparse point")
    if os.path.lexists(d) and d.resolve().parent != root:
        raise IdentityError(f"the delivery folder {delivery_id!r} resolves outside the store")
    return d
