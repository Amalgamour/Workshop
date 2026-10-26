# plan.2 first version

Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: draft
page: 1008.app-plan
why: The smallest Librarian you could use for real work, and one session with it.

## The idea
The first version is the **batch desk**. A batch (`05.NN`) is the review queue: every piece of work a model does, every stop, every conflict, every idea found on the way is a `#NN` on a batch before or as it happens. No model work goes unseen. `1006.redraft` is the model: face `01` says what and why, each `05.NN` is a round, face `06` holds the notes.

The desk has two sides over one set of files:
- **Your side:** see every batch line that needs you (stops first), read it beside the page it names, reply, review solo work, and see what changed since your last visit, including work no batch names.
- **The model side:** commands a model uses to start a page in an authorized place, write its `01`, open a `05.NN`, add `#NN` lines, report status, and stop with an escalation. The same checks guard every write.

It never writes either kernel. Drafts of faces, signing and approving wait for later stages. There are about 79 blank replies waiting today.

## One session
1. **Open.** You open Windows Terminal and type `librarian`. A full-screen terminal app opens.
2. **Find your work.** The home screen says:
   ```text
   Stopped, needs you     1   2007.timer 05.01 #03  stop: no authorized sound library
   Waiting on you        23   1006.redraft 05.18
                           8   2005.face-mod-test 05.01
   Solo, done, to review   4   2007.timer 05.01 #01 #02 #04 #05
   Since your last visit       2003.reference 05.01 #02 status: closed (grok-prime)
   Unseen work             1   app/notes.txt changed, no batch line names it
   Branches to merge       1   build/2006.batch-desk  4 commits, gate passed
   Uncommitted             6 files
   Checker                     kernel.draft: 0 errors reworked, 24 pending
   ```
   On the left is the tree by title: desk, shelf, book, page, with states (draft, signed, approved).
3. **Review a stop.** You open `2007.timer 05.01 #03`. The card shows where the model stopped, what it had planned (the line's `issue` and the page's `01`), and what it needs. The page opens beside it.
4. **Enter something.** You press `r` and reply. Free text, or start with `>take`, `>hold`, `>note`, `>reject`. The app shows exactly the line it will add, and where.
5. **Complete an operation.** You confirm. The app checks the file is unchanged since you opened it, the reply line is still blank, and your text cannot be mistaken for structure. It saves a before-copy, writes in one step, re-reads, and confirms only your reply was added. The card now says *replied*.
6. **Review solo work.** You open the four solo lines. Each has a `status:` with the files it changed and its commit, under a blank reply: that is the solo mark. You read the changes and reply `>take`, or reply with a correction. A correction is carried to the model's next batch with `reason: From 05.NN #NN`.
7. **A worker runs.** In another window a model reads your replies (`librarian items --replied`), does the work, and appends `status:`. If it hits a wall it runs `librarian stop` and the line comes to the top of your screen.
8. **Return later.** Next day you open `librarian`. *Since your last visit* lists the new status and stop lines and the files the workers touched (from git). *Unseen work* lists any changed file no batch line names. *Branches to merge* lists the work branches whose lines are closed. You read the branch and merge it into `main`, or reply with corrections. Merging is yours.

If a worker changed the same batch file while you were typing, step 5 stops: "This file changed since you opened it. Your reply was not written. Reload?" Your typed text is kept.

## A model's session (your timer example)
1. The job names an authorized place, for example band `2000`.
2. `librarian page new --band 2000 --title timer --who <model>` makes `2007.timer` in the lowest open slot, with face `01` and face `08` headers filled. The model writes the why and the body of `01`: what it is building and why.
3. `librarian batch new 2007.timer` opens `05.01`. `librarian item add` writes each job in the `1006` shape: `#NN >command subject`, `issue` when there is a conflict, `recommend`, `Ask: >command` with the reason, `path`, `scale`, and a blank `reply:`. The command must be on the desk command list.
4. Without a grant: it waits for your replies. With a grant that covers this shelf or book: it skips the reply, works through the lines, and after each writes `status:` with the files it changed. Each closed line is a commit on its work branch. If you reply during the run, it follows your reply.
5. If something stops it: `librarian stop` adds a `>stop` line that names where it stopped, what it had planned, and what it needs. It does not guess. It moves on to other lines it may work.
6. A decision that proves wrong goes into the next batch: a new line with `reason: From 05.01 #NN`, and the old line's status says `Carried to 05.02 #NN`.

## In the first version
- Browse the tree by address and title; read any face with its header shown plainly.
- Read every batch on disk, in every old name form; show each line's command and state: waiting, stopped, replied, solo work waiting review, closed, carried.
- Your reply, written safely, with undo.
- Model commands: new page in an authorized band, new batch, add a line, status, stop.
- Run the checker read-only and show its findings per page.
- Since your last visit; unseen work; your replies changed by anyone.
- The same operations as plain commands, with `--json`, so models, scripts and tests use them.

## Waits for later
| feature | why it waits |
| --- | --- |
| Make or edit drafts of faces | Needs one face engine (stage 6) |
| Sign, approve (rename onto the seat), lock, promote | Your acts. Highest risk. After drafts work. |
| Note cleanup by applied mark | Needs drafts and the mark (`05.02` #07) |
| Build menus (`03`), references and custody (`08`) | `2003` and `2004` are still open |
| Sending work to a named model from the app | Needs the dispatch design; models already read replies |
| Colab packs and returns | Separate workflow; works by hand today |
| Search across all text | Useful, not first; needs the index |
| Windows desktop window | Later shell on the same core (see Interface) |
| A merge button for `main` | You merge by hand at first; asked again after stage 5 |

## Interface
Three layers, so the screen can change without touching the rules:
1. **Core** (Python package). Reads the tree, parses faces and batches, checks and writes. It has no screen.
2. **Commands.** `librarian <verb>` in a terminal. Used by you, by worker models, and by tests.
3. **Screen.** Now: a full-screen terminal app built with Textual, a Python library for terminal apps (mouse, panes, keyboard; runs in Windows Terminal). Later: a Windows desktop window built with Qt for Python (PySide6) over the same core.

Why this path: the core and commands are where the rules live. Both screens call the same core, so the Windows app later is a new screen, not a rewrite. Python is already the language of every existing tool, so the reuse in plan.1 carries over. `05.01` #03.

What it costs: two screens over the life of the project instead of one. The terminal screen is small because the core does the work. Going straight to the desktop window instead would roughly double the screen stage and move the Windows packaging questions earlier.

## Storage
- **The files stay the truth.** The app reads and writes the same markdown files that models read. No database holds anything that is not in a file.
- **App state** lives in `.librarian/` at the repo root, outside git (`05.01` #12): your last-visit marker, the write journal (a before-copy of every file the app changed), and later a search index. Deleting `.librarian/` loses only "since last visit" and the undo copies.
- **History and backup** stay git. Models commit on work branches, one commit per closed line (`05.01` #07). `main` is the record you approved; merging into it is yours. The app shows unmerged branches and anything uncommitted.

## Relationship to the existing files
- The app adds a folder for its own code (`app/`, `05.01` #01) and the `.librarian/` state folder. It changes no existing page to work.
- It reads `00.live` and `00.md` to find the desk and kernel. No machine path is stored in code.
- It never writes inside `00.00.00.kernel` or `00.00.00.kernel.draft` in the first version, and never reads `00.00.00.kernel` as a source.
- New batches use one name, `05.NN.md` (`05.02` #01). Old batch files are read as they are and not renamed.
- `jobs.py` stays in use until the app's batch commands pass the same tests. Retiring it is your reply.
- The design pages of the app sit in band `2000` as members, one per stage or module. The code says what it does; the page says why.

## Working beside model workers
Models keep working on the files, as today. The app does not assume it is alone:
0. **Grants.** A worker writes only inside the shelf or book its grant covers. A write outside it is kicked back with the reason (`05.03` #04).
1. **Look before you write.** The app keeps a fingerprint (hash) of each file when it shows it. At write time it reads the file again. If the fingerprint differs, it refuses and reloads.
2. **Append, don't rewrite.** Every app write is a new file, a line appended to an open batch, or text into a blank reply. Nothing already written is changed.
3. **One-step writes.** The app writes a temporary file and swaps it in, so nobody reads half a file. If Windows refuses the swap because another program holds the file, the app reports it and keeps the text.
4. **Undo copy.** Every write keeps the old file in `.librarian/journal/`, with time, file, who, and what changed.
5. **Watching the rules.** The app remembers every reply you wrote through it, and checks on start that each one is still there, unchanged. A reply that appears without passing through your side of the desk is listed as "written outside the app", and you confirm your own in bulk (dev mode, `05.01` #06). It lists changed files that no batch line names. It cannot stop a model editing a file directly. It makes sure you find out.
6. **Same door for models.** AGENTS can tell workers to write batches and status through `librarian` commands, so they get the same checks. That is an instruction to models, not a guarantee (plan.4). `05.01` #11.
