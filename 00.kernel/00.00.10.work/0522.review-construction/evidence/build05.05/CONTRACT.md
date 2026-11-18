# App contract — review-loop entry v2

Date: 2026-11-01. Author: Grok-2. This contract is written before the door and the tests. It is the app contract for `0522.review-construction/05.05`. It does not rewrite `evidence/build05.04/CONTRACT.md`.

## Owner and core

Grok-2 is the sole app-entry integration owner for this batch. The reviewed loop, cycle, constructor, and readers stay the pinned files below. This contract does not change their bytes. A substantive core change is a checkpoint, not a silent edit.

## Pins

Declaration schema `review-loop-pins/2`, version 1, file `app/review-loop-v2.json`. The door checks that declaration against these pins, then checks each file's bytes, before any subprocess.

- `labs/review-loop-pass02/review_loop.py` `8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7`, 47189 bytes
- `labs/prime-cycle-pass03/prime_cycle.py` `496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c`, 76045 bytes
- `labs/review-construction-pass02/construct.py` `b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc`, 36188 bytes
- `labs/prime-review-pass02/prime_review.py` `80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e`, 58560 bytes
- `labs/prime-review-pass01/prime_review.py` `805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0`, 58324 bytes
- `labs/return-lines-pass01/return_lines.py` `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a`, 100897 bytes
- `labs/return-placement-pass01/return_placement.py` `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754`, 66097 bytes
- `labs/return-capture-pass01/return_inspect.py` `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`, 11402 bytes

There is no caller-chosen executable, no shell concatenation, no newest-module selection, and no pin bypass. A symlink or junction on the declaration or on a tool path is refused and is not followed. The old files `app/review-loop.json` and `app/review_loop_tools.py` stay. `librarian.py` does not load them. `prime-review` and the other existing namespaces stay on their own doors.

## App commands

The namespace is `review-loop`. From `D:\Git\lib-build`:

```text
python -B app/librarian.py review-loop describe-legacy --book ABS --member EXACT
python -B app/librarian.py review-loop prepare --fixture-root ABS --request REL
python -B app/librarian.py review-loop record --fixture-root ABS --request REL --decision REL
python -B app/librarian.py review-loop render --fixture-root ABS --request REL
python -B app/librarian.py review-loop read --fixture-root ABS --request REL
python -B app/librarian.py review-loop recover --fixture-root ABS --request REL
```

Each required flag appears once. Flags may be in any order. A value does not start with `--`. `REL` is fixture-relative, uses forward slashes, and contains no empty, `.`, or `..` part and no drive prefix. No other flag is accepted.

`prepare`, `record`, `render`, `read`, and `recover` require an explicit absolute fixture root. The door allows that root only when it is an existing directory, not a link, not a UNC path, contains no `..`, is outside `D:\Git\lib-build`, and is not the live work book `00.kernel/00.00.10.work`. A root inside the checkout is refused before the loop starts.

`describe-legacy` reads the named book and writes nothing under it. The book may be the live work book. Stdout is schema `review-loop-legacy-description/1`. Placement for a legacy member stays pending. The command does not allocate.

A wrapper refusal prints `stop:` on stderr, exits 2, and does not start the loop. The loop's own refusal stays the loop's `refused:` text and the loop's exit. `run` remains the librarian refusal `stop: normal run is not activated`. It is not a review-loop subcommand.

## Reproduce stays a lab command

`reproduce` is a command of `labs/review-loop-pass02/review_loop.py`. It is not an app command. The app refuses it before the loop starts. The lab command creates a disposable book, fixes the page at `0599.synth-lab/05.01` and the submission at `repro-0504`, and writes an explicit destination. The app does not expose `--destination` and does not accept an arbitrary destination.

The lab decision schema is `review-loop-reproduce-decision/1`. Required keys are `attribution`, `agreement`, `goal`, `judgment`, `record_judgment`, `return_text`, `note_text`, `assignment_text`, and `task_id`. `evidence/build05.04/CONTRACT.md` names the lab command and the absent-file refusal. It does not name this schema. That file stays as the pre-test contract of 05.04. This contract records the schema.

## Pilot

The disposable pilot copies live member `0182.desk-app-integration-design-0501` into a book outside `D:\Git\lib-build`. The copy keeps that member's reservation, receipt, manifest, return, and payloads. Origin stays `0519.desk-app` / `05.01`, submission stays `claude-0519-0501`, and the intended line stays `0119.desk-app`. The live page `0519.desk-app/05.01.md` already holds a substantive Prime review. The pilot renders on a new PENDING page at that derived path inside the disposable book. A copy of the substantive page is a render conflict. There is no successor renderer.

The demonstration judgment is labeled `SUPPLIED`. It is synthetic data for the mechanical path. It is not Prime's judgment and it is not an assessment of the 0519 design. Custody records for this member do not name the review task. Task association stays `not-established`. `full_success` is mechanical completion. `accepted` stays false. `custody` stays `not-established`. `filing_claimed` stays false.

## Rollback

Restore `app/librarian.py` to `939484f152c9227482e857f9ce88eaf40649f433a57d6c9d213a07bde16baee5`, 10463 bytes. Restore `app/README.md` to `4164ee218ac7e2bffdfea5bbf8c6f7b0d2a7edf01bb1dd4684d60d4e909c535d`, 26362 bytes. Delete `app/review_loop_tools_v2.py`, `app/review-loop-v2.json`, `app/tests/test_review_loop_entry_v2.py`, `labs/prime-entry-pilot-pass01/`, `00.kernel/00.00.10.work/0522.review-construction/06.09.md`, and `evidence/build05.05/`. Leave the pinned core, the old door, and the live member in place.

## Out of scope

No edit to a predecessor lab, the seam, a source return, `0524`, the Claude lab, kernel law, or an existing app module other than the narrow `librarian.py` registration and the appended README section. No live capture, no migration, no allocation, no `0184`, no seating, no production activation, and no Git write. No AR-01 inventory, bridge, or hard-link race test. No broad app suite.
