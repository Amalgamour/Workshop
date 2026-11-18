#!/usr/bin/env python3
"""N7 return-pointer intake with N5 compatibility (0707/05.17). NONPRODUCTION lab prototype.

Successor of labs/n7-intake-compat-pass01/n7compat.py (preserved). The grammar is selected by the
source kind that intake already measures (pass01 address_of: N5NN / N7NN), set for the duration of
build_intake through a context variable - the same pattern pass03 uses for p2._resolve_page.
- N5NN, or no kind context: the selected pass03 parser, unchanged (no punctuation refusal, no N7 forms).
- N7NN: the two observed N7 forms first, then the unchanged pass03 line forms:
    Returned: PATH (ATTRIBUTION), sha256 HASH, N bytes.
    Artifact manifest: PATH, sha256 HASH, N bytes.
  The only lexical collision (`Artifact manifest: X, sha256 ...`) reads as the N7 delimiter only here.
Attribution text is descriptive only. Nothing is chosen by file existence; nothing is stripped.
--repo-root DIR points the code root at a disposable copy with the production layout (lab only).

usage: n7compat2.py [--patch] [--repo-root DIR] <workbook command and flags>
"""

from __future__ import annotations

import contextvars
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
LIVE = Path(r"D:\Git\lib-build")
V7_JSON = LIVE / "app/review-loop-v7.json"
PACK17 = LIVE / "00.kernel/00.00.10.work/0707.app-use-check/evidence/pack05.17/source-manifest.json"
PATH = r"([A-Za-z0-9][A-Za-z0-9._/-]*)"
RETURNED_RE = re.compile(r"^Returned: " + PATH + r" \(([^()]{1,160})\), sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.$")
N7_MANIFEST_RE = re.compile(r"^Artifact manifest: " + PATH + r", sha256 ([0-9a-f]{64}), ([0-9]+) bytes\.$")
SHA_ANY = re.compile(r"[0-9a-f]{64}")
LABEL_WORDS = ("Submission:", "Artifact manifest:", "Verification:", "Returned:")
KIND = contextvars.ContextVar("n7_source_kind", default=None)


def load_pass03():
    v7 = V7_JSON.read_bytes()
    pins = {f["path"]: f for f in json.loads(PACK17.read_text(encoding="utf-8"))["files"]}
    if hashlib.sha256(v7).hexdigest() != pins["app/review-loop-v7.json"]["sha256"]:
        raise SystemExit("refused: review-loop-v7.json differs from its pack05.17 pin")
    item = json.loads(v7)["tools"]["workbook"]
    path = LIVE / item["path"]
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != item["sha256"] or len(data) != item["bytes"]:
        raise SystemExit("refused: workbook pass03 differs from its v7 pin")
    spec = importlib.util.spec_from_file_location("workbook_review_pass03", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_parser(p3, kind_fn=None):
    """Return a kind-selecting parser. kind_fn() gives the source kind; default: the intake context."""
    original = p3.parse_pointer          # the selected pass03 parser, captured before any replacement
    p2 = p3.p2
    kind_of = kind_fn or KIND.get

    def n7_parse(body):
        findings = []
        parsed = {"findings": findings, "manifest": None, "state": "absent", "submission": None, "verification": None}
        if body is None:
            findings.append({"code": "return-pointer-absent", "path": None})
            return parsed
        stripped = body.strip()
        if stripped == "":
            findings.append({"code": "return-pointer-empty", "path": None})
            parsed["state"] = "empty"
            return parsed
        if stripped == "PENDING.":
            findings.append({"code": "return-pending", "path": None})
            parsed["state"] = "pending"
            return parsed
        fields = {"Submission": None, "Artifact manifest": None, "Verification": None}
        ambiguous = set()
        for raw_line in body.split("\n"):
            line = raw_line.strip()
            if line == "" or line.startswith("Invocation/claim:"):
                continue
            ret = RETURNED_RE.fullmatch(line)
            if ret:
                attribution = ret.group(2)
                if SHA_ANY.search(attribution) or any(w in attribution for w in LABEL_WORDS):
                    findings.append({"code": "attribution-not-descriptive", "path": None, "text": line[:180]})
                    continue
                p3.accept_field(fields, ambiguous, findings, "Submission", {
                    "attribution_text": attribution, "bytes": int(ret.group(4)), "declared_form": "n7-returned",
                    "path": ret.group(1), "sha256": ret.group(3)})
                continue
            man = N7_MANIFEST_RE.fullmatch(line)
            if man:
                p3.accept_field(fields, ambiguous, findings, "Artifact manifest", {
                    "bytes": int(man.group(3)), "declared_form": "n7-manifest", "path": man.group(1), "sha256": man.group(2)})
                continue
            # unchanged pass03 line forms (same order, same acceptance, no added refusal)
            counted = p3.COUNT_RE.fullmatch(line)
            if counted and counted.group(6) in p3.COUNT_TAILS:
                p3.accept_field(fields, ambiguous, findings, counted.group(1), {
                    "bytes": int(counted.group(4)), "file_count": int(counted.group(5)), "path": counted.group(2), "sha256": counted.group(3)})
                continue
            match = p3.FIELD_RE.fullmatch(line)
            if match and p2.suffix_ok(match.group(5)):
                p3.accept_field(fields, ambiguous, findings, match.group(1), {
                    "bytes": int(match.group(4)), "path": match.group(2), "sha256": match.group(3)})
                continue
            findings.append({"code": "unparsed-return-line", "path": None, "text": line[:180]})
        parsed["submission"] = fields["Submission"]
        parsed["manifest"] = fields["Artifact manifest"]
        parsed["verification"] = fields["Verification"]
        parsed["state"] = "ambiguous" if ambiguous else "parsed"
        if parsed["submission"] is None and "Submission" not in ambiguous:
            findings.append({"code": "submission-not-declared", "path": None})
        return parsed

    def parse_pointer(body):
        return n7_parse(body) if kind_of() == "N7NN" else original(body)

    parse_pointer.original = original
    return parse_pointer


def install(p3, patch: bool, repo_root: str | None):
    if repo_root:
        root = Path(repo_root).resolve()
        p3.wb.REPO = root
        p3.p2.REPO = root
        p3.REPO = root
    if patch:
        parse = make_parser(p3)
        build = p3.p2.build_intake                    # pass03's installed build_intake

        def build_intake(book, source, pass_id):
            kind = p3.wb.address_of(source, pass_id).get("kind")
            token = KIND.set(kind)
            try:
                return build(book, source, pass_id)
            finally:
                KIND.reset(token)

        for ns in (p3, p3.p2, p3.wb):
            ns.parse_pointer = parse
            ns.build_intake = build_intake
    return p3


def main(argv=None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    patch = "--patch" in args
    args = [x for x in args if x != "--patch"]
    root = None
    if "--repo-root" in args:
        i = args.index("--repo-root")
        root = args[i + 1]
        del args[i:i + 2]
    p3 = install(load_pass03(), patch, root)
    return p3.main(args)


if __name__ == "__main__":
    sys.exit(main())
