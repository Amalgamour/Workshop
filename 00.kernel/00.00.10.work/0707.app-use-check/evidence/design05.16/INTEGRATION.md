# Integration handoff — smallest builder pack (0707/05.16)
who: claude-opus-5-5 · state: **PROPOSAL for Prime review. Not released; nothing installed.**

## File and function plan (successors only; no existing file edited except one selection line)
| File | Act | Content |
|---|---|---|
| `labs/workbook-review-pass04/workbook.py` | NEW | `proposal/workbook-review-pass04.workbook.py.proposal`: loads the pinned pass03 (9e66d7e4…, 19533 bytes) and replaces **only** `parse_pointer` in the pass03, pass02 and pass01 namespaces |
| `labs/workbook-review-pass04/forms/workbook-review-v1.json` | NEW (a byte copy of pass03's form) | same form; **no schema change** |
| `app/review_loop_tools_v8.py` + `app/review-loop-v8.json` | NEW | v7 copied, with the workbook pin pointed at pass04 and pass03 added as a pinned dependency |
| `app/librarian.py` | **one line** | select `review_loop_tools_v8.py` instead of v7 (Prime-owned shared app edit) |
| pass01, pass02, pass03, v4–v7 | unchanged | kept pinned for rollback |

## Dependencies (read-only roots)
- pass03 → pass02 → pass01 load from `REPO = D:\Git\lib-build` under their pins.
- `return_access`, `review_loop`, `construct`, `prime_cycle` and `prime_review` are pinned by pass01 `PINS` and v7.
- **The lab used a REPO redirect to a disposable copy.** The production pass04 does **not** redirect REPO.

## Identity and pin implications
- **N7 pages:** the intake rows gain the submission and manifest rows and the artifacts, so **`intake_id` values differ from v7's for the same page.** Old stored intakes, reviews, approvals and pointers are **never rewritten**. A stored v7 intake is shown as stale or different by the existing freshness logic and is not silently replaced.
- **N5 pages:** parsing is identical (G1), **except** for a path ending in `, ; : )`. That is now `unrecognized-path-punctuation` instead of a declared path that cannot exist. Prime should scan existing N5 pointers for such paths before selection (they would already have measured as missing).
- **No form or schema change.** `attribution_text` and `declared_form` live only in the parsed pointer, not in stored records, unless pass03 copies the spec. **It does not:** `measure_declared` keeps only path, sha256 and bytes.

## Builder acceptance (must pass before selection)
1. `labs/n7-intake-compat-pass01/tests/test_n7.py` (17 cases) against pass04 instead of the lab wrapper.
2. runs01-equivalent: A (v7) still fails on a copy, and v8 completes, with 26/26 artifacts, on a faithful copy.
3. An unchanged v7 N5 actual-use replay (the 0522/05.13 intake) gives the **same intake_id** under v8.
4. Production pins 50/50 unchanged except the intended new files and the one selection line.

## Hold and rollback
- **Hold** if any N5 replay intake_id differs (other than the documented punctuation case), or if any manual-review protection changes.
- **Rollback:** revert the one selection line to v7. The pass04 and v8 files remain inert. **No data migration is needed;** stored intakes are untouched.

## Not in scope
custody, return-line cutover, the agreement fields, report projection, the kernel, other `Notes:`-style lines (they stay `unparsed-return-line`, informational).
