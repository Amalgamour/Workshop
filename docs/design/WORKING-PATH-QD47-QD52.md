# Working path: QD47, QD48, QD49, QD51, and QD52

**WORKING PATH.** Tester's recommended options, written 2026-11-12
at about 3:25 AM EST (America/Toronto) for Prima to record and for
the Director to review. They are **not rulings** and **not settled
law**. No kernel, core, seated faces, or Designer drafts were
changed.

These are five questions from QUESTIONS-FOR-DIRECTOR.md that still
had no working path. QD50 was not answered (left for Matthew).
QD38, QD41, QD43, QD12, QD61, QD66, and QD67 were not answered or
marked. Q41, Q43, and Q34 were not marked. Kernel Q45 and kernel
Q40 were not given a QD home and were not answered. F8 and F10
were not answered. F.2 was not seated. The D310/R21 shadow case
was not decided.

Checked against R2 (a face may be seated after a trial; this does
not answer an open Director question), R9 (counters run 01-98),
R11 ("This is how we let the compute solve"), R22, R23, R24
(climb 05.01-06; the past is not rewritten), R25 (this path
does not write a 00.counter and does not answer QD66 or QD67),
and the axioms, especially 1, 3, 4, 6, 7, 8, and 9. Also checked
against A1.4, C7, C8.6, C8.7, C8.8, E9, kernel-design.md
(proposed, not law), workflow-loop.md (revision .002) and
workflow-loop.003.md, seqAddr.md, OPEN.md O31, O32, O33, O37,
and O38, CONFLICTS.md K05 and K13, the core, the compute, the
kernel faces, and the books.

None of these five questions has a "Now" line. QD49 also has no
Log line and no D-row.

---

## QD47. Is the computer's fixed start-up (bootstrap) law? Does
the kernel also steer task routing?

This is two questions. They do not depend on each other. Raised
from O31. Log: D91, D129, D250. No "Now" line.

**Best option:** split them, and answer each as follows.

**(a) Making the start-up law needs Matthew.** The start-up is
not a page face, so R2 cannot seat it, and R2 does not let anyone
answer an open Director question. kernel-design.md:111 says the
kernel cannot be the only rule for reading itself, so the
start-up cannot live only in a kernel face either. Until he
rules, keep kernel-design.md proposed (it says it is not
promoted law), and keep following the start-up as built, as
provisional 7 (D91): locate the kernel book, check its version
and address, replay it, require the door, refuse with exit 3,
and write nothing. Two of kernel-design's start-up steps are
not built as written: 7.5 (load the kernel's agreements, then
enable richer operations) and 7.6 (keep a recoverable prior
state when loading fails). BUILD-LOG:54 maps those numbers to
"require the door" and "exit 3", which is what the compute
does. The path names the gap; it does not pretend those two
steps are built (axiom 7). Do not seat.

**(b) For routing, the kernel holds the agreements and the
compute chooses and runs the work.** That is the
"Structural/reasoning kernel" at kernel-design.md:159, and it
is what is built: no kernel code steers routing; the compute
hard-codes the task life and, with R11, how a prompt is
solved. R11 says "This is how we let the compute solve."
kernel-design.md:35 and :166 say the kernel defines agreements
and should not become the intelligence or the authority.
Axiom 3: each leads the part it does best. Axiom 1: compute
enforces authority. The compromise at kernel-design.md:162
(store declarative routing rules in kernel faces, keep the
coordinator outside) stays an offer; the file itself calls it
"a proposal to test."

**Offers, not the path:** if Matthew wants the start-up as law,
make it a short Director ruling, kept small
(kernel-design.md:122). For routing, try the :162 compromise
later, once those faces are seated and a reader exists.

**Findings, not implemented:** D250 and D92 are marked
"settled-by-spec" from kernel-design.md, which calls itself not
law (both rows already note this). At boot, the first
00.00.00.book found across folders wins, with only a warning
(BUILD-LOG:56). The compute does not load the axioms file
(00.00.axioms.jsonl) at boot. The "require the door" step is
a build choice mapped to 7.5; it is not in kernel-design 7's
words.

This does not promote kernel-design.md as a whole. It does not
decide the "first folder wins" shadow rule (not the D310/R21
face-shadow case). It does not define a recoverable prior
state, and it does not write a 00.counter.

Working path, not a ruling.

---

## QD48. Do the reserved numbers 01-09 apply to tasks and
dictionary sections?

Raised from O32 and CONFLICTS K05. Log: D15. No "Now" line. The
question says "tasks"; O32 says "counters". This path answers
for counters (face 05 tasks, face 06 notes, and dictionary
sections on 03). If it answered only for tasks, notes would be
left out.

**Best option:** take A and B together; they are not
alternatives. The reserved 01-09 range is for axes (desk,
shelf, book, and pages 0001-0099), not for counters
(seqAddr.md:24; A1.4 at decisions.md:36: "the reserved 01-09
range does not apply to them. The first counter is 01"). So
tasks, notes, and dictionary sections all count from 01.
R9: counters run 01-98. R24 uses "05.01-06" for the first
stretch of work. Separately, the dictionary page's own layout
sets 03.01-03.09 aside for words that start with digits or
symbols (decisions.md:451, :481). That is a rule of the
dictionary on page 0012, not the axis reservation.
decisions.md:481 itself says A1.4 still stands. D15 stands for
axes.

Why: the two source sentences already agree. Sixteen seated
05.01 and 05.02 counters (pages 0051-0057 and the axioms page,
under R2 and R22) already use 01 and 02, and cannot be
renumbered (axiom 6). Applying 01-09 to counters would break
those seats and R24's own shape.

**Offers, not the path:** plainer words for the dictionary row,
for example "kept for words starting with digits or symbols",
so "reserved" is not read as the axis rule. Wording only;
Matthew's if he wants it.

**Findings, not implemented:** the core labels 01-09 as
reserved on container axes (`axis_role`), but validate does
not refuse a write on those values. The dictionary's 03.01-03.09
job cannot be done with today's card-key rule: a word that
starts with a digit cannot be a card key (it must start with a
letter, C2), and a leading symbol is dropped (`@home` becomes
`home`). The core also does not check which section a word
sits in. These are not answered by QD48.

This does not reopen QD58 (a split of 05 into tasks and
tickets) or what face 05 means, or QD44/D412 (a return lives
on the same counter). It does not decide the 03.00 door
tension with R9, or 03.99.

Working path, not a ruling.

---

## QD49. Page 0117 (pack-lint) sits in a band the workflow
doesn't use. Keep it there?

Raised from O33 and CONFLICTS K13. No "Now" line, no Log line,
and no D-row.

**Best option:** neither keep nor move, because there is no
page 0117 in Workshop. It is not in the kernel, and it is not
in any book. "0117.pack-lint" names the predecessor page in
the old system. workflow-loop.md (revision .002):211 already
says, in the past tense, "This is what 0117.pack-lint was."
The pack-lint templates now live where .002 and .003 put them:
kernel card types under C8.9 (today the draft card `pack-lint`
on 0057.02), still 7 until seated through the kernel's
drafting path (workflow-loop.003.md:232).

Keep the sentence as history (axiom 6: do not rewrite the
past). Mark the link 7.8, because it cannot be opened in this
repo (axiom 8: a connection that cannot be opened is 7.8; do
not repair it from memory). Create no 0117 page. Moving that
past identity would rewrite the line (axiom 6). K13 is not a
band clash, because no page sits in band 1.

.003 says 0100-0299 is "unassigned by this workflow" and
"follows governing band definitions" (workflow-loop.003.md:43).
Only .002 says "N1NN | not in use".

Only Matthew can supply the old page, so that axiom 9's "open
its predecessor" can actually be done. I found no 0117 page
content in this repo.

**Offers, not the path:** if a pack-lint page is ever wanted in
a workflow, it is a new page in a band the workflow names,
with a written link back to the predecessor. That touches F.2
and is an offer only; F.2 is not seated.

**Findings, not implemented:** the kernel draft 0057.02 tells
readers to "Consult the predecessor 0117.pack-lint", which no
reader of this repo can open, and it is not marked 7.8.
`build.mjs --check` does not flag it. QD49 has no Log line and
no D-row.

This does not choose a band for a future pack-lint page. It
does not seat F.2. It does not answer the other half of O13,
QD12 (pointers), or reopen QD40/D407.

Working path, not a ruling.

---

## QD51. What fields does a note carry?

Raised from O37. Log: D39 (D128 also routes note fields here,
and is not in the Log line). No "Now" line. This is about
face 06 notes, not the seated face 05 "What We Learned" cards
that use `type: note`.

**Best option:** use the E9 fields `by`, `date`, `refs`, `why`,
and `unresolved`, and drop `state`. A note is a counter, and
its tail already holds its state (seqAddr.md:140: "Workflow
state lives only on counters"; tails at seqAddr.md:128). A
`state` line in the body would be a second copy that can
disagree (axiom 2: do not copy; axiom 8: two that are
connected must agree).

- `by`: who wrote it, including which model (v2:85; D39
  "recording the model"). It must agree with the log entry's
  writer.
- `date`: when (v2:87). It must agree with the entry's time
  when that time is the real write time. Seeded books today
  share one fixed stamp, so that stamp cannot serve as a
  note's date.
- `refs`: the addresses it refers to (v2:86; D39 "what it
  refers to"). Written connections (axiom 8); a ref that
  cannot be opened is 7.8.
- `why`: why the note exists (v2:87; D39; axiom 4). Required.
- `unresolved`: the findings left open (kernel-design.md:102
  "unresolved findings"); may be empty, with a why ("none").

The four of `by`, `date`, `refs`, and `why` come from the
Director's v2:83-87 (the "when" and "why" share one line at
v2:87, "When it was used why the note exists"; this split is
my reading) and from D39. `unresolved` has a spec source.
E9 is proposed, not applied, and its source file
`claude/kernel-notes.md` is not in the repo (7.8).

Existing kernel 06.01 notes say they carry no fields, because
C7 is open. Any new field rule should be a finding, not a
hard refusal, on what is already written, until it is
updated as a new step (axiom 6, R24). Seated `type: note`
cards on face 05 are not rewritten. Do not write notes into
seated faces. The 0052.01 w04 wording is left to the builder.

**Offers, not the path:** E9 as written, if Matthew wants
`state` as a reader's flag separate from the tail. Or only
the Director's four (`by`, `date`, `refs`, `why`). A further
offer: `by` also names the session, since R20 makes a fresh
session of the same model a different view.

**Findings, not implemented:** the core's `note` type has no
field list, so any fields are accepted. All eight seated
05.01 "What We Learned" cards are `type: note` with fields
`by`, `made`, `sources`, `design`, not E9's names. One 06.01
note (and others) holds several sessions, against "one
counter per session" (seqAddr.md:155). O37 cites
decisions.md:409, which holds only "Status: open, to
discuss"; the fields are at :611.

This does not decide whether 06 notes can be seated (Q35,
not reopened). It does not mark kernel Q44 (whether "what we
learned" belongs on 05 or 06). It does not say how a note is
closed.

Working path, not a ruling.

---

## QD52. Does a failure count only against a word meaning
(brand) that was guessed?

Raised from O38. Log: D73. No "Now" line. Every source says
"assumed", not "guessed": decisions.md:493, brands.md:96,
seqAddr.md:305, OPEN.md O38, D73, and kernel 0055.01. Only
the QUESTIONS title says "guessed". This path uses "assumed".
An assumed brand is stated back (C8.8: "ham, taken as
ham.001, the sandwich"), so it is not a silent guess.
format.md:131 says anything the compute cannot resolve "is
never guessed" (that line is about addresses; the path still
avoids "guessed" so the pieces agree).

**Best option:** yes, as the spec proposes, made exact. Every
resolution and its outcome is still recorded (C8.7; axiom 6:
nothing is dropped). A failure is counted only against a
brand that was assumed: C8.8 step 2 (the brand last used in
this session) or step 3 (the dictionary entry's default),
and only after that assumption is stated back. A failure
after a clear meter match (step 1) is recorded but not
charged to that brand, because the cause is not known
(axiom 7: never invent; do not invent blame). If the same
failure repeats, the compute pushes the model to ask the
person (decisions.md:493, :503; R11: "ask the person what
they are saying, probing them for more detail"). The
person's answer is what may change a meaning (axiom 1).
Step 4 (no brand) has nothing to charge; a failure there is
a sign a meaning is missing.

The repeated-failure question to the person is required, not
optional: if matched failures were never charged and never
raised, a wrong clear match could never be corrected by
failures alone.

**Offers, not the path:** count every failure against the
brand used, matched or assumed. Or record every failure but
charge none, and only ask the person on a repeat. Or charge
the step that chose the brand (the default, or the session
rule) and leave the meaning card untouched.

**Findings, not implemented:** "count against" has no defined
effect on meters (meters are co-occurrence percentages at
decisions.md:438, not success rates). How many failures make
"repeated", and how a failure is detected, stay 7. Nothing
for meters, sessions, or failure counting is built today
(BUILD-LOG:60). "The probe in C8.8" (decisions.md:493) names
a step C8.8 does not label; the nearest text is :503.
0055.05.02 w04 bundles O38 (this question) and O39 (QD53);
a path for QD52 alone leaves that card half-blocked.

This does not answer QD53 (where a new brand card goes). It
does not set what "count against" changes on the card.

Working path, not a ruling.
