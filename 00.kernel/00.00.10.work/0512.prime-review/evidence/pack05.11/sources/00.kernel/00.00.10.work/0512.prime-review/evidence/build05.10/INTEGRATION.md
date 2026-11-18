# Integration - source-capacity candidate

accepted: false
applied: false
state: unapplied candidate bytes

## What a later selection would change

This pack does not apply that selection.

One existing file would change. app/librarian.py would be replaced by labs/review-source-capacity-pass01/candidate/app/librarian.py, 12237 bytes, sha256 d2d7f7a3e25b435708f3f05a7c84a7b0d56e095758e8309237f53a25c1cb9bf4. The working copy differs from the active file in two substitutions: the review-loop docstring names the source-capacity door, and the review-loop load names app/review_loop_tools_source_capacity.py.

These new files would have to remain at the declared paths:

- app/review_loop_tools_source_capacity.py, 11018 bytes, sha256 cde90e02250d1f56c38a0b249bcfd1bcef15d6e3899d2f71375e9a900ab0fd3a
- app/review-loop-source-capacity.json, 4319 bytes, sha256 3a47008e03bae8f8b580fb903514fc98d4683a5e48401f44b2c454d63aa094b5
- labs/review-source-capacity-pass01/prime_review.py, 2031 bytes, sha256 a12b88958dcf2aea0fdc4c83f30c245b0f7f91d6ddf7c515bf31c7119c01fa87

The production pin for prime_review names that successor. The successor loads the historical pass02 module by the pinned hash and rebinds as_list for sources only.

## Adapter and proof tree

labs/review-source-capacity-pass01/workbook.py, 3055 bytes, sha256 7383e6ec4e5bf7909f069796a7fe6c71e23b6f241edec64fc3805656174a742e, is the lab adapter. The candidate declaration points its workbook tool at that adapter so the proof can set REPO to the candidate root and redirect pin_file("prime_review") to the successor. The proof candidate omits 00.kernel/00.00.10.work, which keeps a copied book path from also resolving on the helper. That omitted tree is the proof root. It is not the checkout to install.

Helper root D:\Git\lib-build remains the place the adapter loads pass03, and the place the successor loads pass02. Those historical files stay byte-identical. The fixed helper and the copied book stay distinct.

historical_replay.py, 1824 bytes, sha256 62f9c466b2f8e0df1ae900936377c802a712d99bce8c6ee1902b0c817eafa33b, is the known-reproduction entry. It sets the same REPO and leaves the historical prime_review pin in place.

## Verify before any later apply

Confirm app/librarian.py is sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Confirm the successor, the door, and the declaration match the hashes above. Confirm evidence/build05.10/pin-delta.json. If any of those bytes differ, stop.

## Rollback

Restore app/librarian.py from evidence/build05.10/rollback-librarian.py. That file is the active librarian, sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Leave the new files on disk. The restored v7 door does not load them. A later record of the 29-source 0512/05.09 return through pass02 refuses `limit sources` again. v7, pass02, and pass03 stay the historical pins. This pack does not claim those pins accept the successor.
