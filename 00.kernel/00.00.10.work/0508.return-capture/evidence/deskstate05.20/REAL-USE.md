# Real use — desk-state preservation, 05.20

Date: 2026-10-29. Recorder: Grok Builder 2. This file records the specimen generated after the citation repair. It does not adopt the module.

## Source revision

The view reads the original record `00.kernel/00.00.10.work/0508.return-capture/evidence/deskstate05.19/desk.json`. That file is SHA-256 `18d44923dfc0995c2d9078ba6d2b36807a0c98fb19ff3840ee1386ddee4b8933`, 10117 bytes, schema `desk-state/1`. Every page and citation in it is a git blob at commit `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841`.

`evidence/pack05.20/source-manifest.json` has no commit field. Workshop HEAD when this evidence was written is `377da29cc689f32175541cc0ac82964eea26b06a` on `workshop`. That HEAD is the workshop tip at this check. The specimen source commit remains `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841`.

The command did not pass `--out` or `--candidate`. Those paths resolve under the record's output root, `evidence/deskstate05.19`. Stdout was saved as `evidence/deskstate05.20/view.json`. `VIEW.md` is `render_text` of that same object. `candidate.md` is `candidate_text` of that same object. `candidate.md` stays beside the capture. It is not an argument of the capture command.

```text
python -B labs/desk-state-pass01/desk_state.py view --input D:\Git\lib-build\00.kernel\00.00.10.work\0508.return-capture\evidence\deskstate05.19\desk.json --json
```

The process exited 1. The view field `exit` is 1. That is the attention and unknown exit. `elected` is null. Projection time is `2026-10-29T22:38:50.320662Z`. The historical rehearsal clock remains `2026-10-29T16:25:06.082906Z`.

## What changed in the projection

Compared with `rehearsal.json` from 05.19:

- Lifecycles stay `orientation-correction` `open-accepted-not-terminal`, `capture-handoff` `open-accepted-not-terminal`, `projection-held` `open-held`, and `legacy-assignment` `unprojected`.
- Attention lists match. Unknown lists match. `completed_fixtures` is empty. `conflicts` is empty. `elected` is null.
- The handoff evidence note is `Recorded Prime intent. Not a new instruction from this module.` The 05.19 rehearsal had attached the goal note to that handoff. The goal evidence in this view still carries `Prime reconciliation. Proposed final-exam binding, not an execution release.` Both rows match expected hash `cea41365e952d38e179a2e512aff8eba3ed7f8605197b3c8940c5b1ca2defa94`.
- Each lane carries `review_binding`. The two accepted lanes say terminal null and stay open. The held lane says held and terminal null. The legacy lane has no supplied review.
- `live_times` is absent. Projection time, custody `captured_at`, and live-file observations have separate labels. Live-file observations are none.
- Both readable surfaces name `00.kernel/00.00.10.work/0401.goal/06.01.md` and `00.kernel/00.live.md`.
- Both surfaces print handoff kind `recorded-prime-intent`, author `Codex Prime`, and the evidence commit with the statement.
- Coverage says a decision absent from the record is unexamined, and that an empty conflicts list is not a global clearance.

The historical specimen has no conflicting expected hash. The conflicting-hash case is the unit test `test_citations_for_binds_each_note_and_expectation` and the disposable view `test_view_preserves_citation_notes_and_names_unidentified_paths`. In that test the mismatch stays on the conflict row.

## What Prime still authors

The record still supplies the goal, the milestone, the four task sentences, the D1 statement, the handoff statement and author, coordination, pins, bounds, custody, uninspected labels, and the legacy note. This render copies those sentences. D1 stays unresolved inside the record.

## Files this view did not examine

`00.kernel/00.00.10.work/0412.prime-review/evidence/drift-audit-2026-10-29/DECISIONS.md` is SHA-256 `91c6c7a8c1759d3f35c1455df8df3f137b1b6154e382d1742b6f7e3f52eee739`, 671 bytes. AR-01 stays in that file. The view does not read it and does not insert it. The record's uninspected labels still say Claude's active 0507/05.16 outputs and the SoF repository were not opened.

## Bytes that stayed

These files match the hashes recorded before the repair:

- `00.kernel/00.live.md` `a69245972915b6e140b7528239216ff1a1bc97941cfb1a4de4868d88a541a30d` 1160
- `00.kernel/00.00.10.work/0401.goal/06.01.md` `3578934451fc98e1dcfcc0030adebad27478787c4c2b6177f82268ae6826c38c` 545
- `evidence/deskstate05.19/CONTRACT.md` `fa9aec930ddafdc4f7920e5d257bb634edc7a9f239ef41dd477a839a72959f0a` 9214
- `evidence/deskstate05.19/desk.json` `18d44923dfc0995c2d9078ba6d2b36807a0c98fb19ff3840ee1386ddee4b8933` 10117
- `evidence/deskstate05.19/rehearsal.json` `add4732d618e206f5cda2d54ac669b0cd3b95fd58bbe7b94f2063918dade838f` 113221
- `evidence/deskstate05.19/00.live.candidate.md` `595fb5d45835a4073166bb52bb44f11e7f5185c33f9dbf5f34136d2c22b9a5ca` 3505
- `evidence/deskstate05.19/MIGRATION.md` `120dd41dd060d3de66fb20c5a44bcaefce1301b12309198e9c049df91255dd7e` 1737
- `evidence/deskstate05.19/submission.md` `184b30c42a555eac29ee6f78c6b61c9ba94683d1e16cab999459a45d4102c5d9` 1566
- `DECISIONS.md` as cited above

## Commands inside this view

`raw.commands` has 9 entries: 5 `batch_observe.py observe` calls, 3 `return_inspect.py inspect --member` calls, and 1 `prime_brief.py brief`. The inspected members are 0150.cold-prime-plan-revision-0518, 0149.capture-handoff-entry-0520, and 0136.state-projection-0512. The 05.19 rehearsal also recorded 9 commands. Both counts describe this record's shape. Neither count is a measured saving of time.

## Tests read and run

Command, from `D:\Git\lib-build`:

```text
python -B -m unittest labs.desk-state-pass01.tests.test_desk_state
```

Result on 2026-10-29: 9 tests, 15.022s, exit 0, 0 failed, 0 skipped. The link test created a file symlink and the view refused it with exit 2. The historical 05.19 self-report of 7 passed stays that pass's report.

`test_citations_for_binds_each_note_and_expectation` calls `citations_for` in process. Matching hashes with distinct notes stay distinct objects. A conflicting expected hash stays a mismatch on its own row. Two identical notes consume two reads in order.

`test_view_preserves_citation_notes_and_names_unidentified_paths` runs one disposable `view`. The goal note stays on the goal object. The handoff note is the handoff note. The wrong expected hash stays a mismatch. `notes/plain.md` is named. Both text surfaces omit the goal note, omit `(no page)`, and print the three time headings.

`test_accepted_terminal_and_commit_basis` checks terminal null against terminal completed, a null worker, and the absence of `live_times`. `test_missing_partial_retrospective_ambiguous_and_stale` checks that a stale source stays `not-applied` and names its path.

## Read-back

`VIEW.md` is 5550 bytes, SHA-256 `3b33219111a1da09c832b61a19716ea87f2818949d3407b50565313a306419e5`. `candidate.md` is 5063 bytes, SHA-256 `4ec2f14a2027be18862c2235fe3ecc80a019b186afbd45507e08eeeecb22461f`. Both were read in full before capture. `view.json` is 108342 bytes, SHA-256 `e1a18c162c04015d208abbd7cacf4af971939a2b23e207b0e1e1f2f5f87d39cb`.

## Adoption check

At commit `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841`, compare the captured `view.json` record hash `18d44923dfc0995c2d9078ba6d2b36807a0c98fb19ff3840ee1386ddee4b8933` with `desk.json`. Accepted lanes with terminal null stay `open-accepted-not-terminal` and stay out of `completed_fixtures`. A null worker renders unrecorded. A mismatched citation stays on its own object. The readable handoff names author `Codex Prime`, kind `recorded-prime-intent`, and evidence commit `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841`. `00.kernel/00.live.md` stays byte-identical. The check uses the captured view. It leaves backends, `00.live`, and held fixtures untouched. This pass does not perform that check as adoption.
