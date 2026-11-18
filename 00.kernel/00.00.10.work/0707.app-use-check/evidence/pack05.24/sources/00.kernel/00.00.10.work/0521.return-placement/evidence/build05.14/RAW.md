# Raw record — known failure, retained stamps, and the proof

Date: 2026-11-03. Executor: Grok-2. Reviewer: Codex Prime.

The raw outputs stay in the stamp directories. This page names them. It does not replace them.

## Known failure

Directory `D:\librarian\temp\0521-0514\known-failure`. This is a copy of the 05.13 book with only the copy of `0721.connected-local/06.01.review.md` removed. The live loop was `labs/review-loop-pass03/review_loop.py prepare`. Exit 0. Stderr 0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Stdout `prepare.stdout`, 9802 bytes, sha256 `8d83f24ff21b596eb761306ffc3ff5beb3f2528a6fe2fdb174a4b801c058169c`. Summary `known-failure.json`, 338 bytes, sha256 `45df6e729be89fe76a6e4f6621bfe56ff9f1daa7f48765a7c62cd256d5001970`. Schema `n7-known-failure/0514`. View `prime-cycle-view/4`. Source kind `N7NN`. Target `0721.connected-local/06.01.review.md`. Observation `complete`. Template null. Write token null. Review still absent. The 05.13 stamp was not edited. This reproduction is the known failure.

## Retained first official failure

`D:\librarian\temp\0521-0514\20261103T225239321284Z\run-report.json`, 10310 bytes, sha256 `3823bf1e68f223424d03dce0be46c88420b500cbe88dfe86d9dc4b80fc1503e8`. Schema `n7-first-review-run/0514`. Problems 9. First step `08-n7-record`: N7 record mode was preliminary. Cycle error: `refused: prime_review refused the review: refused: bind requires --root`. The absent-create token was present. The planted temporary and the preliminary review file in that stamp stay. Command stdout and stderr stay under that stamp's `out`.

## Retained measurement miss

`D:\librarian\temp\0521-0514\20261103T225847465645Z\run-report.json`, 11542 bytes, sha256 `873e77ad6e30496c26e8c3e310e459df12b2bb2771e5a5965efb83f13cab2f15`. Problems 2, both at `08-n7-rendered`. The product record stored `reviews/wf98ef20e56a18f26/rendered.md` at 864 bytes. The driver read the cycle folder and stored an empty body. The case list on that stamp is ok. The stamp stays.

## Proof

`D:\librarian\temp\0521-0514\20261103T230047760921Z`. Run report 11495 bytes, sha256 `0caba09ec89bbbb0e9e59e9ac93cf6d86a5452d16a80d49552019a6880a3707b`. Problems 0. `out/n7-rendered.md` 864 bytes, sha256 `d969d9a9364cefa20aa2068fc9da127c11ec16c6e06bc040e5d255fa5ac1933d`. Page `book/0721.connected-local/06.01.review.md` 4009 bytes, sha256 `66b30232469c651229e8db1e8818769ed9a562441896dd02155ddbd5c4510234`.

Command exits on that stamp:

- `01-plan` 0, `02-init` 0. Reserve `03-reserve-n5` and `05-reserve-n7` exit 1, the reserved envelope. Capture `04-capture-n5` and `06-capture-n7` exit 0. Verify `07-verify-n7` and `07-verify-n5` exit 0.
- N7 `08-n7-prepare`, `08-n7-form`, `08-n7-record` exit 0. Workbook mode `cycle-committed`. Nested cycle `record_exit` 1 with result `recorded`. That pair is the cycle tool's recorded result. `09-n7-cycle-read` exit 0, state `create-pending`. `10-n7-publish` exit 0, tool `published` true. `11-n7-read`, `11-n7-recover`, `11-n7-render`, `11-n7-cycle-read` exit 0. Render result `already-rendered`.
- N5 `12-n5-prepare` through `12-n5-publish` exit 0. `13-n5-replay` exit 0, mode `cycle-committed`. Review `wd05e6026273335bf`.
- `14-manual-publish` exit 1, correction `Existing manual review text was kept.`
- `15-after-record` exit 2, rule `target appeared after read`.
- `16-foreign-reread` exit 2, rule `target is not the derived review destination`.
- `17-malformed-reread` exit 2, rule `unsafe path target`.
- `18-token-record` exit 2, rule `absent-create token path is not the derived destination`.
- `19-n5-forge-reread` and `19-n5-forge-record` exit 2, rule `refused: missing file assignment`. The N5 page stayed absent.
- `20-directory-publish` exit 1, correction `target is not a regular file and was not replaced`.
- `22-temp-publish` exit 1, correction `refused: temporary name 06.01.review.md.review-construct.tmp is present`. The temporary remains at `copies/temp/0721.connected-local/06.01.review.md.review-construct.tmp`, 18 bytes, `partial construct`.
- `23-return-changed` exit 1, correction `Publication is blocked because the selected source changed after intake.`

The symlink case created no link. The report records `symlink skipped: WinError 1314`. Each command's stdout and stderr remain under `out` on the proof stamp.
