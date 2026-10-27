"""Result verifier: shape, correlation with the request, and artifact bytes inside the output root."""
import json, os, stat
from pathlib import Path, PurePosixPath
from .canon import StrictJSONError, sha256_file, strict_loads
from .envelope import safe_rel

SCHEMA = "worker-bridge/result@1"
FIELDS = {"schema", "delivery_id", "job_id", "request_sha256", "outcome", "artifacts", "diagnostics"}
REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


def _reparse(p):
    try:
        st = os.lstat(p)
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(st.st_mode) or bool(getattr(st, "st_file_attributes", 0) & REPARSE)


def parse(stdout_bytes):
    """Return (result dict, None) or (None, reason)."""
    try:
        text = stdout_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return None, "stdout is not UTF-8"
    try:
        res = strict_loads(text)
    except json.JSONDecodeError as e:
        return None, f"stdout is not one JSON value ({e.msg})"
    except StrictJSONError as e:
        return None, f"stdout is not strict JSON ({e})"
    if not isinstance(res, dict) or set(res) != FIELDS:
        return None, "result fields are not exactly " + ", ".join(sorted(FIELDS))
    if res["schema"] != SCHEMA:
        return None, f"result schema is not {SCHEMA}"
    if res["outcome"] not in ("done", "failed"):
        return None, "outcome is not done or failed"
    if not isinstance(res["artifacts"], list) or not all(isinstance(a, dict) and set(a) == {"path", "sha256", "bytes"} for a in res["artifacts"]):
        return None, "artifacts are not a list of {path, sha256, bytes}"
    if not isinstance(res["diagnostics"], str):
        return None, "diagnostics is not text"
    return res, None


def correlate(res, env, req_sha):
    bad = []
    for k, want in (("delivery_id", env["delivery_id"]), ("job_id", env["job_id"]), ("request_sha256", req_sha)):
        if res[k] != want:
            bad.append(f"{k} is {res[k]!r}, request has {want!r}")
    return bad


def collect(res, output_root):
    """Verify every declared artifact. Returns (verified list, reasons)."""
    root = Path(output_root).resolve()
    ok, bad = [], []
    for a in res["artifacts"]:
        rel = a["path"]
        if not safe_rel(rel):
            bad.append(f"artifact path is not a safe relative path: {rel!r}")
            continue
        target = Path(os.path.abspath(root / PurePosixPath(rel)))
        cur, chain_bad = root, False
        for part in PurePosixPath(rel).parts:
            cur = cur / part
            if _reparse(cur):
                bad.append(f"artifact path crosses a link or reparse point: {rel}")
                chain_bad = True
                break
        if chain_bad:
            continue
        if root not in target.resolve().parents:
            bad.append(f"artifact escapes the output root: {rel}")
            continue
        if not target.is_file():
            bad.append(f"artifact missing: {rel}")
            continue
        if target.stat().st_size != a["bytes"] or sha256_file(target) != a["sha256"]:
            bad.append(f"artifact bytes differ from the result: {rel}")
            continue
        ok.append({"path": rel, "sha256": a["sha256"], "bytes": a["bytes"]})
    return ok, bad
