# Known reproduction

Stamp `D:\librarian\temp\0522-0516\repro-frozen`. Page `0599.n5-identity-lab`, pass `05.01`, one artifact. Frozen `labs/workbook-review-pass04/workbook.py` prepare and record exited 0.

Stored book: `D:\librarian\temp\0522-0516\repro-frozen\bookA`
Stored instance_id: `49942f2d12ffbd5681fbe15ff7fe56250458e456726e495a1c87c03445a8af2b`
Stored intake_id: `96ea81d74effd77ee4fe08b070b23b96cccb832a878515da6bca95839d67681d`
Review id: `wd968ebf5cc30efc4`
intake.json: `63b613ffdfcdcbc865280e08c8d0e11e94f08e8b37685d5a7613e6217e426355`
journal.json: `189ed9dff949564a1fc9b9176e21271eabaa1077db1806217a1c7e5c18497138`
record.json: `4d03c41e0544bb7eca5929a40608dcc9ee2fcaf23dfb32886ea49c663400e2ce`

The book directory was copied to bookB. Live instance_id `c3977a100c59e5bbe70a203b2ff8cc30bc28af386e3efa1ea4231cde0904a378`. Live intake_id `bfa2e3ae9352000daa198691b0d1b3e66f6e161bbb49e7bbdecd106873ba1687`.

pass04, pass05, and `app/librarian.py review-loop` prepare, read, and recover on bookB each exited 0 with stale false. read and recover returned the stored finding and next_action. The original store and the copied store kept the hashes above.

Report sha256 `f1585c6f23fb78f5f5bbc68c0feeb4d2260b04b8e0f5e414b70538ecfaca78e8`, 8823 bytes. The same bytes are `repro.json` in this directory.
