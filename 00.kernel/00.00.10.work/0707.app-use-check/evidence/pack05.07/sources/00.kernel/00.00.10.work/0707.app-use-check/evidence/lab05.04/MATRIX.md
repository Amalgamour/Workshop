# MATRIX — external acceptance cases for the isolated loop candidate (L1)
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · written before code; implemented in `colab/labs/0707.app-use-check/pass04/cases.py`

## Sources and status
- **Sources:**
  - `design05.03/DELTA-CONTRACT.md` (D1–D5);
  - `design05.03/ACCEPTANCE.md` (L1–L18);
  - `06.03.review.md` (R01, R02, D3.3, legacy eligibility, checks on read, recover and already-rendered);
  - the v2 entry test (T6 fields).
- **This matrix is an execution check, not an acceptance authority.** Prime judges.
- **Status per case:** PASS / FAIL / ERROR / NOT RUN (with a reason), or MANUAL (cannot be exercised by this lab; never counted as a pass).

## Conventions
**Calls.** Every case drives the **candidate CLI** directly:
```
<interpreter> -B <candidate> <command> --fixture-root <disposable book> --request request.json [--decision decision.json]
```
`describe-legacy` uses `--book <root> --member 0182.desk-app-integration-design-0501`.

**Field paths** are contract names (D4). If the reviewed candidate contract names a field differently, Prime supplies `field_map` in the config. Every use of `field_map` is recorded in the run evidence.

**"No writes"** means that, between the snapshots, there is:
- no change to the target page or to `support/`;
- no new `partial/*`;
- no new or changed `cycle/*/rendered.json`.

**Fixtures** (all copied into new roots outside the checkout):
- `pending`: synthetic PENDING page (LF);
- `pending-crlf`: the same page with CRLF line endings;
- `substantive`: the 0519 snapshot;
- `no-heading`;
- `duplicate-heading`;
- `absent`: no target page;
- `legacy-v1-recorded`: a copy of the 05.01 evidence `books/A.after-record`, a genuine /1 record made by loop pass02.

**The decision** comes from the pass01 `decide.py` recipe with pass01's SUPPLIED judgment: held/continue, all required sections. Case A19 overrides the supplied next action.

**Global check (A26):** every JSON object any case receives must carry `accepted: false`, `authority: none`, `custody: not-established`, `allocated: false`, `closes_work: false` and `releases_action: false`.

## Cases
| ID | Source | Fixture and steps | Expected (exit; fields; files) | Evidence that establishes it |
|---|---|---|---|---|
| A01 | L1, D1, F4 | pending: describe → prepare → decide → record → render → read | exit 0 throughout. prepare `target.state` pending, `mechanical.route` record. record `record.result` recorded. render `render.result` rendered. read `pass_state` reviewed, `committed_check.supplied_state` verified-against-committed-record. The page contains `review_disposition (supplied): held`, `pass_terminal (supplied): open`, `goal_terminal (supplied): open` and the not-acceptance disclaimer | raw stdout, page bytes |
| A02 | L2, D1.6 | A01 up to record; tamper `cycle/*/envelope.json` disposition → accepted; render; read | render exit 2, `rule` contains `supplied-state`; no writes. read `mechanical.state` committed-record-mismatch; `committed_check.supplied_state` is not "verified…" | snapshots, stderr |
| A03 | **R01** | A01 up to record; change `envelope.task.task_id`; render | exit 2 **before** apply; no writes (target, support, partial, rendered marker) | Prime's bind demo a8761262 → 8efef653 |
| A04 | R01 | as A03 but change `envelope.agreement.scope` | exit 2; no writes | |
| A05 | R01 | as A03 but change `envelope.evidence[0].label` (supplied → synthetic) | exit 2; no writes | |
| A06 | R01 | as A03 but change `envelope.receipt.return_sha256` | exit 2; no writes | |
| A07 | R01 source change | record, then change `assignment.txt` bytes; render; read | render exit 2; no writes; read `pass_state` review-stale (v2 behaviour, test `test_changed_evidence_stays_stale`) | |
| A08 | L3, D1.1 | record; replace `record.json` with re-serialized bytes; recover | exit 2, `rule` contains `record-hash`; no writes | |
| A09 | L4, D1.2 | record; `envelope.review_identity` → r2; render | exit 2, `rule` contains `review-identity`; no writes | |
| A10 | L5 | pending-crlf: full A01 path, then prepare again | render exit 0. Every line ending in the page is CRLF; the bytes outside the review section are identical. First prepare `target.state` pending; second `constructed-same-binding` | page bytes |
| A11 | L6, **B8** | substantive: prepare → decide → record → render → recover → read | prepare `target.state` existing-review, `mechanical.route` record-then-blocked. record exit 0 and `record.json` matches `COMMITTED.json`. render exit 2, `render.result` render-conflict, page unchanged, exactly 1 partial. recover exit 2, `render.apply_called` false, no new partial. read `mechanical.state` existing-review-conflict; mechanical text says the judgment is retained (R02) | |
| A12 | L7 | record; change one byte outside the section; render; read; prepare | render exit 2, stderr contains `write token changed`; no writes. read `mechanical.state` target-changed-since-record. prepare `target.state` pending (**inspection alone is insufficient**) | |
| A13 | L8 | prepare; change one target byte; decide; record; prepare | record exit 2 with `write token changed since read`; `decision.json` byte-identical; no `cycle/` directory; the second prepare exits 0 | |
| A14a–f | L9, D2 | pending / substantive / pending-crlf / no-heading / duplicate-heading / absent: prepare only | exit 0. Target bytes unchanged (or still absent); no `partial/`; `trace/` written (**prepare is not read-only**). `target.state` respectively pending / existing-review / pending / unsupported / unsupported / absent | |
| A15 | L10 | record; read; recover; read | first read `mechanical.state` render-interrupted, route recover. recover exit 0 rendered. Final read reviewed. Page has the supplied-state lines | |
| A16 | L11, committed checks on shortcut | A01, then render and recover again | `render.result` already-rendered; page unchanged; `committed_check.supplied_state` verified (the shortcut re-checks) | |
| A17 | L12 | A01; delete `cycle/*/rendered.json`; recover; read | recover exit 2; page unchanged; read `mechanical.state` rendered-marker-missing; route not `recover` | |
| A18a–d | L13, R02 | record; then a: delete `record.json` / b: delete `COMMITTED.json` / c: delete `envelope.json` / d: `record.json` not JSON; read; render | no `Traceback` in stderr. render exit 2; no writes. read either refuses (exit 2) or reports `committed_check` not verified; any mechanical text says the state is **not established** | |
| A19 | L14, R02, F7 | the decision's supplied next action is "Run recover now; the render is safe."; record; change the target outside the section; read | `supplied_next_action.text` and `current.next_action.text` equal the supplied text. `next` and `mechanical.text` do not contain it; `mechanical.route` is not recover | |
| A20 | L15, legacy | legacy-v1-recorded (genuine /1): render; read | render exit 0; page has **no** supplied-state block; `committed_check.supplied_state` names legacy /1 | the copied book's source hashes |
| A21 | **forbidden downgrade** | A01 up to record (/2); rewrite `envelope.json` as /1 (drop the state; schema /1); render | exit 2; no writes (**a new /2 record is not eligible for /1**) | |
| A22 | L16, D3.3, R02 | absent: prepare → decide → record → read | prepare `target.state` absent, route none; the text does **not** claim a kept or committed judgment. record exit 2; `decision.json` byte-identical; no `cycle/`. read does not claim a commitment | |
| A23 | R02 | pending: prepare → read (no record) | the mechanical text does not claim a kept, retained or committed judgment | |
| A24 | L17 | pins: wrong construct byte refuses before launch | **MANUAL**: needs a relocated code copy, but ROOT is literal; check the candidate's `pin_set` by inspection at activation | — |
| A26 | L18 | global flags check over every JSON output of the run | as stated above | all stdout |

**Not in this matrix (already proven elsewhere):** the pass04 internals, the cycle couplings, and the /2 envelope through the unchanged cycle.
