# CONTRACT — desk-core/1 prototype
date: 2026-10-31
who: Grok Build (xAI)
state: contract for the bounded prototype; not production law

## Compatibility boundary
This adapter writes schema `desk-core/1` on an explicit disposable book.
It is not `return-capture/1`. It does not create `reservation.json` members,
does not take `0100.band.returns`, and does not allocate the next free 01NN slot.
Do not point `return_capture.py` at a desk-core book.
Do not point `python -m app.desk_core` at `00.kernel/00.00.10.work`.
Pinned modules are reference identities only. Runtime imports of app or labs
code: none. Direct and transitive runtime dependencies: Python standard library only.

Checked identities (not imported), from pack05.01:
- labs/return-capture-pass01/return_capture.py sha256 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac
- app/librarian.py sha256 939484f152c9227482e857f9ce88eaf40649f433a57d6c9d213a07bde16baee5
- app/handoff_tools.py sha256 f1d76a517b64a82ff8e348b811a5c59dfe8870385e6737b67878e0749e705bc2
The `pins` command rechecks every manifest row against the live path and snapshot.

## Invocation
From the repository root, with the standard library only:

```text
python3.11 -B -m app.desk_core <command> ...
```

`--book` is required for book commands and must be an absolute path outside this
checkout, not a symlink. JSON in, one JSON object on stdout.

| Command | Role |
|---|---|
| init | Create a disposable book header. Not a task ledger. |
| record-task | Build the source page, pass face, and task record from a supplied spec. |
| register | Record the supplied release and worker claim against the task binding. |
| show | Exact task, expected outputs, scope, and derived state. |
| assert-done | Record that a worker says done. This does not capture a return. |
| submit-return | Verify and capture the return on the matching line or Colab tail. |
| retrieve | Return text, artifact identities, receipt, unresolved questions. |
| review | Record a supplied judgment and render the full review in its home. |
| recover | Pending state, next actor, and next action from records only. |
| pending | Read-only projection of passes in this book. |
| revise-task | Replace task content at the same identity. Stales claim and review. |
| pins | Verify pack05.01 source pins. |

Exit 0 is success, including an unchanged retry. Exit 2 is a refusal. Exit 3 is
a simulated interrupted write. Exit 1 is an unexpected fault. A refusal in a
declared negative test is not a STOP-NNN.

## Placement
Page id is four digits whose first digit is `0`. The second digit is the band.
`NN` is the last two digits. Subject is `[a-z0-9]+(?:[.-][a-z0-9]+)*`.
Pass is `01`–`99`.

- Band 5, source `05NN.subject`: return directory `01NN.subject`.
  Face `05.PP.md`. Review section on that face: `## Review - Codex Prime`
  (hyphen, as on this batch's own 05.01, not an em dash).
  Return files on the return line: `05.PP.return.md`, `05.PP.receipt.json`,
  `05.PP.artifacts/`.
- Band 7: no return directory. Page-local `05.PP.pack.md`, `05.PP.return.md`,
  `06.PP.review.md`.
- Any other band or shape: refuse `undeclared-source-kind` or
  `undeclared-source-shape`. Write nothing.
- If any directory `01NN.*` exists with a different subject: refuse
  `return-line-occupied`. Do not overwrite or add a second subject on that number.

## Records and projections
Authoritative records, all versioned JSON:
- `desk-core-book/1` at `00.desk.json` (header and limits only)
- `desk-core-task/1` at `05.PP.task.json`
- `desk-core-release/1` at `05.PP.release.json`
- `desk-core-claim/1` at `05.PP.claim.json`
- `desk-core-assertion/1` at `05.PP.assertion.json` when a worker says done
- `desk-core-receipt/1` at `05.PP.receipt.json` on the custody directory
- `desk-core-review/1` at `05.PP.review.json` (N5NN) or `06.PP.review.json` (N7NN)

`01.md` and the pass face are projections. A mismatch is a visible conflict.
The view does not replace the record with the face or with the newest file.
`accepted` is always false. `complete` is true only when a receipt verifies and
no assignment-projection conflict is open. Capture completeness is not acceptance.

## Binding
Task binding is sha256 of canonical JSON (`sort_keys`, compact separators, UTF-8)
of schema `desk-core-task-binding/1` over title, body, expected outputs, scope,
agreement, and bound evidence. Pointer text and review text are outside it.
Review binding is schema `desk-core-review-binding/1` over the task binding,
receipt sha256, agreement sha256, evidence sha256, and the supplied review identity.

## Idempotency and conflict
The pass identity is page + subject + pass. The same return bytes retry in place.
Different return bytes write a conflict record and leave the receipt. A different
claim or release does the same. Stale claim, stale release, and stale review stay
visible. None of them becomes accepted.

## Interrupted write
`submit-return --interrupt` writes staging bytes and does not write a receipt.
State is `partial`, `complete` false. A later successful publish writes the
receipt last. A verifying receipt is the capture commit. Staging without a
receipt is never reported complete.

## Review home and byte rule
N5NN: splice only the body of `## Review - Codex Prime`. Bytes before that
heading and bytes from `## Record note` through end stay put. The rendered body
keeps an empty findings list as `(none)` and keeps every supplied unresolved
question, dissent, Director text, and assessment. N7NN: write `06.PP.review.md`
and do not modify the pack while doing so.
Supplied Director text is stored verbatim in the review record. The tool does
not invent a next action. If the judgment supplies one, recover returns it and
marks it not derived. Earlier states use a derived next step and say so.

## Limits
No OS isolation, no authenticated roles, no race-freedom claim, no model launch,
no live migration, no production-ready claim. Advisory `flock` plus exclusive
create narrows ordinary lost updates only.
Older pages that spell the review heading with an em dash are outside this
writer. Integration must not renormalize those bytes.
