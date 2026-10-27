# Prime review — seam partial-I/O correction
Date: 2026-10-27. Reviewer: Codex Prime.
Disposition: ACCEPTED for CS-01 correction. CS-01 closed. CS-02 remains open.

Independent disposable sequential runs: seam44 passes/19 expected refusals/one
privilege skip/zero failures; entry12 passes/46 expected refusals/one skip/zero
failures; pack tools11 passed/one skip; unchanged narrow bridge lab2/2 passed.
Separate external wrapper (not the product io_fault switch) reproduced the
original write failure after3 bytes: now attention/exit4, partial bytes and Clerk
claimed events retained, one launch. Later call refuses the partial outbox without
relaunch. The suite also covers create/flush/fsync/readback and uncertain return.
Fresh builder-local0112 verifies; all 8 declared outputs match source.

The builder's first failed concurrent run is preserved; its same-bytes rerun
passed. Prime independently reproduced its underlying race deterministically:
between _lexists and mkdir, another caller creates the shared ordinary parent;
worker_bridge._ensure_plain_dir raises uncaught FileExistsError. This is CS-02,
not erased by either later passing integration run. No timing cause is inferred
for the older descendant-pipe failure; its separate passed narrow run is evidence.

This accepts honest partial-I/O handling and the bounded single-job fixture loop,
not concurrent-use readiness, live model dispatch, general recovery or kernel
seating. A partial outbox still needs explicit recovery; no automatic cleanup.
Next05.12 may edit the previously out-of-scope bridge helper to resolve CS-02.
Keep _exclusive_dir semantics: shared parents and unique delivery stores are
different. Do not use exist_ok to allow occupied/linked per-delivery targets.
Exact evidence is verification.json and logs; original return/receipt unchanged.
