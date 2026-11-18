# Prime use - source-capacity candidate

accepted: false
state: staged candidate; active dispatcher unchanged

## Proof command

On the candidate root labs/review-source-capacity-pass01/candidate, with the working directory set to that root:

```
python -B app/librarian.py review-loop COMMAND --book ABS --source PAGE --pass 05.NN
```

COMMAND is prepare, form, record, inspect, read, publish, or recover. record also takes --intake and --judgment. publish also takes --review. The process is that root's app/librarian.py. Exit 0 is a completed command on a disposable book. Exit 0 is not a release. The active D:\Git\lib-build app is unchanged. Direct execution of labs/review-source-capacity-pass01/review_loop_tools_source_capacity.py from the lab directory refuses with `review loop declaration is missing`. That refusal is the uninstalled state.

## Candidate identity

Candidate librarian sha256 d2d7f7a3e25b435708f3f05a7c84a7b0d56e095758e8309237f53a25c1cb9bf4, 12237 bytes. Successor sha256 a12b88958dcf2aea0fdc4c83f30c245b0f7f91d6ddf7c515bf31c7119c01fa87, 2031 bytes. Adapter sha256 7383e6ec4e5bf7909f069796a7fe6c71e23b6f241edec64fc3805656174a742e, 3055 bytes. Declaration schema review-loop-source-capacity/1. The full candidate file list is evidence/build05.10/candidate-index.json. The proof root contains the pinned code files and omits 00.kernel.

## What the author cycle showed

0512/05.09 on a fresh external copy recorded 29 sources and a 125955-byte prime-input. Review wa625af81adaf35cd. Mode preliminary. Custody missing. Cycle called false. Cycle committed false. Separate publish set published true and published_work false. Recover target_state section-verified. The prefix before `## Review - Codex Prime` matched the live page. Finding and next action matched the retained judgment.

0522/05.14 on a fresh external copy recorded 20 sources and a 62200-byte prime-input. Review wcfa3cd82d3322f65. The copied page already contains workbook-review-id wb980a2a872c7e7c7. Separate publish returned correction `stale-own-review`, published false, and the page bytes stayed equal to the live page. Recover target_state not-published. The retained judgment and next action came back. Custody stayed missing. That occupied section was left in place.

## Selection and rollback

Selection is not applied. A later selection is described in evidence/build05.10/INTEGRATION.md. Rollback restores evidence/build05.10/rollback-librarian.py. This note does not file 0112.prime-review.

## Helper root

The adapter and the successor load historical modules from D:\Git\lib-build by hash. The candidate REPO used for declared-path lookup is the candidate root. Those two roots stay distinct.
