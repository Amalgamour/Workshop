"""One ordinary two-pass book. Attach calls the pinned v2 producer. Nothing here is stubbed.

The first package is a copy of the existing real-producer-v2-05.03 envelope.
The second package is prepared into a new directory from that request with the
pass set to 05.02. The live book and the source envelope are not written.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))
import colab_workflow as cw  # noqa: E402


ROOT = Path(r"D:\Git\lib-build")
ENVELOPE = ROOT / "00.kernel/00.00.10.work/0511.workflow-colab/evidence/real-producer-v2-05.03"
PRODUCER = ROOT / "labs/colab-support-pass02/colab_support.py"
PY = sys.executable
PAGE = "0701.colab-exchange-layout"


def invoke(argv):
    code, out, err = cw.execute(argv)
    body = json.loads(out.decode("utf-8")) if out else None
    return code, body, err


def tool(args: list[str]):
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run([PY, "-B", *args], capture_output=True, env=env, shell=False)
    return proc.returncode, proc.stdout, proc.stderr


def write_config(path: Path) -> None:
    cfg = {
        "assembler": str(ROOT / "labs/pack-assembly-pass01/pack_assembly.py"),
        "checker": str(ROOT / "labs/pack-custody-pass01/pack_check.py"),
        "helper": str(ROOT / "labs/return-capture-pass01/return_capture.py"),
        "inspector": str(ROOT / "labs/return-capture-pass01/return_inspect.py"),
        "producer_v1": str(ROOT / "labs/colab-support-pass01/colab_support.py"),
        "python": str(PY),
        "repositories": {"workshop": str(ROOT)},
        "schema": "colab-config/2",
    }
    path.write_bytes(cw.canonical(cfg))


def hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): cw.sha256(path.read_bytes())
        for path in root.rglob("*")
        if path.is_file()
    }


def request_bytes(binding: dict, title: str) -> bytes:
    body = {
        "book": binding["investigation"]["book"],
        "page": PAGE,
        "pass": binding["investigation"]["pass"],
        "schema": "colab-exchange-open/1",
        "targets": binding["targets"],
        "title": title,
    }
    return cw.canonical(body)


def review_body(route: str, next_pass) -> dict:
    return {
        "assessment": "Supplied fixture assessment. The tool does not judge it.",
        "by": "Codex Prime",
        "findings": [
            {
                "consequential": False,
                "director_reply": "Recorded for the disposable two-pass path.",
                "disposition": "answered",
                "id": "F01",
                "observation": "The return file is a projection of stored bytes.",
                "pending": False,
                "reason": "Prime supplied this disposition.",
                "source_binding": "T01",
            }
        ],
        "next_pass": next_pass,
        "on": "2026-11-01",
        "pending_questions": [],
        "route": route,
        "schema": "colab-exchange-review/1",
    }


def fail(step: str, body, err: bytes = b"") -> None:
    text = err.decode("utf-8", "replace")
    raise AssertionError(f"{step}\n{body}\n{text}")


def main() -> int:
    print("real-tool two-pass", flush=True)
    if cw.RUN_PROCESS is not None:
        raise AssertionError("producer stub is installed")
    before_envelope = hashes(ENVELOPE)
    binding = json.loads((ENVELOPE / "package/binding.json").read_text(encoding="utf-8"))
    title = json.loads((ENVELOPE / "package/colab-request.json").read_text(encoding="utf-8"))["title"]
    with tempfile.TemporaryDirectory(prefix="0511-0504-real-") as tmp:
        root = Path(tmp)
        config = root / "config.json"
        write_config(config)
        copied = root / "envelope-05.01"
        shutil.copytree(ENVELOPE, copied)
        book = root / "book"
        book.mkdir()
        opened = root / "open.json"
        opened.write_bytes(request_bytes(binding, title))
        code, body, err = invoke(
            ["open", "--book", str(book), "--request", str(opened), "--closure", str(copied)]
        )
        print("open", code, None if body is None else body.get("result"), flush=True)
        if code != 0:
            fail("open", body, err)
        digest = json.loads((copied / "verification.json").read_text(encoding="utf-8"))["digest"]
        code, body, err = invoke(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.01",
                "--output",
                str(copied),
                "--config",
                str(config),
                "--expect-digest",
                digest,
            ]
        )
        print("attach-05.01", code, None if body is None else body.get("result"), digest, flush=True)
        if code != 0 or body.get("digest") != digest:
            fail("attach-05.01", body, err)
        page = book / PAGE
        first = b"Ordinary local return.\nThe bytes stay as supplied.\n"
        first_path = root / "return-05.01.md"
        first_path.write_bytes(first)
        code, body, err = invoke(
            [
                "seal-return-local",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.01",
                "--return-file",
                str(first_path),
                "--declared-transport",
                "disposable desk copy",
            ]
        )
        print("seal-05.01", code, None if body is None else body.get("result"), flush=True)
        if code != 0 or (page / "05.01.return.md").read_bytes() != first:
            fail("seal-05.01", body, err)
        review = root / "review-05.01.json"
        review.write_bytes(cw.canonical(review_body("request-next", "05.02")))
        code, body, err = invoke(
            ["record-review", "--book", str(book), "--page", PAGE, "--pass", "05.01", "--review", str(review)]
        )
        print("review-05.01", code, None if body is None else body.get("route"), flush=True)
        if code != 0:
            fail("review-05.01", body, err)
        saved = {
            "05.01.pack.md": (page / "05.01.pack.md").read_bytes(),
            "05.01.return.md": (page / "05.01.return.md").read_bytes(),
            "06.01.review.md": (page / "06.01.review.md").read_bytes(),
            "06.01.notes.md": (page / "06.01.notes.md").read_bytes(),
            "snapshot": (page / "artifacts/05.01/package/06.01.notes.md").read_bytes(),
        }
        code, body, err = invoke(["open-pass", "--book", str(book), "--page", PAGE, "--pass", "05.02"])
        print("open-pass", code, None if body is None else body.get("result"), flush=True)
        if code != 0:
            fail("open-pass", body, err)
        source = json.loads((ENVELOPE / "package/colab-request.json").read_text(encoding="utf-8"))
        source["binding"]["investigation"]["pass"] = "05.02"
        request_path = root / "request-05.02.json"
        request_path.write_bytes((json.dumps(source, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
        code, out, err = tool(
            [str(PRODUCER), "preview", "--request", str(request_path), "--config", str(config), "--json"]
        )
        print("preview-05.02", code, flush=True)
        if code != 0:
            fail("preview-05.02", out.decode("utf-8", "replace"), err)
        preview = json.loads(out.decode("utf-8"))
        second_digest = preview.get("digest")
        if not isinstance(second_digest, str) or preview.get("investigation", {}).get("pass") != "05.02":
            fail("preview-05.02", preview)
        prepared = root / "prepared-05.02"
        prepared.mkdir()
        code, out, err = tool(
            [
                str(PRODUCER),
                "prepare",
                "--request",
                str(request_path),
                "--config",
                str(config),
                "--output",
                str(prepared),
                "--digest",
                second_digest,
                "--json",
            ]
        )
        print("prepare-05.02", code, second_digest, flush=True)
        if code != 0:
            fail("prepare-05.02", out.decode("utf-8", "replace"), err)
        code, body, err = invoke(
            [
                "attach",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.02",
                "--output",
                str(prepared),
                "--config",
                str(config),
                "--expect-digest",
                second_digest,
            ]
        )
        print("attach-05.02", code, None if body is None else body.get("result"), flush=True)
        if code != 0 or body.get("digest") != second_digest:
            fail("attach-05.02", body, err)
        second = b"Second pass return.\r\nCRLF stays in the file.\r\n"
        second_path = root / "return-05.02.md"
        second_path.write_bytes(second)
        code, body, err = invoke(
            [
                "seal-return-local",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.02",
                "--return-file",
                str(second_path),
                "--declared-transport",
                "disposable desk copy",
            ]
        )
        print("seal-05.02", code, None if body is None else body.get("result"), flush=True)
        if code != 0 or (page / "05.02.return.md").read_bytes() != second:
            fail("seal-05.02", body, err)
        if b"\r\n" not in (page / "artifacts/05.02/return.md").read_bytes():
            raise AssertionError("crlf was normalized")
        later = root / "review-05.02.json"
        later.write_bytes(cw.canonical(review_body("finish", None)))
        code, body, err = invoke(
            ["record-review", "--book", str(book), "--page", PAGE, "--pass", "05.02", "--review", str(later)]
        )
        print("review-05.02", code, None if body is None else body.get("route"), flush=True)
        if code != 0:
            fail("review-05.02", body, err)
        for name, data in saved.items():
            path = page / "artifacts/05.01/package/06.01.notes.md" if name == "snapshot" else page / name
            if path.read_bytes() != data:
                raise AssertionError("earlier pass changed " + name)
        count = len(json.loads((page / "investigation.json").read_text(encoding="utf-8"))["transitions"])
        code, body, err = invoke(["open-pass", "--book", str(book), "--page", PAGE, "--pass", "05.02"])
        if body.get("result") != "repeat" or body.get("wrote") is not False:
            fail("open-pass-replay", body, err)
        code, body, err = invoke(
            [
                "seal-return-local",
                "--book",
                str(book),
                "--page",
                PAGE,
                "--pass",
                "05.02",
                "--return-file",
                str(second_path),
                "--declared-transport",
                "disposable desk copy",
            ]
        )
        if body.get("result") != "repeat" or body.get("wrote") is not False:
            fail("seal-replay", body, err)
        record = json.loads((page / "investigation.json").read_text(encoding="utf-8"))
        if len(record["transitions"]) != count:
            raise AssertionError("replay appended a transition")
        actions = [item["action"] for item in record["transitions"]]
        if actions != ["open", "attach", "seal-return", "review", "open-pass", "attach", "seal-return", "review"]:
            raise AssertionError(actions)
        if record["schema"] != "colab-exchange-investigation/2":
            raise AssertionError(record["schema"])
        if record["passes"]["05.01"]["return"]["kind"] != "page-local":
            raise AssertionError("n1 return was used")
        if "member" in record["passes"]["05.01"]["return"] or "member" in record["passes"]["05.02"]["return"]:
            raise AssertionError("member field on a page-local return")
        children = sorted(item.name for item in book.iterdir())
        if children != [PAGE]:
            raise AssertionError(children)
        tails = [
            "05.01.pack.md",
            "05.01.return.md",
            "06.01.review.md",
            "05.02.pack.md",
            "05.02.return.md",
            "06.02.review.md",
        ]
        for name in tails:
            if not (page / name).is_file():
                raise AssertionError(name)
        code, shown, err = invoke(["show", "--book", str(book)])
        if code != 0 or shown["wrote"] is not False:
            fail("show", shown, err)
        flags = {item["pass"]: item for item in shown["pages"][0]["passes"]}
        if flags["05.02"]["explicit_finish"] is not True or flags["05.02"]["review_pending"] is not False:
            raise AssertionError(flags["05.02"])
        if flags["05.02"]["return_kind"] != "page-local":
            raise AssertionError(flags["05.02"])
        print("real-tool actions", " ".join(actions), flush=True)
        print("real-tool ok", flush=True)
    if hashes(ENVELOPE) != before_envelope:
        raise AssertionError("source envelope changed")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001 - preserve the partial step log already printed
        print(f"FAIL real-two-pass: {exc}", flush=True)
        sys.exit(1)
