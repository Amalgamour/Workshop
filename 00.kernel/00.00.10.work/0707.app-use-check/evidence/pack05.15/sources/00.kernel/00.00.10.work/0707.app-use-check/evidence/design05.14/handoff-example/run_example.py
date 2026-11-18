"""Run the HANDOFF Step 2 choices through the reference CLI on a COPY of the real sources (external fixture)."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

LIVE = Path(r"D:\Git\lib-build\00.kernel\00.00.10.work")
ROOT = Path(r"D:\librarian\temp\task-agreement-0714\handoff-example")
TA = Path(r"D:\Git\lib-build\labs\task-agreement-reference-pass01\ta.py")
EV = LIVE / "0707.app-use-check" / "evidence" / "design05.14" / "handoff-example"
if ROOT.exists() or EV.exists():
    sys.exit("refused: exists")
W = ROOT / "book" / "00.00.10.work"
for rel in ("0707.app-use-check/05.14.pack.md", "0412.prime-review/01.md", "0412.prime-review/evidence/director-agreement.md"):
    (W / rel).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(LIVE / rel, W / rel)
choices = {"schema": "task-agreement-choices/1", "for": {"page": "0707.app-use-check", "pass": "05.14"},
           "fields": {"goal": {"state": "cited", "refs": [{"source": "self", "heading": "Objective / boundaries of this larger assignment"}]},
                      "scope": {"state": "cited", "refs": [{"source": "self", "heading": "Objective / boundaries of this larger assignment"}]},
                      "finish_criteria": {"state": "cited", "refs": [{"source": "self", "heading": "#05 - Reread and return a usable handoff"}]},
                      "prime_discretion": {"state": "cited", "refs": [{"source": "0412.prime-review/01.md", "heading": "Local work agreement", "applicability": "standing"}]},
                      "director_required": {"state": "cited", "refs": [{"source": "0412.prime-review/evidence/director-agreement.md", "whole": True, "applicability": "standing"}]},
                      "recorded_decisions": {"state": "unknown"}},
           "semantic_findings": [],
           "gloss": {"text": "06.13.review 'Scope increase' paraphrases a Director observation; no verbatim Director record for this increase was found, so it stays unknown.", "by": "Codex Prime (example, SIMULATION)"}}
EV.mkdir(parents=True)
(EV / "choices.json").write_text(json.dumps(choices, indent=1) + "\n", encoding="utf-8")
pack = W / "0707.app-use-check/05.14.pack.md"
steps = [("construct", ["construct", "--book", W, "--page", "0707.app-use-check", "--pass", "05.14", "--choices", EV / "choices.json", "--out", ROOT / "out/construct.json"]),
         ("assemble", ["assemble", "--pack", pack, "--construct", ROOT / "out/construct.json", "--out", ROOT / "out/assembled.md"]),
         ("freeze-copy", None),
         ("bind", ["bind", "--book", W, "--page", "0707.app-use-check", "--pass", "05.14", "--out", ROOT / "out/binding.json"]),
         ("inspect", ["inspect", "--binding", ROOT / "out/binding.json"]),
         ("compare", ["compare", "--binding", ROOT / "out/binding.json", "--book", W])]
log = []
for name, args in steps:
    if args is None:
        pack.write_bytes((ROOT / "out/assembled.md").read_bytes())
        log.append({"step": name, "exit": 0, "note": "the authoring tool's freeze, simulated by copying the assembled pack over the fixture copy"})
        continue
    p = subprocess.run([sys.executable, "-B", str(TA), *map(str, args)], capture_output=True, timeout=60)
    (EV / f"{name}.stdout").write_bytes(p.stdout)
    (EV / f"{name}.stderr").write_bytes(p.stderr)
    log.append({"step": name, "exit": p.returncode})
    print(name, p.returncode, p.stderr.decode("utf-8", "replace").strip()[-200:])
(EV / "steps.json").write_text(json.dumps({"root": str(ROOT), "note": "SIMULATION on a copy; live book untouched", "steps": log}, indent=1) + "\n", encoding="utf-8")
