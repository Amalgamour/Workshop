# Integration walkthrough for 0511.workflow-colab/05.03

schema: colab-exchange-walkthrough/1
status: record of the exchange runs. Not acceptance.

## Commands
Working directory D:\Git\lib-build. Interpreter C:\Users\misg\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe. Environment PYTHONDONTWRITEBYTECODE=1.

```text
python -B labs/colab-workflow-pass02/tests/test_exchange_workflow.py
python -B labs/colab-workflow-pass02/tests/test_real_handoff.py
```

The unit command stubs the producer process. The handoff command is the producer proof. It calls the pinned v2 verifier and the accepted intake. It does not call handoff_check.py. The verifier stdout contains a temporary path, and neither command stores that stdout.

## Unit transcript
```text
ok test_band_and_paths
ok test_attach_notes_and_review
ok test_routes
ok test_custody_refusals
ok test_interrupt_and_links
skip test_symlink_refusal: WinError 1314
ok test_bad_producer_pin
ok test_source_text
executed 7
skipped 1
failed 0
```

Exit 0. The skip is file-symlink creation, WinError 1314. The junction refusal is inside test_interrupt_and_links, and that test passed.

test_band_and_paths opens a source path 00.kernel/00.00.10.work/0411.colab/01.md, leaves a source file 07.md off the emitted page, refuses kind id as unsupported section id, leaves a heading that exists only inside a fence unresolved, and opens a real heading plus one fenced copy of the same heading. test_routes uses four pages: hold, finish, request-next with next pass 05.02 and no 05.02.pack.md, and route-n5nn. A finish with a held finding refuses unresolved findings. A missing director reply refuses director reply required. One occupied pass is not asked to change route.

## Handoff transcript
```text
v1-before exit 0 result 4507760c3b374d89add77d66a02dc5df437dd7c2f4d1214e09ff309381cd2da3 extra 83008
open exit 0 result complete extra 0701.colab-exchange-layout
attach exit 0 result complete extra 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184
stored exit 0 result package/05.01.pack.md extra b46713a78cea87597d04578949d21f4539518133ff58a8c007377fb222ea5a29
stored exit 0 result package/06.01.notes.md extra 2d7fe940fcfbd2a9b88c655ebbbd3f113c290182a18e8f875c2c10758c5349f9
stored exit 0 result package/colab-request.json extra 5778b69507ff4eadd67e0b3eb2bdb3aa7d22440110d1ddb16e09b5e5e7c0b1fa
stored exit 0 result package/binding.json extra d6bfabb615200c91009deb8631bd834c52286037aae2cfb14e5827f49a1a81b1
stored exit 0 result package/snapshots/0001.blob extra 1cff00588bde14723b7058aa3698a30eb727a3632892bb8ad7029b4d049617d9
stored exit 0 result prepared-colab.zip extra 5f77b08318a40b9329f51a9178e274637271d1cf06d4aa3e9e1ea3c354862cfe
repeat exit 0 result repeat extra False
note exit 0 result complete extra True
show exit 0 result False extra None
wrong-digest exit 2 result stale expected hash extra False
wrong-origin exit 2 result wrong origin extra False
hc01 exit 2 result conflicting bytes extra 0799.wrong-investigation
tampered exit 2 result conflicting bytes extra None
missing-verification exit 2 result malformed package extra None
extra exit 2 result conflicting bytes extra None
evaluator exit 2 result conflicting bytes extra None
bad-producer exit 2 result pin mismatch extra False
bad-helper exit 2 result pin mismatch extra False
interrupt exit 2 result interrupted write extra True
resume exit 2 result resume refused extra None
reserve exit 0 result 0101.colab-fixture-0501 extra reserved
intake exit 0 result captured extra None
place exit 0 result complete extra 0101.colab-fixture-0501
review exit 0 result complete extra hold
held-show exit 0 result False extra route=hold;explicit_finish=False;review_pending=True;held=True
return-bytes exit 0 result a74e4ade57f6c1ea369f41a799fae8a30598ce779e005dccbca0e31a13a51ee7 extra 180
v1-after exit 0 result 4507760c3b374d89add77d66a02dc5df437dd7c2f4d1214e09ff309381cd2da3 extra True
envelope exit 0 result unchanged extra True
handoff exit 0
```

Exit 0.

## How to read the handoff columns
Each row is `{step} exit {code} result {result} extra {extra}`.

v1-before: result is the sha256 of labs/colab-workflow-pass01/colab_workflow.py. extra is its length, 83008. v1-after repeats that sha256. extra True means the after hash equalled the before hash.

stored: result is the artifact path under the pass directory. extra is its sha256. Each stored file also matched the envelope bytes.

repeat: extra is wrote, and the value is false. note: extra is wrote, and the value is true. The launch snapshot bytes stayed the package notes.

show: result is wrote, and the value is false. extra is empty. The run also required that 00.live.md was absent.

wrong-digest and the pin rows: extra is wrote, and the value is false. wrong-origin: extra false means the other page grew no artifacts directory.

hc01: extra is the page written into the copy of handoff.json. The real envelope was not edited. Full verify rejected that copy. The standalone checker was not run.

interrupt: extra is wrote, and the value is true. resume did not launch.

reserve: result is the member name. intake: result is the producer intake result. place: extra is the same member. return-bytes: result is the sha256 of the placed file, and extra is its length, 180. Those bytes are the labelled fixture return. They are not a model result.

held-show: result is wrote, false. extra lists route, explicit_finish, review_pending, and held. A hold is pending. It is not approval.

envelope: result unchanged and extra True mean every file under the accepted envelope had the same sha256 after the run as before it.

## What the passing handoff checked
The demonstration book was a new temporary directory. The door 0700.band.colabs/01.md was written by the fixture as `Door only. Not an investigation.` and those bytes were the same at the end. The workflow did not receive the live book path as `--book`. Other refusal books in the same temporary directory were removed with it.

Open used `--closure` on evidence/real-producer-v2-05.03. Page 0701.colab-exchange-layout. Pass 05.01. Result complete.

Attach used `--output` on that envelope, a local colab-config/2, and `--expect-digest` 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184. Result complete. The stored pack, notes, request, binding, snapshot, and ZIP matched the envelope. verification.json matched the envelope bytes. provenance.json did not contain the config path, the text colab-config, or a drive-letter path. The page listing had no handoff.json, no assembler-request.json, no assembler-run.json, no evaluator file, no 07.md, and no filename ending in .colab. Both templates still said THIS IS A TEMPLATE. Return and review did not exist yet.

The second attach was result repeat and wrote false. An append kept the launch snapshot and the package digest. show wrote false.

`--expect-digest` of 64 zeros was stale expected hash. A second disposable book opened 0702.other-question from the snapshot bytes, then attach of the intact envelope was wrong origin.

A copied envelope whose only handoff.json change was investigation.page set to 0799.wrong-investigation was conflicting bytes. A copied snapshot with one added byte was conflicting bytes. A copied envelope with verification.json removed was malformed package. A copied package/EXTRA.md was conflicting bytes. A copied evaluator/secret.md containing EVALUATOR-SECRET-NOT-FOR-PACKAGE was conflicting bytes, and that token was absent from the investigation page.

A producer copy with the last byte flipped, and a helper copy with the last byte flipped, were pin mismatch. The launch hook was not called.

An attach whose artifact write raised left partial.json, wrote true, and reason interrupted write. The next attach was resume refused and left investigation.json unchanged.

Reserve used the accepted helper. Submission fixture-exchange-0503. Name colab-fixture-0501. Origin book 00.00.10.work, page 0701.colab-exchange-layout, batch 05.01. Member 0101.colab-fixture-0501. The return file says it is a labelled fixture and is not a model result. Producer intake result was captured, exit 0. place-return wrote those exact bytes as 05.01.return.md. 08.md names the member and does not contain the return body.

The review record is a supplied fixture. F01 is consequential, held, pending, and bound to T01. The director reply is `hypothetical-fixture: Keep the return bytes exact.` The rendered review contains that line. It does not copy the layout contract's Director quotes. Route hold. No 05.02.pack.md was created. The return bytes were unchanged by the review. The later show had wrote false, explicit_finish false, review_pending true, and held true.

## Limits
The receipt on the later capture is custody. This walkthrough does not approve, accept, seat, or publish the integration. The smallest later action is that Prime independently runs the disposable invocation. That step leaves 00.live and app/librarian.py unedited.
