# Kernel trial (TRIAL-K): the axiom 9 hostile pass

Lane TRIAL-K, 2026-11-11. This pass looks at the kernel from a different view than its builder's. Findings only: nothing in `kernel/` or `books/` was changed.
Target: `kernel/` and `books/*.book` at commit `34d5c00`. The kernel was judged against `docs/spec/` and **Director ruling R1** (`docs/spec/DIRECTOR-RULINGS.md`, commit `5f279b7`). R1 says the full-zero sequence on any axis is the door, and the rulings govern over older spec wording.

## What held up (the checks passed)
- **Determinism:** I ran `node kernel/build.mjs` twice in two clean copies, and `diff -r` showed the books were identical. They were also identical to the committed `books/`. `--check` exits 0, with 70 findings and 0 errors.
- **Replay:** all 54 entries across the 4 books replay to exactly the 54 kernel/sample files. Each `addr` plus `tail` maps back to its file name, and each body matches its file byte for byte (ignoring trailing newlines). Headers are `{"seqbook":1,"address":...}`, `n` runs 1..k, and every entry has `n, at, by, op, addr`.
- **Copying:** every sentence in every 01/02 card body was found word for word somewhere in `docs/spec/`. The check is mechanical (`docs/trial/kernel-trial-copycheck.mjs`, sentence-level, after stripping markdown). No invented sentence was found in a 01/02 body. The 72 "not found" lines are all `7` hole text, session notes, or sample text (see 18).
- **Section numbers:** the dictionary sections are correct: `bob` goes in `03.14` (bi-bq) and `cats` in `03.16` (ca-cg), per `decisions.md:458-459`.
- **C3.2 inside one book:** every 01/02 card has a 04 card with `why:` and a body. 57 of them honestly carry `why: 4.7`.

## Findings

| Severity | Count |
|---|---|
| blocker | 2 |
| major | 8 |
| minor | 11 |

### 1. blocker: every face 00 is seated without Director approval
- **Evidence:** all 15 stamps are written bare, not as `.draft`. That is 9 kernel stamps (`kernel/00.00.00/00.00.00.PPPP.00.md`) and 6 sample stamps (`10.00.00.0000.00`, `10.11.00.0000.00`, `10.11.21.0000.00`, `.0012.00`, `.0056.00`, `.1001.00`). `kernel/build.mjs:74` turns a tail on face 00 into a build error. `MAP.md:11` logs this as a `7`, but the choice it made *is* to seat the faces.
- **What the spec says:**
  - `seqAddr.md:201`: "A face without counters is seated at `DD.SS.BB.PPPP.FF`. `FF.draft` is its unseated draft."
  - `seqAddr.md:283` grammar: `face-part = face [counter] [tail]`, so `draft` is allowed on any face, 00 included.
  - `seqAddr.md:126`: there is also a page tail, `PPPP.draft`.
  - `seqAddr.md:164`: "A new page may start with only drafts."
- **Why it matters:** a `state: draft` line inside a seated file doesn't make the file unseated. The address decides that (axiom 1: "location, state, and a lawful connection decide what is live").

### 2. blocker: a card key is a reserved tail word
- **Evidence:** `kernel/00.00.00/00.00.00.0057.01.draft.md:105` and `00.00.00.0057.04.draft.md:59` both use `## Review`, which gives the key `review`.
- **What the spec says:** `seqAddr.md:280` reads `card = LOWER ...   ; not a tail word`, and `:283` lists `review` as a tail. `seqAddr.md:113` adds: "Tail words are reserved".
- **Why it matters:** `00.00.00.0057.01.review` would parse as a `review` tail on face 01. That tail is illegal without a counter (`seqAddr.md:287`), so the card can't be addressed. `build.mjs` doesn't check card keys against the grammar.

### 3. major: the kernel still uses wording that ruling R1 replaced
- **Evidence:** the kernel faces use "identity" 40 times in 9 files, "board" 19 times in 9 files, and "owner of the level above" once (`0051.04.draft.md:140`). Several 01 law cards are named for the old terms: `0051.01:83` Identity Page, `0051.01:97` Owner Rule, `0052.01:1` Face Identity, and `0052.01:79` Counted Faces ("board"). The builder's messages do the same at `build.mjs:71,88,96,121`. `CONFLICTS.md` K01 is still listed as open.
- **What the spec says:** `DIRECTOR-RULINGS.md:5`: "Older spec wording that calls it owner, identity, or board refers to this same location; use the word 'door'."
- **What's needed:** K01 should be marked as resolved by R1. The faces must change by drafting notes and merges (`drafting.md:11-18`), not by a rewrite.
- **Note:** R1 renames the location. It doesn't say whether the board's job (listing counters and their tails) or the stamp's job moves. Don't infer that (`7`).

### 4. major: the Bob test's session 2 claim isn't supported
- **Evidence:** `kernel/samples/10.11.21/10.11.21.1001.04.draft.md:5` says: "Session 2, 'what is my name', is answered from this card through the dictionary entry `bob`".
- **Why it fails:** none of the words what, is, my or name is in the dictionary. Only `bob` (`0012.03.14`) and `cats` (`0012.03.16`) are. No meters are written, and `MAP.md:53` says so.
- **What the spec says:** `decisions.md:496-503` (C8.8) resolves a word that is *typed*. "what is my name" never types `bob`, so this path to the card is invented. Following axiom 7, it should stay a `7` hole: there is no route from "name" to `bob.001`.

### 5. major: the inheritance sample depends on drafts being live, and the spec says they aren't
- **Evidence:**
  - `MAP.md:52` presents faces 01/02/06 of `10.11.21.0056` as "found at `00.00.00.0056`".
  - Every kernel face is a draft, and `MAP.md:54` (hole 12) logs whether a draft is found as a `7`.
- **What the spec says:** `seqAddr.md:133`: "`draft` | being written; not active". Read literally, today's kernel contributes nothing to any lookup, so every inherited face resolves to missing. The sample shows the opposite as if it were settled.

### 6. major: a face-level override breaks C3.2 on the resolved page
- **Evidence:** `10.11.21.0056.04.draft.md` holds only the `never-from-memory` card. Under the first-match lookup (`seqAddr.md:104`), the local 04 face wins outright. That hides the kernel's 04 cards for `new-face`, `exceptions` (01) and `drafting-ops` (02).
- **Why it fails:** the resolved page now has 01/02 cards with no 04 card, which C3.2 makes a hard error (`seqAddr.md:184`). `build.mjs:99-101` checks C3.2 only inside one book, so it can't see this.
- **Also missing:** axiom 2 needs "a named override, approved by the authority above it". There is none, and `MAP.md:52` logs it as `7`. Whether lookup works per face or per card is not stated (`7`); this sample assumes per face.

### 7. major: many whys lack their source line, and some don't belong to their card
- **Evidence:** 27 `why:` lines are copied word for word, but from a line the card doesn't cite. About 20 say only "why from docs/spec/decisions.md", with no line number. Examples are `0051.04.draft.md:19,58,70,82,107,113,153,179,185,211` and `0057.04.draft.md:7,14,20,40`. This breaks axiom 6 ("Lineage is kept with the piece") and 8.
- **Whys borrowed or scoped wrongly** (axiom 4: "Never invent a reason"):
  - `0051.04:113` `which-pages-need-a-title`: "their number is already their name". That explains why pages 0001-0999 *may* have a title, not the card's rule that pages 1000 and up *must*.
  - `0057.04:40` `risk-and-governing-targets` borrows S02's evidence why (`decisions.md:628`). The same why also sits on `return-shape`.
  - `0051.04:70` `finding`: "This matters for the inherited reserved pages". That's a note on relevance, not a reason.
  - `0000.04.draft.md:3` uses the motto from `kernel-design.md:13`, a line it doesn't cite. That file calls itself "Proposed architecture — for refinement, not promoted law" (`kernel-design.md:4`).

### 8. major: draft faces are booked in a shape that can't hold both the seated face and its draft
- **Evidence:** in `books/*.book`, a draft face is written as `"addr":"...PPPP.01","tail":"draft"`.
- **Why it fails:** `drafting.md:11,28` copies the seated face *to* `FF.draft`, so `FF` and `FF.draft` exist at the same time. Replay keyed by `addr` would merge them. `format.md:120-122` shows `tail` only on counters, and the app mock keys `"01.draft"` (BUILD-LOG `[APP]`). The spec doesn't settle this, so it needs a `7` in BUILD-LOG, and there isn't one.

### 9. major: 01 cards carry no source in the book
- **Evidence:** no 01 card has a `source:` field, so its lineage lives only in `kernel/MAP.md`. That file isn't part of any `.book`.
- **Why it matters:** once a book is exported ("Exporting a book means copying its file", `format.md:76`), the 01 lineage is lost. Axiom 6 says "Lineage is kept with the piece." By contrast, the 02 and 04 cards do carry `source:`.

### 10. major: the books would fail the compute's own checks
- **Evidence:** a byte-for-byte replay works, but `format.md:119` (face 00 plus a content face) and `format.md:123` ("identity page first, board before counters") would reject:
  - 3 identity pages with no content face (`10.00.00.0000`, `10.11.00.0000`, `10.11.21.0000`);
  - 10 counters with no board (8 kernel `06.01`, sample `03.14` and `03.16`).
- These are logged as K02/K10. The point here is that `books/` isn't yet a legal seed for a compute that validates.

### 11. minor: K12 cites the wrong line
`CONFLICTS.md:78` cites `decisions.md:611` for "Where a return lives: on its counter". The text is at `decisions.md:612`. Every other `file:line — "quote"` in CONFLICTS checked out exactly.

### 12. minor: missed conflict: "door" means something else in `.002`
`workflow-loop.md:52` says "`N?00` is the door of each hundred-page band" (also `:42`, "doors band"). R1 makes "door" the full-zero sequence only, and `0400` isn't all zeros. This should be raised, not resolved.

### 13. minor: missed conflict: does page 0000 have a title?
`seqAddr.md:115` says "Page 0000 has none", but `seqAddr.md:56` says "page 0000, whose stamp holds its title". `decisions.md:132` reconciles them ("it holds the book's title in its stamp"), but `seqAddr.md` drops that part. The kernel stamp `00.00.00.0000.00.md:3` carries `title: kernel`.

### 14. minor: missed conflict: are drafts live?
`seqAddr.md:133` ("draft … not active") clashes with `seqAddr.md:164` ("Draft faces count … A new page may start with only drafts") and with live inheritance (`decisions.md:128`). MAP raises this as hole 12, but CONFLICTS doesn't list it, and it decides finding 5.

### 15. minor: K02 leaves out a quote from the same file
`format.md` contradicts itself: `:102` says boards are "never written as entries", while `:123` requires "board before counters". K02 cites only `:102`.

### 16. minor: a derived menu is written as a card
`00.00.00.0050.03.draft.md:1-4` writes a `Menu` card (as hole text) for content the spec calls derived. `drafting.md:40` says derived content is "calculated and never drafted", and `format.md:102` says derived lists are "never written as entries". A hole with nothing requiring it should stay empty (Axioms 7), not become a written card.

### 17. minor: some `.003` cards get their 04 text from `.002` notes
- `0057.04` `roles` uses the one-line read-back at `workflow-loop.002-notes.md:48` as its "full explanation".
- `bound-bands` cites `workflow-loop.002-notes.md:40`.
- CONFLICTS W01-W15 show that `.002` was replaced in places. And a one-line read-back isn't written "for a person" (C3.1).

### 18. minor: the sample override quotes chat, not the spec
`10.11.21.0056.04.draft.md:5`: "Copy it then update don't create from memory." These are the Director's chat words, which are true, but no `docs/spec` line holds them. Check (1), "copied from the cited spec line", can't be verified from the repo. Put it in DIRECTOR-RULINGS, or cite where it came from.

### 19. minor: the axioms' 04 whys describe the axioms rather than give reasons
`0050.04` uses the "Gives" column of `Design.md:57-65` as the why ("the paths that are legal"). Those lines describe what each axiom provides. The axioms' own recorded why, `decisions.md:548` ("a model receives a large concept in a very small package"), isn't used.

### 20. minor: the shelf and desk steps of the lookup are never tested
The `10.11.00` and `10.00.00` samples are identity-only. So nothing shows that a shelf face beats the kernel, or a desk face beats the kernel. Only book → kernel is exercised, against `seqAddr.md:101`.

### 21. minor: gaps in the builder's checks
`build.mjs` doesn't check:
- card keys against the grammar (finding 2);
- C3.2 across inheritance (finding 6);
- whether a `why:` comes from a cited line (finding 7).

It treats every `why:` other than `4.7` as valid.

## Method
- The copy check is `docs/trial/kernel-trial-copycheck.mjs`. It splits every card body into sentences and searches for each one in the lines its card cites (from `MAP.md` and `source:`), then in all of `docs/spec/`.
- The CONFLICTS quotes were checked line by line.
- Replay was checked by mapping each entry to its file. Determinism was checked by two clean builds and `diff -r`.

## Fix pass (lane KERNEL, 2026-11-11)

By the kernel's maker, so it doesn't count as a trial. Every fix below still needs its own hostile pass (axiom 9). Rulings applied: R1 (door) and R2 (build-stage seating). Open items are in `kernel/QUESTIONS.md`; none were answered.

| # | Finding | Result | What and why |
|---|---|---|---|
| 1 | door faces seated | fixed | All 15 door faces are now `00.draft` (`seqAddr.md:201,283`). The builder allows `draft` on face 00. Stamp state is raised as Q8. |
| 2 | `review` card key | fixed | Heading is now `Review (filled)`, the `.003` section heading (`workflow-loop.003.md:195`), giving key `review-filled`. The builder now rejects keys that break `seqAddr.md:280` or are tail words. |
| 3 | R1 wording | fixed | Copied text says "door" in the zero-sequence sense only. Each change is a merge line in the page's 06.01 note. Headings renamed, builder messages say door, K01 marked resolved by R1. Whether the counter list stays the door's job is raised as Q5. |
| 4 | Bob session 2 | fixed + raised | Invented route removed. The card now says `7`: no route from "what is my name" to `bob`. Raised as Q7. |
| 5 | drafts treated as active | fixed + raised | The builder's lookup treats drafts as not active (`seqAddr.md:133`) and prints each missing lookup. MAP says the sample resolves to missing today. Raised as Q2 (CONFLICTS K18). |
| 6 | override breaks C3.2 | raised | The builder now checks C3.2 across the lookup and prints the 3 hidden 04 cards. Per face or per card, and the named override form, are raised as Q3. |
| 7 | whys without line / borrowed | fixed | Every `why:` cites `docs/spec/FILE:LINE`, and the builder checks the text is on that line. The borrowed whys on `which-pages-need-a-title`, `finding` and `risk-and-governing-targets` are now `4.7`. The kernel 0000 why cites `kernel-design.md:13` and notes its proposed status. |
| 8 | draft entry shape | raised | Spec silent. Shape kept so other lanes are not broken. Logged `7` in BUILD-LOG and raised as Q4. |
| 9 | 01 lineage not in book | fixed | Each 04 card's `source:` now names its 01/02 spec lines, so the lineage travels in the `.book`. |
| 10 | books fail compute checks | raised | Doors not written and door pages without content are spec conflicts (K02, K10). Raised as Q5 and Q6. Still builder findings. |
| 11 | K12 wrong line | fixed | Now `decisions.md:612`. The same wrong line was also used as the 04 text of `return-placement`; fixed too. |
| 12 | "door" in `.002` | raised | Added as CONFLICTS K16 and Q9. |
| 13 | page 0000 title | fixed (listed) | Added as K17. The kernel stamp follows `decisions.md:132`. |
| 14 | drafts live | fixed (listed) | Added as K18 and linked to Q2. |
| 15 | K02 missing quote | fixed | Added `format.md:123`. |
| 16 | derived Menu card | fixed | Removed from 0050.03. |
| 17 | `.002` notes as 04 text | fixed | `roles` and `bound-bands` 04 bodies are now `7` holes. |
| 18 | chat quote | fixed | The card's `source:` names Prima chat t42u and says it is not in docs/spec. Adding it to DIRECTOR-RULINGS is outside this lane. |
| 19 | axioms whys | fixed | All nine now use `decisions.md:548`. |
| 20 | shelf/desk lookup untested | left | It would need sample content the spec doesn't give. With drafts not found it would show nothing anyway. |
| 21 | builder gaps | fixed | Added checks for card key grammar, a `why:` on its cited line, C3.2 across the lookup (finding), and `approved-by` on seated faces. |

**R2:** no face qualifies yet. Each one has an open question or an unresolved finding (MAP.md "Seated under R2"). Nothing was seated.
