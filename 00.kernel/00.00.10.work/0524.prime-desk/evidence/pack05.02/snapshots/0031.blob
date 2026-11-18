# prime-desk-pass01

Read-only Prime desk overview and one selected-work packet. Standard library only.
It is not seated runtime. It does not select, release, accept, or dispatch work.

The contract is `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.01/CONTRACT.md`.
`examples/shape.json` shows the request shape. It is not a live request.

```text
python -B labs/prime-desk-pass01/prime_desk.py view --request ABS [--json]
python -B labs/prime-desk-pass01/prime_desk.py packet --request ABS --work-id ID [--json]
python -B -m unittest -v labs/prime-desk-pass01/tests/test_prime_desk.py
python -B labs/prime-desk-pass01/demo.py --out ABS
```

Run these from the repository root with `PYTHONDONTWRITEBYTECODE=1`.

The request names the book instance, the selector, and every file hash. The tool
reads those paths and writes stdout only. A catalog is an index. The selector
decides the current work. A supplied running label is not a process check.
Predecessor readers are pin-checked. Their Git, subprocess, and fixture-lifecycle
entry points are not called. Review-loop successor modules are not imported.
