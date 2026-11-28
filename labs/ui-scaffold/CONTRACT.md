# UI-1 contract: every field the screens show

Builder: Claude. 2026-11-25. Status: `9`.
Pins as in README.md: returns 755d046e, prima/build 5201b243, packs 88be5702.

## How to read this

- One row per field.
- **Source** is one of: wf board output, the compute crate, a face file, or the page log.
- **missing** means no source has the field today. It is never filled from a guess (axiom 7).
- **partial** means a source has part of it, and the row says what is not there.
- "log `init`" means the `init` entry in `pages/<addr>/log.jsonl`. Its keys are read from the 0423 log on packs.

---

## The card (every level)

These six fields are the card shape from the brief (W:74).

| Field | Book level (a page card) | Page level (a pass card) | Pass level (a job card) |
|---|---|---|---|
| address | page id: the folder name under `pages/` (src/board.rs:467-477); also log `init` `address` | `<page>.05.NN` (src/board.rs:350, :357) | `<page>.05.NN` + job key, for example `w01` (src/board.rs:362) |
| holder | **missing.** The book board prints no holder (src/board.rs:486-489) | **partial.** The board prints the claimant: "held by" (src/board.rs:368). The lock holder is in the page log `lockout` entry (src/cmd.rs:582) and in `Hold` (src/page.rs:38-46), but the board does not print it | **missing.** A job has no holder of its own |
| step | the six tail counts (src/board.rs:486-489) | the column and tail (src/board.rs:358) | **partial.** From return on: each job's text from the return entry's `jobs` (src/board.rs:412-413; 0423 log entry 19). From signoff on: the signoff `cards` (src/board.rs:432; 0404 log entry 21). At close: the close `cards` (0404 log entry 22: `w01 accepted`). Before return: no job step |
| next | **missing** on the book board | "next" (src/board.rs:371), from `pass_next` (src/status.rs:24) | **missing** |
| why | face 04 goals: log `face` entries with `face 04`, `section goals` (0403 log entry 2); file `pages/<addr>/04.md` | face 01 "Goal:" line (`pages/90.50.10.0423/01.md` line 4 on packs); also the pack entry `face01` key (0423 log entry 27) | the job text in the pack: "job ..." (src/board.rs:362) |
| ruling id | log `init` `grant_ref`, for example `t413u` (0403 log entry 1) | **missing.** The pack entry has no ref key (0423 log entry 27, keys). Only a `grant` entry carries `ref` (0423 log entry 23: `t584s2361`) | **missing** |

---

## Book board

| Field | Source | Cite |
|---|---|---|
| book address | **missing** as a field. The book board names the folder, not a book address | src/board.rs:473 |
| page count | wf board output | src/board.rs:473 |
| per page: title | wf board output (cut to 30 chars); full text in log `init` `title` | src/board.rs:488 |
| per page: entries, last entry time | wf board output | src/board.rs:488 |
| per page: count in each of the six columns | wf board output | src/board.rs:486-489 |
| per page: attention count | wf board output | src/board.rs:487 |
| per page: halted | wf board output | src/board.rs:489 |
| per page: unreadable, with why | wf board output | src/board.rs:479-483 |
| book title, words, brands | the compute crate, `/book/:addr`, `/brands` | crates/compute/src/lib.rs:247, :253 |
| join of a wf page to its compute book | **missing.** wf checks only the form of a work address at init. It does not look it up in a compute book | src/addr.rs:108-123; src/cmd.rs:187 |

## Page board

| Field | Source | Cite |
|---|---|---|
| address, title, person, prime | wf board output | src/board.rs:284 |
| log entry count, last time, head | wf board output | src/board.rs:285-286 |
| attention lines: question, halt, views differ, waiting check, checked, observer, stale | wf board output | src/board.rs:220-260 |
| column name, side label, count, who owes the next move | wf board output | src/board.rs:25-32, :295-305 |
| closed cards cut, and the footer | wf board output | src/board.rs:18, :338-340 |
| face 00 stamp: address, title, person, Prime, grant | face file `00.md`; written by wf from the log | docs/DESIGN.md:21 |
| face 01 agents card | face file `01.md`, with version, entry and hash in line 2 | `pages/90.50.10.0423/01.md` lines 1-2 on packs |
| face 02 pseudo code | face file `02.md` | docs/DESIGN.md:23 |
| face 03 menu | face file `03.md` | docs/DESIGN.md:24 |
| face 04 dev space | face file `04.md` | docs/DESIGN.md:25 |
| face 05 work: the passes | wf board output (the columns) and face file `05.md` | docs/DESIGN.md:26; src/board.rs:295-305 |
| face 06 prime notes | face file `06.md` | docs/DESIGN.md:27 |
| face 07 labs | face file `07.md`; "not built in wf v0" | docs/DESIGN.md:28 |
| face 08 connections | face file `08.md` | docs/DESIGN.md:29 |
| each face: who holds its lock | the page log `lockout` and `release` entries | src/cmd.rs:582, :624; src/page.rs:38-46 |
| each face: last changed at entry | face file line 2 ("Version: v3 (entry 24 ...)") | `pages/90.50.10.0423/01.md` line 2 on packs |
| page resolve trace and links | the compute crate, `/resolve/:addr`, `/links/:addr` | crates/compute/src/lib.rs:250, :252. Books only, not wf pages |

## Pass card (`wf board <page> --card NN`)

| Field | Source | Cite |
|---|---|---|
| column, side label, tail, last entry, owner | wf board output | src/board.rs:358 |
| outcome | wf board output, from the draft | src/board.rs:359 |
| jobs | wf board output | src/board.rs:362 |
| may touch | wf board output | src/board.rs:364 |
| checks | wf board output | src/board.rs:365 |
| repo, start commit | wf board output | src/board.rs:366 |
| held by (the claimant) | wf board output | src/board.rs:368 |
| lock holder | **partial.** In the page log, not on the card | src/cmd.rs:582; src/page.rs:38-46 |
| next | wf board output | src/board.rs:371 |
| age | wf board output | src/board.rs:372 |
| stale, with why | wf board output | src/board.rs:174-218, :374 |
| pack entry, pack hash, template version, files, pinned hashes | wf board output | src/board.rs:376-400 |
| pass branch | the page log `pack` entry `branch` | 0423 log entry 27 |
| close outcome and job cards | the page log `close` entry `outcome`, `cards` | 0404 log entry 22 |
| is the code on returns | **missing.** Close records say "not merged by wf v0" | 0416 log entry 12 |

## Desk (who holds what)

| Field | Source | Cite |
|---|---|---|
| worker name | the page log: `lockout` entry actor; `claim` entry actor | src/cmd.rs:582; src/board.rs:368 |
| page and face held | the page log `lockout` entry `face` | src/cmd.rs:582 |
| reason | the page log `lockout` entry `reason` | src/cmd.rs:582 |
| since | the lockout time and entry | src/page.rs:38-46 (`seq`, `time`) |
| passes claimed, not returned | the page log `claim` and `return` entries | src/board.rs:368 |
| one list across all pages | **missing.** No wf command and no compute route gives it | src/board.rs:466-495; crates/compute/src/lib.rs:244-261 |
| live wf build each worker runs | **missing.** No record of the live pin | labs/draft-page/QUESTIONS.md Q2 |

---

## Fields the front must not show as live

- Anything under `app/mock/`. Those are fixtures (prima/build `app/mock/fixtures/`).
- A count from a log copy that is shorter than another copy. For example 0403 has 12 entries on packs and 9 on returns (labs/review-stage1-route/C1-REVIEW.md, R9). See QUESTIONS.md Q4.
