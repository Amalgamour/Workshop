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

Status: partly settled. Open items are marked proposed.

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

Proposed:
- Tail words are reserved and can never be titles. Then `PPPP.draft` (an untitled page in draft) and `PPPP.plan.draft` are both unambiguous.
- Allowed tails per level (to confirm):

| Level | Tails |
|---|---|
| Page | `draft`, `retired`? |
| Face | `draft`, `retired` |
| Counter | `draft`, `pack`, `open`, `return`, `review` (bare = closed) |
| Desk / shelf / book | none? |

### A2.6 Bands (proposed reading, to confirm)
The hundreds digit of a page number groups pages into bands: `N3NN` modules, `N4NN` dev, `N5NN` build. One project uses the same title across bands, for example a timer:
- `N4NN.timer` is the dev page: MVP, goals, why, how.
- `N5NN.timer` is the build page. Its `05.NN` counters are passes, and each pass moves through tails like a kanban card.

Open questions:
- Is the set linked by **number** (1423 / 1523 / 1323 share `N` and `NN`), by **title**, or both? Linking by number survives renames, which fits A2.4. Linking by title alone would break when a title changes.
- Is the band digit a **fixed rule** the validator knows, or a **convention defined per book** (for example on a structural page 0050-0099)?
- Which band digits exist, and what do 0-2 and 6-9 mean?
