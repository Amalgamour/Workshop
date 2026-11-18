# Source, dependency and fixture index (0707/05.18)
**Freeze:** pack05.18 has 131/131 live files and 131/131 snapshots equal, at the start and again at the end (`verification.json`).

## Code needed to execute (candidate root)
| Path | sha256 (prefix) | bytes | Source |
|---|---|---|---|
| app/librarian.py | 5bc43806… | 12204 | candidate (proposal) |
| app/review_loop_tools_v8.py | 0335da32… | 11054 | candidate (proposal) |
| app/review-loop-v8.json | 92a718d3… (prod) / 1873f824… (lab) | 4100 / 4064 | candidate / LAB ADAPTER |
| labs/workbook-review-pass04/workbook.py | b7b8776c… (prod) / c6be0b97… (lab) | 6508 / 6584 | candidate / LAB ADAPTER |
| app/review_loop_tools_v4…v7.py, review-loop-v4…v7.json | v7 93a89939…, v7 json bf12aa7c… | — | live, pinned |
| labs/workbook-review-pass03/workbook.py + forms | 9e66d7e4… / form 4b8cf0e8… | 19533 / 4532 | live, pinned |
| labs/workbook-review-pass02, pass01 (+ forms) | 6ce4a5ff…, 60e040fa… | 52574, 79131 | live, pinned; **imported from the live root by pass03 and pass02 constants** |
| labs/return-access-pass01, review-loop-pass03, review-construction-pass04, prime-cycle-pass03, prime-review-pass02 | per the v8 pins | — | live, pinned (each has `ROOT = D:\Git\lib-build`) |
| other app/*.py and *.json | hash recorded in each ROOT-INDEX.json | — | live, copied unchanged (dispatch checks) |

**Full per-file list:** `labs/review-entry-integration-pass01/bundle/INDEX.json` (293 files with sha256, bytes and source).

## Source data needed to reproduce a claim
| Fixture | Pointer page (pack05.18 snapshot) | Declared submission / manifest | Manifest rows |
|---|---|---|---|
| N5 0522.review-construction 05.13 | 05.13.md | evidence/build05.13/submission.md, artifact-manifest.json (e806c09a…) | 29, including 9 code-root rows (app/librarian.py, app/README.md, v7 door and JSON, pass03 files) |
| N5 0512.prime-review 05.06 | 05.06.md (already carries v7 review wbf38837…) | evidence/build05.06/… (983efc6a…) | 14, including 4 code-root rows (labs/review-report-pass03) |
| N7 0707.app-use-check 05.15 | 05.15.pack.md | 05.15.return.md, evidence/design05.15/artifact-manifest.json (f7a50801…) | 26 |
| N7 0707.app-use-check 05.17 | 05.17.pack.md | 05.17.return.md, evidence/design05.17/artifact-manifest.json (49e77dc0…) | 33 |

- **Other top-level page .md files:** copied from live, with the hash recorded per root. They are context for intake: assignment, destination and existing reviews.

## Schemas and forms
- `review-loop-pins/6` (new).
- `workbook-review-form/1`: pass03's form, reused unchanged by pass04.
- `workbook-review-result/1`, `prime-review-record/1` (unchanged).

## Historical context only
- design05.15–05.17;
- 06.17.review;
- 0512/06.12.md (the reporter pin coupling);
- 0522 build05.13 evidence.

## Roots and mutable regions
- **Live `D:\Git\lib-build`:** read-only.
  - It is the import source of pass02 and pass01 code inside every lab run.
  - It is the `ROOT` of the helper modules.
- **Disposable:** `D:/librarian/temp/rie-0718/<run>/<fixture>/`.
  - Mutable: the copied book (`00.kernel/00.00.10.work/**`, including `workbook-review/` records) and `app/librarian.py` (the selection).
  - Retention digests are in `retention.json`. **This is local only, not a durable archive.**

## Lab files (labs/review-entry-integration-pass01)
| File | Purpose |
|---|---|
| candidate/ | proposed production bytes |
| adapter/ | the lab root adapter (pass04 line 28) and the lab declaration |
| rie.py | builds roots, selects the dispatcher, runs the real entry, runs the baseline |
| matrix.py | #03 replay matrix |
| cases/ | the documented adapter that runs the 12 + 17 cases against the candidate pass04 (test files byte-identical) |
| ctx_test.py | context reset |
| lifecycle.py | #04 |
| hostile.py | #05 |
| rollback.py | #06 |
| bundle.py, bundle/INDEX.json, bundle/reconstruct.py | the replay bundle |
