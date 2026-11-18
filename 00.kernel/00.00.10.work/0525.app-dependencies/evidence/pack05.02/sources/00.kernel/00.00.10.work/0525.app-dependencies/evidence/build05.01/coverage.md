# Coverage — edges the declaration set does not close

The selected set is `labs/app-dependencies-pass01/set.json`, set id `review-loop-entry-1`. Twelve `module-declaration/1` records. `coverage.complete_claim` is false on every record. depdecl.py was not modified.

## What the graph answers

`requires --transitive` from `app/librarian.py` exits 0 with status `complete-for-declared-coverage`. The findings are `environment-unverified` 21, `shared` 33, and `condition-inapplicable` 1. Those three are non-blocking in the 05.02 delta. They are not readiness and not approval.

`explain` to `return_capture.py` exits 0 and reports three paths. Each path is the first time that reader was reached. The door hash-checks `return_inspect.py`, `return_lines.py`, and `return_placement.py` before the loop's own edges are expanded, so the stored path is librarian, door, that reader, then `return_capture.py`. The loop's later subprocess of the inspector is in `requires-full.json` as requirement `return-inspect`, mechanism `subprocess`, resolution `resolved`, finding `shared`, because the door already reached that module. A shared revisit is listed once. It is not a second explain path.

`impacted --depth 8` on `return_capture.py` exits 0 with status `candidates-for-review` and no findings. First reaches:

- depth 1, `matches-declared`: `return_lines.py` and `return_placement.py`
- depth 1, `unpinned`: `return_inspect.py`
- depth 2, `matches-declared`: the v2 door, the pass02 loop, and the pass03 cycle
- depth 2, `unpinned`: `review-loop-v2.json`, which stores the lines path and does not hash it
- depth 3, `unpinned`: `app/librarian.py`, which loads the door by path and does not hash it

`--implementation 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` compares the digest only. Direct rows: lines and placement `pin-matches`, inspect `unpinned`.

## Truncation

`impacted --depth 1` exits 1, status `truncated`, finding `depth-limit`. The three direct consumers are listed and not expanded. `unexpanded` gives `return_lines.py` 5 further consumers, `return_placement.py` 7, and `return_inspect.py` 6. A one-level answer does not show the door, the loop, the cycle, or librarian.

`requires --transitive --depth 2` exits 1, status `incomplete`, finding `depth-limit` on nine door edges. The door's targets are resolved and not walked. The set bound is `max_depth` 16. The full transitive answer above used that bound.

## Schema gaps kept visible

1. Digest-only pin. `return_inspect.py` lines 49-70 compare `HELPER_SHA256` and do not compare length. A `requirement.pin` must be both sha256 and bytes. Recording that pair would claim a length check the file does not perform. The edge is `pin: null`. The observed identity is in the reason: sha256 `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`, 45767 bytes. Proposed extension: allow `pin.bytes` null when the caller compares only the digest, and teach `impacted` to say `digest-only` rather than `unpinned`.

2. Git blob basis. `module-declaration/1` refuses any `basis.kind` other than `git-blob`. Nine of these files match the pack pins and are not the blob at HEAD `960d20c5290656095df8457b1740d2d5e586b111`. `git log --find-object` found no commit. Each of those records sets `basis.commit` to that HEAD and says in `provenance.unknown` that the measured bytes are not that blob. The implementation sha256 and length are the measured file. Proposed extension: `basis.kind` `working-tree`, with the observed HEAD stored beside it.

3. Pass ids with an extra segment. `0512.prime-review/05.01.002.md` exists. `face_or_pass` must match `NN` or `NN.NNN` with at most one dot. `05.01.002` does not fit, so that page is named only in `provenance.unknown` on the pass01 review record. Proposed extension: allow the book's existing three-part pass token.

4. Named contract string. `review_loop.py` line 28 sets `CONTRACT` to `00.kernel/00.00.10.work/0522.review-construction/evidence/build05.04/CONTRACT.md`. An address requirement would be `address-unresolved` on every answer, because the reader lists addresses and does not open them. The page is a pinned provenance link, role `source-stated`, sha256 `233aa17bd83964f02981ed5babc089e657d0befe2799f15b1cde9c998afad800`. The loop does not hash that file before use. Proposed extension: a document reference that is not loaded should be non-blocking, distinct from a missing module record.

5. Caller-chosen inputs. The book for `describe-legacy` and the fixture root for the mutation commands are environment rows, `availability: unverified`. They are not modules. Matching tool hashes do not show that `D:\Git\lib-build` exists, that a fixture root is outside it, or that a book is safe to read.

6. One mechanism field. Where a file both hash-checks and later launches the same module, the record has two requirements. `impacted` lists both. That is deliberate.

7. Route versus custody. `return_placement.py` `compute_route` (line 141) does not call `_reader` (lines 201-218). The review-loop entry calls `route`. The capture load is declared with condition `custody-reader` and status `inapplicable`, so `requires` lists it and does not walk it. `impacted` still lists the edge. The inapplicable status is the entry-point bound, not a claim that the function is absent.

## Left outside this set

`run` and `reproduce` are not app commands. `reproduce` launches `return_lines.py`. The door refuses it before the loop starts. The old facade `app/review_loop_tools.py` and `app/review-loop.json` are not loaded by the `review-loop` namespace. Prime-review's other librarian commands are other namespaces. Standard-library imports are not modules. No record here classifies any of this code as production.
