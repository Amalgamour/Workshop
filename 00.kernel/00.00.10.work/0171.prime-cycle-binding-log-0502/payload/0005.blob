# PRIME-USE — current Prime's first real use of the corrected cycle (05.02)

For Codex Prime. This replaces `build05.01/PRIME-USE.md` for the 05.02 tool; the 05.01 guide is kept as it was. Nothing below has been run on a live page: this Builder pass wrote no live review.

**What changed since 05.01:**
- every command takes a journal;
- a template binds your agreement (direction);
- a review whose page, custody or agreement has moved is shown as historical, never as current completion.

## 0. Places

- **Review location:** `<lane>/evidence/prime-cycle-reviews/<pass>/`. You approved this placement in the 05.01 review.
- **Output root**, outside the repository: `D:\prime-cycle-out\`, for templates and packets.
- **Journal root**, outside the repository: `D:\prime-cycle-out\journal\`. It may sit under the output root. Templates and packets may not go inside it. The tool refuses a journal root inside the repository or the members book.

## 1. The smallest real registration (one work: 0508.return-capture/05.20, member 0169)

Save it as `D:\prime-cycle-out\reg-0520.json`. Use the published commit you are reviewing. Write the goal and the agreement in your own words. They are bound into the template, so change them before you read, not between read and record.

```json
{"schema": "prime-cycle-registration/1", "repository": "D:/Git/lib-build", "book": "00.kernel/00.00.10.work",
 "book_label": "00.00.10.work", "source": {"kind": "git-blob", "commit": "<40-hex published commit>"},
 "members_book": "D:/Git/lib-build/00.kernel/00.00.10.work", "output_root": "D:/prime-cycle-out",
 "bounds": {"max_works": 16, "max_page_bytes": 262144, "max_output_bytes": 2097152},
 "works": [{"work_id": "deskstate-0520", "page": "00.kernel/00.00.10.work/0508.return-capture/05.20.md", "pass": "05.20",
            "member": "0169.desk-state-preservation-0520",
            "goal": {"goal_id": "<your goal id>", "statement": "<your page-goal statement>"},
            "agreement": {"goal": "<…>", "scope": "<…>", "prime_discretion": "<…>", "director_required": "<…>",
                          "finish_criteria": [{"id": "<id>", "text": "<…>"}], "recorded_decisions": [{"id": "<id>", "text": "<…>", "source_sha256": "<64 hex>"}]},
            "review_location": "00.kernel/00.00.10.work/0508.return-capture/evidence/prime-cycle-reviews/05.20"}]}
```

## 2. Read and get the template (logged)

```text
python -B labs/prime-cycle-pass01/prime_cycle.py read --registration D:\prime-cycle-out\reg-0520.json --templates D:\prime-cycle-out\t1 --journal-root D:\prime-cycle-out\journal --caller "Codex Prime"
```

**Expected today:** the builder's read-only preview at d192410 gave exactly this.
- `pass state: awaiting-review`;
- custody 0169 `primary-current-candidate`, receipt `94a5fe21…`;
- `! legacy-review-unmapped`;
- the summary line counts 0 finished and 0 completed;
- exit 1;
- the last line reads `journal: D:\prime-cycle-out\journal op <op_id>`.

The template `t1\template-deskstate-0520.json` is `prime-cycle-decision/2`. Its binding is pre-filled, including `direction`; don't edit it.

## 3. Fill only the judgment

This is the same as 05.01. Fill `attribution.actor_label` and `judgment`:
- outcome, disposition, pass_terminal and goal.terminal (with evidence when completed);
- finding, reasons, source_refs, next_action, unresolved and semantic_conflict;
- the sections your outcome needs.

The counts are unchanged: 14 for continue, 18 for complete, 15 for a hold.

To **adopt** your 05.20 prose review, record it as this first typed review, with reasons and source_refs pointing at `evidence/prime-review05.20/REVIEW.md`. Nothing adopts it automatically.

## 4. Record, read, and look at the day (logged)

```text
python -B labs/prime-cycle-pass01/prime_cycle.py record --registration D:\prime-cycle-out\reg-0520.json --decision D:\prime-cycle-out\t1\template-deskstate-0520.json --journal-root D:\prime-cycle-out\journal --caller "Codex Prime"
python -B labs/prime-cycle-pass01/prime_cycle.py read --registration D:\prime-cycle-out\reg-0520.json --journal-root D:\prime-cycle-out\journal --caller "Codex Prime"
python -B labs/prime-cycle-pass01/prime_cycle.py day --journal-root D:\prime-cycle-out\journal --registration D:\prime-cycle-out\reg-0520.json
```

**Expected:**
- record exits 0, or 1 when prime_review shows a hold or attention, and prints `recorded <dir>` plus the journal line;
- read shows `pass state: reviewed`, with your disposition, pass terminal and goal terminal as current values, and the summary counts them;
- day lists your three operations with their status, caller, times (with the timezone offset) and durations. It shows one unique review with its record hash, re-verified now, and the current status from a fresh read. day itself is not logged.

**Refusals** (exit 2; nothing is written; the journal keeps the refusal):
- `direction changed since read: agreement.<field>`: you edited the registration after reading. Read again.
- `decision schema … older read`: a 05.01 template. Read again.
- `source changed since read`, `expected_prior …` and `conflict` are as in 05.01.

**Interrupted write** (exit 3): the journal keeps it as `partial`. Run `inspect`, then record under a new review_id with `recovers`.

**Journal problems:**
- **exit 4:** the journal could not start, and nothing ran. Fix the root and rerun.
- **exit 5:** the operation ran and its output is shown, but the journal end event failed. stderr says whether a review is committed or partial, and where. That journal entry stays incomplete, and nothing is retried.

## 5. If something changes after you record

If the page, the custody or your agreement later changes, read shows `review-stale` and `unknown (historical <value> in <review>)`. The summary and the day view's "current" stop counting it as finished or completed. Your record is kept. Record a successor review (the fresh template sets `supersedes`) to make it current again.

A changed goal id or statement is not stale: the pass stays reviewed, and the goal reads open with a prior-completion note.

## Limits

- The tool records your supplied judgment. It authenticates no one, and `--caller` is a label.
- The journal covers this tool's operations only. Chat, shell commands and model actions are not captured.
- There is no transaction across files, and no OS sandbox. Same-user races are out of scope.
