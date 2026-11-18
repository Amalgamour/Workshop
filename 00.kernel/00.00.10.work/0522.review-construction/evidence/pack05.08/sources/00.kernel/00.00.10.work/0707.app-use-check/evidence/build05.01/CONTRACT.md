# CONTRACT — 0707 pass01 operator-path lab
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · written before the harness

## What runs
- **The app:** only `python -B app/librarian.py review-loop <cmd> …`, cwd `D:\Git\lib-build`, as one subprocess per command. This is the written operator path, in place, because the core executes tools from a hard-coded `ROOT` (notes O7).
- **The byte guard:** before and after every call, `app/librarian.py`, `app/review_loop_tools_v2.py`, `app/review-loop-v2.json` and the 8 tools pinned in that declaration must equal the pack05.01 pins.
  - On a mismatch the harness stops and records that.
  - pack05.01 snapshots all 11 of these files. The live bytes must equal those snapshot pins, which also equal the declaration's own hashes.
- **Not executed:** no `pilot.py`, no test `__main__`, no `reproduce`, no `run`, no other app namespace.

## Where it writes
- **Disposable books:** under `C:\Users\misg\AppData\Local\Temp\claude\D--Git-Librarian\313e7ce7-27d2-405b-881d-6a16a47199dc\scratchpad\0707-books\<run>\<case>`, outside the checkout. They are deleted only after evidence is copied out.
- **Lab code:** `colab/labs/0707.app-use-check/pass01/`.
- **Evidence:** `00.kernel/00.00.10.work/0707.app-use-check/evidence/build05.01/`, holding raw stdout, stderr, exit and argv per call; the book file trees after each case; fingerprints; and the git-status diff.

## Material
- **Member:** `0182.desk-app-integration-design-0501`, copied from pack05.01 snapshot bytes. The copy must equal the 10 pins.
- **Synthetic target:** a SYNTHETIC PENDING page at the derived `0519.desk-app/05.01.md`.
- **Conflict target:** the pack snapshot of the live 0519/05.01 page (b72c8aa0…).
- **Registration and request:** `example-registration.json` and `example-request.json` (pack snapshots), unchanged.
- **`assignment.txt` and `note.md`:** my own labelled synthetic text.
- **`descriptor.json`:** the describe-legacy `descriptor` object, written exactly as `pilot.py` does (sorted, indented 2, trailing newline). That serialization is a disclosed reconstruction; no document states it.

## Supplied judgment
`supplied-judgment.json` in pass01, filled by "Claude (SUPPLIED sample, 0707 lab)". Not Codex Prime's judgment, not Director approval, and not an assessment of the 0519 design. The material is my own return (a self-review conflict, disclosed). `decision-build.json` records, per field, whether its shape came from the template, the documents or `pilot.py`.

## Comparison (new-process recovery)
A field-by-field and byte (sha256 of canonical JSON) comparison between:
- the supplied judgment and record I wrote;
- the decision file recorded;
- the new-process `read` output (`view.latest_review` and its record files under the cycle directory, if exposed);
- the rendered page section.

Source identity compared: return sha, receipt sha, descriptor sha, member and derived member, origin, submission id. Task association and capture integrity are reported separately.

## Cases
A success, B interrupted render → recover, C idempotence, D stale target, E substantive-page conflict, F wrapper refusal. The criteria are in `06.01.notes.md` §Method. First failures are kept. A rerun needs a written changed condition.

## Verification outputs
- `verification.json`: per-case criteria and results, guard results, unexpected writes.
- `artifact-manifest.json`: sha256 and bytes of the return and every artifact, excluding itself.
