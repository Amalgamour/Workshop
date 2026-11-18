# Binding checklist — 0707/05.11 (for Prime, when binding to the returned API)
who: claude-opus-5-5 · state: design. **Every target assertion is NOT RUN.** It is written without reading the target API, its return or its tests.

## Before any case
1. **Copy** `evidence/design05.10/fixtures/book/00.00.10.work` (the book root, per 06.10 corr. 5) into a new disposable book instance outside the checkout. **Never run in place.** Check each copied file against `design05.10/fixture-manifest.json`.
2. **Keep a binding log per case,** a new file beside the run. It lists:
   - the API commands used;
   - every adaptation of fixture paths or bases to the API's declared rules;
   - every measured identity added at setup;
   - the stop mechanism, for E-a;
   - the typed field chosen, for F-c to F-e.
   
   **An adaptation is recorded as a binding step, never as if it had been declared originally.**
3. **Positive baseline (A-base):** build a valid artifact manifest in the copy by measuring every listed file, using the API's declared path base. **Keep the frozen null-digest manifest only for A-digest.**
4. **No fabricated receipts.** The filed mode needs a fixture made by the accepted line tool; otherwise filed mode is out of the run.
5. **Hand-written review text is never tool authority.** A tool review exists only if the tool recorded it in this copy (B-tool prerequisite).
6. **Supplied judgments** (`fixtures/judgments/*.json`) are semantic content. Transcribe them into the RETURNED form; **any identity echoed must be one compute returned.**
7. **Record a tree hash** of the copy before and after each operation, for the no-write and preservation checks.

## Per case
| Case | Source page / pass | Prerequisites | Mutation | Allowed writes | Forbidden writes | Expected states (J P C W R) |
|---|---|---|---|---|---|---|
| A-base | `0599.fixture-review` / 05.01 | valid manifest built at setup | none | the tool's record and review home; the Review area of 05.01.md | `evidence/build05.01/*`; any 01NN path; 05.01.md outside the Review area | J✓ P✓ C✗ W✗ R✗ |
| A-digest | same | frozen null-digest manifest | none | as A-base | as A-base | finding reported |
| A-missing | same | A-base | delete submission.md before prepare | none required | anything that guesses a path | finding; no target |
| A-ambiguous | same | A-base | the pointer names two files | none required | choosing one | finding |
| B-tool | `0799.fixture-colab` / 05.01 | a first review recorded **by the tool** (director-input, Q1, hold D1), then the SYNTHETIC 06.02 decision | record the successor for the **same** pass | the tool's review home for 05.01 | 05.01.pack.md, 05.01.return.md, 06.02.decisions.md; a new pass number | J✓ P✓ W✗ **R✗ (D1)** |
| B-manual | same | the hand-written 06.01.review.md as frozen | record a review | per the API, or none if blocked | overwriting or adopting 06.01.review.md | preserved or blocked |
| C-a / C-b | `0599` / 05.01 | A-base | the Scope word / the T3 row, after record | none | reverting the edit | J✓ P✗ (stale) |
| C-c | same | A-base | none (the tool's own pointer write) | the Review area only | 05.01.md outside the Review area | J✓ P✓ C✗ W✗ R✗ |
| C-d | same | A-base | add 06.99.notes.md (SYNTHETIC) | as A-base | — | J✓ P✓ |
| D | same | A-base plus the manual text in the Review area | none | the tool's record only | the manual text | J✓ **P✗** C✗ W✗ R✗ |
| E-a / E-b / E-c | same | A-base; a supported stop for E-a, otherwise **NOT BINDABLE** | stop / edit the render / edit the pointer | only verified completion, or none | a silent overwrite | P not reported complete without verification |
| F-a…F-e | same | the returned form's declared field types | replay / conflict / wrong type / omit required / nullable unknown | only the first valid record (F-a) and the unknown (F-e) | a second authoritative result; any record on F-c or F-d | as in `index.json` |

States: **J** judgment recorded · **P** publication complete · **C** custody complete · **W** work complete · **R** action released. **Each is reported separately; none implies another** (06.10 corr. 3).

## After each case
- Compare the tree hashes; check the forbidden paths.
- Record each assertion as PASS, FAIL or NOT BINDABLE, **with the observed output kept.** A first failure is kept, and expectations are not rewritten afterwards.
- **Keep author cases, independent cases (these) and reproductions separately labelled** (06.07 Prime application 1).
