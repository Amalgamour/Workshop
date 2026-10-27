"""Adapter interface and the one implemented backend: a configured local worker process.

The adapter carries one released request to one allowlisted backend profile and returns a receipt. It never
picks a route, invents a job, retries on its own, approves work or touches book state.
"""
import json, os, subprocess, sys, threading, time
from pathlib import Path
from .canon import canonical, sha256, sha256_file, write_atomic, write_exclusive
from .envelope import EnvelopeError, request_sha256, validate
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


def _read_capped(stream, cap, out, flag):
    """Read a stream to EOF, keeping at most cap bytes; set flag if more arrived."""
    buf = bytearray()
    while True:
        chunk = stream.read(65536)
        if not chunk:
            break
        room = cap - len(buf)
        if room > 0:
            buf += chunk[:room]
        if len(chunk) > max(room, 0):
            flag.set()
            break
    out.append(bytes(buf))


class LocalProcessAdapter(Adapter):
    def __init__(self, store, profiles, lab_root):
        """store: folder for per-delivery records. profiles: {name: {"kind", "argv"}}; argv[0] may be
        "{python}" for this interpreter. lab_root: profiles' relative paths resolve against it."""
        self.store = Path(store)
        self.profiles = profiles
        self.lab_root = Path(lab_root)

    # ---------- persistence ----------
    def _dir(self, delivery_id):
        return self.store / delivery_id

    def status(self, delivery_id):
        d = self._dir(delivery_id)
        if (d / "receipt.json").is_file():
            return json.loads((d / "receipt.json").read_bytes())
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
        d = self._dir(env["delivery_id"])
        d.mkdir(parents=True, exist_ok=True)
        req_bytes = canonical(env)
        rq = d / "request.json"
        if rq.is_file():
            if rq.read_bytes() != req_bytes:
                return self._refusal(env, req_sha, "delivery_id reused with a different request; use a new delivery_id")
        else:
            write_atomic(rq, req_bytes)
        if (d / "receipt.json").is_file():
            rec = json.loads((d / "receipt.json").read_bytes())
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
        try:
            proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False,
                                    cwd=str(Path(env["output_root"])))
        except OSError as e:
            transport, rc, out, err, over = "launch-failed", None, b"", str(e).encode(), False
        else:
            outs, errs, ofl, efl = [], [], threading.Event(), threading.Event()
            th = [threading.Thread(target=_read_capped, args=(proc.stdout, lim["max_stdout_bytes"], outs, ofl), daemon=True),
                  threading.Thread(target=_read_capped, args=(proc.stderr, lim["max_stderr_bytes"], errs, efl), daemon=True)]
            for t in th:
                t.start()
            try:
                proc.stdin.write(req_bytes)
                proc.stdin.close()
            except OSError:
                pass
            timed_out, over = False, False
            deadline = t0 + lim["timeout_s"]
            while proc.poll() is None:
                if ofl.is_set() or efl.is_set():
                    over = True
                    proc.kill()
                    break
                if time.monotonic() > deadline:
                    timed_out = True
                    proc.kill()
                    break
                time.sleep(0.02)
            proc.wait()
            for t in th:
                t.join(timeout=5)
            for s in (proc.stdout, proc.stderr):   # close the parent's pipe handles (run 01 leaked them)
                try:
                    s.close()
                except OSError:
                    pass
            out, err = (outs[0] if outs else b""), (errs[0] if errs else b"")
            over = over or ofl.is_set() or efl.is_set()
            rc = proc.returncode
            transport = "timeout" if timed_out else "output-limit" if over else "crashed" if rc != 0 else "delivered"
        dur = round(time.monotonic() - t0, 3)
        (att / "stdout.bin").write_bytes(out)
        (att / "stderr.bin").write_bytes(err)
        write_atomic(att / "exit.json", canonical({"returncode": rc, "duration_s": dur, "transport": transport}))
        if _test_crash_before_receipt:
            raise StoreError("simulated crash after the process, before the receipt")
        rec = self._receipt(env, req_sha, prof, out, err, rc, dur, transport)
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
        d = self._dir(delivery_id)
        if (d / "receipt.json").is_file():
            return json.loads((d / "receipt.json").read_bytes())
        need = [d / "request.json", d / "launch.json", d / "attempt" / "exit.json", d / "attempt" / "stdout.bin", d / "attempt" / "stderr.bin"]
        if not all(x.is_file() for x in need):
            return {**self.status(delivery_id), "transport": "uncertain", "recovered": False,
                    "reason": "the attempt was not fully recorded; outcome unknown; not relaunched"}
        env = json.loads((d / "request.json").read_bytes())
        launch = json.loads((d / "launch.json").read_bytes())
        ex = json.loads((d / "attempt" / "exit.json").read_bytes())
        req_sha = request_sha256(env)
        if launch["request_sha256"] != req_sha:
            raise StoreError("the stored request does not match its launch record")
        prof = self.profiles.get(launch["profile"], {"kind": launch["kind"]})
        rec = self._receipt(env, req_sha, prof, (d / "attempt" / "stdout.bin").read_bytes(), (d / "attempt" / "stderr.bin").read_bytes(),
                            ex["returncode"], ex["duration_s"], ex["transport"])
        rec["recovered"] = True
        write_atomic(d / "receipt.json", canonical(rec))
        return rec
