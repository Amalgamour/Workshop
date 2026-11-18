# ACCEPTANCE (proposed) — focused cases for review-loop entry v3
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · state: proposed tests; none run against a successor (none exists)

## Rules for the tests
- Each case states **before** (the current v2 observation, with evidence) and **after** (the expected v3 output).
- Expected values are written from this contract, not copied from the implementation's output.
- Every case runs through `app/librarian.py review-loop` on a disposable root, except the A4.5 unit check.
- Each command is a separate process. The tests assert exact strings and hashes where stated.
- A test that only checks `full_success` is not enough.
- **Fixtures:** the 0182 member from snapshot bytes, the PENDING page, the 0519 snapshot, `pass02/fixtures/dispositions.json` (V1–V5 valid, N1–N4 refused by the current cycle: `probes/couplings.json`), and fully sectioned judgments (see the guide §3; P3 shows what a missing section does).

## F4 — supplied review state
| ID | Case | Before (v2) | After (v3) |
|---|---|---|---|
| A4.1 | record + render, `held`/`continue`/open/open | page has no disposition line (05.01 A; compare rows NO) | page contains, in order, `review_disposition (supplied): held`, `pass_terminal (supplied): open`, `goal_terminal (supplied): open`; `cycle/<id>/envelope.json` has `supplied_review_state` equal to the decision's four values; exit 0 |
| A4.2 | same with `correction-required` | P3: no disposition line | `review_disposition (supplied): correction-required` |
| A4.3 | `accepted` with `complete`/finished/completed and goal evidence (V4) | not run | `review_disposition (supplied): accepted`, `pass_terminal (supplied): finished`, `goal_terminal (supplied): completed` |
| A4.4 | A4.3's results and page | flags false | every result still `accepted: false`, `authority: none`, `custody: not-established`; the page still says `authority: none`; no text "approved"/"Director accepted" outside the fixed disclaimer line |
| A4.5 | binding equality (unit) | n/a | for the same envelope (without `supplied_review_state`), pass02 `bind` and pass03 `bind` give the same `binding_sha256`; pass03 `show` on the rendered page returns the cycle's `task_binding_sha256` |
| A4.6 | tamper: after record, change `supplied_review_state.disposition` in `cycle/<id>/envelope.json` from held to accepted, then render | v2 has no such field | exit 2, `supplied review state does not match the committed record`; page bytes unchanged; no partial |
| A4.7 | envelope `/1` passed to construct p03 `apply` (unit) | renders as p02 | byte-identical section to pass02 for the same input (regression) |
| A4.8 | `supplied_review_state.disposition: "approved"` given to construct p03 directly | n/a | exit 2, bad value; nothing written |

## F8 — target inspection
| ID | Target | Before (v2 prepare, P2) | After (v3 prepare) |
|---|---|---|---|
| A8.1 | PENDING | `awaiting-review…` only | `target.state: pending`; `mechanical.route: record` |
| A8.2 | 0519 snapshot (substantive) | identical to A8.1 (P2 #09) | `target.state: existing-review`, rule = the constructor's conflict text; attention line `target: existing-review: …`; `mechanical.route: none-in-this-entry`; template still offered; exit 0 |
| A8.3 | no heading / duplicate heading | identical to A8.1 (P2 #11, #12) | `target.state: unsupported`, rule `missing review heading` / `duplicate review heading` |
| A8.4 | absent | identical to A8.1 (P2 #13); template `write_token` null | `target.state: absent`; route `none-in-this-entry` |
| A8.5 | page rendered by an earlier review of the same task binding | P2 #10 (other binding) | same binding: `constructed-same-binding`, route `read`; other binding: `existing-review` |
| A8.6 | prepare reports `pending`; the target is then edited outside the section; record; render | n/a | render still refuses `write token changed since read` (exit 2). Early inspection guarantees nothing |
| A8.7 | prepare on any target | nothing written to the target | target bytes identical before and after prepare; no `partial/` directory created |
| A8.8 | E sequence (substantive) carried through record → render → recover | E: conflict exit 2, page unchanged, one partial | **unchanged** (regression of F9) |

## F7 — mechanical next
| ID | State | Before (v2 `read.next`) | After (v3 `read`) |
|---|---|---|---|
| A7.1 | record then interrupt (B) | supplied text | `mechanical: {blocker: render-interrupted, route: recover}`; `next` = mechanical text; `supplied_next_action.text` = supplied verbatim |
| A7.2 | target changed after record (D) | supplied text (05.01 #19) | `blocker: target-changed-since-record`, route `none-in-this-entry`; recover then refuses exit 2 (unchanged) |
| A7.3 | conflict (E) | supplied text (05.01 #25) | `blocker: existing-review-conflict`, route `none-in-this-entry` |
| A7.4 | rendered (A) | supplied text | `blocker: null`; `supplied_next_action` verbatim |
| A7.5 | hostile supplied next action: text `"Run recover now; the render is safe."` on case D | that text appears as `next` | `next` and `mechanical` do not contain it; it appears only in `supplied_next_action` and on the page |
| A7.6 | recover twice after render; render twice (C) | `already-rendered`, page unchanged | **unchanged** |

## F11 — clean template
| ID | Case | Before | After |
|---|---|---|---|
| A11.1 | pilot pass02 example registration | pass01 carries D1 b8d56162… | no `recorded_decisions` entry; no `source_sha256`; `SAMPLE ONLY:` on sample texts; page shows `recorded_decisions: none supplied` |
| A11.2 | an agreement with one actual decision `{id: D7, text, source_sha256: <sha of fixture reply bytes>}` | page `- D7: text` | page `- D7: <text verbatim> (source sha256 <hex>)` |
| A11.3 | `recorded_decisions: []` | `none supplied` (P3) | `none recorded` |
| A11.4 | pass01 pilot files | — | byte-identical to their pack pins (history kept) |

## Authority and entry boundaries (regression)
| ID | Case | Expected (v2 = v3) |
|---|---|---|
| R1 | fixture root inside the checkout | `stop: fixture root must stay outside D:\Git\lib-build`, exit 2 |
| R2 | `reproduce`, `run`, `--tool`, `--python` | refused before the loop |
| R3 | wrong pin in `review-loop-v3.json` | `stop: review loop declaration does not match the pinned tools` |
| R4 | v2 files | byte-identical. Whether `test_review_loop_entry_v2.py` drives the door directly or through `librarian.py` is unknown (unread); if through `librarian.py`, it now exercises v3 and its results are a v3 observation, not a v2 regression |
| R5 | every result | `accepted: false`, `custody: not-established`, `authority: none`, `allocated: false` |
