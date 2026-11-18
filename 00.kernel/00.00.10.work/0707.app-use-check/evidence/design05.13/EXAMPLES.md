# Worked examples (0707/05.13) — readable render
Fixtures: `examples/fixture/` (SYNTHETIC). Measured cuts and specified outcomes: `examples/views/*.json`. **Measured means the cut resolves and has a sha256 at design time. Specified means the behavior the design requires, NOT RUN against any target.**

## (a) A bounded authorized task — `0599.fixture-task/05.02.md`
- **The block cites:**
  - goal `#Goal`, scope `#Scope`, finish `#Finish`;
  - discretion: standing `0412x/01#Local work agreement` plus the agreement;
  - director-required: the standing agreement;
  - decision `06.02.decisions.md`: verbatim `#Director - verbatim` ("SYNTHETIC: Ok pack it"); interpretation and answers `#Prime - exact proposal this reply approves`.
- **Compute checks:** every cut resolves once (measured ✓); verbatim ≠ interpretation; the answers cut resolves.
- **Intelligence supplied:** the cut choices.
- **Unknown:** none.
- **May continue:** review record and publish; work within the cited scope.
- **Must wait:** builder execution needs the named invocation. **"Ok pack it" approved packaging of that proposal only.**

## (b) An N7NN hold, reply and successor — `0799.fixture-colab/05.01.pack.md`
- **The decision binding:** verbatim `06.02#Director - verbatim` ("#Q1 SYNTHETIC: Yes, but only under the page evidence folder."); interpretation `06.02#Prime - interpretation` (**a distinct cut**); answers `06.01.review.md#Question Q1`.
- **Resolves:** Q1 only.
- **Must wait:** D1 (build), which needs a released pack.
- **May continue:** I1, and a successor review on the same pass that records Q1 as answered.

## (c) Missing, changed or conflicting grants
- **c1, an absent block** (`0598.fixture-old/05.01.md`, like the real 0522/05.13): it is reported `absent`, and all six fields are unknown **even though the page has Goal/Scope/Finish headings.** Headings are not authority. A preliminary review may continue; complete, finished and release wait.
- **c2, a decision changed after binding:** the verbatim cut was measured `5524adba…` before and `da00e298…` after.
  - The state is `stale`; the original binding is kept; **no rebinding**.
  - A reconciliation request goes to the **Director**, because a changed verbatim record is a conflict.
  - The fixture was restored afterwards for the other examples.
- **c3, a scope conflict:** the pack says "Excluded: app edits"; the decision says "change the app entry too".
  - The state is `conflict`; both cuts are kept; Director judgment.
  - **Labs-only work may continue; any app edit waits.**

## Design application to this batch (`views/application-0412-06.08.json`)
This pack 0707/05.13 → 0412/06.08 "Ok pack it". The hashes are in `FIELD-SOURCE-MAP.md`. **This is a design application, not an active grant mutation:**
- no record was edited;
- the cuts were measured read-only;
- a production build is **not** covered by this "Ok pack it".
