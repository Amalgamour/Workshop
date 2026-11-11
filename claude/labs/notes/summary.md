# Labs summary: do the axioms change a model's output?

by: claude-opus-5-5
date: 2026-11-10
why: one page to check the lab results against the axioms, axiom by axiom.

## What was run

| Lab | Work | Conditions | Runs |
|---|---|---|---|
| 01 | tool library: loan period 7 to 14 days | A none, B full Axioms.md | 6 (Sonnet x3 each) |
| 02 | community garden: 2027 season, new site, plot allocation | A none, B full, C packed cards only | 12 (Sonnet and Haiku x2 each), plus 4 chain probes |
| 03 | rowing club: the trial of all nine, one trap each | A none, C cards + cites, D cards without cites | 12, plus 4 chain probes |

## Lab 03 in short (the trial of all nine)

- Passes: **A 25, C 30, D 27 of 36.** All nine faced a trap; none broke.
- Five traps hit the ceiling (authority raised, rule placed once, no invented reasons, river-level step kept, self-approval refused by every run).
- Where the axioms decided it: halting on the live South conflict before acting (A 0/4, with axioms 4/8), spotting North's override with no authorization (only two runs, both with axioms), keeping a blank as unknown, and handing the list to compute.
- **Leads needs its cite.** Compute was named only where `3CM` was cited, in all three labs. The card alone (condition D) never did it.
- **The `7.8` / `8.7` line passed.** All four cold readers agreed with it; in lab 02 they had split.

Every run was a fresh model with only its pack. Rubrics were written before the runs; loan dates and allocations were checked by script.

## Short answer

Yes, in the direction you expected, with a small sample.

- Lab 02 passes: **A 16, B 21, C 24 of 32**. The packed cards alone (C) did at least as well as the full text (B).
- The weaker model (Haiku) gains most. Without axioms it rewrote a past record, closed a gap by renumbering, and broke inheritance. With either form, it did none of these.
- Lab 01 hit a ceiling: the traps were signposted, and Sonnet passed them without help. That told us what lab 02 had to change.

## Axiom by axiom

| Axiom | What changed with the axioms | Evidence | Proposal (for the Director, not applied) |
|---|---|---|---|
| 1 Authority | Language of the order: "live record", "raise to whoever holds more". Outcomes the same as without. **Did not fire** on a conflict that had resolved by coincidence ($40 + 5 = the $45 already on the copy). | 01 B2; 02 T1 | Test a conflict still live after the change (lab 03). Consider: "agreement now does not prove they were connected". |
| 2 Fractal | **Clearest gain.** Difference-only pages, inherited items left unrepeated, overrides named and approved. Without it, two runs turned inherited answers into "to be confirmed" gaps, and one rewrote the parent's scope. | 02 T2: pure pages A 0/4, B 1/4, C 2/4 | Keep. Lab 01 B3 shows 2 must sit beside 5: "write only the difference" is for new writing, not permission to restructure what exists. |
| 3 Leads | **Clear gain.** Only runs with the axioms said compute should lead and asked for a re-run of hand work. No A run did, in either lab. | 01 B1, B2; 02 b.s.2, c.s.1, c.s.2 | Face 04: say that C means the compute (a tool or system), not "compute carefully". One run in lab 01 misread it. |
| 4 Why | Same outcome without: no model invented a reason, even under a deadline. **The mark changed**: `Why: 7 (4.7)` written in the page, which compute can find. | 01 all; 02 T4 12/12 | No change. The value is the mark and the habit, not a rescue. |
| 5 Frame | Returns split into "observed, not acted on". Outcomes mostly the same; one A run removed what it should have reported. | 01 B2; 02 a.h.1 | No change. |
| 6 Lineage | **Gain for the weaker model.** Three Haiku runs rewrote a past changelog entry; none with the packed cards did. Runs with the axioms wrote what changed, why, and what governs. | 02 T6 | No change. |
| 7 Missing | Same outcome on inventing; **gain on marking and on not closing gaps by structure.** Every B and C run put `## 5 [7] Missing` in the page. An A run renumbered the sections so the gap disappeared. | 02 T7, a.h.1; 01 A1 invented a rule | Face 04: add "closing a gap by renumbering, merging or rewording is filling it." |
| 8, 9 | Not scrubbed; not tested. | | |

## Chain grammar (from the probe)

- Cold readers treat order as meaningful: first is the lens, later numbers refine it. This holds without being told.
- `4.7` and `7.8` were both read as intended. `8.7` split two ways.
- A cold Haiku found the open question unprompted: is `7` placed before or after what is missing?
- **Decision needed:** `7` always last (`8.7` replaces `7.8`), or `7` first means "missing, of this kind" and `7` last means "this thing is incomplete". Details in `02.md`.

## Limits

- Two or three runs per cell. A single flipped trap moves a cell.
- I wrote the packs and scored them; the rubric was fixed first, but scoring is not blind.
- Only Claude models. Other families are the real test: hand them `packs/02.a.md`, `02.b.md`, `02.c.md`.
- The cites on job items act as hints as well as packed concepts; a condition with the axioms but no cites would separate the two.
- Some traps still hit the ceiling (lab 02: T4, T8).

## Next lab (04), if wanted

1. A model from another family on packs 02 and 03.
2. Harder traps for the five ceilings, or a weaker model where they would separate.
3. Test whether Leads fires from a pack-level `3C` default, as a band head would set it, instead of a cite on each item.

## Lab 03 plan, as it was (kept for the record)

1. A live conflict that stays live after the change (axiom 1).
2. Axioms with no cites on the items, to separate the concept from the hint.
3. A non-Claude model on the same packs.
4. A longer task where the frame matters more: several steps, with tempting work just outside.
