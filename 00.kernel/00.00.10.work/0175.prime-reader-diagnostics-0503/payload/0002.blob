# CONTRACT — prime_cycle.py, 05.03 correction (delta over build05.01 and build05.02 CONTRACT.md)

Written before the code change. Everything in the 05.01 and 05.02 contracts stays in force except where this page replaces it. These are unchanged:
- the registration (`/1`), decision (`/2`) and record (`/2`) schemas;
- the journal schemas;
- the dependency pins;
- the exit codes.

## 1. Observation outcome (new, per work, in the read view)

```json
"observation": {"state": "observed" | "failed", "part": null | "source" | "custody", "kind": "<code>",
                "diagnostic": null | {"source": "<what produced it>", "reader_exit": <int|null>,
                                      "stderr_sha256": "<64 hex>", "stderr_bytes": <int>, "stdout_sha256": "<64 hex>", "stdout_bytes": <int>,
                                      "excerpt": "<≤ 2000 chars>", "retained": {"stdout": "<path>", "stderr": "<path>"} | null,
                                      "retained_note": "<why null>"}}
```

**`kind` for `part: source`:**
- `reader-exit-N`: an exit other than 0 or 1;
- `reader-output-over-bound`;
- `reader-report-invalid` (strict JSON failed);
- `no-source-identity`;
- `page-over-bound`.

**`kind` for `part: custody`:** `member-observation-failed`. The named member's reader role is `observation-failed`, and the excerpt carries that member's inspection exit and attention codes.

**Bounds:**
- `excerpt` is the stderr, or the reason text when stderr is empty, decoded with replacement, at most 2000 characters, with `…[truncated]` when cut.
- In text output, one line of at most 240 characters, with control characters shown as `\n`, `\r`, `\t` or `\xNN`.
- The full bytes are never in the view.

**Retention:**
- With `--journal-root`, the child's stdout and stderr go into the operation's journal folder as `reader-<work_id>-stdout.txt` and `reader-<work_id>-stderr.txt`, exclusive-create, and `retained` gives their paths. Their hashes are already in the diagnostic.
- Without a journal root, `retained` is null and `retained_note` says why.

## 2. Custody state and pass state

`custody.state`, on `observation.state: observed` only:
- `present`: the selected member's role is `primary-current-candidate`.
- `absent`: one of
  - no member is named by the page and none is registered;
  - the selected member's role is `missing` or `reserved`;
  - the role is `origin-mismatch`, `cross-book-origin`, `secondary-historical` or `same-page-retrospective`.
- `unresolved`: one of
  - the role is `incomplete`, `refused`, `ambiguous-primary-candidate`, `page-unidentified` or `not-observed`;
  - the registered member is not named by the page;
  - any other role.

On failure, `custody.state` is `unknown`.

`pass_state`, in precedence order:
1. `observation-failed`: the observation failed, with or without a head review.
2. Head review present: the 05.02 rules (`reviewed`, `review-stale`, `review-unusable`) on the observed binding.
3. No head review:
   - `awaiting-review` when custody is `present`;
   - `no-return` when it is `absent`;
   - `custody-unresolved` when it is `unresolved`.

**When the observation failed and a head review exists:**
- `historical` holds its declarations, with reason `observation-failed`;
- `disposition`, `pass_terminal` and `goal_terminal` are `unknown`, and `next_action` is null;
- the latest review is marked not current;
- holds stay listed and blocking.

**Summary** gains `observation_failed` and `custody_unresolved`. `finished_passes` and `completed_goals` still count current values only.

**Attention text:**
- `observation-failed (<part>): <kind>: <excerpt line>; full output <path|not retained>`;
- `custody-unresolved: member <m> role <role>; not treated as no-return`.

The view schema becomes `prime-cycle-view/3`. A `/2` consumer reading `pass_state` may see the two new values; nothing else is renamed.

## 3. record

The checks are:
1. **Before observing**, `binding.source.page_sha256` must be 64 lowercase hex, and `binding.source.page_bytes` a non-negative int. Otherwise: `refused: template binding has no observed source identity (made from a failed read); read again`.
2. **On a failed fresh observation:** `refused: observation failed (<part>): <kind>: <excerpt line>; full output <path|not retained>; nothing was recorded`.
3. **A `custody: member-observation-failed`** observation is a failed observation, and refuses the same way.

Freshness, fingerprint, direction, prior-state and "an accepted review needs a bound captured return" are unchanged.

## 4. packet coverage

After `review_packet assemble` exits 0, packet reads the output's `packet.json` and `custody.json`, and appends a coverage block to its text output:

```
coverage (this packet's own request; not a complete artifact inventory):
  requested: return (member-file) present 6655 b sha …; receipt (member-file) present …; [page (git-blob) …]
  artifact checks requested: 0
  page included: no (live-file registration; the default request adds the page only for git-blob)
  member captured payloads not gathered: 6 — <logical path>, …
```

The journal `result.coverage` holds the same data as JSON. The request schema, the default request and the packet folder are unchanged. A packet that is refused, or whose packet.json is unreadable, gives `coverage: unavailable (<reason>)`.

## 5. Tests (new file tests/test_observation.py)

- **missing adapter:** a labs copy without `prime-support-pass01`;
- **malformed reader output, and an over-bound result:** an injected `run()` result;
- **observed absent:** a PENDING page with no member;
- **a valid captured return** (`present`);
- **unresolved custody;**
- **failed custody observation:** an injected member role;
- **diagnostic bounds and retention,** with and without a journal;
- **no false finished or completed status** after a completed review whose observation fails;
- **record refusals** (a failed-read template; a failed fresh observation);
- **stale history, and a hold, still behave;**
- **packet coverage.**

The existing suites `test_prime_cycle.py` and `test_binding_log.py` must pass unchanged.
