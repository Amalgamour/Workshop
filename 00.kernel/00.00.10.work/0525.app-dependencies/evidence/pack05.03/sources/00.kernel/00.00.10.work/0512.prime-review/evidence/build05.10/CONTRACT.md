# Contract - source capacity before activation

contract: review-source-capacity/1
date: 2026-11-04
executor: Grok-1
reviewer: Codex Prime
accepted: false
activated: false
state: locked pre-code contract, restated at filing

The locked pre-code contract is 00.kernel/00.00.10.work/0512.prime-review/06.17.md. Its body before the reread is sha256 60ff7af4b26cef53a1de421678d14a2e4e452d2eb48c3ac475d026cf27db8faf, 7516 bytes. One sentence in that body was corrected before any author run, so the adapter root is Path(__file__).resolve().parents[2]. The body was not revised after the first author failure and was not revised after the passing run. This file restates those rules for the return. It does not add a repair rule.

## Freeze

evidence/pack05.10/source-manifest.json was verified before the notes and again at filing. Schema prime-pack-inputs/1. 148 files. bad 0. missing live 0. missing snapshot 0. Manifest sha256 eb9e173cbddd476b8c8bc608c5ca21599413c8ef4ea7720933508b28d3a14c6e, 44512 bytes. The only extra top-level key is prepared. 05.10.md is outside that manifest. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. Index empty.

## Bound

MAX_SOURCES = 32 applies only when as_list is called with where == "sources". MAX_LIST stays 24 for every other list. MAX_DOC stays 262144. MAX_TEXT stays 12000. MAX_INDEX stays 12 and bounds form cuts only. A count above 32 is refused before publication with the actual count, the supported limit, and this next step: split the return so one record binds at most 32 sources. The refusal text is `limit sources: N sources exceeds supported limit 32; split the return so one record binds at most 32 sources`. A document above 262144 bytes still uses `input: input exceeds 262144 bytes`, including when the source count is 32 or below. Ordinary records of 24 or fewer sources keep the historical report. The measured 05.09 document is 125955 bytes, so the count repair covers that return. There is no source-representation or authority fork in this measurement.

## Shape

The production proposal is labs/review-source-capacity-pass01/prime_review.py. It loads labs/prime-review-pass02/prime_review.py by hash 80836a13278365de863ed8231cb8118ad14ddbad672dd02ec2ebf69beff3b44e, 58560 bytes, and rebinds as_list. It does not assign MAX_LIST.

The lab adapter is labs/review-source-capacity-pass01/workbook.py. It loads labs/workbook-review-pass03/workbook.py by hash 9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c, 19533 bytes, from helper root D:\Git\lib-build, then sets the pass01 REPO to the tree root that contains app/ and labs/. In the proof tree that root omits 00.kernel/00.00.10.work. The adapter points pin_file("prime_review") at the sibling successor after a hash check. Its bytes are distinct from the successor. historical_replay.py leaves the historical prime_review pin in place.

The candidate app tree is labs/review-source-capacity-pass01/candidate. It is unselected and uninstalled. The active app/librarian.py stays sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes.

## Proof already required by the notes

External copies of 0512.prime-review and 0522.review-construction keep original bytes and declared paths. Historical replay of 0512/05.09 records exit 2 with `refused: limit sources`. The candidate then prepares, forms, records the retained judgment, inspects, reads, publishes separately, and recovers in a new process. Recovered judgment and next action equal the input. The prefix before the review heading stays byte-identical. 0512/05.09 binds 29 sources. 0522/05.14 binds 20. Publication of these returns is preliminary. Cycle called and committed stay false. Custody stays missing. 0112 and 0122 stay unfiled. An occupied review section is left unchanged.
