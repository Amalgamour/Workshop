#!/usr/bin/env python3
"""Build an unselected pass02 candidate into an explicit new root.

Refuses an existing output path. Copies the lab workbook and reporter
byte for byte. Writes doors whose pins are the executed files. The active
app/librarian.py is read and left in place. Canonical predecessors stay
at their live pins and are not copied.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

REPO = Path(r"D:\Git\lib-build")
LAB = REPO / "labs" / "review-loop-convergence-pass02"
ACTIVE = REPO / "app" / "librarian.py"
ACTIVE_SHA = "c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9"
ACTIVE_BYTES = 12204
PY = Path(sys.executable)
REL = "labs/review-loop-convergence-pass02"
WORKBOOK_REL = f"{REL}/workbook.py"
REPORT_REL = f"{REL}/report.py"
LOOP_REL = f"{REL}/review_loop_tools.py"
REPORT_DOOR_REL = f"{REL}/review_report_tools.py"
DECLARATION_REL = f"{REL}/review-loop.json"
ENTRY = "app/librarian.py"
CAPACITY_REL = "labs/review-source-capacity-pass03/prime_review.py"
CAPACITY_SHA = "c15cbd2460200583cab0518e2ac16f4a95356a779edb4b1978dfb4afc2a3e7ab"
CAPACITY_BYTES = 6136
HARNESS_CHECK = REPO / "labs" / "loop-convergence-harness-pass02" / "inputs_check.py"
PRIOR_INPUTS = REPO / "labs" / "review-loop-convergence-pass01" / "harness-inputs.json"

OLD_DOC = (
    "review-loop forwards workbook prepare, form, record, inspect, publish, read, and recover "
    "to the pinned v7 door. The v4 fixture commands stay on the pinned v4 door. "
    "reproduce is not an app command.\n"
)
NEW_DOC = (
    "review-loop and review-report forward to the unselected pass02 doors under this candidate root. "
    "The doors pin the workbook and reporter in this root. Fixture commands are refused. "
    "reproduce is not an app command. This candidate is not selected.\n"
)
OLD_NAME = '        "review-loop",\n'
NEW_NAME = '        "review-report",\n        "review-loop",\n'
OLD_BRANCH = (
    '    if command == "review-loop":\n'
    '        door = load_module(Path(__file__).resolve().parent / "review_loop_tools_v7.py", "librarian_review_loop_tools_v7")\n'
    "        try:\n"
    "            code = door.perform(args, code_root)\n"
    "        except door.Refuse as exc:\n"
    "            stop(str(exc))\n"
    "        if type(code) is not int:\n"
    '            stop("pinned review loop returned no exit code")\n'
    "        raise SystemExit(code)\n"
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def refuse(message: str) -> None:
    print(f"refused: {message}", file=sys.stderr)
    raise SystemExit(2)


def _lf(text: str) -> bytes:
    data = text.encode("utf-8")
    if b"\r" in data:
        refuse("generated text gained CR")
    return data


def render_librarian() -> bytes:
    data = ACTIVE.read_bytes()
    if len(data) != ACTIVE_BYTES or sha(data) != ACTIVE_SHA or b"\r" in data:
        refuse("active librarian pin mismatch")
    text = data.decode("utf-8")
    branch = (
        '    if command == "review-report":\n'
        "        root = Path(__file__).resolve().parent.parent\n"
        f'        door_path = root / "{REPORT_DOOR_REL}"\n'
        "        if not door_path.is_file():\n"
        '            stop("review-report door is missing")\n'
        "        door = load_module(door_path, \"librarian_review_loop_convergence_pass02_report\")\n"
        "        try:\n"
        "            code = door.perform(args, root)\n"
        "        except door.Refuse as exc:\n"
        "            stop(str(exc))\n"
        "        if type(code) is not int:\n"
        '            stop("pinned review report returned no exit code")\n'
        "        raise SystemExit(code)\n"
        '    if command == "review-loop":\n'
        "        root = Path(__file__).resolve().parent.parent\n"
        f'        door_path = root / "{LOOP_REL}"\n'
        "        if not door_path.is_file():\n"
        '            stop("review-loop door is missing")\n'
        "        door = load_module(door_path, \"librarian_review_loop_convergence_pass02\")\n"
        "        try:\n"
        "            code = door.perform(args, root)\n"
        "        except door.Refuse as exc:\n"
        "            stop(str(exc))\n"
        "        if type(code) is not int:\n"
        '            stop("pinned review loop returned no exit code")\n'
        "        raise SystemExit(code)\n"
    )
    for old, new in ((OLD_DOC, NEW_DOC), (OLD_NAME, NEW_NAME), (OLD_BRANCH, branch)):
        if text.count(old) != 1:
            refuse("candidate patch did not match the active dispatcher once")
        text = text.replace(old, new, 1)
    if "review_loop_tools_v7.py" in text or "review_loop_tools_v9.py" in text:
        refuse("candidate dispatcher still names a versioned review-loop door file")
    if "D:\\\\Git\\\\lib-build" in text and "review-loop-convergence-pass02" in text:
        refuse("candidate dispatcher points a pass02 door at the live repo")
    return _lf(text)


def render_declaration(workbook: bytes) -> bytes:
    document = {
        "schema": "review-loop-pins/10",
        "_note": (
            "Pass02 candidate declaration (0522/05.18). The executed workbook is "
            f"{WORKBOOK_REL}. Historical doors are not copied. This declaration is unselected."
        ),
        "limits": [
            "The door pins this declaration and the workbook under the candidate root.",
            "Fixture commands are refused. There is no live-root fallback.",
            "Canonical predecessors stay at their live pins and are loaded by the workbook.",
            "The N7-local prototype is not imported.",
        ],
        "tools": {
            "workbook": {"bytes": len(workbook), "path": WORKBOOK_REL, "sha256": sha(workbook)},
        },
    }
    return _lf(json.dumps(document, indent=2, sort_keys=True) + "\n")


def render_loop_door(workbook: bytes, declaration: bytes) -> bytes:
    text = f'''#!/usr/bin/env python3
"""Unselected review-loop door for the pass02 candidate (0522/05.18).

Resolves the workbook under the supplied candidate root. Does not require a
canonical path. Does not load a live-repo door when the candidate file is absent.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

SCHEMA = "review-loop-pins/10"
WORKBOOK_REL = "{WORKBOOK_REL}"
DECLARATION_REL = "{DECLARATION_REL}"
WORKBOOK_SHA = "{sha(workbook)}"
WORKBOOK_BYTES = {len(workbook)}
DECLARATION_SHA = "{sha(declaration)}"
DECLARATION_BYTES = {len(declaration)}
COMMANDS = {{"prepare", "form", "record", "inspect", "publish", "read", "recover"}}


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refuse(message)


def _pin(root: Path, rel: str, size: int, digest: str, label: str) -> Path:
    if rel.startswith(("/", "\\\\")) or ".." in rel.split("/"):
        refuse(f"{{label}} path escapes")
    path = root
    for part in rel.split("/"):
        path = path / part
        if path.is_symlink():
            refuse(f"{{label}} pin is linked")
    if not path.is_file():
        refuse(f"{{label}} pin is missing")
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if len(data) != size or got != digest:
        refuse(f"{{label}} pin mismatch got {{len(data)}} bytes sha256 {{got}} want {{size}} bytes sha256 {{digest}}")
    return path


def executed_workbook(document) -> str:
    tools = document.get("tools") if isinstance(document, dict) else None
    workbook = tools.get("workbook") if isinstance(tools, dict) else None
    path = workbook.get("path") if isinstance(workbook, dict) else None
    if path != WORKBOOK_REL:
        refuse("purported workbook is not the executed workbook")
    return path


def perform(args: list[str], code_root: Path) -> int:
    if not isinstance(args, list) or not args or type(args[0]) is not str:
        refuse("unknown review-loop command")
    command = args[0]
    if command not in COMMANDS:
        refuse("fixture and unknown review-loop commands are refused")
    root = Path(code_root)
    declaration = _pin(root, DECLARATION_REL, DECLARATION_BYTES, DECLARATION_SHA, "declaration")
    document = json.loads(declaration.read_bytes().decode("utf-8"))
    if document.get("schema") != SCHEMA:
        refuse("review loop declaration schema is not review-loop-pins/10")
    executed_workbook(document)
    script = _pin(root, WORKBOOK_REL, WORKBOOK_BYTES, WORKBOOK_SHA, "workbook")
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, "-B", os.fspath(script), *args],
        cwd=os.fspath(root),
        env=env,
        check=False,
        shell=False,
    )
    if type(proc.returncode) is not int:
        refuse("workbook returned no exit code")
    return proc.returncode


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args, Path(__file__).resolve().parents[2])
    except Refuse as exc:
        print(f"refused: {{exc.message}}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
'''
    text = text.replace("import subprocess\n", "import json\nimport subprocess\n", 1)
    return _lf(text)


def render_report_door(librarian: bytes, workbook: bytes, report: bytes) -> bytes:
    text = f'''#!/usr/bin/env python3
"""Unselected review-report door for the pass02 candidate (0522/05.18).

Pins the dispatcher, workbook, and reporter under the supplied candidate root.
A hash mismatch is a refusal, not a report. Exit 0 is an observation.
"""

from __future__ import annotations

import hashlib
import importlib.util
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

ENTRY = "{ENTRY}"
REPORT_REL = "{REPORT_REL}"
WORKBOOK_REL = "{WORKBOOK_REL}"
LIBRARIAN_SHA = "{sha(librarian)}"
LIBRARIAN_BYTES = {len(librarian)}
REPORT_SHA = "{sha(report)}"
REPORT_BYTES = {len(report)}
WORKBOOK_SHA = "{sha(workbook)}"
WORKBOOK_BYTES = {len(workbook)}
PASS = re.compile(r"^05\\.\\d\\d$")
FLAGS = ("--book", "--source", "--pass")


class Refuse(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def refuse(message: str) -> None:
    raise Refuse(message)


def _pin(root: Path, rel: str, size: int, digest: str, label: str) -> Path:
    if rel.startswith(("/", "\\\\")) or ".." in rel.split("/"):
        refuse(f"{{label}} path escapes")
    path = root
    for part in rel.split("/"):
        path = path / part
        if path.is_symlink():
            refuse(f"{{label}} pin is linked")
    if not path.is_file():
        refuse(f"{{label}} pin is missing")
    data = path.read_bytes()
    got = hashlib.sha256(data).hexdigest()
    if len(data) != size or got != digest:
        refuse(f"{{label}} pin mismatch got {{len(data)}} bytes sha256 {{got}} want {{size}} bytes sha256 {{digest}}")
    return path


def parse_call(args: list[str]) -> dict[str, str]:
    if not isinstance(args, list) or any(type(item) is not str for item in args):
        refuse("unsupported argument")
    values: dict[str, str] = {{}}
    index = 0
    while index < len(args):
        item = args[index]
        if not item.startswith("--"):
            refuse(f"unknown argument {{item}}")
        if "=" in item or item not in FLAGS:
            refuse(f"unknown flag {{item.split('=', 1)[0]}}")
        if item in values:
            refuse(f"repeated {{item}}")
        if index + 1 >= len(args) or args[index + 1].startswith("--") or args[index + 1] == "":
            refuse(f"missing value for {{item}}")
        values[item] = args[index + 1]
        index += 2
    for flag in FLAGS:
        if flag not in values:
            refuse(f"missing {{flag}}")
    if PASS.fullmatch(values["--pass"]) is None:
        refuse("pass is not 05.NN")
    source = values["--source"]
    if source.strip() == "" or source.startswith("-") or "/" in source or "\\\\" in source or "\\n" in source or "\\r" in source:
        refuse("source is a page id")
    book = values["--book"]
    if book.startswith("\\\\\\\\") or book.startswith("//"):
        refuse("book must be an absolute directory and was not followed when linked")
    path = Path(book)
    if not path.is_absolute() or ".." in path.parts:
        refuse("book must be an absolute directory and was not followed when linked")
    if path.is_symlink() or not path.is_dir():
        refuse("book must be an absolute directory and was not followed when linked")
    return {{"book": book, "pass": values["--pass"], "source": source}}


def perform(args: list[str], code_root: Path) -> int:
    call = parse_call(args)
    root = Path(code_root)
    _pin(root, ENTRY, LIBRARIAN_BYTES, LIBRARIAN_SHA, "dispatcher")
    _pin(root, WORKBOOK_REL, WORKBOOK_BYTES, WORKBOOK_SHA, "workbook")
    path = _pin(root, REPORT_REL, REPORT_BYTES, REPORT_SHA, "reporter")
    spec = importlib.util.spec_from_file_location("convergence_pass02_report_runtime", path)
    if spec is None or spec.loader is None:
        refuse("reporter did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    try:
        body = module.observe(call["book"], call["source"], call["pass"])
    except module.Refuse as exc:
        refuse(exc.message)
    module.emit(body)
    return 0


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    try:
        return perform(args, Path(__file__).resolve().parents[2])
    except Refuse as exc:
        print(f"refused: {{exc.message}}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
'''
    return _lf(text)


def _imports(workbook_path: Path) -> list[dict]:
    probe = Path(r"C:\Users\misg\AppData\Local\Temp") / "0518-trace-imports.py"
    probe.write_bytes(
        "import hashlib, importlib.util, json, sys, types\n"
        "from pathlib import Path\n"
        "repo = Path(r'D:\\Git\\lib-build').resolve()\n"
        "spec = importlib.util.spec_from_file_location('pass02_trace', sys.argv[1])\n"
        "mod = importlib.util.module_from_spec(spec)\n"
        "spec.loader.exec_module(mod)\n"
        "found = []\n"
        "seen = set()\n"
        "def add(path):\n"
        "    file = Path(path).resolve()\n"
        "    try:\n"
        "        rel = file.relative_to(repo).as_posix()\n"
        "    except ValueError:\n"
        "        return\n"
        "    if rel in seen or rel.startswith('labs/review-loop-convergence-pass02/'):\n"
        "        return\n"
        "    seen.add(rel)\n"
        "    data = file.read_bytes()\n"
        "    found.append({'bytes': len(data), 'path': rel, 'sha256': hashlib.sha256(data).hexdigest()})\n"
        "seen_ids = set()\n"
        "def walk(obj):\n"
        "    if not isinstance(obj, types.ModuleType) or id(obj) in seen_ids:\n"
        "        return\n"
        "    seen_ids.add(id(obj))\n"
        "    raw = getattr(obj, '__file__', None)\n"
        "    if isinstance(raw, str):\n"
        "        add(raw)\n"
        "    for value in vars(obj).values():\n"
        "        if isinstance(value, types.ModuleType):\n"
        "            walk(value)\n"
        "walk(mod)\n"
        "pins = {}\n"
        "for key in ('form', 'return_access', 'review_loop', 'construct', 'prime_cycle', 'prime_review'):\n"
        "    path = mod.base.wb.pin_file(key)\n"
        "    pins[key] = str(path)\n"
        "    add(path)\n"
        "print(json.dumps({'imports': found, 'pins': pins}, sort_keys=True))\n".encode("utf-8")
    )
    try:
        proc = subprocess.run(
            [str(PY), "-B", str(probe), str(workbook_path)],
            cwd=str(REPO),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            shell=False,
            check=False,
        )
    finally:
        probe.unlink(missing_ok=True)
    if proc.returncode != 0:
        refuse("import trace failed: " + proc.stderr.decode("utf-8", "replace")[-500:])
    payload = json.loads(proc.stdout.decode("utf-8"))
    rows = payload["imports"]
    prime = payload.get("pins", {}).get("prime_review", "").replace("\\", "/")
    if not prime.endswith(CAPACITY_REL):
        refuse(f"prime_review pin is not the capacity successor: {prime}")
    data = (REPO / CAPACITY_REL).read_bytes()
    if len(data) != CAPACITY_BYTES or sha(data) != CAPACITY_SHA:
        refuse("capacity prime_review pin mismatch")
    if any(row["path"] == "labs/n7-local-lifecycle-pass01/workbook.py" for row in rows):
        refuse("N7-local prototype was imported")
    unique = []
    seen = set()
    for row in rows:
        if row["path"] in seen:
            continue
        seen.add(row["path"])
        blob = (REPO / row["path"]).read_bytes()
        if len(blob) != row["bytes"] or sha(blob) != row["sha256"]:
            refuse(f"traced dependency drifted: {row['path']}")
        unique.append({"bytes": row["bytes"], "path": row["path"], "sha256": row["sha256"]})
    unique.sort(key=lambda item: item["path"])
    return unique


def _write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def _candidate_document(files: list[dict], dependencies: list[dict]) -> bytes:
    document = {
        "schema": "convergence-candidate/2",
        "kind": "combined",
        "selected": False,
        "entry": ENTRY,
        "workbook_entry": WORKBOOK_REL,
        "open_entry": WORKBOOK_REL,
        "files": files,
        "dependencies": dependencies,
        "adapter": {
            "schema": "convergence-adapter/1",
            "proposal": WORKBOOK_REL,
            "transformation": "byte copy of the lab proposal into the candidate root",
            "root_constraint": (
                "code root is the candidate root; canonical predecessors load by absolute pin "
                "from D:\\Git\\lib-build and are not copied"
            ),
            "differences": [
                "fence classifier accepts matching backtick and tilde fences and does not choose the last heading",
                "doors and the dispatcher resolve under the candidate root",
                "the frozen pass01 workbook still refuses a copied canonical path; this workbook does not",
            ],
        },
        "lab_differences": [
            "review-loop loads labs/review-loop-convergence-pass02/review_loop_tools.py under the candidate root",
            "review-report loads labs/review-loop-convergence-pass02/review_report_tools.py under the candidate root",
            "the executed workbook is labs/review-loop-convergence-pass02/workbook.py in that same root",
            "open is that workbook; it is a declared file",
            "canonical predecessors are dependency pins, not copied executed workbooks",
            "no review_loop_tools_vN.py name is used",
        ],
    }
    return _lf(json.dumps(document, indent=2, sort_keys=True) + "\n")


def _harness(candidate_json: bytes, files: list[dict], dependencies: list[dict], output: Path) -> None:
    prior = json.loads(PRIOR_INPUTS.read_bytes())
    kept = []
    for row in prior["dependencies"]:
        if row["status"] != "accepted":
            continue
        for pin in row["files"]:
            data = (REPO / pin["path"]).read_bytes()
            if len(data) != pin["bytes"] or sha(data) != pin["sha256"]:
                refuse(f"accepted dependency drifted: {pin['path']}")
        ref = row["review_ref"]
        data = (REPO / ref["path"]).read_bytes()
        if len(data) != ref["bytes"] or sha(data) != ref["sha256"]:
            refuse(f"accepted review_ref drifted: {ref['path']}")
        kept.append(row)
    pending = [
        {
            "files": "PENDING",
            "id": "R",
            "required": True,
            "review": "0522/05.18 built the reporter successor. Prime has not accepted it. An accepted row would declare interface.route review-report.",
            "role": "reporter observing the combined workbook chain via the dispatcher route review-report",
            "status": "pending",
        },
        {
            "files": "PENDING",
            "id": "W",
            "required": True,
            "review": "0522/05.18 built the external candidate. Prime has not accepted it.",
            "role": "combined workbook, doors, reporter, and dispatcher in one disposable root",
            "status": "pending",
        },
    ]
    by_id = {row["id"]: row for row in kept}
    dependencies_out = [by_id[key] for key in ("G", "L", "K", "I")] + pending
    proposal = {
        "bytes": (LAB / "workbook.py").stat().st_size,
        "path": WORKBOOK_REL,
        "sha256": sha((LAB / "workbook.py").read_bytes()),
    }
    document = {
        "schema": "harness-inputs/2",
        "made_for": "0522/05.18 proposed successor inputs. R and W are pending. This is not an accepted combined row and it is not full readiness.",
        "readiness": "blocked on pending R and pending W",
        "candidate": {
            "name": "review-loop-convergence-pass02",
            "kind": "combined",
            "candidate_json_sha256": sha(candidate_json),
            "files": files,
            "open_entry": WORKBOOK_REL,
            "workbook_entry": WORKBOOK_REL,
            "identity_schema": "convergence-candidate/2",
            "lab_differences": [
                "executed files live under the explicit output root",
                "open_entry is the declared workbook",
                "canonical predecessors are not candidate files",
            ],
        },
        "dependencies": dependencies_out,
        "fixture_source": prior["fixture_source"],
        "judgments": prior["judgments"],
        "proposed_identities": {
            "note": "Builder-measured hashes for the next Prime acceptance of R and W. These hashes are not a review_ref and they do not accept the rows.",
            "output_root": str(output),
            "candidate_json": {"bytes": len(candidate_json), "sha256": sha(candidate_json)},
            "proposal_workbook": proposal,
            "transitive_dependencies": dependencies,
        },
    }
    spec = importlib.util.spec_from_file_location("harness_inputs_check_pass02", HARNESS_CHECK)
    if spec is None or spec.loader is None:
        refuse("harness inputs check did not load")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    problems = module.shape_problems(document)
    if problems:
        refuse("harness inputs shape: " + "; ".join(problems[:8]))
    _write(LAB / "harness-inputs.json", _lf(json.dumps(document, indent=2, sort_keys=True) + "\n"))


def make_candidate(output: Path) -> dict:
    output = Path(output)
    if output.exists():
        refuse(f"output is occupied: {output}")
    try:
        output.resolve().relative_to(REPO.resolve())
    except ValueError:
        pass
    else:
        refuse("output root is inside the live repo")
    workbook = (LAB / "workbook.py").read_bytes()
    report = (LAB / "report.py").read_bytes()
    if b"\r" in workbook or b"\r" in report:
        refuse("proposal has CR")
    librarian = render_librarian()
    declaration = render_declaration(workbook)
    loop_door = render_loop_door(workbook, declaration)
    report_door = render_report_door(librarian, workbook, report)
    _write(LAB / "review-loop.json", declaration)
    _write(LAB / "review_loop_tools.py", loop_door)
    _write(LAB / "review_report_tools.py", report_door)
    mapping = {
        WORKBOOK_REL: workbook,
        REPORT_REL: report,
        LOOP_REL: loop_door,
        REPORT_DOOR_REL: report_door,
        DECLARATION_REL: declaration,
        ENTRY: librarian,
    }
    for rel, data in mapping.items():
        _write(output / rel, data)
    dependencies = _imports(output / WORKBOOK_REL)
    files = [{"bytes": len(data), "path": rel, "sha256": sha(data)} for rel, data in sorted(mapping.items())]
    document = _candidate_document(files, dependencies)
    _write(output / "CANDIDATE.json", document)
    _harness(document, files, dependencies, output)
    return {"candidate_json_sha256": sha(document), "files": len(files), "dependencies": len(dependencies)}


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] != ["--output"] or len(args) != 2 or args[1] == "":
        refuse("usage: make_candidate.py --output ABS")
    made = make_candidate(Path(args[1]))
    print(f"{made['candidate_json_sha256']} files {made['files']} dependencies {made['dependencies']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
