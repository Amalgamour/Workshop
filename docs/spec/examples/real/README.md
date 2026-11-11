# Real-book exports (FOLLOWUPS, 2026-11-11)

These `.seq` files are exported by the seqpage CLI from the real books in `books/`, not written by hand.
They show the current face 00 layout (docs/spec/face00.md, DRAFT; R10, R12, R19) on real pages.

| File | Page | Exported from | Book blob |
|---|---|---|---|
| `10.11.21.1001.bob.seq` | 10.11.21.1001 (bob) | `books/10.11.21.book` as of commit 18b9cfa | 543a9ba |

Regenerate (the books change as the kernel lane rebuilds them, so this file can go stale; no test pins it):

```
CARGO_TARGET_DIR=target/fu cargo build -p seqpage --bin seqpage
target/fu/debug/seqpage export books/10.11.21.book 10.11.21.1001 --dir docs/spec/examples/real
target/fu/debug/seqpage check docs/spec/examples/real/10.11.21.1001.bob.seq --book books/10.11.21.book
```

## What the bob export shows

- Face 01 (brand cards bob and cats) is seated: entry @13 carries `approved-by: build-stage (R2)` and `trial: docs/trial/kernel-trial-2.md@ed82086` (R2, R20).
- Face 05 counters 05.01 (what we learned) and 05.02 (the MVP pack) are seated: entries @14 and @15 carry `approved-by: build-stage (R2)` and `trial: docs/trial/kernel-trial-4.md@4b369fa` (R22). The export shows them as `state := closed` and the registry line as `05 counted`, because seqpage derives counter state from tails, not from seat records.
- Face 00 is still a draft (R14 allows seating faces while face 00 is a draft). Its registry holds `seat-01:`, `seat-05.01:` and `seat-05.02:` lines with full blobs.
- The old 04 face is gone (R15: a brand card on face 01 needs no 04 card).

## `seqpage check` on it (real output, 0 errors, 3 findings)

- stamp state `draft` disagrees with the page's entries (`live`)
- `faces: 01 seated, 05.01 seated, 05.02 seated` disagrees with what the compute derives (`01 seated, 05 counted`); compute-only fields are never hand-edited
- `seat-01:` is not a registry field for type `general` (face00.md section 3)

These are the open questions Q31, Q34 and Q38 (kernel/QUESTIONS.md) that the page's own 05.01 names; the third finding also applies to `seat-05.NN`. They are held `7`, not fixed here.

## Why the older bob example stays

`docs/spec/examples/10.11.21.1001.bob.seq` is the golden fixture for `docs/spec/examples/sources/10.11.21.book` (older layout, with the 04 face). About fifteen seqpage tests (golden.rs, cli.rs, corrupt.rs) are built on its exact text, so it is kept unchanged; this folder holds the real-book view.
