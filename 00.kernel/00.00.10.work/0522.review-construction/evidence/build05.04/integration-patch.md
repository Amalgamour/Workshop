# Integration patch — not applied

Date: 2026-11-01. Author: Grok-2. This file names the repair that landed in versioned successors and the later single-owner step. It does not edit `app/librarian.py`, `app/prime-review.json`, `app/prime_review_tools.py`, `app/review-loop.json`, `app/review_loop_tools.py`, the seam, or any predecessor lab.

## What the successors repair

RL-01. `labs/prime-cycle-pass03/prime_cycle.py` reads `target_page` as the return-page directory and `custody_path` as the custody directory. The review home stays the page derived from origin. For `0599.synth-lab/05.01` the return page is `0199.synth-lab` and the review file is `0599.synth-lab/05.01.md`. A custody path that is a regular file is a conflict: `custody path is not a directory`.

RL-02. A stated `complete` is rechecked by running pinned `labs/return-lines-pass01/return_lines.py verify` and by reading the reservation, manifest, receipt, payload, and return bytes. The regenerated descriptor is compared with the caller descriptor. `verification.tool_path` is accepted only when it is the pinned tool path. A caller-supplied path is not executed. A synthetic receipt, a changed payload, a changed manifest, and a custody file substitute stay off `complete`.

RL-03. `labs/review-construction-pass02/construct.py` pins `labs/prime-review-pass02/prime_review.py`. Nonzero `1599.synth-lab` renders as member `1199.synth-lab`. The pass01 constructor is unchanged and still reports `bad member` for that member.

`legacy-in-place/1` is read through pinned `return_inspect.py`. Actual custody stays the original member directory. Placement stays `pending`. Intended paths come from the reservation origin through the pinned route. `legacy-relocated/1` is verified on the actual relocated custody. `staged-seal/1` is unsupported. A `/2` descriptor is projected to `/1` keys only when placement is `final` and the intended paths equal the actual paths, and only for `return-line-capture/1` or `legacy-relocated/1`. Every other `/2` variant is unsupported. Pass02 cycle still refuses a `/2` body by exact keys. That file was not edited.

Task association on these receipts stays `not-established`. The attention line names that limit. It does not block a supplied review of the declared material. A later change of task, evidence, or agreement makes the `/3` review stale and leaves the record bytes in place.

## Predecessor delta

- `labs/review-construction-pass02/construct.py` copies `labs/review-construction-pass01/construct.py` `8b9d4a6eda460f594404042f7ee232a7ac55fcc09af38905de364defa189ea8a`, 35956 bytes. The delta is the report pin, to `labs/prime-review-pass02/prime_review.py` `80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e`, 58560 bytes. Successor hash `b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc`, 36188 bytes.
- `labs/prime-cycle-pass03/prime_cycle.py` copies `labs/prime-cycle-pass02/prime_cycle.py` `689d63d26b0dfb59363563effa50acbd69856ffcc2ee728b7f54615f16fabd50`, 58448 bytes. The delta is the custody observer and the pass02 constructor pin `b82413ffcb388658bb6fe6aaa7028d573c918108e7feb7c15664c8a8a34eb3cc`. Successor hash `496b4d721cfb136fa847d998d421209616c60508beb5cda5620af73041eed17c`, 76045 bytes.
- `labs/review-loop-pass02/review_loop.py` copies `labs/review-loop-pass01/review_loop.py` `fac0881d1e7e991b630d1deab688a3e28745e2f7b2075c7eb5148251b8ac5595`, 26028 bytes. The delta is the pass03 cycle pin, the pass02 constructor pin, `describe-legacy`, and `reproduce`. `prepare` keeps `full_success` false. Successor hash `8082750fc6ecc740bee3a193bbc357242164913337bbbe7be4f3779d499fedf7`, 47189 bytes.

## Later registration

Prime, as the single owner of the app facade, can later register a new pin file. This pass does not add `app/review_loop_tools_v2.py` or `app/review-loop-v2.json`. The existing `app/review-loop.json` still pins the 05.03 adapter. `librarian.py` does not load it. A door copied from the pass01 bans would refuse `reproduce`, because `--destination` starts with `--dest`. The lab command is the reproduction command.

## What this patch does not do

It does not migrate `0122.review-construction`. It does not allocate a return. It does not allocate `0184`. It does not run `describe-legacy` on the live book. It does not write a staged seal or a relocation-equivalence rule. It does not add a successor renderer for an existing substantive review. It does not treat a rendered review as approval. Custody stays pending.
