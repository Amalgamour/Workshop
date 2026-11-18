"""Bounded demonstration of the Colab review adapter (0518.colab-review 05.01). Every step runs a real CLI in a new process.

  python -B demo.py --out ABS_NEW_DIR

Disposable source repository and book; pinned producer v2, workflow v2, helper, inspector and readiness checker; SYNTHETIC
reviewer results and synthesis only. No model, reviewer or session is launched. Writes OUT/transcript.json and
OUT/sample-review.json (the derived report with mappings back to the immutable fixture inputs).
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent
sys.path.insert(0, str(LAB / "tests"))
import fixture as F  # noqa: E402

READINESS = F.WS / "labs/colab-readiness-pass01/colab_readiness.py"
sha = lambda b: hashlib.sha256(b).hexdigest()


def main():
    out = Path(sys.argv[sys.argv.index("--out") + 1])
    out.mkdir(parents=False, exist_ok=False)
    d = F.Desk(prefix="crv-demo-")
    steps = []

    def step(label, tool, *args, expect):
        code, body, err = F.run(tool, *args)
        raw = (json.dumps(body, indent=1, sort_keys=True) if isinstance(body, dict) else str(body)).encode("utf-8")
        name = f"{len(steps) + 1:02d}.json"
        (out / name).write_bytes(raw.replace(str(d.tmp).encode("utf-8"), b"<desk>").replace(str(d.tmp).replace("\\", "\\\\").encode("utf-8"), b"<desk>"))
        steps.append({"step": label, "tool": Path(tool).name, "argv": [str(a).replace(str(d.tmp), "<desk>") for a in args], "exit": code,
                      "expected_exit": expect, "stdout": name, "stderr": err[-500:].replace(str(d.tmp), "<desk>")})
        print(f"{label}: exit {code} (expected {expect})")
        return code, body
    try:
        plan = d.plan()
        pp = d.write("plan.json", F.canonical(plan))
        pb = pp.read_bytes()
        step("stage review sources and compose colab-request/2", F.ADAPTER, "stage", "--plan", pp, "--request", d.write("base-request.json", d.base_request()),
             "--repo", d.repo, "--out-request", d.path("request.json"), expect=0)
        _, prev = step("producer v2 preview", F.PRODUCER, "preview", "--request", d.path("request.json"), "--config", d.config, "--json", expect=0)
        digest = prev["digest"]
        step("producer v2 prepare", F.PRODUCER, "prepare", "--request", d.path("request.json"), "--config", d.config, "--output", d.path("producer-out"),
             "--digest", digest, "--json", expect=0)
        step("bind: review files inside the verified package", F.ADAPTER, "bind", "--output", d.path("producer-out"), "--config", d.config,
             "--producer", F.PRODUCER, "--expect-digest", digest, "--out", d.path("binding"), "--plan", pp, expect=0)
        req = json.loads(d.path("request.json").read_text(encoding="utf-8"))
        op = d.write("open.json", {"book": F.BOOK, "page": F.PAGE, "pass": F.PASS, "schema": "colab-exchange-open/1",
                                   "targets": req["binding"]["targets"], "title": req["title"]})
        step("workflow v2 open", F.WORKFLOW, "open", "--book", d.book, "--request", op, "--closure", d.path("producer-out"), expect=0)
        step("workflow v2 attach", F.WORKFLOW, "attach", "--book", d.book, "--page", F.PAGE, "--pass", F.PASS, "--output", d.path("producer-out"),
             "--config", d.config, "--expect-digest", digest, expect=0)
        R = d.result
        specs = [("r01-s01", R(pb, "R01", "S01")), ("r02-s01", R(pb, "R02", "S01")),
                 ("r01-s02", R(pb, "R01", "S02", ["SYNTHETIC: section 2 conflates two terms."], comprehension=False)),
                 ("r02-s02", R(pb, "R02", "S02", ["SYNTHETIC: section 2 conflates two terms.", "SYNTHETIC: the fallback path is untested."],
                               comprehension=False))]
        members = [d.capture(d.path("producer-out"), n, r) for n, r in specs]
        steps.append({"step": "reserve and capture four SYNTHETIC results (helper reserve, producer intake)", "members": members,
                      "result_sha256": {m: sha(F.canonical(r)) for m, (_, r) in zip(members, specs)}})
        step("workflow v2 place-return (R01 S01)", F.WORKFLOW, "place-return", "--book", d.book, "--page", F.PAGE, "--pass", F.PASS,
             "--member", members[0], "--config", d.config, expect=0)
        args = ["intake", "--binding", d.path("binding") / "binding.json", "--plan", pp, "--book", d.book, "--config", d.config, "--out", d.path("intake")]
        for m in members:
            args += ["--member", m]
        _, intake = step("adapter intake (S03 optional, not run)", F.ADAPTER, *args, expect=0)
        isha = sha((d.path("intake") / "intake.json").read_bytes())
        synth = {"schema": "colab-review-synthesis/1", "plan_id": "plan-1", "intake_sha256": isha, "by": "Codex Prime (SYNTHETIC)", "label": "SYNTHETIC",
                 "items": [{"id": "X01", "title": "SYNTHETIC: terminology", "findings": ["R01-S02-F01", "R02-S02-F01"],
                            "recommendation": "SYNTHETIC: define both terms once."}],
                 "retained": [{"finding": "R02-S02-F02", "disposition": "minority", "reason": "SYNTHETIC: one reader only; kept open", "of": None}],
                 "disagreements": [{"findings": ["R02-S02-F02"], "text": "SYNTHETIC: R01 did not raise this risk."}], "incomplete": [],
                 "residual_uncertainty": ["SYNTHETIC: isolation is unknown for both readers."], "acceptance": None}
        _, report = step("adapter synthesize", F.ADAPTER, "synthesize", "--intake", d.path("intake") / "intake.json", "--synthesis",
                         d.write("synthesis.json", synth), "--out", d.path("report"), expect=0)
        lost = dict(synth, retained=[])
        step("adapter synthesize: a lost original finding is refused as inconsistent", F.ADAPTER, "synthesize", "--intake",
             d.path("intake") / "intake.json", "--synthesis", d.write("synthesis-lost.json", lost), "--out", d.path("report-lost"), expect=1)
        review = {"schema": "colab-exchange-review/1", "by": "Codex Prime (SYNTHETIC)", "on": "2026-10-31",
                  "assessment": "SYNTHETIC review record; derived report " + report["report_digest"][:16] + " was consulted.",
                  "findings": [{"id": "F01", "consequential": False, "observation": "SYNTHETIC: X01 terminology", "source_binding": "T01",
                                "disposition": "adopted", "director_reply": "hypothetical-fixture: none sought", "pending": False, "reason": "SYNTHETIC"},
                               {"id": "F02", "consequential": True, "observation": "SYNTHETIC: minority finding R02-S02-F02 kept open", "source_binding": "T01",
                                "disposition": "held", "director_reply": "hypothetical-fixture: none sought", "pending": True, "reason": "SYNTHETIC"}],
                  "pending_questions": ["SYNTHETIC: is the fallback path in scope?"], "route": "hold", "next_pass": None}
        step("workflow v2 record-review (Prime-supplied SYNTHETIC record)", F.WORKFLOW, "record-review", "--book", d.book, "--page", F.PAGE,
             "--pass", F.PASS, "--review", d.write("review.json", review), expect=0)
        pkg = d.path("producer-out") / "package"
        files = sorted(p for p in pkg.rglob("*") if p.is_file())
        transport = [{"path": p.relative_to(pkg).as_posix(), "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size} for p in files]
        pack = next(t for t in transport if t["path"] == "05.01.pack.md")
        cat = lambda c, req_, refs, reason: {"category": c, "applicability": "required" if req_ else "not-applicable", "reason": reason, "refs": refs}
        rr = {"schema": "colab-readiness-request/1",
              "purpose": {"statement": "SYNTHETIC: declared-record check of one prepared package", "mode": "read-only",
                          "question": "Is the declared delivery intact and accounted?", "role": "fixture", "method": "read the package",
                          "finish_boundary": "readiness report only"},
              "surface": {"kind": "zip-only", "os": "unknown", "interpreter": "none required", "network": "denied", "install": "denied",
                          "secrets": "none", "read_roots": [str(pkg)], "write_roots": []},
              "delivery_root": str(pkg), "output": str(d.path("readiness")), "transport": transport,
              "entry_points": [{"id": "pack", "path": "05.01.pack.md"}],
              "dependencies": [{"id": "pack", "path": "05.01.pack.md", "sha256": pack["sha256"], "bytes": pack["bytes"], "role": "source-under-review",
                                "required": True, "needed_by": [], "invokes": [], "supply": "supplied", "condition": None, "withhold_reason": None}],
              "evidence": [cat("task-criteria", True, ["sources"], "the review plan and prompts are bound sources"),
                           cat("director-constraints", False, [], "SYNTHETIC fixture: no Director wording"),
                           cat("return-work-custody", False, [], "custody is checked by the workflow, not this read-only check"),
                           cat("contract-code", False, [], "no code is delivered"), cat("tests-evidence", False, [], "no tests are delivered"),
                           cat("source-index", True, ["sources"], "the package source manifest"),
                           cat("capabilities", False, [], "read-only package"), cat("fallback", False, [], "read-only package"),
                           cat("return-route", False, [], "declared in the request text")],
              "references": [{"id": "sources", "format": "prime-pack-sources/1", "path": "source-manifest.json", "follow_nested": False}],
              "withholds": [],
              "smoke": {"status": "not-applicable", "reason": "read-only declared-record check", "command": None, "child_exit": None, "wrapper_exit": None,
                        "expected_state": None, "observed_state": None, "cutoff": "none", "in_flight": [], "manual_fallback": False, "label": "none",
                        "page_sha256": None, "receipt_sha256": None, "pass_state_before": None, "pass_state_after": None, "custody": None,
                        "judgment_label": None, "journal_operations": []},
              "failure_policy": {"declared": True, "retain_first_failure": True, "diagnostic": "report problems", "dependency_check": "declared rows",
                                 "manual_fallback": "none"},
              "independent_checks": [], "bounds": {"max_files": 1000, "max_file_bytes": 2000000, "max_total_bytes": 20000000}}
        step("accepted readiness checker on the exact package (declared-record capability only)", READINESS, "check", "--request",
             d.write("readiness-request.json", rr), expect=0)
        rd = json.loads((d.path("readiness") / "readiness.json").read_text(encoding="utf-8"))
        page = d.book / F.PAGE
        sample = {"schema": "colab-review-sample/1",
                  "label": "SYNTHETIC: an actual observed derived result from SYNTHETIC supplied reviewer results; no model was run",
                  "report": report, "report_json_sha256": sha((d.path("report") / "report.json").read_bytes()),
                  "mappings": {"plan_sha256": sha(pb), "producer_digest": digest, "binding_sha256": sha((d.path("binding") / "binding.json").read_bytes()),
                               "intake_sha256": isha,
                               "members": [{"member": r["member"], "receipt_sha256": r["receipt_sha256"], "result_sha256": r["result_sha256"],
                                            "reviewer": r["result"]["reviewer"], "stage": r["result"]["stage"]} for r in intake["results"]],
                               "placed_return": {"member": members[0], "workflow_return_sha256": sha((page / "05.01.return.md").read_bytes()),
                                                 "member_return_sha256": sha((d.book / members[0] / "return.md").read_bytes())},
                               "workflow_review_md_sha256": sha((page / "06.01.review.md").read_bytes())},
                  "readiness": {k: rd[k] for k in ("ready_for_declared_method", "transport_valid", "runtime_dependencies_resolved",
                                                    "evidence_references_resolved", "minimum_evidence_satisfied", "semantic_sufficiency", "independent_proof")},
                  "limits": ["only R01 S01's return is placed: the workflow places one return per pass; the other three stay in their N1 members",
                             "readiness is a declared-record check of the package bytes; it establishes no semantic quality and no smoke"]}
        (out / "sample-review.json").write_text(json.dumps(sample, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
        (out / "REPORT.md").write_bytes((d.path("report") / "REPORT.md").read_bytes())
        (out / "06.01.review.md").write_bytes((page / "06.01.review.md").read_bytes())
    finally:
        d.close()
    ok = all(s.get("exit") == s.get("expected_exit") for s in steps if "exit" in s)
    (out / "transcript.json").write_text(json.dumps({"schema": "colab-review-demo/1", "steps": steps, "all_exits_as_expected": ok}, indent=1) + "\n",
                                         encoding="utf-8")
    print("all exits as expected:", ok)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
