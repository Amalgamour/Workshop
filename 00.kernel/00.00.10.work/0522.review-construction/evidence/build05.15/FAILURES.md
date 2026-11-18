# Historical failures — 0522/05.15

The copied historical suite exited 1. PASS 13, FAIL 4, ERROR 0. First failure G7. The copied assertions were not edited.

## G7

Semicolon Returned line codes: `malformed-n7-declaration`, `unparsed-return-line`. The old clause that asks for `unparsed-return-line` still holds, and the line binds nothing.

Double comma `Artifact manifest: m.json,, sha256` codes: `malformed-n7-declaration`, `unparsed-return-line`. The manifest binds nothing. Pass04 had accepted this as filename `m.json,,`. Pass05 treats it as a failed N7 comma-delimiter form and blocks it. The old refusal-code set contains `unparsed-return-line`, so that clause now holds. The code was not renamed to `unrecognized-path-punctuation`.

N5 trailing comma `Submission: s.md, sha256` codes: none. The path stays `s.md,`. The assertion asks for `unrecognized-path-punctuation`. That clause fails. This is the preserved pass03 filename, including inside N7 context, and it is the same form P4 requires.

## I4

Patched prepare exit 0, measurement incomplete. Codes include `ambiguous-declared-root`, `custody-missing`, `index-context-bounded`, `unparsed-return-line`, `verification-not-measured`. The assertion asked for `artifact-missing`. The fixture deletes its copy of a path that still exists under `D:\Git\lib-build`. The production root stays that checkout, so the measurement is canonical-root ambiguity.

## H2

Unpatched measurement incomplete, with `declared-hash-mismatch`. Patched measurement incomplete, with `ambiguous-declared-root`. The assertion asked for a complete patched measurement. The decoy name collides with the live checkout. This is the same canonical-root class, and the baseline hash mismatch remains the unpatched result.

## I6

Unpatched codes: `custody-missing`, `index-context-bounded`, `submission-not-declared`, `unparsed-return-line`. Patched measurement: incomplete. The assertion asked for a complete patched measurement. The counted line is still an accepted pass03 form. The incomplete patched result is the canonical-root collision, and the historical test did not store the patched codes.

These four rows are not parser regressions of the accepted N7 forms. They are not four passing cases.
