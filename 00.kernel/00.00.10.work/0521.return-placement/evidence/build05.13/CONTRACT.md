# 05.13 successor command contract

schema: connected-return-review-contract/0513
written: before any driver process and before labs/connected-return-review-pass02
status: frozen when the first driver process starts

This contract replaces the runnable shape of the 05.12 init example. It does not revise evidence/build05.12/CONTRACT.md. The two official 05.12 stamps stay as the prior-failure record. This run does not launch the bare init command again.

A driver defect that exits before any product tool is launched is not the official run. A run that launches a product tool is the official run, including a failed one. Its outputs stay. They are not deleted to improve the story.

## What the 05.12 init example established

The first official stamp, 20261103T173827361432Z, launched pass04 init with only `--book` and `--name`. Pass02 argparse refused it. The required arguments are `--authorization`, `--audit`, `--plan`, `--backup`, `--staging`, and `--retired`.

The second official stamp, 20261103T174140129061Z, passed those six flags at a non-JSON stub. Historical reserve had already created an empty `0100.band.returns` lock directory, so init treated the book as door-marked and refused the stub with `Restore the JSON record.`

The third stamp planned first, bound a synthetic authorization whose layout hash was the predicted line-pass body and whose operations included `init`, then called pass04 init with the six real flags, then copied the measured door page into the lock directory. That sequence is the fixture preparation this contract requires. The synthetic authorization is not a Director release and not live authority.

## Ownership

The driver is new labs/connected-return-review-pass02/drive.py. It is a command record. It is not a second return engine, a patching service, or an app selector.

The disposable book and the copied code root live under a new directory D:\librarian\temp\0521-0513\<UTC-stamp>\. The book is outside D:\Git\lib-build. The driver creates that directory with a timestamp. It does not call tempfile.mkdtemp and it does not remove a directory tree. It does not write under D:\librarian\temp\0521-0512.

The driver writes only under its stamp. Evidence files in this directory, other than this contract, are written after the official run. The shared app, README, live book, frozen labs, pass01, and the 05.12 evidence stay unread for writes.

Python is C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe with -B and PYTHONDONTWRITEBYTECODE=1. Product tool processes use absolute paths. The copied app is started with its code root as the child cwd. The live readiness, the live preflight, and the N7 cycle prepare use cwd D:\Git\lib-build because those tools read that checkout.

## Fixture code

Copy every app/ and labs/ row of evidence/pack05.13/source-manifest.json except app/librarian.py and app/README.md. The copy dispatcher starts from the measured live app/librarian.py, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes, and applies only these two quoted substitutions, once each:

- `parent / "return_line_tools_v2.py"` becomes `parent / "return_line_tools_v3.py"`
- `parent / "handoff_tools.py"` becomes `parent / "handoff_tools_v2.py"`

`authoring_tools_v2.py` and `review_loop_tools_v7.py` stay in place. The copied review launchers still read D:\Git\lib-build. The fixture lists those fixed roots. It is not a self-contained portable app.

## Book and authority

Book name `00.00.10.work`. One small external book. No 83-member migration. No hand-written receipt, manifest, or layout.

Layout bytes come from pass04 init. The predicted body, dumped with indent 2 and sort_keys, is schema `return-line-layout/1`, allocation `line-pass`, sequential_allocation false, bands 5 `matched-workflow-return-line` and 7 `page-local-colab`, book `00.00.10.work`.

The authorization is schema `return-line-authorization/1`, synthetic true, executor exactly `Codex Prime`, release exactly the copied pass02 `RELEASE_TEXT`, operations `capture`, `init`, `preflight`, and `reserve`. book_path is the disposable book. The audit is an empty `{files: [], records: []}` object. The plan is the copied app `return-lines plan` output. Backup, staging, and retired roots are stamp siblings.

The door page copied into `0100.band.returns/01.md` is the measured live page, sha256 c9ff0949c09268451a8e2a2113c1612047b374b3ecc0b3c177b6c5fd22b6842d. The copy happens after init. Historical reserve may already have created the lock directory. That directory is not the line-pass layout.

## Commands

Historical work uses the copied guard, which is the selected writer gate. Capture and verify of a historical member use the guard. The same verify is repeated through the pinned reader `labs/return-capture-pass01/return_capture.py` and through `labs/return-capture-pass01/return_inspect.py inspect --json`. Those are the supported reader and guard paths. The copied app has no historical-verify command. Its historical write path is `capture-return`.

Before any layout exists:

1. Guard reserve of the positive witness. `--name historical-witness`, `--submission hist-witness`, `--expected-output witness.txt`, origin book `00.00.10.work`, page `0504.app-entry`, batch `05.08`, submitter `Grok-2`, reviewer `Codex Prime`, release `historical-witness`. The driver records the printed member. The absent-protection line is recorded and is not protection.
2. Guard capture of that submission. `--return-file` is an absolute file outside the book. `--source-root` is an absolute directory outside the book. `--artifact witness.txt|witness.txt`. The source bytes are the declared payload.
3. Guard verify, reader verify, and inspect of that member. The positive result is `result complete` from verify, with `not approved`, `not accepted`, and `not published`. Inspect status is `complete`. The driver records return.md, receipt.json, manifest.json, and payload/0001.blob hashes.
4. Guard reserve of the negative member. `--name historical-missing`, `--submission hist-missing`, `--expected-output missing.txt`, same origin shape. No capture. This member is the missing-return.md test. It is not the positive witness.
5. Guard reserve of the eligible handoff member. `--name historical-eligible`, `--submission hist-eligible`, `--expected-output return.md`, `--expected-output piece.txt`, same origin shape. No capture yet.
6. Clerk queue, claim, and return for job `fixture-0513` on a store outside the book. The outbox files are the return bytes and the piece bytes. The binding schema is `clerk-capture-handoff/1`. Artifact logical names are `return.md` then `piece.txt`. Their sha256 and byte counts match the source files and the outbox files. The binding member is the printed eligible member. The binding submission is `hist-eligible`.

Then the book is marked:

7. Copied app `return-lines plan` with the empty audit and an absolute `--out` outside the book and outside the copy's live-book path.
8. Write the synthetic authorization, including `init`, with the predicted layout hash.
9. Copied pass04 `init --book BOOK --name 00.00.10.work` plus the six flags. Bare init is not used.
10. Copy the measured door page into the existing `0100.band.returns` directory.

After the layout and door exist:

11. Repeat guard verify, reader verify, and inspect of the positive member. The four file hashes stay identical to step 3. The guard text is the complete read. It is not the declared-layout write refusal.
12. Guard verify of the negative member. Expected text is `missing return.md` and `result refused`. That result stays labeled negative.
13. Copied app `capture-return --binding BINDING` for the eligible member. Expected exit 2. The proof that the selected guard ran is the failure-log field `capture.attempted` true and `capture.stdout` containing `writer_started: false` and `Use the line-pass route.` The short summary may also say `capture-files absent` because the member never gained receipt files. That summary line is not the proof. The eligible member gains no receipt.json and the book gains no new member. The measured file hashes stay the precondition record.
14. Repeat the same capture-return command. The failure-log bytes and the intent.json bytes stay identical. The second transcript retains the prior failure and does not report completion. No new member appears.

Native filing on the same marked book, through the copied app, each write with the six flags:

15. Handwritten source page `0521.connected-return-review/05.01.md` with one vacant `## Review - Codex Prime` body `PENDING.` That vacancy is fixture serialization.
16. `return-lines reserve` and `capture` for page `0521.connected-return-review`, batch `05.01`, submission `s0513a`, output `note.txt`. The return file and note are prepared outside the book. Reserve exit 1. Capture exit 0. The receipt is the tool's receipt.
17. `return-lines lookup` and `verify` by book, source, and pass.
18. `review-loop prepare`, `form`, `record` with a supplied judgment, `inspect`, then a separate `publish`, then separate `read` and `recover`. Judgment fields are the declaration fields. tests_passed is null. semantic_conflict is null. operation is continue. The judgment says it is supplied test data. Inspect stdout is saved before publish starts.

Page-local filing and the N7 diagnosis:

19. Handwritten pack `0721.connected-local/05.01.pack.md`. The file `0721.connected-local/06.01.review.md` is not created by the driver.
20. `return-lines reserve` and `capture` for page `0721.connected-local`, batch `05.01`, submission `s0513n7`. Directory `0121.connected-local` stays absent.
21. `review-loop prepare`, `form`, `record`, and `inspect` for that source and pass. The driver copies the cycle descriptor, registration, and request that the workbook wrote. It does not invent a template.
22. A separate process runs the live `labs/review-loop-pass03/review_loop.py prepare --fixture-root BOOK --request REQUEST`. Stdout, stderr, and exit are saved. This call is the minimal retained case of the template failure. The driver does not create `06.01.review.md` before it. If that file is still absent and the view's template is null while `write_token` is null, the classification is the implementation seam below. A caller correction is not demonstrated. The N7 cycle-success claim stays stopped.
23. `review-loop publish`, `read`, and `recover` may then run as the preliminary fallback. Their exits are recorded. They do not reclassify a null template as cycle-committed.

Read-only observations:

24. Copied readiness: `python -B labs/return-readiness-pass02/readiness.py --code-root CODE --book BOOK --text`
25. Live readiness: the same tool with `--code-root D:\Git\lib-build` and `--book D:\Git\lib-build\00.kernel\00.00.10.work`
26. Live pass04 preflight against the real book with a synthetic authorization whose book_path is the real book. Expected exit 2. This is not a reserve or a capture.

No hard-link race. No AR-01. No model call. No network.

## Expected results

The positive historical verify exits 0 both before and after declaration. Its receipt and return bytes stay the same. `result complete` coexists with `not approved`, `not accepted`, and `not published`.

The negative verify exits 2 with `missing return.md`. The eligible capture-return exits 2 with the guard's `writer_started: false` inside the retained failure log. The repeated call keeps those bytes.

Native reserve exits 1. Native capture exits 0. N5 lookup and verify exit 0 with task_association `not-established`. N5 record mode `cycle-committed` is the tool mode. `closes_work` and `releases_action` stay false. Envelope accepted stays false.

N7 capture exit 0 is the page-local filing. N7 review mode stays `preliminary` when the tool says so. The template failure stays visible. Publish of that preliminary record is not cycle commitment.

The live preflight exits 2 and does not create a live layout. Live librarian.py and the door page keep their start hashes.

## N7 seam the run may confirm

The workbook caller in `labs/workbook-review-pass02/workbook.py` function `write_cycle_inputs` sets an N7 registration target to `intake["destination"]`, which is `{page}/06.{tail}.review.md`. `labs/prime-cycle-pass03/prime_cycle.py` function `address_of` requires that target to equal the derived destination. Function `derive` emits `template` only when the observation is complete, a binding exists, and `write_token_of` returns a token. `write_token_of` returns null when the target path is absent. `labs/review-loop-pass03/review_loop.py` function `prepare` can exit 0 with that null template. The workbook then reports `cycle prepare did not return a template`.

The input invariant that produces the failure is an otherwise accepted N7 registration whose derived review file is absent. The output invariant of the current derive function is `template: null` and `write_token: null`. A later repair in `derive` would emit schema `prime-cycle-decision/3` for that absent-file N7 case while leaving `write_token` null, and `record` would still refuse `target-absent` until a separate create is authorized. N5 keeps its current token requirement because its target is the existing source page. This contract does not apply that repair.

## Failure

The first product command that misses its expected exit, route, or byte invariant is the first failure. Later probes still run when they do not repair a sealed return, receipt, failure log, or intent. The driver writes the transcript either way. Exit 0 from the driver is not Prime review, seating, or app activation.

## Selection handoff the run may report

The proposal remains the two substitutions above, the measured before identities, and the additive sentences already written in evidence/build05.09/SELECTION.md. Those sentences stay proposed text. One next action: after Prime reviews this return, Prime remeasures the shared dispatcher and applies only those two substitutions, using inspect, a full read, and a separate publish pause. The N7 template repair is a separate core change and is not part of that selection. Physical migration is not part of the selection.
