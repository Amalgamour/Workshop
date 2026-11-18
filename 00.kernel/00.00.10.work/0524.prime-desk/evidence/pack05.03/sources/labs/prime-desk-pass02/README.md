# prime-desk-pass02

Read-only Prime desk overview and one canonical work packet. Current work comes
from the assignment record named by `app/development-workspace.json`, read inside
the declared book. A legacy selector is a hint. Standard library only.

The contract is `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.02/CONTRACT.md`.
`examples/shape.json` is a shape, not a live request.

```text
python -B labs/prime-desk-pass02/prime_desk.py view --request ABS [--json]
python -B labs/prime-desk-pass02/prime_desk.py packet --request ABS --work-id ID [--json]
python -B labs/prime-desk-pass02/request_index.py --list ABS --out ABS [--accept REL]
python -B -m unittest -v labs/prime-desk-pass02/tests/test_prime_desk.py
python -B labs/prime-desk-pass02/demo.py --out ABS
```

Run these from the repository root with `PYTHONDONTWRITEBYTECODE=1`.

Pass01 is unchanged. This lab does not seat `00.live`, call Git, or import the
review-loop successors.
