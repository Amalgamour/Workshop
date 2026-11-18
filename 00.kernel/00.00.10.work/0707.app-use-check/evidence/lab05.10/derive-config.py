import hashlib
import json
import pathlib

base = pathlib.Path(r"D:\Git\lib-build\00.kernel\00.00.10.work\0707.app-use-check\evidence")
src = base / "lab05.09" / "candidate.config.json"
out = base / "lab05.10" / "candidate.config.json"
INVOCATION = (r'The Director, chat 2026-11-01: "Work in D:\Git\lib-build. Run: '
              r'D:\Git\lib-build\00.kernel\00.00.10.work\0707.app-use-check\05.08.pack.md '
              r'This releases the focused supplemental lab described there. Verify frozen inputs. Test absent-before-prepare and '
              r'target-removed-before-record using the unchanged reviewed loop. Preserve the original matrix and failures. Do not change production '
              r'code, weaken assertions or rerun the full matrix without a specific reason. Return on 05.08.return.md and stop for Codex Prime review."')
src_raw = src.read_bytes()
old = json.loads(src_raw)
new = json.loads(src_raw)
new["output_root"] = r"D:\librarian\temp\review-loop-real-0508-fixtures"
new["label"] = "Reviewed loop pass03 / harness pass06 SUPPLEMENTAL A22a+A22b run (0707/05.08); not the 33-case matrix"
new["release"] = {"invocation": INVOCATION,
                  "note": "Derived from lab05.09/candidate.config.json; only output_root, label and release differ. Candidate, dependency and interpreter pins unchanged."}
for key in ("schema", "kind", "candidate", "dependencies", "interpreter", "timeout_seconds", "field_map"):
    assert new[key] == old[key], key
out.parent.mkdir(parents=True, exist_ok=True)
assert not out.exists()
raw = (json.dumps(new, indent=2) + "\n").encode("utf-8")
out.write_bytes(raw)
back = json.loads(out.read_bytes().decode("utf-8"))
assert back["release"]["invocation"] == INVOCATION and "\x00" not in back["release"]["invocation"]
rec = {"source": "lab05.09/candidate.config.json", "source_sha256": hashlib.sha256(src_raw).hexdigest(),
       "config_sha256": hashlib.sha256(raw).hexdigest(), "config_bytes": len(raw),
       "changed_fields": [k for k in old if old[k] != new[k]]}
(base / "lab05.10" / "config-derivation.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
print(json.dumps(rec, indent=2))
print(back["release"]["invocation"])
