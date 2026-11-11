# Read Path

by: claude-fable-5-2
date: 2026-11-11
state: draft
axioms: 9
refs: `kernel-notes.md` (the notes this draft is written from); `format.md`; `brands.md`; `seqAddr.md`; `decisions.md` A1.7, A1.8, C3, C8; `axioms/02.md`, `axioms/04.md`; `axioms/06.01.md`; `labs/notes/03.md`
why: the design says how a write is checked and stored. It does not say how a prompt becomes what the model is handed. Without that, the model needs history, and the end goal is a model that needs none.

Every choice here is **proposed**. Nothing is decided. The decisions for the Director are numbered R1-R9 in section 10.

---

## 1. What it is

The read path is everything the compute does between a person's prompt and the model's first word.

```
 person: prompt
      |
      v
 +---------------------------------------------+
 | compute                                     |
 |  1 receive   2 split   3 resolve words      |
 |  4 find pages   5 select   6 check   7 pack |
 +---------------------------------------------+
      |  pack (and nothing else)
      v
 model  --- may ask the compute to open a face --->  compute
      |
      v
 return  ->  the write side (format.md section 4)
```

Three rules hold the whole path:

1. **The model gets the pack and nothing else.** No history, no earlier turns. Continuity lives in the books and in the session note (step 7).
2. **The compute finds by written things only.** Words through the dictionary and concordance, pages through addresses and face 08 links. A match is never a connection (axiom 8).
3. **The pack is stored and shown.** A person can open any pack and see why the model was told what it was told.

## 2. Two kinds of turn

A prompt is either talk or work. Source: kernel law `0015.grammar`, `0053.emit`.

| | Talk | Work |
|---|---|---|
| How the compute knows | no `#NN` and no `>` | the person releases a numbered job: `#03 >run` |
| What the model may do | answer; add to the session note; propose jobs | the one job in the pack |
| What it may write | nothing itself. Note lines, job drafts and a new word meaning (C8.8) are handed to the compute | proposals inside the addresses the pack grants |
| Stored as | a session note entry | a face 05 counter: `draft`, `pack`, `open`, `return`, `review`, closed |

**A job seen in talk becomes a numbered draft.** The model does not start it. It returns a framed job (one sentence, where, stop, done), the compute stores it as `PPPP.05.NN.draft` and shows it as `#NN`, and the person releases it by number. Only then is a work pack built.

Why this shape:

- The compute never has to guess whether free text is a job. The person's release is the split.
- The frame faces the person before any work is done (axiom 5: know the aim before the work).
- It uses the counter tails as they are. Nothing new is needed in `seqAddr.md`.

A basic user need not type the marks: the app can show each job with a release button that sends the same thing.

`#NN` is a label for the session. The compute keeps the map from `#NN` to the full counter address, and the model states the full address back (A1.7).

## 3. The steps

| Step | What happens | Lead | Rule it rests on |
|---|---|---|---|
| 1 Receive | take the prompt and the session state | `3C` | format.md 1.2 |
| 2 Split | talk, or a release of `#NN` | `3CP` | kernel law `0015.grammar` |
| 3 Resolve words | each word to its brand, and to its place | `3C` | C8.8; kernel law `0013.concordance` |
| 4 Find pages | addresses, places, and one step along face 08 | `3C` | A1.8; axiom 8 |
| 5 Select | which faces and cards go in | `3C` | kernel law `0037.pack` |
| 6 Check | every address opens; no live conflict | `3C` | kernel law `0036.colab`, Check; axiom 1 |
| 7 Pack | build, store, state back, hand over | `3C` | format.md 3.3 |

Compute leads every step. That is the point: the path is exact, repeatable, and has no model in it to drift.

### Step 1. Receive

The compute holds, per session:

| State | Use |
|---|---|
| active book, active page or pages | expands short addresses (A1.6, A1.7) |
| the person's level and where it is held | sets what a pack may grant (C5.2a) |
| the brand last used for each word | C8.8 step 2 |
| the `#NN` map | answers by number |
| the session note counter | continuity between turns |

### Step 2. Split

- `#NN` with a `>` ask: a release. Go to a work pack for that counter.
- A bare `>`: malformed. Elevated to the person.
- Anything else: talk.

### Step 3. Resolve words

For each word in the prompt, two lookups. Each one walks book, shelf, desk, kernel (A1.8).

| Lookup | Gives | Source |
|---|---|---|
| Dictionary | the word's brands; one is chosen by C8.8: meters, then last used, then default, then ordinary meaning | `brands.md` |
| Concordance | the word's place: a page | kernel law `0013.concordance` |

- A word in neither index is left alone. That is most words, and it is not a failure.
- An address typed in the prompt is expanded and checked (A1.7). A title that does not match its stamp is elevated (A2.8).
- Each resolution is recorded as a `use` entry (format.md 3.3).

### Step 4. Find pages

The candidates, in this order:

1. Addresses the person typed.
2. The active page.
3. The page of each chosen brand card.
4. The place of each word found in the concordance.
5. One step along face 08 from each page above: its parent, what it continues from, and what it references.

Then, for each page, the rule that governs its kind, found by the lookup (A1.8).

Not done: no search by similarity, no scan of neighbours, no walk past one step. Kernel law `0008.map`: "Do not walk every reference as a parent, scan sideways to guess a missing source, or choose by numerical proximity."

### Step 5. Select

A pack is small on purpose. Kernel law `0036.colab`: "a cold model that is given the whole book answers from the average."

| In | Out |
|---|---|
| face 01 cards that a resolved word or the job names | face 04, unless asked for (below) |
| face 02 cards when the job is a process | faces 05 and 06 of other work |
| the contents list of each packed face | drafts, unless the job is that draft |
| face 08 rows used in step 4 | anything retired |

**The why on request.** A face 01 card is the packed form of its 04 card. When it is not enough, the model asks the compute for the why by card key (axiom 4, `axioms/04.md`). So the model has one tool: open a face or card by address. Reads are open (format.md 1.2). Every request is logged.

A size aim, not a quota (gravity): about five cards beyond the fixed parts.

### Step 6. Check

Before the pack leaves:

| Check | If it fails |
|---|---|
| every address in the pack opens | listed in the pack as missing, `7.8`. It is not repaired. |
| every cite parses | the pack is not sent; a finding is recorded |
| no packed card carries a recorded, unresolved conflict (a finding that a 01 card and its 04 disagree, or a difference from the parent with no named override) | **halt.** Raised to the person; no model call (axiom 1) |
| a work pack has one job, a stop and a done | pack fail. The counter stays `draft`. |
| a work pack's grant is inside the person's level and scope | pack fail |

The compute halts only on conflicts that are already recorded. It cannot judge whether two cards disagree in meaning. A conflict nobody has recorded is for the model to see and raise; in lab 03, models carrying the axioms halted on a live conflict and models without them acted first.

Kernel law `0036.colab`: a page is shipped, or the pack says it is withheld and why. "A halt on a file that is neither included nor withheld is a pack fail."

### Step 7. Pack

The compute builds the pack (section 4), then:

- **Stores it.** A work pack is the body of its counter, moved to `pack`. A talk pack is stored with the session (R6).
- **States back** to the person, in one or two lines: the brands assumed, the pages packed, what is missing.
- **Hands it** to the model.

The session note is what carries a conversation without history. Each return may add note lines; the compute appends them to the session's face 06 counter; the next pack carries that note. The model reads its own earlier notes, not its earlier words.

## 4. The pack

One Markdown page, in a fixed order. Order from kernel law `0037.pack`: "Door first. Then the axioms. Then the seat under test."

| Part | Holds | In a talk pack | In a work pack |
|---|---|---|---|
| Stamp | pack address, kind, date, pack-level cite | yes | yes |
| Door | active book and page with titles; the person's level here | yes | yes |
| Axioms | the nine packed cards from `axioms/02.md`, one line each | yes | yes |
| Words | each resolved word, its brand, how it was chosen | yes | yes |
| Pages | the selected cards, each under its full address and state | yes | yes |
| Missing | what could not be opened, as `7` chains | yes | yes |
| Note | the session note so far | yes | no (R7) |
| Prompt | the person's words, unchanged | yes | - |
| Job | one sentence; for, where, do, stop, done | - | yes |
| Grant | the addresses this pack may propose writes to | none | yes |
| Return | the shape the answer must take | talk shape | work shape |

Why the packed axiom cards and not the full text: in lab 02 the cards did at least as well (24 against 21 of 32).

**Cites are copied, not chosen.** Each packed card and stamp carries its own `axioms:` field. A job item takes the cite of its counter, else its band head's default lead. Lab 03: "The packed cards carry the concept; the cite carries the assignment."

### Return shapes

| Talk | Work |
|---|---|
| answer | did: each item, with the full address it touched |
| note: lines for the session note | blocked |
| jobs: any job seen, each framed | need |
| unprompted | unprompted |
| overflow | overflow |
| | proposals: the writes, for the write side |

Source: `axioms/04.md` axiom 5 (did, blocked, need, unprompted, overflow); kernel law `0038.return`.

### Skeleton

```
# Pack 10.10.11.1523.05.04
kind: work
date: 2026-11-11
axioms: 1.7.8

## Door
book: 10.10.11.user
page: 10.10.11.1523.timer
level: 01, held on book 10.10.11

## Axioms
<nine packed cards>

## Words
Ham: ham.002, a friend from work. chosen by: form (capital H)
timer: place 10.10.11.1523

## Pages
### 10.10.11.1523.01 (seated)
<cards>
### 10.10.11.1026.01.ham (seated)
<brand card>

## Missing
none

## Job
axioms: 5.4
Shorten the timer page's law face to what Ham asked for.
for: Ham's use of the timer
where: 10.10.11.1523.01
do: draft the shorter face through drafting
stop: if a rule has no why (4.7), or the change reaches another page
done: a draft at 10.10.11.1523.01.draft, every note struck, handed back for review

## Grant
10.10.11.1523.01.draft

## Return
did / blocked / need / unprompted / overflow / proposals
```

Book `10.10.11` and the `ham` brands are the example in `brands.md`. Page `1523.timer` is made up for this skeleton.

## 5. Worked example

The person types, with book `10.10.11` active: **"Ham wants the timer page shorter."**

1. **Receive.** Active book `10.10.11`, no active page.
2. **Split.** No `#`, no `>`: talk.
3. **Resolve.** `Ham`: three brands; the capital H matches only `ham.002`'s forms. `timer`: the concordance gives `10.10.11.1523`. The other words are in neither index.
4. **Find.** `10.10.11.1026` (the brand card's page) and `10.10.11.1523`. Face 08 of `1523` adds nothing.
5. **Select.** The `ham` brand card; the face 01 contents list and cards of `1523`.
6. **Check.** Everything opens. No conflict.
7. **Pack.** Talk pack. Stated back: "Ham, taken as ham.002, a friend from work. Timer, taken as page 10.10.11.1523."

The model answers, and returns one job: "Shorten the timer page's law face", framed. The compute stores it as `10.10.11.1523.05.04.draft` and shows it as `#01`.

The person types **`#01 >run`**. The compute builds the work pack in the skeleton above, moves the counter to `pack`, and hands it to a cold model.

If the person had typed "No, I meant the sandwich", that is a restatement: the `use` entry for `ham.002` is the one in question (C8.7).

## 6. What the compute keeps

All derived from the logs, none written by hand:

| Index | From |
|---|---|
| dictionary: word to brands | the `0012.03` index cards |
| concordance: word to place | R4 |
| links: page to page, both ways | face 08 rows (C4) |
| boards, contents lists | A4.4, C2 |

## 7. When it does not work

| Case | What the compute does |
|---|---|
| no word resolves and no page is active | a talk pack with door, axioms, note and prompt only. The state-back says nothing was found. |
| a word has several places | narrowed by the active book and page; a band set is one place; otherwise stated back as an assumption (R4) |
| a leading-dot address with several active pages | elevated (A1.6) |
| a required page is missing | listed under Missing; for a work pack, pack fail |
| two live claims conflict | halt, raised to the person |
| the pack is over its size aim | the lowest-ranked pages become contents lines only; the model can ask |

## 8. What this gives the drift check

The read path makes four things checkable on the way back, with no judgment:

1. **Addresses.** Every address in a return must exist, or be inside the grant.
2. **Grant.** Every proposal must be inside the grant. Anything else belongs under unprompted or overflow.
3. **Requests.** Every face the model asked to open is logged. Requests far from the job are a finding.
4. **Shape.** A return that is missing a part is not accepted.

Meaning is still not checked here. That is the trial's job (axiom 9).

## 9. Not in this draft

- The write side: `format.md` section 4.
- Section D: what happens after the return (review, failure, marks). Notes are in `kernel-notes.md` section 3.
- Transport: how a model client reaches the compute (`format.md` section 6).
- Homework before work (kernel law `0061.coldboot`): see R9.

## 10. Decisions for the Director

| | Decision | Recommended | Why |
|---|---|---|---|
| R1 | How is talk told from work? | The person releases a numbered job. Free text is always talk. | No guess by the compute, and the frame is seen before the work. |
| R2 | Does a model help with the split? | No. | A model in the read path can drift, and nothing would check it. |
| R3 | May similarity propose pages? | Not in the first build. | Axiom 8. If added later, it proposes only, and the pack marks such pages as unconnected. |
| R4 | Where does the concordance come from? | Derived by the compute from page titles, stamp keywords and card keys. | Hand-written indexes drift. The kernel's "one word, one place" cannot hold where titles repeat (A2.4), so a word may have several places. |
| R5 | How big is a pack? | An aim of about five cards beyond the fixed parts. | Gravity. Lab packs of this size worked. |
| R6 | Is the raw prompt kept? | Yes, with the pack that was built from it. | "Checkable by a person": a pack cannot be checked without the prompt it answers. |
| R7 | Does a work pack carry the session note? | No. Only what the job names. | Kernel law `0037.pack`: no face 06. A cold worker should not inherit the talk. |
| R8 | Where does the session note live? | Face 06 of the active book's page `0000`. | Fractal: the book's notes on the book's own page. Weak point: overflow at 98 sessions lands in the reserved range. |
| R9 | Homework before a work pack? | Not in the first build. | Worth a lab first: does it catch a model that did not read the pack? |

## 11. Open (`7`)

- Which page holds a job that concerns no existing page. (The same question as C8.10 for brand cards.)
- What a job item cites when neither its counter nor its band head has a cite.
- Whether a pack's grant is the "written permission" of axiom 7. `axioms/06.01.md` leaves this open; this draft assumes yes.
- How many requests a model may make in one turn.
- Levels `02` and `03`, which decide what a pack may grant to whom (C5.2).
