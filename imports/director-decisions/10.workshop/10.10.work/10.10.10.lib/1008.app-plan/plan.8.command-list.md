# plan.8 command list

version: 001
Authorization: draft — 2026-10-15
who: claude-opus-5-5
state: draft
page: 1008.app-plan
why: The desk command list, drafted for review (05.03 #06). 24 commands with `>grant` (1009.calling 05.02 #04). Every command once: what it asks of the Director, what the model does after, and where its meaning comes from. Where it is seated is asked on 05.03 #09.

## How to read this list
- **The command is the kind of a line** (`05.02` #02). It is read from the `Ask:` line. The heading `#NN >command subject` should start with the same word.
- **Grammar:** `>word`, optionally followed by `.target` (`>run.05.05`, `>approve.0004`, `>draft.10.lib.0000-0009`). The word is the command. The target narrows it. It is not a new command.
- **Case:** read as lower case. `>Note` and `>note` are one command. Headings have used capitals 120 or more times; new lines write lower case.
- **A command not on this list is kicked back** with the reason (`05.02` #02). A book may add a local list later that inherits this one.
- **Source** says where the meaning comes from. "From use" means no page defines it yet; the meaning is read from the lines that used it, and is marked so. Nothing here is invented.
- **Counts** are from 122 batch files in `10.workshop`, `00.00.00.kernel.draft` and `colab/designs` on 2026-10-15: `Ask` is lines that asked it, `reply` is your replies that used it.

- **Calling** (`1009.calling 05.01 #12`): each command carries three hands, answers / does / checks, from compute, model, user. A line's calling is read from its command. An act with no calling is kicked back.
- **`>keep` and `>take` in a reply** (`1009.calling 05.02 #06`): `>keep` accepts the proposal with the amendments in the reply; aligned, it closes; needing change, it rolls into the next batch. `>take` is the recommendation plus any overflow the reply adds. `>decided` and `>confirmed` read as `>take`. Replies stay free-form.

## Keep a seated face fresh
`1004.improvements` face `01`, section Fresh: these keep a seated face fresh when it is not being replaced. Nothing is removed from an approved seated face. Patches, strikes and notes merge when the next draft is written.

| command | asks of you | the model then | source | Ask / reply | calling: answers / does / checks |
| --- | --- | --- | --- | --- | --- |
| `>patch` | allow a minor, dated correction to a section | writes the corrected lines on the active face, dated, with the `#NN`; not a rewrite | 1004 Fresh; law `0021` card (`patch: minor. dated on the active face. not a rewrite`) | 8 / 19 | user / model / compute |
| `>note` | record a face issue, or a finding, without changing the face | writes the note on face `06` (or the place the line names); a note does not govern | 1004 Fresh | 94 / 51 | user / model / compute |
| `>strike` | mark a line as no longer valid; the line stays | draws a line through it with the date and `#NN`; merges on the next draft; never a delete | 1004 Fresh; law `0026` card | 6 / 9 | user / model / compute |
| `>point` | correct a mapping (a parent, a child, a link) | changes the pointer only | 1004 Fresh | 21 / 8 | user / model / compute |
| `>fix` | apply one of `>patch`, `>note`, `>strike`, `>point` from a return | writes it; names the page and the sentence; does not approve itself | 1004 Fresh; law `0021` card (`fix: a return made into a write`) | 0 / 20 | user / model / compute |

## Draft, sign and seat
| command | asks of you | the model then | source | Ask / reply | calling: answers / does / checks |
| --- | --- | --- | --- | --- | --- |
| `>draft` | allow a new draft `FF.VVV.md` beside the seat | writes the draft; the seat stays | law `0021` card (`rewrite: FF.VVV beside the seat`) | 10 / 6 | user / model / compute |
| `>amend` | allow a change to an unsigned or signed draft before it is seated | changes the draft in place and says what changed | from use (`1006.redraft` 05.13, "signed drafts were amended in place") | 13 / 22 | user / model / compute |
| `>sign` | (now a model and compute step: the page is finished and functional; `1009.calling 05.01 #07`) | sets `Authorization: signed`; compute verifies; signed is not seated | law `0021` card (`sign: prime stamp`); Director ruling on the solo return ("signed is the legal level a prime can take work to") | 27 / 55 | model / model / compute (ready) |
| `>approve` | seat a signed draft | renames the old seat to `FF.VVV.09` into `00.retire.09`, renames the draft onto `FF.md`, stamps approved, in one act | law `0022` card; law `0009` (`the prime trigger is >approve or >retire`) | 31 / 25 | user / compute (rename) / compute |
| `>retire` | retire a face | marks it `FF.VVV.09` and moves it to `00.retire.09` | law `0009` | 0 / 1 | user / compute / compute |
| `>lock` | lock a face | stamps `Authorization: lock` | from use (`Authorization: lock` on `00.about`, `00.readme`; 2 `source:` lines) | 0 / 0 | user / compute / compute |
| `>promote` | promote a book | follows law `0023`: commit, build the candidate, verify, retire the old book, lock | law `0023` card | 0 / 0 | user / compute / compute |
| `>keep` | accept the proposal, with any amendments written in the reply | aligned: applies them and closes the line; needing change: rolls the line into the next batch | `1009.calling 05.02 #06` | 2 / 1 | user / model / compute |

## The batch flow
| command | asks of you | the model then | source | Ask / reply | calling: answers / does / checks |
| --- | --- | --- | --- | --- | --- |
| `>take` | accept the recommendation, with any overflow the reply adds | does what the recommendation, the Ask and the reply's overflow say, and no more; a miss rolls into the next batch | `2002.face` 01 (`A reply of >take accepts the line`) | 81 / 69 | user / model / compute |
| `>hold` | keep the line open; no act now | writes nothing; the line stays open or is carried | from use | 22 / 9 | user / none / compute |
| `>review` | read finished work and say take or correct | nothing until your reply; a correction is carried to the next batch | from use; `05.03` #07 | 25 / 0 | user / none / compute |
| `>decide` | choose between options the line lists | does the chosen option | this page, `05.01` #09, #10 | 2 / 0 | user / model / compute |
| `>ignore` | discard a line from a return because acting on it would undo an approval | closes it; nothing is written | from use (`1006.redraft` 05.18) | 5 / 2 | user / none / compute |
| `>build` | release a build job | builds within the job's scope, on the named branch | AGENTS (job type build); this page | 3 / 0 | user / model / compute |
| `>read` | have a model read cold and report the misses | reads and reports; writes only its notes | from use (`1006.redraft`) | 1 / 0 | user / model / compute |
| `>run` | run a batch that is already answered | executes each released line and files the batch | from use (`>run.05.NN` in 7 `source:` lines) | 0 / 0 | user / model, then compute writes status / compute |
| `>go` | go ahead with what was just proposed | proceeds within the proposal | from use (reply only) | 0 / 17 | user / model / compute |
| `>grant` | **new.** Engage the local mode for a shelf or book, as `>grant local <place>`, listing the acts handed down | nothing; compute activates and records the grant; ends on withdrawal or its end date; never hands down merge, grants, AGENTS, the kernel, money | `1009.calling 05.02 #04` | 0 / 0 | user / compute / compute |
| `>stop` | **new.** The model is blocked and needs you | nothing until your reply; it says where it stopped, what it had planned, what it needs | `05.02` #02 | 0 / 0 | user / none, the model waits / compute |

## Seen but not listed
These words appear in replies or sources but are not on the list. Each is asked on `05.03` #10. Until then, a new line using one is kicked back.
- **Two spellings, one act?** `>amend.draft` (18 Ask lines) against `>amend` (13): by the grammar above, `.draft` is a target, so both are `>amend`. `>redraft` (1 reply) against `>draft`.
- **Past tense:** `>approved`, `>noted`, `>patched`, `>retired` appear in replies. They read as status, not asks.
- **Plural:** `>notes` (2 replies).
- **Reply only, once or twice:** `>explain`, `>update`, `>write`, `>align`, `>check`, `>replace`, `>repair`, `>setup`, `>crawl`, `>lead`, `>prep`, `>design`, `>scope`, `>restore`, `>guard`, `>finish`, `>let`, `>date`, `>name`, `>choose`, `>carry`, `>limit`, `>show`, `>tell`, `>place`, `>rewrite`.
- **Known conflict:** a discard asks `>ignore` in `1006.redraft` 05.18, while law `0039` says "A discard is still a #NN. The ask is >strike." Two faces disagree; this list does not pick (05.18 already names it).

## Not
Not law. Not seated. Nothing in old batches is renamed or rewritten by this list.
