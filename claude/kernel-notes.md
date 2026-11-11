# Kernel notes: what the old kernel answers

by: claude-fable-5-2
date: 2026-11-11
refs: `D:\Git\Librarian\00.00.00.kernel.draft\10-14-2026-00.00.00.kernel.zip` (books `00.00.00.syntax` and `00.00.01.law`); `decisions.md`; `alignment-notes.md`; `axioms/06.01.md`
why: the kernel is the predecessor. Workshop is the fresh design. This page records what the predecessor answers, so the next sitting does not read it again.
axioms: 9

## How to use this page

- Workshop governs. The kernel informs; it does not govern (axiom 9: open the predecessor, read-only).
- Every answer below is a proposal for the Director. None is applied.
- Each answer names the kernel page it came from, as `law NNNN.title` or `syntax NNNN.title`.
- Where I could not find an answer, the item is marked `7`.

## What was read

- The zip holds 621 files: 472 live, 149 in the retire warehouses.
- Read: about 70 live faces, mostly face 01, in both books. The list is at the end.
- Not read: the retire warehouses, most faces 02, 03, 04, 06 and 08, and law pages `0002`-`0003`, `0010`-`0011`, `0014`, `0020`, `0025`, `0027`, `0050`-`0055`, `0106`, `0110`.
- The temp band pages named in `00.order.md` (`0137`-`0160`, including `0142.solo-pass` and `0149.self-attack.test`) are not in the zip.

## Words the kernel uses

| Kernel word | Meaning | Workshop word |
|---|---|---|
| director | the person who approves | person, authority |
| prime | the sitting that packs, reads returns and signs | `7`: no word yet (carried item 3, hats) |
| sleeve | a model sitting; a cold sleeve has only its pack | cold model |
| sitting | one session of one model | session |
| clerk | the part that opens faces for a model. "There is no clerk. The model is doing that work until a local app can open the face." | **the compute** |
| seat | the active face, `FF` | seated face |
| door | a band head, or a container's `00.md` | band head, identity page |
| furniture | files beside the book door: `00.md`, `00.axioms`, `00.retire.09` | `7`: no equivalent |
| colab | a job handed to a cold model and read back | lab; pack and return |
| factfind | the numbered holes a return did not close | "need" in a return |

The clerk row matters most. The kernel was written for a model doing compute's job by hand. Every "do not" in the kernel that guards a file move is a rule the Workshop compute can enforce.

---

## 1. The read side: how a prompt becomes a pack

Open question: nothing in Workshop says how a prompt becomes a pack.

The kernel has the steps, spread over six pages. Put in order:

| Step | What happens | Kernel source |
|---|---|---|
| 1. Split | Sort the prompt into talk, a job (`#NN`) and an ask (`>`). Talk is not work and does not change the book. An unknown verb stays unknown. | law `0015.grammar` |
| 2. Resolve words | Look up each word and the page it lives on, before the act. "Learn, then do." | syntax `0013.triangulate`, Chain |
| 3. Find the place | Dictionary gives the word and its meaning. Concordance gives "one word, one place": a page. | law `0012.dictionary`, `0013.concordance` |
| 4. Find the rule | No face 01 on the page: go to page `0001`. No face 02: go to page `0002`. Then climb. | law `0059.rhyme`, `0032.climb` |
| 5. Choose what to pack | Door first, then the axioms, then the seat under test. Faces 01-04, and 08 if it exists. No 05, no 06, no drafts, nothing retired. | law `0037.pack`, `0036.colab` |
| 6. Check the pack | Walk every page the job names and every cite. A missing page is shipped, or the pack says it is withheld and why. | law `0036.colab`, Check |
| 7. State the job | One sentence. "A pack with no job is a pack fail." Two jobs in one pack cannot be graded. | law `0037.pack`, `0036.colab` |

Proposal: this is the read path. Steps 1-4 are the "translate" in the end goal; steps 5-7 are the "card".

Points that change the Workshop design:

- **Concordance is missing from `brands.md`.** The kernel splits two jobs: dictionary (word to meaning) and concordance (word to page). Workshop's dictionary is an index to brand cards only (C8.3). The pack builder needs word to page for words that are not brands, such as page keywords and card keys. `seqAddr.md` section 6 already reserves a concordance page.
- **The split step needs a model today.** Law `0015.grammar`: "Not a command runner. Compute is later. The model does this work with the user." `#NN` and `>` are typed by the person, so compute can split on them. Free text with neither is talk.
- **The pack check is compute work.** Step 6 is a walk over written links: exact, and no judgment.
- **"Eating the book is the fail."** A pack is small on purpose: "a cold model that is given the whole book answers from the average."

Also useful, still a kernel draft: law `0061.coldboot`. A pack carries homework, a few questions answerable only from the pack, and a sealed key. A sleeve that cannot answer has not read the pack. With a compute the key never ships: the compute holds it and checks the homework. This is a drift check that runs before the work starts.

## 2. Who picks the cites

Open question: lab 03 found that a cite carries the assignment, so someone must choose it.

Kernel answer: nobody chooses at pack time. Every face stamp carries its own `cite:` line (`cite: 1.7` on approve, `cite: 5.8` on ticket, `cite: 8.8` on pack). The cite is written when the page is written, checked at align ("a stale cite is a halt", law `0021.write`), and travels with the page.

Proposal:

- The pack builder copies cites from the stamps and cards it packs. That is compute work, and checkable.
- The cite was chosen once, by the page's author, and faced review with the page.
- A job item with no page behind it takes its band head's default lead (already proposed in `06.01.md`, lab 03).
- `7`: what a job item cites when neither exists.

## 3. Section D: tasks, returns, review, marks

### 3.1 Tasks and tickets

Law `0005.ticket` (signed draft `01.005`):

| Kind | Counters | Must name |
|---|---|---|
| Task (work on this page) | `05.01`-`05.49` | target, instruction, completion condition |
| Ticket (work sent outward) | `05.50`-`05.99` | path, instruction, return destination, completion condition |

- A task with no completion condition is not complete. This is axiom 5's "what done looks like".
- "A work item does not mint permission to edit, approve, lock, or promote law."
- "A closed item stays on the page. It is not reopened. The number is not reused. The next work takes the next number."

Proposal for the failure path (open in section D): a rejected review does not send the counter back to `open`. The counter closes with its outcome, and the rework is a new counter linked `continues-from`.

Conflict: Workshop counters run `01-98` with no split (A1.4). The task and ticket split is a decision for the Director.

### 3.2 The return

Law `0038.return`, `0036.colab`:

- Scores first, opinion second.
- One file per page, plus one factfind. "Chain, break, repair. The difference only."
- The hostile reader "names the face it was tempted to obey as live".
- Holes are numbered and point at a page, so the next pass can say "hole 1 closed".
- Opinion on how to solve is allowed in the factfind, "and only here".
- Overflow: "what did not fit will be invented later if it is not parked."
- Unprompted: "one thing you would have written differently, and why."
- "A return is not a promote."

This agrees with the return shape in `axioms/04.md` under axiom 5 (did, blocked, need, unprompted, overflow).

### 3.3 Reading a return

Law `0039.report`, `0040.lead`, `0053.emit`, `0036.colab`:

- Two passes. First read and note. Then make the jobs. "Do not write a seat in either pass."
- Notes and jobs go on one temp page first. "A return written straight onto a seat will eat the page."
- One number is one learning: overview, issue (only when something conflicts), why, ask. The path names the page and the face.
- The person answers by number. Each number can be released or held on its own.
- Jobs split into three: decisions, the writes those decisions named, and what is parked. Gravity is five.
- A fitness scale: 5 no break, 4 wording, 3 a careful sitting survives, 2 two lawful lines, 1 a literal walk halts, 0 cannot be followed.

### 3.4 Where a return lives

Open item in `06.01.md`: the workflow puts a return on a returns page; the tail design keeps it on the counter.

Kernel answer: both, as two different things. The return itself is one artefact that lands in one place (law `0038.return`). Its findings are then booked: "a note on face 06 keeps the learning on the page the learning is about. A task on that same page's face 05 is the work that follows" (law `0040.lead`). Booking them on a reserved page or on `0005` "is a miss".

Proposal: the return stays on its counter (the tail design). Its findings are booked as 06 notes and 05 tasks on the pages they concern. No returns page is needed.

### 3.5 Marks: signed, approved, lock

Carried item 2 in `06.01.md`. The kernel uses four states:

| Mark | Who | What it allows | Source |
|---|---|---|---|
| draft | any writer | nothing | law `0021.write` |
| signed | prime: "sign is the prime stamp" | "A signed face may be read. Acting on it needs approved." | law `0001.law`, Authority |
| approved | the director | the draft is seated; it may be acted on | law `0022.approve` |
| lock | the director | "A lock means state live." It is changed only by a replacement draft. | syntax `0017.dev` |

- "A signature is not an approval. An approval is not a lock."
- The way onto the seat is "align, then sign, then approve". Align checks the other faces and the cite.
- `7`: the kernel itself records "no page says what a lock is".

Proposal: sign is the maker's claim that a draft is aligned (every note struck, faces agree, cite fresh). Approve is the authority's `promote`. Lock is a flag on kernel-only law that needs level `00` to replace.

### 3.6 Small changes to a seated face

Law `0021.write`: "An active face can take a note, a patch, or a strike. A note is a footnote. A patch adds a missing sentence. A strike draws a line through a sentence that is no longer valid. If none of the three can hold the change, write a draft."

Conflict: Workshop D0 sends every change through copy, note, merge, promote. In an append-only log a patch and a strike are also appends, so the kernel's ladder may fit as two more operations. Whether Workshop allows them is a decision for the Director. They would cut the number of full drafts.

## 4. Where a conversation lives

Open question: no rule says where a turn lives.

Kernel answer: a turn does not live anywhere. Only work does.

- "Talk has no # and no >. It is not work. It does not sync the book." (law `0015.grammar`)
- "A job seen inside the talk gets a `# NN`, so it is not lost." (law `0053.emit`)
- One number per item until it is closed; no new number for the same item on the next prompt (law `0040.lead`, face 02).
- "A separate working note may capture the sitting before its findings are placed." (law `0006.note`)
- Temp band `0100`-`0199`: "a model may work there." (law `0056.band`)

Proposal:

| Thing | Where it lives |
|---|---|
| A session | one face 06 counter (already A4.4: one counter per session) |
| A job found in the talk | a face 05 counter on the page it concerns |
| The sitting's working note | a temp-band page, until its findings are placed |
| A turn of talk | not a page |

This removes my capacity worry. The limit of 98 applies to sessions and tasks per page, not to turns.

`7`: whether the raw talk is kept at all. Brand meters need the sentence words (C8.7 `use` entries), and a drift check needs the prompt. The kernel is silent, because it had no compute.

## 5. Approval without stalling

Open question: if every write needs a person, a conversation stalls.

Kernel answer, in part:

- Approval is batched and answered by number. "Batch as `#NN` so each finding can be released or held." The ask is "the `>` you want, so the director can release it."
- Signed is a real middle state. Work can be signed and read without being approved. Only acting on it waits.
- Law `0001.law`, Scope: each section declares an owner class: kernel-only, desk-local, or book-local. "The class is not a rank. It does not approve." It names who authorized the law.

So the model and compute keep working and signing; the person releases a batch in one reply.

`7`: what levels `02` and `03` grant. The kernel has no user levels.

## 6. Brand outcome signals

Open question: who detects a failed resolution? Compute writes meters (C8.7), but spotting a restatement is a judgment.

Kernel: no answer for words. Two related things:

- Book doors carry `born`, `used`, `fail`, `fresh` (law `00.md`, Note). The same meter shape exists at book scale.
- The kernel's outcome signals are explicit: the person's answer by number (release, hold, strike) and the 0-5 scale.

Proposal: count explicit outcomes as the signal (approve, strike, halt). Record a suspected restatement as a finding, not as a meter update. `7` otherwise.

## 7. Kernel position

Open question: a book entry does not record which kernel state it was validated against.

Kernel answer: the kernel does not change in a drip. `00.live` names which law book is live: "Today that slot is `01`." Promote rebuilds live from an approved draft: "Commit first. The snapshot is the undo. Build the candidate. Verify the copy. Then retire the old live book" (law `0023.promote`).

Proposal: kernel changes reach books as promoted releases, and each proposal records the kernel release it was validated against. This narrows A2.9 (live inheritance), which is settled, so it needs the Director.

---

## Open items in `alignment-notes.md`

### C4: face 08 links

Law `0008.map`, `0058.custody`, `0029.walk`:

| Row | Meaning |
|---|---|
| `member-of` | idea grouping |
| `continues-from` | the work chain directly before this |
| `references` | an ordinary dependency or pointer |
| owner | the address of who authorized the law |
| exception | source section, target scope, difference, reason, approving record |
| custody | parent, child, start, stop |

- "These labels describe connections and grant no authority." "A map row never approves itself."
- Start is "the thought the chain opens"; stop is "the thought it does not cross".
- Resolution: "Locate, verify identity, inspect relation." Do not walk every reference as a parent, do not scan sideways, do not choose by number. "Proximity is not lineage" (law `0018.seqaddr`).
- "A page with a child requires a map." "A child that does not point back is a hole. Do not fill it." This is `8.7`.

Proposal: the Workshop `link` card's `kind` field (now continuation or child) takes these kinds. The compute builds its in-memory graph from 08 rows in the log.

### C5: precedence between levels

Law `0001.law` (Scope, Inheritance, Overrides) and law `0018.seqaddr` (Hierarchy):

- "Left outranks right. A present axis governs downward. It does not bleed upward."
- "Outside that band, peers do not outrank. 20 does not parent 21 unless the proof says so."
- A local definition is usable "only if it owns that subject and scope and agrees with inherited constraints, or has a lawful named approved exception".
- "A book owned by the kernel is not overridden by a local desk without permission."
- A conflict is reported with both artefacts kept, "not settled by majority vote".

This supports C5.4 as proposed. The addition is the owner class: the nearest definition wins for a desk-local or book-local subject, and a kernel-only section is never overridden without a named, approved exception.

### C7: notes metadata

Law `0006.note`, Lineage card: "Observation; source; proposed/change state; why; unresolved."

Proposal: note fields `by`, `date`, `refs` (source), `why`, `state`, `unresolved`. `06.01.md` already uses the first four.

### C8.10: where a new brand card goes

Law `0012.dictionary`: "A dictionary stores the word, the brand, and a short meaning. It does not store the page."

So in the kernel the dictionary itself holds a short meaning, and a word with no page still has a home. This conflicts with C8.3 (the dictionary is only an index). An option for the Director, not an answer.

### C1.4: do continuation pages share the `pointer` type?

`7`. Law `0018.seqaddr`: "A full 99seq is parked. No page form yet."

### Axiom 9: must the hostile pass come from a different intelligence?

Partly answered.

- Law `0036.colab`, Prime: "the sleeve that wrote the pack must not grade only its own sentences."
- Law `0031.sim`: "Use only the page. Do not use the last sitting's memory." A pass is "one cold act completed from the page".

Reading: a fresh sitting with only the page is enough to test whether a page can be followed. Grading the work needs a view that did not write it. `7`: the kernel's own tests of this (`0142.solo-pass`, `0149.self-attack.test`) are not in the zip.

### Carried items in `06.01.md`

- **Item 6, `FF.VVV.09`.** Law `0024.version`: "VVV is a three-digit axis. It has two forks. One is the version on a face. The other is a brand." Law `0009.retire`: "09 is the retirement tail, not a page face." In Workshop the log replaces the version fork, and the `retired` tail replaces `.09`. Proposal: three digits mean a brand only, and item 6 closes.
- **Item 9, the axioms page number.** In the kernel the axioms are not a page. They are furniture: `00.axioms` beside the book door, "outside the pages", and another book writes its own "only for a local modification". Workshop has no furniture. `7`: its closest lawful home.
- **Item 3, hats.** The kernel roles are director, prime and sleeve, with the clerk as the compute.

---

## Where the kernel and Workshop disagree

Workshop governs. These are listed so nobody copies the kernel by mistake.

| Subject | Kernel | Workshop |
|---|---|---|
| Shelf `00` | "Shelf number `00` does not exist. There is no shelf sentinel." | `DD.SS.00` is the shelf's own book (A4.1) |
| Kernel books | two books on desk `00`: syntax `00.00.00` and law `00.00.01`; "kernel books `01`-`09` match that face" | one kernel book `00.00.00`; desks `01-09` are kernel branches (A6.3) |
| Page `0012` | gravity in the syntax book; dictionary in the law book | dictionary (C8.3), while `axioms/04.md` cites `0012.gravity` and `0013.triangulate` |
| Face 09 | "the end of the tail. It is not a face." | unassigned (A4.3) |
| Face 00 | "Face `00` is not a page file." | the page's identity face (A4.2) |
| Versions | `FF.VVV` drafts, `FF.VVV.09` retired, a retire warehouse per book | the append-only log |
| Dictionary slices | a slice past twenty words breaks | 52 fixed sections, never re-split (C8.6) |
| Bands under `0100` | door ends in 0, band ends on 9, sizes vary | fixed ranges in `seqAddr.md` section 6 |

The page `0012` row is a live conflict inside Workshop, not only against the kernel. With one kernel book, gravity and the dictionary cannot both be page `0012`.

## Unprompted

- Pages `0001`-`0009` rhyme with the faces: page `0005` is the law of face 05, page `0002` face 01 is "the law of schema" (law `0059.rhyme`, The cross). Workshop keeps `0001-0009` as "special reserved pages" without saying this. If the rhyme is kept, each face's rules have a fixed home, and the fallback in step 4 above works.
- Slot allocation is compute work. Law `0034.slot`: "The lowest missing member number is the slot." "Do not pick `0040` because it looks round." A model should never choose a page number.
- Law `0009.retire` records three readings of when a retired face may be opened, and chooses none. Workshop axiom 9 chose one: open the predecessor, read-only, before replacing.

## Faces read

- **Syntax book `00.00.00`:** `00.md`; face 01 of `0001.rules`, `0003.operate`, `0010.about`, `0013.triangulate`, `0014.design`, `0016.compose`, `0017.dev`.
- **Law book `00.00.01`:** `00.md`, `00.order.md`; face 01 of `0001.law`, `0004.user`, `0005.ticket` (`01.005`), `0006.note`, `0007.reserved`, `0008.map`, `0009.retire`, `0011.contents`, `0012.dictionary`, `0013.concordance`, `0015.grammar`, `0016.compose`, `0018.seqaddr`, `0021.write`, `0022.approve`, `0023.promote`, `0024.version`, `0026.strike`, `0028.crawl`, `0029.walk`, `0030.method`, `0031.sim`, `0032.climb`, `0033.point`, `0034.slot`, `0035.halt`, `0036.colab`, `0037.pack`, `0038.return`, `0039.report`, `0040.lead`, `0053.emit`, `0056.band`, `0057.bands`, `0058.custody`, `0059.rhyme`, `0060.drafting`, `0061.coldboot`.
- **Other faces:** face 02 of `0006.note`, `0008.map`, `0037.pack`, `0038.return`, `0039.report`, `0040.lead`; face 04 of `0005.ticket` (`04.005`) and `0036.colab`; face 07 of `0001.law` (`07.002`).
