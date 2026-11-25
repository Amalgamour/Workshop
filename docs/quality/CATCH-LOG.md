# Catch log

**Purpose.** One place to see where mistakes happen, how they get caught, by whom, and why it matters. Refusals count too. A model refusing work that breaks our standards is a success, so it goes here.

**Who writes it.** The checker or the Prime. Never the model that made the mistake. (Matthew, t586u.)

**When.** At check, signoff or close. Or as soon as a refusal or catch happens.

**Rules.**
- One row per event.
- Append only. The newest row goes at the bottom. Never edit or delete an old row. To correct one, add a new row that points back to it (axiom 6).
- Cite a commit, a log entry or a Director message for every row. No evidence, no row.
- Times are EST.

**Kinds.**
- **mistake**: something wrong got made.
- **refusal**: a model or wf said no to work that broke a rule.
- **catch**: a check, test or review found a mistake before it was accepted.
- **near-miss**: it could have caused harm, but did not.

| # | Date (EST) | Page.pass | Kind | What happened | Who made it | Caught by | How caught | Why it matters (axiom) | Outcome / fix | Evidence |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Mon Nov 23, 10:49 AM | 0701.05.03 | mistake | Two returns were written to the 0701 log at nearly the same time. The 05.02 return replaced the 05.03 return, so the log stopped growing only at its end. | wf return race (two builders, one page log) | Grok-1 (recovery prep), Codex (review) | Prime review | 6: the past is not rewritten | Replayed 05.03 by append only on Tue 2:43 PM. Original work kept. | a3a0f83a (log break), 7f5f7b9, ab33552, 3f8cbd11 |
| 2 | Mon Nov 23, 2:35 PM | 0408.05.01 | catch | The return had no lab trial file tests/lab_0408.rs. | Grok-2 (builder) | Grok-Check | checker | 9: trial before promotion | Closed failed, cards accepted. Lab trial carried to 0701. | 0408 entry 9, report 8d168644, close 21be13b9 |
| 3 | Mon Nov 23, about 3 PM | lead split (0422, 0423, 0426) | mistake | Prima's sub-lead split gave both acting leads work that needed the same locked files, with no way forward. | Prima | Director | Director | 5: frame must let the work finish | Lanes rebalanced. Lesson: every worker needs a free lane. | t569u, t570u; Codex-lead-20261123-1436.md |
| 4 | Mon Nov 23, 3:33 PM | 0416.05.01 | catch | No Linux run of cargo test --test wf, and one Windows test went over its 10 s limit. | Grok-1 (builder) | Grok-Check | checker | 9: trial before promotion | Closed failed, Windows fixes kept. | 0416 entry 10, report 478c150c, close 49654b6a |
| 5 | Mon Nov 23, 5:43 PM | 0423.05.01 | catch | The lockout build could not read logs published before the lockout existed. Two replay regressions. | Grok-2 (builder) | Grok-Check | checker, test | 6: published history must stay readable | Closed failed. Repair 05.02 passed. | check f5125ea (entry 10), close 1fdef9ad |
| 6 | Tue Nov 24, 3:07 PM | 0701.05.02, 0701.05.03 | catch | Both lab checks passed, but the sealed done-when asked for the whole Windows suite, and it still had failures. | (start harness, not the builders) | Codex (acting lead) | Prime review | 4: never claim done without the why met | Closed failed, so the record does not claim the full suite passed. Lab cards accepted. | 14467f3e |
| 7 | Tue Nov 24, 2:22 PM (found Wed Nov 25, about 12:30 PM) | 0423.05.02 | catch | The lockout fix passed its two packed checks, but 131 older tests stopped running ("lockout first" in the test helpers). Builder and checker reported page_0408 and wf.rs. They missed lab_0404 and page_0407. | Grok-2 (builder); pack scope by acting lead | Prima | Prime review (full-suite re-run on the box) | 9 and 7: a dark test suite is a hole | Packed 0423.05.03 to make the helpers take the lock. | bf520780, return a21473c, check fca0563, pack 1e0d74c6 |
| 8 | Wed Nov 25, about 12:45 PM | box (0423 trial) | mistake | The executor deleted the box folder /tmp/lab0423-failed-1b0d2c1 without asking. It was a cache another run had made. | Grok Bot (executor) | Grok Bot (executor) | self-report | 1: deleting box files needs Matthew's yes | Reported to Matthew. The cache rebuilds itself. | executor report, Wed Nov 25 |
| 9 | Wed Nov 25, 1:04 PM | 0001, 0403 | near-miss | wf intake refuses these two pages every time: "the returned log does not continue this run folder's log". | (older log history) | wf | wf refusal | 6 and 8: a log must continue its own line | Known and left alone. Nothing taken. Not repaired yet (7). | intake output Wed Nov 25; Grok-Check reports f2178076, 28f055bc |
| 10 | Wed Nov 25, 1:12 PM | 0407.05.01 | catch | The return had no lab trial file tests/lab_0407.rs. | Grok-1 (builder) | Grok-Check | checker | 9: trial before promotion | Closed failed, cards accepted. Lab trial carried to 0701. | 0407 entry 10, report ef137eb2, close bbb7d956 |
| 11 | Wed Nov 25, 1:05 to 3:00 PM | 0701, 0419, 0407 closes; work page | mistake | 8 Prima-side commits were authored "t <t@t>", a test setting left on in the shell. Content and trailers were right. | Grok Bot (executor) | Grok Bot (executor) | self-check | 6: lineage must show who acted | Setting removed. Author confirmed Prima before every later commit. No force push, so old commits stay. | 3090160d, 07fe4d5f, ee40448d, a72be090, bbb7d956, b111fd1d, dcdab6385, a45807d |
| 12 | Wed Nov 25, afternoon | 0423.05.03 | refusal | Grok-2 refused to claim 0423.05.03 because it was not packed yet. | prompt relayed before the pack existed | Grok-2 | model refusal | 1: act only inside what is granted | Grant and pack done at 3:10 PM, then the prompt was reissued. | t581u; pack 1e0d74c6 |
