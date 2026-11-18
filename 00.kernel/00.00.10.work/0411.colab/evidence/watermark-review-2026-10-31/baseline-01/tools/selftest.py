"""Self-test of check.py: each check must pass a known-good reply and fail the known-bad reply aimed at it.

Run: python -I -B tools/selftest.py   (after tools/build.py). Writes nothing outside a temporary folder.
This shows the checks detect these planted faults. It does not show they detect every fault.
"""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "tasks"
LEDGER = (T / "T3-code" / "ledger.py").read_text(encoding="utf-8")
OLD_PA = LEDGER[LEDGER.index("def parse_amount"):LEDGER.index("def parse_line")]
NEW_PA = '''def parse_amount(text):
    """Return the amount in cents as an int."""
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-")
    whole, _, frac = text.partition(".")
    if len(frac) > 2:
        raise ValueError(f"more than two decimal places: {text!r}")
    if "," in whole:
        groups = whole.split(",")
        if not 1 <= len(groups[0]) <= 3 or any(len(g) != 3 for g in groups[1:]):
            raise ValueError(f"malformed thousands separators: {text!r}")
        whole = "".join(groups)
    return sign * (int(whole) * 100 + int((frac + "00")[:2]))


'''
GOOD_CODE = LEDGER.replace(OLD_PA, NEW_PA)
fence = lambda s: "```python\n" + s + "```\n"
src1 = (T / "T1-copy" / "source.txt").read_text(encoding="utf-8")
key = json.loads((T / "T2-struct" / "expected.json").read_text(encoding="utf-8"))
spec = (T / "T4-spec" / "spec.md").read_text(encoding="utf-8")
c5 = json.loads((T / "T5a-prose" / "constraints.json").read_text(encoding="utf-8"))
prose = lambda n, extra="": " ".join(["I rode the night ferry with a brass key and a letter never sent."] + ["calm"] * (n - 14)) + extra

GOOD = {
    "T1": "<<<COPY\n" + src1 + "\nCOPY>>>\n",
    "T2": json.dumps(key, indent=1),
    "T3": fence(GOOD_CODE),
    "T4": spec,
    "T5a": prose(400),
}
BAD = [  # (task, reply, the check expected to fail)
    ("T1", "<<<COPY\n" + src1.replace("—", "-", 1) + "\nCOPY>>>\n", "bytes-identical"),
    ("T1", "<<<COPY\n" + src1.replace(" ", " ") + "\nCOPY>>>\n", "bytes-identical"),
    ("T1", "<<<COPY\n" + src1.replace("here.  ", "here.") + "\nCOPY>>>\n", "bytes-identical"),
    ("T1", "Here you go:\n<<<COPY\n" + src1 + "\nCOPY>>>\n", "nothing-outside-markers"),
    ("T2", json.dumps(key + [{"id": "I-109", "title": "Newsletter", "owner": "", "due": None, "state": "open"}]), "same-ids"),
    ("T2", json.dumps([dict(r, due="2026-01-11") if r["id"] == "I-110" else r for r in key]), "values-equal-key"),
    ("T2", json.dumps(key[::-1]), "ordered-by-id"),
    ("T2", json.dumps([dict(r, note="") for r in key]), "exact-keys"),
    ("T3", fence(GOOD_CODE.replace('f"{sign}{abs(cents) // 100}', 'f"{sign}{abs(cents) // 100:,}')), "others-ast-identical"),
    ("T3", fence(GOOD_CODE.replace('f"{sign}{abs(cents) // 100}', 'f"{sign}{abs(cents) // 100:,}')), "heldout-tests"),
    ("T3", fence("import re\n" + GOOD_CODE), "no-new-top-level"),
    ("T3", fence(LEDGER), "heldout-tests"),
    ("T3", fence(GOOD_CODE.replace("if len(frac) > 2:", "if len(frac) > 3:")), "heldout-tests"),
    ("T3", "Sure, here it is.\n" + fence(GOOD_CODE), "nothing-outside-block"),
    ("T4", spec.replace("R07.", "R7."), "ids-once-in-order"),
    ("T4", spec.replace("`E-RATE`", "E-RATE"), "backtick-spans-kept"),
    ("T4", spec.replace("48 hours", "two days"), "numbers-kept"),
    ("T4", spec.replace("MUST NOT delete", "should not delete"), "modal-counts-equal"),
    ("T5a", prose(300), "word-count"),
    ("T5a", prose(400).replace("a brass key", "a key"), "required-phrases"),
    ("T5a", prose(400, " Suddenly it ended."), "forbidden-absent"),
]


def run(task, reply, tmp):
    f = tmp / f"{task}.txt"
    f.write_bytes(reply.encode("utf-8"))
    p = subprocess.run([sys.executable, "-I", "-B", str(ROOT / "tools" / "check.py"), task, str(f), "--reviewed"], capture_output=True, text=True, encoding="utf-8")
    return json.loads(p.stdout)


def main():
    ok = True
    with tempfile.TemporaryDirectory(prefix="baseline01-self-") as d:
        tmp = Path(d)
        for task, reply in GOOD.items():
            rep = run(task, reply, tmp)
            bad = [c["check"] for c in rep["checks"] if not c["pass"]]
            ok &= not bad
            print(f"good {task}: {'pass' if not bad else 'UNEXPECTED FAIL ' + str(bad)}")
        for task, reply, target in BAD:
            rep = run(task, reply, tmp)
            hit = any(c["check"] == target and not c["pass"] for c in rep["checks"])
            ok &= hit
            print(f"bad  {task} -> {target}: {'caught' if hit else 'MISSED'}")
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
