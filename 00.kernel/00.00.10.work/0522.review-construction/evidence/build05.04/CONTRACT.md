# Contract — real custody into the Prime review loop

Schema of this file: review-loop-contract/0504.
Date: 2026-11-01. Executor: Grok-2. Batch: 0522.review-construction/05.04.
This file is written before the pass03 cycle, the pass02 loop, and the pass02 constructor.
It does not change the shared seam, the 0521 producer, or any predecessor lab.

## Authority

- Consumer meanings: `0417.return-placement/evidence/integration-consumer-pass02.md`.
- Descriptor `/1`: `0417.return-placement/evidence/integration-seam-v1.md`, schema `return-line-descriptor/1`.
- Route arithmetic: pinned `labs/return-placement-pass01/return_placement.py` `compute_route`, exposed by its `route` command. This lane does not re-decide an undeclared band.
- Producer: pinned `labs/return-lines-pass01/return_lines.py`. Read-only commands used here are `verify`, `lookup`, and `descriptor`. Disposable tests may also call `init`, `reserve`, `capture`, `stage`, and `adopt` on a book outside `D:\Git\lib-build`.
- Legacy reader: pinned `labs/return-capture-pass01/return_inspect.py`, which loads its pinned helper. This lane does not call `reserve`.
- Review report: pinned `labs/prime-review-pass02/prime_review.py`.
- Binding and render shape: the pass01 constructor contract, with the report pin moved as named below.

A stated `complete`, a matching caller hash, or an evidence file's existence is not custody proof. Re-execute the pinned validator and compare it with the current records. Compute does not supply a semantic judgment, accept work, or establish live matching-line custody.

## Pins this lane loads and does not edit

| role | path | sha256 | bytes |
| --- | --- | --- | --- |
| producer | labs/return-lines-pass01/return_lines.py | 863968c59974d85910626ba5e80cf49f14a3186c8d33b855efe00bf6ccec378a | 100897 |
| placement | labs/return-placement-pass01/return_placement.py | db96f7023c73dcececba0e7d42b821da8193af7534a4bdf8cd2e5d6cd53d0754 | 66097 |
| inspector | labs/return-capture-pass01/return_inspect.py | 947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b | 11402 |
| helper | labs/return-capture-pass01/return_capture.py | 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac | 45767 |
| report | labs/prime-review-pass02/prime_review.py | 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e | 58560 |
| report pass01 | labs/prime-review-pass01/prime_review.py | 805995a1ea8ec3c0b62efad7b5d9ebc8991ba9fd3da75e200b8f626908f4edd0 | 58324 |
| constructor pass01 | labs/review-construction-pass01/construct.py | 8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a | 35956 |
| cycle pass02 | labs/prime-cycle-pass02/prime_cycle.py | 689d63d26b0dfb59363563effa50acbd69856ffcc2ee728b7f54615f16fabd50 | 58448 |
| loop pass01 | labs/review-loop-pass01/review_loop.py | fac0881d1e7e991b630d1deab688a3e28745e2f7b2075c7eb5148251b8ac5595 | 26028 |

A mismatch raises `pinned tool hash does not match` and writes nothing. The caller `verification.tool_path` is compared with the pinned path. It is never the program that runs.

## Successors and deltas

`labs/review-construction-pass02/construct.py` is pass01 plus the report pin. `TOOL` is `labs/prime-review-pass02/prime_review.py` at the report hash above. Destination derivation, binding `/2`, write-token checks, conflict partials, and outside-section preservation stay. The pass01 constructor file stays byte-identical and still pins pass01.

`labs/prime-cycle-pass03/prime_cycle.py` is pass02 plus custody observation and the pass02 constructor pin. Registration, decision, review, fingerprint, and historical `/1` and `/2` readings stay. `/3` currentness is still the `review-task-binding/2` digest plus origin, member, direction, and goal. The review-home hash is still only the write token. Rendering does not stale a review. A changed task, evidence, agreement, or receipt does.

`labs/review-loop-pass02/review_loop.py` is pass01 plus the pass03 cycle pin, the pass02 constructor pin, `describe-legacy`, and `reproduce`. `prepare` may exit 0 when it has reported a state. `full_success` on prepare is false. `full_success` is true only when a later render lands and the report exit is 0 or absent. Exit 1 remains a recorded report, not approval.

## Descriptor /1

Exact keys stay the seam keys. `target_page` equals the derived return-page directory: `{N}1{NN}.{subject}` for an N5NN origin, and the N7NN page directory for a page-local origin. It does not equal the review file. `custody_path` equals `{target_page}/{batch}.custody` and must be a directory. `return_path` equals `{target_page}/{batch}.return.md`. Receipt and manifest paths are the files inside that directory. The review home is `{page}/{batch}.md` for N5NN and `{page}/06.{tail}.review.md` for N7NN.

Supported `/1` formats are `return-line-capture/1` and `legacy-relocated/1`. Any other format, including `staged-seal/1`, is `unsupported`. A custody path that is a regular file is `custody path is not a directory`.

Observation calls `return_lines.py verify --book --page --batch` on the pinned program. The regenerated descriptor must equal the caller descriptor. A difference is `descriptor does not match the pinned validator`. The validator state is then the observation state: `complete`, `reserved`, `incomplete`, or `conflict`. Those states stay distinct. A missing descriptor file stays `missing`. An unreadable descriptor stays `observation-failed`.

On `complete` for `return-line-capture/1`, this lane also reads the receipt. Schema must be `return-line-capture/1` and kind `receipt`. Submission, reservation hash, manifest hash, return hash, payload hashes, and the page tail must match the custody bytes. `approved`, `accepted`, and `published` must be false, and `acceptance` must be null. A synthetic receipt schema is not complete. For `legacy-relocated/1`, the receipt schema is the historical `return-capture/1`, `relocation.json` is present, and the same pinned verify result is required. This lane does not rewrite legacy bytes.

`verification.tool_path` must be `labs/return-lines-pass01/return_lines.py` for these formats. Any other path is `verification tool_path is not the pinned validator`. The named path is not executed.

Wrong origin, pass, subject, route, or submission is `conflict` and names that check. A reserved or incomplete producer descriptor stays that state and does not become a template.

## Descriptor /2

Exact keys are the `/1` keys plus `placement`. `placement` exact keys: `status`, `intended_target_page`, `intended_return_path`, `relocation_record_path`, `occupancy`. `status` is `pending` or `final`.

This slice supports `legacy-in-place/1` with `status` `pending`. `target_page` and `custody_path` are the original member directory. `return_path`, `receipt_path`, and `manifest_path` are files in that directory. Origin comes from the reservation, not the directory name. `intended_target_page` and `intended_return_path` come from `compute_route` on that origin. `relocation_record_path` is null. `occupancy` is null in this adapter. `verification.tool_path` is `labs/return-capture-pass01/return_inspect.py`. Custody `complete` means the inspector status is `complete`. `placement.status` stays `pending`. `filing_claimed` stays false. A `/2` body that says `final` for this format is `legacy-in-place placement is pending`.

`staged-seal/1` returns `unsupported`. A `/2` body whose format is `return-line-capture/1` or `legacy-relocated/1` is accepted only when `placement.status` is `final` and the intended paths equal the actual paths. It then uses the `/1` validator. Every other `/2` variant is `unsupported`.

A `/1` reader still refuses a `/2` body by exact keys. This successor does not upgrade stored `/1` descriptors.

## Task association

Custody verification and the declared review task are different facts. These receipts do not name `task_id`. A complete observation sets `task_association` to `not-established` and says that the custody records do not name the review task. That limit does not by itself refuse a supplied review of the declared material. Changing the declared task, evidence, or agreement after record still makes the `/3` review stale. This lane does not invent a fresh task binding from receipt presence.

## describe-legacy

Command: `describe-legacy --book ABS --member EXACT`.

The book is read only, including the live book. The command writes no queue, layout, capture, review, or trace under that book. Stdout is schema `review-loop-legacy-description/1` with the `/2` descriptor, the inspector result, the route, and the material hashes. The caller may save that stdout elsewhere. Unknown member prefixes and undeclared routes are `unsupported`, with the inspector or route reason kept. `/1` final captures remain readable through the consumer above. This command does not allocate and does not call `reserve`.

## reproduce

Command: `reproduce --destination ABS --decision ABS`.

The decision file is the caller's typed judgment. The command refuses when that file is absent. It creates a disposable book outside `D:\Git\lib-build`, runs pinned `init`, `reserve`, and `capture`, and passes the unchanged descriptor through prepare, record, render, and a new-process read. It writes the transcript under `--destination`. `--destination` may be outside the checkout or under `evidence/build05.04/`. It must not be the live work book. The disposable book is not the live book.

## Results

Loop results stay schema `review-loop-result/1`. Every result sets `custody` `not-established`, `allocated` false, `closes_work` false, `releases_action` false, `authenticates_actor` false, `authority` `none`, and `accepted` false. `filing_claimed` is false. A refusal is schema `review-loop-refusal/1`, exit 2, and stderr `refused:`. The request, pins, observation, supplied judgment, current and historical state, and the next correction stay on the result. Partial files and the input descriptor stay.

`missing`, `reserved`, `incomplete`, `conflict`, `observation-failed`, `unsupported`, `review-stale`, `review-unusable`, `render-pending`, and `render-conflict` stay distinct. None of them is `full_success`.

## Out of scope

No edit to 0521, the seam, a predecessor lab, `librarian.py`, or an existing pin file. No live capture, no migration, no staged seal, no relocation equivalence, no successor renderer, no sequential allocation, no `0184`, no seating, and no Git write. No AR-01 inventory, bridge, or hard-link race test. No broad app suite. `test_construct.py` is not rerun, because its teardown writes `evidence/build05.02`.
