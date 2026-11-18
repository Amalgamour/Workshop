"""Disposable fixtures for colab_review: a local git source repository (task-local identity), a disposable book, a colab-config/2,
a valid colab-request/2, a review plan and SYNTHETIC reviewer results. Every tool runs through its pinned documented CLI.
Nothing here launches a model or writes the workshop tree."""
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
WS = LAB.parent.parent
ADAPTER = LAB / "colab_review.py"
PRODUCER = WS / "labs/colab-support-pass02/colab_support.py"
WORKFLOW = WS / "labs/colab-workflow-pass02/colab_workflow.py"
HELPER = WS / "labs/return-capture-pass01/return_capture.py"
INSPECTOR = WS / "labs/return-capture-pass01/return_inspect.py"
PAGE, PASS, BOOK = "0702.colab-review-fixture", "05.01", "00.00.10.work"
SUBJECT = f"00.kernel/{BOOK}/0599.synthetic-subject/01.md"
GIT_ID = ["-c", "user.name=colab-review fixture", "-c", "user.email=fixture@localhost", "-c", "commit.gpgsign=false"]
sha = lambda b: hashlib.sha256(b).hexdigest()


def canonical(v) -> bytes:
    return (json.dumps(v, sort_keys=True, indent=1, ensure_ascii=False) + "\n").encode("utf-8")


def writable_retry(func, path, exc):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def run(*argv, timeout=600):
    p = subprocess.run([sys.executable, "-B", *map(str, argv)], capture_output=True, timeout=timeout, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    out = p.stdout.decode("utf-8", "replace")
    body = json.loads(out) if out.startswith("{") else out
    return p.returncode, body, p.stderr.decode("utf-8", "replace")


class Desk:
    def __init__(self, prefix="crv-"):
        self.tmp = Path(tempfile.mkdtemp(prefix=prefix))
        self.repo = self.tmp / "src"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        (self.repo / SUBJECT).parent.mkdir(parents=True)
        (self.repo / SUBJECT).write_bytes(b"# 01 - SYNTHETIC subject\n\nA fixture design page under review. Not real work.\n")
        self.git("add", "-A")
        self.git("commit", "-q", "-m", "SYNTHETIC subject")
        self.book = self.tmp / "book"
        self.book.mkdir()
        self.config = self.tmp / "config.json"
        self.config.write_bytes(canonical({
            "schema": "colab-config/2", "python": sys.executable, "repositories": {"fixture": str(self.repo)},
            "assembler": str(WS / "labs/pack-assembly-pass01/pack_assembly.py"), "checker": str(WS / "labs/pack-custody-pass01/pack_check.py"),
            "helper": str(HELPER), "inspector": str(INSPECTOR), "producer_v1": str(WS / "labs/colab-support-pass01/colab_support.py")}))

    def close(self):
        shutil.rmtree(self.tmp, onexc=writable_retry)

    def git(self, *a):
        return subprocess.run(["git", "-C", str(self.repo), *GIT_ID, *a], capture_output=True, check=True).stdout.decode().strip()

    def path(self, name):
        return self.tmp / name

    def write(self, name, value):
        p = self.tmp / name
        p.write_bytes(value if isinstance(value, bytes) else canonical(value))
        return p

    def base_request(self):
        commit = self.git("rev-parse", "HEAD")
        return {
            "schema": "colab-request/2",
            "binding": {"schema": "colab-binding/1", "investigation": {"book": BOOK, "page": PAGE, "pass": PASS},
                        "targets": [{"id": "T01", "book": BOOK, "page": "0599.synthetic-subject", "file": "01.md", "section": None,
                                     "source": {"repository": "fixture", "commit": commit, "path": SUBJECT,
                                                "sha256": sha((self.repo / SUBJECT).read_bytes())}}]},
            "title": "SYNTHETIC review of a fixture design page", "date": "2026-10-31", "author": "Codex Prime (SYNTHETIC fixture)",
            "recipient": "SYNTHETIC reviewer, unassigned", "reviewer": "Codex Prime", "mode": "open-design", "scoring": {"state": "unscored"},
            "context": "A SYNTHETIC fixture design page. The review plan and prompts are included as required sources.",
            "question": "Explain the design first, then report findings, following the review plan.",
            "why": "Fixture: proves the review plan and prompts survive preparation and verification.",
            "built_state": "Nothing is built; this is a fixture.", "known_gaps": ["SYNTHETIC fixture only."],
            "method": "Read COMPREHENSION.md and answer it before any finding; fill RESULT-TEMPLATE.json.",
            "cases": [{"id": "C01", "text": "Explain what the subject proposes, then list findings, if any."}],
            "environment": {"kind": "zip-only", "read": "the files in this package only", "write": "your one return file",
                            "execute": "nothing is required", "network": "not required"},
            "permissions": ["Read every file in the package."], "stop": ["Stop if a snapshot does not match its sha256."],
            "prior_involvement": "None for a SYNTHETIC fixture reviewer.", "required_sources": [], "withheld": [], "unavailable": [],
            "director_replies": [], "return_route": {"destination": "the reserved N1 member for this pass", "submission_hint": "SYNTHETIC"},
            "preparation_notes": ["SYNTHETIC fixture request for the colab-review adapter tests."]}

    def plan(self, **over):
        ctx = {"conversation_supplied": "none", "host_context": "SYNTHETIC: none declared", "familiarity": "SYNTHETIC: none", "isolation": "unknown"}
        p = {"schema": "colab-review-plan/1", "plan_id": "plan-1", "investigation": {"book": BOOK, "page": PAGE, "pass": PASS},
             "mode": "combination",
             "reviewers": [{"id": "R01", "label": "SYNTHETIC reader one", "context": dict(ctx)},
                           {"id": "R02", "label": "SYNTHETIC reader two", "context": dict(ctx)}],
             "stages": [{"id": "S01", "kind": "comprehension", "reviewers": ["R01", "R02"], "required": True},
                        {"id": "S02", "kind": "critique", "reviewers": ["R01", "R02"], "required": True},
                        {"id": "S03", "kind": "simplicity", "reviewers": ["R01"], "required": False}],
             "ordered": True, "read_scope": ["the package files only"], "withheld": [{"item": "SYNTHETIC: other drafts", "reason": "unreviewed"}],
             "finish_boundary": "a return per stage; Prime synthesizes; the Director decides any design fork",
             "simplicity": {"before": "SYNTHETIC design v1", "after": "SYNTHETIC design v2", "fixes_under_review": ["F-A"]},
             "round": {"number": 1, "cap": 2}}
        p.update(over)
        return p

    def result(self, plan_bytes, reviewer, stage, findings=(), status="completed", comprehension=True, simplicity=None, **over):
        r = {"schema": "colab-review-result/1", "plan_id": "plan-1", "plan_sha256": sha(plan_bytes), "reviewer": reviewer, "stage": stage,
             "status": status,
             "context": {"conversation_supplied": "none", "host_context": "SYNTHETIC: none declared", "familiarity": "SYNTHETIC: none", "isolation": "unknown"},
             "comprehension": ({"proposed": f"SYNTHETIC {reviewer}: the page proposes a fixture design.",
                                "current_system": "SYNTHETIC: nothing exists yet.", "task_authority": "SYNTHETIC: Prime reviews; the Director decides forks.",
                                "handback_route": "SYNTHETIC: one return in the reserved member."} if comprehension else None),
             "findings": [{"id": f"{reviewer}-{stage}-F{n:02d}", "target": "T01", "location": "SYNTHETIC section", "text": t} for n, t in enumerate(findings, 1)],
             "simplicity": simplicity, "label": "SYNTHETIC"}
        r.update(over)
        return r

    # ---- the supported route ----
    def stage(self, plan, name="plan.json"):
        pb = canonical(plan)
        pp = self.write(name, pb)
        rq = self.write("base-request.json", self.base_request())
        out = self.path("request.json")
        code, body, err = run(ADAPTER, "stage", "--plan", pp, "--request", rq, "--repo", self.repo, "--out-request", out)
        return code, body, pp, out

    def prepare(self, request, name="producer-out"):
        code, body, err = run(PRODUCER, "preview", "--request", request, "--config", self.config, "--json")
        assert code == 0, (body, err)
        digest = body["digest"]
        out = self.path(name)
        code, body, err = run(PRODUCER, "prepare", "--request", request, "--config", self.config, "--output", out, "--digest", digest, "--json")
        assert code == 0, (body, err)
        return out, digest

    def bind(self, output, digest, plan=None, name="binding"):
        args = ["bind", "--output", output, "--config", self.config, "--producer", PRODUCER, "--expect-digest", digest, "--out", self.path(name)]
        return run(ADAPTER, *args, *(["--plan", plan] if plan else []))

    def open_attach(self, request_path, output, digest):
        req = json.loads(request_path.read_text(encoding="utf-8"))
        op = self.write("open.json", {"book": BOOK, "page": PAGE, "pass": PASS, "schema": "colab-exchange-open/1",
                                      "targets": req["binding"]["targets"], "title": req["title"]})
        c1, b1, e1 = run(WORKFLOW, "open", "--book", self.book, "--request", op, "--closure", output)
        c2, b2, e2 = run(WORKFLOW, "attach", "--book", self.book, "--page", PAGE, "--pass", PASS, "--output", output, "--config", self.config,
                         "--expect-digest", digest)
        return (c1, b1, e1), (c2, b2, e2)

    def new_book(self, name):
        b = self.tmp / name
        b.mkdir()
        return b

    def capture(self, output, name, result_value, body_text=None, book=None, artifact="review-result.json"):
        book = book or self.book
        code, out, err = run(HELPER, "reserve", "--book", book, "--submission", f"fx-{name}", "--name", name, "--origin-book", BOOK,
                             "--origin-page", PAGE, "--origin-batch", PASS, "--expected-output", artifact, "--submitter", "SYNTHETIC fixture",
                             "--reviewer", "Codex Prime", "--release", "SYNTHETIC fixture reservation")
        assert code == 0, (out, err)
        member = next(p.name for p in book.iterdir() if p.name.endswith("." + name))
        src = self.tmp / f"src-{name}"
        src.mkdir()
        (src / artifact).write_bytes(result_value if isinstance(result_value, bytes) else canonical(result_value))
        ret = src / "return.md"
        ret.write_bytes((body_text or f"# SYNTHETIC return {name}\n\nLabelled fixture. Not a model result.\n").encode("utf-8"))
        code, body, err = run(PRODUCER, "intake", "--output", output, "--config", self.config, "--book", book, "--member", member,
                              "--return-file", ret, "--source-root", src, "--artifact", f"{artifact}|{artifact}", "--json")
        assert code == 0 and body.get("result") == "captured", (body, err)
        return member

    def intake(self, binding_dir, plan_path, members, name="intake", book=None):
        args = ["intake", "--binding", binding_dir / "binding.json", "--plan", plan_path, "--book", book or self.book, "--config", self.config, "--out", self.path(name)]
        for m in members:
            args += ["--member", m]
        return run(ADAPTER, *args)

    def synthesize(self, intake_dir, synthesis, name="report"):
        sp = self.write(f"{name}-synthesis.json", synthesis)
        return run(ADAPTER, "synthesize", "--intake", intake_dir / "intake.json", "--synthesis", sp, "--out", self.path(name))


def route(d: Desk, plan=None):
    """stage -> preview/prepare (pinned producer) -> bind; returns (plan_path, plan_bytes, request, output, digest, binding_dir)."""
    p = plan or d.plan()
    code, body, pp, req = d.stage(p)
    assert code == 0, body
    output, digest = d.prepare(req)
    code, body, err = d.bind(output, digest, pp)
    assert code == 0, (body, err)
    return pp, pp.read_bytes(), req, output, digest, d.path("binding")
