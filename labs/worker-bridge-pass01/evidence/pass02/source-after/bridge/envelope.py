"""Request envelope: shape, identity and input checks. Validation proves well-formedness, not authority."""
import math, re
from pathlib import Path, PurePosixPath
from .canon import canonical, sha256, sha256_file
from . import ids

SCHEMA = "worker-bridge/request@1"
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
FIELDS = {"schema", "delivery_id", "job_id", "role", "work_ref", "inputs", "input_root", "output_root", "limits", "release", "backend"}
LIMITS = {"timeout_s", "max_stdout_bytes", "max_stderr_bytes"}


class EnvelopeError(Exception):
    pass


MAX_TIMEOUT_S = 3600          # lab ceiling: one hour
MAX_CAPTURE_BYTES = 64 * 1024 * 1024   # lab ceiling per stream: 64 MiB


def check_limits(lim):
    """timeout_s: an int or float, not a bool, finite, 0 < t <= MAX_TIMEOUT_S.
    max_stdout_bytes, max_stderr_bytes: an int, not a bool, 1 <= n <= MAX_CAPTURE_BYTES (05.02 #03)."""
    if not isinstance(lim, dict) or set(lim) != LIMITS:
        raise EnvelopeError("limits must be exactly {timeout_s, max_stdout_bytes, max_stderr_bytes}")
    t = lim["timeout_s"]
    if isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t) or not 0 < t <= MAX_TIMEOUT_S:
        raise EnvelopeError(f"timeout_s must be a finite number with 0 < timeout_s <= {MAX_TIMEOUT_S}, not {t!r}")
    for k in ("max_stdout_bytes", "max_stderr_bytes"):
        v = lim[k]
        if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= MAX_CAPTURE_BYTES:
            raise EnvelopeError(f"{k} must be an integer with 1 <= {k} <= {MAX_CAPTURE_BYTES}, not {v!r}")


def request_sha256(env):
    return sha256(canonical(env))


def safe_rel(rel):
    """A relative '/' path with no empty, '.', '..' or drive parts."""
    if not isinstance(rel, str) or not rel or rel.startswith("/") or "\\" in rel or ":" in rel:
        return False
    return all(p not in ("", ".", "..") for p in rel.split("/"))


def inside(root, rel):
    """Resolve root/rel and confirm it stays inside root after following links."""
    root = Path(root).resolve()
    target = (root / PurePosixPath(rel)).resolve()
    return target if (target == root or root in target.parents) else None


def validate(env, check_inputs=True):
    if not isinstance(env, dict):
        raise EnvelopeError("envelope is not an object")
    extra, missing = set(env) - FIELDS, FIELDS - set(env)
    if extra or missing:
        raise EnvelopeError(f"envelope fields: missing {sorted(missing)}, unknown {sorted(extra)}")
    if env["schema"] != SCHEMA:
        raise EnvelopeError(f"schema is not {SCHEMA}")
    try:
        ids.check(env["delivery_id"])
    except ids.IdentityError as e:
        raise EnvelopeError(str(e))
    if not isinstance(env["job_id"], str) or not ID.match(env["job_id"]):
        raise EnvelopeError("job_id is not a plain identifier")
    for k in ("role", "work_ref", "backend", "input_root", "output_root"):
        if not isinstance(env[k], str) or not env[k]:
            raise EnvelopeError(f"{k} is empty")
    check_limits(env["limits"])
    if not isinstance(env["release"], dict) or set(env["release"]) != {"by", "ref"}:
        raise EnvelopeError("release must be {by, ref}")
    ins = env["inputs"]
    if not isinstance(ins, list):
        raise EnvelopeError("inputs is not a list")
    names = set()
    for i in ins:
        if not isinstance(i, dict) or set(i) != {"name", "path", "sha256", "bytes"}:
            raise EnvelopeError("an input is not {name, path, sha256, bytes}")
        if i["name"] in names:
            raise EnvelopeError(f"input name repeated: {i['name']}")
        names.add(i["name"])
        if not safe_rel(i["path"]):
            raise EnvelopeError(f"input path is not a safe relative path: {i['path']!r}")
        if check_inputs:
            p = inside(env["input_root"], i["path"])
            if p is None:
                raise EnvelopeError(f"input escapes its root: {i['path']}")
            if not p.is_file():
                raise EnvelopeError(f"input missing: {i['path']}")
            if p.stat().st_size != i["bytes"] or sha256_file(p) != i["sha256"]:
                raise EnvelopeError(f"input hash differs from the envelope: {i['path']}")
    return request_sha256(env)
