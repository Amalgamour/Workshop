# task-agreement-reference-pass02 — NONPRODUCTION reference lab (0707/05.15)

The successor of pass01 (preserved byte-identical). Spec: `00.kernel/00.00.10.work/0707.app-use-check/evidence/design05.15/SPEC.md`. **Not installed or selected.**

```text
python -B ta2.py construct --lab-root ROOM --book DIR --page PAGE --pass 05.NN --choices FILE --out ROOM/NEW
python -B ta2.py assemble  --lab-root ROOM --pack FILE --construct FILE --out ROOM/NEW
python -B ta2.py bind      --lab-root ROOM --book DIR --page PAGE --pass 05.NN --out ROOM/NEW [--profile core-measured-agreement-v1 | FILE]
python -B ta2.py inspect   --binding FILE
python -B ta2.py compare   --binding FILE --book DIR
python -B ta2.py reconcile-request --lab-root ROOM --binding FILE --book DIR --field NAME --proposal T --reason T --by NAME --out ROOM/NEW
python -B tests/test_ta2.py --root NEW-EXTERNAL-DIR --out FILE
python -B compat16/run_compat16.py --root NEW-EXTERNAL-DIR --out FILE    # unchanged pass01 cases through compat16/ta.py
```

**Files:**
- `core_compat.py` observes the frozen core helper by AST extraction (pin-checked; no module import).
- `compat16/` holds the byte-identical pass01 test file and profile, plus a documented shim.

**Exit codes:** 0 ok · 1 findings · 2 refused. **Not OS confinement, not production; author lab tests only.**
