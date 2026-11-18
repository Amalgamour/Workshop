# Prima usage reserve - Director instruction
date: 2026-11-01
state: active operating instruction; not a metered quota enforcement tool
source: 00.kernel/00.00.10.work/0422.prima/06.02.md

## Reserve
Keep AT LEAST 5% of the relevant shared Grok allowance available for basic bot work.
The reserve belongs to the account's ongoing work, not separately to each worker.
All other account activity can consume that pool too. Never treat a stale reading
or a per-worker figure as guaranteed spendable balance. Five percent is a floor,
not permission to launch a job whose cost could cross it.

## Check and report
Read the provider's actual usage meter when available: at startup, before each new
assignment or worker launch, at meaningful long-run checkpoints, on completion,
and during the already scheduled two-hour check. Do not create extra polling.
Record observation time with offset, source (provider-observed or Director/Prime-
supplied), exact pool/window, remaining percent, reported reset time and uncertainty.
If the display reports used percent, preserve that value and label the derived
remaining percent. Do not mix weekly, short-window or paid-credit meters.
Report all applicable limiting pools separately; do not invent a reset date.
Usage inaccessible is UNKNOWN, never zero cost or full allowance.

Before substantial or overnight work, estimate a conservative upper usage bound
from observed comparable runs where possible and allow for concurrent bots. Start
only if the bound leaves the 5% reserve plus justified uncertainty headroom. An
estimate is not a hard cap. If no adequate meter or bound is available, report the
gap and request a current reading or explicit bounded budget from Prime before
starting substantial unattended/delegated work. Do not enable paid overages.

## Stop and resume
At or below 5%, or when the next work cannot reasonably preserve it: launch no new
workers or substantial jobs. Ask current workers to checkpoint and return retained
evidence at a safe boundary rather than discarding work or repeatedly relaunching.
Report a usage hold to Prime with the latest evidence and reset information.
Preserve essential status/handoff/basic bot activity within the remaining allowance;
do not announce that all bots have been disabled. No repeated unchanged alerts.
An exposed reset time is not proof the allowance reset: obtain a fresh observation
before clearing a usage hold. Explicit Prime/Director direction may select work
within the reserve policy; do not silently lower or bypass the Director's floor.

## Durable report
Store usage observations as separate timestamped files under the current run's
evidence directory (usage/); never rewrite earlier observations or a sealed return.
Each final report includes: opening and closing observations, remaining percentage,
observed percentage-point change, other concurrent work/attribution limits, reset
time, unknowns and whether further work is held. A pool-wide change is not proven
to be this assignment's consumption. Report currency only if actually observed.
Give Prime a short current usage line on completion or a meaningful reserve change.
If a run is already sealed, publish a new advisory usage file instead of modifying
its hashed report. This policy adds no new code or schedule by itself.
