"""Mechanical checks for baseline-01. Each check states what it establishes and what it does not.

Run: python -I -B tools/check.py TASK OUTPUT_FILE [--reviewed] [--json OUT]
OUTPUT_FILE holds the model's reply exactly as saved (see PROTOCOL.md, transfer path).
T3 executes the returned code only with --reviewed, after a person has read it. That run is not sandboxed.
Exit 0 when every check passes, 1 when any fails, 2 on a usage error.
"""
import ast
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "tasks"


def res(name, ok, establishes, not_established, detail=None):
    return {"check": name, "pass": bool(ok), "establishes": establishes, "does_not_establish": not_established, "detail": detail}


def first_diff(a, b):
    n = next((i for i, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
    return {"offset": n, "expected": a[max(0, n - 12):n + 12].decode("utf-8", "replace"), "got": b[max(0, n - 12):n + 12].decode("utf-8", "replace")}


def t1(out, _):
    src = (T / "T1-copy" / "source.txt").read_bytes()
    a, b = b"<<<COPY\n", b"\nCOPY>>>"
    i = out.find(a)
    j = out.find(b, i + len(a)) if i >= 0 else -1
    if i < 0 or j < 0:
        return [res("markers-found", False, "the reply contains both marker lines", "anything about the copy", "a marker is missing")]
    span = out[i + len(a):j]
    outside = (out[:i] + out[j + len(b):]).strip()
    return [
        res("markers-found", True, "the reply contains both marker lines", "anything about the copy"),
        res("bytes-identical", span == src, "the text between the markers equals the source byte for byte",
            "that the surface or copy path did not alter bytes before saving; a failure may come from the transfer path",
            None if span == src else {"source_bytes": len(src), "got_bytes": len(span), **first_diff(src, span)}),
        res("nothing-outside-markers", not outside, "the reply has no other text outside the markers",
            "anything about the copy itself", None if not outside else outside[:120].decode("utf-8", "replace")),
    ]


def t2(out, _):
    text = out.decode("utf-8", "replace").strip()
    m = re.fullmatch(r"```(?:json)?\s*\n(.*?)\n```", text, re.S)
    fenced = m is not None
    try:
        got = json.loads(m.group(1) if m else text)
    except ValueError as e:
        return [res("json-parses", False, "the reply (or its single json fence) parses as JSON", "anything about content", str(e))]
    want = json.loads((T / "T2-struct" / "expected.json").read_text(encoding="utf-8"))
    keys = {"id", "title", "owner", "due", "state"}
    shape = isinstance(got, list) and all(isinstance(r, dict) and set(r) == keys for r in got)
    out = [res("json-parses", True, "the reply parses as JSON", "anything about content", "inside a code fence" if fenced else None),
           res("exact-keys", shape, "an array whose every object has exactly the five keys", "that the values are right")]
    if not shape:
        return out
    ids_got, ids_want = [r["id"] for r in got], [r["id"] for r in want]
    out.append(res("same-ids", sorted(ids_got) == sorted(ids_want), "the set of ids equals the answer key (I-109 excluded, none missing)",
                   "that the other fields are right", {"missing": sorted(set(ids_want) - set(ids_got)), "extra": sorted(set(ids_got) - set(ids_want))}))
    out.append(res("ordered-by-id", ids_got == sorted(ids_got), "objects are in id order", "anything else"))
    by = {r["id"]: r for r in got}
    wrong = [{"id": w["id"], "field": k, "want": w[k], "got": by[w["id"]][k]} for w in want if w["id"] in by for k in sorted(keys) if by[w["id"]][k] != w[k]]
    out.append(res("values-equal-key", not wrong, "every field of every matched id equals the fixed answer key",
                   "correctness beyond this one note; the key was written by the preparer", wrong or None))
    return out


def defs(tree):
    return {n.name: ast.dump(n) for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))}


def top_names(tree):
    names = set()
    for n in tree.body:
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            names |= {"import " + (a.asname or a.name) for a in n.names}
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(n.name)
        elif isinstance(n, (ast.Assign, ast.AnnAssign)):
            names.add("assign " + ast.unparse(n)[:40])
    return names


def t3(out, reviewed):
    text = out.decode("utf-8", "replace")
    blocks = re.findall(r"^```python[^\n]*\n(.*?)^```", text, re.S | re.M)
    rest = re.sub(r"^```python[^\n]*\n.*?^```", "", text, flags=re.S | re.M).strip()
    r = [res("one-python-block", len(blocks) == 1, "the reply holds exactly one ```python block", "anything about the code", f"{len(blocks)} blocks"),
         res("nothing-outside-block", not rest, "no other text outside the block", "anything about the code", rest[:120] or None)]
    if len(blocks) != 1:
        return r
    code = blocks[0]
    try:
        new = ast.parse(code)
    except SyntaxError as e:
        return r + [res("parses", False, "the code parses as Python", "that it runs or is correct", str(e))]
    old = ast.parse((T / "T3-code" / "ledger.py").read_text(encoding="utf-8"))
    od, nd = defs(old), defs(new)
    touched = sorted(k for k in od if k != "parse_amount" and nd.get(k) != od[k])
    r += [res("parses", True, "the code parses as Python", "that it runs or is correct"),
          res("others-ast-identical", not touched, "parse_line, total and format_cents are AST-identical to the original (docstrings included; comments and blank lines ignored)",
              "that parse_amount is right, or that behaviour elsewhere is unchanged at runtime", touched or None),
          res("no-new-top-level", top_names(new) == top_names(old), "no top-level imports, functions, classes or assignments were added or removed",
              "anything inside function bodies", sorted(top_names(new) ^ top_names(old)) or None)]
    if not reviewed:
        return r + [res("heldout-tests", False, "NOT RUN: pass --reviewed after reading the code", "anything", "skipped")]
    tmp = Path(tempfile.mkdtemp(prefix="baseline01-t3-"))
    try:
        (tmp / "ledger.py").write_text(code, encoding="utf-8", newline="\n")
        shutil.copy(T / "T3-code" / "tests_heldout.py", tmp)
        p = subprocess.run([sys.executable, "-I", "-B", str(tmp / "tests_heldout.py")], capture_output=True, text=True, timeout=60, cwd=tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    fails = [l for l in p.stderr.splitlines() if l.startswith(("FAIL:", "ERROR:"))]
    return r + [res("heldout-tests", p.returncode == 0, "the 6 held-out tests pass (13 new-behaviour inputs, 10 kept-behaviour inputs, parse_line, total, format_cents)",
                    "correctness on inputs these tests do not cover", fails or None)]


def rules(text):
    found, cur = [], None
    for line in text.splitlines():
        m = re.match(r"\s*\**(R\d\d)\.?\**", line)
        if m:
            cur = [m.group(1), line[m.end():]]
            found.append(cur)
        elif cur and line.strip():
            cur[1] += " " + line
    return found


def modal_counts(s):
    return {"MUST NOT": len(re.findall(r"\bMUST NOT\b", s)), "MUST": len(re.findall(r"\bMUST\b(?! NOT)", s)), "MAY": len(re.findall(r"\bMAY\b", s))}


def t4(out, _):
    text = out.decode("utf-8", "replace")
    m = re.fullmatch(r"\s*```(?:markdown|md)?\s*\n(.*?)\n```\s*", text, re.S)
    text = m.group(1) if m else text
    src = dict(rules((T / "T4-spec" / "spec.md").read_text(encoding="utf-8")))
    got = rules(text)
    ids = [g[0] for g in got]
    r = [res("ids-once-in-order", ids == list(src), "rule ids R01-R11 each appear once, at line start, in order",
             "that each rule still says the same thing", {"got": ids})]
    gd = dict(got)
    lost_tok, lost_num, modal = [], [], []
    for rid, body in src.items():
        g = gd.get(rid, "")
        lost_tok += [f"{rid}: `{t}`" for t in re.findall(r"`([^`]+)`", body) if f"`{t}`" not in g]
        lost_num += [f"{rid}: {n}" for n in re.findall(r"\d+", body) if not re.search(rf"(?<!\d){n}(?!\d)", g)]
        if rid in gd and modal_counts(g) != modal_counts(body):
            modal.append({"rule": rid, "source": modal_counts(body), "got": modal_counts(g)})
    r.append(res("backtick-spans-kept", not lost_tok, "every backticked span of each source rule appears, in backticks, in the same rule",
                 "that it is used with the same meaning", lost_tok or None))
    r.append(res("numbers-kept", not lost_num, "every number of each source rule appears in the same rule", "that it still qualifies the same thing", lost_num or None))
    r.append(res("modal-counts-equal", not modal, "each rule has the same count of MUST, MUST NOT and MAY as the source",
                 "INDICATOR ONLY: equal counts do not show equal obligations, and a difference is not by itself an error; it directs human review", modal or None))
    return r


def words(s):
    return re.findall(r"[A-Za-zÀ-ɏ0-9]+(?:['’-][A-Za-zÀ-ɏ0-9]+)*", s)


def t5a(out, _):
    c = json.loads((T / "T5a-prose" / "constraints.json").read_text(encoding="utf-8"))
    text = out.decode("utf-8", "replace")
    n = len(words(text))
    low = text.lower()
    missing = [q for q in c["required"] if q not in low]
    used = sorted({w for w in words(low) if w in c["forbidden"]})
    return [res("word-count", c["words"][0] <= n <= c["words"][1], f"{c['words'][0]}-{c['words'][1]} words by this tool's word rule", "length as a reader would count it", n),
            res("required-phrases", not missing, "each required phrase appears verbatim (case-insensitive)", "that it is used meaningfully", missing or None),
            res("forbidden-absent", not used, "none of the forbidden words appears as a whole word", "anything about quality", used or None)]


def ngrams(ws, n=8):
    return {tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)}


def t5b(out, _):
    sample = T / "T5b-voice" / "VOICE-SAMPLE.txt"
    if not sample.exists():
        return [res("sample-present", False, "the voice sample exists", "anything", "T5b is withheld")]
    ws, ss = [w.lower() for w in words(out.decode("utf-8", "replace"))], [w.lower() for w in words(sample.read_text(encoding="utf-8"))]
    shared = len(ngrams(ws) & ngrams(ss))
    return [res("word-count", 300 <= len(ws) <= 400, "300-400 words by this tool's word rule", "anything about voice", len(ws)),
            res("no-long-copying", shared == 0, "no 8-word run is copied from the sample", "that the voice matches; that is a human judgment", shared)]


CHECKS = {"T1": t1, "T2": t2, "T3": t3, "T4": t4, "T5a": t5a, "T5b": t5b}


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) < 2 or args[0] not in CHECKS:
        print(__doc__, file=sys.stderr)
        return 2
    out_json = argv[argv.index("--json") + 1] if "--json" in argv else None
    if out_json in args:
        args.remove(out_json)
    results = CHECKS[args[0]](Path(args[1]).read_bytes(), "--reviewed" in argv)
    report = {"schema": "baseline-check/1", "task": args[0], "output": args[1], "all_pass": all(x["pass"] for x in results), "checks": results}
    text = json.dumps(report, indent=1, ensure_ascii=False)
    if out_json:
        Path(out_json).write_text(text + "\n", encoding="utf-8", newline="\n")
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    print(text)
    return 0 if report["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
