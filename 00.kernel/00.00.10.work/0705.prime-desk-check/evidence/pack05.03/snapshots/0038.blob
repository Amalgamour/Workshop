# 0705.prime-desk-check / pass01

An independent acceptance oracle for the approved Prime desk (0420.prime-desk/01.md), written by Claude for 0705/05.01. These are declarative cases, not product code. They have not been run against any desk tool.

- `cases.json`: 18 cases (C01–C18). Each case has:
  - the exact frozen sources it uses, as path plus sha256 from pack05.01;
  - a declarative setup (empty for real-frozen cases; mutations of a disposable copy for synthetic ones);
  - the expected facts, unknowns, attention items and refusals, each with its basis;
  - forbidden inferences;
  - the evidence required;
  - a finish criterion.
- `check_fixtures.py`: checks shape and pins only. Run with standard-library Python:
  ```text
  python -I -B check_fixtures.py --cases <abs>/cases.json --manifest <abs>/00.kernel/00.00.10.work/0705.prime-desk-check/evidence/pack05.01/source-manifest.json
  ```
  It does not verify that the expected facts are true, and it never reads live pages.

How to use it later against Grok-1's returned tool:
1. Build each synthetic setup in a disposable copy.
2. Run the tool's own view and packet commands.
3. Compare its JSON facts, their basis and their source links with `expected`. Check the absence of every `forbidden` inference.

Agreement with the tool's own summary text is not evidence. Passing these cases does not approve or close the deliverable.
