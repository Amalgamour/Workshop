# Integration - source-capacity 64 candidate

accepted: false
applied: false
state: unapplied candidate bytes

## What a later selection would change

This pack does not apply that selection.

One existing file would change. app/librarian.py would be replaced by labs/review-source-capacity-pass02/candidate/app/librarian.py, 12246 bytes, sha256 a4e0ec03095a43291a997fbf9e9899f89409863a3df718c7ba9e219ed63ea6bf.
The working copy differs from the active file in two substitutions: the review-loop sentence names the source-capacity-64 door, and the review-loop load names app/review_loop_tools_source_capacity_v2.py.

These new files would have to remain at the declared paths:

- app/review_loop_tools_source_capacity_v2.py, 11355 bytes, sha256 78815b908c22618fe2ab85b9dbe9a3cd4aa534f7c3a9b2afc35bf986ad192d6c
- app/review-loop-source-capacity-v2.json, 4753 bytes, sha256 c64a83f82331fb89d405aa93bf9707fdf913366d241c313b764d8bdcf91906cd
- labs/review-source-capacity-pass02/prime_review.py, 2160 bytes, sha256 32567d68ccd6dc838c175af078610c53e4ec777d7c2f5eddb9d6ea8ea9c4644f

The production pin for prime_review names that successor.
The successor loads the historical pass02 module by the pinned hash and rebinds as_list for sources only.

## Adapter and proof tree

labs/review-source-capacity-pass02/workbook.py, 3119 bytes, sha256 41ef1f5448215bc763648219a5a7b2ba75ade86818734adef6edea6659eff38d, is the lab adapter.
The candidate declaration points its workbook tool at that adapter so the proof can set REPO to the candidate root and redirect pin_file("prime_review") to the successor.
The proof candidate omits 00.kernel/00.00.10.work. That omitted tree is the proof root. It is not the checkout to install.
historical_replay.py leaves the historical prime_review pin in place.
predecessor_replay.py points that pin at the byte-copied pass01 successor.
Helper root D:\Git\lib-build remains the place the adapter loads pass03, and the place the successor loads pass02.

## Verify before any later apply

Confirm app/librarian.py is sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes.
Confirm the successor, the door, and the declaration match the hashes above.
Confirm evidence/build05.11/pin-delta.json. If any of those bytes differ, stop.
Also confirm whether the return being recorded has any source content_bytes above 262144.
The 64-source bound does not make that field valid.

## Rollback

Restore app/librarian.py from evidence/build05.11/rollback-librarian.py.
That file is the active librarian, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes.
Leave the new files on disk. The restored v7 door does not load them.
A later record through pass02 refuses the 44-source return at `limit sources` again.
The pass01 successor still refuses it at 32.
This successor still refuses it at content_bytes 276423.
This pack does not claim those pins accept a published 05.10 review.
