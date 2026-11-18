# Contract — return-route readiness

Schema: `return-route-readiness-contract/0510`
Date: 2026-11-02. Executor: Grok-2. Reviewer: Codex Prime.
This contract is written before the tool. It is not a release, not a receipt, and not app selection.

## Input

The command is `labs/return-readiness-pass01/readiness.py`. It takes `--code-root` and `--book`, each an absolute path to a plain directory. `--text` asks for a text projection of the same observation. Any other flag is refused.

A path that is relative, missing, linked, not a directory, or contains a `..` segment is refused before an observation. Exit 2. Stdout is empty. Stderr is one `refuse:` line. The tool creates no file.

The tool reads only:

- `app/librarian.py` under the code root
- the known facade and declaration paths below
- the dependency paths below
- `0100.band.returns` and, when that door is a plain directory, `0100.band.returns/01.md`
- `return-line-layout.json` under the book

It does not scan the book, hash the repository, import inspected modules, or start a subprocess. It does not open the review-loop implementation or classify other dispatch branches.

## Known contracts

Pins for paths that are rows in `pack05.10` are those manifest rows. `labs/return-access-pass01/return_access.py` is not its own manifest row. Its pin is the adapter entry inside the frozen `app/return-lines-v2.json` row: sha256 `501d40d7c7b08720d3ae061441284ac26d544e7b80100059b2ddce25f67358f5`, 26561 bytes. The on-disk file matches that entry. `labs/return-readiness-pass01/contracts.json` copies the manifest rows and that one declaration entry. The suite stops if the copy disagrees. The tool does not accept caller-supplied pins and does not invent a new signature.

`return-lines` old selector: facade `app/return_line_tools_v2.py`, declaration `app/return-lines-v2.json`. Dependencies: `labs/return-access-pass01/return_access.py`, `labs/return-lines-pass03/return_lines.py`, `labs/return-lines-pass02/return_lines.py`, `labs/return-lines-pass01/return_lines.py`, `labs/return-placement-pass01/return_placement.py`, `labs/return-capture-pass01/return_capture.py`.

`return-lines` new selector: facade `app/return_line_tools_v3.py`, declaration `app/return-lines-v3.json`. Dependencies: `labs/return-access-pass02/return_access.py`, `labs/return-lines-pass04/return_lines.py`, `labs/return-lines-pass03/return_lines.py`, `labs/return-lines-pass02/return_lines.py`, `labs/return-lines-pass01/return_lines.py`, `labs/return-placement-pass01/return_placement.py`, `labs/return-capture-pass01/return_capture.py`.

`capture-return` old selector: facade `app/handoff_tools.py`, declaration `app/capture-handoff.json`. Dependencies: `labs/capture-handoff-pass01/handoff.py`, `labs/clerk-handoff-pass02/clerk.py`, `labs/return-capture-pass01/return_capture.py`, `labs/return-capture-pass01/return_inspect.py`.

`capture-return` new selector: facade `app/handoff_tools_v2.py`, declaration `app/capture-handoff-v2.json`. Dependencies: `labs/clerk-handoff-pass02/clerk.py`, `labs/return-capture-guard-pass01/return_capture_guard.py`, `labs/capture-handoff-guard-pass01/handoff.py`, `labs/return-capture-pass01/return_capture.py`, `labs/return-capture-pass01/return_inspect.py`.

The predecessor dispatcher snapshot is `00.kernel/00.00.10.work/0522.review-construction/evidence/pack05.11/sources/app/librarian.py`. Its hash is provenance. A different whole-file hash is not, by itself, a route failure.

The accepted layout body is pass01 `layout_body`: schema `return-line-layout/1`, allocation `line-pass`, `sequential_allocation` false, and bands `5` = `matched-workflow-return-line`, `7` = `page-local-colab`, plus the book name. Canonical bytes are `json.dumps` with `sort_keys`, indent 2, and a trailing newline. For book name `00.00.10.work` those bytes are sha256 `2c414ac4e11cd874d28b8c477b7eed30ee477e216ed1653552d802f03c4d7804`, 216 bytes. That identity is the one recorded in `build05.09/CUTOVER.md`.

## Recognizer

The recognizer is a static `ast` pattern. It is not a Python interpreter. Matching the pattern does not prove what `load_module` will do at runtime.

A selection candidate is an `if` whose test is exactly `command == "return-lines"` or `command == "capture-return"`. An `in` or `not in` test against a tuple of command names is an activation guard. It is not a selection. Any other test that mentions one of those two strings makes that route `unsupported`.

The candidate body must contain exactly one `load_module` call of the form `Path(__file__).resolve().parent / "LITERAL.py"` or `Path(__file__).parent / "LITERAL.py"`, with a string module name and no keywords. The literal is one `.py` path segment. Any other call shape is `unsupported`. A load in the `else` side is `unsupported`. Two candidate `if` nodes for one command are `ambiguous`, including a second node that may be unreachable. Comments, docstrings, and expression statements are not selection.

A literal outside the old and new filenames is `unknown`. The tool does not rescan or adopt it as a new contract.

The dispatcher file is read twice. Every contract file that is read is read twice. If either read differs, the observation state is `unstable`, the route selections are empty, and the two cuts are not combined. `inspect(..., read_bytes=...)` is the unit fault-injection seam. The public command has no injection flag.

## Output

Stdout is one JSON object, schema `return-route-readiness/1`, then an optional text projection of that object. The text is not a second measurement.

`authorization` is false. `selection_is_authorization` is false. `authority` is `not-assessed`. The tool does not search for a release and does not call a verifier. `migration_assessed`, task association, approval, and completion stay negative.

Route `state` is one of `selected-valid`, `selected-but-invalid`, `unknown`, `absent`, `ambiguous`, `unsupported`, `unstable`. `selected-valid` requires a known selector whose facade, declaration, and every contract dependency are regular files, link count 1, not links, and equal to the manifest bytes. A known selector with a missing, linked, or different pin is `selected-but-invalid`. The predecessor can be `selected-valid` while the successor file merely exists. That successor is `staged`. Its bytes are reported and do not, by themselves, invalidate the selected predecessor.

Book `door.state` is `missing`, `linked`, `wrong-type`, or `present`. Layout `state` is `missing`, `linked`, `wrong-type`, `malformed`, `conflicting`, or `valid`. Duplicate JSON keys are `malformed`. A parseable layout that is not the canonical body is `conflicting`. `declared` is true only when the door is `present` and the layout is `valid`. `declared` does not mean the migration ran, the historical writer is confined, or the work is approved.

These three warnings are always present:

- An unselected successor does not protect the app.
- A guard on an undeclared book delegates to the historical writer.
- Historical direct scripts remain runnable.

A static `app_selected` field in predecessor status is named as a historical tool claim. This tool does not read that field as dispatch evidence.

Provenance cites `0521/05.09`, `06.18.md`, the operator addendum, and `build05.09/SELECTION.md`. `missing_prerequisites` and `next_checks` are statements for Prime. They are not shell commands and they are not authorization.

Exit 0 means an observation was produced, including an invalid, missing, ambiguous, unsupported, or unstable observation. Exit 2 means the invocation was refused. A Python traceback is a crash, not an observation.

## Failure

The tool has no write path. It does not create a status file, registry, queue, cache, lock, sidecar, marker, journal, layout, or root. A linked or escaping contract path is a mismatch or a refusal, not a read outside the supplied root. The whole dispatcher hash is reported and is not a permanent pin.
