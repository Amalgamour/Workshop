# Contract — 0521.return-placement/05.14

Schema: `n7-first-review-contract/0514`
Date: 2026-11-03
Executor: Grok-2
Reviewer: Codex Prime
Status: frozen when the first successor driver process starts

## Known failure this contract does not repair in place

The pinned core stays `labs/prime-cycle-pass03/prime_cycle.py` sha256 `496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c`, 76045 bytes, and `labs/review-loop-pass03/review_loop.py` sha256 `47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b`, 55474 bytes.

Before any successor file is written, one reproduction copies the retained 05.13 book to `D:\librarian\temp\0521-0514\known-failure\book` and removes only the copy of `0721.connected-local/06.01.review.md`. It then runs the live review loop, cwd `D:\Git\lib-build`:

`labs/review-loop-pass03/review_loop.py prepare --fixture-root <copy> --request workbook-review/0721.connected-local/05.01/w8fd4cbf791e32f26/cycle/request.json`

The expected view is schema `prime-cycle-view/4`, source kind `N7NN`, target `0721.connected-local/06.01.review.md`, observation state `complete`, `template` null, `write_token` null, exit 0, stderr empty. That output is the known failure. It is not coverage of the successor. The 05.13 stamp is not modified. The successor driver does not rewrite `known-failure`.

## Successor ownership

New tree `labs/n7-first-review-pass01`:

- `prime_cycle.py`, a copy of pass03. `write_token_of` returns schema `review-write-token/1` with `state` `absent-create`, `sha256` null, and `bytes` null only when the path does not exist and the registration is N7NN whose derived destination equals `target`. A present regular file keeps today's token shape, with `sha256` and `bytes` and without `state`. `derive` emits `prime-cycle-decision/3` when that creation token is present, because the token is no longer null. `record_review` rechecks that the path is still absent before committing. It does not create the page file.
- `review_loop.py`, a copy of pass03. Its cycle pin points at this successor `prime_cycle.py`. `record` allows the cycle commit when the live token is `absent-create` for that same derived path. `render` is the authorized creation: it sets `expect_sha256` to `absent` and `permit_create` to true only for that path, then calls the pinned constructor. A path that exists after the bound read is not overwritten. `mechanical` offers recover while the bound file is still absent.
- `workbook.py`, a copy of workbook pass02. It still loads live workbook pass01 by the existing pin. After load it repins `review_loop` and `prime_cycle` to this lab. Its cycle publish accepts a newly created review file whose surrounding bytes are empty. An existing manual review is still refused.

Pinned read-only, not copied and not edited:

- `labs/review-construction-pass04/construct.py` `6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20`, 42582 bytes. Its absent apply already requires `permit_create` and exclusive create. A temporary name that already exists is refused and kept.
- `labs/workbook-review-pass01/workbook.py` `60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a`, 79131 bytes.
- `labs/prime-review-pass02/prime_review.py`, return-lines pass01, return-placement pass01, and return-capture inspect, at the hashes already pinned by pass03.

No app file, README, current wrapper, or live core file is edited. The successor is a launcher into those pins. It is not a portable app.

## What the implementation covers

Covered: one first N7 cycle whose derived review file starts absent; exclusive creation of that file at render with the constructor body; refusal when a file, link, or directory appears after prepare; refusal of an existing manual review and of Director text; refusal of a foreign or non-derived target; N5 present-file token and cycle behavior; a planted constructor temporary file left unremoved and unmarked complete; source or return bytes changed after record blocking publication; the corrected `writer_started` parser in the new driver.

Not covered: power loss beyond the retained temporary or partial files, multiwriter races, AR-01, live migration, shared route selection, and a second review on the same N7 page. No such guarantee is claimed.

## Disposable book

Stamp `D:\librarian\temp\0521-0514\<UTC>\`. The book is outside the checkout. Synthetic authorization schema `return-line-authorization/1`, synthetic true, is fixture authority for that book only. Layout body sha256 `2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804`. Pass04 init uses the six flags. The measured door page is copied into the lock directory. No live book command reserves or captures.

Native filing uses the reviewed return-lines pass04 capture and the reviewed access verify. Receipts come from capture. A supplied judgment is test data. `closes_work` and `releases_action` stay false. `authority` stays `none`.

## Commands the successor driver runs

1. Build the marked disposable book and file N7 `0721.connected-local` pass `05.01` and N5 `0521.connected-return-review` pass `05.01`. The N7 review path is absent after filing.
2. Successor workbook prepare, form, record, and inspect on that N7 pass. Record mode `cycle-committed` only if the cycle committed. The review path is still absent. Read `rendered.md` in full and require the supplied finding and the supplied next-action text.
3. Successor publish, then a new-process read and recover. The review path now exists and contains the task binding. Authority lines stay false.
4. Hostile cases, each on its own member or its own copy of the filed page: existing manual review with Director text; a file created after prepare; return bytes changed after record; a malformed target; a foreign target in the registration; a directory at the destination; a planted `06.01.review.md.review-construct.tmp`; an N5 replay; two further author cases, forged N5 absent-create and a decision token whose path is not the derived destination. A symlink or reparse point is attempted and skipped with the Windows error if the privilege is absent.
5. The driver report field `writer_started` is false for the sample line `writer_started: false`.

## Failure

The first successor command that misses its expected exit or byte invariant is the first failure. Later probes still run when they do not repair a sealed return, receipt, or review file. Exit 0 from the driver is not Prime review, seating, or app activation.

## Selection

This pack does not select the shared app and does not patch the active core. One next action, after Prime review: Prime remeasures the successor delta and decides whether to stage it into the shared cycle modules, using inspect, a full read, and a separate publish pause. That action is not the two return-route substitutions, and it is not physical migration.
