# WORKING PATH: recommendations only, not a ruling.
# Tester (Grok Bot) hostile pass on the pack template.

Checked docs/design/PACK-TEMPLATE.md at 7579788 (HEAD, file
unchanged). Mon 16 Nov 2026, 6:58 PM EST. Only Matthew rules.
Cites: T = PACK-TEMPLATE.md at 7579788. C = WORK-BOOK-CONCEPT.md
at 54b737d. RUL = docs/spec/DIRECTOR-RULINGS.md. WL =
docs/spec/workflow-loop.003.md. CHK = my own earlier check,
docs/review/WORK-BOOK-CONCEPT-CHECK.md (093c64a).
Axioms.md (docs/spec): 1 :13, 2 :15, 3 :17, 4 :19, 5 :21, 6 :23,
7 :25, 8 :27, 9 :29. t223u/t226u/t227u = docs/review/DIRECTOR-
WORDS-*.md.

## Verdict: holds, with fixes

Plain words: the split is right. Prima writes the thinking; the
compute writes where, when, who and from which code (T:59). Most
rows match WL 5.1 (WL:103-116) and R37 item 3 (RUL:197). But the
builder has no way to reach the compute, the return drops two
approved parts, and pages are "matched" by number, not by link.

## Top issues

1. No road back. The builder must claim and return through the
   gate itself; Prima may not relay (T:145). But the compute
   listens on 127.0.0.1 only and refuses any other address
   without --allow-remote (crates/compute/src/main.rs:4, :12).
   A model on Matthew's machine cannot reach it, and has no
   writer token. Pack 1 stalls at the claim. Hurt: Matthew, who
   queues a model that can never hand back.
2. Return template drops approved parts. WL:189 (approved S02)
   wants deviations and their why; WL:192 wants questions,
   permission asked, solutions proposed; WL:193 wants notes.
   T:134-143 has none of them. C:264-267 (W5) wants cost
   (time, tries, tokens, dollars); also missing.
3. Matched pages by number (T:72, row 10; T:101). Axiom 8 :27:
   "two pieces that match are not connected by matching".
   R18 needs CC AND title (RUL:71-72). WL:60 (proposed F.2)
   needs written links both ways. Fix: follow face 08 links;
   no link = "not available", never a lookalike (WL:61).
4. Pack 1 has no page to live on. T:171 puts it at
   <page>.05.<NN>. That page's type is locked once set (R36,
   RUL:189-190) and W8 is not ruled (C:198). W8 blocks pack 1.

## Row by row (part 1, T:61-86)

Pass unless listed. Axioms 1 :13, 3 :17, 6 :23 checked on every
row; R37 items 1-10 (RUL:195-204) checked on the whole table.
- Row 3 by: pass. The compute takes it from the token
  (crates/compute/src/store.rs:731-733), not from the caller.
- Row 5 pack hash: tension. Hashed "at draft -> pack" (P4), but
  pack 1 never takes that step (T:168). No hash point for it.
- Row 7 baseline: tension. Branch is fixed text "prima/build"
  (T:69, T:115). Fill it like any other value. See P3.
- Row 10 matched pages: fail, issue 3.
- Row 11 authorized: pass in design. For pack 1 it cannot
  resolve (no approval ids, T:220), and WL:239 makes that hard.
- Rows 11, 18, 20 have two writers, yet T:59 says "each field
  has one owner". Say "Prima writes, compute checks" in T:59.
- Row 22 checks: pass. Row 23 read first: pass (R37 item 7).
- Sheet door label (T:96, T:113): from Tester's own work
  (CHK:126). Not trialed here, needs a different view.
- Missing row: a refusal shape. R37 item 8 (RUL:202) says refuse
  with a handback. T says a bad pack "stays draft" but not what
  the compute hands back. Add: rule, field, why.
- Missing: R37 item 5 (RUL:199): selected, pending, accepted are
  separate states. Board columns (T:193) show outcome only.
- Part 4, AGENTS.md (T:155-162) and SPEC B2 column: from
  Tester's own work (T:24, "Tester's eight AGENTS.md sections").
  Not trialed here, needs a different view. Not graded.
- Filled example (T:171-198):
  - "grant: read-only" and "stop if: any write" (T:189-190)
    clash with editing four code paths. Say "no book writes".
  - C:149 says "three paths", C:145 lists four. Fix C, not T.

## P1. Which order does a return use?

1. Plain: done, created, noticed first, then job items? Or job
   items first?
2. Answer: job items first. Each job says done, created (paths)
   and proof. Then noticed, not done, notes. Then unprompted and
   overflow last.
3. Why: t226u:11 says only that unprompted and overflow go "at
   the end of the return. After the job items." It does not put
   done or created before the jobs. WL:189-193 and C:167-174
   both put jobs first. T's order (T:136-143) splits "what was
   done" from the job it belongs to. Hurt: the reviewer, matching
   a done-line to a job by hand.
4. Options: ask Matthew to pick by showing both orders filled
   for one small job. Or a one-line summary at the top, made by
   the compute from the job results (not typed).
5. Axioms: 2 :15 pass (one order, WL and C agree); 5 :21 pass;
   4 :19 pass; 9 :29 tension (untried).

## P2. Who fills "authorized"?

1. Plain: should Prima write the approval, or only name it?
2. Answer: agree with T:218. Prima names it; the compute checks.
3. Why: axiom 1 :13, authority is granted, never claimed.
4. Options: until approval ids exist (T:220), use the ruling
   address (e.g. "R37 item 3, RUL:197") or Matthew's t-number,
   and let the compute check the text exists in RUL or
   docs/review. Weak, but not a guess. For pack 1 it needs a
   fresh t-number from Matthew, not an old one stretched.
5. Axioms: 1 :13 pass; 6 :23 pass; 7 :25 tension (no ids);
   8 :27 tension (the name points to a file, not a book line).

## P3. Where does the start commit come from?

1. Plain: the compute cannot read GitHub. What does the sheet
   show for the start commit?
2. Answer: Prima's push step sends the SHA it pushed through the
   gate. The compute checks it exists in the local repo
   (git cat-file), then records it on the pack. Else "not
   available" (agree T:224).
3. Why: no new outside network door for the compute (axiom 1
   :13; R33 item 4, RUL:165-166, the Host check). Hurt: the
   reviewer, comparing against the wrong base.
4. Options: (a) pin the start at claim time, not pack time; the
   branch may move between them (WL:220, "regenerated when
   stale"). (b) The builder's return states the commit it really
   started from; a mismatch blocks acceptance (WL:244).
5. Axioms: 6 :23 pass; 7 :25 pass; 1 :13 pass (no new grant);
   8 :27 tension (git and book hold different halves).

## P4. What is hashed, and when?

1. Plain: which fingerprints does the compute keep?
2. Answer: the three in T:230, plus two: the handoff sheet as
   given, and the pack at put time when it skips draft -> pack.
3. Why: a review must bind to what was read (R37 item 4,
   RUL:198). The builder reads the sheet, not the pack. Hurt:
   Matthew, approving work done from a sheet nobody can replay.
4. Options: hash-chain every log line (each line carries the
   hash of the one above). R37 item 1 (RUL:195) log becomes
   tamper-evident, which also weakens forged lines while the
   K8 door is open (C:157). Bigger job; its own pack.
5. Axioms: 6 :23 pass; 9 :29 pass; 7 :25 tension (method open);
   2 :15 pass (a hash is not a copy).

## P5. Where does the sheet shape live?

1. Plain: seat it with the templates, with a code copy for
   pack 1 only?
2. From Tester's own work (CHK:137-138, CHK:155-156). Not
   trialed here, needs a different view. Not graded.
3. One new fact for that view: T:204 says no template is seated
   and WL:232 is still 7. So "ends the day the template is
   seated" (T:236) has no date. Ask for a pack number as the end.

## Bootstrap exception: pack 1 is hand-written

Plain words: pack 1 is written by hand and goes in unchecked.
Whether to allow it at all came from Tester's own work
(CHK:118-122, CHK:158-159). Not trialed here, needs a different
view. Below are only the risks and safer ways, as asked.
Risks:
- t227u:5: "you should hand the jobs to the compute ...
  Otherwises you will [drift]". Hand-writing is exactly that.
- Unchecked: it enters as `pack` with no check step
  (crates/seqaddr-core/src/tail.rs:95-97; WL:171). No one sees
  a missing field before a builder claims it.
- Lineage (axiom 6 :23): an override must link back to who
  authorized it. R7 (RUL:31-32) puts a local override on its
  own page (behavior range 0020-0049) with what, why, need and
  aim. T:168 keeps it only inside the pack. Not R7 form.
- Drift: pack 1 becomes the example every later pack copies
  (axiom 2 :15). If its shape is off, the error spreads.
- authorized cannot resolve (row 11), and no hash point (row 5).
Safer ways:
- A. The computer fills it. A one-off script reads the field
  rows of T part 1 (T:61-86) as its only shape, fills the
  compute rows from real sources (token name, clock, git SHA,
  free counter from the board), and leaves the Prima rows as
  empty slots. Prima fills only those.
- B. Hand-written, then a different view (not Prima, Designer
  or Tester) checks it field by field against WL:238-250 and
  records the check before it is put as `pack`.
Recommend: A then B. A removes hand-typed shape, so the drift
t227u names cannot start. B is the trial axiom 9 :29 asks for,
since nothing in the compute checks it. Record the exception
as an R7 page, linked from the pack. The script is not the
template: it reads T, so there is still one shape.

## Concept and Director words, checked

- t223u:8 (pack into 05.NN, jobs list, returns per job): pass.
- t223u:6 (model pulls files): pass (row 8). t223u:10 (model
  pushes): pass only once the road back exists (issue 1).
- t226u:9 (compute does status): pass. t226u:11: see P1.
- t227u:5: pass for later packs; pack 1 see above.
- C:264-267 (W5 cost): missing from T part 3 (issue 2).
