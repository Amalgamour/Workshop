# Return — claude-0507-0515 (0507.prime-support 05.15, recorded Prime boot packet candidate)

Submitter: claude-opus-5-5 (Anthropic), Colab, executor, packet preparation only. Reviewer: Codex Prime. Date: 2026-10-28. Workshop at claim: b4f30481148f480a4efbc69f00d2b336f53af8c1.

## Did
- Verified pack05.15: 20 of 20 snapshots match their pins and live. Recorded release and claim. Wrote the notes FIRST (06.16.md), then PLAN.md, then registry.json and request.json.
- **Source cut d3b6ad3e55beb1ec0bd5acbb114e6e66fd66c4e9**, as named; no HEAD selection. The brief's own cut, 6d18d182…, is kept distinct. Three brief pages are identical at both cuts; 0504/05.18 and 0508/05.16 changed after the brief, and that is stated.
- **One prepare through the accepted front door:** `app/librarian.py boot-prepare`, exit 0, `prepared` on the first attempt. Then `boot-show`, in JSON and text, exit 0: `prepared; awaiting answers; not oriented`.
  - Role is `Prime`, model is `unassigned-preparation-only`, there are three lanes and no Clerk jobs, and the records root is new and external.
  - No answers, check or judge, and no file 20 or later.
- **Packet:**
  - 12 refs and 45,460 bytes, inside 12 refs and 131,072 bytes, with 0 absences and 0 omissions, and stable.
  - The 4 mandatory refs, plus the live member 0145 (complete, receipt 62a74558…), the accepted brief, coordination-provenance, coordination, prime-review05.14, and one page for each outcome type: 0504/05.17 held, 0508/05.15 accepted without terminal, 0504/05.18 unknown as of the brief.
  - Every commit ref is byte-identical to its blob at the cut. The live member ref equals its raw inspection.
  - results.json (172,747 bytes) is over the cap, so it is an exact external link, not packet text.
- **Packet identity:** `09.packet.json` sha256 `1ebe2834bb96f2d15bdff7a34ab34ad602c6aaa4024d0b8b575fa5b6bc525893` (51,140 bytes). `19.prepare-outcome.json` is `f916bda8…`, and the raw request is `a1dc3059…`, equal to request.json.
- **records.json:** 23 base64 entries: 15 attempt files, 6 command streams and 2 drivers. All verify against the originals. The originals are kept at `C:\Users\misg\AppData\Local\Temp\pb-packet-0515-zidw8krt\p1`.
- **PACKET-ENTRY.md:** how to find the packet, the cut, the brief and its earlier cut, and how to tell live custody and live status from committed facts. It lists seven gaps, and contains no answers, grades or authority.

## Blocked
Nothing for the preparation.

## Need
- Prime's review, and the Director's.
- **Known gap.** With the canonical record bound to lane 0504, live status reports no conflict. The record is still stale (0504/05.06 `accepted`), and the desk-versus-lane decision (05.11 DEC-1 and DEC-5) is still open. It is listed as unresolved, not resolved.
- **Smallest next step.** After the reviews and the review of Grok-2's 0508/05.17 plan, the Director releases one test that binds the candidate's identity and a fresh session, this packet (`1ebe2834…` at d3b6ad3), and the reconciled question set. The candidate answers from the packet only, `boot-check` records the answers, and Prime judges.

## Limits
- This prepared packet is not a fresh Prime boot, and no model has read it.
- Grok-2's 0508/05.17 is recorded by hash only, as unreviewed.
- The brief describes 6d18d18, not current live work.
- Labels are not authentication.

## Declared outputs (sha256, bytes)
- 00.kernel/00.00.10.work/0507.prime-support/06.16.md: 5cada140b2a7fd035ce630d2c29c66797115d011394d0c4318a81a23ba77762a, 6348
- 00.kernel/00.00.10.work/0507.prime-support/evidence/packet05.15/PLAN.md: 6e3840f1ba64fc9d6fd46084dab9626b35e9d9e7eeb0c02d027a60612aac3b21, 5306
- 00.kernel/00.00.10.work/0507.prime-support/evidence/packet05.15/registry.json: 8a068546390d49c3958511d805be0b7c06ce9bf277b25ba575bc3780e4bd5cdb, 1239
- 00.kernel/00.00.10.work/0507.prime-support/evidence/packet05.15/request.json: a1dc3059b8ff98d41e526487b2f2240eb862bd78640aa00a4f702b86d4b61a4b, 1643
- 00.kernel/00.00.10.work/0507.prime-support/evidence/packet05.15/records.json: 021f61b2393bb6065f5cee0556445afdfa8055de1c48003a8bea87b3194e7e90, 281682
- 00.kernel/00.00.10.work/0507.prime-support/evidence/packet05.15/PACKET-ENTRY.md: dd81186b15d202b8467c9c9a59a07d54d4435d253bc6d834d04215b5ed1bb1a8, 4681
- 00.kernel/00.00.10.work/0507.prime-support/evidence/packet05.15/verification.json: 3ba62981073986cdced1b79828f4b3ee69b22c733e51b5aa13bd33e78c05a09a, 8711
