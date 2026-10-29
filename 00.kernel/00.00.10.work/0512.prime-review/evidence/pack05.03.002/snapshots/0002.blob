# prime-review-pass01

Draft reports and declared-hold checks for the current Codex Prime (0512.prime-review/05.01).
Standard library only. Not seated law, not a dispatcher, and not a release gate.

Prime supplies the outcome and the words. This tool checks the record shape, the source hashes, and the holds Prime declared. It does not decide that a repair is routine or that a design conflicts. A report label, a model name, and the word yes are not authority.

```text
python -B labs/prime-review-pass01/prime_review.py report --input ABS [--root ABS] [--json]
python -B labs/prime-review-pass01/prime_review.py guard --input ABS [--root ABS] [--json]
python -B labs/prime-review-pass01/prime_review.py check-next --input ABS [--root ABS] [--json]
python -B labs/prime-review-pass01/prime_review.py draft --input ABS --dest ABS --repo ABS --expect-sha256 HEX [--root ABS]
python -B -X dev labs/prime-review-pass01/tests/test_prime_review.py -v
```

Run the commands from the repository root. Every path argument is absolute.

Exit 0 is a shaped continue, develop, or complete-as-supplied report with no attention, or a guard result `independent-of-holds`. Exit 0 still does not release, accept, or close work. Exit 1 is a shaped hold or attention. Exit 2 is a refusal.

`closes_work`, `releases_action`, and `authenticates_actor` are always false. A bound Director reply does not expand the grant. `check-next` on an action inside a hold stays `blocked` or `not-released`. An action outside those scopes is not frozen.

The contract is `00.kernel/00.00.10.work/0512.prime-review/evidence/build05.01/CONTRACT.md`.
Examples in `examples/` are hypothetical fixtures.

Limits: no model call, no Git, no network, no live page write, no import of the accepted helpers. Document cap 262144 bytes. List cap 24. Text cap 12000 characters. Symlinks, junctions, hard links, `..`, and UNC paths are refused.
