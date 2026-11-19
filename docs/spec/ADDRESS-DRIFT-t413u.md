# Spec note: wf address drift (t412u-t414u)

Status: draft for Designer review (t414u: nothing is released until checked against the axioms, the seqaddr rules and the design files).

## The rules (t413u, docs/review/DIRECTOR-WORDS-t413u.md)
- Desk, shelf and book axes: 00-09 are system-reserved. Work starts at 10.
- `DD.SS.00` is a shelf's authority book. Only the system writes there.
- Pages 0000-0099 are reserved.
- A page ending in 00 (`NN00`, at 0100 and up) is the band door. You enter there and find the work; work goes on `NN01` and up within the band. For wf, the band is 0400.
- crates/seqaddr-core/src/addr.rs already encodes this: `axis_role` (00 door, 01-09 reserved, 99 pointer), `page_kind` (0000 door, 0001-0099 reserved kinds, PP00 band head, PP99 continuation, 9999 book continuation), `band_head`.

## Why it drifted
- wf was built as a standalone kit. Its only address check is `page::check_addr`, which allows letters, digits, dots, `-` and `_`, so the path is safe. It never asked seqaddr-core what an address means.
- So every wf page took the first-looking slot: 90.10.00.0001, 90.20.00.0001, 90.30.00.0001 and 90.50.00.0001. Each one is book 00 (a shelf authority book) and page 0001 (reserved). No tool refused them, and no review compared them with seqaddr.
- The wf repo cannot depend on seqaddr-core today, because the crate is not on the wf branches on GitHub. So the fix copies the rules into wf (src/addr.rs) and cites the source. A shared crate comes later, if Designer wants one.

## The fix
1. Retire, never delete or rewrite. wf has no retire command, so:
   - Pages with no open pass get a `halt` entry with the note "retired: invalid address (...), t413u". wf then refuses draft, pack and claim.
   - 90.50.00.0001 had a returned pass, so halt is refused. It gets a face 06 note instead, and its pass is checked and closed in the normal way.
2. New work goes to band 90.50.10.04xx:
   - door 90.50.10.0400: face 01 holds the registry by hand;
   - job 1 at 0401;
   - job 2 at 0402.
3. Job 2 (90.50.10.0402) makes init-page refuse invalid work addresses. `--system --system-ref tNNNu` lets system pages through. Only init-page checks, so old pages stay readable.

## Gaps (glitchy, for Designer)
- No retire verb. Halt plus a note is the closest. A packed but unclaimed pass cannot be withdrawn, so halt is refused and a builder can still claim it.
- No face 00 or registry on a door page. The registry is written by hand in face 01, and the door needed a placeholder grant (docs/) because init-page requires one.
- Open: should 99 on an axis (pointer), PP99 and 9999 also be refused for work? seqaddr-core marks them as system kinds; t413u does not say.
