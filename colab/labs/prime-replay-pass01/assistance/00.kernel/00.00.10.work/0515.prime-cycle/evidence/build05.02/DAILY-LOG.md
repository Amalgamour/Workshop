# DAILY-LOG — the prime cycle's operation journal (0515.prime-cycle 05.02)

This is a new bounded addition, at the Director's request (0415/06.03). It logs what this tool actually did each day. It is not a chat log, a shell history or telemetry.

## Coverage

| covered (when `--journal-root` is given) | not covered |
|---|---|
| every `read`, `record`, `inspect` and `packet` invocation: successes, refusals, partial writes, replays, unexpected errors and interrupted runs (start without end) | argument-parse errors (the root is not yet known); `day` itself (read-only, not logged); chat turns, other shell commands, model actions, Director instructions; any operation run without `--journal-root` |

**Enabled or disabled is always visible:**
- text output ends with `journal: <root> op <op_id>`, or `journal: disabled (no --journal-root; this operation is not logged)`;
- JSON output carries a `journal` field.

Prime's documented normal use (PRIME-USE) enables it on every command.

The registration or setup step is not observed by the tool, so it is not logged and no event is invented for it. The first logged fact is the first read.

## What is authoritative

| record | authority |
|---|---|
| `<review_location>/<review_id>/record.json` (+ REVIEW.md, COMMITTED.json) | Prime's decision and reasons. This is the work-local record, and it is unchanged by the journal. |
| `<journal_root>/<date>/<op_id>/start.json`, `end.json` | the machine facts of one invocation: when it started and ended, the tool hash, argv, input hashes, exit, status, output hash and result references. |
| `registration.json`, `decision.json`, `stdout.txt` beside them | exact snapshots of the inputs and output of that invocation |
| the `day` view | derived. It is rebuilt from the events, then checked against the review records on disk now. |

**Machine facts and supplied text are separate.** `machine` holds facts observed by the tool. `supplied` holds `--caller` and `--note` exactly as given, which are labels and not authentication. Reasons and decisions are never copied into the journal: an end event points at the review by directory and record hash.

## Restart and failure

**One invocation, one directory.** `<op_id>` is the UTC time plus 12 random hex digits. Every file is exclusive-create. Nothing in the journal is ever rewritten, deleted or retried.

| situation | what you see | exit |
|---|---|---|
| start event cannot be written (bad root, root inside the repository or members book, link, collision, disk) | `refused: journal start failed …; nothing was run`; the operation did not run | 4 |
| operation ran, end event cannot be written | the operation's normal output, then on stderr: `journal: end event FAILED … the review IS committed at <dir>` (or partial). The entry stays incomplete. | 5 |
| unexpected exception inside the operation | `error: …`; the end status is `error` | 6 |
| interrupted (Ctrl-C, kill, power) | no end event; `day` shows `incomplete`, end state unknown | — |
| review write interrupted | the end status is `partial`, with the files present and their hashes; the partial stays on disk | 3 |

**After a crash,** run `day` to see the incomplete operation. A record may still have reached the review location, so run `read` or `inspect` to check. Recover a partial review only by a new review_id with `recovers`.

## How to inspect a day

```text
python -B labs/prime-cycle-pass01/prime_cycle.py day --journal-root D:\prime-cycle-out\journal --registration D:\prime-cycle-out\reg-0520.json
python -B labs/prime-cycle-pass01/prime_cycle.py day --journal-root D:\prime-cycle-out\journal --date 2026-10-30 --json
```

The date is the local date at operation start. The default is today.

The view shows:
- **attempts,** by operation and status;
- **each operation:** op_id, local start time with offset, duration, exit and caller, the first line of a refusal, and the review it touched;
- **unique reviews:** recorded or replayed reviews keyed by (directory, record hash), each re-verified against its marker now, with the number of invocations and replays;
- **declared:** finished passes, completed goals and holds from unique verified records. Each work's pass and each work goal counts once, however many invocations or reviews declare it. Declared is not current.
- **current** (only with `--registration`): a fresh read's finished passes, completed goals, open holds, and the works whose latest review is not current. A stale, unusable, partial or invalid review is never current completion.

**What the day view does not do:**
- it gives no time totals; incomplete operations have unknown duration;
- it never treats a missing time as zero;
- it derives no productivity from operation counts.

## What remains manually supplied

- Prime's judgment, the goal statements and the agreement, as before.
- The caller label and any note.
- The choice to pass `--journal-root` on each command.
- Anything outside this tool: conversation capture and Director instructions, which remain unbuilt connections.
