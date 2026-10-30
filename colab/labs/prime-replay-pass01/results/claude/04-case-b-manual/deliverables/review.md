# Review — case B (0514.review-packet 05.01, member 0167), MANUAL condition

Reviewer: claude-opus-5-5, Colab run 04-case-b-manual. A lab output, not a live review.

**Disclosure.**
- The builder was Grok Builder 1, not me.
- I have used review_packet as a pinned dependency.
- **Carryover:** run 03 (B assisted) came immediately before. Its findings and its reading of the page, return, CONTRACT and REAL-USE were in my context. I did not re-read those four files in this run; that is carryover, not independent reading.
- No assistance bundle was invoked: no prime_cycle, and no review_packet run as a reviewer aid. The subject's own tests were run as subject evidence.

## Did, Blocked, Need
**Did:** checked with my own hashing script and Python, all wrapped:
- custody: receipt, reservation, manifest, 7 payloads and return/submission identity;
- the 19-row artifact manifest;
- the internal consistency and completeness of both specimen directories;
- the subject tests, re-run;
- a skim of the classification and origin-conflict code.

**Blocked:** nothing.

**Need:** one Prime-side preservation check on the specimen evidence (below). There is no builder pack.

## Verified versus claimed

| claim | status | how |
|---|---|---|
| Receipt bf8cef9f… equals the page pointer | **verified** | own hash |
| Manifest, reservation and 7 payloads bound; submission.md == return.md | **verified** | own hash and byte compare |
| 19 artifact rows bind the build | **verified** | own hash: 19/19 match, none missing |
| Tests: 10 ran, 1 skip, 0 failed | **verified** | re-run: `Ran 10 … OK (skipped=1)` |
| 0163 specimen: 41 historical-match, 28 changed-live | **verified as recorded** | specimen-0163/packet.json counts are exactly 41 and 28; custody complete; acceptance false |
| 0164 pin manifest is an unsupported schema, rows not interpreted | **verified as recorded** | specimen-0164/packet.json: `prime-entry-pin-artifact-manifest/1`, `unsupported-schema`, no rows |
| "Keep both specimens as evidence" (pack #04); "an exact portable evidence copy… so Prime can open the decisive evidence" (#03) | **not fully met in the retained evidence** | see Defects 1 |

## Defects and meaningful unknowns
1. **Specimen evidence is incomplete as retained and bound.**
   - Each request wrote its packet directly into `evidence/build05.01/specimen-016x`.
   - Each specimen's own `manifest.json` names 11 files (0163) and 12 files (0164): custody.json, custody-stderr.txt, helper-verify.txt and its stderr, `sources/*.blob`, packet.json and PACKET.md.
   - The retained folders hold only `PACKET.md`, `packet.json`, `manifest.json` and `assembly-status.json`. The 0514 artifact-manifest binds only those 4 per specimen.
   - So the nominated captured packet (0164) refers to source snapshots and custody files that a reviewer cannot open from the retained evidence.
   - **Unknown:** whether the missing files existed and were left unbound and unpublished, or were never kept. This frozen input cannot tell.
   - Severity: a preservation gap in the pass's evidence, not a tool defect. The tool writes the full set (tests and my run 03 packets confirm it).
2. **Unknown:** the file-symlink refusal on this host. It is implemented but the test skips.
3. **Pack ambiguity, as in run 03:** "do not open Claude's uncommitted work" against hashing live rows. The builder hashed without copying, and disclosed it. I accept that reading.

## Disposition
- **Pass:** finished, accepted, with one preservation finding (defect 1) to resolve by checking the published evidence, not by a rebuild.
- **Goal** ("a bounded mechanical packet… preserving exact evidence…"): **completed for the tool.** The helper produces exact, bound, portable packets.
- **The pass's own specimen retention is incomplete.** If the missing specimen files cannot be recovered, record that fact on the page; the tool goal is unaffected.
- **Director:** not needed.

## Difference from run 03 (assisted)
Run 03 accepted the pass with goal completed and NO PACK REQUIRED. It did not open the specimen directories' file lists. Its packet assembly made fresh complete packets, which hid the gap in the retained ones. This manual run found defect 1 by checking each specimen's manifest against its folder. I have not rewritten run 03.

## Preservation
Nothing in the subject was changed.

## One bounded next action
Prime checks whether the full specimen directories (custody.json, helper-verify, sources/*.blob) exist at the published revision or in the builder's retained workspace:
- if they exist, bind them in a follow-up evidence record without altering 0167;
- if not, append a note that the specimens are packet.json and PACKET.md only.

This is a custody and evidence check by Prime, not a build.

## Factfind
- `evidence/build05.01/specimen-0163/manifest.json` names `sources/0001-return-text.blob` … `0005-artifact-manifest.blob`, and none of them are present.
- `request-0163.json` `output` is the specimen folder itself.

## Hostile
The path that should break: "assembly complete" read as "evidence retained". The face I was tempted to obey was run 03's conclusion. It looked complete because the tool can make complete packets.

## Overflow
I did not determine which commit published the specimen folders (provenance and history are out of bounds).

## Unprompted
Manual effort found the only substantive case B finding. The assisted route spent its effort on re-generating packets.
