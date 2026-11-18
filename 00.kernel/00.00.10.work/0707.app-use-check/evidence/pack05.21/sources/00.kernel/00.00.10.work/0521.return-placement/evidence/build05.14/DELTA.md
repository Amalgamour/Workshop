# Delta — N7 absent-target first review

Schema: `n7-first-review-delta/0514`
Date: 2026-11-03
Executor: Grok-2
Reviewer: Codex Prime

`CONTRACT.md` is the pre-code contract. It was frozen when the first successor driver started. This file records the measured module, API, pin, and schema delta. It does not revise that contract.

## Modules

| Role | Path | sha256 | bytes |
| --- | --- | --- | --- |
| Live cycle, unchanged | `labs/prime-cycle-pass03/prime_cycle.py` | `496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c` | 76045 |
| Successor cycle | `labs/n7-first-review-pass01/prime_cycle.py` | `b664c2c989a132108aa236ea6885e2503cf0dca266a12538ebe0b26cf9dba81d` | 77501 |
| Live loop, unchanged | `labs/review-loop-pass03/review_loop.py` | `47f47d16426e4d69987398a8244877de58b6089326874f3279003f696814450b` | 55474 |
| Successor loop | `labs/n7-first-review-pass01/review_loop.py` | `fb0e1e32a33e25b0f36013fbca6231094fccda5f65491b8596320c8594c89fe4` | 59229 |
| Successor workbook | `labs/n7-first-review-pass01/workbook.py` | `5c1df5b18a5e068d4480f486607a0cb21020256cdffb4da58553f98875c84939` | 54735 |
| Successor driver | `labs/n7-first-review-pass01/drive.py` | `d2b5aed969f3ee178b375872680e841dd32d8d5a36264504bfd26d357fb605f0` | 48467 |
| Live workbook base, unchanged | `labs/workbook-review-pass01/workbook.py` | `60e040fa30f61348adac76a4f3bdfbfdb9aba859f25bacadf317937c167e9b0a` | 79131 |
| Live constructor, unchanged | `labs/review-construction-pass04/construct.py` | `6d541d4225ed0f9ccdb6263b475a79f55e4312be80a7e9a810a3622e5bd8df20` | 42582 |
| Cycle bind constructor, unchanged | `labs/review-construction-pass02/construct.py` | `b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc` | 36188 |
| Pinned prime review, unchanged | `labs/prime-review-pass02/prime_review.py` | `80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e` | 58560 |

The successor cycle pin key stays `prime_cycle_pass03`. Its path string is `labs/n7-first-review-pass01/prime_cycle.py`. The loop pin key stays `review_loop`. Its path string is `labs/n7-first-review-pass01/review_loop.py`. The workbook launcher loads live pass01, then replaces those two pins. The launcher is a pin overlay. This return claims no portable copy.

## Schema

`review-write-token/1` gains one bound state. For an N7 registration whose derived destination equals `target`, and only while that path does not exist, the token is:

- `schema`: `review-write-token/1`
- `path`: the derived destination `{page}/06.{tail}.review.md`
- `state`: `absent-create`
- `sha256`: null
- `bytes`: null

A present regular file keeps the existing token shape: `sha256`, `bytes`, and no `state` key. N5 uses that shape. No new review filename and no new authority name are introduced. Decision schema stays `prime-cycle-decision/3`. The view schema stays `prime-cycle-view/4`.

## API

`creation_permitted` is true only when the source kind is `N7NN`, the address kind is `N7NN`, and the address destination equals the registration target.

`write_token_of` returns the absent-create token only for that permitted absent path. An existing path still goes through the regular-file read. A link or directory is refused.

`derive` emits the decision because the token is no longer null. The derive condition itself is the existing one.

`record_review` rechecks the absent-create token before commit: creation still permitted, path equal to the derived target, hash and byte count null, and the path still absent. The refusal for a later appearance is `target appeared after read`. A token path that differs from the derived destination is `absent-create token path is not the derived destination`. Record does not create the page file.

`review_loop.record` allows the cycle commit when the live token is absent-create for that derived path and the path is still absent. `render_committed` is the authorized creation. It sets `expect_sha256` to `absent` and `permit_create` true, then calls the pinned constructor. A later render of the same committed decision uses the live file hash and `rendered.json`, and returns `already-rendered` when they match. `recover` calls that same render path. `mechanical` reports `create-pending` with route `recover` while both tokens are absent-create and the target is still absent.

`workbook.prime_record` stores `bind` false for N7 and for N5. The pinned cycle record and the pinned constructor call `prime_review` report without `--root`. A bind-true N7 source is refused by that pinned report. The file bytes are still read and hashed. `do_publish` refuses an absent N7 destination from a preliminary record: `target file is absent; a preliminary record does not create it`. Cycle-committed publish accepts a new file whose prefix is the review heading and whose suffix is empty. An existing manual review is kept.

## Corrections kept with the earlier stamps

The first official stamp marked N7 sources bind true. Record stayed preliminary. The successor workbook now stores bind false. The second official stamp read `workbook-review/{page}/{pass}/{review_id}/rendered.md`. Record stores `reviews/{review_id}/rendered.md`. The driver now reads that store path. Both stamps remain. This delta does not rewrite them.
