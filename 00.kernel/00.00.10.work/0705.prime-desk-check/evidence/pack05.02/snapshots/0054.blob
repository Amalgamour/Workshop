"""Demo for state_projection.py (0507.prime-support/05.12). Fixture inputs only; no real desk state.

  python -B demo.py

Builds a disposable member book with the real pinned return_capture.py and inspects it through the pinned
return_inspect.py. It projects three items in one lane:
- a correction-required item (bound review, current candidate);
- an item whose review names a historical secondary member (mismatched binding);
- a separately and explicitly completed item.
Then it prints the readable view. The projection grants no authority.
"""
import json
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB / "tests"))
import test_state_projection as t  # noqa: E402


class Demo(t.Fixture):
    def runTest(self):
        pass


def main():
    d = Demo()
    d.setUp()
    try:
        fix = d.member("fix", page="0507.prime-support", batch="05.21")
        hist = d.member("hist", page="0509.pack-assembly", batch="05.01", retrospective=True)
        own = d.member("own", page="0507.prime-support", batch="05.22")
        done = d.member("done", page="0507.prime-support", batch="05.23")
        rows = [
            t.obs(batch="05.21", **{"return": {"pointer": "present", "members": [fix], "candidate": None},
                                    "review": t.bound(fix, d.receipt(fix), disposition="correction-required", terminal=None,
                                                      followup="0507.prime-support/05.24 (fixture follow-up)")}),
            t.obs(batch="05.22", **{"return": {"pointer": "present", "members": [hist, own], "candidate": None},
                                    "review": t.bound(hist, d.receipt(hist))}),
            t.obs(batch="05.23", **{"return": {"pointer": "present", "members": [done], "candidate": None},
                                    "review": t.bound(done, d.receipt(done)),
                                    "publication": {"status": "at-ref", "ref": "refs/remotes/origin/fixture", "commit": "e" * 40}}),
        ]
        path = d.tmp / "demo-input.json"
        path.write_bytes(json.dumps(d.doc(rows)).encode())
        print(f"fixture member book {d.mbook}\ninput {path}\n")
        r = subprocess.run([sys.executable, "-B", str(t.TOOL), "project", "--input", str(path), "--inspect"],
                           capture_output=True, text=True, encoding="utf-8")
        print(r.stdout, end="")
        print(f"exit {r.returncode} (1 = projected with attention)")
        print("\nFixture data only. Nothing was written. No release, acceptance, seat or work was granted.")
    finally:
        d.tearDown()


if __name__ == "__main__":
    main()
