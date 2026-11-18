# Interface delta — 0522.review-construction/05.07

Predecessor labs/review-construction-pass03/construct.py sha256 6eec5653c6818cfdeb98ffcd929cdf26f0ddf15c3121c703ce795abea6eb755d, 42216 bytes.
Successor labs/review-construction-pass04/construct.py sha256 6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20, 42582 bytes.

Envelope schemas review-construction/1 and review-construction/2 are unchanged. supplied-review-state/1 keys are unchanged. Bind inputs are unchanged. Result schemas review-construction-result/1, review-task-binding/2, review-construction-show/1, and review-target-inspection/1 are unchanged. ROOT stays the literal checkout path.

The task_binding line is now the first located line matching `task_binding: ` plus 64 lowercase hex digits after a split on the separator newline_of already chose. inspect and show both use that split. Section hashes stay hashes of the original located bytes.

On LF, show stdout stays byte-identical to pass03. On CRLF, show returns the binding the renderer wrote. pass03 show of that same CRLF section still exits 2.

A supplied enum that is an array, object, null, number, boolean, or unknown text raises Refusal. The CLI prints `refused:` and exits 2. preview writes nothing.

No cycle, loop, door, or app command is changed. This page does not select pass04.
