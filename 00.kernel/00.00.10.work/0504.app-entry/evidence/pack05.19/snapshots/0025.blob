"""Adapter interface and the one implemented backend: a configured local worker process.

The adapter carries one released request to one allowlisted backend profile and returns a receipt. It never
picks a route, invents a job, retries on its own, approves work or touches book state.
"""
import json, os, subprocess, sys, threading, time
from pathlib import Path
from .canon import canonical, sha256, sha256_file, strict_loads, write_atomic, write_exclusive
from .envelope import EnvelopeError, request_sha256, validate
from .ids import IdentityError, store_dir
from . import verify

RECEIPT_SCHEMA = "worker-bridge/receipt@1"


class Adapter:
    """deliver(envelope) -> receipt; status(delivery_id) -> receipt or state. Backends implement _run."""

    def deliver(self, env):
        raise NotImplementedError

    def status(self, delivery_id):
        raise NotImplementedError


class StoreError(Exception):
    pass


class _Capture:
    """One output stream's capture, owned by its reader thread (05.03, BR-01b).

    The reader thread is the only code that reads or closes the stream. The adapter never closes a pipe a reader
    may still be blocked on: on Windows that close waits for the reader's buffered-stream lock, and so for
    whichever process holds the other end (the 5.078 s blockage in Prime review BR-01b). At the end of the
    adapter's budget it calls snapshot(), which freezes what was captured; bytes that arrive later are counted and
    dropped, never added to the result. The reader keeps draining to EOF so a descendant writing to the pipe is not
    blocked by a full pipe, then closes the stream itself."""

    def __init__(self, cap):
        self.cap = cap
        self.buf = bytearray()
        self.lock = threading.Lock()
        self.frozen = False
        self.late_bytes = 0
        self.over = threading.Event()
        self.eof = threading.Event()
        self.error = None

    def feed(self, chunk):
        with self.lock:
            if self.frozen:
                self.late_bytes += len(chunk)
                return
            room = self.cap - len(self.buf)
            if room > 0:
                self.buf += chunk[:room]
            if len(chunk) > max(room, 0):
                self.over.set()

    def snapshot(self):
        with self.lock:
            self.frozen = True
            return bytes(self.buf)


def _reader(stream, capture):
    """Drain an unbuffered pipe to EOF into its capture, then close it. Runs in its own daemon thread."""
    try:
        while True:
            chunk = stream.read(65536)
            if not chunk:
                break
            capture.feed(chunk)
    except (OSError, ValueError) as e:
        capture.error = type(e).__name__
    finally:
        try:
            stream.close()
        except (OSError, ValueError):
            pass
        capture.eof.set()


CLEANUP_ALLOWANCE_S = 2.0   # after the deadline: time allowed to kill the child, reap it and let the I/O threads finish


def _write_stdin(stream, data, done, errors):
    """Write the whole request to an unbuffered pipe and close it, in its own thread, so a child that never reads
    cannot block the adapter past the deadline (05.02 #01, BR-01). This thread is the only owner of stdin."""
    try:
        view = memoryview(data)
        while view:
            n = stream.write(view)
            if not n:
                raise OSError("stdin accepted no bytes")
            view = view[n:]
    except (OSError, ValueError) as e:
        errors.append(f"stdin: {type(e).__name__}")
    finally:
        try:
            stream.close()
        except (OSError, ValueError):
            pass
        done.set()


def _execute(argv, cwd, req_bytes, lim, t0):
    """Run one child under ONE deadline (t0 + timeout_s) that covers writing stdin, reading stdout and stderr to
    EOF, and the child's exit. On overrun or an output cap the direct child is killed. Then at most
    CLEANUP_ALLOWANCE_S more is spent reaping it and letting the three I/O threads finish. After that the adapter
    RETURNS: it never closes, joins or waits on a stream that a thread still owns. A thread still running (for
    example on a pipe that a descendant inherited) is named in cleanup.retained; it finishes and closes its own
    stream when the other end closes, or when this interpreter exits (daemon thread). Output captured up to
    that point is a frozen snapshot; anything later is dropped. A bounded best effort, not a real-time guarantee;
    only the direct child is killed."""
    cleanup = {"allowance_s": CLEANUP_ALLOWANCE_S, "complete": True, "notes": [], "retained": []}
    try:
        proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, cwd=cwd,
                                bufsize=0)
    except OSError as e:
        return {"transport": "launch-failed", "returncode": None, "stdout": b"", "stderr": str(e).encode(), "cleanup": cleanup}
    cout, cerr = _Capture(lim["max_stdout_bytes"]), _Capture(lim["max_stderr_bytes"])
    wdone, werr = threading.Event(), []
    th = [("stdout reader", threading.Thread(target=_reader, args=(proc.stdout, cout), daemon=True, name="bridge-stdout-reader")),
          ("stderr reader", threading.Thread(target=_reader, args=(proc.stderr, cerr), daemon=True, name="bridge-stderr-reader")),
          ("stdin writer", threading.Thread(target=_write_stdin, args=(proc.stdin, req_bytes, wdone, werr), daemon=True,
                                            name="bridge-stdin-writer"))]
    for _, t in th:
        t.start()
    deadline = t0 + lim["timeout_s"]
    timed_out = over = False
    while True:
        if cout.over.is_set() or cerr.over.is_set():
            over = True
            break
        if proc.poll() is not None and wdone.is_set() and cout.eof.is_set() and cerr.eof.is_set():
            break
        if time.monotonic() >= deadline:
            timed_out = proc.poll() is None or not wdone.is_set()
            break
        time.sleep(0.01)
    if (over or timed_out) and proc.poll() is None:
        try:
            proc.kill()
        except OSError as e:
            cleanup["notes"].append(f"kill: {type(e).__name__}")
    end = time.monotonic() + CLEANUP_ALLOWANCE_S
    try:
        proc.wait(timeout=max(0.0, end - time.monotonic()))
    except subprocess.TimeoutExpired:
        cleanup["complete"] = False
        cleanup["notes"].append("the direct child had not exited within the cleanup allowance")
    for name, t in th:
        t.join(timeout=max(0.0, end - time.monotonic()))
        if t.is_alive():
            cleanup["complete"] = False
            cleanup["retained"].append(name)
            cleanup["notes"].append(f"{name} still owns its pipe after the cleanup allowance (a descendant may hold the other end); "
                                    "left to finish and close it on its own")
    out, err = cout.snapshot(), cerr.snapshot()   # frozen now: later bytes are counted on the capture and dropped
    cleanup["notes"] += werr + [f"{n}: {c.error}" for n, c in (("stdout reader", cout), ("stderr reader", cerr)) if c.error]
    over = over or cout.over.is_set() or cerr.over.is_set()
    rc = proc.returncode
    streams_open = not (cout.eof.is_set() and cerr.eof.is_set())
    if timed_out:
        transport = "timeout"
    elif over:
        transport = "output-limit"
    elif rc not in (0, None):
        transport = "crashed"
    elif rc is None or streams_open or not wdone.is_set():
        transport = "incomplete-output"   # the child ended, but its output was not complete within the budget
    else:
        transport = "delivered"
    return {"transport": transport, "returncode": rc, "stdout": out, "stderr": err, "cleanup": cleanup}


class LocalProcessAdapter(Adapter):
    def __init__(self, store, profiles, lab_root):
        """store: folder for per-delivery records. profiles: {name: {"kind", "argv"}}; argv[0] may be
        "{python}" for this interpreter. lab_root: profiles' relative paths resolve against it."""
        self.store = Path(store)
        self.profiles = profiles
        self.lab_root = Path(lab_root)

    # ---------- persistence ----------
    def _dir(self, delivery_id):
        """Every entry point (deliver, status, recover, and the CLI through them) gets its folder here: the
        shared identity rules and resolved containment in the store (05.02 #02)."""
        return store_dir(self.store, delivery_id)

    @staticmethod
    def _id_refusal(delivery_id, e):
        return {"delivery_id": delivery_id if isinstance(delivery_id, str) else None, "state": "refused", "transport": "refused",
                "reason": f"delivery_id: {e}", "launched": False, "review": "not performed"}

    def status(self, delivery_id):
        try:
            d = self._dir(delivery_id)
        except IdentityError as e:
            return self._id_refusal(delivery_id, e)
        if (d / "receipt.json").is_file():
            return strict_loads((d / "receipt.json").read_bytes())
        if (d / "launch.json").is_file():
            return {"delivery_id": delivery_id, "state": "uncertain",
                    "reason": "launched, no receipt: the earlier attempt's outcome is unknown; not relaunched"}
        if (d / "request.json").is_file():
            return {"delivery_id": delivery_id, "state": "accepted-not-launched"}
        return {"delivery_id": delivery_id, "state": "unknown"}

    def _refusal(self, env, req_sha, reason):
        return {"schema": RECEIPT_SCHEMA, "delivery_id": env.get("delivery_id") if isinstance(env, dict) else None,
                "job_id": env.get("job_id") if isinstance(env, dict) else None, "request_sha256": req_sha,
                "transport": "refused", "reason": reason, "launched": False, "review": "not performed"}

    # ---------- deliver ----------
    def deliver(self, env, _test_crash_before_receipt=False, _test_crash_in_receipt=False):
        try:
            req_sha = validate(env)
        except EnvelopeError as e:
            return self._refusal(env, None, f"envelope: {e}")
        prof = self.profiles.get(env["backend"])
        if prof is None:
            return self._refusal(env, req_sha, f"backend {env['backend']!r} is not an allowlisted profile")
        try:
            d = self._dir(env["delivery_id"])
        except IdentityError as e:
            return self._refusal(env, req_sha, f"delivery_id: {e}")
        d.mkdir(parents=True, exist_ok=True)
        req_bytes = canonical(env)
        rq = d / "request.json"
        if rq.is_file():
            if rq.read_bytes() != req_bytes:
                return self._refusal(env, req_sha, "delivery_id reused with a different request; use a new delivery_id")
        else:
            write_atomic(rq, req_bytes)
        if (d / "receipt.json").is_file():
            rec = strict_loads((d / "receipt.json").read_bytes())
            rec["replayed"] = True          # the same request again: nothing is relaunched or applied twice
            return rec
        if (d / "launch.json").exists():
            return {**self.status(env["delivery_id"]), "request_sha256": req_sha, "transport": "uncertain", "launched": True,
                    "review": "not performed"}
        argv = [sys.executable if a == "{python}" else (str((self.lab_root / a).resolve()) if a.endswith(".py") else a) for a in prof["argv"]]
        launch = {"delivery_id": env["delivery_id"], "request_sha256": req_sha, "profile": env["backend"], "kind": prof["kind"],
                  "argv": argv, "launched_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
        try:
            write_exclusive(d / "launch.json", canonical(launch))   # before the process starts; a second launcher fails here
        except FileExistsError:
            return {**self.status(env["delivery_id"]), "transport": "uncertain", "launched": True, "review": "not performed"}
        att = d / "attempt"
        att.mkdir(exist_ok=True)
        lim = env["limits"]
        t0 = time.monotonic()
        x = _execute(argv, str(Path(env["output_root"])), req_bytes, lim, t0)
        transport, rc, out, err = x["transport"], x["returncode"], x["stdout"], x["stderr"]
        dur = round(time.monotonic() - t0, 3)
        (att / "stdout.bin").write_bytes(out)
        (att / "stderr.bin").write_bytes(err)
        write_atomic(att / "exit.json", canonical({"returncode": rc, "duration_s": dur, "transport": transport, "cleanup": x["cleanup"]}))
        if _test_crash_before_receipt:
            raise StoreError("simulated crash after the process, before the receipt")
        rec = self._receipt(env, req_sha, prof, out, err, rc, dur, transport)
        rec["cleanup"] = x["cleanup"]
        write_atomic(d / "receipt.json", canonical(rec), fail_before_replace=_test_crash_in_receipt)
        return rec

    def _receipt(self, env, req_sha, prof, out, err, rc, dur, transport):
        rec = {"schema": RECEIPT_SCHEMA, "delivery_id": env["delivery_id"], "job_id": env["job_id"], "request_sha256": req_sha,
               "backend": env["backend"], "worker_kind": prof["kind"], "launched": True, "returncode": rc, "duration_s": dur,
               "diagnostics": {"stdout": {"path": "attempt/stdout.bin", "sha256": sha256(out), "bytes": len(out)},
                               "stderr": {"path": "attempt/stderr.bin", "sha256": sha256(err), "bytes": len(err)}},
               "review": "not performed"}
        if transport in ("timeout", "output-limit"):
            rec.update(transport=transport, outcome_uncertain=True, claimed_outcome=None, collection="not attempted",
                       reason="killed after launch; work may or may not have happened; not relaunched")
        elif transport == "incomplete-output":
            rec.update(transport=transport, outcome_uncertain=True, claimed_outcome=None, collection="not attempted",
                       reason="the child exited but its output streams were still open when the budget ended "
                              "(a descendant may hold them); the captured bytes are a partial snapshot and are not parsed")
        elif transport in ("launch-failed", "crashed"):
            rec.update(transport=transport, outcome_uncertain=transport == "crashed", claimed_outcome=None, collection="not attempted",
                       reason=f"exit {rc}" if transport == "crashed" else "the process did not start")
        else:
            res, why = verify.parse(out)
            if res is None:
                rec.update(transport="malformed", outcome_uncertain=True, claimed_outcome=None, collection="not attempted", reason=why)
            else:
                mism = verify.correlate(res, env, req_sha)
                if mism:
                    rec.update(transport="malformed", outcome_uncertain=True, claimed_outcome=res["outcome"], collection="not attempted",
                               reason="result does not correlate: " + "; ".join(mism))
                else:
                    ok, bad = verify.collect(res, env["output_root"])
                    rec.update(transport="delivered", outcome_uncertain=False, claimed_outcome=res["outcome"], artifacts=ok,
                               collection="collected" if not bad else "uncollected", reason="; ".join(bad) or None)
        return rec

    def recover(self, delivery_id):
        """Rebuild a missing receipt from the recorded attempt, without relaunching. Only possible when the
        attempt finished and its exit record exists; otherwise the delivery stays uncertain."""
        try:
            d = self._dir(delivery_id)
        except IdentityError as e:
            return {**self._id_refusal(delivery_id, e), "recovered": False}
        if (d / "receipt.json").is_file():
            return strict_loads((d / "receipt.json").read_bytes())
        need = [d / "request.json", d / "launch.json", d / "attempt" / "exit.json", d / "attempt" / "stdout.bin", d / "attempt" / "stderr.bin"]
        if not all(x.is_file() for x in need):
            return {**self.status(delivery_id), "transport": "uncertain", "recovered": False,
                    "reason": "the attempt was not fully recorded; outcome unknown; not relaunched"}
        env = strict_loads((d / "request.json").read_bytes())
        launch = strict_loads((d / "launch.json").read_bytes())
        ex = strict_loads((d / "attempt" / "exit.json").read_bytes())
        req_sha = request_sha256(env)
        if launch["request_sha256"] != req_sha:
            raise StoreError("the stored request does not match its launch record")
        prof = self.profiles.get(launch["profile"], {"kind": launch["kind"]})
        rec = self._receipt(env, req_sha, prof, (d / "attempt" / "stdout.bin").read_bytes(), (d / "attempt" / "stderr.bin").read_bytes(),
                            ex["returncode"], ex["duration_s"], ex["transport"])
        rec["recovered"] = True
        rec["cleanup"] = ex.get("cleanup")
        write_atomic(d / "receipt.json", canonical(rec))
        return rec
