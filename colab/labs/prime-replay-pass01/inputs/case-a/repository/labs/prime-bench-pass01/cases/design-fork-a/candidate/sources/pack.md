# 05.08 — make copy replay safe
Executor: worker. Reviewer: Prime.

## Finish criteria
- F1. A second copy to the same destination never overwrites.
- F2. The behaviour is documented in the contract.

## Recorded Director reply (2026-10-20)
"Do not change an exit code a consumer already relies on without asking me first."
