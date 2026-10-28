# STATE-PROPOSAL — desk and lane current state (0507.prime-support 05.11)

Author: claude-opus-5-5, Colab. Date: 2026-10-27. Source commit: 4cca1d2e9ac845e82a2d44df432f8f7f6584f1e5. Live HEAD at claim: dc90fe1.

**Status of this document.** This is a design proposal. Nothing here is seated, installed or decided. Proposed paths are marked *(proposed)*. Choices that need authority are listed as DEC-n, owned by the Director or Prime. Routine details are proposed concretely, so no one is asked about naming. The worked cases are in `worked-cases.json`. Each case is marked `actual` (a commit blob, or a live observation labelled as such) or `synthetic`.

## 0. The problem in one paragraph

A fresh reader today meets three current-state signals that disagree:
- the desk record `0401.goal/06.01.md` (v1, 3578934…), which says 0504/05.06 is accepted;
- the batch headers, which use at least three conventions (older 0502 and 0503 pages add "packed" forms; six header forms across 50 pages):
  - 0504 headers say `state: returned`;
  - 0508 headers say `released by the Director …; claimed by …`;
  - every 0507 header, plus 0506/05.03, 05.05 and 05.06 and 0504/05.03, says `draft; awaiting Director release`, with `Release: PENDING` in all but 0504/05.03, because executors may only append below the Return pointer;
- the Return pointer and Review sections, which carry the real release, claim, return and review.

The rehearsal (0131) and Prime's judgement (prime-review05.10) confirmed this. The cause is structural. One hand-maintained record tries to name "the" current work for a desk running four parallel lanes. And headers are asked to carry execution facts that their writers are forbidden to update.

## 1. Model: three record classes, one direction of flow

| Class | Written by | Changes | Examples (existing) | Rule |
|---|---|---|---|---|
| **A. Decision and event records** | the actor who made the decision or did the act | append-only; never rewritten | a Director release quoted on the batch Return pointer; the Claim line; a capture member `01NN` (receipt); a Prime Review section plus `evidence/prime-reviewNN/review.md`; a publication commit at the remote ref | the only source of truth for what happened |
| **B. Coordination records** | Director, or Prime as the Director's recorder (DEC-1) | rarely; dated | `0401.goal/06.01.md` (desk); the registry's lane list (tool input) | says what the desk is aiming at and which lanes exist, never which batch is "current" |
| **C. Derived projection** | compute, read-only | recomputed on demand | none yet *(proposed: `state-projection/1`)* | computed from A and B; never hand-edited; never written into source pages |

The flow runs A and B into C, and never the other way. A projection may report that a class-A record is missing, stale or conflicting. It never writes, repairs or invents one.

## 2. D1 — desk goal versus lane assignment

**What stays canonical at desk scope** (class B, hand-written): desk, book, workflow space, focus (the finish line now pursued), the active lane list, and desk-level waits and next. That is the information no batch page holds.

**What moves to lane scope, as derived data and not a new hand file:** each lane's current batch and its state. Every fact the v1 record tried to hold (`current_work`, `pack`, `assignment_state`, `waits_on`, `next`) already exists as a class-A record on that lane's batch pages and reviews. A second hand-written copy is exactly what went stale.

**Lane-local selection rule** (compute):
- A batch is **open** when it has a recorded release and its review facet is `none` or `pending`.
- A batch is **closed** when its review facet is `text` or `bound`, that is, when the Review section is no longer PENDING. Compute does not read the disposition out of prose. The disposition is quoted verbatim, whether it is accepted, held or returned for correction. When a held review names a follow-up draft, that follow-up is read from the review's own pointer text. It is not computed.
- The lane's current view is:
  - `open` if exactly one batch is open, listing it;
  - `open-multiple` if more than one is open, listing all of them, as attention, never choosing one;
  - `idle` if none is open, showing the latest closed batch and its review's own next-action pointer, plus any drafts with no release, as `awaiting-release`.
- An unreleased draft is never current. The newest page number is never current just by being newest. The last builder to return is never current just by returning.

**Schema reuse.**
- The per-lane derived view is expressed with the existing v1 key set (0410 `assignment-record`), so existing readers understand it:

  | Field | Value |
  |---|---|
  | `current_work` | the open batch, or `none` |
  | `pack` | that batch path |
  | `assignment_state` | derived and mapped onto the v1 enum: released → `released`, claimed with no return → `running`, captured with no review → `returned`. For a closed batch: `accepted` or `stopped` only from a bound review's machine `reviewed_disposition` (DEC-3). For a text-only review it stays `returned`, with `waits_on: disposition is review text; read it`. Compute never upgrades prose to `accepted`. |
  | `waits_on` | the next missing class-A record |
  | `next` | the review's own pointer, verbatim |

- This is a **generated view** with the same keys, not a new hand-written source.
- No new axis, no seqaddr change and no global role.

**Desk record migration** (proposed; DEC-1, DEC-2):
1. Draft `0401.goal/06.01.002.md` *(proposed name, from the face-version rule)*, schema `desk-coordination` version 2. Keys:
   - `record: desk-coordination`, `schema: …0410.imports/01.md#desk-coordination version 2` *(proposed anchor; 0410 is not edited in this pass)*;
   - `desk`, `book`, `workflow_space`, `focus`;
   - `lanes`: lane page folders joined by ` + `;
   - `waits_on`, `next`, `updated`.
   There is no `current_work` key.
2. v1 (`06.01.md`, 3578934…) stays seated and unchanged until the Director seats v2. Then it is retired under the law-0018 retire name. That is the Director's act; this proposal does not choose the name.
3. **Compatibility with fixed pins.** prime_support 700d60d2… parses only v1 `canonical_assignment`. A v2 record named there would be reported as a conflict ("missing or not a v1 assignment record"). So while migrating, registries omit the optional `canonical_assignment` key, which is a supported shape, and the projection carries the desk record. The prime_support, prime_boot and inspector pins stay unchanged. Nothing selects a higher version.
4. **Rollback.** The Director does not seat v2, and v1 stays. Nothing else depends on v2.

**Tension to record, not resolve (DEC-2).** Law 0010 says "Face 06 is a note. It does not govern." The desk record has lived on a face-06 file since Pack B. Moving it is a law or structure decision. This proposal keeps the home for continuity and names the tension.

## 3. D2 — document state is not execution state

A batch has six independent facets. The projection reports each facet separately, and also gives a summary.

| Facet | Values | Read from (class A or header) | Notes |
|---|---|---|---|
| document | `draft` or `seated`, plus legacy text verbatim | header `state:` | Proposed meaning going forward: document status only. Legacy execution words in headers (`returned`, `released by …`, `packed …`) are shown verbatim as `header-legacy` and never used for execution. |
| release | `none`, `recorded`, `conflict` | the Return pointer `Release:` line (the Director's words quoted); otherwise a non-PENDING Assignment `Release:` line (legacy 0504 and 0508 forms) | compute checks the line exists; it never infers a release from a claim or a capture |
| claim | `none`, `recorded` | the Return pointer `Claim:` line, or the legacy Assignment `Claim:` | actor text verbatim (§4) |
| return | `none`, `pointer-only`, `captured`, `custody-problem`, `pointer-missing` | the primary member chosen by **origin page and batch** from the pinned inspector, plus the pointer text | custody only |
| review | `none`, `pending`, `text`, `bound`, `stale-candidate` | the page Review section; a review record (§5) | a quoted "Accepted" sentence is `text`, never `bound` |
| publication | `unknown`, `at-ref` | the review text present at the published remote ref (Git object) | a fact about bytes, not approval |

**Summary state** (derived): `draft`, `released`, `claimed`, `returned`, `captured`, `reviewed:<disposition-verbatim>`, `published`. It is the furthest facet reached by a consistent chain, plus attention items.

**Precedence and escalation.** These apply only between records of different reliability. Between two decision records, compute never decides.
1. **Release.** A Return pointer `Release:` beats an Assignment `Release: PENDING`, because the pointer is the later, append-only record. This is reported as a `stale-duplicate` notice, not a conflict.
2. **Missing release.** A claim, a capture or a review with no recorded release anywhere is reported as a `conflict: execution without recorded release`, and escalated to Prime. Compute never writes or assumes a release.
3. **Pointer versus custody.**
   - The pointer names member M, but M is not `complete`: `custody-problem`.
   - A complete member whose origin is this page and batch exists, but the pointer is PENDING: `pointer-missing`. This is an interrupted pointer append. It is shown; it is not repaired.
4. **Review versus return.** A review bound to receipt R, while the current primary member's receipt differs: `stale-candidate`, escalated as "re-review needed".
5. **Header versus facets.** A header that disagrees with the facets is a `stale-duplicate` notice. The header never wins.
6. **Two decision-level sources contradict** (for example, two Release quotes with different scope): `conflict`, escalated to the Director. There is no automatic winner.

**Future pack headers** (proposal, DEC-4; existing pages are never rewritten):
- `state:` carries document status only (`draft`, then `seated` when the Director seats the page).
- The Assignment block names the Executor and the Reviewer. In place of `Release: PENDING. Claim: PENDING.` it says `Release and claim: recorded in the Return pointer.`
- Execution words never appear in the header.

This matches the existing executor rule: executors append below the Return pointer and never edit above it.

## 4. D3 — actor, role, session and per-batch assignment

| Reference | Home (existing) | Meaning | Not |
|---|---|---|---|
| role | `0408.seats/01.md`: Director, Prime (Codex), Colab (Claude) | a standing seat with its law page | not created by a batch |
| executor label | the batch `Executor:` line, e.g. "Grok Builder 1" | the actor named for that batch only (0408: "A pack may name an executor without filling the Builder seat") | not a seat; needs no 0408 row |
| actor and session | the batch `Claim:` line, e.g. "Grok 4.7 (xAI), session 01a179…" or "claude-opus-5-5 (Anthropic), Colab" | who actually ran the batch | not authentication |
| author | header `who:` | who wrote the document | not the executor; never relabelled |

The projection records `executor_label` and `claim_actor` verbatim side by side. It does not map labels to seats.

**Stale context** is a seat or record that describes a past scope. The 0408 Builder cell scoped to 0504/05.01 is an example. It is history, and it is not a gap.

**A real grant gap** is one of:
- a claim with no recorded release;
- a claim by an actor the batch does not name and the Director did not release;
- an actor taking a seat decision (approve, accept, seat, publish) without that seat.

The first is mechanical. The others are text that Prime checks. No new standing seat, and no actor decision, is made here.

## 5. D4 — handoff contract between records and the projection

The projection never parses page prose. It consumes one observation per batch page from the return-shape reader that Grok-2's corpus (0508/05.12) is preparing. That corpus is not yet returned (Release PENDING at 4cca1d2 and live). So this contract is **provisional**, and maps onto the corpus's planned field families: source identity, actual observation, evidenced facts, proposed behaviour, unresolved decisions.

`batch-observation/1` *(proposed)*, one per page:

```text
source:      {path, commit, sha256, bytes}                      ← corpus "source identity"
parser:      {tool, sha256, status, reason, revision_id|null}   ← corpus "actual observation" (prime_support verbatim)
document:    {header_state_raw}
assignment:  {executor_raw, release_raw, claim_raw}             (raw lines or null)
return:      {kind: absent|pending|present|ambiguous, lines_raw[], release_raw, claim_raw, execution_raw,
              members: [{name, role: primary-claimed|secondary|quoted|proposed|fenced}]}
review:      {kind: absent|pending|text|ambiguous, text_raw, record_path|null,
              bound: null|{member, receipt_sha256, disposition_raw, reviewer, record_sha256}}
ambiguity:   [strings]                                          ← corpus "unresolved decisions"
```

The corpus's "proposed behaviour" field is not consumed. It informs the reader slice, not the projection.

Projection duties on that input:
- **Primary member.** The primary member is confirmed only by the pinned inspector (947915fe…), as status `complete` with origin page and batch equal to this batch. A reader's `primary-claimed` label is a hint, not proof. *Actual case:* 0508/05.10 names 0128 first, but 0128's origin is 0509/05.01 (retrospective); the batch's own return is 0129. 0508/05.11 is the same, with 0132 and 0133.
- **Ambiguity.** `kind: ambiguous` means unknown. It is never absent and never present. prime_support reports "ambiguous heading" on most 0507 pages, so its `revision_id` is unavailable there. Batch identity then uses the whole-page sha at the read commit, with the parser observation kept verbatim.
- **Review binding.** A review is `bound` only when it names a member and a receipt sha that the projection can check against the inspector. Every existing review is `text`, with a pointer to its review record. That is correct; it is not an error. New reviews may add a small block to become bound (DEC-3, Prime's choice):
  - `reviewed_member:`;
  - `reviewed_receipt_sha256:`;
  - `reviewed_disposition:`, one of `accepted`, `held` or `returned-for-correction`.

  The prose disposition stays authoritative text. The machine field is Prime's own declaration, never compute's reading.
- **Live versus commit.** Observations carry a commit, or `live`, and are never mixed. A live complete member does not make a commit-time page "returned".
- **Fixed-pin migration.** The new reader and the projection are new pinned tools. Existing pins are unchanged. Consumers switch only by an explicit pin change, never by version discovery.

## 6. Decisions this proposal needs (not assumed)

| # | Owner | Decision |
|---|---|---|
| DEC-1 | Director | Adopt desk-coordination v2 at `0401.goal` (draft `06.01.002.md`), and say who records it: proposed Prime, when publishing a release or review. |
| DEC-2 | Director | Keep the desk record on face 06 despite law 0010 ("does not govern"), or move it (a structure decision). |
| DEC-3 | Prime | Add a machine-checkable review binding to new reviews (`reviewed_member`, `reviewed_receipt_sha256`, `reviewed_disposition`). |
| DEC-4 | Prime with the Director | The future header convention (§3). Old pages are never rewritten. |
| DEC-5 | Director | The active lane list for the desk record. Proposed from the records: 0504.app-entry, 0506.clerk-handoff, 0507.prime-support, 0508.return-capture. Activity is a decision, not inferred. |

## 7. Recommended first implementation slice (one; not a code pack yet)

**`labs/state-projection-pass01/`** *(proposed)*: a fixture-only projection over explicit observations.

- **Module boundaries.**
  - `state_projection.py` reads a fixed list of `batch-observation/1` JSON files, a desk record (v1 or v2 key form), and the pinned inspector for named members.
  - It writes one `state-projection/1` JSON and a text view, to stdout or an external records root only.
  - It does not read pages, does not import or modify prime_support or prime_boot, and does not write to the book.
- **Pins.** return_inspect 947915fe…, with its sibling return_capture 8f3da5c6…, hash-checked before launch.
- **Tests.** One fixture per worked case W1-W7, plus:
  - stale-duplicate is reported and is not a conflict;
  - execution without a release escalates;
  - a quoted "Accepted" is never bound;
  - ambiguous stays unknown;
  - the primary member is chosen by origin, not pointer order;
  - live and commit facets stay separate;
  - `open-multiple` never picks one;
  - no class-A or class-B record is written;
  - the source and pin bytes are unchanged.
- **Dependency.** The observation format is joint with Grok-2's reader slice. Fixture observations are used until Prime accepts the corpus's input contract. If the corpus diverges, the projection adapts its input mapping; prime_support is not edited.
- **Migration and rollback.** Lab only. Nothing is seated or registered. Rollback is to stop using it.
- **Acceptance.**
  - Every W case projects exactly as `worked-cases.json` expects.
  - No invented release, review or primary.
  - Exit codes separate a clean run, attention items and a refusal.
  - Prime's independent run matches.

## 8. Limits

- A design over a fixed commit, plus explicitly labelled live observations.
- The return-reader behaviour is Grok-2's corpus's to establish; nothing here parses prose.
- Compute checks presence, links and hashes. It never grades semantics, accepts, releases or seats.
- A complete receipt is custody. A published review is a separate record.
