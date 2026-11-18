# Prime use — desk-core/1
date: 2026-10-31
who: Grok Build (xAI)
state: prototype instructions; not a release and not acceptance

## What this is
A local CLI that builds work-book pages for one disposable desk loop.
Intelligence supplies the task text, the release, the claim, the return, and
the judgment. Compute builds the page, the face, the custody files, the pointer,
and the readable review. It does not decide that the work is correct.

Run from the repository root:

```text
python3.11 -B -m app.desk_core --help
python3.11 -B -m app.desk_core.demo --transcript /absolute/path/demo.txt
```

Give `--book` an absolute directory outside this checkout. A path inside the
Librarian tree is refused. Do not point it at `00.kernel/00.00.10.work`.

## One pass
1. `init` the disposable book.
2. `record-task` with a synthetic spec. For `0523.subject` the face is
   `0523.subject/05.01.md`. The return line is not created yet.
3. `register` the supplied Director release and worker claim.
4. `show` in a new process. It prints the task body, expected outputs, scope,
   and state `claimed`. `complete` is false. `accepted` is false.
5. `submit-return`. N5NN bytes land on `0123.subject` as `05.01.return.md`,
   `05.01.receipt.json`, and `05.01.artifacts/`. The source face gains a return
   pointer. A second identical submit is idempotent. Different bytes are refused
   and the original receipt stays.
6. `retrieve` for the return text, artifact hashes, receipt, and questions.
   Retrieval is not a review.
7. `review` with a typed judgment. The full assessment is spliced under
   `## Review - Codex Prime` on `05.01.md`. Findings may be an empty list and
   are rendered as `(none)`. Director text is stored verbatim in the review JSON.
8. `recover` in a new process. If the review binding is fresh, the next actor
   and action are the ones the judgment supplied, and `derived` is false.
   `accepted` remains false.

`pending` lists passes by reading the book root and each source page only.
It is not a second job ledger.

## Colab
A `07NN` page keeps `05.NN.pack.md`, `05.NN.return.md`, and `06.NN.review.md`
on that page. Review does not modify the pack. No `01NN` directory is created.
Any other band is refused and nothing is allocated.

## What a fresh review is
The task binding covers title, body, expected outputs, scope, agreement, and
declared evidence identities. It does not cover the pointer or the review text.
The review binding also covers the receipt and the supplied review identity.
Changing the task, the evidence list, or the agreement makes the review stale.
The old review stays on the face and is not current authority.
A worker who only says done, or an interrupted write with no receipt, is not
complete.

## Do not treat these as approval
A receipt, a passing test, a review record, and this note are different.
None of them grants Director approval, seating, migration, or permission to
launch a model. Actor strings are not authentication. The file lock is not a
proof that two writers cannot race.

## Suggested integration, after review
Keep `app/librarian.py` and `return-capture/1` unchanged for historical
sequential members. Do not send a desk-core book through `return_capture.py`.
A later reviewed pack can add one librarian subcommand that execs
`python -m app.desk_core` with an explicit book and still refuses the live book.
Do not overwrite `0123.boot-validation-0508`. This batch's matching name would
be `0123.desk-core` only after that occupant is handled by a reviewed migration.
When reading older pages, accept both `## Review - Codex Prime` and the em-dash
spelling already on some faces, and do not rewrite those bytes.
No universal face builder is required for this loop.
