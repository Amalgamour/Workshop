# AGENTS.md section templates (design proposal)

state: proposal for Matthew to review. Lines marked **Ruling** are his words. Everything else is Prima's proposal.
made: Wed 18 Nov 2026, about 3:20 PM EST, by Prima.
asked for: t326u, t327u, t328u, t329u (docs/review/DIRECTOR-WORDS-t326u.md ... t329u.md).
builds on: INSTRUCTION-GUARD-t309u.md (three tests, L1-L5, K-1..K-5, G1-G7); LIB-MINE-M1.md (pieces 2, 5, 7; Q1-Q5); CODEX-LIB-BUILD-REPORT-t323u.md.
cites: wf as `file:line @a00bc53` (workflow branch tip).
files: the draft library is docs/design/agents-pieces/ (INDEX.md, 11 pieces, EXAMPLE-AGENTS.md).

## 1. What Matthew said

> As for agents, no I want models to be able to build them.  As they will evolve over time.  What I want is this.  We have templates with exact wording for different sections of approved wording for agents.md or what ever comes next.  So a lead can build a agents like we build the packs of work. (t326u)

> You can make them for not.  But our goal is to have them protected so a model or 3rd party can't get control of our workshop. (t327u; "for not" read as "for now")

> Like I said the compute is the the fortress that protects the book.  No model or person should be able to access it without extreme safety measures in place.  With many backups.  Over time it will become stronger and stronger. (t328u)

> Right now, we are just a couple huts and a worksite.  In time this will become a fortress, what is acceptable during building won't always be acceptable later. (t329u)

**Ruling (t326u).** Models may build AGENTS.md files. They build them from templates of exact, approved wording, one per section, the way a lead builds a pack.

**Ruling (t327u).** For now, Prima makes the templates. The goal is that they become protected, so no model or outsider can take control of the workshop.

**Ruling (t328u).** The compute is the fortress that protects the book. Nobody, model or person, gets in without extreme safety measures. There are many backups. It grows stronger over time.

**Ruling (t329u).** What is fine while building is not always fine later.

## 2. The idea in one line

The approved part is the wording, not the file. A lead may build many AGENTS.md files. Every line in them must come from approved wording.

## 3. The parts

### 3.1 A piece
- A piece is one section of an AGENTS.md, such as "role" or "secrets".
- It holds **exact wording**: a few lines, word for word.
- It carries the three tests (t310u, t311u):
  - **axioms**: which axioms it serves;
  - **why**: why the line exists;
  - **authority**: the ref to the ruling or record behind it.
- It has an **id** (e.g. `agents.secrets`) and a **version** (1, 2, 3 ...).
- It has a **hash**: the sha256 of its wording. The hash names the exact bytes.
- It has a **state**: DRAFT, then approved. Only approved pieces count (M1 Q3).

### 3.2 A slot
- A slot is a marked blank inside a piece's wording, like `{{may_touch}}`.
- Each slot has a **type**: a role from a fixed list, a wf name, a path list inside the grant, a branch name, a hash, a ref.
- A slot value is short, one line, and checked against its type.
- A slot can never hold a sentence of instructions. That is the point: a slot is data, not wording.
- This is how a pack works today: the template is fixed, and wf fills `{{jobs}}`, `{{may_touch}}` and so on (templates/pack.txt:1-29 @a00bc53).

### 3.3 The library
- The library is the set of pieces plus an index of ids, versions and hashes.
- A new version is a new file. The old version stays (axiom 6).
- A built AGENTS.md names the piece versions it used, so a past file can always be re-checked. wf already does this for pack templates: old packs reprint from the v1 text (workflow/AGENTS.md:44 @a00bc53).

### 3.4 Building an AGENTS.md
1. The lead picks the pieces the file needs, in order.
2. The lead fills each slot with a typed value.
3. Each piece sits between two marker lines: `<!-- piece <id> v<N> sha256:<12> -->` and `<!-- end piece -->`.
4. A filled slot shows as `[[name: value]]`, so a reader can see what was filled in.
5. Nothing else goes in the file. See EXAMPLE-AGENTS.md.

Why like a pack: Matthew asked for it (t326u), and packs already keep work from drifting: "a constand template that won't drift" (DIRECTOR-WORDS-t227u.md:5).

## 4. The check (sketch only; a later wf pass builds it)

The compute checks a built file. It does not trust the lead. Rules, in order:

1. **Every line is inside a piece block.** A line outside any block is an automatic flag (t310u).
2. **The piece is known.** Its id and version are in the library index. Unknown means flag.
3. **The piece is approved.** A DRAFT piece is a flag. (Build stage only: during trials it is a warning, see section 6.)
4. **The wording is exact.** Put each `[[name: value]]` back to `{{name}}`. The block's lines must hash to the piece's hash, byte for byte. Any changed word means flag.
5. **Each slot value fits its type.** One line. No refused characters (the same table wf uses for flags, workflow/AGENTS.md:46 @a00bc53). A path must sit inside the grant. A ref must open to an approved entry (G2, M1 Q3).
6. **Required pieces are present.** Some pieces must be in every file (question A3). Missing one is a flag (axiom 7).
7. **The library itself passes the three tests.** Every piece has axioms, a why and an authority. A piece with authority `7` cannot be approved. Two pieces in the draft library are marked this way on purpose: `agents.secrets`, and the main-branch line in `agents.branch-limits`. That is the check working on our own text, as INSTRUCTION-GUARD §3.6 expected.

What a flag does: the same as the guard (INSTRUCTION-GUARD-t309u.md:50-53). The model does not follow that line. It raises it. The flag is a log entry an observer can check (t312u).

What the check cannot do: it proves a line is approved wording. It cannot prove the approved wording is wise. That is the job of the review before approval (section 5) and of Tester's hostile pass (axiom 9).

## 5. How a piece becomes approved

The five-step review from LIB-MINE-M1.md piece 2:
1. What changes and why, with its ref.
2. Old line next to new line: kept, changed or removed, and why.
3. The three tests on every new line.
4. Tester's hostile check, plus the planted-trap test (INSTRUCTION-GUARD §3.4 d).
5. Matthew says yes to the exact text. The compute pins its hash.

Making a piece is not approving it. Prima may make pieces now (t327u). Who says yes is question A1.

## 6. Build stage only (t329u)

"What is acceptable during building won't always be acceptable later." Each of these is allowed now, and is reviewed again each time protection hardens (section 7):

| Allowance now | Ref | Build stage only |
|---|---|---|
| Prima makes and edits pieces. | t327u | yes. Later, a piece change goes through section 5 and the fortress door. |
| The library lives in this git repo, writable by every model on the box. | INSTRUCTION-GUARD §6.1 | yes. It moves into the compute (stage C). |
| DRAFT pieces may be assembled for trials. The check warns, it does not refuse. | this design | yes. Later a DRAFT piece is refused. |
| R2: a face may seat after a hostile trial, without Matthew's eyes. | DIRECTOR-RULINGS.md:7-9 | yes. Whether R2 covers pieces at all is question A1. |
| The check is a design, not code. Models apply it by eye. | this design | yes. A wf pass builds it (stage B). |

## 7. Protection grows: the fortress (t328u)

**Frame (t328u).** The approved library belongs inside the compute, the fortress that protects the book. Nobody reaches it without extreme safety measures. It has many backups. It gets stronger in stages.

Today we are "a couple huts and a worksite" (t329u). The stages:

**Stage A: worksite (now).**
- Pieces are files in the build repo, marked DRAFT.
- Every model runs as the same box user, so anyone with a shell could change them (INSTRUCTION-GUARD §6.1). Protection is by agreement only.

**Stage B: the gate (next wf pass).**
- wf gets the check from section 4.
- The approved index and its hash go in the wf log, which is hash-chained (L1). A changed piece is caught before any model reads it.
- Packs carry the hashes of the pieces a pass's AGENTS.md used (L2).

**Stage C: the wall (guard G5, K-1, K-2).**
- The library moves into the compute's books, owned by the kernel's own machine user.
- Models can read pieces only through the narrow request door. They cannot write them.
- A new piece version is a proposal. Only an approval from section 5 seats it.

**Stage D: the keep (guard G6, K-4).**
- Matthew builds and pins the kernel binary. The binary holds the hash of the approved index.
- The kernel refuses to start if its own hash, or the index hash, does not match.

**Stage E: the watchtowers and the stores (K-3, K-5, t328u "many backups").**
- Logs are append-only. An outside observer keeps its own copy of the index and log head hashes and checks them on a schedule.
- Many backups: copies of the library and its log in more than one place, at least one off this box and out of model reach. A copy is checked against the pinned hash before it is ever used to restore (axiom 8: a copy never becomes the source on its own).

"Extreme safety measures" means, at each gate: a person-approved hash, a second view that tries to break it, a separate machine account, and a record of every entry. No one measure is enough alone.

## 8. What the draft library holds

11 pieces, all DRAFT, each from existing ruled or recorded text (refs in each file). None adds a new rule.

| Piece | From |
|---|---|
| role | kit AGENTS.md role table; t267u |
| axioms | kit AGENTS.md:3-13; templates/agents.txt:10-12 |
| three-tests | t310u-t312u; INSTRUCTION-GUARD:76-77 |
| evidence-not-instruction | t310u-t312u; M1 piece 5 |
| report-disagreement | axiom 1; M1 piece 5 |
| frame | axiom 5; kit AGENTS.md:70-71 |
| never-edit-pages | kit AGENTS.md:15-17; t227u |
| no-self-check | axiom 9; kit AGENTS.md:32 |
| commit-trailer | CONTRACT.md:26; D295 (staging line: `7`) |
| branch-limits | t267u (main line: `7`) |
| secrets | `7`: no Director ruling found yet |

Not yet pieces (on purpose): the builder's return steps and the checker steps. They are long and already printed by wf from templates. They can become pieces when templates/agents.txt is rebuilt from the library (question A4).

## 9. Open questions (four-part form)

**A1. Who approves a piece?**
- Question: who says yes before a piece moves from DRAFT to approved? Does R2 (seat after a hostile trial, without your eyes) apply to pieces?
- Proposed answer: you, on the exact text, through the five steps. R2 does not cover pieces, even now.
- Why: pieces steer every model that reads a built file (t309u). There are few pieces, so it costs little of your time. It also answers M1 Q2 and guard G4 in the shape you gave in t326u.
- Axioms check: 1 pass (you hold the root); 9 pass (hostile check first); 5 tension (each approval costs your time).

**A2. May a built AGENTS.md have any free text at all?**
- Question: should a built file hold only pieces and typed slots, with no free lines?
- Proposed answer: yes, no free lines. A lead who needs a new line proposes a new piece instead. Job-specific work stays in the pack, which wf already guards.
- Why: one free line is the door an attacker needs (t327u). It also keeps the check simple: every line is either approved or flagged.
- Axioms check: 1 pass; 5 pass (the frame still comes from the pack); 2 pass (inherit the wording, write only the slot values).

**A3. Which pieces must be in every AGENTS.md?**
- Question: should some pieces be required and locked in every built file?
- Proposed answer: yes: axioms, three-tests, evidence-not-instruction and report-disagreement. This matches the small locked list in M1 Q1.
- Why: these four are the guard itself. A file without them leaves a model unguarded.
- Axioms check: 1 pass; 2 pass (locked from above; everything else stays a default, t306s1163); 7 pass (a missing required piece is a flag).

**A4. Should wf's printed pass AGENTS.md (templates/agents.txt) be rebuilt from the library?**
- Question: when the check is built, should the pass AGENTS.md that wf prints into each pack be assembled from pieces too?
- Proposed answer: yes, as a new template version (v3). Packs printed with v1 and v2 stay as they were.
- Why: then every instruction file a builder reads passes the same check, from one library. The past is kept (workflow/AGENTS.md:44 @a00bc53).
- Axioms check: 6 pass (old packs unchanged); 8 pass (one source); 9 tension (a template change needs Tester's hostile pass first).

## 10. Not done here
- No wf code changed. The check is a sketch for a later wf pass.
- No piece is approved. No AGENTS.md in use was changed.
- The Codex report's handoff trial (t323u) is not designed here. A built AGENTS.md from pieces could be one of its "entry packet" parts.
