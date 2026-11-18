# Director walkthrough — law 0001 v005 and 0002 v004 (prepared by Colab for Prime)
date: 2026-11-02 · prepared by: claude-opus-5-5, **the author of both candidates; not a cold review** · Prime assesses, recommends and presents · template: kernel-update-review v2, stage 03

**Candidates:**
- `0001.law` v005: `design05.02/candidates/0001.law.01.005.candidate.md`, sha256 f46ae1cd…;
- `0002.schema` v004: `design05.03/candidates/0002.schema.01.004.candidate.md`, sha256 d16f05b2….

**Direction is approved; these exact bytes are not.** Labels:
- **[S]** a settled Director direction; please confirm the text is consistent with it;
- **[O]** an actual open Director judgment;
- **[T]** a technical prerequisite;
- **[P]** a discrepancy for Prime to investigate.

"COLAB recommendation" is my author view, for Prime to assess. **Every Director answer below is UNANSWERED.** Coverage and anchors are in `PRESERVATION-MAP.md`.

## #01 — Face 01: templates no longer have to be shorter than the rule [S] + finding [P]
**Current (0001 seat, Correspondence):** "Face 02 is present where a compact form is shorter than the rule."

**Proposed (0001 v005):**
> Face 02 is present where a declared working form serves a job. A card is shorter than the rule it carries. A template is complete enough to build its artifact, and a schema to check one; neither is held to shortness.

**Change and why:** you called the shortness limit a mistake that had to be fixed (06.02 #01). Shortness now applies to cards only. Use and Construction say "working forms" to match.

**Example:**
- **Success:** a pack template longer than its rule is lawful because it builds the pack.
- **Failure:** a "card" that is longer than its rule and only paraphrases it is still a defect.

**Finding F-1 [P]:** 0001 v005 predates the payload model. A face 02 whose only job is controlling attached payloads (#05) has no presence sentence here. **Proposal:** the successor 0001 adds "or controls attached payloads". The syntax axioms' "The card is face 02" and "Face 02 is the snippet" read as shelf-local; Prime should confirm (D-1).

**COLAB recommendation:** confirm, and accept a successor 0001 that fixes F-1.

**Director answer:** UNANSWERED

## #02 — A conflict between a form and the law goes to you; the affected act waits [S]
**Current:** 0001 seat says only "A disagreement is recorded for authority review, not settled by majority vote." (kept).

**Proposed (0001 v005):**
> A form never amends its rule. A conflict between a form and its rule goes to the Director, and the affected act waits.

**Proposed (0002 v004, Agreement):**
> A conflict between a form and its governing source goes to the Director. Intelligence names and explains the conflict. It does not choose which source to follow, amend the source, or waive a check. The act that depends on the form waits for the answer.

**Change and why:** your 06.02 #02 ("we can't just let intelligence choose which source it wants to follow").

**Example:**
- **Success:** a template that requires "risk ≤ 2 before release" (a rule the law lacks) is held and reported to you; the build of that one pack waits.
- **Failure:** the model quietly drops the field, or follows the template.

**COLAB recommendation:** confirm. Only the dependent act waits, not unrelated work.

**Director answer:** UNANSWERED

## #03 — Several named forms per subject, chosen from the menu [S]
**Current (0002 seat):** "Face 02 supplies a compact form … a card, template, or schema …"; "These forms are named separately rather than treating every box as interchangeable."

**Proposed (0002 v004, Forms):**
> One face 02 section may hold several forms of its subject. Each form declares its name, kind, purpose, governing source section, and revision.

> Work selects a form by its name. A profile or other selector is lawful when its declared mapping names the section, the form, and the revision. Do not select by kind alone, by the newest file, or by guess.

**Change and why:** your 06.02 #03 ("different pieces that a model can request from the menu"). The form name is a label inside the section, **not a new address axis**.

**Example:**
- **Success:** the menu offers `pack-card`, `pack-create`, `pack-revise` and `pack-check`, and a request names `pack-create`.
- **Failure:** "the template for Pack" is refused, because there are two templates.

**COLAB recommendation:** confirm.

**Director answer:** UNANSWERED

## #04 — Required fields name their grounds; unknowns stay unknown [O]
**Proposed (0002 v004, Requirements):**
> A form requirement has two parts, and each names its ground. The meaning part says what must be present, allowed, or done. Its ground is the governing face 01 section, or a recorded task grant that applies to the work. The representation part says how that meaning is written: a field, a type, an order, a count, or an encoding. Its ground is the form's own declaration.

**Proposed (0002 v004, Fields):**
> The answers are: not supplied, null, empty, a value, and not applicable. A field declares only the answers it needs and how each is written; a required text may accept only a value. An empty answer keeps its field's shape.

**Change and why:** this is **new law**, not wording. It stops a form from adding rules unnoticed (#02). It also prevents the pilot failures (prose in a yes/no field, and an unknown test turning into "passed"). Your 06.02 #06 asked for the examples to be fixed, but **this grounds rule itself was proposed by Colab and Prime, not decided by you.**

**Example:**
- **Success:** `tests_passed` given "no, it does not" is refused at that field, with help.
- **Failure:** a field `budget` marked required with no ground is accepted silently.

**Choice:** adopt the two-part grounds rule and the per-field answers as kernel law, or keep them as guidance for forms only.

**COLAB recommendation:** adopt. It is the smallest rule that makes "a form adds no conditions" checkable.

**Director answer:** UNANSWERED

## #05 — `02.filename.VVV.filetype` payloads attached to their face 02; no permission to run [S]
**Proposed (0002 v004, Payload):**
> A payload is a file named `02.NAME.VVV.TYPE`: the face tag, a name, the payload's revision, and its type.

> The tag, the type, and a declared invocation grant no permission to run.

**Change and why:** your 06.03 #02 and #05 ("a payload with a 02 face attached to it"; metadata "attached to the system"; "preserve the naming conventions"). The attachment, kept with the face, records the owner, location, selected revision and bytes, the form served, dependencies, invocation and outputs. **No companion file per script.**

**Example:**
- **Success:** two pages each hold `02.check.001.py`; each is found through its own face (fixture A1–A2).
- **Failure:** a bare filename search is ambiguous and is refused (A3).

**Note:** no 0018 amendment. "For now it is a .md file" keeps payload files out of the face scan (Prime 06.03 review concurred).

**COLAB recommendation:** confirm.

**Director answer:** UNANSWERED

## #06 — Work stays bound to the revision it selected [S]
**Proposed (0002 v004, Binding):**
> A newer draft does not replace a selected revision, and a version number does not make one revision superior to another.

> In this development phase, a changed binding, conflicting applicability, or a proposed replacement of stable governing work goes to the Director.

**Change and why:** your 06.02 #04 ("most of our work should be old and very stable. Changing that shouldn't be easy").

**Example:**
- **Success:** a pack bound to `pack-create` 001 keeps using 001 while a draft 002 exists.
- **Failure:** a tool silently switches to 002 because its number is higher.

**COLAB recommendation:** confirm.

**Director answer:** UNANSWERED

## #07 — Building is reviewable, and review is not approval [S]
**Proposed (0002 v004, Construction):**
> A review binds the candidate it judged. When recording the review changes the artifact, the candidate and the final artifact each keep their own identity.

> Building, checking, and review do not sign, approve, seat, lock, or release.

**Change and why:** your 06.02 #06 and #07, and Prime's 0526 A1 finding: review against an inspected hash failed because adding the review changed the document. This applies to templates only. Cards and schemas do not build.

**Example:**
- **Success:** Prime reviews draft X; the published file X+review has its own identity, and both are kept.
- **Failure:** a green build is reported as approved.

**COLAB recommendation:** confirm.

**Director answer:** UNANSWERED

## #08 — Lifecycle, warehouse layout and the missing tool [O] + [T]
**The sequence** (law 0021/0022/0060/0023): the model requests signing → compute checks → **you approve the exact signed bytes** → compute seats, retiring the old face into this book's `00.retire.09` in the same act → lock and promotion separately.

**[O] Warehouse layout (U1).** Law 0009 says only "Move that file into this book's `00.retire.09`".
- **Proposal:** one folder per originating page inside it (`00.retire.09/0001.law/01.004.09.md`, `00.retire.09/0002.schema/01.003.09.md`), plus a `09.md` statement and an append-only ledger.
- **Consequence:** a flat folder collides when two pages retire the same `01.004.09.md` (fixture L10). **This is a proposal, not 0009 text.**

**[T] Technical prerequisites, not decisions for you:**
- **no seating tool exists;** the simulator is evidence only;
- Prime's 06.04 conditions:
  - the plan is bound to its page, release and approval, checked on every run;
  - the rollback decision is revalidated on every resume;
  - writes are counted by state;
  - two narrow write roots (the book and the work evidence);
  - `version` and `who` stay fixed;
- a cold review of the exact final cut before approval (0411/06.04).

**Example:**
- **Success:** both faces seat; a restart re-verifies the hashes.
- **Failure:** a swapped plan from another page reports "verified" (Prime's P1). The tool must hold instead.

**COLAB recommendation:** approve the page-folder layout as the U1 choice. Treat the rest as Prime's build prerequisites.

**Director answer:** UNANSWERED
