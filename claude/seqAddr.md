# Sequence Address (seqAddr)

Reworked from `../seqAddr.md` with the decisions in `decisions.md` (A1-A6). Section numbers in brackets point to the decision behind each rule.

## What it is

A file type in which a page has several faces instead of one. Each face holds a different kind of information about the same page, for a different reader: agents, compute, users.

---

## 1. Address structure

### 1.1 Axes
Five axes, highest on the left, separated by dots. Widths are exact: `4442.1` is invalid. [A1.5]

| Axis | Width | Name | Role |
|---|---|---|---|
| `DD` | 2 | desk | highest controlling environment |
| `SS` | 2 | shelf | themed work space |
| `BB` | 2 | book | localized environment |
| `PPPP` | 4 | page | the work inside a book |
| `FF` | 2 | face | one view of a page |

A counter `NN` (2 digits, 01-98) may follow a face. Counters are not an axis and attach only to faces. [A1.4]

### 1.2 Reserved values on every axis
| Value | Meaning |
|---|---|
| `00` / `0000` | the owner of the level above, itself [A4.1] |
| `01-09` / `0001-0099` | reserved |
| `99` / `9999` | pointer: look for the next location [A5.1] |

### 1.3 Desks [A6.3]
| Desk | Use |
|---|---|
| `00` | kernel. Its own book is `00.00.00`. |
| `01-09` | kernel branches, downloaded into the repository as needed |
| `10-98` | user environments |
| `99` | reserved pointer |

Each repository is its own namespace and contains its own kernel. [A6.2, A6.4]

### 1.4 The owner rule
00 at any level means "the owner of the level above, itself". [A4.1]

| Address | Meaning |
|---|---|
| `DD.00.00` | the desk's own book |
| `DD.00.BB` | a desk book: owned by the desk, no shelf |
| `DD.SS.00` | the shelf's own book |
| `DD.SS.BB.0000` | the book's own page |
| `PPPP.00` | the page's own identity face |
| `FF.00` | a counted face's board |

### 1.5 Identity
Every container is identified by a page 0000, whose stamp holds its title. [A3.1]

| Container | Identity page |
|---|---|
| Book `10.11.21` | `10.11.21.0000` |
| Shelf `10.11` | `10.11.00.0000` |
| Desk `10` | `10.00.00.0000` |

A page is identified by its face 00, which holds the page stamp (address, title, state). Faces carry no stamp of their own. [A4.2]

---

## 2. Reading an address

### 2.1 The page is the anchor [A1.2]
The page is the only 4-digit axis, so any address containing it reads by position alone:

```
[DD.][SS.][BB.] PPPP [.FF][.NN] [.title][.tail]
```

- Right of the page: one group is `FF`, two are `FF.NN`.
- Left of the page, reading right to left: `BB`, `SS`, `DD`.
- Missing ancestors are taken from the active book.

| Written | Inferred | In active book `10.11.21` |
|---|---|---|
| `PPPP...` | DD, SS, BB | `4442.01` -> `10.11.21.4442.01` |
| `BB.PPPP...` | DD, SS | `12.2523.04` -> `10.11.12.2523.04` |
| `SS.BB.PPPP...` | DD | `30.12.2523` -> `10.30.12.2523` |
| `DD.SS.BB.PPPP...` | nothing | full address |

### 2.2 No page: a container address from the desk [A1.3]
`21` is desk 21, `10.11` is a shelf, `10.11.21` is a book. A sibling book in short form is written through its identity page: `21.0000`.

### 2.3 Leading dot: the active page [A1.6]
`.04` is face 04 of the active page, and `.05.03` is task 03 on it. If several pages are active, a leading-dot address is elevated to the user.

### 2.4 Short form is for users [A1.7]
Users may write short form. Models always write the full address and state it back when a user wrote short form, including where it was found if inherited.

### 2.5 Finding [A1.8, A2.9]
Reading needs only the rules above. Finding looks up in order:

```
book 10.11.21 -> shelf 10.11.00 -> desk 10.00.00 -> kernel 00.00.00
```

The first match wins. Books follow the kernel live: anything not overridden locally is found in the kernel. If nothing is found, the address is elevated to the user, never guessed.

---

## 3. Titles [A2]

- A word after `DD`, `SS`, `BB` or `PPPP` is a title. Faces never have titles: a face is `PPPP.FF` or `PPPP.FF.NN`. [A2.1, A2.2]
- Characters: lowercase letters, digits, hyphens. Starts with a letter. No dots or spaces. [A2.3]
- Tail words are reserved and are never titles. [A2.5]
- A title is a label, not identity. `4442` and `4442.timer` are the same page, and several pages may share a title. [A2.4]
- Pages 1000 and up must have a title. Pages 0001-0999 may. Page 0000 has none. [A2.8]
- A title stored in a stamp is the truth. A title written in an address is checked against it, and a mismatch is elevated to the user. [A2.8, A3.2]

---

## 4. Tails [A2.5]

A tail follows a title or a face. Only a tail may follow a title.

| Level | Written | Tails |
|---|---|---|
| Page | `PPPP.title.tail` or `PPPP.tail` | `draft`, `retired` |
| Face | `PPPP.FF.tail` | `draft`, `retired` |
| Counter | `PPPP.FF.NN.tail` | `draft`, `pack`, `open`, `return`, `review`; bare = closed |
| Desk / shelf / book | none | state comes from the identity page: `10.11.21.0000.retired` |

| Tail | Meaning |
|---|---|
| `draft` | being written; not active |
| `pack` | ready to run |
| `open` | being run by a worker |
| `return` | what was done |
| `review` | under review |
| `retired` | previously seated, retired before removal |

Workflow state lives only on counters.

---

## 5. Faces

### 5.1 Face numbers [A4.3]
| Face | Name | For |
|---|---|---|
| `00` | identity | the page stamp |
| `01` | law | agents: the meaning of the page, in model-efficient cards |
| `02` | schema | model or compute: templates, formats, exact processes |
| `03` | operate | compute: operations for executing a card; the card menu; where authority comes from. Mainly in the kernel and desk books. |
| `04` | user | users: the why of the page, long form, for inspection |
| `05` | tasks | working agents: passes, as counters |
| `06` | notes | models leaving information: one counter per session |
| `07` | reserved | not active |
| `08` | map | links: authority, dependencies, what is needed to find and use the page |
| `09` | reserved | unassigned |
| `10-98` | reserved | for later customization |
| `99` | reserved | |

### 5.2 Face content
- **Contents:** a viewable list of the face's cards.
- **Cards:** like kanban cards. A title that can be referenced to find and retrieve one piece of information, with details as the body.
- **Cross-face links:** cards link across faces by title. A face 01 card that needs a schema, format or template has it on face 02.
- **Face 04 mirrors 01 and 02:** every card on face 01 and 02 has a section on face 04 with its why and a full readable explanation. Face 04 also records the user's own ideas, which need no counterpart on 01 or 02. Most user-created pages have only face 04.
- **Face 06 notes** record which model wrote them, what they reference, when, and why.

### 5.3 Counted faces [A4.4, A4.5]
- A face is counted if and only if `FF.00` exists. `FF.00` is the board: every counter and its current tail.
- A counter without a board is invalid.
- A counted face is never seated. Plain `FF` on a counted face means `FF.00`.
- Faces 05 and 06 are always counted. Others may be counted on certain page types (for example 03 or 04 on a contents or dictionary page).
- A face without counters is seated at `DD.SS.BB.PPPP.FF`. `FF.draft` is its unseated draft. `FF.retired` is a previously seated face awaiting removal.

```
1523.05.00   board
  05.01  closed
  05.02  review
  05.03  open
  05.04  pack
```

---

## 6. Book page layout [A2.7]

The kernel is the template for `0000-0999` in every book.

| Range | Use |
|---|---|
| `0000` | book identity |
| `0001-0009` | special reserved pages |
| `0010-0019` | contents, dictionary, concordance and other required pages |
| `0020-0049` | localized behaviour: exists locally or is inherited |
| `0050-0099` | structural pages, mostly in the kernel or templates |
| `0100-0999` | standard bands modelled by the kernel |
| `1000-9998` | user space; users design their own bands |
| `9999` | book continuation |

A page in `0001-0099` that exists in a book is a local override of the inherited environment.

### 6.1 Bands [A2.6]
A page number reads as `NDNN`. `D`, the second digit, is the band.

```
0 4 23
N D NN     D = 4 = dev band, NN = 23 = item in the band
```

- Every band is exactly 100 pages, `PP00-PP99`.
- Every page at or above `0100` ending in `00` is a band head, holding the band's definition and contents.
- `PP99` is the band's continuation.
- Pages with the same `N` and `NN` in different bands form a set: `0423.timer` (dev) and `0523.timer` (build). Titles should match.

---

## 7. Continuation and links [A5, A6.1]

- 99 at any level is a pointer to the next location. It lists every valid path onward. Its face 08 records each target and the kind of link (continuation or child).
- A pointer may list several targets: several child desks, several continuations, or a fork.
- Every target's identity page links back. A one-way link is invalid.
- Each pointer's direct links are the source of truth. An ancestor's list of everything further down the chain is derived by walking the links, never edited by hand.
- Child desks take their own desk number. Hierarchy beyond the fixed depth exists only through links.
- Missing is a valid state: no `FF.00` means not counted, no `FF.99`, `PP99` or `9999` means no continuation. [A4.6]

### 7.1 Overflow
- **Counters:** once `FF.98` exists, `FF.99` points to the same face on the next free page in the same band. Counting restarts at `01`. Old counters never move.
- **Bands:** a full band continues through `PP99` to the next free hundred (`1099` -> `2100`). Bands never grow in place. Items in a continuation band link to their set explicitly in face 08.

---

## 8. Grammar

```
address    = container / page-addr / active-rel
container  = desk [ "." shelf [ "." book ] ] [ "." title ]
page-addr  = [ ancestors "." ] page [ "." page-end ]
ancestors  = book / shelf "." book / desk "." shelf "." book
page-end   = face-part / title [ "." page-tail ] / page-tail
active-rel = "." face-part
face-part  = face [ "." counter ] [ "." tail ]

desk       = 2DIGIT
shelf      = 2DIGIT
book       = 2DIGIT
face       = 2DIGIT
counter    = 2DIGIT                       ; 00 board, 01-98, 99 continuation
page       = 4DIGIT
title      = LOWER *( LOWER / DIGIT / "-" )   ; not a tail word
page-tail  = "draft" / "retired"
tail       = "draft" / "retired" / "pack" / "open" / "return" / "review"
```

Rules the grammar does not express:
- `retired` only without a counter; `pack`, `open`, `return`, `review` only with one.
- A counter requires its face's `00` board.
- Counter `00` is the board itself; write it as `FF.00`.
- Containers need their identity page to be legal.
- Pages 1000 and up need a title in their stamp.

---

## 9. Not yet designed

From `seqaddr-review.md`, sections B-D:

- **On-disk format:** one file per page or per face, file naming and folders, body syntax, stamp fields, card syntax and title matching.
- **Faces:** which faces each page type requires, how face 04 is kept in sync with 01 and 02, whether face 08 is written or derived, and authority precedence between levels.
- **Task lifecycle:** failure paths (rejected review, dead worker), how an agent claims a `pack`, and how a seated face is replaced by its draft.
