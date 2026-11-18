"""Compose every task prompt from its header and fixture, then write MANIFEST.json with sha256 of each.

Run: python -I -B tools/build.py
A changed prompt is a new version: bump its version in TASKS, never edit a run's recorded prompt.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T = ROOT / "tasks"
PROTOCOL = "baseline-01"
sha = lambda b: hashlib.sha256(b).hexdigest()

# T1 source: built from escapes so tabs, trailing spaces and the non-breaking space are exact. No final newline.
T1_LINES = [
    "# Release line \u2014 0518.colab-review 05.01",
    "Director: \u201cBuild and test the new Colab review adapter; do not launch reviewers.\u201d",
    "Scope:\tlabs/colab-review-pass01 only",
    "Pin: " + sha(b"baseline-01 T1 pin"),
    "Path: D:\\Git\\lib-build\\00.kernel\\0411.colab",
    "Trailing two spaces here.  ",
    "Non-breaking space between these:\u00a0words.",
    "R\u00e9sum\u00e9 \u2265 draft; na\u00efve caf\u00e9 \u2014 keep the accents.",
    "  Indented two spaces, then `code` and *stars*.",
    "Numbers: 0.10, 1,234.50, 007, -3.",
    "",
    "Last line has no full stop",
]
T5A = {
    "words": [350, 450],
    "required": ["the night ferry", "a brass key", "a letter never sent"],
    "forbidden": ["suddenly", "tapestry", "delve", "testament", "whisper", "whispered"],
}

HEADERS = {
    "T1": ("Copy the text between the line <<<COPY and the line COPY>>> exactly, character for character, "
           "including spaces, tabs, punctuation and line breaks. Reply with the line <<<COPY, then the copied text, "
           "then the line COPY>>>, and nothing else. Do not use a code block.\n\n"),
    "T2": ("Convert the status note below into a JSON array of objects with exactly the keys id, title, owner, due "
           "and state. due is a date as YYYY-MM-DD, or null if none is given. state is one of open, in-progress, "
           "blocked or done. Follow the note's instructions about what to include. Order the objects by id. "
           "Output only the JSON.\n\nStatus note:\n"),
    "T3": ("Here is ledger.py. Change parse_amount so that:\n"
           "1. it accepts thousands separators, for example '1,234.50' gives 123450;\n"
           "2. it raises ValueError for more than two decimal places, for example '3.505', and for malformed "
           "separators, for example '1,23.40' or '12,3456'.\n"
           "Keep its behaviour otherwise. Do not change any other function, and do not add imports. "
           "Reply with the complete new ledger.py in a single ```python code block, and nothing else.\n\n"),
    "T4": ("Revise this specification for clarity and plain English. Preserve every requirement exactly: do not add, "
           "drop, weaken or strengthen any. Keep each rule's id (R01 to R11) at the start of its line, in the same "
           "order, one rule per line. Keep all text in backticks verbatim. Keep MUST, MUST NOT and MAY in capitals. "
           "Output only the revised specification.\n\n"),
    "T5a": (f"Write an original short scene of {T5A['words'][0]} to {T5A['words'][1]} words, in the first person and "
            f"the past tense. It must include {', '.join(T5A['required'][:-1])} and {T5A['required'][-1]}. Do not use "
            f"these words: {', '.join(T5A['forbidden'])}. Give it no title. Output only the scene."),
    "T5b": ("Here is a passage by the author. Continue it for 300 to 400 words in the same voice. Do not repeat the "
            "passage, and do not explain or comment. Output only the continuation.\n\nPassage:\n"),
}
TASKS = {"T1": ("T1-copy", "v1"), "T2": ("T2-struct", "v1"), "T3": ("T3-code", "v1"), "T4": ("T4-spec", "v1"),
         "T5a": ("T5a-prose", "v1"), "T5b": ("T5b-voice", "v1")}


def compose(task):
    folder = T / TASKS[task][0]
    head = HEADERS[task].encode("utf-8")
    if task == "T1":
        src = "\n".join(T1_LINES).encode("utf-8")
        (folder / "source.txt").write_bytes(src)
        return head + b"<<<COPY\n" + src + b"\nCOPY>>>\n", [folder / "source.txt"]
    if task == "T2":
        return head + (folder / "source.txt").read_bytes(), [folder / "source.txt", folder / "expected.json"]
    if task == "T3":
        return head + b"```python\n" + (folder / "ledger.py").read_bytes() + b"```\n", [folder / "ledger.py", folder / "tests_heldout.py"]
    if task == "T4":
        return head + (folder / "spec.md").read_bytes(), [folder / "spec.md"]
    if task == "T5a":
        (folder / "constraints.json").write_text(json.dumps(T5A, indent=1) + "\n", encoding="utf-8", newline="\n")
        return head + b"\n", [folder / "constraints.json"]
    sample = folder / "VOICE-SAMPLE.txt"
    if not sample.exists():
        return None, []
    return head + sample.read_bytes(), [sample]


def main():
    entries = {}
    for task, (name, version) in TASKS.items():
        folder = T / name
        folder.mkdir(parents=True, exist_ok=True)
        prompt, fixtures = compose(task)
        rel = lambda p: p.relative_to(ROOT).as_posix()
        if prompt is None:
            entries[task] = {"version": f"{task}.{version}", "state": "withheld",
                             "reason": f"{rel(folder / 'VOICE-SAMPLE.txt')} not supplied: a passage of the Director's own writing"}
            continue
        (folder / "prompt.txt").write_bytes(prompt)
        entries[task] = {"version": f"{task}.{version}", "state": "ready", "prompt": rel(folder / "prompt.txt"),
                         "prompt_sha256": sha(prompt), "prompt_bytes": len(prompt),
                         "fixtures": {rel(p): sha(p.read_bytes()) for p in fixtures}}
    tools = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes()) for p in sorted((ROOT / "tools").glob("*.py"))}
    manifest = {"schema": "baseline-manifest/1", "protocol": PROTOCOL, "tasks": entries, "tools": tools}
    (ROOT / "MANIFEST.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({k: (v["state"], v.get("prompt_sha256", "")[:12]) for k, v in entries.items()}))


if __name__ == "__main__":
    main()
