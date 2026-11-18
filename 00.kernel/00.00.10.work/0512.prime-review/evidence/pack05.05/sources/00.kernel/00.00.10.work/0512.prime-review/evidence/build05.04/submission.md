# Submission - 0512.prime-review/05.04

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0112.prime-review unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.04. It is a claim. It is not acceptance, not custody, and not a release. Notes in 06.05.md were reread after the author suite and integrated there. The contract was not revised after tests. This file does not carry the artifact-manifest hash. That hash is written only on the 05.04 return pointer after the manifest exists.

## Did

Verified evidence/pack05.04/source-manifest.json before the notes. Schema prime-pack-inputs/1. 45 files. bad 0. missing live 0. missing snapshot 0. live drift 0. snapshot mismatch 0. extra snapshots 0. Manifest sha256 3104c065ed3fc153f1cfe82c86831723b8689a6828e80837f4e3fe806033d4a3, 15289 bytes. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. The freeze was not repinned.

Read 0412/06.08, 0412/06.07, and 0707/06.12.followup. The held draft evidence/next05.04/PACK-DRAFT.md was left byte-for-byte. Built labs/review-report-pass01. The command is python -B labs/review-report-pass01/report.py --code-root ABS --book ABS --source PAGE --pass 05.NN. Stdout is one JSON object, schema review-report/1, including the projection of that same object. It calls librarian review-loop inspect, read, and recover. It does not prepare, record, or publish.

report.py sha256 72e9bda15c5f3ca844350be5dae2fcfcf4e7c609c262b8f7e702d64467eb94cc, 42127 bytes. tests/test_report.py sha256 1b7c4cee3fed7bc9e18b02245415f0213768e1d08650eae0dd287330ff900ca8, 27696 bytes. CONTRACT.md sha256 590fed944628a95f07ee7fd8f2ca5530a2dbc7b7ec35d4f8046000d8dd3474b2, 15139 bytes. 06.05.md sha256 3eaede10972f07a61036d626b68f91fe964f3040d37b57c6b48745cea9d7042b, 5863 bytes. README.md sha256 d58390cff299c5d5a248c77ed9f71723a58407e005e047f0b27f2ca516eac9f3, 843 bytes. PRIME-USE.md sha256 0a1edb29b223efc441e2b0c0ae5535d48a099ea6a261b92e925d02870eaa981f, 1511 bytes.

The second author run was 14 tests, 22.527 seconds, OK, exit 0. Python 3.14.0. The first run crashed on a refused report because pass_terminal was missing from the blank object. That traceback is evidence/build05.04/first-failure/usage.txt. The repair is in the lab. The contract was not revised. The cases are author cases. They are not independent and they are not a known-failure reproduction.

The live observation used two processes on the current book, source 0522.review-construction, pass 05.13. Both exited 0 with the same object. Review w4c5ae945c250d823. Disposition accepted. Custody missing. The six agreement attention lines and the bounded tests_note are in the projection. tests_passed true is a supplied bounded assessment. Publication class complete and stale false. work_complete false. action_released false. The stored render omits the note and the attention lines. The live journal, record, render, judgment, intake, and 05.13.md were unchanged. The saved stdout is evidence/build05.04/current-review/report.json.

## Blocked

Matching line 0112.prime-review is unfiled. This slice does not file it and does not invent a receipt. Custody on the live review stays missing. The six agreement fields stay unknown. Physical retention stays deferred at 0419.work-history/06.02. The proposed renderer integration is not applied to the core. Codex Prime has not reviewed this pack. This builder does not commit.

## Need

Codex Prime review of this return. The integration delta is in the contract and in labs/review-report-pass01/PRIME-USE.md. Stop here.

## API and ownership

The caller supplies an absolute code root, an absolute book, a source page id, and a pass. The process checks the pinned doors, then inspects, reads, and recovers that one address. Exit 0 means the selected record is recoverable and the core stale flag is false. Exit 1 returns the report for stale, held, not-recorded, or identity-mismatch. Exit 2 is a bad call, a pin mismatch, or a non-JSON core result. Exit 0 is not approval.

Attention and prime_review_effective are read from record.json only after the journal record_sha256 matches and the judgment matches the core. A hash mismatch is held and the file text is not displayed. The newest reviews directory is not selected. Claims stay not-recorded unless a structured row exists. This record schema has none. A missing declared path is reported and is not created.

Pins are the table in evidence/build05.04/CONTRACT.md. app/librarian.py stayed sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. app/README.md stayed sha256 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920, 39687 bytes. The lab does not edit them.

The proposed later core change is to add attention and prime_review_effective to inspect, read, and recover from the journal-checked record. journal.current stays the selected id. publication.review_id stays the published id. Historical rendered.md stays the published bytes under its recorded rendered_sha256. This pack does not edit the core.

## Claim, case, result, limit

| Claim | Case | Result | Limit |
|---|---|---|---|
| Supplied tests_passed true keeps its note and limits | coverage | exit 0; note and limit are in the projection; render omits the note | author case; the boolean is not proof all tests ran |
| Accepted disposition keeps attention and missing custody | attention | exit 0; effective attention; six agreement lines; custody missing | author case; agreement fields stay unknown |
| Null coverage stays unknown | unknown-coverage | exit 0; tests_passed, tests_note, and limits are unknown | the render line none supplied is historical text, not the judgment |
| Hold, reply, and successor stay distinct | hold-reply-successor | exit 0; successor_of is the prior id; Director words and the reply are both shown | author case; the reply is not a new judgment |
| Blocked publication keeps the judgment | blocked-publication | exit 0; class blocked; finding preserved | author case on a read-only N7 target; pointer-pending |
| Source drift stays visible | source-drift | exit 1; stale true; class complete; finding preserved | author case; staleness is not cleared |
| A changed record is not authoritative | changed-record | exit 1; state held; attention not-exposed; TAMPERED absent | author case; first run crashed before emit and was repaired |
| A missing record does not invent findings | missing-record | exit 1; state held; findings unknown | author case; same first-run crash, then repaired |
| Another book is another instance | another-book | exit 1; state not-recorded; instance_id differs | author case |
| Missing evidence is not regenerated | missing-evidence | exit 1; missing-referenced; the path was not created | author case |
| A newer folder is not selected | hostile-newer-folder | exit 0; journal current kept; NEWER FOLDER WINS absent | author hostile; not independent |
| Prose does not become coverage | hostile-prose-pass | exit 0; claims.rows empty; both proof flags false; the note is verbatim | author hostile; not independent |
| The live 05.13 review can be read without writes | live, two processes | exit 0 twice; objects match; six lines; note; accepted; custody missing | observation only; not self-approval or permission to publish |

## Factfind, hostile, overflow, unprompted

Factfind: reviewed inspect returns a judgment without the journal hash check. The report withholds that copy when the hash differs. The published render for w4c5ae945c250d823 shows tests_passed true and prime_review_effective attention, and it omits the tests_note and the six attention lines. Intake unknowns are four names. Attention is six lines.

Hostile: the newer-folder and prose-pass cases are above. Raw rerun logs are evidence/build05.04/hostile/. The first product failure is the pass_terminal KeyError, kept in evidence/build05.04/first-failure/usage.txt.

Overflow: none. Full rows and sections are in the detailed projection. No padding count was added.

Unprompted: app/README.md is not a freeze row. The suite and this return still record its unchanged hash. The blank report omitted pass_terminal until the repair.

## Reread

06.05.md states the freeze, the gap, the first-run crash, the repair, and the live observation. It does not carry this file's hash or the manifest hash.
