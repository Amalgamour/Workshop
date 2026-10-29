# CONTRACT — colab-support-pass01 (0510.colab-tools/05.02)
State: written after notes 06.02 and before code. This is a lab contract, not law or runtime. It implements the shared interface `0411.colab/evidence/n7nn-interface-v1/CONTRACT.md` without changing it.

## Commands
```text
python -B colab_support.py preview --request ABS --config ABS --json
python -B colab_support.py prepare --request ABS --config ABS --output ABS --digest HEX --json
python -B colab_support.py verify  --output ABS --config ABS --json
python -B colab_support.py intake  --output ABS --config ABS --book ABS --member 01NN.slug
       --return-file ABS --source-root ABS --artifact REL|LOGICAL [--artifact ...] --json
```
All paths are absolute. Exits: 0 is a completed preview, prepare, `already-prepared`, intact verify or completed intake (including the helper's `already-captured`). 1 is a recorded negative: a partial or mismatched package, or intake attention. 2 is a refusal: invalid input, a digest mismatch, a collision, a wrong origin, a bad pin or a tool failure. Expected failures print no traceback.

## Config `colab-config/1` (local, never packaged)
`{"schema","repositories":{LABEL:ABS},"python":ABS,"assembler":ABS,"checker":ABS,"helper":ABS,"inspector":ABS}`. Each tool is hash-pinned in code: assembler 75d49679…, checker 9bbd9d57…, helper 8f3da5c6…, inspector 947915fe…. A mismatch refuses before any launch. `python` names the interpreter that runs pinned tools, called with `-B` and an argument array, never a shell.

## Request `colab-request/1`
Strict UTF-8 JSON. A BOM, duplicate keys, trailing data, NaN or Infinity, unknown or missing keys, or a wrong type refuses. Strings are single-line where noted. The request is at most 262144 bytes.

| key | type and rule |
|---|---|
| schema | `colab-request/1` |
| binding | exact `colab-binding/1` object (below) |
| title, author, recipient, reviewer | single line |
| date | `YYYY-MM-DD`, a real day |
| mode | `open-design`, `hostile-read`, `diagnostic` or `controlled-experiment` |
| scoring | `{"state":"unscored"}`; or open `{"state":"scored","blind":false,"rubric":text,"meaning":text}`; or blind `{"state":"scored","blind":true,"evaluator_sources":[path, 1–64]}`. A blind rubric lives only in committed evaluator sources, because the request itself travels in the package. (Changed during the build, before any return: the first draft allowed rubric text in a blind request, and that text would have reached the candidate inside colab-request.json. Test `test_blind_rubric_text_not_allowed_in_request` now holds the rule.) |
| context, question, why, built_state, method | text |
| known_gaps | list of text, 0–64 items |
| cases | list of `{"id":"C01".., "text"}` in order, 1–64 items |
| environment | `{"kind":"zip-only" or "local-tools","read","write","execute","network"}` |
| permissions, stop | list of single lines, 1–64 items each |
| prior_involvement | text |
| required_sources | list of `{"path","role"}`, 0–64 items; read at the binding's single commit |
| withheld | list of `{"item","reason"}`: deliberate withholds |
| unavailable | list of `{"item","reason","kind":"required-omission" or "tool-limitation"}` |
| director_replies | list of `{"id":"D01"..,"date","source","reply","status":"actual" or "hypothetical-fixture"}`; reply text is copied verbatim |
| return_route | `{"destination","submission_hint"}`, single lines |

Text is at most 16384 characters, has no NUL or other control characters except LF and TAB, and holds no structural heading outside a fence. For a `zip-only` environment, recipient-facing text may not name an absolute local path (a drive letter, UNC or leading `/`).

## Binding `colab-binding/1` (shared interface, unchanged)
- `investigation.page` must be N7NN, 0701–0799. 0700 (the door) and any other band refuse. `pass` is `05.NN`.
- Target ids match `^T[0-9]{2}$` exactly as the shared schema says, and are unique. There are 1–32 targets. Two targets that differ only by id refuse.
- `source.path` is a canonical relative path (the checker's `declared_path`). Its last segments equal `book`, `page`, then `file` split on `/`.
- A target whose book and page equal the investigation's refuses.
- Every target and required source shares one repository label and one commit. This is a limit of the pinned assembler's single `revision`, and it refuses rather than retargeting.
- `source.sha256` must equal the blob at that commit; a mismatch is stale and refuses. HEAD and the worktree are never read for a target.
- `section: null` binds the whole named file. A heading section is the exact line text without its line ending, matched outside fenced blocks. With `occurrence: null` exactly one match is required; with `n` there must be at least `n` matches. Zero matches, or duplicates without an explicit occurrence, refuse. The extent runs to the next heading of the same or higher level, outside fences, or to the end of the file.
- `kind: id` refuses as `unsupported-section-id`, because v1 declares no id syntax.

## Package
```text
OUT/
  package/
    05.NN.md                 assembler draft (Release/Claim/Return/Review PENDING)
    request.snapshot         assembler request bytes (adapter output)
    source-manifest.json     prime-pack-sources/1 (assembler)
    snapshots/NNNN.blob      targets first (unique paths, request order), then required sources
    completion-receipt.json  assembler receipt
    binding.json             canonical binding bytes
    colab-request.json       exact supplied request bytes
    ENTRY.md                 self-contained recipient entry
    06.NN.md                 supplied purpose/reason/context/replies only
    RETURN-TEMPLATE.md       return shape
  prepared-colab.zip         deterministic ZIP of package/ (fixed time 1980-01-01, stored, sorted)
  evaluator/                 only for scored+blind: source-manifest.json and snapshots/; never in the ZIP
  assembler-request.json     the adapter's request file passed to the assembler CLI (same bytes as package/request.snapshot)
  assembler-run.json         raw assembler stdout/stderr/exit, as JSON strings
  verification.json          written last: colab-package-verification/1
```
Canonical JSON here means sorted keys, `indent=2`, `ensure_ascii=False` and one trailing LF.

## Digest `colab-package-digest/1`
SHA-256 over parts. Each part is an 8-byte big-endian length followed by the bytes:
1. `colab-package-digest/1`
2. the colab request bytes
3. the canonical binding bytes
4. the assembler digest
5. for each colab-planned file in fixed order (binding.json, colab-request.json, ENTRY.md, 06.NN.md, RETURN-TEMPLATE.md, then evaluator files), its path, sha256 and decimal length
6. the planned ZIP's sha256 and decimal length

The ZIP is planned from the assembler's planned bytes plus the colab files, so preview knows it before anything is written. The receipt-free assembler outputs are part of its digest. `completion-receipt.json` is generated after its checker runs, so its bytes are planned by calling the assembler's own `receipt_bytes` with the expected checker result (`pass`, exit 0, rows equal to the number of sources). Prepare then confirms that the written receipt equals the plan; if it differs, the package is partial.

## Prepare sequence
1. Validate the request and config, load the pins, read Git through the pinned assembler module, resolve sections, plan everything and compare the digest. Any failure writes nothing.
2. Check the output: it must be absent or empty, its parent a real directory, and it must lie outside every configured repository and outside any directory that contains `00.kernel`. If it holds an intact package at the same digest, the result is `already-prepared` (exit 0, nothing written). Anything else refuses with the retained paths.
3. Create OUT. Run the assembler CLI `assemble` into OUT/package with the planned digest. Write assembler-run.json.
4. Write the colab files exclusively (O_EXCL), then the evaluator files, then the ZIP, then verification.json.
5. Any failure stops, leaves files in place and reports which were written. Private hooks: `before-assembler`, `after-assembler`, `before-zip` and `before-verification`.

## Verify
`verification.json` must exist (otherwise partial, exit 1). Its key set is exact. It checks the package file set and every hash, the recomputed digest, the assembler `verify` on a temp projection (raw stdout and exit kept), binding validation, and section re-resolution against the packaged snapshots. It checks that the ZIP's member set and bytes equal package/, and that its sha256 is as recorded. It checks that evaluator paths are disjoint from candidate snapshots, and that every source line ENTRY names is in the manifest. Findings carry a `kind` of `pack-defect`, `input-defect` or `tool-limitation`. `not_checked` names meaning, adequacy, authenticity, permission and design findings.

## Intake `colab-intake-provenance/1`
1. Verify the package; it must be intact.
2. Run the inspector on the member. `reserved` or `complete` is required, and the reservation origin must equal the binding's investigation `{book,page,batch=pass}`. Otherwise the result is `wrong-origin`, exit 2, before capture. Origin pages outside N7NN refuse.
3. Run the helper: `capture` with the reservation's submission id, then `verify`, then the inspector again.
4. Print the provenance: package digest and binding sha256, investigation, targets (id, path, commit), member, submission, receipt, manifest and return sha256, and each tool's argv, exit, stdout and stderr. It also records which of the headings `Hostile`, `Factfind`, `Overflow`, `Unprompted` and `Director replies` appear in the return file. That is a presence fact, not a grade. Statements: not approved, not accepted, not released, not published; labels do not authenticate.
5. An identical replay is the helper's `already-captured` (exit 0). A helper conflict, partial or failed verify gives `attention` (exit 1) or a refusal (exit 2), with raw output kept. Nothing is deleted, overwritten or retried.

## Not
No scheduler, dispatch, model call, semantic grading, review or acceptance, live page edit, Git write, change to 0411 or band 0700, or reading of Grok outputs.
