# Dependency and input contract (0707/05.21)
**Files:** `labs/loop-convergence-harness-pass01/inputs/inputs-proto-l.json`, `inputs-staged-g.json`, `inputs-combined.json` (written by `make_inputs.py`).

| Id | Role | Status at this freeze | Files | Review |
|---|---|---|---|---|
| G | strict N7 parser (pass05, v9 door and JSON) | **accepted** | pass05 86f40268…, v9 door, v9 JSON (frozen live bytes) | 0522/06.33 |
| L | N7-local lifecycle (prototype over pass04) | **accepted** (bounded prototype) | `labs/n7-local-lifecycle-pass01/workbook.py` 43995fc7… | 0707/06.20.review |
| K | record source capacity, source-only bound 64 | **pending** | `PENDING` | 0512/06.18 (05.10 correction required); 0512/05.11 not reviewed |
| I | N5 copied-book instance binding | **pending** | `PENDING` | 0420/06.48; 0522/05.16 not reviewed |
| R | reporter observing the combined chain | **pending** | `PENDING` | 06.19/06.20 obligations; unassigned |
| W | combined workbook + door + dispatcher | **pending** | `PENDING` | not built |

**Retained judgments** (frozen; expected source counts from Prime):
| Judgment | Expected sources | Review |
|---|---|---|
| 0512/05.09 `judgment.json` | 29 | 0512/06.16 |
| 0522/05.14 `judgment.json` | 20 | 0522/06.31 |
| 0512/05.10 `judgment-open.json` | 44 | 0512/06.18; 0420/06.49 |

**The fixture source** is `evidence/pack05.21/source-manifest.json` (635 rows).

## Replacement procedure (after Prime accepts K, I and R and the integration W exists)
1. Prime freezes each accepted file in a new pack manifest.
2. Copy each path, sha256 and bytes from THAT manifest into the dependency row. Set `status: accepted` and cite the review.
3. Build the combined candidate root; write its `CANDIDATE.json` (every file, plus a stated list of lab differences).
4. Set `candidate` from it, with `open_entry` = the candidate's declared pack-observation command, or null.
5. Run the full suite. **READY requires every row accepted and every required case `pass`.**

**Never:**
- edit a pending row's files to a guess (refused, HX-3);
- point a row at an unreviewed lane output;
- reuse a baseline candidate's manifest for the combined run.

## Candidate identities in this pass (lab baselines, external)
| Candidate | CANDIDATE.json sha256 | Lab differences |
|---|---|---|
| proto-l | 172ec4e9… (`D:/librarian/temp/lch-0721/cand-proto-l`) | the 05.20 lab declaration, overlay adapter, 05.18 pass04 adapter, 05.18 candidate dispatcher |
| staged-g | 062a3c8d… (`D:/librarian/temp/lch-0721/cand-staged-g`) | pass05 lab adapter (REPO, side-path pass04, pass04 pin); lab pass04 at the side path; lab v9 JSON (`_note`, workbook pin); dispatcher with the v9 line |

**Both are reproducible with `make_candidate.py`** (RC-1 shows a rebuilt root has identical files).
