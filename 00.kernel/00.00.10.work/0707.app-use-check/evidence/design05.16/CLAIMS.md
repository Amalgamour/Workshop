# Claim → case → result → limit (0707/05.16)
Provenance labels:
- **KR** — known-failure reproduction;
- **AT** — author test;
- **AH** — author hostile;
- **FP** — future independent probe (not run).

**Every run is on disposable copies** under `D:/librarian/temp/n7-intake-0716/` (local retention, not an archive).

| Claim | Case | Class | Result | Limit |
|---|---|---|---|---|
| The real 05.15 return fails today exactly as 0522/06.27 records | runs01 **A-app-prepare** (selected app entry, live code root) and **B-faithful-prepare** (unchanged pass03, faithful layout) | KR | both `incomplete`: `unparsed-return-line` (Returned), `submission-not-declared`, `declared-file-missing` for `…artifact-manifest.json,` | A's book is a copy; its code root is the live checkout (read-only) |
| The repair completes the real N7 intake with exact coverage | runs01 **R-faithful-prepare** | AT | `complete`; **30 rows:** assignment, submission (Returned), manifest, **26/26 artifacts with declared = measured**, return | the faithful layout needs the lab REPO redirect (disclosed) |
| Judgment and next action survive record → inspect → read → recover | runs01 R-faithful-* and R-noreview-* | AT | same review id and next action across processes | **a LAB-ONLY synthetic judgment** |
| An existing manual review is preserved | runs01 R-faithful-publish | AT | exit 1, `correction: manual-review`; the copy's `06.15.review.md` is byte-unchanged | — |
| Publish works where no review exists | runs01 R-noreview-publish | AT | exit 0; `06.15.review.md` created in the copy only | a copy without Prime's real review |
| Custody and release are not invented | all R steps | AT | `custody: missing`; accepted, approved, closes_work and releases_action are false | — |
| Old N5 syntax is unchanged | G1 | AT | identical parse dicts for 4 N5 inputs | inputs synthetic |
| The real N7 pointer parses; the comma is not kept | G2 | KR + AT | old: comma path; new: exact paths | — |
| LF and CRLF give the same parse | G3 | AT | identical | — |
| Duplicate or conflicting lines | G4, G5, G6 | AT | `ambiguous-submission` / `ambiguous-manifest` | — |
| Punctuation is refused, not stripped | G7 | AT | refused (`unparsed-return-line` / `unrecognized-path-punctuation`) | run01 FAIL was my expectation (code choice) |
| Leading `.` or `/` paths do not match | G8 | AT | no submission | — |
| Traversal is refused by the existing guard | I5 | AT | `malformed-declared-path` | — |
| Wrong hash or length | I1, I2 | AT | `declared-hash-mismatch`, incomplete | — |
| A missing manifest or payload | I3, I4 | AT | `declared-file-missing` / `artifact-missing` | — |
| An attribution cannot smuggle a declaration | **H1** | AH | `attribution-not-descriptive` | — |
| **No stripping or fuzzy match, even when a comma-named decoy exists** | **H2** | AH | unpatched binds the decoy (`declared-hash-mismatch`); patched binds the real manifest, `complete` | — |
| pass03's grammar reaches intake (my hypothesis D2 was **wrong**) | D2, I6 | AT | run01 FAIL refuted the hypothesis; run02 asserts the true fact | the hypothesis came from an incomplete code read |
| Production files are unchanged | runs01 `production_unchanged` | AT | 50/50 equal before and after | hash proof over the pack inputs only |
| An independent attack on the grammar | — | **FP** | **not run** | for Prime |
