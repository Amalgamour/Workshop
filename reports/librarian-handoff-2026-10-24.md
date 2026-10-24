# Librarian Rebuild — Handoff for a Review Bot

**Date:** 2026-10-24  
**From:** grok-prime (work prime for the rebuild)  
**To:** a Grok bot that will review this work and advise on using bots to speed the build  
**Book:** `10.workshop/10.10.work/10.10.12.rebuild` on branch `rebuild`  
**Repo:** https://github.com/Amalgamour/Librarian  

This report is written from the pages, not from memory. Sources are named.

---

## 1. What Librarian is

Librarian is a system for preserving the work of a user and models so that the next model does not have to reconstruct it. The files are the only memory. If it is not written in the repo, the next model does not have it.

The Director is Matthew John Fisher. He decides. The work prime proposes and writes the packs. Models are replaceable. The clerk is the mechanical compute that records and retrieves so models and the Director do not search or do mechanical work.

The current book is `10.10.12.rebuild`. Its purpose, from `00.md`:

> This book rebuilds the kernel with its compute inside it, so the kernel can run and models stop working without compute.

The working kernel is `00.00.00.kernel.draft`. The closed check kernel is `00.00.00.kernel`. `00.kernel` is a third copy. Recent packs write only to the draft. That is the current seat (`0113.law-align/05.17`).

---

## 2. How the book is divided

Normal bands are centuries. A band starts at NN00. NN99 is the end sentinel. Only the 00NN range uses decades. A user band may expand (example: 1200–1499).

The process bands for this book, from `00.md` and `0407.workflow/01.md`:

| Band | Pages | Job |
|------|-------|-----|
| Law | 0000–0099 | Face law, about, behavior, structure |
| Returns | 0100–0199 | Builder writes the return |
| Code | 0200–0299 | Module while it is being written |
| Compute | 0300–0399 | Seated modules that run |
| Dev | 0400–0499 | Decisions. Director answers here |
| Packs | 0500–0599 | Work prime writes the ready pack |
| Notes | 0600–0699 | Notes that match a pack number |
| Reserved | 0700–0899 | Closed |
| Temp | 0900 | Session scratch. Not authoritative |

Matching rule: one number, one name. A slice decided on `04NN`, packed on `05NN`, built on `03NN` (or coded on `02NN`), and returned on `01NN` is one trackable pass. The `05.NN` numbers stay aligned.

Book order for the front matter (Director, 2026-10-23):

1. About — the back of the book, the publisher page.
2. Contents — what exists in this book.
3. Dictionary — words used here that are not average meanings.
4. Concordance — every place those words appear.

`0012` is the dictionary. `0013` is the concordance. Face 06 of `0013` was revised to match (`0513/05.20`).

---

## 3. The loop

From `0407.workflow/01.md`:

1. A decision is released on a `04NN` page.
2. The work prime writes a ready pack on the matching `05NN`.
3. The builder runs only the ready lines, writes the return on the matching `01NN`, commits and pushes.
4. The reviewer closes what is clear and surfaces only real choices (the issue, the options, and what each option does).
5. The Director answers. The answer is applied. The next pack is `05.NN+1`.

Lifecycle of a pack file:

- `05.NN.draft.md` — open, editable. Builder ignores it.
- `05.NN.pack.md` — ready. Builder may run it. Frozen.
- `05.NN.return.md` on the `01NN` page — the builder’s return.
- `05.NN.md` — closed. Prime has reported.

No one renames a file by editing its name. Commands do it.

Pack shape (every overview):

- Do: one sentence, the exact change or the exact test.
- Stop if: the condition that blocks.
- File: where the hole is written.
- Return must start with Did, Blocked, and Need.

Return shape (before the `#NN` statuses):

- Did: what landed.
- Blocked: what stopped, or “nothing.”
- Need: the next action, or “none.”

Every pack also asks: Does this work well? Does a tool need to be updated? Did you cold-boot test?

---

## 4. What works

These are confirmed by returns, not by intention.

**Compute owns the form.** Direct model writes drift. Tools stamp headers, versions, and hashes. When a model invents a title, the tools stop it (`jobs.py` refused invented titles; `page.py stand` refused the check kernel).

**The pack/return loop is readable.** Did / Blocked / Need lets the prime see the outcome in three lines. The `#NN` statuses hold the detail.

**Wider packs are faster.** One small change per pack left the builder idle in minutes. A pack that carries three related moves (tool fix, the work, the next hole that uses the same tool) finishes in one run. Confirmed on `0514/05.13` and `0513/05.12`.

**The queue page keeps the prime from waiting.** `0415.queue` holds Out, Waiting, Next, Goal, and Labs. When no return is in, the prime writes the next pack from Next. Confirmed: the builder stayed fed across the law-align stretch.

**Private words and lookup work.** Ten user-unique words were stored on `0116.words`. `journal.py lookup` returns the private meaning from a stood page when the book has no `0013` page. A missing word stays missing (`0513/05.15`).

**A bare version 001 face can be seated.** `clerk.py seat` writes a bare face onto the draft law book and keeps the source block. It refuses the check kernel and `00.kernel` (`0513/05.12`).

**`00.live` is the clerk save.** Four lines: last, when, goal, pages. The clerk writes it. A model cannot. On boot the clerk can hand those four lines to a model (`0513/05.20`).

**The sample law list is seated.** 54 titles. All are on `00.00.00.kernel.draft/00.00.01.law`. The door `1000.work` exists and names `1001.accounting`. The order lists `1000.work`.

---

## 5. What we learned

**Memory bleeds.** A model that writes from memory invents titles, points at the wrong path, or uses an old name. The tools stopped several of these. The fix is: read the page, name only what is on the page, and let the tool refuse the rest.

**Narrow packs waste the builder.** The builder finishes a one-line pack in minutes and waits. The prime must have the next pack ready, or the builder idles. The queue and the “three related moves” rule address this.

**The Director is not a rubber stamp.** A pack that asks for a decision without explaining the issue, the options, and what each option does produces a flawed or missing decision. The prime’s job is to explain before asking. Confirmed by the Director on 2026-10-22.

**Face sentences drift.** While seating work ran, `00.readme`, face 06 of `0013`, and the contents seat fell out of agreement with the approved faces. Face clean-up is a separate pass. It does not block tools, but a cold model will follow the wrong sentence if it is left.

**The clerk should hold the live state.** `00.live` was a file that tracked what was being worked on. It is now the clerk’s save: last action, when, goal, and pages. The clerk overwrites it at the end of a pack. Older lines stay in the returns.

**Testing is part of every pack.** Cold-boot, tool-update, and “does this work well” are recorded on every return. That made the holes visible (page.py test looking for `01.001.draft.md`, lookup stopping on a missing concordance, stand refusing the draft law book).

---

## 6. Roadblocks still open

These are the remaining holes. None of them block the tools that already run. They will block a cold model or a later pass.

1. **Desk boot does not call `clerk.py live`.** `00.live` exists and holds the four lines, but a boot does not yet read it and hand it to the model. The handoff is designed; the call is not wired (`0513/05.20` Overflow).
2. **Contents seat is not promoted.** The draft `02.005.md` of `0011.contents` names `1001.accounting`. The approved seat still says `list: empty`. Promote is a later step.
3. **`00.start.md` still says `00.live` names the law book.** The sentence was not revised in `05.20`. A cold model that reads `00.start` first will get the old claim.
4. **Order note still lists a missing folder.** The note on `00.order.md` keeps `- 0160.structure-door.temp`. That folder is absent, so the checker counts the line. The note was not rewritten.
5. **lcheck still reports pending errors.** Reworked: 1 error / 0 warn / 60 info. Pending: 31 errors / 43 warn / 32 info. Order warn stayed 33. These are not cleared.
6. **Three books of the law.** The draft is the seat. The check kernel and `00.kernel` do not hold the new pages. No choice was made to promote or to close the other two. A later pass must decide whether the draft becomes the only seat.
7. **Dictionary and concordance are not fully compute-backed.** Words can be stored and looked up from a stood page. A full concordance that points every word to every page is not built. Face 03 parent slices `03.10`–`03.19` were not created.
8. **Interface is not built.** The goal is a kernel that models can use through the Director’s computer or GitHub. The clerk is modules. An interface and an enforced clerk come later. No terminal or GUI is in this stretch.

---

## 7. How bots can speed the build

The current loop is one prime and one builder. The prime writes packs. The builder runs them. The Director answers only real choices.

A bot can take a slice of that loop if it is given the pages and the rules, and if it is not asked to invent.

**What a bot can own without the Director**

- Writing the next pack from the queue when no return is in.
- Reviewing a return: read Did / Blocked / Need, update the queue, pack the next clear move.
- Face clean-up that is already decided (revise a sentence to match an approved face).
- Cold-boot checks and hash records.
- Keeping `00.live` current at the end of a pack.

**What a bot must not own**

- Choosing a title that is not on a page or in the sample list.
- Promoting an approved seat.
- Deciding which law book is the only seat.
- Asking the Director for a decision without explaining the issue and the options.

**How to use bots to go faster**

1. **One bot on the queue.** It watches for returns, updates `0415.queue`, and writes the next pack from Next. The prime reviews the pack before it is marked ready, or the pack is marked draft until the prime promotes it.
2. **One bot on face clean-up.** It reads the overflow of each return and packs the sentence fixes that do not need a decision. It does not touch tools.
3. **One bot on the test desk.** It runs the three session checks (timer, private words, PDF) after a tool change and files the hole if a check stops. It does not invent an exporter or a page.
4. **The builder stays the builder.** It runs only ready packs. It does not design. The compute stops it when it would invent.

The speed gain is not more models writing at once. It is fewer idle minutes between a return and the next ready pack, and fewer packs that stop because the path or the title was wrong.

---

## 8. Pages the review bot should open first

- `10.workshop/10.10.work/10.10.12.rebuild/00.md` — book sentinel and band layout.
- `0407.workflow/01.md` — the loop, the shapes, the lifecycle.
- `0415.queue/01.md` and `0415.queue/06.20.md` — purpose and current lists.
- `0010.about/01.md` — how to read a page.
- `0012.dictionary/01.md` — dictionary purpose.
- `0113.law-align/05.17.return.md` — current seat.
- `0113.law-align/05.20.return.md` — `00.live` and concordance face.

Do not invent a title that is not on those pages. If a path is missing, stop and file the hole.

---

## 9. Notes taken while reading this draft

These notes were written while reading the draft above, then merged into the sections they belong to. They are struck here so the merge is visible.

- The band table in section 2 matches `00.md`, including reserved and temp. Merged.
- The lifecycle tails are listed in order. Merged.
- “What works” cites a return, not a plan. Merged.
- Roadblocks exclude holes already closed. Merged.
- The bot section names what a bot must not own. Merged.
- The first pages to open are named with paths. Merged.

---

## 10. What this report is not

It is not a pack. It is not a promote. It does not edit the kernel. It is a handoff so another model can review the work and advise on bots without reconstructing the loop from chat.
