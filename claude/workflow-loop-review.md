# Review of workflow-loop.002.md

by: Fable (model)
date: 2026-11-11
reviewed: `workflow-loop.002.md` (root, read only; not edited)
checked against: `seqAddr.md` sections 4, 5.7, 6, 6.1, 7, 7.1; `decisions.md` A1.4, A2.6, A2.7, A6.1, C8.9, D0, E1-E9
state: review notes. Nothing here is applied. Every recommendation is a proposal for the Director.
axioms: 9.4

The loop itself is sound: one counter per pack, the return on the same counter, a reviewer who is not the builder, and a hard stop on runaway passes. It is not ready to go live. Nine points need a decision, plus smaller ones.

## Needs a decision

### 1. The approval of S01-S12 cannot be checked
Line 16 points to `workflow-loop.002-notes.md`, which does not exist in the repository. S01-S12 are defined nowhere else: the only file that names them is the draft itself. By the draft's own S01, an approval is a record with an identifier.

Recommend: record the twelve in `decisions.md` as a section, each with its why.

### 2. The band map reaches into user space
Section 2 applies N3/N4/N5/N7 "in any thousands band" and calls N0NN reserved. A2.7 gives `1000-9998` to users to design, and `1000` is the head of the first user band (first open page `1001`). The draft's own example `1401`/`1501` is in user space.

Recommend: the map holds for `0100-0999` only; a user band adopts it by name.

### 3. S05 changes A2.6 more than it says
A2.6: pages with the same `N` and `NN` in different bands "are one set". The draft: a possible set, real only with face 08 links. The draft also renames the bands (A2.6's example has `05` as build; here N3 is build and N5 is jobs). I agree with the draft's direction (axiom 8: agreement is not connection), but it is a change to a settled decision and should be logged as one, as E9 does for the others.

### 4. Three outcomes have no path to closed
Tails move `open -> return -> review -> closed`. An abandoned claim has no return to review, yet 6.4 closes it `abandoned`. `blocked` and `needs-authority` are unclear in the same way: does the builder return first?

Recommend: compute writes a short return for an abandoned claim, so every close passes through the same steps.

### 5. The halt at pass 6 may never lift
Section 9: the person's answer resets the count only if it "explicitly changes or reauthorizes" the frame. An answer that says "carry on" does not. Pass 5 is unstated. The table header says "passes without the person" while S09 counts per frame.

Recommend: an answer to a halt is a recorded reauthorization of the frame.

### 6. The lead rates its own risk
`risk` selects how hard the work is checked, and the lead writes it on its own pack.

Recommend: compute sets a floor from the targets (face 01, 02, 04, kernel pages); the lead may only raise it.

### 7. "Governing change" is never defined
Mandatory N7 and the limit on delegated promotion both hang on it. Compute cannot judge it by meaning, so it needs a definition by target. "Routine" (S04) is its complement and is undefined for the same reason.

### 8. Compute cannot enforce a grant on repo files
Section 3.1 puts code in the repo. The builder writes it with its own tools, so compute can only compare the diff to the grant afterwards. The draft should say "verifies" for repo paths, and say what happens to a write found outside the grant.

### 9. Independent review rests on open E7
6.3 allows the reviewer to be "the lead" or "a cold model in N7". The lead wrote the pack, so it judges the return against its own framing. Whether a fresh sitting of the same model counts as another view is the open part of E7. The lint row "reviewer distinct from builder" needs an identity compute can compare.

## Stands on unsettled items

- 6.1 says the return on its counter "settles" where a return lives. E9 lists it as proposed, not applied.
- `continues-from` (3, 6.3, 6.4) is a C4 link kind, proposed in E9 only.
- Section 4 calls the approval "written permission". That is open in E8.
- E4's raise rule is missing. A builder who is not the lead raises before moving forward. The claim step could be that raise, if the draft says so.
- The band default lead `3MC` (5.1) is stated but not recorded anywhere as set.

## Smaller

- "Pack" now means two things. Here it is the lead's job list, and the compute's handoff is a "manifest" (S06). `claude/readpath.md` calls the compute-built handoff a pack. This draft matches the `pack` tail better, so `readpath.md` should change. Not yet done.
- The code fence in section 6 swallows the sentence about `closed`.
- Card results (`done`, `blocked`, `need`) and counter outcomes (`blocked`, `needs-authority`) use different words with no mapping.
- The example card's `reason` is a placeholder, and lint only checks that the field exists. `placed:` is used but never defined.
- Section references should read seqAddr 6.1 and 7.1.
- No one is named as moving `return -> review`, and no reviewer claim is recorded.
- N4 face 05 "design questions" would meet the E9 tasks/tickets proposal if that is taken up.

## Unprompted

The draft adds three identifiers (approval ID, N4 revision, frame ID) without saying how they relate. One approval record carrying all three would be simpler to check.

Order: point 1 first. The other eight are easier to decide once S01-S12 are written down.
