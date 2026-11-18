# Coverage

The graph can be valid and still incomplete. Validate status `valid` on the positive set is an answer about the declared rows. It leaves the pending slots pending.

## Pending

Combined workbook W and reporter-on-W have no accepted path and no accepted hash. The wrapper always emits both slots with path null, sha256 null, bytes null, and state `pending`. The address edges `pending-w` and `pending-reporter` point at `00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md` with condition status `unknown`. On the instance-door requires answer those edges are `address-unresolved` and `condition-unknown`.

## Unknown environment

Every executable record carries a python row, availability `unverified`. Records that contain a fixed-root compare also carry `canonical-helper-root`, availability `unverified`. The positive report lists unknown environment `canonical-helper-root` and `python`. The measured interpreter for the suite is CPython 3.14.0. No source row enforces that version. The helper-root comparisons were inspected and were not executed.

## Visible gaps the controls showed

- A missing pass04 record surfaces as `record-missing`. The wrapper exits 1.
- A missing pass04 fixture file makes the reader refuse. The wrapper exits 2 with `reader_refused` true and `activation_ready` false.
- A wrong pin digest surfaces as `pin-differs`.
- A wrong implementation length surfaces as `declaration-length-wrong` and, for a pair pin of the old length, `identity-pair-mismatch`.
- Depth 1 from the instance door surfaces `depth-limit`. Truncation stays a truncation.
- The unpinned selected-v7 edge stays `selected` with pin form `unpinned`.
- Digest-only resolves on the digest. The live callers inspected for this set use a pair pin or no pin.
- H2's git-blob commit is `supplied-unverified`. `commit_authenticated` stays false.

## Uncovered, repeated by the wrapper

- v4 through v8 historical door pins except the named v7 and v9 files
- pass01 and pass02 workbook fan-out, and the pass03 load of pass02
- capacity pass01 and pass02 prime_review pins inside source-capacity-prime-review
- the rest of the reporter PINS table
- `labs/review-report-hardening-pass01/librarian.py`
- the nested candidate tree under `labs/review-source-capacity-pass03/candidate`
- index and delta commands
- Git authentication, custody, app selection, concurrency, power loss, and AR-01

`06.35.md` records that form does not expose instance applicability. This preflight leaves that fact as a review note and does not make it a dependency edge.

## Pages left unopened

`0522.review-construction/05.17.md` and `0707.app-use-check/05.23.md` were not opened. Their evidence was not opened. `0707.app-use-check/06.20.review.md` is the accepted L provenance and was read before the lab.
