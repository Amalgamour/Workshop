Did.
Moved the existing `MEMBER_MIN`/`MEMBER_MAX` check ahead of existence classification in `return_inspect.py`. Absent and existing `0100.door`, `0200.outside`, and `9999.outside` now refuse at exit 2 with `capture` null and unchanged bytes. Names `0101` and `0199` keep `missing`, `reserved`, and `complete`. Schema `return-capture-inspection/1` and the capture core are unchanged. `return_capture.py` stayed at SHA-256 `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`, 45767 bytes, and was not edited.

Regenerated the worked example in `evidence/correction05.05/CONTRACT.md` from one disposable helper capture. Origin book `00.00.10.work`, page `0508.return-capture`, batch `05.04`. Reservation SHA-256 `ed5fafc4a4f4597dc241996794c6043eb6787d35f61a8a2037b8453220050669`. Manifest SHA-256 `a86053d3c94bf6a384b12e37b9483448d792738b61ddb23fd434de78cba14057`. Receipt SHA-256 `fd822d4260c7329f3171d26dafbfb8a6ca19e4373d24bfa70b430778a7668d9c`. Return SHA-256 `e1d4ac07dade356a40ea3da83f437c1ae36d3d89bd8718601600925bc842223b`, 5 bytes. Payload SHA-256 `389ed6887e49a315f706f6c2b931b1dcf0d797c91437124f32eb98555c669758`, 5 bytes. The original `evidence/inspection05.04/CONTRACT.md` stayed SHA-256 `2a37dc0720067f1380f00a63a8501fa9ac36f52e9bda6a63356ee6654fd4734c`, 7305 bytes. A parsed origin is validated shape. It is not proof that the caller labels are true.

Pins in `evidence/pack05.05/source-manifest.json` matched before the claim. All 9 live paths matched. `0114.inspection-range-0505` held only `01.md` and `reservation.json` when this submission was written. Before bytes of the inspector and its tests are under `evidence/correction05.05/before/`.

The inspection suite command is `python -B labs/return-capture-pass01/tests/test_return_inspect.py -v`. One run: 14 tests, 13 passed, 1 skipped, exit 0, 16.291 seconds. The skip is WinError 1314 on a directory symlink. A fresh process read a complete member at exit 0, an absent `0199.missing` at exit 1, and a receipt-damaged member as `incomplete` with `capture` null. Public `verify` agreed. Live members were not fixtures. HEAD at this submission is `7eb3f523cd3ade9b69b47665178e418df6f747e2` on `workshop`. No shared commit.

Output hashes, measured after the files were final:

- `return_inspect.py` | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` | 11402
- `test_return_inspect.py` | `45abbbe6f1402d2f775332c30b70f2a638128f1c5d3a886e6714d17c4f2c0f37` | 29472
- `README.md` | `2a72d2d961d417fdb06e2fc8a9430270971df74351343bf7488cabd10a1a9ebd` | 11164
- `06.06.md` | `5712c2986d28f32e80ed1e7dc4a51dc0e8cd311ceb5105c0f19979078c22e6ad` | 6219
- `CONTRACT.md` | `20ca12577129885747e2b90f280b79b81b41561aa023f394e2c95fa837a68a5b` | 7295
- `tests.txt` | `f9928caa023faeca1883eeee95d52cb3c3bd4928d25aca11617009a37ebf8548` | 2922
- `verification.json` | `1e8acdf19e64a036e01184d665eba3f95bdd5758b4a35568db0ae7e9312d9986` | 5434
- `before/return_inspect.py` | `0066bc87f60c95371a6421313b81c8d5d05e551a50bd6f090cef33188b22f534` | 11402
- `before/test_return_inspect.py` | `ab9bea08ddbc24e51272228d2f9a89eaee9f522372f507a0cc71a96090d7a9be` | 23129

Blocked.
Directory symlinks cannot be created in this process: WinError 1314. That case is skipped and recorded in `tests.txt`. No other test failed. This batch does not backfill, repair, allocate, or decide acceptance. The capture helper was not edited.

Need.
Prime reviews this correction. A receipt records capture of this submission. It is not approval, acceptance, seating, or publication. The reserved slot authorizes no further work.

Limits.
The helper pin is `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac`. Exit 0 is `complete`. Exit 1 is `reserved` or `missing` for an in-band member. Exit 2 is `incomplete`, `refused`, or argparse. An out-of-band name refuses before the path is classified as absent or present. `receipt_sha256` is the helper's recomputation of the receipt bytes. A damaged receipt does not become a capture identity. Caller origin labels confer no authority. This submission contains no Review heading.
