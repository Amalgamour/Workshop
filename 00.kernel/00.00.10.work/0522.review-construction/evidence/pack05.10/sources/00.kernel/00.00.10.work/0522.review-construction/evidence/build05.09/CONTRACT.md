# CONTRACT — review-loop app entry v3
date: 2026-11-01
who: Grok-1
state: implementation contract for 0522.review-construction/05.09, written before the v3 door and the librarian selection
reviewer: Codex Prime

This is the app-entry delta from the selected v2 door. It follows reviewed L1 on 0522/05.08 and the reviewed absent-target coverage on 0707/05.07 and 0707/05.08. It does not revise evidence/build05.08/CONTRACT.md. It does not edit a lab module.

accepted is false. authority is none. custody is not-established. This builder does not commit. A result from this door is not release, acceptance, filing, or a live review.

## Selection
Before this slice, app/librarian.py loads app/review_loop_tools_v2.py, module name librarian_review_loop_tools_v2, declaration app/review-loop-v2.json. That declaration's review_loop pin is labs/review-loop-pass02/review_loop.py. Its construct pin is labs/review-construction-pass02/construct.py.

After this slice, the review-loop branch loads app/review_loop_tools_v3.py, module name librarian_review_loop_tools_v3, declaration app/review-loop-v3.json. Every other librarian command stays on its existing branch. The module docstring that does not name v2 stays.

Rollback, not performed here: point that one branch back at review_loop_tools_v2.py and librarian_review_loop_tools_v2, and restore the review-loop section of app/README.md from evidence/build05.09/before/README.md. Leave the v3 files on disk. Do not delete them to manufacture a green tree.

## Schema
The declaration schema stays review-loop-pins/2. The version stays 1. v3 is a file successor name, not a new kernel grammar. Top keys stay schema, version, _note, and tools. Each tool object stays path, sha256, and bytes.

The tool key set is not the v2 set. One key named construct cannot name both constructors. The keys are:

- construct_pass04. labs/review-construction-pass04/construct.py sha256 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20, 42582 bytes. This is the loop's direct inspect, apply, show, and pre-apply bind. The loop's own pin_set calls this file construct.
- construct_pass02. labs/review-construction-pass02/construct.py sha256 b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc, 36188 bytes. This is the unchanged cycle's bind. This door does not launch it and does not substitute it for pass04.
- prime_cycle_pass03. labs/prime-cycle-pass03/prime_cycle.py sha256 496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c, 76045 bytes.
- prime_review_pass01. labs/prime-review-pass01/prime_review.py sha256 805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0, 58324 bytes.
- prime_review_pass02. labs/prime-review-pass02/prime_review.py sha256 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e, 58560 bytes.
- return_inspect. labs/return-capture-pass01/return_inspect.py sha256 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b, 11402 bytes.
- return_lines. labs/return-lines-pass01/return_lines.py sha256 863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a, 100897 bytes.
- return_placement. labs/return-placement-pass01/return_placement.py sha256 db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754, 66097 bytes.
- review_loop. labs/review-loop-pass03/review_loop.py sha256 47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b, 55474 bytes. This is the only module the door launches.

The declaration and the Python TOOLS table must be the same path, sha256, byte length, and key set. A mismatch refuses before launch.

labs/review-loop-pass02/review_loop.py sha256 8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7, 47189 bytes, stays the reproduce delegate inside the pass03 loop. This door does not pin it and does not expose reproduce. labs/colab-workflow-pass04/colab_workflow.py sha256 8ec953c503edbb9a890216b3cdb6630062967c7c4113fbd9b9304ace83bc9d7d, 74884 bytes, is not selected.

## Commands
The allowlist stays describe-legacy, prepare, record, render, read, and recover. describe-legacy takes --book and --member and stays read-only. The other five take --fixture-root and --request. record also takes --decision.

reproduce is refused as a lab command that is not an app command. run is refused. capture, reserve, draft, and a caller executable, module, pins, destination, or tool flag are refused. There is no highest-version discovery and no caller-selected Python.

A fixture root must be an absolute directory outside D:\Git\lib-build and outside the live work book. A linked declaration or tool path is not followed. A missing file, a hash mismatch, or a size mismatch refuses before the subprocess. The subprocess is the current Python executable, argument -B, the pinned review_loop path, and the forwarded arguments. cwd is the code root. shell is false. PYTHONDONTWRITEBYTECODE is 1. The door copies the integer exit. It does not capture or rewrite the loop's stdout or stderr.

Wrapper refusals from librarian.py print stop: and exit 2. The loop's own refusal still prints refused: and keeps its exit. A render-conflict exits 2 and does not print refused:.

## Result
The loop's stdout is forwarded. The result schema is review-loop-result/2. This door does not reimplement mechanical state. current.next_action_label is supplied. Top-level next is mechanical.text. supplied_next_action is the supplied action, or null. Flags stay accepted false, authority none, custody not-established, allocated false, closes_work false, releases_action false, and authenticates_actor false.

Absent before prepare: the reviewed loop returns target.state absent, view.template null, mechanical state awaiting-review, blocker target-absent, route none-in-this-entry, and the text "No judgment is recorded. The target is absent, so this entry does not commit one." The target is not recreated. No decision is invented here.

Removed before record: after a real decision from a present target, an absent target refuses before the cycle with "target file is absent; the cycle did not commit this decision". The decision bytes stay. This door does not add a second lifecycle.

A24 stays MANUAL. A disposable declaration or planted-file mismatch is a declared-pin test. It is not the relocated-checkout altered-construct experiment.

where and validate stay on their existing librarian branches and stay read-only in the focused check. This door does not call them.

## References for a later registration
This slice does not invent or edit an N3NN address. A later registration can point at:

- 00.kernel/00.00.10.work/0522.review-construction/05.08.md and evidence/build05.08/CONTRACT.md
- 00.kernel/00.00.10.work/0522.review-construction/05.09.md and this file
- the nine pins above
- 00.kernel/00.00.10.work/0707.app-use-check/05.07.return.md and its Prime review
- 00.kernel/00.00.10.work/0707.app-use-check/05.08.return.md and its Prime review
- 00.kernel/00.00.10.work/0511.workflow-colab/05.05.md, recorded as not selected

Matching line 0122.review-construction stays pending. No receipt is written. The current-assignment record is not repaired.
