# Workflow loop

state: draft
copy of: `workflow-loop.md` (the Director's original, unchanged)
by: claude-opus-5-5, 2026-11-11
axioms: 5.3.6
why: how work loops from a design to a build and back, so a model can run passes without history and a person can check every step.

How to read this draft:
- `axioms:` lines are the quick why. Each section cites the axioms it rests on; open `Axioms.md` for the reason.
- **(filled)** marks a detail added in this draft that the original did not have. The Director asked for the missing pieces to be found and filled (`7`). Each one is a proposal.
- `7` marks what is still missing and needs the Director.

---

## 1. Roles

axioms: 1.3

| Role | Who | Does | Does not |
|---|---|---|---|
| Person | the Director, or whoever holds the level | approves the N4 page; approves changes to 01 and 04; answers elevations | |
| Lead | a model, once the N4 page is approved; or a person | reads N4, writes packs, reads returns, runs passes, drafts changes to 01/04 | change 01 or 04 without approval |
| Builder | a model, a person, or compute | claims a pack, does its work cards, writes the return | write outside the pack's grant |
| Reviewer | a view other than the builder **(filled)** | tries to break the return before it closes | review its own work |
| Compute | the compute | holds the templates, lints packs and returns, moves tails, counts passes, forces the why questions | decide a disputed question |

A lead is not authority (axiom 3). The lead works inside what the approved N4 page grants (axiom 1).

## 2. Band design

axioms: 2.6

Bands use the hundreds digit of the page (seqAddr section 6): `N4` means `N400-N499` in any thousands band.

| Band | Name | Holds |
|---|---|---|
| N0NN | doors **(filled)** | band heads: the default lead, the default page type `workflow`, which lint template applies |
| N1NN | not in use | |
| N2NN | not in use | |
| N3NN | build | modules built, with explanation. Face 01: what the module is. Face 02: the module's files described (section 3.1). Face 08: links to the files in the repo |
| N4NN | dev | the design: what the work is, its MVP, goals, what we are trying to prove. Person and model talk here. Face 04 mostly, with 01 to go with it |
| N5NN | jobs | packs and returns, as face 05 counters |
| N6NN | not in use | |
| N7NN | colab | labs: cold-model trials of the page's work |
| N8NN, N9NN | not in use **(filled)** | reserved |

`N00` in each band is the door; work starts at `N01`.

Conflict to settle: decision A2.6 uses another band example (4 dev, 5 build), and the earlier pack-lint run used 1 returns, 2 code, 3 compute. This draft follows the Director's newest map. A2.6 should be corrected to match once approved.

## 3. Bound bands

axioms: 2.6.8

- One subject has one two-digit number across bands. A timer: design `0401.timer`, packs and returns `0501.timer`, build `0301.timer`, labs `0701.timer`.
- They must link. Each page's face 08 links to its set, both ways (axiom 8).
- **(filled)** The compute checks the set: a set page that is named but cannot be opened is `7.8`, raised, never created from a lookalike.
- **(filled)** Lineage runs through the set: from a build back to its pack, from the pack back to the design, from the design back to its approval (axiom 6).
- **(filled)** A subject that outgrows one page continues through `99` (seqAddr section 7); the set number stays the same in the next thousands band (`1401` binds to `1501`).

### 3.1 Code lives in the repo, linked

axioms: 8.6

Decided by the Director (2026-11-11): code lives in the repo, not in the book.

- The N3 page describes the module: face 01 what it is, face 02 its files, what each does and its interface.
- Face 08 links each file by its repo path. A work card's `path` is the same repo path.
- **(filled)** Each link records the commit it was last checked at, so the build page's lineage can be followed in the repo's history (axiom 6).
- **(filled)** The compute checks that each linked path exists. A path that cannot be opened is `7.8`, raised, never repointed to a similar file.
- **(filled)** The book keeps the why; the repo keeps the code. If the code rots, the why on N4 and N3 is enough to rebuild it.

## 4. The N4 page and its approval

axioms: 1.4.5

- N4 states the work: the MVP for this page, the goals, what we are trying to prove. Written on face 04, with an agents.md-style face 01 to go with it.
- **The person approves the N4 page.** Once it is approved, a model lead may design packs and run loops on it. (Director)
- **(filled)** That approval is the written permission of axiom 7 for this subject: work inside the approved N4 page needs no further grant; work outside it is raised. This answers part of open item E8.
- **(filled)** N4 face 05 holds the design questions still open on the page. N4 face 06 holds the lead's notes, one per pass (section 7). `7`: whether N4 05 counters should mirror the N5 counter numbers.

## 5. Packs

axioms: 5.3.9

A pack is a face 05 counter on the N5 page: `0501.05.NN`. It is an agents.md-style build list for a builder. `05.01` is the first place a pack can be written.

### 5.1 Pack header

| Field | Holds | axioms |
|---|---|---|
| `by` | who made the pack | 6 |
| `authorized` | the approval it rests on: the N4 page's approval record **(filled)** | 1.7 |
| `lead` | the lead letters, if they differ from the band default (`3MC`) **(filled)** | 3 |
| `axioms` | the chain for the whole pack **(filled)** | |
| `outcome` | what done looks like | 5 |
| `overview` | what the work is trying to achieve; matches N4 01 and 04 | 5.2 |
| `stop if` | where the builder stops and raises **(filled)** | 5.1 |
| `grant` | the addresses the builder may write to **(filled)** | 1 |

### 5.2 Work cards

The original calls each piece of work `#NN`. A model can add as many as the work needs, which is good: the pack grows with the work.

**Proposed term (filled): a work card, written `W01`, `W02`.**
- `NN` already means a counter (`05.NN`), so `#NN` inside a counter reads as two counters.
- `#NN` is also used for jobs released in talk (`#03 >run`, `claude/readpath.md`).
- `CC` clashes with C for compute in the lead letters (`3CM`).
- `W` is free, short, and says what it is. A work card is a card in seqAddr's sense: a `##` heading with field lines, so it uses the card shape that already exists (axiom 2). Card type `work`.

Each work card:

```text
## W01 build the lead command
axioms: 5.4
placed: 2026-10-22
reason: From 0107.workflow/05.09 W05.
recommend: In jobs.py, add a command that takes Did, Blocked, and Need and writes them as three lines before the first work card on a return. It refuses a counter that is not a return. Stamp the change. Keep the older copy.
path: 10.workshop/10.10.work/10.10.10.lib/code/jobs.py
scale: 2
lead: 3C
ask: >build Add the lead command.
```

- `reason` is the why (axiom 4). A work card with no reason fails lint.
- `scale` **(filled, `7` until confirmed)**: the size and risk of the card, 1 to 5. A card at 4 or 5 needs a lab in N7 before its result is promoted (axiom 9).
- `lead` only when it differs from the pack's.
- `axioms` optional, and encouraged: it is the quick why for the builder.

## 6. The loop

axioms: 5.6.9

Tails move one step at a time, and the compute enforces them (seqAddr section 4):

```
draft -> pack -> open -> return -> review -> closed
```

| Step | Tail | Who | What happens | axioms |
|---|---|---|---|---|
| 1 Write | `draft` | lead | writes the pack and its work cards | 5 |
| 2 Lint | `draft -> pack` | compute | checks the pack against its template (section 8). A pack that fails stays `draft` | 3C |
| 3 Claim | `pack -> open` | builder | claims it; the first claim wins (format.md) | 3 |
| 4 Work | `open` | builder | completes each work card. Asks questions; applies for permission or solutions to what blocks it; stops at `stop if` | 5.1 |
| 5 Return | `open -> return` | builder | appends the return to the **same counter** (section 6.1). Lint checks its shape | 6 |
| 6 Review | `return -> review` | reviewer | tries to break it **(filled)** | 9 |
| 7 Close | `review -> closed` | compute, on the reviewer's outcome | closed with its outcome: passed, or failed | 6 |
| 8 Lead pass | | lead | reads, notes, elevates, decides the next pack (section 7) | 6.4 |

### 6.1 The return lives on the counter (filled)

The original says the builder "makes a copy calling it 05.NN.return". In the book format nothing is copied: the builder moves the counter's tail to `return` and appends the return body. The pack text stays in the log as the earlier entry, readable and never rewritten (axiom 6). This settles where a return lives.

### 6.2 Return shape

axioms: 5.6

- Per work card: `W01 done`, `blocked`, or `need`, with what was done and the full address it touched.
- Then: questions, permission asked, solutions proposed to what blocked it.
- Then, at the end, each with its why: **notes**, **unprompted** (one thing the builder would have done differently), **overflow** (what was seen outside the frame, reported and not acted on).

### 6.3 Review (filled)

axioms: 9.1

- The reviewer is a view other than the builder: the lead, a person, or a cold model in N7. The builder never reviews its own return.
- It checks the return against the pack's outcome, every address against the grant, and tries to break the result.
- **A failed review does not reopen the counter.** It closes with outcome `failed`, and the rework is a new counter linked `continues-from` (proposed by Fable from the old kernel). The record of what failed stays.

### 6.4 Open while the builder is gone (filled)

A counter left `open` with no return: `7` how long before the compute marks it stale. Once stale, it is raised to the lead, and the work goes into a new counter `continues-from` it. The stale counter is closed with outcome `abandoned`.

## 7. The lead's pass

axioms: 6.4.1

Each pass, before writing a new pack, the lead:

1. **Reads N4 01 and 04,** the notes on N4 face 06, and the reviewed return. Every pass. (Director)
2. **Writes a note** to N4 as a matching `06.NN`: what the return taught, what changed, why.
3. **Elevates changes to 01 and 04.** When they need updating, the lead does not change them. It elevates with suggested changes, as a draft, and the person approves (axioms 1 and 9; drafting).
4. **Decides:** if the MVP is complete, the loop ends. If not, it writes the next pack.

## 8. Pack lint

axioms: 2.3C.8

The compute holds the template for the shape a model must produce: a pack, a work card, and a return. The template lives in the kernel as card types (decision C8.9), so every book inherits it and a band may override it only by name (axiom 2). This is what `0117.pack-lint` was.

**(filled)** What the lint checks:

| Check | On | Kind |
|---|---|---|
| header has `by`, `authorized`, `outcome`, `overview`, `stop if`, `grant` | pack | hard: stays `draft` |
| `authorized` points to an approved N4 page | pack | hard |
| every work card has `reason`, `path` and `ask` | pack | hard |
| every `path` is inside the `grant`, and inside the authorizer's level | pack | hard |
| every address in the pack opens | pack | hard; missing ones are listed as `7.8` |
| `axioms:` chains parse | pack, card | hard |
| every work card has a result (`done`, `blocked`, `need`) | return | hard: stays `open` |
| every address the return touched is inside the grant | return | hard |
| notes, unprompted and overflow present (may be empty, with a why) | return | finding |
| a work card with no `axioms:` line | pack | finding |

Hard checks refuse the tail move with a reason. Findings are recorded for review.

## 9. Gravity: how many passes

axioms: 5.4.1

The number of passes is an aim, not a quota. 1-3 passes is normal. Models left alone loop on one detail, so there are hard move-on points.

The compute counts passes **by one lead without consulting the person**: return counters on the N5 page since the person last approved or answered. For example, the page is at `05.24` and this lead has run 4 of them since the person last spoke.

| Passes without the person | What happens |
|---|---|
| 1-3 | normal |
| 4 | **the compute forces the why questions** before the next pack can leave `draft`. The lead answers; the compute records the answers as an N4 06 note. |
| 6 **(filled)** | **halt.** No new pack until the person answers. Elevated with the recorded answers. |

**(filled)** The why questions:

1. Why does this need another pass? (4)
2. What did the last return change, in one sentence? (6)
3. Is the frame the right size, and does it let the work finish? (5)
4. Is the remaining gap worth its cost, in proportion to being wrong? (4)
5. Is this the same detail as the last pass? If so, why will this pass differ? (9)
6. What is missing that only the person can give? (7.1)

**(filled)** The compute also records a finding when two passes in a row carry work cards with the same `path` and `ask`: a loop on one detail.

## 10. Open (`7`)

- Whether N4 face 05 counters mirror the N5 counter numbers.
- `scale`: confirm the meaning (size and risk, 1-5) and the lab threshold.
- The term `W01` for work cards.
- How long an `open` counter waits before it is stale.
- When N7 labs are required: by scale, by changes to law faces, or only when the lead or person asks.
- Decision A2.6 to be corrected to this band map.
