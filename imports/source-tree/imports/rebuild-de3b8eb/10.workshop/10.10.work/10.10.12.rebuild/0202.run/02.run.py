#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version: 001
# Authorization: draft — 2026-10-18
# who: grok-builder
# state: draft
# Face: 02
# PPPP: 0202
# desk: 10.workshop
# shelf: 10.10.work
# book: 10.10.12.rebuild
# keyword: run
# why: The loader. It finds a compute page by keyword, reads its card, and runs the named code face.
#
# cite: 3.1

"""The loader. Find a compute page, read its card, load, and run. Write nothing."""

from __future__ import annotations

import importlib.util
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

FACE_RE = re.compile(r"^02\.([A-Za-z_][A-Za-z0-9_]*)\.py$")
PAGE_RE = re.compile(r"^03(\d{2})\.(.+)$")
STAMP_KEYS = (
    "version",
    "Authorization",
    "who",
    "state",
    "Face",
    "PPPP",
    "desk",
    "shelf",
    "book",
    "keyword",
    "why",
    "cite",
)


def die(msg: str) -> None:
    print(f"stop: {msg}", file=sys.stderr)
    raise SystemExit(2)


def book_of(script: Path) -> Path:
    return script.resolve().parent.parent


def find_page(book: Path, keyword: str) -> Path:
    if not keyword or keyword in (".", "..") or "/" in keyword or "\\" in keyword:
        die(f"keyword is not a page title: {keyword}")
    if not book.is_dir():
        die(f"book is missing: {book}")
    hits = []
    for child in sorted(book.iterdir()):
        if not child.is_dir():
            continue
        hit = PAGE_RE.fullmatch(child.name)
        if hit and hit.group(2) == keyword:
            hits.append(child)
    if not hits:
        die(f"no compute page for {keyword}")
    if len(hits) > 1:
        die(f"more than one compute page for {keyword}")
    return hits[0]


def first_fence(text: str) -> str:
    lines = text.splitlines()
    start = None
    mark = ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if start is None:
            opened = re.match(r"^(```+|~~~+)(.*)$", stripped)
            if not opened:
                continue
            start = i + 1
            mark = opened.group(1)
            continue
        closed = re.match(r"^(```+|~~~+)\s*$", stripped)
        if closed and closed.group(1)[0] == mark[0] and len(closed.group(1)) >= len(mark):
            return "\n".join(lines[start:i])
    if start is None:
        die("card has no fence")
    die("card fence does not close")


def parse_uses(body: str) -> tuple[str, str]:
    parts = body.split()
    if len(parts) == 1:
        return parts[0], ""
    if len(parts) == 3 and parts[1] == "as":
        return parts[0], parts[2]
    die(f"uses line is not a face: {body}")


def parse_card(text: str) -> dict:
    fence = first_fence(text)
    runs = None
    uses = []
    args = None
    for raw in fence.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("runs:"):
            if runs is not None:
                die("card has two runs")
            runs = line.split(":", 1)[1].strip()
        elif line.startswith("uses:"):
            uses.append(parse_uses(line.split(":", 1)[1].strip()))
        elif line.startswith("args:"):
            if args is not None:
                die("card has two args")
            args = shlex.split(line.split(":", 1)[1].strip())
        else:
            die(f"card line is not runs, uses, or args: {line}")
    if not runs:
        die("card has no runs")
    return {"runs": runs, "uses": uses, "args": args or []}


def plain_name(filename: str, alias: str) -> str:
    if filename != Path(filename).name:
        die(f"module has no face address: {filename}")
    hit = FACE_RE.fullmatch(filename)
    if not hit:
        die(f"module has no face address: {filename}")
    stem = hit.group(1)
    if alias and alias != stem:
        die(f"uses name does not match the face: {filename}")
    return stem


def face_path(page: Path, filename: str) -> Path:
    plain_name(filename, "")
    path = page / filename
    if not path.is_file():
        die(f"face is missing: {filename}")
    return path


def stamp_text(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeError:
        die(f"code face is not utf-8: {path.name}")
    got = []
    for line in lines[2:]:
        if line.startswith("#"):
            got.append(line[1:].strip())
            continue
        if line.strip() == "":
            continue
        break
    return "\n".join(got)


def require_stamp(path: Path) -> None:
    text = stamp_text(path)
    for key in STAMP_KEYS:
        if not re.search(rf"(?m)^{re.escape(key)}:[ \t]*\S", text):
            die(f"code face has no stamp: {path.name}")


def load_face(path: Path, plain: str) -> None:
    require_stamp(path)
    spec = importlib.util.spec_from_file_location(plain, path)
    if spec is None or spec.loader is None:
        die(f"face did not load: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[plain] = module
    spec.loader.exec_module(module)


def run_main(path: Path, argv: list[str]) -> None:
    require_stamp(path)
    spec = importlib.util.spec_from_file_location("__main__", path)
    if spec is None or spec.loader is None:
        die(f"face did not load: {path.name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["__main__"] = module
    old = sys.argv
    sys.argv = argv
    try:
        spec.loader.exec_module(module)
    finally:
        sys.argv = old


def launch(book: Path, keyword: str, caller: list[str]) -> int:
    page = find_page(book, keyword)
    card_path = page / "02.md"
    if not card_path.is_file():
        die("card is missing: 02.md")
    try:
        card_text = card_path.read_text(encoding="utf-8")
    except UnicodeError:
        die("card is not utf-8: 02.md")
    card = parse_card(card_text)
    loaded = []
    for filename, alias in card["uses"]:
        loaded.append((face_path(page, filename), plain_name(filename, alias)))
    run_file = face_path(page, card["runs"])
    old_cwd = os.getcwd()
    code = 0
    try:
        os.chdir(page)
        for path, plain in loaded:
            load_face(path, plain)
        try:
            run_main(run_file, [str(run_file), *card["args"], *caller])
        except SystemExit as exc:
            if isinstance(exc.code, int):
                code = exc.code
            elif exc.code is None:
                code = 0
            else:
                print(exc.code, file=sys.stderr)
                code = 1
    finally:
        os.chdir(old_cwd)
    return code


def main(argv: list[str] | None = None) -> None:
    args = list(sys.argv[1:] if argv is None else argv)
    if args[:1] == ["test"]:
        cmd_test()
        return
    if not args:
        die("use a keyword")
    code = launch(book_of(Path(__file__)), args[0], args[1:])
    raise SystemExit(code)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\r\n", "\n").encode("utf-8"))


def stamped(pppp: str, keyword: str, why: str, body: str) -> str:
    head = (
        "#!/usr/bin/env python3\n"
        "# -*- coding: utf-8 -*-\n"
        "# version: 001\n"
        "# Authorization: draft \u2014 2026-10-18\n"
        "# who: grok-builder\n"
        "# state: draft\n"
        "# Face: 02\n"
        f"# PPPP: {pppp}\n"
        "# desk: 10.workshop\n"
        "# shelf: 10.10.work\n"
        "# book: 10.10.12.rebuild\n"
        f"# keyword: {keyword}\n"
        f"# why: {why}\n"
        "#\n"
        "# cite: 3.1\n"
    )
    return head + "\n" + body


def snap(root: Path) -> dict[str, bytes]:
    found = {}
    for path in root.rglob("*"):
        rel = path.relative_to(root).as_posix()
        if path.is_dir():
            if path.name == "__pycache__":
                found[rel + "/"] = b"pycache"
            continue
        found[rel] = path.read_bytes()
    return found


def run_loader(loader: Path, args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        return subprocess.run(
            [sys.executable, str(loader), *args],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=30,
        )
    except subprocess.TimeoutExpired:
        die("test failed: loader timed out")


def check(ok: bool, name: str, proc: subprocess.CompletedProcess[str] | None = None) -> None:
    if not ok:
        if proc is not None:
            print(proc.stdout, file=sys.stderr)
            print(proc.stderr, file=sys.stderr)
        die(f"test failed: {name}")
    print(f"pass: {name}")


def card(body: str) -> str:
    return "# 02\n\n```text\n" + body.strip() + "\n```\n"


def trap(folder: Path) -> None:
    write_text(folder / "02.md", card("runs: 02.trap.py"))


def cmd_test() -> None:
    source = Path(__file__).resolve()
    require_stamp(source)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        book = root / "10.workshop" / "10.10.work" / "10.10.12.rebuild"
        seat = book / "0202.run"
        seat.mkdir(parents=True)
        loader = seat / "02.run.py"
        loader.write_bytes(source.read_bytes())
        trap(seat)
        trap(book / "0402.run")
        trap(book / "0502.run")
        trap(book / "0102.run")

        page = book / "0302.run"
        write_text(page / "note.txt", "note-ok\n")
        write_text(
            page / "02.sentinel.py",
            stamped("0302", "run", "Test use.", 'MARK = "sentinel-ok"\n'),
        )
        write_text(
            page / "02.worker.py",
            stamped(
                "0302",
                "run",
                "Test run.",
                "import sentinel\n"
                "import pathlib\n"
                "import sys\n"
                "print(sentinel.__name__)\n"
                "print(sentinel.MARK)\n"
                "print(pathlib.Path('note.txt').read_text(encoding='utf-8').strip())\n"
                "print(' '.join(sys.argv[1:]))\n",
            ),
        )
        write_text(
            page / "02.md",
            card(
                "runs: 02.worker.py\n"
                "uses: 02.sentinel.py as sentinel\n"
                "args: --from card"
            ),
        )

        before = snap(root)
        proc = run_loader(loader, ["run", "extra"], root)
        check(proc.returncode == 0, "runs exit", proc)
        check(
            proc.stdout.splitlines() == ["sentinel", "sentinel-ok", "note-ok", "--from card extra"],
            "runs and uses",
            proc,
        )
        check(proc.stderr == "", "runs quiet", proc)
        check(snap(root) == before, "writes nothing")

        miss = book / "0311.miss"
        write_text(miss / "02.md", card("runs: 02.absent.py"))
        before = snap(root)
        proc = run_loader(loader, ["miss"], root)
        check(proc.returncode != 0, "missing face exit", proc)
        check("face is missing: 02.absent.py" in proc.stderr, "missing face", proc)
        check(snap(root) == before, "missing face writes nothing")

        before = snap(root)
        proc = run_loader(loader, ["gone"], root)
        check(proc.returncode != 0, "missing page exit", proc)
        check("no compute page for gone" in proc.stderr, "missing page", proc)
        check(snap(root) == before, "missing page writes nothing")

        bare = book / "0312.bare"
        write_text(bare / "name.py", "print('name-ran')\n")
        write_text(bare / "02.md", card("runs: name.py"))
        before = snap(root)
        proc = run_loader(loader, ["bare"], root)
        check(proc.returncode != 0, "name.py exit", proc)
        check("module has no face address: name.py" in proc.stderr, "name.py", proc)
        check("face is missing" not in proc.stderr, "name.py before missing", proc)
        check("name-ran" not in proc.stdout, "name.py did not run", proc)
        check(snap(root) == before, "name.py writes nothing")

        nostamp = book / "0313.nostamp"
        write_text(
            nostamp / "02.bare.py",
            "#!/usr/bin/env python3\n# -*- coding: utf-8 -*-\nprint('should-not-run')\n",
        )
        write_text(nostamp / "02.md", card("runs: 02.bare.py"))
        before = snap(root)
        proc = run_loader(loader, ["nostamp"], root)
        check(proc.returncode != 0, "no stamp exit", proc)
        check("code face has no stamp: 02.bare.py" in proc.stderr, "no stamp", proc)
        check("should-not-run" not in proc.stdout, "no stamp did not run", proc)
        check(snap(root) == before, "no stamp writes nothing")

        nocard = book / "0314.nocard"
        nocard.mkdir()
        before = snap(root)
        proc = run_loader(loader, ["nocard"], root)
        check(proc.returncode != 0, "missing card exit", proc)
        check("card is missing: 02.md" in proc.stderr, "missing card", proc)
        check(snap(root) == before, "missing card writes nothing")

        write_text(
            book / "0399.run" / "02.other.py",
            stamped("0399", "run", "Duplicate.", "print('duplicate-ran')\n"),
        )
        write_text(book / "0399.run" / "02.md", card("runs: 02.other.py"))
        before = snap(root)
        proc = run_loader(loader, ["run", "extra"], root)
        check(proc.returncode != 0, "two pages exit", proc)
        check("more than one compute page for run" in proc.stderr, "two pages", proc)
        check("duplicate-ran" not in proc.stdout, "two pages did not run", proc)
        check(snap(root) == before, "two pages writes nothing")

    print("pass: loader test")


if __name__ == "__main__":
    main()
