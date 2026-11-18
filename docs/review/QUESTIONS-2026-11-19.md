# Questions for Matthew, Thu Nov 19, 2026 (after the usage reset)

Saved by Prima while Matthew was away (t337u: "Keep going work around any issues you need me to address. We can deal with them tomorrow when usage resets."). One at a time, each in four parts in its source doc. Most important first.

1. Who approves an AGENTS.md option? (AGENTS-MANAGER-t333u.md M1) Proposed: you, on the exact text, after Tester's hostile check.
2. Which sections are locked in the kernel? (M2) Proposed: Axioms, Three tests, Evidence, Disagreement, Records, No self-check, Secrets.
3. Build the manager first as `wf agents build|verify`? (M3) Proposed: yes, moved into the compute core later.
4. Version numbers: the compute gives the next number, a model never picks it; stop and ask if it differs from your words. (LIB-MINE-M2.md Q1) Proposed: yes.
5. May a model type up your words as the source for an option? (LIB-MINE-M2.md Q2) Proposed: only after you confirm the typed text; the compute stamps "confirmed by".
6. Can a rule be locked (C9), and the 0000-0009 layout (C10). (LIB-MINE-M1.md Q1, roadmap section 8)
7. Joining characters (ZWJ/ZWNJ): wf refuses them, so emoji combos and some Hindi/Persian words are refused. (WF-90.30.md section 9) Proposed: keep refusing in names and addresses; decide later for free notes.
8. Board: tool words as columns with body-shop side labels; STALE after 24h; log-only first. (WF-BOARD.md Q1-Q3)
9. Handoff trial: run it (8 runs), the planted line, the answer key, Tester as scorer, read-only workers. (HANDOFF-TRIAL-01.md section 9)
10. t262u reading: several models working one page at the same time (unanswered card t318s1214).
11. Roadmap conflicts C1-C12 and guard G1-G7 (roadmap sections 8 and 9), as time allows.
12. Disk: 89% full; may Tester's old scratch folders (tester-3003 475M and others) be deleted?

Already answered (do not re-ask): Researcher's M2 Q3 = the three safety rules, approved t335s1296.

Added 3:56 PM EST:
13. `wf board` (read-only kanban view) is built on branch board-dev; Tester's check found two narrow fixes, now being fixed. Its AGENTS.md/README lines use the proposed answers to question 8 and are marked "build stage, pending Director answer". Tester flags ax1: with no ruling yet, those lines should not merge into the workflow branch's AGENTS.md. Proposed: answer question 8, then Prima merges board-dev into workflow.

Added 4:16 PM EST:
14. Log order check (branch harden-dev, 385452a): wf now refuses to read a page whose log has steps in the wrong order. Tester passed it. One test page made with two different wf versions (halted by the new one, then packed by an old one with no halt) is now stuck: every write is refused, resume included. No real page has this. Why it matters: axiom 6 says the past should not block the next step for good. Proposed: new writes must always follow the order; a page that already has an out-of-order entry still loads, shows "out of rule at entry N" on status and board, and allows only resume or a Prime note. The order rules have no Director ruling yet, so they are marked build stage.
15. The old wf binary (wf-bin/wf-8eb1fdb) can still write pages and does not know about halt. Proposed: rename it to wf-8eb1fdb.old-do-not-write (a rename, not a delete) so nobody runs it by accident.
16. Merge harden-dev into workflow together with board-dev, after question 14.

Added 5:08 PM EST:
17. harden-dev now ends at 1f32ecb. Tester passed every round up to a7f9700 and called the series ready. 1f32ecb is a one-line display fix (the observe loop line escapes close outcomes) and has its own test, but Tester has not checked it yet; Tester checks it first tomorrow. Option for later: refuse at load a close whose outcome differs from its signoff's (stronger than escaping). Proposed: yes, as a small follow-up after question 14 is answered.
