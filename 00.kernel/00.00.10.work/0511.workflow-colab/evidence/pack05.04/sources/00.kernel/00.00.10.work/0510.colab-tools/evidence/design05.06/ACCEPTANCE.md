# ACCEPTANCE v2 — ran (prototype) and planned (integration)
date: 2026-11-01 · who: claude-opus-5-5 (Claude)

## Ran: pure-rule prototype and workflow model (SYNTHETIC)
- **Runner:** `colab/labs/0510-reserved-review/pass02/run_probe.py`. Each run is a new directory under `evidence/design05.06/runs/`.
- **Run 1 `20261101T203634Z-8fb571`:**
  - P1 re-observed the pass01 CRLF rejection;
  - P2 gave **1 error**: my fuzz test put a list into a set, which also showed that some substitutions were accepted without being named;
  - P3 wrote the examples.
- **Run 2 `20261101T203654Z-84a6ef`**, after naming the accepted substitutions and adding the at-least-one-requirement rule: P2 **51 of 51 OK**.

| Group | Cases |
|---|---|
| **ParseView (C03)** | LF = CRLF findings with different raw hashes; mixed endings; lone CR refused; BOM recorded; non-UTF-8 refused; missing and duplicate blocks; duplicate key, NaN, non-object block |
| **Types** | descriptor field fuzz ([], {}, 5, None, True, "x" on every key): only the 7 named valid substitutions are accepted; status list → `enum`; finding list → `type`; findings not a list → `type` |
| **Mode (C05)** | reserved without a descriptor refuses; ordinary stays ordinary; a descriptor in an ordinary job refuses; unknown mode refuses; reserved ready |
| **Verifier (C04)** | both agree; handoff valid alone with producer partial refuses; producer digest mismatch; handoff mismatch; identity split; wrong report kind |
| **Launch** | trigger, unready cut, cut mismatch, renamed context bytes, requirement and authority missing, withhold undeclared, continuing session |
| **Stage (C01/C02)** | valid with recorded order [2, 3, 4, 5] and `not_proved`; a CRLF first return end to end; no N1NN `member` anywhere; seal missing → chain; descriptor names another seal; bytes differ; first packet digest differs; review did not request the pass; informed packet already attached; chain tamper; packet lacks the first return; cut changed; missing first findings; environment difference recorded |
| **WorkflowModel** | seal replay no-op and conflict refused; review before return; attach to an unopened pass; history rewrite refused, while append is allowed |
| **Reconcile** | unresolved R03 with reason, unique U01, the disagreement listed; incomplete; unknown finding; reason required |

## Planned: integration (not run; exact later plan)
Each item runs in a new run directory, on disposable books and a disposable local repository outside `D:\Git\lib-build`. There is no project Git mutation, push or network. The existing live-book refusal stays.

1. **H2, descriptor packaging:**
   - In a disposable repository, commit a synthetic target, requirement, authority file and `00.kernel/00.00.10.work/0799.synthetic-reserved/evidence/reserved05.01.json`.
   - Producer `preview`, `prepare`, `verify` → `intact`; `handoff_check check` → `valid`, with the descriptor row role `required`.
   - Expect: `reserved_check launch --expect reserved` → `reserved-launch-ready-as-declared`. The same package with `--expect ordinary` → `descriptor-in-ordinary-job`.
   - A package without the descriptor plus `--expect reserved` → `reserved-expected-missing-descriptor`.
2. **K1–K3, workflow pass03:**
   - open → attach 05.01 → `seal-return-local` (an LF return) → `record-review` request-next 05.02 → `open-pass 05.02`.
   - Assert the transitions seq 1–5 and the chain. `05.01.return.md` must be byte-identical to the input.
   - **Negatives:** seal again with different bytes → `occupied different content`; `open-pass 05.03` → `next pass not requested`; a hand-edited `investigation.json` that drops a transition → `history rewritten` on the next write; ordinary pass02 regression (N1NN `place-return` still works for the existing fixture).
3. **Stage and reconcile end to end:**
   - Commit `05.01.return.md` and `reserved05.02.json` in the disposable repository.
   - Prepare and verify 05.02 → `reserved_check stage --expect reserved` before attach → ready.
   - attach 05.02 → `seal-return-local` (a **CRLF** return) → `reconcile` → `reconciled-as-declared`, with unresolved and unique lists equal to the block.
   - **Negatives:** a stage check after attach → `stage-order`; a changed commit → `target-changed`; producer verify on a tampered OUT → `producer-not-intact`.
4. **The pins are checked before and after.** No existing tool bytes change.
