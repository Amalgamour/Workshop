# Axioms

Redrafted from the kernel's approved axioms page (`00.00.00.syntax`, `00.axioms`, faces 01-04, approved 2026-10-12). The nine keep their numbers and order: chains cite them by number, so the numbers are the identity. The wording is the original, tightened only where it repeated. Proposed changes are in the notes at the end and are **not** applied.

## The nine

1. **Authority.** Written is not the lock. Location, state, and a lawful tie decide. Between a live face and a copy, the record decides. Two live claims on one title, and no twin, halt. Do not choose. A draft, a note, or a remembered copy does not outrank the live record.
   *Why: an act with no one governing it drifts.*

2. **Fractal.** Inherit the agreement. Write the difference. A contradiction needs a named and approved override. If no lawful source exists, it stays missing. Fractal is not a mirror. The shape is intentional, so a hole on this page can be uncovered from the same shape on other pages. One damaged page does not rebuild itself. The book is the rebuild. Do not fill the hole from memory.
   *Why: the same shape at a smaller scale makes the work understandable. The infinite between nothing and the whole becomes sectors you can work.*

3. **Dance.** Human directs. Model reasons. Compute maintains. They are not the same job. Compute scans the name. The model climbs the rank. The person reads the title. Talk is not work. A menu points. It does not become law. Sync does not grant permission.
   *Why: a person, a model, or compute alone is not the best. The dance is how the three work as one.*

4. **Why.** Recover the cause in proportion to the cost of being wrong. Unknown stays unknown. Do not invent a reason so the page feels finished.
   *Why: a success you cannot explain is only an answer, and an answer can rot.*

5. **Narrow.** Narrow before spending the work. The work is the target, the next act, the hold, the allowed, and the done. Not the desk. Narrow is the size of the work, not a clock.
   *Why: a narrow path makes the work clear.*

6. **Lineage.** Change only through a visible transition: what changed, why, and what now governs. Do not rewrite notes as history. A change checks its twin in the same change. That check is not permission to rewrite the twin.
   *Why: this is how understanding is built over time.*

7. **Missing.** `7` means the piece is not complete. Do not invent the missing part. A bare `7` warns and does not name the hole. A chain such as `1.7` means the law of that page is missing a piece: read what is written and work around the hole. A page that works and is not finished carries `7`. A folder named `reserved` is left unless there is a reason to open it. A hole nothing requires stays empty; empty is a header and a why. Absence does not start a search. A required absence is a defect: report it, and draft from the governing face, marked draft. Never from the absence. Never from memory.
   *Why: a hole is not a wrong. Its time of understanding has not come yet.*

8. **Record.** The file governs. A carried sentence is not the file. Memory may hold the form and still not govern. Reopen `1.7.8` before a write. If the file and the sentence disagree, reopen the axiom. If the number cannot be opened, that piece stays missing.
   *Why: without the file the intelligence evaporates. Memory does not keep it.*

9. **Hostile.** Open the predecessor before replacing. The predecessor is the last thing, before the one being replaced, that held this title and did this job. A retired predecessor is opened read-only and cited as `FF.VVV.09`. Never act on it. The archive is everything else. New, old, or biggest is not proof. Exploration is cheap. Promotion is hard. Self-attack does not clear the lock. `9` means do not trust it as it stands. A draft that is not ready carries `9`.
   *Why: enthusiasm cannot replace a critical look. Bad ideas die under that look. Good ones become clear.*

**Cold set:** `1.7.8`. Reopen authority, missing, and record before a write.

## Chains

- A one-digit mark is an axiom. It is not an axis; an axis is two digits at minimum. Axiom `1` is not face `01`.
- A chain is a key: the posture the next sitting reads. It is not a set, and it is not permission.
- A dot orders axioms inside one piece. Left is first. `2.3` (fractal, then dance) is not `3.2`.
- A later axiom refines. It does not replace. Primary identifies, secondary composes, tertiary qualifies. In `1.7.9` the `9` does not erase the `1`.
- A comma splits pieces. `1.3.9` is one piece; `1,3,9` is three. `1,1.2` is two pieces: read the first, then the second.
- A cite is an intent key. It runs nothing, permits nothing, and does not paste the box.
- The chain carries the constraint. The why carries the job. A piece stands or fails alone; a chain stands or fails whole.
- Do not stamp all nine on every page.

## Hats and marks

- **Director** holds intent, approval, and lock. **Prime** walks, drafts, and signs after the walk. **Worker** runs one ticket. **Compute** maintains.
- A face moves draft, then signed, then approved, then lock. Reading a signed file to orient is lawful. Acting on its permissions needs approved.
- Unknown, draft, parked, retired, and conflicting are states. Permission is never inferred.

## Twin

A twin is not equality. It names the two sides, which side governs which dimension, why both exist, and what must agree. Face 01 governs; face 04 is the person face, carries the law in readable form, and adds no law. A note lives on 06, a ticket on 05: an important ticket needs a recoverable note, and a note does not mint a ticket. Face 08 is the map: it names where a design is found and does not govern.

---

## Notes: what I want to change (proposed, not applied)

Each note says what, why, and which axiom it serves. None of these change the nine.

1. **C5 authority precedence: take it from axiom 2.** A lower level may differ from a higher one only through a named and approved override. Replace "nearest level wins" in the C5 discussion with this. The lookup order (book, shelf, desk, kernel) still finds things; axiom 2 decides whether a found difference is lawful. [2]
2. **Add marks to the design.** Our tails carry `draft` and `retired` only, and D0's `promote` jumps from draft to seated. Add signed, approved, and lock, and tie `promote` to approved. This belongs in section D. [1, 6, 9]
3. **Add hats to the design.** Director, Prime, Worker, and Compute map onto our user, models, and compute, but the design has no roles. Section D needs them to say who may sign, approve, and lock. [3]
4. **Twin rule into C3.** Add: "If face 04 disagrees with face 01, face 04 is wrong. Face 04 adds no law." [2, twin]
5. **`axioms:` as a card field.** Cards cite chains (`axioms: 1.2`). Add `axioms` as an optional field on every card type (C8.9) and on the page stamp. [chains]
6. **Version citations vs brands.** `FF.VVV.09` puts a 3-digit version right after a face. C8.2 says a 3-digit group is a brand. Proposed: position decides. Three digits after a face are a version; three digits after a card key are a brand. The trailing `09` needs its meaning recorded (retired, read-only). [8, 9]
7. **Chains are not addresses.** Exact widths (A1.5) already make `1.7.8` impossible to read as an address. Say so in the grammar so a parser treats one-digit groups as a chain. [chains]
8. **Page types vs "TT is not an axis".** Our page `type` is a stamp field, not an axis, so it keeps the rule. The original says type is the page keyword; confirm whether the keyword and the stamp `type` are one thing or two. [2]
9. **Where this page lives.** The original seat is `00.axioms` in `00.00.00.syntax`. In the new layout a page needs four digits. Proposed: a reserved kernel page in `0001-0009`, beside `0007.reserved`. Needs your choice of number. [1]
10. **Per-face headers move.** The original repeats version, authorization, and state on each face. In the new design the page stamp lives on face 00 and versions come from the log, so these headers are not repeated. [8]
11. **My earlier twelve.** Their design rules stay where they belong: position and exact widths in `seqAddr.md`; derived lists and back-links in `decisions.md`. They are not axioms.
