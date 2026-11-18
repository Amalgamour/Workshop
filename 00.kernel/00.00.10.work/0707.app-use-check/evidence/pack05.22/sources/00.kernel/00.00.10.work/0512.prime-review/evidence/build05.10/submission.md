# Submission - 0512.prime-review/05.10

date: 2026-11-04
executor: Grok-1
reviewer: Codex Prime
accepted: false
committed_by_this_builder: false
custody: pending
matching line: 0112.prime-review unfiled
readiness: returned for Codex Prime review

This is the builder return for the named invocation of 05.10. It is a claim. It is not acceptance, custody, or a release. The notes in 06.17.md were reread after the author suite. The contract body was corrected once before any author run and was not revised after the passing run. This file does not carry the artifact-manifest hash. That hash is written only on the 05.10 return pointer after the manifest exists.

## Did

Verified evidence/pack05.10/source-manifest.json before the notes and again before this filing. Schema prime-pack-inputs/1. 148 files. bad 0. missing live 0. missing snapshot 0. Manifest sha256 eb9e173cbddd476b8c8bc608c5ca21599413c8ef4ea7720933508b28d3a14c6e, 44512 bytes. 05.10.md is outside that manifest. HEAD 960d20c5290656095df8457b1740d2d5e586b111. Branch workshop. Index empty. The worktree already had other dirty paths. They were left in place. The freeze was not repinned.

Read 06.16.md and both frozen core records. The frozen live record of 0512/05.09 exits 2 with correction `refused: limit sources`. The retained judgment stays evidence/prime-review05.09/core-review/judgment.json. A read-only measurement wrote source-measurement.json. 0512/05.09 emits 29 sources in a 125955-byte document. 0522/05.14 emits 20 sources in a 62200-byte document. Artifact rows are a different count from emitted sources. The rejecting bound is MAX_LIST = 24 on the source list. MAX_DOC, MAX_TEXT, MAX_INDEX, and the other list limits stay as they were.

The first external copy, book D:\librarian\temp\0512-0510-report\books\g1-0509, did not reach the capacity refusal. locate_declared found work-prefixed artifacts on the copy and again on the helper, so record returned `The artifact measurement is incomplete. The judgment was not recorded.` Those logs are known-reproductions. The capacity refusal was then reproduced by historical_replay.py on a candidate root that omits 00.kernel. That record exits 2 with `refused: limit sources`. The author suite repeated it on books/author-hist-0509. Both logs are in this return.

The successor is labs/review-source-capacity-pass01/prime_review.py, sha256 a12b88958dcf2aea0fdc4c83f30c245b0f7f91d6ddf7c515bf31c7119c01fa87, 2031 bytes. MAX_SOURCES = 32 applies only to sources. The lab adapter is workbook.py, sha256 7383e6ec4e5bf7909f069796a7fe6c71e23b6f241edec64fc3805656174a742e, 3055 bytes. The candidate librarian is sha256 d2d7f7a3e25b435708f3f05a7c84a7b0d56e095758e8309237f53a25c1cb9bf4, 12237 bytes. The declaration is sha256 3a47008e03bae8f8b580fb903514fc98d4683a5e48401f44b2c454d63aa094b5, 4319 bytes. The door is sha256 cde90e02250d1f56c38a0b249bcfd1bcef15d6e3899d2f71375e9a900ab0fd3a, 11018 bytes. Helper root D:\Git\lib-build is disclosed. The active app/librarian.py stayed sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. app/README.md stayed sha256 3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920, 39687 bytes, which is the digest the passing author results recorded.

The author cycle on a fresh copy of 0512/05.09 ran prepare, form, record, inspect, read, a separate publish, and a new-process recover through the candidate librarian. Sources 29. Prime-input 125955 bytes, sha256 d4696fc278e17411b0db1ab785a3bd419f5d17d66dc53685b0bf091cca6339c2. Review wa625af81adaf35cd. Mode preliminary. Custody missing. Cycle called false and committed false. accepted false. authority none. published_work false. Publish set published true. Recover target_state section-verified, record_ok true, stale false. Finding and next action equal the retained judgment. The prefix before the review heading equals the live page. The same cycle on 0522/05.14 recorded 20 sources and a 62200-byte prime-input, sha256 4a2dd8e043daf0293a404301442c577afb5bc6bfe763a675ac13db511077a4cd. Review wcfa3cd82d3322f65. Publish returned `stale-own-review` because the copied section already holds wb980a2a872c7e7c7. The page bytes stayed equal to the live page. Recover target_state not-published, with the new judgment and next action retained and custody missing.

The passing author suite was 18 tests, 62.369 seconds, OK, exit 0, Python 3.14.0. The first failure log remains author-suite-first.txt, sha256 2bb81350963d423c9643fe8d0d17050b607e8905c794f5c18fa5c3784910b1e8, 3344 bytes. The pre-code contract digest before the reread is sha256 60ff7af4b26cef53a1de421678d14a2e4e452d2eb48c3ac475d026cf27db8faf, 7516 bytes.

## Blocked

Matching line 0112.prime-review is unfiled. This slice does not file it and does not invent a receipt. Custody on these returns stays missing. The candidate is unselected. Codex Prime has not reviewed this pack. This builder does not commit. The occupied 0522/05.14 review section stays occupied. N7 grammar and the first-target repair stay outside this pack. A source count above 32, or a document above 262144 bytes, is still refused.

## Need

Codex Prime review of this return. The candidate command, the pin list, and the rollback are in PRIME-USE.md and INTEGRATION.md. Stop here.

## Claim, case, result, limit

The table is TEST-TABLE.md. The bounds are bounds.md. The pin delta is pin-delta.json. The commands are command-log.json. The candidate file list is candidate-index.json. The source rows are source-bindings.json, and the full prime-input documents are bindings/0509-prime-input.json and bindings/0514-prime-input.json. The locked rules are CONTRACT.md and 06.17.md.

## Factfind, hostile, overflow, unprompted

Factfind: 36 artifact rows on the 05.09 return are not 29 emitted sources. Seven inline records on that return, and eleven on the 05.14 return, are null because the decoded text is outside MAX_TEXT. That omission is the historical source row. The artifact-manifest role is measured and is not emitted. Code-root rows are measured and are not emitted. index-context-bounded does not by itself make measurement incomplete. The author record of 05.09 lists six agreement fields as unknown. That attention is the historical gap on a page whose agreement is null. The naive copy failure and the capacity refusal are different logs, and both are kept.

Hostile: a 33-long source list that repeats one path is refused with the count 33. A 276423-byte document of 22 sources is refused with `input: input exceeds 262144 bytes`. A changed or missing artifact before record leaves the judgment unrecorded. A changed or deleted artifact after record makes read stale and still returns the stored finding. A wrong successor hash stops with `pinned tool hash does not match: labs/review-source-capacity-pass01/prime_review.py`. A wrong pass02 workbook byte stops with `pass02 pin mismatch`. A junction under the candidate labs path stops with `tool path is linked and was not followed`.

Overflow: none. The emitted source identities, hashes, and byte sizes are in source-bindings.json. The inline texts that fit MAX_TEXT are in the copied prime-input files. No source was sampled out of the record to make the count fit.

Unprompted: the suite compares app/README.md. The root README.md is a different file and was not the compared surface. Git porcelain was already dirty and was not cleaned. v8 and the other 05.14 code artifacts were copied into the candidate by hash so the declared paths resolve. They were not read as the design of this door. The post-filing suite log stays outside the sealed manifest.
