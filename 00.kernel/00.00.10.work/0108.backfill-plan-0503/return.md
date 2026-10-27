Did.
Re-checked `evidence/pack05.03/source-manifest.json` before writing `06.04.md`. Six live paths match their snapshots. Snapshot `0003.blob` matches the supplied door, SHA-256 `9d9efcd2f5bfbb5b4f44789303e27025ebbba6ffc5c281a2120fb5e7cb24cff5`, 2844 bytes. The live door is SHA-256 `e0f3abc3eeb4afcf23e2515126ea18f459c7258b2432746ae3479444d495d868`, 3435 bytes, and was left unchanged. The capture helper `labs/return-capture-pass01/return_capture.py` matches SHA-256 `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`, 45767 bytes. This batch adds no code.

Inventoried published commit `75ae515d826482113c4126274d015de112aa249b` with read-only `git cat-file`. The tree has 2920 files and 31 batch pages. Classification sums to 31: `no-return` 2, `return-and-review` 25, `return-pending` 2, `return-present` 1, `review-without-return` 1. Status sums to 31: `excluded` 5, `not-proposed` 3, `proposed` 3, `unresolved` 20. Three historical root files under `returns/` sit outside that 31. The one recommended next batch is `00.kernel/00.00.10.work/0505.observer-design/05.01.md`, return SHA-256 `952fb8a774cb174fe1b96ddbfdc9bc9df42a2f0e18e42557d21da02a52f2fea3`, 3216 bytes, five payloads, draft character, no member address.

`06.04.md` was written before `evidence/plan05.03/`. The reservation's three outputs are this note, `backfill-plan.json`, and `backfill-report.md`.

The pin check and the count reconciliation finished with exit 0. This batch adds no test suite and reports no test failure. The door difference is the recorded live text of a snapshot that itself matches.

Output hashes, measured after the three files were final:

- `00.kernel/00.00.10.work/0508.return-capture/06.04.md` | `2e5f0b8028fc3c3b69017c9c9f9e3aee04d1237c73709c65cc2925f4731b44aa` | 12277
- `00.kernel/00.00.10.work/0508.return-capture/evidence/plan05.03/backfill-plan.json` | `28994db7ef036af72282d0ff42068d090a7fbbeb5bc23ab550f8e5852b4fd16c` | 84040
- `00.kernel/00.00.10.work/0508.return-capture/evidence/plan05.03/backfill-report.md` | `f89539a0f4f22878752e887c3aaaa5bbfc62e14a47609e0581898508991abdb6` | 54400

Blocked.
Twenty batch pages stay unresolved. A named path is missing or a named directory is above the 12-file bound, and those rows keep an empty payload list. `0501.bootstrap/05.01.md`, `0501.bootstrap/05.02.md`, and `0504.app-entry/05.02.md` have no completed return body. `returns/clerk-handoff-proposal-claude-2026-10-27.md` stays a proposal. `returns/sof-gm-kit-pass01.md` is absent at the inventory commit and was left absent. Members `0101` through `0105` stay excluded. `0106.entry-regression-0509` and `0107.clerk-types-0505` stay other reservations. No mass backfill ran. No further member was reserved. No shared Git commit or push. HEAD at this submission is `acc3831f9560c86d4c000b84e9f026ca0570207b`.

Need.
Prime reviews this plan. A receipt records capture of the plan. It is not approval, acceptance, or publication. The observer draft needs a separate decision before any address is chosen. This reserved slot authorizes no further work.

Limits.
The inventory commit is `75ae515d826482113c4126274d015de112aa249b`. Rollout publication commit `086da87a07978413d810d3663d98df10d2a4bda3` is a different object. The expansion bound of 12 is this plan's rule. An earlier filename-join scan was discarded and is not evidence. Historical bytes come from `git cat-file` of the inventory commit. Named checker scripts were not executed. This capture passes no retrospective flag and no Prime-review flag. This submission contains no Review heading.
