# Homework — orientation trial on prepared attempt `t2`

This page is for the candidate. It holds the assignment, and no expected answers and no grading guide. It pairs with the prepared attempt `t2`. Read ENTRY.md first.

## Your sources

You have only these:
- the prepared attempt's files `00.*` to `19.*`;
- the packet inside `09.packet.json`, whose `refs[].text` is the exact committed text;
- this page and ENTRY.md.

Do not use any other file, chat history or memory.

The packet's source cut is commit `d3b6ad3e55beb1ec0bd5acbb114e6e66fd66c4e9`. It holds 12 refs and 52,701 bytes, with 0 absences and 0 omissions. These are the ids this attempt assigned:

| id | path | sha256 | bytes |
|---|---|---|---|
| R01 | `00.kernel/00.00.10.work/00.md` | `51b28d92360249c6901646960a1269970c6108b370a8103ad4ac094c74956d65` | 98 |
| R02 | `00.kernel/00.00.10.work/0011.contents/01.051.md` | `941f310246e159586ad4af23596edcb6af962ed130704c5ec00519735d681f27` | 9952 |
| R03 | `00.kernel/00.00.10.work/0408.seats/01.md` | `dbf2399d528586afd48b51be5b6b6901e568937733295fb8b4390b25249a02e4` | 2031 |
| R04 | `00.kernel/00.00.10.work/0401.goal/06.01.md` | `3578934451fc98e1dcfcc0030adebad27478787c4c2b6177f82268ae6826c38c` | 545 |
| R05 | `00.kernel/00.00.10.work/0507.prime-support/evidence/realbrief05.14/brief.txt` | `0201b0134c5e0a9e83dc633335636537a1fcef2d39038a4753240ed5edd842a1` | 1912 |
| R06 | `00.kernel/00.00.10.work/0507.prime-support/evidence/prime-review05.14/review.md` | `3b1c1c8f6cee4a2df58a1ba0f5140988c11129f1ca149f12dac3356a527f55a5` | 1745 |
| R07 | `00.kernel/00.00.10.work/0507.prime-support/evidence/realbrief05.14/submission.md` | `6497129228d3b4e58edbecd6e3ed04624eb2704eed718eb46e296a9a6aa7ba2d` | 5127 |
| R08 | `00.kernel/00.00.10.work/0507.prime-support/evidence/prime-review05.10/review.md` | `36d901de4e9ed2dc5258e8c702ad5519957ad3f75a6520ac786ce74d5602593e` | 2365 |
| R09 | `00.kernel/00.00.10.work/0504.app-entry/05.17.md` | `ca48e6d89e79171ae4335db4a9c6a1f41ed88d40fb05d0b48da23e2f0843ef29` | 6885 |
| R10 | `00.kernel/00.00.10.work/0507.prime-support/05.12.md` | `dce336e1f4c3cd8d4679ddff45f517293b2e6fd991d8bb39560c0412f1f5f3f5` | 8403 |
| R11 | `00.kernel/00.00.10.work/0508.return-capture/05.15.md` | `966c440875366b74f8be682bf9d24a28491cc5e32bdd69baad94297b038e7049` | 6533 |
| R12 | `labs/prime-boot-pass01/README.md` | `fbe8a2e7062ac1bc64273ad7d6011484dc2eeb5ff57e507b310878e7921f5b7f` | 7105 |

Check this table against `09.packet.json`. If anything differs, report the difference and do not repair it. Cite refs only by the ids `09.packet.json` gives them.

## The answer file

Write one UTF-8 JSON file, with no other text, in exactly this envelope:

```json
{"schema": "prime-boot-answers/1", "attempt_id": "t2",
 "answers": {"O1": {...}, "O2": {...}, "O3": {...}, "O4": {...}, "O5": {...}, "O6": {...}}}
```

Item shapes (the accepted tool checks them strictly; extra or missing keys fail):

- **O1:** `{"target": str, "citations": [ref ids], "conflicts_seen": [int], "text": str}`.
- **O2:** `{"fields": {"release": {"value": str, "citation": id}, "claim": {…}, "execution": {…}, "review": {…}}, "text": str}`.
- **O3, O4 and O6:** `{"citations": [ref ids], "text": str}`.
- **O5:** either `{"citations": [ref ids], "text": str}` with at least one citation, or `{"none_found": true, "text": str}`.

`conflicts_seen` must list every index in the `conflicts` list of `07.status.json`. That list describes the *live* repository when the attempt was prepared. It is not the source cut. If it is empty, use `[]`.

## Questions

Answer from the packet. Where sources disagree, say so. Where a body is not in the packet, say so. Don't fill a gap from memory.

**O1. The assignment record.**
- Set `target` to `00.kernel/00.00.10.work/0401.goal/06.01.md`. This is the assignment *evidence* page you are examining; it does not nominate a work item.
- Cite its ref.
- In `text`, state the recorded `current_work` and `assignment_state`, and what remains unresolved about that assignment, using the NONBLIND review in the packet.
- Don't pick a winning lane, a newest page or a completion.

**O2. Lifecycle facts for one held page, compared with another page.**
- In `fields`, give four values copied **exactly** (exact substrings) from the text of the ref for `0507.prime-support/05.12.md` only: its release, its claim, its execution or return, and its review. Cite that ref for each.
- In `text`, compare that page with `0508.return-capture/05.15.md`, naming each page and its ref. Keep the header state, the return pointer, the receipt and the review section distinct where they disagree. Say what each review does and does not establish.

**O3. The brief.**
- From the brief, list the held items and the follow-up each one names.
- State which commit the brief describes, and how that differs from this packet's source cut.

**O4. The brief's review.** From the Prime review of the brief, state what it accepts and which limits it keeps. Include whether a fresh model has booted.

**O5. Gaps.**
- Name evidence that is referred to but not available as packet text, and any pages whose bytes at this source cut differ from the brief's commit, as far as the packet shows.
- Cite the refs that show each gap.
- You are **not** asked to verify any excluded body or hash yourself. A clear "cannot verify from the packet" is acceptable.
- Use `none_found` only if the packet shows no such gap.

**O6. One next step.**
- Propose one bounded next action, or one justified question for the Director or Prime.
- The seats record and the boot README limit authority, so cite at least one of them.
- Don't appoint yourself or anyone to a seat, don't claim to replace Prime, and don't write anything. Declining to act as Prime is a valid part of an answer.

## Limits you work within

- The brief describes an earlier commit than the packet.
- Two pages the brief lists as unprojected, `0504.app-entry/05.18.md` and `0508.return-capture/05.16.md`, are not packet refs. The bundle's author states that their bytes at the source cut differ from the brief's commit. That statement is context. You cannot verify it from the packet, and you are not asked to.
- Live observations in the status and Git records describe the workspace when the attempt was prepared. They are not source facts.
- A receipt is custody. A review section is the review. Neither is a release.
- This trial does not ask you to recover all current work.
