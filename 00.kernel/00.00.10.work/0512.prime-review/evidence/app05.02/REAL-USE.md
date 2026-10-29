# Real use — one app command

0512.prime-review/05.02. This is the command that replaces the direct lab invocation for the retained Prime review. It is an assessment. It is not a release.

## Command

```text
python -B app/librarian.py prime-review --input D:\Git\lib-build\00.kernel\00.00.10.work\0512.prime-review\evidence\prime-review05.01\actual-prime-review-input.json --root D:\Git\lib-build --json
```

Run from D:\Git\lib-build. The input is the record Codex supplied for the current three-return review. The root is the workspace those three return files sit in.

Observed on this run: exit 0, stderr empty, stdout 5011 bytes, sha256 deb4c1cb5fd53dc84a046ead990bde2d2d0322dc48846b155e7165cb1d60bf5f.
effective continue. authority none. closes_work false. releases_action false. attention empty.
The JSON report matches evidence/prime-review05.01/actual-prime-review-output.json field for field.

The same bytes come from the direct lab command:

```text
python -B labs/prime-review-pass01/prime_review.py report --input D:\Git\lib-build\00.kernel\00.00.10.work\0512.prime-review\evidence\prime-review05.01\actual-prime-review-input.json --root D:\Git\lib-build --json
```

## What the command removes

One launch path. The caller names the input and the root. The entry checks the pin, starts the accepted module, and returns that module's bytes and exit. The caller does not pass a module path.

## What stays manual

Prime still writes the judgment, the outcome, and any holds.
Prime still decides whether the account is right.
A continue result is not a grant and not a release.
The three bound return files stay evidence. This command does not edit them.
Seating the 05.01 page amendments remains a later Director choice.
No clock was taken. No token total is claimed.
