"""PROTOCOL TEST WORKER. Not a model. Reads one request on stdin, reads its named input, writes one artifact,
prints one result. Its behaviour is chosen only by the allowlisted --mode argument of its profile.

Task (fixed): count the input's lines that contain a non-whitespace character; write {"count": N} to
result.json in the output root.
"""
import argparse, hashlib, json, os, sys, time
from pathlib import Path, PurePosixPath


def canonical(v):
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", required=True, choices=["ok", "crash", "sleep", "garbage", "partial", "flood", "wrong-id",
                                                       "missing-artifact", "bad-hash", "escape", "bad-shape",
                                                       "no-stdin-reader", "flood-stderr", "dup-keys"])
    mode = ap.parse_args().mode
    if mode == "no-stdin-reader":   # never reads stdin; exits by itself after 10 s so a regression cannot hang a suite
        with open("launches.log", "a", encoding="utf-8") as f:   # its working directory is the output root
            f.write("(stdin not read) no-stdin-reader\n")
        time.sleep(10)
        return
    env = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    req_sha = hashlib.sha256(canonical(env)).hexdigest()
    with open(Path(env["output_root"]) / "launches.log", "a", encoding="utf-8") as f:   # lets tests count real launches
        f.write(f"{env['delivery_id']} {mode}\n")
    if mode == "crash":
        sys.stderr.write("fixture: simulated crash\n")
        sys.exit(3)
    if mode == "sleep":
        Path(env["output_root"], "started.marker").write_text("work started before the timeout\n", encoding="utf-8")
        time.sleep(30)
    if mode == "flood-stderr":
        sys.stderr.write("e" * 5_000_000)
        sys.stderr.flush()
        return
    if mode == "flood":
        sys.stdout.write("x" * 5_000_000)
        sys.stdout.flush()
        return
    if mode == "garbage":
        sys.stdout.write("this is not json")
        return
    if mode == "partial":
        sys.stdout.write('{"schema": "worker-bridge/result@1", "delivery_id": ')
        return
    inp = env["inputs"][0]
    data = (Path(env["input_root"]) / PurePosixPath(inp["path"])).read_bytes()
    count = sum(1 for line in data.decode("utf-8").splitlines() if line.strip())
    out = canonical({"count": count})
    rel = "result.json"
    if mode == "escape":
        rel = "../escaped.json"
        (Path(env["output_root"]) / rel).write_bytes(out)
    elif mode != "missing-artifact":
        (Path(env["output_root"]) / rel).write_bytes(out)
    art = {"path": rel, "sha256": hashlib.sha256(out).hexdigest(), "bytes": len(out)}
    if mode == "bad-hash":
        art["sha256"] = "0" * 64
    res = {"schema": "worker-bridge/result@1", "delivery_id": env["delivery_id"], "job_id": env["job_id"],
           "request_sha256": req_sha, "outcome": "done", "artifacts": [art], "diagnostics": f"fixture mode {mode}: counted {count}"}
    if mode == "wrong-id":
        res["delivery_id"] = "someone-else"
    if mode == "bad-shape":
        res["outcome"] = "approved"
    if mode == "dup-keys":   # the same key twice: Python would keep the last; the strict reader refuses
        sys.stdout.write(json.dumps(res)[:-1] + ', "outcome": "failed"}')
        return
    sys.stdout.write(json.dumps(res))


if __name__ == "__main__":
    main()
