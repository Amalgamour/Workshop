# Prime use - referenced-source candidate

accepted: false
state: staged candidate; active dispatcher unchanged

## Proof command

On the candidate root labs/review-source-capacity-pass03/candidate, with the working directory set to that root:

```
python -B app/librarian.py review-loop COMMAND --book ABS --source PAGE --pass 05.NN
```

COMMAND is prepare, form, record, inspect, read, publish, or recover.
record also takes --intake and --judgment. publish also takes --review.
Exit 0 is a completed command on a disposable book. Exit 0 is not a release.
Direct execution of labs/review-source-capacity-pass03/review_loop_tools_source_capacity_v3.py from the lab directory refuses with `review loop declaration is missing`.

## Candidate identity

Candidate librarian sha256 82935705ffc900ffa288d96b8d331b633bcce9004e5f0982e0acf3a884b9921c, 12249 bytes.
Successor sha256 c15cbd2460200583cab0518e2ac16f4a95356a779edb4b1978dfb4afc2a3e7ab, 6136 bytes.
Adapter sha256 fe887c0f378fc1da3f5e778ac4642c907f713614040d5ebf3b74272b02512b1f, 3126 bytes.
Door sha256 8df0253100fe0b5bd68a5e4f645322a44d3870b5f583af35e0e0aee75bc280eb, 11744 bytes.
Declaration sha256 e79c93ef29b04ed810b4fa31efeaf6c9a28dd9957f3bb5d4a4e6ed74b3f90b9c, 5052 bytes. Schema review-loop-source-capacity/3.
The candidate file list is evidence/build05.12/candidate-index.json.
The proof root contains the pinned code files and omits 00.kernel.

## What the author cycle showed

0512/05.09 on a fresh external copy recorded 29 sources and a 125955-byte prime-input.
Review wa2e4f7a1d3e48fab. Mode preliminary. Custody missing. Separate publish set published true and published_work false.
Recover target_state section-verified. Agreement fields stayed unknown.

0522/05.14 on a fresh external copy recorded 20 sources and a 62200-byte prime-input.
Review w5da8c91e140b119c. The copied page already contains workbook-review-id wb980a2a872c7e7c7.
Separate publish returned stale-own-review. Recover target_state not-published. The occupied section was left in place.

0512/05.10 on a fresh external copy recorded the open judgment. Sources 44. Prime-input 137328 bytes.
Review wa7922b9b4f84d400. hostile/over-document.json stayed 276423 bytes with a null inline record and bind true.
The finished-terminal judgment refused `a held review keeps the pass and the goal open` before that record.
Inspect, read, a separate publish, and a new-process read and recover kept the retained finding.
The pass02 successor still refuses this return with `limit sources[24].content_bytes`.
The pass01 successor still refuses it at 32 sources and still writes all 44 identities.
