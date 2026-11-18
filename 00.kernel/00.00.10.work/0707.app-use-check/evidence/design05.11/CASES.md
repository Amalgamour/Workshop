# Independent acceptance cases, revised — 0707/05.11
who: claude-opus-5-5 (Claude), Colab design/labs · state: design. **Every target assertion (39) is NOT RUN.** It supersedes `design05.10/CASES.md` (preserved). Machine form: `index.json`. Binding: `BINDING-CHECKLIST.md`. Changes: `CORRECTIONS.md`.

Sources: the frozen contract prefix (C-line numbers), 0412/01, 06.06, 06.07, the Director agreement, and **06.10.review (Prime's technical interpretation, not Director words).** I did not read the target API, its return or its tests.

## State model (06.10 corr. 3)
Five states, each reported separately:
- **J** judgment recorded;
- **P** publication complete;
- **C** custody complete;
- **W** work complete;
- **R** action released.

A preliminary publication can be current while W and R stay false.

## Cases
- **A — thin N5NN intake, preliminary judgment.** `0599.fixture-review/05.01`.
  - **A-base:** a valid manifest built at binding.
  - A-digest: the null digest kept. A-missing: the submission deleted. A-ambiguous: two named files.
  - **Assertions A1–A11:**
    - evidence beyond the submission; null digest as a finding;
    - **no custody, receipt or association**; exact new-process read;
    - **T3 prose preserved and never summarized as passed**; W and R false; sources unchanged;
    - **compute-derived candidate and final identities; an echo allowed, a fabrication refused**;
    - finding dispositions kept;
    - missing or ambiguous return is a finding, with no guess.
- **B — N7NN same-pass successor.** `0799.fixture-colab/05.01`.
  - **B-tool:** a first review recorded **by the tool** (director-input, Q1, D1), the SYNTHETIC Director decision, then the successor for the **same pass**.
  - **B-manual:** the hand-written 06.01 is preserved or blocks; never adopted.
  - **Assertions B1–B6:**
    - a successor in the same pass's review home, with no new numbering; predecessor kept; current selected;
    - Director words verbatim and separate;
    - **D1 not released by "continue"**;
    - I1 never held; nothing executed.
- **C — drift (PRIMARY HOSTILE).**
  - C-a: a Scope edit. C-b: a T3-row edit. Both stale, with the judgment kept, the edit not reverted, and **the stale state surviving recovery.**
  - **C-c:** the tool's own pointer write is **not** stale: P is true and C, W, R are false; the diff is limited to the Review area.
  - **C-d:** an unselected notes file is not automatically drift.
- **D — blocked by manual Review-area text.**
  - **The manual text is preserved and not adopted.**
  - The exact judgment, next action and holds are recovered from the durable record.
  - **P is false, and is reported so.**
  - A removed render does not change the judgment.
- **E — interruption and false completion (PRIMARY HOSTILE).**
  - E-a: a supported stop between render and pointer, otherwise NOT BINDABLE. Partial before recovery; then **either** complete after verification **or** hold with a supported retry.
  - **E-b and E-c:** a changed render or pointer is **never reported complete** and never silently overwritten.
- **F — replay and typing.**
  - F-a: no duplicate authoritative result (diagnostics allowed). F-b: a conflict refused, the original intact.
  - F-c: wrong type on a field the **returned form declares**.
  - F-d: a required field omitted → refused.
  - **F-e:** a declared nullable unknown stays unknown, never passed.

## Primary hostile cases
- **E-b catches recovery that trusts a done label.**
- **C-a together with C-c catches whole-page hashing.** It either breaks the tool's own pointer write, or, "fixed" by exclusion, misses a real edit.

## Prime interpretations used (06.10; not Director words)
- **B:** "continue selects the review and next bounded action; it does not release D1 merely by recording."
- **C:** "freeze selected source/dependency/decision/template bytes. A new unselected notes file is not automatically drift."
- **F:** "Missing required typed fields refuse; declared nullable unknowns remain explicit unknown."

## Limits
**Not specified:**
- the same address in another book instance;
- refusal of a finding without a disposition (it depends on the returned form);
- the 0412 per-operation report floor;
- the filed mode (it needs a line-tool fixture at binding).
