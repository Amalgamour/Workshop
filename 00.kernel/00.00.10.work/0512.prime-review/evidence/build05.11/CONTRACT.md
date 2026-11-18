# Contract - 05.11 source capacity 64

accepted: false
state: candidate unselected

MAX_SOURCES is 64 and applies only when as_list is called with where == sources.
MAX_LIST stays 24. MAX_DOC stays 262144. MAX_TEXT stays 12000.
The successor does not assign MAX_LIST.
A count above 64 is refused with the actual count, the limit 64, and this next step: keep every source identity on this record and stop for a versioned successor whose source bound covers the count.
That sentence does not say to split, drop, or rewrite the return.
The pass01 successor stays at 32 and still refuses 33 and the 44-source return with its own split sentence.
The historical pin still refuses 25 sources with `refused: limit sources`.
Holds and answers of 25 still refuse `limit holds` and `limit answers`.
A document above 262144 bytes still refuses `input: input exceeds 262144 bytes` when the source count is within 64.
The historical count() ceiling also refuses a source content_bytes value above 262144.
The observed 05.10 return emits 44 sources in a 137328-byte prime-input.
Source 24 is 0512.prime-review/evidence/build05.10/hostile/over-document.json at 276423 bytes, with a null inline record.
The candidate record of the open judgment therefore stops at `refused: limit sources[24].content_bytes`.
The finished-pass judgment still stops earlier at `a held review keeps the pass and the goal open`.
This pack does not raise MAX_DOC and does not drop that check.

Successor labs/review-source-capacity-pass02/prime_review.py sha256 32567d68ccd6dc838c175af078610c53e4ec777d7c2f5eddb9d6ea8ea9c4644f, 2160 bytes.
Adapter workbook.py sha256 41ef1f5448215bc763648219a5a7b2ba75ade86818734adef6edea6659eff38d, 3119 bytes.
Door review_loop_tools_source_capacity_v2.py sha256 78815b908c22618fe2ab85b9dbe9a3cd4aa534f7c3a9b2afc35bf986ad192d6c, 11355 bytes.
Declaration review-loop-source-capacity-v2.json sha256 c64a83f82331fb89d405aa93bf9707fdf913366d241c313b764d8bdcf91906cd, 4753 bytes. Schema review-loop-source-capacity/2.
Candidate librarian sha256 a4e0ec03095a43291a997fbf9e9899f89409863a3df718c7ba9e219ed63ea6bf, 12246 bytes.
Helper root D:\Git\lib-build loads the historical modules by hash.
The candidate root omits 00.kernel/00.00.10.work.
The active app and the pass01 lab stay on their pins.
