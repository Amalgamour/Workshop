# Lessons from lab 0702 (so far)

Page 90.50.10.0702. Builder: Claude. Written in pass 05.02, 2026-11-23, because Matthew asked for it (t506u, as page 0702 face 06 entry 12 records it). It feeds docs/lessons/ later. This pass does not write there (05.02/PACK.md, overview).

How to read the cites:
- `lab@56f89178:N` is line N of labs/0702/LAB-0702-SEQ-GRAMMAR.md in pass 05.01 (commit 56f89178).
- Spec and code cites are at prima/build 8e96151d.

Each lesson says what went wrong, why it went wrong, and what to do next time.

1. **I paraphrased a rule more narrowly than its source.**
   - What: I wrote "An entry number appears once in the file" (lab@56f89178:176).
   - Why: I read seqpage.md:135 alone. I did not read it together with :199-201 (one history line per booked block) or with the lines that refer to a number (`source :=`, `cites:`).
   - Next time: before stating a rule, search the examples for every place the token appears. Then state the rule so it fits all of them.

2. **I stated a negative without reading the code that enforces it.**
   - What: I wrote "The file never checks body text" (lab@56f89178:183).
   - Why: I read seqpage.md:169 ("cannot be mistaken for structure") as "not checked". seqpage.md:186 and parse.rs:366-370 check a block's `cards :=` against its body.
   - Next time: a "never" or "not checked" claim needs a search of the code, and the claim must name where I searched.

3. **I listed settled questions as open because I read the spec but not the rulings.**
   - What: I listed conflicts K2, K4, K5, K7 and K9 as open (lab@56f89178:294-296 and the K rows below them).
   - Why: R26, R9, R10, R28 and R35 had already settled them (DIRECTOR-RULINGS.md:103-106, :37-41, :113-115, :179-180). DIRECTOR-RULINGS.md was not on the 05.01 source list, and I did not open it, though the specs cite rulings by name (for example seqpage.md:4).
   - Next time: when a source names a ruling ("R9", "updated by"), open the ruling. If it is outside the source list, end the job `need` and say so, instead of reporting a conflict the ruling may already settle.

4. **I left questions open that the code already answers.**
   - What: Q5 and Q6 were open in pass 05.01 (lab@56f89178:341, :347).
   - Why: state.rs:607-631 settles how a `copy` is addressed, and derive.rs:119-145 settles where `why-draft :=` comes from. I read only specs and did not open the code (lab@56f89178:398).
   - Next time: where a crate implements the spec, read the function that does the job before calling a point open.

5. **I described values as "shown only by example" and then wrote one wrong.**
   - What: I wrote that derived values were shown only by example, and gave `source := book BB @n @m` (lab@56f89178:171).
   - Why: derive.rs:168-170, :216, :230 and :255 print the exact form, always with the full book address. I did not look.
   - Next time: take a value grammar from the code that prints the value, not from my reading of one example.

6. **My own check of the pack commands did not match how wf runs them.**
   - What: my 05.01 return said all heading greps passed. That was true when I ran them by hand.
   - Why: on Windows, wf splits a quoted pattern that contains spaces. The same form, `git grep -q -F "## 3. Results"`, failed in the 0703 dry-run with "ambiguous argument '3.'" (pages/90.50.10.0703/05.01/PACK.md, checks line). The 05.02 pack now uses `[[:space:]]` patterns (pages/90.50.10.0702/05.02/PACK.md:25).
   - Next time: prove the checks the way the checker will run them. If a pack's check has a space inside a quoted pattern, stop and raise it, as the 05.02 stop-if says (pages/90.50.10.0702/05.02/PROMPT.md:40).

7. **I chained a failing step to the next one.**
   - What: in the 0703 cross-check, I ran `wf.exe intake` and `wf.exe check --dry-run` in one command. The check ran even though intake exited 1.
   - Why: I joined them with `;` for speed. The builder rules say to stop when a step fails (pages/90.50.10.0702/05.02/BUILDER-PROMPT.md:2-3).
   - Next time: run each step that can fail on its own, read its exit code, and only then go on.

8. **Partial reads and "covered" verdicts were reported honestly. Keep doing that.**
   - What: pass 05.01 listed the partly read files and their line ranges, and said its verdicts were readings, not tool output (lab@56f89178 section 0 and :398).
   - Why it mattered: that let Codex aim the cross-check at what was really unverified.
   - Next time: keep stating read scope and evidence type. Also run `seqpage check` on the examples whenever a pack allows running code.
