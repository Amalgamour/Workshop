# Prime use — 05.04 review loop

Date: 2026-11-01. Author: Grok-2. This note is for Prime's review. It is not acceptance, seating, adoption, or custody.

## What is ready to inspect

The kept demonstration is `evidence/build05.04/demo/`. A disposable book was created outside `D:\Git\lib-build` by the pinned producer `labs/return-lines-pass01/return_lines.py`, then removed after the destination files were written. The loop wrote only the named destination. The supplied judgment is labeled `SUPPLIED`. The label is not authentication. Compute did not invent the judgment.

From `D:\Git\lib-build`, the reproduction command is:

```text
python -B labs/review-loop-pass02/review_loop.py reproduce --destination D:\Git\lib-build\00.kernel\00.00.10.work\0522.review-construction\evidence\build05.04\demo-rerun --decision D:\Git\lib-build\00.kernel\00.00.10.work\0522.review-construction\evidence\build05.04\demo-decision.json
```

`demo-rerun` is a new destination. The command above leaves the kept `demo/` files in place. `--destination` must be absolute. Inside this checkout it must be under `evidence/build05.04/`. It must not be the live work book. The decision file must already exist. A missing decision exits 2 and does not create the destination.

The decision schema is `review-loop-reproduce-decision/1`. Required keys are `attribution`, `agreement`, `goal`, `judgment`, `record_judgment`, `return_text`, `note_text`, `assignment_text`, and `task_id`. `CONTRACT.md` names the command and the absent-file refusal. It does not name this schema. That contract file was left unchanged after the tests. This note is the disclosure.

The kept decision asks for a review of one disposable capture. `task_id` is `repro-task`. The command itself fixes the page at `0599.synth-lab/05.01`, the submission at `repro-0504`, and the producer calls `init`, `reserve`, `capture`, and `descriptor`. The return text is:

```text
Did.
The disposable capture returned one note.
```

The judgment outcome is `continue`. The finding is `The disposable note is present.` The supplied next action is `Pack one bounded correction for the disposable capture.` Attribution is `Codex Prime (SUPPLIED)`, role `prime`, with the evidence sentence that the label is not authentication and the judgment is not acceptance.

The kept run exited 0. The unchanged descriptor is `demo/descriptor.json`: schema `return-line-descriptor/1`, state `complete`, `target_page` `0199.synth-lab`, `custody_path` `0199.synth-lab/05.01.custody`, format `return-line-capture/1`, tool `labs/return-lines-pass01/return_lines.py`. The result is schema `review-loop-result/1`, `full_success` true, `pass_state` `reviewed`, `accepted` false, `custody` `not-established`, `authority` `none`, `allocated` false, `filing_claimed` false. Observation state is `complete`, `custody_verified` true, `placement_status` `final`, and `task_association` `not-established`. The transcript attention says the custody records do not establish the task association. `demo/sample-review.md` keeps `OUTSIDE-Δ-TOKEN`, `TAIL-Δ-TOKEN`, `authority: none`, and `custody: not-established`.

`full_success` means the mechanical prepare, record, render, and new-process read finished. It does not accept the work. A complete custody observation is custody integrity. It does not mean filed, reviewed, or accepted. These receipts do not name `task_id`, so task association stays `not-established`.

## Other commands

```text
python -B labs/review-loop-pass02/review_loop.py describe-legacy --book ABS --member EXACT
python -B labs/review-loop-pass02/review_loop.py prepare --fixture-root ABS --request REL
python -B labs/review-loop-pass02/review_loop.py record --fixture-root ABS --request REL --decision REL
python -B labs/review-loop-pass02/review_loop.py render --fixture-root ABS --request REL
python -B labs/review-loop-pass02/review_loop.py read --fixture-root ABS --request REL
python -B labs/review-loop-pass02/review_loop.py recover --fixture-root ABS --request REL
```

`describe-legacy` reads the named book and writes nothing under it. Stdout is schema `review-loop-legacy-description/1`. Placement for a legacy member stays `pending`. This pass demonstrated that command on disposable historical-format fixtures. It was not run against the live book. Prime chooses any later live member.

`prepare` may exit 0 with `full_success` false. Exit 2 prints `refused:` on stderr. A fixture root must be absolute and outside `D:\Git\lib-build`.

## Pins

Interpreter: `C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe`, Python 3.14.0, Windows-10-10.0.19045-SP0.

- `labs/review-loop-pass02/review_loop.py` `8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7`, 47189 bytes
- `labs/prime-cycle-pass03/prime_cycle.py` `496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c`, 76045 bytes
- `labs/review-construction-pass02/construct.py` `b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc`, 36188 bytes
- `labs/prime-review-pass02/prime_review.py` `80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e`, 58560 bytes
- `labs/return-lines-pass01/return_lines.py` `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a`, 100897 bytes
- `labs/return-placement-pass01/return_placement.py` `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754`, 66097 bytes
- `labs/return-capture-pass01/return_inspect.py` `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`, 11402 bytes

The pass02 constructor is the report pin for nonzero rendering. Pass01 `construct.py` still pins pass01 `prime_review.py`. A nonzero page rendered through `labs/review-construction-pass01/construct.py` still stops at `bad member`.

## What stays deferred

`librarian.py` does not load this loop. No `app/review_loop_tools_v2.py` was added. The pass01 door refuses a flag that starts with `--dest`, so that door cannot carry `reproduce`. Staged-seal and relocation equivalence are outside this slice. An existing substantive review remains a render conflict. Same-home succession is recorded and its renderer is deferred. Matching-line custody stays pending at `0122.review-construction`.
