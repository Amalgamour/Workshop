# Pins

The door declaration is schema `review-loop-pins/8`. Its workbook pin is the candidate workbook. Pass05, pass04, pass03, pass02, pass01, and v4 through v9 stay at the hashes in `review-loop.json`. The door's `pin_predecessors` repeats those predecessor hashes and refuses before `workbook_call`.

Candidate workbook `3f8118ccdc2c7afc4abdca2d52c3510864f159642ed06aee52a485709be55aba`, 5916 bytes. It pins pass05 `86f40268fe2f45005fd0f037f69e2d0ecb854041f6f5d59b61beeb085c09c991`, 6994 bytes, and reads that pin only after the canonical-path check.

There is no lab root adapter. A copied workbook or door is a different path and exits 2. Matching bytes under another root are not treated as this candidate.

`candidate/app/librarian.py` is a real copy of `app/librarian.py` with the review-loop branch loading `labs/review-instance-binding-pass01/review_loop_tools.py` and passing `D:\Git\lib-build` as code_root. Hash `a0de0b4fbd935e65d061836794d1d11bb19c22932d080bb9ca06a56edd947561`, 12397 bytes. The suite executed that file. It did not execute the production librarian bytes under an eval that pretends they are this candidate.
