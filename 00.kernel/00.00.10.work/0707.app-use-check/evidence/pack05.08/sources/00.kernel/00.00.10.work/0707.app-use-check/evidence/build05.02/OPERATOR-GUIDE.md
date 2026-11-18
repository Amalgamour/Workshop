# OPERATOR-GUIDE — review-loop entry
guide version: 1 · applies to: review-loop entry **v2** (current, `app/review-loop-v2.json`). §8 lists the **proposed v3** differences.
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · state: proposed guide for Codex Prime; every rule cites the source that enforces it

This guide is for writing a supplied review of a captured return through `app/librarian.py review-loop`. A completed command is not approval. Every result says `accepted: false`, `authority: none`.

## 1. Book layout (a disposable fixture root)
The fixture root must be an existing absolute directory outside `D:\Git\lib-build` and outside the live work book. It must not be a link or a UNC path (`review_loop_tools_v2.py` 190–212).

| Path in the book | What | Written by |
|---|---|---|
| `<member>/` | the captured return, copied byte for byte (receipt, reservation, manifest, return, payload) | you; check the copy against its pins |
| `<page>/<batch>.md` | the **review target**, at the path derived from the descriptor's `origin` (for 0182: `0519.desk-app/05.01.md`) | you |
| `descriptor.json` | the `descriptor` object from `describe-legacy` stdout, unchanged | you |
| `registration.json` | `prime-cycle-registration/2` (§2) | you |
| `request.json` | `{"schema": "review-loop-request/1", "registration_path": "registration.json"}` (exact keys: `review_loop.py` 177–188) | you |
| `assignment.txt` | the assignment text the review answers; it becomes a hashed source row | you |
| each `registration.evidence[].logical_path` | the supplied evidence files; each becomes a source row | you |
| `decision.json` | your filled decision (§3) | you |
| `cycle/`, `support/`, `scratch/`, `trace/`, `partial/` | the tools' own records | the tools |

**Target format.**
- Exactly one review heading line, `## Review - Codex Prime` (or the em-dash form; `construct.py` `HEADINGS`).
- Its section runs to the next `## ` heading.
- A new target's section must be `PENDING` or `PENDING.` (stripped).
- Anything else is an existing review, and render will refuse it (`compose` 784–843).
- **Check the section yourself before writing a judgment.** v2 `prepare` does not look at the target.

## 2. Registration: what is yours, what is sample
- **Agreement.** `agreement` is copied verbatim into your review's Agreement block.
- **Recorded decisions.** Put in `agreement.recorded_decisions` only actual decisions from the assignment page. Each is `{id, text, source_sha256}`, where `source_sha256` is the sha256 of the exact cited reply bytes (`prime_review.py` 441–445).
- **None to record?** Use `null`. It renders as `recorded_decisions: none supplied`.
- **Do not reuse the pilot.** The pass01 pilot's `example-registration.json` holds a sample D1 (b8d56162…) that belongs to that pilot. Do not carry it into a review.
- **Goal.** `goal.statement` is hashed into `goal_sha256`, which your judgment must repeat (`prime_cycle.py` 1302–1305). Prepare's template already holds it.

## 3. Filling the decision (`prime-cycle-decision/3`)
Start from `view.template` in `prepare` stdout. Fill three keys and leave the rest as they are.

**`attribution`**: `{actor_label, role: "prime", evidence}`. The label is not authentication.

**`judgment`** (the cycle checks it, `check_judgment` 1295–1333):

| Field | Allowed | Coupling |
|---|---|---|
| `outcome` | `continue`, `director-input`, `develop`, `complete` | `complete` ⇔ `goal.terminal: completed` |
| `disposition` | `accepted`, `held`, `correction-required` | `director-input` requires `held` |
| `pass_terminal` | `open`, `finished` | `held`/`correction-required` require `open` and `goal.terminal: open` |
| `goal` | `{terminal: open\|completed, goal_id, goal_sha256, evidence: [text]}` from the template | `completed` needs `disposition: accepted`, `pass_terminal: finished`, ≥1 evidence |
| `finding` | non-empty text | |
| `reasons`, `source_refs`, `unresolved` | lists of non-empty text | |
| `next_action` | null or `{action_id: LABEL, text, authorized_in_grant: true\|false\|null}` | |
| `semantic_conflict` | null or bool | |
| `design_fork` | null or object | |
| `holds`, `answers` | lists | |
| `sections` | the 24 keys from the template | per-outcome requirements below |

These couplings were checked against the current cycle on 9 synthetic fixtures (`build05.02/probes/couplings.json`).

**Required sections per outcome** (`prime_review.py` pass02, `complete_ready` 870 and the per-outcome block around 932–1000). If any is missing, the record is still committed, but the result is `effective: attention` and **exit 1** (probe P3):
- `continue`: `return_result`, `prime_finding`, `within_direction`, `next_bounded_action`, and a non-null `next_action`;
- `director-input`: `issue`, `consequences`, `options`, `recommendation`, `question`, `affected`;
- `develop`: `exploration`, `assumptions`, `open_questions`;
- `complete`: `outcome_evidence`, `limits`, `tests_note`, `learning`, `preservation`, `remaining_choices` (not null), and the finish-criteria checks that follow (`complete_ready` 870 onward).

**`supplied_record`** (`prime-review-record/1`; the cycle checks it, `align_supplied`/`align_sources` 1336–1400):
- `{schema, attribution, sources, agreement, holds, answers, review_passes, gaps, judgment}`.
- **`agreement`** must equal `registration.agreement`.
- **`judgment`** holds `{outcome, finding, reasons, semantic_conflict, design_fork, next_action: <text or null>, sections}`, equal to the decision judgment's fields. There is **no `disposition`** here: `prime_review` refuses unknown keys.
- **`sources`:** one row per assignment, per evidence path and per return. Each row has:
  - `bind: false`;
  - `content_sha256` and `content_bytes` of the file;
  - `transport_*` (the same values);
  - `prior_*: null`;
  - `record` (the file text);
  - `kind` (`page`, `supplied-text` or `capture`);
  - `identity`.
- **The return row's `identity`** is `{schema: "return-capture/1", member: <descriptor.placement.intended_target_page>, submission_id, receipt_sha256: <sha of the receipt bytes>, origin}`.
- A worked recipe is `colab/labs/0707.app-use-check/pass01/decide.py` (lab code, not a contract).

## 4. Commands, results and exits
| Command | Does | Success looks like |
|---|---|---|
| `describe-legacy --book ABS --member NAME` | reads the member; writes nothing | `state: complete`, a `descriptor` |
| `prepare` | reads the cycle state; writes `trace/` | `pass_state: awaiting-review`, `view.template` |
| `record --decision REL` | validates and commits `cycle/<review_id>/` | `record.result: recorded`, `pass_state: render-pending` |
| `render` | writes the review section into the target | `render.result: rendered`, `pass_state: reviewed` |
| `read` | reads the state | `pass_state: reviewed`, `render_state: rendered` |
| `recover` | see §6 | as render |

**Exits:**
- **0:** done.
- **1:** done, but `prime_review` returned attention. Read `effective` and the page's `#### Attention`.
- **2:** refused. `stop:` on stderr is the app door; `refused:` is the loop or its tools; nothing is written, except a partial on a render conflict.

`full_success` is per command: `record` reports true while the page is still pending.

## 5. Recovering your judgment in a new process
1. `read` names `current.latest_review.directory` and `current.latest_review.record_sha256`. `read`'s `supplied_judgment` is always null.
2. Open `<directory>/record.json`, check that its sha256 equals that `record_sha256`, and use `record.decision`.
3. **The page's `record_sha256:` line is a different file:** `support/<review_identity>/record.json`, the supplied record. Do not compare it with the cycle hash.

## 6. What `recover` means
`recover` retries rendering of **the same committed review** against an **unchanged** target.
- After an interrupted render it renders.
- After a render it reports `already-rendered`.
- After a render conflict it reports `render-conflict` again.
- It does **not** repair a target that changed after record (`write token changed since read`, exit 2), and it does not replace an existing review.
- This entry has no supersession route. The template's `supersedes` and `recovers` keys are not an operator procedure here.

## 7. Reading a blocked state in v2
`read.next` shows the supplied judgment's next-action text even when the pass is blocked. Decide from `pass_state`, `render_state` and the two write tokens instead:

| `render_state` | tokens (`view.write_token` vs `view.latest_review.write_token`) | Meaning | Do |
|---|---|---|---|
| `pending` | equal | render was interrupted | `recover` |
| `pending` | different | the target changed after record | stop; no route in this entry |
| `conflict` | — | the target holds another review | stop; a successor process is required; the judgment is kept |
| `rendered` | — | done | `read` |

## 8. Proposed v3 differences (not in force)
- **`prepare`** reports `target.state`: `pending`, `existing-review`, `constructed-same-binding`, `absent` or `unsupported`. It comes with an attention line and `mechanical.route`. Check it before writing a judgment.
- **The page** shows `### Supplied review state`: disposition, pass_terminal and goal_terminal, labelled supplied and not acceptance.
- **Results** carry `mechanical {blocker, route, text}` and `supplied_next_action` separately. `next` is mechanical only, so §7's manual table is no longer needed.
- **Recorded decisions** render with their source sha256; `[]` renders as `none recorded`.
- **A clean example registration** with no sample D1 ships in `labs/prime-entry-pilot-pass02/`.
