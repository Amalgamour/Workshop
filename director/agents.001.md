# Workshop

Proposed agent brief. `AGENTS.md` stays as written until this file is accepted.

The order is the same as `AGENTS.md`: deliverables, then the technical spec, then the work. The technical spec governs the deliverables and the work. A choice that hits a deliverable and breaks the technical spec is not done.

`AGENTS.md` says design only. That line stands until this brief is accepted. The build is coming, and it is not this edit. When the build is asked for, it follows `claude/format.md` and the settled entries in `claude/decisions.md`. It does not reopen them.

## Sources, in order

1. Settled entries in `claude/decisions.md`. A1 through A6, C1 except the open split in C1.4, C2, C3.1, C3.2, and C8.1 through C8.5 are settled.
2. **Decided** entries in `claude/format.md`. **Proposed** entries there are not settled.
3. `seqAddr.md`, where those two files do not already decide the point.
4. This file, for how the work is done and for the first build.

`claude/research-b-format.md` is the research behind the book file. `claude/seqaddr-review.md` is the question list. Section B of that review is answered by `claude/format.md`. `seqAddr.001.md` is an older draft. `brands.md` and `drafting.md` are the sources for C8 and D0. Leave those files unchanged unless asked.

## Deliverables

1. **The choices are made. The build follows them.** Hardware, software, and design are choices. Software and the book file are decided in `claude/format.md`. Hardware is not decided, and it is not part of the first build.
2. **A persistent, retrievable store of whys.** A why is the reason to do something. A finished spec is a recipe, and a recipe can rot. Face 04 holds the why a person reads. The book log is what makes a rebuild possible.
3. **Reliability.** Intelligence bleeds. A decision left in a chat is not kept. A torn last line is dropped. Nothing earlier in the book can be damaged.
4. **The store is the one already chosen.** A book is one append-only text file. The options and the reasons they were set aside are in `claude/format.md` section 2. SQLite is the fallback if that log proves too slow. It is not the first build.
5. **A person can check it.** The file is JSON Lines. Face content is Markdown. A person can read a why in an editor.

## Technical spec

These are requirements. They are not style.

1. **Architecture.** Clean, modular, separated. Four parts, and they stay four:
   - **Core.** Address parser and validator, book reader and writer, tail rules. One implementation.
   - **Compute.** One process per repository. It owns every book, including the kernel. Reads are open. Writes are proposals. Only the compute appends to a book. Agents, users, and the app never touch book files.
   - **App.** TypeScript, Next.js, using the core compiled to WebAssembly, so the browser validates as the compute does.
   - **Agent clients.** Any language. They talk to the compute. They do not write books.
2. **Fractal.** One book file is the shape at every level. `10.11.21.book` is a book. `10.11.00.book` is the shelf. `10.00.00.book` is the desk. `00.00.00.book` is the kernel. A page is not its own file. Before a different shape is introduced, record why this one failed a written constraint.
3. **Why.** A decision that is not recorded rots with the recipe. Record the reason with the choice. Face 04 carries `why:` for every card that exists on face 01 or 02.
4. **Record.** Take notes and review them. The book log is the record of approved writes. A process that is not written down is not recovered.

## How it is built

Decided in `claude/format.md`.

| Part | Language | Why |
|---|---|---|
| Core | Rust | One parser for the compute and the app. Tail states and addresses are types, so an illegal transition cannot be constructed. |
| Compute | Rust, using the core | Long-running. Must not corrupt a book. One program. |
| App | TypeScript, Next.js | The core as WebAssembly. |
| Agent clients | any | They only talk to the compute. |

Set aside for the core: TypeScript for everything. Faster to start, and one language with the app, but weaker at runtime and a likely rewrite of the core later.

A book is an append-only log. The current state is the replay of its entries. Each entry is one JSON object on one line. Line 1 is the header: format name, version, book address. Later lines are approved writes: `put`, `tail`, `snapshot`. Face content in `body` stays Markdown. A card is a `##` heading. Boards, contents lists, and ancestor lists are derived and are never written as entries.

```
{"seqbook":1,"address":"10.11.21"}
{"n":1,"at":"...","by":"user","op":"put","addr":"10.11.21.0000.00","body":"..."}
```

## The work

### Fractal design

The storage shape is decided: one `.book` file for a book, a shelf, a desk, and the kernel. The remaining fractal work is to show that the same address rules and the same log entries describe a face, a page, and the kernel book. A second container needs a recorded failure of this one.

### Sequence addressing

`seqAddr.md` plus the settled decisions. The file type is the book log, not a page file.

Settled, and not reopened by the build:

- Short form, the leading dot, exact widths, titles as labels, tails by position (A1, A2).
- Container identity on page `0000` (A3). `00` is the owner of the level above. Face `00` is the page stamp (A4).
- `99` is a pointer, with a required back-link (A5).
- The kernel is desk `00`. Its book is `00.00.00`. Desks `01-09` are kernel branches. Desks `10-98` are user environments. One namespace per repository (A6).
- A page needs face `00` and at least one content face. A card key is the heading in title form. The same key on two faces is the same card (C1.1, C2).
- Every face 01 or 02 card has a face 04 card with the same key, a `why:` line, and a body (C3.1, C3.2).

### Kernel

Desk `00`, book `00.00.00`, identity page `00.00.00.0000`. The lookup ends there: book, shelf, desk, kernel. The kernel is the template for pages `0000-0999`, live, not copied at creation (A2.9). Page types live on kernel structural pages `0050-0099` (C1.4). The first build includes the kernel only as a book file the lookup can open. It does not fill the template.

## First build

Not started. This is the slice to build when asked. It is the core, not the compute process and not the app.

Done when all of these hold:

1. A full address parses. A short address expands against an active book. A bad width is rejected, not padded. A leading dot resolves against one active page, and is refused when more than one page is active.
2. A `.book` file replays to current faces. A `put` appends. A `tail` moves only when `from` is the current tail. A partial last line is dropped and earlier entries still replay.
3. The writer API is the only way to append. A caller cannot hand the library a raw line and have it stored.
4. One fixture book, `10.11.21`: identity page `0000`, page `1001` title `timer`, faces `00`, `01`, and `04` sharing the card `purpose`, with a `why:` on face `04`.
5. A person can open the fixture in an editor and read the why.

Left out of the first build, on purpose:

- The compute process, its queue, and how clients talk to it (HTTP, MCP, or both). Open in `claude/format.md`.
- The Next.js app and WebAssembly.
- Snapshots, archives, and fork reconciliation. Open.
- Drafting ops `copy`, `note`, `merge`, `promote`. The principle is settled. The mechanism is proposed (D0).
- Dictionary meters and word resolution (C8.6 through C8.9, proposed).
- A dead worker, and where a rejected review goes. Still open in `claude/seqaddr-review.md` section D.
- Filling kernel pages.

## Still open

These stay open. The first build does not settle them. Each one starts at research when its turn comes.

- Client transport: HTTP, MCP, or both.
- How the compute reconciles two copies of a book edited apart.
- When to append a snapshot, and when to move old entries to an archive.
- Whether continuation pages share the `pointer` page type (C1.4).
- The drafting mechanism (D0), beyond the principle.
- Brand meters, resolution, and card types (C8.6 through C8.9).
- Task failure: a rejected review, and a worker that dies while `open`.
- Hardware.

## How a new question is done

Settled entries are not researched again. A question that is still open uses this process.

1. **Research.** Name systems that already do this. A lookalike that fails a written constraint is rejected here, with the constraint it fails.
2. **Choices.** List each survivor with the reason to try it and the reason to doubt it. Name which one is first, and why.
3. **Lab gate.** Say whether a lab is required. A lab is required only when more than one candidate still meets every written constraint and the remaining difference is behavior.
4. **Build.** Write the design slice, then the code for that slice only. Another model can attack the slice against `claude/decisions.md` and `claude/format.md`.

A hostile pass looks for a reopened settled choice, a contradiction with those files, a concern folded into another, a why missing from the record, and a first build that quietly includes something listed under "left out."

## Conduct

1. Check the technical spec on every change. Core, compute, app, and clients stay separate.
2. Do not build until asked. When asked, build the first build and stop at its edge.
3. Do not invent a second book format. Do not number a new kernel.
4. Leave an open item open.
5. Be concise. No emojis.
