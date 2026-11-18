# IMPACT-MAP (proposed) — modules, pins and consumers for review-loop entry v3
date: 2026-11-01 · who: claude-opus-5-5 (Claude) · state: design; built from source reading of pack05.02 bytes. Not a complete-closure claim.

## 1. Current pin chain (observed in source)
```text
app/librarian.py:97-106            loads app/review_loop_tools_v2.py by path (unhashed)
app/review_loop_tools_v2.py:28-68  TOOLS: 8 pins (path, sha256, bytes); checks app/review-loop-v2.json equals them
app/review-loop-v2.json            the same 8 pins (data)
labs/review-loop-pass02/review_loop.py:27-50   pins construct p02, prime_review p01+p02, cycle p03, return_lines, return_placement, return_inspect; pin_set() 148-160
labs/prime-cycle-pass03/prime_cycle.py:28-48   pins construct p02, return_lines, return_placement, return_inspect, prime_review p01+p02; calls construct p02 `bind` (:919)
labs/review-construction-pass02/construct.py:27-30  pins prime_review p02
labs/return-capture-pass01/return_inspect.py   digest-only pin of sibling return_capture.py (0525 D-05)
```

## 2. Slice-1 change set (one owner, one change set)

| File | Change | Why | Existing bytes |
|---|---|---|---|
| NEW `labs/review-construction-pass03/construct.py` | copy of pass02, plus: envelope `/2` with `supplied_review_state`; the `### Supplied review state` block; `inspect` command; recorded-decision sha line; null vs `[]` text | F4, F8, F11 | pass02 unchanged; still pinned by the cycle and the door |
| NEW `labs/review-loop-pass03/review_loop.py` | copy of pass02, plus: CONSTRUCT → pass03 for apply/show/inspect; `build_envelope` `/2`; render integrity check against `record.json`; prepare calls `inspect`; `review-loop-result/2` (`mechanical`, `supplied_next_action`, `target`); the `next` rule | F4, F7, F8 | pass02 unchanged |
| NEW `app/review_loop_tools_v3.py` | v2 copy with TOOLS = loop p03, construct p03, construct p02 (cycle `bind` dependency), cycle p03, prime_review p01, p02, the 3 readers; forwards the same 6 commands; adds no command | pins | v2 unchanged |
| NEW `app/review-loop-v3.json` | `review-loop-pins/3` with the same entries | pins | v2 unchanged |
| EDIT `app/librarian.py` | `review-loop` loads `review_loop_tools_v3.py` (one path at line 99); module docstring line 10 | entry | current d07de8a7…, 11037 bytes (the 0522/05.05 result); the builder records the new before/after |
| EDIT append `app/README.md` | v3 section | docs | append only |
| NEW `app/tests/test_review_loop_entry_v3.py` | the acceptance cases in `ACCEPTANCE.md` | tests | v2 tests unchanged |
| NEW `labs/prime-entry-pilot-pass02/` | clean example registration, real-decision template `/2`, operator guide copy, synthetic disposition fixtures | F11, F1, F2, F6 | pass01 unchanged |

**Unchanged:** cycle pass03, prime_review p01/p02, construct p02, the readers, pass01 pilot, v1 and v2 doors and declarations.

**Why the cycle can stay:**
- It validates only `envelope.record` and `envelope.target` (1521–1524), and stores the envelope bytes.
- Its `bind` (pass02) and the pass03 `show` must agree on the binding, and A4.5 tests that.
- If A4.5 fails, the cycle needs a successor that pins construct pass03. That is a checkpoint to stop at, not to paper over.

## 3. Pins and declarations that must update together
1. `review_loop_tools_v3.py` TOOLS and `review-loop-v3.json` agree, entry for entry.
2. Loop pass03's constants must equal the shipped construct p03 bytes (CONSTRUCT_SHA/BYTES), with cycle p03 and the others unchanged.
3. Construct p03 TOOL pins prime_review p02 (unchanged value).
4. `librarian.py` (path only; unhashed today, per 0525 coverage "depth 3 unpinned").
5. **0525 declaration records:** the set is **not accepted** (Prime review D-04 git-blob basis false for working-tree bytes; D-05 digest-only pin shown as unpinned). New records are needed for loop p03, construct p03, door v3 and declaration v3, plus a changed `librarian-review-loop` record. They belong in the 0525/05.02 v2 representation once accepted. Slice 1 must not wait for it, must not edit Grok-2's records, and must not claim dependency closure.

## 4. Consumers bound to the current (v2) entry or its outputs

| Consumer | Bound how | Effect of the v3 switch |
|---|---|---|
| `labs/prime-entry-pilot-pass01/pilot.py` | runs `app/librarian.py review-loop`; asserts `full_success`, `render.result`, `observation.*`, the render-conflict exit 2 | runs v3 once librarian switches. Its asserted keys survive in `/2`, but it was not run; treat as historical, do not rerun into 0522 evidence |
| `app/tests/test_review_loop_entry_v2.py` | named in 0522 CONTRACT; **not in pack05.02, unread** | may assert v2 pins or `next` text; builder must run it against v2 files and keep it, not edit it |
| `colab/labs/0707.app-use-check/pass01/*` | `compare.py` asserts `supplied_judgment` is null and reads `read.current.latest_review` | a deliberate behavioural difference under `/2`; pass01 stays historical |
| Prime's 0707 reproduction (`evidence/prime-review05.01`) | same | historical |
| `review_loop.py` `reproduce` (lab) | uses construct p02 via ROOT | unchanged in p02; p03 keeps `reproduce` as a lab command |
| 0525 selected set `review-loop-entry-1` | describes v2 | stays a description of v2 |

**Unknown:** other app namespaces do not load the review-loop door (0525 coverage "Left outside this set"). I did not read app tests or other app modules.

## 5. Rollback (proposed)
- Restore `app/librarian.py` and `app/README.md` to their pre-slice hashes.
- Delete the five NEW paths.
- v2 then resumes unchanged.
- No historical evidence is touched.
