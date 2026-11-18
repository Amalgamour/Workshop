# IMPACT-MAP (corrected) — isolated loop successor first
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · source inspection of pack05.03 bytes; nothing edited

## Slice L1: isolated loop successor (recommended first)
| Path | Change |
|---|---|
| NEW `labs/review-loop-pass03/review_loop.py` | copy of pass02 with: `CONSTRUCT` → pass04 (`6d541d42…`, 42582) for apply, show and inspect; `build_envelope` /2 (D1); `verify_committed` before apply in `render_committed` (render and recover) (D1); `prepare` calls pass04 `inspect` (D2); `review-loop-result/2` fields (D4); the cycle and its pins unchanged |
| NEW `labs/review-loop-pass03/tests/` | ACCEPTANCE L-cases, driving `review_loop.py` directly (not the app) on disposable roots |

**Unchanged:**
- `app/*`: the door v2, `review-loop-v2.json` and `librarian.py`;
- cycle pass03 (`prime_cycle.py`, 76045 bytes; it still pins and calls construct **pass02** `bind`, line 919);
- construct pass02, pass03 and pass04;
- prime_review pass01 and pass02;
- the readers;
- the v2 test;
- the 0525 sets.

**Internal pins in loop pass03 (`pin_set`):**
- construct pass04, as `CONSTRUCT`;
- cycle pass03;
- prime_review pass01 and pass02;
- return_lines, return_placement and return_inspect, unchanged values;
- its own bytes.

**Construct pass02 remains reachable only through the cycle.** The loop no longer calls pass02.

**`reproduce`** (lab command) keeps using its pass02 constructor path unless the builder states otherwise. It is outside L1.

## Slice L2: entry selection (separately bounded, later)
**New files:**
- `app/review_loop_tools_v3.py`;
- `app/review-loop-v3.json`.

**TOOLS** = loop pass03, construct pass04, construct pass02 (cycle bind dependency), cycle pass03, prime_review pass01 and pass02, and the three readers.

**One load-path edit** in `app/librarian.py`, plus an appended README section.

**Tests:** a new `app/tests/test_review_loop_entry_v3.py`; the v2 test stays as it is.

**Pilot pass02 data:** clean example registration, `SAMPLE ONLY:` texts, no D1.

**Coordinated records** in the 0525 v2 representation: loop pass03, construct pass04, door v3 and declaration v3, plus a changed `librarian-review-loop`. Do not edit /1 or existing v2 records to describe future code.

**Not in L1 or L2:** portability (sequential, same owner); the K1–K3 page-local workflow (Grok-2's 0511/05.04; not a dependency); live-book use.

## Subprocess map (L1)
| Caller | Callee | Command |
|---|---|---|
| loop pass03 | cycle pass03 | `read`, `record` (unchanged) |
| cycle pass03 | construct pass02 | `bind` (unchanged) |
| loop pass03 | construct pass04 | `inspect` (prepare), `apply` (render, recover), `show` (after apply) |
| loop pass03 | inspector, placement | `describe-legacy` (unchanged) |
