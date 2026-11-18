# DELTA-CONTRACT — loop successor after constructor pass04
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · state: design delta against `evidence/build05.02/CONTRACT.md` (kept unchanged). Not implemented, released or seated.

**Unchanged from 05.02 unless listed here:**
- invariants §0;
- F7 separation;
- F11 data;
- deferred F3 and F5;
- failure semantics.

Source facts T1–T8 are in `06.03.notes.md`. Prototype: `colab/labs/0707.app-use-check/pass03/` (nonproduction).

## D0. Corrections to the 05.02 contract and map
| 05.02 said | Now |
|---|---|
| new constructor **pass03** | the accepted constructor is **pass04** (`labs/review-construction-pass04/construct.py` `6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20`, 42582). pass03 is held (G01 CRLF binding; G02 enum TypeError) |
| constructor `inspect` was "proposed" | **pass04 has it** (T3), with newline-aware binding reading |
| "slice 1a = constructor alone" | **done and accepted** (0522/05.07). The /2 envelope through the unchanged cycle was replayed once by Prime (record, read, bind exit 0; bindings equal) |
| 0525 set "not an accepted basis" | **0525/05.02 v2 is verified within declared coverage**: 21 environment rows are unverified and there is no closure claim. Records for new modules belong in the v2 representation |
| v2 entry test "unread" | **now read** (T6). It drives `librarian.py`; its asserted fields are listed in §D5 |
| `outcome` rendered as supplied state | **pass04 renders 3 supplied-state lines.** `outcome` is validated but shown only through the existing `outcome:` line (T2). Recorded as is; not a defect |

## D1. Supplied state against the committed judgment (F4 integration)
**At `record`**, loop pass03 builds the envelope:
- `schema: review-construction/2`;
- `supplied_review_state` = {`supplied-review-state/1`, `cycle decision judgment`, `judgment.disposition`, `judgment.pass_terminal`, `judgment.goal.terminal`, `judgment.outcome`}, copied verbatim from the decision being recorded.

The cycle stores the envelope bytes as given (`prime_cycle.py` 1521–1564; T4).

**Before any constructor `apply`** (render and recover), `verify_committed` runs. Each failure below refuses with exit 2, writes nothing, and keeps the committed judgment:

| # | Check | Refusal |
|---|---|---|
| 1 | sha256(`cycle/<dir>/record.json`) = `COMMITTED.json.record_sha256` = the cycle read's `latest_review.record_sha256` | `record-hash` |
| 2 | `envelope.review_identity` = registration `review_identity`; `record.review_id` = `decision.review_id` = `latest_review.review_id` = `<pass>-<review_identity>` | `review-identity` |
| 3 | `decision.binding.task_binding_sha256` = `latest_review.task_binding_sha256` | `binding` |
| 4 | `envelope.record` = `decision.supplied_record` | `envelope-record` |
| 5 | (`envelope.target`, `envelope.pass`) = registration | `envelope-target` |
| 6 | /2: `envelope.supplied_review_state` = the state rebuilt from `decision.judgment` | `supplied-state` |

- **Legacy /1:** allowed, reported `legacy-/1-envelope: no supplied state is rendered`.
- **After `apply`**, the existing checks stay: the target hash after rename, and the pass04 `show` binding = the committed task binding (`finish_render`).
- **The prototype** proves checks 1–6 on a copy of the real 05.01 A record: 10 of 10, with each tamper refusing distinctly (probe U1).
- **Authority:** `review_disposition (supplied)` is the reviewer's technical state. Results keep `accepted: false` and `authority: none`. Nothing here is Director acceptance or release.

## D2. Target inspection and the mechanical next (F8 and F7)
**`prepare`** calls pass04 `inspect --fixture-root --target --binding <template task binding>` and adds the result as `target` (`review-target-inspection/1`).
- **The inspection is read-only:** probe U2 found the target bytes and the root contents unchanged in 8 of 8 runs.
- **`prepare` still writes its own `trace/`**, as today. The two must not be described as one read-only step.

**Every result adds `mechanical {state, blocker, route, text, target, detail?}`.** It is a pure function of the cycle view, the inspection and the D1 check (prototype `mechanical`; 11 of 11 states in probe U2). It never reads supplied text.

| State | When | Route |
|---|---|---|
| `awaiting-review` | target pending | `record` |
| `awaiting-review` + blocker `target-existing-review` / `-unsupported` / `-constructed-same-binding` | the target can't take this render | `record-then-blocked`: recording preserves the judgment (B8); render will refuse |
| `awaiting-review` + `target-absent` | no target page | `none-in-this-entry`: `record` itself refuses an absent target today (T5); see D3 |
| `render-interrupted` | committed; tokens equal; target pending | `recover` |
| `render-blocked` | committed; tokens equal; target existing or unsupported | `none-in-this-entry`; the judgment is committed |
| `target-changed-since-record` | tokens differ, not this binding | `none-in-this-entry` |
| `rendered-marker-missing` | tokens differ; inspect `constructed-same-binding` with the committed binding (T7) | `none-in-this-entry`; recover refuses today |
| `existing-review-conflict` | `render_state: conflict` | `none-in-this-entry` |
| `rendered` | reviewed and rendered | `read` |
| `committed-record-mismatch` | a D1 refusal | `none-in-this-entry` |
| `unknown-state` | anything else | `none-in-this-entry` |

- **`supplied_next_action`** carries the supplied {action_id, text, authorized_in_grant} verbatim.
- **`current.next_action` keeps its existing value and position,** because the v2 test asserts it (T6).
- **Top-level `next` = `mechanical.text`.** It is never supplied prose.
- **Inspection alone is insufficient.** The 05.01 D page, changed outside its review section, inspects as `pending`, and only the token comparison detects the change (U2). Final render checks always run; a pending preflight guarantees nothing.
- **Recover** retries the same committed render into an unchanged target. It does not repair a changed target, a conflict or a missing marker.

## D3. B8: preserving valid judgments (Director: "Preserve the judgment; clearly report the block")
- **`record` is never refused because of the target's review state.** Existing-review, unsupported and constructed targets are reported through `mechanical`, and the cycle commits the valid judgment.
- **Render refuses unsafe writes** as today: `render-conflict` (exit 2, one partial, page unchanged), or the stale write-token refusal.
- **Unchanged validations that still refuse `record`,** and are not overridden by B8:
  1. the source and judgment checks (cycle `check_judgment` and `align_*`);
  2. a target that changed between prepare and record (`prime_cycle.py:1517`). The decision file is untouched; re-run prepare and copy the judgment words into the new template;
  3. **an absent target.** The loop hashes the target before calling the cycle (T5).
- **D3.3 is an existing behaviour that B8's wording may or may not cover.** I do not reopen B8. I recommend keeping it: an absent derived target is an addressing defect, and `prepare` now reports it *before* judgment work, so no judgment is lost. If Prime reads B8 as requiring a record without a target, that is a cycle and loop change outside this slice.
- **No supersession and no overwrite.** Earlier and successor reviews stay separate. The template's `supersedes` and `recovers` keys are not operated by this slice.

## D4. Commands, schemas and exits
- **Commands:** the same six loop commands. No new command and no new gate.
- **Result schema `review-loop-result/2`** adds `target` (prepare), `mechanical` (all), `supplied_next_action` (all) and `committed_check` (render, recover, read).
- **Kept keys:** `pass_state`, `full_success`, `render.result`, `render.apply_called`, `current.*`, flags.
- **Refusals stay `review-loop-refusal/1`.** The D1 codes appear in `rule`.
- **Exits are unchanged:** 0 complete, 1 attention, 2 refusal or render-conflict.

## D5. /1 compatibility and consumers
**v2 test assumptions (T6) that a v3 result must keep:**
- `pass_state`, `full_success`, `render.result`, `render.apply_called`;
- exit codes;
- `review-loop-refusal/1` with "refused:" on stderr for refusals;
- no "refused:" on render-conflict;
- `current.next_action.text`.

**Two v2-test cases touch the L2 switch. Source inspection says both still hold** (not run):
1. `test_core_pins_and_old_facade_stay` checks the PINS of the unchanged v2-era files, plus two `librarian.py` facts: it contains `review-loop`, and its sha is not 939484f1…. A load-path edit keeps both true.
2. The T7 case still expects a refusal. v3 reports `rendered-marker-missing` and does not auto-repair, so it still refuses.

Every other v2 case would then exercise v3 through `librarian.py`. Its asserted fields are kept (above).

**Consumers:** pilot pass01 and 0707 pass01 stay historical. **The v2 test must never be run as `__main__`,** because it writes into 0522 evidence.
