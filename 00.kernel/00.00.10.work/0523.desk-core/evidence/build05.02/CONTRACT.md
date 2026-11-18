# CONTRACT — desk-core/2 repair
date: 2026-10-31
who: Grok Build (xAI)
state: repair contract; not production law

## Compatibility
`desk-core/1` task and review preimages stay recomputable.
New writes use `desk-core-task/2`, `desk-core-task-binding/2` and
`desk-core-review-binding/2`. A version 1 hash is not treated as a version 2
hash. Books are still explicit disposable directories outside this checkout.
`return-capture/1` is still not called. `app/librarian.py` stays unchanged.
Runtime dependency: Python standard library only.

## Platforms
Target: Windows Python 3.12+ and Linux.
This repair is executed on Linux with Python 3.11.2 as the permitted
supplementary cloud check. Windows Python 3.12+ is pending Prime.
No runtime is installed. An untested platform is not reported as passed.

## Portable I/O
`file_lock` uses `fcntl.flock` on POSIX and `msvcrt.locking` (one byte,
blocking `LK_LOCK`) on Windows. It does not substitute a no-op on Windows.
Both are advisory. They are not OS isolation and not race freedom.
`atomic_write` and `exclusive_write` open with `O_BINARY` where that flag
exists, and they loop until the whole buffer is written.
`atomic_write` uses `O_CREAT|O_EXCL` for `name.tmp`. An existing temporary
file is refused with `temp-occupied` and is not truncated.

## Placement
A source page is four digits. Digit 0 is the workflow prefix N and is kept.
Digit 1 is the band. The last two digits are NN.
Band 5 maps to return prefix `N` + `1` + NN, same subject.
Band 7 stays on that page (`05.PP.pack.md`, `05.PP.return.md`, `06.PP.review.md`).
Any other band, including band 1, is refused. No second subject is written
onto an occupied return number.

## Binding
Version 2 task binding hashes schema, page, subject, pass, kind, title, body,
expected outputs, scope, agreement and declared evidence.
Equal text at two source addresses does not share a binding.
A review binds that task binding, the receipt hash, the receipt's captured
task binding, agreement, evidence, source identity and the review identity.
A review is fresh only when the receipt's captured task binding, the release
and the claim all match the current task. Otherwise the next action stays
derived and is not taken from the review.

## Revision
`revise-task` requires `reason` and `authorizing_reference` supplied by the
caller. The tool does not invent a Director decision.
Before replacement it stores the exact prior task and face bytes under
`05.PP.history/<revision>/` with before/after hashes.
`05.PP.selected.json` is the selected-revision pointer. History files are
not rewritten. The same request hash does not append another revision.
`--interrupt` stores the prior bytes and a partial marker, then stops without
replacing the selected task or face.

## Trace
Pass traces are `05.PP.trace/NNNN.json`, linked by the previous record hash.
A refusal that reaches an open pass also stores the received request under
`05.PP.refusals/`. The result names `contract`, `check`, `input_sha256`,
`outcome` and `next_route`. No credentials are logged. No model is launched.

## Old records
A stored `desk-core-task/1` record is loaded only when its version 1 preimage
recomputes. That hash is not reused as a version 2 binding.
A review recorded before `desk-core-review-binding/2` does not become fresh
just because its old hash can be recomputed. The next action stays derived.
Revision history keeps the exact prior task and face bytes. `revision.json`
is not rewritten after it is stored. `05.PP.selected.json` is the only
selected-revision pointer. An interrupted revision leaves the prior selected
bytes in place.
No pass-01 disposable book is migrated into the live work book. Matching
`0123` custody remains occupied by `0123.boot-validation-0508` and is not
claimed by this repair.

