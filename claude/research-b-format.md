# B: Single-File Book Format Research

Question: can a book be one file (a modular file type) instead of a folder of many files, and still serve an agent swarm?

## What breaks the folder-per-page design

1. **"Rename is an atomic claim" only holds on one disk.** Agents working in separate git clones can both rename `05.03.pack` to `05.03.open`, and both succeed. The claim mechanism was weaker than presented.
2. **No single document.** A folder of files has no one file the user can point to, move or export (sqlite.org, "pile of files").
3. **Export is needed anyway.** If a book must export as one file, a folder design means two formats to keep in sync.

## Options

| Option | One file | Concurrent agents | Atomic claim | Readable without the app | Git |
|---|---|---|---|---|---|
| Folder of Markdown files | no | good | same disk only | yes | diffs and merges well |
| Single text file (Org-mode style) | yes | poor: all edits hit one file | no | yes | diffs; conflicts when agents collide |
| ZIP container (EPUB, docx) | yes | poor: each edit rewrites the archive | no | no | binary |
| CRDT document (Automerge) | yes | best: edits from separate machines merge | **no**: merging lets both claims win | no | binary |
| **SQLite database** | yes | good on one host: many readers, one short writer at a time | **yes**, in a transaction | with the app or `sqlite3` | binary; text diffs via `.dump` |

### Single text file
Org-mode already does much of this: TODO keywords as workflow states on headings and property drawers for metadata, all in one text file. TiddlyWiki stores many tiddlers in one HTML file but hits scaling limits: forum reports of saves over 120 s, and linear search. For large wikis it moved to the Node version, with tiddlers as separate files plus a single-file build. That is the folder design with an export.

### CRDT
Automerge saves a document as one binary file and merges independent edits automatically, including across machines. But a merge keeps both sides' changes, so two agents claiming the same task both succeed. A CRDT cannot provide an exclusive claim. History also grows and needs compaction.

### SQLite
The SQLite project argues for a database as an application file format: one file, no custom parser, new features as new tables.
- One writer at a time, with concurrent readers in WAL mode. `BEGIN IMMEDIATE` plus a busy timeout is the standard multi-process pattern.
- WAL requires all processes on the same host; it is unsuitable over a network file system.
- Git stores it as binary. A `textconv` driver running `.dump` gives readable SQL diffs. Git cannot merge two branches that both changed the same book.

## How SQLite maps onto the design

- **A book is one file:** `10.11.21.book`. Exporting a book means copying it.
- **Every container is a book file** (A4.1): `10.00.00.book` for desk 10, `10.11.00.book` for shelf 10.11, `00.00.00.book` for the kernel. A repository becomes a folder of book files.
- **The address is the key.** Pages, faces and counters are rows keyed by their address.
- **Claims are real.** `UPDATE ... SET tail = 'open' WHERE address = ? AND tail = 'pack'` succeeds for exactly one agent.
- **Boards are derived** (A4.4, A5.4): `FF.00` is a query over the counter rows, never edited by hand.
- **Live inheritance** (A1.8, A2.9): the lookup attaches the shelf, desk and kernel books and queries in order.
- **Face content stays Markdown text** inside rows, so the content format does not change.
- **The client app can open it:** the official SQLite WebAssembly build runs in the browser, so the Next.js app can read a `.book` the user opens, with no server.

## Costs of SQLite

- Not readable in a plain editor or on GitHub's web view. Needs the app or `sqlite3`.
- One machine at a time per book. A distributed swarm needs one host that owns each book, not agents in separate clones.
- Git cannot merge two branches that changed the same book. Changes must be serialized, or a text dump (`.sql`) kept as the merge-friendly form.

## Sources

- [SQLite As An Application File Format](https://sqlite.org/appfileformat.html)
- [SQLite forum: critique of the essay](https://sqlite.org/forum/forumpost/2138fc3612)
- [SQLite isolation](https://sqlite.org/isolation.html)
- [SQLite concurrent writes and "database is locked"](https://tenthousandmeters.com/blog/sqlite-concurrent-writes-and-database-is-locked-errors/)
- [Simon Willison: tracking SQLite database changes in git](https://simonwillison.net/2023/Nov/1/tracking-sqlite-database-changes-in-git)
- [gitsqlite](https://github.forks.workers.dev/danielsiegl/gitsqlite)
- [TiddlyWiki: Microkernel Architecture](https://tiddlywiki.com/dev/static/Microkernel%2520Architecture.html)
- [TiddlyWiki: strategies for large wikis](https://groups.google.com/g/tiddlywiki/c/TNt4RxyQF3w/m/JdIS5OxZAgAJ)
- [Org Syntax](https://orgmode.org/worg/dev/org-syntax-edited.html)
- [Automerge cross-platform vignette](https://cran.r-project.org/web/packages/automerge/vignettes/cross-platform.html)
