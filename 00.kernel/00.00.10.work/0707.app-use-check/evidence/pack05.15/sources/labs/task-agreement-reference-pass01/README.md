# task-agreement-reference-pass01 — NONPRODUCTION reference lab (0707/05.14)

A passive resolver for references-only `task-agreement` blocks: construct → assemble → bind → inspect / compare → reconcile-request.
- **Not installed or selected; no app door.**
- Spec: `00.kernel/00.00.10.work/0707.app-use-check/evidence/design05.14/SPEC.md`.

```text
python -B ta.py construct --book DIR --page PAGE --pass 05.NN --choices FILE --out NEWFILE
python -B ta.py assemble  --pack FILE --construct FILE --out NEWFILE
python -B ta.py bind      --book DIR --page PAGE --pass 05.NN --out NEWFILE [--profile profiles/legacy-headings-v0.json]
python -B ta.py inspect   --binding FILE
python -B ta.py compare   --binding FILE --book DIR
python -B ta.py reconcile-request --binding FILE --field NAME --proposal TEXT --reason TEXT --by NAME --out NEWFILE
python -B tests/test_ta.py --root NEW-DIR-OUTSIDE-CHECKOUT --out NEWFILE
```

**Exit codes:** 0 ok · 1 completed with findings · 2 refused (stderr `stop: …` with a correction hint).

**Guarantees:**
- Outputs are written only to NEW paths; inspect and compare write nothing.
- Raw bytes are measured as stored (CRLF and LF); strict UTF-8.
- Headings inside code fences are ignored.
- Escapes and links are refused.

**Not guaranteed:** confinement, races, power loss, or semantic equivalence. **Author lab tests only.**
