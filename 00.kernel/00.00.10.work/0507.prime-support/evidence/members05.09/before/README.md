# prime-boot-pass01

A fixture-only prototype of the recorded Prime boot (0507.prime-support/05.07). It is the accepted design in `boot-design05.06/BOOT.md`, carrying the PB-01 to PB-05 review requirements. Standard library only.

The contract is `00.kernel/00.00.10.work/0507.prime-support/evidence/build05.07/CONTRACT.md`.

```
python -B prime_boot.py prepare --request REQ.json --records ROOT --attempt ID
python -B prime_boot.py check   --attempt ROOT/ID --answers ANSWERS.json
python -B prime_boot.py judge   --attempt ROOT/ID --judgement JUDGEMENT.json
python -B prime_boot.py show    --attempt ROOT/ID [--json]
python -B -X dev tests/test_prime_boot.py -v
python -B demo.py
```

## What it does

`prepare` follows a fixed order:
1. It allocates `ROOT/ID` exclusively.
2. It keeps the request bytes and an intent record.
3. It runs ten stages, each writing its own write-once file:
   - request;
   - links to a previous attempt;
   - tool pins;
   - Git identities and dirty paths;
   - the book pointer and `check_book`;
   - role and assignment records as text;
   - `prime_support status`;
   - member `verify`;
   - the packet;
   - a stability re-read.
4. It writes `19.prepare-outcome.json`, which is `prepared`, `partial` or `failed`.

A failed stage stops the run, and its record is kept. An interrupted run leaves its files with no outcome, and `show` reports it as interrupted.

The packet holds the exact committed blob text at the requested commit, within 12 refs and 128 KiB. It also holds:
- a separate live observation per ref: `same`, `differs` with the live hash, or `absent`;
- absence records `A01…` for sources missing at the commit;
- omission records for anything capped out.

Nothing is truncated.

`check` records fixture answers O1-O6 and checks them:
- citations;
- the O1 target against the declared scope (attention order is advice);
- acknowledgement of every reported conflict;
- the O2 field values against the cited text;
- O5 `none_found`.

`judge` records a supplied judgement and writes `39.outcome.json`, which is `oriented`, `partial` or `not-oriented`. Every outcome says `authority: none`.

Retries are immutable. An identical second `check` or `judge` reports `already-recorded`; a different one refuses with `conflict`. A new attempt links the earlier one by path, and never edits it.

## What it does not do

- **Not a model boot.** It does not call a model, so it cannot claim a model cold-booted. The answers and judgements are fixtures.
- **No live or Clerk inputs.** It installs no live registry. A registry with `clerk_jobs` is refused as unsupported.
- **No shared records.** It does not acknowledge, dispatch or change assignment records.
- **No return inspector.** It does not read or import `return_inspect.py`. Member returns get capture integrity only, through `return_capture.py verify`.
- **No authority.** Orientation is not authority. An `oriented` outcome means the recorded exercise passed; reported conflicts may still be unresolved.

## Pinned tools

The hashes are fixed in `PINS`. A tool is checked before every launch, and a mismatch never launches.

| Tool | sha256 |
|---|---|
| prime_support.py | 700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70 |
| clerk_adapter.py | 2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4 |
| check_book.py | fc16d2f68a3645050b6766ce18ce55f8169a0e2bad52d3392b4d059c629073a4 |
| return_capture.py | 8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac |

## Validation and replay (05.08, PB-06 and PB-07)

The contract addendum is `00.kernel/00.00.10.work/0507.prime-support/evidence/repair05.08/CONTRACT.md`.

**Exit codes, every command**

| exit | meaning |
|---|---|
| 0 | the stage completed with a positive result |
| 1 | the stage completed with a recorded negative result: `partial`, checks failed, or not oriented |
| 2 | refused (nothing new recorded), or prepare failed at a stage and recorded that failure, as in 05.07 |
| 3 | incomplete: an identical replay found raw input but no readable terminal record |

**Shape validation.** Answers, judgements, and the registry and tool-report fields that this lab reads itself are type-checked before use. Wrong-shaped JSON never ends in a traceback. It is recorded as a failure, and the raw bytes are kept.
- Answers: `22.checks.json` gets `status: failed`, and the failing item is marked `phase: shape`.
- Judgements: `31.judgement.json` gets `status: failed`, and `39.outcome.json` gets `not-oriented` with `judgement: invalid`. No supplied grade is used.

**Replay.** An identical second `check` or `judge` reads the stage's terminal record, `22` or `39`, and reports `already-recorded: …`. If that record is missing or unreadable, it reports `incomplete: …; start a new linked attempt` with exit 3. Replay never writes, repairs or completes a stage. Different bytes still refuse with `conflict`.

**show.** `show` names the stage: interrupted, prepare-failed, awaiting-answers, check-incomplete, checked, judgement-incomplete or outcome. `--json` adds `stage` and `complete`. Only a readable `39` gives an outcome. A raw file on its own never does.
