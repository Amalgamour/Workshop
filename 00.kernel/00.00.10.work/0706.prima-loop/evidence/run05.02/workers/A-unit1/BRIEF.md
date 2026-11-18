# Worker A, unit 1: cold audit of N7 source-kind grammar and intake preservation
Read ../COMMON.md first; it applies in full.

## Purpose
Independently audit the frozen, accepted N7 intake repair, looking for meaningful counterexamples. This is not a full app run.

## Read, in the source room (/workspace/prima/run0502/source-room)
1. Start with these:
   - labs/n7-intake-compat-pass02/n7compat2.py (plus its tests/ and compat17/)
   - 00.kernel/00.00.10.work/0707.app-use-check/evidence/design05.17/CONTRACT.md
   - 00.kernel/00.00.10.work/0707.app-use-check/evidence/design05.17/proposal/workbook-review-pass04.workbook.py.proposal
2. Then, as needed:
   - labs/workbook-review-pass03, pass02 and pass01
   - the other design05.17 evidence files

## Focus
- Ambiguous declarations.
- Duplicate or contradictory forms.
- Measured source-kind propagation and reset.
- N5 equivalence (see labs/n7-intake-compat-pass02/n5_replay.py).
- Path and source identity.
- Whether evidence stays attached to the right pass.

## Already known (not new)
K1, the old punctuation refusal, is already fixed. Don't report it as new; find additional counterexamples, or report what you could actually establish.

## Limits
Don't claim full app execution on this host.
