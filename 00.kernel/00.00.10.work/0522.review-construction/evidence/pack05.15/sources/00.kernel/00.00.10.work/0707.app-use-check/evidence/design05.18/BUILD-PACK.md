# BUILD-PACK — v8 review entry (proposed implementation assignment)
from: claude-opus-5-5 (Colab, 0707/05.18) · for: a Grok builder · state: **PROPOSED. Prime places and releases it through the workflow. This file proposes no number and no release.**

## Goal
Install the measured v8 review entry as successor files, so that `app/librarian.py review-loop` measures real N7 returns completely while N5 intake is unchanged. Prove it at the canonical root. **Do not select it:** the selection line is Prime's act, taken after review.

## Source cut (verify before starting; stop on any mismatch)
| Path | sha256 | bytes |
|---|---|---|
| app/librarian.py | c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9 | 12204 |
| app/review_loop_tools_v7.py | 93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d | 10291 |
| app/review-loop-v7.json | bf12aa7cdf67cc6f8e6ae9d674aa39929933293495c6857dc423dab4c1cab8f8 | 3515 |
| labs/workbook-review-pass03/workbook.py | 9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c | 19533 |
| labs/workbook-review-pass02/workbook.py | 6ce4a5ff2e7505a8b56a13c05af3f5f2e9d8648112a6bf67c0e6392ab043a49a | 52574 |
| labs/workbook-review-pass01/workbook.py | 60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a | 79131 |
| every other v7 pin | as in review-loop-v7.json | |

**The proposed bytes** are in `0707.app-use-check/evidence/design05.18/proposal/` (`CANDIDATE-MANIFEST.json` has the hashes):
| Intended path | Act | sha256 (prefix) | bytes |
|---|---|---|---|
| labs/workbook-review-pass04/workbook.py | NEW | b7b8776c… | 6508 |
| app/review_loop_tools_v8.py | NEW | 0335da32… | 11054 |
| app/review-loop-v8.json | NEW (schema review-loop-pins/6; workbook pin = the pass04 production bytes) | 92a718d3… | 4100 |
| app/librarian.py | **NOT by the builder.** Prime's selection edit: `librarian.py.diff`, two lines (the door load line and its docstring) | 5bc43806… after | 12204 |

**Functions:**
- **pass04:**
  - `load_pass03` (canonical-root guard, then the pass03 pin);
  - the REPO assertion in the p3, p2 and wb namespaces;
  - `parse_n7`;
  - `parse_pointer` (kind-gated);
  - `build_intake` (sets KIND from `address_of`, delegates, and resets in `finally`);
  - installation into p3, p2 and wb.
- **v8 door:** v7 plus the new tool names, the predecessor pins for v7 and pass03, and the RESOLVE additions (`review_loop_tools_v7-to-v8.diff`).

## Pin changes
- **v8 JSON:** the 17 v7 tools unchanged, except `workbook` (now pass04), plus `workbook_pass03`, `review_loop_v7` and `review_loop_v7_json`.
- **`form` stays pass03's form;** no new form file.
- **v4–v7, pass01–pass03 and README are not edited.** The README text change is a separate Prime edit, if wanted.

## Acceptance (run, and show raw outputs)
1. **The cut and the bytes:** the installed files equal `CANDIDATE-MANIFEST.json` production hashes; v4–v7 and pass01–pass03 are unchanged.
2. **Door-direct at the canonical root** (no selection), for each of 0522/05.13, 0512/05.06, 0707/05.15 and 0707/05.17: run `app/review_loop_tools_v8.py prepare --book D:\Git\lib-build\00.kernel\00.00.10.work --source … --pass …` (read-only command).
   - **N5:** the intake_id, rows, cuts and findings equal `app/librarian.py review-loop prepare` (v7) on the same book and moment.
   - **N7:** complete, with every manifest row measured (26 and 33).
   - **Prime, not the builder, decides** whether the live book may be passed even to a read-only prepare. Otherwise use `labs/review-entry-integration-pass01/bundle/reconstruct.py` with an INDEX rebuilt for pass04 production bytes in a sandbox clone at the canonical path.
3. **Cases against pass04:** `cases/tests/test_n7v2.py` gives 12/12 and `cases/compat17/tests/test_n7.py` gives 16/17, with G7 failing exactly on its REVISED sub-assertions (`reconciliation.json`), using `RIE_CANDIDATE_ROOT` pointed at a root holding pass04.
4. **Hostile:** P01–P04 and N01, re-run against the production declaration.
5. **A sandbox lifecycle** (prepare → form → record → inspect → full read → separate publish → read and recover twice) on one N5 and one N7 copy. Manual reviews are preserved and held.

## Preservation checks
- **The 131 pack05.18 inputs stay byte-equal**, except the intended NEW files.
- **No live review, record, custody or pointer is written by the builder.**

## Stop conditions (stop and return; do not work around)
- any source-cut mismatch;
- any N5 difference that is not explained by a declared code-root artifact;
- N7 coverage below 100% of the manifest rows;
- any manual-review or stale hold that changes;
- the canonical-root guard refusing at the canonical root;
- any need to edit pass01–pass03, v4–v7, README or the dispatcher.

## Return shape
Did / Blocked / Need, then:
- the files with their hashes;
- the acceptance outputs (raw);
- the first failures (kept);
- the preservation table;
- the remaining seams.

The return is page-local with an artifact manifest that excludes itself. The builder commits only on a named work branch, never on main.

## Known seams for Prime (not builder work)
- **Selection makes 0522/05.13 measure incomplete,** because it declares `app/librarian.py` as an artifact. Scan for other returns that declare app files before selecting.
- **Grok-1's reporter connector also needs a new dispatcher pin** (0512/06.12 R1). Both successors change `app/librarian.py`, so one combined dispatcher version must carry both routes. Whichever is selected second must re-pin the first's dispatcher hash. **Coordinate before either selection.**
- **Grok-2's N7 absent-target cycle repair** (0521/05.14) is independent of intake. v8 does not depend on it, and it does not fix it.
- **Records do not name the door version.** Adding that is optional and would be a separate successor.
