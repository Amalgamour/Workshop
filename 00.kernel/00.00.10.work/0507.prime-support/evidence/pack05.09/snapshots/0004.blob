"""Demo for prime_boot.py (0507.prime-support/05.07): fixture answers and a fixture judgement, no model.

  python -B demo.py

Builds a disposable Git fixture and an external records root under the system temp directory, then runs
prepare -> fixture answers -> check -> fixture judgement -> show, twice: attempt 1 is capped too tightly and its
answers miss the reported conflict, so it is judged with a remediation; attempt 2 links attempt 1, carries the
remedy and is oriented. Orientation grants no authority. Nothing here is a cold model boot.
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB / "tests"))
import test_prime_boot as t  # noqa: E402


class Demo(t.Fixture):
    def runTest(self):
        pass

    def say(self, title, out):
        print(f"\n== {title}\n{out.rstrip()}")


def main():
    demo = Demo()
    demo.setUp()
    try:
        demo.head = demo.commit({t.ASSIGN: t.assignment(state="waiting", work=f"{t.PAGE}/05.01.md")})
        reg = demo.registry(canonical={"repository": "work", "path": t.ASSIGN, "lane": "fixture"})
        print(f"fixture repository {demo.repo}\nrecords root {demo.records}")

        req1 = demo.request(registry=reg, limits={"max_refs": 5, "max_bytes": 131072})
        a1, code, out = demo.prepare(req1, attempt="a1")
        demo.say("attempt 1: prepare (max_refs 5)", out)
        conflicts = demo.stage(a1, "07.status.json")["conflicts"]
        print("reported conflicts:", json.dumps(conflicts, indent=1))
        ans1 = demo.good_answers(a1, target=t.ASSIGN)
        ans1["answers"]["O2"]["fields"] = {k: {"value": v, "citation": "R04"} for k, v in
                                           {"release": "waiting", "claim": "builder", "execution": "waiting",
                                            "review": "next: return"}.items()}
        demo.say("attempt 1: check (fixture answers)",
                 demo.cli("check", "--attempt", a1, "--answers", demo.write_json("ans-a1.json", ans1))[1])
        j1 = demo.judgement(a1, grade="gap", remediation=[
            {"kind": "reference", "detail": "raise max_refs so both lane pages are in the packet"},
            {"kind": "question", "detail": "acknowledge the canonical-record conflict in O1"}])
        demo.say("attempt 1: judge (fixture judgement)",
                 demo.cli("judge", "--attempt", a1, "--judgement", demo.write_json("jud-a1.json", j1))[1])
        demo.say("attempt 1: show", demo.cli("show", "--attempt", a1)[1])

        req2 = demo.request(registry=reg, attempt=2, previous_attempt=str(a1))
        a2, code, out = demo.prepare(req2, attempt="a2")
        demo.say("attempt 2: prepare (links attempt 1, max_refs 12)", out)
        print("link:", json.dumps({k: v for k, v in demo.stage(a2, "02.links.json").items() if k != "status"}, indent=1))
        ans2 = demo.good_answers(a2, conflicts=range(len(conflicts)))
        demo.say("attempt 2: check", demo.cli("check", "--attempt", a2, "--answers", demo.write_json("ans-a2.json", ans2))[1])
        demo.say("attempt 2: judge",
                 demo.cli("judge", "--attempt", a2, "--judgement", demo.write_json("jud-a2.json", demo.judgement(a2)))[1])
        demo.say("attempt 2: show", demo.cli("show", "--attempt", a2)[1])
        print("\nattempt 1 files:", " ".join(sorted(p.name for p in a1.iterdir())))
        print("attempt 2 files:", " ".join(sorted(p.name for p in a2.iterdir())))
        print("\nNo model was called. Answers and judgements are fixtures. Orientation is not authority.")
    finally:
        demo.tearDown()


if __name__ == "__main__":
    main()
