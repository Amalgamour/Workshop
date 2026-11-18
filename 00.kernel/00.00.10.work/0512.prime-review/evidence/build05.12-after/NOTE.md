# Post-filing supplement - 05.12

This directory sits outside the sealed artifact manifest. The sealed return, 06.21.md, and the 05.12 return pointer stay as filed.

The author suite ran again after the return pointer was filed. 30 tests, 137.874 seconds, OK, exit 0. The log is author-suite.txt, sha256 6156d959c031356406c2ac53c1dc9951b8f3a302ee5550b458c6ed436eeea645, 3147 bytes, CR 0. The sealed pre-filing log stays in evidence/build05.12/author-suite.txt (30 tests, 52.854 seconds, OK).

A prepare-only probe copied the live 0512.prime-review tree into D:\librarian\temp\0512-0512-report\books\probe-0512 and ran the candidate librarian with the working directory set to labs/review-source-capacity-pass03/candidate:

```
python -B app/librarian.py review-loop prepare --book D:\librarian\temp\0512-0512-report\books\probe-0512 --source 0512.prime-review --pass 05.12
```

Exit 0. Stderr was empty. Measurement is incomplete. The command was prepare. Record and publish stayed unused. No Prime judgment for 05.12 was supplied. accepted, approved, closes_work, published_work, and releases_action are false. authority is none. custody is missing. The live page has no workbook-review directory. The external probe book contains no workbook-review directory.

Measured rows: 52. Unique paths: 51. Roles: assignment 1, submission 1, artifact-manifest 1, artifact 49. Roots: book 50, code 2. The largest measured row is 137328 bytes at 0512.prime-review/evidence/build05.12/bindings/0510-prime-input.json (root book, sha256 79bdae35350bf05319c632b416b882b07a607aa2954512bd2b119f7c89fb95b1). That file is the sealed 05.10 prime-input binding. Its length is within the JSON document cap of 262144 and within the referenced-source cap of 16777216. This prepare does not record the 05.12 return.

Duplicate measured path: 0512.prime-review/evidence/build05.12/submission.md. One row has the submission role and one has the artifact role. Both rows carry sha256 ca0701cbe5ea59ef51f751d1379f11ee081f3234fe1d24d7408551ca77aa0d14.

Findings:

- verification-not-measured: 00.kernel/00.00.10.work/0512.prime-review/evidence/build05.12/submission.md
- index-context-bounded: count 60, path 00.kernel/00.00.10.work/0512.prime-review/evidence/build05.12/artifact-manifest.json
- artifact-missing: labs/review-source-capacity-pass03/build_candidate.py
- artifact-missing: labs/review-source-capacity-pass03/candidate-build.json
- artifact-missing: labs/review-source-capacity-pass03/candidate/app/librarian.py
- artifact-missing: labs/review-source-capacity-pass03/candidate/app/review-loop-source-capacity-v3.json
- artifact-missing: labs/review-source-capacity-pass03/candidate/app/review_loop_tools_source_capacity_v3.py
- artifact-missing: labs/review-source-capacity-pass03/capacity64_replay.py
- artifact-missing: labs/review-source-capacity-pass03/historical_replay.py
- artifact-missing: labs/review-source-capacity-pass03/predecessor_replay.py
- artifact-missing: labs/review-source-capacity-pass03/review-loop-source-capacity-v3.json
- artifact-missing: labs/review-source-capacity-pass03/review_loop_tools_source_capacity_v3.py
- artifact-missing: labs/review-source-capacity-pass03/tests/test_capacity.py
- custody-missing: 0112.prime-review
- return-missing: 0112.prime-review/05.12.return.md

The top-level missing list is empty. Unknowns are agreement.goal, agreement.scope, recorded_decisions, and receipt.

Two declared code-root rows resolved from the candidate root, with hashes matching the sealed manifest:

- labs/review-source-capacity-pass03/prime_review.py: 6136 bytes, sha256 c15cbd2460200583cab0518e2ac16f4a95356a779edb4b1978dfb4afc2a3e7ab
- labs/review-source-capacity-pass03/workbook.py: 3126 bytes, sha256 fe887c0f378fc1da3f5e778ac4642c907f713614040d5ebf3b74272b02512b1f

Eleven artifact-missing paths are present in the checkout and match the sealed manifest. Each declared path is absent when resolved from the candidate root. The three candidate/app files are present in the candidate at app/ relative paths, and those bytes match the manifest. Prepare looked up the declared labs/review-source-capacity-pass03/candidate/app/ paths and did not find them. The sealed manifest still lists all eleven. This supplement leaves those listings in place.

- labs/review-source-capacity-pass03/build_candidate.py: checkout 9027 bytes, sha256 37075262474cb319b104c8289ffa6d29e16b069c9137910bd767f04078960ed6, absent at that declared path on the candidate root.
- labs/review-source-capacity-pass03/candidate-build.json: checkout 11838 bytes, sha256 b1ed0403f0329a8ed60d51d7eca69f5f06ae8f269712ca1eb6c9c2d303887cc4, absent at that declared path on the candidate root.
- labs/review-source-capacity-pass03/candidate/app/librarian.py: checkout 12249 bytes, sha256 82935705ffc900ffa288d96b8d331b633bcce9004e5f0982e0acf3a884b9921c, absent at that declared path on the candidate root. Candidate holds app/librarian.py (12249 bytes, sha256 82935705ffc900ffa288d96b8d331b633bcce9004e5f0982e0acf3a884b9921c, bytes match the manifest).
- labs/review-source-capacity-pass03/candidate/app/review-loop-source-capacity-v3.json: checkout 5052 bytes, sha256 e79c93ef29b04ed810b4fa31efeaf6c9a28dd9957f3bb5d4a4e6ed74b3f90b9c, absent at that declared path on the candidate root. Candidate holds app/review-loop-source-capacity-v3.json (5052 bytes, sha256 e79c93ef29b04ed810b4fa31efeaf6c9a28dd9957f3bb5d4a4e6ed74b3f90b9c, bytes match the manifest).
- labs/review-source-capacity-pass03/candidate/app/review_loop_tools_source_capacity_v3.py: checkout 11744 bytes, sha256 8df0253100fe0b5bd68a5e4f645322a44d3870b5f583af35e0e0aee75bc280eb, absent at that declared path on the candidate root. Candidate holds app/review_loop_tools_source_capacity_v3.py (11744 bytes, sha256 8df0253100fe0b5bd68a5e4f645322a44d3870b5f583af35e0e0aee75bc280eb, bytes match the manifest).
- labs/review-source-capacity-pass03/capacity64_replay.py: checkout 2485 bytes, sha256 3dca5797eab0410d2b3190faaca37973d989b92ead3a552e3fedca342021ce25, absent at that declared path on the candidate root.
- labs/review-source-capacity-pass03/historical_replay.py: checkout 1815 bytes, sha256 1975dabe626e466c50dd030210e29ea9dc6f27b6ce98d3ade439ba9dce2de45b, absent at that declared path on the candidate root.
- labs/review-source-capacity-pass03/predecessor_replay.py: checkout 2405 bytes, sha256 6a83c9d1b81dc3cb80d805f0ff3fc3e26a8044ffbf9a06906b9ddc4120c25083, absent at that declared path on the candidate root.
- labs/review-source-capacity-pass03/review-loop-source-capacity-v3.json: checkout 5052 bytes, sha256 e79c93ef29b04ed810b4fa31efeaf6c9a28dd9957f3bb5d4a4e6ed74b3f90b9c, absent at that declared path on the candidate root.
- labs/review-source-capacity-pass03/review_loop_tools_source_capacity_v3.py: checkout 11744 bytes, sha256 8df0253100fe0b5bd68a5e4f645322a44d3870b5f583af35e0e0aee75bc280eb, absent at that declared path on the candidate root.
- labs/review-source-capacity-pass03/tests/test_capacity.py: checkout 74703 bytes, sha256 9007b661ef688d5ad4ee7661a040b1b7be7583bef6b86eaa2302e2cfc1e706b9, absent at that declared path on the candidate root.

index-context-bounded names the sealed artifact manifest and count 60, the manifest's own file count. verification-not-measured names the sealed submission. custody-missing and return-missing name 0112.prime-review, which stays unfiled.

The proven record remains the open 05.10 judgment on the pass03 candidate, already sealed: 44 sources, document 137328 bytes, external content_bytes 276423, inline record null, review wa7922b9b4f84d400. This prepare is a separate measurement of the filed 05.12 return, and that measurement is incomplete.

Row detail is new-return-count.json.
