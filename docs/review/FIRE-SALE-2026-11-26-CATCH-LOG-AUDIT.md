# Catch log audit

File checked: docs/quality/CATCH-LOG.md (rows 1-19, local d675cb6, published 6853d434).

Written by the Prima fire-sale worker, Thu Nov 26 2026, finished 12:19 AM EST (log time).
All times are EST. This audit does not edit the catch log (it is append only).

## How I checked

- Every commit id in the Evidence column was looked up in the local repo and in a read-only clone of the public repo (all branches).
- For each one: does it exist, which branch holds it, its time and author.
- Cited files and line numbers were opened at the cited commit.
- Columns were counted per row.

## Result in one line

All 19 rows have 11 filled columns. 33 of 34 cited commits exist on GitHub. Most evidence holds. 9 findings, mostly small.

## Evidence that holds

| Row | Checked | Result |
|---|---|---|
| 1 | a3a0f83a (Mon 10:49 AM, return 0701.05.02), 7f5f7b9, ab33552, 3f8cbd11 (Tue 2:43 PM recover) | holds |
| 2 | 0408 log entry 9 is the Grok-Check check; 8d168644 report (Mon 2:37 PM); 21be13b9 close | holds |
| 3 | reports/mvp/lead/Codex-lead-20261123-1436.md is on returns | holds (path not given, see A7) |
| 4 | 0416 entry 10 is a check FAIL on cargo test --test wf; 478c150c, 49654b6a | holds |
| 5 | 0423 entry 10 is the check; f5125ea (Mon 5:46 PM), 1fdef9ad close | holds |
| 6 | 14467f3e close 0701.05.02 and .05.03 failed (Tue 3:07 PM) | holds |
| 7 | bf520780, a21473c (Tue 2:22 PM), fca0563, 1e0d74c6 pack (Wed 3:10 PM) | holds (outcome now stale, see A5) |
| 9 | Grok-Check reports f2178076:44 and 28f055bc:47 both say intake refused only 90.50.00.0001 and 90.50.10.0403 | holds |
| 10 | 0407 entry 10 check; ef137eb2 (Wed 1:13 PM); bbb7d956 close (1:37 PM) | holds |
| 12 | 1e0d74c6 pack at 3:10 PM matches "grant and pack done at 3:10 PM" | holds (time vague, see A8) |
| 13 | returns reports/lab/draft-page/Claude-20261125-1203.md:45 says exactly this; be9b6fb2 | holds |
| 14 | labs/draft-page/QUESTIONS.md:123-127 at 314784b8 ("Not a question, but raised", a823 has no withdraw or lockout) | holds |
| 15 | `git diff c1750c32 prima/build` on the four seqaddr-core files is empty; cc5f95fa QUEUE.md | holds |
| 16 | f1e2481a on pass/90.50.10.0423.05.03; tests/wf.rs:976-978 is the `#[cfg(unix)]` test `reprint_failure_after_append_says_logged_as` | holds (outcome now stale, see A5) |
| 17 | returns 128a541b; reports/lab/review-stage1-route/Claude-20261125-1450.md:10 "## Which pack" | holds (time, see A6) |
| 18 | c5bde1e2 is only on pass/90.50.10.0416.05.01, not on returns; C1-REVIEW.md:88 (P14) and :113 (U2) | holds |
| 19 | bf7014ad; X1-README-REVIEW.md:15, :64; src/cmd.rs@1e0d74c6 lines 293-298 refuse any tail not "closed" | holds |

## Findings

### A1. Medium. Row 11 cites a commit that is not on GitHub.
- Row 11 (CATCH-LOG.md:33) lists 8 commits. `a45807d` exists only in the local repo.
- Its published copy is `dcdab638`, which the row already lists as `dcdab6385`.
- So it is 7 commits, not 8. One id will never open for Matthew.
- Fix: add a new row pointing back to row 11: "a45807d is the local copy of dcdab638; 7 commits".

### A2. Medium. Row 11's time range is wrong.
- Row 11 says "1:05 to 3:00 PM".
- The 7 `t <t@t>` commits run from 12:49 PM (dcdab638) to 1:37 PM (bbb7d956, b111fd1d). I found no other `t` commit on any branch since Nov 24.
- Fix: in the pointer row, say "12:49 PM to 1:37 PM".

### A3. Medium. Row 8 has no checkable evidence.
- Row 8 (CATCH-LOG.md:30) evidence: "executor report, Wed Nov 25".
- The log's own rule (CATCH-LOG.md:12): "Cite a commit, a log entry or a Director message for every row. No evidence, no row."
- Fix: add a pointer row that cites a file or message (for example, the Director message where it was reported), or mark row 8 "evidence: self-report only".

### A4. Medium. Who writes a row when Prima made the mistake?
- Rule (CATCH-LOG.md:5): "The checker or the Prime. Never the model that made the mistake."
- Rows 3, 13, 14, 15 name Prima as the maker. Rows 8 and 11 name Prima's executor. All six were written in Prima's own commits (c96b1df rows 1-12, 35e2f49 rows 13-15).
- The rule has no case for "the Prime is the maker".
- This needs a Director ruling. Parked as Question Q1 below.

### A5. Low. Three outcomes are now stale and need a follow-up row.
- Row 7 says "Packed 0423.05.03". Row 16 says "Not closed. Listed for the 0423.05.03 check".
- 0423.05.03 closed **failed** at 5:41 PM Wed (returns ec78461d). w02 carried to a later 05.04.
- Rows 18 and 19 say "Open". No row records what happened next.
- Fix: one new row: "0423.05.03 closed failed (ec78461d); rows 7 and 16 carry to 05.04".

### A6. Low. Row 17's time does not match its evidence.
- Row 17 says 3:25 PM. The C1 commit 128a541b is 3:47 PM. Row 18 (same review) says 3:47 PM.
- 3:25 PM may be when the prompt was relayed. The row does not say.
- Fix: in a pointer row, say which event 3:25 PM marks.

### A7. Low. Some evidence cells give a file name with no folder or branch.
- Row 3: "Codex-lead-20261123-1436.md". The real path is reports/mvp/lead/ on returns.
- Row 9: "intake output Wed Nov 25" is not stored anywhere. The two reports cited next to it do hold the evidence.
- Fix: write full paths in new rows from now on.

### A8. Low. Row 12's date is "afternoon".
- Every other row has a clock time. The log says times are EST (CATCH-LOG.md:13).
- Fix: in new rows, give a time, or "before 3:10 PM" with the pack commit.

### A9. Low. Rows are not in time order.
- Rows 13-15 (1:04-1:10 PM) come after row 12 (afternoon, before 3:10 PM). Row 17 (3:25 PM) comes after row 16 (4:40 PM).
- This is fine for an append-only log (rows go in when written).
- Fix: change "The newest row goes at the bottom" (CATCH-LOG.md:11) to "The newest-written row goes at the bottom", so no one "fixes" the order.

## Count for the Weekly Metrics sheet (week of Nov 23)

- 19 rows in all.
- mistake: 4 (rows 1, 3, 8, 11)
- catch: 11 (rows 2, 4, 5, 6, 7, 10, 13, 14, 15, 18, 19)
- near-miss: 3 (rows 9, 16, 17)
- refusal: 1 (row 12)

## Parked question for Matthew

### Q1. Who writes a catch-log row when Prima made the mistake?

**Question.** The rule says "the checker or the Prime, never the model that made the mistake". When Prima (the Prime) made the mistake, who writes the row?

**Why it matters.** Six of 19 rows (3, 8, 11, 13, 14, 15) are about Prima or her executor and were written by Prima. A maker writing its own row can soften it. That is the very thing the rule guards against.

**Options.**
- A (default): Prima may write it, but the row quotes the catcher's own words with a cite, and a second view (Grok-Check or Codex) confirms the row in its next report. This follows the existing design: the checker checks, the record is kept by the Prime.
- B: The catcher writes the row text in its own returns report. Prima only copies it into the log, word for word.
- C: Only Matthew writes rows about Prima.

**What happens if no answer.** Prima keeps writing these rows, as now. Each one is marked "written by the maker (Prima)" so it is easy to spot and check later.
