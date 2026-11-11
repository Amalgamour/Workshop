# The .seq page file: a reader's guide

For: Matthew (the Director).
Status: a guide. It explains the spec. It does not change it.
The full spec stays in `docs/spec/seqpage.md`. If this guide and the spec ever disagree, the spec wins, and the guide is wrong.

Every example below is copied from a real file in `docs/spec/examples/`.
Every command below was run, and its real output is shown.

---

## 1. What a .seq file is

A `.seq` file holds **one page**.

It shows all of that page's faces, top to bottom, as plain text you can read.

---

## 2. Why it exists

The **book** is the real copy. The `.seq` file is only a **view** of one page. (R3)

- You get a `.seq` file **out** of a book. (export)
- You send a `.seq` file **back in**. (import)
- Sending it back never writes the book directly. It becomes a request that waits in line for a check. (the proposal queue, R3)

Going out and back in loses nothing. Every field, every body, every entry number comes back the same. (lossless, R3; seqpage.md section 1)

---

## 3. The file name

The name is the page address, then the title, then `.seq`.

```
10.11.40.1001.cats.seq
```

- `10.11.40.1001` is the page address. (desk.shelf.book.page)
- `cats` is the page title, from face 00.
- A page with no title has no title in its name: `10.11.40.0000.seq`.

If the title in the name does not match the title inside, you are told. It is never fixed quietly. (A2.8; seqpage.md section 2)

---

## 4. The example we will walk through

The real file is `docs/spec/examples/face00/10.11.40.1001.cats.seq`.

It is 48 lines long. It is a new page called "cats", still a draft.

Here it is, whole. The line numbers on the left are not part of the file.

```
 1  seqpage 1
 2  = 00 registry 10.11.40.1001.00
 3  title := cats
 4  state := draft
 5  registry := draft
 6  why-draft := a new page starts as a draft (drafting.md)
 7  faces := 01 draft
 8  type := general
 9  axioms := -
10  lineage := 10.11.40.1001 < 10.11.40 < 10.11.00 < 10.00.00 < 00.00.00
11  source := book 10.11.40 @9
12
13  --- @9 put 10.11.40.1001.00.draft
14  at: 2026-11-11T21:09:00Z
15  by: user
16  reason: a new page starts as a draft (drafting.md)
17  | ---
18  | address: 10.11.40.1001
19  | title: cats
20  | type: general
21  | state: draft
22  | why-draft: a new page starts as a draft; the user has not confirmed the meaning yet
23  | ---
24  |
25  | ## Registry
26  | faces: 01 draft
27  | why-01: the user has not confirmed this meaning yet
28
29  = 01 law 10.11.40.1001.01
30  state := draft
31  why-draft := the user has not confirmed this meaning yet
32  source := book 10.11.40 @10
33
34  --- @10 put 10.11.40.1001.01.draft
35  at: 2026-11-11T21:10:00Z
36  by: user
37  reason: the user has not confirmed this meaning yet
38  cards := cats
39  | ## cats
40  | type: brand
41  | brand: cats.001
42  | forms: cats
43  | means: animals the user likes
44
45  ~ history
46  @9 put 10.11.40.1001.00.draft
47  @10 put 10.11.40.1001.01.draft
48  ~ end
```

The next sections take it a piece at a time.

---

## 5. The first line

```
 1  seqpage 1
```

This says "this is a .seq file, version 1". (the magic line)

It is always line 1. (seqpage.md section 3)

---

## 6. Face 00 comes first

```
 2  = 00 registry 10.11.40.1001.00
```

A line starting with `= ` opens a face. (a face section header)

Face 00 is always first. On every page, face 00 is the **registry**: the place that says what the page is and what faces it has. (R10)

A file with no face 00 at the top is refused. (seqpage.md section 4)

---

## 7. Face 00 holds three things

Face 00 holds:

1. **the stamp**: what the page is (address, title, state). (R12)
2. **the type**: what kind of page it is.
3. **the registry**: a list of fields. Which fields depends on the type. (R19)

In the file, you see these in the written part, lines 17 to 27:

```
17  | ---
18  | address: 10.11.40.1001
19  | title: cats
20  | type: general
21  | state: draft
22  | why-draft: a new page starts as a draft; the user has not confirmed the meaning yet
23  | ---
24  |
25  | ## Registry
26  | faces: 01 draft
27  | why-01: the user has not confirmed this meaning yet
```

- Lines 17 to 23, between the two `---`, are **the stamp**.
- Line 20 is **the type**. Here it is `general`.
- Lines 25 to 27, under `## Registry`, are **the registry**.

The exact field list is still a draft. It lives in `docs/spec/face00.md`.

---

## 8. Lines with `:=` are worked out by the computer

```
 3  title := cats
 4  state := draft
 ...
11  source := book 10.11.40 @9
```

A line with `:=` is **worked out by the computer** when the file is made. (a derived line)

- It is there so you can see the answer at a glance.
- It is checked when the file is read. If it is wrong, the file is refused.
- It is **never imported**. Changing it cannot change the book.
- You may leave these lines out when you write by hand.

(seqpage.md section 7)

What each one in face 00 means:

| Line | Plain meaning |
|---|---|
| `title := cats` | the page title, read from the stamp |
| `state := draft` | the page is a draft |
| `registry := draft` | face 00 itself is a draft |
| `why-draft := ...` | why it is a draft (R5) |
| `faces := 01 draft` | the faces this page has, and their state |
| `type := general` | the page type, read from the stamp |
| `axioms := -` | no axioms named (`-` means "none written") |
| `lineage := ...` | the chain up: page, book, shelf, desk, kernel |
| `source := book 10.11.40 @9` | which book and entry this came from |

A `7` in one of these means "could not be worked out".

---

## 9. A block is one write

```
13  --- @9 put 10.11.40.1001.00.draft
```

A line starting with `--- ` opens a **block**. A block is one write.

Read this one as: "entry number 9 in the book, a `put`, to the address `10.11.40.1001.00.draft`".

- `@9` means it is **already in the book**, as entry 9.
- `new` instead of `@9` means it is **a write you are asking for**. (a proposal)

Here are the first lines of a real `new` block, from `docs/spec/examples/proposals/10.11.21.1001.bob.seq`:

```
--- new put 10.11.21.1001.06.01
| ## Session 2
| model: grok-bot
| why: the Bob test, session 2
```

`new` blocks always come after the blocks already in the book. New work goes after the past, never in front. (axiom 6; seqpage.md section 6.1)

---

## 10. Fields: who, when, why

```
14  at: 2026-11-11T21:09:00Z
15  by: user
16  reason: a new page starts as a draft (drafting.md)
```

Right under the block opener come its **fields**, one `key: value` per line.

- `at:` is when it was written. (the time is in UTC; 21:09 UTC is 4:09 PM EST)
- `by:` is who wrote it.
- `reason:` is why. (R5)

A booked block must have `at` and `by`.
A `new` block must **not** have them. The computer stamps those when it books the write.

(seqpage.md section 6.2)

---

## 11. Body lines start with a bar

```
39  | ## cats
40  | type: brand
41  | brand: cats.001
42  | forms: cats
43  | means: animals the user likes
```

A line starting with `| ` (bar, then space) is **body text**. It is the page's actual words.

- Every body line starts with `|`. So nothing in a body can be mistaken for the file's structure.
- A lone `|` is an empty line in the body (line 24).
- A heading like `## cats` starts a **card**: a named piece inside the face.

(seqpage.md section 6.4)

---

## 12. Other faces

```
29  = 01 law 10.11.40.1001.01
30  state := draft
31  why-draft := the user has not confirmed this meaning yet
32  source := book 10.11.40 @10
```

After face 00 come the other faces, in number order. Here it is face 01, named `law`.

- A face only shows up if it has writes. A missing face is fine. (A4.6)
- Faces have no 00 or 99 slots of their own. Counters run 01 to 98. (R9)
- On page 0000, face 00 is the only face allowed. (R10)

(seqpage.md section 5)

---

## 13. Drafts, and why they are drafts

```
34  --- @10 put 10.11.40.1001.01.draft
```

A draft has `.draft` on the end of its address. (R8)

A draft exists only while the face is being drafted. It is the working copy, so seated work is never replaced from memory. (R8, drafting.md)

Every draft shows **why** it is a draft: (R5)

```
31  why-draft := the user has not confirmed this meaning yet
```

The computer takes that from the `reason:` on the write that opened the draft (line 37). If there is no reason, it uses the first line of a note. If there is neither, it shows `7` and flags it. (seqpage.md section 5.1)

---

## 14. The history

```
45  ~ history
46  @9 put 10.11.40.1001.00.draft
47  @10 put 10.11.40.1001.01.draft
```

`~ history` starts a list of every write to this page, in book order: number, kind of write, address.

- It only grows. (axiom 6)
- Every booked block has a history line, and every history line has a block. They must match.
- `new` blocks are not in the history yet. They are not booked.

(seqpage.md section 8)

---

## 15. The end marker

```
48  ~ end
```

`~ end` is always the last line.

A file without it was cut off, and it is refused. Nothing may come after it. (seqpage.md section 8)

---

## 16. Plain characters only

A `.seq` file uses **plain characters only**. (R4)

That means the keys on a plain US keyboard: letters, numbers, spaces and ordinary marks. Plus the line break. (ASCII 0x20 to 0x7E, plus newline 0x0A)

Not allowed:

- accented letters, like an e with an accent
- curly quotes (use straight `"` and `'`)
- long dashes (use `-` or `--`)
- tabs (use spaces)
- emoji

The checker stops at the first bad character and tells you the line and column.

Real example. I copied the cats file and put an accented e into line 43. The check said:

```
{
  "ok": false,
  "errors": [
    {
      "line": 43,
      "code": "invalid",
      "rule": "R4",
      "detail": "column 30: U+00E9 is not allowed; a .seq file is plain ASCII 0x20-0x7E plus newline"
    }
  ],
  "findings": []
}
```

(seqpage.md section 3)

---

## 17. How to check a file yourself

Run these from the repo folder. First build the tool once:

```
cargo build -p seqpage
```

The tool is then at `target/debug/seqpage`.

The answers come back as JSON. `"ok": true` means good. The command exits with 1 on any error.

### 17.1 Check a file

This reads the file and compares it to its book.

```
target/debug/seqpage check docs/spec/examples/face00/10.11.40.1001.cats.seq --book docs/spec/examples/sources/10.11.40.book
```

Real output:

```
{
  "ok": true,
  "errors": [],
  "findings": []
}
```

### 17.2 Make a file from a book

```
target/debug/seqpage export docs/spec/examples/sources/10.11.40.book 10.11.40.1001 --out /tmp/cats.seq
```

Real output:

```
{
  "file": "/tmp/cats.seq",
  "ok": true,
  "page": "10.11.40.1001"
}
```

I compared `/tmp/cats.seq` to the example file with `diff`. They are the same, byte for byte.

### 17.3 Send a file back in

Import never writes anything. It shows the request it would make.

The cats file has no `new` blocks, so there is nothing to ask for:

```
target/debug/seqpage import docs/spec/examples/face00/10.11.40.1001.cats.seq --book docs/spec/examples/sources/10.11.40.book --by matthew
```

Real output:

```
{
  "booked": [
    9,
    10
  ],
  "findings": [
    {
      "code": "invalid",
      "detail": "no `new` blocks: nothing to propose",
      "line": 0,
      "rule": "seqpage 10"
    }
  ],
  "ok": true,
  "page": "10.11.40.1001",
  "proposal": {
    "by": "matthew",
    "ops": []
  }
}
```

The Bob file does have a `new` block. Adding `--books` also runs the computer's own check, as a dry run:

```
target/debug/seqpage import docs/spec/examples/proposals/10.11.21.1001.bob.seq --book docs/spec/examples/sources/10.11.21.book --by matthew --books docs/spec/examples/sources
```

Real output (shortened only where marked `...`):

```
{
  "booked": [
    7,
    8,
    9
  ],
  "dry_run": {
    "entries": [
      10
    ],
    "findings": [
      {
        "code": "finding",
        "detail": "page 1001: stamp says `state: draft` but its faces make it live",
        "rule": "R12"
      }
    ],
    "reasons": [],
    "status": "approved"
  },
  "findings": [
    ... five notes: the Bob page's older drafts have no recorded reason (R5),
        its stamp has no why-draft (R5), and it has no ## Registry card (R19) ...
  ],
  "note": "dry run only: nothing was written; the compute books an approved proposal",
  "ok": true,
  "page": "10.11.21.1001",
  "proposal": {
    "by": "matthew",
    "ops": [
      {
        "addr": "10.11.21.1001.06.01",
        "body": "## Session 2\nmodel: grok-bot\nwhy: the Bob test, session 2\n\nThe user asked \"what is my name\". The dictionary page 10.11.21.0012 lists `bob` -> 10.11.21.1001.01.bob, so the answer is the card: Bob.",
        "op": "put"
      }
    ]
  }
}
```

Read it as: the one `new` block became one request, the computer said `approved`, and **nothing was written**.

The notes are flags, not refusals. The Bob example was made before face 00's new layout, so it is missing the newer parts.

### 17.4 What happens if someone edits the past

I copied the cats file into `/tmp/try/` and changed line 43 from "likes" to "loves". That rewrites entry 10, which is already in the book. The check said:

```
{
  "ok": false,
  "errors": [
    {
      "line": 34,
      "code": "lineage",
      "axiom": "6",
      "rule": "seqpage 10",
      "detail": "@10 differs from the book's entry; the past is not rewritten (change it with a `new` block)"
    }
  ],
  "findings": []
}
```

So you cannot change the past by editing the file. You add a `new` block instead.

---

## 18. Rules, and where each comes from

| Rule, in plain words | Comes from |
|---|---|
| The book is the real copy. A .seq file is one page's view. | R3 |
| Import becomes a request in the queue. It never writes the book. | R3; seqpage.md section 10 |
| Out and back in loses nothing. | R3; seqpage.md section 1 |
| The name is the page address, then the title, then `.seq`. | seqpage.md section 2 |
| Line 1 is `seqpage 1`. | seqpage.md section 3 |
| Plain characters only (ASCII 0x20-0x7E plus newline). | R4; seqpage.md section 3 |
| Face 00 comes first. It is the registry. | R10; seqpage.md section 4 |
| The stamp lives in face 00. | R12 |
| Face 00 holds the stamp, the type and a registry. Registry fields depend on the type. | R19; face00.md |
| Page 0000 has only face 00. | R10; seqpage.md section 4.1 |
| Faces have no 00 or 99 slots. Counters run 01 to 98. | R9; seqpage.md section 5.2 |
| A draft is addressed `...FF.draft`, and exists only while drafting. | R8; seqpage.md section 5.1 |
| Every draft shows why it is a draft. | R5; seqpage.md section 5.1 |
| `:=` lines are worked out by the computer, checked, never imported. | seqpage.md section 7 |
| Body lines start with `|`. | seqpage.md section 6.4 |
| A booked block needs `at` and `by`. A `new` block may not have them. | seqpage.md section 6.2 |
| `new` blocks come after booked blocks. | axiom 6; seqpage.md section 6.1 |
| A booked block must match the book. The past is not rewritten. | axiom 6; seqpage.md section 10 |
| The history lists every booked write and only grows. | axiom 6; seqpage.md section 8 |
| The last line is `~ end`. | axiom 7; seqpage.md section 8 |
| No override pages while we build the app. | R21 |

---

## 19. Open questions

These are still open. Each is one plain line. You do not need to answer them now.

From `seqpage-QUESTIONS.md` (S questions):

- **S1** Lines with `:=` can change when the page changes. Is that OK, when all other lines only grow?
- **S2** Faces borrowed from the shelf, desk or kernel are not in the file. Should the file at least list where they come from?
- **S3** The lineage line shows only the address chain, not face 08 links. Is that enough for now?
- **S4** Spaces at the end of a body line are kept. Should they be made visible?
- **S5** Can you write a file by hand for a page that does not exist yet, to ask for it to be made?
- **S7** A draft's reason is kept in a `reason:` field on the write that opened it. Is that the right place?

From `face00.md` (F questions):

- **F1** On page 0000, is the stamp title the book's title, with no title in the address?
- **F2** Is the face list in face 00 written by hand, or worked out by the computer?
- **F3** Which face 00 problems should block a file, instead of just being flagged?
- **F4** The dictionary's 03.00 is called a "door" (R16), but faces have no door slots (R9). Which wins?
- **F5** Should lineage show the chain up, the trail of who allowed it, or both?
- **F6** What does a workflow page's approval record look like?
- **F7** What are the right owner kinds for a system page?
- **F9** What is the exact layout of face 00, to match the kernel?
- **F10** What type is page 0000, a continuation page, and the common questions list?
- **F11** What does the `code` page type mean, beyond "a page about code"?

Settled or parked (no answer needed):

- **S6** settled by R8 (drafts are addressed `FF.draft`).
- **S8** settled by R19 (what face 00 holds; detail in face00.md).
- **S9** settled by R12 and R19 (title, state and type live in face 00's stamp).
- **S10** and **F8** parked by R21 (no override pages for now).
- **F12** closed: the core's request now has a `reason` field (`crates/seqaddr-core/src/validate.rs`, field `reason` on `OpRequest`), so a request can carry why a draft was opened.

---

## 20. Where to look next

- The full spec: `docs/spec/seqpage.md`
- Face 00 in detail: `docs/spec/face00.md`
- The questions file: `docs/spec/seqpage-QUESTIONS.md`
- Your rulings: `docs/spec/DIRECTOR-RULINGS.md`
- The code: `crates/seqpage`
- The examples: `docs/spec/examples`
