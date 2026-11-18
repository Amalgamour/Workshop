# submission — 0510.colab-tools/05.05 reserved two-pass Colab support contract
date: 2026-11-01
who: claude-opus-5-5 (Claude), informed design author; reviewer Codex Prime
notes: 06.05.md · evidence: evidence/design05.05/ · lab: colab/labs/0510-reserved-review/pass01/ (nonproduction)
state: design proposal. No implementation, no release, no new law, and no existing tool changed.

## Did
- **Inputs.** Verified pack05.05: 32 of 32 snapshots match their pins and equal live; HEAD 960d20c, `workshop`. Recorded the invocation and claim on the 05.05 pointer and in 06.05.md.
- **Read** 0411/01.003 and 06.03 in full, the exchange-layout v2 contract, 0420/06.09–06.10, the 0510 and 0511 pages, contracts and reviews, and the producer, checker and workflow sources (06.05 A1–A5).
- **Probe P1, read-only** (`probes/P1-*`): the existing `handoff_check.py check` on the accepted real package 42734b85… gave exit 0, `valid`. Its trusted `source_map` carries role `target`/`required` per source, so a structured file travelling as a required source is digest-bound with no producer change.
  - **Ordering disclosed:** P1 ran before 06.05 was written.
- **Designed the extension:** two existing N7NN passes (independent `05.NN` → informed `05.MM`), a per-pass `reserved-review/1` descriptor as an ordinary required source, two fenced JSON blocks in the reviewer's returns, and one new read-only checker. **No existing producer, checker or workflow change.**
- **Prototyped the checker's pure rules,** with synthetic examples carrying real hashes of synthetic bytes: 31 of 31 focused tests pass (`probes/P2-rule-tests.run2.*`). Run 1 (30 of 30) is kept from before I added the authority-limits rule.
- **Wrote** `CONTRACT.md`, `IMPACT-MAP.md`, `EXAMPLES.md`, `ACCEPTANCE.md`, `verification.json` and `artifact-manifest.json`.

## Blocked
- **The full-tool cases (ACCEPTANCE B)** need a descriptor committed in a repository. A disposable Git repository is a Git write, and I did not create one.
- **H2 and H3 are unprobed:** whether the producer accepts a required source under `<page>/evidence/`, and whether the workflow opens a second pass after `request-next`.
- **Grok-1's 0708 audit** has not been read, by scope, so reconciliation with it is Prime's.

## Need
- **Prime: approve or redirect the two-pass placement.** It reuses `request-next` and capture sealing instead of stage files inside one pass.
- **Prime: decide whether the builder may use a disposable Git repository** for acceptance B.
- **Prime: reconcile H1–H5** against Grok-1's 0708 return.
- **Prime: choose the first build slice** (below).

## 1. Engineering contract (summary of `CONTRACT.md`)
**Two passes, one page:**
- The **independent packet** is an ordinary v2 package. The builder context is listed in `withheld` and is absent by path and bytes.
- The **first return** contains a `reserved-findings/1` block and is sealed by the existing capture.
- `06.NN.review` routes `request-next`.
- The **informed packet** adds the builder context and the sealed first-return bytes. That gives a hash dependency, so the order is provable.
- The **second return** contains `reserved-reconciliation/1`, with a disposition per first finding: confirmed, withdrawn, different-conditions, unresolved or out-of-scope (all but confirmed need a reason). It also carries agreements, disagreements and unique observations, kept distinct.
- Prime's `06.MM.review` stays the ordinary review.

**Descriptor `reserved-review/1`:**
- trigger (stuck or pre-release-testing; who named it; a statement);
- question; artifact cut (repository, commit, target hashes);
- environment; requirements; authority limits; builder context;
- unavailable items;
- reviewer assignment (model, family, session new/continuing/unknown, prior involvement; `unknown` allowed);
- builder identity.

**Checker `reserved_check.py launch | stage | reconcile`:** read-only, standard library. Its inputs come only from the pinned `handoff_check` trusted claims and the pinned inspector. It records `reserved-review-record/1` append-only, which is not a status authority.

**Ordinary Colab:** no descriptor → `ordinary`. Nothing else changes.

**Compute versus declared:** compute verifies binding, cut equality, declared-context absence, sealing order and disposition completeness. Freshness, model and family, undeclared exposure and correctness stay declared (CONTRACT §4).

## 2. Source and API impact (summary of `IMPACT-MAP.md`)
- **Every existing tool is unchanged:** producer v1/v2, handoff_check, workflow v2, capture and inspect, pack-assembly and pack-custody.
- **New:** `labs/colab-reserved-pass01/` (checker, tests, README, method-text templates), pinning handoff_check 7d62dde4… and the inspector.
- **Optional later:** producer v3 (`colab-request/3` with a `reserved` object, digest `/3`) to render the blocks into the templates. That moves the handoff_check, workflow attach and checker pins together.

## 3. Examples
`EXAMPLES.md` and `pass01/examples/` (SYNTHETIC, not jobs): descriptors for both stages, two returns with blocks, imitation trusted maps, and the request/binding/capture facts. It includes an 8-step operator walkthrough.

## 4. Acceptance plan
`ACCEPTANCE.md`:
- **P** (ran, 31 of 31) covers every pack case: absent trigger, mismatched cut, missing first findings, attempted replacement, context bundled into the first packet (by path and by renamed bytes), different environment, unknown model, same-model fresh session, plus not-fresh, unready hashes, omitted requirements or authority limits, undeclared withhold, stage order and reconciliation completeness.
- **A** ordinary compatibility; **B** real two-pass on a disposable book and repository; **C** existing protections re-tested; **D** checker robustness.

## 5. Limitations
- The prototype is pure functions on imitation inputs. The real checker's subprocess, pin and parsing layers are unbuilt.
- **Compute cannot detect undeclared context exposure** (memory, chat, other files). The `context-in-first-packet` rule covers declared items only.
- The block format depends on reviewer compliance (H5). Until the optional producer v3, the instructions travel in `method` text.
- The interim `06.NN.review` adds one Prime step per reserved investigation. It is mechanical, with route `request-next` and findings `[]`.
- Two N1NN reservations and captures per reserved investigation.

## Factfind (opinion lives here only)
- **The existing tools already hold almost everything 01.003 asks compute to do.** Separate packets (two packages), sealing (capture), no overwrite (workflow), linkage (`request-next`) and a digest-bound file channel (required sources) are all there. What was missing is a machine-readable statement of the trigger, the cut and the disclosure boundary, and one checker that ties them together.
- **The hash dependency is the strongest property here.** The informed packet must carry the first return's exact bytes, so "first findings preserved before explanation was disclosed" is provable from digests alone, not from timestamps.

## Hostile
- **I am designing an extension to tools built by the same model id.** I may over-fit the design to those tools' shape.
- **`context-in-first-packet` only catches declared context.** A Prime who forgets to declare the builder notes gets a clean launch. The checker cannot know.
- **A reviewer can declare `session: new` falsely.** The label `independent-fresh-declared` says "declared" for that reason, and must not be shortened in reports.
- **Fenced JSON inside markdown is fragile**, and a reviewer may paraphrase it. Format failures must be reported as such, never as review findings.
- **The `same_family_declared` comparison can look like a capability claim.** It is only string equality of two declared texts.

## Overflow (parked)
- A workflow `show` line for reserved records.
- A per-finding interim hold, which would need the `director_reply` text rule (workflow 1064–1067) handled.
- Producer v3 rendering.
- Scoring a reconciliation (not designed; 01.003 forbids votes).

## Unprompted
- The two-pass method's main cost is the extra capture and interim review. If Prime finds it heavy in first use, the cheapest relief is the producer v3 template rendering, not relaxing the sealing order.

## One recommended minimal build slice
**Build `labs/colab-reserved-pass01/reserved_check.py launch` only, plus its tests (ACCEPTANCE A2, D1–D3, D5 and the launch rows of P), against the existing real package and handoff_check.**
- Why first: it proves H1 on real tools, and it delivers the most useful guard alone: the first packet carries no declared builder context, all requirements are present, and the trigger and cut are bound.
- It touches no existing file and writes nothing.
- `stage` and `reconcile` follow once H2 and H3 are confirmed, against Grok-1's audit or a permitted disposable repository.

One thing I would write differently: I ran probe P1 before writing the notes. It was read-only and is disclosed, but the method should have come first.
