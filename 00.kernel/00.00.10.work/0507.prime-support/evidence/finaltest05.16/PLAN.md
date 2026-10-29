# PLAN — reconciled fresh-session orientation test bundle (0507.prime-support 05.16)

Author: claude-opus-5-5, Colab. Date: 2026-10-29. Test preparation only. The author of this bundle also wrote its evaluator, so the author cannot be the blind candidate.

## Question this trial asks

Can a **new** session, given only this bundle, do four things without the Director reconstructing chat?
- Read a declared historical snapshot.
- Tell claims, custody, review and authority apart.
- Identify the unresolved gaps.
- Propose one bounded next action.

It does **not** test recovery of all current work. It doesn't settle D1, replace Prime, or authorise any execution.

## Binding (fixed before any answer)

| item | value | source |
|---|---|---|
| source cut | `d3b6ad3e55beb1ec0bd5acbb114e6e66fd66c4e9` | RECONCILIATION.md, DEPENDENCIES.json |
| brief observation cut (distinct) | `6d18d182535df8dc60b698c585b04cd276c5df85` | the brief itself |
| packet | the twelve commit blobs in `0508.return-capture/evidence/cold-prime05.18/DEPENDENCIES.json`, 52,701 bytes; members `[]`, members_book `null` | DEPENDENCIES.json |
| registry | `0507.prime-support/evidence/packet05.15/registry.json`, sha256 `8a068546390d49c3958511d805be0b7c06ce9bf277b25ba575bc3780e4bd5cdb` | RECONCILIATION.md: Prime's preparation choice, **not** a D1 resolution or a lane winner |
| predecessor | attempt 1: the original 0148 attempt `C:\Users\misg\AppData\Local\Temp\pb-packet-0515-zidw8krt\p1` (intent sha `1573f3bf…`), verified intact against packet05.15/records.json | RECONCILIATION.md; 05.16 #03 |
| this attempt | number 2; external records root (new); attempt id `t2` | 05.16 #03 |
| model label | `unassigned-preparation-only`. The real candidate's identity is recorded later, separately, by LAUNCH.md | 05.16 #05 |
| tools | the accepted `app/librarian.py boot-prepare` and `boot-show`, pinned through app/prime-boot.json, unchanged | 05.16 #02 |

This replaces 0148's packet *for the next test only*. 0148 and 0150 are never edited or relabelled.

## Paired clarifications, bound before any answer (from RECONCILIATION.md)

| | candidate instruction (HOMEWORK) | evaluator criterion (EVALUATOR) |
|---|---|---|
| O1 | `target` is the assignment evidence page `00.kernel/00.00.10.work/0401.goal/06.01.md`. Cite its ref, and state the recorded current_work in the text. | Grade the evidence-target reading. Don't demand a citation of the absent current-work body. The target nominates nothing. |
| O2 | `fields` holds four exact substrings from 0507/05.12 only. 0508/05.15 is compared in `text`. | Grade both the extraction and the comparison. No second fields array. |
| O5 | Name the unavailable evidence and the source-cut differences. Don't verify excluded bodies. | Don't penalise a justified "cannot verify". Hidden chat knowledge is not required. |
| envelope | `{schema: "prime-boot-answers/1", attempt_id: "t2", answers: {O1…O6}}`, citing actual prepared ids | the same |

Grok-2's original `cold-prime05.18/HOMEWORK.md` and `EVALUATOR.md` stay untouched. These are new, paired copies for this exact packet.

## Outputs

- **ENTRY.md**, for the candidate: purpose, role, status, environment, cuts, reading order, the allowed read-only command, the answer shape, the limits and the stop point.
- **HOMEWORK.md**, for the candidate: the actual ids and the O1-O6 instructions. No expected answers.
- **EVALUATOR.md**, Director and Prime only: the strict pass rule, the critical violations and the paired criteria. It applies to this packet only.
- **LAUNCH.md**, for the Director: one copyable prompt, plus the procedure for recording the candidate's identity separately.
- **candidate.zip:** ENTRY, HOMEWORK, attempt files 00-19 and a manifest. No evaluator, grading driver, source pack or repository dump.
- **evaluator.zip:** EVALUATOR, the binding metadata and a manifest, marked Director and Prime only. This is an instructional separation, not an OS security claim.
- **records.json, verification.json:** the preserved attempt and the checks.

## Expected

`prepare` gives `prepared`, with 12 refs, 52,701 bytes, 0 absences, 0 omissions, and stable. `show` gives "awaiting answers". If the result is `partial` or `failed`, it is kept as it is and reported as a blocker.
