# CONTRACT — prime-boot-pass01 (0507.prime-support 05.07)

Author: claude-opus-5-5. Date: 2026-10-27.
This is a fixture-only prototype of the accepted design (boot-design05.06/BOOT.md), carrying PB-01 to PB-05. Every format here is provisional and local to the lab. Nothing grants authority.

## 1. Pinned tools (full SHA-256 constants in prime_boot.py)

| Tool | sha256 | Use |
|---|---|---|
| prime_support.py | 700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70 | `status --registry R --json` (subprocess) |
| clerk_adapter.py (sibling of prime_support.py) | 2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4 | checked only; imported by prime_support |
| check_book.py | fc16d2f68a3645050b6766ce18ce55f8169a0e2bad52d3392b4d059c629073a4 | `--root W --revision C --book B --json` |
| return_capture.py | 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac | `verify --book MB --member M` |

The request names each tool's absolute path; the hash is fixed in code.
- Each file must be a plain file with those bytes, checked before every launch. A mismatch fails the `tools` stage, and nothing is executed.
- The launch form is `[sys.executable, "-I", "-B", <path>, …]`, with no shell.
- `return_inspect.py` is not used.
- Git subcommands allowed: rev-parse, cat-file, show, status. They run with `GIT_OPTIONAL_LOCKS=0`. There are no writes and no network.

## 2. Request (`prime-boot-request/1`): strict JSON, exact keys

```json
{"schema": "prime-boot-request/1", "boot_id": "<label>", "attempt": 1, "previous_attempt": null,
 "workspace": "<abs>", "branch": "<name>", "commit": "<40 hex>", "role": "Prime", "model": "<label>",
 "book": "<rel>", "role_record": "<rel>", "assignment_record": "<rel>",
 "registry": {"path": "<abs>", "sha256": "<64 hex>"},
 "tools": {"prime_support": "<abs>", "check_book": "<abs>", "return_capture": "<abs>"},
 "members": [], "members_book": null,
 "packet": ["<rel>", "..."], "limits": {"max_refs": 12, "max_bytes": 131072}}
```

- Labels are plain ids.
- Paths are relative POSIX paths with no `..`, or absolute where shown.
- `limits`: 1 ≤ max_refs ≤ 12 and 1 ≤ max_bytes ≤ 131072.
- `previous_attempt` is null or the absolute path of an earlier attempt directory. `attempt` must then be greater than that attempt's number.
- `members` is non-empty only when `members_book` is absolute.

## 3. Attempt directory (PB-01)

**Root.** `prepare --records ROOT --attempt ID`. ROOT must be an absolute, existing, plain directory outside every Git working tree. Otherwise the call refuses with `refused: record store unusable: …; nothing was recorded`, exit 2.

**Order.**
1. `ROOT/ID` is created with an exclusive mkdir. An occupied ID refuses.
2. `00.request.raw` (the exact bytes) and `00.intent.json` are written before anything is parsed.
3. Each stage then writes `NN.<stage>.json`, every file exclusive-create, never edited:

| NN | stage | ok means |
|---|---|---|
| 01 | request | the schema is valid |
| 02 | links | the previous attempt exists, has an intent, and has a lower attempt number |
| 03 | tools | all four hashes match |
| 04 | git | the commit exists; HEAD and the branch ref are recorded; dirty paths under the book are recorded |
| 05 | book | `00.md` at the commit has one `contents in X.` pointer; check_book's JSON is recorded (exit 0 or 1 accepted, 2 fails) |
| 06 | records | the role and assignment records are read at the commit as text, and the assignment is parsed against the 0410 keys or recorded unparsed |
| 07 | status | the registry sha matches and the registry has no `clerk_jobs` (otherwise `unsupported`); prime_support status JSON is recorded |
| 08 | members | `verify` per member: exit code and stdout recorded; `structured: unavailable (return_inspect unaccepted)` |
| 09 | packet | refs within the caps, with absence and omission records |
| 10 | stability | HEAD, the branch, the registry and the tool hashes are re-read and compared |
| 19 | prepare-outcome | `prepared`, `partial` (unstable or omissions) or `failed` (with the failing stage) |

**Failure.** A failing stage writes its file with `"status": "failed"`, and 19 with `failed`. Later stages do not run.

**Interruption.** An uncaught exception leaves the files written so far and no 19. `show` reports `interrupted after <last stage>`.

## 4. Packet (PB-04, PB-05)

**Refs, in order:**
1. `<book>/00.md`;
2. the contents face;
3. role_record;
4. assignment_record;
5. then `packet[]`.

**Each ref records:**
- `id` (`R01`…);
- path and commit;
- `kind: commit-blob`;
- sha256 and bytes;
- `text` (UTF-8);
- `live`, which is `same`, `differs` with `live_sha256`, or `absent`. The live bytes are never included as text.

**Other records:**
- **Absence:** a path absent at the commit becomes `A01…` with `{path, commit, absent: true}`, and no text.
- **Omission:** a ref that would exceed max_refs, or cumulative raw bytes beyond max_bytes, or that is not UTF-8, is recorded in `omitted` with its reason and sha. No truncated text is ever stored as if complete.
- **Scope:** the packet paths plus every registered lane file in the status output. The attention list is recorded as advice.

## 5. Answers and checks (PB-02, PB-03)

`check --attempt DIR --answers FILE` requires 19 to be `prepared` or `partial`. It writes `20.answers.raw`, `21.answers.json` and `22.checks.json`, all exclusive.

**Answers** (`prime-boot-answers/1`): `{attempt_id, answers: {O1..O6}}`.
- **O1:** `{target, citations, conflicts_seen, text}`.
  - `target` must lie inside the scope, and a cited ref must have that path.
  - If the status output reported conflicts, `conflicts_seen` must list every conflict index.
  - Attention order is not used.
- **O2:** `{fields: {release, claim, execution, review: {value, citation}}, text}`. Each value must occur as a line, or as part of a line, of the cited ref's text.
- **O3, O4, O6:** `{citations, text}`. Each citation must be a packet R or A id.
- **O5:** `{none_found: true, text}` or `{citations, text}`.

Unknown keys, wrong types and duplicate keys fail the input.

**Retry.** An identical re-check reports `already-recorded`. A different one refuses with `conflict`.

## 6. Judgement and outcome

`judge --attempt DIR --judgement FILE` requires 22. It writes `30.judgement.raw`, `31.judgement.json` and `39.outcome.json`.

**Judgement** (`prime-boot-judgement/1`): `{attempt_id, reviewer, grades {O1..O6: pass|gap|wrong}, reasons {O1..O6: str}, remediation: [{kind: reference|question, detail}]}`. The reviewer is a label, not authentication.

**Outcome:**
- **oriented:** prepare `prepared`, all checks ok, all grades pass;
- **partial:** prepare `prepared` or `partial`, no failed check, no `wrong` grade;
- **not-oriented:** anything else.

**Always:** `authority: none; orientation grants no new work authority`.

## 7. Limits

This is a fixture lab. There is no live registry, no acknowledgement, no model call and no dispatch. Clerk-job boot and structured member fields are unsupported here. Grading free text is the judge's job; compute grades nothing.
