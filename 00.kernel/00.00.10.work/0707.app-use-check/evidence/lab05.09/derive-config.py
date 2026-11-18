import hashlib
import json
import pathlib

base = pathlib.Path(r"D:\Git\lib-build\00.kernel\00.00.10.work\0707.app-use-check\evidence")
first = base / "lab05.09" / "candidate.config.json"
kept = base / "lab05.09" / "candidate.config.derivation1-corrupt.json"
assert not kept.exists()
first_raw = first.read_bytes()
first.rename(kept)  # bytes preserved under a distinct name; never used for a run

INVOCATION = (r'The Director, chat 2026-11-01: "Work in D:\Git\lib-build. Run: '
              r'D:\Git\lib-build\00.kernel\00.00.10.work\0707.app-use-check\05.07.pack.md '
              r'This releases the bounded nonproduction candidate-acceptance lab described there. '
              r'Verify the frozen inputs, record this invocation, and run the reviewed loop through the repaired harness '
              r'in new disposable fixtures. Preserve failures and unchanged assertions. Do not repair until green, change '
              r'the active app, or launch bots. Return on 05.07.return.md and stop for Codex Prime review."')
t_raw = (base / "pack05.07" / "candidate-template.json").read_bytes()
t = json.loads(t_raw)
c = json.loads(t_raw)
c["release"] = {"invocation": INVOCATION,
                "note": "Derived from pack05.07/candidate-template.json for the named 0707/05.07 release; only release.invocation and release.note differ from the template."}
raw = (json.dumps(c, indent=2) + "\n").encode("utf-8")
assert not first.exists()
first.write_bytes(raw)
assert all(t[k] == c[k] for k in t if k != "release")
rec = {"template_sha256": hashlib.sha256(t_raw).hexdigest(), "template_bytes": len(t_raw),
       "config_sha256": hashlib.sha256(raw).hexdigest(), "config_bytes": len(raw),
       "changed_fields": ["release.invocation", "release.note"],
       "first_derivation": {"file": kept.name, "sha256": hashlib.sha256(first_raw).hexdigest(), "bytes": len(first_raw),
                            "defect": "shell heredoc + Python string escapes turned \\0 sequences in the quoted path into control characters; never used"}}
(base / "lab05.09" / "config-derivation.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
print(json.dumps(rec, indent=2))
print(json.loads(raw)["release"]["invocation"])
