# Dev journal: fixes after RELEASE-CHECK-90.50.10 (t414u, t415u)

date: Thu 19 Nov 2026, about 1:25-1:40 PM EST. written by: Prima builder-b21.
Why: Designer blocked 0400 and 0402 (docs/review/RELEASE-CHECK-90.50.10.md @ 55d87c8). t414u: nothing goes out unchecked.

- packs was already at 648e2858 (job 1 closed); returns still 60dd7e25. Nothing pulled was needed.
- 0400: face 01 v2 (entry 4). It says temporary (no face 00 registry in wf v0, replaced by `type: band` plus compute contents), 0401 dropped (repeats job 1), 0402 superseded, 0403 live, docs/ grant a tension.
- 0401, 0402: face 06 drop notes (entry 7 each). wf cannot withdraw a packed pass, so they stay packed and unpublished; folders kept; addresses never reused (titles fixed, DIRECTOR-RULINGS.md:129-130).
- Why 0403, not 05.02 on 0402: a second pack on 0402 needs 05.01 closed, and a packed pass can only close after a claim and return. A new address is the only clean path (Designer's fallback).
- 0403: same job as 0402 plus 99 on any axis, PP99, 9999 (seqAddr.md:31, :39, :226, :242, :249; DESIGN.md:137; addr.rs @ 79f12ed). axioms 1.7.8, overview with the door back-link. Packed, not published.
- Self-check: docs/review/SELF-CHECK-90.50.10.0403-b21.md.
