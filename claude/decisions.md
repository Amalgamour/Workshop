# seqAddr Decisions

Working record of decisions on the open items in `seqaddr-review.md`. A full rework of `seqAddr.md` follows once A1-A6 are settled.

---

## A1. Short form

Status: settled.

### A1.1 Every address is full; short form only leaves parts unstated
A page or face always has a full address `DD.SS.BB.PPPP[.FF[.NN]]`. Short form is a way of *writing* it that leaves out ancestors. Those are inferred from the active book's book, shelf and desk.

### A1.2 The page is the anchor
The page is the only 4-digit axis. Any address with a 4-digit group can be read by position alone:

```
[DD.][SS.][BB.] PPPP [.FF][.NN] [.tail]
```

- Right of the page: 1 group = `FF`, 2 groups = `FF.NN`.
- Left of the page, reading right to left: `BB`, then `SS`, then `DD`.
- The number of groups on the left decides what is inferred:

| Written | Inferred from active book | Example in `10.11.21` |
|---|---|---|
| `PPPP...` | DD, SS, BB | `4442.01` -> `10.11.21.4442.01` |
| `BB.PPPP...` | DD, SS | `12.2523.04` -> `10.11.12.2523.04` |
| `SS.BB.PPPP...` | DD | `30.12.2523` -> `10.30.12.2523` |
| `DD.SS.BB.PPPP...` | nothing | already full |

### A1.3 No page means a container address from the desk
An address with no 4-digit group is always read from the desk: `21` is desk 21, `10.11` is a shelf, `10.11.21` is a book. To refer to a sibling book in short form, use its sentinel page: `21.0000` is book 21 on the active shelf.

### A1.4 Counters attach only to faces
`NN` exists only directly after `FF`. Counters are not an axis, so the reserved 01-09 range does not apply to them. The first counter is `01`.

### A1.5 Exact widths
Every group must have its exact width. `4442.1` is invalid, not padded to `4442.01`.

### A1.6 Active page
The session has one active book, and usually an active page, but sometimes several pages are in play. A bare `04` cannot mean "face 04 of the active page", because A1.3 already reads it as desk 04.

A **leading dot** means "relative to the active page".
- `.04` is face 04 of the active page.
- `.05.03` is task 03 on the active page.
- No other address starts with a dot, so this never collides with A1.3.
- If more than one page is active, `.04` is ambiguous and is elevated to the user (same as A1.8).

### A1.7 Short form is for users; models echo the full address
Users may write short form. Models always write the full address. When a user writes short form, the model states the expanded full address back. If the address was inherited (A1.8), the model also states where it was found.

### A1.8 Reading vs. finding
- **Reading** (is it well formed?) uses only A1.2-A1.5. It needs no context beyond the active book.
- **Finding** (where is it?) looks up in order: book -> shelf -> desk -> kernel. The first match wins. This matters for the inherited reserved pages (0020-0049).
- If nothing is found, the address is **elevated to the user** to resolve. It is never guessed.

### Carried forward
- Where a shelf or desk physically keeps its own pages (needed for the A1.8 lookup) belongs to **A4**.
- The kernel's address belongs to **A6**.

---

## A2. Titles and tails

Status: settled.

### A2.1 Position decides
A word after DD, SS, BB or PPPP is a title. A word after FF or NN is a tail. Faces never have titles.

### A2.2 Faces carry no title
A face is written `PPPP.FF` or `PPPP.FF.NN`. `2423.05.01` is page 2423, face 05 (tasks), counter 01: one task. "Go to 2423.05.01 and run it" is unambiguous.

### A2.3 Title characters
Lowercase letters, digits and hyphens. Starts with a letter. No dots, no spaces.

### A2.4 Titles are labels and need not be unique
A title is not part of identity: `4442` and `4442.plan` are the same page. Several pages may share a title on purpose. This is how a band set works (A2.6).

### A2.5 Where tails attach
A tail follows a title or a face:
- Page: `PPPP.title.tail`
- Face: `PPPP.FF.tail`
- Counter: `PPPP.FF.NN.tail`

Only a tail may follow a title.

Tail words are reserved and can never be titles. `PPPP.draft` and `PPPP.plan.draft` both mean page PPPP in draft.

Allowed tails per level:

| Level | Tails |
|---|---|
| Page | `draft`, `retired` |
| Face | `draft`, `retired` |
| Counter | `draft`, `pack`, `open`, `return`, `review` (bare = closed) |
| Desk / shelf / book | none |

Workflow state lives only on counters. A container takes its state from its sentinel page: `10.11.21.0000.retired` retires the book, `10.11.21.0000.draft` is a book still being set up.

### A2.6 Bands
A page number reads as `NDNN`. `D` (the second digit) is the band.

```
0 4 23
N D NN     D = 4 = dev band, NN = 23 = item in the band
```

- **Fixed width.** Every band is exactly 100 pages, `PP00` to `PP99`.
- **Head by number.** Every page at or above 0100 ending in `00` is a band head. It holds the band's definition and contents. No marker or tail is needed: listing pages that end in `00` finds every band.
- **`PP99` is continuation.** A band that outgrows 100 pages points to its continuation from `PP99`, as page 9999 does for a book. This mirrors the axis sentinels: `00` start, `99` end.
- **Sets across bands are linked by number.** Pages with the same `N` and `NN` in different bands are one set: `0423.timer` (dev) and `0523.timer` (build). Titles should match; a mismatch is elevated to the user (A2.8).

### A2.7 Book page layout
The kernel is the template for `0000-0999` in every book, including what each band digit means there.

| Range | What it is |
|---|---|
| `0000` | book identity (sentinel) |
| `0001-0099` | reserved; a page here is a local override of the inherited environment |
| `0100-0999` | standard bands modelled by the kernel (`0100` ... `0900`) |
| `1000-9998` | user space; users design their own bands (`1000` ... `9800`) |
| `9999` | continuation (sentinel) |

`1000` is the head of the first user band, which is why the first open page is `1001`.

### A2.9 Live inheritance
Books follow the kernel template live; they do not copy it at creation. Anything a book does not override is found through the A1.8 lookup (book -> shelf -> desk -> kernel), so a kernel change reaches every book that has not overridden it.

### A2.8 Which pages need a title
1. Pages 1000 and up must have a title, stored in the stamp.
2. Pages 0001-0999 may have a title; their number is already their name. Page 0000 has none (it holds the book's title in its stamp).
3. A title in a written address is optional. If written, it is checked against the stamp. A mismatch (`4442.timer` when the stamp says `clock`) is elevated to the user.
4. Tail words can never be titles (A2.5).

---

## A3. Where container titles live

Status: settled.

### A3.1 Every container is identified by a page 0000
Each desk, shelf and book has an identity page. Its stamp holds the container's title.

| Container | Identity page |
|---|---|
| Book `10.11.21` | `10.11.21.0000` |
| Shelf `10.11` | `10.11.00.0000` |
| Desk `10` | `10.00.00.0000` |

### A3.2 Titles in addresses are checked labels
A title written in a container address (`10.11.21.tools`) is checked against the identity page's stamp. A mismatch is elevated to the user (A2.8).

---

## A4. Meaning of 00 and 99

Status: A4.1 settled; face and counter axes open.

### A4.1 00 means "the owner of the level above, itself"
One rule for every container axis:

| Address | Meaning |
|---|---|
| `DD.00.00` | the desk's own book (identity, law, overrides) |
| `DD.00.BB` | a desk book: owned by the desk, no shelf |
| `DD.SS.00` | the shelf's own book |
| `DD.SS.BB.0000` | the book's own page |

Consequences:
- The A1.8 lookup uses real books: book `10.11.21`, then shelf `10.11.00`, then desk `10.00.00`, then kernel. An inherited page such as `0020` lives at `10.11.00.0020` or `10.00.00.0020`.
- A container's state uses page tails (A2.5): `10.00.00.0000.retired` retires the desk.
- Shelf 00 and book 00 are never ordinary shelves or books.
