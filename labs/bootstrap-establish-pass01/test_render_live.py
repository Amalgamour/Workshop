"""Pack B #06 check 6: identical output across processes, a tampered view cannot change the assignment,
missing or malformed input refuses. Runs on copies under the ignored scratch folder.

  python -B test_render_live.py -v
"""
import hashlib, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "render_live.py"
LB = HERE.parents[1]
SCRATCH = LB / "labs" / "bootstrap-git-bytes-pass01" / "scratch" / "render-tests"
RECORD = "00.kernel/00.00.10.work/0401.goal/06.01.md"
REGISTER = "00.kernel/00.00.10.work/0410.imports/manifests/step03-selection-register.tsv"
VIEW = "00.kernel/00.live.md"


def run(*a):
    return subprocess.run([sys.executable, "-B", str(TOOL), *a], capture_output=True, text=True)


class Render(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix=self._testMethodName[:20] + "-", dir=SCRATCH))
        for rel in (RECORD, REGISTER):
            (self.root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(LB / rel, self.root / rel)

    def refused(self, r, words):
        self.assertEqual(r.returncode, 2, r.stdout + r.stderr)
        self.assertIn(words, r.stdout)

    def test_two_processes_identical(self):
        a, b = self.root / "a.md", self.root / "b.md"
        self.assertEqual(run("render", "--root", str(self.root), "--out", str(a)).returncode, 0)
        self.assertEqual(run("render", "--root", str(self.root), "--out", str(b)).returncode, 0)
        self.assertEqual(a.read_bytes(), b.read_bytes())
        self.assertIn(hashlib.sha256((self.root / RECORD).read_bytes()).hexdigest(), a.read_text(encoding="utf-8"))

    def test_tampered_view_cannot_change_the_assignment(self):
        self.assertEqual(run("render", "--root", str(self.root)).returncode, 0)
        record_before = (self.root / RECORD).read_bytes()
        good = (self.root / VIEW).read_bytes()
        (self.root / VIEW).write_bytes(good.replace(b"state: returned", b"state: accepted"))
        self.refused(run("check", "--root", str(self.root)), "does not match the record")
        self.assertEqual((self.root / RECORD).read_bytes(), record_before)
        self.assertEqual(run("render", "--root", str(self.root)).returncode, 0)
        self.assertEqual((self.root / VIEW).read_bytes(), good)
        self.assertEqual(run("check", "--root", str(self.root)).returncode, 0)

    def test_missing_inputs_refuse(self):
        (self.root / RECORD).unlink()
        self.refused(run("render", "--root", str(self.root)), "missing input")

    def test_malformed_records_refuse(self):
        base = (self.root / RECORD).read_text(encoding="utf-8")
        cases = {
            "missing key": base.replace("waits_on:", "waits on:"),
            "repeated key": base + "desk: 00.kernel\n",
            "unknown key": base + "extra: x\n",
            "empty value": "\n".join("next: " if l.startswith("next: ") else l for l in base.split("\n")),
            "bad state": base.replace("assignment_state: returned", "assignment_state: done"),
            "crlf": base.replace("\n", "\r\n"),
            "other schema": base.replace("version 1", "version 2"),
        }
        words = {"missing key": "unknown key", "repeated key": "repeats a key", "unknown key": "unknown key", "empty value": "empty value",
                 "bad state": "assignment_state", "crlf": "CR line endings", "other schema": "version 1"}
        for name, text in cases.items():
            with self.subTest(case=name):
                (self.root / RECORD).write_bytes(text.encode("utf-8"))
                self.refused(run("render", "--root", str(self.root)), words[name])


if __name__ == "__main__":
    unittest.main()
