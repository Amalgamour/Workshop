# PRIME-USE — 0511.workflow-colab/05.05

Interpreter: C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe
Python 3.14.0. Commands run with python -B from D:\Git\lib-build.
Environment: PYTHONDONTWRITEBYTECODE=1.

CONTRACT.md sha256 e9d4d5e34ac8703aa3b1c2e22b83e54d592c7227c951629ce2ba30f0006347ba, 8996 bytes. FAILURE.md sha256 79b6b116b1be112684ec9cae1d0751762acbcdd992eea0e4b313cb1ed4c3e055, 5186 bytes. Both predate the recorded commands. labs/colab-workflow-pass04/colab_workflow.py sha256 8ec953c503edbb9a890216b3cdb6630062967c7c4113fbd9b9304ace83bc9d7d, 74884 bytes. Pass03 stays fc469af91f8bdcbaa980457535b7276a5c4e2421a81ad861e93ff750a511c944, 68410 bytes, and still truncates authority files in place.

## Recorded reproduction of WF01

python -B 00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.05/reproduce/run.py

Saved at 00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.05/reproduce/runs/20261101T221040Z. Leave that directory in place. The script creates a new UTC directory on a later run and does not clear the recorded one.

The script loads labs/colab-workflow-pass03/colab_workflow.py by file path. It opens page 0797.wf01 in a temporary book whose prefix is 0511-0505-wf01-. The note bytes are `# Notes` and a newline. The open request is schema colab-exchange-open/1, target id T01, source commit 6896224510fe0bcebac291fce7ed311a2cd085cb, path subj/note.md, repository workshop. It then commits that same loaded record. The injection wraps os.open and os.write. The first write to the page-root investigation.json writes half of the buffer, rounded up to at least one byte. The second write sets a done flag and raises OSError. The done flag keeps a later recycled file descriptor from raising again inside the partial-marker write. This is a controlled partial write. It is a process injection, and the claim covers that injection.

Runner exit 0 records the defect. Recorded outcome Refuse: interrupted write. Before 760 bytes. After 380 bytes. prior_record_intact false. old_seal_intact true. partial_marker true. checkpoint_dir false. calls 2. summary.json schema colab-workflow-wf01-reproduction/1. The saved files are summary.json, prior-investigation.json, torn-investigation.json, and seal.json. Pass03 was not patched. Prime's earlier fixture, 768 bytes to 384 bytes, is a different page and stays in evidence/prime-review05.04.

## Recorded successor suite

python -B labs/colab-workflow-pass04/tests/run_suite.py

Saved exit 0 at 00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.05/runs/20261101T221100Z. Leave that directory in place.

The runner starts labs/colab-workflow-pass04/tests/test_pass04.py, then labs/colab-workflow-pass04/tests/test_real_two_pass.py. A non-zero child exit makes the aggregate exit 1, and the earlier child's output stays.

test_pass04.py stubs the producer. Recorded child exit 0. Executed 9, skipped 1, failed 0. The skip is test_symlink_refusal, WinError 1314. No symlink was created and no privilege was requested. The junction refusal is inside test_legacy_live_and_links, and that test passed.

test_real_two_pass.py leaves the producer process unset and calls the pinned v2 verifier. It copies 00.kernel/00.00.10.work/0511.workflow-colab/evidence/real-producer-v2-05.03 into a temporary directory. Page 0701.colab-exchange-layout. Recorded child exit 0. Digests 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184 and 933171c1201b91ddf8f87a00179ec23a3fe83dcc0ce440cd6614b68494af4b0e. Actions: open, attach, seal-return, review, open-pass, attach, seal-return, review. The source envelope is not a write target.

Stored suite.stdout and suite.stderr are LF. The Windows runner wrote 28 CR on stdout and 0 CR on stderr. newlines.txt records that conversion. Text and exit are unchanged. suite.stderr is empty. suite.exit is the text 0 and a newline.

## Pass04 failure shape

An identical recommit of the open record on pass04 refuses publication collision, wrote false, before the lock and before any checkpoint. That call is the pass03 reproduction shape. It is a collision on pass04. The successor mid-write is a later seal whose candidate bytes differ.

The synthetic books below are removed with each test. Rerun python -B labs/colab-workflow-pass04/tests/test_pass04.py to recreate them. The pages are:

- 0721.wf01. Identical recommit refuses publication collision and leaves the root pair. The following seal of the bytes `kept` and a newline fails during the staged investigation.json write. The root pair and checkpoints/<that seal sha256>/ stay the pre-seal pair. partial.json predecessor is retained-prior.
- 0722.open. The first open fails during the staged investigation write. No investigation.json, no seal.json, and no checkpoints directory. partial.json predecessor is none.
- 0723.replace. REPLACE_HOOK raises before the page-root investigation.json replace. The root pair and the checkpoint stay the prior pair.
- 0724.seal. REPLACE_HOOK raises before the page-root seal.json replace, after the investigation replace. The root investigation is the candidate. The root seal is the prior seal. The checkpoint is the prior pair, and its transition list omits the failed action.
- 0725.proj. A second-pass seal fails during the staged 08.md write, before that projection is replaced. The live 08.md and the root pair stay. The 05.01 artifact, pack, review, and page-local return stay hash-identical.
- 0726.two. A second-pass seal fails during the staged investigation write after 05.01 has a package, a page-local return, and a review. The root pair and the checkpoint match the pre-seal pair. The retained record still has passes.05.02.return null. The 05.01 bytes stay hash-identical. Deleting only partial.json leaves the page partial, because attempt.json remains. The next seal returns resume refused, wrote false.
- 0727.keep. The open publication says predecessor none and has a .published marker. No checkpoint exists yet. Planting checkpoints/<current investigation sha256>/ makes the next attach refuse checkpoint collision, wrote false, with the planted bytes kept and no partial.json. After that plant is removed, attach and seal succeed. An identical seal returns repeat, wrote false, and adds no checkpoint. A different transport label on the same bytes returns declared transport differs and leaves the stored bytes. open-pass before a request returns next pass not requested. After request-next, open-pass adds one open-pass transition. A CRLF return stays CRLF in the artifact and in 05.02.return.md. A directory checkpoints/ followed by 64 f characters is ignored by show. The title stays Exchange question.
- 0728.hook. WRITE_HOOK raises before the staged investigation.json is opened. The root pair and the checkpoint stay. The staged investigation file is absent. Projections are replaced before that staged record write, so 08.md may already name the new return while the root pair is still the prior pair.
- 0728.legacy. A schema colab-exchange-investigation/1 record with a matching seal returns unknown schema, wrote false.
- 0729.sym. The file-symlink refusal did not run.
- 0730.pin. A producer copy with the last byte flipped returns pin mismatch, wrote false, and does not launch.

propose on D:\Git\lib-build\00.kernel\00.00.10.work returns live work book is not a fixture. A junction created with cmd mklink /J returns unsafe path, and the test removes the junction.

A failed interrupted command returns refused, reason interrupted write, wrote true. show then reports partial true, passes [], transitions null. The show result name can still be complete. That name means the read finished.

## Inspection

Stop. Leave partial.json, attempt.json, and every checkpoint in place.

1. If partial.json, attempt.json, and .write.lock are all absent, and seal.json is schema colab-exchange-seal/1 whose sha256 equals the sha256 of investigation.json, that root pair is the current authority. Ignore every checkpoints directory.
2. Otherwise read attempt.json. Its retained_checkpoint is the only prior id. Open checkpoints/<that id>/ only. Verify identity.json schema colab-exchange-checkpoint/1, role retained-prior, and that checkpoint_id, investigation_sha256, and seal_sha256 are the same digest. Verify the investigation file hashes to that digest and the seal file's sha256 field equals it.
3. If predecessor is none, there is no prior sealed pair to copy aside.
4. Copying the checkpoint pair back onto the page, or deleting partial.json or attempt.json, is a later Prime decision. This tool does neither. There is no recover command and no cleanup command.

While attempt.json exists, the root pair is an unfinished publication even when the bytes look complete. A torn 08.md is rebuilt, if Prime chooses, from the retained investigation record and the artifact return bytes. The tool does not rewrite that projection during inspection.

Current, previous, and partial identities are the root pair, the checkpoint id named by attempt.json, and partial.json. Selection is that named id. The tool does not choose the highest version.

## Limits

Pass02 remains the reader for schema colab-exchange-investigation/1. Show JSON on a loaded page stays the pass03 shape. A rewrite that recomputes every transition hash and the seal still passes show. The file-symlink refusal did not run. Custody on 0111.workflow-colab stays pending. No receipt was written. 0184 was not allocated. No capture slot was opened. accepted is false. Exit 0 records the command. Prime review, seating, and app activation remain with Codex Prime. Do not point the app, the door, the loop, or the cycle at pass04 from this page. The claim stops at the injected write failures above. AR-01 stays held.
