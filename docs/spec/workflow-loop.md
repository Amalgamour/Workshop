# Workflow loop

state: draft — Director review required; not live
copy of: `workflow-loop.001.md` (preserved unchanged)
revision: `.002`, 2026-11-11
revision-authority: Director approved S01-S12 and four design choices; implementation details marked `7` remain proposed
axioms: 5.3.6
why: how work loops from a design to a build and back, so a model can run passes without history and a person can check every step.

How to read this draft:
- `axioms:` lines are the quick why. Each section cites the axioms it rests on; open `Axioms.md` for the reason.
- **(filled)** marks prior `.001` additions retained as context.
- **(approved Sxx)** marks decisions approved for `.002` by the Director; implementation remains a draft until this full document is reviewed.
- **(proposed detail)** marks one possible implementation of an approved solution, not a newly approved governing law.
- `7` marks a detail still missing or needing authority.
- See `workflow-loop.002-notes.md` for copy → notes → strike/update → reread reconciliation.

---

## 1. Roles

axioms: 1.3

| Role | Who | Does | Does not |
|---|---|---|---|
| Person | the Director, or whoever holds the level | approves a specific N4 revision, its frame and delegation; authorizes governing changes; answers elevations | delegation cannot exceed their own authority |
| Lead | a model, once the N4 page is approved; or a person | reads N4, writes packs, reads returns, runs passes, drafts changes to 01/04 | change 01 or 04 without approval |
| Builder | a model, a person, or compute | claims a pack, does its work cards, writes the return | write outside the pack's grant |
| Reviewer | a view other than the builder **(approved S10)** | independently checks evidence against acceptance criteria; challenges assumptions; uses N7 for required higher-risk trials | review its own work; accept the builder's summary as proof |
| Compute | the compute | resolves approved revisions, enforces grants, creates handoffs, lints records, verifies recorded state changes, moves tails, counts passes, records claims | decide a disputed question or infer an approval |

A lead is not authority (axiom 3). The lead works inside what the approved N4 page grants (axiom 1).

## 2. Band design

axioms: 2.6

Bands use the hundreds digit of the page (seqAddr section 6): `N4` means `N400-N499` in any thousands band.

| Band | Name | Holds |
|---|---|---|
| N0NN | reserved / existing kernel allocation | not a universal doors band; each allocated band has its own `N?00` band head **(approved S05)** |
| N1NN | not in use | |
| N2NN | not in use | |
| N3NN | build | modules built, with explanation. Face 01: what the module is. Face 02: the module's files described (section 3.1). Face 08: links to the files in the repo |
| N4NN | dev | the design: what the work is, its MVP, goals, what we are trying to prove. Person and model talk here. Face 04 mostly, with 01 to go with it |
| N5NN | jobs | packs and returns, as face 05 counters |
| N6NN | not in use | |
| N7NN | colab | labs: cold-model trials of the page's work |
| N8NN, N9NN | not in use **(filled)** | reserved |

`N?00` is the door of each hundred-page band (for example `0400` or `1500`); ordinary subject work starts at `N?01`. This notation is explanatory, not a new SeqAddr grammar. The existing special ranges `0000-0099` still obey SeqAddr reservations.

**(approved S05)** This workflow specializes the band map as N3 build, N4 dev, N5 jobs, N7 colab. The prior examples in decision A2.6 and pack-lint history are not authority to overwrite this map. Update their documentation through its own authorized drafting path; do not silently edit SeqAddr. `7`: confirm whether other page types use a different band specialization.

## 3. Bound bands

axioms: 2.6.8

- One subject has one two-digit number across bands. A timer: design `0401.timer`, packs and returns `0501.timer`, build `0301.timer`, labs `0701.timer`.
- They must link. Each page's face 08 links to its set, both ways (axiom 8).
- **(filled)** The compute checks the set: a set page that is named but cannot be opened is `7.8`, raised, never created from a lookalike.
- **(filled)** Lineage runs through the set: from a build back to its pack, from the pack back to the design, from the design back to its approval (axiom 6).
- **(approved S05)** Matching subject digits establish a possible *set*, not continuation. Thus `1401` (dev) and `1501` (jobs) are band counterparts, **not** a continuation link. Overflow follows SeqAddr section 7: a `PP99` pointer names the next allocated hundred for the **same role**, with explicit Face 08 forward and back-links. Never infer a continuation target from matching digits or title.
- If a new continuation changes subject numbering, record a `continues-from` relation and set membership explicitly. The original identities remain immutable.

### 3.1 Code lives in the repo, linked

axioms: 8.6

Decided by the Director (2026-11-11): code lives in the repo, not in the book.

- The N3 page describes the module: face 01 what it is, face 02 its files, what each does and its interface.
- Face 08 links each file by its repo path. A work card's `path` is the same repo path.
- **(filled)** Each link records the commit it was last checked at, so the build page's lineage can be followed in the repo's history (axiom 6).
- **(approved S02)** The return cites exact changed paths and Git commit or working-tree revision plus verification evidence. A claimed change without inspectable evidence is not accepted merely because the builder reported `done`.
- **(filled)** The compute checks that each linked path exists. A path that cannot be opened is `7.8`, raised, never repointed to a similar file.
- **(filled)** The book keeps the why; the repo keeps the code. If the code rots, the why on N4 and N3 is enough to rebuild it.

## 4. The N4 page and its approval

axioms: 1.4.5

- N4 states the work: the MVP for this page, the goals, what we are trying to prove. Written on face 04, with an agents.md-style face 01 to go with it.
- **(approved S01)** The person approves **one identified N4 revision** with its acceptance criteria, permitted scope, approving authority, and delegation terms. Approval is a lineage record with a stable identifier, not a mutable flag on the page.
- **(approved S04)** Within the explicitly approved N4 scope, the lead may direct passes and authorize routine completion and promotion **only to the extent delegated**. Promotion still requires independent trial and compute checks. Governing changes, changed acceptance criteria, expanded grants, or material changes outside the approved frame require elevation and fresh approval.
- A pack links to the exact approval record and N4 base revision. Compute refuses an unrelated, stale, or insufficient grant; it does not guess whether a later N4 edit was approved.
- **(filled)** This revision-bound approval is written permission to act within the agreed frame, not blanket permission to alter law, change Face 01/04 independently, or expand the frame. Axiom `1.7.8` is checked before each write.
- **(approved S12)** N4 Face 05 holds design questions; N5 Face 05 holds execution packs. These are independent counted boards, not mirrored counters. Every related question and pack uses explicit Face 08 links to its counterpart, where one exists.
- N4 Face 06 holds the lead's session/pass notes. A note references the exact reviewed N5 return and N4 revision it was written against. Matching counter numbers may help a reader but are **never evidence of connection**.

## 5. Packs

axioms: 5.3.9

A pack is a face 05 counter on the N5 page: `0501.05.NN`. It is an agents.md-style build list for a builder. `05.01` is the first place a pack can be written.

### 5.1 Pack header

| Field | Holds | axioms |
|---|---|---|
| `by` | who made the pack | 6 |
| `authorized` | immutable approval ID and approved N4 revision **(approved S01)** | 1.6 |
| `lead` | the lead letters, if they differ from the band default (`3MC`) **(filled)** | 3 |
| `axioms` | the chain for the whole pack **(filled)** | |
| `outcome` | what done looks like | 5 |
| `overview` | what the work is trying to achieve; matches N4 01 and 04 | 5.2 |
| `stop if` | where the builder stops and raises **(filled)** | 5.1 |
| `grant` | explicit allowed operations and target addresses/path patterns, bounded by the approval **(approved S01, S08)** | 1 |
| `frame` | approved MVP/work-frame ID for gravity accounting **(approved S09)** | 5.6 |
| `risk` | risk/impact rating used to select evidence and independent trial **(approved S02, S10)** | 5.9 |
| `predecessor` | previous pack or issue and expected artifact revisions, if any **(approved S06)** | 6.8 |

### 5.2 Work cards

The original calls each piece of work `#NN`. A model can add as many as the work needs, which is good: the pack grows with the work.

**(approved S07)** The work-card key is lowercase `w01`, `w02`, ... (the title-form key required by SeqAddr). `W01` in older examples is a historical label, not the new canonical key.
- `NN` already means a counter (`05.NN`), so `#NN` inside a counter reads as two counters.
- `#NN` is also used for jobs released in talk (`#03 >run`, `claude/readpath.md`).
- `CC` clashes with C for compute in the lead letters (`3CM`).
- `w` distinguishes work cards from face counters. Use a heading `## w01` so the normalized key is precisely `w01`; place the description in a `title:` field, not in the heading. A work card is a SeqAddr card with `type: work`.

Each work card:

```text
## w01
type: work
title: build the lead command
axioms: 5.4
placed: 2026-10-22
reason: From a recorded, resolvable predecessor card (full SeqAddr reference required in the live pack).
recommend: In jobs.py, add a command that takes Did, Blocked, and Need and writes them as three lines before the first work card on a return. It refuses a counter that is not a return. Stamp the change. Keep the older copy.
path: 10.workshop/10.10.work/10.10.10.lib/code/jobs.py
risk: 2
lead: 3C
ask: >build Add the lead command.
```

- `reason` is the why (axiom 4). A work card with no reason fails lint.
- **(approved S02, S10)** Use `risk` for the initial 1–5 impact scale; evidence must be proportional to likely harm, reversibility, and scope. A low-risk documentation correction may need a diff and lint; a governing change requires a recorded N7 independent trial and broader verification. **(proposed detail)** Risk levels 4–5 also require N7. `7`: the calibrated risk rubric and any mandatory thresholds beyond governing changes.
- `lead` only when it differs from the pack's.
- `axioms` optional, and encouraged: it is the quick why for the builder.

## 6. The loop

axioms: 5.6.9

Tails move one step at a time, and the compute enforces them (seqAddr section 4):

```
draft -> pack -> open -> return -> review -> closed

`closed` is the **bare** `FF.NN` counter (no `.closed` tail). Its separately recorded `outcome` may be `passed`, `failed`, `blocked`, `needs-authority`, or `abandoned` **(approved S03)**.
```

| Step | Tail | Who | What happens | axioms |
|---|---|---|---|---|
| 1 Write | `draft` | lead | writes the pack and its work cards | 5 |
| 2 Lint | `draft -> pack` | compute | checks the pack against its template (section 8). A pack that fails stays `draft` | 3C |
| 3 Claim | `pack -> open` | builder via compute | atomic first valid claim wins; record owner, claim ID, start, and recovery terms **(approved S11)** | 1.3.6 |
| 4 Work | `open` | builder | completes each work card. Asks questions; applies for permission or solutions to what blocks it; stops at `stop if` | 5.1 |
| 5 Return | `open -> return` | builder via compute | appends the return to the **same counter** with per-card results and inspectable evidence; lint checks shape and recorded grant **(approved S02)** | 5.6 |
| 6 Review | `return -> review` | independent reviewer | inspects actual artifacts/evidence; N7 is mandatory for governing changes **(approved S10)** | 9 |
| 7 Close | `review -> bare counter` | compute, on recorded review/outcome | preserves `passed`, `failed`, `blocked`, `needs-authority`, or `abandoned` without rewriting previous events **(approved S03)** | 6.7 |
| 8 Lead pass | | lead | reads, notes, elevates, decides the next pack (section 7) | 6.4 |

### 6.1 The return lives on the counter (filled)

The original says the builder "makes a copy calling it 05.NN.return". In the book format nothing is copied: the builder moves the counter's tail to `return` and appends the return body. The pack text stays in the log as the earlier entry, readable and never rewritten (axiom 6). This settles where a return lives.

### 6.2 Return shape

axioms: 5.6.9

- Per work card: `w01` with `result: done | blocked | need`; list exact changed file paths or full SeqAddr addresses and **inspectable evidence** (test command/output, diff, commit, or other relevant proof). Record deviations and their why **(approved S02)**.
- Evidence is proportional to risk; compute validates presence and references, while an independent reviewer assesses whether it actually proves the claim. Tests failing must be disclosed, not rebranded as success.
- Then: questions, permission asked, solutions proposed to what blocked it.
- Then, at the end, each with its why: **notes**, **unprompted** (one thing the builder would have done differently), **overflow** (what was seen outside the frame, reported and not acted on).

### 6.3 Review (filled)

axioms: 9.1

- The reviewer is a view other than the builder: the lead, a person, or a cold model in N7. The builder never reviews its own return.
- It checks the return against the pack's acceptance criteria, every target against the approved grant, and the actual evidence against claims; it tries to break the result.
- **(approved S10)** A reviewer must not be the builder. For significant risk, the cold reviewer starts from the approved criteria and artifact before seeing the builder's persuasive summary. Governing changes always require a recorded N7 lab trial before promotion.
- **(approved S03)** `blocked` means a prerequisite is absent; `needs-authority` means the next step exceeds the grant; `failed` means acceptance criteria were attempted but unmet. These are separate from an abandoned claim.
- **A failed review does not reopen the counter.** It closes with outcome `failed`, and the rework is a new counter linked `continues-from` (proposed by Fable from the old kernel). The record of what failed stays.

### 6.4 Open while the builder is gone (filled)

**(approved S11)** A claim records claim ID, owner, start, last checkpoint/heartbeat if available, and a recovery policy. Compute must not assume a worker is dead from silence alone. On an authorized stale determination, it records evidence, stops further writes under the old claim, elevates, and closes it `abandoned` only after the recovery rule is met. Replacement work gets a **new** counter with explicit `continues-from` and a fresh authorization check. `7`: timeout/heartbeat and lease policy, including offline builders and how to fence a returning stale worker.

## 7. The lead's pass

axioms: 6.4.1

Each pass, before writing a new pack, the lead:

1. **Reads N4 01 and 04,** the notes on N4 face 06, and the reviewed return. Every pass. (Director) The read is pinned to the active approved N4 revision, not whatever content happens to be newest **(approved S01)**.
2. **Writes a note** to N4 Face 06: what the return taught, what changed, why, and an explicit link to its N5 return. Note counters need not mirror job counters **(approved S12)**.
3. **Elevates changes to 01 and 04.** When they need updating, the lead does not change them. It elevates with suggested changes, as a draft, and the person approves (axioms 1 and 9; drafting).
4. **Separates three outcomes (approved S04):** (a) individual pack passed review, (b) the accumulated MVP satisfies approved acceptance criteria, and (c) an authorized promotion may occur. The lead recommends completion; compute checks objective evidence and delegation; the person decides any matter reserved by the approval. If unfinished and permitted, the lead writes a focused next pack.
5. **(approved S06)** Before each cold builder handoff, compute derives a read-only manifest from the live records: approved N4 revision and grant, pack counter, predecessor return(s), current source commits/revisions, unresolved blockers, required faces/cards, acceptance criteria, and stop conditions. A manifest is a **view**, not a new authority; it identifies exact source links and is regenerated when stale.

## 8. Pack lint

axioms: 2.3C.8

The compute holds the template for the shape a model must produce: a pack, a work card, and a return. The template lives in the kernel as card types (decision C8.9), so every book inherits it and a band may override it only by name (axiom 2). This is what `0117.pack-lint` was.

**(filled)** What the lint checks:

| Check | On | Kind |
|---|---|---|
| header has `by`, `authorized`, `outcome`, `overview`, `stop if`, `grant`, `frame`, `risk` | pack | hard: stays `draft` |
| `authorized` resolves to an approved, specific N4 revision; grant and promotion delegation cover the requested operation **(S01, S04)** | pack | hard |
| every `wNN` card has `type: work`, `title`, `reason`, declared target intent, and `ask` **(S07, S08)** | pack | hard |
| every actual write target is inside the authorized grant and scope; the right to create is validated against allowed address/path range **(S08)** | pack, return | hard |
| **existing dependency** must open; **modify target** must exist and be writable; **create target** must be legal and available, not already present **(S08)** | pack | hard, with `7.8` for required missing dependencies |
| `axioms:` chains parse | pack, card | hard |
| every work card has a result (`done`, `blocked`, `need`) plus touched targets; `done` supplies proportional inspectable evidence **(S02)** | return | hard: stays `open` |
| every address the return touched is inside the grant | return | hard |
| notes, unprompted and overflow present (may be empty, with a why) | return | finding |
| each return has a reviewer distinct from builder; mandatory N7 trial exists for governing changes **(S10)** | promotion | hard |
| claim and expected revision remain valid; stale claims cannot write **(S01, S11)** | transitions | hard |
| material N4 design updates do not reuse old approval without a renewed grant **(S01)** | pack, promotion | hard |
| a work card with no `axioms:` line | pack | finding |

Hard checks refuse the tail move with a reason. Findings are recorded for review.

## 9. Gravity: how many passes

axioms: 5.4.1

The number of passes is an aim, not a quota. 1-3 passes is normal. Models left alone loop on one detail, so there are hard move-on points.

**(approved S09)** Compute counts passes under one **approved N4 work-frame/MVP ID**, not all counters on a page or every task performed by a particular lead. Count independently the consecutive attempts against the same unresolved blocker. A person's answer resets the gravity sequence only when it explicitly changes or reauthorizes that frame; an unrelated conversation does not reset it. Retain historic counts in lineage.

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

**(approved S09)** Compute records a possible loop when two passes repeat the same target, request, and unchanged evidence; matching `path` and `ask` alone is a finding, not proof of wasted work. The next pass must cite new evidence, a changed hypothesis/method, or explicit authorization.

## 10. Decisions still requiring definition (`7`)

The Director approved S01–S12 and the following choices: delegated promotion *inside* approved N4 scope; risk-proportional evidence; risk-based N7 trials with **mandatory N7 for governing changes**; lowercase `w01` card keys. These are agreed directions, not proof of an implemented mechanism.

- `7` **Risk rubric:** calibrate levels 1–5 and whether levels 4–5 automatically require N7. Mandatory N7 for governing changes is already approved.
- `7` **Claim recovery:** lease/heartbeat duration, offline work, claim fencing, and who confirms abandonment.
- `7` **Approval compatibility:** which kinds of N4 edits are material, exact revision-token representation, and how approval spans a changed source commit.
- `7` **Promotion target:** the record that declares the MVP complete and how delegated promotion interacts with page-type restrictions.
- `7` **Continuation allocation:** exact permissible free-band selection and subject set link migration in SeqAddr; do not invent a target.
- `7` **Evidence policy:** minimal trusted evidence by work type and risk; verify source and claims rather than treating model text as proof.
- `7` **Cross-book transactions:** when a pack writes reciprocal Face 08 links in separate physical books, require coordinated commit or a blocked/escalated operation.
- `7` **Versioned governance:** update decision A2.6 and relevant kernel lint schema using their authorized drafting/review procedure; do not silently replace them.

---

## 11. Strike/update reconciliation — retained for Director review

These struck phrases are the superseded `.001` claims. The governing replacement appears in the numbered sections above; the original `.001` file remains unchanged.

| Superseded `.001` position | `.002` disposition |
|---|---|
| ~~The person approves the N4 page~~ (unversioned) | **S01:** approves a specific revision, frame, and grant |
| ~~`W01` as work-card key~~ | **S07:** `w01` in a `## w01` heading |
| ~~Every address in the pack opens~~ | **S08:** distinguish existing, modifying, and creation targets |
| ~~Return says `done`~~ as adequate proof | **S02:** evidence is required in proportion to risk |
| ~~Closed outcome: passed or failed~~ | **S03:** also blocked, needs-authority, abandoned |
| ~~If the MVP is complete, the loop ends~~ (single unspecified event) | **S04:** distinguish pack acceptance, MVP completion, promotion |
| ~~`1401` binds to `1501`~~ as a continuation | **S05:** band counterparts are not continuation links |
| ~~N4 and N5 counter numbers might mirror~~ as identity | **S12:** separate boards, linked by explicit references |
| ~~Pass count by one lead since person last spoke~~ | **S09:** count per approved frame and repeated blocker |
| ~~A different reviewer is sufficient~~ | **S10:** independent evidence review, mandatory N7 for governing changes |
| ~~A silent `open` task is abandoned~~ | **S11:** documented claim/recovery policy and fenced replacement |

`S06` adds a computed handoff manifest; it does not replace an earlier literal sentence. The next review should decide which `7` items require design now and which remain implementation experiments.
