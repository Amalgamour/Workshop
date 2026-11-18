# EXAMPLES v2 — SYNTHETIC; not review jobs
date: 2026-11-01 · who: claude-opus-5-5 (Claude)

- **Generator:** `colab/labs/0510-reserved-review/pass02/examples.py`.
- **Written copies:** `evidence/design05.06/runs/20261101T203654Z-84a6ef/examples/`.
- **What is fictitious:** page `0799.synthetic-reserved`, commit `1111…`, and the package digests (sha256 of a fixed SYNTHETIC string).
- **What is real:** every other hash is the real sha256 of synthetic bytes.
- **What is imitated:** the trusted maps and the producer report imitate the real output shapes; those tools did not produce them.
- **What is modelled:** the page record is produced by `workflow_model.py`, the model of the *proposed* K1–K3.

| File | Shows |
|---|---|
| `descriptor-05.01-independent.json` | `reserved-review/2`, independent: trigger, cut, a requirement, an authority limit, builder context withheld, reviewer `unknown`/`new` |
| `descriptor-05.02-informed.json` | informed: `first_return` names the 05.01 package digest, return hash and length, seal seq 3 and the seal transition hash; no N1NN member |
| `05.01.return.SYNTHETIC.md` and `.crlf.md` | the same `reserved-findings` block (R01–R03) with LF and with CRLF |
| `05.02.return.SYNTHETIC.md` | `reserved-reconciliation`: R01 different-conditions, R02 confirmed, R03 unresolved with a reason; one agreement, one disagreement, U01 from the builder |
| `page-record.SYNTHETIC.json` | the K3 transitions: open(05.01) → attach → seal-return → review request-next 05.02 → open-pass(05.02) |
| `trusted-05.01.json`, `trusted-05.02.json`, `producer-verify-05.01.json` | verifier-shaped inputs: the first packet without builder notes; the second with the notes and the sealed first return |
