# Return placement candidate

This lab computes where a sealed return sits, and it can rehearse that copy inside a disposable fixture. It does not migrate the work book and it does not call `return_capture.py reserve`.

Band 5 keeps the leading workflow-space digit. `0504.app-entry` pass `05.06` is `0104.app-entry/05.06.return.md`. `1504.app-entry` is `1104.app-entry`. `9504.x` is `9104.x`. A second pass of the same page is another tail on that page. Band 7 stays on its own page at any prefix, including `1702.design`, with `05.NN.pack.md`, `05.NN.return.md`, and `06.NN.review.md`. This candidate does not invent pack or review bytes. Any other band is refused as `undeclared origin`.

A different-name directory on the target number blocks the final page. The fixture copy then goes under `staging/{old-member}/` and is not complete. Retirement is not performed. The plan lists every such occupied line.

The custody directory keeps the captured `01.md`, `reservation.json`, `manifest.json`, `receipt.json`, `return.md`, and `payload/` bytes. `relocation.json` is the only new file there. The sealed reservation destination is not rewritten. Before a source is ready, the pinned reader checks the sealed package. `complete` requires that check, an adopted line, and a placed or verified-equal copy. A missing receipt, manifest, or payload is not complete. A capture with no `return.md` stays incomplete. Acceptance stays null.

`apply` and `resume` refuse a fixture root that contains `0100.band.returns`. The live work book is that case. `plan` only reads the book and the pinned audit, then writes the requested `--out` file.

```text
python -B labs/return-placement-pass01/return_placement.py route --book 00.00.10.work --page 0504.app-entry --batch 05.06
python -B labs/return-placement-pass01/return_placement.py plan --book BOOK --audit AUDIT --out PLAN.json
python -B labs/return-placement-pass01/return_placement.py apply --root FIXTURE --source FIXTURE/0101.name
python -B labs/return-placement-pass01/return_placement.py resume --root FIXTURE
python -B labs/return-placement-pass01/return_placement.py rollback --root FIXTURE
python -B labs/return-placement-pass01/return_placement.py lookup --root FIXTURE --page 0504.app-entry --batch 05.06
python -B labs/return-placement-pass01/return_placement.py filing-check --book BOOK --page 0121.return-placement
```

Exit 0 means the journal is complete. Exit 1 means a result was recorded and is not complete. Exit 2 is a refusal. Exit 3 is an interrupted copy that can be resumed. `filing-check` is read-only and creates nothing. Sequential allocation is not retired by this lab.
