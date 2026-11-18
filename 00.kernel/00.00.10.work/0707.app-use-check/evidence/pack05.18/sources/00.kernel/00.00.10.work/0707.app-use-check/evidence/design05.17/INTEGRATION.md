# Integration handoff — corrected (0707/05.17)
who: claude-opus-5-5 · state: **PROPOSAL for Prime review. Not released; nothing installed.** It supersedes `design05.16/INTEGRATION.md`.

## What changed from 05.16
- **The punctuation refusal is removed.**
- **The grammar is selected by the measured source kind** (`CONTRACT.md`).
- **`build_intake` is wrapped** to carry that kind.
- **The N5 replay is an actual intake identity comparison** (n5replay-run01).

## File and function plan
Successors only; no existing file is edited except one selection line.

| File | Act | Content |
|---|---|---|
| `labs/workbook-review-pass04/workbook.py` | NEW | `proposal/workbook-review-pass04.workbook.py.proposal`. It loads the pinned pass03 (9e66d7e4…, 19533 bytes), captures `p3.parse_pointer` and `p3.p2.build_intake`, and installs a kind-selecting `parse_pointer` plus a kind-setting `build_intake` into the p3, p2 and wb namespaces. |
| `labs/workbook-review-pass04/forms/workbook-review-v1.json` | NEW (byte copy of pass03's form) | **no schema change** |
| `app/review_loop_tools_v8.py` + `app/review-loop-v8.json` | NEW | v7 copied, with the workbook pin pointed at pass04 and pass03 added as a pinned dependency |
| `app/librarian.py` | **one line** | select v8 instead of v7. This is a Prime-owned shared app edit. |
| pass01–pass03, v4–v7 | unchanged | kept pinned, for rollback |

## Dependencies (read-only, pinned)
- **The workbook chain:** pass03 → pass02 (6ce4a5ff…, 52574 bytes) → pass01 (60e040fa…, 79131 bytes).
- **The functions pass04 calls on pass03:** pass01 `address_of` (kind), plus pass03's `accept_field`, `COUNT_RE`, `COUNT_TAILS`, `FIELD_RE` and `p2.suffix_ok`.
- **The modules pass01 PINS and v7 already pin:** `return_access`, `review_loop`, `construct`, `prime_cycle` and `prime_review`.
- **Python stdlib only:** `contextvars`, `hashlib`, `importlib`, `re`.
- **`REPO = D:\Git\lib-build` stays hard-coded.** pass04 does **not** redirect it; only the lab and the check harness do.

## Identity implications
- **N5 pages:** intake_id is unchanged. This is proven on the real 0522/05.13 and on three synthetic punctuation pages.
- **N7 pages:** the intake gains the declared rows, so intake_id differs from v7's for the same page.
  - Stored v7 intakes, reviews and pointers are never rewritten.
  - The existing freshness logic shows a stored v7 intake as stale.
- **No form or stored schema change.**

## Builder acceptance (all must pass before selection)
1. `labs/n7-intake-compat-pass02/tests/test_n7v2.py` gives 12/12 against pass04.
   - Replace `n7compat2.make_parser` and `install` with pass04's `parse_pointer`, `KIND` and `build_intake`.
   - KR1 and KR2 stay pass, as known failures of preserved pass01.
2. The 17 historical cases through an adapter give 16 pass, plus **G7 failing exactly on its REVISED sub-assertions** (`CLAIMS.md` #12).
3. A faithful 05.15 copy under v8: `complete`, **26/26** artifacts, the manual-review hold kept, and the no-review copy publishing.
4. **The 0522/05.13 replay under v8** gives the same intake_id as an unpatched pass03 on the same copy (`n5_replay.py`, with pass04 in place of `--patch`). Add any further real N5 returns Prime chooses.
5. `proposal_check.py` gives `ok` against the built pass04 file (with pass04 in place of the proposal path).
6. Production pins are unchanged, except the intended new files and the one selection line.

## Hold and rollback
- **Hold if:**
  - any N5 intake_id differs;
  - any N5 parse differs from pass03 in P1-type equality;
  - manual-review protection changes;
  - an N7 page binds a file by a name the pointer did not spell.
- **Rollback:** revert the one selection line to v7. pass04 and v8 remain inert. **No data migration is needed.**

## Not in scope
- custody;
- the return-line cutover;
- the agreement fields;
- report projection (06.12.followup);
- the kernel;
- `Notes:`-style lines, which stay `unparsed-return-line` (informational).
