# Write once: the spec

state: describes the code on branch build at 2166b46 (core-wf 2f66bda). Draft choices are not rulings. They wait for Matthew's K4 ruling.
made: Wed 18 Nov 2026, by Prima, because Matthew asked (t303u): "Make sure you are writing the spec documentation to go with the work. So I can understand what we did and have the why's in there."
page: 90.20.00.0001 "core: write once". The story of how it was built is in docs/journal/2026-11-18-write-once.md.
technical sources: docs/CONTRACT.md (the two 2026-11-18 delivery-id addenda, lines 54-79) and docs/BUILD-LOG.md (lines 452-486).

How to read the labels:
- A line in square brackets at the end of a point is a side label for engineers. It names the code or test (file:line).
- `7` means "not complete yet" (axiom 7). Here it marks a draft choice that waits for Matthew.
- File paths are short: `store.rs` is `crates/compute/src/store.rs`, `lib.rs` is `crates/compute/src/lib.rs`, `delivery.rs` is `crates/compute/tests/delivery.rs`.

---

## 1. What write once is

**A write that is sent twice is saved only once.**

The compute is the one program that owns the books. Every change goes through its one gate. (Side label: `POST /propose`.)

A book is an append-only log file. Each change is one book line. Lines are never edited or removed.

With write once, a sender can put an id on a write. (Side label: the id is called a *delivery id*, field `delivery_id`.)
- The same id with the same content gets the first answer back. Nothing new is written.
- The same id with other content is refused.
- A write with no id works as it always did.

Matthew already ruled on this. R37 item 2 says: "a delivery id can't change its content" (docs/spec/DIRECTOR-RULINGS.md:196). The detailed shape is the open question K4 (docs/design/CORE-AND-TOOLS-SPEC.md:949).

## 2. The problem it solves: the lost reply

Here is the story it fixes.
1. A tool sends a change.
2. The compute saves it in the book.
3. The reply back to the tool gets lost. Maybe the compute restarts, or the network drops.
4. The tool does not know if the change landed. So it sends it again.
5. Before write once, the compute saved it a second time. The page now held the same change twice.

That doubled change is a false step in the page's history. It breaks axiom 6 (lineage). The design spec listed this as the one hole that "fails today" (B6).

With write once, step 5 changes. The tool resends with the same id. The compute sees it already saved that write. It hands back the first answer and saves nothing new. This holds even after the compute restarts.

Codex (t292u) set the bar for "done": a committed write whose reply was lost can be resent after a restart without a second edit. That bar was met in pass 05.02. [test: delivery.rs:59, `lost_reply_survives_restart`]

## 3. How a client uses it

A client is any program that sends writes to the compute.

1. Make a new id for each new write. Any id up to 128 plain characters works. A random string is a good choice.
2. Put the same id on every op in the write. (An op is one change inside a write. One write can hold several ops.) [field: `delivery_id` on each op; `delivery-id` also works]
3. Send the write with your token, as usual.
4. If you get no reply, send the exact same write again, with the same id.
5. Read the answer:
   - **200**: done. If it was a resend, this is the first answer, and nothing new was written.
   - **409**: this id was already used for other content. The first write stands. Do not resend the other content. To save new content, use a new id. To get the first answer, resend the first content with the same id.
   - **400**: the id is bad (too long, a control character, or mixed ids). Fix it and send again. Nothing was saved.
   - **401**: your token is missing or wrong. Nothing was saved.
   - **422** with rule R4: the id has a non-plain character (not ASCII). Nothing was saved.

The answer codes are numbers the compute sends back. (Side label: HTTP status codes.)

[doc: CONTRACT.md:54-79; what to do on 409: CONTRACT.md:76]

## 4. What the compute promises, and why

Each rule below says what happens, then why.

### 4.1 Auth first

**What:** The compute checks the token before it looks at the id. A missing or wrong token gets 401. It is never treated as a resend. Nothing is saved.

**Why:** The id belongs to a writer, and only the token says who the writer is. So the token must be checked before the id can mean anything. Codex (t292u) asked for this order: "First authenticate the caller, then look up that writer's receipt."

[code: lib.rs:190-193 (`who`), then store.rs:748-755; test: delivery.rs:123. Note: this test also passes on the old code, because auth was already first. It is a guard test, kept on purpose.]

### 4.2 Ids are per writer

**What:** Each writer has their own ids. If Bob uses the same id as Alice, that is a new write for Bob. It is not a resend of Alice's.

**Why:** Two writers cannot see each other's ids. They could pick the same one by chance. One writer must never be able to block or read another's write. K4's proposed answer says the same: "An id belongs to one token name, so two writers cannot collide."

[code: store.rs:1131 (the index key is writer plus id); test: delivery.rs:150]

### 4.3 The receipt is kept in the book line, with the edit

**What:** When a write with an id is saved, the id is saved on the same book line as the change. There is no separate receipt file.

**Why:** Codex (t292u): "A crash must not leave a committed edit without the receipt needed to recognize a retry." If the receipt lived in a second file, a crash between the two saves could leave the change without its receipt. Then a resend would save it twice. One line, one save: the change and its receipt land together or not at all. It also needed no change to the book format beyond one optional field.

[code: seqaddr-core validate.rs:229-230 (id copied onto the entry), log.rs:177-179 (`Entry::delivery_id`); test: delivery.rs:24, book line checked at :50]

### 4.4 The same content gets the first answer back

**What:** Same writer, same id, same content: the compute hands back the first answer and saves nothing. (Side label: a *replay*, shown as `+0`, meaning zero new lines.)

**Why:** This is the whole point. The sender gets what it would have got the first time. The book stays true.

[code: store.rs:1128-1134 (`delivery_replay`); test: delivery.rs:24]

### 4.5 Other content under the same id is refused (409)

**What:** Same writer, same id, but different content: refused with 409. Nothing is saved. The answer names:
- `first_fingerprint`: a fingerprint of the first write's content;
- `first_book`: the book the first write went to.

The answer body is `{"status":"rejected","error":"conflict","rule":"K4","detail":...,"delivery_id":...,"first_fingerprint":...,"first_book":...,"reasons":[],"entries":[]}`.

**Why:** Matthew's ruling R37 item 2: "a delivery id can't change its content." If a resend could change the content, an id would not mean "this one write" any more. The fingerprint lets the sender see which content won, without a second read.

[code: store.rs:1135-1140; test: delivery.rs:212, before and after a restart]

### 4.6 How the fingerprint works

A fingerprint is a short code made from the content. The same content always gives the same code. Any change gives a different code. (Side label: a SHA-256 hash, written as 64 lowercase hex characters.)

How it is made:
1. Take the list of ops in the write.
2. Remove the id from each op. The id is not content.
3. Write the ops as JSON with the keys sorted.
4. Hash that text with SHA-256.

What this means:
- The layout of the request, the order of keys, and how characters are escaped do not change it.
- Any change to a value does change it. That includes spaces inside a body.
- The same body under two different ids gives two different writes.

**Why:** It has to tell "the same write, sent again" from "a different write". Sorting the keys means two programs that lay out JSON differently still match. Tester tried 19 different shapes of op and found no false 409, before or after a restart.

SHA-256 is written inside the compute (62 lines). The builder did not add a library, because that would change a file outside the grant (Cargo.lock).

[code: store.rs:1069-1085 (`proposal_content`, `proposal_fingerprint`), crates/compute/src/sha256.rs; after a restart the content is rebuilt from the book lines by `entry_as_op`, store.rs:1200]

### 4.7 The first write wins

**What:** If an id was somehow saved twice, the first one counts.
- Inside one book, the earlier line wins. Books only grow, so line order is the true order.
- Across two books, the earlier time stamp wins.
- If the two time stamps are equal, the lower book id wins.

**Why:** "First" must be something the compute can prove from what is on disk. Before pass 05.03, the lowest book id always won, even when it was written second. Tester showed that the first sender's resend then got 422 instead of its own 200 (Tester 05.02 follow-up 1). Two copies sent at the same instant cannot both be first: Tester sent 16 different bodies with one id at once, and 1 was saved, and 15 got 409.

[code: store.rs:1152-1170 (`rebuild_deliveries`, uses `log::check_time_order`); test: delivery.rs:88 (one book), :254 (two books)]

### 4.8 Refused answers leave the id free

**What:** If a write is refused (any answer that is not 200), the id is not used up. A later good write with that id is saved.

**Why:** A refusal saves nothing in the book. So after a restart, the compute would have no record of it. If it remembered refusals only in memory, it would answer one way before a restart and another way after. That would be worse than not remembering at all. Remembering them across restarts would need a new file next to the books, which the pass did not allow.

[code: store.rs:761-763 (only `code == 200` is remembered); test: delivery.rs:310 (a guard test: it passes on the old code too, by design)]

### 4.9 Limits on the id

**What:**
- Up to 128 characters. 129 or more is refused with 400.
- No control characters (such as a new line, a tab, or DEL). They get 400.
- Plain characters only (ASCII). A character like `é` gets 422 under rule R4. This check runs after the 400 checks.
- All ops in one write must carry the same id. Mixed ids get 400. An id on some ops and none on others also gets 400.
- Spaces at the start and end are trimmed off before the id is used.
- An empty id, or one that is only spaces, counts as no id.
- Ids are case-sensitive. `Id` and `id` are two different ids.

**Why:**
- The 128 cap and the control-character rule: the reason was not written down at the time (unknown). They came from Tester's 05.01 check, which sent a 200,000-character id and saw it accepted. Prima's reading now, not a record: a cap keeps memory bounded (see risk 3).
- R4 (plain characters) already applies to every field the compute stores. The id gets the same rule, so it gets the same 422 as any other field.
- One write is one unit. A half-tagged write cannot be resent whole, so it is refused.
- The 400 body is `{"status":"rejected","error":"invalid","detail":...,"reasons":[],"entries":[]}`. The three detail texts are in CONTRACT.md:75.

[code: store.rs:1025-1048 (`delivery_request_error`), seqaddr-core validate.rs:183 (R4); tests: delivery.rs:172, :292]

### 4.10 After a restart, the memory is rebuilt from the books

**What:** The compute keeps its list of ids in memory. When it starts, it reads every book and rebuilds that list from the ids on the book lines.

**Why:** Matthew's ruling R37 item 1: one append-only log is the only source of truth, so a fresh process can rebuild from it. No extra file is needed. This is what makes the lost-reply story work after a restart.

[code: store.rs:320 (called at start-up), :1152 (`rebuild_deliveries`), :1176 (`delivery_group`); test: delivery.rs:59]

### 4.11 The queue id comes back from `.queue`

**What:** Every answer carries a `queue_id` (for example `q5`), a number for that request. After a restart, a replay finds its original queue id again in the `.queue` file.

`.queue` is a file next to the books. The compute adds a record to it for every answer it gives.

If no matching record is found, the replay has no `queue_id`. That can happen if the compute crashed after saving the book line but before writing `.queue` (7).

400 and 409 answers, and replays, get no new queue id and no `.queue` record. They never reached the write rules.

**Why:** The first answer should come back as whole as we can honestly make it. `.queue` already keeps every record, so this needed no new file and no format change. A replay is not a new request, so it gets no new number.

[code: store.rs:1108-1122 (`queue_ids`), :1190-1192; the queue id is issued at :756-757; test: delivery.rs:328]

### 4.12 Why findings come back empty after a restart

**What:** Some answers carry `findings` (notes from the rule checks, R7). In the same session, a replay gives them back. After a restart, a replay gives `findings: []`, an empty list.

**Why:** Findings are worked out against the state of the world at the moment of the write. They are not saved anywhere on disk. Working them out again later could give a different answer. So the compute does not make them up. Axiom 4: never invent a reason so the work feels finished. Saving them would need a change to the book format or `.queue`, which needs a ruling.

What a client should know: after a restart, `book`, `status` and `entries` are the same as the first answer. `queue_id` is the same if `.queue` has it. `findings` is empty.

[code: store.rs:1192; test: delivery.rs:343]

### 4.13 What does not change

- A write with no id is saved exactly as before.
- The book file format gained one optional field. Nothing else changed.
- `seqaddr-core` (the shared library) only stores the id. Write once is enforced by the compute.

## 5. Limits and risks

These are known. None is fixed in code. Each is a note for Matthew, marked 7 in BUILD-LOG.md:476 and :484.

1. **A hand-edited book line is trusted.** If someone edits a book file by hand and puts an id on a line, the compute believes it at the next start. That line then replays as saved, and the real first content gets 409. There is no check that a line was not tampered with. (Side label: the v0 trust line.)
2. **A lost or forged `.queue`.** If `.queue` is lost, replays after a restart come back with no `queue_id`. The queue counter also starts again at q1 (that is older behaviour, not new). If someone forges a `.queue` line, a replay could carry the forged queue id.
3. **Memory grows with every id.** Each unique id costs about 6 KB of memory. There is no cap and nothing is ever dropped. Tester measured 20,000 ids taking the compute from 9.7 MB to 129 MB. Start-up with 50,000 ids took 295 ms against 107 ms with none.
4. **Long ids booked in pass 05.01.** Pass 05.01 had no length cap. Pass 05.02 added the 128 limit. The id check now runs before the replay. So a line saved under 05.01 with an id over 128 characters, or with a new line, can no longer be resent: the resend gets 400. Nobody has looked to see if such a line exists in a real book.
5. **Rebuilt content must match the request.** After a restart, the fingerprint is made from the book line. If some op shape is stored differently from how it was sent, an honest resend could get a false 409. Tester tried 19 shapes and found none. A replay after a promote was not tested (the promote was refused in the test setup).

Other open edges, not risks:
- The drift test (section 7) checks only some behaviours.
- Small doc nits, listed in section 7.

## 6. Draft choices waiting on Matthew's K4 ruling

The builders had to choose some details that K4 did not settle. Each one is marked 7 in BUILD-LOG as "draft choice, not a ruling; awaits Matthew's K4 ruling". The one complete list is BUILD-LOG.md:483.

Below, each choice has: what we do now, the other options, Prima's proposed answer, why, and an axioms check. **The options and proposals were written for this spec. They are not rulings, and Matthew may pick any option.**

**C1. The field name.**
- Now: `delivery_id`; `delivery-id` also works. [BUILD-LOG.md:455]
- Options: (a) keep; (b) a plainer name such as `write_id`.
- Proposed: (a) keep.
- Why: it matches how other fields work (`approved_by` / `approved-by`). Renaming later costs every client.
- Axioms: 2 (fractal) pass: same shape as other fields. 7 pass while marked.

**C2. Empty ids, trimming, and case.**
- Now: an empty or all-space id counts as no id. Spaces at the ends are trimmed. Case matters. [BUILD-LOG.md:455, :483]
- Options: (a) keep; (b) refuse empty or padded ids with 400; (c) fold case.
- Proposed: (a) keep.
- Why: a stray space should not make two different writes out of one. Folding case would quietly merge ids a client meant to keep apart.
- Axioms: 6 pass: no false second write. 4 pass: the why is written.

**C3. Ids are per writer.** [BUILD-LOG.md:459]
- Options: (a) per writer; (b) one shared space for everyone.
- Proposed: (a).
- Why: K4's own proposed answer says "an id belongs to one token name". A shared space would let one writer block another.
- Axioms: 1 (authority) pass: the token decides whose id it is.

**C4. Limits: 128 characters, no control characters (400), plain characters only (422 R4).** [BUILD-LOG.md:461, :483]
- Options: (a) keep; (b) a different cap; (c) no cap.
- Proposed: (a) keep.
- Why: a cap keeps memory bounded (see risk 3). R4 is the rule every other field already follows. (The original reason for 128 was not recorded.)
- Axioms: 2 pass: reuses R4, nothing new.

**C5. Mixed or partial ids in one write get 400.** [BUILD-LOG.md:461, :468]
- Options: (a) refuse; (b) treat the write as having no id.
- Proposed: (a) refuse.
- Why: one write is one unit. Silently dropping the id (option b, the 05.01 behaviour) would make a resend save twice.
- Axioms: 6 pass. 9 pass: Tester tried it.

**C6. Other content gets 409 `conflict`, rule K4, with `first_fingerprint` and `first_book`.** [BUILD-LOG.md:465, :470]
- Options: (a) keep 409 and these fields; (b) a different code (such as 422); (c) keep 409 and also add `first_entries`, so the client can find the first write without a read (the 05.03 builder's idea).
- Proposed: (a) now; (c) later if a client needs it.
- Why: 409 already means "conflict" in the compute (CONTRACT.md:42). The fields are enough to act on.
- Axioms: 8 (connection) pass: the refusal points back to the first write.

**C7. The fingerprint method.** [BUILD-LOG.md:465, :470, :483]
- Now: SHA-256 of the sorted-key JSON of the ops, id removed; full 64 hex characters; spaces in a body count.
- Options: (a) keep; (b) a looser match (for example, ignore spaces in bodies).
- Proposed: (a) keep.
- Why: a looser match could call two real different writes "the same". Exact is safer.
- Axioms: 6 pass: the history shows what was really sent.

**C8. The first write wins: earlier line in a book; earlier time across books; lower book id on a tie.** [BUILD-LOG.md:466]
- Options: (a) keep; (b) lowest book id always (the old behaviour).
- Proposed: (a) keep.
- Why: "first" should mean first in time. Option (b) broke the first sender's resend.
- Axioms: 6 pass.

**C9. Refused answers are not remembered.** [BUILD-LOG.md:469]
- Options: (a) id stays free; (b) remember refusals, which needs a new file next to the books.
- Proposed: (a).
- Why: it answers the same way before and after a restart, with no new file.
- Axioms: 4 pass: why recorded. 2 pass: no new file.

**C10. What a replay gives back after a restart.** [BUILD-LOG.md:460, :467, :470]
- Now: `book`, `status`, `entries` as before; `queue_id` from `.queue` if found; `findings` empty. Replays, 400 and 409 get no new queue id.
- Options: (a) keep; (b) save findings on the book line or in `.queue`, so the replay is whole (a format change).
- Proposed: (a) for now.
- Why: the parts a client needs to know "did it land, where" all come back. Findings cannot be rebuilt honestly.
- Axioms: 4 pass: nothing is made up. 7 pass: the gap is marked.

**C11. Long or new-line ids booked under 05.01.** [BUILD-LOG.md:476]
- Options, as BUILD-LOG lists them: (1) keep today's order: those lines cannot be resent (400); (2) look up the receipt first, then check a new id's shape, so such a line still replays; (3) wait, and decide only if such a line is found in a real book.
- Proposed: (3), plus one cheap read-only search of the real books. If none is found, (1).
- Why: 05.01's code was the newest on the work branch core-wf only from 12:32 to 12:48 PM EST (commits f363e28 to 800ea5e). Whether any real book was written by it is unknown. Option (2) moves the check order for a case that may not exist.
- Axioms: 9 pass: decide from evidence. 7 pass while marked.

## 7. How it is tested

- 11 tests in `crates/compute/tests/delivery.rs`. Each one that guards new behaviour was shown to fail on the code from before its own pass, for the expected reason. Two are guard tests that pass on old code by design: auth first (:123) and refused answers leave the id free (:310).
- 1 SHA-256 known-answer test in `sha256.rs`.
- 1 drift test, `crates/compute/tests/contract_delivery.rs:79`. It starts a real compute and checks that the codes written in CONTRACT.md (400, 409, 200, 401, the 128 cap) are what the compute really does. It fails if two pinned lines in the doc disagree.
- What the drift test does **not** catch (Tester 05.05): a wrong code in a bullet only, the 128 changed in the doc only, a wrong claim about findings, a dropped bullet, a bad cite, and code changes to trimming, the alias, mixed-id 400, or the control-character check.
- Whole suite: 291 tests pass (`cargo test -q -p compute -p seqaddr-core`, on core-wf 2f66bda).

Follow-ups and nits (none blocks the work):
- Extend the drift test to trimming, the alias, mixed-id 400 and control characters (Tester 05.05).
- The R4 rule name is inside `reasons[].rule`, not at the top of the answer (Tester 05.05).
- CONTRACT.md:74 cites store.rs:761; the queue id is issued at store.rs:756-757 (Tester 05.05).
- crates/seqaddr-core/API.md is older than this page in places: `counter_role` still lists Door/Item/Continuation, and 52 public items are not named (Tester 05.04).
- BUILD-LOG.md:454 has plan text that later passes changed. It is append-only, so it stays.
