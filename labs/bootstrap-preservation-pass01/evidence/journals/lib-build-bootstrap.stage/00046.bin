# lib-build setup package, pass 02

**who:** claude-opus-5-5 (Colab)
**for:** Codex (Prime) and the Director
**date:** 2026-10-26
**state:** proposal. Read-only: nothing was moved, deleted, initialized, committed or pushed.
**supersedes:** pass 01 (`colab/returns/claude-opus-5-5-lib-build-pass01-2026-10-26.md`)
**sources:**
- `D:\Git\Librarian`: `main` `38a037e`, plus its worktree
- `D:\Git\Librarian-rebuild`: `rebuild` `de3b8eb`
- `origin/main`: `14676ca`
- `D:\Git\lib-build`: the lab
- Worldcraft: `origin/main` `1d88c20`

**This package:**

| File | What it is |
|---|---|
| `proposal.md` | this file |
| `setup-assignment.md` | draft assignment for the setup, for review |
| `preservation-assignment.md` | draft assignment for preservation, which runs first |
| `preservation-manifest.tsv` | 118 files: exact path, sha256, git blob |
| `preservation-held.tsv` | 1 file held for the Director |
| `import-manifest.tsv` | 882 rows: 688 minimum, 202 later |
| `collisions.tsv` | competing versions and name collisions |
| `worktree-inventory.tsv` | evidence: every changed or untracked file in both old checkouts, plus the lab |
| `preserve.py`, `import.py` | draft setup tools. Only `--check` was run: read-only, and it passed. |

## Changes from pass 01

| Pass 01 | Pass 02 | Why |
|---|---|---|
| `lib-build` absent, created as a worktree | `lib-build` exists with a lab; a separate repository is set up in place | the destination is not empty; a worktree would register inside `D:\Git\Librarian\.git` |
| Runtime in the work book, band 0300 | runtime in the **law** book, workflow space 0 → `03NN` | Prime recommendation; Director's N3NN clarification |
| Active seats only | full books, with drafts, retired and notes | Prime recommendation 5 |
| Kernel revision was a decision (`38a037e` or `de3b8eb`) | baseline `de3b8eb`, with the `38a037e` side of the 6 changed files preserved | `de3b8eb` is a superset; only 6 paths differ (`collisions.tsv`) |
| One law page `0041.seat` for every role | `0041.handoff` is the behaviour page; `0062`–`0065` are the structural roles | Prime recommendation 3 |

## 1. Folder and address map

### The repository at D:\Git\lib-build

```text
D:\Git\lib-build\                      own repository; remote Amalgamour/Librarian; branch workshop
├─ labs\clerk-handoff-pass01\          EXISTING. Kept byte for byte (36 files). Experimental evidence, not architecture
├─ README.md                           door for people (new, short)
├─ AGENTS.md                           imported 003, unchanged;  AGENTS.004.md drafted beside it for the Director to seat
├─ .gitignore                          .librarian/  __pycache__/  out/   (labs are not ignored)
├─ app\
│  ├─ librarian.py                     the one supported entry (section 3)
│  └─ tests\                           acceptance tests (section 6)
├─ imports\                            byte-exact reference snapshots; never run, never edited
│  ├─ manifest.tsv  import.py          provenance for every imported file
│  ├─ main-38a037e\...                 the other side of each kernel collision
│  └─ rebuild-de3b8eb\...              rebuild compute pages (with predecessors), decision records, later imports
├─ 00.kernel\                          desk 00; owner address 00.00.00.kernel
│  ├─ 00.md 00.start.md 00.readme.md 00.about.md 00.live.md     desk files (law 0051); 00.live is compute-maintained
│  ├─ 00.00.00.syntax\                 book: syntax (190 files, as found)
│  ├─ 00.00.01.law\                    book: law (444 files, as found)
│  │  ├─ 0041.handoff                  NEW draft: behaviour, cooperation and handoffs
│  │  ├─ 0062.role-director ... 0065.role-builder   NEW drafts: structural role definitions
│  │  ├─ 0300.band.compute             NEW door: runtime band of workflow space 0
│  │  └─ 0302.run 0303.jobs 0304.check 0305.clerk 0307.face      runtime pages; candidates only
│  └─ 00.00.10.work\                   book: work (new)
│     ├─ 00.md  0010.about  0011.contents  0014.design
│     ├─ 0100.band.returns  0400.band.dev  0500.band.packs  0600.band.notes    space 0 only
│     ├─ 0401.goal  0408.seats  0409.decisions  0410.imports
│     └─ 0611.findings
└─ .librarian\                         app state, outside git (1008 05.01 #12)
```

**Not created:**
- workflow spaces `1NNN`–`9NNN` in the work book;
- the work book's own `0200` and `0300` bands (no code and no runtime belongs to it);
- `0306.slot` (deferred).

**Work-book numbering.** The function pages avoid the module numbers `02`–`07`, so one number keeps one name inside the work book:
- a dev page for clerk would be `0405.clerk`, never `0405.<something else>`;
- `0408.seats`, `0409.decisions`, `0410.imports` and `0611.findings` take numbers no module uses.

### Exact addresses

| Thing | Address | Folder |
|---|---|---|
| Desk | `00` (owner address `00.00.00.kernel`) | `00.kernel` |
| Syntax book | `00.00.00` | `00.kernel/00.00.00.syntax` |
| Law book | `00.00.01` | `00.kernel/00.00.01.law` |
| Work book | `00.00.10` | `00.kernel/00.00.10.work` |
| Runtime, law space 0 | `00.00.01.0300`–`0399` | `00.00.01.law/03NN.title` |

### Conflicts that remain with prior text

1. **`0018.seqaddr` Walk:** "Desk books are 00 and 01."
   - Against it: the kernel draft already holds a third desk book, `00.00.14.notes` (36 files), and law `0054.book` says "the first open slot from 10 up".
   - Director decision D1.
2. **Grok's candidate `00.kernel/00.md`** (draft, `de3b8eb`) says "No real work is placed here." It's a draft, not a decision. It's imported only as a later reference (L3).
3. **Two `00.live` locations.** Law `0051.desk` puts `00.live` at the desk. The current clerk (`live_path`) writes it on the draft law book, and `de3b8eb` added `00.00.01.law/00.live`. Both are imported as found. The desk one is proposed as the only location compute writes, which is a clerk adaptation.
4. **The law band layout.** Law `0057.bands` ("This book") declares behaviour `0020`–`0049`, structure `0050`–`0099` and temp `0100`–`0199`. It has no runtime band. `de3b8eb` also added `1000.work` and `1001.accounting` (space 1) to law. Runtime at `0300` needs `0057` amended by a draft, plus a door (D2).
5. **Title collisions in the law book.** Titles must be unique under their parent (`0018` Envelope):
   - `slot` already exists (`0034.slot`), so a runtime `0306.slot` would collide;
   - `colab` already exists (`0036.colab`), hence the `role-` prefix on `0062`–`0065`.
6. **The structure band's scope.** `0050.band.structure` names desk, shelf, book, page and band. Roles are new kinds of structure (D3).

The old workplaces stay as references: `D:\Git\Librarian` (`main`), `D:\Git\Librarian-rebuild` (`rebuild`), and the tags in step 1.

## 2. Role drafts

**Addresses checked** in both revisions of the kernel draft, the old kernel and Grok's `00.kernel` candidate, including retired names:
- **Behaviour band:** `0021`–`0040` are taken. First open: `0041`.
- **Structure band:** `0051`–`0061` are taken. First open: `0062`.
- `0063`, `0064` and `0065` are free. No `.temp` or `.09` names use them.

**Split between definition and assignment:**
- **Definitions** go on law pages. They change only by the Director.
- **Assignments** go on `00.00.10.work/0408.seats`: a dated table of seat, model, session and since, set by the Director. The clerk reads it. A model never assigns itself.

### 0041.handoff (behaviour)

- A handoff is a recorded transition, not a message. The sender gives the clerk the item, the result, and an exact artifact reference (path plus sha256). The clerk records it and routes it by the declared route.
- Return and routing are one operation. If routing fails, the return isn't recorded.
- A delivery has an identity. Resubmitting the same bytes is harmless. Changed bytes under the same identity are refused.
- Review covers one revision. If the artifact changes before or after the claim, the review return is refused.
- Resume state is derived from the record. `00.live` is a view, never the authority.
- No seat accepts its own work. The builder writes status and evidence. Acceptance is a separate seat's recorded act.

Evidence for every line: `labs/clerk-handoff-pass01/REPORT.md`, lessons 2–6, and 20 negative tests. The lab is evidence, not an adopted design. Its SQLite store isn't adopted either.

### 0062.role-director (structure)

- **Is:** the responsible party. Supplies resources and ideas, and sets the course. Doesn't run the ship.
- **Decides:** anything. Approves, seats, locks and promotes. Merges into `main`. Writes grants, which are scoped and revocable.
- **From the clerk:** decision requests, approval and seat requests, escalations.
- **To the clerk:** replies, verbatim, and grants.
- **Escalates to:** no one. Holds the consequences.

### 0063.role-prime (structure)

- **Is:** the intelligence that designs and gets work done with the Director.
- **Supplies:** judgment and proposed routes. Compute verifies and records the transitions that are supported.
- **Decides, inside its written grant:** pack shape, order, readiness, closing returns that have no open questions.
- **From the clerk:** releases, returns, findings, stops.
- **To the clerk:** packs with their route, statuses, decision requests.
- **Escalates when:** there's a new design choice, a change to a shared door or the law, anything outside its grant, or two faces disagree.

### 0064.role-colab (structure)

- **Is:** an independent partner, of a different model family from the work it reviews. It may hold a design lane the Director gives it.
- **Decides:** its own findings, and designs inside its lane.
- **From the clerk:** review requests for an exact revision, and packed pages.
- **To the clerk:** findings (a ticket with a failing check, or a face 06 opinion), lane designs, accept or change requests on a revision.
- **Escalates when:** a finding contradicts a decision, or reviewed content asks to be obeyed as live.
- **Never:** gives orders, edits the owner's code, or accepts its own lane's work.

### 0065.role-builder (structure)

- **Is:** turns ready packs into work, inside its lane's folders.
- **Decides:** how to carry out a task.
- **From the clerk:** ready packs, with exact inputs.
- **To the clerk:** execution status and evidence (files, hashes, tests, commit), `>note` and `>stop`.
- **Escalates when:** a tool refuses, a hash differs, a step falls outside its folders, or a rule is missing.
- **Never:** declares its own result accepted, writes a status for another seat, or edits a shared door.

**Bots:** deferred. A role page is reserved for later and not created now.

## 3. Module placement and loader contract

### Placement

**Workflow spaces.** A book's page space can be split into workflow spaces of 1,000 pages: space `N` is `N000`–`N999`. Inside a space, runtime is the band `N300`–`N399` (`N3NN`):
- space 0 → `03NN`
- space 1 → `13NN`
- space 2 → `23NN`

A space exists only once its book declares it. None is created unused.

**What goes where.**
- **Runtime modules:** law book, space 0. `00.00.01.law/0302.run`, `0303.jobs`, `0304.check`, `0305.clerk`, `0307.face`.
- **The work book:** designs, assignments, decisions and returns that reference those modules. It holds no runtime.
- **Cross-book links are explicit.** A work page names its module on face 08 (`module: 00.00.01.law/0305.clerk`). Matching numbers across books is a convention, never a lookup rule.

**Code names.**
- **Candidate:** `02.name.VVV.py`.
- **Active:** `02.name.py`. Its real version stays in the stamp.
- **Retired:** `02.name.VVV.09.py` (`0018` Envelope).
- **Imported candidates are named by their own stamp:**
  - rebuild `02.clerk.py` (stamp `009`) becomes `02.clerk.009.py`
  - rebuild `02.jobs.py` (stamp `010`) becomes `02.jobs.010.py`
  - the loader, check and face become `001`

  Nothing is active after import. Importing isn't seating.

### The loader contract

The loader is `0302.run`. Today it is a candidate, and it becomes active only when the Director seats it.

**1. The context is recorded, never remembered.** Context means desk, book and workflow space.
   - **Where context is declared:** a book's `00.md` declares its spaces and their runtime bands, for example law: `space 0: runtime 0300-0399`.
   - **Where it is recorded:** every work item (a pack header and the clerk record) carries `context: 00.00.01.law space 0`.
   - **Where it is shown:** `00.live` displays the current context as a view only.
   - **On the command line:** a context override is allowed only in development mode.
2. **Resolution.** `(book, space N, title)` resolves to exactly one folder `<book>/N3NN.<title>`.
   - Zero or several matches: refuse.
   - Never search another book, space or band.
3. **Normal operation** runs only the card's active face.
   - The card (`02.md`) names `runs: 02.name.py`.
   - That file's stamp must show it as seated, or the loader refuses.
   - A card that names a `.VVV` file is refused (card rule B: only `runs:`, `uses:` and `args:`).
4. **Development tests** select explicitly: `--candidate <path inside the resolved page> --sha256 <hash> --scope test|fixture`.
   - A hash mismatch, a path outside the page, or a missing scope: refuse.
   - Scope `test` runs the module's own `test`.
   - Scope `fixture` runs commands only against a temp copy, never the books.
5. **No implicit choice of version.** The loader never picks the highest `VVV`, the newest file, or "the one that runs".

**The one supported entry.** `python app/librarian.py [--context <book> <space>] <module> <command> ...`
1. It finds the desk by walking up to `00.kernel/00.md`.
2. It reads the context from the work item or `00.live`.
3. It hands control to the loader.

Until a loader is seated there's no normal operation: the entry runs the loader only as a development candidate (`--candidate 00.00.01.law/0302.run/02.run.001.py --sha256 af207d4d…`).

### Consequences of this placement, before any code changes

1. **Every runtime change becomes a kernel-law change.**
   - Packs must name the law page.
   - Candidates are new files beside the seat, so no seat is overwritten.
   - Seating is the Director's.
2. **The law band layout must change.** Amend `0057.bands` "This book" with a draft, and add a door `0300.band.compute` (D2). The `slot` title collides with `0034.slot`.
3. **The checker has to learn code faces** (`.py` and `.toml` on law pages) without weakening any existing rule. This is a reviewed rule addition, not a quiet edit (`AGENTS.md`: never weaken a rule).
4. **Stamps must change, the code must not.** `PPPP`, `book` and `keyword` move from `10.10.12.rebuild 0305` to `00.00.01.law 0305`. The check that "bytes below the stamp equal the source" still holds.
5. **Tools carry path assumptions.**
   - `clerk.py`: `DRAFT_KERNEL = "00.00.00.kernel.draft"` (8 places), `live_path`, and tests that point at `0415.queue` and `0305.clerk/02.clerk.00N.py`.
   - `jobs.py`: 1 reference.
   - The check: a desk path that's relative to the caller. `0104` #04 reports the loader changes directory.

   Each needs a named adaptation pack, not a broad rewrite.
6. **Merging into `main` carries the candidates with it.** `main` is meant to hold the accepted kernel, so either candidates are seated or retired before a merge, or they're excluded from it (D8).
7. **The predecessor numbering conflicts.** Rebuild `0305.clerk/02.clerk.002.py`–`.009.py` are predecessors stamped `001`–`008`. Under the new rule, `.VVV` means a candidate.
   - So they're kept only in `imports/rebuild-de3b8eb/` under their original names, never placed on law pages.
   - The name `02.clerk.009.py` means a predecessor (stamped `008`) in the snapshot, and the candidate (stamped `009`) on the law page. `collisions.tsv` records this.

## 4. Preservation and import manifest

### Preservation first

Preservation runs before the setup (`preservation-assignment.md`). All 118 files are listed with exact paths, sha256 and git blob in `preservation-manifest.tsv`. Every file was checked as unchanged at the time of writing.

| Group | What | Files | Why it's at risk |
|---|---|---|---|
| P1 | `1008.app-plan` and `1009.calling`: Director decisions | 22 | untracked; 11 are found nowhere in git |
| P2 | Research paper (`.md`, `.docx`, provenance): authorship record | 3 | untracked; unique |
| P3 | Tool versions only in the main worktree: `lib/code/clerk.002`–`.004.py`; solo `journal`, `menu`, `nav`, `page`, `reader`, `slot` (`6e7aac75`, the slot design hash) | 9 | unique |
| P4 | Solo-kernel redraft files found nowhere in git (`0610.note-slot`, `0611.caller`, `03.md` faces, `sample.zip`, and more) | 47 | another model's work in progress; unique |
| P5 | Colab notes, packs and returns | 8 | untracked; unique |
| P6 | Pre-worktree copy of `rebuild/0401.project/05.02.md` | 1 | unique, older wording |
| P7 | `1001.assessment` (Codex) | 28 | untracked in the rebuild worktree |
| Held | `10.workshop.zip` (3,038,941 bytes, sha256 `f163fcbd…`) | 1 | no index of its contents; the Director decides (D7) |

**Not preserved:** the 264 files deleted in the main worktree (their earlier versions are in git), and every untracked file whose exact blob is already in git history. The other 1008 and 1009 files are kept anyway, so each folder stays whole.

### Import manifest

`import-manifest.tsv` lists 882 rows. Each row gives the id, tier, class, source (`rev:path`), git blob, sha256, destination and action. Bytes come only from git objects.

| Id | Tier | What | Rows | Class | Action |
|---|---|---|---|---|---|
| M1 | minimum | kernel draft desk files (`de3b8eb`) → `00.kernel/` | 5 | accepted reference | keep; adapt later by pack |
| M2 | minimum | syntax book, every file (`de3b8eb`) | 190 | 95 seats, plus drafts, retired and notes | keep unchanged |
| M3 | minimum | law book, every file (`de3b8eb`) | 444 | 332 reference, 49 candidates, 63 predecessors (by name) | keep unchanged |
| M4 | minimum | the `38a037e` side of the 6 changed kernel paths → `imports/main-38a037e/` | 6 | competing version | keep; difference reported |
| M5 | minimum | runtime candidates → law `0302`–`0307`, named by stamp | 8 | unfinished candidate | keep bytes; not active |
| M6 | minimum | rebuild `0202`, `0303`, `0304`, `0305` pages, whole (predecessors included) → `imports/rebuild-de3b8eb/` | 28 | reference, candidate, predecessor | keep unchanged |
| M7 | minimum | decision records: rebuild `0300/05.01`, `0401/05.01`–`05.03`, `0409.goal` | 6 | accepted decision | keep unchanged |
| M8 | minimum | `AGENTS.md` 003 | 1 | proposed rule (draft boot) | keep; 004 drafted beside it |
| — | minimum, after preservation | P1 (`1008`, `1009`) from the archive branch → `imports/archive-…/` | 22 | accepted decision | keep unchanged (rows are added once the archive commit exists) |
| L1 | later | `00.00.14.notes` | 36 | historical record | keep unchanged |
| L2 | later | kernel draft `00.retire.09`, `_snapshot`, `downloads`, desk zips | 9 | historical predecessor | keep unchanged |
| L3 | later | Grok's `00.kernel` candidate | 138 | proposed rule | keep unchanged |
| L4 | later | solo-kernel code apart from `face` | 8 | experimental | keep; differs from P3 |
| L5 | later | slot pages `0106`, `0406`, `0506` | 8 | unfinished candidate | keep; D4 |
| L6 | later | labs `timer`, `pdf`, `words` | 3 | experimental | keep unchanged |

**Kernel collisions.** Of 19 differing paths, 13 exist only in `de3b8eb`, so only 6 collide:

| Path | `38a037e` → `de3b8eb` |
|---|---|
| `syntax/00.md` | +8 −1 |
| `law/00.order.md` | +17 −1 |
| `law/0013.concordance/06.md` | +8 −1 |
| desk `00.md` | +16 −2 |
| `00.readme.md` | +8 −1 |
| `00.start.md` | +9 −2 |

The `de3b8eb` side goes into the books. The `38a037e` side goes into `imports/main-38a037e/`. Nothing is overwritten or renumbered.

**Imported as found, flagged as findings:**
- **Four syntax drafts stamped approved.** `0001.rules/01.008`, `0003.operate/01.007`, `0003.operate/04.004` and `0014.design/04.005` say `Authorization: approved — 2026-10-25`, beside their seats. Every commit carries the Director's name, so authorship can't be verified (D6). The import carries the stamp as found. It confers nothing.
- **Grok's direct commit `14676ca` on `main`.** It's carried as history.

**Kinds of material:**
- **Executable tools:** loader, clerk, jobs, check, face, slot; Worldcraft `sync.py` as prior experience.
- **Experimental code:** solo `door`, `page`, `journal`, `menu`, `nav`, `reader`, `desk`; labs `timer`, `pdf`, `words`; `clerk-handoff-pass01`.
- **Proposed rules:** `AGENTS` 003 and 004, Grok's `00.kernel`, `0418` lifecycle, the `0409.goal` lanes.
- **Accepted decisions:** M7 and P1.
- **Historical records:** ran batches, returns `0101`–`0106`, queue notes, face 06, retired `.09` pages.

## 5. Ordered setup steps

The exact commands are in `setup-assignment.md`.

| # | Step | Result | Verify |
|---|---|---|---|
| 0 | Baseline | fingerprints of both old checkouts and the lab | A1, A2 recorded |
| 1 | Preservation (`preservation-assignment.md`), in a temp clone | `archive/librarian-worktree-2026-10-26`, `archive/rebuild-worktree-2026-10-26`, tags `archive/main-14676ca`, `archive/rebuild-de3b8eb` pushed | `ls-remote`; a fresh clone matches every manifest sha256; A2 |
| 2 | Repository in place in `lib-build` (`git init`, remote, fetch, branch at `14676ca`, empty index) | `.git` exists; no file written to disk | the lab is unchanged (A1); `git status` shows staged deletions plus untracked `labs/` |
| 3 | Commit "clear the floor" | the branch has an empty tree; history intact | `git ls-tree HEAD` is empty; `git log` reaches `bf5f04d` |
| 4 | Commit the lab unchanged | `labs/clerk-handoff-pass01`, 36 files | A1 |
| 5 | `import.py` minimum, M1–M8, plus P1 rows | books, candidates and snapshots | A3 |
| 6 | New drafts: work book skeleton and pages, law `0041`, `0062`–`0065`, `0300` door, `0057` draft, `AGENTS.004.md` | addresses exist as drafts | A4 (dev mode) |
| 7 | Entry `app/librarian.py` and acceptance tests | one entry | A4, A5, A6 |
| 8 | Push `workshop`; the Director reviews | remote branch | A2 again; the Director seats or returns it |

**Not in this setup:** no seating, no approval, no adaptation of tool code beyond stamp lines on candidates (step 6 is drafts only), no pending packs, no broad tool rewrite. Code adaptation (consequence 5) comes as named packs after review.

## 6. Acceptance checks

| Check | Passes when |
|---|---|
| **A1. The lab survives** | All 36 lab files keep their sha256 (`worktree-inventory.tsv`, workspace `lib-build`) after every step. After step 4, `git ls-files labs` gives 36 and `git diff HEAD -- labs` is empty. `run_lab.py` is re-run only into a temp copy, never into the lab folder. |
| **A2. The old workspaces are unchanged** | For both `D:\Git\Librarian` and `D:\Git\Librarian-rebuild`, the fingerprint before and after every step is identical. The fingerprint is the sha256 of `git status --porcelain -uall`, plus `HEAD`, `git stash list`, `git worktree list` and `git for-each-ref`. Baseline at handoff, after this return was written: `D:\Git\Librarian` `561ad5addd59a405`, `D:\Git\Librarian-rebuild` `0307b0f62508f6c6`. No step uses a worktree, a checkout or a copy whose destination is either one. |
| **A3. Imported candidates stay identifiable** | Every imported file's sha256 equals its manifest row. Every M5 file's version in its name equals its stamp. No `02.<name>.py` (active) exists on a runtime page. `imports/` holds both sides of each collision. Normal mode refuses with "no active module". |
| **A4. A fresh worker finds the desk** | In a fresh clone of `workshop` under `%TEMP%`, the entry's `where` prints desk `00.kernel` and the books `00.00.00.syntax`, `00.00.01.law` and `00.00.10.work`, the goal page `0401.goal`, and the context. The header-block check (from Worldcraft sync) passes on `AGENTS.md`, `CLAUDE.md` and `GROK.md` once 004 is seated. A cold model given only `AGENTS.md` names the desk, the books and the current work. |
| **A5. No old absolute paths** | A gate over tracked code and entry files refuses `[A-Z]:\`, `00.00.00.kernel.draft` and `10.10.12.rebuild` (history in `imports/` and notes is allowed). Candidate tests pass from a clone at another path and from a working folder that isn't the root. |
| **A6. Current work can be recovered** | Process 1 records an item in context `00.00.01.law space 0`. A fresh process 2 derives the same item and context from the record, and a falsified `00.live` doesn't change the result (lab lesson 4). |

## 7. Decisions the Director has to make

| | Decision | Recommendation |
|---|---|---|
| D1 | Work book at `00.00.10.work`, against `0018`'s "desk books are 00 and 01" | yes. `00.00.14.notes` is already a third desk book, and `0054` says "from 10 up". Amend `0018` Walk by a draft. |
| D2 | Law gains a runtime band (`0057` draft, door `0300.band.compute`) | yes, for space 0 only. The runtime slot module takes a title other than `slot`. |
| D3 | Roles as structure (`0062`–`0065`, `role-` titles), which extends `0050`'s list | yes |
| D4 | Candidates named by their stamped version at import; rebuild predecessors kept only in `imports/` | yes |
| D5 | Seat the loader and the first modules, so normal operation exists | after A3–A6 pass. Until then, development mode only. |
| D6 | The four syntax drafts stamped approved on 2026-10-25 | the Director confirms or rejects. They're imported as found either way. |
| D7 | Scope of preservation: P4 (another model's in-progress redraft) and the held `10.workshop.zip`; and who commits the archive branches | preserve P4; the Director looks at the zip first; a model commits at his word, only the listed paths |
| D8 | Whether candidates travel with a merge into `main` | no. Seat or retire them first, or exclude them from the merge. |
| D9 | Seat `AGENTS.004.md` | at step 8. A4's header check depends on it. |

**Already decided, so reused rather than asked again:**
- AI commits only on named branches; only the Director merges into `main`
- layered review; card rule B
- files are the truth; app at the top; `.librarian/`; core Python with no screen; `.venv`
- `FF.md` and `FF.VVV`; `02.name.py`; one number, one name
- batch states open, ready, ran; work is released by dev decisions
- the N3NN runtime pattern (Director, 2026-10-26)

**Routine:**
- a `Model:` line in every commit
- stamp lines after the coding line, never inside a docstring
- `.gitignore`
- the provenance row for every import

## Overflow

- Returns `0101`–`0106` on `rebuild` hold 25 unreviewed lines. Their defects go into `0611.findings` with citations, and the returns stay in `rebuild`.
- `0418` and `0519` opened on 2026-10-26 with mismatched numbers.

One thing I'd have written differently: in pass 01 I'd have checked the work book's page numbers against the module numbers. It took this pass to see that `0402.seats` would have taken the run module's number.
