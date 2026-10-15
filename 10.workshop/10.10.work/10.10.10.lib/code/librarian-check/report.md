# librarian-check report

| tier | error | warn | info |
|---|---|---|---|
| reworked | 29 | 24 | 104 |
| pending | 32 | 54 | 34 |

## REWORKED pages
rule counts: carry-terms error=2, dangling-page error=3, face-name error=2, reassigned-number error=7, register error=1, same-version-differs error=2, seat-is-draft error=1, sentinel error=1, stale-address error=9, status-footer error=1, dangling-page warn=1, face-07-filled warn=1, order warn=1, stale-address warn=1, stale-draft warn=19, stamp-missing warn=1, dangling-page info=16, stale-address info=33, status-footer-lock info=14, twin-heading info=26, work-file-name info=15

### error (29)
- [carry-terms] `00.00.01.law/0006.note/02.md`: face 01 carries "overflow"; face 02 does not
- [carry-terms] `00.00.01.law/0006.note/04.md`: face 01 carries "overflow"; face 04 does not
- [dangling-page] `00.00.01.law/0000.invariant/01.md`: "page `0009`": no page 0009 in any book
- [dangling-page] `00.00.01.law/0000.invariant/02.md`: "page 0009": no page 0009 in any book
- [dangling-page] `00.readme.md`: cites 0102.templates; no such page
- [face-name] `00.00.01.law/0012.dictionary/03.10.md`: filename "03.10.md" is not FF / FF.VVV / FF.VVV.09 / 05.NN
- [face-name] `00.00.01.law/0012.dictionary/07.sample.md`: filename "07.sample.md" is not FF / FF.VVV / FF.VVV.09 / 05.NN
- [reassigned-number] `00.00.01.law/0000.invariant/01.md`: "page `0026`": 0026 was "promote" (now at 0023), is now "strike"
- [reassigned-number] `00.00.01.law/0000.invariant/08.md`: "page `0026`": 0026 was "promote" (now at 0023), is now "strike"
- [reassigned-number] `00.00.01.law/0002.schema/01.md`: "page 0051": 0051 was "rhyme" (now at 0059), is now "desk"
- [reassigned-number] `00.00.01.law/0002.schema/04.md`: "page 0051": 0051 was "rhyme" (now at 0059), is now "desk"
- [reassigned-number] `00.00.01.law/0014.design/03.md`: "page 0058": 0058 was "desk" (now at 0051), is now "custody"
- [reassigned-number] `00.00.01.law/0014.design/03.md`: "page 0059": 0059 was "shelf" (now at 0052), is now "rhyme"
- [reassigned-number] `00.readme.md`: "page `0028`": 0028 was "colab" (now at 0036), is now "crawl"
- [register] `00.00.00.syntax/00.REG.md`: REG row 0009 0009.retire: no such folder
- [same-version-differs] `00.00.00.syntax/0010.about/01.002.md`: draft 002 and seat 01.md (version 002) differ in body text
- [same-version-differs] `00.00.00.syntax/0014.design/01.006.md`: draft 006 and seat 01.md (version 006) differ in body text
- [seat-is-draft] `00.00.01.law/0025.clean/02.md`: seat stamped draft
- [sentinel] `00.00.14.notes`: book has no 00.md sentinel
- [stale-address] `00.00.01.law/0000.invariant/08.md`: "Promote is page `0026`": 0026 is ['law-crawl', 'strike']; "promote" lives at ['0023'] (moves ledger confirms)
- [stale-address] `00.00.01.law/0002.schema/01.md`: "Rhyme is page 0051": 0051 is ['desk']; "rhyme" lives at ['0028', '0059'] (moves ledger confirms)
- [stale-address] `00.00.01.law/0002.schema/04.md`: "Rhyme is page 0051": 0051 is ['desk']; "rhyme" lives at ['0028', '0059'] (moves ledger confirms)
- [stale-address] `00.00.01.law/0006.note/08.md`: cites 0016.write; 0016 is now ['compose'], "write" lives at 0021
- [stale-address] `00.00.01.law/0014.design/01.md`: "Desk is 0058": 0058 is ['custody']; "desk" lives at ['0051'] (moves ledger confirms)
- [stale-address] `00.00.01.law/0014.design/01.md`: "Shelf is 0059": 0059 is ['rhyme']; "shelf" lives at ['0052'] (moves ledger confirms)
- [stale-address] `00.readme.md`: "Colab is page `0028`": 0028 is ['crawl', 'rhyme']; "colab" lives at ['0036'] (moves ledger confirms)
- [stale-address] `00.readme.md`: "Colab home on live law is `0028`": 0028 is ['crawl', 'rhyme']; "colab" lives at ['0036'] (moves ledger confirms)
- [stale-address] `00.readme.md`: cites 0024.write; 0024 is now ['crawl', 'version'], "write" lives at 0021
- [status-footer] `00.00.01.law/0025.clean/02.md`: header draft, footer "last change ... approved"

### warn (24)
- [dangling-page] `00.00.01.law/0014.design/03.md`: "page 0062": no page 0062 in any book
- [face-07-filled] `00.00.01.law/0001.law/07.md`: face 07 is filled
- [order] `00.00.01.law/00.order.md`: lists 0009.retire, folder not in this desk
- [stale-address] `00.00.01.law/0000.invariant/08.md`: cites 0000.desk-retired; 0000 is now ['invariant']; no page titled "desk-retired"
- [stale-draft] `00.00.00.syntax/0001.rules/01.006.md`: draft 006 is a copy of seat 01.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0001.rules/02.004.md`: draft 004 is a copy of seat 02.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0001.rules/03.002.md`: draft 002 is a copy of seat 03.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0001.rules/04.002.md`: draft 002 is a copy of seat 04.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0002.schema/01.004.md`: draft 004 is a copy of seat 01.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0003.operate/01.005.md`: draft 005 is a copy of seat 01.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0010.about/08.002.md`: draft 002 is a copy of seat 08.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0013.triangulate/01.002.md`: draft 002 is a copy of seat 01.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0013.triangulate/02.002.md`: draft 002 is a copy of seat 02.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0013.triangulate/03.002.md`: draft 002 is a copy of seat 03.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0013.triangulate/04.002.md`: draft 002 is a copy of seat 04.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0014.design/01.004.md`: draft 004 < seat version 006; not retired (.09)
- [stale-draft] `00.00.00.syntax/0014.design/01.005.md`: draft 005 < seat version 006; not retired (.09)
- [stale-draft] `00.00.00.syntax/0014.design/02.004.md`: draft 004 < seat version 005; not retired (.09)
- [stale-draft] `00.00.00.syntax/0014.design/02.005.md`: draft 005 is a copy of seat 02.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0014.design/03.002.md`: draft 002 < seat version 003; not retired (.09)
- [stale-draft] `00.00.00.syntax/0014.design/03.003.md`: draft 003 is a copy of seat 03.md (same version, same body): approve copied instead of renamed
- [stale-draft] `00.00.00.syntax/0014.design/04.002.md`: draft 002 < seat version 003; not retired (.09)
- [stale-draft] `00.00.00.syntax/0014.design/04.003.md`: draft 003 is a copy of seat 04.md (same version, same body): approve copied instead of renamed
- [stamp-missing] `00.00.01.law/0004.user/01.md`: missing stamp: Authorization, Face, PPPP, book, why

### info: 104 (use --all to list)

## PENDING pages
rule counts: carry-terms error=5, seat-is-draft error=16, stale-address error=9, stamp-mismatch error=2, dangling-page warn=6, order warn=31, reassigned-number warn=9, stale-address warn=1, stamp-missing warn=7, dangling-page info=3, stale-address info=6, twin-heading info=22, work-file-name info=3
(pending pages: counts only; use --all to list)
