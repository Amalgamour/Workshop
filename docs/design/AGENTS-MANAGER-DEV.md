# AGENTS.md manager: dev doc (`wf agents build`, `wf agents verify`)

state: DEV DOC DRAFT. Not committed, not pushed. Not approved by Matthew. Asked for at t352u (Prima's relay).
made: Thu 19 Nov 2026, about 10:45 AM EST, by Designer.
merges: docs/design/AGENTS-MANAGER-t333u.md (Prima, 1c68f52; marked "Prima") and
scratch/AGENTS-MANAGER-design-draft.md (Designer; marked "Designer").
cites: wf as `wf:<file>:<line> @a00bc53` (workflow head); compute and docs at build 488d2ba. Both heads re-checked
Thu 19 Nov 10:40 AM EST.
marks: "His words" = recorded verbatim. "Proposed (Prima)" / "proposed (Designer)" = not his words. 7 = not settled.

## Summary for Matthew

1. The compute writes every AGENTS.md. A model never types one.
2. A lead picks one approved wording for each section.
3. A model can fill in nothing more than things "like addresses or approved links" (your words).
4. The compute fills the rest: versions, dates, branch, Prime, pins.
5. Every build is written in the log, with what went into it.
6. A check can rebuild the file and catch any changed word.
7. A changed file is flagged in the log for the lead to see.
8. A new wording is a new version. The old one stays.
9. Today this catches changes. It cannot block them yet. That comes later.
10. Nine questions for you are at the end. Each has a proposed answer.

## 1. What it is, and why

- **What.** A part of the compute that writes AGENTS.md files. "A lead does not write an AGENTS.md. A lead picks
  options. The compute writes the file." (Prima, t333u doc :25)
- **Why.** An AGENTS.md steers every model that reads it. One slipped-in line makes every model obey an attacker.
- **His words.**
  - "build anti hacker into the compute.  To protect us against hackers attacking agents.md files" (t309u.md:8)
  - "We have templates with exact wording for different sections of approved wording for agents.md or what ever
    comes next.  So a lead can build a agents like we build the packs of work." (t326u.md:7)
  - "I want sections, and options for each section.  With model fillable fields and compute fillable.  The model
    fillable can't give anything more then like addresses or approved links." (DIRECTOR-AGENTS-DRAFT-t332u.md:3)
  - "This is a new piece we need to build our agents.md manager for compute." (t333u.md:9)
- **Name kept loose.** "or what ever comes next" (t326u.md:7): the code must not hard-code the file name.

### Exists today (re-checked)
- wf prints one AGENTS.md per pass from a template built into the binary: wf:render.rs:15, :104-108, :209.
- The template version is pinned in the pack entry: wf:cmd.rs:368; wf:render.rs:23, :30-41. Old packs reprint
  from v1 (wf:render.rs:18-21; wf:AGENTS.md:44).
- A slot left unfilled is refused: wf:render.rs:45-53.
- Axioms and design hashes are pinned per pack: wf:render.rs:24-25; wf:cmd.rs:352.
- `wf verify` reprints every view, AGENTS.md included, and compares hashes: wf:render.rs:293-321; wf:lib.rs:138-159.
  `wf check` refuses if a view was edited: wf:cmd.rs:565-566.
- Append-only, hash-chained log: wf:log.rs:1-3, :94-111.
- One refused-character table: wf:chars.rs:1-7, :196, :236-241. Grant check: wf:page.rs:82; wf:cmd.rs:339.
- Pins for 04, 06 and last closed 05: wf:cmd.rs:222-229, :271, :343-345.
- Compute: writes need a token, the body's `by` is not trusted (crates/compute/src/lib.rs:87-96); all writes go
  through `propose` (crates/compute/src/store.rs:744); compute-only card fields are refused from others
  (crates/seqaddr-core/src/validate.rs:243-252).

### Does not exist (re-checked)
- No `wf agents` command (help list wf:lib.rs:20-38). No section, option or link library. No field kinds.
  No stamp entry for an AGENTS.md build.
- No AGENTS.md code in crates/compute (only a comment, crates/seqaddr-core/src/face.rs:12).
- The kit's top AGENTS.md (wf:AGENTS.md, 92 lines) is hand-written and unmanaged.
- **Gap.** Today's pass AGENTS.md copies in text the lead typed: jobs, checks, stop-if, the face 01 goal
  (wf:render.rs:83-93; wf:templates/agents.txt:15-22). That is more than "like addresses or approved links". Q7.

## 2. Inputs

1. **Options (templates).** One file per option version: id, section, version, exact wording, sha256 of the
   wording, axioms, why, authority, state (DRAFT or approved), build-stage flag (Prima, t333u doc :40-45).
   - Now: docs/design/agents-pieces/ (11 drafts, INDEX.md). All DRAFT.
   - Proposed (Prima, t333u doc :149): `agents/sections.txt`, `agents/options/<section>/<id>.v<N>.md`,
     `agents/lists/<list>.txt`, `agents/selections/<file>.sel`. Where they live: Q4.
   - A new wording is a new file and version; the old stays (axiom 6). Every build pins id, version and hash.
2. **Sections.** Ordered list: id, required or optional, locked or not. The list sets the order (Prima, :30-33).
   - Locked sections come from the kernel; no lead may swap, drop or reword them (Prima, :47-49; Q8).
   - Inheritance runs kernel > desk > shelf > book (his words t306u.md:5). Above the book a pick is a default
     (t306s1163.md:16). A book changes a default only in its 0000-0009 area (t307u.md:8; Prima's reading :52).
3. **One option per section.** No free lines (Prima's old A2, t333u doc :195).
4. **Field kinds.** Each blank has exactly one kind:
   - **fixed text**: the approved wording. Nobody fills it.
   - **model field**: his words: "like addresses or approved links". Proposed (Designer): the build accepts an
     address (it must parse and exist) or a link from the approved list, one line; anything else is refused
     until Matthew says more.
   - **name from a list** (role, seat, branch from the grant): proposed (Prima, t333u doc :62). Designer proposes
     instead that these be compute fields (Q7).
   - **compute field**: versions, pins (04, 06, last closed 05), pass address, branch, dates, Prime, hashes,
     grant paths, approved-by refs (Prima, :67-75). Only the compute fills them.
5. **Approved links.** A versioned, pinned list file. What counts and who adds: Q1.
6. **Selection.** The lead's input: one option per section, plus model-field values. Nothing else.

## 3. `wf agents build`

Steps:
1. Load sections, options and the link list. Re-hash each; refuse on any mismatch.
2. Read the selection. Every named section exists; every required and locked section is present.
3. Each pick: option exists at that version and hash, and (later) is approved.
4. Each model field: proposed (Designer) line as in section 2.4; same refused-character table (wf:chars.rs:196).
5. Fill compute fields from the log and the pack. A selection that sets one is refused (Prima, :74).
6. Pins must be current (same rule as wf:cmd.rs:343-345).
7. Render: sections in order, each between marker lines; model values `[[m:..]]`, compute values `[[c:..]]`
   (Prima, t333u doc :87-99). Nothing else is allowed in the file.
8. File a stamp entry in the log (wf: page log.jsonl, actor `wf`, role `tool`). Then print the file as a view.

Output: the AGENTS.md (a view, output only) and the stamp (selection hash; each option id, version and hash;
link-list hash; every compute value; output hash).

Refusals (each names section, field and why; exit 1; nothing written):
- wording not in the library (DRAFT warns during build stage; rule A9);
- unknown section, option or field;
- a model field outside the proposed line (section 2.4);
- a selection setting a compute field;
- a stale pin;
- a missing required or locked section;
- an option with no axioms, why or authority (t310u, t311u).

## 4. `wf agents verify`

- **What.** Rebuild from the stamp's pinned inputs. Compare byte for byte with the file (Prima, :81).
- **Finds.** Hand edits; extra lines; a missing file; a library file changed since the build.
- **Reports.** `ok: 05.02 AGENTS.md matches stamp entry 41`, or the first differing line, its section, and the
  failed check. Builder text escaped on output (wf:AGENTS.md:48).
- **Exit codes (proposed, Designer).** 0 match; 1 differs; 2 cannot verify (stamp or input missing, unknown
  version). wf today exits 1 on any error (wf:main.rs:7-9).
- **Logged.** A failure files a flag entry: file, line, test, why (INSTRUCTION-GUARD-t309u.md:50-53). A clean
  verify writes nothing, like `wf verify` now (wf:lib.rs:104, :138-140).
- **Never rewrites picks.** `--fix` only reprints from the stamp, as wf:lib.rs:141-149 does.

## 5. The fortress

His words: "the compute is the the fortress that protects the book.  No model or person should be able to access
it without extreme safety measures in place.  With many backups." (t328u.md:7). "our goal is to have them
protected so a model or 3rd party can't get control of our workshop." (t327u.md:7). Shape: "The page is the what
the compute sits in.  person, model sit outside" (t262u.md:5-7).

- **Who writes.** Only the compute (wf for now). The file is a view of the log (wf:lib.rs:1-3;
  wf:templates/agents.txt:28-29 "Do not edit this file").
- **Output only.** A change is a new selection or a new option version, never an edit.
- **Changes are proposals.** The compute files them; a wording is not live until approved (Q6). Same rule as
  "no role writes a face directly" (docs/design/WORKFLOW-TOOLS.md:215-240).
- **Check on start.** Verify before `claim` and `pack` (new). `check` already refuses edited views (wf:cmd.rs:565-566).
- **Check on push.** No push hook exists; the push is the ping (WORKFLOW-TOOLS T3, open). `return` already
  holds the diff to the frame (wf:cmd.rs:446). Add: verify on return.
- **Stages (Prima, t333u doc :165; AGENTS-TEMPLATES-t326u.md section 7):** A worksite (now), B the gate (wf checks), C the wall
  (inside the compute, its own user), D the keep (person-pinned option index hash), E watchtowers and backups.
- **Honest limit.** Every model is the same box user today. This detects edits; it cannot stop them until
  stage C. His words: "Right now, we are just a couple huts and a worksite." (t329u.md:7)

Build-stage allowances (Prima, t333u doc :156-163): Prima makes option drafts (t327u); options are files any box
model can write; DRAFT options may be built for trials and verify warns; verify by eye until built.

## 6. Data shapes (sketch, not code)

```
enum Owner     { Kernel, Desk, Shelf, Book }                    // Prima
enum State     { Draft, Approved { by_ref: String } }
struct Section { id: String, order: u16, owner: Owner, required: bool, locked: bool }
struct Template {                                               // one option version; one file
    id: String, section: String, version: u32, state: State,
    wording: String, sha256: String, fields: Vec<Field>,
    axioms: Vec<u8>, why: String, authority: Vec<String>, build_stage_only: bool }
enum ModelKind   { Address, Link { list: String } }  // proposed line for "like addresses or approved links"
                 // Name { list } is proposed (Prima); left out until Q7 is answered
enum ComputeKind { Version, Pin(Face), PassAddr, Branch, Date, Prime, Hash(String), GrantPaths, ApprovedBy }
enum FieldKind   { Model(ModelKind), Compute(ComputeKind) }     // fixed text has no field
struct Field     { name: String, kind: FieldKind }
struct Fill      { field: String, value: String, by: FillBy }   // FillBy { Model, Compute }
struct Pick      { section: String, option: String, version: u32, model_fills: Vec<Fill> }
struct Selection { target: String, level: Owner, local_change: Option<String>, picks: Vec<Pick> }
struct Stamp {                                                  // filed in the log; verify replays it
    entry: u64, target: String, picks: Vec<(String, u32, String)>, link_list: String,
    compute_fills: Vec<Fill>, selection_hash: String, output_hash: String }
```

CLI:
- `wf agents build <page> <NN> --select FILE --as NAME`   lead; files a stamp, prints the view.
- `wf agents verify <page> [<NN>|--all] [--fix]`          anyone; read only unless --fix.
- `wf agents list [--section S]`                           read only: sections, options, states, links.
- Stage C: the same verbs behind the compute's request door (Prima's M3, now Q9).

## 7. Build order and tests

1. Library loader, re-hash, `wf agents list` (read only). Test: a tampered option is refused.
2. Field kinds and checks. One test per refusal: free text, unlisted link, bad address, compute field set,
   refused character, unknown field, missing locked section.
3. Render and stamp. Test: same selection twice gives the same bytes (golden file).
4. Verify. Tests: hand edit, extra line, missing file, changed library, unknown version (exits 0, 1, 2).
5. Hooks: verify before claim and pack, and on return. Test: an edited AGENTS.md blocks claim.
6. Pass template v3 from the library (Prima's old A4, t333u doc :195). Waits on Q7. v1 and v2 packs reprint unchanged.
7. Move into crates/compute behind `propose` (stage C). Waits on Q9.

Fixtures (proposed): `tests/fixtures/agents/` with lib-ok/, lib-tampered/, sel-ok.txt, sel-freetext.txt,
sel-badlink.txt, sel-outside-grant.txt, sel-sets-compute.txt, sel-no-locked.txt, built-ok.md, built-handedit.md.
Each refusal fixture is named for the rule it breaks. Tester's hostile pass comes first (axiom 9).

## 8. Rules table

Axiom lines: 1 Axioms.md:13, 2 :15, 3 :17, 4 :19, 5 :21, 6 :23, 7 :25, 8 :27, 9 :29.

| # | Rule | Why | Axioms | Authority |
|---|---|---|---|---|
| A1 | An AGENTS.md is built only from approved section wording. | no stray line can steer a model | 1 pass, 2 pass, 8 pass | t326u.md:7 |
| A2 | Each section has options; the lead picks one. | choice without new words | 2 pass, 3 pass | DIRECTOR-AGENTS-DRAFT-t332u.md:3 |
| A3 | A model can fill in nothing more than things "like addresses or approved links". | a pointer cannot give orders | 1 pass, 8 pass, 5 tension (less room to explain) | t332u.md:3 |
| A3a | Proposed line: the build accepts addresses and approved links; anything else is refused until Matthew says more. | a check needs a clear edge | 1 pass, 7 pass (unknown stays out) | proposed (Designer) |
| A3b | A model may also pick a name from a list (role, seat, branch). | short typed values | 1 pass, 2 tension (Designer prefers compute fills) | proposed (Prima) |
| A4 | Only the compute fills versions, pins, dates, Prime, branch, hashes. | a model that types a proof could fake it | 1 pass, 6 pass | t332u.md:3; DIRECTOR-RULINGS.md:193 (his yes), :197 (recorded reading) |
| A5 | The manager is part of the compute core, in Rust. | the core must be secure | 1 pass, 3 pass | t333u.md:7, :9 |
| A6 | Wording is protected from models and outsiders. | no one takes control of the workshop | 1 pass, 9 pass | t327u.md:7; t309u.md:8 |
| A7 | Nobody reaches the library or builds except through the compute. | the compute is the fortress | 1 pass, 8 pass, 7 tension (not true until stage C) | t328u.md:7; t312u.md:8 |
| A8 | Every option carries axioms, why and authority; one missing is a flag. | so an observer can check | 4 pass, 1 pass, 7 pass | t310u.md:8; t311u.md:8; t312u.md:8 |
| A9 | Build-stage allowances are marked and reviewed later. | what is fine now is not fine later | 9 pass, 7 tension | t329u.md:7; t327u.md:7 |
| A10 | Picks inherit kernel > desk > shelf > book; above the book a pick is a default. | same shape at every scale | 2 pass, 1 pass | t306u.md:5; t306s1163.md:16 |
| A11 | Locked kernel sections cannot be swapped, dropped or reworded. | the guard itself must be in every file | 1 pass, 2 pass, 7 pass | proposed (Prima), M2 -> Q8 |
| A12 | AGENTS.md is output only; changes come as proposals filed by the compute. | roles stay outside the page | 1 pass, 6 pass, 8 pass | proposed (Designer), from t262u.md:5-7 |
| A13 | Verify compares byte for byte; any difference is a flag. | a changed word is a changed order | 6 pass, 9 pass | proposed (Designer); "automatic flag" t310u.md:8 |
| A14 | A build with a stale pin is refused. | the file must match the live record | 1 pass, 6 pass | proposed (Designer); pins open as T4 (WORKFLOW-TOOLS.md:304-308) |
| A15 | A new wording is a new version; old versions and builds stay. | the past is not rewritten | 6 pass, 2 pass | proposed (Prima, :45); wf practice wf:AGENTS.md:44 |
| A16 | Every build, refusal and failed verify is a log entry. | so an observer can check | 6 pass, 9 pass | t312u.md:8; detail proposed (Prima :82, Designer) |
| A17 | Model fields pass the refused-character table. | hidden characters hide orders | 1 pass, 9 pass | proposed (Prima :64); table wf:chars.rs:1-7 |
| A18 | Texts of pieces 09 (stage by path), 10 (branch), 11 (secrets) are approved. | known safety rules | 1 pass, 4 pass | t335s1296.md:12 |
| A19 | Who approves a wording change: not recorded. | wording steers every model | 1 pass, 5 tension | 7; proposed (Prima M1, Designer) -> Q6 |

Rules count: 21 rows (11 with recorded authority, 2 recorded in part, 8 proposed).

## 9. Open questions (four-part form)

Mapping: Prima's M1 -> Q6 (merged). M2 -> Q8. M3 -> Q9. M4 answered at t335s1296 (t335s1296.md:12-14), not
re-asked. Her old A2 and A4 are carried (sections 2.3, 7.6), not re-asked.

**Q1. What is an "approved link", and who keeps the list?**
1. Question: your words are "like addresses or approved links". What may a link point at, and who adds one?
2. Proposed (Designer): a repo path or seqaddr address already in the book; no web addresses for now. The list
   is a versioned file; adding a link is a wording change (Q6).
3. Why: a web link can change under us, and a third party could control it (t327u.md:7). Hurt: every model.
4. Checked: 8 [Axioms.md:27] pass. 1 [:13] pass. 5 [:21] tension (some work needs outside docs).

**Q2. May an address point outside the grant?**
1. Question: can a model field name an address the pass may not touch?
2. Proposed: yes for reading, marked "read only"; never as may-touch (that stays a compute field from the grant).
3. Why: models must read governing pages (axioms, seqAddr) that no pass may write.
4. Checked: 5 [:21] pass. 1 [:13] pass. 8 [:27] pass.

**Q3. What happens when verify fails mid-pass?**
1. Question: if a pass's AGENTS.md fails verify after claim, does work stop?
2. Proposed: a flag is filed; return, check and signoff are refused until Prime reprints from the stamp and writes
   why on 06. The work in git is kept.
3. Why: the worker may have read bad text. Hurt: the checker, judging against a forged frame.
4. Checked: 7 [:25] pass. 9 [:29] pass. 3 [:17] tension (stalls the worker).

**Q4. Where do the templates live?**
1. Question: in the build repo, the wf kit, or the compute's own store?
2. Proposed: now, `agents/` in the wf kit, marked build stage (Prima's file layout). Stage C: inside the compute.
3. Why: wf reads them from the kit; stage C is where they are safe (t328u.md:7).
4. Checked: 2 [:15] pass. 1 [:13] tension (any box user can edit them now). 6 [:23] pass.

**Q5. One AGENTS.md per pass, or per page?**
1. Question: does each pass get its own built file?
2. Proposed: one per pass, as wf does now (wf:render.rs:209). Each pins its own inputs.
3. Why: a pass is what is issued and checked; one per page would drift between passes.
4. Checked: 6 [:23] pass. 5 [:21] pass. 2 [:15] tension (repeats sections each pass).

**Q6. Who approves a wording change, and how is it versioned? (merges Prima's M1)**
1. Question: who says yes before an option moves from DRAFT to approved, and how is it recorded?
2. Proposed (Prima M1, Designer): a proposal entry (old text, new text, why, authority); Tester's hostile check;
   then your yes on the exact text; the compute pins the new hash as a new version. Prima proposes that the
   seat-without-your-eyes allowance does not cover options.
3. Why: options steer every model (t309u.md:8). Recorded words only let Prima make them "for now" (t327u.md:7).
4. Checked: 1 [:13] pass. 6 [:23] pass. 9 [:29] pass. 5 [:21] tension (each yes costs your time).

**Q7. What about text a lead types today (jobs, checks, stop-if, goal), and Prima's "name from a list"?**
1. Question: today's pass AGENTS.md copies these in (wf:render.rs:83-93). Does that fit "like addresses or
   approved links"? And should role, seat and branch be model picks from a list?
2. Proposed (Designer): move the typed text to PACK.md and PROMPT.md; AGENTS.md points to the pack by address
   and hash. Role, seat and branch become compute fields from the claim and grant. Prima's proposal keeps them
   as model "names from a list" (t333u doc :62). Both are proposals.
3. Why: the pack is already guarded and pinned; a pointer cannot instruct.
4. Checked: 8 [:27] pass. 5 [:21] tension (the frame moves one file away). 6 [:23] pass (v1, v2 packs unchanged).

**Q8. Which sections are locked in the kernel? (Prima's M2)**
1. Question: should Axioms, Three tests, Evidence, Disagreement, Records, No self-check and Secrets be locked,
   with everything else a default?
2. Proposed (Prima): yes, and keep the list this small. Secrets now has your words (t335s1296.md:12).
3. Why: these are the guard itself; a file without them leaves a model unguarded (Prima, t333u doc :178).
4. Checked: 1 [:13] pass. 2 [:15] pass. 7 [:25] pass (a missing locked section is a flag).

**Q9. Build it in wf first, then move it into the compute? (Prima's M3)**
1. Question: may the manager start as `wf agents build|verify`, then move into the compute at stage C?
2. Proposed (Prima): yes. wf already has the log, the character table and template versions.
3. Why: a working check soon; the later move is one module. The compute's request door is not built yet.
4. Checked: 8 [:27] pass. 6 [:23] pass. 9 [:29] tension (Tester must re-check after the move).

## What is his words vs our reading

1. **t311u.** The brief said every rule needs why, axioms and authority "(t311u)". His t311u words are only
   "Where is the authority for this action." (t311u.md:8). Axioms and why are t310u.md:8. t312u.md:8 confirms
   Prima's reading of t311u.
2. **t328u.** Typed after a question about pushing; it does not answer it (t328u.md:3). It is about the compute
   guarding the book. Using it for templates is a reading (supported by t327u.md:7).
3. **t327u.** Besides "protected", his words let Prima make templates for now ("for not", read as "for now",
   Prima's reading, t327u.md:9).
4. **The t332u draft file.** t333u point 2: "ignore it's just a sample not what we are doing right now." That
   point 2 is about his file is Prima's reading (t333u.md:11). This doc uses his covering words (draft.md:3),
   not the file's content.
5. **"like addresses or approved links".** His word is "like", which is softer than "only". This doc keeps
   "like". Where the build needs a line, that line is a proposal (A3a). Prima's "name from a list" is a
   proposal (A3b, Q7).
6. **Who approves wording.** "Only Matthew approves wording" was Designer's framing, taken from the standing
   approval rule for this build. It has no recorded source. Q6.
7. **`wf agents`.** His words: "agents.md manager for compute" (t333u.md:9). Starting in wf is Prima's
   proposal M3 (Q9).
8. **t350u.** No recorded file for t350u in docs/review.
9. **t352u.** No recorded file for t352u in docs/review (checked with rg). The ask for this dev doc is relayed only.

## Not done here
- No repo file changed. No code. No option approved. Nothing pushed.
- Prima's section table of the 11 draft pieces is not repeated; see t333u doc :101-117.
