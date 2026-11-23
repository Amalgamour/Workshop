# Name the reviewer and the filer

**What happened.** The 90.50.10.0702.05.02 check event names Codex as the checker and holds Codex's manual findings. An executor filed that judgment with `wf check ... --as Codex --fail`. The event has no separate field for who typed the command, so the log alone cannot tell the reviewer from the filer. Matthew said both should be named (`labs/0704/MATTHEW-RESPONSES.md`).

**Why.** `wf check` stores one name, the `--as` / `WF_AS` caller, on the check event (`src/cmd.rs` at a823ee28, the `p.add(who, "checker", "check", ...)` call). There is no `filed_by` field.

**What to do next time.** Until wf records both names, say in the check `--note` who typed the command if that person is not the reviewer. The proposed fix is a `filed_by` field on the check event, on a later wf work page once `src/cmd.rs` is free. Do not close or restage 0702 on this lesson alone.

**Source.** `.workshop/logs/90.50.10.0702/log.jsonl` entry 18 on returns; `labs/0704/DRIFT-REVIEW.md` and `labs/0704/LESSONS.md`; `labs/0704/MATTHEW-RESPONSES.md` ("2. Yes").
