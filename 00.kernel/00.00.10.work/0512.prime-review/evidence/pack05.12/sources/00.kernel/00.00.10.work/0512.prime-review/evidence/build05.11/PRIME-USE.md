# Prime use - source-capacity 64 candidate

accepted: false
state: staged candidate; active dispatcher unchanged

## Proof command

On the candidate root labs/review-source-capacity-pass02/candidate, with the working directory set to that root:

```
python -B app/librarian.py review-loop COMMAND --book ABS --source PAGE --pass 05.NN
```

COMMAND is prepare, form, record, inspect, read, publish, or recover.
record also takes --intake and --judgment. publish also takes --review.
Exit 0 is a completed command on a disposable book. Exit 0 is not a release.
Direct execution of labs/review-source-capacity-pass02/review_loop_tools_source_capacity_v2.py from the lab directory refuses with `review loop declaration is missing`.

## Candidate identity

Candidate librarian sha256 a4e0ec03095a43291a997fbf9e9899f89409863a3df718c7ba9e219ed63ea6bf, 12246 bytes.
Successor sha256 32567d68ccd6dc838c175af078610c53e4ec777d7c2f5eddb9d6ea8ea9c4644f, 2160 bytes.
Adapter sha256 41ef1f5448215bc763648219a5a7b2ba75ade86818734adef6edea6659eff38d, 3119 bytes.
Declaration schema review-loop-source-capacity/2.
The candidate file list is evidence/build05.11/candidate-index.json.
The proof root contains the pinned code files and omits 00.kernel.

## What the author cycle showed

0512/05.09 on a fresh external copy recorded 29 sources and a 125955-byte prime-input.
Review wecc2ddb1f86340b2. Mode preliminary. Custody missing. Cycle called false. Cycle committed false.
Separate publish set published true and published_work false. Recover target_state section-verified.
Finding and next action matched the retained judgment. Agreement fields stayed unknown.

0522/05.14 on a fresh external copy recorded 20 sources and a 62200-byte prime-input.
Review w72c59674fc0615ad. The copied page already contains workbook-review-id wb980a2a872c7e7c7.
Separate publish returned `stale-own-review`. The page bytes stayed equal to the live page.
Recover target_state not-published. The occupied section was left in place.

0512/05.10 on a fresh external copy kept 44 source identities in a 137328-byte prime-input.
The finished-pass judgment was refused with `a held review keeps the pass and the goal open`.
The open judgment was refused with `limit sources[24].content_bytes`.
The copy of 05.10.md was not published. The live page was not written.

## Selection and rollback

Selection is not applied. A later selection is described in evidence/build05.11/INTEGRATION.md.
Rollback restores evidence/build05.11/rollback-librarian.py onto app/librarian.py.
This note does not file 0112.prime-review.

## Helper root

The adapter and the successor load historical modules from D:\Git\lib-build by hash.
The candidate REPO used for declared-path lookup is the candidate root.
Those two roots stay distinct.
