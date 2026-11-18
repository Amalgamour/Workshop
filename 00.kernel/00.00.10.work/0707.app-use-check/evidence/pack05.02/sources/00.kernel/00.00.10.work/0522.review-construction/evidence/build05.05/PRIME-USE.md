# Prime use — 05.05 review-loop app entry

Date: 2026-11-01. Author: Grok-2. This note is for Prime's review. It is not acceptance, seating, adoption, or custody. The door is registered. It is not a production runtime.

## Pins

`app/review-loop-v2.json` is schema `review-loop-pins/2`, version 1. The door checks that declaration, then each file, before any subprocess.

- `labs/review-loop-pass02/review_loop.py` `8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7`, 47189 bytes
- `labs/prime-cycle-pass03/prime_cycle.py` `496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c`, 76045 bytes
- `labs/review-construction-pass02/construct.py` `b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc`, 36188 bytes
- `labs/prime-review-pass02/prime_review.py` `80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e`, 58560 bytes
- `labs/prime-review-pass01/prime_review.py` `805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0`, 58324 bytes
- `labs/return-lines-pass01/return_lines.py` `863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a`, 100897 bytes
- `labs/return-placement-pass01/return_placement.py` `db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754`, 66097 bytes
- `labs/return-capture-pass01/return_inspect.py` `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`, 11402 bytes

`app/review-loop.json` and `app/review_loop_tools.py` stay and are not loaded for this command. `prime-review` stays on its own door. `run` with no namespace is still `stop: normal run is not activated`.

## App commands

From `D:\Git\lib-build`:

```text
python -B app/librarian.py review-loop describe-legacy --book ABS --member EXACT
python -B app/librarian.py review-loop prepare --fixture-root ABS --request REL
python -B app/librarian.py review-loop record --fixture-root ABS --request REL --decision REL
python -B app/librarian.py review-loop render --fixture-root ABS --request REL
python -B app/librarian.py review-loop read --fixture-root ABS --request REL
python -B app/librarian.py review-loop recover --fixture-root ABS --request REL
```

`prepare`, `record`, `render`, `read`, and `recover` require a disposable fixture root outside `D:\Git\lib-build` and outside the live work book. `describe-legacy` may name the live book and writes nothing under it. A wrapper refusal prints `stop:` and exits 2 before the loop starts. The loop's own refusal stays `refused:` and the loop's exit.

`reproduce` is a lab command of `labs/review-loop-pass02/review_loop.py`. The app refuses it with `reproduce is a lab command and is not an app command`. The lab decision schema is `review-loop-reproduce-decision/1`. Required keys are `attribution`, `agreement`, `goal`, `judgment`, `record_judgment`, `return_text`, `note_text`, `assignment_text`, and `task_id`. That schema is in `evidence/build05.05/CONTRACT.md`. `evidence/build05.04/CONTRACT.md` was not rewritten.

## First-use checklist

Read `labs/prime-entry-pilot-pass01/PILOT.md`. The declared request is `example-request.json`. The declared registration is `example-registration.json`. The labeled demonstration words are `supplied-judgment.json`. The unfilled real-decision template is `real-decision-template.json`. It is not a runnable decision. Prime fills `attribution`, `judgment`, and `supplied_record` on the prepare template from a disposable run.

The kept demo is `evidence/build05.05/pilot-demo`. It copied live member `0182.desk-app-integration-design-0501` into a book outside this checkout, described that copy, and rendered a new PENDING page at `0519.desk-app/05.01.md` inside the disposable book. Origin stayed `0519.desk-app` / `05.01`. Submission stayed `claude-0519-0501`. The derived line is `0119.desk-app`. Actual custody of the copy stayed the member directory, placement pending. The new-process read is `full_success` true, `pass_state` `reviewed`, `accepted` false, `custody` `not-established`, `task_association` `not-established`. `sample-review.md` keeps `OUTSIDE-Δ-TOKEN`, `TAIL-Δ-TOKEN`, and the supplied finding `The copied return file is present.`

Custody of the copied member was verified by the pinned inspector. These custody records do not name the review task. Verified custody and task association are different facts. Task association stays `not-established`. That limit does not by itself block a supplied review of the declared copy. The supplied words are not Prime's judgment and they are not an assessment of the 0519 design.

A second disposable book used the live page bytes as the review target. Render returned `render-conflict` and the rule `existing review conflicts; a successor process is required and this review was not overwritten`. The page bytes were unchanged. One partial was created under that disposable book, which the pilot then deleted. The live page was not the render target. There is no successor renderer.

To repeat the pilot without replacing the kept demo, choose a directory that does not exist:

```text
python -B labs/prime-entry-pilot-pass01/pilot.py --destination D:\Git\lib-build\00.kernel\00.00.10.work\0522.review-construction\evidence\build05.05\pilot-demo-rerun
```

An existing destination is refused and is not replaced. The working books stay in the temp directory and are deleted when the command finishes.

## What this entry does not do

Exit 0 is not approval. `full_success` is mechanical completion. Nothing here seats the loop, migrates a return, or allocates `0184`. Matching-line custody stays pending at `0122.review-construction`. The same-user gap between the hash read and the subprocess is not closed. No model is called.
