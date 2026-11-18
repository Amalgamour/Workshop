# CONTRACT - constructor pass04, newline and malformed-state repair
date: 2026-11-01
who: Grok-2
state: delta written before code; not Prime review and not acceptance

This file is the delta for 0522.review-construction/05.07. It was written before labs/review-construction-pass04. It binds only this constructor.

Predecessor: labs/review-construction-pass03/construct.py sha256 6eec5653c6818cfdeb98ffcd929cdf26f0ddf15c3121c703ce795abea6eb755d, 42216 bytes. That file and evidence/build05.06 stay byte-identical. The cycle, loop, door, app, prime_review, and readers stay byte-identical.

## What this slice builds

A new labs/review-construction-pass04/construct.py. It is the pass03 constructor plus two repairs:

- CRLF-safe reading of the task_binding line during read-only inspection and show
- a string check before membership on the four supplied_review_state enums

ROOT remains the literal D:\Git\lib-build. Envelope keys, result schemas, and bind inputs stay the pass03 sets. This slice does not change the cycle, the loop, or the door.

## Rendering and binding

review-construction/1 section text stays byte-identical to pass03, and therefore to pass02, including legacy null and empty-list wording. review-construction/2 keeps the supplied-state block, the single outcome line, and the source-hash decision line. Bytes outside the review section stay the caller's bytes.

bind and measure keep the pass03 inputs. The envelope schema and supplied_review_state are not binding inputs. Equivalent agreement bytes and equivalent source-file bytes produce the same binding_sha256 on /1 and /2, and the same binding_sha256 as pass03 and pass02 bind of the /1 envelope. A changed source file or a changed agreement changes the binding.

## Inspect and show

inspect keeps review-target-inspection/1 and the states absent, unsupported, pending, constructed-same-binding, and existing-review. Classification still uses newline_of, locate, and the compose order. The task_binding value is the first located line that is exactly `task_binding: ` plus 64 lowercase hex digits, after the section is split on the separator newline_of already selected. The same split is used by show. The section sha256 remains the hash of the original located bytes, CR included when the file is CRLF. This slice does not rewrite a file to LF.

A CRLF review that carries the same binding as `--binding` classifies as constructed-same-binding. An LF review of the same text still classifies as constructed-same-binding. constructed-same-binding does not authorize compose to replace a different body. Pending is still decided before the binding comparison. Absent, unsupported, and existing-review stay. Inspect writes no target, support, partial, or trace file. Symlink, non-regular, escape, checkout-root, and bad-binding refusals stay exit 2.

show keeps review-construction-show/1. On LF its stdout stays byte-identical to pass03. On CRLF it returns the binding the renderer wrote, instead of refusing that the binding is absent.

## Supplied-state refusal

disposition, pass_terminal, goal_terminal, and outcome are accepted only when the value is a string and a member of the existing set. The string test runs before membership, so an array or object does not raise TypeError. Null, numbers, booleans, and any other non-string or unknown text use the same Refusal message as an unknown string: `bad supplied_review_state.<field>`. exact keys and the schema and source checks stay. The constructor still does not check cycle couplings and does not compare the supplied object with record.json.

preview, apply, and bind of a malformed supplied object return exit 2 with `refused:` on stderr and no traceback. preview writes nothing. A refused command leaves an existing target unchanged and creates no support, partial, or trace file.

## Evidence

The build reproduces G01 and G02 by calling the frozen pass03 on new disposable fixtures, and retains that first result. The successor suite then shows the repair. It adapts the pass03 focused suite, keeps the symlink privilege skip, and covers LF and CRLF rendered sections, outside-section bytes, inspect writes-none, malformed enums through the CLI, same binding with a different body, /1 byte identity, and /1-/2 binding equality. The 05.06 cycle evidence writer is not rerun.

Exit 0 is an answer about the constructor command. It is not Prime review, seating, or app activation.
