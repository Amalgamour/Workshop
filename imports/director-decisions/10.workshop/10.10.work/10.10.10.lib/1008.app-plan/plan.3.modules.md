# plan.3 modules

Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: draft
page: 1008.app-plan
why: The pieces of the first version, what each owns, and the later pieces. Proposed boundaries, not commitments.

## Map
```text
screen ----+
           +--> batches ---> face --> tree --> place
commands --+      |  +-----> write ----------> place
           |      +--------> pages ---> tree, write
           +--> changes ---> batches, write, place, git
           +--> check -----> place, lcheck.py
           +--> tree/show -> face, tree
```

Read each arrow as "uses". `place` uses nothing. Only `write` writes into the tree. The screen and commands hold no rules.

## First-version modules

### place
- **For you:** the app always knows where your desk is and which folders it must not touch. No machine path in code.
- **Owns:** finding the repo root (the folder holding `00.md`, `00.live.md` and `00.00.00.kernel.draft`); reading `00.live`; looking up a rule book, then shelf, then desk, then kernel, stopping at the first that answers (`05.03` #05; the first version holds only the desk level, built so the others can be added); the desk command list (`05.03` #06); the grants that cover each shelf and book (`05.03` #04); the no-read list (`00.00.00.kernel`, `.git`) and no-write list (both kernels in v1, retired `.09`); the path to `lcheck.py`; the `.librarian/` state folder.
- **Not here:** what a folder name means (`tree`).
- **In / out / stored:** in: the start folder. Out: a `Place` record. Stored: nothing. Optional `.librarian/config.toml` for overrides only.
- **Depends on:** nothing.
- **Reuses:** solo `desk.py` (`repo_root`, `live_fields`, `read_live`).
- **New work:** remove the constants (return hole 6); one place for kernel names.
- **Works when:** tests find the root from any subfolder; a test tree with a different name works; a missing `00.md` stops with a clear message.
- **Open decision:** none.

### tree
- **For you:** browse desk, shelf, book, page, face by title and state, not raw names.
- **Owns:** parsing a folder or file name into address, title, kind (desk, shelf, book, page, seat, draft, slice, retired, batch, furniture, unknown); walking from `00.md`; skipping retired `.09` items unless asked.
- **Not here:** the text inside a face (`face`).
- **In / out / stored:** in: `Place`. Out: nodes with address, title, kind, path. Stored: nothing (rebuilt each start; later cached in the index).
- **Depends on:** `place`.
- **Reuses:** `NAME_RE`, `parse_name`, `kind_of` from `clerk.py` / `face.py` / `jobs.py` (one copy, three sources); the walk from solo `nav.py`.
- **New work:** read both draft forms (`FF.VVV.md`, `FF.VVV.draft.md`; the writer will use `FF.VVV.md`, `05.02` #06), dotted titles (`band.build.page`), slices (`03.10.md`), and every batch name form. Report a name it cannot place instead of guessing.
- **Works when:** a walk of the real tree finds every page folder `find` lists; every face file in the lib book and kernel draft gets a kind; a name table passes.
- **Open decision:** none for reading.

### face
- **For you:** any face reads cleanly: header fields up top, then sections, then notes.
- **Owns:** splitting a face into header, sections, and trailer (`## Note`, `### notes`); reading header fields (`Authorization`, `state`, `version`, `who`, `why`, `cite`); the fingerprint (hash of the raw bytes); keeping line endings as found.
- **Not here:** writing; batch lines (`batches`).
- **In / out / stored:** in: a path. Out: a `Face` record plus raw bytes and hash. Stored: nothing.
- **Depends on:** `tree`.
- **Reuses:** `split_document`, `header_field`, `normalize`, `sha256` from `clerk.py`; `unmash_header` from solo `face.py`.
- **New work:** one parser for faces from both code shelves and the kernel draft.
- **Works when:** every face under kernel.draft and the lib book parses with no exception; header fields match a hand-checked sample of 20 faces.
- **Open decision:** none.

### batches
- **For you:** everything that needs you, stops first; your reply; solo work to review. **For models:** the way to record work before and as they do it.
- **Owns:**
  - Reading: `05` batches in every name form; the header (`state`, `Overview`, `Learned`, `How`, `Scale`); each `#NN` with its command (from the heading and `Ask:`) and its fields (`reason`, `issue`, `choice`, `recommend`, `how`, `now`, `later`, `path`, `scale`, `Ask`, `reply`, `status`); the line state (waiting, stopped, replied, solo work waiting review, closed, carried); the carry chain (`reason: From` and `Carried to`).
  - Writing (through `write`): a new batch `05.NN.md`; a line appended to an open batch; your reply into a blank `reply:`; a `status:` after the full reply, or under a blank reply when a grant covers the location (solo work); a `>stop` line. A closed line makes a commit on the work branch with the files it names.
- **Not here:** how bytes reach the disk (`write`); judging what a reply means; making pages (`pages`).
- **In / out / stored:** in: the tree. Out: line lists, one line, write plans (file, place, new text). Stored: nothing of its own.
- **Depends on:** `face`, `tree`, `write`.
- **Reuses:** `BATCH_RE`, `ITEM_RE`, `REPLY_RE`, `ITEM_FIELD_RE`, the rule that a reply line is never rewritten, the `Carried to 05.NN #NN` check, from `jobs.py`.
- **New work:** line states; checking each command against the desk list and kicking back the rest; telling a blank reply in a `ran` batch from a live wait; skipping `00.00.00.kernel`; the solo rules; the write checks in plan.4.
- **Works when:** waiting counts match a hand count on five named batches; each write changes only its own bytes; a reply over a filled reply is refused; a solo status outside any grant is refused; a command not on the list is refused; a reply from a model command is refused; a write to a file changed after reading is refused; `jobs.py carry` accepts the chains the app writes.
- **Open decisions:** none. Taken on `05.01` #05, #06, #07 and `05.02` #01, #02, #03, #05. The command list itself is `05.03` #06.

### pages
- **For models:** start a page in an authorized place, the first step of your timer example.
- **Owns:** the lowest open slot in a band; the folder `PPPP.title`; face `01` and face `08` with headers filled from the folder; refusing a location no grant covers.
- **Not here:** the why and body of `01` (the model writes them); drafts of existing faces (stage 6).
- **In / out / stored:** in: book, band, title, who, why, body. Out: the new page. Stored: nothing.
- **Depends on:** `tree`, `write`.
- **Reuses:** solo `slot.py` (`next_open`, `next_member`) and `page.py` (`place_page`); the header from `clerk.py` `stamp`.
- **New work:** a full decade stops with a message instead of guessing (return hole 3 stays open for you); refuse bands below `1000` unless the job names them.
- **Works when:** a new page lands in the lowest open slot of a fixture band; an existing folder is never touched; a full decade stops.
- **Open decision:** the decade-full rule (not needed while work is at `1000` and above).

### write
- **For you:** nothing the app does can lose your work or a worker's work silently.
- **Owns:** every write into the tree: zone check, fingerprint check, temp file and swap, re-read and compare, the journal entry with the before-copy, and undo of the last app write.
- **Not here:** what text to write (callers decide).
- **In / out / stored:** in: path, expected hash (or "must not exist"), new bytes, who, reason. Out: done, or refused with the reason. Stored: `.librarian/journal/` (one entry per write: time, path, old hash, new hash, who, reason, before-copy).
- **Depends on:** `place`.
- **Reuses:** `guarded()` from `clerk.py`; `refuse_kernel_write` from solo `face.py`.
- **New work:** the swap on Windows (retry once, then report); the journal; `librarian undo`.
- **Works when:** a write to either kernel is refused; a changed file is refused; a new file over an existing one is refused; a crash between temp and swap leaves the old file; undo restores the exact old bytes.
- **Open decision:** `05.01` #12.

### check
- **For you:** the checker's view without reading its report files.
- **Owns:** running `lcheck.py` read-only (`--json` to a temp file, never `--fix-sentinel` or `--write-moves`); counts per tier and per page.
- **Not here:** the rules. `rules.toml` and `moves.toml` are not touched.
- **Depends on:** `place`.
- **Reuses:** `lcheck.py` as is.
- **New work:** the adapter, and refusing the two write flags in code.
- **Works when:** counts equal a direct `lcheck.py` run (today 0/0/60 reworked, 24/41/32 pending); the tree is byte-identical after a run.
- **Open decision:** none.

### changes
- **For you:** since your last visit; unseen work; your replies changed by anyone.
- **Owns:** the last-visit marker; asking git for changed and uncommitted files and for work branches not yet merged into `main`; comparing changed files with the files named in `path:` and `status:` lines (unseen work, `05.02` #04); comparing replies in the journal with what is on disk now.
- **Not here:** merging into `main` (yours). Commits on work branches are made by `batches` when a line closes (`05.01` #07).
- **Depends on:** `batches`, `write` (journal), `place`.
- **Reuses:** nothing existing. Uses git as installed.
- **Works when:** a scripted worker change in a test repo appears; a changed file with no batch line is flagged; a hand-edited reply raises the warning.
- **Open decisions:** none. Taken on `05.01` #07 and `05.02` #04.

### commands
- **For you and the models:** the same operations from any terminal or script.
- **Owns:** `where`, `tree`, `show`, `items` (filters: waiting, stopped, solo, replied), `item`, `reply`, `undo`, `page new`, `batch new`, `item add`, `status`, `stop`, `confirm` (your replies written outside the app, in bulk), `check`, `changes`, `sandbox` (a practice copy inside `.librarian/`). Text a model can read; `--json` for scripts. `who` is always passed in, never defaulted.
- **Not here:** any rule. It calls the modules.
- **Depends on:** all of the above.
- **Works when:** each command has a test on the fixture tree; `--help` lists every command.
- **Open decision:** none. AGENTS requires these commands from version 004, after stage 3 (`05.01` #11).

### screen
- **For you:** the full-screen app in plan.2.
- **Owns:** panes, keys, the reply editor, confirmation dialogs.
- **Not here:** any rule. A screen that checks something on its own is a bug.
- **Depends on:** the same modules as `commands`.
- **New work:** all of it, in Textual.
- **Works when:** a scripted run (Textual's test pilot) opens the home screen, opens a line, writes a reply on the fixture, and the file matches the command result byte for byte. Then your own demo.
- **Open decision:** `05.01` #03.

## Later modules
| module | job | depends on |
| --- | --- | --- |
| drafts (face engine) | one program for `draft`, `drop`, `revise`, `derive`; writes each section's `by:` line (`1009.calling 05.02 #01`); merges `clerk.py` and solo `face.py`; writes `FF.VVV.md` | `05.02` #06, #07 |
| note sweep | proposes `applied:` marks on face `06` as a batch; a draft carries only unmarked notes | drafts; `05.02` #07 |
| seat | sign, approve as rename onto the seat, retire to `00.retire.09` (law `0021`, `0022`) | drafts; your acts only |
| menu and reference | build `03`, cites, and `08` (`2003`, `2004`, solo `menu.py`) | drafts; `2004` state `built` |
| batch rename | rename old batch files to `05.NN.md`, by its own batch | `05.02` #01 |
| dispatch | hand a replied line to a named model worker and track it | batches; cost decision |
| index and search | SQLite cache of tree and text; full-text search; rebuildable | tree, face |
| colab | build a pack, intake a return, number holes | tree, index |
| desks from a brief | stand a user desk (`journal.py`) | pages |
| drift | compare stored source hashes to the template (return hole 13) | drafts |
| reader walk | cold-boot walk from syntax `0014` Order (`reader.py`) | tree |
| desktop shell | Windows window in Qt (PySide6), then an installer | all v1 modules unchanged |
| promote | build candidate, verify, retire, lock (law `0023`) | seat; your act |
| prompt clerk | reads the words of a prompt before the model sees it, finds key words and their brands in the book's dictionary and concordance (law `0012`, `0013`), and hands the model the rules and meanings it needs (`05.03` #05) | index; rule lookup |
| local command lists | a book adds commands that inherit the desk list | command list |
| merge from the app | a merge into `main` you press, with the branch, its lines and its gate shown | changes; asked after stage 5 |
