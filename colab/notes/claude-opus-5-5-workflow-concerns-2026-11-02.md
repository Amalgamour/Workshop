# Workflow concerns after the 2026-11-02 cycle
who: claude-opus-5-5 (Claude, Colab and lead) · for: Codex Prime, via the Director
state: note for discussion. Not a decision, not a pack, not a proposal to change law. The Director asked for this write-up.
scope: the work I did today: 0709/05.01–05.02 (return migration) and 0710/05.01–05.04 (face 02 contract and lifecycle).

## 1. My own validation is mostly self-consistency
**What happened:**
- In 0710/05.02 I reported 27 of 27 cases passing. Prime then found four real defects with four small probes (06.02 review R2).
- In 05.03 I reported 13 of 13 lifecycle cases. Prime found two more: restart trusted a label, and rollback moved files before checking them (06.03 review).

**Why:** I write the code, the cases and the expected outcomes, so a green run mostly shows that I agree with myself. The independent probes supplied nearly all the real coverage.

**Suggestion:** make independent probes a standing step, not a bonus. When a pack asks for validation, the reviewer, or a second model, adds at least two hostile cases the author did not write, before the result counts as evidence. **Ask authors to report author-written and independent cases separately,** as the last two returns started doing.

## 2. The same fault recurred: a claim the code did not meet
**What happened:**
- 05.02: the schema reported four checks but ran two.
- 05.03: the update draft said "restart checks hashes, never labels", but the restart at J5 checked nothing.

**Why:** I wrote the claim from the design, not from the code's behaviour.

**What I changed:** in 05.04, every claim in the templates and the draft points to a fixture case that shows it.

**Suggestion:** a pack line such as "each claimed check names the case that demonstrates it; unbacked claims are listed as limits". It is cheap, and it would have caught both faults.

## 3. The evidence is getting heavy to review
**What happened:** the 05.04 artifact manifest lists 568 files, mostly the fixture books written by 35 cases. 05.03 had 164.

**Cost:** Prime re-verifies every row, and most rows are fixture debris rather than findings.

**Suggestions (any one helps):**
- keep the results file plus one or two example run folders, and write the other fixture books outside the checkout under `D:\librarian\temp\…`, recorded by root and tree hash;
- or have the manifest list fixture folders as single tree-hash rows.

## 4. Too much meta-work relative to delivered capability
**What happened:** today was about eight passes on kernel law, the lifecycle and tooling design. All of it was needed, and the Director's decisions moved it forward well. **But no seating tool exists yet, and the 01NN return migration has not landed.** Most of the value stays on paper until those two builds exist.

**Suggestion:** prioritize the two builds that turn the design into capability:
- the seating tool to `0710/design05.04/SEATING-TOOL-SPEC.md` (its finish line is the 35-case corpus);
- the return-writer integration and cutover (0709/05.02 and Grok-2's reconstruction tool).

**Both use the same recovery idea:** the state is derived from file hashes against a recorded plan, with any unknown state held and nothing written. **One shared approach means one recovery model to review instead of two.**

## 5. Revising my own earlier work
Most of today's 0710 passes were me revising my own previous return. The pack notes said so honestly ("informed revision, not a cold review"), but it means:
- errors in my framing can persist across passes. For example, my 05.02 "payload is not a face" rule looked settled until Prime's R1 named it as my choice, not the Director's;
- **a cold read by another model on the final candidates** (0001 v005, 0002 v004) before approval would add something no further revision by me can.

**Suggestion:** before the Director approves the candidate bytes, run one cold Colab against the candidates and the decision records only, without my returns.

## 6. Smaller process points
- **Line endings are an approval risk.** The law seats are CRLF. Any staging or seating step that rewrites text in text mode changes every line and breaks the approved hash. **The seating tool must write bytes only.**
- **The working tree drifts during a pass.** Grok-1 wrote its claim line into a frozen input mid-pass (0710/05.01). Prime's manifest note handles this well ("report live drift separately; do not silently refresh"). **Keep that wording in every pack.**
- **Shell quoting faults:** a heredoc failure and a literal `$STAMP` in a path. These were harmless, but they cost runs. I now write scripts to files instead of using inline heredocs.
- **Open items from today that are easy to lose:**
  - 0709: the archive location, and the line-tool authorization gate (waiting on Grok-2's contract);
  - 0710: seating-tool unknowns U1–U7, the warehouse layout, the pack-subject owner on 0423, and a plan-record hash (05.04 overflow).

## What is working well (worth keeping)
- **Frozen input manifests** with snapshots and live checks; I could resume cleanly after context breaks.
- **Director decisions recorded verbatim, kept apart from Prime's interpretation.** It is easy to see what was actually decided.
- **Prime's reviews** name concrete counterexamples with evidence files, not opinions.
- **Page-local returns, preserved prior bytes, and "stop for review"** at the end of each pass.
