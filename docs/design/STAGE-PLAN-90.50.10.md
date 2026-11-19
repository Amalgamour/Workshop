# Stage plan: WF for daily use (band 90.50.10.04xx)

state: draft v1 for Prima to review with Matthew. Not live. The door's next face 01
version waits for his review; no wf page was touched.
made: 2026-11-19, 1:38 PM EST, by Designer.
address: the plan belongs on the band door 90.50.10.0400 (t422.md:4).
template: docs/research/PM-DESIGN-2026-11-19.md section 10 (:157-184), with t422 answers.
axioms: 1.5.8

## 1. Stage goal, in plain words

- Goal: Matthew can hand Prima work every day, and WF carries it with few hand steps.
- Why: t401u.md:7 "lets get WF into a functional state. It doesn't have to be perfect,
  it can be glitchy, we just need I can give you work." (spaces shortened). This is
  roadmap stage 1, "WF for daily use" (ROADMAP-2026-11-18.md:55, :72).
- Done when: every page below is closed `passed`; the stage review step has run; and
  Matthew has said go, hold or redo (section 7).

Order rule: t402u.md:3 "connecting the minimum pieces required to have a loop be
completed ... then we aim for automating it, then we refine for polish and security
last." So the buckets run: loop, automate, polish, security.

## 2. What Matthew answered (t422), checked against his words

| Point | His words (DIRECTOR-WORDS-t422.md) | Relay check |
|---|---|---|
| Plan lives on the band door | :4 "Yes, the stage plan lives on the band door page" | Same |
| Needs are links on both pages | :6 "Yes, page needs are written as links on both pages" | Same. "Face 08" is not in his answer or the question (:5); it came from Researcher's proposal (PM-DESIGN:194) and wf's face table (kit docs/DESIGN.md:29) |
| Independence test | :7 question: "neither needs the other and they change no shared files"; :8 "Yes, that's the independence test; check shared reads later" | Close. The test words are the question's, which he approved. Relay said "no shared files"; his test is "change no shared files", so shared reads are allowed for now |
| Open pages | :10 "No limit on open pages" | Same. It overrides Researcher's default of 3 (PM-DESIGN:207) |
| Stage end | :12 "Yes, the stage ends with the roadmap's review step plus my go, hold or redo" | Same. The roadmap step is ROADMAP-2026-11-18.md:130 |

Also: t422.md:14 (Prima's plain words) says Researcher's defaults were approved. Q2's
default also said an unwritten need shows "unknown" and is not run in parallel
(PM-DESIGN:195). That part was not in the question he answered (t422.md:5).

## 3. Where the band stands

- 0400: door. Face 01 v2 lists the band by hand (wf-run-gh pages/90.50.10.0400/01.md:5-10).
- 0401, 0402: dropped, kept as history, never reused (DIRECTOR-RULINGS.md:129-130).
- 0403: live, the address guard, packed (pages/90.50.10.0403/05.md:4). It touches
  src/addr.rs, src/cmd.rs, src/lib.rs, tests/wf.rs (05.01/PACK.md:19).
- New pages: 0404 and up, in order, never above 0498 (seqAddr.md:323, :242; A1-A9).

## 4. The pages

Files are what each page is expected to touch, read from the wf source at
origin/returns 60dd7e25. Prime confirms them at pack time (`may touch`). Sizes are in
passes (a pass is 30-50 minutes; PM-DESIGN:79), written best/likely/worst.

### 0404  wf lint: returns state a design review (t416u)   [loop]
- Goal: a return for a pass packed on the new template must carry a line naming the
  design files the builder compared. wf refuses the return without it.
- Why: t416u.md:7 "Must be confirmed before the return is complete. We can't force it but
  we can force it to confirm it did this via our WF" (spaces shortened).
- Done when: a test shows a return with no `design review:` line is refused, naming
  t416u; a return with the line is accepted; a pass packed on the old template (0403)
  is not affected (t381u.md:8: no rule change mid pass).
- Needs: none. Waits for: 0403 to close (shared src/cmd.rs).
- Touches: templates (a new version beside templates/v3/), src/render.rs (it picks the
  template, render.rs:19-27), src/cmd.rs (`ret`, cmd.rs:462), its own test file.
- Size 1/2/3.

### 0405  tests build and run on Windows   [automate]
- Goal: `cargo test` builds on Windows. Unix-only tests are gated, and checks that use
  `true`, `grep` or `test` run there or skip with a reason.
- Why: builders work on Windows (t400u.md:7); today the builder must skip the e2e tests
  (0403 PACK.md:23). Known gap: tests/wf.rs:4 imports `std::os::unix`; wf
  docs/spec/WF-GITHUB-LOOP.md:43 lists the `true`/`grep` checks.
- Done when: `cargo test` passes on the box, and `cargo build --tests` succeeds for the
  Windows target (or a Windows builder's proof line shows it), with each skip named.
- Needs: none. Waits for: 0403 to close (shared tests/wf.rs).
- Touches: tests/wf.rs only.
- Size 2/3/5.

### 0406  needs links on face 08, both ways   [automate]
- Goal: one wf command writes "needs" on both pages' logs; `wf verify` flags a link that
  has no back-link.
- Why: t422.md:6 (links on both pages); seqAddr.md:251 "A one-way link is invalid";
  Axioms.md:27. Until it lands, Prime writes the links by hand on face 08, which wf
  already allows (cmd.rs:220). That is the manual first step (t402u.md:3).
- Done when: tests show the link appears on both pages, a one-way link is reported, and
  a link to a missing page is refused.
- Needs: none. Waits for: 0404 (shared src/cmd.rs, src/render.rs).
- Touches: src/cmd.rs, src/lib.rs, src/page.rs, src/render.rs, its own test file.
- Size 2/3/4.

### 0407  the door prints its own type and contents   [automate]
- Goal: a page ending in 00 shows `type: band` on face 00 and a contents list of the
  band's pages, built by wf from the pages folder, not written by hand.
- Why: the door's registry is hand-written today (0400/01.md:5); face00.md:141 (band
  head is `type: band`), :206 (contents is compute-only); drafting.md:40 (derived
  content is not hand-written).
- Done when: tests show a band door lists each page in its band with its state; a
  dropped page shows as dropped; a non-door page shows no list.
- Needs: 0403 (it reads `page_kind` from the new src/addr.rs). Waits for: 0406 (shared
  src/render.rs).
- Touches: src/render.rs, its own test file.
- Size 1/2/3.

### 0408  withdraw a packed pass nobody has claimed   [automate]
- Goal: Prime can withdraw a pass at `pack` with no claim. It is kept in the log as
  withdrawn, and a claim on it is refused.
- Why: 0401 and 0402 hold packed passes that can still be claimed if published
  (ADDRESS-DRIFT-t413u.md:28). Today the only guard is "never publish".
- Done when: tests show withdraw works at `pack`, is refused at `open` or later, and a
  later claim is refused; the log keeps the pass (Axioms.md:23).
- Needs: none. Waits for: 0406 (shared src/cmd.rs, src/lib.rs, src/page.rs).
- Touches: src/cmd.rs, src/lib.rs, src/page.rs, its own test file.
- Size 1/2/3.

### 0409  retire a page   [automate]
- Goal: Prime can mark a page retired with a reason. It stays on record, leaves the
  door's list of live work, and refuses new drafts.
- Why: DIRECTOR-RULINGS.md:153-154 (a linked page can only be retired). Today halt plus
  a note stands in (ADDRESS-DRIFT-t413u.md:18-19, :28).
- Done when: tests show retire works when no pass is open, is refused otherwise, and the
  page still verifies.
- Needs: 0408 (a page with a packed pass can only retire after the pass is withdrawn;
  halt is refused while a pass is open, cmd.rs:84). Waits for: 0408.
- Touches: src/cmd.rs, src/lib.rs, src/page.rs, its own test file.
- Size 1/2/3.

### 0410  intake checks the packs head   [security, last]
- Goal: `wf intake` takes a returned log only if it continues from the log published
  on the packs branch for that page.
- Why: wf docs/spec/WF-GITHUB-LOOP.md:41 "closes most of Tester's full-rewrite hole.
  t402u moved it later." t402u.md:3: security last.
- Done when: tests show a returned log that rewrites a published entry is refused, and a
  clean continuation is taken.
- Needs: none. Waits for: all pages above (security last, t402u.md:3; shared src/cmd.rs).
- Touches: src/cmd.rs (`intake`, cmd.rs:579), src/git.rs, its own test file.
- Size 2/3/5.

Polish bucket: no page planned. Polish items come from the returns' overflow lines.

Not a page: who wf records as the page starter. It is question Q1 (section 8).

Merged or split from Prima's list: "retire and withdraw" is split into 0408 and 0409
(two jobs; 0409 needs 0408). "wf lint" is kept to one check, the t416u line; a general
lint command is later work.

## 5. Needs links, both ways (write these on face 08 by hand until 0406 lands)

| Page | Needs (written on this page) | Needed by (written on the other page) |
|---|---|---|
| 0403 | none | 0407 |
| 0407 | 0403 (src/addr.rs `page_kind`) | none |
| 0408 | none | 0409 |
| 0409 | 0408 (withdraw before retire) | none |
| 0404, 0405, 0406, 0410 | none | none |
| every page | the door 0400 (band) | 0400 lists it |

## 6. Order and what can run at once

Test (t422.md:7-8): two pages run at once only if neither needs the other and they
change no shared files. Shared reads are allowed for now. No limit on open pages
(t422.md:10). wf checks file overlap only between passes on the same page
(cmd.rs:317-332), so across pages Prime checks it by hand at pack time.

Most pages edit src/cmd.rs or src/lib.rs, so most must wait their turn. Real
parallel work exists only if each new page writes its tests in its own file (Q2).

```mermaid
graph LR
  P0403[0403 address guard - loop, live] --> P0404[0404 design-review line - loop]
  P0403 --> P0405[0405 Windows tests - automate]
  P0404 --> P0406[0406 face 08 links - automate]
  P0403 -. needs .-> P0407[0407 door contents - automate]
  P0406 --> P0407
  P0406 --> P0408[0408 withdraw pass - automate]
  P0408 -. needs .-> P0409[0409 retire page - automate]
  P0407 --> P0410[0410 intake packs head - security]
  P0409 --> P0410
  P0405 --> P0410
```
Solid arrow: waits (shared file or order). Dotted: a written need.

| Wave | Pages | Can run with | Why |
|---|---|---|---|
| 0 | 0403 | nothing new | it holds src/cmd.rs, src/lib.rs, tests/wf.rs |
| 1 | 0404, 0405 | each other | no need between them; files differ (0405 is tests/wf.rs only; 0404 uses its own test file) |
| 2 | 0406 | 0405 | 0405 changes only tests/wf.rs |
| 3 | 0407, 0408 | each other, and 0405 | 0407 is src/render.rs; 0408 is cmd.rs, lib.rs, page.rs |
| 4 | 0409 | 0407, 0405 | needs 0408 |
| 5 | 0410 | nothing | security last |

If Q2 is answered no (tests stay in tests/wf.rs), every page shares tests/wf.rs and the
whole stage runs one page at a time: 0403, 0404, 0405, 0406, 0407, 0408, 0409, 0410.

Size: 10/18/26 passes (best/likely/worst), plus 0403. The roadmap guessed 4-6 for this
stage (ROADMAP-2026-11-18.md:55), before t400u-t402u and t413u-t416u added work.

## 7. How the stage ends

1. Every page closed `passed`, each return checked by someone other than its builder
   (Axioms.md:29; ROADMAP-2026-11-18.md:128).
2. The roadmap's review step (ROADMAP-2026-11-18.md:130): "Each stage ends with a hostile
   pass, then the page halts and Matthew gets a short report." The page that halts is
   the door 0400.
3. Matthew says go, hold or redo (t422.md:12).

## 8. Open questions for Matthew

Q1. Who should wf record as the person who starts a page?
- Proposed: (default) the log names who really ran it, and names Matthew as the one who
  granted it, by a recorded words file. Other option: a build-stage allowance, Prima acts
  as him, marked build-stage.
- Why: asked at t420.md:11; his answer (:12) gave the planning flow, not this. wf
  refuses unless the starter is the person (wf src/cmd.rs:171), so every page shows
  actor `matthew`. Who gets hurt: an observer who cannot tell who acted.
- Axioms: 1 (Axioms.md:13) pass for default, tension for the other; 6 (:23) pass; 8 (:27) pass.

Q2. Should each new page put its tests in its own test file?
- Proposed: (default) yes. One page, one job, one test file, so pages that change
  different code can run at once.
- Why: his test is "change no shared files" (t422.md:7-8). Today every page would touch
  tests/wf.rs, so nothing could run at once. Same shape as "one folder per page and one
  file per face" (DIRECTOR-RULINGS.md:142). Who gets hurt: Matthew, waiting on a queue.
- Axioms: 2 (Axioms.md:15) pass, same shape at each scale; tension, small test helpers may
  be copied between files; 5 (:21) pass, a clear frame per page.

Q3. Which work counts as "novel" for the t416u design review?
- Proposed: (default) all work in Workshop, for now. Every return carries the line.
- Why: t416u.md:7 says "Novel work requires additional reviews"; t415u.md:5 says "Work
  done here is often very novel." No file says how to tell novel from routine. Who gets
  hurt: a builder who skips the review on work that only looked routine.
- Axioms: 7 (Axioms.md:25) pass, no invented test for "novel"; 9 (:29) pass; 1 (:13) pass.

Q4. Is security (0410) last in this stage, or after the whole build?
- Proposed: (default) last in this stage. Each stage keeps the same order: loop,
  automate, polish, security. Other option: move it to roadmap stage 2, "Lock the door".
- Why: t402u.md:3 "We can't secure until it's finished. That is one of the last steps to
  be completed." "It" could mean this stage or the whole build. Who gets hurt: if late,
  the rewrite hole stays open (WF-GITHUB-LOOP.md:41).
- Axioms: 2 (Axioms.md:15) pass for default; 5 (:21) tension, the frame of "finished" is unclear.

Q5. What happens to the roadmap's older stage 1 list?
- Context: ROADMAP-2026-11-18.md:73 lists `wf bench` in Rust, merges at close, halted
  state in status, observer findings in the log, and the reprint error. Three are in
  wf now (halt shows on the board, board.rs:229; `observe --record`, lib.rs HELP;
  merge at `return --push`). `wf bench` is not in the kit.
- Proposed: (default) keep the roadmap as written, and add a note that this plan is the
  newer step for stage 1, with `wf bench` moved to a later stage. Other option: add a
  `wf bench` page here.
- Why: Axioms.md:23, add a step and do not erase; t402u.md:3 puts measuring after the
  loop works. Who gets hurt: Matthew, if the roadmap and the plan say different things.
- Axioms: 6 (Axioms.md:23) pass; 2 (:15) pass; 4 (:19) pass.

## 9. Release check of this plan (RELEASE-CHECK.md @ c0e5b22)

| Item | Source file:line | Seen in this plan | Result |
|---|---|---|---|
| A1-A4 addresses | t413u.md:7, :9; seqAddr.md:320-322 | 90.50.10.0404-0410 | PASS |
| A5, A6 band 0400, door 0400 | seqAddr.md:323; t420.md:4 | section 3-4 | PASS |
| A9 not PP99, 9999 | seqAddr.md:325 | highest page 0410; cap 0498 | PASS |
| H1 page numbers | seqAddr.md:323; DIRECTOR-RULINGS.md:129-130 (0401, 0402 not reused) | next free numbers from 0404, in order | PASS |
| H1 bucket order | t402u.md:3 | loop, automate, polish, security | PASS |
| H1 one page, one job | t249u.md:9 ("one-page work"); t223u.md:8; WORK-BOOK-SPEC.md:79 (draft) | section 4 split | TENSION (no ruling says "one job per page" in those words) |
| H1 sizes in passes | PM-DESIGN:79; t400u plain words :12 (30-50 min a pass) | section 4 | PASS |
| H1 own test file per page | none yet | section 6 | TENSION (asked as Q2) |
| Plan on the door | t422.md:4 | address line | PASS (not yet written there; waits for review) |
| Needs both ways | t422.md:6; seqAddr.md:251 | section 5 | PASS |
| Independence test | t422.md:7-8 | section 6 | PASS |
| No open-page limit | t422.md:10 | section 6 | PASS |
| Stage end | t422.md:12; ROADMAP-2026-11-18.md:130 | section 7 | PASS |
| Packs on the page's own 05 | t420.md:6; seqAddr.md:324 | one 05.NN per pass per page | PASS |
| t416u gate as its own page | t416u.md:7; t381u.md:8 | 0404, not inside 0403 | PASS |
| Files touched | wf source @ 60dd7e25 | section 4 | TENSION (expected, not proven until pack) |
| Quotes from recorded files | t422, t416u, t415u, t401u, t402u, t420 | sections 1-8 | PASS |
| Axioms 1 Authority (Axioms.md:13) | plan is a proposal; Matthew decides | state line | PASS |
| Axioms 7 Missing (:25) | unknowns asked, not filled | section 8 | PASS |
| Axioms 9 Trial (:29) | Designer's own plan, no hostile pass yet | - | TENSION |
| Stage size vs roadmap | ROADMAP-2026-11-18.md:55 (4-6) | 10/18/26 | TENSION (scope grew; Q5) |

Overall verdict: no FAIL. Ready for Prima to review with Matthew. Five tensions stay:
one-job rule only in a draft, own test files (Q2), files expected not proven, no
hostile pass yet, and the stage is bigger than the roadmap guessed.
