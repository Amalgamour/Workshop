# Workflow loop

state: draft — Director review required; not live
copy of: [root `.002` draft](workflow-loop.md)
revision: `.003`, 2026-11-11
revision-authority: Director authorized drafting `.003`. [Decision record F.1](decisions.md#f1-approval-record-for-s01s12) records the S01–S12 directions. Review and trial of `.003` remain due (`9`).
axioms: 5.3.6
why: how work loops from a design to a build and back, so a model can run passes without history and a person can check every step.

How to read this draft:
- `axioms:` lines are the quick why. Each section cites the axioms it rests on; open `Axioms.md` for the reason.
- **(filled)** marks prior `.001` additions retained as context.
- **(approved Sxx)** marks decisions approved for `.002` by the Director; implementation remains a draft until this full document is reviewed.
- **(proposed detail)** marks one possible implementation of an approved solution, not a newly approved governing law.
- `7` marks a detail still missing or needing authority.
- See [`.003` drafting notes](workflow-loop.003-notes.md) for the change record and read-back. The [`.002` notes](workflow-loop.002-notes.md) preserve earlier lineage.

---

## 1. Roles

axioms: 1.3

| Role | Who | Does | Does not |
|---|---|---|---|
| Person | the Director, or whoever holds the level | approves a specific N4 revision, its frame and delegation; authorizes governing changes; answers elevations | delegation cannot exceed their own authority |
| Lead | a model, once the N4 page is approved; or a person | reads N4, writes packs, reads returns, runs passes, drafts changes to 01/04 | change 01 or 04 without approval |
| Builder | a model, a person, or compute | claims a pack, does its work cards, writes the return | write outside the pack's grant |
| Reviewer | a view other than the builder **(approved S10)** | independently checks evidence against acceptance criteria; challenges assumptions; uses N7 for required higher-risk trials | review its own work; accept the builder's summary as proof |
| Compute | the compute | resolves approved revisions, enforces grants on its own writes, verifies external changes, creates handoffs, lints records, moves tails, counts passes, records claims | decide a disputed question or infer an approval |

A lead is not authority (axiom 3). The lead works inside what the approved N4 page grants (axiom 1).

## 2. Band design

axioms: 2.6

The workflow map defaults within the standard range `0100–0999` (A2.7, SeqAddr §6.1). `N4` means the dev role. In the default map it is `0400–0499`. A user band in `1000–9998` adopts a workflow role by name in its band definition. `1000` is the first user band head.

| Band | Name | Holds |
|---|---|---|
| `0000–0099` | existing kernel allocation | separate from the workflow map |
| `0100–0299` | unassigned by this workflow | follows governing band definitions |
| `0300–0399` (N3) | build | modules built, with explanation. Face 01: what the module is. Face 02: the module's files described (section 3.1). Face 08: links to the files in the repo |
| `0400–0499` (N4) | dev | the design: what the work is, its MVP, goals, what we are trying to prove. Person and model talk here. Face 04 mostly, with 01 to go with it |
| `0500–0599` (N5) | jobs | packs and returns, as face 05 counters |
| `0600–0699` | unassigned by this workflow | follows governing band definitions |
| `0700–0799` (N7) | colab | labs: cold-model trials of the page's work |
| `0800–0999` | unassigned by this workflow | follows governing band definitions |

`N?00` denotes a hundred-page band head, such as `0400` or the user band `1500`. Ordinary subject work starts at `N?01`. The notation explains the existing SeqAddr grammar.

**S05, F02–F03.** The proposed [F.2 amendment](decisions.md#f2-a26-amendment-for-workflow-sets) records the map and the change to A2.6. `7`: reconcile the affected A2.6 and A6.1 wording and inherited schemas through their own drafting path before enabling the amended rules.

## 3. Bound bands

axioms: 2.6.8

- A matching two-digit subject number helps find counterparts. Example: design `0401.timer`, packs and returns `0501.timer`, build `0301.timer`, labs `0701.timer`.
- Under proposed F.2, membership requires reciprocal Face 08 links (axiom 8). This amends A2.6's current membership by number.
- **(filled)** The compute checks the set: a set page that is named but cannot be opened is `7.8`, raised, never created from a lookalike.
- **(filled)** Lineage runs through the set: from a build back to its pack, from the pack back to the design, from the design back to its approval (axiom 6).
- **S05.** Overflow follows SeqAddr §7.1. The `PP99` pointer names the next allocated hundred for the same role and has explicit Face 08 forward and back-links. Follow the pointer's recorded target.
- If a continuation changes subject numbering, record its predecessor and set membership explicitly. The original identities remain immutable. `7`: the `continues-from` link kind remains proposed under C4/E9.

### 3.1 Code lives in the repo, linked

axioms: 8.6

Decided by the Director (2026-11-11): code lives in the repo, not in the book.

- The N3 page describes the module: face 01 what it is, face 02 its files, what each does and its interface.
- Face 08 links each file by its repo path. A work card's `path` is the same repo path.
- **(filled)** Each link records the commit it was last checked at, so the build page's lineage can be followed in the repo's history (axiom 6).
- **(approved S02)** The return cites exact changed paths and Git commit or working-tree revision plus verification evidence. A claimed change without inspectable evidence is not accepted merely because the builder reported `done`.
- **(filled)** The compute checks that each linked path exists. A path that cannot be opened is `7.8`, raised, never repointed to a similar file.
- **(filled)** The book keeps the why; the repo keeps the code. If the code rots, the why on N4 and N3 is enough to rebuild it.

**F08.** For Compute-owned writes, Compute checks authority and scope before executing, then verifies and records the result. For external Git or filesystem writes, Compute validates declared targets before work and verifies actual changes against the pack's recorded baseline afterward. Compare additions, modifications, removals, renames and untracked files within the verification workspace. Record pre-existing changes with the baseline. Use both sides of a rename when checking the grant.

If a change falls outside the grant or its attribution is uncertain, preserve the evidence, report the finding and block acceptance and promotion pending authorized remediation. The return can still record what happened. `7`: define a reliable workspace boundary and attribution policy. A shared diff shows differences, and concurrent writers can make their origin ambiguous. An isolated worktree or exclusive workspace is a candidate for the first implementation.

## 4. The N4 page and its approval

axioms: 1.4.5

- N4 states the work: the MVP for this page, the goals, what we are trying to prove. Written on face 04, with an agents.md-style face 01 to go with it.
- **(approved S01)** The person approves **one identified N4 revision** with its acceptance criteria, permitted scope, approving authority, and delegation terms. Approval is a lineage record with a stable identifier, not a mutable flag on the page.
- **(approved S04)** Within the explicitly approved N4 scope, the lead may direct passes and authorize routine completion and promotion **only to the extent delegated**. Promotion still requires independent trial and compute checks. Governing changes, changed acceptance criteria, expanded grants, or material changes outside the approved frame require elevation and fresh approval.
- A pack links to the exact approval record and N4 base revision. Compute refuses an unrelated, stale, or insufficient grant; it does not guess whether a later N4 edit was approved.
- The recorded grant supplies the workflow's explicit operation scope. Altering law, changing Face 01/04, or expanding the frame follows the applicable authority and drafting rules. Check `1.7.8` before each write. `7`: the general E8 definition of written permission remains open.
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
| `lead` | explicit lead letters unless a recorded band default applies. `7`: no `3MC` workflow default is seated. | 3 |
| `axioms` | the chain for the whole pack **(filled)** | |
| `outcome` | what done looks like | 5 |
| `overview` | what the work is trying to achieve; matches N4 01 and 04 | 5.2 |
| `stop if` | where the builder stops and raises **(filled)** | 5.1 |
| `grant` | explicit allowed operations and target addresses/path patterns, bounded by the approval **(approved S01, S08)** | 1 |
| `frame` | approved MVP/work-frame ID for gravity accounting **(approved S09)** | 5.6 |
| `risk` | lead's proposed risk. Compute records its floor and the effective risk (§5.3). | 5.9 |
| `predecessor` | previous pack or issue and expected artifact revisions, if any **(approved S06)** | 6.8 |
| repository baseline | starting source revision and pre-existing workspace changes for external work (§3.1). `7`: exact record format. | 5.6 |

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
reason: A person needs one place to inspect what the builder completed and what still blocks the job.
recommend: In jobs.py, add a command that takes Did, Blocked, and Need and writes them as three lines before the first work card on a return. It refuses a counter that is not a return. Stamp the change. Keep the older copy.
path: 10.workshop/10.10.work/10.10.10.lib/code/jobs.py
risk: 2
lead: 3C
ask: >build Add the lead command.
```

- `reason` states why the work is needed (axiom 4). A work card with no reason fails lint. When the reason depends on prior work, cite the exact predecessor revision or full SeqAddr reference. The example is illustrative.
- **(approved S02, S10)** Evidence is proportional to likely harm, reversibility and scope. A low-risk documentation correction may need a diff and lint. A governing change requires a recorded independent N7 trial before promotion. The initial 1–5 scale and a level 4–5 cutoff remain candidates under §5.3.
- `lead` only when it differs from the pack's.
- `axioms` optional, and encouraged: it is the quick why for the builder.

### 5.3 Risk and governing targets

**F06–F07.** Compute derives a floor from the registered target type, operation, grant and authority metadata. The effective risk is the higher of that floor and the lead's proposal. Record the inputs and reason so a reviewer can reproduce the decision.

A governing change edits a registered governing target or declares a change to governing behavior. Targets include the Axioms, SeqAddr grammar, kernel contracts, type definitions, authority, inheritance and workflow lifecycle rules. A source-code change can affect the same behavior. An unknown target or disputed behavioral impact is raised for classification before routine delegation can be used. Governing changes require Director or applicable governing authority approval and a recorded N7 trial before promotion.

`7`: the target registry, risk rubric, routine eligibility and N7 thresholds beyond governing changes. Until those are defined, the lead's rating alone cannot establish review or promotion eligibility.

## 6. The loop

axioms: 5.6.9

The N5 `05.00` board shows each job counter `05.NN` as one Kanban card (A4.4). Its current tail determines its column. The counter keeps the same identity throughout. The lead, builder and reviewer complete their work on that card, and Compute records each handoff in its history before showing the card in the next column. The board derives its current view from that history.

```
draft -> pack -> open -> return -> review -> closed
```

`closed` is the board label for the **bare** `05.NN` counter. Its separately recorded `outcome` may be `passed`, `failed`, `blocked`, `needs-authority`, or `abandoned` **(approved S03)**.

| Step | Tail | Who | What happens | axioms |
|---|---|---|---|---|
| 1 Write | `draft` | lead | writes the pack and its work cards | 5 |
| 2 Lint | `draft -> pack` | compute | checks the pack against its template (section 8). A pack that fails stays `draft` | 3C |
| 3 Claim | `pack -> open` | builder via compute | atomic first valid claim wins. Record owner, claim ID, start and recovery terms. Record the E4 raise before work if the builder differs from the lead. | 1.3.6 |
| 4 Work | `open` | builder | completes each work card. Asks questions; applies for permission or solutions to what blocks it; stops at `stop if` | 5.1 |
| 5 Return | `open -> return` | builder via Compute, or Compute during authorized recovery | records the return with per-card results or verified recovery facts and the evidence available | 5.6 |
| 6 Review | `return -> review` | Compute on a valid reviewer claim | records reviewer identity, the exact return revision and review scope. While the card is in `review`, the reviewer checks the artifacts and evidence and records the finding and outcome. | 9 |
| 7 Close | `review -> bare counter` | Compute | moves the card to Closed once the review and its outcome are recorded. The card retains the history of every stage. | 6.7 |
| 8 Lead pass | | lead | reads, notes, elevates, decides the next pack (section 7) | 6.4 |

### 6.1 Return placement and recording

The `.003` workflow draft uses the E9 proposal to append the return to the same counter as the pack. The earlier pack body remains in the log. `7`: seat the E9 placement and specify how the return body and `open -> return` become visible as one durable change or recover to a consistent state after interruption.

Compute records a structurally valid return from a current claim even when the record shows missing proof, a failure, a blocker or a grant violation. Review uses those findings to decide the outcome. A malformed or stale submission cannot advance the tail. Preserve the reason for refusal and use the authorized recovery path if the claim can no longer produce a valid return.

### 6.2 Return shape

axioms: 5.6.9

- Per work card: `w01` with `result: done | blocked | need`; list exact changed file paths or full SeqAddr addresses and **inspectable evidence** (test command/output, diff, commit, or other relevant proof). Record deviations and their why **(approved S02)**.
- Evidence is proportional to risk; compute validates presence and references, while an independent reviewer assesses whether it actually proves the claim. Tests failing must be disclosed, not rebranded as success.
- A `blocked` card supplies the missing prerequisite. A `need` card identifies the operation and authority needed. Use these to support `blocked` and `needs-authority` outcomes, respectively. If blockers and missing authority coexist, record all of them and the why for the outcome selected. `7`: decide whether mixed outcomes require a deterministic precedence rule.
- Then: questions, permission asked, solutions proposed to what blocked it.
- Then, at the end, each with its why: **notes**, **unprompted** (one thing the builder would have done differently), **overflow** (what was seen outside the frame, reported and not acted on).

### 6.3 Review (filled)

axioms: 9.1

- **S10, F09.** Record reviewer identity and context, what they saw first, the checks and hostile attempts they performed, and the evidence and finding for each. The builder is ineligible to review its own return. Compare actual artifacts and changes against the approved criteria and grant. For a replacement, open the predecessor read-only (E7).
- Proposed review classes: R1 uses a separate reviewer for routine work. R2 uses fresh context and opens approved criteria and the artifact before the builder's conclusions. R3 adds a recorded hostile N7 trial for governing work, with a reviewer separate from both builder and pack author. Governing changes require N7 before promotion. `7`: settle the identity evidence, when a same-model session counts under E7, and risk thresholds beyond governing changes. Every promotion still requires the E7 trial.
- **S03.** `passed` requires satisfied pack criteria and resolved violations. `blocked` records a missing prerequisite. `needs-authority` records a next step outside the grant. `failed` records unmet criteria or rejected evidence or scope. `abandoned` requires the verified recovery record in §6.4. Record the outcome and why on the transition to the bare counter.
- A failed review closes the counter. Rework gets a new counter and an explicit predecessor reference. `7`: the formal `continues-from` link kind remains proposed (C4/E9).

### 6.4 Open while the builder is gone (filled)

**S11, F04.** A claim records its ID, owner, start, last checkpoint or heartbeat if available, and recovery policy. Silence alone leaves the claim unresolved. After the required authority records an abandonment decision, Compute fences the old claim and records a system return on the same counter. Include the reason, last verified checkpoint, observed changes, unverified changes and outstanding work. Attribute only facts supported by evidence. The system return proceeds through `review` before closing with outcome `abandoned`. Replacement work uses a new counter, an explicit predecessor reference and a fresh authorization check.

`7`: define who may confirm abandonment, timeout and offline policies, and the fencing mechanism. Fencing can reject the old claim in Compute. For external writes, separately protect the replacement workspace from late changes by the original builder.

## 7. The lead's pass

axioms: 6.4.1

Each pass, before writing a new pack, the lead:

1. **Reads N4 01 and 04,** the notes on N4 face 06, and the reviewed return. Every pass. (Director) The read is pinned to the active approved N4 revision, not whatever content happens to be newest **(approved S01)**.
2. **Writes a note** to N4 Face 06: what the return taught, what changed, why, and an explicit link to its N5 return. Note counters need not mirror job counters **(approved S12)**.
3. **Elevates changes to 01 and 04.** When they need updating, the lead does not change them. It elevates with suggested changes, as a draft, and the person approves (axioms 1 and 9; drafting).
4. **Separates three outcomes (approved S04):** (a) individual pack passed review, (b) the accumulated MVP satisfies approved acceptance criteria, and (c) an authorized promotion may occur. The lead recommends completion; compute checks objective evidence and delegation; the person decides any matter reserved by the approval. If unfinished and permitted, the lead writes a focused next pack.
5. **(approved S06)** Before each cold builder handoff, compute derives a read-only manifest from the live records: approved N4 revision and grant, pack counter, predecessor return(s), current source commits/revisions, unresolved blockers, required faces/cards, acceptance criteria, and stop conditions. A manifest is a **view**, not a new authority; it identifies exact source links and is regenerated when stale.

### 7.1 Promotion manifest

**F10.** A promotion manifest names the exact artifact revisions eligible for publication. It records the pack and reviewed return revision, N4 revision, frame and approval, exact source revisions and SeqAddr records, the review evidence and required trial, exclusions and unresolved findings, and the promotion authorization. It also identifies the expected live predecessors. A handoff manifest supplies builder inputs under S06.

Before publishing, Compute checks that the manifest scope is covered by the recorded authorization and that the artifact and predecessor revisions still match. A changed artifact must be reviewed at its new revision. `7`: specify how validation and publication share a revision guard, and how a mixed Git and book promotion recovers from partial publication. Hold mixed-store promotion until that contract is defined.

## 8. Pack lint

axioms: 2.3C.8

Compute uses templates for packs, work cards and returns. This draft proposes kernel-owned card types under C8.9. Any permitted specialization needs a named override under axiom 2. `7`: seat the workflow card types and templates through the kernel's drafting path. Consult the predecessor `0117.pack-lint`.

**(filled)** What the lint checks:

| Check | On | Kind |
|---|---|---|
| header has `by`, `authorized`, `outcome`, `overview`, `stop if`, `grant`, `frame`, `risk` | pack | hard: stays `draft` |
| `authorized` resolves to an approved, specific N4 revision and the grant covers the requested work. Verify promotion delegation when promotion is requested. | pack, promotion | hard |
| every `wNN` card has `type: work`, `title`, `reason`, declared target intent, and `ask` **(S07, S08)** | pack | hard |
| intended targets and operations are inside the grant; Compute-owned writes are checked before execution; actual external changes are checked against the baseline **(S08, F08)** | pack, write, review | hard before controlled writes and before acceptance. Violations remain recordable. |
| **existing dependency** must open; **modify target** must exist and be writable; **create target** must be legal and available, not already present **(S08)** | pack | hard, with `7.8` for required missing dependencies |
| `axioms:` chains parse | pack, card | hard |
| a builder return records each work-card result and its touched targets or explicitly identifies what is unknown. Review checks `done` against proportional evidence. Recovery returns follow §6.4. | return, review | hard for malformed return shape. Missing proof or out-of-grant changes block acceptance. |
| notes, unprompted and overflow present (may be empty, with a why) | return | finding |
| reviewer identity is recorded and distinct from builder | review | hard before claiming review |
| the E7 trial, mandatory N7 for governing changes, and artifact-specific authorization resolve | promotion | hard before publication |
| claim and expected revision remain valid; stale claims cannot write **(S01, S11)** | transitions | hard |
| material N4 design updates do not reuse old approval without a renewed grant **(S01)** | pack, promotion | hard |
| a work card with no `axioms:` line | pack | finding |

Record the reason for a refused transition or acceptance. Preserve findings in the return and review so a refusal remains inspectable.

## 9. Gravity: how many passes

axioms: 5.4.1

The number of passes is an aim, not a quota. 1-3 passes is normal. Models left alone loop on one detail, so there are hard move-on points.

**S09, F05.** Compute counts passes under the approved N4 frame and independently tracks repeated attempts against an unresolved blocker. Changing lead, counter or blocker label does not reset the frame count. Proposed counting event: each successful `draft -> pack` release consumes one pass exactly once. `7`: specify how release and accounting commit together and how blocker identity survives revision and relabeling.

| Next pass in the frame's current allowance | What happens before release |
|---|---|
| 1-3 | normal |
| 4 | Compute requires the why questions. The lead answers and Compute records the answers as an N4 06 note. |
| 5 | Keep the pass-4 requirement. The lead records new evidence or a changed method against the earlier answers. |
| 6 | Halt before release. Raise the named frame, blocker history, and recorded answers to the authority. |

A decision responding to the recorded halt can continue the frame for a stated allowance, revise the frame with fresh approval, delegate within a stated scope and allowance, or stop. Proposed default: a reply such as “carry on” tied to the halt and given by the authority for that frame grants one additional release when it specifies no count. Continued releases carry the pass-5 check. Halt again when the allowance is exhausted. Unrelated conversation leaves the halt in force. Retain the previous counts and reasons in lineage. `7`: confirm the default allowance and restart policy.

**(filled)** The why questions:

1. Why does this need another pass? (4)
2. What did the last return change, in one sentence? (6)
3. Is the frame the right size, and does it let the work finish? (5)
4. Is the remaining gap worth its cost, in proportion to being wrong? (4)
5. Is this the same detail as the last pass? If so, why will this pass differ? (9)
6. What is missing that only the person can give? (7.1)

**(approved S09)** Compute records a possible loop when two passes repeat the same target, request, and unchanged evidence. Matching `path` and `ask` alone is a finding. The next pass must cite new evidence, a changed hypothesis or method, or explicit authorization. The pass-5 check and any continuation checks still apply.

## 10. Decisions still requiring definition (`7`)

The Director approved S01–S12 and the following choices: delegated promotion *inside* approved N4 scope; risk-proportional evidence; risk-based N7 trials with **mandatory N7 for governing changes**; lowercase `w01` card keys. These are agreed directions, not proof of an implemented mechanism.

- `7` **Risk and review:** target registry, calibrated levels, routine eligibility, any N7 threshold beyond governing changes, E7 reviewer identity, and reviewer reassignment after interruption.
- `7` **Claim and return recovery:** lease/heartbeat duration, offline work, claim fencing, abandonment authority, durable return transition, and mixed outcome precedence.
- `7` **Approval compatibility:** which kinds of N4 edits are material, exact revision-token representation, and how approval spans a changed source commit.
- `7` **Promotion mechanics:** the MVP completion record, page-type restrictions, revision guards and mixed-store reconciliation.
- `7` **Continuation allocation:** exact permissible free-band selection and subject set link migration in SeqAddr; do not invent a target.
- `7` **Evidence policy:** minimal trusted evidence by work type and risk; verify source and claims rather than treating model text as proof.
- `7` **Cross-book transactions:** when a pack writes reciprocal Face 08 links in separate physical books, require coordinated commit or a blocked/escalated operation.
- `7` **Versioned governance:** seat F.2 through A2.6/A6.1 and align the kernel lint schema, plus the E8 and E9 dependencies named above. When revising the proposed read path, distinguish the lead's `pack` from Compute's handoff manifest.
- `7` **External verification and gravity:** define the workspace attribution boundary and durable accounting for releases, blockers and continuations.
- `9` **Trial:** hostile review of this draft and the scenarios in [`.003` notes](workflow-loop.003-notes.md#review-cases).

---

## 11. Strike/update reconciliation

The [`.003` notes](workflow-loop.003-notes.md) track changes from `.002`. The following table preserves the `.001` to `.002` dispositions as history.

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

`S06` added a computed handoff manifest in `.002`. Section 7.1 records the promotion manifest proposed in `.003`.
