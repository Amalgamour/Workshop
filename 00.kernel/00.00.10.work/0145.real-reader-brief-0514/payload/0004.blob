"""End-to-end fixture demo for prime_brief.py (0507.prime-support/05.13; fixtures in the real reader shape since 05.14).
SYNTHETIC data only; no real desk state. The actual-source rehearsal is evidence/realbrief05.14/rehearse.py.

  python -B demo.py

Builds a disposable member book with the real pinned return_capture.py, then briefs six labelled reader-observation
fixtures through the pinned, repaired state projection (fresh custody through the pinned inspector):
- a returned item awaiting review;
- a correction-required item with a follow-up;
- an item whose only member is a same-origin retrospective capture (never completes);
- an explicitly completed fixture;
- a fenced release line with no coordination (unprojected);
- a decision bound to a changed source (unprojected).
"""
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB / "tests"))
import test_prime_brief as t  # noqa: E402


class Demo(t.Fixture):
    def runTest(self):
        pass


def main():
    d = Demo()
    d.setUp()
    try:
        L = t.LANE
        a = d.member("await", batch="05.31")
        fix = d.member("fix", batch="05.32")
        retro = d.member("retro", batch="05.33", retrospective=True)
        done = d.member("done", batch="05.34")
        o1, o2, o3, o4 = (t.robs(batch="05.31", members=[a]), t.robs(batch="05.32", members=[fix]),
                          t.robs(batch="05.33", members=[retro]), t.robs(batch="05.34", members=[done]))
        o5 = t.robs(batch="05.35", release_raw='Release: "do everything" (inside a fenced example)')
        o6 = t.robs(batch="05.36", members=[done])
        c6 = t.coord(o6, review=t.decision(done, d.receipt(done)))
        c6["source_sha256"] = t.sha("an earlier version of the page")
        pairs = [(o1, t.coord(o1), "SYNTHETIC"),
                 (o2, t.coord(o2, review=t.decision(fix, d.receipt(fix), disposition="correction-required", terminal=None,
                                                    followup=f"{L}/05.37 (fixture follow-up)")), "SYNTHETIC"),
                 (o3, t.coord(o3, review=t.decision(retro, d.receipt(retro))), "SYNTHETIC"),
                 (o4, t.coord(o4, review=t.decision(done, d.receipt(done))), "SYNTHETIC"),
                 (o5, None, "SYNTHETIC"), (o6, c6, "SYNTHETIC")]
        path = d.tmp / "demo-input.json"
        import json
        path.write_bytes(json.dumps(d.doc(pairs), ensure_ascii=False).encode("utf-8"))
        print(f"fixture member book {d.mbook}\ninput {path}\n")
        r = subprocess.run([sys.executable, "-B", str(t.TOOL), "brief", "--input", str(path), "--inspect"], capture_output=True)
        sys.stdout.write(r.stdout.decode("utf-8"))
        print(f"exit {r.returncode} (1 = brief with attention or unprojected items)")
        print("\nSYNTHETIC fixtures only. Nothing was written, selected or dispatched. No authority was granted.")
    finally:
        d.tearDown()


if __name__ == "__main__":
    main()
