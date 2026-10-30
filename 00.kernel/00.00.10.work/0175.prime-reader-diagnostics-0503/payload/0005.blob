# PRIME-USE — reading the 05.03 states (delta over build05.02/PRIME-USE.md)

For Codex Prime. The commands, registration, journal root and template filling are unchanged from `build05.02/PRIME-USE.md`. This page covers only what you will now see differently. Prime accepts and pins this tool identity before 0516 packages it; it is not substituted into the first replay's bundle.

## Pass states you may now see

| pass state | means | what to do |
|---|---|---|
| `no-return` | The read **succeeded** and saw no current return for this page: no member named or registered, the member is missing or only reserved, or it belongs to another origin. | Nothing to review yet. |
| `custody-unresolved` | The read succeeded and saw custody, but it is not usable: `incomplete`, `refused`, an ambiguous primary, or a registered member the page does not name. | Run `return_inspect.py inspect` for the member and fix the custody or the registration. This is never treated as no-return. |
| `observation-failed` | The page (`part: source`) or the member's inspection (`part: custody`) could not be observed. | Read the attention line. It gives the reader's kind (`reader-exit-2`, `reader-report-invalid`, …), a one-line excerpt, and the path of the full stderr when `--journal-root` was given. Fix the environment, then read again. |

`awaiting-review`, `reviewed`, `review-stale` and `review-unusable` are unchanged.

**When a recorded review exists and the observation fails:**
- its declarations show as `unknown (historical … in <review>, observation-failed)`;
- the summary and day view count nothing as finished or completed;
- holds stay listed and blocking.

When the observation works again, the same review is current again. Nothing is rewritten.

## Example: the replay's missing adapter, as it now reads

```text
pass state: observation-failed   review disposition: unknown   pass terminal: unknown
! observation-failed (source): reader-exit-2: missing clerk_adapter.py; full output <journal>\<date>\<op>\reader-A-stderr.txt
```

The JSON gives `observation.diagnostic`:
- the reader exit, and stdout and stderr hashes and byte counts;
- an excerpt of at most 2000 characters;
- `retained` paths.

The text line is at most 240 characters on one line, with control characters escaped.

## record refusals added

- `template binding has no observed source identity (made from a failed read); read again`: the template came from a read whose observation failed.
- `observation failed (<part>): <kind>: <excerpt>; full output <path|not retained>; nothing was recorded`.

## packet coverage

`packet` now ends with a coverage block. For example:

```text
coverage (this packet's own request; not a complete artifact inventory):
  requested: return (member-file) present …; receipt (member-file) present …
  artifact checks requested: 0
  page included: no (not requested: the default request adds the page only for a git-blob registration)
  member captured payloads not gathered: 1 - note.txt
```

The same data is in the journal end event, as `result.coverage`. The packet request is unchanged. For artifact rows, write an explicit `review_packet` request (05.02 practice); the 0516 minimum-evidence plan decides any default change.

## Limits

- The custody-part diagnostic carries only what the reader reports: the inspector's exit and attention codes, not its stderr. Run the inspector for detail.
- Diagnostics are not authentication or authority.
- There is still no OS sandbox, and same-user races are not covered.
