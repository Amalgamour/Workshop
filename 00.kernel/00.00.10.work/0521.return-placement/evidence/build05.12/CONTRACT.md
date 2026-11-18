# 05.12 command contract

schema: connected-return-review-contract/0512
written: before any driver process and before labs/connected-return-review-pass01
status: frozen when the first driver process starts

This contract is not revised after that process starts. A driver defect that exits before any product tool is launched is not the official run. The same contract governs the rerun. A run that launches a product tool is the official run, including a failed one. Its outputs stay. They are not deleted to improve the story.

## Ownership

The driver is new labs/connected-return-review-pass01/drive.py. It is a command record. It is not a second return engine, a patching service, or an app selector.

The disposable book and the copied code root live under a new directory D:\librarian\temp\0521-0512\<UTC-stamp>\. The book is outside D:\Git\lib-build. The driver creates that directory with a timestamp. It does not call tempfile.mkdtemp and it does not remove a directory tree.

The driver writes only under that stamp. Evidence files in this directory, other than this contract, are written after the official run from those outputs. The shared app, README, live book, and frozen labs stay unread for writes.

Python is C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe with -B and PYTHONDONTWRITEBYTECODE=1. Product tool processes use absolute paths. The copied app is started with its code root as the child cwd. The live preflight is started with cwd D:\Git\lib-build.

## Fixture

Code closure: every source-manifest row under app/ or labs/, except app/librarian.py and app/README.md, is copied byte-for-byte from D:\Git\lib-build. app/README.md is not copied and is not opened.

The dispatcher copy starts from the measured app/librarian.py, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Exactly two substitutions, each one occurrence:

- parent / "return_line_tools_v2.py" becomes parent / "return_line_tools_v3.py"
- parent / "handoff_tools.py" becomes parent / "handoff_tools_v2.py"

authoring_tools_v2.py, review_loop_tools_v7.py, and every other branch stay byte-for-byte. authoring_tools_v2.py is not in the frozen closure and is not copied. The preserved authoring branch still names it. Invoking authoring on the copy is out of this run.

The copy is not a self-contained app. These helpers keep a fixed checkout root D:\Git\lib-build, so the review core reads the live reviewed modules even when the facade is the copy:

- labs/workbook-review-pass01/workbook.py
- labs/workbook-review-pass02/workbook.py
- labs/workbook-review-pass03/workbook.py

Return-line, placement, capture, guard, handoff, clerk, and readiness copies resolve their repo root from their own file path. Their live-book identity is <code-root>\00.kernel\00.00.10.work. This run does not create that directory. The disposable book is a different path, so the synthetic fixture is not pointed at the copy's live identity.

The driver lists every copied file that still contains the literal checkout path.

## Book

Layout book name: 00.00.10.work. This is the name inside the layout, not a claim that the disposable directory is the live book.

Pages:

- N5 source 0521.connected-return-review. Passes 05.01 and 05.02 file on 0121.connected-return-review. Pass 05.03 is the later artifact probe on that same line.
- N7 source 0721.connected-local pass 05.01 stays on 0721.connected-local. It must not create 0121.connected-local.

Door: copy the measured 0100.band.returns\01.md into the disposable book as a directory 0100.band.returns containing that file. Layout bytes come from the reviewed init command, not from a hand-built layout.

Handwritten fixture serialization, labeled in the files or in the run report:

- empty audit JSON with keys files and records, both empty lists
- synthetic authorization JSON
- source pages and the N7 pack page
- return bodies and note payloads that capture then copies
- supplied judgment JSON
- clerk job and binding for the legacy-write probe

Compute-generated, and not rewritten by hand:

- layout file from init
- plan file from the plan command
- reservation, manifest, receipt, and return bytes from reserve and capture
- review intake, record, and published review text from the review commands

Authorization: schema return-line-authorization/1, synthetic true, executor Codex Prime, book 00.00.10.work, release equal to RELEASE_TEXT in the copied labs/return-lines-pass02/return_lines.py. The driver reads that constant. It does not paraphrase it. operations are capture, preflight, and reserve. layout, plan, and audit hashes are measured from the files this run just produced. backup, staging, and retired are three sibling directories under the stamp, outside the book, outside the copy's live-book path, and not containing each other or 0100.band.returns.

No recorded release is written. The disposable book is not classified canonical. The full migration writer is not run. adopt, stage, publish, retire, and reconstruct are not run. The 83-member rehearsal is not run.

## Commands

Preparation, before the book is marked, through the copied tools:

1. Guard reserve on the still undeclared book. This is disposable preparation, not the native positive case. The absent-protection line is recorded and is not protection. The real book is not reserved. --name is the slug. The historical writer chooses the member directory from the next free number in 0101-0199. The driver records the printed member and uses that directory. It does not invent a second number.
   python -B labs/return-capture-guard-pass01/return_capture_guard.py reserve --book BOOK --submission hist-0512 --name historical-read --origin-book 00.00.10.work --origin-page 0504.app-entry --origin-batch 05.08 --expected-output final-report.md --expected-output piece.txt --submitter Grok-2 --reviewer Codex Prime --release historical-read-prep
2. Backend init, because the app facade requires an authorization that already pins the layout hash:
   python -B labs/return-lines-pass04/return_lines.py init --book BOOK --name 00.00.10.work
3. App plan after the empty audit exists. --out is absolute and outside the book and outside the copy's live-book path.
   python -B app/librarian.py return-lines plan --book BOOK --audit AUDIT --out PLAN

Then the door is copied and the authorization file is written.

Native filing through the copied app, each with --authorization --audit --plan --backup --staging --retired:

4. return-lines reserve --book BOOK --page 0521.connected-return-review --batch 05.01 --submission s0512a --output note.txt --submitter Grok-2 --reviewer Codex Prime --release synthetic fixture filing; not a Director release
5. return-lines capture for that page and batch, --return-file the prepared return, --artifact note.txt the prepared note
6. The same reserve and capture for batch 05.02, submission s0512b
7. return-lines reserve and capture for page 0721.connected-local batch 05.01, submission s0512n7
8. return-lines reserve and capture for page 0521.connected-return-review batch 05.03, submission s0512c

Expected route facts: 05.01 and 05.02 and 05.03 share target page 0121.connected-return-review. The N7 target page is 0721.connected-local. Directory 0121.connected-local is absent.

Retrieval through the copied app:

9. return-lines status --book BOOK
10. return-lines lookup --book BOOK --source 0521.connected-return-review --pass 05.01
11. return-lines verify --book BOOK --source 0521.connected-return-review --pass 05.01
12. The same lookup and verify for 05.02 and for the N7 source and pass

Review of 05.01, then of the N7 pass, through the copied app. Judgment fields are only the declaration fields. tests_passed is null. semantic_conflict is null. operation is continue. The judgment says it is supplied test data. Inspect stdout is saved before the publish process starts. Publish, read, and recover are separate processes.

13. review-loop prepare --book BOOK --source PAGE --pass PASS
14. review-loop form with the same book, source, and pass
15. review-loop record --book BOOK --source PAGE --pass PASS --intake INTAKE --judgment JUDGMENT
16. review-loop inspect --book BOOK --source PAGE --pass PASS
17. review-loop publish --book BOOK --source PAGE --pass PASS --review REVIEW
18. review-loop read, then review-loop recover, same book, source, and pass

The N5 source page includes a vacant `## Review - Codex Prime` body `PENDING.` so the core publish splice has a slot. That vacancy is fixture serialization. It is not a completed review.

Faults on the same book, after the 05.01 filing and its restart read:

19. New process verify of 05.01 immediately after filing and before its review. The receipt hash must match the capture receipt.
20. Conflicting capture retry of 05.02 with different return bytes and the same submission and artifact name. The sealed 05.02 return bytes stay. The first refusal text is kept. The receipt is not rewritten into a corrected success.
21. verify --source 0521.other-subject --pass 05.01. That source is not the filed source. Its result must not be the 05.01 complete receipt, and the 05.01 receipt bytes stay.
22. After 05.03 capture, change the captured note payload. verify that pass. Keep the first failure. Do not restore the payload and do not rewrite the receipt. The receipt file bytes stay.
23. Selected door: clerk queue, claim, and return against a fixture store outside the book, then
    python -B app/librarian.py capture-return --binding BINDING
    The binding names the disposable book and the member printed by command 1. Its artifact logical names are final-report.md and piece.txt, in that order. The capture launch is the guarded writer. The book must not gain a new receipt for that attempt, and the command 1 member directory must not gain a receipt.json.
24. Guard reserve of slug guard-refuse on the declared book, with the same origin shape as command 1 and submission guard-refuse. Expected refusal before allocation: exit 2, writer_started false, result refused, and no new member directory.
25. Guard verify --book BOOK --member MEMBER, using the command 1 member. This is the historical read. It must not be the declared-layout write refusal.

Read-only observations:

26. Copied readiness, with --text:
    python -B labs/return-readiness-pass02/readiness.py --code-root CODE --book BOOK --text
27. Live readiness, read-only:
    python -B labs/return-readiness-pass02/readiness.py --code-root D:\Git\lib-build --book D:\Git\lib-build\00.kernel\00.00.10.work --text
28. Live pass04 preflight against the real book with a synthetic authorization whose book_path is the real book. This is the canonical refusal. It is not a reserve or a capture.
    python -B labs/return-lines-pass04/return_lines.py preflight --book LIVE --authorization LIVEAUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED

No hard-link race. No AR-01. No model call. No network.

## Expected results

Native reserve exits 1 and says the reservation is stored. Native capture exits 0 and leaves a receipt from the tool. Lookup and verify of a filed pass exit 0 with task_association not-established. That read is not approval.

Review command exit 0 means the command completed. It does not mean Prime accepted the work, custody was filed, or execution was released. Exit 1 on record or publish means the judgment was kept and publication or recovery is blocked. The run records that and does not invent a receipt or a custody row. Mode preliminary stays preliminary. work_complete and action_released are recorded from the tool and are not treated as a Director release. Agreement fields the source heading does not carry stay unknown.

The guarded declared-book reserve exits 2 before a new member exists. The app capture-return attempt does not allocate a new historical member. If the handoff stops before the capture launch, that earlier refusal is labeled and is not counted as the layout refusal. The guard reserve in command 24 remains the layout-refusal proof.

The live preflight exits 2 and does not create a live layout. Live librarian.py and the door page keep their start hashes. The copy's readiness and the live readiness are both recorded. Copy selection is the substituted dispatcher. Real selection remains the unsubstitued dispatcher. The real book stays undeclared.

## Failure

The first product command that misses its expected exit, route, or byte invariant is the first failure. Later probes still run when they do not repair a sealed return or receipt. The driver writes the transcript either way. Exit 0 from the driver is not Prime review, seating, or app activation.

## Selection handoff the run may report

The proposal is only the two substitutions above, the measured before identities, the tested successor pins, and the additive sentences already written in evidence/build05.09/SELECTION.md. Those sentences stay proposed text. One next action: after Prime reviews this return and the other relevant builder return, Prime remeasures the shared dispatcher and applies only those two substitutions, using inspect, a full read, and a separate publish pause. Report projection from the same review record is later work and is not part of this run. Physical migration is not part of the selection.
