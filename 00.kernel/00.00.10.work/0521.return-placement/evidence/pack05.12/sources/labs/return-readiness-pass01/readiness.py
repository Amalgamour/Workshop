#!/usr/bin/env python3
"""Read-only return-route readiness.

The public command observes two dispatch branches and one book. It does not
select a route, write a file, or assess a release. inspect(..., read_bytes=...)
is a unit fault-injection seam. The command line has no injection flag.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPARSE = 0x400
SCHEMA = "return-route-readiness/1"
DISPATCHER_REL = "app/librarian.py"
COMMANDS = ("return-lines", "capture-return")
LAYOUT_KEYS = {"schema", "book", "allocation", "sequential_allocation", "bands"}
WARNINGS = (
    "An unselected successor does not protect the app.",
    "A guard on an undeclared book delegates to the historical writer.",
    "Historical direct scripts remain runnable.",
)
NEXT_CHECKS = (
    "Prime reviews this observation before any app selection.",
    "After the review-loop repair is reviewed, measure the then-current dispatcher and apply only the two branch substitutions in build05.09/SELECTION.md.",
    "A separate Director release is required before roots or a physical migration.",
    "Remeasure dependency bytes at selection time. A mismatch stops selection.",
    "Historical direct scripts stay runnable until a reviewed route is actually selected.",
)
LIMITS = (
    "The static pattern does not prove Python runtime behavior.",
    "Other dispatch branches are not classified.",
    "The whole dispatcher hash is provenance, not a pin.",
    "Authority is not assessed and no release file is sought.",
    "A declared book and a selected facade do not confine historical scripts.",
    "Predecessor status app_selected is not read as dispatch evidence.",
    "Unreachable duplicate branches count as ambiguous.",
)
PROVENANCE = (
    "0521.return-placement/05.09",
    "0521.return-placement/06.18.md",
    "0521.return-placement/evidence/prime-review05.09/OPERATOR-ADDENDUM.md",
    "0521.return-placement/evidence/build05.09/SELECTION.md",
)


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def default_read(path: str) -> bytes:
    with open(path, "rb") as handle:
        return handle.read()


def contracts() -> dict:
    path = Path(__file__).resolve().parent / "contracts.json"
    body = json.loads(path.read_text(encoding="utf-8"))
    if body.get("schema") != "return-route-readiness-contracts/1" or body.get("version") != 1:
        raise Refuse("readiness contracts schema is wrong")
    sample = canonical_layout(body["layout"]["known_book"])
    if sha(sample) != body["layout"]["known_sha256"] or len(sample) != body["layout"]["known_bytes"]:
        raise Refuse("layout identity drifted from the readiness contract")
    return body


def canonical_layout(name: str) -> bytes:
    body = {
        "allocation": "line-pass",
        "bands": {"5": "matched-workflow-return-line", "7": "page-local-colab"},
        "book": name,
        "schema": "return-line-layout/1",
        "sequential_allocation": False,
    }
    return (json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")


def book_name_ok(name: object) -> bool:
    return isinstance(name, str) and bool(name) and len(name) <= 4096 and all(
        ch not in name for ch in "/\\\n\r"
    )


def is_reparse(path: str) -> bool:
    info = os.lstat(path)
    attrs = getattr(info, "st_file_attributes", 0) or 0
    return bool(attrs & REPARSE) or stat.S_ISLNK(info.st_mode)


def safe_rel(rel: str) -> bool:
    if not isinstance(rel, str) or rel == "" or "\\" in rel or ":" in rel or rel.startswith("/"):
        return False
    parts = rel.split("/")
    return all(part not in ("", ".", "..") for part in parts)


def inside(root: str, full: str) -> bool:
    try:
        root_n = os.path.normcase(os.path.abspath(root))
        full_n = os.path.normcase(os.path.abspath(full))
        return os.path.commonpath([root_n, full_n]) == root_n
    except ValueError:
        return False


def blank_identity(rel: str) -> dict:
    return {"bytes": None, "data": None, "path": rel, "sha256": None, "sha256_reread": None, "state": "missing"}


def read_identity(root: Path, rel: str, read_bytes) -> dict:
    row = blank_identity(rel)
    if not safe_rel(rel):
        row["state"] = "escaping"
        return row
    full = os.path.abspath(str(root.joinpath(*rel.split("/"))))
    if not inside(str(root), full):
        row["state"] = "escaping"
        return row
    if not os.path.lexists(full):
        return row
    if is_reparse(full):
        row["state"] = "linked"
        return row
    info = os.lstat(full)
    if not stat.S_ISREG(info.st_mode):
        row["state"] = "wrong-type"
        return row
    if info.st_nlink != 1:
        row["state"] = "linked"
        return row
    first = read_bytes(full)
    second = read_bytes(full)
    row["bytes"] = len(first)
    row["sha256"] = sha(first)
    row["sha256_reread"] = sha(second)
    if first != second:
        row["state"] = "unstable"
        return row
    row["data"] = first
    row["state"] = "file"
    return row


def public_row(row: dict, root_label: str) -> dict:
    return {
        "bytes": row["bytes"],
        "path": row["path"],
        "root": root_label,
        "sha256": row["sha256"],
        "state": row["state"],
    }


def is_simple(test: ast.AST) -> str | None:
    if not isinstance(test, ast.Compare) or len(test.ops) != 1 or not isinstance(test.ops[0], ast.Eq):
        return None
    if not isinstance(test.left, ast.Name) or test.left.id != "command" or len(test.comparators) != 1:
        return None
    value = test.comparators[0]
    if isinstance(value, ast.Constant) and isinstance(value.value, str):
        return value.value
    return None


def in_membership_tuple(parents: tuple[ast.AST, ...]) -> bool:
    if len(parents) < 2 or not isinstance(parents[-1], ast.Tuple) or not isinstance(parents[-2], ast.Compare):
        return False
    compare = parents[-2]
    if len(compare.ops) != 1 or not isinstance(compare.ops[0], (ast.In, ast.NotIn)):
        return False
    return parents[-1] in compare.comparators


def mention_kind(test: ast.AST, command: str) -> str:
    if is_simple(test) == command:
        return "simple"
    saw = False
    other = False

    def walk(node: ast.AST, parents: tuple[ast.AST, ...]) -> None:
        nonlocal saw, other
        if isinstance(node, ast.Constant) and node.value == command:
            saw = True
            if not in_membership_tuple(parents):
                other = True
        for child in ast.iter_child_nodes(node):
            walk(child, parents + (node,))

    walk(test, ())
    if not saw:
        return "none"
    if other:
        return "other"
    return "activation"


def path_call(node: ast.AST) -> bool:
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "Path"
        and len(node.args) == 1
        and not node.keywords
        and isinstance(node.args[0], ast.Name)
        and node.args[0].id == "__file__"
    )


def parent_expr(node: ast.AST) -> bool:
    if not isinstance(node, ast.Attribute) or node.attr != "parent":
        return False
    inner = node.value
    if isinstance(inner, ast.Call) and isinstance(inner.func, ast.Attribute) and inner.func.attr == "resolve":
        if inner.args or inner.keywords:
            return False
        inner = inner.func.value
    return path_call(inner)


def facade_literal(call: ast.Call) -> str | None:
    if not isinstance(call.func, ast.Name) or call.func.id != "load_module":
        return None
    if len(call.args) != 2 or call.keywords:
        return None
    path_arg, name_arg = call.args
    if not isinstance(name_arg, ast.Constant) or not isinstance(name_arg.value, str):
        return None
    if not isinstance(path_arg, ast.BinOp) or not isinstance(path_arg.op, ast.Div):
        return None
    right = path_arg.right
    if not isinstance(right, ast.Constant) or not isinstance(right.value, str):
        return None
    filename = right.value
    if "/" in filename or "\\" in filename or not filename.endswith(".py") or filename in ("", ".", ".."):
        return None
    if not parent_expr(path_arg.left):
        return None
    return filename


def load_calls(statements: list[ast.stmt]) -> list[ast.Call]:
    found = []
    for stmt in statements:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "load_module":
                found.append(node)
    return found


def recognize(source: str) -> dict:
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {"routes": {}, "state": "malformed"}
    routes = {}
    for command in COMMANDS:
        simple = []
        other = False
        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            kind = mention_kind(node.test, command)
            if kind == "other":
                other = True
            elif kind == "simple":
                simple.append(node)
        if other:
            routes[command] = {"facade": None, "state": "unsupported"}
            continue
        if not simple:
            routes[command] = {"facade": None, "state": "absent"}
            continue
        if len(simple) != 1:
            routes[command] = {"facade": None, "state": "ambiguous"}
            continue
        node = simple[0]
        if load_calls(node.orelse):
            routes[command] = {"facade": None, "state": "unsupported"}
            continue
        loads = load_calls(node.body)
        if len(loads) != 1:
            routes[command] = {"facade": None, "state": "unsupported"}
            continue
        filename = facade_literal(loads[0])
        if filename is None:
            routes[command] = {"facade": None, "state": "unsupported"}
            continue
        routes[command] = {"facade": filename, "state": "recognized"}
    return {"routes": routes, "state": "parsed"}


def blank_route(state: str) -> dict:
    return {
        "declaration_matches_contract": None,
        "dependencies": [],
        "facade_matches_contract": None,
        "mismatches": [],
        "predecessor_matches_contract": None,
        "predecessor_present": False,
        "selected_facade": None,
        "selector": "none",
        "staged_notes": [],
        "state": state,
        "successor_matches_contract": None,
        "successor_path": None,
        "successor_staged": False,
    }


def same_bytes(row: dict, spec: dict) -> bool:
    return row["state"] == "file" and row["sha256"] == spec["sha256"] and row["bytes"] == spec["bytes"]


def problem(row: dict, label: str) -> str | None:
    if row["state"] == "file":
        return None
    if row["state"] == "missing":
        return f"{label} missing"
    if row["state"] == "linked":
        return f"{label} linked"
    if row["state"] == "wrong-type":
        return f"{label} wrong-type"
    if row["state"] == "escaping":
        return f"{label} escaping"
    return f"{label} {row['state']}"


def remember(reads: dict, row: dict, root_label: str) -> None:
    reads[(root_label, row["path"])] = public_row(row, root_label)


def successor_fields(code_root: Path, spec: dict, selector: str, read_bytes, reads: dict) -> dict:
    facade = read_identity(code_root, spec["facade"]["path"], read_bytes)
    declaration = read_identity(code_root, spec["declaration"]["path"], read_bytes)
    remember(reads, facade, "code")
    remember(reads, declaration, "code")
    facade_match = same_bytes(facade, spec["facade"])
    declaration_match = same_bytes(declaration, spec["declaration"])
    notes = []
    if facade["state"] != "missing" and not facade_match and facade["state"] != "unstable":
        notes.append("staged facade bytes differ")
    if declaration["state"] != "missing" and not declaration_match and declaration["state"] != "unstable":
        notes.append("staged declaration bytes differ")
    exists = facade["state"] == "file"
    return {
        "notes": notes,
        "successor_matches_contract": facade_match and declaration_match if exists or declaration["state"] == "file" else None,
        "successor_path": spec["facade"]["path"],
        "successor_staged": exists and selector != "new",
        "unstable": facade["state"] == "unstable" or declaration["state"] == "unstable",
    }


def predecessor_fields(code_root: Path, spec: dict, selector: str, read_bytes, reads: dict) -> dict:
    row = read_identity(code_root, spec["facade"]["path"], read_bytes)
    remember(reads, row, "code")
    return {
        "predecessor_matches_contract": same_bytes(row, spec["facade"]) if row["state"] == "file" else False if row["state"] != "missing" else None,
        "predecessor_present": row["state"] == "file" and selector != "old",
        "unstable": row["state"] == "unstable",
    }


def evaluate_route(code_root: Path, command: str, recognized: dict, pinned: dict, read_bytes, reads: dict) -> dict:
    sides = pinned["routes"][command]
    names = {Path(item["facade"]["path"]).name: side for side, item in sides.items()}
    if recognized["state"] != "recognized":
        route = blank_route(recognized["state"])
        staged = successor_fields(code_root, sides["new"], "none", read_bytes, reads)
        route["staged_notes"] = staged["notes"]
        route["successor_matches_contract"] = staged["successor_matches_contract"]
        route["successor_path"] = staged["successor_path"]
        route["successor_staged"] = staged["successor_staged"]
        if staged["unstable"]:
            route["state"] = "unstable"
        return route
    filename = recognized["facade"]
    selector = names.get(filename)
    if selector is None:
        route = blank_route("unknown")
        route["selected_facade"] = f"app/{filename}"
        route["selector"] = "unknown"
        staged = successor_fields(code_root, sides["new"], "unknown", read_bytes, reads)
        route["staged_notes"] = staged["notes"]
        route["successor_matches_contract"] = staged["successor_matches_contract"]
        route["successor_path"] = staged["successor_path"]
        route["successor_staged"] = staged["successor_staged"]
        if staged["unstable"]:
            route["state"] = "unstable"
        return route
    chosen = sides[selector]
    route = blank_route("selected-but-invalid")
    route["selector"] = selector
    route["selected_facade"] = chosen["facade"]["path"]
    facade = read_identity(code_root, chosen["facade"]["path"], read_bytes)
    declaration = read_identity(code_root, chosen["declaration"]["path"], read_bytes)
    remember(reads, facade, "code")
    remember(reads, declaration, "code")
    mismatches = []
    unstable = facade["state"] == "unstable" or declaration["state"] == "unstable"
    facade_problem = problem(facade, "facade")
    if facade_problem:
        mismatches.append(facade_problem)
    elif not same_bytes(facade, chosen["facade"]):
        mismatches.append("facade bytes differ")
    declaration_problem = problem(declaration, "declaration")
    if declaration_problem:
        mismatches.append(declaration_problem)
    elif not same_bytes(declaration, chosen["declaration"]):
        mismatches.append("declaration bytes differ")
    dependencies = []
    for item in chosen["dependencies"]:
        row = read_identity(code_root, item["path"], read_bytes)
        remember(reads, row, "code")
        unstable = unstable or row["state"] == "unstable"
        matched = same_bytes(row, item)
        dependencies.append({
            "bytes": row["bytes"],
            "matches_contract": matched,
            "path": item["path"],
            "role": item["role"],
            "sha256": row["sha256"],
            "state": row["state"],
        })
        item_problem = problem(row, f"dependency {item['role']}")
        if item_problem:
            mismatches.append(item_problem)
        elif not matched:
            mismatches.append(f"dependency bytes differ: {item['role']}")
    staged = successor_fields(code_root, sides["new"], selector, read_bytes, reads)
    prior = predecessor_fields(code_root, sides["old"], selector, read_bytes, reads)
    unstable = unstable or staged["unstable"] or prior["unstable"]
    route["dependencies"] = dependencies
    route["facade_matches_contract"] = same_bytes(facade, chosen["facade"])
    route["declaration_matches_contract"] = same_bytes(declaration, chosen["declaration"])
    route["mismatches"] = [] if unstable else mismatches
    route["predecessor_matches_contract"] = prior["predecessor_matches_contract"]
    route["predecessor_present"] = prior["predecessor_present"]
    route["staged_notes"] = staged["notes"]
    route["state"] = "unstable" if unstable else "selected-valid" if not mismatches else "selected-but-invalid"
    route["successor_matches_contract"] = staged["successor_matches_contract"]
    route["successor_path"] = staged["successor_path"]
    route["successor_staged"] = staged["successor_staged"]
    return route


def parse_layout(data: bytes) -> tuple[str, str | None]:
    def pairs(seq):
        obj = {}
        for key, value in seq:
            if not isinstance(key, str) or key in obj:
                raise ValueError("duplicate")
            obj[key] = value
        return obj

    try:
        parsed = json.loads(data.decode("utf-8"), object_pairs_hook=pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError):
        return "malformed", None
    book = parsed.get("book") if isinstance(parsed, dict) else None
    book_text = book if isinstance(book, str) else None
    if book_name_ok(book_text) and data == canonical_layout(book_text):
        return "valid", book_text
    return "conflicting", book_text


def measure_layout(book: Path, read_bytes) -> dict:
    row = read_identity(book, "return-line-layout.json", read_bytes)
    body = {
        "book": None,
        "bytes": row["bytes"],
        "path": row["path"],
        "sha256": row["sha256"],
        "state": row["state"] if row["state"] != "file" else "conflicting",
    }
    if row["state"] == "file":
        state, name = parse_layout(row["data"])
        body["state"] = state
        body["book"] = name
    return body


def measure_door(book: Path, name: str, read_bytes, reads: dict) -> dict:
    full = os.path.abspath(str(book / name))
    if not inside(str(book), full) or not safe_rel(name):
        return {"page": None, "state": "escaping"}
    if not os.path.lexists(full):
        return {"page": None, "state": "missing"}
    if is_reparse(full):
        return {"page": None, "state": "linked"}
    info = os.lstat(full)
    if not stat.S_ISDIR(info.st_mode):
        return {"page": None, "state": "wrong-type"}
    page = read_identity(book, f"{name}/01.md", read_bytes)
    remember(reads, page, "book")
    return {"page": public_row(page, "book"), "state": "present"}


def prerequisites(routes: dict, declared: bool) -> list[str]:
    items = []
    if not declared:
        items.append("the book has no valid line-pass declaration")
    ready = all(
        routes[name]["state"] == "selected-valid" and routes[name]["selector"] == "new"
        for name in COMMANDS
    )
    if not ready:
        items.append("the reviewed successor is not selected on both routes")
    items.append("migration and release authority were not assessed")
    items.append("no Director release is recorded by this tool")
    return items


def observation(code_root: Path, book: Path, code_text: str, book_text: str, dispatcher: dict, routes: dict, door: dict, layout: dict, reads: dict) -> dict:
    declared = door["state"] == "present" and layout["state"] == "valid"
    return {
        "app_selection_applied": False,
        "approval": "not-established",
        "authority": "not-assessed",
        "authorization": False,
        "book": book_text,
        "book_declaration": {"declared": declared, "door": door, "layout": layout},
        "code_root": code_text,
        "completion": "not-established",
        "dispatcher": dispatcher,
        "historical_status_note": "A static app_selected field in predecessor status is a historical tool claim. It is not this dispatch measurement.",
        "limits": list(LIMITS),
        "migration_assessed": False,
        "missing_prerequisites": prerequisites(routes, declared),
        "next_checks": list(NEXT_CHECKS),
        "provenance": list(PROVENANCE),
        "reads": [reads[key] for key in sorted(reads)],
        "recognizer": "static-ast-pattern",
        "routes": routes,
        "schema": SCHEMA,
        "selection_is_authorization": False,
        "task_association": "not-established",
        "warnings": list(WARNINGS),
    }


def inspect(code_root: Path, book: Path, *, read_bytes=default_read, code_text: str | None = None, book_text: str | None = None) -> dict:
    pinned = contracts()
    code_text = str(code_root) if code_text is None else code_text
    book_text = str(book) if book_text is None else book_text
    reads: dict = {}
    dispatcher_row = read_identity(code_root, DISPATCHER_REL, read_bytes)
    remember(reads, dispatcher_row, "code")
    prior = pinned["predecessor_dispatcher"]
    dispatcher = {
        "bytes": dispatcher_row["bytes"],
        "matches_predecessor_snapshot": dispatcher_row["state"] == "file" and same_bytes(dispatcher_row, prior),
        "path": DISPATCHER_REL,
        "predecessor_bytes": prior["bytes"],
        "predecessor_sha256": prior["sha256"],
        "sha256": dispatcher_row["sha256"],
        "sha256_reread": dispatcher_row["sha256_reread"],
        "state": "measured" if dispatcher_row["state"] == "file" else dispatcher_row["state"],
        "whole_file_hash_is_provenance": True,
    }
    layout = measure_layout(book, read_bytes)
    remember(reads, {
        "bytes": layout["bytes"],
        "path": layout["path"],
        "sha256": layout["sha256"],
        "state": "file" if layout["state"] in {"valid", "conflicting", "malformed"} else layout["state"],
    }, "book")
    door = measure_door(book, pinned["door"], read_bytes, reads)
    if dispatcher_row["state"] == "unstable":
        routes = {name: blank_route("unstable") for name in COMMANDS}
        dispatcher["state"] = "unstable"
        return observation(code_root, book, code_text, book_text, dispatcher, routes, door, layout, reads)
    if dispatcher_row["state"] != "file":
        state = "absent" if dispatcher_row["state"] == "missing" else "unsupported"
        routes = {name: blank_route(state) for name in COMMANDS}
        return observation(code_root, book, code_text, book_text, dispatcher, routes, door, layout, reads)
    parsed = recognize(dispatcher_row["data"].decode("utf-8"))
    if parsed["state"] != "parsed":
        routes = {name: blank_route("unsupported") for name in COMMANDS}
        dispatcher["state"] = "malformed"
        return observation(code_root, book, code_text, book_text, dispatcher, routes, door, layout, reads)
    routes = {}
    unstable = False
    for command in COMMANDS:
        routes[command] = evaluate_route(code_root, command, parsed["routes"][command], pinned, read_bytes, reads)
        unstable = unstable or routes[command]["state"] == "unstable"
    if unstable:
        routes = {name: blank_route("unstable") for name in COMMANDS}
        dispatcher["state"] = "unstable"
    return observation(code_root, book, code_text, book_text, dispatcher, routes, door, layout, reads)


def project_text(body: dict) -> str:
    lines = [
        body["schema"],
        f"authority: {body['authority']}",
        "authorization: false",
    ]
    for name in COMMANDS:
        route = body["routes"][name]
        facade = route["selected_facade"] or "-"
        lines.append(f"{name}: {route['state']} {route['selector']} {facade}")
        lines.append(f"successor {name} staged: {str(route['successor_staged']).lower()}")
    book = body["book_declaration"]
    lines.append(f"door: {book['door']['state']}")
    lines.append(f"layout: {book['layout']['state']}")
    lines.append(f"declared: {str(book['declared']).lower()}")
    for warning in body["warnings"]:
        lines.append(f"warning: {warning}")
    return "\n" + "\n".join(lines) + "\n"


def dump(body: dict) -> str:
    return json.dumps(body, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def require_dir(text: str, label: str) -> Path:
    if not isinstance(text, str) or not os.path.isabs(text):
        raise Refuse(f"{label} is not absolute")
    if any(part == ".." for part in Path(text).parts):
        raise Refuse(f"{label} escapes")
    if not os.path.lexists(text):
        raise Refuse(f"{label} is absent")
    if is_reparse(text):
        raise Refuse(f"{label} is linked")
    info = os.lstat(text)
    if not stat.S_ISDIR(info.st_mode):
        raise Refuse(f"{label} is not a directory")
    return Path(text)


def parse_args(argv: list[str]) -> tuple[str, str, bool]:
    code = None
    book = None
    text = False
    seen: set[str] = set()
    index = 0
    while index < len(argv):
        item = argv[index]
        if item == "--text":
            if "text" in seen:
                raise Refuse("repeated --text")
            seen.add("text")
            text = True
            index += 1
            continue
        if item in ("--code-root", "--book"):
            key = item[2:]
            if key in seen:
                raise Refuse(f"repeated {item}")
            if index + 1 >= len(argv):
                raise Refuse(f"missing value for {item}")
            seen.add(key)
            if item == "--code-root":
                code = argv[index + 1]
            else:
                book = argv[index + 1]
            index += 2
            continue
        raise Refuse("unknown argument")
    if code is None:
        raise Refuse("missing --code-root")
    if book is None:
        raise Refuse("missing --book")
    return code, book, text


def main(argv: list[str] | None = None) -> int:
    try:
        chosen = list(sys.argv[1:] if argv is None else argv)
        code_text, book_text, text = parse_args(chosen)
        code_root = require_dir(code_text, "code root")
        book = require_dir(book_text, "book")
        body = inspect(code_root, book, code_text=code_text, book_text=book_text)
        sys.stdout.buffer.write(dump(body).encode("utf-8"))
        if text:
            sys.stdout.buffer.write(project_text(body).encode("utf-8"))
        return 0
    except Refuse as exc:
        sys.stderr.buffer.write(f"refuse: {exc.message}\n".encode("utf-8"))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
