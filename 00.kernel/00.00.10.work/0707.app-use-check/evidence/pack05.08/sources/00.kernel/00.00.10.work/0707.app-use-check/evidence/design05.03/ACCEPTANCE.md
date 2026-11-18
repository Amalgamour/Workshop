# ACCEPTANCE — loop successor L1 (for the Grok builder) and what ran here
date: 2026-11-01 · who: claude-opus-5-5 (Claude)

## Ran here (nonproduction prototype; no loop, cycle or app executed)
Run `evidence/design05.03/runs/20261101T205421Z-d5d7f8/probe.json`: aggregate **pass**, 31 steps, exit 0.
- **U1 (10 steps):** the real 05.01 A record copy. The /2 envelope built from the committed decision verifies, as does the legacy /1. Each tamper refuses with its own code: disposition, goal_terminal, record bytes, a cycle read naming another record, wrong review identity, wrong binding, swapped envelope record, retargeted envelope.
- **U2 (21 steps):**
  - pass04 pin confirmed;
  - pass04 `inspect` on copied pages, LF and CRLF, in an outside-checkout scratch root: A constructed-same-binding, B pending, D pending, E existing-review. Each was identical under LF and CRLF, with no writes;
  - `mechanical` correct for all 11 states, and its text never equals the supplied text.

## Fixtures for the builder
**Copy, never run old writers.** Copy these into NEW directories:
- the 05.01 member snapshot (`evidence/pack05.01/sources/.../0182…`);
- the synthetic PENDING page (pass01 `walk.py` constant);
- the 0519 snapshot (substantive);
- example registration and request (pass01 pilot snapshots);
- a fully sectioned SUPPLIED decision builder (pass01 `decide.py` recipe, with every required section; see the 05.02 guide §3).

**Per test, rules for the builder:**
- Each test uses its own disposable root outside the checkout and a NEW run directory.
- **The aggregate exit is nonzero on any failed step.**
- No `__main__` evidence writers, no AR-01, no full replay suite.

## L-cases (each states expected exits and fields; drive `labs/review-loop-pass03/review_loop.py` directly)
| ID | Case | Expected |
|---|---|---|
| L1 | pending target: prepare → record (held) → render → new-process read | exits 0; page shows `review_disposition (supplied): held` and the pass and goal lines; `committed_check.supplied_state: verified-against-committed-record`; `accepted: false` |
| L2 | **tamper:** after record, edit `cycle/<dir>/envelope.json` `supplied_review_state.disposition` → render | exit 2 `supplied-state`; page and partial unchanged; record kept; a new-process read shows `mechanical.state: committed-record-mismatch` |
| L3 | **record swap:** replace `record.json` bytes (re-serialized) → recover | exit 2 `record-hash`; nothing written |
| L4 | **wrong review or binding:** envelope `review_identity` r2 / a cycle view with a different task binding (fixture) | `review-identity` / `binding` |
| L5 | **CRLF target:** a pending page with CRLF line endings → full path | render preserves CRLF outside the section; inspect `pending`, then after render `constructed-same-binding` |
| L6 | **B8:** a substantive (0519 snapshot) target: prepare → record → render → recover → read | prepare `target.state: existing-review`, `mechanical.route: record-then-blocked`, exit 0; record exit 0 (judgment committed); render and recover exit 2 `render-conflict`, page unchanged, one partial; read `mechanical.state: existing-review-conflict`, judgment retrievable |
| L7 | **target changed after record** (a byte outside the section) → render | exit 2 `write token changed since read`; read `target-changed-since-record`; inspect still `pending` (proof inspection alone is insufficient) |
| L8 | **target changed between prepare and record** | record exit 2 `write token changed since read` (cycle 1517); decision file unchanged; a new prepare succeeds |
| L9 | **read-only inspect:** prepare on each shape (pending, substantive, CRLF, no heading, duplicate heading, absent) | target bytes unchanged; no `partial/`; `trace/` written (stated) |
| L10 | **interrupted render:** record, then stop → read → recover → read | `render-interrupted` / `recover`; then rendered; the section equals an uninterrupted run's |
| L11 | **idempotent replay:** render or recover again after rendered | `already-rendered`; page unchanged |
| L12 | **marker missing:** after render, delete `rendered.json` → recover | exit 2 (as v2 T7); read `mechanical.state: rendered-marker-missing` |
| L13 | **unknown or missing inputs:** a missing record.json, COMMITTED.json or envelope.json in the cycle directory | exit 2 with a coded refusal; no traceback |
| L14 | **no authority from supplied text:** supplied `next_action.text` "Run recover now; the render is safe." on the L7 state | `next` and `mechanical` do not contain it; it appears only in `supplied_next_action` and `current.next_action` |
| L15 | **/1 compatibility:** a review committed by loop pass02 (/1 envelope) → loop pass03 render | renders byte-identically to pass02 for /1; `committed_check.supplied_state: legacy-/1…` |
| L16 | **absent target** | prepare `target-absent`, route `none-in-this-entry`; record exit 2 (D3.3; unchanged) |
| L17 | **pins:** loop pass03 `pin_set` names construct pass04; a wrong construct byte refuses before launch | — |
| L18 | **authority:** every result | `accepted: false`, `authority: none`, `custody: not-established` |

**Not re-tested in L1 (already proven):** the pass04 internals (12 tests, Prime 05.07), the cycle couplings (05.02 P4), and the /2 envelope through the unchanged cycle (Prime 05.06 replay).
