"""OR-01 reproduction and focused regressions, run against one copy of the lab.
python -B repro.py <lab-copy> <out.json>
Each case commits one synthetic contents face in a disposable repository built by the lab's own test helpers."""
import importlib.util
import json
import sys
from pathlib import Path

LAB = Path(sys.argv[1]).resolve()
if "lib-build" in str(LAB).lower():
    sys.exit("stop: run only against a disposable copy")
spec = importlib.util.spec_from_file_location("orientation_test_helpers", LAB / "tests" / "test_check_book.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SYN = "Syntax: `../00.00.00.syntax/00.001.md`."
LAW = "Law: `../00.00.01.law/00.001.md`."
TAIL = "Each lists what it holds."
MISS = "Missing: `../00.00.99.missing/00.md`."
HEAD = m.GOOD.split("## Other books")[0]


def section(body, heading="## Other books"):
    return HEAD + heading + "\n" + body


CASES = [
    # name, contents face text, outcomes acceptable after the repair
    ("R01 Prime fixture: second line names a missing book",
     m.GOOD.replace(" Each lists what it holds.", "\nMissing: `../00.00.99.missing/00.md`."), {"finding", "refuse"}),
    ("R02 same line: unlabelled lower-case text holding a missing path",
     section(f"{SYN} see `../00.00.99.missing/00.md`. {LAW} {TAIL}\n"), {"finding", "refuse"}),
    ("R03 same line: comma instead of the item separator",
     section(f"Syntax: `../00.00.00.syntax/00.001.md`, Law: `../00.00.01.law/00.001.md`. {TAIL}\n"), {"refuse"}),
    ("R04 same line: an item after the trailing sentence",
     section(f"{SYN} {LAW} {TAIL} {MISS}\n"), {"finding", "refuse"}),
    ("R05 a prose line inside the section",
     section(f"{SYN} {LAW} {TAIL}\nSee also the old index.\n"), {"refuse"}),
    ("R06 a later heading ends the section",
     m.GOOD + "\n## Notes\nFree text `../00.00.99.missing/00.md` here.\n", {"clean"}),
    ("R07 valid multiline form with a blank line",
     section(f"{SYN}\n\n{LAW} {TAIL}\n"), {"clean"}),
    ("R08 duplicate Other books heading",
     m.GOOD + "\n## Other books\n" + MISS + "\n", {"refuse"}),
    ("R09 near-miss heading spelling",
     section(f"{MISS}\n", heading="## Other Books"), {"refuse"}),
    ("R10 second line: back-quoted path with no label",
     section(f"{SYN} {LAW} {TAIL}\n`../00.00.99.missing/00.md`.\n"), {"refuse"}),
    ("R11 trailing sentence on an earlier line",
     section(f"{SYN} {TAIL}\n{LAW}\n"), {"refuse"}),
    ("R12 item without its final period",
     section(f"{SYN} Law: `../00.00.01.law/00.001.md` {TAIL}\n"), {"refuse"}),
    ("R13 trailing whitespace after the sentence",
     section(f"{SYN} {LAW} {TAIL}  \n"), {"refuse"}),
    ("R14 the existing committed form",
     m.GOOD, {"clean"}),
    ("R15 multiline form, missing book on a later line",
     section(f"{SYN}\n{LAW}\n{MISS} {TAIL}\n"), {"finding"}),
]


def outcome(code):
    return {0: "clean", 1: "finding", 2: "refuse"}.get(code, f"exit {code}")


results = []
for name, text, ok in CASES:
    case = m.Book(methodName="test_correct_book_is_clean")
    case.setUp()
    files = dict(case.files)
    files[m.BOOK + "/0011.contents/01.002.md"] = text
    sha = case.commit(files)
    import subprocess
    r = subprocess.run([sys.executable, "-B", str(m.TOOL), "--root", str(case.repo), "--revision", sha,
                        "--book", m.BOOK, "--json"], capture_output=True, text=True, timeout=60)
    got = outcome(r.returncode)
    try:
        rep = json.loads(r.stdout)
    except ValueError:
        rep = {"stdout": r.stdout}
    detail = rep.get("reason") or rep.get("error") or [f["kind"] for f in rep.get("findings", [])]
    results.append({"case": name, "exit": r.returncode, "outcome": got, "accepted_after_repair": sorted(ok),
                    "meets_repair_contract": got in ok, "detail": detail,
                    "other_books": [o.get("path") for o in rep.get("other_books", [])]})
    print(f"{'ok ' if got in ok else 'BAD'} {got:8} {name} :: {detail}")
Path(sys.argv[2]).write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
print("meets contract", sum(r["meets_repair_contract"] for r in results), "of", len(results))
