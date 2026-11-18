# Prime review - 0524.prime-desk/05.02.md
date: 2026-11-01
who: Codex Prime

Disposition: canonical-selection/packet repair improved, but routing still requires correction.

All 49 frozen source pins, 72 artifact rows and return/manifest pointer hashes
match. The only live input differences are app/librarian.py and README changed by
the separately authorized app lane; they aren't inputs to these demo requests.
Prime independently ran 14 tests on native Python 3.12.14: all pass in 5.250s.
A new disposable demo completed; its tool attention exits remain distinct from
the demo wrapper's success. Original output evidence was not overwritten.

PD-01 canonical selection is repaired: the existing assignment record named by
development-workspace governs current work; legacy selector/catalog disagreement
is visible and does not select. Work-bound packet material differs by selected
work. Explicit attribution spans separate Director/model text. The malformed
reader Stop exception is now handled; the new tests cover structured malformed
selection rather than the prior traceback. These are substantial useful repairs.

PD-05 review/custody conflation remains. page_identity(0521.return-placement/
05.03.md) derives review_path 0121.return-placement/05.03.md. That is wrong: full
Prime review belongs on 0521.return-placement/05.03.md, in its review section.
0121 is the return/custody line, whose return tail is 05.03.return.md. The demo
then treats the missing wrong review path as custody-pending. Existing custody
may be pending, but that must not move or obscure the already available review.
The app loop correctly renders under N5NN; do not connect the two tools with this
conflicting routing rule. This is against the existing spec, not a new design.

PD-06 identity coverage is incomplete. page_identity returns null for
1599.synth-lab/05.01.md, 1705.prime-desk-check/06.01.review.md, and even zero-prefix
0705.prime-desk-check/05.01.pack.md. Current code uses absolute ranges 0500-0599
and 0700-0799 and accepts the review tail as an N7 identity, not its source pack.
Source work, return and review identities are distinct. Honor declared N while
preserving same N/NN/subject/pass. N7 source pack 05.NN.pack maps to local return
05.NN.return and review 06.NN.review, not N1NN. Test actual source packs, not only
an already-known review file. Explicitly unknown kinds stay unsupported.

The 14 passing tests encode the wrong N1NN review expectation or lack these
positive cases; they are not cross-contract conformance evidence. Keep them as
historical output and add corrected independent route-table regressions in a
versioned successor. No actual desk view/packet was trusted for live review writes.
Bounded readonly use is inspectable, but combined desk acceptance is held. Proposed
05.03 is a narrow existing-contract repair; no broader architecture or new law.
