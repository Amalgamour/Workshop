"""End-to-end lab of the first desk workflow (0519.desk-app/05.01): Prime records an assignment, a worker retrieves it,
returns it into durable custody, Prime retrieves and reviews it, and the next action survives a restart.

  python -B demo.py [--transcript OUT.json] [--keep]

SYNTHETIC tasks, returns and decisions. No model, reviewer or session runs. Everything happens in one disposable Git
repository under the system temp directory, with task-local git identity. Every tool call is a new process: the pinned
return_capture, return_inspect, batch_observe and prime_cycle, plus this lab's desk_lab.py. Each step states what it
expects; the transcript records argv, exit, the stdout/stderr bytes' digests and an excerpt, and whether the expectation
held. A failed expectation is reported, never hidden.
"""
import hashlib
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

LAB = Path(__file__).resolve().parent
LABS = LAB.parent
DESK = LAB / "desk_lab.py"
RC = LABS / "return-capture-pass01" / "return_capture.py"
PC = LABS / "prime-cycle-pass01" / "prime_cycle.py"
BOOK = "00.kernel/00.00.10.work"
GENV = dict(os.environ, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@local", GIT_COMMITTER_NAME="fixture",
            GIT_COMMITTER_EMAIL="fixture@local", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull,
            PYTHONDONTWRITEBYTECODE="1")
WORKER = "Builder-X (SYNTHETIC)"
PRIME = "Codex Prime (SYNTHETIC)"
AGREEMENT = {"goal": "SYNTHETIC goal: write out.md.", "scope": "SYNTHETIC scope: this page only.",
             "prime_discretion": "Prime may accept a bounded repair inside this scope.",
             "director_required": "Any change of design or scope.",
             "finish_criteria": [{"id": "done", "text": "out.md exists and says what it did."}],
             "recorded_decisions": [{"id": "D1", "text": "SYNTHETIC release.", "source_sha256": "0" * 64}]}


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def tree_digest(p: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(x for x in p.rglob("*") if x.is_file()):
        h.update(f.relative_to(p).as_posix().encode() + b"\0" + f.read_bytes() + b"\0")
    return h.hexdigest()


class Run:
    def __init__(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="desk-lab-"))
        self.repo = self.tmp / "repo"
        self.book = self.repo / BOOK
        self.book.mkdir(parents=True)
        self.inputs = self.tmp / "inputs"
        self.inputs.mkdir()
        self.out = self.tmp / "out"
        self.out.mkdir()
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.repo)], check=True, env=GENV, capture_output=True)
        self.steps = []
        self.n = 0

    def call(self, label, tool, args, expect_exit, check=None):
        argv = [sys.executable, "-I", "-B", str(tool), *map(str, args)]
        p = subprocess.run(argv, capture_output=True, timeout=600, env=GENV)
        out, err = p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")
        ok = p.returncode in (expect_exit if isinstance(expect_exit, tuple) else (expect_exit,))
        note = None
        if ok and check:
            try:
                note = check(out, err)
                ok = note is True or (isinstance(note, str) and not note.startswith("FAIL"))
            except Exception as e:  # an unexpected shape is a failed expectation, recorded
                ok, note = False, f"FAIL check raised {type(e).__name__}: {e}"
        self.n += 1
        step = {"n": self.n, "step": label, "argv": [Path(sys.executable).name, "-I", "-B", self.rel(tool),
                                                       *[self.rel(a) for a in args]],
                "exit": p.returncode, "expected_exit": expect_exit, "expectation_held": ok, "check": note,
                "stdout_sha256": sha(p.stdout), "stdout_bytes": len(p.stdout), "stderr_sha256": sha(p.stderr),
                "stdout_excerpt": out[:1500], "stderr_excerpt": err[:600]}
        self.steps.append(step)
        print(f"[{self.n:02d}] {'ok  ' if ok else 'FAIL'} exit {p.returncode} (want {expect_exit})  {label}" + (f"  -- {note}" if note and note is not True else ""))
        if not ok and err.strip():
            print("      stderr: " + err.strip()[:600])
        return p.returncode, out, err

    def rel(self, a):
        s = str(a)  # text substitution only: the tools and the disposable repo may sit on different drives
        return s.replace(str(self.tmp), "<tmp>").replace(str(LABS.parent), "<checkout>").replace("\\", "/")

    def write_input(self, name, obj):
        p = self.inputs / name
        p.write_bytes(json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"))
        return p

    def page_path(self, lane, batch="05.01"):
        return self.book / lane / f"{batch}.md"

    def page_sha(self, lane, batch="05.01"):
        return sha(self.page_path(lane, batch).read_bytes())

    def view(self, label, *extra, expect=(0, 1), check=None):
        code, out, err = self.call(label, DESK, ["view", "--repo", self.repo, "--json", *extra], expect, check)
        return json.loads(out) if out.startswith("{") else None

    def close(self, keep):
        if keep:
            print(f"kept: {self.tmp}")
            return
        shutil.rmtree(self.tmp, onexc=lambda f, p, e: (os.chmod(p, stat.S_IWRITE), f(p)))


def task(view, member):
    return next(t for t in view["tasks"] if t["member"] == member)


def expect_state(member, state, actor=None):
    def check(out, err):
        t = task(json.loads(out), member)
        if t["state"] != state or (actor is not None and t["actor"] != actor):
            return f"FAIL {member} is {t['state']} / {t['actor']}, wanted {state} / {actor}"
        return f"{member}: {state}, actor {t['actor']}, next: {t['next']}"
    return check


def batch_input(lane, member, submission, title):
    return {"template": "batch-page/1", "title": title, "pppp": lane[:4], "pass": "05.01", "who": PRIME,
            "executor": WORKER, "reviewer": PRIME, "workspace": "<disposable>", "branch": "workshop",
            "goal": "SYNTHETIC: write out.md describing one change.",
            "steps": [{"title": "Do it", "text": "Write evidence/build05.01/out.md and submission.md (Did, Blocked, Need)."}],
            "allowed_writes": f"Only {lane}/evidence/build05.01 and capture {member}.",
            "capture": {"member": member, "submission": submission,
                        "return_file": f"{BOOK}/{lane}/evidence/build05.01/submission.md",
                        "artifacts": [f"{BOOK}/{lane}/evidence/build05.01/out.md"]}}


def fill_decision(template, kind):
    d = json.loads(json.dumps(template))
    d["attribution"] = {"actor_label": PRIME, "role": "prime", "evidence": "SYNTHETIC decision; the label is not authentication."}
    j = d["judgment"]
    page = d["binding"]["page"]
    j.update(finding="SYNTHETIC finding.", reasons=["SYNTHETIC reason."], source_refs=[page], semantic_conflict=False,
             design_fork=None, unresolved=[], holds=[], answers=[])
    s = j["sections"]
    if kind == "accept":
        j.update(outcome="continue", disposition="accepted", pass_terminal="finished",
                 next_action={"action_id": "next-pass", "text": "Pack 05.02: add the second change.", "authorized_in_grant": True})
        j["goal"]["terminal"] = "open"
        s.update(return_result="The pass returned out.md.", prime_finding="Meets its own scope.",
                 within_direction="Inside the grant.", next_bounded_action="Pack 05.02.")
    else:
        j.update(outcome="continue", disposition="held", pass_terminal="open",
                 next_action={"action_id": "repair", "text": "Correct out.md: it omits Blocked.", "authorized_in_grant": True})
        j["goal"]["terminal"] = "open"
        s.update(return_result="The pass returned out.md.", prime_finding="Held: Blocked is missing.",
                 within_direction="Inside the grant.", next_bounded_action="Repair out.md.")
    return d


def scenarios(r):
    A, B = "0598.demo-loop", "0597.demo-stale"
    # ---- 1. Prime records the assignment: compute builds the page, the helper reserves the member
    r.call("1a Prime: construct batch page A from a structured spec", DESK,
           ["construct", "--template", "batch-page/1", "--input", r.write_input("a-page.json",
            batch_input(A, "0101.demo-a-0501", "syn-a-0501", "SYNTHETIC loop A")), "--target", r.page_path(A),
            "--expect-sha256", "absent", "--write"], 0)
    r.call("1b Prime: reserve member A (existing helper)", RC,
           ["reserve", "--book", r.book, "--submission", "syn-a-0501", "--name", "demo-a-0501", "--origin-book", "00.00.10.work",
            "--origin-page", A, "--origin-batch", "05.01", "--expected-output", "out.md", "--submitter", WORKER,
            "--reviewer", PRIME, "--release", f"Reservation only; Director release must be recorded on {A}/05.01."], 0)
    reg = {"schema": "prime-cycle-registration/1", "repository": str(r.repo), "book": BOOK, "book_label": "00.00.10.work",
           "source": {"kind": "live-file", "commit": None}, "members_book": str(r.book), "output_root": str(r.out),
           "bounds": {"max_works": 16, "max_page_bytes": 262144, "max_output_bytes": 2097152},
           "works": [{"work_id": "A", "page": f"{BOOK}/{A}/05.01.md", "pass": "05.01", "member": "0101.demo-a-0501",
                      "goal": {"goal_id": "gA", "statement": "SYNTHETIC goal A."}, "agreement": AGREEMENT,
                      "review_location": f"{BOOK}/{A}/evidence/prime-cycle-reviews/05.01"}]}
    regp = r.write_input("registration.json", reg)
    # ---- 2. Worker retrieves; nothing is released yet
    r.view("2  worker view: assigned, not released", "--as", WORKER, check=expect_state("0101.demo-a-0501", "awaiting-release", "director"))
    r.call("2b construct batch page A again (exists) is refused", DESK,
           ["construct", "--template", "batch-page/1", "--input", r.inputs / "a-page.json", "--target", r.page_path(A),
            "--expect-sha256", "absent", "--write"], 2)
    # ---- 3. Release and claim recorded on the page by construction
    r.call("3a record the Director release (constructed line)", DESK,
           ["construct", "--template", "return-pointer/1", "--input", r.write_input("a-release.json",
            {"template": "return-pointer/1", "kind": "release", "by": "the Director (SYNTHETIC)", "date": "2026-10-31",
             "quote": "Run loop A. Capture as 0101.demo-a-0501."}), "--target", r.page_path(A),
            "--expect-sha256", r.page_sha(A), "--write"], 0)
    r.view("3b worker view: released", "--as", WORKER, check=expect_state("0101.demo-a-0501", "released", WORKER))
    r.call("3c stale compare-and-swap: claim with an old page hash is refused", DESK,
           ["construct", "--template", "return-pointer/1", "--input", r.write_input("a-claim.json",
            {"template": "return-pointer/1", "kind": "claim", "actor": WORKER, "at_commit": None, "scope": "this batch only"}),
            "--target", r.page_path(A), "--expect-sha256", "0" * 64, "--write"], 2)
    r.call("3d worker claims (compute binds the assignment hash)", DESK,
           ["construct", "--template", "return-pointer/1", "--input", r.inputs / "a-claim.json", "--target", r.page_path(A),
            "--expect-sha256", r.page_sha(A), "--write"], 0)
    # ---- 4. Missing return is not done
    r.view("4a worker view: claimed, no return (not done)", check=expect_state("0101.demo-a-0501", "claimed", WORKER))
    r.call("4b prime_cycle read: claimed work is not awaiting review or reviewed", PC, ["read", "--registration", regp, "--json"], (0, 1),
           lambda o, e: (lambda w: (f"FAIL {w['pass_state']}" if w["pass_state"] in ("awaiting-review", "reviewed") else
                                    f"{w['pass_state']} (custody {w['custody']['state']}: {w['custody']['state_reason']})"))(json.loads(o)["works"][0]))
    # ---- 5. Worker returns into durable custody
    ev = r.book / A / "evidence" / "build05.01"
    ev.mkdir(parents=True)
    (ev / "out.md").write_bytes(b"SYNTHETIC out: one change described.\n")
    (ev / "submission.md").write_bytes(b"Did: wrote out.md (SYNTHETIC).\nBlocked: nothing.\nNeed: Prime review.\n")
    capture_args = ["capture", "--book", r.book, "--submission", "syn-a-0501", "--return-file", ev / "submission.md",
                    "--source-root", r.repo, "--artifact", f"{BOOK}/{A}/evidence/build05.01/out.md|out.md"]
    r.call("5a worker captures the return (existing helper)", RC, capture_args, 0)
    r.call("5b verify in a fresh process", RC, ["verify", "--book", r.book, "--member", "0101.demo-a-0501"], 0,
           lambda o, e: True if "result complete" in o else "FAIL no result complete")
    r.call("5c compute writes the Execution line from the inspected receipt", DESK,
           ["construct", "--template", "return-pointer/1", "--input", r.write_input("a-exec.json",
            {"template": "return-pointer/1", "kind": "execution", "by": WORKER, "member": "0101.demo-a-0501",
             "summary": "SYNTHETIC: wrote out.md. Prime reviews."}), "--target", r.page_path(A),
            "--expect-sha256", r.page_sha(A), "--repo", r.repo, "--write"], 0)
    # ---- 6. Repeated and changed handback
    before = tree_digest(r.book / "0101.demo-a-0501")
    r.call("6a identical handback: already-captured, nothing written", RC, capture_args, 0,
           lambda o, e: True if tree_digest(r.book / "0101.demo-a-0501") == before else "FAIL member changed")
    (ev / "out.md").write_bytes(b"SYNTHETIC out: CHANGED after capture.\n")
    r.call("6b changed handback under the same submission: conflict, nothing written", RC, capture_args, 2,
           lambda o, e: True if tree_digest(r.book / "0101.demo-a-0501") == before else "FAIL member changed")
    # ---- 7. Prime retrieves and reviews
    r.view("7a Prime view: awaiting review", "--as", WORKER, "--registration", regp,
           check=expect_state("0101.demo-a-0501", "awaiting-review", PRIME))
    tdir = r.out / "templates"  # prime_cycle requires templates under output_root (run1 kept: refused)
    r.call("7b prime_cycle read writes the decision template", PC, ["read", "--registration", regp, "--templates", tdir], (0, 1))
    t = json.loads((tdir / "template-A.json").read_text(encoding="utf-8"))
    dec = r.write_input("decision-A.json", fill_decision(t, "accept"))
    r.call("7c Prime records the typed review (prime_cycle record)", PC, ["record", "--registration", regp, "--decision", dec], (0, 1))
    r.view("7d view after the typed review: reviewed, next action shown", "--registration", regp,
           check=expect_state("0101.demo-a-0501", "reviewed"))
    review_dir = r.repo / BOOK / A / "evidence" / "prime-cycle-reviews" / "05.01" / t["review_id"]
    # ---- 8. Construct the page Review section from the typed record; observe the binding conflict
    r.call("8a compute writes the page Review section from record.json", DESK,
           ["construct", "--template", "review-section/1", "--input", r.write_input("a-review.json",
            {"template": "review-section/1", "by": PRIME, "date": "2026-10-31", "summary": "SYNTHETIC: meets its scope.",
             "record": str(review_dir)}), "--target", r.page_path(A), "--expect-sha256", r.page_sha(A), "--repo", r.repo, "--write"], 0)
    r.view("8b FINDING: writing the Review section makes the typed review stale (whole-page binding)", "--registration", regp,
           check=expect_state("0101.demo-a-0501", "review-stale", PRIME))
    r.call("8c a second Review construction over existing text is refused (no silent rewrite)", DESK,
           ["construct", "--template", "review-section/1", "--input", r.inputs / "a-review.json", "--target", r.page_path(A),
            "--expect-sha256", r.page_sha(A), "--repo", r.repo, "--write"], 2)
    # ---- 9. Restart: two fresh processes derive the same state from files only
    v1 = r.view("9a restart: fresh-process view 1", "--registration", regp)
    v2 = r.view("9b restart: fresh-process view 2", "--registration", regp,
                check=lambda o, e: True if json.loads(o)["state_digest"] == v1["state_digest"] else "FAIL digests differ")
    # ---- 10. Stale assignment after claim, interrupted capture, superseded return
    r.call("10a Prime: construct batch page B", DESK,
           ["construct", "--template", "batch-page/1", "--input", r.write_input("b-page.json",
            batch_input(B, "0102.demo-b-0501", "syn-b-0501", "SYNTHETIC stale B")), "--target", r.page_path(B),
            "--expect-sha256", "absent", "--write"], 0)
    r.call("10b reserve member B", RC,
           ["reserve", "--book", r.book, "--submission", "syn-b-0501", "--name", "demo-b-0501", "--origin-book", "00.00.10.work",
            "--origin-page", B, "--origin-batch", "05.01", "--expected-output", "out.md", "--submitter", WORKER,
            "--reviewer", PRIME, "--release", "Reservation only."], 0)
    for kind, inp in (("release", {"template": "return-pointer/1", "kind": "release", "by": "the Director (SYNTHETIC)",
                                   "date": "2026-10-31", "quote": "Run B."}),
                      ("claim", {"template": "return-pointer/1", "kind": "claim", "actor": WORKER, "at_commit": None, "scope": "B only"})):
        r.call(f"10c construct B {kind}", DESK, ["construct", "--template", "return-pointer/1", "--input",
               r.write_input(f"b-{kind}.json", inp), "--target", r.page_path(B), "--expect-sha256", r.page_sha(B), "--write"], 0)
    pb = r.page_path(B)
    pb.write_bytes(pb.read_bytes().replace(b"SYNTHETIC: write out.md", b"SYNTHETIC: write out.md AND a second file"))
    r.view("10d assignment edited after claim: attention, stays claimed", "--member", "0102.demo-b-0501",
           expect=1, check=lambda o, e: True if any("assignment-changed-after-claim" in x for x in
                                                     task(json.loads(o), "0102.demo-b-0501")["attention"]) else "FAIL no attention")
    evb = r.book / B / "evidence" / "build05.01"
    evb.mkdir(parents=True)
    (evb / "out.md").write_bytes(b"SYNTHETIC B out.\n")
    (evb / "submission.md").write_bytes(b"Did: B.\nBlocked: nothing.\nNeed: review.\n")
    helper = r.inputs / "interrupt_capture.py"
    helper.write_bytes(("import hashlib,importlib.util,sys\n"
                        f"p={str(RC)!r}\n"
                        "assert hashlib.sha256(open(p,'rb').read()).hexdigest()=='8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac'\n"
                        "s=importlib.util.spec_from_file_location('rc_pinned',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)\n"
                        # string paths, as the CLI passes them (run4 passed Path objects and was refused, nothing written)
                        "res=m.capture(sys.argv[1],'syn-b-0501',sys.argv[2],sys.argv[3],[sys.argv[4]],interrupt='before-receipt')\n"
                        "sys.stdout.write(res.text)\nsys.exit(res.code)\n").encode())
    r.call("10e interrupted capture (helper's own before-receipt point): partial retained", helper,
           [r.book, evb / "submission.md", r.repo, f"{BOOK}/{B}/evidence/build05.01/out.md|out.md"], 2,
           lambda o, e: True if "interrupted before-receipt" in o else "FAIL no partial reported")
    r.view("10f view: partial capture is a custody problem, not a return", "--member", "0102.demo-b-0501", expect=1,
           check=expect_state("0102.demo-b-0501", "custody-problem", "prime"))
    r.call("10g amended return: new submission supersedes A", RC,
           ["reserve", "--book", r.book, "--submission", "syn-a-0501-r2", "--name", "demo-a-0501-r2", "--origin-book",
            "00.00.10.work", "--origin-page", A, "--origin-batch", "05.01", "--expected-output", "out.md", "--submitter", WORKER,
            "--reviewer", PRIME, "--release", "Reservation only; amendment.", "--supersedes", "0101.demo-a-0501"], 0)
    r.view("10h view: A's first member is superseded, successor waits for capture", expect=(0, 1),
           check=lambda o, e: (lambda v: True if task(v, "0101.demo-a-0501")["state"] == "superseded"
                               and task(v, "0103.demo-a-0501-r2")["state"] in ("released", "claimed")
                               else f"FAIL {task(v, '0101.demo-a-0501')['state']} / {task(v, '0103.demo-a-0501-r2')['state']}")(json.loads(o)))
    # ---- 11. Guard: construction never touches the shared checkout
    r.call("11 construct into the shared checkout is refused", DESK,
           ["construct", "--template", "batch-page/1", "--input", r.inputs / "a-page.json",
            "--target", LABS.parent / BOOK / "0599.never" / "05.01.md", "--expect-sha256", "absent"], 2)
    r.view("12 final human view", expect=(0, 1))
    code, out, err = r.call("12b final text view", DESK, ["view", "--repo", r.repo, "--registration", regp], (0, 1))
    print(out)


def main():
    keep = "--keep" in sys.argv
    tpath = Path(sys.argv[sys.argv.index("--transcript") + 1]) if "--transcript" in sys.argv else None
    r = Run()
    aborted = None
    try:
        scenarios(r)
    except Exception as e:  # an aborted demo is recorded, never reported as success
        aborted = f"{type(e).__name__}: {e}"
        print(f"ABORTED: {aborted}")
    finally:
        held = sum(s["expectation_held"] for s in r.steps)
        print(f"expectations held: {held} of {len(r.steps)}" + (f"; aborted: {aborted}" if aborted else ""))
        if tpath:
            tpath.write_bytes((json.dumps({"schema": "desk-lab-demo-transcript/1",
                                           "label": "SYNTHETIC tasks, returns and decisions; disposable repository; no model",
                                           "python": sys.version.split()[0], "held": held, "aborted": aborted, "steps": r.steps},
                                          ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
        r.close(keep)
    return 0 if held == len(r.steps) and not aborted else 1


if __name__ == "__main__":
    sys.exit(main())
