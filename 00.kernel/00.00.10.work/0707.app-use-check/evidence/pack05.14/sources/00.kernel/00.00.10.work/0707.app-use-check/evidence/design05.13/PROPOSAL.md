# Source-bound task agreement — proposal (0707/05.13)
who: claude-opus-5-5 (Claude), Colab design · state: **PROPOSAL.** Not enacted. No kernel rule. It works under the existing 0412 development agreement. Machine form: `task-agreement.declaration.json`.

## Problem (measured)
The first real core review (0707/05.12) recorded, published and recovered a judgment while all six of `agreement.goal`, `scope`, `prime_discretion`, `director_required`, `finish_criteria` and `recorded_decisions` were **unknown**. The core looks for a "selected source-heading format", and real packs do not have it (0522/05.13 has `Goal / method`, `#01–#03`, `Outputs / boundaries`). **Compute must retrieve the agreement (the form lists it as `not_submitted`), but nothing tells it where.**

## Proposal in one paragraph
Each new pack carries **one fenced `task-agreement` block before `## Return pointer`,** so the block is part of the frozen pack cut. For each field, the block **names exact source cuts:**
- a heading in the pack itself;
- a heading in a standing record (0412/01, the director agreement);
- or a heading in a decision record.

**Compute** measures each cut at intake (it resolves exactly once; sha256; bytes) and stores the binding **in the existing intake record**. **Intelligence** chooses the cuts. Compute checks shape, identity and pairing, never meaning. **There is no companion file and no second ledger.** Old packs without the block are reported as `absent`, never back-filled.

## Fields (all required now except `gloss`)
| Field | Cites | Allowed states |
|---|---|---|
| goal | a pack heading | cited, unknown |
| scope | pack heading(s): included, excluded, allowed writes | cited, unknown, conflict, stale |
| finish_criteria | a pack heading | cited, unknown, not-applicable (with a reason) |
| prime_discretion | standing 0412/01 "Local work agreement" (+ an optional pack narrowing) | cited, unknown, stale |
| director_required | standing director agreement (+ any pack stop line) | cited, unknown, stale |
| recorded_decisions | a list of decision bindings, or `none-recorded` | cited, none-recorded, unknown, stale, conflict |
| gloss (optional) | Prime's interpretation text | labelled interpretation; **never authority** |

Prime discretion and Director-required are cheap: they usually cite the two **standing** records, which already exist (0412/01; director agreement).

## Decision binding (Director text kept separate)
A decision binding names:
- the record;
- its **verbatim cut** (for example `## Director - verbatim`);
- a **different** interpretation cut (`## Prime - exact proposal this reply approves`, or `## Prime - interpretation`);
- the **answers cut** (the proposal or question being answered);
- `answers_scope: only the cited proposal`.

**"Ok pack it" is bound to the proposal it answered and to nothing wider.** A reply resolves only its own question; other holds remain. The Director text stays in its record, and the binding only points at it by cut and sha256.

## What compute does and does not do
- **It does:**
  - resolve each cut exactly once;
  - measure the sha256;
  - check that the verbatim and interpretation cuts differ and that the answers cut resolves;
  - keep bindings in the intake record;
  - re-measure on read, giving `stale` if the bytes changed;
  - **apply the holds table** (declaration `holds`): an unknown or stale field blocks only the acts that depend on it.
- **It does not:**
  - choose a source by newest file, keyword or heading guess;
  - authenticate a person from a heading, label, Boolean or "yes";
  - decide that a cited sentence semantically authorizes an act;
  - rebind silently;
  - fill an unknown to turn a form green.

## Revisions and stale decisions
- **A binding is immutable.** A revised pack is a new pass or a new reviewed cut, with a new binding. **The old one stays as history.**
- **A changed bound cut** gives `stale`. The original binding and its hash are kept. A **reconciliation request** names the stale binding, the bound and observed hashes, and a proposed cut.
- Prime reviews a task-cut change. **A changed Director verbatim record is itself a conflict and goes to the Director.**
- **A refused or stale binding is not a rejected idea.**

## Necessary now versus optional
- **Necessary now:** the block (new packs only); the six fields with states; the decision binding; storage in the intake binding; the holds.
- **Optional:** `gloss`; dedicated `## Scope` and `## Finish` headings. These make cuts cleaner, but existing headings such as `Deliverables / boundaries` can be cited.
- **Not proposed:** grammar growth; a companion file per artifact; a migration of old packs; a new permission rank.

## True Director decisions versus technical choices
- **Director decisions this design relies on (already recorded):**
  - 0412 director agreement (routine continues; hard stop on judgment or forks);
  - 0412/06.06 (compute assigns the form);
  - 0412/06.08 "Ok pack it" for this design.
- **It does NOT rely on:** the proposed 0002 Requirements rule (0710 #04, UNANSWERED).
- **Technical choices (Prime's):**
  - the block lives in the pack;
  - the pack cut ends before `## Return pointer`;
  - heading cuts are exact-once;
  - the holds table content.
- **A possible Director fork, only if Prime wants it:** whether a pack *must* carry the block before release (a release-gate rule). **I propose that it stays reporting-only** (absent = unknown, with holds) until real use shows it is needed.
