# WORKING PATH: recommendations only, not a ruling.
# Tester (Grok Bot) hostile pass on the dev, work and lab pages.

Checked docs/design/DEV-WORK-LAB-PAGES.md at 203b903 (HEAD; file
unchanged). Fit checked against PACK-TEMPLATE.md at 7d11343 and
WORK-BOOK-CONCEPT.md at 54b737d (its latest). Mon 16 Nov 2026,
7:52 PM EST. Only Matthew rules.
Cites: D = DEV-WORK-LAB-PAGES.md at 203b903. PT = PACK-TEMPLATE.md
at 7d11343. WC = WORK-BOOK-CONCEPT.md at 54b737d. RUL =
docs/spec/DIRECTOR-RULINGS.md. WL = docs/spec/workflow-loop.003.md.
SA = docs/spec/seqAddr.md. Axioms.md (docs/spec): 1 :13, 2 :15,
3 :17, 5 :21, 6 :23, 7 :25, 8 :27, 9 :29.

## Verdict: holds, with fixes

Plain words: three pages, one number, joined by written links,
is a sound reading of t226u:7. The link rule is right (D:79).
But face 05 means two different things in the rulings, every
return gets a lab trial when the workflow says only risky ones,
and the compute's link-writing would make your approval stale.

## Top issues

1. Face 05 clash. R22 (RUL:88): every page's face 05 holds "the
   work pack to reach that page's MVP", seated (R23-R24,
   RUL:90-97). D:50 puts design questions on dev face 05 (WL:92,
   S12); D:63 puts trials on lab face 05. Two Director words in
   tension. Axiom 1 :13: "halt, and raise it ... Do not choose."
   Neither D nor PT says when the best pack is seated (R23).
2. Lab trial for every return (D:40, D:136). WL:200 says a lab
   (N7) trial is for governing or higher-risk work; routine work
   gets a separate reviewer on the work slot. Hurt: Matthew,
   paying a second model for every small job.
3. Approval goes stale (D3). You approve one dev page version
   (WL:88, S01). D:168 then has the compute write face 08 links
   on that same page. A changed page makes reviews stale (R37
   item 4, RUL:198). Fix: write the links before the approval,
   or keep face 08 outside what the approval covers.

## Matthew's words: flags

(a) Compute issues packs from a fixed template (t227u:5;
    R37 item 3, RUL:197). D:98-101 pass for later packs.
    - D:99 cites "PT:10" from the old PT (7579788, D:17): pack 1
      "hand-written". PT now has it script-filled (PT:189-192).
      Stale cite key; fix D:17.
    - PT's pack 1 plan (PT P8) is from Tester's own work, not
      trialed here. But it adds an R7 override page (PT:192).
      R21 (RUL:82-84): "No overrides for now"; R7 code "not
      exercised". That was Tester's own error in 3078e0f. Raise.
(b) Returns list done, created, noticed; overflow last
    (t226u:11). D:110 pass (order left open).
    - D:130 says "in t226u order". t226u:11 fixes only that
      unprompted and overflow come after the job items. Clash
      with D:110. Say "in the return template order".
    - PT P1 order B is from Tester's own work, not trialed here.
(c) Pages linked by written link, not number (axiom 8 :27;
    R18, RUL:71-72). D:74-79 pass: number and title find, only
    face 08 links both ways connect (WL:93).
    - The rule itself (D2, PT P7) is from Tester's own work
      (PACK-TEMPLATE-CHECK.md issue 3), not trialed here.

## D1. What is the lab page for, and where does a trial sit?

Depends on W9, working path only.
1. Plain: is the lab for trying to break the work, or for showing
   it working? Where does one trial go?
2. Answer: break it, as WL:48 says. But only for governing or
   higher-risk work (WL:200). Routine work stays on the work
   slot's review step. Trials on lab slots, each naming the
   exact return version it tried: agree with D:159.
3. Why: axiom 9 :29 wants a trial before promotion, not two
   reviews of every job. Hurt: Matthew's budget.
4. Options: (a) ask Matthew which "lab" he meant: the old
   "inspect" demo (OWB 00.md:36, D:151) may be what he liked;
   (b) a demo is one kind of trial (D:159), with Matthew as the
   person who runs it; (c) only make the lab page when the
   first trial is needed (see D3).
5. Axioms: 9 :29 pass; 2 :15 pass (return in one place); 8 :27
   pass; 7 :25 tension (no spec says which face holds a trial).
6. Rulings: R22 (RUL:88) tension on face 05 (issue 1).

## D2. When is a page linked?

From Tester's own work (PACK-TEMPLATE-CHECK.md, issue 3; now
PT P7). Not trialed here, needs a different view. Not graded.
One fact for that view: SA:243 still says a set is pages with
the same N and NN, "Titles should match". WL:60 (F.2) amends it
but is not seated (WL:53). The narrowing needs Matthew's yes.

## D3. Who makes the three pages and links, and when?

Depends on W8 (page type locks), working path only.
1. Plain: who creates the work and lab pages and the links?
2. Answer: the compute, in one change, as D:168 says. But
   timing: make the set and its face 08 links when the dev page
   is drafted, before approval. Make the lab page only when a
   trial is needed; until then the link says "not yet made".
3. Why: (a) writing face 08 after approval changes the approved
   page (issue 3); (b) a linked page can never be deleted, only
   retired (R32, RUL:153-154). Empty lab pages stay forever.
   Axiom 7 :25: "A hole nothing requires stays empty".
4. Options: a set record in the band's door page that names all
   three, written once by the compute; or links on face 08 only
   of the work page, back-linked later.
5. Axioms: 1 :13 pass; 3 :17 pass (compute leads bindings);
   8 :27 pass; 6 :23 tension (approval revision); 7 :25 tension
   (cross-book write has no safe one-step form, WL:292).
6. Rulings: R33 item 1 (RUL:159) pass; R37 item 3 (RUL:197)
   pass; R36 (RUL:189-190) blocks until W8 is ruled.

## D4. Is 05NN "jobs" or "build"?

No W-dependency.
1. Plain: SA:243 calls 0523 "build"; WL calls 05NN jobs and
   03NN build. Which stands?
2. Answer: WL's map (agree D:174), fixed in SA by a new step
   through its own drafting path.
3. Why: S05 is a Director direction (WL:6). Hurt: a model that
   reads SA alone puts packs in the build band.
4. Options: ask Matthew to confirm with one line; his R18 words
   name "a workflow from N3-N7" (RUL:71) but not band roles.
   Note WL:6: ".003" review and trial are still due (9).
5. Axioms: 2 :15 tension until SA is fixed; 6 :23 pass; 1 :13
   pass.
6. Rulings: none found against it.

## D5. Must Prima's dev note come before the next pack?

Depends on W13 (check step) and W9, working path only.
1. Plain: should the compute refuse a new pack until Prima has
   written what the last return taught?
2. Answer: yes, but narrowly. Only when an earlier pack on the
   same work page has closed. The compute checks the note links
   that exact return (WL:217). "Nothing learned" is allowed, with
   a why.
3. Why: as written (D:180) pack 1 has no return to note, and
   two packs in parallel would block each other. A forced note
   with no room for "nothing" invites empty filler. Hurt:
   Matthew, reading notes that say nothing.
4. Options: the compute fills the note's frame (links, return
   hash, outcome) and Prima writes one judgment line; or the
   lead pass (WL:214-219) is a slot step, not a refusal.
5. Axioms: 6 :23 pass; 5 :21 pass; 4 :19 pass (why kept);
   9 :29 tension (untried).
6. Rulings: R37 item 7 (RUL:201) pass; R37 item 3 pass.

## Smaller fixes

- D:17 cite key: PT is now 7d11343, not 7579788.
- D:45 cites WL:83-93; the face list is WL:87-93. Minor.
- D:62 cites WL:29 for "trial required". WL:29 says N7 is for
  "required higher-risk trials": it backs issue 2, not a trial
  for every return. Add WL:200.
- Workflow page type (WC W8 option) is from Tester's own work,
  not trialed here. D does not depend on it.
