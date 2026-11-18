#!/usr/bin/env python3
"""0707/05.06 pass06: NONPRODUCTION acceptance harness, successor of pass05/harness5.py (unchanged).

usage:
  harness6.py preflight --config ABS
  harness6.py run --config ABS --matrix real|stub --evidence ABS

H04 (this pass): path text in the CLI and config is validated before use, and
ValueError/OSError from filesystem calls and the interpreter launch become coded
REFUSED at their sites. Other exceptions are not swallowed. pass05 winjob.py,
stub_cases5.py and stubs/STUB5.py are reused unchanged, by hash.

Earlier repairs kept: H01 timeout output kept, launched tree contained by a Job Object;
H02 canonical output/evidence boundaries, re-checked at the fixture-write entry;
H03 complete config validation with controlled REFUSED. The real matrix is
pass04's cases.py with pass04's fixtures.py, loaded unchanged by hash; only the
fixture-write entry is wrapped in memory. A null candidate identity is UNREADY and
its path is never opened. Exit 0 PASS, 1 FAIL or INCOMPLETE, 2 UNREADY or REFUSED.
Execution status only; not acceptance.
"""

from __future__ import annotations

import datetime
import hashlib
import importlib
import json
import os
import re
import secrets
import subprocess
import sys
import time
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
PASS04 = HERE.parent / "pass04"
PASS05 = HERE.parent / "pass05"
sys.path.insert(0, str(HERE))
sys.path.insert(1, str(PASS05))
import guards6 as G  # noqa: E402

CHECKOUT = G.CHECKOUT
PACK = G.LIVE_BOOK / "0707.app-use-check" / "evidence" / "pack05.06" / "source-manifest.json"
REUSED = ("colab/labs/0707.app-use-check/pass05/winjob.py", "colab/labs/0707.app-use-check/pass05/stub_cases5.py",
          "colab/labs/0707.app-use-check/pass05/stubs/STUB5.py")


def _reused_provenance() -> dict:
    pins = {r["path"]: r for r in json.loads(PACK.read_text(encoding="utf-8"))["files"]}
    out = {}
    for rel in REUSED:
        digest = hashlib.sha256((CHECKOUT / rel).read_bytes()).hexdigest()
        if digest != pins[rel]["sha256"]:
            raise SystemExit(f"reused pass05 file differs from its pack05.06 pin: {rel}")
        out[rel] = digest
    return out


REUSED_PROVENANCE = _reused_provenance()
import winjob  # noqa: E402  (pass05, unchanged, hash-checked above)
CONFIG_SCHEMA = "acceptance-candidate/1"
CONFIG_KEYS = {"schema", "kind", "label", "candidate", "dependencies", "interpreter", "output_root", "timeout_seconds", "field_map", "release"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
MAX_CONFIG = 1 << 20
LAUNCH_HOOK = None
ACTIVE_FIXTURES: Path | None = None


class Refused(Exception):
    def __init__(self, code: str, detail: str) -> None:
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def dump(v) -> bytes:
    return (json.dumps(v, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n").encode("utf-8")


# ---------------------------------------------------------------- H03 config
def path_field(value, label: str) -> str:
    """H04: shape-level path text check; no filesystem access."""
    try:
        return G.path_text(value, label)
    except G.Boundary as exc:
        raise Refused("config-path", exc.detail) from None


def read_config(path_text) -> bytes:
    if not isinstance(path_text, str) or not path_text:
        raise Refused("config-path", "--config is required")
    p = Path(path_field(path_text, "--config"))
    try:
        if not p.is_file():
            raise Refused("config-missing", f"config file not found: {path_text}")
        raw = p.read_bytes()
    except (ValueError, OSError) as exc:
        raise Refused("config-read", f"{type(exc).__name__}: {exc}") from None
    if len(raw) > MAX_CONFIG:
        raise Refused("config-size", "config is larger than 1 MiB")
    return raw


def parse_config(raw: bytes) -> dict:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise Refused("config-encoding", "config starts with a BOM")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise Refused("config-encoding", "config is not UTF-8") from None

    def pairs(items):
        keys = [k for k, _ in items]
        if len(keys) != len(set(keys)):
            raise Refused("config-json", "config repeats a key")
        return dict(items)

    def constant(name):
        raise Refused("config-json", f"config has non-finite number {name}")

    try:
        cfg = json.loads(text, object_pairs_hook=pairs, parse_constant=constant)
    except json.JSONDecodeError as exc:
        raise Refused("config-json", f"config is not JSON: {exc.msg} at {exc.pos}") from None
    validate_config(cfg)
    return cfg


def _pin(value, where: str, *, nullable: bool) -> None:
    if not isinstance(value, dict) or set(value) != {"path", "sha256", "bytes"}:
        raise Refused("config-shape", f"{where} must be an object with exactly path, sha256, bytes")
    if not isinstance(value["path"], str) or not value["path"]:
        raise Refused("config-shape", f"{where}.path must be a non-empty string")
    s, b = value["sha256"], value["bytes"]
    if nullable and s is None and b is None:
        return
    if (s is None) != (b is None):
        raise Refused("config-shape", f"{where} identity is half-known: sha256 and bytes must both be null or both be set")
    if not isinstance(s, str) or HEX64.fullmatch(s) is None:
        raise Refused("config-shape", f"{where}.sha256 must be 64 lowercase hex")
    if not isinstance(b, int) or isinstance(b, bool) or b < 0:
        raise Refused("config-shape", f"{where}.bytes must be a non-negative integer")


def validate_config(cfg) -> None:
    """Shape only. Unknown candidate identity is NOT a shape error; it is decided later (UNREADY)."""
    if not isinstance(cfg, dict):
        raise Refused("config-shape", "config must be a JSON object")
    if set(cfg) != CONFIG_KEYS:
        missing, extra = sorted(CONFIG_KEYS - set(cfg)), sorted(set(cfg) - CONFIG_KEYS)
        raise Refused("config-shape", f"config keys differ: missing {missing}, extra {extra}")
    if cfg["schema"] != CONFIG_SCHEMA:
        raise Refused("config-shape", "schema must be acceptance-candidate/1")
    if cfg["kind"] not in ("candidate", "stub") or not isinstance(cfg["kind"], str):
        raise Refused("config-shape", "kind must be candidate or stub")
    if not isinstance(cfg["label"], str) or not cfg["label"].strip():
        raise Refused("config-shape", "label must be non-empty text")
    _pin(cfg["candidate"], "candidate", nullable=True)
    deps = cfg["dependencies"]
    if not isinstance(deps, list):
        raise Refused("config-shape", "dependencies must be a list")
    if cfg["kind"] == "candidate" and not deps:
        raise Refused("config-shape", "a candidate config must pin at least one dependency")
    for i, dep in enumerate(deps):
        _pin(dep, f"dependencies[{i}]", nullable=False)
    interp = cfg["interpreter"]
    if not isinstance(interp, dict) or set(interp) != {"path", "version"} or not all(isinstance(interp[k], str) and interp[k] for k in interp):
        raise Refused("config-shape", "interpreter must be {path, version} with non-empty strings")
    if not isinstance(cfg["output_root"], str) or not cfg["output_root"]:
        raise Refused("config-shape", "output_root must be a non-empty string")
    t = cfg["timeout_seconds"]
    if not isinstance(t, int) or isinstance(t, bool) or not 1 <= t <= 600:
        raise Refused("config-shape", "timeout_seconds must be an integer from 1 to 600")
    fm = cfg["field_map"]
    if not isinstance(fm, dict) or not all(isinstance(k, str) and k and isinstance(v, str) and v for k, v in fm.items()):
        raise Refused("config-shape", "field_map must map non-empty strings to non-empty strings")
    rel = cfg["release"]
    if not isinstance(rel, dict) or set(rel) != {"invocation", "note"} or not (rel["invocation"] is None or isinstance(rel["invocation"], str)) \
            or not isinstance(rel["note"], str):
        raise Refused("config-shape", "release must be {invocation: null|string, note: string}")
    # H04: path text of every path-bearing field (string checks only; an unknown candidate is never opened)
    path_field(cfg["candidate"]["path"], "candidate.path")
    for i, dep in enumerate(deps):
        path_field(dep["path"], f"dependencies[{i}].path")
    path_field(interp["path"], "interpreter.path")
    path_field(cfg["output_root"], "output_root")


def check_file_pin(pin: dict, where: str) -> None:
    p = Path(pin["path"])
    p = p if p.is_absolute() else CHECKOUT / p
    try:
        if not p.is_file():
            raise Refused("pin", f"{where} is missing: {pin['path']}")
        data = p.read_bytes()
    except (ValueError, OSError) as exc:
        raise Refused("pin", f"{where} could not be read: {type(exc).__name__}: {exc}") from None
    if sha(data) != pin["sha256"] or len(data) != pin["bytes"]:
        raise Refused("pin", f"{where} bytes differ from its pin: {pin['path']}")


def preflight(cfg: dict, matrix: str | None = None) -> dict:
    """Assumes validate_config passed. Order: kind/matrix, output boundary, identity, pins, interpreter."""
    try:
        if matrix == "real" and cfg["kind"] != "candidate":
            raise Refused("kind", "the real matrix requires kind candidate; a stub never produces loop evidence")
        if matrix == "stub" and cfg["kind"] != "stub":
            raise Refused("kind", "the stub matrix runs only stub configs")
        try:
            out = G.output_root(cfg["output_root"])
        except G.Boundary as exc:
            raise Refused(exc.code, exc.detail) from None
        if cfg["candidate"]["sha256"] is None:
            return {"status": "UNREADY", "reasons": ["candidate identity unknown: sha256/bytes are null; nothing is launched and the path is not read"],
                    "candidate": "unknown", "output_root_canonical": str(out)}
        check_file_pin(cfg["candidate"], "candidate")
        for i, dep in enumerate(cfg["dependencies"]):
            check_file_pin(dep, f"dependency {i}")
        ipath = Path(cfg["interpreter"]["path"])
        try:
            if not ipath.is_file():
                raise Refused("interpreter", "interpreter is missing")
            probe = subprocess.run([str(ipath), "-I", "-B", "-c", "import platform;print(platform.python_version())"], capture_output=True, timeout=30)
        except (ValueError, OSError) as exc:
            raise Refused("interpreter", f"interpreter could not be launched: {type(exc).__name__}: {exc}") from None
        except subprocess.TimeoutExpired:
            raise Refused("interpreter", "interpreter version probe timed out") from None
        got = probe.stdout.decode("utf-8", "replace").strip()
        if probe.returncode != 0 or got != cfg["interpreter"]["version"]:
            raise Refused("interpreter", f"interpreter version {got!r} differs from {cfg['interpreter']['version']!r}")
    except Refused as exc:
        return {"status": "REFUSED", "reasons": [f"{exc.code}: {exc.detail}"]}
    return {"status": "READY", "reasons": [], "candidate": "pinned", "output_root_canonical": str(out)}


# ---------------------------------------------------------------- pass04 matrix, unchanged, by hash
def load_pass04():
    pins = {r["path"]: r for r in json.loads(PACK.read_text(encoding="utf-8"))["files"]}
    prov = {}
    for name in ("cases.py", "fixtures.py"):
        rel = f"colab/labs/0707.app-use-check/pass04/{name}"
        data = (PASS04 / name).read_bytes()
        if sha(data) != pins[rel]["sha256"]:
            raise Refused("provenance", f"pass04 {name} differs from its pack05.05 pin")
        prov[rel] = pins[rel]["sha256"]
    if str(PASS04) not in sys.path:
        sys.path.insert(0, str(PASS04))
    fixtures = importlib.import_module("fixtures")
    cases = importlib.import_module("cases")
    if getattr(fixtures.build_book, "_pass06_guard", False) is False:
        original = fixtures.build_book

        def guarded_build_book(root, kind):
            """H02 at the fixture-write entry: a fresh, link-free directory under the run's fixture root."""
            if ACTIVE_FIXTURES is None:
                raise Refused("boundary", "no active fixture root; fixtures are written only during a READY run")
            try:
                G.chain_without_links(Path(root).parent)
                resolved = G.canonical(Path(root))
            except G.Boundary as exc:
                raise Refused(exc.code, exc.detail) from None
            if not G.within(resolved, ACTIVE_FIXTURES) or G.protected_hit(resolved) is not None:
                raise Refused("boundary", f"fixture book {resolved} is not inside the run's fixture root {ACTIVE_FIXTURES}")
            if os.path.lexists(root):
                raise Refused("occupied", f"fixture book {root} already exists")
            return original(root, kind)

        guarded_build_book._pass06_guard = True
        fixtures.build_book = guarded_build_book
    return cases, fixtures, prov


# ---------------------------------------------------------------- H01 launch
class Run:
    def __init__(self, cfg: dict | None, raw: bytes | None, matrix: str, evidence: Path) -> None:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.name = f"{stamp}-{secrets.token_hex(3)}"
        G.fs(evidence.mkdir, "mkdir evidence", parents=True, exist_ok=True)
        self.dir = G.fresh_dir(evidence / self.name, evidence)
        self.cfg, self.matrix, self.launches = cfg, matrix, 0
        self.fixtures: Path | None = None
        if raw is not None:
            (self.dir / "config.raw").write_bytes(raw)

    def call(self, case_dir: Path, label: str, argv: list[str]) -> dict:
        calls = case_dir / "calls"
        calls.mkdir(exist_ok=True)
        stem = f"{len(list(calls.glob('*.json'))) + 1:02d}-{label}"
        if LAUNCH_HOOK:
            LAUNCH_HOOK(argv)
        self.launches += 1
        start = time.time()
        flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
        kw = {"creationflags": flags} if os.name == "nt" else {"start_new_session": True}
        proc = subprocess.Popen(argv, cwd=str(CHECKOUT), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"), **kw)
        box = winjob.Containment(proc)
        timed_out, reason, termination, leftover = False, None, None, None
        try:
            out, err = proc.communicate(timeout=self.cfg["timeout_seconds"])
            status = "complete"
            active = box.active()
            if active:
                leftover = active
                termination = box.terminate()
        except subprocess.TimeoutExpired:
            timed_out = True
            reason = "pipes held by a descendant after the parent exited" if proc.poll() is not None else "parent still running"
            termination = box.terminate()
            try:
                out, err = proc.communicate(timeout=15)
                status = "complete-after-termination"
            except subprocess.TimeoutExpired as late:
                out, err = late.stdout or b"", late.stderr or b""
                status = "partial-cleanup-incomplete"
        finally:
            box.close()
        (calls / f"{stem}.stdout").write_bytes(out)
        (calls / f"{stem}.stderr").write_bytes(err)
        row = {"label": label, "argv": argv, "parent_exit": proc.returncode, "exit": None if timed_out else proc.returncode,
               "timed_out": timed_out, "timeout_reason": reason, "termination": termination,
               "containment": {"method": box.method, "note": box.note}, "leftover_descendants": leftover,
               "output_status": status, "stdout_bytes": len(out), "stderr_bytes": len(err),
               "stdout_sha256": sha(out), "stderr_sha256": sha(err), "seconds": round(time.time() - start, 3)}
        (calls / f"{stem}.json").write_bytes(dump(row))
        try:
            parsed = json.loads(out.decode("utf-8")) if out.strip() else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            parsed = None
        return dict(row, json=parsed, stderr=err.decode("utf-8", "replace"))


class Ctx:
    """Same interface the pass04 cases use."""

    def __init__(self, run: Run, case_id: str) -> None:
        self.run, self.id = run, case_id
        self.dir = G.fresh_dir(run.dir / "cases" / case_id, run.dir)
        self.checks, self.calls, self.root = [], [], None

    def check(self, label, ok, observed=None, expected=None):
        self.checks.append({"check": label, "ok": bool(ok), "observed": observed, "expected": expected})
        return bool(ok)

    def field(self, obj, path):
        path = self.run.cfg["field_map"].get(path, path)
        cur = obj
        for part in path.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return "<absent>"
            cur = cur[part]
        return cur

    def cli(self, label, *args):
        cand = self.run.cfg["candidate"]["path"]
        cand = cand if Path(cand).is_absolute() else str(CHECKOUT / cand)
        row = self.run.call(self.dir, label, [self.run.cfg["interpreter"]["path"], "-B", cand, *args])
        self.calls.append(row)
        return row


def run_matrix(config_text: str, matrix: str, evidence_text: str) -> tuple[int, dict]:
    global ACTIVE_FIXTURES
    try:
        evidence = G.evidence_root(evidence_text)
    except G.Boundary as exc:
        return 2, {"aggregate": "REFUSED", "reasons": [f"{exc.code}: {exc.detail}"], "run": None, "evidence": "not written (evidence boundary refused)"}
    raw, cfg, pre = None, None, None
    try:
        raw = read_config(config_text)
    except Refused as exc:
        pre = {"status": "REFUSED", "reasons": [f"{exc.code}: {exc.detail}"]}
    try:
        run = Run(None, raw, matrix, evidence)
    except G.Boundary as exc:
        return 2, {"aggregate": "REFUSED", "reasons": [f"{exc.code}: {exc.detail}"], "run": None,
                   "evidence": "not written (run directory could not be created; no fallback location)"}
    if pre is None:
        try:
            cfg = parse_config(raw)
        except Refused as exc:
            pre = {"status": "REFUSED", "reasons": [f"{exc.code}: {exc.detail}"]}
    run.cfg = cfg
    if pre is None:
        pre = preflight(cfg, matrix)
    (run.dir / "preflight.json").write_bytes(dump(pre))
    try:
        if matrix == "real":
            module, _fx, prov = load_pass04()
        else:
            module, prov = importlib.import_module("stub_cases5"), {}
    except Refused as exc:
        pre = {"status": "REFUSED", "reasons": [f"{exc.code}: {exc.detail}"]}
        module, prov = None, {}
    rows = []
    if pre["status"] == "READY":
        out_root = Path(pre["output_root_canonical"])
        try:
            run.fixtures = G.fresh_dir(out_root / run.name, out_root)
            ACTIVE_FIXTURES = run.fixtures
        except G.Boundary as exc:
            pre = {"status": "REFUSED", "reasons": [f"{exc.code}: fixture root: {exc.detail}"]}
            (run.dir / "preflight.json").write_bytes(dump(pre))
    try:
        for case in (module.CASES if module else []):
            cid, title, fn, manual = case["id"], case["title"], case["fn"], case.get("manual")
            if pre["status"] != "READY":
                rows.append({"id": cid, "title": title, "status": "NOT RUN", "reason": f"preflight {pre['status']}"})
                continue
            if manual:
                rows.append({"id": cid, "title": title, "status": "MANUAL", "reason": manual})
                continue
            try:
                ctx = Ctx(run, cid)
            except G.Boundary as exc:
                rows.append({"id": cid, "title": title, "status": "ERROR", "error": f"case directory: {exc.code}: {exc.detail}"})
                continue
            error = None
            try:
                fn(ctx)
                status = "PASS" if ctx.checks and all(c["ok"] for c in ctx.checks) else "FAIL"
            except Exception:  # noqa: BLE001
                status, error = "ERROR", traceback.format_exc()
            anomalies = [c["label"] for c in ctx.calls if c["timed_out"] or c["leftover_descendants"] or c["output_status"] != "complete"]
            if anomalies:
                status = "ERROR"
            (ctx.dir / "checks.json").write_bytes(dump({"checks": ctx.checks, "error": error, "call_anomalies": anomalies}))
            rows.append({"id": cid, "title": title, "status": status, "failed_checks": [c["check"] for c in ctx.checks if not c["ok"]],
                         "call_anomalies": anomalies, "error": error and error.splitlines()[-1]})
    finally:
        ACTIVE_FIXTURES = None
    if pre["status"] in ("REFUSED", "UNREADY"):
        aggregate, code = pre["status"], 2
    elif any(r["status"] in ("FAIL", "ERROR") for r in rows):
        aggregate, code = "FAIL", 1
    elif any(r["status"] in ("MANUAL", "NOT RUN") for r in rows):
        aggregate, code = "INCOMPLETE", 1
    else:
        aggregate, code = "PASS", 0
    summary = {
        "schema": "acceptance-run/2", "run": run.name, "matrix": matrix, "kind": cfg.get("kind") if cfg else None,
        "config_sha256": sha(raw) if raw is not None else None, "preflight": pre, "aggregate": aggregate, "exit": code,
        "loop_evidence": bool(cfg) and cfg.get("kind") == "candidate" and pre["status"] == "READY",
        "launches": run.launches, "cases": rows, "matrix_provenance": prov, "reused_pass05": REUSED_PROVENANCE,
        "code_sha256": {n: sha((HERE / n).read_bytes()) for n in ("harness6.py", "guards6.py")},
        "canonical_paths": {"evidence_root": str(evidence), "run_dir": str(run.dir), "fixture_root": str(run.fixtures) if run.fixtures else None},
        "command": [sys.executable, "-I", "-B", str(HERE / "harness6.py"), "run", "--config", config_text, "--matrix", matrix, "--evidence", evidence_text],
        "statement": "execution status of this harness only; not acceptance, review or release",
    }
    (run.dir / "summary.json").write_bytes(dump(summary))
    table = ["| case | status | detail |", "|---|---|---|"] + [
        f"| {r['id']} | {r['status']} | {r.get('reason') or ', '.join((r.get('failed_checks') or []) + (r.get('call_anomalies') or [])) or (r.get('error') or '')} |"
        for r in rows]
    (run.dir / "CASES.md").write_text(f"# {run.name} — {matrix} matrix — aggregate {aggregate}\n\n" + "\n".join(table) + "\n", encoding="utf-8")
    return code, summary


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        if args[:1] == ["preflight"] and len(args) == 3 and args[1] == "--config":
            cfg = parse_config(read_config(args[2]))
            pre = preflight(cfg)
            print(json.dumps(pre, indent=2))
            return 0 if pre["status"] == "READY" else 2
        if (args[:1] == ["run"] and len(args) == 7 and args[1] == "--config" and args[3] == "--matrix"
                and args[4] in ("real", "stub") and args[5] == "--evidence"):
            code, summary = run_matrix(args[2], args[4], args[6])
            print(summary["run"], summary["aggregate"], f"exit {code}", *summary.get("reasons", []))
            return code
    except Refused as exc:
        print(f"refused: {exc.code}: {exc.detail}", file=sys.stderr)
        return 2
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
