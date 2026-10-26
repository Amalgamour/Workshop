# plan.1 starting point

Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: draft
page: 1008.app-plan
why: What exists today, what was run, and what blocks an app. Evidence, not opinion.

## How this was checked
Read: the kernel draft furniture and syntax pages `0001`, `0002`, `0003`, `0014`; the law cards (face `02`) of `0003`, `0004`, `0005`, `0018`, `0021`, `0022`, `0023`, `0024`, `0055`, `0058`; lib pages `0010`, `0014`, `1000`, `2000` to `2005`; both code shelves; the colab return `claude-solo-kernel-pass01-2026-10-15.md`.
Not read page by page: the rest of the law book, faces `04` and `06` on most pages, `Research/`, `notes/`, older colab returns, `law.draft/`, the `drill/` and `sample/` folders.

Run on 2026-10-15 (Python 3.14.7, at `C:\Users\misg\AppData\Local\Python\pythoncore-3.14-64\python.exe`):

| run | result | writes |
| --- | --- | --- |
| `clerk.py test` | `test: pass` | temp folder only |
| solo-kernel `door`, `face`, `menu`, `nav`, `page`, `slot`, `reader`, `journal` `test` | all eight `test: pass` | temp folder only; `git status` clean after |
| `lcheck.py 00.00.00.kernel.draft` (default, read-only) | reworked pages: 0 error, 0 warn, 60 info. Pending pages: 24 error, 41 warn, 32 info | none |

Notes on the runs:
- `python` is not on the Git Bash path. It runs from PowerShell through the Windows Store alias. The app needs one known way to start Python.
- `lcheck.py` fails when Python runs in isolated mode (`-I`). It imports `sentinel.py` from its own folder. Fine for now. Worth knowing.
- A passing self-test proves only what that test checks. Every test here was written by the same model that wrote the code. None runs against the real tree except `reader.py` (per its log) and `lcheck.py`. That is why "passes" below is not "reliable".

## What already works
| tool | what it does today | evidence | reliability |
| --- | --- | --- | --- |
| `lib/code/librarian-check/lcheck.py` + `rules.toml` | lints a kernel tree, sorts findings into reworked and pending pages | ran clean, report above | Verified to run. Rules not audited by me. |
| `lib/code/jobs.py` | finds, places, files `05.NN` batches; checks reply lines are never rewritten; `carry` checks next-links | read; `--help` ran; used for `2002.face` batches | Not run against the tree. The parser is the best existing reader of `#NN`. |
| `lib/code/clerk.py` | `drop`, `draft`, `derive`, `revise` on faces; header from folders; source hash | `test: pass` | Verified test only. Copies face `06` notes onto a draft. |
| solo `face.py` | makes a face draft from a template; stamp, hash, header | `test: pass`; return: 52 of 52 sample hashes match | Verified test only. Refuses face `06`. |
| solo `nav.py`, `door.py`, `desk.py` | walks desk, shelf, book from `00.md`; reads and writes sentinels | `test: pass` | Hard-codes `D:\Git\Librarian` (return hole 6). |
| solo `slot.py`, `page.py` | finds the lowest open slot; makes a page folder | `test: pass` | Stops on a full decade below `1000` (return hole 3). |
| solo `menu.py` | builds face `03` from face `01` headings | `test: pass` | Follows a Director reply that differs from seated law `0003` (return hole 9). |
| solo `reader.py` | reads syntax `0014` Order and walks a desk cold | `test: pass` | Authority check is string matching (return hole 5). |
| solo `journal.py` | stands a user desk from a brief (`use/10.ned`) | `test: pass` | Brief format fixed; hard-coded paths. |
| `lib/code/build.py`, `install.py` | rebuilt and installed the `law.draft` sample | read the guide only | Experiment. Finished its job. |

## Reuse, modify, or leave
| code | verdict | why |
| --- | --- | --- |
| `lcheck.py`, `rules.toml`, `moves.toml` | reuse as is, called from outside | It is the checker AGENTS names. The app runs it. It does not edit it. |
| `jobs.py` parsing (`BATCH_RE`, `ITEM_RE`, `REPLY_RE`, field regexes, "reply never rewritten" check) | reuse, move into the app core | This is the ask reader the first version needs. |
| `jobs.py` write commands (`open`, `piece`, `ran`, `carry`) | keep beside the app for now | The workers already use them. The app reads their output. Merge later. |
| `clerk.py` and solo `face.py` | modify: one face engine, later (stage 6) | Two programs do one job with opposite face `06` policy (return hole 4). `05.02` #07. |
| address parsing (`NAME_RE` in `clerk.py`, `jobs.py`, `face.py`; `parse_name`, `kind_of`) | reuse once, in one module | Three copies of the same rule today. |
| solo `desk.py`, `nav.py` walk | reuse the walk; replace the constants | The walk is right. The paths are hard-coded. |
| solo `menu.py`, `slot.py`, `page.py`, `door.py`, `journal.py`, `reader.py` | later modules | Useful, not needed for the first workflow. |
| `build.py`, `install.py`, `check_v0.py` | leave as experiments | One-time tools. |

## What is missing for an application
1. One program. Today it is twelve scripts, each with its own copy of the address rules.
2. One place that says where things are. Paths and kernel names are written into the code (return hole 6). `00.live` already names book, owner and sitting.
3. A reader for every batch form actually on disk: `05.NN.md` with `state: open`, `05.NN.open.md`, and `05.plan.md`. All three exist today.
4. A safe write layer: version check before a write, atomic replace, a before-copy of each change, and a refusal list. Today each script guards itself.
5. A view of what waits on the Director. About 79 blank `reply:` lines sit in 16 batch files across the lib book, the solo book and the kernel draft. Some are inside batches already filed as `ran`. Nothing today tells those apart.
6. A screen. Today the Director reads raw files.
7. A record of what changed since the last visit, and of every write the app made.
8. A launcher and setup steps that a cold model can repeat.

## Settled enough to build on
| behavior | where it is settled |
| --- | --- |
| Folder name is address plus title: `DD.title`, `DD.SS.title`, `DD.SS.BB.title`, `PPPP.title` | law `0018` card; `jobs.py` docstring; Director reply on `1006.redraft/05.10` `#17` (full address form; "database will address this") |
| Faces: `01` binds, `02` card, `03` menu, `04` person, `05` asks, `06` report and notes, `08` custody | law `0055` card; `00.readme` |
| A seat is `FF.md`; a draft sits beside it with a version | law `0021`, `0024` cards (the draft file name is not settled, see below) |
| A job is `#NN` plus `>` on that line; a blank reply waits; talk without `>` is not work | `00.readme`, `10.workshop/00.readme.md`, law `0005` card, AGENTS |
| A reply is never rewritten; status is appended after the whole reply | AGENTS Authority; `jobs.py` `ran` |
| Approve renames the draft onto the seat; it does not copy | law `0021`, `0022` cards |
| Neither kernel is written by tools; `00.00.00.kernel` is not used | AGENTS; Director 2026-10-15 |

## Not settled, and what each blocks
| question | blocks | decision |
| --- | --- | --- |
| Draft file name: `FF.VVV.md` (law `0021`, `0024`, and the drafts in kernel.draft) or `FF.VVV.draft.md` (Director 2026-10-13 in `clerk.py`; solo book) | stage 6 writes; the reader accepts both | Director chose `FF.VVV` in chat; `05.02` #06 |
| Does a draft carry face `06` notes? `clerk.py` yes, `face.py` no | stage 6 | Director: full copy now, clean later; `05.02` #07 |
| The batch name forms (`05.NN.md`, `.open`, `.replied`, `.closed`, `05.plan.md`) | nothing; the reader accepts all | `05.02` #01 |
| What a full decade below `1000` does (return hole 3) | later page-making module | none now |
| State `built` for a derived face (`2004.approve` open) | later `02`, `03`, `08` builder | none now |
| A dot in a title (`band.build.page`, `band.behavior`) against law `0018` | address parser must allow it; it already does | none now |
| Replies written by a solo run carry no mark (return hole 1) | the batch view could mislabel them as the Director's | `05.02` #03 (solo mode) |
| Shelf sentinel wording (return hole 10) | nothing in the first version | none now |

## Stale references
These were found and left as they are.
- `10.workshop/00.start.md` and `10.workshop/00.about.md` call `00.00.00.kernel` "the check". Known; AGENTS step 3.
- `lib/code/readme.md` says "The check kernel is `00.00.00.kernel`." Same family.
- `lib/2002.face/01.md` keeps "Clerk mode points at the kernel", which reads `00.00.00.kernel`. Same family.
- `00.00.00.kernel/` still holds open batches (`05.plan.md`, `05.01.md`) that mirror kernel.draft. The ask reader must skip that folder or it will double-count.
- `1000.band.active/01` names `1006.redraft` as the active page. The build work moved to band `2000` on 2026-10-12. Not a contradiction, but a cold model will land on `1006`.
