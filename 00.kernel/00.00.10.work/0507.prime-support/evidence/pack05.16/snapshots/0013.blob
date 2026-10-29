# Homework for the fresh session

Date: 2026-10-28. This page is the model-facing assignment for one later session. It contains no expected answers and no grading guide. The session that wrote it did not call a model and did not boot a Prime.

You receive an external attempt directory and the committed sources listed below. The attempt’s `09.packet.json` assigns each ref an id. Cite those ids. A citation is valid only when it is an id written in that attempt. Do not reuse ref names from any earlier plan. If a path below has a different id in the attempt, cite the attempt.

The snapshot commit is `d3b6ad3e55beb1ec0bd5acbb114e6e66fd66c4e9`. This session asks you to orient that snapshot. It does not ask you to recover every later live page.

## Sources

The calculated order for the request in the builder’s plan is below. Confirm each blob’s SHA-256 and length against the attempt. Report a mismatch. Do not repair it.

| Path | SHA-256 | Bytes |
|---|---|---|
| `00.kernel/00.00.10.work/00.md` | `51b28d92360249c6901646960a1269970c6108b370a8103ad4ac094c74956d65` | 98 |
| `00.kernel/00.00.10.work/0011.contents/01.051.md` | `941f310246e159586ad4af23596edcb6af962ed130704c5ec00519735d681f27` | 9952 |
| `00.kernel/00.00.10.work/0408.seats/01.md` | `dbf2399d528586afd48b51be5b6b6901e568937733295fb8b4390b25249a02e4` | 2031 |
| `00.kernel/00.00.10.work/0401.goal/06.01.md` | `3578934451fc98e1dcfcc0030adebad27478787c4c2b6177f82268ae6826c38c` | 545 |
| `00.kernel/00.00.10.work/0507.prime-support/evidence/realbrief05.14/brief.txt` | `0201b0134c5e0a9e83dc633335636537a1fcef2d39038a4753240ed5edd842a1` | 1912 |
| `00.kernel/00.00.10.work/0507.prime-support/evidence/prime-review05.14/review.md` | `3b1c1c8f6cee4a2df58a1ba0f5140988c11129f1ca149f12dac3356a527f55a5` | 1745 |
| `00.kernel/00.00.10.work/0507.prime-support/evidence/realbrief05.14/submission.md` | `6497129228d3b4e58edbecd6e3ed04624eb2704eed718eb46e296a9a6aa7ba2d` | 5127 |
| `00.kernel/00.00.10.work/0507.prime-support/evidence/prime-review05.10/review.md` | `36d901de4e9ed2dc5258e8c702ad5519957ad3f75a6520ac786ce74d5602593e` | 2365 |
| `00.kernel/00.00.10.work/0504.app-entry/05.17.md` | `ca48e6d89e79171ae4335db4a9c6a1f41ed88d40fb05d0b48da23e2f0843ef29` | 6885 |
| `00.kernel/00.00.10.work/0507.prime-support/05.12.md` | `dce336e1f4c3cd8d4679ddff45f517293b2e6fd991d8bb39560c0412f1f5f3f5` | 8403 |
| `00.kernel/00.00.10.work/0508.return-capture/05.15.md` | `966c440875366b74f8be682bf9d24a28491cc5e32bdd69baad94297b038e7049` | 6533 |
| `labs/prime-boot-pass01/README.md` | `fbe8a2e7062ac1bc64273ad7d6011484dc2eeb5ff57e507b310878e7921f5b7f` | 7105 |

## Answers

Write schema `prime-boot-answers/1` for this attempt, with exactly O1 through O6. The shapes stay as the tool defines them.

- O1 is `{target, citations, conflicts_seen, text}`. `target` is a string. `conflicts_seen` is a list of integers. Cite a packet ref whose path is the target. Set `conflicts_seen` to every conflict index in the attempt’s status record, and to an empty list when that record lists none.
- O2 is `{fields, text}`. `fields` is exactly `release`, `claim`, `execution`, and `review`. Each is `{value, citation}`. The value must occur in the text of the cited ref.
- O3, O4, and O6 are `{citations, text}`.
- O5 is `{none_found: true, text}` or `{citations, text}` with at least one citation.

Use only the attempt and these sources. Where the sources disagree, say so. Where a body is absent, say so.

O1. From the assignment record, state the recorded `current_work` and `assignment_state`. From the NONBLIND review, state what remains open about that assignment. Do not elect a lane winner, a newest page, or a completion.

O2. Report release, claim, execution, and review for the held projection page and for the page the brief calls accepted without a terminal declaration. Keep a header state, a return pointer, a receipt, and a review section distinct when they disagree.

O3. From the brief, list the held items and the follow-up each one names. State the commit identity the brief is describing.

O4. From the brief’s Prime review, state what that review accepts and which limits it keeps. Include whether a fresh model has booted.

O5. Name the visible gaps whose bodies are not packet refs. Include the raw results file the submission names, the current-work page the assignment names, and any rehearsal page whose bytes at this snapshot are a different identity from the brief’s commit. Cite the refs that show the gap. Use `none_found` only when the packet shows no such gap.

O6. Propose one bounded next action or one justified question. The seats record and the boot README both limit authority. Do not appoint a seat, do not publish a page, and do not treat this session as a new Prime.

## One read-only command

After the attempt directory exists, you may run this once and keep the stdout, stderr, and exit:

```text
python -B labs/prime-boot-pass01/prime_boot.py show --attempt <external-attempt-directory> --json
```

You do not run prepare, check, or judge. You do not run prime-status, pack-assemble, clerk-deliver, or any command that writes the desk, the book, or Git. Exit text is an observation. It does not close work.

## Limits you acknowledge

The brief’s rehearsal commit and this snapshot commit are different identities. Three listed pages match at both. Two rehearsal pages named by the brief are not in the list above because their snapshot bytes differ. The live book entry may point at a later contents face. That face is not one of the sources. A receipt records custody. A review section is the review. This homework does not recover all current work.
