# 05.01 return — 0702.desk-state-review

## Identity

Grok 4.7, published by xAI, in the Grok Build session `01a17dfa-bc23-7730-bec3-c49938f96187`, on 2026-10-29. Role: Grok Builder 2 acting as Colab. Submission `grok-2-0702-0501`. Reviewer: Codex Prime. Investigation: `00.00.10.work/0702.desk-state-review` pass 05.01.

Prior involvement: I wrote `labs/desk-state-pass01` and the historical Builder return captured as `0152.desk-state-view-0519`. `snapshots/0009.blob` already says that a further Colab from that author is informed self-critique. This return is that critique. Findings come from the package snapshots. Recollection is not evidence. I do not certify the lab as independently proven.

Authorization recorded for this contextual review: “The Director authorizes this contextual review.” The pack and the preparation notes supply no `reply:` lines. This sentence authorizes the review. It does not adopt the lab.

## Inputs actually read

Package `00.kernel/00.00.10.work/0702.desk-state-review/package05.01` at manifest commit `a8b2c590e46f5068c8bc19d6f6174296375ee1b6`. I hashed all 11 snapshots against `source-manifest.json`. Each digest and length matched.

Opened in full, or by structured extraction where the file is large:

- `ENTRY.md`, `05.01.pack.md`, `06.01.notes.md`, `source-manifest.json`, `templates/05.01.return.TEMPLATE.md`
- `snapshots/0001.blob` CONTRACT.md, target blob `fa9aec930ddafdc4f7920e5d257bb634edc7a9f239ef41dd477a839a72959f0a`
- `snapshots/0002.blob` historical return
- `snapshots/0003.blob` `desk_state.py`
- `snapshots/0004.blob` tests, read and not executed
- `snapshots/0005.blob` README
- `snapshots/0006.blob` `desk.json`
- `snapshots/0007.blob` MIGRATION.md
- `snapshots/0008.blob` `rehearsal.json`
- `snapshots/0009.blob` PRIME-INTAKE.md
- `snapshots/0010.blob` DECISIONS.md
- `snapshots/0011.blob` `0412.prime-review/01.md`
- `evidence/INTAKE.md`
- reserved `0168.desk-state-colab-0501/01.md` and `reservation.json`

`prime_brief.py` is not in the package. I did not open it. I did not open live module files, other workers’ unfinished files, Claude’s benchmark, or the Grok-1 assembler.

## Answer

The contract and the JSON view can give Prime a faithful bounded view of one authored historical record. They do not give a current desk, and the default readable brief still drops the source of the most current-sounding sentence.

On the supplied specimen the protective distinctions hold in the data. Accepted reviews with `terminal: null` are `open-accepted-not-terminal`. The held review stays `open-held` with its follow-up. The unidentified legacy page stays `unprojected`. Every worker is null and means `unrecorded`. `elected` is null. Exit is 1 because attention and unknowns are visible. `completed_fixtures` is empty. Citation blobs that were read are `match` or they would be unknowns. A later Director hold that is not in the record is left untouched.

The smallest useful corrections are in the readable surface and in citation attachment:

- Print the handoff’s kind, author, and evidence commit with the statement.
- Copy the supplied review’s `disposition` and `terminal` onto the lane beside the derived lifecycle.
- Keep each citation’s own note when two citations share a path and commit.
- Name the path on an unprojected return row that has no batch id.
- Label member `captured_at` separately from a live-file observation time.
- State, on the readable view, that decisions absent from the record stay unresolved.

Those corrections are proposals. This pass does not apply them. No score is assigned.

## Cases

C01. A reader who uses the lifecycle cannot honestly call the historical accepted lanes finished. A reader who copies only the task sentence, or only the word Accepted inside the raw review text, still can.

Record authorship in `snapshots/0006.blob`: coordination for `0508.return-capture/05.18` and `0504.app-entry/05.20` has `disposition: accepted` and `terminal: null`. The lane tasks say “Accepted as that correction only.” and “Accepted within that backend scope only.” Those sentences are copied onto the view by `lane_row`. They are not a completion calculation.

Derived fact in `snapshots/0008.blob`: both lanes have `lifecycle: open-accepted-not-terminal` and attention “accepted without an explicit terminal declaration”. `returns.other_open` carries them. `returns.completed_fixtures` has length 0. `returns.correction_or_held` carries `0507.prime-support/05.12` as `open-held` with follow-up `0507.prime-support/05.13`. `elected` is null. The stored exit is 1.

The lane object does not itself repeat `disposition` or `terminal`. Those fields remain on the desk record and inside `raw.brief.projection.batches[].facets.review`, where `terminal` is null. The same facet also stores `binding_check: current` and `status: bound`. The readable reconstruction does not print `binding_check`. A consumer of the raw JSON can still treat the token `current` as present-tense authority. This package does not include the brief source, so this return does not define that token. It records that the token sits beside `terminal: null` and that desk-state does not clear it.

`snapshots/0004.blob` `test_accepted_terminal_and_commit_basis` asserts three different lifecycles for accepted work: `open-accepted-not-terminal`, `completed`, and `open-commit-custody-unverified`. That assertion was read. It was not run.

C02. A null worker stays unrecorded. An absent lane is omitted. An old handoff can still be read as a current assignment when the reader sees only the default text.

Source of the worker claim: `snapshots/0006.blob` sets `worker: null` on all four lanes. `snapshots/0003.blob` `lane_row` sets `worker_meaning` to `unrecorded` when the worker is null, and to `label` when it is a string. `render_text` prints `worker unrecorded`. The reconstructed text from `snapshots/0008.blob` does not contain the word `available`. `snapshots/0005.blob` states the same rule. `snapshots/0004.blob` `test_two_lanes_and_unbound_source` asserts a null worker is `unrecorded` and that the lane JSON does not contain `available`. That test was not run.

Source of an absent lane: the view iterates `doc["lanes"]` in record order. A lane that is not in the record is not invented. The specimen has four lanes. No fifth lane appears.

Source of the handoff: `snapshots/0006.blob` `handoff.author` is `Codex Prime`. The statement is the Prime sentence beginning “Next work is one final prepared test bundle”. Its evidence cites `RECONCILIATION.md` at commit `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841` with the note “Recorded Prime intent. Not a new instruction from this module.” `snapshots/0003.blob` sets `handoff.kind` to `recorded-prime-intent` and copies the statement. The JSON view keeps author, kind, and evidence. `render_text` prints the heading “Recorded next step” and the statement only. The reconstructed text does not contain `Codex Prime` or `recorded-prime-intent`. The sentence is present tense and has no age. That is the path on which an old recorded intent becomes a current-sounding assignment.

C03. A gap that the record and the brief already name stays visible. A later decision that was never supplied is neither resolved nor announced. Shared citations can lose the second note.

Source basis of the specimen: every page in `snapshots/0008.blob` `sources` is `kind: git-blob` at commit `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841`. The three identified coordination hashes equal the observed page hashes: `05.18` `314f96a4b87b35e0bb5f8a2c1a85f42a6eb0fac42c7a264f7e691baf741b5395`, `05.20` `76b18077d9e57935aa661f018d7fae27469206c524e882cd424cb0a5f054669b`, `05.12` `dce336e1f4c3cd8d4679ddff45f517293b2e6fd991d8bb39560c0412f1f5f3f5`. This specimen therefore does not demonstrate a stale source hash. The contract says a different `source_sha256` is passed through and left unprojected, and that the module does not rewrite the hash. The implementation sends the coordination object to the brief and copies an unprojected reason when the brief returns one. `test_missing_partial_retrospective_ambiguous_and_stale` expects lifecycle `unprojected` and the reason text “different source sha256”. That test was not run, and the brief implementation is outside the package.

A missing blob is specified as `observation-failed` with `source: null` in `test_malformed_paths_pins_failure_and_output`. The specimen’s own missing-page case is the unidentified `0401.goal/06.01.md` and `00.kernel/00.live.md`: reader exit 1, no book/page/batch, lifecycle `unprojected` for the lane, and both paths listed in `unknowns`. `00.live` legacy citation status is `match` at the declared commit. The note calls it a stale mirror and says it is not an input. The module’s protected paths include `00.kernel/00.live.md`.

Observation time: `projection.projected_at` is `2026-10-29T16:25:06.082906Z`. `live_times` are inspection `captured_at` values `2026-10-28T18:28:40.563826Z`, `2026-10-28T18:37:49.618537Z`, and `2026-10-28T00:36:15.423334Z`. No page is a live file, so none of those stamps is a live-file observation. The candidate heading “Live observation times” would present capture times under that name. The contract says a repeated view may differ in `projected_at` while lane decisions and citation bytes stay put. Inspections in the specimen have `retrospective: false` and report status `complete`. That is custody of the named members at those capture times. It is not a statement that the pages are the live desk.

Later decision: `snapshots/0010.blob` records AR-01, “Hold until race is addressed”, and says those answers authorize no new execution, release, test-run, or deployment. The desk record does not cite that file. `returns.conflicts` is empty. The view does not invent a clearance and does not mention AR-01. The goal statement, which the readable view does print, says that passing the snapshot test does not recover all current work. Silence is the preservation of an unsighted decision. A morning reader who stops at the handoff sentence will not see the hold.

Citation attachment: `citations_for` returns the first citation with the same path and commit. Goal evidence and handoff evidence both cite `RECONCILIATION.md` at `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841`. Both raw reads match hash `cea41365e952d38e179a2e512aff8eba3ed7f8605197b3c8940c5b1ca2defa94`. `view.handoff.evidence[0].note` is the goal note, “Prime reconciliation. Proposed final-exam binding, not an execution release.” The handoff note remains only in `raw.citations`. The view substitutes one authored note for the other. In this specimen the hashes agree, so no unknown is raised. Two citations of one path with different hashes would still show the first hash on the handoff object.

C04. The specimen reduces retyping of observations the tools already return. It moves the judgment into the record, which Prime or a builder still has to author.

Still supplied by hand in `snapshots/0006.blob`: the goal, the milestone, four task sentences, the D1 statement, the handoff statement and author, coordination release/claim/review/publication, tool pins, bounds, custody mode, the uninspected labels, and the legacy note. `snapshots/0002.blob` says those carried fields were not retyped for the render. That claim matches the copy in `assemble`.

The view adds, from the historical run stored in the rehearsal: five reader observations, three inspection reports, six citation reads, brief lifecycles, attention, and unknowns. Prime does not have to reconstruct those tool results from scratch if the rehearsal is trusted as a historical capture. Trusting it still requires the record hash `18d44923dfc0995c2d9078ba6d2b36807a0c98fb19ff3840ee1386ddee4b8933` and the source commit above. This Colab did not regenerate the view.

Smallest useful adoption check, proposed and not performed: at one named commit, compare a captured `view.json` with the desk record. Confirm `record.sha256` equals the record bytes. Confirm each accepted lane with `terminal: null` is `open-accepted-not-terminal` and is absent from `completed_fixtures`. Confirm a null worker renders `unrecorded`. Confirm a mismatched citation or a different `source_sha256` stays unknown. Confirm the readable handoff line names author, kind, and evidence commit. Confirm `00.kernel/00.live.md` is unchanged. `snapshots/0007.blob` already requires a later adopted reader to be checked against the record hash and the source cuts, after Prime review and a Director decision. This check adds the discriminating rows. It does not authorize a backend repair, a live rewrite, or fixture execution. AR-01 remains.

## Actual operations

Read the package files listed above. Verified 11 of 11 snapshot hashes and lengths with a local Python hash of the blob bytes. Parsed `desk.json` and `rehearsal.json`. Compared coordination hashes to observed source hashes by equality. Reconstructed the default readable view by applying the `render_text` rules in `snapshots/0003.blob` to the stored view object. Counted seven `def test_` methods in `snapshots/0004.blob`.

Read `0168.desk-state-colab-0501/reservation.json`: schema `return-capture/1`, submission `grok-2-0702-0501`, submitter “Grok Builder 2 acting as Colab”, reviewer Codex Prime, expected output the recipient notes path. The member directory held `01.md` and `reservation.json` before intake.

Did not execute `desk_state.py`, `test_desk_state.py`, `batch_observe.py`, `return_inspect.py` against the specimen, `prime_brief.py`, `state_projection.py`, held app fixtures, or race probes. Did not edit a source page, the package, `00.live`, or the module. Did not write Git. The historical “7 passed, exit 0” line in `snapshots/0002.blob` and `snapshots/0008.blob` is self-reported by the original run. It is not a result of this pass.

Custody of these bytes is the reserved intake and fresh verify specified in `evidence/INTAKE.md`. That custody step is not a re-execution of desk-state. A receipt, when the command completes, records these bytes. It does not change these findings.

## Hostile

Failing path: default stdout, reconstructed from the specimen, under “Recorded next step”.

First misleading sentence: “Next work is one final prepared test bundle and Director-led trial, with schema ambiguities resolved above. Director must launch/name the actual fresh session; no identity is invented by compute or this review.”

The sentence is true as a copied Prime statement at commit `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841`. The heading does not say whose statement it is, which commit it cites, or that the kind is `recorded-prime-intent`. A morning reader can take it as the module’s current assignment.

The first misleading lane sentence is the task “0508/05.18 planning correction captured in 0150. Accepted as that correction only.” The line above it says `open-accepted-not-terminal`, and the following attention line says there is no explicit terminal declaration. A reader who copies only the task can drop both qualifiers. The raw review text begins “Accepted as the bounded CP-01/CP-02 planning correction” and later says it is not a current-work handover. That longer text is protective when read whole, and it is buried in `raw`.

Missing relationship: `lane_row` does not carry the supplied `terminal` value; `render_text` does not carry the handoff author; `citations_for` does not carry the second note; the Returns renderer prints `(no page)` when `id` is null even though `unknowns` still has the path.

Protective rule that blocks a convenient current desk: the goal statement says this snapshot does not recover all current work, settle D1, replace Prime, or hand over authority. Overflow, a pin mismatch, a raised bound, and a write onto `00.kernel/00.live.md` or `0401.goal/06.01.md` refuse. A missing blob stays `observation-failed`. A stale `revise --expected` hash refuses and leaves the record in place. Those blocks are the contract working. They stop this pass from turning the historical record into today’s authority. `snapshots/0011.blob` also says complete is not automatic closure from green tests, and that the desk-state return is unreviewed and not a dependency.

## Factfind

F01. `snapshots/0003.blob` `render_text` prints `view["handoff"]["statement"]` and does not print author or kind. Observation: the reconstruction from `snapshots/0008.blob` lacks both. Proposed test: readable stdout for this record contains `recorded-prime-intent`, `Codex Prime`, and commit `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841` on the handoff.

F02. `snapshots/0003.blob` `citations_for` matches path and commit and returns the first row. Observation: `view.handoff.evidence[0].note` equals the goal note, while `raw.citations` still holds “Recorded Prime intent. Not a new instruction from this module.” Proposed test: two same-path citations with different notes remain distinct on the objects that cited them.

F03. `snapshots/0006.blob` review `terminal` is null for the two accepted batches. `snapshots/0008.blob` stores `open-accepted-not-terminal`, empty `completed_fixtures`, and `elected: null`. Proposed test: the existing `test_accepted_terminal_and_commit_basis`, re-run by Prime, plus an assertion that `binding_check: current` with `terminal: null` does not set `elected` and does not enter `completed_fixtures`.

F04. `snapshots/0006.blob` and `snapshots/0008.blob`: four lanes, each `worker: null`, each `worker_meaning: unrecorded`. Proposed test: the existing assertion that lane JSON does not contain `available`, extended to the readable text.

F05. `snapshots/0008.blob` `returns.unprojected` has two items with `id: null` and the same reason. Reconstruction prints `(no page)` twice. `unknowns` names `00.kernel/00.00.10.work/0401.goal/06.01.md` and `00.kernel/00.live.md`. Proposed test: each readable unprojected row includes that path.

F06. `snapshots/0008.blob` `live_times` are three `captured_at` stamps. Every `sources[].kind` is `git-blob`. `snapshots/0003.blob` `candidate_text` headings call that list “Live observation times”. Proposed test: a git-blob-only record labels those stamps as capture times.

F07. `snapshots/0010.blob` AR-01 is absent from `snapshots/0006.blob` and from `returns.conflicts`. Proposed observation: adding no citation of DECISIONS.md leaves conflicts empty and does not produce a clearance sentence.

F08. `snapshots/0003.blob` passes coordination through and copies the brief’s unprojected reason. It does not compare `source_sha256` itself. The specimen’s three hashes match, so the stale branch is unshown. `snapshots/0004.blob` expects “different source sha256” to stay `unprojected`. Proposed test: Prime runs that one fixture only if a later adoption review authorizes it. This pass does not.

F09. `snapshots/0004.blob` refuses `bounds.max_sources` of 100 and `max_source_bytes` of 20 with exit 2. `source_count_overflow` refuses before further launch when the declared count exceeds the bound. The specimen is inside the bounds: 5 pages, 3 members, 6 citation reads, view well under the output cap. Proposed observation: a declared source past the cap yields `refused:` and no view. Already asserted for a raised cap. Not re-run here.

F10. `snapshots/0008.blob` command list is five `batch_observe.py observe` calls, three `return_inspect.py inspect` calls, and one `prime_brief.py brief`. That matches the historical return’s “5 reader calls, 3 member inspections, and 1 brief” as a count of stored commands. It is evidence of what the rehearsal recorded. It is not a fresh execution.

## Pack and tool defects

No pack defect found. Eleven snapshots matched `source-manifest.json` schema `prime-pack-sources/1`, commit `a8b2c590e46f5068c8bc19d6f6174296375ee1b6`, repository `workshop`.

`05.01.return.md` and `06.01.review.md` are absent from the package, as ENTRY says. The reservation and intake instructions were present.

Tool limits, separate from the design findings: this Colab was not authorized to run desk-state or its backends. The brief implementation is not a package snapshot, so the meaning of `binding_check: current` and the stale-hash comparison inside the brief were not confirmed from brief source. Independent adoption remains Prime’s later review. Network was not used.

## Overflow

The projection note stored on the specimen is “not a v1 assignment record and not canonical”. The projection authority string is “none; a projection grants no release, acceptance, seat or work”. Those strings support the contract and are easy to miss because they sit under `raw`.

`0401.goal/06.01.md` is both a page and the lane `legacy-assignment`. `00.kernel/00.live.md` is a page and the legacy citation, and it is not a lane. The readable unknowns repeat the unidentified-page reason once per path and again for the lane. The repetition is noisy and still does not invent a batch id.

`revise` is a guarded record write. The README says the new file is not a worker command. The specimen command is `view`, not `revise`.

`snapshots/0011.blob` places 0412 as design, says compute does not infer approval, and says Colab outputs and the desk-state return are unreviewed. That agrees with `snapshots/0009.blob`: publication of return 0152 verified custody and did not accept the lab.

The package commit and the specimen commit differ. Using `a8b2c590e46f5068c8bc19d6f6174296375ee1b6` as if it were the desk’s source basis would be a mistake. The desk pages name `5d7f15b6b205d3aed6afbcb0b1263a4bc3e44841`.

## Unprompted

Add the source kind and commit to each readable lane line. The JSON already stores them on `lane.source`. The default text shows the record hash and not the git commit, so a reader can mix the pack cut, the record hash, and the page commit.

Refuse a readable banner that promotes `binding_check: current` into election or completion. Leave the token inside `raw` until the brief’s meaning is reviewed with the brief source.

Investigate, at adoption and not here, whether two citations of one blob with different expected hashes can show `match` on the attached evidence while `unknowns` reports the second read. The specimen’s duplicate hashes agree, so that failure is a code path, not a demonstrated specimen result.

Cut nothing that refuses a pin mismatch before launch, a write to `00.live`, or a view that would have to drop a required fact to fit the cap.

## Director replies

none

## Limits

This return does not establish independent proof of the seven tests, current worker availability, current desk status, adoption, seating, publication, or a clearance of AR-01. It does not regenerate `rehearsal.json`. It does not change any page. A receipt for member `0168.desk-state-colab-0501` is custody of this submission. Prime reviews the result. The pack Return pointer and `## Review — Codex Prime` stay for Prime.
