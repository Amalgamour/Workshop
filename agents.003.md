# Workshop

Proposed agent brief. `AGENTS.md` is the user's brief and governs; this file adds how the work is done. Updated 2026-11-11, after the user edited `AGENTS.md` directly.

The order follows `AGENTS.md`: folders and sources, then deliverables, then the technical spec, then the work. The technical spec governs the deliverables and the work.

## Folders

| Folder | Holds | Agents may |
|---|---|---|
| `/` (Workshop root) | the latest version of the design | update, following "How a document changes" |
| `director/` | the user's own work and originals | read only. Never edit, move or delete. |
| `claude/` | Claude's working notes, research and history; tracked on the `claude` git branch | add notes; keep history |

New work the user places in `director/` is input. It is discussed, decided, recorded in `decisions.md`, and only then carried into the root documents.

## Sources, in order

1. **`Axioms.md`.** The nine axioms: the shape every piece of work starts from. Their faces are in `axioms/`.
2. **Settled entries in `decisions.md`.** Each has a number and a reason. Section E records the axioms.
3. **Decided entries in `format.md`.** Proposed entries there are not settled.
4. **`seqAddr.md`, `brands.md`, `drafting.md`, `Design.md`.** They apply the decisions. Where one disagrees with `decisions.md`, `decisions.md` wins and the document is corrected.
5. **This file,** for how the work is done.

Proposed, not settled: `kernel-design.md` (the kernel's role and bootstrap), `claude/readpath.md` (how a prompt becomes a pack). They become sources only when the user decides them (decision E9).

Background, not rules: `claude/seqaddr-review.md` (the original question list), `claude/research-b-format.md` (research behind the book file), `claude/alignment-notes.md` (open items and how inconsistencies were resolved), `claude/kernel-notes.md` (what the old Librarian kernel answers; it informs and does not govern), `claude/labs/` (cold-model trials of the axioms).

## Deliverables

From `AGENTS.md`:

1. **Design first.** `AGENTS.md` no longer says "design only", and now names compute, the database and a Next.js UI. User, 2026-11-11: the Rust core has started, and the aim is an app a person can use, where a model proposes and the compute's decision is visible. The next packs for that aim are drafted on `10.10.10` and are not a grant to build them until the person answers the open questions on page `0405`.
2. **The choices are made:** hardware, software and design. Software and the book file are decided in `format.md`. Hardware is not decided.
3. **A persistent, retrievable store of whys.** A why is the reason to do something. A finished spec is a recipe, and recipes rot. Face 04 holds the why a person reads; the book log makes a rebuild possible.
4. **Reliability.** Intelligence bleeds. Models never write from memory (`drafting.md`). Every change is an approved, appended log entry.
5. **Storage options were given.** `format.md` section 2 lists the options and why each was chosen or set aside.
6. **A person can check it.** Books are JSON Lines with Markdown faces.

## Technical spec

1. **Four parts, kept separate.**
   - **Core** (Rust): address parser and validator, book reader and writer, tail rules. One implementation.
   - **Compute** (Rust): one per repository. Owns every book, including the kernel. Reads are open; writes are proposals the compute validates and approves. Only the compute appends to a book.
   - **App** (TypeScript, Next.js): the reader for faces and links, using the core as WebAssembly.
   - **Agent clients** (any language): talk to the compute; never touch book files.
2. **Fractal.** The same shape at every level: identity at `00`, continuation at `99`, types with kernel rules, a word after a container is a title and after a face is a card. Every container is a book file: `10.11.21.book`, `10.11.00.book`, `10.00.00.book`, `00.00.00.book`. Before a different shape is introduced, record why this one failed a written constraint.
3. **Why.** Every decision is recorded with its reason. Every 01 or 02 card has a 04 card with `why:`.
4. **Record.** Notes are taken and reviewed. A process not written down is not recovered.

## Settled

| Area | Entries | Where applied |
|---|---|---|
| Addresses: short form, titles, tails, bands, layout, identity, 00 and 99, kernel, namespace | A1-A6 | `seqAddr.md` |
| Faces: required faces, page types, cards, 04 as full explanation, face 03 | C1 (except the C1.4 split), C2, C3, C6 | `seqAddr.md` |
| Dictionary and brands: brand cards, index, layout, meters, resolution, card types | C8 (except C8.7's open question and C8.10) | `brands.md` |
| Drafting principle | D0 (the mechanism is proposed) | `drafting.md` |
| Book file: compute model, one file per book, append-only log, Rust core, one compute per repository | `format.md` sections 1, 2, 3, 5 | `format.md` |
| Authority: the order, user levels, scope, halts | C5.1-C5.3 | `decisions.md` |
| The nine axioms, the `axioms:` field, chain grammar, default lead, lineage, trial | E1-E7 | `Axioms.md`, `axioms/`, `seqAddr.md` |

Settled entries are not reopened unless the user asks.

## Open

- C1.4: do continuation pages (`99`, `9999`, `PP99`) share the `pointer` type?
- C4: how the compute holds and traces face 08 links in memory.
- C5.4: authority precedence between levels (proposed); levels `02`, `03`, `05-09`.
- E8: open from the axioms: written permission, marks, hats, the axioms' page number, whether a trial needs a different intelligence.
- E9: proposals awaiting the user: the read path (R1-R9), the kernel bootstrap, and answers from the old kernel (C4 link kinds, C7 note fields, where a return lives, task and ticket counters, patch and strike, a concordance).
- C7: notes metadata.
- C8.7: does a failure count only against an assumed brand?
- C8.10: where a new brand card goes when no page for it exists.
- D0: the drafting mechanism (`copy`, `note`, `merge`, `promote`).
- `format.md`: proposal batches, the `use` record, the compute's write lifecycle, client transport (HTTP, MCP, or both), fork reconciliation, snapshot policy.
- Section D: a rejected review, a worker that dies while `open`, how claims work.
- Dictionary boundaries within each letter: checked against a real word list before freezing.
- Hardware.

## How a question is worked

1. **State the concern** plainly, with a concrete example of it breaking.
2. **Research** when the answer is not already in the sources. Name existing systems that do this, and say what would argue against the current idea.
3. **Recommend** one option, with the reason and the cost. Give the user the decision; do not decide for them.
4. **Record** the answer in `decisions.md` with a number, a status (settled or proposed) and the reason.
5. **Apply** it to the root documents (below).

## How a document changes

The drafting rule applies to documents too:

1. Take notes first: what changes, in which file, and why.
2. Update from the notes. Change the lines that need changing; do not rewrite a document from memory.
3. Check every root document against `decisions.md` afterwards, and record any inconsistency found and how it was resolved.
4. The user's files in `director/` are never edited. If one needs an aligned version, make a copy beside it in the root or in `claude/`.

## First build

The user confirmed this start on 2026-11-11. Address of the temp workbook: `10.10.10`. The core lives in `core/`.

The core library, not the compute or the app. Done when:

1. A full address parses; a short address expands against an active book; a bad width is rejected, not padded; a leading dot resolves against one active page and is refused when more than one is active.
2. A `.book` file replays to current faces. A `put` creates a face; a `tail` moves only from the current tail; a partial last line is dropped and earlier entries still replay.
3. The writer API is the only way to append.
4. One fixture book `10.11.21`: identity page `0000`, page `1001` titled `timer`, faces `00`, `01` and `04` sharing the card `purpose`, with `why:` on face 04.
5. A person can open the fixture in an editor and read the why.

## Conduct

1. The Rust core's first checks are met. The aim is the usable app. On 2026-11-11 the person ordered three passes without waiting for the open questions on `10.10.10.0405`. Those questions stay open. A local HTTP server in a pass is a trial so a browser can see the compute. It does not settle HTTP, MCP, or both.
2. Leave an open item open; do not settle it by implication.
3. Carry the axioms: cite them on work (`axioms:`), and test a change against cold models before it is promoted (axiom 9, `claude/labs/`).
4. Never edit `director/`.
5. Anything that cannot be resolved goes to the user, never guessed.
6. Be concise. No emojis.
