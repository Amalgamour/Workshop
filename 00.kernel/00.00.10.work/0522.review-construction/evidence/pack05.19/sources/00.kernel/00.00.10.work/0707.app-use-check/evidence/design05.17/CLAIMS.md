# Claims — 0707/05.17
**Labels:**
- **KR** = known-failure reproduction;
- **AT** = author test (mine, not independent coverage);
- **ADAPTED** = a historical author case run through the documented adapter;
- **REVISED** = a historical expectation changed by K1, labelled separately.

All runs used disposable roots under `D:/librarian/temp/n7-intake-0717/`. **No independent probe ran** in this pass.

| # | Claim | Case / run | Result | Limit |
|---|---|---|---|---|
| 1 | pass01 refuses the legal N5 names `return.md,` `;` `)` that pass03 accepts (K1) | KR1, v2-run01 | reproduced | parser level; Prime's files supplied the filesystem proof |
| 2 | pass01 also silently changed the N5 meaning of `Artifact manifest: m.json, sha256` from `m.json,` to `m.json` | KR2, v2-run01 | reproduced | found by my reread; Prime's probe did not cover it |
| 3 | In N5 context, pass02 equals pass03 on 13 inputs (`, ; )` names, collision line, duplicates, conflicts, Returned-on-N5, PENDING, empty, garbage) | P1 | 13/13 equal | inputs are mine |
| 4 | With no intake context, pass02 equals pass03, including on the real N7 pointer | P2 | 14/14 equal | — |
| 5 | In N7 context the real 05.15 pointer binds exactly; the collision line is the N7 delimiter | P3 | pass | — |
| 6 | In N7 context, non-N7 lines keep the pass03 meaning (`return.md,` stays `return.md,`) | P4 | pass | — |
| 7 | N7 duplicates and cross-form conflicts leave the field unbound (ambiguous) | P5 | pass | — |
| 8 | Malformed N7 lines bind nothing: no comma after `)`, no final period, trailing text, a hash or label in the attribution | P6 | pass | — |
| 9 | LF and CRLF give identical parses in both contexts | P7 | pass | built from the frozen 05.15 pack |
| 10 | An N5 page with **real** files `return.md,` + `artifact-manifest.json,` (likewise `)` and `;`): unpatched and patched intake give identical intake_id, rows, findings and measurement, and the punctuated file is resolved | I-N5-comma / -paren / -semicolon | 3/3 | synthetic page in a faithful code layout |
| 11 | The 17 historical cases, unedited, run through the adapter `compat17/n7compat.py` | compat17-run01 | 16 pass; **G7 fails by design** | ADAPTED |
| 12 | **REVISED G7:** `Artifact manifest: m.json,, sha256` and `Submission: s.md, sha256` are now accepted as `m.json,,` and `s.md,` (pass03 meaning), not refused. The `;` after a Returned path is still refused. | compat17-run01 G7 detail | as revised | the historical file is kept unchanged; its failure is the K1 correction |
| 13 | Faithful 05.15 copy: v7 app and unpatched pass03 are both `incomplete` with the same intake_id; patched is `complete` with 30 binding rows and **26/26 unique artifacts, all hashes equal** | flow01 A/B/R | as stated | KR for A and B; AT for R |
| 14 | Manual-review protection is kept: the faithful publish exits 1 with `correction: manual-review`; the no-review copy publishes; read and recover are exact | flow01 | as stated | copy only |
| 15 | **The real 0522/05.13 N5 replay:** unpatched, patched and unpatched-again give an **identical intake_id** `1e583695…`, measurement `complete`, 32 identical rows, identical findings and cuts; kind `N5NN`; copied bytes unchanged; no files added | n5replay-run01 | identical | the copy holds the top-level .md files of 0522, the submission, the manifest and the 29 rows, not all 1815 files of the page |
| 16 | v7 app on the same 0522 copy (live code root) gives a different id and `ambiguous-declared-root` | n5replay-run01 A-app | as stated | the 05.16 two-root effect (the copy's book under the live REPO), not a regression |
| 17 | The **unapplied pass04 proposal** equals the lab: its parse is equal for every input in N5, N7 and no context, and it reproduces both intake_ids (51d6f637… N7, 1e583695… N5) | propcheck-run01 | ok | the REPO redirect is applied by the check harness, not by the proposal |
| 18 | The 108 pack05.17 inputs are byte-equal to live and to the snapshots at the end; 55 pass01 and 05.16 artifacts are unchanged | verification.json | 108/108, 55/55 | — |
