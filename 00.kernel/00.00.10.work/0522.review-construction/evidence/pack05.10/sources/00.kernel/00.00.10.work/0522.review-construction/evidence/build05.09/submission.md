# Submission — 0522.review-construction/05.09

## Did

Verified evidence/pack05.09/source-manifest.json before any door edit. Schema prime-pack-inputs/1, sha256 441a6e49fe683f10c6c064f905f05a6f24d033718125cc207a54620740b5a127, 51946 bytes. 136 rows, 0 bad, 0 missing, 1893984 live bytes. Each row's live bytes and snapshot bytes matched the declared sha256 and length. Recorded the invocation and the claim on 05.09 and in 06.17.md before the door. Wrote evidence/build05.09/CONTRACT.md before the selection. The draft at evidence/pack05.09/draft-before-finalization.md stayed sha256 fda6a613b3f5d33a6f2f5ed83800b984d0954bb312e7c3f251d9abcf6c102846, 4617 bytes.

Added app/review_loop_tools_v3.py, sha256 0a7960a279ece3d60cedc008698e6000a56c4f5d4f1e4029757053f40169dad9, 11540 bytes, and app/review-loop-v3.json, sha256 83184e4f3684a5a8eedf90e8b06b4f5aff9754de998927b9de389f3b12abb393, 2346 bytes. The declaration schema stays review-loop-pins/2, version 1. The door launches only labs/review-loop-pass03/review_loop.py. construct_pass04 is the direct constructor. construct_pass02 is the cycle bind and is not substituted for pass04. app/librarian.py loads this door for the review-loop command only. app/README.md documents that door in the review-loop section. The text before that section is unchanged.

The app test is app/tests/test_review_loop_entry_v3.py, sha256 6ae5d5b46c1a660a958c8a1a36e15a2f879f130d7692bf874fd00e8f6febae6b, 38911 bytes. Cited run evidence/build05.09/runs/20261101T225355Z-b3e958a5: 13 tests, 0 failures, 1 skip, 26.747s, process exit 0. Calls go through app/librarian.py in fresh directories outside the checkout, except the labelled declared-pin test, which calls the door on a disposable code copy. The loop, both constructors, the cycle, both prime_review modules, the three readers, workflow pass04, and 0519.desk-app/05.01.md stayed at their frozen hashes. This builder did not commit.

## Blocked

Codex Prime has not reviewed this pack. accepted is false. committed_by_this_builder is false. Matching line 0122.review-construction stays pending. No receipt was written. No 0122 slot was added. No N3NN address was created. The current-assignment record was not repaired.

A24 stays MANUAL. The disposable pin tests are declared-pin mismatches. They do not replace the live construct file under a relocated checkout. test_linked_declaration_is_not_followed skipped with WinError 1314. That skip is not symlink protection. Workflow pass04 is not selected. The v2 entry test, the 05.08 lab suite, and the old app test mains were not run. No live-book write and no live-use pilot.

## Need

Codex Prime review of this app-entry wiring: the v3 selection, the two constructor pins, the forwarded result schema, and the disposable-book tests. After that review, a separately specified current-Prime live-use pilot is the next milestone. This page does not start it.

## Selection delta

Before this slice, the review-loop branch loaded app/review_loop_tools_v2.py and app/review-loop-v2.json. That declaration's launched loop is labs/review-loop-pass02/review_loop.py, and its construct pin is constructor pass02.

After this slice, the same branch loads app/review_loop_tools_v3.py and app/review-loop-v3.json. The launched loop is labs/review-loop-pass03/review_loop.py. The door checks nine pins, then runs the current Python executable with -B and that loop path. shell is false. Wrapper refusals print stop: and exit 2. The loop's stdout, stderr, and integer exit are copied. reproduce and run are refused. A fixture root inside the checkout is refused. Result schema review-loop-result/2 is forwarded. Top-level next is mechanical.text. current.next_action_label is supplied. accepted stays false.

app/librarian.py sha256 ce5c768ccd0268a2fab5b39157a5a06b0237e02b2b8b4c8b4659a2cbfa90a1da, 11037 bytes. The before-edit copy is the same length because the v2 and v3 names are the same length. The test checks that the only source change is those names. app/README.md sha256 39f0dd37fd881b1b12bdb34e45b173e0a32106f5d855f372d07468359d3a8a34, 30675 bytes.

## Declared pins

| Key | Path | sha256 | bytes |
|---|---|---|---|
| review_loop | labs/review-loop-pass03/review_loop.py | 47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b | 55474 |
| construct_pass04 | labs/review-construction-pass04/construct.py | 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20 | 42582 |
| construct_pass02 | labs/review-construction-pass02/construct.py | b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc | 36188 |
| prime_cycle_pass03 | labs/prime-cycle-pass03/prime_cycle.py | 496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c | 76045 |
| prime_review_pass01 | labs/prime-review-pass01/prime_review.py | 805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0 | 58324 |
| prime_review_pass02 | labs/prime-review-pass02/prime_review.py | 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e | 58560 |
| return_lines | labs/return-lines-pass01/return_lines.py | 863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a | 100897 |
| return_placement | labs/return-placement-pass01/return_placement.py | db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754 | 66097 |
| return_inspect | labs/return-capture-pass01/return_inspect.py | 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b | 11402 |

The declaration and the Python table agree. The loop's own result pin still calls pass04 construct. labs/review-loop-pass02/review_loop.py sha256 8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7, 47189 bytes, remains the reproduce delegate and is not an app command. labs/colab-workflow-pass04/colab_workflow.py sha256 8ec953c503edbb9a890216b3cdb6630062967c7c4113fbd9b9304ace83bc9d7d, 74884 bytes, is not selected.

Later registration can point at 0522/05.08, evidence/build05.08/CONTRACT.md, 0522/05.09, evidence/build05.09/CONTRACT.md, the nine pins, 0707/05.07 and its Prime review, and 0707/05.08 and its Prime review. 0511/05.05 is recorded as not selected. This slice does not create that address.

## Commands and exits

Command, from D:\Git\lib-build:

python -B app/tests/test_review_loop_entry_v3.py

Cited run 20261101T225355Z-b3e958a5. 60 calls. 42 exit 0, 6 exit 1, 12 exit 2. Process exit 0. The 6 exits of 1 are return_lines reserve, which the fixture allows. The 12 librarian exits of 2 are 4 wrapper refusals, 4 where/validate refusals before a config read, 1 absent-target record refusal, 2 blocked render and recover results, and 1 stale-target render refusal.

round-read exited 0. Top-level next was "Read the rendered review." supplied_next_action.text was "Pack one bounded correction for the disposable capture." again-recover exited 0 with render.result already-rendered and apply_called false. A22a prepare exited 0 with view.template null, route none-in-this-entry, and the no-record sentence. A22b record exited 2. stderr was "refused: target-absent: target file is absent; the cycle did not commit this decision". The decision hash was unchanged and no cycle file was written.

where and validate without --root exited 2 with "stop: missing --root". The same commands with an empty disposable root exited 2 with "stop: missing config" and left that directory empty.

## First failures

Neither run failed a test. 20261101T225253Z-26a12bed passed 13 tests in 26.533s and is preserved. Its process warned about a bytes literal. That warning is not a test failure. The cited run is the later file, after the literal was written as an explicit encode. No directory was deleted.

## Source before and after

Before-edit copies are under evidence/build05.09/before/. librarian.py was sha256 d07de8a7c6d0c2ecb03300c5a4aed1d2659122e4fdecd843431adafba715857b, 11037 bytes. README.md was sha256 f33cf04646fbc6841bea4a9e99a37841edbd3d9e04635f52297d0fca906b2b3c, 29833 bytes. Those working-tree bytes already differed from HEAD 960d20c5290656095df8457b1740d2d5e586b111 and matched the frozen pack. This slice did not revert them.

The v2 door stays sha256 e57f7aea3339dad60124f495d974282142902ee078d642230e2315b0c432a408, 11126 bytes. The v2 declaration stays sha256 1a3e12e0b3496a1e14dc07b34efcf0e789b9e38c61c9e6feccb92eac6afb72e3, 1892 bytes. The older door stays sha256 b77617c81e073449147c1171aa09bd3c9d4378ff737704ccceec2e3b0bfcecea, 6417 bytes. The older declaration stays sha256 bd3e917fc57ffcc435467cd90e6fa2d13fcf07e8233d1462772cc324365e2aae, 1089 bytes.

After the edits, the frozen pack's live check differs on app/librarian.py and app/README.md only. 134 rows still match. The snapshot was not rewritten.

## PRIME-USE and rollback

evidence/build05.09/PRIME-USE.md gives the prepare, record, render, separate-process read, and recover commands, and it marks the supplied sentence apart from the mechanical sentence. Rollback names review_loop_tools_v2.py and review-loop-v2.json, plus the before-edit README section. Rollback was not performed. The v3 files were not deleted.

## Factfind

Pass04 is the loop's direct bind and renderer. Pass02 is still the cycle's bind. On the cited fixture the result pins named pass04 as construct and pass03 as review_loop. A blocked render of the 0519 page copy kept disposition held and did not change the copied page. The live 0519 page stayed sha256 b72c8aa0dcede36d72cb5d1ebcf3aadc7e6cf82798eb5f8db700df467e819104, 16129 bytes.

## Hostile

Exit 0 is not acceptance. The supplied next and the mechanical next are both present after a successful render, and they are different sentences. The declared-pin refusal does not prove the A24 altered-file case. The symlink skip does not prove link refusal on this machine.

## Overflow

Live review, assignment repair, N3NN registration, workflow adoption, and the live-use pilot stay outside this slice.

## Unprompted

The old door remains loadable by restoring one branch in librarian.py. The one next bounded step is Codex Prime's review. The artifact manifest lists the files for this return and excludes itself. Its hash is written on 05.09 after this submission is frozen.

## Verification

evidence/build05.09/verification.json records the pre-edit pack count, the two expected post-edit drifts, the contract hash, the cited run, and the preserved run. CONTRACT.md sha256 b77507e66d3c35ccd3ccc9b6c265c7407f2f746f79eaa9c4b93d4af1daf85f19, 7137 bytes, was not revised after the commands. HEAD is still 960d20c5290656095df8457b1740d2d5e586b111 on workshop. The Git index was empty. Python 3.14.0.
