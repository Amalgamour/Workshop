"""Manual custody and artifact check for one case (run 01/04 manual condition): plain hashing, no Prime assistance tool.
usage: python -B custody_check.py MEMBER_DIR PAGE_POINTER_RECEIPT_SHA [ARTIFACT_MANIFEST]   (cwd = disposable repository)"""
import hashlib, json, re, sys
from pathlib import Path

sha = lambda b: hashlib.sha256(b).hexdigest()
mem = Path(sys.argv[1]); want_receipt = sys.argv[2]
out = {"member": str(mem)}
rb = (mem / "receipt.json").read_bytes()
out["receipt_sha256"] = sha(rb); out["receipt_matches_page_pointer"] = sha(rb) == want_receipt
rec = json.loads(rb)
mb = (mem / "manifest.json").read_bytes()
man = json.loads(mb)
out["manifest_sha256"] = sha(mb)
out["receipt_keys"] = sorted(rec)
out["receipt_names_manifest"] = [k for k, v in rec.items() if v == sha(mb)]
rows = man.get("artifacts") or man.get("payloads") or man.get("files") or []
out["manifest_keys"] = sorted(man)
checks = []
for r in rows:
    blob = mem / "payload" / Path(r.get("blob") or r.get("payload") or "").name if (r.get("blob") or r.get("payload")) else None
    got = sha(blob.read_bytes()) if blob and blob.is_file() else None
    src = r.get("source") or r.get("path") or r.get("logical_path")
    live = Path(src) if src else None
    live_sha = sha(live.read_bytes()) if live and live.is_file() else None
    checks.append({"row": {k: r[k] for k in r if k in ("source", "path", "logical_path", "blob", "payload", "sha256", "bytes")},
                   "blob_sha256": got, "blob_matches_row": got == r.get("sha256"), "repo_file_sha256": live_sha,
                   "repo_matches_row": live_sha == r.get("sha256")})
out["payload_checks"] = checks
ret = (mem / "return.md").read_text(encoding="utf-8")
declared = re.findall(r"^- (\S+?): ([0-9a-f]{64}), (\d+)", ret, re.M) + [(p, h, None) for p, h in re.findall(r"^- (\S+) \(not captured[^)]*\): ([0-9a-f]{64})", ret, re.M)]
out["declared_outputs"] = [{"path": p, "declared": h, "actual": sha(Path(p).read_bytes()) if Path(p).is_file() else None,
                            "match": Path(p).is_file() and sha(Path(p).read_bytes()) == h} for p, h, _ in declared]
if len(sys.argv) > 3:
    am = json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
    arts = am.get("artifacts") or am.get("files") or []
    res = []
    for a in arts:
        p = Path(a["path"])
        res.append({"path": a["path"], "match": p.is_file() and sha(p.read_bytes()) == a["sha256"], "present": p.is_file()})
    out["artifact_manifest"] = {"rows": len(res), "match": sum(r["match"] for r in res), "missing": [r["path"] for r in res if not r["present"]],
                                "mismatch": [r["path"] for r in res if r["present"] and not r["match"]]}
print(json.dumps(out, indent=1))
