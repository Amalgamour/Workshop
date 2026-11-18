# Submission — 0511.workflow-colab/05.04

## Did

Read the pack, the corrected design at 0510.colab-tools/evidence/design05.06/CONTRACT.md, and Prime's review on 0510.colab-tools/05.06.md and in evidence/prime-review05.06/REVIEW.md. The page review and the evidence review agree. 0510.colab-tools/06.08.md records the selected route: ordinary and reserved N7NN work keeps 05.NN.pack.md, 05.NN.return.md, and 06.NN.review.md on the same investigation page. N5NN keeps its matching N1NN line.

Verified 40 frozen inputs before the notes and again before this return. Live bytes, snapshot bytes, and declared hashes matched. Bad count 0. Manifest sha256 d30a0492adf17b7480ad719119dfcc8b0ccd8d4b7f1b06d8359bfb97ca7e2a70, 13741 bytes, schema prime-pack-inputs/1. Recorded the invocation and the claim in 06.04.md and on this page before the successor code. HEAD 960d20c5290656095df8457b1740d2d5e586b111, branch workshop. Python 3.14.0.

Wrote evidence/build05.04/CONTRACT.md and evidence/build05.04/FAILURE.md before the module. The place-return fact keys gained manifest_sha256, origin_batch, origin_book, and origin_page before any saved verification command. CONTRACT.md remains sha256 8b05292bcee82877975519ae9473a2cf0a7feb8888dc966fda50161cfc7d8273, 10094 bytes. FAILURE.md remains sha256 3cca7a114d630b9b12159701285904f863e6423221968e00e8acf8feb2d1c4df, 3691 bytes. contract_revised_after_commands is false.

Added labs/colab-workflow-pass03. colab_workflow.py sha256 fc469af91f8bdcbaa980457535b7276a5c4e2421a81ad861e93ff750a511c944, 68410 bytes. Pass02 remains sha256 4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec, 47247 bytes. Producer v2 remains sha256 2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b, 53892 bytes. The app, the door, the loop, the cycle, the constructor, and the prior captures stay unmodified.

seal-return-local stores the supplied file bytes as artifacts/<pass>/return.md and as 05.NN.return.md. The slot is colab-exchange-local-return/1. open-pass adds one empty later slot from exactly one recorded request-next review whose package and page-local return are intact. Transitions stay in investigation.json. seal.json stays the sha256 of that record. An interrupted write leaves partial.json, and a later command returns resume refused.

Recorded command, from D:\Git\lib-build, PYTHONDONTWRITEBYTECODE=1:

python -B labs/colab-workflow-pass03/tests/run_suite.py

Saved at evidence/build05.04/runs/20261101T211832Z. Suite exit 0. test_pass03.py exit 0: executed 10, skipped 1, failed 0. The skip is test_symlink_refusal, WinError 1314. test_real_two_pass.py exit 0. The real child called the pinned producer. First digest 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184. Second digest 933171c1201b91ddf8f87a00179ec23a3fe83dcc0ce440cd6614b68494af4b0e. Actions: open, attach, seal-return, review, open-pass, attach, seal-return, review. The live envelope was copied into a temporary book and its source tree hash matched before and after. Stored logs are LF. The Windows runner wrote 29 CR on stdout and 0 on stderr. Text and exit are unchanged.

verification.json sha256 bfaa8f80d774ab0c2f3b75184713df81831b4b258235680d1f33acdf29c9a537, 4993 bytes, schema colab-workflow-pass03-verification/1. accepted is false.

## Blocked

No recorded child failed. The file-symlink refusal did not run. WinError 1314 is stored as a skip, and no privilege was requested. The suite still exits 0.

## Need

Codex Prime review of this isolated successor. This builder does not accept the result and did not commit. Matching line 0111.workflow-colab stays pending. No receipt was written. 0184 was not allocated. No new capture slot was opened. Pass03 stays unselected in the app, the door, the loop, and the cycle. Passing tests do not select live tooling, approve findings, or release another pack.

## CONTRACT and API/schema delta

The binding text is evidence/build05.04/CONTRACT.md. Unchanged names: colab-exchange-result/1, colab-exchange-open/1, colab-exchange-review/1, colab-exchange-seal/1, colab-exchange-partial/1, colab-exchange-provenance/1, colab-package-digest/2, colab-package-verification/2, colab-config/2.

The investigation schema is colab-exchange-investigation/2. A pass02 record is unknown schema. Pass03 does not rewrite it. The new slot object colab-exchange-local-return/1 has exact keys schema, kind, return_sha256, return_bytes, declared_transport, package_digest, pass. kind is page-local. The legacy place-return object keeps the pass02 keys and adds kind n1nn. Its exact keys are kind, manifest_sha256, member, origin_batch, origin_book, origin_page, receipt_sha256, return_bytes, return_sha256.

New commands:

seal-return-local --book ABS --page NNNN.name --pass 05.NN --return-file ABS --declared-transport TEXT

open-pass --book ABS --page NNNN.name --pass 05.MM

Show on a loaded page includes transitions. Each pass flag includes return_kind with value null, page-local, or n1nn. A partial page reports partial true, passes [], and transitions null. The command result name complete means the read finished. 01.md lists sorted pass ids on one passes line. A page-local 08.md sentence names the pass, the page-local return, the sha256, the byte length, the transport label, the package digest, and the file name.

A transition object has exact keys action, facts, pass, prev, seq, sha256. Actions are open, attach, append-note, place-return, seal-return, review, and open-pass. RETURN_LIMIT is 1048576. TRANSITION_LIMIT is 64. TEXT_LIMIT is 4096. Exit 0 writes canonical JSON to stdout. Refuse exits 2 with canonical JSON on stdout, reason and wrote set, and empty stderr.

## Failure and recovery

The binding text is evidence/build05.04/FAILURE.md. commit takes the lock, writes extras, writes projections, writes investigation.json, writes seal.json, removes partial.json when it is present and is not a reparse, and removes the lock in finally. write_bytes calls WRITE_HOOK before it truncates. Any exception other than Refuse writes partial.json with schema colab-exchange-partial/1 and reason interrupted write, then raises Refuse interrupted write with wrote true. require_loaded returns resume refused while partial.json or .write.lock exists. There is no cleanup command and no automatic restore. The injected boundaries are the return artifact, the page-local projection, investigation.json, and seal.json, plus the existing attach-artifact case. At the seal.json boundary the new investigation bytes may already be on disk while seal.json still names the previous bytes. partial.json keeps that page refused. A crash after truncation has begun is outside the plan. AR-01 stays held.

## Compatibility

Pass02 remains the tool for schema /1 books. Pass03 refuses those books. Show JSON, 01.md, and 08.md follow the /2 rules above. Kept commands keep their ordinary refusal reasons where the new checks do not name a more specific reason. record-review still commits and then refuses malformed review, wrote true, when the requested next pack file already exists. open-pass does not create that pack file. place-return stays available and does not satisfy open-pass. repo_root() stays Path(__file__).resolve().parents[2]. Attach still pins the v2 producer and runs verify. No live book write, no Git write, and no capture reservation is added.

## Tests, fixtures, and source

The command and the exits are in Did and in evidence/build05.04/PRIME-USE.md. Synthetic books use temporary directories with prefix 0511-0504- and are removed with the test. The real child copies evidence/real-producer-v2-05.03. Page 0701.colab-exchange-layout. Passes 05.01 and 05.02. The source envelope is not a write target. LF and CRLF return bytes both round-trip in the recorded real path.

Source before this slice: labs/colab-workflow-pass02/colab_workflow.py, 47247 bytes, sha256 4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec. Those bytes are unchanged.

Source added by this slice: labs/colab-workflow-pass03/colab_workflow.py, 68410 bytes, sha256 fc469af91f8bdcbaa980457535b7276a5c4e2421a81ad861e93ff750a511c944. README.md, tests/run_suite.py, tests/test_pass03.py, and tests/test_real_two_pass.py are in the same new directory. The artifact manifest binds their final bytes.

## Factfind (opinion lives here only)

Under one review per pass, the review that opened a later pass still names that pass. A second review naming the same future pass cannot be stored through these commands without breaking the recorded link. The suite calls open_pass_decision with synthetic in-memory records for conflicting requests, occupied pass, and occupied different state. A sealed book that cannot represent those three states is reported as hash conflict.

The reachable CLI earlier-pass path opens 05.03, requests 05.04, seals that pass, then records a 05.04 review naming 05.02 while 05.02.pack.md is absent. open-pass 05.02 refuses earlier pass, wrote false, and creates no slot. Opening 05.01 when no review names it returns next pass not requested.

The tamper test rebuilds the transition list with a new title and a recomputed seal. show then succeeds. The checkpoint compares the loaded seal with the loaded record and requires the new list to keep that list as its prefix. A wholesale rewrite that recomputes every transition hash and the seal is outside that check. The contract states this limit, and the test records it.

review_pending false is the stored flag. It is not a completeness mark. On a partial page the show command result name can still be complete, and that name means the read finished. The page row carries partial true and transitions null.

## Hostile

A one-byte append to a projection stays on disk, and show returns hash conflict, wrote false. Changing the slot return hash and recomputing only the seal, without rebuilding the chain, returns hash conflict. A different return body returns occupied different content and leaves the previous bytes. A different transport label on the same bytes returns declared transport differs and leaves the stored label. An N1 place-return of those bytes, followed by a seal of the same bytes, returns occupied different content. request-next plus open-pass after that placement returns local return required and does not create 05.02.pack.md.

Injected failures at the return artifact, the return projection, investigation.json, and seal.json each leave partial.json, wrote true, and reason interrupted write. A later seal returns resume refused, wrote false. The attach artifact hook does the same. A junction created with mklink /J returns unsafe path. A producer copy with one flipped byte returns pin mismatch and does not launch. The file-symlink refusal did not run.

## Overflow (parked)

Schema /1 books stay with pass02. This module does not migrate them. V01 through V03 stay with the later checker. Descriptor packaging H2 stays out of this slice. No reserved-exposure gate is added. The post-commit pack-file refusal on record-review stays. repo_root() stays parents[2]. No capture slot and no 0184 allocation are opened here.

## Unprompted

Stop for Codex Prime. The next bounded action is that review. App integration, live migration, and another pack are not started by this suite.
