# CONTRACT - 0512.prime-review/05.07 app connector

date: 2026-11-03
executor: Grok-1
reviewer: Codex Prime
state: locked before code
accepted: false

This contract is the staged read-only connector in front of review-report-pass03. It is not revised after tests. A failing test is repaired in the lab or in the new connector, or it is recorded as a limit. The report meaning stays the 05.06 contract, sha256 e5849352644b63c8f249546d4f5bd7ccad575218d9c2062db2f4814a55babc6c, 12396 bytes. This pack does not select an app route and does not edit app/librarian.py.

## Command

Staged command, available without a dispatcher edit:

```
python -B app/review_report_tools_v1.py --book ABS --source PAGE --pass 05.NN
```

Proposed command, unapplied:

```
python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN
```

The public argument list is `--book`, `--source`, and `--pass`, each exactly once. There is no public `--code-root`, `--record`, `--publish`, `--prepare`, `--form`, or `--tool`. An equals form such as `--publish=1` is the same refusal as the bare flag. Unknown tokens and positional tokens are refused. A missing value is refused.

`--pass` matches `^05\.\d\d$`. `--source` is a page id: non-empty, not starting with `-`, and free of `/`, `\`, CR, and LF. `--book` is an absolute path, contains no `..` part, is not a reparse point, and is an existing directory.

The installed root is `Path(__file__).resolve().parent.parent`. The running file must resolve to `INSTALLED/app/review_report_tools_v1.py`. `perform(args, code_root)` refuses when `code_root` resolves to any other directory. A copy that is not seated at that app path refuses as well. The refusal text is `copied fixture root X is not the installed app root Y`, with both paths in the sentence.

Argument checks run before any pin read. The root check runs after the argument checks and before any pin read. Pin checks run before the reporter process is started.

A connector refusal exits 2. Stdout is empty. Stderr is `stop: MESSAGE`. The tool main prints that line. The proposed dispatcher handler passes `Refuse` to the existing `stop` helper, which prints the same prefix.

## Launch

When the checks pass, the connector starts this process once and does not retry:

```
python -B labs/review-report-pass03/report.py --code-root INSTALLED --book BOOK --source PAGE --pass 05.NN
```

The working directory is the installed root. The child environment is the caller environment plus `PYTHONDONTWRITEBYTECODE=1`. There is no timeout. The connector copies the child stdout bytes, the child stderr bytes, and the integer exit. It does not parse the JSON and does not write a second rendering.

The reporter's own exit 2 still carries one JSON object and a `refused:` line. That is a forwarded reporter result. It is distinct from a connector refusal, which has empty stdout and a `stop:` line.

Exit 0 remains the reporter's readable state. Exit 0 is not approval, publication, custody, or release. Exit 1 remains stale, held, not-recorded, or identity-mismatch. The JSON object, attention, the bounded tests_note, and the declared, measured, addressed, content, and unknown-physical counters stay the reporter's bytes.

## Declaration

app/review-report-v1.json has schema `review-report-command/1`, version 1, a non-empty `_note`, and `tools`. Duplicate keys, a BOM, trailing non-space, and a CR byte are refused as a declaration that is not strict LF JSON. Each tools key is a repo-relative path. Each value has integer `bytes` and string `sha256` and no other field. The object equals the map embedded in app/review_report_tools_v1.py.

A key containing `\`, a leading slash, a drive prefix, an empty segment, `.`, or `..` is `tool path escapes the code root`. Any other difference from the embedded map is `declaration does not match the pinned tools`. Both refusals happen before the reporter starts.

## Pins

Twenty-three regular files are hashed before launch. The three reporter files are:

- labs/review-report-pass03/report.py, 8091, 70028dfe97bc6178a3497c814cf585476bb0b41650ce67fc79dd3d5b118dfade
- labs/review-report-pass02/report.py, 38323, d13d8d4f54d79cbdb22e1a40fdffb89bd26b85a611bf8620dc36854be9eb852e
- labs/review-report-pass01/report.py, 42127, 72e9bda15c5f3ca844350be5dae2fcfcf4e7c609c262b8f7e702d64467eb94cc

The other twenty are the pass01 `PINS` table, including app/librarian.py at 12204 bytes and sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9. A size or hash mismatch uses this sentence:

```
dependency conflict PATH got GOT_BYTES bytes sha256 GOT_SHA want WANT_BYTES bytes sha256 WANT_SHA
```

A missing file uses `got missing` in that sentence and still names the wanted size and sha256. A reparse point on a pin path is not followed: `dependency conflict PATH is linked and was not followed`.

labs/review-report-pass03/PRIME-USE.md and labs/review-report-pass03/tests/test_report.py are freeze inputs. report.py does not import them, so they are not launch pins. The 05.06 contract is the meaning record and is not a launch pin.

The connector does not change a drifted file. The author test of a wrong hash calls the audit on a temp tree whose copy of pass03 report.py was tampered. The live pin stays in place.

Applying the dispatcher diff changes app/librarian.py. After that change, this pin and the pass01 pin refuse until a separate reviewed pin change. This contract does not include that pin change. Rollback restores app/librarian.py to the hash and length above. Until that later review, callers use the staged tool command.

## Dispatcher harness

labs/review-report-app-pass01/librarian.py is the frozen dispatcher plus the three hunks in 06.11.md. labs/review-report-app-pass01/DISPATCHER.diff is the unified diff from the frozen file to that proposed file. invoke.py refuses unless the on-disk app/librarian.py still has the hash and length above, then executes the proposed source with `__file__` bound to the installed app/librarian.py. The lab file is not executed as the acceptance command.

Empty `review-loop` through the harness stops with `unknown review-loop command` and does not mutate. Empty `authoring` stops with `missing --book`. Empty `return-lines` stops with `command is not on this door`. `where` with no arguments stops with `missing --root`.

## Tests

The suite is labs/review-report-app-pass01/tests/test_connector.py. It is author work. It is not an independent run and it does not rerun the pass03 suite. Retained books go to D:/librarian/temp/0512-0507-report.

The three-way compare covers the direct pass03 command, the staged tool, and invoke.py on 0512.prime-review/05.06 and on 0521.return-placement/05.13. Stdout, stderr, and exit match. The run hashes the source pages, the two journal trees, app/librarian.py, app/README.md, and the three report.py files before and after. The connector does not record, publish, or approve.

Disposable fixtures cover a page with no recorded review (state not-recorded, exit 1), a published note edited afterward (state stale, exit 1), and a record file that no longer matches the journal digest (state held, exit 1). Each is a three-way byte compare. Fixture prepare, record, and publish use the existing review-loop on the disposable book only.

Mid-observation hold remains the frozen pass03 test `test_author_journal_current_changed_during_read` in labs/review-report-pass03/tests/test_report.py, sha256 f477fd4e4dac922435fac822a5b85ee34b34d731583a730842b08f5c110e18de, 32678 bytes. This suite checks that frozen file and does not rerun it.

Author hostile cases: a different `perform` root, a second copy of the tool, an unknown mutation flag, a declaration key `../`, a malformed pass, a repeated flag, and a direct run of the lab librarian.py. Prime's future independent probes are listed in the test module and are not executed.
