# Submission — claude-0517-0501 (0517.dependencies 05.01, module dependency declarations prototype)
who: claude-opus-5-5 (Anthropic), executor named Claude, in the Claude Code desktop app; a long continuing session that built prime-cycle-pass01, and probably the 0507 prime-support passes (compacted; recall partial). 2026-10-31, workshop at 5f9909ed9b4d58db3ff113fe7d284ab4010a79a8, source base f0ccb90.

## Did
- Verified pack05.01: 20 of 20 snapshots match their pins and their committed objects at f0ccb90, and 16 of 16 non-0516 live files are equal. The four 0516 references were used only as pack snapshots and committed objects: no live 0516 file was read, hashed, listed or touched.
- Recorded the claim. Wrote 06.01.md, then CONTRACT.md, then code.
- **Built `labs/module-dependencies-pass01/depdecl.py`** (standard library; it does not import subprocess):
  - `validate`;
  - `requires`, direct or `--transitive`;
  - `explain`;
  - `impacted` (reverse);
  - `identity`;
  - `index` (derived, written only to a new folder);
  - `delta` (the completion seam).
- It reads only a caller-supplied, hash-pinned set. It never imports, executes or follows anything a declaration names.
- **Schema** (CONTRACT §2–§3, §8):
  - `module-declaration/1`: module `{repository, path}` under the scoped `repo-path/1`; purpose, interface and limits; the exact implementation sha and its git-blob basis; covered entry points; and either an explicit `no_requirements` or a non-empty list. An empty list without it is refused.
  - **Requirements, stated in one direction:** kind (runtime-code, runtime-resource, environment, evidence, task-context), target (module, external, environment or full address), pin and `pin_required`, mechanism, condition (always, or conditional with a stated status), availability, reason and source lines.
  - **Provenance:** full book/page/pass/file links, pinned or unpinned, or explicit unknowns.
  - `module-declaration-set/1`, with an explicit `select` (never "highest"), and `module-change/1`.
- **Findings, never empty success:**
  - root `undeclared` (null) versus `declared-dependency-free`;
  - record-missing, pin-differs, ambiguous-version, identity-conflict and duplicate;
  - cycle, shared and depth-limit;
  - condition-unknown and condition-inapplicable (caller statements recorded);
  - environment-unverified or unavailable, and external-unverified;
  - withheld, provenance-unknown or unpinned, and address-unresolved.
- **Examples,** prototype declarations read from committed source at f0ccb90:
  - prime_cycle → batch_observe (subprocess), and prime_review, review_packet, return_inspect, return_capture (conditional);
  - batch_observe → prime_support (dynamic import) and clerk_adapter (hash-check), plus conditional inspector, helper and git;
  - prime_support → clerk_adapter (import, no own pin) and conditional git;
  - clerk_adapter → the external Clerk tool (conditional).
  - The diamond is real. The tools without records stay record-missing. batch_observe's provenance is unknown; prime_support's and clerk_adapter's are docstring citations, unpinned; prime_cycle has seven pinned links (design, assignments, reviews, return 0175).
- **Demonstration** (`demo.py`, 13 steps, all exits as expected):
  - the real chain, transitive (`incomplete`, correct);
  - explain, finding the two diamond paths;
  - a record-missing root;
  - identity (four snapshot copies identical, a SYNTHETIC copy changed);
  - reverse impact of the changed bytes (consumers with pin-differs, transitive consumers, provenance);
  - an index;
  - SYNTHETIC complete chain, dependency-free module and missing record;
  - the completion seam, consistent (exit 0) and an omitted change (exit 1).
- **Tests:** 15 cover every case pack #04 lists (absent versus zero; missing transitive; duplicate and conflict; changed bytes; multiple consumers; diamond; cycle; condition unknown or inapplicable; environment and external; the same page in another book and the same path in another repository; provenance unknown or unpinned; unsafe paths and a junction; malformed input; bounds; occupied and partial index; delta; the real chain unmodified).
  - 15 OK on the final bytes, in dev and default mode, 0 skips.
  - 9 of 9 targeted mutations caught.
- **The demo found one defect:** `impacted` always exited 1, against CONTRACT §7. It was fixed, with a regression assertion. My expectation in that demo run was also wrong; the log is kept.

## Blocked
Nothing blocks this batch.

## Need
**Prime:**
- review the schema and the completion seam;
- decide whether import-by-path requirements must carry a pin (prime_support → clerk_adapter);
- decide where accepted declarations live (module-local beside each lab, with the index derived).

**Recommended next action:** Prime reviews this prototype. Then a builder writes declarations for the four record-missing tools (prime_review, review_packet, return_inspect, return_capture), with pinned provenance from their construction pages, so the prime-cycle chain can be answered without record-missing.

## Integration proposal
- **Builders** return a `module-change/1` with each module build or change, and compute runs `delta` on it.
- **Prime** reviews the meaning and writes `select` entries.
- **A later delivery checker** (0516's consumer, after its repair) reads the selected set by hash, instead of a hand-declared dependency list. It adds no authority and no second schema.
- **Page-local reasons** stay on the pages; declarations link to them.

## Limits
- Declarations are model-authored, from reading source. `complete_claim` is false; they are not proof of runtime closure.
- A digest proves bytes, not compatibility.
- Environment availability is never probed.
- No string content is interpreted.
- There is no OS sandbox or race safety.
- Symlink (as opposed to junction) set paths are not exercised on this host.

## Declared outputs (sha256)
- `00.kernel/00.00.10.work/0517.dependencies/06.01.md` 5558d9c26be87724e717529db97f8cc6ac9a27642043fdbee9a4b63589f3e8fd
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.01/CONTRACT.md` 3c3b7e88f3d35d7854778e4aef75d09cede8bc97e35762cc0e412fc600de99e8
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.01/verification.json` 62ff5a9ae3169a97495c09aa1d93b6cea1534bcc37bb900fbe187cb9d79d0d7c
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.01/artifact-manifest.json` a30afbb21093f3b63a907503fa7d1fcf032a6d5c45b2b8b7f53ebd4dabd3229d
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.01/PRIME-USE.md` 396b8e46c75fac6adda7e0cc608a565134e239415354a345b98d86f52ed911b8
- `00.kernel/00.00.10.work/0517.dependencies/evidence/build05.01/sample-dependencies.json` 774c40053d3a3db50339c8faa9e88f2db7d120c2909c9c02a1f588927c16c951

artifact-manifest.json binds the lab code, tests, demo, README, example declarations and set, notes and evidence (14 files), including depdecl.py 5c35692cb22e3c57….
