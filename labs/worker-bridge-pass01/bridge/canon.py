"""Canonical JSON and hashing helpers."""
import hashlib, json, os
from pathlib import Path


def canonical(value):
    """Canonical JSON bytes. NaN and Infinity are refused (allow_nan=False): they are not JSON (05.02 #03)."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


class StrictJSONError(ValueError):
    pass


def _reject_constant(name):
    raise StrictJSONError(f"non-standard JSON number {name}")


def _no_duplicates(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise StrictJSONError(f"duplicate key {k!r}")
        out[k] = v
    return out


def strict_loads(data):
    """Parse one JSON value from UTF-8 bytes or text, refusing NaN, Infinity, -Infinity and duplicate keys,
    which Python's json module otherwise accepts (05.02 #03)."""
    if isinstance(data, (bytes, bytearray)):
        data = bytes(data).decode("utf-8")
    return json.loads(data, parse_constant=_reject_constant, object_pairs_hook=_no_duplicates)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_atomic(path, data, fail_before_replace=False):
    """Write bytes to a temp file beside the target, flush, then replace. A crash before the replace leaves
    the old target (or none) and a stray .tmp; readers ignore .tmp files."""
    path = Path(path)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "wb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if fail_before_replace:
        raise OSError("simulated crash before replace")
    os.replace(tmp, path)


def write_exclusive(path, data):
    """Create a file that must not exist yet (exclusive create). Raises FileExistsError otherwise."""
    with open(path, "xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
