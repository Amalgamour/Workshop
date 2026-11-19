# How WF testing went (report for Matthew)

Written by Prima on Thu Nov 19, 2026, about 11:50 AM EST.
Your ask (t391u, 11:39 AM EST): "Then I want your report on how WF testing went."
Every number here comes from a file or a git log. The source is in brackets after it.

How to read this:
- A **commit** is one saved step of code, named by a short id such as a00bc53.
- **Tester** is the model that checks the work. A builder never checks its own work (axiom 9).
- **Unit tests** check small parts of the code. **End-to-end tests** run the whole `wf` tool the way a person would. [side label: e2e]
- A **hostile pass** is Tester trying to break the tool on purpose, for example with a faked log.

---

## 1. What WF is

WF is a small tool called `wf`. It runs one page per piece of work.
Nobody writes on a page by hand. People and models ask `wf`, and `wf` writes every step into one log file.
The log is the truth. The other page files are copies printed from it. A hand edit is caught and refused.
A piece of work moves in passes: Prime plans it, a builder does it, a checker tests it, and Prime signs it off.
[workflow branch a00bc53: README.md lines 3-14, docs/DESIGN.md section 5]

---

## 2. What was tested, and how

There were three kinds of test.

1. **The tool's own tests.** Each new commit came with new tests. Tester rebuilt the code in a fresh folder and ran them all.
2. **Failing first.** Tester ran the new tests on the code from *before* the change. They had to fail there. That proves each test really tests the new thing.
3. **Hostile passes.** Tester faked logs, hand-edited files, stripped hashes, planted extra files and tried to dodge every rule.

And one real-world test:

4. **The real pages.** The three real pages (90.10, 90.20 and 90.30, each `.00.0001`) were checked read-only after every change. They must still verify, and none of their 106 files may change.

The real pages are also real use. Together they hold 19 closed passes. 12 passed and 7 failed and were redone. One return was refused and one observer finding was filed. [read from the three `wf-run/pages/*/log.jsonl` files today]

---

## 3. Results, branch by branch

None of these branches is merged into `workflow`. Merges wait for you.

| Branch | Head | What it adds | Latest tests | Tester |
|---|---|---|---|---|
| `workflow` (on GitHub) | a00bc53 | The tool you can build today. The real pages were made with it. | 29 unit + 78 e2e, all pass | Pass (page 90.30, entry 35) |
| `board-dev` | 193da07 | `wf board`: a read-only work-order board | 41 unit + 92 e2e, all pass | Pass after one fix round |
| `harden-dev` | 2b5a7ef | Refuses faked or wrong-order logs; escapes text that could fool your screen | 43 unit + 117 e2e, all pass | Pass |
| `merge-rehearsal` | 52d35db | A practice merge of board-dev and harden-dev (1f32ecb) | 43 unit + 110 e2e, all pass | No conflicts; real pages ok |
| `q14-draft` | 5b14a7c | Draft answer to question 14: a bad log entry is skipped, and the page still loads | 43 unit + 113 e2e, all pass | Pass after one fix round |
| `agents-hash` | c224329 | Fingerprints on AGENTS.md and PROMPT.md, the hashed links, the mid-pass lock, the merged v3 AGENTS.md | 45 unit + 133 e2e, all pass | Pass |

Sources:
- a00bc53: I rebuilt it today in a fresh folder and ran its tests (29 unit + 78 e2e, 0 failed). The page 90.30 journal gives the same counts [docs/journal/2026-11-18-wf-90.30.md, "The short version"].
- 193da07: [scratch/tester-board2/run-new-1.txt].
- 2b5a7ef: [scratch/tester-harden9/CHECK-RESULTS.md, "Suite"].
- 52d35db: [merge-rehearsal docs/spec/MERGE-REHEARSAL.md, "Result"].
- 5b14a7c: [scratch/tester-q14b/FINDINGS.md].
- c224329, and a786566 before it (45 unit + 132 e2e): [scratch/tester-ahash/CHECK-a786566-c224329.md, "Builds"].

The agents-hash steps, one at a time. Each one passed Tester's check and its failing-first run.

| Commit | What it does | Tests | Source |
|---|---|---|---|
| b3ecb44 | Records a fingerprint of each AGENTS.md and PROMPT.md when it is issued (t373u) [side label: SHA-256] | 43 + 121 | CHECK-RESULTS.md |
| bbcec61 | Reuses an AGENTS.md when its text has not changed (t378u) | 44 + 124 | CHECK-RESULTS.md |
| adcadad | A narrow v3 AGENTS.md with 4 links, each with a fingerprint (t379u, t380u) | 44 + 128 | CHECK-4e64e47.md |
| 4e64e47 | A pack with its fingerprints stripped is invalid. A rule file that changes during an open pass locks that pass (t381u, t382u, t383u) | 44 + 132 | CHECK-4e64e47.md |
| a786566 | Merges your t386u AGENTS.md review, using my keep or drop choices | 45 + 132 | CHECK-a786566-c224329.md |
| c224329 | `status` shows the lock. The read-only `observe` still runs on a locked page | 45 + 133 | CHECK-a786566-c224329.md |

The real pages: on every binary in this series, 90.10, 90.20 and 90.30 verify ok with 85, 49 and 37 entries. All 106 files are unchanged. [CHECK-4e64e47.md, "Real pages"; CHECK-a786566-c224329.md, "Real pages"]
I checked the same three counts today with the pinned tool `wf-bin/wf` (built from a00bc53).

---

## 4. Holes found, and fixed

These were found by Tester and then fixed. Each fix was re-checked.

1. **A crash on a strange log.** A log entry for a pass that was never drafted made the board crash for every page. Fixed in 193da07. [docs/journal/2026-11-18-wf-board-and-log-order.md]
2. **A faked log could steer a command.** Entries out of order were accepted. Now a log that breaks the order is refused, with the entry number and the rule. Fixed from 385452a on. [same journal]
3. **A failing check could look like a pass.** A builder's test output could use screen codes to repaint the checker's screen as "pass". This was the most serious hole. Output is now escaped. Fixed in e2ee1c0. [scratch/tester-harden8/SWEEP-FINDINGS.md item 1; tester-harden9/CHECK-RESULTS.md item 1]
4. **Faked names printed raw in refusals.** Fixed in 2b5a7ef and b3ecb44. [tester-harden9/CHECK-RESULTS.md; tester-ahash/CHECK-RESULTS.md]
5. **A skipped bad entry was still counted** as a failed check on the board. Fixed in 5b14a7c. [tester-q14/FINDINGS.md, tester-q14b/FINDINGS.md]
6. **A hand-edited AGENTS.md could pass.** Now it is invalid, and `--fix` will not wash it clean. Fixed in b3ecb44. [tester-ahash/CHECK-RESULTS.md section 2]
7. **Stripping the fingerprints made a new page look old,** so its files could be swapped. Closed for labelled packs in 4e64e47. [CHECK-4e64e47.md claim 1]
8. **An extra AGENTS.md planted on a reusing pass was not noticed.** It now gives a warning. Fixed in 4e64e47. [CHECK-4e64e47.md claim 2]
9. **A locked page said nothing about the lock,** and `observe` refused to run. Fixed in c224329. [CHECK-a786566-c224329.md]

---

## 5. Still open

1. **The outside-anchor hole (parked).** Someone who rewrites a page's whole log can make it look like an old page. Then `wf verify --fix` swaps in the old v1 AGENTS.md and PROMPT.md without a warning. Nothing inside the page can catch a full rewrite. The fix is a copy of the log's fingerprint kept outside the page. I parked it with the "pins by revision" idea, because both need the same outside record. [CHECK-4e64e47.md, "Residual hole"; docs/design/AGENTS-V3-REVIEW-decisions.md]
2. **The car-steering examples are broken.** They broke on 17 Nov at commit 8a2c6eb, before this series. They are not a new break. [tester-ahash/CHECK-RESULTS.md section 5]
3. **One small display leftover.** In the v3 links table, backticks and `](` are not escaped. A markdown viewer can show a faked cell oddly. It cannot add a column or get past verify. [CHECK-a786566-c224329.md, part (b)]
4. **Some text is still printed raw.** These are names you type yourself on the command line, and some page view files. [tester-harden9/CHECK-RESULTS.md, "Still raw"]
5. **Merges held for you.** Nothing new is merged into `workflow`.
   - board-dev and harden-dev wait on questions 8 and 13-16. [docs/review/QUESTIONS-2026-11-19.md]
   - q14-draft waits on questions 14, 18 and 19.
   - agents-hash waits on your OK of this round.
   - q14-draft and agents-hash grew from different points. They have not been merged or tested together yet.
6. **Names are not proven.** `wf` trusts `--as <name>`. Any agent could type `--as matthew`. This is a known gap in v0. [workflow README.md, "Not in v0"]
7. **Not tested on Windows.** Every test ran on this Linux box. I can't test on Windows. Risks are listed in docs/guide/LOCAL-BUILDER-SETUP.md.

---

## 6. What this means for real builders

- The loop works end to end: page, draft, pack, claim, return, check, signoff, close. It ran 19 real passes, and failed passes were caught and redone.
- The tool you can build today is a00bc53. It is on GitHub, the pinned tool is built from it, and the real pages were made with it.
- a00bc53 does **not** have the newer fixes. The worst missing one is hole 3: a failing check can repaint the screen. So with a00bc53 the checker must confirm the verdict with `wf status` or the `05.md` view. Those always show the true result from the log.
- The newer branches are safer, but they are not merged. They are also not on GitHub yet.
- Every agent on your machine can claim any name. So keep one builder at a time, and watch what each one does.

---

## 7. Ready or not

**Ready for a small, watched trial. Not ready for builders working alone.**

Why it's ready:
- Every Tester round on every branch ended in a pass.
- The real pages verify on every version.
- The loop has already run 19 real passes.

Why not yet for builders working alone:
- Names are not proven.
- The newest fixes are not merged.
- a00bc53 still has the screen-repaint hole.
- The outside-anchor hole is parked.
- Windows is untested. The line-ending risk could make every check fail on day one.

My advice: run one trial page on your machine with one builder, one checker and you watching. Use a00bc53. Merge the newer branches after you answer the held questions.
