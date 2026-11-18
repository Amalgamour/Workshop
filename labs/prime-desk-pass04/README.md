# prime-desk-pass04

Read-only Prime desk overview and work packet. Current work comes from the
assignment record named by `app/development-workspace.json`, read inside the
declared book. A legacy selector is a hint. Standard library only.

This lab keeps the pass03 routes. It prints supplied context in the markdown
and a short brief above the numbered sections. View schema is
`prime-desk-view/4`. Packet schema is `prime-desk-packet/4`.

A declared operation named `review-loop` is the review-loop row. When none is
declared, the overview still shows a pending row with no source file.

The contract is `00.kernel/00.00.10.work/0524.prime-desk/evidence/build05.05/CONTRACT.md`.
`examples/shape.json` is a shape, not a live request.

```text
python -B labs/prime-desk-pass04/prime_desk.py view --request ABS [--json]
python -B labs/prime-desk-pass04/prime_desk.py packet --request ABS --work-id ID [--json]
python -B labs/prime-desk-pass04/request_index.py --list ABS --out ABS [--accept REL]
python -B -m unittest -v labs/prime-desk-pass04/tests/test_prime_desk.py
python -B labs/prime-desk-pass04/demo.py --out ABS
```

Run these from the repository root with `PYTHONDONTWRITEBYTECODE=1`.

Pass01, pass02, and pass03 are unchanged. This lab does not seat `00.live`,
call Git, or launch a review-loop module.
