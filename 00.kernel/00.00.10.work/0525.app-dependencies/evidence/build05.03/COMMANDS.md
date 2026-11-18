# Commands, exits, and provenance

## Static

`06.05.md` records the caller reading done before the lab. Pair means the caller compares sha256 and byte length. The selected app load of v7, the inert candidate load of the instance door, and the three doors' reads of their declaration JSON are unpinned path reads. Digest-only appears in this pack as a one-change reader control on a copy of the instance workbook's `pass05-workbook` pin.

These canonical helper constraints were read in source and were not executed:

- pass05, pass04, and the n7 overlay compare `parents[2]` with `D:\Git\lib-build`.
- The instance workbook and the instance door compare their resolved path with the exact file under `D:\Git\lib-build`.
- The capacity adapter's `HELPER` is `D:\Git\lib-build`.
- The reporter `HELPER_ROOT` is `D:\Git\lib-build`.
- The inert candidate sets `code_root` to `D:\Git\lib-build`. The selected dispatcher loads v7 from its own parent directory.

That reading is observation. It is separate from platform readiness and from any security claim.

## Executed reader

Python is CPython 3.14.0 at `C:\Users\misg\AppData\Local\Programs\Python\Python314\python.exe`. Launches use `python -B` and `PYTHONDONTWRITEBYTECODE=1`. The reader is `labs/module-dependencies-pass02/depdecl.py`. Declared modules were not imported. No live app command ran. `index` and `delta` were not run.

Prime command:

```
python -B labs/app-dependencies-pass03/preflight.py --set D:\Git\lib-build\labs\app-dependencies-pass03\set.json
```

On the positive copy, that wrapper exited 0. `activation_ready` is false. `closure`, `compatibility`, and `release` are false. `commit_authenticated` is false. `measured_faults` is empty. The recommendation is: Hold activation. The declared rows are a preflight of accepted pieces. Combined workbook W and reporter-on-W are pending. This report is not closure, compatibility, or release.

Reader answers inside that positive report:

| Command | Reader exit | Status | Findings |
| --- | --- | --- | --- |
| validate | 0 | valid | |
| identity | 1 | incomplete | 17 fixture results identical; incoming pair-differs on the disclosed reporter pin |
| requires --transitive of the instance door | 1 | incomplete | address-unresolved 4, condition-unknown 4, environment-unverified 10, shared 3, withheld 5 |
| requires --transitive --depth 1 of the instance door | 1 | incomplete | depth-limit 3, address-unresolved 2, condition-unknown 2, environment-unverified 2, withheld 3 |
| explain of the instance door to pass05 | 1 | incomplete | address-unresolved 4, condition-unknown 4, environment-unverified 10, shared 3, withheld 5; explain_paths 3 |
| impacted --depth 1 of pass05 | 1 | truncated | depth-limit 1 |
| requires --transitive of the reporter | 1 | incomplete | pin-differs 1, environment-unverified 3, withheld 3 |
| requires --transitive of app/librarian.py | 1 | incomplete | environment-unverified 2, withheld 2 |

The selected-v7 edge resolves as `selected` with pin form `unpinned`. The reporter edge `selected-app-pin` resolves as `pin-differs`. The wrapper records that difference and still exits 0, because the fixture bytes of the selected app match the declaration and the pin difference is the disclosed inert hardening pair `f1d23d455f20319e3f430d345b2893bda039fd8c84be4f3691b4e4be123b8983`, 12804 bytes.

## Author cases

These cases are this author's. This filing does not claim an independent Prime run. `drive.py` wrote `D:\librarian\temp\0525-0503\run-20261104b`. The failure list is empty.

| Case | Exit | Change |
| --- | --- | --- |
| positive | 0 | byte copy of the lab set |
| digest-only | 0 | instance workbook `pass05-workbook` pin bytes set to null; pin form digest-only; resolution resolved |
| wrong-digest | 1 | pass05 `pass04-workbook` pin sha256 first hex digit flipped; fault pin-differs |
| wrong-length | 1 | pass05 implementation bytes increased by 1; result declaration-length-wrong; fault identity-pair-mismatch |
| missing-record | 1 | pass04 declaration and its select row removed; fault record-missing |
| missing-file | 2 | fixture `labs__workbook-review-pass04__workbook.py` deleted; reader refused; activation_ready false |
| hostile-digest-length | 1 | digest-only pin and the wrong pass05 length together; incoming relation digest-matches; result declaration-length-wrong |
| hostile-git-blob | 0 | reporter basis changed to git-blob, verification supplied-unverified, commit 40 zeros; commit_authenticated false |
| reconstruct | positive 0, negative 1 | second root, then the same wrong-digest change |
| reader-regression | 0 | `python -B -X dev labs/module-dependencies-pass02/tests/test_repair02.py -v`; Ran 8 tests in 44.177s, OK |

H1 keeps the digest-only incoming relation on requirement `pass05-workbook` from the instance workbook. The pair pins of pass05 from the v9 door and the instance door still name the fixture bytes. The wrong declaration length is a separate identity result. The report text has no phrase that would mark the set ready for activation.

H2 leaves the reporter implementation sha256 and length unchanged. The reader accepts the supplied-unverified git-blob shape and does not fetch Git.

## Reconstruction

`D:\librarian\temp\0525-0503\reconstruct-20261104b\from-checkout` copies the lab declaration files and reads fixture bytes again from the checkout paths in `set.json`. Each re-read matched the fixture sha256. The negative directory `wrong-digest` copies that tree and flips the pass05 `pass04-workbook` pin digest. Caller sources stayed in place. `drive.py` refuses when `run-20261104b` or `reconstruct-20261104b` already exists. A later rerun needs a new stamp pair. These directories were left in place.

## Earlier stamp

`D:\librarian\temp\0525-0503\run-20261104` is the first author run. It exited 1 with these failures:

- positive-exit: 1
- positive-identity: incoming pair-differs on `lib-build:labs/review-report-hardening-pass01/report.py` requirement `selected-app-pin`
- digest-exit: 1 with the same incoming relation
- h2-exit: 1 with the same incoming relation
- reconstruct-exit: 1 with the same incoming relation

The other controls on that run already matched the expected exits. The stamp remains so the wrapper correction stays visible. The proof cited above is `run-20261104b`.

## Hashes of the retained reports

- Stamp suite `D:\librarian\temp\0525-0503\run-20261104b\suite.json` sha256 `a53796115e034cfef3037ee5e041bd66bec0769ff89401dff8c56df07df506c3`, 2507 bytes. The evidence copy is the same bytes.
- Positive report `D:\librarian\temp\0525-0503\run-20261104b\positive-preflight.json` sha256 `fa7c345d60c719cfee93eaabf95cc8af9e1285e200291baad7d1a819c4385cb4`, 21434 bytes. The evidence copy is the same bytes.
- Earlier suite `D:\librarian\temp\0525-0503\run-20261104\suite.json` sha256 `a63d9a6d082d2469b707c73dffb6ece711642d9d52e15cd4c49afb86eca81997`, 3132 bytes. It stays outside this evidence directory.
- Reconstruction set `D:\librarian\temp\0525-0503\reconstruct-20261104b\from-checkout\set.json` sha256 `0152daea079d887984f1548bfa13986d8f553aa74048b72ffbcfab1ff0e31082`, 11706 bytes.

## Frozen files, start and end of run-20261104b

The map was equal at the start and the end.

- `app/README.md` sha256 `3c2125aa0cebd7ddc1604de2a823c1250edf40a8e97bd7dbd2eb09ca91155920`, 39687 bytes
- `app/librarian.py` sha256 `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes
- `app/review_loop_tools_v9.py` sha256 `b9a8b9fe5920430b966aae761c5374aa121a060c4074f260cb4ebf89d00f4c47`, 11765 bytes
- `labs/module-dependencies-pass01/depdecl.py` sha256 `be32e7be8b481d7439f9f884f3cc709841964c807c8274f68bed7a3ce12567f0`, 48898 bytes
- `labs/module-dependencies-pass02/depdecl.py` sha256 `a517b0ec3906589e16e2df9bcfb6b3e21a5dd0bd3ef1099d59bf95c0f15ff4e7`, 53693 bytes
- `labs/n7-local-lifecycle-pass01/workbook.py` sha256 `43995fc72db252c22baeadb1e7c3b16012125eb286ce4f2356ff96e051044d2a`, 9750 bytes
- `labs/review-instance-binding-pass01/workbook.py` sha256 `3f8118ccdc2c7afc4abdca2d52c3510864f159642ed06aee52a485709be55aba`, 5916 bytes
- `labs/review-report-hardening-pass01/report.py` sha256 `27e513f462b241e9c7298d3077d50d08ea5ac703a6f2d0769dc5935fcb51b58b`, 18139 bytes
- `labs/review-source-capacity-pass03/workbook.py` sha256 `fe887c0f378fc1da3f5e778ac4642c907f713614040d5ebf3b74272b02512b1f`, 3126 bytes
- `labs/workbook-review-pass05/workbook.py` sha256 `86f40268fe2f45005fd0f037f69e2d0ecb854041f6f5d59b61beeb085c09c991`, 6994 bytes
