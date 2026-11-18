# Reconstruction index

These external trees are the proof roots for this run. They are not a durable archive. The reports below are copied into this evidence directory.

| Role | Path | Report sha256 | Bytes |
| --- | --- | --- | --- |
| Frozen-entry reproduction | `D:\librarian\temp\0522-0516\repro-frozen` | `f1585c6f23fb78f5f5bbc68c0feeb4d2260b04b8e0f5e414b70538ecfaca78e8` | 8823 |
| Author suite | `D:\librarian\temp\0522-0516\suite-20261104` | `be93e3c0f6794474692b6f3c7f13c4a472be2aea1545377753e4e15baecd1d00` | 4588 |

`drive.py` sha256 `88d715449ffe24d2bb883bc75f57e117d8d86b1223574269c520de0fd5292a03`, 31939 bytes, rebuilds the author cases on the suite path named in that file. The reproduction script was a session scratch file and is not part of the candidate. Its measured report is `repro.json`.

Author cases are the 18 suite rows. The baseline-copy row reruns the known pass05 defect. Independent future tests belong to Prime. The frozen pass04 and v7 reads are in the reproduction report, separate from the author suite.
