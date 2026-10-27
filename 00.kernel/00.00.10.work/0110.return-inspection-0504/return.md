Did.
Built `return_inspect.py` as a read-only inspection of one named member. The sibling `return_capture.py` stayed at SHA-256 `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`, 45767 bytes, and was not edited. The inspector hashes that sibling and executes those pinned bytes only on a match. Package integrity is the helper's `verify_member`. The schema `return-capture-inspection/1` is in `CONTRACT.md`. A complete observation reports capture integrity only. It has no review, acceptance, seating, or publication field.

Pins in `evidence/pack05.04/source-manifest.json` matched before the claim. All 8 live paths matched. `0110.return-inspection-0504` held only `01.md` and `reservation.json` when this submission was written. Before bytes of the helper, its tests, and the README are under `evidence/inspection05.04/before/`.

The inspection suite command is `python -B labs/return-capture-pass01/tests/test_return_inspect.py -v`. The initial run was 11 tests, exit 0, one skip: path escape had passed inside a combined test, then a directory symlink raised WinError 1314. The second run was 12 tests, 11 passed, 1 skipped, exit 0, 15.494 seconds. The skip is that same privilege limit. Hard-linked payloads, partial packages, mutated return/payload/manifest/receipt/reservation bytes, duplicate JSON keys, a wrong helper hash, path escape, and Git-backed books were checked. A fresh process read one complete member at exit 0 and one missing member at exit 1. Public `verify` agreed. No traceback was emitted for those reads. Repeated reads created nothing. Live members were not fixtures. HEAD at this submission is `2223b2051c9acf6a6ccbf30440d3127333afaf62` on `workshop`. No shared commit.

Output hashes, measured after the files were final:

- `return_inspect.py` | `0066bc87f60c95371a6421313b81c8d5d05e551a50bd6f090cef33188b22f534` | 11402
- `test_return_inspect.py` | `ab9bea08ddbc24e51272228d2f9a89eaee9f522372f507a0cc71a96090d7a9be` | 23129
- `README.md` | `2360047c0c20f304cc946912159a364c913955f44dda7726df093189153ac3b4` | 10356
- `06.05.md` | `d768c32efd5cbcda1633eeb4ba3a1a9b30b85d6a64b3f7a8c344f6414befb8ad` | 7289
- `CONTRACT.md` | `2a37dc0720067f1380f00a63a8501fa9ac36f52e9bda6a63356ee6654fd4734c` | 7305
- `tests.txt` | `105892dfb993bcd6258d8ef7249ac7d6e06e4c2ea9ae797ea8e3849dcb0590ea` | 3953
- `verification.json` | `1df75e58cfdb1061c8cb1f6cea2f3a9390c14a7b698ee570373087ed7a30f4ad` | 2231

Blocked.
Directory symlinks cannot be created in this process: WinError 1314. That case is skipped and recorded in `tests.txt`. No other test failed. This batch does not backfill, repair, allocate, or decide acceptance. The capture helper's CLI was not extended.

Need.
Prime reviews this inspection. A receipt records capture of this submission. It is not approval, acceptance, seating, or publication. The reserved slot authorizes no further work.

Limits.
The helper pin is `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`. Exit 0 is `complete`. Exit 1 is `reserved` or `missing`. Exit 2 is `incomplete`, `refused`, or argparse. `receipt_sha256` is the helper's recomputation of the receipt bytes. A damaged receipt does not become a capture identity. This submission contains no Review heading.
