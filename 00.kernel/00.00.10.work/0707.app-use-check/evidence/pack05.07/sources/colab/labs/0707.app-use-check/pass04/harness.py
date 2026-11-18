#!/usr/bin/env python3
"""0707/05.04 pass04: NONPRODUCTION external acceptance harness for the isolated loop candidate.

usage:
  harness.py preflight --config ABS
  harness.py run --config ABS --matrix real|stub [--evidence ABS]

A candidate with a null identity is UNREADY: its path is never opened, statted or
hashed, and nothing is launched. A changed candidate, dependency or interpreter
is REFUSED before launch. A stub config can only run the stub matrix. Exit
0 PASS, 1 FAIL or INCOMPLETE, 2 UNREADY or REFUSED. Execution status is not
acceptance; Prime judges.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import os
import secrets
import signal
import subprocess
import sys
import time
import traceback
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
CHECKOUT = Path(r"D:\Git\lib-build")
LIVE_BOOK = CHECKOUT / "00.kernel" / "00.00.10.work"
DEFAULT_EVIDENCE = LIVE_BOOK / "0707.app-use-check" / "evidence" / "lab05.04" / "runs"
CONFIG_SCHEMA = "acceptance-candidate/1"
CONFIG_KEYS = {"schema", "kind", "label", "candidate", "dependencies", "interpreter", "output_root", "timeout_seconds", "field_map", "release"}
PIN_KEYS = {"path", "sha256", "bytes"}
LAUNCH_HOOK = None  # tests may set a callable(argv) to observe launches


class Refused(Exception):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def inside(child: Path, parent: Path) -> bool:
    c = os.path.normcase(os.path.abspath(child))
    p = os.path.normcase(os.path.abspath(parent))
    return c == p or c.startswith(p.rstrip(os.sep) + os.sep)


def load_config(path: Path) -> tuple[dict, bytes]:
    raw = path.read_bytes()
    cfg = json.loads(raw.decode("utf-8"))
    if not isinstance(cfg, dict) or set(cfg) != CONFIG_KEYS or cfg.get("schema") != CONFIG_SCHEMA:
        raise Refused("config is not acceptance-candidate/1 with the exact keys")
    return cfg, raw


def check_pin(pin, where: str, *, allow_unknown: bool) -> str:
    """Return 'unknown' or 'ok'; raise Refused on any mismatch. Never touches the file when unknown."""
    if not isinstance(pin, dict) or set(pin) != PIN_KEYS or not isinstance(pin["path"], str) or not pin["path"]:
        raise Refused(f"{where} pin is malformed")
    if pin["sha256"] is None or pin["bytes"] is None:
        if allow_unknown:
            return "unknown"
        raise Refused(f"{where} identity is unknown")
    path = Path(pin["path"])
    path = path if path.is_absolute() else CHECKOUT / path
    if not path.is_file():
        raise Refused(f"{where} is missing: {pin['path']}")
    data = path.read_bytes()
    if sha(data) != pin["sha256"] or len(data) != pin["bytes"]:
        raise Refused(f"{where} bytes differ from its pin: {pin['path']}")
    return "ok"


def preflight(cfg: dict, matrix: str | None = None) -> dict:
    """READY, UNREADY or REFUSED. Order: shape, roots, kind/matrix, candidate identity, then bytes."""
    reasons: list[str] = []
    try:
        if cfg["kind"] not in ("candidate", "stub"):
            raise Refused("kind is not candidate or stub")
        if matrix == "real" and cfg["kind"] != "candidate":
            raise Refused("the real matrix requires kind candidate; a stub can never produce loop evidence")
        if matrix == "stub" and cfg["kind"] != "stub":
            raise Refused("the stub matrix runs only stub configs")
        out = Path(cfg["output_root"]) if isinstance(cfg["output_root"], str) else None
        if out is None or not out.is_absolute() or not out.is_dir():
            raise Refused("output_root must be an existing absolute directory")
        if inside(out, CHECKOUT) or inside(CHECKOUT, out) or inside(out, LIVE_BOOK):
            raise Refused("output_root must be outside the checkout and the live book")
        t = cfg["timeout_seconds"]
        if not isinstance(t, int) or isinstance(t, bool) or not 1 <= t <= 600:
            raise Refused("timeout_seconds must be an integer from 1 to 600")
        if not isinstance(cfg["field_map"], dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in cfg["field_map"].items()):
            raise Refused("field_map must map contract paths to candidate paths")
        state = check_pin(cfg["candidate"], "candidate", allow_unknown=True)
        if state == "unknown":
            return {"status": "UNREADY", "reasons": ["candidate identity unknown: sha256/bytes are null; nothing is launched and the path is not read"],
                    "candidate": "unknown"}
        for i, dep in enumerate(cfg["dependencies"]):
            check_pin(dep, f"dependency {i}", allow_unknown=False)
        interp = cfg["interpreter"]
        if not isinstance(interp, dict) or set(interp) != {"path", "version"}:
            raise Refused("interpreter must be {path, version}")
        ipath = Path(interp["path"])
        if not ipath.is_file():
            raise Refused("interpreter is missing")
        probe = subprocess.run([str(ipath), "-I", "-B", "-c", "import platform;print(platform.python_version())"],
                               capture_output=True, timeout=30)
        got = probe.stdout.decode("utf-8", "replace").strip()
        if probe.returncode != 0 or got != interp["version"]:
            raise Refused(f"interpreter version {got!r} differs from {interp['version']!r}")
    except Refused as exc:
        return {"status": "REFUSED", "reasons": [str(exc)]}
    return {"status": "READY", "reasons": reasons, "candidate": "pinned"}


def kill_tree(proc: subprocess.Popen) -> dict:
    """Kill only the child this harness launched and that child's descendants."""
    if os.name == "nt":
        r = subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], capture_output=True, timeout=30)
        how = {"method": "taskkill /T /F on the launched child pid", "exit": r.returncode}
    else:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
            how = {"method": "killpg on the child's own session", "exit": 0}
        except ProcessLookupError:
            how = {"method": "killpg", "exit": "already-exited"}
    try:
        proc.communicate(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
    return how


class Run:
    def __init__(self, cfg: dict, cfg_raw: bytes, matrix: str, evidence: Path) -> None:
        stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.name = f"{stamp}-{secrets.token_hex(3)}"
        evidence.mkdir(parents=True, exist_ok=True)
        self.dir = evidence / self.name
        self.dir.mkdir()  # exclusive
        self.cfg, self.matrix = cfg, matrix
        (self.dir / "config.json").write_bytes(cfg_raw)
        self.fixtures = Path(cfg["output_root"]) / self.name if isinstance(cfg.get("output_root"), str) else None
        self.launches = 0

    def call(self, case_dir: Path, label: str, argv: list[str]) -> dict:
        calls = case_dir / "calls"
        calls.mkdir(exist_ok=True)
        n = len(list(calls.glob("*.json"))) + 1
        stem = f"{n:02d}-{label}"
        if LAUNCH_HOOK:
            LAUNCH_HOOK(argv)
        self.launches += 1
        start = time.time()
        kw = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        proc = subprocess.Popen(argv, cwd=str(CHECKOUT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, **kw)
        timed_out, killed = False, None
        try:
            out, err = proc.communicate(timeout=self.cfg["timeout_seconds"])
        except subprocess.TimeoutExpired:
            timed_out = True
            killed = kill_tree(proc)
            out, err = b"", b""
        (calls / f"{stem}.stdout").write_bytes(out)
        (calls / f"{stem}.stderr").write_bytes(err)
        try:
            parsed = json.loads(out.decode("utf-8")) if out.strip() else None
        except (UnicodeDecodeError, json.JSONDecodeError):
            parsed = None
        row = {"label": label, "argv": argv, "exit": None if timed_out else proc.returncode, "timed_out": timed_out, "killed": killed,
               "seconds": round(time.time() - start, 3), "stdout_sha256": sha(out), "stderr_sha256": sha(err)}
        (calls / f"{stem}.json").write_bytes(dump(row))
        row["json"], row["stderr"] = parsed, err.decode("utf-8", "replace")
        return row


class Ctx:
    """What a case function sees. Every check is recorded; nothing is silently skipped."""

    def __init__(self, run: Run, case_id: str) -> None:
        self.run, self.id = run, case_id
        self.dir = run.dir / "cases" / case_id
        self.dir.mkdir(parents=True)
        self.checks: list[dict] = []
        self.calls: list[dict] = []
        self.root: Path | None = None

    def check(self, label: str, ok: bool, observed=None, expected=None) -> bool:
        self.checks.append({"check": label, "ok": bool(ok), "observed": observed, "expected": expected})
        return bool(ok)

    def field(self, obj, path: str):
        path = self.run.cfg["field_map"].get(path, path)
        cur = obj
        for part in path.split("."):
            if not isinstance(cur, dict) or part not in cur:
                return "<absent>"
            cur = cur[part]
        return cur

    def cli(self, label: str, *args: str) -> dict:
        cand = self.run.cfg["candidate"]["path"]
        cand = cand if Path(cand).is_absolute() else str(CHECKOUT / cand)
        argv = [self.run.cfg["interpreter"]["path"], "-B", cand, *args]
        row = self.run.call(self.dir, label, argv)
        self.calls.append(row)
        return row


def run_matrix(cfg: dict, cfg_raw: bytes, matrix: str, evidence: Path) -> tuple[int, dict]:
    run = Run(cfg, cfg_raw, matrix, evidence)
    pre = preflight(cfg, matrix)
    (run.dir / "preflight.json").write_bytes(dump(pre))
    if matrix == "real":
        import cases as M
    else:
        import stub_cases as M
    rows = []
    for case in M.CASES:
        cid, title, fn, manual = case["id"], case["title"], case["fn"], case.get("manual")
        if pre["status"] != "READY":
            rows.append({"id": cid, "title": title, "status": "NOT RUN", "reason": f"preflight {pre['status']}"})
            continue
        if manual:
            rows.append({"id": cid, "title": title, "status": "MANUAL", "reason": manual})
            continue
        ctx = Ctx(run, cid)
        try:
            fn(ctx)
            status = "PASS" if ctx.checks and all(c["ok"] for c in ctx.checks) else "FAIL"
            if any(c.get("timed_out") for c in ctx.calls):
                status = "ERROR"
            error = None
        except Exception:  # noqa: BLE001 - every harness or case error is evidence
            status, error = "ERROR", traceback.format_exc()
        (ctx.dir / "checks.json").write_bytes(dump({"checks": ctx.checks, "error": error}))
        rows.append({"id": cid, "title": title, "status": status, "failed_checks": [c["check"] for c in ctx.checks if not c["ok"]],
                     "error": error and error.splitlines()[-1]})
    if pre["status"] == "REFUSED":
        aggregate, code = "REFUSED", 2
    elif pre["status"] == "UNREADY":
        aggregate, code = "UNREADY", 2
    elif any(r["status"] in ("FAIL", "ERROR") for r in rows):
        aggregate, code = "FAIL", 1
    elif any(r["status"] in ("MANUAL", "NOT RUN") for r in rows):
        aggregate, code = "INCOMPLETE", 1
    else:
        aggregate, code = "PASS", 0
    summary = {"schema": "acceptance-run/1", "run": run.name, "matrix": matrix, "kind": cfg.get("kind"),
               "config_sha256": sha(cfg_raw),
               "code_sha256": {n: sha((HERE / n).read_bytes()) for n in ("harness.py", "fixtures.py", "cases.py", "stub_cases.py", "stubs/STUB_loop.py")},
               "command": [sys.executable, "-I", "-B", str(HERE / "harness.py"), "run", "--matrix", matrix],
               "preflight": pre, "aggregate": aggregate, "exit": code,
               "loop_evidence": cfg.get("kind") == "candidate" and pre["status"] == "READY",
               "launches": run.launches, "cases": rows,
               "statement": "execution status of this harness only; not acceptance, review or release"}
    (run.dir / "summary.json").write_bytes(dump(summary))
    table = ["| case | status | detail |", "|---|---|---|"] + [
        f"| {r['id']} | {r['status']} | {r.get('reason') or ', '.join(r.get('failed_checks') or []) or (r.get('error') or '')} |" for r in rows]
    (run.dir / "CASES.md").write_text(f"# {run.name} — {matrix} matrix — aggregate {aggregate}\n\n" + "\n".join(table) + "\n", encoding="utf-8")
    return code, summary


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    sys.path.insert(0, str(HERE))
    try:
        if args[:1] == ["preflight"] and len(args) == 3 and args[1] == "--config":
            cfg, _ = load_config(Path(args[2]))
            pre = preflight(cfg)
            print(json.dumps(pre, indent=2))
            return {"READY": 0}.get(pre["status"], 2)
        if args[:1] == ["run"] and len(args) in (5, 7) and args[1] == "--config" and args[3] == "--matrix" and args[4] in ("real", "stub"):
            evidence = Path(args[6]) if len(args) == 7 and args[5] == "--evidence" else DEFAULT_EVIDENCE
            cfg, raw = load_config(Path(args[2]))
            code, summary = run_matrix(cfg, raw, args[4], evidence)
            print(summary["run"], summary["aggregate"], f"exit {code}")
            return code
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 2
    print(__doc__, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
