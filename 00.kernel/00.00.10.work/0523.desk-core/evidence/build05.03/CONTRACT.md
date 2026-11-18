# CONTRACT — desk-core/2 reliability lab
date: 2026-11-01
who: Grok Build (xAI)
state: lab contract before code; not production law

## Compatibility
Request and result connector names stay the same. Result schema remains
`desk-core-result/1`. Contract id remains `desk-core/2`.
New internal records are `desk-core-revision-intent/1` only. A sealed
`desk-core-revision/1` is not rewritten. `desk-core-selected/1` still names
both task and face hashes. Unsupported input is refused. A version 1 task
preimage still recomputes and is not treated as version 2.
`DESK_CORE_FAULT` is not a request field and not a CLI flag. A model JSON
body cannot set it. If the environment value is not empty and not one of the
boundaries below, the command refuses `fault`.

## Platforms
Target: Windows Python 3.12+ and Linux.
This lab runs on Linux Python 3.11.2. Python 3.10.22 may be reported only as
an extra Linux check. Windows Python 3.12+ is pending Prime.
No runtime is installed. An untested platform is not a pass.
These checks do not prove race freedom, power loss, every filesystem, or
concurrent writers.

## Faces
A heading line may end in LF or CRLF. The CR is not part of the heading text.
Projection checks compare logical newlines and do not write the face back.
Receipts, history, task bytes, and hashes are not normalized.
Newly rendered section bodies are LF. Bytes outside a replaced section stay
exact, including CRLF headings.
If the heading bytes are present but the line is not one LF or CRLF heading,
the refusal is `face-format` and names `cr-only` or `not-a-heading-line`.
It does not say the heading is missing. A heading that is absent stays `face`.

## Lock
`file_lock` is unchanged: POSIX `fcntl.flock`, or one-byte blocking
`msvcrt.LK_LOCK` on Windows. It is not a no-op.
The regression child must be a separate process. On Windows it uses
`msvcrt.LK_NBLCK` for one byte. On POSIX it uses `fcntl.LOCK_EX|LOCK_NB`.
The parent holds `file_lock`. The child must fail to acquire the lock.

## Revision write order
For selected pair A and proposal B the writer does only this, in order:
1. `before-prior-task` — no history files. Live A is untouched. B is not invented.
2. `intent.json` — request hash, reason, authorizing reference, planned hashes.
3. exact prior task bytes.
4. `after-prior-task`.
5. exact prior face bytes.
6. `after-prior-face`.
7. exact proposed task bytes.
8. `after-proposed-task`.
9. exact proposed face bytes.
10. `after-proposed-face`.
11. sealed `revision.json`. The seal is not a selection.
12. `after-revision-journal`. Live files are still A.
13. replace the live task with B.
14. `after-task-replacement`. The pair is split. Not complete. Not selected.
15. replace the live face with B.
16. `after-face-replacement`. Both live files are B. Selection is not committed.
17. write `selected.json` only if both live hashes match the proposal.
18. `after-selection-before-cleanup`.
19. remove a partial marker if one exists. History is not removed.

A crash inside a single `write` call is not a separate matrix row. An existing
`name.tmp` stays occupied and is not truncated. This is not a power-loss proof.

`DESK_CORE_FAULT=<boundary>` writes a trace row and then `os._exit(91)`.
Expected injected exits are not unexpected build failures.

## Recovery
`show` does not mutate. `recover` in a new process may:
- keep A when both live files still match the preserved prior bytes;
- write `selected.json` when both live files already match one sealed proposal
  and that proposal's staged hashes verify;
- restore both live files from the preserved prior bytes when the pair is split
  and selection was not committed;
- remove a partial marker only after selected task and face hashes both match;
- refuse `revision-corrupt` or `revision-ambiguous` without deleting staged files.

`recover` does not choose the highest revision id. A different request while an
unsealed intent or an unselected proposal is open is `revision-unfinished`.
The same request may resume missing files and must not open a second history
directory or overwrite a mismatched staged file.
`revise-task` of that same request may finish the recorded proposal. That is
the revision command, not a hidden choice inside `recover`.
Receipts are not rewritten. A return captured for A is not a fresh review of B.
`complete` is false unless the selected task and face are one verified pair
and the usual receipt rules pass. One replaced file is not completion.
A second `recover` does not change task, face, history, receipt, or selected
bytes.

## Trace
Pass traces stay `05.PP.trace/NNNN.json`. Fault and recover rows name the
contract, the boundary or check, the input hash, the outcome, and the next
route. No credentials. No model launch.

## Not claimed
No production integration, no live 0123 custody, no adoption of this schema by
the normal app, and no Windows acceptance from a Linux run.
