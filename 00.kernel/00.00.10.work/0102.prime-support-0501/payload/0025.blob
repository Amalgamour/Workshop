## Review — Codex Prime
Date: 2026-10-27.
Disposition: ACCEPTED AS DESIGN INPUT WITH REQUIRED IMPLEMENTATION CORRECTIONS.
This accepts design direction, not runtime behavior, new global law, a real intake
store, or a shadow Prime. No implementation or session trial ran in this review.

What works: status reads owning records rather than making another queue; seen,
reviewed and accepted remain separate; unresolved findings survive acknowledgement
store loss; local/published conflicts stay visible; discovery is bounded; the first
lab has no dependence on unaccepted Clerk code. This is directly useful to the
Director's goal of reducing Prime's repeated reading and enabling a shadow trial.

Independently verified: all 9 design-manifest entries match their bytes. The
synthetic v1 returned and reviewed files have the same prefix hash
5e4439fc0dc7084eb32965617383471beb63f2c4ffb53c464999831eb7394d86;
amended v2 has 4443b4b2e2162dfb696519a643fbe64cd2ca1f125adb3491d3cd687fe8dfd73e.
The examples are constructed examples, not results from an implemented tool.

Required corrections (open until implementation evidence):
- PS-01: The first line beginning `## Review` is not an unambiguous boundary.
  Prime reproduced two different return bodies with the same identity when such
  a line appears inside a fenced example. Use one exact recognized top-level
  Review heading outside fenced blocks; reject ambiguous/misordered structures.
  Test fenced decoys, heading prefixes, duplicate headings and normal appended
  reviews. Do not let a later differing payload inherit an earlier review.
  Define which bytes are reviewable and how pre-boundary metadata edits behave;
  changed reviewed bytes need renewed review, never implicit acceptance.
- PS-02: External SoF currently returns at the explicit bootstrap path
  `returns/sof-gm-kit-pass01.md` on `sof/gm-kit`, not at a root 05.NN page.
  Register an exact return-file source kind alongside page folders, or clearly
  report it unsupported. Prefer the small explicit adapter. No repository crawl
  and no conversion of SoF's history into workshop page numbering.
- PS-03: The fixture lab must retain finding lineage across amendments even when
  the current page no longer carries an older Review. Use declared review sources
  or bounded source history, never the acknowledgement store as a findings ledger.
  Missing historical evidence is unknown/attention, not zero findings. Add a test
  deleting acknowledgements and removing the old Review from the amended page.

Implementation guidance: reserve only provisional fixture schemas for the four
one-line fields. M02 is not adopted as universal law by this review. M01 may remain
an explicit temporary --intake path for the lab; defer a real store installation.
Status must describe scan scope, last-observed refs, unsupported sources and
legacy unknowns. A fixture acknowledgement may not edit real work pages or refs.
The attention priority is a configurable written recommendation, not authority.
The illustrative current-state report is dated to its input snapshot; it is not
today's live status after subsequent Prime reviews/publications.

Next bounded action: implement the fixture-only status/intake lab with PS-01–03
covered, then demonstrate it against a disposable snapshot containing both a
workshop return and the actual SoF bootstrap return format. No observer fetch,
Clerk adapter, app integration, model launch or real intake rollout yet.
Builder release remains a Director action. Claude can implement this bounded lab
after receiving a released assignment; this review is not itself that assignment.
