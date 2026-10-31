# Colab readiness, pass 01

Standard-library checker for a declared Colab delivery. It reports transport, runtime dependencies, evidence references, minimum evidence, smoke, and ready-for-method as separate results.

```text
python -B colab_readiness.py check --request ABS
```

Exit 0 means a complete report was written. It does not mean the delivery is ready, true, or accepted. The checker never executes the smoke command text.

The 05.01 contract and guide stay the captured original. The repaired evaluation is `00.kernel/00.00.10.work/0516.colab-readiness/evidence/build05.02/CONTRACT.md`. Prime's repaired guide is `PRIME-USE.md` beside that delta.
`inventories/replay-revision-sources.json` is a source list for a future replay revision. This lab does not build that revision.
`00.00.10.work/0316.dependencies` can later supply this checker's declared rows. This lab does not implement that registry. A preinstalled requirement stays unknown until its bytes are supplied or the feature is declared not-applicable. Deleting the requirement is not a repair.
