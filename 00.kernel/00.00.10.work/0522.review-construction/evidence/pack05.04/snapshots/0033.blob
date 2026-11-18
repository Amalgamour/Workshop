"""Disposable fixtures for prime_cycle tests and demo: a real Git repository and book, real reserve/capture through the
pinned helper, and synthetic SUPPLIED decisions. Nothing here touches a shared checkout or calls a model."""
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
LABS = LAB.parent
TOOL = LAB / "prime_cycle.py"
RC = LABS / "return-capture-pass01"
BOOK = "00.kernel/00.00.10.work"
GENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local", GIT_COMMITTER_NAME="fixture",
            GIT_COMMITTER_EMAIL="fixture@local", GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1")
AGREEMENT = {"goal": "SUPPLIED FIXTURE goal.", "scope": "SUPPLIED FIXTURE scope: this page only.",
             "prime_discretion": "Prime may accept a bounded repair inside this scope.",
             "director_required": "Any change of design or scope.",
             "finish_criteria": [{"id": "done", "text": "The fixture page's stated goal is met."}],
             "recorded_decisions": [{"id": "D1", "text": "SUPPLIED FIXTURE release.", "source_sha256": "0" * 64}]}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def writable_retry(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def page_text(member=None, receipt=None, review="PENDING.", extra=""):
    ptr = f"Execution: returned. Member {member}. Receipt sha256 {receipt}. Fresh verify: result complete." if member else "PENDING."
    return (f"# 05 — Fixture cycle batch\nversion: 001\nstate: draft\nFace: 05\nPPPP: 0599\nbook: 00.00.10.work\n\n"
            f"## Assignment\nExecutor: fixture builder. Reviewer: fixture Prime.\n\n## #01 — Do it\nWrite out.txt.{extra}\n\n"
            f"## Return pointer\n{ptr}\n\n## Review — Codex Prime\n{review}\n")


class Desk:
    """One disposable repository, book, members book and output root."""

    def __init__(self, prefix="pcy-"):
        self.tmp = Path(tempfile.mkdtemp(prefix=prefix))
        self.repo = self.tmp / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.book = self.repo / BOOK
        self.book.mkdir(parents=True)
        self.out = self.tmp / "out"
        self.out.mkdir()
        self.src = self.tmp / "src"
        self.src.mkdir()
        self.n = 0

    def close(self):
        shutil.rmtree(self.tmp, onexc=writable_retry)

    def git(self, *a):
        return subprocess.run(["git", "-C", str(self.repo), *a], capture_output=True, env=GENV, check=True).stdout.decode().strip()

    def rc(self, *args):
        r = subprocess.run([sys.executable, "-B", str(RC / "return_capture.py"), *map(str, args)], capture_output=True,
                           text=True, encoding="utf-8", timeout=120)
        assert r.returncode == 0 and r.stderr == "", r.stdout + r.stderr
        return r.stdout

    def member(self, name, lane, batch, retrospective=False):
        self.n += 1
        folder = self.rc("reserve", "--book", self.book, "--submission", f"fx-{name}", "--name", name, "--origin-book", "00.00.10.work",
                         "--origin-page", lane, "--origin-batch", batch, "--expected-output", "note.txt", "--submitter", "fixture",
                         "--reviewer", "fixture", "--release", "fixture only").split()[1]
        (self.src / "note.txt").write_bytes(f"note {self.n}\n".encode())
        (self.src / f"{name}.md").write_bytes(f"Did {name}.\n".encode())
        extra = ["--retrospective", "--source-commit", "a" * 40] if retrospective else []
        self.rc("capture", "--book", self.book, "--submission", f"fx-{name}", "--return-file", self.src / f"{name}.md",
                "--source-root", self.src, "--artifact", "note.txt|note.txt", *extra)
        return folder

    def receipt(self, folder):
        return sha((self.book / folder / "receipt.json").read_bytes())

    def page(self, lane, batch, text):
        p = self.book / lane / f"{batch}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        (p.parent / "evidence").mkdir(exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
        return f"{BOOK}/{lane}/{batch}.md"

    def commit(self):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "fixture")
        return self.git("rev-parse", "HEAD")

    def work(self, work_id, lane, batch, member, goal_id="g1", statement="SUPPLIED FIXTURE goal statement."):
        return {"work_id": work_id, "page": f"{BOOK}/{lane}/{batch}.md", "pass": batch, "member": member,
                "goal": {"goal_id": goal_id, "statement": statement}, "agreement": AGREEMENT,
                "review_location": f"{BOOK}/{lane}/evidence/prime-cycle-reviews/{batch}"}

    def registration(self, works, source=None, name="reg.json", bounds=None):
        reg = {"schema": "prime-cycle-registration/1", "repository": str(self.repo), "book": BOOK, "book_label": "00.00.10.work",
               "source": source or {"kind": "live-file", "commit": None}, "members_book": str(self.book), "output_root": str(self.out),
               "bounds": bounds or {"max_works": 16, "max_page_bytes": 262144, "max_output_bytes": 2097152}, "works": works}
        p = self.tmp / name
        p.write_bytes(json.dumps(reg, indent=1).encode())
        return p

    def cli(self, *args):
        r = subprocess.run([sys.executable, "-B", str(TOOL), *map(str, args)], capture_output=True, timeout=600)
        return r.returncode, r.stdout.decode("utf-8"), r.stderr.decode("utf-8")

    def read(self, reg):
        code, out, err = self.cli("read", "--registration", reg, "--json")
        assert err == "", err
        return code, (json.loads(out) if out.startswith("{") else out)

    def write_decision(self, d, name):
        p = self.tmp / name
        p.write_bytes(json.dumps(d, indent=1).encode())
        return p


def fill(template, kind, actor="Codex Prime (SUPPLIED FIXTURE)", **over):
    """A synthetic SUPPLIED decision from a read template. kind: accept-finished-open | complete | held | director-input."""
    d = json.loads(json.dumps(template))
    d["attribution"] = {"actor_label": actor, "role": "prime", "evidence": "SUPPLIED FIXTURE decision; the label is not authentication."}
    j = d["judgment"]
    page = d["binding"]["page"]
    j.update(finding="SUPPLIED FIXTURE finding.", reasons=["SUPPLIED FIXTURE reason."], source_refs=[page],
             semantic_conflict=False, design_fork=None, unresolved=[], holds=[], answers=[])
    s = j["sections"]
    if kind == "accept-finished-open":
        j.update(outcome="continue", disposition="accepted", pass_terminal="finished",
                 next_action={"action_id": "next-pass", "text": "Pack the next bounded pass toward the page goal.", "authorized_in_grant": True})
        j["goal"]["terminal"] = "open"
        s.update(return_result="The fixture pass returned.", prime_finding="The pass meets its own scope.",
                 within_direction="Inside the fixture grant.", next_bounded_action="Pack the next bounded pass.")
    elif kind == "complete":
        j.update(outcome="complete", disposition="accepted", pass_terminal="finished", next_action=None)
        j["goal"].update(terminal="completed", evidence=[page, d["binding"]["member"] + "/receipt.json"])
        s.update(outcome_evidence="SUPPLIED FIXTURE evidence: the page goal is met.", limits="Fixture only.",
                 tests_note="Fixture tests are not a goal judgment.", learning="SUPPLIED FIXTURE learning.",
                 preservation="Captured member and this review record.", remaining_choices=["None in this fixture."],
                 findings_account=[{"finding_id": f"{page}#F-01", "status": "accepted"}], finish_assessments=[{"criterion_id": "done", "assessment": "met"}])
    elif kind == "held":
        j.update(outcome="continue", disposition="held", pass_terminal="open",
                 next_action={"action_id": "repair-pass", "text": "Correct the held finding.", "authorized_in_grant": True})
        j["goal"]["terminal"] = "open"
        s.update(return_result="The fixture pass returned.", prime_finding="Held for a fixture defect.",
                 within_direction="Inside the fixture grant.", next_bounded_action="Correct the held finding.")
    elif kind == "director-input":
        q = "SUPPLIED FIXTURE question: should the design change?"
        qs = sha(q.encode())
        j.update(outcome="director-input", disposition="held", pass_terminal="open", next_action=None,
                 holds=[{"hold_id": "H1", "finding_id": f"{page}#F-01", "kind": "director-judgment", "question_id": "Q1",
                         "question_revision": "r1", "question_sha256": qs, "dependent_scope": ["design-change"]}])
        j["goal"]["terminal"] = "open"
        s.update(issue="SUPPLIED FIXTURE design question.", consequences="Either choice changes later passes.",
                 options=["Keep the design.", "Change the design."], recommendation="Keep the design.",
                 question={"id": "Q1", "revision": "r1", "content_sha256": qs, "text": q},
                 affected=[{"action_id": "design-change", "dependency": "the open design question"}])
    for k, v in over.items():
        j[k] = v
    return d
