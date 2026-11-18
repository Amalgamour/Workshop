# CONTRACT (proposed) — review-loop entry v3: usability successor
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · state: design proposal for Codex Prime; not released, not accepted, not implemented

This contract covers four repairs: F4, F8, F7 and F11.
- F1, F2 and F6 are covered by `OPERATOR-GUIDE.md`, which is documentation.
- F3 (mechanical prefill) and F5 (verified judgment expansion) are deferred, with their tradeoffs given below.
- Portability is a separate slice (`PORTABILITY.md`).

**Current behaviour cited here is observed** (probe or source line). **Proposed behaviour is marked PROPOSED.**

## 0. Invariants the successor must keep (current, verified in 05.01 and reproduced by Prime)
1. **Refusal boundaries stay as they are.**
   - A wrapper refusal is `stop:`, exit 2, and the loop never starts.
   - Render after a target change is refused (`write token changed since read`, exit 2).
   - A substantive existing review causes `render-conflict`, exit 2: the page is unchanged and one partial is kept.
   - A fixture root inside the checkout or the live book is refused.
2. **Judgment and source bytes are kept exactly.**
   - `cycle/<id>/record.json` hashes to the `record_sha256` that `read` names.
   - Its decision equals the recorded decision, compared as canonical bytes.
   - The page's support record equals the supplied record.
3. **The authority layer is unchanged.** Every result carries `accepted: false`, `custody: not-established`, `authority: none`, `allocated`/`closes_work`/`releases_action`/`authenticates_actor: false`. No supplied value changes any of them.
4. **Interrupted render → `recover` renders. A repeated render or recover → `already-rendered`,** with the page unchanged.
5. **Unchanged modules:**
   - the pass03 cycle (`labs/prime-cycle-pass03/prime_cycle.py`);
   - `prime_review` pass01 and pass02;
   - the readers (`return_inspect`, `return_capture`, `return_lines`, `return_placement`);
   - the pass02 constructor (it stays on disk, still pinned and called by the cycle for `bind`).

## 1. F4 — visible supplied review state
**Current.**
- The page's `### Judgment` block (`construct.py` pass02, `render_review`, lines 522–552) prints only outcome, effective, finding and semantic_conflict, all from the `prime_review` pass02 report.
- `prime_review` pass02 `parse_judgment` (line 586) takes an exact key set without `disposition`, so the supplied record cannot carry it.
- The disposition is only in the cycle decision (`prime_cycle.py check_judgment` 1295–1333) and in `cycle/<id>/REVIEW.md`.
- Probe P3: a `correction-required` review rendered with no disposition line (`probes/run1/P3-page-after.md`; `P3-REVIEW.md` shows "disposition: correction-required").

**PROPOSED.**

**Connector:** the loop's `record` builds the envelope as schema `review-construction/2`. Its keys are the 13 keys of `/1` plus `supplied_review_state`:

```json
"supplied_review_state": {
  "schema": "supplied-review-state/1",
  "source": "cycle decision judgment",
  "disposition": "<judgment.disposition verbatim>",
  "pass_terminal": "<judgment.pass_terminal verbatim>",
  "goal_terminal": "<judgment.goal.terminal verbatim>",
  "outcome": "<judgment.outcome verbatim>"
}
```

- **Copied, never derived.** The values come from the decision file being recorded. The envelope is an input to the cycle's `record`, which then validates that same decision; render re-checks the copy against the committed `record.json`.
- **No new decision.** The cycle validates `envelope.record` and `envelope.target` only (`prime_cycle.py` 1521–1524) and stores the envelope bytes in `cycle/<id>/envelope.json`. So no cycle change is needed. Probes do not cover this; it is from source reading, and acceptance case A4.1 must prove it.

**Integrity at render:**
- `render_committed` reads `cycle/<id>/record.json`, checks that its sha256 equals `latest_review.record_sha256`, and checks that the envelope's `supplied_review_state` equals the same four fields of `record.decision.judgment`.
- On a mismatch it refuses, exit 2: `supplied review state does not match the committed record`.
- `COMMITTED.json` does not bind `envelope.json` (it names record and REVIEW.md only), so this check closes a real gap.

**Renderer:** a new `labs/review-construction-pass03/construct.py`.
- It accepts `/1`, rendered exactly as pass02 does, and `/2`.
- For `/2` it validates `supplied_review_state` with exact keys and the cycle's enums: disposition {accepted, held, correction-required}; pass_terminal {open, finished}; goal_terminal {open, completed}; outcome {continue, director-input, develop, complete}.
- It does **not** re-check the couplings (the cycle owns them). It renders, directly after `### Judgment`'s existing lines:

```text
### Supplied review state
review_disposition (supplied): held
pass_terminal (supplied): open
goal_terminal (supplied): open
This is the reviewer's supplied state. It is not Director acceptance, approval, seating or authority; see authority: none above.
```

**Binding is unchanged.** `bind`, `measure` and the task-binding computation must stay byte-for-byte equal to pass02. The cycle keeps calling pass02 `bind` (`prime_cycle.py:919`), and the loop compares the pass03 `show` binding with the cycle's (`review_loop.py` `finish_render`). Acceptance case A4.5 proves equality.

**Not done:** no change to `prime_review`, no new disposition values, no inference of acceptance. `accepted: false` stays on every result whatever the disposition (A4.4).

## 2. F8 — target inspection before judgment work
**Current.**
- `prepare` reports `awaiting-review: a described return has no recorded review` for all six target shapes: PENDING, substantive, a constructed review with another binding, no heading, duplicate heading, and absent (`probes/run1/08–13-P2-*.stdout`).
- For an absent target the template's `write_token` is null.
- The constructor's conflict rule is in `compose` (pass02, 784–843), after the expected-hash check: `locate()` must find exactly one review heading; a section equal to the new body is idempotent; a stripped section not in {`PENDING`, `PENDING.`} is a conflict.
- `preview` runs that rule read-only but needs a complete envelope with a supplied record, so it cannot run before a judgment.
- `show` requires a `task_binding:` line, so it refuses PENDING and hand-written reviews alike (`probes/run1/02–07-P1-*`).
- **No existing call classifies a target before judgment. This is the missing connector.**

**PROPOSED.**

**Connector:** constructor pass03 gains a read-only command:

```text
construct.py inspect --fixture-root ABS --target REL [--binding HEX64]
```

- Output `review-target-inspection/1`: `{state, rule, target_sha256|null, target_bytes|null, section_sha256|null, binding_sha256|null}`.
- `state` is one of:
  - `absent`;
  - `unsupported` (the `locate` refusal text, for example `missing review heading`, `duplicate review heading` or `unsupported format: not utf-8`);
  - `pending`;
  - `constructed-same-binding`;
  - `existing-review`.
- The rule order and texts are exactly those of `compose`. It reuses `newline_of`, `locate` and the PENDING set.
- **It never writes,** including no partial.
- The prototype is `colab/labs/0707.app-use-check/pass02/proto.py classify_target`. It imports the pinned pass02 `locate`, and on 8 shapes it matches the expected states (`probes/proto-check.json`).

**Loop `prepare`:** after the cycle read, the loop calls `inspect` with the template binding and adds:
- `target: <review-target-inspection/1>`;
- one attention line, `target: <state>: <rule>`;
- a `mechanical` block (see F7).

Prepare still exits 0 and still offers the template. **This is reporting, not a gate.**

**Mechanical text per state:**

| state | `mechanical.route` | text |
|---|---|---|
| `pending` | `record` | Supply a typed judgment and supplied_record, then record. |
| `existing-review` | `none-in-this-entry` | The target already holds a review. This entry will refuse to render over it; a successor process is required. Writing a new judgment here will commit a record that cannot be rendered. |
| `constructed-same-binding` | `read` | A constructed review for this task binding is present. Read it before writing another judgment. |
| `absent` | `none-in-this-entry` | The derived target page is absent. This entry does not create targets. |
| `unsupported` | `none-in-this-entry` | `<rule>` |

**Final checks unchanged:** render still does the expected-hash, write-token and `compose` checks. A pending result at prepare guarantees nothing at render (A8.6).

**Prime decision (B8):** should `record` also refuse when the target is `existing-review`, `absent` or `unsupported`? Doing so would stop the unrenderable committed record seen in 05.01 E. It is a new refusal point in an existing command, not a new command. My recommendation is report-only (A) in this slice and B only if Prime wants it. B changes what `record` commits, which is the cycle's evidence.

## 3. F7 — mechanical next, separate from supplied next action
**Current.** `review_loop.read_back` (512–524) puts `view.next_action.text`, the supplied words, into `next` whenever present. That holds in D (render-pending after a refusal) and E (render-conflict): `next` = "Codex Prime supplies its own judgment…". The view already holds what is needed:
- `view.write_token` (current page);
- `view.latest_review.write_token` (recorded against);
- `render_state`;
- `pass_state`.

In 05.01: D 3c7f…≠a3fc…, B equal, E conflict.

**PROPOSED.** Result schema `review-loop-result/2` for prepare, record, render, recover and read:
- `mechanical: {blocker, route, text}`, a pure function of the cycle view and the render outcome (prototype `mechanical_state`, 5 of 5 against recorded views). Blockers: `render-interrupted` → route `recover`; `target-changed-since-record` → `none-in-this-entry`; `existing-review-conflict` → `none-in-this-entry`; `unknown-state` → null. No blocker when the review is rendered or awaiting record.
- `supplied_next_action`: the supplied `{action_id, text, authorized_in_grant}` verbatim, or null. It is labelled supplied and never used to compute `mechanical`.
- `next`: in `/2`, equal to `mechanical.text`. It is **never** the supplied text. The supplied words stay in `supplied_next_action` and on the page.
- `/1` consumers are listed in `IMPACT-MAP.md`.

**Recover meaning** (also in the guide): retry rendering of the same committed review against an unchanged target. It does not repair a changed target or a conflict. There is no supersession in this entry.

## 4. F11 — clean decision template and example provenance
**Current.**
- The example registration (`labs/prime-entry-pilot-pass01/example-registration.json`) carries `recorded_decisions: [D1, source_sha256 b8d56162…, "The disposable copy was supplied for this pilot."]`. It is rendered verbatim into any review page that reuses the example (05.01 F11).
- `prime_review` accepts `recorded_decisions` as null or a list of `{id, text, source_sha256}` (`parse_agreement` 448–470). The constructor renders both null and `[]` as `none supplied` (pass02 597–603), and prints `id: text` with no source hash.
- Probe P3 (`recorded_decisions: []`) recorded and rendered with `recorded_decisions: none supplied`.
- P3 exited 1 because my fixture omitted three sections that outcome `continue` requires (see Findings G4). The `[]` agreement was not the cause.

**PROPOSED (data and docs, plus one render line):**
- **A NEW `labs/prime-entry-pilot-pass02/`** with:
  - `example-registration.json` setting `agreement.recorded_decisions: null`, `director_required`/`prime_discretion` texts prefixed `SAMPLE ONLY:`, and no `source_sha256` anywhere;
  - `real-decision-template.json` schema `review-loop-real-decision-template/2`, whose `agreement` is entirely null with a note: "fill from the actual assignment page; each recorded decision needs the sha256 of the exact cited Director reply bytes".
- **pass01 files stay unchanged as history.**
- **Constructor pass03** renders a recorded decision as `- D1: <text> (source sha256 <hex>)`, so an actual Director decision stays attributable on the page. It renders `null` as `none supplied` and `[]` as `none recorded`. Today the page cannot tell those apart.
- **Not done:** no default D1, no deletion or reinterpretation of historical replies, no new speaker or path field. `prime_review` `/1` records have only the sha, and a path field needs a `prime_review` successor, which is out of this slice.

## 5. Deferred: F3 and F5 (dependencies and tradeoffs)
**F3, mechanical prefill.**
- `prepare` could emit `supplied_record` with `sources`, the capture identity and `agreement` filled, leaving `attribution` and `judgment` null.
- It depends on the same measured bytes the cycle re-checks (`align_sources`), so a prefill bug becomes a refusal, not silent corruption.
- The cost is that the loop must reproduce `source_row` exactly. The only reference for that is `pilot.py`/`decide.py`, a lab recipe, not a reviewed contract.
- Do it after the slice-1 envelope `/2` lands, because both touch `prepare`/`record` output.

**F5, verified judgment expansion.**
- `read` could add `committed: {record_sha256, decision_judgment, verified: true}` after re-hashing `record.json`. The page support hash would be reported as `support_record_sha256`, a separate name, so the two identities do not share the label `record_sha256`.
- It depends on nothing new, but it doubles `read` output size and is pure convenience.
- The guide gives the manual route now (OPERATOR-GUIDE §5).

## 6. Failure semantics (all PROPOSED unless marked current)
- **Current:** exit 0 = command completed with no attention. Exit 1 = completed, but `prime_review` returned attention; the record is committed, or the page is rendered with `effective: attention` (P3). Exit 2 = refusal; nothing written except a partial on a conflict.
- **`inspect`:** exit 0 for every classified state, including absent and unsupported. Exit 2 only for argument or fixture-root refusals.
- **Missing pinned file:** a refusal (exit 2), not a traceback. This belongs to the portability slice; slice 1 must not introduce new unguarded `read_bytes` on pinned paths.
