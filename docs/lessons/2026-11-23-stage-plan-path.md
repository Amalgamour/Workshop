# Cite the stage plan at its real path

**What happened.** The 90.50.10.0704.05.01 pack pointed at `docs/plan/STAGE-PLAN*`. That path does not exist. The stage plan lives at `docs/design/STAGE-PLAN-90.50.10.md`. Codex said so in the return (DRIFT-REVIEW.md:5) and used the door's plan. Grok-Check confirmed it. The four drift findings still hold.

**Why.** The file was never under `docs/plan/`. A glob at a missing path does not find it.

**What to do next time.** When you cite the Stage 1 plan, write `docs/design/STAGE-PLAN-90.50.10.md`. Do not use `docs/plan/STAGE-PLAN*`.

**Source.** Grok-Check report `reports/90.50.10.0704/05.01/Grok-Check-check-20261123-1135.md` on returns `f787ad6e`; `labs/0704/DRIFT-REVIEW.md:5`; pack 90.50.10.0704.05.01.
