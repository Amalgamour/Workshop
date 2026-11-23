# Lessons from lab 0702 (so far)

Page 90.50.10.0702. Builder: Claude. Written in pass 05.02, 2026-11-23, because Matthew asked for it (t506u, as page 0702 face 06 entry 12 records it). Lessons 3, 4, 6 and 7 were tightened in pass 05.03 from Codex's check of pass 05.02 (page 0702 face 05, check entry 18). It feeds docs/lessons/ later. These passes do not write there (05.03/PACK.md, overview).

How to read the cites:
- `lab@56f89178:N` is line N of labs/0702/LAB-0702-SEQ-GRAMMAR.md in pass 05.01 (commit 56f89178).
- Spec and code cites are at prima/build 8e96151d.
- `EVIDENCE:N` is line N of labs/0702/EVIDENCE-0703-p1-session.txt. That file is Claude's own copy of session output, not a wf record.

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
   - The opposite mistake came next (pass 05.02). A ruling can settle a general rule and still leave an exception open. R9 settles "no `FF.00`", but R16 calls the dictionary's 03.00 "a door" and is held 7 with that tension named (DIRECTOR-RULINGS.md:65-66; face00.md:470). Pass 05.02 marked Q2 answered with no word of R16.
   - Next time: when a source names a ruling ("R9", "updated by"), open the ruling. If it is outside the source list, end the job `need` and say so, instead of reporting a conflict the ruling may already settle. Before marking a point answered, search the rulings for any later "held 7" or "TENSION" naming the same thing.

4. **I left questions open that the code already answers.**
   - What: Q5 and Q6 were open in pass 05.01 (lab@56f89178:341, :347).
   - Why: state.rs:607-631 shows how a `copy` is addressed today, and derive.rs:119-145 shows where `why-draft :=` comes from today. I read only specs and did not open the code (lab@56f89178:398).
   - The code answers "what does it do now". It does not always answer "what should it do". derive.rs:121 itself calls the why-draft rule "Provisional (QUESTIONS S7)", and face00.md:113 marks the stamp's `why-draft` name PROPOSED. So Q5 and Q6 are answered as current implementation, while the design decision behind Q6 stays open (lab O10).
   - Next time: where a crate implements the spec, read the function that does the job before calling a point open. Then say which it is: implemented behaviour, or a decided design. Code marked provisional is not a ruling.

5. **I described values as "shown only by example" and then wrote one wrong.**
   - What: I wrote that derived values were shown only by example, and gave `source := book BB @n @m` (lab@56f89178:171).
   - Why: derive.rs:168-170, :216, :230 and :255 print the exact form, always with the full book address. I did not look.
   - Next time: take a value grammar from the code that prints the value, not from my reading of one example.

6. **My own check of the pack commands did not match how wf runs them.**
   - What: my 05.01 return said all heading greps passed. That was true when I ran them by hand.
   - Why: on Windows, wf runs each check command through `cmd /C` (src/git.rs:111 @a823ee28), and `cmd` does not read quotes the way `sh` does. The actual error is in the 0703 pass 1 dry-run transcript. `git grep -q -F "## 3. Results"` failed with "fatal: ambiguous argument '3.'" (EVIDENCE:27-30), while the same command run by hand passed (EVIDENCE:43-44). The pattern text is in pages/90.50.10.0703/05.01/PACK.md, checks line.
   - Removing spaces alone did not fix it. The 05.02 pack used `"^##[[:space:]]0[.]"` (pages/90.50.10.0702/05.02/PACK.md:25), which has no space but still has quotes and a caret. Under `cmd`, `^` is the escape character, so the caret issue stays even when spaces are gone. Under `sh -c`, a bare `##` would start a comment (05.03/PACK.md, overview). The 05.03 pack uses `[#][#][[:space:]]N[.]`: no caret, no quotes, no space. I did not reproduce a caret failure myself; Codex's check of 05.02 says those commands passed on Linux (page 0702 face 05, check entry 18), so how they behave under `cmd` is `7` here.
   - Next time: prove the checks the way the checker will run them, through `wf check --dry-run` on the same OS, not by hand. If a pack's check has a caret, quotes or a space inside a pattern, stop and raise it, as the 05.03 stop-if says (pages/90.50.10.0702/05.03/PROMPT.md, stop-if line).

7. **I chained a failing step to the next one.**
   - What: in the 0703 cross-check, I ran `wf.exe intake` and `wf.exe check --dry-run` in one command. The check ran even though intake exited 1.
   - Evidence: the only record is my own copy of the session output (EVIDENCE:10 the joined command; :20-21 intake refused and exited 1; :22 the check still ran). No wf log, return or other repo file records it. The builder prompt supports the rule (pages/90.50.10.0702/05.02/BUILDER-PROMPT.md:2-3: "Stop and tell Matthew if a step fails"). It does not establish that the incident happened. Codex could not check the incident from the cited material, and that is fair.
   - Why: I joined them with `;` for speed.
   - The same habit hit again when I recorded the 0703 pass 2 check. I filtered wf's output with `Select-Object -First 6`, which ended wf after its log line but before its view reprint. It left a stale `.wf-lock` that only a hand removal, approved by Matthew, could clear. That too is recorded only in my session output, not in any repo file.
   - Next time: run each step that can fail on its own, and read its exit code before going on. Never pipe or filter wf output. When an incident matters for a lesson, save its transcript where it can be cited, at the time it happens.

8. **Partial reads and "covered" verdicts were reported honestly. Keep doing that.**
   - What: pass 05.01 listed the partly read files and their line ranges, and said its verdicts were readings, not tool output (lab@56f89178 section 0 and :398).
   - Why it mattered: that let Codex aim the cross-check at what was really unverified.
   - Next time: keep stating read scope and evidence type. Also run `seqpage check` on the examples whenever a pack allows running code.
