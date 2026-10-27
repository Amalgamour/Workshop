"""Fixture demonstration for prime_support.py (0507.prime-support/05.02).

  python -B demo.py --out <new absolute dir outside Git> --workshop-repo D:\\Git\\lib-build --sof-repo D:\\Git\\SoF

Real sources are read only as Git objects at pinned commits (git show, GIT_OPTIONAL_LOCKS=0) and copied into
disposable repositories under --out. No working checkout of either repository is read or written. Every
prime_support.py call is a separate process, and its argv, exit code and stdout are kept in transcript.json.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
TOOL = LAB / "prime_support.py"
EM = "\u2014"
PINNED = {  # (repo key, commit, path) -> sha256
    ("workshop", "d9775fabe705c6a90be9bc770b17289b6b7c7188", "00.kernel/00.00.10.work/0504.app-entry/05.05.md"):
        "56f15524a800dfc6c3cf280fa9d264afc294ec901508d8a5ba20413c1a14ddbf",
    ("workshop", "cf25d56a5356d741b751a6d03a13dfe07a269064", "00.kernel/00.00.10.work/0504.app-entry/05.05.md"):
        "56c4e2c1dfff4bc0214604c7f80f73753ee2368da2829ebf136295f71c9928cd",
    ("workshop", "2c581eb91e32a04883826c1dea48183ab1bf49f4", "00.kernel/00.00.10.work/0504.app-entry/05.05.md"):
        "5a52d9e9905faf2cbb36e4b0d70e701fbab55b63faccb8617ed8e507341c5d6f",
    ("workshop", "54274e698dde1c6cbd5e25177395c62c2a2c645a", "00.kernel/00.00.10.work/0504.app-entry/05.06.md"):
        "8365ec5ebe811d34bb61f81d5ce8b46a212fbf3b1dd334a1a6d81d7607b65805",
    ("workshop", "54274e698dde1c6cbd5e25177395c62c2a2c645a", "00.kernel/00.00.10.work/0401.goal/06.01.md"):
        "1ee161c5497212eccfcc13d6703e94df7b8c05d31e1dae00e978ac321d7978bc",
    ("sof", "01b8fe6b8247c5314c39e2bbc003b85db8840088", "returns/sof-gm-kit-pass01.md"):
        "a99a3893c2608bdd5b8eae260dcea25cefd59a96492ee5c6b196d5f663e44d08",
}
ENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local", GIT_COMMITTER_NAME="fixture",
           GIT_COMMITTER_EMAIL="fixture@local", GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1")
transcript = []


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, env=ENV, check=True).stdout


def pinned_blob(sources, key):
    repo_key, commit, path = key
    data = git(sources[repo_key], "show", f"{commit}:{path}")
    if hashlib.sha256(data).hexdigest() != PINNED[key]:
        sys.exit(f"stop: pinned blob does not match: {repo_key} {commit[:7]} {path}")
    return data


def make_repo(root, name, branch):
    repo = root / name
    repo.mkdir()
    git(repo, "init", "-q", "-b", branch)
    bare = root / f"{name}-origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], env=ENV, check=True, capture_output=True)
    git(repo, "remote", "add", "origin", str(bare))
    return repo


def commit(repo, files, msg, branch, push=True):
    for rel, data in files.items():
        p = repo / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", msg)
    if push:
        git(repo, "push", "-q", "origin", branch)
    return git(repo, "rev-parse", "HEAD").decode().strip()


def tool(step, *args):
    argv = [sys.executable, "-B", str(TOOL), *map(str, args)]
    r = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8", timeout=120)
    transcript.append({"step": step, "argv": argv, "exit": r.returncode, "stdout": r.stdout, "stderr": r.stderr})
    return r.returncode, r.stdout


def status_json(step, reg, store):
    code, out = tool(step, "status", "--registry", reg, "--intake", store, "--json")
    return code, json.loads(out)


def entry(rep, lane, path):
    return next(e for l in rep["lanes"] if l["lane"] == lane for e in l["files"] if e["path"] == path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--workshop-repo", required=True)
    ap.add_argument("--sof-repo", required=True)
    a = ap.parse_args()
    out = Path(a.out)
    if not out.is_absolute() or out.exists():
        sys.exit("stop: --out must be a new absolute directory")
    probe = out.parent
    while probe != probe.parent:
        if (probe / ".git").exists():
            sys.exit("stop: --out must be outside every Git working tree")
        probe = probe.parent
    out.mkdir(parents=True)
    sources = {"workshop": a.workshop_repo, "sof": a.sof_repo}
    checks = []

    def expect(name, cond, detail=""):
        checks.append({"check": name, "ok": bool(cond), "detail": detail})

    # A. real shapes: three revisions of 0504/05.05, 05.06 and the canonical record, plus the SoF return file
    app_page = "00.kernel/00.00.10.work/0504.app-entry/05.05.md"
    canon = "00.kernel/00.00.10.work/0401.goal/06.01.md"
    ws = make_repo(out, "workshop", "workshop")
    keys = list(PINNED)
    commit(ws, {app_page: pinned_blob(sources, keys[0]), keys[3][2]: pinned_blob(sources, keys[3]),
                canon: pinned_blob(sources, keys[4])}, "d9775fa shape", "workshop")
    commit(ws, {app_page: pinned_blob(sources, keys[1])}, "cf25d56 shape", "workshop")
    commit(ws, {app_page: pinned_blob(sources, keys[2])}, "2c581eb shape", "workshop")
    sof = make_repo(out, "sof", "sof/gm-kit")
    sof_path = "returns/sof-gm-kit-pass01.md"
    commit(sof, {sof_path: pinned_blob(sources, keys[5])}, "01b8fe6 shape", "sof/gm-kit")
    reg = out / "registry-real.json"
    reg.write_text(json.dumps({
        "schema": "prime-support-registry", "version": 1,
        "repositories": {
            "workshop": {"local": str(ws), "branch": "workshop", "remote_ref": "refs/remotes/origin/workshop",
                         "worktree": "registered-paths", "history_limit": 50},
            "sof": {"local": str(sof), "branch": "sof/gm-kit", "remote_ref": "refs/remotes/origin/sof/gm-kit",
                    "worktree": "off", "history_limit": 50}},
        "canonical_assignment": {"repository": "workshop", "path": canon, "lane": "app"},
        "lanes": [
            {"lane": "app", "project": "workshop", "owner_label": "Grok Builder 1", "repository": "workshop",
             "pages": ["00.kernel/00.00.10.work/0504.app-entry"], "return_files": [], "review_sources": []},
            {"lane": "sof", "project": "SoF (separate repository)", "owner_label": "SoF builder", "repository": "sof",
             "pages": [], "return_files": [sof_path], "review_sources": []}]}, indent=1), encoding="utf-8")
    store = out / "intake-store"
    tool("A1 status text", "status", "--registry", reg, "--intake", store)
    code, rep = status_json("A2 status json", reg, store)
    app = entry(rep, "app", app_page)
    rev = app["revisions"][0]
    expect("05.05 has one current revision (published = local = worktree)", len({r["revision_id"] for r in app["revisions"]}) == 1)
    expect("05.05 legacy whole-hash review binds through history", rev["review"] == "reviewed", rev.get("review_source"))
    expect("05.05 disposition shown verbatim", (rev.get("disposition") or "").startswith("REPAIR REQUIRED"), rev.get("disposition"))
    expect("05.05 amended revision supersedes the first", rev["supersedes"] is not None)
    expect("05.05 execution unknown (legacy)", rev["execution"] == "unknown")
    s06 = entry(rep, "app", keys[3][2])["revisions"][0]
    expect("05.06 return is PENDING, not eligible", (s06["execution"], s06["eligible"]) == ("pending", False))
    sofrev = entry(rep, "sof", sof_path)["revisions"]
    expect("SoF return-file eligible, execution and review unknown/needed",
           all((r["execution"], r["review"], r["eligible"]) == ("unknown", "review-needed", True) for r in sofrev))
    expect("SoF worktree not read (worktree off)", [r["label"] for r in sofrev] == ["published", "local"])
    expect("findings not machine-readable on real pages", rep["lanes"][0]["findings"] == {})
    expect("canonical waiting for 05.06 with no return: no canonical conflict", not rep["conflicts"], rep["conflicts"])
    tool("A3 intake scan", "intake", "scan", "--registry", reg, "--intake", store)
    c1, o1 = tool("A4 ack SoF return", "intake", "ack", "--registry", reg, "--intake", store, "--lane", "sof",
                  "--path", sof_path, "--revision", sofrev[0]["revision_id"], "--as", "codex-prime")
    c2, o2 = tool("A5 ack SoF again (idempotent)", "intake", "ack", "--registry", reg, "--intake", store, "--lane", "sof",
                  "--path", sof_path, "--revision", sofrev[0]["revision_id"], "--as", "codex-prime")
    expect("ack then idempotent re-ack", c1 == 0 and "seen" in o1 and c2 == 0 and "already-recorded" in o2)
    code, rep = status_json("A6 status after ack", reg, store)
    expect("SoF now seen, still review-needed, nothing accepted",
           all(r["intake"] == "seen" and r["review"] == "review-needed" for r in entry(rep, "sof", sof_path)["revisions"]))
    tool("A7 intake show", "intake", "show", "--intake", store)

    # B. synthetic walk: unseen -> seen -> reviewed -> amended with the old Review removed; SY-01 carried
    page = "00.kernel/00.00.10.work/0599.synthetic-lane/05.01.md"
    head = (f"# 05 {EM} SYNTHETIC batch\nstate: draft; awaiting Director release\n\n## Assignment\nRelease: SYNTHETIC.\n\n"
            f"## Return {EM} synthetic-builder\nexecution: returned\nDid: wrote out.txt.\n")
    syn = make_repo(out, "synthetic", "main")
    commit(syn, {page: (head + f"\n## Review {EM} Codex Prime\nPENDING.\n").encode()}, "v1 returned", "main")
    reg2 = out / "registry-synthetic.json"
    reg2.write_text(json.dumps({
        "schema": "prime-support-registry", "version": 1,
        "repositories": {"syn": {"local": str(syn), "branch": "main", "remote_ref": "refs/remotes/origin/main",
                                 "worktree": "registered-paths", "history_limit": 50}},
        "lanes": [{"lane": "synthetic", "project": "workshop (SYNTHETIC)", "owner_label": "synthetic-builder",
                   "repository": "syn", "pages": ["00.kernel/00.00.10.work/0599.synthetic-lane"], "return_files": [],
                   "review_sources": []}]}, indent=1), encoding="utf-8")
    store2 = out / "intake-store-synthetic"
    code, rep = status_json("B1 unseen", reg2, store2)
    r1 = entry(rep, "synthetic", page)["revisions"][0]
    expect("B1 unseen and review-needed", (r1["intake"], r1["review"]) == ("unseen", "review-needed"))
    v1 = r1["revision_id"]
    tool("B2 ack v1", "intake", "ack", "--registry", reg2, "--intake", store2, "--lane", "synthetic", "--path", page,
         "--revision", v1, "--as", "codex-prime")
    code, rep = status_json("B3 seen", reg2, store2)
    expect("B3 seen", entry(rep, "synthetic", page)["revisions"][0]["intake"] == "seen")
    commit(syn, {page: (head + f"\n## Review {EM} Codex Prime\nreviewed_return_prefix: {v1}\n"
                               "Disposition: REPAIR REQUIRED, SY-01.\nfindings: SY-01=unresolved\n").encode()}, "review", "main")
    code, rep = status_json("B4 reviewed", reg2, store2)
    r4 = entry(rep, "synthetic", page)["revisions"][0]
    expect("B4 same revision, reviewed, not re-queued", (r4["revision_id"], r4["review"], r4["intake"]) == (v1, "reviewed", "seen"))
    commit(syn, {page: (head + "Amendment: out.txt ends with a newline (answers SY-01).\n").encode()}, "amend, old Review removed", "main")
    code, rep = status_json("B5 amended", reg2, store2)
    r5 = entry(rep, "synthetic", page)["revisions"][0]
    f5 = rep["lanes"][0]["findings"]
    expect("B5 new revision, unseen, stale review, supersedes v1",
           r5["revision_id"] != v1 and (r5["intake"], r5["review"], r5["supersedes"]) == ("unseen", "stale-review", v1))
    expect("B5 SY-01 still open from history", f5.get("SY-01", {}).get("state") == "open", json.dumps(f5))
    for p in sorted(store2.rglob("*"), reverse=True):
        p.unlink() if p.is_file() else p.rmdir()
    store2.rmdir()
    code, rep = status_json("B6 acknowledgements lost", reg2, store2)
    expect("B6 ack loss: v2 unseen, SY-01 still open, nothing accepted",
           rep["lanes"][0]["findings"].get("SY-01", {}).get("state") == "open"
           and "accepted" not in json.dumps(rep).replace("not accepted", ""))
    tool("B7 status text", "status", "--registry", reg2, "--intake", store2)

    (out / "transcript.json").write_text(json.dumps(transcript, indent=1), encoding="utf-8")
    (out / "checks.json").write_text(json.dumps(checks, indent=1), encoding="utf-8")
    failed = [c for c in checks if not c["ok"]]
    for c in checks:
        print(("ok   " if c["ok"] else "FAIL ") + c["check"])
    print(f"processes {len(transcript)}  checks {len(checks)}  failed {len(failed)}")
    print("demo ok" if not failed else "demo FAILED")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
