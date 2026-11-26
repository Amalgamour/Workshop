# Fire sale: proposed fixes to the Nov 30 work page

state: proposal, for Prima to approve. By Prima's fire-sale worker, Thu Nov 26 2026, 12:27 AM EST.
Page: docs/plan/WORK-PAGE-2026-11-30.md at local f6d47b0. **The page was not edited.**
Findings: docs/review/FIRE-SALE-2026-11-26-WORK-PAGE-REVIEW.md (F1-F16 and F19 are about this page; F17-F18 are about the EOW page, which is done, so they are left out).

How to use this:
- Each fix gives the line, the current text (exact), and the replacement text (exact).
- "Insert after line N" means a new line. Line numbers are from f6d47b0. Apply from the bottom up so the numbers hold.
- Fixes marked **Prima decides** change an option or a default. The text is a draft. Prima, as lead, keeps or drops it (t387u-t390u). Anything that changes what Matthew is asked goes to him as a question, with the design-following option marked "(default)" (t384u).
- State facts are as of returns ec78461d (Wed 5:41 PM EST). Re-check returns before applying F2.

## Summary

| Fix | Finding | Severity | Lines | Kind |
|---|---|---|---|---|
| 1 | F1 Q13 default known to fail | High | 147 | Prima decides |
| 2 | F2 X3/X4 stale after 0423.05.03 failed | High | 99, 100 | text |
| 3 | F3 X3 misses catch row 18 | High | 99 | text (merged with fix 2) |
| 4 | F4 Claude check not assigned | High | 42, new rows after 116 | Prima decides (adds packs) |
| 5 | F5 manual-return block in no-wf prompts | Medium | 169-175, 197-203 | text |
| 6 | F6 no done status | Medium | new lines after 60 | text |
| 7 | F7 Claude prompt skips packs | Medium | 159 | text |
| 8 | F8 C20 dispute has no judge | Medium | 87 | text |
| 9 | F9 Q6 default and ★ split | Medium | 137 | Prima decides |
| 10 | F10 "8 prompts" | Medium | 86 | text |
| 11 | F11 C18 misses row 17 | Low | 85 | text |
| 12 | F12 untestable Done-when cells | Low | 77, 79, 99-116 | text |
| 13 | F13 "this week" | Low | 15, 84, 85 | text |
| 14 | F14 report path for packs/ | Low | 35 | text |
| 15 | F15 X15 source | Low | 111 | text |
| 16 | F16 X20 short id | Low | 116 | text |
| 17 | F19 Claude "touch no data" line | Low | 163 | text |

## Fixes

### Fix 1 (F1, High, Prima decides). Q13.

Line 147, current:
> 13. **Q5. The three unclaimed packs (0426, 0424, 0418).** A, default ★: approve a pinned build with withdraw, then the Prime withdraws each and repacks. B: keep them held.

Replace with:
> 13. **Q5. The three unclaimed packs (0426, 0424, 0418).** Note: withdraw-then-repack does not work today. `wf draft` refuses a pass whose tail is not "closed" (catch log row 19; Codex X1, labs/review-draft-page/X1-README-REVIEW.md:64). A, default ★: keep the three packs held until a granted wf fix makes "withdrawn" final for drafting, then the Prime withdraws each and repacks. B: approve a pinned build with withdraw now and accept that repack waits on that fix. C: keep them held with no fix planned.

Why A is the default: it follows the existing design (no pass reopened by hand, wf stays in control, t528u) and asks for no step the tool refuses.

### Fix 2 and 3 (F2 + F3, High). X3 and X4.

Line 99, current:
> | X3 | labs/stage1-route/ | Refresh PAGES.csv. Fix 0407 (closed failed, returns bbb7d956). Add 0419 closed passed and 0423.05.03 packed. | Every row matches the latest log entry. Repeat X3 at the start of any day after a close. |

Replace with:
> | X3 | labs/stage1-route/ | Refresh PAGES.csv. Fix 0407 (closed failed, returns bbb7d956). Fix 0423: 05.03 closed failed (returns ec78461d), w02 carried to a later 05.04. Add a column "code on returns": for each closed page, yes or no, with the commit (0416's c5bde1e2 is only on pass/90.50.10.0416.05.01, catch log row 18). | Every row matches the latest entry in the returns log, with its commit. Every closed page has "code on returns" filled. |

Line 100, current:
> | X4 | labs/stage1-route/packs/ | Replacement pack text for 0426.05.01, at the post-0423.05.03 head. | A full draft file, ready for Prima. |

Replace with:
> | X4 | labs/stage1-route/packs/ | Replacement pack text for 0426.05.01. Start commit: the returns head after 0423.05.04 closes. If 05.04 is not closed when you start, write "waiting on 0423.05.04" and stop. | A full draft file that names: start commit, grant paths, may-touch, done-when lines, and files confirmed free against labs/stage1-route/QUEUE.md (with its commit). |

(The "Repeat X3" duty moves to Fix 6's status block.)

### Fix 4 (F4, High, Prima decides). Independent check of Claude's work.

Line 42, current:
> - Every Claude change is checked by another view before anyone uses it. Codex checks the design labs. Prima reviews each pack.

Replace with:
> - Every Claude change is checked by another view before anyone uses it. Codex checks the design labs (packs X21-X23). Prima reviews each pack. A Claude pack is "not usable until checked" until its check row below says passed.

Insert after line 116 (new rows in the Codex table):
> | X21 | labs/review-claude-specs/ | Hostile check of C4-C9 (pin-record, pin-move, delegated-grant). C8 first: it widens Prima's authority. | Each spec marked holds, breaks or unclear, with cites. Any widening of authority listed as a question for Matthew. |
> | X22 | labs/review-claude-specs/ | Hostile check of C10-C15 (overlap-check, stale-pack, retire-0409). | Same as X21. |
> | X23 | labs/review-claude-specs/ | Hostile check of C16-C19 (catch-log-flow, prompt-check). | Same as X21. |

Note for Prima: this adds 3 Codex packs (about 15% of Codex's week at t588u's 5% a run). If that is too much, the other choice is to name Prima or Grok-Check as checker per pack, in a new "Checked by" column. The folder name labs/review-claude-specs/ must be added to the Codex lane list (line 58) so lanes stay disjoint. The EOW UI-1 check (d7da9e80) is not on this page; it needs its own row or note.

### Fix 5 (F5, Medium). Manual-return block in no-wf prompts.

Lines 169-175 (Claude prompt), current: the 7-line block that starts
> MANUAL RETURN (docs/plan/MANUAL-RETURN.md). If wf fails:

Replace all 7 lines with:
> You run no wf command. If anything seems to need wf, stop and write it as a question in your report.

Lines 197-203 (Codex prompt): the same 7-line block. Replace with the same one line.

Why: both prompts already say "Run no wf command" (lines 27, 164). The block tells a no-wf worker how to retry wf.

### Fix 6 (F6, Medium). Done status.

Insert after line 60 (before the heading "## Claude packs (design and hostile review)" at line 61):
> **Status (update after each return).** Done: C1 (returns 128a541b), X1 (returns bf7014ad). Next: C2, X2. Matthew fills the pack number from "Next".
> After any close, re-run X3 before the next stage1-route pack.

### Fix 7 (F7, Medium). Claude reads packs.

Line 159, current:
> 1. git fetch origin; git pull --ff-only origin returns. Also read origin/prima/build.

Replace with:
> 1. git fetch origin; git pull --ff-only origin returns. Also read origin/packs and origin/prima/build (read only).

### Fix 8 (F8, Medium). C20 judge.

Line 87, current:
> | C20 | labs/draft-page/ | RESPONSE.md: answer Codex's hostile review (X1-X2). Accept or dispute each finding. | Every finding answered with a cite. No rule weakened. |

Replace with:
> | C20 | labs/draft-page/ | RESPONSE.md: answer Codex's hostile review (X1-X2). Accept or dispute each finding. Prima rules on each dispute. | Every finding answered with a cite. No rule weakened. Each dispute listed for Prima's ruling; any reversal goes in the catch log (written by Prima, not Claude). |

### Fix 9 (F9, Medium, Prima decides). Q6 default and ★.

Line 137, current:
> 6. **Q5. Where does a draft's page log live?** A, default: on the draft branch. B ★: a later wf change, so the log always goes to returns (one live record). C: by hand.

Proposed (B as default, since ★ marks the axiom 2 fit and R37 item 1 says one append-only log is the only source of truth):
> 6. **Q5. Where does a draft's page log live?** A: on the draft branch. B, default ★: a later wf change, so the log always goes to returns (one live record, R37 item 1). C: by hand.

If Prima reads A as the design-following option, flip it: A gets "default ★" and the ★ comes off B. Either way, one option carries both marks.

### Fix 10 (F10, Medium). Prompt count.

Line 86, current:
> | C19 | labs/prompt-check/ | Run the C18 checklist against the 8 prompts on WORK-PAGE-2026-11-25.md. | A table: prompt, item, pass or fail. |

Replace with:
> | C19 | labs/prompt-check/ | Run the C18 checklist against the 6 prompts on WORK-PAGE-2026-11-25.md (A1-A4, B1, B2). | A table: prompt, item, pass or fail, with all 6 prompts present. |

### Fix 11 (F11) and 13 (F13, Low). C17, C18, and "this week".

Line 84, current:
> | C17 | labs/catch-log-flow/ | Two worked examples from this week's real checks. | Both examples cite their check entry. |

Replace with:
> | C17 | labs/catch-log-flow/ | Two worked examples from real checks in the week of Nov 23. | Both examples cite their check entry. |

Line 85, current:
> | C18 | labs/prompt-check/ | A checklist of prompt mistakes, from this week's prompts and catch log rows 12-13. | Each item has an example and how to catch it. |

Replace with:
> | C18 | labs/prompt-check/ | A checklist of prompt mistakes, from the prompts of the week of Nov 23 and catch log rows 12, 13 and 17. | Each item has an example and how to catch it. |

Line 15, current:
> ## Issues from this week

Replace with:
> ## Issues from the week of Nov 23

### Fix 12 (F12, Low). Testable Done-when cells.

| Line | Pack | Current Done when | Replacement |
|---|---|---|---|
| 77 | C10 | Spec and the cost of each option. | Spec with 2 or 3 options, each with its cost (files touched, new tests). |
| 79 | C12 | Spec and the cost of each option. | Spec with 2 or 3 options, each with its cost (files touched, new tests). |
| 101 | X5 | Same as X4. | Same as X4 (start commit, grant paths, may-touch, done-when lines, files confirmed free against QUEUE.md). |
| 103 | X7 | Full draft. Files confirmed free. | Full draft. Files confirmed free against labs/stage1-route/QUEUE.md, citing its commit. |
| 112 | X16 | Every piece links to its source. | Every wf command, kernel page and stage 1 page listed, each with a link to its source file. |
| 113 | X17 | Same. | Every file in docs/plan, docs/quality and reports/ listed, each with a link. |
| 115 | X19 | A list, and fix options for Matthew. | A list, and 2 or 3 fix options for Matthew, each written in four parts. |

X8-X12 ("Same.") follow X7 once line 103 is fixed. X3's standing duty is moved by Fix 2 and Fix 6.

### Fix 14 (F14, Low). Report path.

Line 35, current:
> - Report path: `reports/lab/<folder>/<Agent>-<YYYYMMDD-HHMM>.md`, local time.

Replace with:
> - Report path: `reports/lab/<folder>/<Agent>-<YYYYMMDD-HHMM>.md`, local time. For a subfolder such as labs/stage1-route/packs/, use the top folder: `reports/lab/stage1-route/`.

### Fix 15 (F15, Low). X15 source.

Line 111, current:
> | X15 | labs/0498-accept/ | Map each of the 11 Stage 1 acceptance items to its evidence. | Every item has a source, or is marked missing. |

Replace with:
> | X15 | labs/0498-accept/ | Map each of the 11 Stage 1 acceptance items (docs/plan/MVP-GOAL-PROPOSAL.md) to its evidence. | All 11 items listed. Every item has a source, or is marked missing. |

### Fix 16 (F16, Low). X20 address.

Line 116, current:
> | X20 | labs/intake-0001-0403/ | Read-only: why does intake always refuse 0001 and 0403? | Cause, with cites, and repair options. |

Replace with:
> | X20 | labs/intake-0001-0403/ | Read-only: why does intake always refuse 90.50.00.0001 and 90.50.10.0403? | Cause, with cites, and 2 or 3 repair options. |

### Fix 17 (F19, Low). Claude: touch no data.

Line 163, current:
> 5. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule.

Replace with:
> 5. Put any rule conflict as a question for Matthew. Do not decide it. Do not weaken any rule. Touch no data, logs or test files (t580u).

## Not proposed

- F17, F18: the EOW page is done (UI-1, UI-2 returned). Fixing it changes nothing for workers.
- No change to any question's meaning beyond Fix 1, Fix 4 and Fix 9.
