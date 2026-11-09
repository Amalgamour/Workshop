# Design

The system overview. It ties the other documents together; each rule is defined in exactly one of them.

| Document | Defines |
|---|---|
| `seqAddr.md` | addresses, faces, cards, page layout, grammar |
| `format.md` | the book file and the compute |
| `brands.md` | dictionary and word meanings |
| `drafting.md` | how a face is changed |
| `decisions.md` | every decision and its reason, numbered |
| `alignment-notes.md` | what is still open |

## What it is for

A persistent, retrievable store of **whys**. A why is the reason to do something. A finished spec is a recipe, and recipes rot. With the why, a rebuild is possible. Every part of the design serves four requirements (AGENTS.md):

| Requirement | How the design meets it |
|---|---|
| Store whys | Face 04 holds a `why:` for every card on 01 and 02 (C3). |
| Reliability: intelligence bleeds | Models never write from memory (drafting). Every change is an approved, appended log entry; nothing is edited in place. |
| Checkable by a person | Books are text: JSON Lines with Markdown faces. Meters and boards are visible. |
| Record | The log is the record. Decisions carry their reasons (`decisions.md`). |

## The parts

```
 users, models, agents
        |  read any face / submit proposals
        v
   +---------+        validates every proposal against
   | compute |  <---  seqAddr rules, page and card types,
   +---------+        drafting, 04 checks
        |  appends approved writes
        v
   book files (one per book, shelf, desk, kernel)
```

| Part | Language | Role |
|---|---|---|
| Core | Rust | address parser and validator, book reader and writer, tail rules |
| Compute | Rust | one per repository; owns every book; open reads; queued, approved writes |
| App | TypeScript, Next.js | the reader: shows faces and how they link; uses the core as WebAssembly |
| Agent clients | any | talk to the compute; never touch book files |

## Fractal

The same shapes repeat from the smallest level to the largest:

| Pattern | Book | Page | Face |
|---|---|---|---|
| Identity at `00` | page `0000` | face `00` | board `FF.00` |
| Continuation at `99` | page `9999` | band `PP99` | `FF.99` |
| Types with kernel rules | - | page types | card types |
| Word after it | title | title | card key |

Every container is a book, so the kernel, a desk and a shelf are stored exactly like a book.

## How work flows

1. **Read.** Anyone reads any face. Short addresses expand against the active book; inherited pages are found by the lookup book, shelf, desk, kernel.
2. **Propose.** A writer submits one or more operations. Existing faces change only through drafting: copy, note, merge, promote.
3. **Validate.** The compute checks the address, the page and card types, the 04 rules and back-links. Hard failures are rejected with a reason; findings are recorded for review.
4. **Append.** Approved operations are appended to the book. Boards, contents, menus, ancestor paths and meters are derived from the log.
5. **Elevate.** Anything the compute cannot resolve goes to the user and is never guessed.

## Meaning

Words resolve through brands (`brands.md`): the user's own meanings, recorded on brand cards and found through each book's dictionary. Assumptions are stated back, and failed retrievals update the meters.

## Not yet decided

- Hardware.
- Client transport (HTTP, MCP, or both), fork reconciliation, snapshot policy (`format.md`).
- C1.4, C4, C5, C7, C8.7, C8.10 and section D (`alignment-notes.md`).
