# Prime status and intake, lab pass 01

**Batch:** `00.kernel/00.00.10.work/0507.prime-support/05.02.md`, released by the Director on 2026-10-27.
**Who:** claude-opus-5-5.
**State:** fixture lab.
- No real intake store is installed. Nothing is seated.
- Status grants nothing: it does not release, accept, route or dispatch.
- Every field it reads beyond the existing conventions is a provisional fixture contract, not workshop law.

**Contract:** `00.kernel/00.00.10.work/0507.prime-support/evidence/build05.02/DESIGN.002.md`. It is additive to the 05.01 design, and it covers PS-01, PS-02 and PS-03 from Prime's 05.01 review.

## Run the demonstration (one command)

```text
python -B demo.py --out <new absolute directory outside any Git tree> --workshop-repo D:\Git\lib-build --sof-repo D:\Git\SoF
```

- **Read-only on the source repositories.** The demo reads six pinned blobs with `git show`, checks each sha256, and copies them into disposable repositories under `--out`, each with a local bare origin. It never reads or writes either repository's working tree.
- **Real shapes it uses:**
  - three revisions of `0504.app-entry/05.05.md`;
  - `05.06.md`;
  - the canonical record;
  - SoF's `returns/sof-gm-kit-pass01.md` at `sof/gm-kit` `01b8fe6`.
- **The synthetic walk:** unseen → seen → reviewed → amended, with the old Review removed and SY-01 carried forward. The acknowledgements are then deleted, and SY-01 is still open.
- **Output:** each tool call runs as a separate process and is recorded in `transcript.json`. It ends with `demo ok`.

## Commands

```text
python -B prime_support.py status --registry <abs lanes.json> [--intake <abs store>] [--json]
python -B prime_support.py intake scan --registry <abs lanes.json> [--intake <abs store>] [--json]
python -B prime_support.py intake ack --registry R --intake S --lane L --path P --revision <64 hex> --as LABEL
python -B prime_support.py intake show --intake <abs store> [--json]
```

**Read-only commands:** `status`, `scan` and `show`.
- Git runs only through an allowlist: rev-parse, show, ls-tree, log, status, merge-base, for-each-ref, cat-file. Any other subcommand, fetch included, raises before it runs.
- Remote refs are reported as last observed, never fetched.

**`ack` writes exactly one file** in the store it is given, by exclusive create. The store must be absolute and outside every Git working tree.

**Exit codes:** 0 nothing needs attention, 1 attention items exist, 2 refused (invalid registry, store or arguments).

## What it reads

The registry (`prime-support-registry` v1) owns paths and scope, never state. Per lane it can name:
- **page folders:** only root `05.NN.md` files are read;
- **exact return files**, such as the SoF bootstrap return;
- **exact review sources.**

Per file, it reads the published ref, HEAD, the worktree (only when the repository's `worktree` setting is `registered-paths`), and bounded history.

**Return identity:** `revision_id` is sha256 of the bytes before the one recognized top-level Review heading. Fenced blocks are skipped, trailing blank lines are removed, and one LF is added. Ambiguous, duplicate or misordered headings refuse the source as `unsupported`.

**Review and findings:**
- Review state and findings are derived from page Reviews and declared review sources across bounded history.
- They are never read from the intake store.
- Missing history is reported as `history incomplete` or `history none`, as an attention item, never as zero findings.
- `Disposition:` text is shown verbatim. Acceptance is never computed.

## Tests

```text
python -B -X dev tests/test_prime_support.py -v
```

There are 19 tests, each building disposable repositories with local bare origins under the system temp directory. Run them from a copy of the lab if you want nothing at all near the shared checkout.

## Limits

- `--as` is a label. Hashes bind bytes; they do not authenticate anyone.
- Findings are machine-readable only where a provisional `findings:` line exists. Real pages today mostly have none, and status says so.
- No Observer fetch, no Clerk adapter, no real store, no app wiring, no scheduler.
- Remote state is only as fresh as the last fetch someone else made.
- Path checks are not an operating-system sandbox.
