# PRIME-USE — 0511.workflow-colab/05.04

Interpreter: C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe
Python 3.14.0. Commands run with python -B from D:\Git\lib-build.
Environment: PYTHONDONTWRITEBYTECODE=1.

## Recorded suite

python -B labs/colab-workflow-pass03/tests/run_suite.py

Saved exit 0 at 00.kernel/00.00.10.work/0511.workflow-colab/evidence/build05.04/runs/20261101T211832Z.
Leave that directory in place. The runner does not clear a previous run.

The suite starts labs/colab-workflow-pass03/tests/test_pass03.py, then labs/colab-workflow-pass03/tests/test_real_two_pass.py. A non-zero child exit makes the aggregate exit 1, and the earlier child's output stays.

test_pass03.py is the synthetic child. Tests that replace the producer process say they are synthetic. Recorded child exit 0. Executed 10, skipped 1, failed 0. The skip is test_symlink_refusal, WinError 1314. No symlink was created and no privilege was requested. The junction refusal is inside test_interrupt_attach_and_links, and that test passed.

test_real_two_pass.py leaves the producer process unset and calls the pinned v2 verifier. It copies 00.kernel/00.00.10.work/0511.workflow-colab/evidence/real-producer-v2-05.03 into a temporary directory. Recorded child exit 0. Open, attach 05.01, seal an LF return, request-next 05.02, open-pass, preview, prepare, attach 05.02, seal a CRLF return, finish review. Digests 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184 and 933171c1201b91ddf8f87a00179ec23a3fe83dcc0ce440cd6614b68494af4b0e. Actions: open, attach, seal-return, review, open-pass, attach, seal-return, review. The source envelope hash matched before and after.

Stored suite.stdout and suite.stderr are LF. The Windows runner wrote 29 CR on stdout and 0 CR on stderr. newlines.txt records that conversion. Text and exit are unchanged. suite.stderr is empty. suite.exit is the text 0 and a newline.

## What the suite holds

Page-local seal stores the supplied file bytes at artifacts/<pass>/return.md and at 05.NN.return.md. Identical replay adds no transition. Different bytes refuse occupied different content. A different label on the same bytes refuses declared transport differs and leaves the stored label. An N1 place-return leaves open-pass at local return required. Injected write failures leave partial.json, reason interrupted write, wrote true, and a later command returns resume refused. A one-byte producer copy returns pin mismatch and does not launch.

## Limits

CONTRACT.md sha256 8b05292bcee82877975519ae9473a2cf0a7feb8888dc966fda50161cfc7d8273, 10094 bytes, and FAILURE.md sha256 3cca7a114d630b9b12159701285904f863e6423221968e00e8acf8feb2d1c4df, 3691 bytes, stay as written before the saved commands. The place-return fact-key correction is inside that contract hash and predates the commands.

Pass02 remains the reader for schema colab-exchange-investigation/1. Pass03 refuses that schema. Show JSON, 01.md, and 08.md differ from pass02 where the contract says they do. The checkpoint compares the loaded seal with the loaded record. A rewrite that recomputes every transition hash and the seal passes show. There is no cleanup command. The file-symlink refusal did not run. Custody on 0111.workflow-colab stays pending. No receipt was written. 0184 was not allocated. No capture slot was opened. accepted is false. Exit 0 is not Prime review, seating, or app activation. Do not point the app, the door, the loop, or the cycle at pass03 from this page.
