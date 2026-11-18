# Unresolved decisions and needs — 0710/05.02
date: 2026-11-02 · who: claude-opus-5-5 (Claude)

## For the Director (genuine forks only)
**F2 — payload file naming under 0018.**
- Under candidate 0002 v004 Payload, `02.run.003.py` is a payload, not a face.
- But 0018 says compute reads "the rank, the version, and a 09 without opening the file". By that rule the name scans as a draft of face 02 at v003 (L7).
- **The fix is one 0018 Envelope sentence** (`SECTION-IMPACT-MAP.md`). However, 0018 already has a pending draft, `01.011.md` (2026-10-26, mine), and the next number by 0024 would be 010. A second 0018 draft would compete with it.
- **Options:**
  - (a) Prime prepares one 0018 successor that carries the pending 011 change plus this sentence, after the 011 status is settled;
  - (b) hold the sentence until 011 is seated or withdrawn; meanwhile payload names stay ambiguous to a filename scan;
  - (c) keep payload versions out of filenames and declare them on the face. This changes the existing `02.NAME.VVV.ext` practice the Director described.
- **I recommend (a).**

**Already decided, so not asked again:**
- face = a logical object, Markdown for now (#05);
- conflicts go to the Director (#02);
- several forms per subject (#03);
- elevate stable replacement (#04);
- fix 0001 (#01).

## For Prime (engineering or ownership, not Director forks)
- **N1:** the owner of pack-specific requirements (R05). Generic work-item law is 0005; the pack subject owner is not identified. The pack example stays illustrative until it is.
- **N2:** the content of `00.retire.09/09.md`, needed by the first seating (0009: "The statement inside is `09.md`").
- **N3:** a seating tool. None is active in lib-build. Either a reviewed tool, or a reviewed, compute-verified rename procedure.
- **N4:** whether Grok-1's profile id counts as a form selection under candidate Forms (`GROK1-ALIGNMENT.md` row 3).
- **N5:** whether 0003 "exact available face-section targets" requires a menu entry to address the form itself. If so, that is a 0003 change. Today it is overflow.
