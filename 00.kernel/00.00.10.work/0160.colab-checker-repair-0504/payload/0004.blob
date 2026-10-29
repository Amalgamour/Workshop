# REAL-USE — repaired standalone handoff checker (0510/05.04)

State: run by the 0510/05.04 executor on 2026-10-29 against the accepted 05.03 real-source package (digest 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184, fixture 0701 binding). That package was prepared earlier by the FROZEN producer 2b720434…, which is unchanged. No model was called.

## Exact invocation (consumer side, no producer or workflow import)
```text
python -B D:/Git/lib-build/labs/colab-support-pass02/handoff_check.py check --output OUT --expected-digest 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184 --json
python -B D:/Git/lib-build/labs/colab-support-pass02/handoff_check.py copy --output OUT --expected-digest <same> --to FRESH_DEST --json
```
The only input a consumer must trust is the expected digest carried with the launch. handoff.json is compared, never trusted.

## HC01 before and after (the same tampered copy of OUT; raw outputs in verification.json)
| checker | exit | result | identity reported |
|---|---|---|---|
| held handoff_check db921e1c… | 0 | valid | page `0799.wrong-investigation` (wrong) |
| repaired handoff_check 7d62dde4… | 1 | mismatch: `handoff.investigation differs from the value derived from bound bytes` | none |
| frozen producer verify | 1 | mismatch: `handoff.json differs from the recomputed plan` | n/a |

## Comparison on the real package (one tamper at a time)
| case | held | repaired | frozen producer |
|---|---|---|---|
| clean | 0 valid | 0 valid | 0 intact |
| HC01 investigation.page | **0 valid** | 1 mismatch | 1 mismatch |
| exchange.primary_instruction | 1 | 1 | 1 |
| envelope pack role | 1 | 1 | 1 |
| source_map role | **0 valid** | 1 mismatch | 1 mismatch |
| not_created emptied | **0 valid** | 1 mismatch | 1 mismatch |
| preimage order | 1 | 1 | 1 |
| zip.members drop | 1 | 1 | 1 |
| pack bytes | 1 | 1 | 1 |

The held checker accepted three wrong claims (bold), not only HC01. The repaired checker agrees with the frozen producer verify in every case.

## Valid package still checks and copies exactly
- `check`: exit 0, `valid`. Trusted investigation 0701.colab-exchange-layout/05.01, primary instruction 05.01.pack.md.
- `copy` to a fresh destination: exit 0, `copied`, 16 files, each byte-equal. The source is unchanged.
- `copy` again to the same destination: exit 2, `refused` / `already-copied`. Read-only; nothing written.

## What a consumer can rely on, and what it cannot
- **Relied on (derived from bound bytes):**
  - the investigation and binding;
  - exchange names, roles and the not-created list;
  - the source to snapshot map, with target ids and roles;
  - the support projection, ZIP membership and evaluator separation;
  - the assembler and package digests.
- **Not verified by this standalone tool** (bounded and listed in its output):
  - whether the prose files were rendered correctly from the request;
  - heading line ranges;
  - the assembler receipt's checker result;
  - tool pins.

  For those, run the pinned producer `verify`. Prime's 05.03 review says workflow must use the pinned full producer verifier meanwhile. This repair does not change that instruction; only Prime can.

## Remaining Prime inputs
The expected digest at launch, and the choice of which verifier a workflow pass uses.
