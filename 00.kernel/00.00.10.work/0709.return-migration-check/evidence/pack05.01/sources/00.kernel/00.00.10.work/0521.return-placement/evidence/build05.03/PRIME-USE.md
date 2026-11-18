# Prime use — read only until a later acceptance

The live plan is `migration-plan.json` in this directory. `live_moves` and `live_apply` are false. Enforcement is pending. Exit 0 on the plan command means the file was written. It does not authorize a move.

Do not run `stage`, `adopt`, `rollback-stage`, or `rollback-adopt` against `00.kernel/00.00.10.work`. Those commands refuse that path and any book that contains `0100.band.returns`. Do not remove that refusal and do not point the placement candidate's applier at the live book.

The plan command, which is the live read:

```text
python -B labs/return-lines-pass01/return_lines.py plan --book 00.kernel/00.00.10.work --audit 00.kernel/00.00.10.work/0417.return-placement/evidence/audit-corrected.json --out 00.kernel/00.00.10.work/0521.return-placement/evidence/build05.03/migration-plan.json
```

This pass wrote that file. Item count 83. Changes since the audit: 0. Occupancy conflicts: 18. Audit sha256 `c3bf8c1e25bfd1a59ce40230d87f650897f3105691db732eadfe5abf4e275606`, 391778 bytes. Plan sha256 `52951e1dbc0f37fa7f8c76be390a9510999a6944d7dc9f4e20c00c365f326f66`, 789717 bytes.

`app/return_line_tools.py` forwards to the lab after checking the pins. A pin mismatch exits 2 and does not run the tool.

A disposable rehearsal already ran outside the repository at `D:\lib-build-rl-0503` and was removed after the report matched. The report is `rehearsal-report.json`. It copied 1209 files, interrupted the stage, resumed, adopted, rolled the adoption back, adopted again, and filed synthetic pass `05.21` on the existing `0104.app-entry` line. The live fingerprint was the same before and after.

Preconditions before any live operation:

- Prime accepts this pack and the caller patch in `integration-patch.md`.
- Shared caller bytes are still the hashes in that patch, or the caller pack has updated them together.
- Stage every source to a backup outside the work book and outside the page namespace.
- Retire an occupant only after the backup hash matches the stage journal.
- Leave `0154.colab-support-first-0501` incomplete. Do not invent its return.
- Do not call the sequential allocator. Do not allocate `0184`.
- Do not file `0121.return-placement` while `0121.archive-resolution-0508` is still the occupant.

A verified receipt is not approval, acceptance, seating, publication, or finish.
