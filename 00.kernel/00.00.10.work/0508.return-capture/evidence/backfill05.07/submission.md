Did.
Captured two historical slices from commit `75ae515d826482113c4126274d015de112aa249b`. The bytes came from read-only `git cat-file blob`. Each return was stored whole, including its embedded Review section. Those sections stay old source bytes. They were not executed and they are not a current approval. No archived command was run.

`0118.workflow-start-0501`, submission `historical-0502-0501-75ae515`, is `00.kernel/00.00.10.work/0502.workflow-start/05.01.md`, SHA-256 `7f43ea75f0fc6f01229e0171312bc1f42a067df7a27e9689eab602d5f1bcfe17`, 20298 bytes, plus its 28 listed companions in reservation order. Origin is book `00.00.10.work`, page `0502.workflow-start`, batch `05.01`. Manifest `8a04bdec84e7c29701e75e8235fd7caa26a1a020f04ac497b57e0535af587638`. Receipt `972cecd6af207b8ea57f4301f3fe5d124755f3151c96cd66f0eebcdb2fa8d3c0`.

`0119.app-entry-0503`, submission `historical-0504-0503-75ae515`, is `00.kernel/00.00.10.work/0504.app-entry/05.03.md`, SHA-256 `6452628638d2237a82ca850da3925a57cc9c128ba1f92f28454087acce486187`, 12335 bytes, plus its 19 listed companions in reservation order. Origin is book `00.00.10.work`, page `0504.app-entry`, batch `05.03`. Manifest `5f036c7ab6d007ba0685985d2d8eca3b883c8e0c983edcad3e0a4da65d79e4e5`. Receipt `36909eb2d763ad9a484568703e4b86e37db7e2a20c8e308589186ffeaad7f344`. The live worktree copy of `app/README.md` differs from the inventory commit. The captured companion is the pinned blob `f57ff8b523dbdd7fdc6cc19da9ee34dc611a5cef1aed5a01b544726384ca6cbf`, 6930 bytes.

Both captures set `--retrospective`, `--source-commit 75ae515d826482113c4126274d015de112aa249b`, and `--return-includes-prime-review`. Fresh verify of each exited 0: result complete, not approved, not accepted, not published. Inspect of each exited 0 with status `complete`. The reads left the archived bytes unchanged.

`return_capture.py` stayed SHA-256 `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`, 45767 bytes. `return_inspect.py` stayed SHA-256 `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`, 11402 bytes. No product code changed. `0118` and `0119` were already complete when this submission was written. `0120` held only `01.md` and `reservation.json`. This report does not contain the later `0120` receipt.

Output hashes, measured after those files were final:

- `06.08.md` | `81b30259ba2c172e037e98cedb385e5cec36aafac86e5cf5ca0d63e41b248095` | 5528
- `source-plan.json` | `f2feffe0b4eeeda01e658c9a36088f3d594c11925df9404a9b631ccd34ab858b` | 60936
- `capture-log.txt` | `527f4a8509db7af87c09ca905288cef4b57d2b0c1b9cd4fdbda7220ba89bcf9a` | 41240
- `verification.json` | `e29920733f7b590bcb170b0a8becf856164cda638b7952189384e8de88b23df9` | 23478

Blocked.
Neither historical capture refused or left a partial package. This batch does not capture another inventory row, edit product code, or decide acceptance.

Need.
Prime reviews all three records. A later receipt records capture of this submission. It is not approval, acceptance, seating, or publication. This submission does not contain that later receipt. The reserved slots authorize no further work.

Limits.
The helper pin is `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`. The reader pin is `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b`. A receipt records custody. Embedded reviews confer no new authority. This submission contains no Review heading.
