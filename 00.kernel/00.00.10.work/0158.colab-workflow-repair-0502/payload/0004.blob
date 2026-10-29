# Integration walkthrough for 0511.workflow-colab/05.02

schema: colab-workflow-walkthrough/1
status: record of the repaired runs. Not acceptance.

## Commands
Working directory D:\Git\lib-build. Interpreter C:\Users\misg\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe. Environment PYTHONDONTWRITEBYTECODE=1.

```text
python -B labs/colab-workflow-pass01/tests/test_colab_workflow.py
python -B labs/colab-workflow-pass01/tests/test_real_handoff.py
```

This continuation ran the unit suite again on the current colab_workflow.py. Exit 0. The handoff command was not run again. The handoff transcript below is the stdout of the completed disposable run from the repair. That run printed handoff exit 0 only after its checks passed. This continuation did not edit colab_workflow.py before the unit rerun.

## Unit transcript
```text
ok template
ok schema rules
ok band and open
ok band refusals
ok conflicts and second pass
ok targets and sources
ok malformed
ok package attach
ok statements and close
ok reconciliation
ok show and live
ok interrupt
ok junction
skip file symlink: WinError 1314
ok pin
ok custody
executed 15
skipped 1
failed 0
```

Exit 0. The skip is file-symlink creation, WinError 1314. The junction refusal passed.

The row ok targets and sources covers a source path 00.kernel/00.00.10.work/0411.colab/01.md, a source file subj/07.md whose page listing has no 07.md, kind id refused as unsupported section id, a heading that exists only inside a fence left unresolved, and a real heading plus one fenced copy of the same heading opened. The row ok package attach refuses the 05.01 synthetic directory as legacy package without launch, then legacy-diagnose exits 0 with result legacy, wrote false, and label legacy-synthetic-05.01.

## Handoff transcript
```text
open exit 0 result complete extra None
attach exit 0 result complete extra a4b91dd63d2f7b845d1ee43ad3a3da63253851231cb79659c0fdaed6fc46d7c4
repeat exit 0 result repeat extra False
show exit 0 result False extra None
wrong-digest exit 2 result stale expected hash extra None
wrong-origin exit 2 result wrong origin extra None
tampered exit 2 result conflicting bytes extra None
missing-envelope exit 2 result malformed package extra None
extra exit 2 result conflicting bytes extra None
evaluator exit 2 result conflicting bytes extra None
bad-producer exit 2 result pin mismatch extra None
bad-helper exit 2 result pin mismatch extra None
interrupt exit 2 result interrupted write extra True
resume exit 2 result resume refused extra None
reserve exit 0 result member 0101.colab-fixture-0501
submission fixture-0701-0501
result reserved extra None
intake exit 0 result captured extra None
return-pointer exit 0 result complete extra 0101.colab-fixture-0501
pending exit 0 result False extra True
close exit 0 result complete extra None
explicit exit 0 result True extra True
handoff exit 0
```

Exit 0. The reserve row is one report row. The helper stdout contains newlines, so it prints as three lines.

## How to read the handoff columns
Each row is `{step} exit {code} result {result} extra {extra}`.

show: result is wrote, and the value is false. extra is empty. The run also required that 00.live.md was absent.

pending: result is explicit_completion, and the value is false. extra is review_pending, and the value is true. That show also required held_followup and custody_complete.

explicit: result is explicit_completion, and the value is true. extra is review_pending, and the value is still true.

attach: extra is the digest. repeat: extra is wrote, and the value is false. interrupt: extra is wrote, and the value is true. return-pointer: extra is the member name.

Before the printed close row, the run required an explicit false closure to refuse with reason explicit close required. That refusal has no printed row. The process still printed handoff exit 0.

## What the passing handoff checked
The book was a new temporary directory. The door 0700.band.colabs/01.md was written by the fixture as `Door only. Not an investigation.` and those bytes were the same at the end. The workflow did not receive the live book path as `--book`.

Open used `--closure` on evidence/real-producer05.02. Page 0701.colab-compute-ops. Pass 05.01. Result complete. The page listing contained no 07.md.

Attach used `--output` on that envelope, a local colab-config/1, and `--expect-digest` a4b91dd63d2f7b845d1ee43ad3a3da63253851231cb79659c0fdaed6fc46d7c4. Result complete. These stored files matched the envelope bytes and these sha256 values:

- package/colab-request.json 460e8ef45e5095e1af91133a475524a727d4aa21a4d3d1d84801bc0d5e2a3e25
- package/binding.json e1311900743bde2274e9ceb729150673fb815d9d47320602d4de71ada1136a21
- package/snapshots/0001.blob 1a9b2ce890e1ab4078154ed26b218cdea7bf9d6624d06ca5b1d43dfb5f29e3e0
- verification.json 444094243dcd1c5cef418cd75e93543228167cefb7bded407715f33e82bec11d
- prepared-colab.zip f44c4bf1985ba893a4e09d80593438ac011cb1fe35d695a378c811ec41f44c60

The stored names had no evaluator/ prefix, no name ending in .colab, no 07.md, and neither assembler-request.json nor assembler-run.json. provenance.json did not contain the config path, the text colab-config, or EVALUATOR.

The second attach was result repeat and wrote false. investigation.json bytes stayed the same. show wrote false.

`--expect-digest` of 64 zeros was stale expected hash. A second disposable book opened 0702.other-question from the snapshot bytes named by package/source-manifest.json, then attach of the intact envelope was wrong origin and wrote no artifacts directory. A copied envelope with one added byte on package/snapshots/0001.blob was conflicting bytes. A copied envelope with verification.json removed was malformed package. A copied envelope with package/EXTRA.md was conflicting bytes. A copied envelope with evaluator/secret.md containing EVALUATOR-SECRET-NOT-FOR-PACKAGE was conflicting bytes, and that token was absent from the investigation page.

A producer copy with the last byte flipped, and a helper copy with the last byte flipped through a config that pointed only the helper at the copy, were pin mismatch. The launch hook was not called.

An attach whose artifact write raised left partial.json, wrote true, and reason interrupted write. The next attach was resume refused, did not launch, and left investigation.json unchanged.

Reserve used the accepted helper. Submission fixture-0701-0501. Name colab-fixture-0501. Origin book 00.00.10.work, page 0701.colab-compute-ops, batch 05.01. Result reserved. Member 0101.colab-fixture-0501. The return file says it is a labelled fixture and is not a model result. It includes the heading sections, the line `hypothetical-fixture: Keep review manual for now.`, and `Do not manufacture a number.` Producer intake result was captured, exit 0. The workflow return-pointer result was complete for that member.

F01 was supplied, consequential, and held, with followup later-colab, source binding T01, affected page 0411.colab, file 01.md, and a director reply labelled hypothetical-fixture. F02 was supplied, not consequential, and then rejected. The review statement text was PENDING. The pending show had explicit_completion false, review_pending true, held_followup true, and custody_complete true. After both dispositions, a subject proposal for F01, and an explicit true closure, close was result complete. Stored actions were F01 held and F02 rejected. The later show had explicit_completion true and review_pending true.

Every file under the accepted envelope had the same sha256 after the run as before it. The temporary book was removed when the process left that directory.

## Limits
The receipt on a later capture is custody. This walkthrough does not approve, accept, seat, or publish the repair. G01 through G07 stay recorded on the Prime review. The smallest later action is that Prime independently runs the disposable invocation. That step leaves 00.live and app/librarian.py unedited.
