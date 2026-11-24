# Workers used, week to the Nov 26 reset

Running roll (t562u). Append one row per job. Claude and Codex both append here. Times are the machine's local time (America/Toronto).

| Date | Lead | Worker | Job | Page | Pass | Result | Time | Commit / report |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | Claude | Claude | 0422 plan, first version | 90.50.10.0422 | plan | pushed | ~25 min | returns 0b91d431, report reports/90.50.10.0422/plan/Claude-lead-20261123-1345.md |
| 2026-11-23 | Claude | Claude | 0422 plan, revision 2 (Prima's answers) | 90.50.10.0422 | plan | pushed | ~10 min | returns faf87ad2, report reports/90.50.10.0422/plan/Claude-lead-20261123-1354.md |
| 2026-11-23 | Claude | Claude | handover start: state check, blockers raised | 90.50.10.0422 | lead | stuck on 0408 close and 0422 init-page | ~5 min | reports/90.50.10.0422/lead/Claude-lead-20261123-1402.md |
| 2026-11-23 | Codex | Codex | MVP acting-lead handover review | 90.50.10.0408 | 05.01 | stopped on recorded Prime and 0416 handover conflicts | ~5 min | reports/mvp/lead/Codex-lead-20261123-1407.md |
| 2026-11-23 | Claude | Claude | 0422 faces 01, 04, 08 and publish (init by Matthew) | 90.50.10.0422 | page | published, waiting on 0408 and 0423 to close | ~10 min | packs a18af716, report reports/90.50.10.0422/lead/Claude-lead-20261123-1411.md |
| 2026-11-23 | Codex | Codex | Record t565s2260 MVP order and check authority | 90.50.10.0423 / 0426 / 0425 | lead | 0423 close and trial, then Claude's 0426, then 0425; 0408 Prime entry pending | ~1 min | reports/mvp/lead/Codex-lead-20261123-1418.md |
| 2026-11-23 | Claude | Claude | 0426 split-commands plan and pack text; 0422 plan revision 3 (grants re-pointed); 0422 face 04 decision | 90.50.10.0426 / 0422 | plan | pushed; 0426 needs Matthew's init-page | ~15 min | packs dcc23879, report reports/90.50.10.0426/plan/Claude-lead-20261123-1421.md |
| 2026-11-23 | Claude | Claude | 0426 faces 01, 04, 08 and publish (init by Matthew) | 90.50.10.0426 | page | published, waiting on 0423 close and trial | ~5 min | packs 044bef48, report reports/90.50.10.0426/lead/Claude-lead-20261123-1423.md |
| 2026-11-23 | Claude | Claude | read Prima's answer (t568u); confirmed 0408 closed; raised acting-lead actor rule and 0423-trial wait | 90.50.10.0426 / 0422 | lead | waiting on 0423 close; two points for Matthew | ~5 min | reports/90.50.10.0426/lead/Claude-lead-20261123-1430.md |
| 2026-11-23 | Codex | Codex | signoff and close as Prima under t567u | 90.50.10.0408 | 05.01 | failed; w01 and w02 accepted; 0701 trial carried | lead turn ~8 min total | returns 21be13b; packs 7450d7a; reports/mvp/lead/Codex-lead-20261123-1431.md |
| 2026-11-23 | Codex | Codex | draft, verify and publish pack as Prima | 90.50.10.0423 | 05.01 | published for Grok-5 | same lead turn | packs be6ade5; returns ff34cd7; reports/mvp/lead/Codex-lead-20261123-1431.md |
| 2026-11-23 | Codex | Grok-Check | review Grok-1's published handover return | 90.50.10.0416 | 05.01 | running per Matthew; Grok-2 on hold | in progress | pass branch e07cf426; reports/mvp/lead/Codex-lead-20261123-1431.md |
| 2026-11-23 | Codex | Grok-5 | build one-worker | 90.50.10.0423 | 05.01 | pack published; prompt provided for Matthew to relay | claim not verified | packs be6ade5; reports/mvp/lead/Codex-lead-20261123-1431.md |
| 2026-11-23 | Codex | Codex | t570u lane rebalance and published pack verification | 90.50.10.0423 | 05.01 | same Grok-5 pack; awaiting return; other watches handed to Claude | lead turn ~2 min total | packs be6ade5; returns ff34cd7; reports/mvp/lead/Codex-lead-20261123-1436.md |
| 2026-11-23 | Codex | Codex | draft book-prime against planned 0426 split and probe baseline | 90.50.10.0425 | 05.01 draft | draft ready on returns; pack waits for 0426 close | same lead turn | labs/mvp-plan/PACK-0425-05.01.txt; reports/mvp/lead/Codex-lead-20261123-1436.md |
| 2026-11-23 | Codex | Grok-2 | build one-worker, reassigned from unused Grok-5 slot | 90.50.10.0423 | 05.01 | assigned; claim pending | pending | packs be6ade5; reports/mvp/lead/Codex-lead-20261123-1438.md |
| 2026-11-23 | Claude | Claude | signoff + close 0416.05.01 failed, jobs accepted (typed as prima, t570u) | 90.50.10.0416 | 05.01 | closed failed | ~10 min | returns 49654b6a, packs b30ff68b |
| 2026-11-23 | Claude | Claude | 0426 revision 2; faces 01 and 06; draft and pack 0426.05.01 for Grok-3; check prompts 0419.05.02 and 0407.05.01; 0424 prompt for Grok-4 | 90.50.10.0426 | 05.01 | packed | ~20 min | packs 40091ee4, returns d08ee0de, report reports/90.50.10.0422/lead/Claude-lead-20261123-1439.md |
| 2026-11-23 | Codex | Grok-2 | build one-worker | 90.50.10.0423 | 05.01 | returned; two compatibility risks disclosed | 32m17s claim to return | build 1b0d2c1; returns 85d951f; reports/mvp/lead/Codex-lead-20261123-1631.md |
| 2026-11-23 | Codex | Grok-Check | independent check of Grok-2 return | 90.50.10.0423 | 05.01 | prompt given to Matthew; verdict pending | pending | returns 85d951f; reports/mvp/lead/Codex-lead-20261123-1631.md |
| 2026-11-23 | Codex | Grok-Check | independent check | 90.50.10.0423 | 05.01 | failed, two replay regressions reproduced | recorded wf check 11.939s; total unreported | f5125ea; reports/mvp/lead/Codex-lead-20261124-1253.md |
| 2026-11-24 | Codex | Codex | signoff and close as Prima | 90.50.10.0423 | 05.01 | closed failed; w03, w04 and w06 carried | lead turn ~5 min total | returns 1fdef9a; reports/mvp/lead/Codex-lead-20261124-1253.md |
| 2026-11-24 | Codex | Codex | draft and publish repair pack as Prima | 90.50.10.0423 | 05.02 | verified and packed | same lead turn | packs 49295a6; returns ec64190; reports/mvp/lead/Codex-lead-20261124-1253.md |
| 2026-11-24 | Codex | Grok-2 | build replay compatibility repair | 90.50.10.0423 | 05.02 | assigned; claim pending | pending | packs 49295a6; reports/mvp/lead/Codex-lead-20261124-1253.md |
| 2026-11-24 | Codex | Grok-1 | verify 0701 recovery evidence and draft 0423 trial checklist | 90.50.10.0701 | 05.03 prep | assigned, report only | pending | returns d34fe49; reports/mvp/lead/Codex-lead-20261124-1305.md |
| 2026-11-24 | Codex | Grok-1 | verify recovery evidence and draft trial scenarios | 90.50.10.0701 | 05.03 prep | report-only complete; release publication gap found | ~9 min | returns 7f5f7b9; reports/mvp/lead/Codex-lead-20261124-1319.md |
| 2026-11-24 | Codex | Grok-2 | replay compatibility repair | 90.50.10.0423 | 05.02 | returned; older unlocked fixtures fail | 21m17s claim to return | build bf520780; returns a21473c; reports/mvp/lead/Codex-lead-20261124-1324.md |
| 2026-11-24 | Codex | Grok-Check | independently check replay compatibility | 90.50.10.0423 | 05.02 | relay prompt prepared for Matthew | pending | returns a21473c; reports/mvp/lead/Codex-lead-20261124-1324.md |
| 2026-11-24 | Codex | Codex | build Stage 1 operating checklist and acceptance map | 90.50.10.0498 | plan | current evidence and dependencies recorded | ~2 min | labs/mvp-plan/README.md |
