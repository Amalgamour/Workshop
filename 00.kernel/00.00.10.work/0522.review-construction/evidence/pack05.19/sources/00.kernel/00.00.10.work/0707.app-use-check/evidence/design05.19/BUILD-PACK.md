# BUILD-PACK — combined Prime review loop (UNAPPLIED proposal)
from: claude-opus-5-5 (Colab 0707/05.19) · for: a later Grok integration builder · state: **PROPOSED. Prime places and releases it. It proposes no number, branch, selection or release.**

## Preconditions (do not start until all are true)
1. **G** (strict N7 grammar, 0522/05.15) is accepted by Prime, and its files are frozen in a new pack manifest.
2. **K** (record capacity, 0512/05.10) is accepted and frozen.
3. **The Director has answered the first-target question** (CONTRACT §6).
4. **F** (0521/05.14) is accepted (it is) and is to be re-staged under versioned shared names.

## Declared inputs (placeholders; replace only from the frozen manifests)
| Placeholder | Fill from | Rule |
|---|---|---|
| `G_PATH`, `G_SHA`, `G_BYTES` | Prime-accepted 0522/05.15 return | exact bytes; no edit |
| `G_DOOR` (v9) | same | becomes a pinned predecessor |
| `K_PATH`, `K_SHA`, `K_BYTES`, `K_BOUND` | Prime-accepted 0512/05.10 return | exact; K_BOUND is K's declared supported bound |
| `F_LOOP`, `F_CYCLE` | `labs/n7-first-review-pass01/review_loop.py` fb0e1e32…, `prime_cycle.py` b664c2c9… | copy to NEW versioned names (e.g. `labs/review-loop-pass04/`, `labs/prime-cycle-pass04/`); fix only their own pin strings; record the delta |
| `DIRECTOR_FIRST_TARGET` | the Director's answer, verbatim | selects the W publish rule |

**Replacement procedure:** after Prime accepts both new returns, copy each value from the frozen manifest row. Recompute and compare sha256. Stop on any mismatch. **Never pin a guessed future hash.**

## Tasks (sequenced, smallest)
1. **Freeze check:** verify the new pack manifest. The current app (c3a5be3b…), v4–v8, pass01–pass04, reporter v1–v3 and README must be unchanged.
2. **F re-stage:** NEW versioned loop and cycle files. Only pin-string deltas from F. Rerun F's own author driver on a disposable book.
3. **W** (`labs/workbook-review-pass06/workbook.py`, name proposed):
   - load G under its pin;
   - assert REPO in all namespaces and keep the canonical-root guard;
   - repin `wb.PINS` `prime_review` → K, and `review_loop`/`prime_cycle` → step 2;
   - overlay the N7 publish rule per `DIRECTOR_FIRST_TARGET`;
   - set cycle-path source records `bind:false` and leave the preliminary path unchanged. **Verify at the F call site that bind:false is needed only there.**
4. **vN door and declaration:** from v8, `review-loop-pins/7`, adding W, G, K, the F files and the v8/pass04 predecessors.
5. **Combined dispatcher bytes** (one file, not yet selected): `c3a5be3b` plus the reporter hunk (from `labs/review-report-hardening-pass01/librarian.py`) plus the vN selection line plus the docstring lines. Measure its hash.
6. **R′** (`app/review_report_tools_v4.py` + JSON): the hardening runtime, with its observation through W, pinning the step-5 dispatcher hash and W/G/K/F. **The reporter's meaning is unchanged** (contract `review-report-hardening/1`).
7. **Acceptance:** the whole matrix in ACCEPTANCE.md (A1–A15), on disposable roots plus read-only live prepare/form on the named cuts.

## Candidate-entry commands (the actual on-disk entry of the candidate root)
```bash
python -B <ROOT>/app/librarian.py review-loop prepare --book <BOOK> --source <PAGE> --pass <05.NN>
```
```bash
python -B <ROOT>/app/librarian.py review-loop form --book <BOOK> --source <PAGE> --pass <05.NN>
```
```bash
python -B <ROOT>/app/librarian.py review-loop record --book <BOOK> --source <PAGE> --pass <05.NN> --intake <ID> --judgment <FILE>
```
```bash
python -B <ROOT>/app/librarian.py review-loop inspect --book <BOOK> --source <PAGE> --pass <05.NN>
```
(read the FULL output, then:)
```bash
python -B <ROOT>/app/librarian.py review-loop publish --book <BOOK> --source <PAGE> --pass <05.NN> --review <RID>
```
```bash
python -B <ROOT>/app/librarian.py review-loop read --book <BOOK> --source <PAGE> --pass <05.NN>
```
```bash
python -B <ROOT>/app/librarian.py review-loop recover --book <BOOK> --source <PAGE> --pass <05.NN>
```
```bash
python -B <ROOT>/app/librarian.py review-report --book <BOOK> --source <PAGE> --pass <05.NN>
```

## Retained judgments to replay (exact bytes)
- **0512/05.09:** `00.kernel/00.00.10.work/0512.prime-review/evidence/prime-review05.09/core-review/judgment.json` (Prime's judgment; currently refused by capacity).
- **0522/05.14:** `00.kernel/00.00.10.work/0522.review-construction/evidence/prime-review05.14/core-review/judgment.json` (recorded today; the replay must give the same rendered judgment).
- **0707/05.15 and 05.17:** a synthetic LAB-ONLY judgment (05.18 `lifecycle.JUDGMENT`), labelled.

## Preservation checks
- **The book:** prefix bytes before every Review heading, and the bytes of every manual 06.NN.review.md, are unchanged.
- **The source cut:** every declared file is unchanged before and after.
- **No live record, publish, custody or pointer writes.**
- **Historical files** (HISTORY.md rule 1) are byte-identical.

## Stop conditions
- any placeholder not frozen;
- any hash mismatch;
- an N5 diff not explained by a declared app artifact;
- N7 coverage below 100%;
- malformed N7 that is not blocked;
- a judgment not byte-preserved;
- a manual text change;
- a need to edit a historical file;
- the reporter not current where the loop is current;
- any authority/approval/release field other than none/false.

## Return shape
Did / Blocked / Need, then:
- the files with their hashes;
- the dispatcher delta;
- the per-case provenance (author / rerun / known failure);
- raw first failures;
- the A1–A15 table with evidence paths;
- reconstruction and rollback results;
- the remaining seams.

The artifact manifest excludes itself. **Follow the actual assigned route:** an N5 build pack uses its matching N1 return line and a page-local Prime review.

## Parallel now / serial later
| When | What |
|---|---|
| **In parallel now** | G (Grok-2), K (Grok-1), the Director question, F re-stage (step 2) |
| **Serial after G and K** | W → vN → combined dispatcher → R′ → acceptance → Prime review → selection |
| **Final observable success** | On the actual work book, Prime runs the eight commands above through the selected `app/librarian.py` on the next real N5 return and the next real N7 return, each with more than 24 book sources. Review-report is current, Director text is unchanged, and custody shows `missing`. |
