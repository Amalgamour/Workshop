# Submission claude-0519-0501 — desk app core integration design and lab
From: claude-opus-5-5 (Claude), executor on 0519.desk-app/05.01. To: Codex Prime.
Member: 0182.desk-app-integration-design-0501. Workspace D:/Git/lib-build, branch workshop, HEAD 960d20c (uncommitted pages).

## Did
- Verified pack05.01: 51 of 51 snapshots match their pins and equal live. 49 equal HEAD; the other two are uncommitted Prime records.
- Recorded the release and the claim on 05.01.
- Wrote notes first (06.01), and acknowledged both mid-assignment clarifications:
  - 0519/06.02 with 0416/06.04: compute constructs the review loop's pages from structured inputs;
  - 0519/06.03 with 0416/06.05: Grok-2 owns the broad execution and replay lab, and this lane narrows to design.
- **integration-map.json:** a source-backed map of the ten loop steps, each with its real files and interfaces, what was demonstrated, what is unverified, the limits and what is missing.
- **DESIGN.md:** authoritative records with no new store, CLI interfaces, module pins, minimum compute construction, derived states and next actor, release versus receipt, binding, restart and partial writes, trust assumptions, and findings F1–F8.
- **BUILD-PLAN.md:**
  - three contracts (C1 templates, C2 review binding, C3 page address);
  - packs G0–G5 with file ownership, dependencies, tests and parallelism;
  - a hostile self-review;
  - Director choices D1–D6, each with a recommendation.
- **Lab** labs/desk-app-integration-pass01:
  - `desk_lab.py view`: read-only; reservations + pinned return_inspect + batch_observe (+ prime_cycle);
  - `desk_lab.py construct`: batch-page/1, return-pointer/1 (release, claim, execution) and review-section/1; placeholder-only, compare-and-swap, refuses removals and the checkout;
  - `demo.py`: 36 synthetic steps in a disposable repository, each a separate process.

  Final run: 36 of 36 held, exit 0. Earlier failing and aborted runs are kept in evidence/build05.01/runs.
- **Live read-only view** of the real book: 83 tasks, 27508 files identical before and after. One small probe of where reviews live.

## Blocked
Nothing blocks this return. Boundaries found, not bypassed:
- **F4.** prime_cycle binds a review to the whole page, so constructing the page's Review pointer makes that review stale (lab 8b). This needs a prime_cycle pass (G3) and is not patched here.
- **F1.** `librarian.py where` and `validate` exit 2 on the live `assignment_state: prepared`. This is app code; reported only.

## Need
- **Prime:** review the design. Decide D1–D6 with the Director, starting with D3: the return band has 16 members left (0184–0199).
- **Recommended next action:** release G1 (read-only `librarian.py desk`) and G0 to Grok, and agree contracts C1 and C2 so G2 and G3 can run in parallel.
- Compare with Grok-2's independent 0520 evidence before implementation, as 0519/06.03 says. I did not read it.

Limits:
- SYNTHETIC data only; no model or session ran.
- Labels are not authentication; same-user; no sandbox.
- The live view misreads legacy review addresses (F3) and does not resolve versioned or 07NN page layouts (F7).
- Not approved, not accepted, not published.
