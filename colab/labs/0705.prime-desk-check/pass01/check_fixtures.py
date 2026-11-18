"""Shape and pin checker for the 0705/05.01 declarative oracle (cases.json). Standard library only.

  python -I -B check_fixtures.py --cases ABS --manifest ABS

Checks only the fixture file: exact keys, unique ids, required topics covered, and that every
cited source path and sha256 equals a row in the frozen pack manifest and its snapshot bytes.
It does not run any desk tool, read live pages, or judge whether an expected fact is true.
Exit 0 ok, 1 findings, 2 refused input.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

CASE_KEYS = {"id", "topic", "kind", "sources", "setup", "expected", "forbidden", "evidence_required", "finish"}
EXPECTED_KEYS = {"facts", "unknowns", "attention", "refusals"}
REQUIRED_TOPICS = [
    "stale selector", "two parallel assignments", "wrong instance, same address",
    "unreviewed return versus completed review", "Director words versus interpretation", "missing receipt",
    "unresolved hold and unrelated work", "unregistered Observer sources", "supplied worker activity",
    "long history and overview overflow", "absent dependency", "quoted commands in discussion",
    "changed source hash", "model or process restart",
]


def strict(path: Path):
    def pairs(items):
        keys = [k for k, _ in items]
        if len(keys) != len(set(keys)):
            raise ValueError(f"{path.name}: duplicate key")
        return dict(items)
    return json.loads(path.read_bytes().decode("utf-8"), object_pairs_hook=pairs)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--manifest", required=True)
    a = ap.parse_args(argv)
    try:
        doc = strict(Path(a.cases))
        man_path = Path(a.manifest)
        man = strict(man_path)
    except (OSError, ValueError, UnicodeDecodeError) as e:
        print(f"refused: {e}", file=sys.stderr)
        return 2
    pins = {}
    for row in man["sources"]:
        snap = (man_path.parent / row["snapshot"]).read_bytes()
        pins[row["path"]] = (row["sha256"], hashlib.sha256(snap).hexdigest() == row["sha256"] and len(snap) == row["bytes"])
    findings = []
    ids = set()
    for c in doc.get("cases", []):
        cid = c.get("id")
        if set(c) != CASE_KEYS:
            findings.append(f"{cid}: keys {sorted(set(c) ^ CASE_KEYS)}")
            continue
        if cid in ids:
            findings.append(f"{cid}: duplicate id")
        ids.add(cid)
        if c["kind"] not in ("real-frozen", "synthetic"):
            findings.append(f"{cid}: kind {c['kind']}")
        if set(c["expected"]) != EXPECTED_KEYS:
            findings.append(f"{cid}: expected keys")
        if not c["forbidden"] or not c["evidence_required"] or not c["finish"]:
            findings.append(f"{cid}: empty forbidden/evidence/finish")
        if not any(c["expected"][k] for k in EXPECTED_KEYS):
            findings.append(f"{cid}: no expectation at all")
        for s in c["sources"]:
            if set(s) != {"path", "sha256"}:
                findings.append(f"{cid}: source keys")
                continue
            pin = pins.get(s["path"])
            if pin is None:
                findings.append(f"{cid}: source not in frozen manifest: {s['path']}")
            elif pin[0] != s["sha256"]:
                findings.append(f"{cid}: sha256 differs from manifest for {s['path']}")
            elif not pin[1]:
                findings.append(f"{cid}: snapshot bytes do not match manifest for {s['path']}")
    topics = {c.get("topic") for c in doc.get("cases", [])}
    missing = [t for t in REQUIRED_TOPICS if t not in topics]
    for t in missing:
        findings.append(f"required topic not covered: {t}")
    report = {"schema": "prime-desk-oracle-check/1", "cases": len(doc.get("cases", [])), "required_topics": len(REQUIRED_TOPICS),
              "required_topics_covered": len(REQUIRED_TOPICS) - len(missing), "sources_checked": sum(len(c.get("sources", [])) for c in doc.get("cases", [])),
              "findings": findings, "result": "ok" if not findings else "findings",
              "limits": "shape and pins only; expected facts are not verified by this checker"}
    sys.stdout.buffer.write((json.dumps(report, indent=1) + "\n").encode("utf-8"))
    return 0 if not findings else 1


if __name__ == "__main__":
    sys.exit(main())
