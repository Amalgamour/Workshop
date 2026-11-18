# BUILD-PACK — N7-local exchange in the combined loop (UNAPPLIED proposal)
from: claude-opus-5-5 (Colab 0707/05.20) · for: a later Grok integration builder · state: **PROPOSED. Prime places and releases it. No number, branch, selection or release.**

## Candidate identity (prototype, lab)
| File | sha256 | bytes | Role |
|---|---|---|---|
| labs/n7-local-lifecycle-pass01/workbook.py | 43995fc72db252c22baeadb1e7c3b16012125eb286ce4f2356ff96e051044d2a | 9750 | production-shaped overlay: canonical guard; pins pass04 b7b8776c… (6508) |
| labs/n7-local-lifecycle-pass01/adapter/workbook.lab.py | 94aed77733db76d88551436adf3004243fd23a65643b90f11696e9e2a7943f9a | 9917 | **LAB:** differs in exactly two places (REPO = own root; pass04 pin = the 05.18 lab adapter c6be0b97…, 6584) |
| labs/n7-local-lifecycle-pass01/adapter/review-loop-v8.n7local.lab.json | ddbf3c0ffd22e4d9f2139ada6f226a569b131ec02bae79f7b822da8f6a45b765 | 4046 | **LAB:** the 05.18 lab v8 declaration with `workbook` pointing at the overlay |
| labs/n7-local-lifecycle-pass01/make_adapter.py | (manifest) | | derives both LAB files from the overlay; reproducible |

**The production-shaped overlay has not run at the canonical root** (that would need installation). Its success path is shown only through the two-line lab adapter.

## What production must change (exact interfaces; future pins PENDING)
1. **The combined workbook W** (05.19 plan) includes the overlay's four functions **unchanged in meaning**:
   - `build_intake` (N7: exchange, n1 not-applicable, unmatched → incomplete);
   - `source_changed` (N7: book instance; pack bound region);
   - `result` (N7: emit exchange);
   - `open`.
   - Pin W over **G (the strict grammar)**, not over pass04, once G is accepted. The overlay only reads parsed rows and finding codes, so G's blocking composes before it.
2. **The door vN** adds `open` to its WORKBOOK command set (today v8 refuses unknown commands), and pins W.
3. **Record label** (`pass02.do_record` successor behavior in W): for an N7 record, set `custody` to `not-applicable` (a new value; the reporter and any reader enumerating custody values must accept it). `render_body` then prints `custody: not-applicable`. **Freeze the schema value set** (06.19.review: use actual schema names and enumerate them).
4. **F (0521):** do NOT carry its "preliminary record does not create an absent N7 target" refusal onto the N7-local route. If F's cycle path is kept for any other route, gate it by that route explicitly.
5. **The reporter successor R′** observes through W, including the exchange. Parity obligation: a matched, published N7 exchange reports current. **Rehashing the dispatcher is not sufficient** (05.19 X7).
6. **N5:** no change. That includes leaving the copied-book weakness as is (R2). Fixing it for N5 would be a separate, reviewed N5 change.

## Acceptance (each claim has a case)
- **Rerun `labs/n7-local-lifecycle-pass01/run_matrix.py` against W** (swap the overlay bytes for W in `new_root`, plus the vN declaration): 9/9, with the same expected states.
- **Rerun `replay_history.py`:** 0707/05.15 and 05.17 `matched`/`unverified`, with artifact rows equal to G's own count; N5 copied-book unchanged.
- **Add after G:**
  - 05.19 X1 and X2 (decoy manifest, refused-plus-valid) must block before the exchange is `matched`.
- **Add after K:**
  - a matched N7 exchange with more than 24 book sources records.
- **Reporter:** review-report on the T1, T5 and T3 roots gives current / current / stale.
- **Read-only on the live book** (Prime-authorized cuts only): `prepare` on 0707/05.15, 05.17 and 05.19 gives `matched`, chronology `unverified`. **No record or publish on live.**

## Stop conditions
- any N5 stdout difference against the selected predecessor on the same cut;
- any non-`matched` state recorded or published;
- a manual target overwritten;
- a judgment not canonically equal after a refusal;
- chronology claimed from mtime or dates;
- a need to edit pass01–pass04, v4–v8 or any declared artifact in place.

## Return shape
Did / Blocked / Need, then:
- the files with their hashes;
- the dispatcher and door delta;
- per-case provenance (author / rerun / known failure);
- raw first failures;
- the acceptance table;
- live read-only outputs;
- the remaining seams.

The artifact manifest excludes itself. **Follow the actual assigned route.**
