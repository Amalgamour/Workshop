#!/usr/bin/env python3
"""Colab support v2: prepare, verify and take in N7NN exchange-layout packages.

Layout v2 names one pass exchange 05.NN.pack.md / 05.NN.return.md /
06.NN.notes.md / 06.NN.review.md. This producer emits only the pack, the notes and
visibly-marked templates; it never creates a real return or review.

Accepted v1 (labs/colab-support-pass01, pinned) is loaded read-only and reused for
request/binding validation, section resolution, pinned tool loading and launch,
the deterministic ZIP and output checks. v1 and the helpers are never edited.

  python -B colab_support.py preview --request ABS --config ABS --json
  python -B colab_support.py prepare --request ABS --config ABS --output ABS --digest HEX --json
  python -B colab_support.py verify  --output ABS --config ABS --json
  python -B colab_support.py intake  --output ABS --config ABS --book ABS --member 01NN.slug \
      --return-file ABS --source-root ABS --artifact REL|LOGICAL [...] --json

Contract: 00.kernel/00.00.10.work/0510.colab-tools/evidence/exchange05.03/CONTRACT.md
"""

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import zipfile
import io
from pathlib import Path

sys.dont_write_bytecode = True

REQUEST_SCHEMA = "colab-request/2"
CONFIG_SCHEMA = "colab-config/2"
LAYOUT = "colab-exchange-layout/2"
DIGEST_DOMAIN = "colab-package-digest/2"
VERIFICATION_SCHEMA = "colab-package-verification/2"
HANDOFF_SCHEMA = "colab-handoff/2"
REPORT_SCHEMA = "colab-support-report/2"
PROVENANCE_SCHEMA = "colab-intake-provenance/2"
PLACEMENT_SCHEMA = "colab-placement-proposal/2"
V1_PIN = ("33bbe41c52485fc7b2b611d830bae8a15129721ad807a931e8193f17944c467c", 67781)
CONFIG_KEYS = ("schema", "repositories", "python", "assembler", "checker", "helper", "inspector", "producer_v1")
HOOKS = ("before-assembler", "after-assembler", "before-zip", "before-verification")
SIDE_FILES = ("assembler-request.json", "assembler-run.json", "handoff.json", "verification.json")

STATEMENTS = [
    "This package is a draft. Preparation is not a Director release.",
    "05.NN.pack.md is the one primary instruction source; support/ is transport support only.",
    "No 05.NN.return.md or 06.NN.review.md exists at preparation. Templates are templates.",
    "A verified package or receipt is custody, not review or acceptance.",
    "The investigation binding is supplied by Prime; it does not open a live investigation.",
    "Labels and quoted Director text do not authenticate anyone.",
]
NOT_CHECKED = [
    "meaning, adequacy and design findings",
    "authenticity of labels and quoted replies",
    "permission: nothing is released, reviewed, accepted, seated or published",
    "workflow integration: no consumer of this layout has been reviewed",
]


class ColabError(Exception):
    def __init__(self, code, detail, kind="input-defect"):
        super().__init__(detail)
        self.code = code
        self.detail = detail
        self.kind = kind


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def finding(exc):
    return {"kind": getattr(exc, "kind", "tool-limitation"), "code": getattr(exc, "code", "error"),
            "detail": getattr(exc, "detail", str(exc))}


# ---------------------------------------------------------------- config and v1

def _pairs(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ColabError("duplicate-key", f"duplicate key: {key}")
        obj[key] = value
    return obj


def load_json(raw, label):
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ColabError("bom", f"{label} has a UTF-8 BOM")
    try:
        text = raw.decode("utf-8")
        value = json.loads(text, object_pairs_hook=_pairs,
                           parse_constant=lambda name: (_ for _ in ()).throw(ColabError("nonfinite", name)))
    except UnicodeError as exc:
        raise ColabError("encoding", f"{label} is not UTF-8") from exc
    except json.JSONDecodeError as exc:
        raise ColabError("json", f"{label} is not strict json: {exc.msg}") from exc
    if not isinstance(value, dict):
        raise ColabError("json", f"{label} is not an object")
    return value


class Context:
    """Config, pinned v1 module and its pinned assembler/checker."""

    def __init__(self, config_path):
        if not isinstance(config_path, str) or not os.path.isabs(config_path):
            raise ColabError("path", "config must be an absolute path")
        try:
            raw = Path(config_path).read_bytes()
        except OSError as exc:
            raise ColabError("missing", f"config could not be read: {exc.strerror or exc}") from exc
        cfg = load_json(raw, "config")
        if cfg.get("schema") != CONFIG_SCHEMA:
            raise ColabError("version", f"config schema is {cfg.get('schema')!r}, not {CONFIG_SCHEMA}")
        if set(cfg) != set(CONFIG_KEYS):
            raise ColabError("config", "config keys are not " + ", ".join(CONFIG_KEYS))
        path = cfg["producer_v1"]
        if not isinstance(path, str) or not os.path.isabs(path):
            raise ColabError("path", "producer_v1 must be an absolute path")
        probe = Path(path)
        if probe.is_symlink() or not probe.is_file():
            raise ColabError("pin", "producer_v1 is not a plain file", "tool-limitation")
        data = probe.read_bytes()
        if sha256(data) != V1_PIN[0] or len(data) != V1_PIN[1]:
            raise ColabError("pin", "producer_v1 does not match the accepted v1 pin 33bbe41c…", "tool-limitation")
        spec = importlib.util.spec_from_file_location("colab_support_v1_pinned", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.v1 = module
        v1cfg = {k: cfg[k] for k in CONFIG_KEYS if k != "producer_v1"}
        v1cfg["schema"] = "colab-config/1"
        # Reuse v1's config rules on the shared keys; the v1 label is internal only.
        try:
            for label, root in cfg["repositories"].items():
                module.one_line(label, "repository label")
                module.require_absolute(root, f"repository {label}")
            for key in ("python", "assembler", "checker", "helper", "inspector"):
                module.require_absolute(cfg[key], key)
            self.tools = module.Tools(v1cfg)
        except module.ColabError as exc:
            raise ColabError(exc.code, exc.detail, exc.kind) from exc
        self.cfg = cfg
        self.v1cfg = v1cfg
        self.errors = (ColabError, module.ColabError)


# ---------------------------------------------------------------- request

def validate_request(ctx, raw):
    v1 = ctx.v1
    if len(raw) > v1.MAX_REQUEST_BYTES:
        raise ColabError("limit", f"request is larger than {v1.MAX_REQUEST_BYTES} bytes")
    doc = v1.strict_json(raw, "request")
    schema = doc.get("schema")
    if schema != REQUEST_SCHEMA:
        raise ColabError("version", f"request schema is {schema!r}; this preparer takes only {REQUEST_SCHEMA}. "
                         "Nothing is migrated: a v1 request belongs to labs/colab-support-pass01.")
    if "preparation_notes" not in doc:
        raise ColabError("missing-key", "request is missing key: preparation_notes")
    notes = v1.bounded_list(doc["preparation_notes"], "preparation_notes", 0, v1.MAX_ITEMS)
    for item in notes:
        v1.text_block(item, "preparation note")
    shaped = {k: doc[k] for k in doc if k != "preparation_notes"}
    shaped["schema"] = "colab-request/1"
    v1.validate_request(shaped)
    if doc["environment"]["kind"] == "zip-only":
        for item in notes:
            if v1.LOCAL_PATH_RE.search(item):
                raise ColabError("local-path", "a preparation note names a local path; a ZIP-only recipient needs included inputs")
    return doc


# ---------------------------------------------------------------- rendering

def names_for(doc):
    p = doc["binding"]["investigation"]["pass"]
    nn = p[3:]
    return {
        "pass": p,
        "nn": nn,
        "pack": f"{p}.pack.md",
        "notes": f"06.{nn}.notes.md",
        "return_name": f"{p}.return.md",
        "review_name": f"06.{nn}.review.md",
        "return_template": f"templates/{p}.return.TEMPLATE.md",
        "review_template": f"templates/06.{nn}.review.TEMPLATE.md",
        "support_batch": f"support/assembler/{p}.md",
    }


def assembler_request(doc, names):
    """Adapter onto the accepted assembler. Its draft is transport support only."""
    binding = doc["binding"]
    inv = binding["investigation"]
    first = binding["targets"][0]["source"]
    paths = []
    for target in binding["targets"]:
        if target["source"]["path"] not in paths:
            paths.append(target["source"]["path"])
    paths.extend(item["path"] for item in doc["required_sources"])
    instructions = [{"nn": "01", "heading": "Transport support only", "text": (
        f"This is the accepted assembler's draft, kept under support/ for custody checks. "
        f"It is not an instruction source. Read ENTRY.md, then {names['pack']}."
    )}, {"nn": "02", "heading": "Method", "text": doc["method"]}]
    for case in doc["cases"]:
        instructions.append({"nn": f"{len(instructions) + 1:02d}", "heading": f"Case {case['id']}", "text": case["text"]})
    instructions.append({"nn": f"{len(instructions) + 1:02d}", "heading": "Return", "text": (
        f"Return one file shaped like {names['return_template']}. Prime places it as {names['return_name']} "
        "only after capture; this package does not contain it."
    )})
    items = [{"name": f"withheld {w['item']}", "detail": w["reason"]} for w in doc["withheld"]]
    items += [{"name": f"{u['kind']} {u['item']}", "detail": u["reason"]} for u in doc["unavailable"]]
    if not items:
        items = [{"name": "sources", "detail": "every selected source is included as a snapshot"}]
    request = {
        "schema": "pack-assembly-request/1",
        "template": "pack-assembly-draft/1",
        "title": doc["title"],
        "date": doc["date"],
        "author": doc["author"],
        "origin": {"book": inv["book"], "page": inv["page"], "batch": inv["pass"]},
        "identity": {"book": inv["book"], "pppp": inv["page"][:4], "keyword": inv["page"][5:], "batch": inv["pass"]},
        "executor": doc["recipient"],
        "reviewer": doc["reviewer"],
        "goal": "Question: " + doc["question"] + "\nWhy: " + doc["why"],
        "scope": ["Recipient writes: " + doc["environment"]["write"]],
        "revision": first["commit"],
        "paths": paths,
        "instructions": instructions,
        "evidence": "One return file in the return template shape. A receipt of it is custody, not acceptance.",
        "dependencies": {"state": "supplied", "items": items},
        "return_destination": {"state": "supplied", "path": doc["return_route"]["destination"]},
        "repository_label": first["repository"],
    }
    return (json.dumps(request, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def replies_block(doc, entry_style):
    out = []
    if not doc["director_replies"]:
        return ["None supplied."]
    for reply in doc["director_replies"]:
        if entry_style:
            label = "actual Director reply" if reply["status"] == "actual" else "HYPOTHETICAL FIXTURE, not a Director decision"
            out.append(f"{reply['id']} ({label}; {reply['date']}; {reply['source']}):")
        else:
            out.append(f"{reply['id']} [{reply['status']}] {reply['date']} {reply['source']}")
        out.append("```text")
        out += [f"reply: {line}" for line in reply["reply"].split("\n")]
        out.append("```")
    return out


def numbered(prefix, items, lines_of):
    out = []
    for index, item in enumerate(items, start=1):
        parts = lines_of(item)
        out.append(f"{prefix}{index:02d}. {parts[0]}")
        out += parts[1:]
    return out or ["None supplied."]


def target_lines(doc, sections, snap):
    out = []
    by_id = {s["target"]: s for s in sections}
    for target in doc["binding"]["targets"]:
        res = by_id[target["id"]]
        where = f"{target['book']}/{target['page']}/{target['file']}"
        if res["kind"] == "whole-file":
            scope = "whole named file (not the whole page)"
        else:
            scope = (f"section `{res['value']}` occurrence {res['occurrence'] or 1} of {res['matches']}, "
                     f"lines {res['line_start']}-{res['line_end']}")
        out.append(f"- {target['id']}: {where}; {scope}; blob {target['source']['sha256']}; "
                   f"read `{snap[target['source']['path']]}`.")
    return out


def render_entry(v1, doc, names, sources, sections):
    L = v1.lines_of
    inv = doc["binding"]["investigation"]
    src = doc["binding"]["targets"][0]["source"]
    snap = {s["path"]: s["snapshot"] for s in sources}
    out = [
        f"# ENTRY — {doc['title']}",
        "",
        f"Layout: {LAYOUT}. Investigation: book {inv['book']}, page {inv['page']}, pass {inv['pass']}.",
        f"Prepared by {doc['author']} on {doc['date']} for {doc['recipient']}. Reviewer: {doc['reviewer']}.",
        f"Every source here is the exact Git blob at {src['repository']} commit {src['commit']}.",
        "This entry is orientation. It releases, seats and authorizes nothing.",
        "",
        "## One instruction source",
        f"Your instructions are in `{names['pack']}`. It is the only instruction source for pass {inv['pass']}.",
        f"`{names['notes']}` holds Prime's supplied preparation notes. They are context, not a review.",
        "`support/` is transport support for the accepted pack assembler. It is not an instruction source.",
        "",
        "## The exchange for this pass",
        f"- `{names['pack']}`: this pass's pack (here).",
        f"- `{names['notes']}`: preparation notes (here).",
        f"- `{names['return_name']}`: your return, placed by Prime only after capture. It is NOT in this package. Shape: `{names['return_template']}`.",
        f"- `{names['review_name']}`: Prime's later review. It is NOT in this package and does not exist yet. Shape: `{names['review_template']}`.",
        "",
        "## Role and mode",
        f"You are a Colab. Mode: {doc['mode']}.",
        "You may challenge the method and propose a better one. Your findings do not change any page by themselves.",
        "",
        "## Context",
    ]
    out += L(doc["context"])
    out += ["", "## Built state"] + L(doc["built_state"])
    out += ["", "## Known gaps"] + numbered("G", doc["known_gaps"], L)
    out += ["", "## Targets (the subjects of this investigation)"] + target_lines(doc, sections, snap)
    out += ["", "## Reading order", "1. This ENTRY.md.", f"2. `{names['pack']}`.", f"3. `{names['notes']}`.",
            "4. The target snapshots, in target order."]
    if doc["required_sources"]:
        out.append("5. Required sources:")
        for item in doc["required_sources"]:
            out.append(f"   - `{snap[item['path']]}` = {item['path']} — {item['role']}")
    out.append(f"Last: `{names['return_template']}`. `source-manifest.json` lists every snapshot with its sha256.")
    out += ["", "## Supplied, withheld and unavailable",
            "Supplied: every file in this package. Anything not here and not listed below was not supplied; do not invent it."]
    out.append("Withheld on purpose:" if doc["withheld"] else "Withheld on purpose: none.")
    out += [f"- {w['item']}: {w['reason']}" for w in doc["withheld"]]
    omissions = [u for u in doc["unavailable"] if u["kind"] == "required-omission"]
    limits = [u for u in doc["unavailable"] if u["kind"] == "tool-limitation"]
    out.append("Required but unavailable (a pack gap, not a design finding):" if omissions else "Required but unavailable: none.")
    out += [f"- {u['item']}: {u['reason']}" for u in omissions]
    out.append("Tool limitations (not design findings):" if limits else "Tool limitations declared: none.")
    out += [f"- {u['item']}: {u['reason']}" for u in limits]
    env = doc["environment"]
    out += ["", "## Environment and capabilities", f"Kind: {env['kind']}.", f"Read: {env['read']}", f"Write: {env['write']}",
            f"Execute: {env['execute']}", f"Network: {env['network']}"]
    if env["kind"] == "zip-only":
        out.append("You have only this package. Paths in it are labels; they give no access to any local drive.")
    out += ["", "## Prior involvement and shared context"] + L(doc["prior_involvement"])
    out += ["", "## Director replies (quoted data)"] + replies_block(doc, True)
    out += [""]
    return "\n".join(out).encode("utf-8")


def render_pack(v1, doc, names, sources, sections):
    L = v1.lines_of
    inv = doc["binding"]["investigation"]
    snap = {s["path"]: s["snapshot"] for s in sources}
    out = [
        f"# 05 — {doc['title']}",
        "version: 001",
        f"Authorization: draft — {doc['date']}",
        f"who: {doc['author']}",
        "state: draft",
        "Face: 05",
        f"PPPP: {inv['page'][:4]}",
        f"book: {inv['book']}",
        f"keyword: {inv['page'][5:]}",
        f"exchange: {names['pack']} (pack) for pass {inv['pass']}",
        "",
        "This pack is the one primary instruction source for this pass.",
        "",
        "## Assignment",
        f"Executor: {doc['recipient']}",
        f"Reviewer: {doc['reviewer']}",
        "Release: PENDING. This draft grants no release.",
        "Claim: PENDING.",
        f"Investigation: {inv['book']}/{inv['page']} pass {inv['pass']}.",
        f"Mode: {doc['mode']}.",
        "",
        "## Question",
    ]
    out += L(doc["question"])
    out += ["", "## Why"] + L(doc["why"])
    out += ["", "## Targets"] + target_lines(doc, sections, snap)
    out += ["", "## Sources"]
    for s in sources:
        out.append(f"- `{s['snapshot']}` = {s['path']} {s['sha256']} {s['bytes']}")
    out += ["", "## #01 — Method"] + L(doc["method"])
    for index, case in enumerate(doc["cases"], start=2):
        out += ["", f"## #{index:02d} — Case {case['id']}"] + L(case["text"])
    out += ["", "## Scoring"]
    scoring = doc["scoring"]
    if scoring["state"] == "unscored":
        out.append("Unscored. State the qualitative result. Do not invent a number.")
    elif scoring["blind"]:
        out.append("A formal scored method is declared. Its evaluator material is withheld from you by design and is not in this package.")
    else:
        out += ["Scored, not blind. Rubric:"] + L(scoring["rubric"]) + ["What a score means:"] + L(scoring["meaning"])
    out += ["", "## Permissions"] + [f"- {p}" for p in doc["permissions"]]
    out += ["", "## Stop and escalate"] + [f"- {s}" for s in doc["stop"]]
    out += ["", "## Return",
            f"Destination: {doc['return_route']['destination']}",
            f"Submission: {doc['return_route']['submission_hint']}",
            f"Shape: `{names['return_template']}`. After capture, Prime places your exact bytes as `{names['return_name']}`.",
            "A receipt of your return is custody, not acceptance.",
            "", "## Return pointer", "PENDING.", "", "## Review", f"PENDING. Prime's review will be `{names['review_name']}`.", ""]
    return "\n".join(out).encode("utf-8")


def render_notes(v1, doc, names):
    L = v1.lines_of
    inv = doc["binding"]["investigation"]
    out = [
        f"# 06 — Preparation notes — {doc['title']}",
        "version: 001",
        f"Authorization: draft — {doc['date']}",
        f"who: {doc['author']}",
        "state: draft; supplied preparation notes, not a review",
        "Face: 06",
        f"PPPP: {inv['page'][:4]}",
        f"book: {inv['book']}",
        f"keyword: {inv['page'][5:]}",
        f"exchange: {names['notes']} (notes) for pass {inv['pass']}",
        "",
        f"These notes are Prime's supplied working text. They are not the review; the review will be `{names['review_name']}`, written later.",
        "",
        "## Preparation notes (supplied)",
    ]
    out += numbered("N", doc["preparation_notes"], L)
    out += ["", "## Supplied purpose"] + L(doc["question"]) + [""] + L(doc["why"])
    out += ["", "## Supplied context"] + L(doc["context"])
    out += ["", "## Supplied known gaps"] + numbered("G", doc["known_gaps"], L)
    out += ["", "## Director replies (exact, as supplied)"] + replies_block(doc, False)
    out += ["", "## Findings", "None. Findings arrive in the captured return and in Prime's later review.", ""]
    return "\n".join(out).encode("utf-8")


def render_return_template(doc, names):
    inv = doc["binding"]["investigation"]
    out = [
        f"# TEMPLATE — {names['return_name']} for {inv['book']}/{inv['page']}",
        "",
        "THIS IS A TEMPLATE. It is not a returned answer and not accepted work.",
        f"Fill it in and send it back. After capture, Prime places your exact bytes as `{names['return_name']}`.",
        "Keep every heading. An empty section may say what you looked for and that nothing was found.",
        "",
        "## Identity",
        "Model, publisher or interface, session id if known, date. Prior involvement and shared context.",
        "",
        "## Inputs actually read",
        "The snapshot files you opened. Anything you could not open.",
        "",
        "## Answer",
        "The answer to the question, with evidence and a reasoned assessment. An honest unknown is a result.",
        "",
        "## Cases",
    ]
    out += [f"{case['id']}: result and evidence." for case in doc["cases"]]
    out += [
        "", "## Actual operations", "What you actually read, ran or changed. Mark anything self-reported.",
        "", "## Hostile", "The failing path; the first misleading sentence or row; a missing relationship; where a protective rule blocks legitimate work.",
        "", "## Factfind", "Numbered holes F01.. tied to an exact page, face or source, each with a test or observation.",
        "", "## Pack and tool defects", "Missing inputs and tool limits. These are not design findings.",
        "", "## Overflow", "Relevant discoveries outside the ask, parked.",
        "", "## Unprompted", "What to add, cut, refuse or investigate that was not asked, and why.",
        "", "## Director replies", "Exact attributed `reply:` lines from any Director exchange, or `none`.",
    ]
    if doc["scoring"]["state"] == "scored":
        out += ["", "## Scoring", "The declared method, raw evidence and what the score means."]
    out += ["", "## Limits", "What this return does not establish.", ""]
    return "\n".join(out).encode("utf-8")


def render_review_template(doc, names):
    inv = doc["binding"]["investigation"]
    out = [
        f"# TEMPLATE — {names['review_name']} for {inv['book']}/{inv['page']}",
        "",
        "THIS IS A TEMPLATE. No review has happened. Nothing here is an assessment, a Director reply or a decision.",
        f"Prime writes the real `{names['review_name']}` after reading the captured `{names['return_name']}`.",
        "",
        "## Return provenance",
        "Member, receipt sha256 and return sha256 from the verified capture (copied from the placement record).",
        "",
        "## Prime assessment",
        "Prime's reading of the return, finding by finding. Keep the return's own numbering.",
        "",
        "## Director reply",
        "Exact attributed `reply:` lines only. If there is none, write `pending` or `not needed`, as explicitly supplied. Never write an approval that was not given.",
        "",
        "## Unresolved questions",
        "What remains open, and for whom.",
        "",
        "## Dispositions and reasons",
        "For each finding: adopted, answered, rejected, deferred or escalated, and why.",
        "",
        "## Route",
        "One of: finish; hold; request a next Colab pass (a new 05.NN.pack.md, not automatic); route an implementation job to N5NN. None is chosen by this template.",
        "",
    ]
    return "\n".join(out).encode("utf-8")


def render_support(names):
    out = [
        "# support — transport support, not instructions",
        "",
        "The files in `support/assembler/` are byte copies of the accepted pack assembler's own outputs:",
        f"- `{names['support_batch']}` is its legacy draft. It is NOT an instruction source. The instruction source is `{names['pack']}`.",
        "- `request.snapshot` is the adapter request it was given.",
        "- `completion-receipt.json` is its completion receipt. A receipt is custody, not acceptance.",
        "They exist so the pinned assembler verify can check this package. `source-manifest.json` and `snapshots/` at the package root are shared with them.",
        "",
    ]
    return "\n".join(out).encode("utf-8")


# ---------------------------------------------------------------- planning

def plan(ctx, request_raw, read_sources, read_evaluator):
    v1 = ctx.v1
    asm = ctx.tools.asm
    doc = validate_request(ctx, request_raw)
    names = names_for(doc)
    asm_raw = assembler_request(doc, names)
    try:
        asm_req = asm.validate_request(asm.parse_json(asm_raw), ctx.tools.checker)
    except asm.AssemblyError as exc:
        raise ColabError("assembler-request", f"pinned assembler refuses the adapted request: {exc.detail}",
                         "tool-limitation") from exc
    binding = doc["binding"]
    commit = binding["targets"][0]["source"]["commit"]
    resolved, sources = read_sources(commit, asm_req["paths"])
    if resolved != commit:
        raise ColabError("commit", "the bound commit did not resolve to itself")
    by_path = {s["path"]: s for s in sources}
    sections = []
    for target in binding["targets"]:
        src = by_path[target["source"]["path"]]
        if src["sha256"] != target["source"]["sha256"]:
            raise ColabError("stale-source", f"{target['id']} blob at the commit is {src['sha256']}, "
                             f"not the bound {target['source']['sha256']}; nothing was retargeted")
        sections.append(v1.resolve_section(target, src["data"]))
    identities, planned, asm_digest = asm.plan_outputs(asm_raw, asm_req, commit, sources)
    receipt = asm.receipt_bytes({
        "request": asm_req, "planned": planned, "digest": asm_digest, "request_raw": asm_raw,
        "commit": commit, "sources": identities,
        "checker_sha256": ctx.tools.checker_sha, "checker_bytes": ctx.tools.checker_bytes,
    }, {"result": "pass", "rows_checked": len(sources)}, 0)
    asm_files = {item["path"]: item["data"] for item in planned}
    asm_files["completion-receipt.json"] = receipt
    colab_files = [
        ("ENTRY.md", render_entry(v1, doc, names, identities, sections)),
        (names["pack"], render_pack(v1, doc, names, identities, sections)),
        (names["notes"], render_notes(v1, doc, names)),
        (names["return_template"], render_return_template(doc, names)),
        (names["review_template"], render_review_template(doc, names)),
        ("binding.json", v1.canonical(binding)),
        ("colab-request.json", request_raw),
        ("support/SUPPORT.md", render_support(names)),
    ]
    support = [
        (names["support_batch"], f"{names['pass']}.md"),
        ("support/assembler/request.snapshot", "request.snapshot"),
        ("support/assembler/completion-receipt.json", "completion-receipt.json"),
    ]
    package = {"source-manifest.json": asm_files["source-manifest.json"]}
    package.update({name: data for name, data in asm_files.items() if name.startswith("snapshots/")})
    for name, data in colab_files:
        package[name] = data
    for spath, aname in support:
        package[spath] = asm_files[aname]
    evaluator = []
    scoring = doc["scoring"]
    if scoring["state"] == "scored" and scoring["blind"]:
        ev_commit, ev_sources = read_evaluator(commit, scoring["evaluator_sources"])
        candidate = {s["sha256"] for s in sources}
        for src in ev_sources:
            if src["sha256"] in candidate:
                raise ColabError("evaluator-overlap", f"evaluator source {src['path']} has the same bytes as a candidate input")
        manifest = {"schema": "prime-pack-sources/1", "commit": ev_commit, "sources": [
            {"path": s["path"], "sha256": s["sha256"], "bytes": s["bytes"], "snapshot": s["snapshot"]} for s in ev_sources]}
        evaluator = [("evaluator/source-manifest.json", v1.canonical(manifest))]
        evaluator += [("evaluator/" + s["snapshot"], s["data"]) for s in ev_sources]
    zip_bytes = v1.make_zip(package)
    preimage = [("text", DIGEST_DOMAIN), ("text", LAYOUT), ("file", "package/colab-request.json"),
                ("file", "package/binding.json"), ("text", asm_digest)]
    for name, data in colab_files:
        preimage += [("text", "package/" + name), ("text", sha256(data)), ("text", str(len(data)))]
    for name, data in evaluator:
        preimage += [("text", name), ("text", sha256(data)), ("text", str(len(data)))]
    for spath, aname in support:
        preimage += [("text", "package/" + spath), ("text", aname)]
    preimage += [("text", sha256(zip_bytes)), ("text", str(len(zip_bytes)))]
    files_for = {"package/colab-request.json": request_raw, "package/binding.json": v1.canonical(binding)}
    digest = hashlib.sha256()
    for kind, value in preimage:
        digest.update(v1.length_prefix(files_for[value] if kind == "file" else value))
    result = {
        "doc": doc, "names": names, "asm_raw": asm_raw, "asm_digest": asm_digest, "asm_files": asm_files,
        "commit": commit, "sources": identities, "sections": sections, "package": package,
        "colab_files": colab_files, "support": support, "evaluator": evaluator, "zip": zip_bytes,
        "preimage": preimage, "digest": digest.hexdigest(),
    }
    result["handoff"] = render_handoff(ctx, result)
    return result


def roles(names):
    return {
        "ENTRY.md": "entry", names["pack"]: "pack-primary-instruction", names["notes"]: "notes",
        names["return_template"]: "template-return", names["review_template"]: "template-review",
        "binding.json": "binding", "colab-request.json": "request", "source-manifest.json": "source-manifest",
        "support/SUPPORT.md": "support-declaration",
    }


def render_handoff(ctx, p):
    names = p["names"]
    role_of = roles(names)
    support_names = {s for s, _ in p["support"]}
    envelope = []
    for name, data in sorted(p["package"].items()):
        role = role_of.get(name) or ("snapshot" if name.startswith("snapshots/") else
                                      "support-assembler" if name in support_names else "unknown")
        envelope.append({"path": "package/" + name, "role": role, "sha256": sha256(data), "bytes": len(data)})
    targets_by_path = {}
    for t in p["doc"]["binding"]["targets"]:
        targets_by_path.setdefault(t["source"]["path"], []).append(t["id"])
    required = {r["path"] for r in p["doc"]["required_sources"]}
    source_map = [{"source_path": s["path"], "snapshot": "package/" + s["snapshot"], "sha256": s["sha256"],
                   "bytes": s["bytes"], "targets": targets_by_path.get(s["path"], []),
                   "role": "target" if s["path"] in targets_by_path else ("required" if s["path"] in required else "other")}
                  for s in p["sources"]]
    body = {
        "schema": HANDOFF_SCHEMA,
        "layout": LAYOUT,
        "digest": p["digest"],
        "digest_domain": DIGEST_DOMAIN,
        "digest_preimage": [{"kind": k, "value": v} for k, v in p["preimage"]],
        "digest_rule": "sha256 over parts in order; each part is an 8-byte big-endian length then its bytes; "
                       "a 'text' part is its UTF-8 value, a 'file' part is the bytes of that OUT path",
        "investigation": p["doc"]["binding"]["investigation"],
        "binding": p["doc"]["binding"],
        "binding_sha256": sha256(ctx.v1.canonical(p["doc"]["binding"])),
        "exchange": {
            "pass": names["pass"], "nn": names["nn"], "pack": names["pack"], "notes": names["notes"],
            "return_name": names["return_name"], "review_name": names["review_name"],
            "return_template": names["return_template"], "review_template": names["review_template"],
            "primary_instruction": names["pack"],
        },
        "not_created": [names["return_name"], names["review_name"]],
        "envelope": envelope,
        "source_map": source_map,
        "support_projection": [{"support_path": "package/" + s, "assembler_name": a,
                                "sha256": sha256(p["package"][s]), "bytes": len(p["package"][s])} for s, a in p["support"]],
        "zip": {"path": "prepared-colab.zip", "sha256": sha256(p["zip"]), "bytes": len(p["zip"]),
                "members": sorted(p["package"])},
        "evaluator": [{"path": n, "sha256": sha256(d), "bytes": len(d)} for n, d in p["evaluator"]],
        "verify": {
            "argv": ["python", "-B", "labs/colab-support-pass02/colab_support.py", "verify",
                     "--output", "<OUT>", "--config", "<CONFIG>", "--json"],
            "standalone": ["python", "-B", "labs/colab-support-pass02/handoff_check.py", "check",
                           "--output", "<OUT>", "--expected-digest", "<DIGEST>", "--json"],
            "config_schema": CONFIG_SCHEMA,
            "config_keys": list(CONFIG_KEYS),
            "pins": {"producer_v1": V1_PIN[0], **{k: v[0] for k, v in sorted(ctx.v1.PINS.items())}},
        },
        "statements": STATEMENTS,
    }
    return ctx.v1.canonical(body)


def out_expected(ctx, p):
    out = {"package/" + n: d for n, d in p["package"].items()}
    out.update(dict(p["evaluator"]))
    out["prepared-colab.zip"] = p["zip"]
    out["assembler-request.json"] = p["asm_raw"]
    out.update({"assembler-output/" + n: d for n, d in p["asm_files"].items()})
    out["handoff.json"] = p["handoff"]
    out["verification.json"] = verification_bytes(ctx, p, out)
    return out


def verification_bytes(ctx, p, files):
    listed = sorted((n, d) for n, d in files.items() if n not in ("verification.json",))
    body = {
        "schema": VERIFICATION_SCHEMA,
        "result": "prepared",
        "layout": LAYOUT,
        "digest": p["digest"],
        "assembler_digest": p["asm_digest"],
        "repository": p["doc"]["binding"]["targets"][0]["source"]["repository"],
        "commit": p["commit"],
        "investigation": p["doc"]["binding"]["investigation"],
        "binding_sha256": sha256(ctx.v1.canonical(p["doc"]["binding"])),
        "handoff_sha256": sha256(p["handoff"]),
        "out_files": [{"path": n, "sha256": sha256(d), "bytes": len(d)} for n, d in listed],
        "raw_records": ["assembler-run.json"],
        "sections": p["sections"],
        "statements": STATEMENTS,
    }
    return ctx.v1.canonical(body)


def plan_from_git(ctx, request_path):
    raw = ctx.v1.read_file(request_path, "request")
    doc = validate_request(ctx, raw)
    label = doc["binding"]["targets"][0]["source"]["repository"]
    if label not in ctx.cfg["repositories"]:
        raise ColabError("repository", f"repository label {label} has no local root in config")
    reader = ctx.v1.git_reader(ctx.tools, ctx.cfg["repositories"][label])
    return plan(ctx, raw, reader, reader)


# ---------------------------------------------------------------- reports

def report(command, result, findings=(), p=None, **extra):
    body = {
        "schema": REPORT_SCHEMA, "command": command, "result": result, "layout": LAYOUT,
        "digest": None, "investigation": None, "exchange": None, "commit": None, "targets": [],
        "planned": [], "findings": list(findings), "statements": STATEMENTS, "not_checked": NOT_CHECKED,
    }
    if p is not None:
        body["digest"] = p["digest"]
        body["investigation"] = p["doc"]["binding"]["investigation"]
        body["exchange"] = {k: p["names"][k] for k in ("pass", "pack", "notes", "return_name", "review_name",
                                                       "return_template", "review_template")}
        body["commit"] = p["commit"]
        body["targets"] = p["sections"]
        files = [("package/" + n, d) for n, d in sorted(p["package"].items())] + list(p["evaluator"])
        files.append(("prepared-colab.zip", p["zip"]))
        body["planned"] = [{"path": n, "sha256": sha256(d), "bytes": len(d)} for n, d in files]
    body.update(extra)
    return body


def preview(request_path, config_path):
    try:
        ctx = Context(config_path)
        p = plan_from_git(ctx, request_path)
    except Exception as exc:  # noqa: BLE001 - only expected tool errors are reported; others re-raise
        if not hasattr(exc, "code"):
            raise
        return report("preview", "invalid", [finding(exc)]), 2
    return report("preview", "preview", p=p), 0


# ---------------------------------------------------------------- prepare

def prepare(request_path, config_path, output, supplied, hooks=None):
    hooks = hooks or {}
    try:
        ctx = Context(config_path)
        p = plan_from_git(ctx, request_path)
    except Exception as exc:  # noqa: BLE001
        if not hasattr(exc, "code"):
            raise
        return report("prepare", "invalid", [finding(exc)], supplied_digest=supplied), 2
    v1 = ctx.v1
    if supplied != p["digest"]:
        return report("prepare", "invalid", [{"kind": "input-defect", "code": "digest-mismatch",
                      "detail": "supplied digest does not match the recomputed plan"}], p=p, supplied_digest=supplied), 2
    try:
        state = v1.check_output(output, ctx.cfg)
    except v1.ColabError as exc:
        return report("prepare", "invalid", [finding(exc)], p=p, supplied_digest=supplied), 2
    if state == "occupied":
        body, code = verify(output, config_path)
        if code == 0 and body.get("digest") == p["digest"]:
            return report("prepare", "already-prepared", p=p, supplied_digest=supplied, output=output, written=[]), 0
        detail = "output holds a different package" if code == 0 else "output holds a partial, damaged or foreign package"
        return report("prepare", "collision", [{"kind": "pack-defect", "code": "collision", "detail": detail}],
                      p=p, supplied_digest=supplied, output=output, retained=v1.written_list(output)), 2
    root = Path(output)
    try:
        root.mkdir(exist_ok=True)
        v1.write_new(root / "assembler-request.json", p["asm_raw"])
        if "before-assembler" in hooks:
            hooks["before-assembler"](root)
        label = p["doc"]["binding"]["targets"][0]["source"]["repository"]
        run = v1.run_tool(ctx.v1cfg, "assembler", [
            "assemble", "--request", str(root / "assembler-request.json"), "--repo", ctx.cfg["repositories"][label],
            "--checker", ctx.cfg["checker"], "--output", str(root / "assembler-output"), "--digest", p["asm_digest"], "--json",
        ])
        v1.write_new(root / "assembler-run.json", v1.canonical(run))
        if run["exit"] != 0:
            raise ColabError("assembler", f"pinned assembler exit {run['exit']}", "tool-limitation")
        for name, data in p["asm_files"].items():
            if (root / "assembler-output" / name).read_bytes() != data:
                raise ColabError("assembler", f"assembler-output/{name} differs from the plan", "pack-defect")
        if "after-assembler" in hooks:
            hooks["after-assembler"](root)
        for name, data in sorted(p["package"].items()):
            v1.write_new(root / "package" / name, data)
        for name, data in p["evaluator"]:
            v1.write_new(root / name, data)
        if "before-zip" in hooks:
            hooks["before-zip"](root)
        for name, data in p["package"].items():
            if (root / "package" / name).read_bytes() != data:
                raise ColabError("drift", f"package/{name} differs from the plan before zipping", "pack-defect")
        v1.write_new(root / "prepared-colab.zip", p["zip"])
        v1.write_new(root / "handoff.json", p["handoff"])
        if "before-verification" in hooks:
            hooks["before-verification"](root)
        expected = out_expected(ctx, p)
        v1.write_new(root / "verification.json", expected["verification.json"])
    except Exception as exc:  # noqa: BLE001
        if not hasattr(exc, "code") and not isinstance(exc, OSError):
            raise
        detail = finding(exc) if hasattr(exc, "code") else {"kind": "tool-limitation", "code": "io", "detail": str(exc)}
        return report("prepare", "partial", [detail], p=p, supplied_digest=supplied, output=output,
                      retained=v1.written_list(output)), 2
    return report("prepare", "prepared", p=p, supplied_digest=supplied, output=output,
                  written=v1.written_list(output)), 0


# ---------------------------------------------------------------- verify

def verify(output, config_path):
    findings = []
    try:
        ctx = Context(config_path)
        v1 = ctx.v1
        v1.require_absolute(output, "output")
        if v1.kind_of(output) != "dir":
            raise ColabError("missing", "output is not a directory", "pack-defect")
        tree = v1.read_tree(output)
    except Exception as exc:  # noqa: BLE001
        if not hasattr(exc, "code"):
            raise
        return report("verify", "invalid", [finding(exc)]), 2
    if "verification.json" not in tree:
        return report("verify", "partial", [{"kind": "pack-defect", "code": "not-completed",
                      "detail": "verification.json is absent"}], present=sorted(tree)), 1
    try:
        recorded = load_json(tree["verification.json"], "verification")
        if recorded.get("schema") != VERIFICATION_SCHEMA:
            raise ColabError("version", f"OUT verification schema is {recorded.get('schema')!r}, not {VERIFICATION_SCHEMA}; "
                             "nothing is migrated")
        package = {n[len("package/"):]: d for n, d in tree.items() if n.startswith("package/")}
        if "colab-request.json" not in package:
            raise ColabError("missing", "package/colab-request.json is missing", "pack-defect")

        def read_evaluator(commit, paths):
            manifest = load_json(tree.get("evaluator/source-manifest.json", b"{}"), "evaluator manifest")
            rows = manifest.get("sources") or []
            if [r.get("path") for r in rows] != list(paths):
                raise ColabError("manifest", "evaluator manifest differs from the request", "pack-defect")
            out = []
            for row in rows:
                data = tree.get("evaluator/" + row["snapshot"])
                if data is None:
                    raise ColabError("missing", f"evaluator/{row['snapshot']} is missing", "pack-defect")
                out.append({"path": row["path"], "sha256": sha256(data), "bytes": len(data),
                            "snapshot": row["snapshot"], "data": data})
            return manifest.get("commit"), out

        p = plan(ctx, package["colab-request.json"], v1.package_reader(package), read_evaluator)
    except Exception as exc:  # noqa: BLE001
        if not hasattr(exc, "code"):
            raise
        kind = getattr(exc, "kind", "pack-defect")
        code = 2 if getattr(exc, "code", "") == "version" else 1
        return report("verify", "invalid" if code == 2 else "mismatch", [{"kind": kind, "code": exc.code,
                      "detail": exc.detail}]), code
    expected = out_expected(ctx, p)
    for name in sorted(set(expected) | set(tree)):
        if name == "assembler-run.json":
            continue
        if name.endswith(".return.md") or name.endswith(".review.md"):
            findings.append({"kind": "pack-defect", "code": "fabricated-exchange",
                             "detail": f"{name} exists; preparation never creates a return or review"})
            continue
        if name not in tree:
            findings.append({"kind": "pack-defect", "code": "missing", "detail": f"{name} is missing"})
        elif name not in expected:
            findings.append({"kind": "pack-defect", "code": "extra", "detail": f"{name} is not part of the package"})
        elif tree[name] != expected[name]:
            findings.append({"kind": "pack-defect", "code": "differs", "detail": f"{name} differs from the recomputed plan"})
    try:
        run = load_json(tree.get("assembler-run.json", b""), "assembler-run.json")
        if run.get("tool") != "assembler" or run.get("exit") != 0:
            raise ColabError("assembler-run", "assembler-run.json does not record a successful assemble", "pack-defect")
    except ColabError as exc:
        findings.append(finding(exc))
    try:
        with zipfile.ZipFile(io.BytesIO(tree.get("prepared-colab.zip", b""))) as archive:
            members = {info.filename: archive.read(info.filename) for info in archive.infolist()}
        if members != p["package"]:
            findings.append({"kind": "pack-defect", "code": "zip", "detail": "ZIP members differ from package/"})
    except (zipfile.BadZipFile, OSError) as exc:
        findings.append({"kind": "pack-defect", "code": "zip", "detail": f"ZIP is unreadable: {exc}"})
    asm_run = None
    with tempfile.TemporaryDirectory(prefix="colab2-verify-") as tmp:
        projection = Path(tmp) / "pack"
        files = {"source-manifest.json": package.get("source-manifest.json", b"")}
        files.update({n: d for n, d in package.items() if n.startswith("snapshots/")})
        for spath, aname in p["support"]:
            files[aname] = package.get(spath, b"")
        for name, data in files.items():
            dest = projection.joinpath(*name.split("/"))
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
        try:
            asm_run = v1.run_tool(ctx.v1cfg, "assembler", ["verify", "--pack", str(projection), "--checker",
                                                            ctx.cfg["checker"], "--json"])
        except v1.ColabError as exc:
            findings.append(finding(exc))
        if asm_run is not None:
            asm_run["args"] = ["verify", "--pack", "<temporary projection>", "--checker", "<pinned checker>", "--json"]
            asm_run["stdout"] = asm_run["stdout"].replace(str(projection), "<temporary projection>")
            if asm_run["exit"] != 0:
                findings.append({"kind": "pack-defect", "code": "assembler-verify",
                                 "detail": f"pinned assembler verify on the support projection exit {asm_run['exit']}"})
    if findings:
        return report("verify", "mismatch", findings, p=p, assembler_verify=asm_run), 1
    return report("verify", "intact", p=p, assembler_verify=asm_run), 0


# ---------------------------------------------------------------- intake

def intake(output, config_path, book, member, return_file, source_root, artifacts):
    runs = []

    def done(result, code, findings=(), **extra):
        body = {"schema": PROVENANCE_SCHEMA, "result": result, "member": member, "findings": list(findings),
                "runs": runs, "statements": STATEMENTS + [
                    "Intake edits no work page and no returned bytes. Placement below is a proposal only."]}
        body.update(extra)
        return body, code

    try:
        ctx = Context(config_path)
        v1 = ctx.v1
        for path, label in ((book, "book"), (return_file, "return file"), (source_root, "source root")):
            v1.require_absolute(path, label)
        if not isinstance(member, str) or not v1.MEMBER_RE.fullmatch(member):
            raise ColabError("member", "member is not 01NN.slug")
        if not artifacts:
            raise ColabError("artifact", "at least one --artifact is required")
        for name in ("helper", "inspector"):
            v1.pinned_bytes(ctx.v1cfg, name)
    except Exception as exc:  # noqa: BLE001
        if not hasattr(exc, "code"):
            raise
        return done("invalid", 2, [finding(exc)])
    package, code = verify(output, config_path)
    if code != 0:
        return done("package-not-verified", 2, package["findings"])
    handoff = load_json((Path(output) / "handoff.json").read_bytes(), "handoff")
    inv = handoff["investigation"]
    names = handoff["exchange"]
    base = {"package_digest": package["digest"], "binding_sha256": handoff["binding_sha256"],
            "investigation": inv, "exchange": names}
    try:
        first = v1.run_tool(ctx.v1cfg, "inspector", ["inspect", "--book", book, "--member", member, "--json"])
        runs.append(first)
        seen = v1.parse_inspection(first)
    except Exception as exc:  # noqa: BLE001
        if not hasattr(exc, "code"):
            raise
        return done("invalid", 2, [finding(exc)], **base)
    if seen.get("status") not in ("reserved", "complete"):
        return done("not-reserved", 2, [{"kind": "input-defect", "code": "member",
                    "detail": f"member status is {seen.get('status')}"}], **base)
    reservation = seen.get("reservation") or {}
    origin = reservation.get("origin")
    want = {"book": inv["book"], "page": inv["page"], "batch": inv["pass"]}
    if origin != want:
        return done("wrong-origin", 2, [{"kind": "input-defect", "code": "wrong-origin",
                    "detail": f"reservation origin {origin} is not the investigation {want}"}], **base)
    submission = reservation.get("submission_id")
    args = ["capture", "--book", book, "--submission", str(submission), "--return-file", return_file,
            "--source-root", source_root]
    for item in artifacts:
        args += ["--artifact", item]
    try:
        cap = v1.run_tool(ctx.v1cfg, "helper", args)
        runs.append(cap)
        ver = v1.run_tool(ctx.v1cfg, "helper", ["verify", "--book", book, "--member", member])
        runs.append(ver)
        after_run = v1.run_tool(ctx.v1cfg, "inspector", ["inspect", "--book", book, "--member", member, "--json"])
        runs.append(after_run)
        after = v1.parse_inspection(after_run)
    except Exception as exc:  # noqa: BLE001
        if not hasattr(exc, "code"):
            raise
        return done("attention", 1, [finding(exc)], **base)
    capture = after.get("capture") or {}
    replay = "already-captured" in cap["stdout"]
    try:
        presence = v1.heading_presence(v1.read_file(return_file, "return file"))
    except v1.ColabError:
        presence = None
    extra = dict(base, submission=submission, capture=capture, return_headings=presence,
                 helper_capture="already-captured" if replay else ("captured" if cap["exit"] == 0 else "refused"))
    if cap["exit"] != 0 or ver["exit"] != 0 or after.get("status") != "complete":
        return done("attention", 1, [{"kind": "pack-defect", "code": "custody",
                    "detail": f"capture exit {cap['exit']}, verify exit {ver['exit']}, status {after.get('status')}"}], **extra)
    ret = capture.get("return") or {}
    extra["placement"] = {
        "schema": PLACEMENT_SCHEMA,
        "action": "proposed; not written",
        "destination": {"book": inv["book"], "page": inv["page"], "file": names["return_name"]},
        "source": {"member": member, "file": "return.md", "sha256": ret.get("sha256"), "bytes": ret.get("bytes"),
                   "receipt_sha256": capture.get("receipt_sha256"), "manifest_sha256": capture.get("manifest_sha256")},
        "rule": "exact bytes from the verified capture; provenance stays in this record, not in the text",
        "review": f"{names['review_name']} is not created by intake",
    }
    extra["pointer"] = (f"Member {member}. Receipt sha256 {capture.get('receipt_sha256')}. Verify exit 0: result complete; "
                        f"not approved; not accepted; not published. Package digest {package['digest']}.")
    return done("already-captured" if replay else "captured", 0, **extra)


# ---------------------------------------------------------------- CLI

def build_parser():
    parser = argparse.ArgumentParser(description="N7NN Colab exchange-layout v2 support. Drafts and custody only.")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("preview", "prepare", "verify", "intake"):
        item = sub.add_parser(name)
        item.add_argument("--config", required=True)
        item.add_argument("--json", action="store_true", required=True)
        if name in ("preview", "prepare"):
            item.add_argument("--request", required=True)
        if name in ("prepare", "verify", "intake"):
            item.add_argument("--output", required=True)
        if name == "prepare":
            item.add_argument("--digest", required=True)
        if name == "intake":
            item.add_argument("--book", required=True)
            item.add_argument("--member", required=True)
            item.add_argument("--return-file", required=True)
            item.add_argument("--source-root", required=True)
            item.add_argument("--artifact", action="append", default=[])
    return parser


def main(argv=None):
    opts = build_parser().parse_args(argv)
    try:
        if opts.command == "preview":
            body, code = preview(opts.request, opts.config)
        elif opts.command == "prepare":
            body, code = prepare(opts.request, opts.config, opts.output, opts.digest)
        elif opts.command == "verify":
            body, code = verify(opts.output, opts.config)
        else:
            body, code = intake(opts.output, opts.config, opts.book, opts.member, opts.return_file,
                                opts.source_root, opts.artifact)
    except ColabError as exc:
        body, code = report(opts.command, "invalid", [finding(exc)]), 2
    sys.stdout.buffer.write((json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    return code


if __name__ == "__main__":
    sys.exit(main())
