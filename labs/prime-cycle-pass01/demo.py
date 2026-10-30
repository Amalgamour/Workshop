"""End-to-end demo of the Prime read-record-read cycle on a disposable book (0515.prime-cycle/05.01; journal added in 05.02).

  python -B demo.py [--transcript OUT.json]

SYNTHETIC SUPPLIED decisions only; no model, no real desk state. Four works in one book:
- A: a new return, left awaiting review;
- B: reviewed held for correction (pass open, goal open);
- C: accepted, pass finished, page goal still open;
- D: accepted, then a separate explicit goal completion recorded as a successor;
then D's page changes, so its completion is shown as historical, and the day view is read in a new process.
Each step runs the real CLI in a new process with an explicit --journal-root; the transcript keeps argv, exit and stdout.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "tests"))
import fixture as F  # noqa: E402


def main():
    out_path = Path(sys.argv[sys.argv.index("--transcript") + 1]) if "--transcript" in sys.argv else None
    d = F.Desk(prefix="pcy-demo-")
    steps = []

    journal = d.out / "journal"

    def cli(label, *args, log=True):
        if log:
            args = (*args, "--journal-root", journal, "--caller", "Codex Prime (SYNTHETIC DEMO)")
        code, out, err = d.cli(*args)
        steps.append({"step": label, "argv": ["python", "-B", "prime_cycle.py", *[str(a) for a in args]], "exit": code, "stdout": out, "stderr": err})
        print(f"$ prime_cycle.py {args[0]} ...  [{label}]  exit {code}")
        return code, out

    try:
        works = []
        for wid, lane in (("A", "0597.demo-a"), ("B", "0596.demo-b"), ("C", "0595.demo-c"), ("D", "0594.demo-d")):
            m = d.member(f"demo{wid.lower()}", lane, "05.01")
            d.page(lane, "05.01", F.page_text(m, d.receipt(m)))
            works.append(d.work(wid, lane, "05.01", m))
        reg = d.registration(works)
        tdir = d.out / "templates"
        cli("1 first read; templates written", "read", "--registration", reg, "--templates", tdir)
        for wid, kind in (("B", "held"), ("C", "accept-finished-open"), ("D", "accept-finished-open")):
            t = json.loads((tdir / f"template-{wid}.json").read_text(encoding="utf-8"))
            cli(f"2 record {wid} ({kind})", "record", "--registration", reg, "--decision", d.write_decision(F.fill(t, kind), f"dec-{wid}.json"))
        code, out = cli("3 read after records", "read", "--registration", reg, "--json")
        tD = next(w["template"] for w in json.loads(out)["works"] if w["work_id"] == "D")
        cli("4 record D goal completion (successor)", "record", "--registration", reg, "--decision", d.write_decision(F.fill(tD, "complete"), "dec-D2.json"))
        code, out = cli("5 new-process read", "read", "--registration", reg)
        print("\n" + out)
        d.page("0594.demo-d", "05.01", F.page_text(works[3]["member"], d.receipt(works[3]["member"]), extra="\nEdited after completion."))
        code, out = cli("6 read after D's page changed", "read", "--registration", reg)
        print(out)
        date = next(journal.iterdir()).name
        code, out = cli("7 day view (new process, not logged)", "day", "--journal-root", journal, "--date", date, "--registration", reg, log=False)
        print(out)
        if out_path:
            out_path.write_text(json.dumps({"schema": "prime-cycle-demo-transcript/1", "label": "SYNTHETIC SUPPLIED decisions; disposable book; no model",
                                            "steps": steps}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    finally:
        d.close()


if __name__ == "__main__":
    main()
