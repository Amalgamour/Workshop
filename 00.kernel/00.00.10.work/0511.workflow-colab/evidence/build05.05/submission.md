# Submission — 0511.workflow-colab/05.05

## Did

Read 0511.workflow-colab/05.05.md and the Prime review of 05.04 on the page and in evidence/prime-review05.04/REVIEW.md. The page review and the evidence review agree. Disposition recorded there: useful isolated implementation; correction required before routine use or selection. WF01 is the pass03 path that opens investigation.json with O_TRUNC. The pass03 hook runs before that open.

Verified 52 frozen inputs before the notes and again before verification.json. Live bytes, snapshot bytes, and declared hashes matched. Bad count 0. Manifest sha256 10bc2ebeb135379d61072d479d83daf7133cf40a0aa5bcdbb5c71cb5c3b17cbb, 18028 bytes, schema prime-pack-inputs/1. Recorded the invocation and the claim in 06.06.md and on this page before the successor code. HEAD 960d20c5290656095df8457b1740d2d5e586b111, branch workshop. Python 3.14.0.

Wrote evidence/build05.05/CONTRACT.md and evidence/build05.05/FAILURE.md before the module. One correction, still before any saved command, refuses publication collision when the publication file already exists, and it does so before the lock and before a checkpoint. CONTRACT.md remains sha256 e9d4d5e34ac8703aa3b1c2e22b83e54d592c7227c951629ce2ba30f0006347ba, 8996 bytes. FAILURE.md remains sha256 79b6b116b1be112684ec9cae1d0751762acbcdd992eea0e4b313cb1ed4c3e055, 5186 bytes. contract_revised_after_commands is false.

Added labs/colab-workflow-pass04. colab_workflow.py sha256 8ec953c503edbb9a890216b3cdb6630062967c7c4113fbd9b9304ace83bc9d7d, 74884 bytes. Pass03 remains sha256 fc469af91f8bdcbaa980457535b7276a5c4e2421a81ad861e93ff750a511c944, 68410 bytes. Pass02 remains sha256 4a2ece9e646224468b36ce63947c739d8ecd73155fbb62fb34f0442cbd2dceec, 47247 bytes. Producer v2 remains sha256 2b720434ac4c4331835c1484b0eca362e01e8afbecde0ab800ca392530abf68b, 53892 bytes. The app, the door, the loop, the cycle, the constructor, and the prior captures stay unmodified.

Pass04 keeps the pass03 investigation schema, page-local return, open-pass rule, and transition list. Before it replaces an existing investigation.json and seal.json pair, it copies that verifying pair to checkpoints/<seal sha256>/. The candidate bytes are written under staging/<publication id>/ with O_EXCL and then published with os.replace. Those two authority files are never opened with O_TRUNC. publication_id is the sha256 of the candidate investigation bytes. An identical candidate refuses publication collision, wrote false, and leaves no new checkpoint.

Recorded reproduction, from D:\Git\lib-build, PYTHONDONTWRITEBYTECODE=1:

python -B 00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.05/reproduce/run.py

Saved at evidence/build05.05/reproduce/runs/20261101T221040Z. Runner exit 0. That exit records the pass03 defect on new page 0797.wf01. Outcome Refuse: interrupted write. The investigation file went from 760 bytes to 380 bytes. The seal bytes stayed. partial.json is present. No checkpoints directory was created. Pass03 was not patched.

Recorded suite, same interpreter and environment:

python -B labs/colab-workflow-pass04/tests/run_suite.py

Saved at evidence/build05.05/runs/20261101T221100Z. Suite exit 0. test_pass04.py exit 0: executed 9, skipped 1, failed 0. The skip is test_symlink_refusal, WinError 1314. test_real_two_pass.py exit 0. The real child called the pinned producer. First digest 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184. Second digest 933171c1201b91ddf8f87a00179ec23a3fe83dcc0ce440cd6614b68494af4b0e. Actions: open, attach, seal-return, review, open-pass, attach, seal-return, review. The source envelope hash matched before and after. Stored logs are LF. The Windows runner wrote 28 CR on stdout and 0 on stderr. Text and exit are unchanged.

verification.json sha256 41ec769075d2fbbada6fe122bc23aeb307aa7bd1d819e737ec0778129deab195, 6823 bytes, schema colab-workflow-pass04-verification/1. accepted is false.

## Blocked

No recorded child failed. The file-symlink refusal did not run. WinError 1314 is stored as a skip, and no privilege was requested. The suite still exits 0.

## Need

Codex Prime review of this isolated successor. This builder does not accept the result and did not commit. Matching line 0111.workflow-colab stays pending. No receipt was written. 0184 was not allocated. No new capture slot was opened. Pass04 stays unselected in the app, the door, the loop, and the cycle. Passing tests do not select live tooling, approve findings, or release another pack.

## CONTRACT and API/schema delta

The binding text is evidence/build05.05/CONTRACT.md. Unchanged names: colab-exchange-result/1, colab-exchange-investigation/2, colab-exchange-local-return/1, colab-exchange-open/1, colab-exchange-review/1, colab-exchange-seal/1, colab-exchange-partial/1, colab-exchange-provenance/1, colab-package-digest/2, colab-package-verification/2, colab-config/2.

New objects: colab-exchange-checkpoint/1 at checkpoints/<seal sha256>/identity.json; colab-exchange-publication/1 at publications/<publication id>.json; colab-exchange-published/1 at publications/<publication id>.published; colab-exchange-attempt/1 at attempt.json. partial.json keeps schema colab-exchange-partial/1 and reason interrupted write, and adds publication_id, predecessor, and retained_checkpoint.

The current authority pair is page/investigation.json and page/seal.json, and only when partial.json, attempt.json, and .write.lock are absent and the seal matches. require_loaded reads that pair. It does not read checkpoints. Show on a loaded page keeps the pass03 JSON shape. A partial page reports partial true, passes [], and transitions null. The show result name complete means the read finished.

Commands stay propose, open, attach, append-note, place-return, record-review, seal-return-local, open-pass, and show. RETURN_LIMIT stays 1048576. TRANSITION_LIMIT stays 64. TEXT_LIMIT stays 4096. Exit 0 writes canonical JSON to stdout. Refuse exits 2 with canonical JSON on stdout, reason and wrote set, and empty stderr.

## Failure and recovery

The binding text is evidence/build05.05/FAILURE.md. commit computes the candidate and the publication id, refuses an existing partial, attempt, or lock, and refuses an existing publication file before it creates the lock or a checkpoint. It then creates the lock, retains the prior pair when the predecessor is retained-prior, exclusive-creates the publication record and attempt.json, writes extras, replaces projections from exclusive staging, and replaces investigation.json and then seal.json from exclusive staging. After the root pair reads back as the candidate, it exclusive-creates the published marker and only then removes attempt.json and partial.json. The lock is removed in finally.

A Refuse from a check propagates and does not write partial.json. Any other exception writes partial.json and raises Refuse interrupted write with wrote true. The checkpoint, publication record, attempt.json, and staged files stay. There is no recover command and no cleanup command.

A failed commit leaves the prior root pair, with a matching checkpoint when the copy finished; or the candidate investigation with the prior seal and a checkpoint of the prior pair; or predecessor none, with no checkpoint and no fabricated prior success. Prior artifact bytes this commit does not rewrite stay hash-identical. Projections are replaced before the authority pair, so a failure during the staged record write can leave a new 08.md while the root pair is still the prior pair. A failure during the staged projection write, before os.replace, leaves the live projection unchanged.

Inspection: when the three blockers are absent and the root seal matches, the root pair is current and checkpoints are ignored. Otherwise read attempt.json and open only checkpoints/<retained_checkpoint>/. Verify the identity digest, the investigation hash, and the seal field. Copying that pair back, or deleting a blocker, is outside the tool. predecessor none means there is no prior pair to copy aside. The tool does not pick the highest checkpoint id. AR-01 stays held.

## Compatibility

Pass02 remains the tool for schema /1 books. Pass04 refuses those books. Pass03 remains the tool that truncates authority files in place, so the recorded reproduction can still show WF01. Show JSON, 01.md, and 08.md follow the pass03 rules. Identical replay returns repeat, wrote false, and adds no checkpoint. record-review still commits and then refuses malformed review, wrote true, when the requested next pack file already exists. open-pass does not create that pack file. place-return stays available and does not satisfy open-pass. repo_root() stays Path(__file__).resolve().parents[2]. Attach still pins the v2 producer and runs verify. No live book write, no Git write, and no capture reservation is added.

## Tests, fixtures, and source

The commands and the exits are in Did and in evidence/build05.05/PRIME-USE.md. Synthetic books use temporary directories with prefix 0511-0505- and are removed with the test. The reproduction fixture is inside evidence/build05.05/reproduce/run.py: page 0797.wf01, note bytes `# Notes` and a newline, then a same-record commit with a partial os.write of the page-root investigation.json. The successor mid-write uses a later seal and injects on staging/<publication id>/investigation.json. PRIME-USE.md names each synthetic page.

The real child copies evidence/real-producer-v2-05.03. Page 0701.colab-exchange-layout. Passes 05.01 and 05.02. The source envelope is not a write target. LF and CRLF return bytes both round-trip in the recorded real path. tests/test_real_two_pass.py is the pass03 file's bytes, sha256 c9f34688a7b87edfd1741d5981fe798cf49e54e9f3df17771d9c79715d8fbe9f, 13810 bytes, and it imports the workflow beside it.

Source before this slice: labs/colab-workflow-pass03/colab_workflow.py, 68410 bytes, sha256 fc469af91f8bdcbaa980457535b7276a5c4e2421a81ad861e93ff750a511c944. Those bytes are unchanged.

Source added by this slice: labs/colab-workflow-pass04/colab_workflow.py, 74884 bytes, sha256 8ec953c503edbb9a890216b3cdb6630062967c7c4113fbd9b9304ace83bc9d7d. README.md, tests/run_suite.py, tests/test_pass04.py, and tests/test_real_two_pass.py are in the same new directory. The artifact manifest binds their final bytes.

## Factfind (opinion lives here only)

The pass03 WRITE_HOOK runs before os.open, so a hook failure never shows a short write after truncation has begun. Prime's injection writes after that open. The successor moves the authority bytes to an exclusive staging file and calls os.replace only after the staged bytes read back.

publication_id is the sha256 of the candidate investigation bytes. Recommitting the open record therefore collides with the publication file created by open, and the corrected order refuses that collision before retain_prior. A pass04 demonstration of WF01 has to seal a different candidate. The recorded pass03 reproduction still commits the same record, because pass03 has no publication file.

require_loaded ignores checkpoints whenever the root seal matches and the three blockers are absent. A directory named with 64 f characters does not become authority. While attempt.json remains, deleting partial.json leaves show partial. The root bytes can look complete and still be an unfinished publication.

The replace order writes projections before the authority pair. A record mid-write can therefore leave a new 08.md beside the old root pair. The recovery source for that projection is the retained record plus the artifact return bytes. The tool does not rewrite the projection during inspection.

The inherited limit remains: a rebuilt transition list whose every hash and the seal are recomputed passes show. record-review can still commit and then refuse malformed review, wrote true, when the requested next pack file already exists. review_pending false is the stored flag. On a partial page the show command result name can still be complete, and that name means the read finished.

## Hostile

The recorded synthetic child injected a partial os.write of the staged investigation on an existing pair and on the first open, a write hook before that staged file was opened, replace failures before the investigation replace and before the seal replace, and a partial write of the staged 08.md projection. Each interrupted case returned interrupted write, wrote true, and left partial.json. A later command, where the test issued one, returned resume refused, wrote false. The second-pass case kept the 05.01 artifact, pack, review, and page-local return hash-identical.

Planting checkpoints/<current seal id>/ returned checkpoint collision, wrote false, kept the planted bytes, and wrote no partial.json. An identical seal returned repeat, wrote false, and added no checkpoint. A different transport label on the same bytes returned declared transport differs and left the stored bytes. A schema /1 record returned unknown schema, wrote false. propose on the live work book returned live work book is not a fixture. A junction created with mklink /J returned unsafe path, and the test removed the junction. A producer copy with one flipped byte returned pin mismatch and did not launch. The file-symlink refusal did not run.

## Overflow (parked)

Schema /1 books stay with pass02. This module does not migrate them and does not repair a pass03 page that is already torn. V01 through V03 stay with the later checker. Descriptor packaging H2 stays out of this slice. No reserved-exposure gate is added. The post-commit pack-file refusal on record-review stays. repo_root() stays parents[2]. No capture slot and no 0184 allocation are opened here. The claim covers the injected write failures in FAILURE.md. It does not extend to a killed process, a disk failure, or a race.

## Unprompted

Stop for Codex Prime. The next bounded action is that review. App integration, live migration, and another pack are not started by this suite.
