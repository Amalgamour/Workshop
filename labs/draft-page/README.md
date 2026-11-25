# Lab: the draft-page kernel

Builder: Claude (Matthew's PC, D:\Git\claude). 2026-11-25.
Brief: docs/plan/WORK-PAGE-2026-11-25.md, Part B, on prima/build at dcdab638 (lines 189-192 and 232-243).
Request: t566u, as named on that page (line 189).

Status: `9`. This is a design that has not faced its trial yet (docs/AXIOMS.md:31).
Every rule below is a **Claude proposal**, unless it is cited as an existing rule or as code.
Open choices are in QUESTIONS.md. They are not decided here.

How cites read:
- `file:line` with no commit means the returns head, **d4a9785f**.
- `@dcdab638` means prima/build at dcdab638.

---

## 1. The problem, in plain words

- The kernel is the part of wf that every page uses: the shared helpers, the log, the page lock and the router (labs/0426-plan/README.md:17).
- Page 0426 will split the kernel into smaller files (labs/0426-plan/README.md:41-65).
- That split touches `src/cmd.rs`, `src/lib.rs` and `src/page.rs` (labs/0426-plan/README.md:78).
- Almost every other page needs those same files (labs/0426-plan/README.md:26).
- So while the split is being made, everyone else waits.
- That is the jam this week had (WORK-PAGE-2026-11-25.md:190-192 @dcdab638).
- The goal: the live kernel keeps working while its replacement is drafted (WORK-PAGE-2026-11-25.md:234 @dcdab638).

---

## 2. Two things are called "live" today

This is the key fact the design rests on.

**Live tool.** This is the wf binary each worker runs.
- It must be a pinned build, kept apart from where builders build (AGENTS.md:22-26).
- Today the pin is a823 (WORK-PAGE-2026-11-25.md:61 @dcdab638).

**Live source.** This is the code at the head of returns.
- It already has code the pinned tool does not have.
- Example: `withdraw` is at src/cmd.rs:460 on returns. The pinned a823 tool has no `withdraw` (WORK-PAGE-2026-11-25.md:61 @dcdab638).
- Example: the 0423 lockout is at src/cmd.rs:575. It closed passed at entry 22 of the 0423 log (.workshop/logs/90.50.10.0423/log.jsonl). But the a823 tool does not enforce it.

So "closed" and "live" are not the same thing.
- A change is closed when its pass closes.
- A change is live only when the pin moves to a build that has it.
- Nothing records that second step today. That is a gap (`7`). See QUESTIONS.md Q2.

The design uses both meanings:
- The **live kernel** is the pinned tool, plus the kernel files at the returns head.
- A **draft kernel** is a replacement that is neither of those yet.

---

## 3. The idea in five rules

1. **The live kernel stays the authority.**
   - "A draft, a copy, or a memory does not outrank it" (docs/AXIOMS.md:15).
   - Nobody runs, pins or builds from a draft as if it were live.
2. **The draft is written beside the live kernel, never on top of it.**
   - The draft's code goes to its own branch, not to returns.
   - wf can already do this today. A pack takes `--branch` (src/cmd.rs:389-391), and a return merges only into the pack's branch (src/cmd.rs:680-681).
3. **The draft is one work-order page, with one worker at a time.**
   - It is the same page shape as any other work (docs/DESIGN.md:9-10).
   - It uses the same lock rules (src/page.rs:280-288, :382-386).
4. **The switch is its own checked pass, approved by authority.**
   - Promotion is hard and exploration is cheap (docs/AXIOMS.md:31).
   - The switch catches the draft up to the live head, is checked by another view, and is then merged.
5. **Nothing published is rewritten.**
   - The draft only gains commits. The switch is a merge. Old commits stay reachable.
   - The past is not rewritten; add the new step after it (docs/AXIOMS.md:25).

This is the same shape that faces already have, one scale up (axiom 2, docs/AXIOMS.md:17):
- A face has `FF.draft`, its unseated draft (docs/spec/seqAddr.md:206 @dcdab638).
- A draft is copied, noted, merged, then promoted after review (docs/spec/drafting.md:24-31 @dcdab638).
- Here, the "face" is the kernel's code, and "promote" is the switch.

---

## 4. How the draft is named and found

**The page.**
- The draft lives on the work-order page that replaces the kernel.
- For the split, that page is 90.50.10.0426, titled split-commands (labs/0426-plan/README.md:1).
- The page is live as a page. Only its product, the new kernel, is a draft.
- A page that is all drafts would carry `state: draft` and a `why-draft:` line (docs/spec/face00.md:103, :107-111 @dcdab638). This design does not need a whole draft page. QUESTIONS.md Q1 asks whether it should have one.

**The branch.**
- Proposed name: `draft/<page>`. For 0426 that is `draft/90.50.10.0426`.
- It starts at the live head that the draft pass is packed from.
- The pack records it. The pack entry stores `branch` and `start` (src/cmd.rs:389-391; the pack data in the same function).

**How anyone finds it.**
1. Face 08 of the draft page carries one line: `draft: branch draft/<page>, from <live commit>, replaces <files>`.
   - Face 08 is where links to exact files and commits go (docs/DESIGN.md:29).
2. `wf status <page>` shows the draft pass and its tail, like any pass.
3. The branch name starts with `draft/`. A plain `git branch -r` lists every draft.

**What a draft is not.**
- It is not a second copy of the kernel files on returns.
- It is not a hidden local folder. Dirty local files are not proof (docs/review/PENDING-RULES.md:70 @dcdab638, t547u rule 4).

---

## 5. Who may write the draft

**One worker per page** (t533u, docs/review/PENDING-RULES.md:22-26 @dcdab638).
- Only the builder who claims the draft pass writes the draft code. The first claim wins (docs/DESIGN.md:57).
- That builder holds the page's lockout on face 05 for the whole session (src/page.rs:382-386).
- Any other worker is refused while it holds (src/page.rs:284-285).
- The Prime writes faces 01, 04, 06 and 08 of the draft page, under its own lockout (src/page.rs:369-381).
- The checker is never the builder (docs/DESIGN.md:44-45).

**The lock is per page, not per file.**
- The lockout names one face of one page (src/page.rs:38-46).
- It does not stop a worker on another page from editing the same file.
- wf checks may-touch overlap only between passes of the same page (src/cmd.rs:344, refuse_overlap loops over `p.passes` only).
- So keeping different pages off the same files is a planning rule today (t569u, WORK-PAGE-2026-11-25.md:31 @dcdab638). The lead keeps it. wf does not.

**Why the draft branch frees the lanes.**
- The draft's commits land only on `draft/<page>` (src/cmd.rs:680-681, :728-736).
- So while it is drafted, it changes no kernel file on returns.
- Other pages can keep working on returns, on their own lanes.
- Proposed rule: a pass packed on a `draft/` branch holds its files only on that branch, until its switch pass.
- This changes how t569u is read. So it is QUESTIONS.md Q4, not a decision.

**Where the draft pass's log goes.**
- `return --push` pushes the page log to the pack's branch (src/cmd.rs:716-718, :773-797).
- So a draft pass's log lands on `draft/<page>`, not on returns.
- Intake can read it: `wf intake --branch draft/<page>` (src/cmd.rs:832).
- But the page then has its log on two branches. QUESTIONS.md Q5 asks how to keep one home.

---

## 6. How the switch from live to draft happens

The switch is a separate pass on the draft page. Call it the **switch pass**.
It is separate because commits added after a check need their own check (axiom 9).

**Step 1: freeze the lanes.**
- List every open pass, on any page, whose may-touch overlaps the draft's may-touch.
- wf cannot list this for you (section 5). The lead lists it, with the command in TEST-PLAN.md, test D11.
- The switch waits until that list is empty.
- No new pass on those files is packed until the switch closes.

**Step 2: catch up to the live head.**
- The live head may have moved while the draft was written.
- For a **move** (like 0426), replay the recipe at the live head. For 0426, that is labs/0426-plan/tools/split_cmd.py (labs/0426-plan/README.md:14).
- For any other change, merge the live head into the draft branch. A merge adds a commit; it rewrites nothing.
- After the catch-up, the live head must be an ancestor of the draft head. That is the proof the draft includes everything live.

**Step 3: prove nothing broke.**
- Run the draft's own proof at the caught-up head.
- For 0426, that proof is tests/page_0426.rs. It refreshes its golden copy at the start commit first, then the move must pass with that golden unchanged (labs/0426-plan/README.md:8-9, :109-116).
- Run every existing test as well.

**Step 4: trial by another view.**
- Grok-Check checks the switch pass, like any pass (docs/DESIGN.md:62-65).

**Step 5: approval.**
- The Prime signs off the switch pass (docs/DESIGN.md:66-70).
- But a switch changes what is live for every page. So this design proposes that the person approves it too (axiom 1, docs/AXIOMS.md:15).
- Who approves is QUESTIONS.md Q3. The default there is "Prime signs off, Matthew approves".

**Step 6: merge and move the pin.**
- Merge `draft/<page>` into returns, as a normal merge, never forced.
- Then the pin moves to a build of that merge.
- That pin move must be recorded somewhere everyone reads (QUESTIONS.md Q2).

**Step 7: unfreeze and repack.**
- A pack whose start is before the switch and whose may-touch overlaps the draft is now stale.
- wf refuses stale pins of faces 04, 06 and 05 (src/cmd.rs:382). It does not check a start commit against a kernel move.
- So the lead lists those packs (TEST-PLAN.md, test D10), and each is withdrawn and packed again at the new head.
- `withdraw` exists in the source (src/cmd.rs:460) but not in the a823 pin (WORK-PAGE-2026-11-25.md:61 @dcdab638). Until the pin moves past 0408, a stale pack can only stay unclaimed.

---

## 7. How history stays append-only

- **Page logs.** Every pass, draft or switch, writes only by wf, as appended entries (docs/DESIGN.md:31-34; src/page.rs:266-277).
- **Pushing logs.** A push is refused unless the published log is a byte prefix of the local log (src/cmd.rs:771-794). So no published entry is lost.
- **The draft branch.** It only gains commits: the builder's commits, the catch-up merge or replay, and the golden refresh.
- **The switch.** It is a merge into returns. The old live head stays an ancestor of the new head. Nothing is forced.
- **The old pin.** Its commit stays in git. The record of the pin move names both the old pin and the new one (QUESTIONS.md Q2).
- **Stale packs.** They are withdrawn, not edited. The withdrawn pass stays in the log (STAGE-PLAN-90.50.10.md:110-115 @dcdab638).
- A change that is not recorded did not happen (docs/AXIOMS.md:25). So every step above leaves a log entry or a commit.

---

## 8. How a failed draft is dropped, with no harm to the live page

A draft fails if its check fails, its catch-up cannot be made clean, or authority says no.

1. The Prime closes the draft pass, or the switch pass, as `failed` (docs/DESIGN.md:66-70).
2. If the pass was packed but never claimed, it is withdrawn instead (src/cmd.rs:460), once the pin has `withdraw`.
3. Nothing was merged into returns. So no kernel file on returns changed.
4. The pin did not move. So no worker's tool changed.
5. The draft branch stays, as a record of what was tried. Whether to keep it or delete it is QUESTIONS.md Q6.
6. Face 08 of the draft page gets one more line: `draft dropped: <reason>, see close entry <N>`.
7. A later try is a new pass, from the live head of that day.

The live page is not touched at any step.
That is the whole point of drafting beside it, not on top of it.

---

## 9. What wf already does, and what is missing

**Already there (no new code needed):**
- A pass can be packed on its own branch (src/cmd.rs:389-391).
- A return merges only into that branch (src/cmd.rs:680-681, :728-736).
- One worker per page, by lockout (src/page.rs:280-288, :382-386).
- Log pushes are prefix-checked and never forced (src/cmd.rs:771-797).
- Intake can read any branch (src/cmd.rs:832).
- Stale face pins are refused at pack (src/cmd.rs:382).
- Time can be fixed for tests with `WF_NOW` (src/log.rs:32-34).

**Missing (`7`), each raised in QUESTIONS.md:**
- No record of which build is live, or of when the pin moved (Q2).
- No check across pages for overlapping files (Q7).
- No check that a pack's start is older than a kernel switch (Q8).
- One page log on two branches, when a pass uses a draft branch (Q5).

None of these block a first try. The lead can do the checks by hand, with the scripts in TEST-PLAN.md.

---

## 10. Worked example: 0426, the kernel split

**What 0426 is.**
- It splits `src/cmd.rs` into `src/cmd/mod.rs` plus one file per command group, and moves the kind rules under `src/page/rules/` (labs/0426-plan/README.md:41-65).
- It is a move only, with no behaviour change (labs/0426-plan/README.md:8-9).
- Its grant is `src/cmd.rs`, `src/cmd/`, `src/lib.rs`, `src/page.rs`, `src/page/` and `tests/page_0426.rs` (labs/0426-plan/README.md:78; page 0426 log entry 1).

**What went wrong this week, without a draft page.**
- 0426.05.01, the proof test, was packed at start bcf0680e (0426 log entry 8).
- Then 0423 landed live in the source and changed how every page loop runs. Every write now needs a lockout (src/page.rs:382-386).
- So the golden copy that 0426.05.01 would record is the old loop, with no lock. The pass is stale before anyone claims it (WORK-PAGE-2026-11-25.md:65 @dcdab638).
- This is exactly the failure this design is for: a draft pinned to an old live head, with no rule for catching up.

**How 0426 runs under this design.**

1. **Proof first, on returns.**
   - Repack the proof test, `tests/page_0426.rs`, at the live head after 0423.05.03 (WORK-PAGE-2026-11-25.md:65 @dcdab638).
   - It touches one free file, so it can stay on returns. It does not need a draft branch.
2. **The move, on the draft branch.**
   - Pack 0426.05.02 with `--branch draft/90.50.10.0426`, from the live head of that day.
   - The builder claims it, holds 0426's face 05 lockout, and refreshes the golden copy first, as its own commit.
   - Then the builder runs the split recipe (labs/0426-plan/tools/split_cmd.py) and fixes what the recipe cannot do.
   - The builder returns to `draft/90.50.10.0426`. Returns is not touched.
3. **Live work goes on, on returns.**
   - For example, 0425 (Codex) or 0423.05.03 (Grok-2) may change `src/cmd.rs` or `tests/` on returns that same day (WORK-PAGE-2026-11-25.md:42 @dcdab638).
   - They are not blocked by 0426, if Q4 is answered "yes".
4. **Grok-Check checks 0426.05.02** at the draft head. The Prime signs off and closes it.
5. **The switch pass, 0426.05.03.**
   - Freeze: list the open passes that overlap 0426's grant. Wait until there are none.
   - Catch up: re-run the split recipe at the new live head, on the draft branch, as new commits. Refresh the golden copy first.
   - Prove: tests/page_0426.rs and every existing test pass.
   - Check: Grok-Check checks it.
   - Approve: the Prime signs off. Matthew approves the switch (Q3 default).
   - Merge `draft/90.50.10.0426` into returns. Move the pin. Record the pin move (Q2).
6. **After the switch.**
   - Repack every stale pack whose start is before the merge and whose files moved. For example, 0422.05.01-05.03 are re-pointed to the new paths (labs/0426-plan/README.md:120-122).
   - The grant on page 0422 still lists the old paths, so Matthew records the new grant first (labs/0426-plan/README.md:122).
7. **If it fails.**
   - Close 0426.05.02 or 05.03 as failed. Returns and the pin are unchanged.
   - Every other page keeps working, as it did the whole time.

**Why a move is the easy case.**
- A move can be replayed from a recipe at any start commit (labs/0426-plan/README.md:14).
- So catch-up is "run it again", not "merge two edits of the same lines".
- A draft that changes logic cannot be replayed. It must merge the live head in, and conflicts are its builder's job, inside the switch pass.

---

## 11. Sources read

- docs/AXIOMS.md and docs/DESIGN.md at the returns head d4a9785f.
- labs/0426-plan/README.md at d4a9785f.
- .workshop/logs/90.50.10.0423/log.jsonl at d4a9785f (entries 1-22).
- docs/plan/WORKER-ROLES.md, docs/design/STAGE-PLAN-90.50.10.md, docs/plan/WORK-PAGE-2026-11-25.md, docs/spec/seqAddr.md, docs/spec/drafting.md, docs/spec/face00.md and docs/review/PENDING-RULES.md on prima/build at dcdab638.
- src/cmd.rs, src/page.rs, src/log.rs and AGENTS.md at d4a9785f, read only.
- docs/plan/WORKER-ROLES.md had nothing on drafts. It is cited only for roles (line 9: Claude does lab and design work).
