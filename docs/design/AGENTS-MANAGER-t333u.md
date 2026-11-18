# AGENTS.md manager for the compute (design proposal)

state: proposal for Matthew to review. Lines marked **Ruling** are his words. Everything else is Prima's proposal.
made: Wed 18 Nov 2026, about 3:32 PM EST, by Prima.
asked for: t332u, t333u (docs/review/DIRECTOR-AGENTS-DRAFT-t332u.md, DIRECTOR-WORDS-t333u.md).
replaces the shape of: AGENTS-TEMPLATES-t326u.md. Its 11 pieces in agents-pieces/ are kept as option drafts.
builds on: t306u, t306s1163, t307u, t309u-t312u, t326u-t329u; INSTRUCTION-GUARD-t309u.md; LIB-MINE-M1.md.

## 1. What Matthew said

> I want sections, and options for each section.  With model fillable fields and compute fillable.  The model fillable can't give anything more then like addresses or approved links. (t332u)

> We aren't rust only, I just wanted that for the core of the compute.  We can use NextJS for the Kamban workshop space. (t333u, point 1)

> ignore it's just a sample not what we are doing right now. (t333u, point 2, about his t332u file)

> This is a new piece we need to build our agents.md manager for compute. (t333u, point 3)

**Ruling (t332u).** An AGENTS.md is built from sections. Each section has options. Fields are either model-fillable or compute-fillable. A model may only fill in things like addresses or approved links.

**Ruling (t333u).** Rust is for the compute core only. NextJS is allowed for the kanban workshop front. His t332u file is a sample, not rules. The AGENTS.md manager is a new part of the compute.

## 2. The idea in one line

A lead does not write an AGENTS.md. A lead picks options. The compute writes the file.

## 3. The model

### 3.1 A file is a list of sections
- An AGENTS.md is an ordered list of sections, such as Role, Axioms, Frame, Project.
- The order is fixed by the section list, not by the lead.
- Some sections are **required**. A file without them is not built.
- Some sections are **optional**. The lead may leave them out.

### 3.2 Each section has options
- An option is one approved wording for that section, word for word.
- The lead picks **one option per section**. Nothing else.
- Example: the section "UI" could have the options "NextJS" and "none".

### 3.3 Each option carries its three tests
- **axioms**: which axioms it serves.
- **why**: why the wording exists.
- **authority**: the ref to the ruling behind it (t311u).
- It also has an id, a version, a hash (sha256 of its exact wording) and a state (DRAFT or approved).
- A new version is a new option file. The old one stays (axiom 6).

### 3.4 Locked kernel sections
- Some sections belong to the kernel. They are **locked**.
- Every file inherits them. No lead can swap, drop or reword them.
- Inheritance runs down one chain: kernel > desk > shelf > book (t306u).
- Above the book, a pick is a default. A lower level may change a default, but never a locked section (t306s1163).
- A book changes a default only in its 0000-0009 local-change area, with its why (t307u). The manager reads that entry; it is the only way a book's pick differs from its shelf's.

## 4. Two kinds of field

A field is a marked blank in an option's wording. Each field has exactly one kind.

### 4.1 Model-fillable fields
- The lead types a value. It must be one of these typed values:
  - a **seqaddr address** (it must parse and must exist);
  - a **link from an approved list** (the list is itself approved);
  - a **name from a list** (a role, a seat, a branch from the grant).
- Never a sentence. Never free text. One line, short.
- The compute refuses anything else. It uses the same refused-character table wf uses (workflow/AGENTS.md:46 @a00bc53).
- Why: a free line is the door an attacker needs (t327u). A typed value can only point, not instruct.

### 4.2 Compute-fillable fields
- The compute fills these from what it knows for sure:
  - hashes (for example of AXIOMS.md, or the option index);
  - dates and times;
  - page addresses and the grant's paths;
  - versions;
  - approved-by refs.
- Models never type them. If a selection tries to set one, that is a flag.
- Why: these values prove things. A model that types a proof could fake it.

## 5. What the manager does in the compute

1. **Stores options.** Each with id, version, hash, axioms, why, authority and state. Models can read them; they cannot write them.
2. **Builds a file.** Input: a *selection record* (which option per section, plus the model values). The manager checks every value, fills the compute fields, and renders the file.
3. **Verifies a file.** It rebuilds from the selection record and the stored compute values, then compares byte for byte. Any line that differs or is extra is an automatic flag (t310u).
4. **Logs everything.** Every build, verify and flag is a log entry an observer can check (t312u).
5. **Keeps approved options fixed.** A model may propose a new option version. Only an approval seats it (section 8, question M1).

A flag does what the guard says: the model does not follow that line, and raises it (INSTRUCTION-GUARD-t309u.md:50-53).

## 6. How a built file looks

```
<!-- agents file book:<addr> selection sha256:<12> built <date> -->
<!-- section axioms option agents.axioms v1 sha256:<12> locked kernel -->
Read docs/AXIOMS.md before you start. Its pinned hash is [[c:axioms_hash f802...]].
<!-- end section -->
<!-- section role option agents.role v1 sha256:<12> -->
You are [[m:role Builder]]. Your name is [[m:name b3]]. ...
<!-- end section -->
```
- `[[m:...]]` is a model value. `[[c:...]]` is a compute value. A reader sees at a glance who filled what.
- Nothing else is allowed in the file.

## 7. The 11 draft pieces as sections and options

Each draft piece becomes option v1 of one section. Slots are re-sorted into the two field kinds.

| Section | Owner | Req. | Locked | Option v1 (piece) | Fields |
|---|---|---|---|---|---|
| Role | desk | yes | no | 01-role | m: role (list), m: name (seat list) |
| Axioms | kernel | yes | yes | 02-axioms | c: axioms_hash |
| Three tests | kernel | yes | yes | 03-three-tests | none |
| Evidence | kernel | yes | yes | 04-evidence | none |
| Disagreement | kernel | yes | yes | 05-disagree | none |
| Frame | desk | yes | no | 06-frame | m: grant address; c: may_touch (from the grant) |
| Records | kernel | yes | yes | 07-pages | none |
| No self-check | kernel | yes | yes | 08-trial | none |
| Commit label | desk | yes | no | 09-trailer ⚠ | c: trailer (from the seat) |
| Branches | desk | yes | no | 10-branch ⚠ | m: push_target (branch list from the grant) |
| Secrets | kernel | yes | yes | 11-secrets ⚠ | none |

- Change from the old draft: `may_touch` and `trailer` move to the compute. The model now gives only the grant's address; the compute reads the paths and the seat from it.
- ⚠ = no recorded words from Matthew behind it yet. It cannot be approved until it has authority (question M4).

### 7.1 A project section, for illustration only
His t332u file is a sample (t333u). Its headings only show what a project section with options could look like:
- Section "UI": option `ui.nextjs` ("Use NextJS for the kanban workshop front", authority t333u point 1); option `ui.none`.
- Section "Compute core": option `core.rust` (authority t333u point 1).
- Section "Read first": a model-fillable link field, such as the sample's "view Axioms.md", picked from the approved link list.
None of these are proposed rules. They show the shape.

## 8. Rust core shapes (sketch, minimal)

```rust
enum Owner { Kernel, Desk, Shelf, Book }
struct Section { id: String, order: u16, owner: Owner, required: bool, locked: bool }
enum State { Draft, Approved { by_ref: String } }
struct OptionText {                 // one file per option version
    id: String, version: u32, section: String, state: State,
    axioms: Vec<u8>, why: String, authority: Vec<String>,
    fields: Vec<Field>, wording: String, sha256: [u8; 32],
    build_stage_only: bool,          // t329u
}
enum ModelKind { SeqAddr, Link { list: String }, Name { list: String } }
enum ComputeKind { Sha256Of(String), Date, PageAddr, Version, ApprovedBy, GrantPaths, Seat }
enum Kind { Model(ModelKind), Compute(ComputeKind) }
struct Field { name: String, kind: Kind }
struct Pick { section: String, option: String, version: u32, values: BTreeMap<String, String> } // model values only
struct Selection { file: String, level: Owner, parent: Option<[u8; 32]>, local_change: Option<String>, picks: Vec<Pick> }
struct BuildEntry { selection: [u8; 32], output: [u8; 32], options: Vec<[u8; 32]>, computed: BTreeMap<String, String> }
```
Files: `agents/sections.txt`, `agents/options/<section>/<id>.v<N>.md`, `agents/lists/<list>.txt`, `agents/selections/<file>.sel`. Build and flag entries go in the hash-chained log.

### 8.1 Where it lives (proposal)
- **Now (stage B):** a small new wf module, `src/agents.rs`, with two commands: `wf agents build <selection>` and `wf agents verify <file>`. wf already has the hash-chained log, the refused-character table and versioned templates.
- **Later (stage C):** the same module moves into `crates/compute` as `agents.rs`, behind the narrow request door (K-2). Models then reach it only by request.
- Rust, because this is the compute core (t333u). No new crate until the move.

## 9. Build stage now, fortress later (t328u, t329u)

| Allowance now | Build stage only |
|---|---|
| Prima makes and edits option drafts (t327u). | yes. Later only an approval seats an option. |
| Options live as files in the build repo, writable by any model on the box. | yes. Stage C moves them inside the compute, owned by the kernel's own user (K-1). |
| DRAFT options may be built into trial files; verify warns, it does not refuse. | yes. Later a DRAFT option is refused. |
| Verify is done by eye until `wf agents verify` exists. | yes. Stage B builds it. |

Stages stay as in AGENTS-TEMPLATES-t326u.md section 7: A worksite (now), B the gate (wf checks), C the wall (inside the compute), D the keep (person-pinned kernel holds the option index hash), E watchtowers and many backups.

## 10. Open questions (four-part form)

**M1. Who approves an option?**
- Question: who says yes before an option moves from DRAFT to approved? Does R2 (seat after a hostile trial, without your eyes) apply?
- Proposed answer: you, on the exact text, after Tester's hostile check. R2 does not cover options.
- Why: options steer every model that reads a built file (t309u). There are few options, so it costs little time. Same as A1 and M1 Q2.
- Axioms check: 1 pass (you hold the root); 9 pass (hostile check first); 5 tension (each yes costs your time).

**M2. Which sections are locked in the kernel?**
- Question: should Axioms, Three tests, Evidence, Disagreement, Records, No self-check and Secrets be locked kernel sections, with everything else a default?
- Proposed answer: yes, and keep the list this small. Secrets joins only once it has your authority (M4).
- Why: these are the guard itself. A file without them leaves a model unguarded. Everything else stays a default, as in t306s1163.
- Axioms check: 1 pass; 2 pass (locked from above, the rest inherited as defaults); 7 pass (a missing locked section is a flag).

**M3. Where is it built first?**
- Question: may the manager start as `wf agents build|verify` in wf, then move into the compute at stage C?
- Proposed answer: yes. wf already has the log, the character table and template versions, so it is the smallest first step.
- Why: it gets a working check soon, and the move later is one module. The compute's request door (K-2) is not built yet.
- Axioms check: 8 pass (one module, one source); 6 pass (logs kept through the move); 9 tension (Tester must re-check it after the move).

**M4. Will you give your words for the three ⚠ rules?**
- Question: may "add files by name only", "never merge into main, never force push" and "never print or commit a secret" become options, with your words as their authority?
- Proposed answer: yes. They are rules we already follow. Your yes, recorded verbatim, becomes their authority.
- Why: the check flags them today because no recorded words of yours stand behind them. That is the guard working on our own text.
- Axioms check: 1 pass (your words give the authority); 4 pass (the why is written down); 7 pass (fills a known gap).

## 11. Not done here
- No wf or compute code changed. No option is approved. No AGENTS.md in use was changed.
- Carried, not re-asked: no free lines in a built file (old A2); rebuilding wf's printed pass AGENTS.md from options (old A4).
