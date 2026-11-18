# CONTRACT - 0512.prime-review/05.08 deployment candidate

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
state: locked before code
accepted: false

This contract is the versioned deployment candidate for the review-report command. It is not revised after tests. A failing test is repaired in the new lab or the new connector, or it is recorded as a limit. The report meaning stays the 05.06 contract, sha256 e5849352644b63c8f249546d4f5bd7ccad575218d9c2062db2f4814a55babc6c, 12396 bytes. This pack does not select an app route and does not edit app/librarian.py.

## Known failures already reproduced

The 05.07 dispatcher, 12792 bytes, sha256 b253a89751a48b64089bb95c4fde3715de00e6dc3c61dd8bad8653051234f3fa, written on disk as app/librarian.py and launched through the frozen v1 connector, stops before the reporter. The stop line names app/librarian.py, got 12792 bytes and that sha256, want 12204 bytes and sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9. Stdout is empty. Exit 2.

The historical author test test_author_contract_and_dispatcher_stay_put expects the 05.07 return pointer to stay PENDING. After the legitimate filing, that assertion fails. The historical test stays as that known failure. Successor tests do not inherit it.

Neither reproduction is new independent coverage.

## Command

Proof command, on a candidate root whose app/librarian.py is the deployment file:

```
python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN
```

The process executed is that on-disk file. The connector derives the code root from the installed app/review_report_tools_v2.py. A second root is refused. The public arguments are --book, --source, and --pass, each once. There is no public --code-root, --record, --publish, --prepare, --form, or --tool.

The same connector file on the active tree, where app/librarian.py is still the old pin, refuses that dispatcher before the reporter starts. Direct execution of labs/review-report-deployment-pass01/librarian.py is not an installation.

## Pins

The v2 declaration schema is review-report-command/2 and the version is 2. The declaration matches the connector pin table. The pin table binds the measured candidate dispatcher, every other pass01 pin at its current hash and length, labs/review-report-pass01/report.py, labs/review-report-pass02/report.py, labs/review-report-pass03/report.py, and labs/review-report-deployment-pass01/report.py. A hash validates those declared bytes. It does not grant authority and it does not select the route.

The deployment runtime, contract review-report-deployment/1, checks that set except its own file, then calls pass03 observe and the pass03-patched finish. It does not call pass01.check_pins and it does not launch pass03 main. pass03 main on the candidate tree still refuses the candidate dispatcher through the unchanged pass01 pin. v1 does the same. Those checks are not weakened.

Argument checks happen before pin hashing. Pin hashing happens before reader execution. A dependency conflict uses the sentence dependency conflict PATH got GOT_BYTES bytes sha256 GOT_SHA want WANT_BYTES bytes sha256 WANT_SHA, or got missing, or is linked and was not followed. A connector conflict is exit 2, empty stdout, and a stop: line. A runtime conflict is the reporter refusal: JSON on stdout, refused: on stderr, exit 2.

The measured candidate dispatcher hash is written into the v2 declaration and the runtime pin table after the file is built. This contract is not edited to insert that hash.

## Roots

Source root: the candidate or active tree that contains the executed app/librarian.py. Fixed live helper root: D:\Git\lib-build, because labs/workbook-review-pass03/workbook.py sets REPO to that path and loads its pass02 from it. The candidate copy of that module stays byte-identical and still uses that helper root. The book path is the caller's absolute book. The source pages are read from that book.

## Report meaning

Stdout of a completed report is the pass03 object, schema review-report/3, copied as bytes. Exit 0 is the reporter's readable state. Exit 0 is not approval, custody, or release. Exit 1 is stale, held, not-recorded, or identity mismatch, with the JSON object. The comparison on one disposable code root captures pass03 output before app/librarian.py is replaced, then runs the installed candidate command. Meaning, exit, judgment, attention, tests_note, counters, custody, stale, coherence, and authority are compared. A field that differs because the source root changed is explained. Fields are not removed to force equality. The source page bytes stay the same.

Verified physical-file identity stays unknown. unique_files stays absent. tests_note stays an object. Custody stays the review's custody.

## Lifecycle

The 05.08 task body is the page bytes before the return-pointer heading. Successor tests require that body to stay sha256 63defe4b9c4e0a04ef142eb7c21a02d48e4b7f1b808920f1bb8233f039f5de2b. The return pointer and the review section are lifecycle regions. Tests accept those regions while they say PENDING and on a copy after a legitimate pointer and review have been written. A changed task body fails. The historical 05.07 test is not edited.

## Routes

On the candidate installation, review-loop, authoring, and return-lines still dispatch through their existing doors. Empty review-loop stops with unknown review-loop command. Empty authoring stops with unknown authoring command. authoring form without a book stops with missing --book before a subprocess. Empty return-lines stops with command is not on this door. where without --root stops with missing --root. These checks do not mutate the live book.

## Selection

Selection replaces one existing file, app/librarian.py, with labs/review-report-deployment-pass01/librarian.py. It also requires these new files at their pinned paths: app/review_report_tools_v2.py, app/review-report-v2.json, and labs/review-report-deployment-pass01/report.py. It does not change v1, pass01, pass02, pass03, the selected core, or the helper module. Rollback restores app/librarian.py to sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. Until Prime reviews this return, the active command is not selected.

## Boundaries

Author tests start with test_author_. Two new hostile deployment cases are author provenance. The retained R1 and R2 logs are not those cases. No broad fixture, test_entry, or bridge suite. No network, install, model, bot, commit, or 0112 filing. Exit 0 is not a release.
