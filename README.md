# Workshop build (Prima)

Built from the Director's rework in `docs/spec/` (the spec governs; code follows it).
Stack per Design.md: Rust core + compute, Next.js reader app, books as append-only JSON Lines logs.

- `crates/seqaddr-core` address grammar, book log, replay, tail rules
- `crates/compute` the one process that owns the books; open reads, queued proposals
- `kernel/` seed kernel book `00.00.00.book`
- `app/` Next.js reader
- `docs/BUILD-LOG.md` every choice and its why
