# REAL-USE — 0164 and 0163 packets

This note compares operations that were run by hand with the assembler command. It does not estimate tokens, accuracy, completion, or benchmark readiness.

## Commands

Interpreter: `C:\Users\misg\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`

```text
python -B labs/review-packet-pass01/review_packet.py assemble --request 00.kernel/00.00.10.work/0514.review-packet/evidence/build05.01/request-0164.json
python -B labs/review-packet-pass01/review_packet.py assemble --request 00.kernel/00.00.10.work/0514.review-packet/evidence/build05.01/request-0163.json
python -B -m unittest discover -s labs/review-packet-pass01/tests -v
```

Both assemble commands exited 0. The test command exited 0: ran 10, skipped 1, failed 0. The skip is file-symlink creation, WinError 1314. The junction refusal ran and passed.

## Hand observations before the command

Pack source-manifest.json, 3190 bytes, sha256 8b03d471e212e5832c65dec95a7e07975160ed126df20ae01d92e33bbdb96b11. All 13 sources matched their snapshots. bad 0.

`git log -1` for `00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/artifact-manifest.json` printed 749cfd9c670fe77fbedd232c2630f98b0529025d.
`git cat-file blob` at that commit and at HEAD a8825689ab3220396841b144f3a7ebe95c9c9a66 both returned 14030 bytes, sha256 da06ab6cfdee15497c1d19394fb9e22433e5c1db6623a3fd8462d20749274634.
The same path is absent at 80f7025425d7bb3fdcf3b0ee56057cd6d8b6b9fe and at 32da8205d405d6008b8542cea3c8546f0d95d7df.
A row check at that earlier time found 69 historical blobs matching the manifest. 27 live paths differed in bytes. File text was not opened. During that check the live length of `labs/prime-bench-pass01/prime_bench.py` moved from 106837 to 106845.

## What the assembler recorded

0164.prime-entry-pin-repair-0503: assembly complete, custody complete, acceptance false, origin conflicts none.
Sealed return sha256 c0d1d2c65b02f0ce4486b408a9d691b94b2afe6d28df9fd55dc610c2a83fb7da, 1605 bytes.
Helper verify text included `result complete`, `not approved`, `not accepted`, and `not published`.
The pin artifact manifest was reported as schema `prime-entry-pin-artifact-manifest/1`, rows interpreted false.
Nominated packet.json sha256 bfcd0ee84d2505b06ebea0593bc66dc4504393ea966e357d58fae580ce98d6e4, 8393 bytes.
Nominated PACKET.md sha256 83b4d69f95910aaca4af4e4400e0d72551265f3700599f1564305363f86e0f20, 1999 bytes.

0163.prime-bench-harness-0501: assembly complete, custody complete, acceptance false, origin conflicts none.
Sealed return sha256 742beefbf856429ce3dfcf59e675a06f618c1b75b74f8f09b87c67dc6575198e, 6655 bytes.
The git blob at 749cfd9c matched the hand hash above.
The git blob at 80f7025 is absent in the packet, with `live file was not read`.
Of 69 artifact-manifest/1 rows, 41 are historical-match and 28 are changed-live-working-copy.
`labs/prime-bench-pass01/prime_bench.py` historical sha256 258727eef76693583ab0b88813c1b5afbded0009561f43c9bb61797b9d4dd650, 68800 bytes; live sha256 a6dc98b8b6dbcaa8e080903a3ec537381e511b2b94206b259bb5c723c0696fe3, 106951 bytes.
`labs/prime-bench-pass01/README.md` also differed at packet time (historical 4664 bytes, live 6022 bytes). The earlier hand pass had not listed that README difference, and the live `prime_bench.py` length had changed again. Those are working-copy differences between observations.
Specimen packet.json sha256 c6eeaa6bfa5a1c03577152f6d4b4df5a33601fb7f67ef58bbbace23fbb5599ad, 57915 bytes.
Specimen PACKET.md sha256 2443bc01d88d00590adccc47fd6749be75b484e083d6aa7ff3b81edf2dea0c18, 25501 bytes.
The row paths and hashes are in `specimen-0163/PACKET.md`. Live row bytes were hashed and were not copied into the packet.

The hand git hash and the assembler git hash for the 0513 manifest are the same. The hand result that 80f7025 lacks the path and the assembler result that the blob is absent are the same fact. The assembler added the custody record, the sealed-file copies, and the per-row live hashes. It did not decide why a live file differs.
