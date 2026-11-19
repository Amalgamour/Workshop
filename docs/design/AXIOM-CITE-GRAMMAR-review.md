# Axiom Cite Grammar: review of the t383u draft

Reviewer: Designer. Reviews: docs/design/AXIOM-CITE-GRAMMAR-draft-t383u.md (8a93c89).
Status: review for Prima. Not an answer from Matthew. Desk check only: no fresh worker, no cold trial.

v2 (t384u): each G now lists its options. The option that follows the existing settled design is marked (default). Matthew's words, from docs/review/DIRECTOR-WORDS-t384u.md:5: "When you have an answer that is fractally compliance, mark it as the default option.  I can deviant if its required.  But we don't want to drift randomly in our design." Nothing else in v1 was rewritten (axiom 6). Where the default differs from my proposed answer, both are kept.

## Summary (plain words)

1. The draft fits the settled cite rules almost everywhere. All nine axiom names match Axioms.md.
2. Reading left to right works on two-number chains. Lab 02 and lab 03 readers agreed on those.
3. It splits on three numbers. In `5.1.4`, does the last number add to the one before it or to the first?
4. The draft's own `1.7.8` example adds to the one before it. The rule text says "keep the earlier focus". Two careful readers can pick differently.
5. It also splits on `7` after a number. `4.7` reads "the why is missing", but `8.7` reads "the link is there but incomplete".
6. The smallest split is `6.7`. One reader says "the history is missing"; another says "the history is there but has a hole". `6.7` is already used in the repo.
7. With `3MPC` in a chain (`7.3MPC`), readers split too: "no lead is named" or "the model leads on this gap".
8. Small mismatches: the draft calls one number a "piece", but Axioms.md calls a dotted run a "piece". The 9 question asks what was tested, but 9 marks what was not.
9. Six questions for Matthew, G1-G6, each with a proposed answer.
10. Timing: this is design only and touches no code. Prima decides whether to do it now or park it.

## 1. Recorded words check

- Draft line 3 holds: "This is for designer to work on.  our grammar for axioms.  If now isn't the right time.  Park as additional work for later in our dev cycle."
- This matches the relayed brief word for word. The only difference is double spaces between sentences.
- I could only compare the copy against Prima's relay. I did not see Matthew's original message.
- Draft lines 9-82 are marked verbatim (line 5) and contain non-ASCII quotes and dashes. I left them as they are.

## 2. Sources checked

| Source | Found at | Used for |
|---|---|---|
| Axioms.md | docs/spec/Axioms.md:5, :7, :9, :13-29 | names, chain rule, the 7 line, 3 letters |
| decisions.md E1-E4 | docs/spec/decisions.md:533-548 (E1), :550-556 (E2), :558-566 (E3), :568-572 (E4) | settled grammar, lab evidence pointers |
| decisions.md lab pointer | docs/spec/decisions.md:531 says lab evidence is in `claude/labs/notes/` | locating labs |
| Lab 02 record | /workspace/cursor-build-review/claude/labs/notes/02.md:82-102 (commit 0476d75, branch cursor/build) | chain probe, 8.7 split |
| Lab 03 record | /workspace/cursor-build-review/claude/labs/notes/03.md:5, :72, :80, :84-96 (commit b69d9ee) | 7 line passed, Leads needs its cite |
| Lab summary | /workspace/cursor-build-review/claude/labs/notes/summary.md:20-21, :48-51 | order is meaningful |
| 00.00.00.ruled.book | docs/spec/examples/sources/00.00.00.ruled.book:5 (addr 00.00.00.0050.02.draft, the Cite card) and :7 (0050.04.draft, the nine) | same text as decisions.md:560-564 and Axioms.md |
| Kernel cite card | kernel/00.00.axioms/00.00.axioms.02.draft.md (cites decisions.md:560-564) | same rules |
| seqAddr.md | docs/spec/seqAddr.md:172, :293 | a chain is never an address |
| DIRECTOR-RULINGS.md | no cite-grammar entry found (rg "axiom|cite|3MPC|chain") | nothing to compare |
| Repo uses of chains | docs/spec/workflow-loop.003.md:170-177; docs/spec/workflow-loop.002-notes.md:7 | real chains in use |

Not found in this repo:
- The lab records are not in /workspace/workshop-build/repo on any local branch. I checked with `git ls-files`, `git log --all -- 'claude/*'` and by listing every local ref.
- I found them in a separate checkout, /workspace/cursor-build-review, on branch cursor/build.
- The GitHub claude branch is not fetched here, so I could not confirm the copies match it.
- `axioms/06.01.md` (named at decisions.md:531) is not in the repo. The nearest file is kernel/00.00.axioms/00.00.axioms.06.01.draft.md.

## 3. Does "read left to right, keep the earlier focus" hold?

The draft rule is at draft:47: "Read left to right. Each dot brings a new axiom to bear on the reading so far. Keep the earlier focus as the chain grows."
Neither test chain is in the draft or the labs. The labs used 1.7, 4.1.7, 2.5, 5.2, 3CM,7, 2.6.1, 9.5, 9, 1.7.9, 7.4, 6.8, 8.6 and 2.6.

### Test 1: a three-number chain, `5.1.4`

Subject: a pack frame attached to a pass (`axioms: 5.1.4` on the frame card).

- **Reader A** follows how the draft reads `1.7.8` at draft:63, where 8 adds to 7 ("a missing or unresolved connection").
  - Reading: "This is about the frame. Who granted it? And is the why for that grant recorded?"
  - Check: the grant record's why.
- **Reader B** follows draft:47, "keep the earlier focus", and Axioms.md:21 ("know what the work aims at, and why").
  - Reading: "This is about the frame. It must sit under granted authority, and the frame's own why must be recorded."
  - Check: the why on the frame (face 04 or the pack).
- **Split: yes.** The two readers check different records, and a worker can pass one check and fail the other.
- **Cause:** with three or more numbers, the rule does not say which earlier number the later one adds to. With two numbers it can't be unclear.
- **Rule that removes it:** "Each number adds to the one just before it, and the whole chain stays about the first." This matches draft:63 and the kernel note at 02.md:87 ("tertiary qualifies"). The opposite rule ("each adds to the first") would also remove the split. See G1.

### Test 2: a chain with 3MPC, `7.3MPC`

Subject: a return reporting a gap in a pass.

- **Reader A** treats `7` first as "something is missing, of this kind". This is how `7.8` reads at Axioms.md:7 and :25, and at draft:60.
  - Reading: "What is missing is the lead. The order model, person, compute was not set on this work."
  - Action: report a defect, because every piece of work needs a lead (Axioms.md:17).
- **Reader B** keeps the letters attached to 3 as an assignment, as draft:49 says ("It names the lead order"). Lab 03 also found that "the cite carries the assignment" (03.md:80).
  - Reading: "There is a gap here. The model leads on it, then the person, then compute."
  - Action: the model starts on the gap.
- **Split: yes.** One reader stops and reports; the other acts.
- **Cause:** `7.X` means "X is missing", but `3MPC` names a lead and doesn't describe a slot. The grammar allows `7.3` without letters (draft:39), which could carry "no lead named".
- **Rule that removes it:** "Letters on 3 always assign. To say no lead is named, write `7.3` with no letters." See G3.

### Smallest split example: `6.7`

- **Reader A** follows Axioms.md:7 ("the same order rule as every axiom": `8.7` is a connection that is incomplete).
  - Reading: "The history (lineage) exists but has a hole."
- **Reader B** follows Axioms.md:25 ("a chain names what is missing: `4.7` a why") and draft:62 ("Its why is missing").
  - Reading: "The history is missing."
- `6.7` is used today at workflow-loop.003.md:176 (step 7 Close), so this is live, not invented.
- **Cause:** the settled 7 line was trialled on `7.8` and `8.7` only (03.md:86). `4.7` is still read as "missing" (02.md:88). So one shape, a number then 7, has two meanings.
- **Rule that removes it:** "A number then 7 means that thing is not complete. The readback says whether it is absent or partial." This is how draft:60 already treats `7.8`. See G2.

### What still trips a cold reader where the readers agree

- Two-number chains without 7 (2.5, 5.2, 6.8, 8.6, 9.5) were read the same by all lab readers (02.md:91, 03.md:86).
- Long runs are used as lists, not as ordered meaning. For example, workflow-loop.002-notes.md:7 has `axioms: 1.2.4.6.7.8.9`. A cold reader who applies left to right there will build a meaning nobody intended. See G5.

## 4. Conflicts (noted, not resolved)

| # | Draft side | Other side | Note |
|---|---|---|---|
| C1 | draft:42 "The distinct-letter rule is proposed for the draft." | decisions.md:562 "one to three distinct letters ... (Status: settled, :559)"; ruled.book:5 | Already settled. The draft understates it. |
| C2 | draft:38-39 one number is a "piece"; a dotted run is a "chain" | Axioms.md:5 and decisions.md:560: "A dot orders axioms inside one piece"; "A comma splits pieces" | Same word, different size. |
| C3 | draft:62 `4.7` "Its why is missing" | Axioms.md:7 and decisions.md:563 (same order rule: `8.7` incomplete); lab 02 option 2 at 02.md:95 lists `4.7` with `8.7` as "this thing is incomplete" | Agrees with Axioms.md:25. Axioms.md is split with itself (:7 vs :25). |
| C4 | draft:66 "The failed read does not establish that the target is absent"; trial case 3 at draft:74 | Axioms.md:27 "A connection that cannot be opened is missing (`7.8`)" | They fit if case 3's expected cite is `7.8`. But a written pointer could also lead a reader to `8.7`. Fix the expected answer before any trial. See G4. |
| C5 | draft:31 9 asks "What has another view actually tested?" | Axioms.md:29 "`9` marks what has not yet faced its trial"; lab 03 reads `1.7.9` as "untried" (03.md:86) | The question points the opposite way to the mark. |
| C6 | draft:39 allows 1-3 letters | Axioms.md:17 "One or two letters may be named" | That line means letters may be left out; decisions.md:562 says one to three. Wording only. |
| C7 | draft:48 a comma gives two readings of the same subject | decisions.md:572 / 03.md:72 `3CM,7` worked as an assignment plus a gap | No clash. Noted as support. |

- No clash with seqAddr.md: draft:42 matches seqAddr.md:293 and decisions.md:561.
- DIRECTOR-RULINGS.md has no cite-grammar entry.

## 5. Names and numbers

| Draft | Real title (Axioms.md) | Line | Result |
|---|---|---|---|
| `1` Authority | Authority | :13 | match |
| `2` Fractal | Fractal | :15 | match |
| `3` Leads | Leads | :17 | match |
| `4` Why | Why | :19 | match |
| `5` Frame | Frame | :21 | match |
| `6` Lineage | Lineage | :23 | match |
| `7` Missing | Missing | :25 | match |
| `8` Connection | Connection | :27 | match |
| `9` Trial | Trial | :29 | match (question wording in tension, C5) |
| "piece" = one number | Axioms.md calls one number an "axiom" and a dotted run a "piece" | :5 | mismatch (C2) |

- Numbers and order also match decisions.md:535-546. The old names (Dance, Narrow, Record, Hostile) appear only in the "Was" column there.
- **3MPC, as the draft defines it** (draft:39-40, :49): axiom 3 (Leads) with lead letters M = model, P = person, C = compute. It means the model leads, then the person, then compute.
- It maps to one real axiom, 3 Leads (Axioms.md:17). It is not three axioms, and the letters are not axioms. The draft adds that the workflow sets handoffs and the grant sets permissions (draft:49). That fits "A lead is not authority" (Axioms.md:17).

## 6. Questions for Matthew (t189u four-part form)

**G1. In a chain of three or more numbers, which number does each later one add to?**
- Proposed: the one just before it, while the whole chain stays about the first. `5.1.4` = the frame, its grant, and the grant's why.
- Why: the draft's own `1.7.8` reads this way (draft:63). Without a rule, two workers check different records (section 3, test 1).
- Axioms.md checked: :5 "A later axiom refines; it does not replace" pass; :21 Frame pass; :27 `1.7.8` pass.
- Options:
  - (a) Each number adds to the one just before it; the whole chain stays about the first. This is my proposed answer, and it matches draft:63.
  - (b) (default) Each later number adds to the first number, the lens. Cite: lab 02 says "the first number is the lens, and later numbers refine it" (02.md:87; summary.md:48).
  - (c) Each later number adds to the whole reading so far, with no rule on which part (draft:47 as written).
- Default note: no settled rule picks one. decisions.md:560 says only "A later axiom refines; it does not replace". I marked (b) because the lab outcome backs it, but that lab wording is weak: "it" could mean the reading, not the first number. **The default differs from my proposed answer (a).**

**G2. Does a number then 7 mean "that thing is missing" or "that thing is there but incomplete"?**
- Proposed: one meaning for all, "that thing is not complete". The readback then says absent or partial, as draft:60 does.
- Why: `4.7` and `8.7` have the same shape but get two meanings today. `6.7` is already live at workflow-loop.003.md:176. The lab trial covered only `7.8` and `8.7` (03.md:86).
- Axioms.md checked: :7 pass; :25 tension ("a chain names what is missing: `4.7` a why"); :19 pass.
- Options:
  - (a) A number then 7 always means "that thing is not complete". The readback says absent or partial. This is my proposed answer.
  - (b) (default) Same order rule for 7 as every axiom: 7 first = "missing, of this kind" (`7.8`, `7.4`); 7 last = "this thing is there but incomplete" (`8.7`, `4.7`). Cite: decisions.md:563 (settled), Axioms.md:7, lab 02 option 2 (02.md:95), passed in lab 03 (03.md:86, :96).
  - (c) Keep today's mixed reading: `4.7` = the why is missing, but `8.7` = the link is incomplete (Axioms.md:25, draft:62).
- Default note: Axioms.md disagrees with itself (:7 against :25), so no option follows all of the existing design. I marked (b) because the settled decisions.md:563 rule backs it. Under (b), `4.7` means the why is there but incomplete, and a wholly absent why is written `7.4`. That changes draft:62 and goes against Axioms.md:25. **The default differs from my proposed answer (a).**

**G3. In `7.3MPC`, do the letters name who leads on the gap, or say a lead is missing?**
- Proposed: letters always assign a lead. "No lead named" is written `7.3` with no letters.
- Why: Leads only fires when cited (decisions.md:572; 03.md:80). If a reader takes it as a defect report, the hand-off is lost.
- Axioms.md checked: :17 pass; :25 tension (7 first names what is missing); :5 pass (only 3 takes letters).
- Options:
  - (a) (default) Letters on 3 always assign the lead order. "No lead named" is written `7.3` with no letters. This is also my proposed answer. Cite: Axioms.md:17 ("`3MPC` means the model leads"), decisions.md:562 and E4 (decisions.md:572; 03.md:80, "the cite carries the assignment").
  - (b) In `7.3MPC`, 7 first names what is missing, so it means the lead order M, P, C is missing (the 7-first rule at decisions.md:563, Axioms.md:25).
- Default note: tension with the 7-first rule (decisions.md:563). The default is the same as my proposed answer.

**G4. Which cite is expected when a written pointer can't be opened: `7.8` or `8.7`?**
- Proposed: `7.8`, as Axioms.md:27 says. The readback adds "pointer written, target not opened, reason X, not proven absent" (draft:66).
- Why: the draft's trial case 3 (draft:74) needs one expected answer before any trial. Otherwise the reviewer scores a careful worker as wrong.
- Axioms.md checked: :27 pass; :25 pass ("unknown stays unknown"); :7 tension (a written link could read as incomplete).
- Options:
  - (a) (default) `7.8`, with the readback "pointer written, target not opened, reason X, not proven absent" (draft:66). This is also my proposed answer. Cite: Axioms.md:27 "A connection that cannot be opened is missing (`7.8`)", same text in ruled.book:7.
  - (b) `8.7`: the link is written, so it is a connection that is there but incomplete (Axioms.md:7, decisions.md:563).
- Default note: the default is the same as my proposed answer.

**G5. Is a long run like `1.2.4.6.7.8.9` allowed as a plain list?**
- Proposed: no. A list of axioms that all apply is written with commas (`1,2,4`). The dot is kept for ordered meaning.
- Why: workflow-loop.002-notes.md:7 uses a seven-number dot run. A cold reader will build a meaning from it that nobody meant.
- Axioms.md checked: :5 pass (dot orders, comma splits); :15 pass (same shape everywhere).
- Options:
  - (a) (default) No. A list of axioms that all apply uses commas (`1,2,4`), and the dot keeps its ordered meaning. This is also my proposed answer. Cite: Axioms.md:5 and decisions.md:560: "A dot orders axioms inside one piece ... A comma splits pieces."
  - (b) Yes. A long dot run may stand as a plain list, as at workflow-loop.002-notes.md:7.
- Default note: the default is the same as my proposed answer.

**G6. Should the draft's names and the 9 question match Axioms.md wording?**
- Proposed: yes. One number is an "axiom", a dotted run is a "piece", and the whole cite is a "chain" (Axioms.md:5). The 9 question becomes "What has not yet faced a hostile pass from another view?"
- Why: a fresh model given both the grammar card and Axioms.md sees two meanings for "piece", and a 9 question pointing the wrong way (C2, C5).
- Axioms.md checked: :5 pass; :29 tension with the draft's current question.
- Options:
  - (a) (default) Use Axioms.md words (one number = axiom, dotted run = piece, whole cite = chain) and reword the 9 question to "What has not yet faced a hostile pass from another view?" This is also my proposed answer. Cite: Axioms.md:5, decisions.md:560, Axioms.md:29.
  - (b) Keep the draft's words (one number = piece, dotted run = chain) and its 9 question (draft:31, :38-39).
- Default note: the default is the same as my proposed answer.

## 7. Timing (input for Prima, not decided)

- For now:
  - It is desk work: no code, no kernel files, no face writes.
  - G2 and G4 touch the expected answers of the draft's own trial (draft:68-78). Settling them first makes any later cold trial cheaper.
  - `6.7` is already live in workflow-loop.003.md:176.
- For parking:
  - G2, G5 and G6 would lead to changes in rule files (Axioms.md, decisions.md). Only Matthew changes those, and rule files change only once a pass is closed (DIRECTOR-WORDS-t381u.md, t383u entry).
  - The build passes in flight don't depend on cite reading.
- A middle path Prima could weigh: send G1-G4 now as questions only, and park any rule-file change and the cold trial.
