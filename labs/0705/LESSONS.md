# Lessons from lab 0705 (pass 05.01)

Page 90.50.10.0705. Builder: Claude. 2026-11-23.
Cites are to wf at a823ee28 or prima/build 661732f5 unless a commit is named. Each lesson says what went wrong or what held, why, and what to do next time.

1. **A check that does not push is a check Prima cannot see.**
   - What: my 0703 pass 2 check (log entry 18) stayed in my run folder only. The next `git checkout -- pages` would have erased it, so I saved a copy outside the repos before running it.
   - Why: `wf check` appends and reprints but never pushes (src/cmd.rs:786-793). Only `return --push` pushes a log (src/cmd.rs:533-536, :558-579).
   - Next time: the design makes `check` push its report (SPEC.md section 2). Until it is built, a checker must push the page log by hand, as docs/plan/GROK-BUILDER-QUEUE.md:50 says, or say plainly that it did not.

2. **"Does not continue" means two different things.**
   - What: intake refused 0702 on 2026-11-23 with "the returned log does not continue this run folder's log". The returns log was only behind the packs log, not diverged: entries 1-20 matched, and packs added 21-24.
   - Why: intake checks only whether the remote log starts with the local one (src/cmd.rs:629-631), and gives the same refusal for "behind" and "diverged".
   - Next time: compare the two logs before treating a refusal as a fault. The design asks intake to say "up to date" for a prefix (SPEC.md section 2), and has a worker sync from packs before it appends (SPEC.md section 2, step 2).

3. **Read the code path before designing over it.**
   - What held: tracing where wf already pushes (`merge_into_shared`, `push_log`, src/cmd.rs:545-579) showed the report can ride the existing return push, with no new transport.
   - It also showed the lock is held through the push (src/lib.rs:154; src/cmd.rs:533-536), which is how a killed push can leave a dead lock.
   - Next time: for any "wf should also do X" design, list the functions that already do something like X, with their lines, before proposing a new command.

4. **A new module still needs the declaring file.**
   - What: the obvious split, "put the report system in a new `src/report.rs` so it touches no held file", does not compile without `mod report;` in `src/lib.rs` (src/lib.rs:5-13), which 0408 holds.
   - Why: in Rust, a module is part of the crate only once its parent declares it.
   - Next time: when a grant says "a new module is allowed", check which existing file must name it, and put that file in the same grant (BUILD-PAGES.md section 2, page 0422).

5. **The stopgap's timestamp names can collide; log numbers cannot.**
   - What: the interim report path uses a local `YYYYMMDD-HHMM` stamp (docs/plan/REPORTS.md:17, :22). Two reports from one worker in the same minute get the same name, and machines' clocks differ.
   - Why: the page log already gives every entry a unique, ordered number (src/page.rs:192-199).
   - Next time: name per-page artefacts by log entry number, and use time only where there is no page (SPEC.md section 3).

6. **Stopping on a failed step works when the failure is real, and costs a round trip when it is not.**
   - What: the 0702.05.03 prompt listed the expected intake refusals as 0001, 0403 and 0404, and the run also refused 0702.
   - I checked the two logs, found 0702 only behind (lesson 2), and went on, recording why (commit 6c01d008, `.workshop/returns/90.50.10.0702.05.03.md`, noticed (3)).
   - In this pass the refusals were 0001 and 0403 only, the known pair.
   - Next time: when a refusal is not on the expected list, show the evidence that it is harmless in the same message, so the call is checkable. If the evidence is not clear, stop.

## Added in pass 05.02 (t530u, t531u, t533u)

7. **Unit of work: one work order with passes, not one page per file group.**
   - What: pass 05.01 split the build into five pages, 0422-0426, one per file group (BUILD-PAGES.md section 1 at d7c505ba).
   - Matthew ruled that the report system is one work order: "N4 is our dev band so the work for building the report system goes that is a work order page." (docs/review/DIRECTOR-WORDS-t530.md:45).
   - Why I split it: I used the page as the unit that carries a grant. In wf, a pass carries its own may-touch inside the page grant (kit docs/DESIGN.md:54-55). Pages were never needed for disjoint grants.
   - Next time: start from "one goal, one page". Give each step a pass with its own may-touch. Propose a second page only when two parts must run at the same time with two workers. t533u allows only one worker per page (docs/review/DIRECTOR-WORDS-t533.md:5), so parallel work is the only reason for a second page.

8. **Records that belong to no work page still belong to a page.**
   - What: pass 05.01 left setup reports with no chain, as a file only, because a setup "has no page" (DESIGN.md:130-131 at d7c505ba). Grok-Check flagged that the default landed nowhere (0705 face 05, signoff note at entry 10).
   - Matthew's answer gives every worker a page in band N6, titled with its name (docs/review/DIRECTOR-WORDS-t530.md:11-19; docs/review/PENDING-RULES.md:13-16).
   - Why I missed it: I treated "page" as "work item" only. The address system already gives other kinds of things their own bands: labs are 0700-0799 (seqAddr.md:351@8e96151d), and worker pages are now 0600-0699.
   - Next time: when something has "no page", ask which band it belongs in before proposing an unchained record. An unchained record is a gap in lineage (Axioms.md:23@8e96151d).

9. **A rule with an opt-out gets skipped.**
   - What: pass 05.01 offered "`wf check` pushes only with `--push`" as an option (DESIGN.md:136-138 at d7c505ba). Matthew chose "Always (Recommended)" (docs/review/DIRECTOR-WORDS-t530.md:25).
   - Why it matters: the one case that went wrong on 2026-11-23 was a check that stayed in one run folder. wf check never pushes today (src/cmd.rs:786-793), and my own 0703 pass 2 check entry 18 never reached GitHub (lesson 1).
   - Next time: when the failure is "someone forgot a step", make the step part of the command, with no flag to skip it. A no-network worker queues the push; it does not skip it (FAILURES.md sections 2-3).

10. **Saying out loud where I differed from the job wording was enough.**
    - What: job w04 in pass 05.01 said "fetch and rebase". FAILURES.md:17-19 kept wf's merge instead, and said why: a rebase drops the commit SHA the return already recorded (src/cmd.rs:542-544, :524).
    - The return's proof line raised the difference. Grok-Check recorded it as a minor that does not fail a Done when, and Prima's signoff note agreed (0705 face 05, signoff entry 10).
    - Next time: when the right design departs from a job's wording, keep the design, give the reason with a cite, and name the difference in the return. Do not quietly follow the wording.
