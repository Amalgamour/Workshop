"""Builds dependencies.json from pins.raw.json (AST-extracted) plus hand-recorded discovered edges with line evidence.
Reads only; executes nothing from the source room."""
import json, os, hashlib
SR = "/workspace/prima/run0502/source-room"
A2 = "/workspace/prima/run0502/workers/A2"
pins = json.load(open(A2 + "/probes/pins.raw.json"))
def meas(rel):
    p = os.path.join(SR, rel)
    if not os.path.isfile(p): return {"path": rel, "present_in_room": False, "sha256": None, "bytes": None}
    b = open(p, "rb").read(); return {"path": rel, "present_in_room": True, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
# discovered edges: (from, to, mechanism, root_used, evidence, dep_class, on_v7_review_loop_path)
E = [
 ("app/librarian.py","app/review_loop_tools_v7.py","in-process exec (importlib load_module)","Path(__file__).parent","app/librarian.py:36-42,103","code-execution",True),
 ("app/review_loop_tools_v7.py","app/review-loop-v7.json","read + strict schema check","code_root = librarian parent.parent","app/review_loop_tools_v7.py:125-152,226","source-data",True),
 ("app/review_loop_tools_v7.py","app/review_loop_tools_v4.py","in-process exec for fixture/describe-legacy/V4 commands","code_root","app/review_loop_tools_v7.py:192-201,236-255","code-execution",True),
 ("app/review_loop_tools_v7.py","labs/workbook-review-pass03/workbook.py","subprocess [sys.executable,-B,script,*args], cwd=code_root","code_root","app/review_loop_tools_v7.py:204-219,246-249","code-execution",True),
 ("app/review_loop_tools_v4.py","labs/review-loop-pass03/review_loop.py","subprocess, cwd=code_root","code_root (v4 also defines CHECKOUT=D:\\Git\\lib-build line 28)","app/review_loop_tools_v4.py:28,338-346","code-execution",True),
 ("labs/workbook-review-pass03/workbook.py","labs/workbook-review-pass02/workbook.py","in-process exec at import (load_pass02)","FIXED REPO=D:\\Git\\lib-build","labs/workbook-review-pass03/workbook.py:21-24,51-64","code-execution",True),
 ("labs/workbook-review-pass03/workbook.py","labs/workbook-review-pass03/forms/workbook-review-v1.json","read via wb.FORM_REL override; PINS['form'] digest None","FIXED REPO","labs/workbook-review-pass03/workbook.py:25,503-504; labs/workbook-review-pass01/workbook.py:207-215,876-877","source-data",True),
 ("labs/workbook-review-pass02/workbook.py","labs/workbook-review-pass01/workbook.py","in-process exec at import (load_pass01)","FIXED REPO=D:\\Git\\lib-build","labs/workbook-review-pass02/workbook.py:20-21,44-48","code-execution",True),
 ("labs/workbook-review-pass01/workbook.py","labs/return-access-pass01/return_access.py","subprocess via PINS/call_json, cwd=REPO","FIXED REPO","labs/workbook-review-pass01/workbook.py:22,31-60,207-215,611-617","code-execution",True),
 ("labs/workbook-review-pass01/workbook.py","labs/review-loop-pass03/review_loop.py","subprocess via PINS/call_json","FIXED REPO","labs/workbook-review-pass01/workbook.py:37-41,611-617","code-execution",True),
 ("labs/workbook-review-pass01/workbook.py","labs/review-construction-pass04/construct.py","subprocess via PINS/call_json","FIXED REPO","labs/workbook-review-pass01/workbook.py:42-46,611-617","code-execution",True),
 ("labs/workbook-review-pass01/workbook.py","labs/prime-cycle-pass03/prime_cycle.py","subprocess via PINS/call_json","FIXED REPO","labs/workbook-review-pass01/workbook.py:47-51,611-617","code-execution",True),
 ("labs/workbook-review-pass01/workbook.py","labs/prime-review-pass02/prime_review.py","subprocess via PINS/call_json","FIXED REPO","labs/workbook-review-pass01/workbook.py:52-56,611-617","code-execution",True),
 ("labs/return-access-pass01/return_access.py","labs/return-lines-pass03/return_lines.py","in-process exec (load_module), then _PASS03.load_pass02()","repo_root() = __file__/../..","labs/return-access-pass01/return_access.py:20-22,110-112,125-145","code-execution",True),
 ("labs/return-access-pass01/return_access.py","labs/return-capture-pass01/return_capture.py","in-process exec (load_reader)","repo_root()","labs/return-access-pass01/return_access.py:32-34,148-152","code-execution",True),
 ("labs/return-access-pass01/return_access.py","labs/return-lines-pass02/return_lines.py","pin_bytes only here (loaded by return-lines-pass03.load_pass02, not visible)","repo_root()","labs/return-access-pass01/return_access.py:23-25,138-141","code-execution (inferred)",True),
 ("labs/return-access-pass01/return_access.py","labs/return-lines-pass01/return_lines.py","pin_bytes only here","repo_root()","labs/return-access-pass01/return_access.py:26-28,138-141","unknown (pinned; use not visible)",True),
 ("labs/return-access-pass01/return_access.py","labs/return-placement-pass01/return_placement.py","pin_bytes only here","repo_root()","labs/return-access-pass01/return_access.py:29-31,138-141","unknown (pinned; use not visible)",True),
 ("labs/review-loop-pass03/review_loop.py","labs/review-construction-pass04/construct.py","subprocess run_tool after pin_file","FIXED ROOT=D:\\Git\\lib-build","labs/review-loop-pass03/review_loop.py:28-55,150-176","code-execution",True),
 ("labs/review-loop-pass03/review_loop.py","labs/prime-review-pass01/prime_review.py","pinned for run_tool","FIXED ROOT","labs/review-loop-pass03/review_loop.py:36-38,150-176","code-execution (inferred: pinned tool)",True),
 ("labs/review-loop-pass03/review_loop.py","labs/prime-review-pass02/prime_review.py","pinned for run_tool","FIXED ROOT","labs/review-loop-pass03/review_loop.py:39-41,150-176","code-execution (inferred)",True),
 ("labs/review-loop-pass03/review_loop.py","labs/prime-cycle-pass03/prime_cycle.py","pinned for run_tool","FIXED ROOT","labs/review-loop-pass03/review_loop.py:42-44,150-176","code-execution (inferred)",True),
 ("labs/review-loop-pass03/review_loop.py","labs/return-lines-pass01/return_lines.py","pinned for run_tool","FIXED ROOT","labs/review-loop-pass03/review_loop.py:45-48,150-176","code-execution (inferred)",True),
 ("labs/review-loop-pass03/review_loop.py","labs/return-placement-pass01/return_placement.py","pinned for run_tool","FIXED ROOT","labs/review-loop-pass03/review_loop.py:49-51,150-176","code-execution (inferred)",True),
 ("labs/review-loop-pass03/review_loop.py","labs/return-capture-pass01/return_inspect.py","pinned for run_tool","FIXED ROOT","labs/review-loop-pass03/review_loop.py:52-55,150-176","code-execution (inferred)",True),
 ("labs/review-loop-pass03/review_loop.py","labs/review-loop-pass02/review_loop.py","string reference in reproduce()","FIXED ROOT","labs/review-loop-pass03/review_loop.py:1167","historical-context (inferred)",False),
 ("labs/review-construction-pass04/construct.py","labs/prime-review-pass02/prime_review.py","subprocess TOOL, pinned TOOL_SHA256/TOOL_BYTES","FIXED ROOT=D:\\Git\\lib-build","labs/review-construction-pass04/construct.py:31-34,526-535","code-execution",True),
 ("labs/prime-cycle-pass03/prime_cycle.py","labs/review-construction-pass02/construct.py","pinned for run_tool","FIXED ROOT","labs/prime-cycle-pass03/prime_cycle.py:28-47,305-345","code-execution (inferred)",True),
 ("labs/prime-cycle-pass03/prime_cycle.py","labs/prime-review-pass01/prime_review.py","pinned for run_tool","FIXED ROOT","labs/prime-cycle-pass03/prime_cycle.py:305-345","code-execution (inferred)",True),
 ("labs/prime-cycle-pass03/prime_cycle.py","labs/prime-review-pass02/prime_review.py","pinned for run_tool","FIXED ROOT","labs/prime-cycle-pass03/prime_cycle.py:305-345","code-execution (inferred)",True),
 ("labs/prime-cycle-pass03/prime_cycle.py","labs/return-lines-pass01/return_lines.py","pinned for run_tool","FIXED ROOT","labs/prime-cycle-pass03/prime_cycle.py:33-35,305-345","code-execution (inferred)",True),
 ("labs/prime-cycle-pass03/prime_cycle.py","labs/return-placement-pass01/return_placement.py","pinned for run_tool","FIXED ROOT","labs/prime-cycle-pass03/prime_cycle.py:305-345","code-execution (inferred)",True),
 ("labs/prime-cycle-pass03/prime_cycle.py","labs/return-capture-pass01/return_inspect.py","pinned for run_tool","FIXED ROOT","labs/prime-cycle-pass03/prime_cycle.py:40-42,305-345","code-execution (inferred)",True),
 ("app/review_loop_tools_v7.py","app/review_loop_tools_v5.py","hash-checked only (resolve_tool + pin_named); never loaded","code_root","app/review_loop_tools_v7.py:182,230","historical-context",False),
 ("app/review_loop_tools_v7.py","app/review_loop_tools_v6.py","hash-checked only; never loaded","code_root","app/review_loop_tools_v7.py:184,232","historical-context",False),
 ("app/review_loop_tools_v7.py","app/review-loop-v4.json","hash-checked only","code_root","app/review_loop_tools_v7.py:181,229","historical-context (v4 itself may read it: not checked)",False),
 ("app/review_loop_tools_v7.py","app/review-loop-v5.json","hash-checked only","code_root","app/review_loop_tools_v7.py:183,231","historical-context",False),
 ("app/review_loop_tools_v7.py","app/review-loop-v6.json","hash-checked only","code_root","app/review_loop_tools_v7.py:185,233","historical-context",False),
 ("app/review_loop_tools_v7.py","labs/workbook-review-pass01/forms/workbook-review-v1.json","hash-checked only; pass03 overrides FORM_REL to pass03 form","code_root","app/review_loop_tools_v7.py:187,206-207; labs/workbook-review-pass03/workbook.py:503-504","historical-context",False),
 ("app/review_loop_tools_v7.py","labs/workbook-review-pass02/forms/workbook-review-v1.json","hash-checked only; pass03 overrides FORM_REL","code_root","app/review_loop_tools_v7.py:189,206-207","historical-context",False),
]
UNRES = [
 {"ref":"D:\\Git\\lib-build","where":["labs/workbook-review-pass03/workbook.py:21","labs/workbook-review-pass02/workbook.py:20","labs/workbook-review-pass01/workbook.py:22","labs/review-loop-pass03/review_loop.py:28","labs/review-construction-pass04/construct.py:31","labs/prime-cycle-pass03/prime_cycle.py:28","app/review_loop_tools_v4.py:28"],"why":"fixed Windows root; does not exist on this host; every pass03->pass02->pass01 load and every pass01/review_loop/construct/prime_cycle tool call resolves under it, not under v7's code_root"},
 {"ref":"code_root","where":["app/librarian.py:101","app/review_loop_tools_v7.py:261"],"why":"dynamic: parent of app/ wherever librarian.py lives; pins are checked here"},
 {"ref":"repo_root()","where":["labs/return-access-pass01/return_access.py:110-112"],"why":"dynamic: __file__/../.. of return_access.py (under fixed REPO when launched by pass01)"},
 {"ref":"sys.executable","where":["app/review_loop_tools_v7.py:211","labs/workbook-review-pass01/workbook.py:615"],"why":"interpreter is whatever runs librarian.py; not pinned"},
 {"ref":"app/context.py, authoring_tools_v2.py, return_line_tools_v2.py, boot_tools.py, prime_intake.py, prime_review_tools.py, batch_tools.py, handoff_tools.py, prime_tools.py, worker_bridge.py, clerk_seam.py, runner (config)","where":["app/librarian.py:112-232,276"],"why":"loaded by librarian.py for other commands; absent from the room; context.py is loaded at line 181 in main (whether before the review-loop branch is not established here)"},
]
nodes = {}
for e in E:
    for p in e[:2]: nodes[p] = meas(p)
for p in pins:
    if isinstance(p["path"], str) and "/" in p["path"]: nodes.setdefault(p["path"], meas(p["path"]))
for p in ("app/review-report-v1.json","app/review_report_tools_v1.py"): nodes[p]=meas(p)
declared = [{"declarer": p["declarer"], "line": p["line"], "form": p["form"], "key": p.get("key"), "path": p["path"], "declared_sha256": p["sha256"], "declared_bytes": p["bytes"], "room_match": p["match"]} for p in pins if isinstance(p["path"], str) and "/" in p["path"]]
v7 = json.load(open(SR + "/app/review-loop-v7.json"))["tools"]
v7paths = {v["path"] for v in v7.values()}
disc_from_chain = {e[1] for e in E if e[6] and e[5].startswith("code-execution")}
cmp = {
 "v7_declared": sorted(v7paths),
 "discovered_execution_on_review_loop_path": sorted(disc_from_chain | {"app/review_loop_tools_v7.py"}),
 "executed_but_not_in_v7_declaration": sorted((disc_from_chain | {"app/review_loop_tools_v7.py"}) - v7paths),
 "in_v7_declaration_but_not_executed": sorted(v7paths - disc_from_chain),
}
out = {"schema":"worker-a2-dependency-inventory/1","assignment":"prima-0706-0502 unit 2","method":"static read + Python ast only; nothing from the source room executed",
 "source_room": SR, "selected_declaration": meas("app/review-loop-v7.json"), "entry": meas("app/librarian.py"),
 "nodes": sorted(nodes.values(), key=lambda n: n["path"]),
 "edges": {"declared_pins": declared,
           "discovered": [dict(zip(("from","to","mechanism","root","evidence","class","on_v7_review_loop_path"), e)) for e in E]},
 "v7_declared_vs_discovered": cmp,
 "classes": {"code-execution": sorted({e[1] for e in E if e[5].startswith("code-execution")}),
             "source-data": sorted({e[1] for e in E if e[5]=="source-data"}),
             "historical-context": sorted({e[1] for e in E if e[5].startswith("historical")} | {"00.kernel/00.00.10.work/0707.app-use-check/evidence/design05.17/ (all; incl. proposal/workbook-review-pass04.workbook.py.proposal, NOT INSTALLED)", "app/review-report-v1.json (pins v7 tools and librarian; not read by the v7 review-loop path)"}),
             "unknown": sorted({e[1] for e in E if e[5].startswith("unknown")})},
 "unresolved": UNRES}
json.dump(out, open(A2 + "/dependencies.json", "w"), indent=1)
print(json.dumps(cmp, indent=1)); print("nodes", len(nodes), "absent", sum(1 for n in nodes.values() if not n["present_in_room"]))
print([n["path"] for n in nodes.values() if not n["present_in_room"]])
