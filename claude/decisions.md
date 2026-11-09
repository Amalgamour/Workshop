# seqAddr Decisions

Working record of decisions on the open items in `seqaddr-review.md`. A full rework of `seqAddr.md` follows once A1-A6 are settled.

---

## A1. Short form

Status: settled, except A1.6 (active page), which is proposed.

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

### A1.6 Active page (proposed)
The session has one active book, and usually an active page, but sometimes several pages are in play. A bare `04` cannot mean "face 04 of the active page", because A1.3 already reads it as desk 04.

Proposal: a **leading dot** means "relative to the active page".
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
