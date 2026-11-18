# Builder handoff v2 — task agreements in authoring and review intake (0707/05.15)
who: claude-opus-5-5 · state: **implementation-ready PROPOSAL.** It supersedes `design05.14/HANDOFF.md` (preserved). The reference is `labs/task-agreement-reference-pass02` (author lab). **No connector below exists, and no hashes are guessed.**

## What passed (author lab; external fixtures)
- **The fence grammar, binding revalidation and output-room cases:** 21/21 in new-run02, including **5 reproductions** of Prime's disclosed failures.
- **The 16 pass01 cases:** 16/16 through the shim, with the test file byte-identical.
- **The whole flow** with own-pointer freshness and outside-cut context change.
- **Exact frozen-helper observations** for all six legacy fields.

## What the lab cannot establish
- production integration;
- OS-level write confinement;
- symlink behavior (skipped);
- concurrency, power loss or races;
- semantic correctness of any cited text;
- that the core helper's defects are acceptable.

## What a builder must preserve
**The full list of SPEC v3 "Unchanged guarantees", plus:**
1. **The J1 grammar exactly,** or refuse anything outside it. Never count fenced text as a heading. Never cut the pack at a fenced pointer.
2. **J2:** validate a stored binding on every use, through one resolver, before reading.
3. **J3: the host enforces a concrete write scope.** The lab's `--lab-root` is only a model of it.
4. **Legacy compatibility is a separate `legacy_observation`,** never merged into block-mode states, and never a decision pairing or a grant.
5. **The helper defects stay visible** in projections until Prime decides on a core fix.

## Modules and connectors (unchanged plan, refined)
| Module | Responsibilities (v2 additions in **bold**) |
|---|---|
| **A** agreement library (NEW lab module) | parse, **J1 scanner**, cut resolution, bind and compare, **binding validation (J2)**, reconcile-request; CLI for operators |
| **B** authoring connector (a successor pass) | form kind `agreement`: compute lists the **real** headings (J1 scanner) and the standing or decision records; intelligence chooses; the tool generates the hash-free block before review and freeze |
| **C** intake connector (a successor) | binds the frozen pack with A; stores the binding in the intake record, **plus a `legacy_observation` from the existing helper for packs without a block**; new ids when evidence is added |
| **D** report projection | field states; compare status; **the legacy observation labelled legacy, with its known defects**; no release text; unknowns shown |
| host | **its own write scope (J3)** and its own declared policy; the resolver stays passive |

## Model-facing authoring interaction (SIMULATION; unchanged from v1, with the J1 note)
1. `authoring form --kind agreement` returns a menu of **real headings only.** A heading that appears only inside a fence is not offered, and an indented duplicate is flagged.
2. Prime returns a small choices JSON (meaning and selection only).
3. The tool generates the block; Prime reviews the candidate; the tool freezes.
4. Intake binds. Legacy packs get `block-absent` plus the helper observation.

The design05.14 `handoff-example/` was a real run of steps 2–4 on a copy of the 05.14 pack. **W-flow repeats the sequence under the J3 room rules.**

## Tests the builder must pass
- **The 21 pass02 cases and the 16 pass01 cases**, on disposable copies.
- **Prime's independent probes,** labelled separately.
- **Integration cases:**
  - B offers no fenced heading;
  - C stores both the block binding and the legacy observation, distinctly;
  - D renders legacy defects;
  - **a host write outside its scope is refused before creation;**
  - a tampered stored binding is refused on read.

## Bounded build order
1. **A**, including J1, J2 and the core-compat observer, to the 37 lab cases.
2. **C**, reporting-only, with the host write scope.
3. **D**.
4. **B.**

**Each step is separately reviewed.** A core-helper fix (CRLF, fences) is a **separate Prime decision,** not part of this build.
