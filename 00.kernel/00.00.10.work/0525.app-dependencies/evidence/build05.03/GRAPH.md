# Graph and source basis

Set schema `module-declaration-set/2`. Set id `accepted-loop-preflight-1`.
Set file `labs/app-dependencies-pass03/set.json` sha256 `0152daea079d887984f1548bfa13986d8f553aa74048b72ffbcfab1ff0e31082`, 11706 bytes.
Each record is `module-declaration/2`, version 1, status `prototype`, `complete_claim` false, `supersedes` null.
Positive basis is `observed-file`, form `working-tree`, `context_head` null, repository `lib-build`. A working-tree digest is the measured file. `context_head` null records that this pass stored no commit.
Home for every record is book `00.00.10.work`, page `0316.dependencies`, face `01`, file `01.001.md`.
The caller checks behind these edges are the static reading recorded in `06.05.md`. The executed reader answers are in `COMMANDS.md`.

## Records

### n7-local-workbook

- Path: `labs/n7-local-lifecycle-pass01/workbook.py`
- Bytes: 9750
- sha256: `43995fc72db252c22baeadb1e7c3b16012125eb286ce4f2356ff96e051044d2a`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `pass04-workbook` runtime-code hash-check pin pair b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2 6508 availability not-applicable condition applicable -> lib-build:labs/workbook-review-pass04/workbook.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- `pending-w` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- `pending-reporter` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- Withheld: pass05. This overlay does not pair-pin pass05. Later composition is a separate workbook.
- Provenance review 0707.app-use-check / 06.20 / 06.20.review.md sha256 `0f547990906bcf6cceef86f2f62db9906b572fde237588615c72141caf1d884e` status pinned

### review-instance-candidate-librarian

- Path: `labs/review-instance-binding-pass01/candidate/app/librarian.py`
- Bytes: 12397
- sha256: `a0de0b4fbd935e65d061836794d1d11bb19c22932d080bb9ca06a56edd947561`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `candidate-door` runtime-code dynamic-import pin unpinned availability not-applicable condition applicable -> lib-build:labs/review-instance-binding-pass01/review_loop_tools.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- Provenance review 0522.review-construction / 06.35 / 06.35.md sha256 `507b9c101c2b165ac6e7cc92e2c7909a98c2d80fed15c44bbde7b027efd2f0f2` status pinned

### review-instance-declaration

- Path: `labs/review-instance-binding-pass01/review-loop.json`
- Bytes: 5278
- sha256: `e15856d136e4721856b530a552d9115ecb1b90a62cc9905eb80d79709d2dd26f`
- Basis: observed-file, form working-tree, context_head null
- Requirements: none
- Withheld: pin enforcement. The instance door enforces the tool rows and its pin_named constants.
- Provenance review 0522.review-construction / 06.35 / 06.35.md sha256 `507b9c101c2b165ac6e7cc92e2c7909a98c2d80fed15c44bbde7b027efd2f0f2` status pinned

### review-instance-door

- Path: `labs/review-instance-binding-pass01/review_loop_tools.py`
- Bytes: 13142
- sha256: `134221019b9854bc44529ff6a909c99c464bc3515a3e39da5536b2524d00cb22`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `declaration-json` runtime-code read pin unpinned availability not-applicable condition applicable -> lib-build:labs/review-instance-binding-pass01/review-loop.json
- `instance-workbook` runtime-code hash-check pin pair 3f8118ccdc2c7afc4abdca2d52c3510864f159642ed06aee52a485709be55aba 5916 availability not-applicable condition applicable -> lib-build:labs/review-instance-binding-pass01/workbook.py
- `pass05-workbook` runtime-code hash-check pin pair 86f40268fe2f45005fd0f037f69e2d0ecb854041f6f5d59b61beeb085c09c991 6994 availability not-applicable condition applicable -> lib-build:labs/workbook-review-pass05/workbook.py
- `v9-door` runtime-code hash-check pin pair b9a8b9fe5920430b966aae761c5374aa121a060c4074f260cb4ebf89d00f4c47 11765 availability not-applicable condition applicable -> lib-build:app/review_loop_tools_v9.py
- `v9-json` runtime-code hash-check pin pair f22063a0e4e5648ba8f018ee252f52b726480b0a1b39f2332611f6dd8b408656 4670 availability not-applicable condition applicable -> lib-build:app/review-loop-v9.json
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- `pending-w` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- `pending-reporter` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- Withheld: historical door pins. pin_named checks for v4 through v8 and pass01 through pass04 are outside this subset
- Provenance review 0522.review-construction / 06.35 / 06.35.md sha256 `507b9c101c2b165ac6e7cc92e2c7909a98c2d80fed15c44bbde7b027efd2f0f2` status pinned

### review-instance-workbook

- Path: `labs/review-instance-binding-pass01/workbook.py`
- Bytes: 5916
- sha256: `3f8118ccdc2c7afc4abdca2d52c3510864f159642ed06aee52a485709be55aba`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `pass05-workbook` runtime-code hash-check pin pair 86f40268fe2f45005fd0f037f69e2d0ecb854041f6f5d59b61beeb085c09c991 6994 availability not-applicable condition applicable -> lib-build:labs/workbook-review-pass05/workbook.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- Provenance review 0522.review-construction / 06.35 / 06.35.md sha256 `507b9c101c2b165ac6e7cc92e2c7909a98c2d80fed15c44bbde7b027efd2f0f2` status pinned

### review-loop-declaration-v9

- Path: `app/review-loop-v9.json`
- Bytes: 4670
- sha256: `f22063a0e4e5648ba8f018ee252f52b726480b0a1b39f2332611f6dd8b408656`
- Basis: observed-file, form working-tree, context_head null
- Requirements: none
- Withheld: pin enforcement. The v9 door enforces the tool rows. This file does not enforce them.
- Provenance review 0522.review-construction / 06.33 / 06.33.md sha256 `debbb40515843cd37ffa11e6da8ef75d0159793fa337c0dcd14a3f939464453b` status pinned

### review-loop-door-v9

- Path: `app/review_loop_tools_v9.py`
- Bytes: 11765
- sha256: `b9a8b9fe5920430b966aae761c5374aa121a060c4074f260cb4ebf89d00f4c47`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `declaration-json` runtime-code read pin unpinned availability not-applicable condition applicable -> lib-build:app/review-loop-v9.json
- `pass05-workbook` runtime-code hash-check pin pair 86f40268fe2f45005fd0f037f69e2d0ecb854041f6f5d59b61beeb085c09c991 6994 availability not-applicable condition applicable -> lib-build:labs/workbook-review-pass05/workbook.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `pending-w` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- `pending-reporter` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- Withheld: historical door pins. pin_named checks for v4 through v8 and pass01 through pass04 are outside this subset
- Provenance review 0522.review-construction / 06.33 / 06.33.md sha256 `debbb40515843cd37ffa11e6da8ef75d0159793fa337c0dcd14a3f939464453b` status pinned

### review-report-hardening

- Path: `labs/review-report-hardening-pass01/report.py`
- Bytes: 18139
- sha256: `27e513f462b241e9c7298d3077d50d08ea5ac703a6f2d0769dc5935fcb51b58b`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `helper-pass03` runtime-code hash-check pin pair 9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c 19533 availability not-applicable condition applicable -> lib-build:labs/workbook-review-pass03/workbook.py
- `selected-app-pin` runtime-code hash-check pin pair f1d23d455f20319e3f430d345b2893bda039fd8c84be4f3691b4e4be123b8983 12804 availability not-applicable condition applicable -> lib-build:app/librarian.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- Withheld: remaining PINS rows. The rest of the PINS table is outside this subset.
- Withheld: hardening librarian. labs/review-report-hardening-pass01/librarian.py is another unselected dispatcher and is not reporter-on-W.
- Provenance source-stated 0420.prime-desk / 06.56 / 06.56.md sha256 `7948480497821a986eecd5413b85747893e90e50c025512f369150fd2ca5b39a` status pinned

### selected-app-librarian

- Path: `app/librarian.py`
- Bytes: 12204
- sha256: `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `selected-v7` runtime-code dynamic-import pin unpinned availability not-applicable condition applicable -> lib-build:app/review_loop_tools_v7.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- Withheld: other app commands. authoring, return-lines, and the rest of the dispatcher are outside this preflight
- Provenance review 0522.review-construction / 06.35 / 06.35.md sha256 `507b9c101c2b165ac6e7cc92e2c7909a98c2d80fed15c44bbde7b027efd2f0f2` status pinned
- Provenance source-stated 0420.prime-desk / 06.56 / 06.56.md sha256 `7948480497821a986eecd5413b85747893e90e50c025512f369150fd2ca5b39a` status pinned

### selected-review-loop-v7

- Path: `app/review_loop_tools_v7.py`
- Bytes: 10291
- sha256: `93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- Withheld: predecessor pin fan-out. v7 internal pins are outside this subset
- Provenance review 0522.review-construction / 06.33 / 06.33.md sha256 `debbb40515843cd37ffa11e6da8ef75d0159793fa337c0dcd14a3f939464453b` status pinned

### source-capacity-declaration

- Path: `labs/review-source-capacity-pass03/review-loop-source-capacity-v3.json`
- Bytes: 5052
- sha256: `e79c93ef29b04ed810b4fa31efeaf6c9a28dd9957f3bb5d4a4e6ed74b3f90b9c`
- Basis: observed-file, form working-tree, context_head null
- Requirements: none
- Withheld: pin enforcement. The capacity door enforces the tool rows.
- Provenance review 0512.prime-review / 06.22 / 06.22.md sha256 `b3bf76d560457f438d78243c0cff8d2ac90d115ac3a6fa53ec71956547be5e2a` status pinned

### source-capacity-door

- Path: `labs/review-source-capacity-pass03/review_loop_tools_source_capacity_v3.py`
- Bytes: 11744
- sha256: `8df0253100fe0b5bd68a5e4f645322a44d3870b5f583af35e0e0aee75bc280eb`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `declaration-json` runtime-code read pin unpinned availability not-applicable condition applicable -> lib-build:labs/review-source-capacity-pass03/review-loop-source-capacity-v3.json
- `capacity-workbook` runtime-code hash-check pin pair fe887c0f378fc1da3f5e778ac4642c907f713614040d5ebf3b74272b02512b1f 3126 availability not-applicable condition applicable -> lib-build:labs/review-source-capacity-pass03/workbook.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `pending-w` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- `pending-reporter` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- Withheld: historical door pins. pin_named checks for v4 through v7, pass01, pass02, and earlier capacity prime_review files are outside this subset
- Provenance review 0512.prime-review / 06.22 / 06.22.md sha256 `b3bf76d560457f438d78243c0cff8d2ac90d115ac3a6fa53ec71956547be5e2a` status pinned

### source-capacity-prime-review

- Path: `labs/review-source-capacity-pass03/prime_review.py`
- Bytes: 6136
- sha256: `c15cbd2460200583cab0518e2ac16f4a95356a779edb4b1978dfb4afc2a3e7ab`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- Withheld: predecessor pins. pair pins of labs/prime-review-pass02/prime_review.py and the capacity pass01 and pass02 prime_review files are outside this subset
- Provenance review 0512.prime-review / 06.22 / 06.22.md sha256 `b3bf76d560457f438d78243c0cff8d2ac90d115ac3a6fa53ec71956547be5e2a` status pinned

### source-capacity-workbook

- Path: `labs/review-source-capacity-pass03/workbook.py`
- Bytes: 3126
- sha256: `fe887c0f378fc1da3f5e778ac4642c907f713614040d5ebf3b74272b02512b1f`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `pass03-workbook` runtime-code hash-check pin pair 9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c 19533 availability not-applicable condition applicable -> lib-build:labs/workbook-review-pass03/workbook.py
- `capacity-validator` runtime-code hash-check pin pair c15cbd2460200583cab0518e2ac16f4a95356a779edb4b1978dfb4afc2a3e7ab 6136 availability not-applicable condition applicable -> lib-build:labs/review-source-capacity-pass03/prime_review.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- `pending-w` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- `pending-reporter` evidence document pin unpinned availability not-applicable condition unknown -> 00.00.10.work / 0420.prime-desk / 06.56 / 06.56.md
- Provenance review 0512.prime-review / 06.22 / 06.22.md sha256 `b3bf76d560457f438d78243c0cff8d2ac90d115ac3a6fa53ec71956547be5e2a` status pinned

### workbook-review-pass03

- Path: `labs/workbook-review-pass03/workbook.py`
- Bytes: 19533
- sha256: `9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- Withheld: pass02 load. pass03 loads pass02 from the helper root. That edge is outside this subset.
- Provenance review 0512.prime-review / 06.22 / 06.22.md sha256 `b3bf76d560457f438d78243c0cff8d2ac90d115ac3a6fa53ec71956547be5e2a` status pinned

### workbook-review-pass04

- Path: `labs/workbook-review-pass04/workbook.py`
- Bytes: 6508
- sha256: `b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `pass03-workbook` runtime-code hash-check pin pair 9e66d7e4413e8f0aedcc4ff416080c549ce435b10103149ef73de493b245ff8c 19533 availability not-applicable condition applicable -> lib-build:labs/workbook-review-pass03/workbook.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- Provenance review 0522.review-construction / 06.33 / 06.33.md sha256 `debbb40515843cd37ffa11e6da8ef75d0159793fa337c0dcd14a3f939464453b` status pinned

### workbook-review-pass05

- Path: `labs/workbook-review-pass05/workbook.py`
- Bytes: 6994
- sha256: `86f40268fe2f45005fd0f037f69e2d0ecb854041f6f5d59b61beeb085c09c991`
- Basis: observed-file, form working-tree, context_head null
- Requirements: listed
- `pass04-workbook` runtime-code hash-check pin pair b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2 6508 availability not-applicable condition applicable -> lib-build:labs/workbook-review-pass04/workbook.py
- `python` environment path-reference pin unpinned availability unverified condition applicable -> environment:python
- `canonical-helper-root` environment path-reference pin unpinned availability unverified condition applicable -> environment:canonical-helper-root
- Provenance review 0522.review-construction / 06.33 / 06.33.md sha256 `debbb40515843cd37ffa11e6da8ef75d0159793fa337c0dcd14a3f939464453b` status pinned
