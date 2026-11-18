# Prime review - 0705.prime-desk-check
date: 2026-11-01
who: Codex Prime

Disposition: independent checker lab accepted with explicit evidence limits;
actual desk acceptance remains not-run.

All 56 frozen inputs match; 28 artifact rows and return/manifest pointer hashes
match. Two live work pages changed because builders returned; frozen inputs remain
the experiment's source. Prime ran the unmodified 20 self-tests on Windows Python
3.12.14 with a new explicit report destination: 20 passed in 25.510s. Original
transcripts were not overwritten. This validates the checker/self-test behavior,
not the actual desk. 54 assertions, 16 executable cases and 24 manual checklist
items remain candidate-not-run until raw output is connected.

The lab correctly distinguishes synthetic data, adapter-not-connected, missing or
unsupported fields and pending human assessment. Synthetic positives generated
from expectations are circular as Claude discloses; negative tests are valuable,
but do not independently prove those expectations. Producer/adapter/manual actor
labels are supplied metadata, not authentication. A forged local label can exercise
verdict logic; it cannot prove real candidate execution.

Review-stage checks on candidate data must preserve raw output bytes/hashes,
exact tool/request/fixture identities, invocation/exit and explicit field mappings.
The adapter must never calculate expected selected work from the fixture and then
present it as the candidate's result. It may build requests, not invent observations.
Unmapped fields remain unsupported. Subset contains checks can overlook conflicting
extra facts, so explicit duplicate/conflict assertions or manual checks must catch
contradictory output; don't claim all forbidden inferences are mechanically proven.
The manual checklist is for Prime to complete based on inspection, not to be
populated with invented yes answers. An overall not-passed can mean incomplete
coverage, not necessarily a product defect; show these distinctly.

PD-01 found on the actual Grok-1 return is precisely the kind of gap this lab should
now expose. The next bounded Colab should connect a pinned pass01 baseline first,
retain the failing evidence, and allow a future explicitly pinned successor rerun.
No reading an evolving candidate or modifying product code. No need to rewrite the
oracle to match a failing product. Proposed 05.03.pack is held for Director review.
