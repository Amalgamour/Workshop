# Book Format

How seqAddr books are stored and served, and why. The address design is in `seqAddr.md`, and the research behind these choices is in `research-b-format.md`.

Each choice is marked **decided** (agreed) or **proposed** (recommended, awaiting agreement).

---

## 1. The model

### 1.1 A page is multi-dimensional — decided
A page is not a flat document. It is one object with several faces, and each face is a view of that object for a different reader: agents, compute, users. seqAddr is the coordinate system for every part of it: page, face, counter, tail.

### 1.2 The compute holds the books — decided
One process, **the compute**, owns the books. There is **one compute per repository**, and it owns every book in it, including the kernel. This matches one namespace per repository (A6.2), and the A1.8 lookup never leaves the process.
- **Reads are open.** Anyone may read any face.
- **Writes are proposals.** Writers submit a write to the compute's queue. The compute validates it against seqAddr's rules and approves or rejects it.
- **Only the compute writes to disk.** Agents, users and the app never touch book files.

### 1.3 A book is one file — decided
A book exports as a single file. Every container is a book (A4.1), so desks, shelves and the kernel are book files too:

| File | Holds |
|---|---|
| `10.11.21.book` | book 10.11.21 |
| `10.11.00.book` | shelf 10.11's own book |
| `10.00.00.book` | desk 10's own book |
| `00.00.00.book` | the kernel |

Exporting a book means copying its file.

---

## 2. Why this shape

Every file format has to rank four goals that pull against each other. The compute model settles most of the tension:

| Goal | How it is met |
|---|---|
| One file | Required. A book is one file. |
| Many writers at once | Solved by the compute: writers queue proposals, and only the compute writes. |
| Exclusive claims | Solved by the queue: proposals are approved one at a time, so the first claim on a `pack` wins and the second is rejected. |
| Readable as plain text | Met by a text encoding (section 3). |
| Mergeable in git | Approved writes are appended, so git diffs are clean additions. Two copies edited apart are a fork, which the compute reconciles. |

Options considered and set aside:

| Option | Why not |
|---|---|
| Folder of files per page | No single file to export. "Rename is a claim" only works on one disk. |
| Single text file edited in place | Every write rewrites the file. Does not scale (TiddlyWiki's experience). |
| ZIP container (docx, EPUB) | Changing one part rewrites the whole archive. Binary. |
| CRDT (Automerge) | Merging keeps both sides, so two agents can both win a claim. |
| SQLite | Strong candidate: one file, real transactions. But binary, not mergeable in git, and its transactions duplicate what the compute's queue already does. It remains the fallback if the log proves too slow. |

---

## 3. Encoding — decided

### 3.1 A book is an append-only log of approved writes
The compute's queue and the file are the same thing. Each approved write is appended to the end of the book as one entry. Nothing is ever edited in place. The current state of a book is the result of replaying its entries in order.

This gives, without extra machinery:
- **History.** Every past state of every face can be rebuilt.
- **Rewind and fork** for SoF: replay up to entry *n*, or continue two logs from a shared prefix.
- **Clean git diffs.** New work shows up as lines added at the end.
- **Crash safety.** A partly written last line is detected and dropped. Nothing earlier can be damaged.

### 3.2 Text, one entry per line
Each entry is one JSON object on one line (JSON Lines). It is readable in any editor, works with standard tools, and is easy for models to read.

```
{"seqbook":1,"address":"10.11.21"}
{"n":1,"at":"2026-11-09T14:02:11Z","by":"user","op":"put","addr":"10.11.21.0000.00","body":"---\ntitle: tools\n---"}
{"n":2,"at":"2026-11-09T14:05:40Z","by":"claude-opus-5-5","op":"put","addr":"10.11.21.1523.05.03","tail":"pack","body":"## Build timer\n..."}
{"n":3,"at":"2026-11-09T14:06:02Z","by":"agent-7","op":"tail","addr":"10.11.21.1523.05.03","from":"pack","to":"open"}
```

- **Line 1 is the header:** the format name and version, and the book's address.
- **Every later line is one approved write:** sequence number, time, author, operation, full address, and content.
- **Face content stays Markdown,** in `body`. Cards are `##` headings.

### 3.3 Operations
| Op | Effect |
|---|---|
| `put` | set the content of a face or counter, optionally with its tail |
| `tail` | move a tail from one state to another; rejected if the `from` state is not current |
| `snapshot` | the full current state, written so replay can start here instead of at line 2 |

Boards (`FF.00`), contents lists and ancestor path lists are derived from the log and never written as entries (A4.4, A5.4).

### 3.4 Snapshots
A long log replays slowly. The compute periodically appends a `snapshot` entry, and readers start from the latest one. Older entries stay in the file for history. They can be moved to an archive file if size becomes a problem.

---

## 4. The compute — proposed

### 4.1 Write lifecycle
```
submitted -> validated -> approved (appended to the book)
                       -> rejected (reason returned to the writer)
```

Validation checks:
- the address is well formed (seqAddr grammar)
- the target exists, or the write creates it legally (identity page first, board before counters)
- the tail move is allowed (for example `pack -> open`, never `pack -> return`)
- required back-links exist (A5.3)

### 4.2 Reads
The compute keeps each open book's current state in memory and serves any face by address, including short-form and leading-dot addresses resolved against the reader's active book and page. Inherited pages are found through the A1.8 lookup across the book, shelf, desk and kernel files.

### 4.3 Elevation
Anything the compute cannot resolve goes to the user and is never guessed: unknown addresses, title mismatches, ambiguous leading-dot addresses.

---

## 5. Language — decided

| Part | Language | Why |
|---|---|---|
| Core library: seqAddr parser and validator, book reader/writer, tail rules | **Rust** | One implementation, shared everywhere |
| Compute | **Rust**, using the core | Long-running and must never corrupt a book. Rust's memory safety and async queue handling fit. Ships as one program. |
| App | **TypeScript**, Next.js (AGENTS.md) | Uses the core compiled to WebAssembly, so the browser validates exactly as the compute does |
| Agent clients | any | They only talk to the compute |

Why Rust for the core:
- **One parser everywhere.** The app and the compute can never disagree about an address.
- **The rules become types.** Tail states and addresses are types, so illegal transitions and malformed addresses cannot be constructed.
- **It suits a file format.** Exact layouts are precise and fast to read and write.

Set aside: TypeScript for everything. Faster to start, and one language with the app, but weaker typing at runtime and a likely rewrite of the core later.

---

## 6. Open

- **How clients talk to the compute:** HTTP, MCP, or both.
- **Fork reconciliation:** how the compute merges two copies of a book that were edited apart.
- **Snapshot and archive policy:** when to snapshot, and when to move old entries out.
- **Face rules** (review section C) and **task failure paths** (section D) still apply on top of this format.
