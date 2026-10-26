# Pack B return: establish one development desk (with addendum 001)

**packs:**
- `packs/lib-build-bootstrap-pass01-2026-10-26/PACK-B-establish.md`
- `packs/lib-build-pack-B-addendum-001-2026-10-26/ADDENDUM-001.md`
- One execution unit: the addendum overrides only the clauses it names.

**executor:** claude-opus-5-5 · **date:** 2026-10-26
**release:** the Director in chat, "You have two packs B and Addendum B  Run addendum-B first then Pack B"
**state:** returned for Prime review. Nothing here is approved, seated or locked.
**evidence commit:** `07adf6eb21ae1dc66060ebbc960eea904c9eefaf` on `workshop`, pushed and verified from GitHub. This return is committed after it; that commit is reported in the handoff.

## Headline

- **Desk established.** `00.kernel`, with books `00.00.00.syntax`, `00.00.01.law` and `00.00.10.work`, on branch `workshop`.
- **Clerk routing NOT integrated.**
- **Normal runtime NOT active.** No seated loader and no active module.
- **AGENTS.004 NOT seated.**
- **Lock and release NOT implemented.**

## Commits on `workshop` (base `14676ca3c01833cc1b472198e62e3451ef706ec3`)

| Commit | What | Files |
|---|---|---|
| `6220a6ac5d00249c124bc57c63cf1ff86a44d693` | empty-tree start (the inherited tree stays in history) | 0 |
| `211cd3a05b0f56f1f60587013b4f0e855c8b457c` | tracked `.gitattributes` and `.gitignore`, before any payload | 2 |
| `d0bdd53a1d9d3cffda600b7102e3bcb0934359eb` | the baseline as found: 39 original + 338 additive | 377 |
| `ac0dea09513516f2f82cceaf7b3244b0056cda42` | imports from pinned Git objects | 995 |
| `07adf6eb21ae1dc66060ebbc960eea904c9eefaf` | drafts, work records, Pack B tools and evidence | 179 |

Tracked after `07adf6e`: 1,553 files. There are no mode 160000 entries (no gitlinks).
Only `workshop` was pushed, as a new branch with no force. `main` (`14676ca`) and `rebuild` (`de3b8eb`) are unchanged. The three archive refs are unchanged too: `e8b1a994…`, `586cfa4a…`, `fe42b017…`.

## Addendum 001

### #B-A01 Dependency and return overrides: pass

- Addendum package (12 files), 13 pinned dependencies, the original package (18 files) and the original baseline (39 files) all matched by length and SHA-256.
- The remote archive refs equal the pinned final commits: `e8b1a994da07000fa576fd771e455a94718ed431` (90 rows), `586cfa4ae055c29a98c1106bb70143901c57cc11` (28) and `fe42b017b5e8c288f70878d696cb227b09ab5a8e` (49).
- After fetching into the **new** repository, all 167 archive rows were verified there by `COMMIT:path` blob (`labs/bootstrap-establish-pass01/evidence/step02/init.log`).
- Returns are in `returns/`. Pack A was not rerun.

### #B-A02 Git-byte fixture gate: pass, 6 of 6

Tool `labs/bootstrap-git-bytes-pass01/gitbytes.py`, tests `test_gitbytes.py`, output `evidence/gate-test-output.txt`.

**The refusals, each captured in `evidence/gate-calls/`:**
1. **CRLF under `* text=auto eol=lf`.** The worktree check passes, but the index check refuses: `index: differs labs/fx/crlf.md (28 bytes, 083c12d5071a)`. Attributes refuse with `text is auto`. Nothing was committed.
2. **Tracked `-text` custody.** CRLF, LF and binary (with NUL) stay exact in worktree, index and commit. App code outside custody stays `text: auto` with LF. Effective attributes are in `evidence/effective-attributes-fixture.txt`.
3. **Wrong bytes staged behind a correct worktree file.** Refused: `index: differs labs/fx/crlf.md (13 bytes, cb5b1095de59)`.
4. **A mismatching committed blob** fails: `commit …: differs imports/fx/data.bin`. A missing path also fails.
5. **An independent clone** (`--no-local --no-hardlinks --no-checkout`, then `core.autocrlf=true`, then checkout, with no local attributes) keeps every byte in worktree, index and commit.
6. **A local `.git/info/attributes` override** is itself refused.

Only test repositories got `core.autocrlf=true`. Global and system configuration was not changed: the system setting is `true`, and global is unset.

**Later:** the verifier's index check was changed to read the whole index (see #03), and the gate was re-run: 6 of 6 again.

### #B-A03 Tracked attributes at every Git boundary: pass

**The policy**, committed in `211cd3a`, exactly as the addendum gives it:
- `* text=auto eol=lf`
- `-text` on `/imports/**`, `/labs/**`, `/notes/**`, `/packs/**`, `/returns/**` and `/00.kernel/**`

**What was checked for each custody set before staging:** effective attributes (`text` unset; no `filter`, `ident`, `working-tree-encoding` or `crlf`), and no local or configured attribute file overriding them. There is no nested `.gitattributes` outside scratch.

**Byte checks** (worktree, then index before commit, then `COMMIT:path` after commit, then the fresh clone):

| Set | Rows | Worktree | Index | Commit | Fresh clones (local, and GitHub with `autocrlf=true`) |
|---|---|---|---|---|---|
| Original baseline | 39 | pass | pass (within baseline) | pass | pass |
| Baseline stage (39 + 338) | 377 | pass | pass | pass | pass |
| Control files | 2 | pass | pass | pass | pass |
| Imports (890 + 81 + 22 + 2) | 995 | pass | pass | pass | pass |
| New byte-exact files | 171 | pass | pass | pass | pass |
| New LF text (`README.md`, `AGENTS.004.md`, `app/README.md`) | 3 | pass | pass | pass | pass |
| The new-files manifest itself | 1 | pass | pass | pass | pass |

These are per set and overlap (for example, the original 39 sit inside the 377). They aren't a count of unique files.

### #B-A04 Scratch exclusion and additive baseline: pass

**Tracked ignore rules, exactly three:**
- `/labs/bootstrap-preservation-pass01/clones/`
- `/labs/bootstrap-preservation-pass01/tests-tmp/`
- `/labs/bootstrap-git-bytes-pass01/scratch/`

**Nested repositories:** 32, all inside those folders, recorded by HEAD, branch and remote (`evidence/step02/baseline-capture/nested-repositories.tsv`) and never walked into. Five are Pack A clones; their remote archive refs identify them. The rest are test repositories. None is tracked.

**The additive baseline** (`evidence/step02/baseline-capture/additive-baseline-2026-10-26.tsv`) classifies every file:

| Class | Files | What happened |
|---|---|---|
| Original | 39 | committed |
| Additive | 338 | committed |
| Control | 2 | committed in the policy commit |
| Excluded scratch | 88 | ignored |
| Deferred | 40 | Pack B's two working labs, committed at the evidence boundary with their own manifest |

The 39-file manifest is unchanged. The new-files manifest leaves out its own bytes; those are recorded in `evidence/step07/manifest-self.tsv`.

### #B-A05 Evidence landing: done

- **Tracked with their source hashes:** the Pack A builder return, the Prime report, the Prime's JSON and check script (`returns/`), and the final `verify_remote.py` (`labs/bootstrap-preservation-pass01/`, sha256 `3d3eebf7…`, matching the addendum's inputs).
- **Pack A's original helper and tests** are kept as evidence. The new verifier (`gitbytes.py`) has its own source and tests.
- **The archive branches' helper doesn't implement the stored-blob check.** It's the version Pack A ran.
- **Recorded on `0410.imports` and `0501.bootstrap`.**

## Pack B

### #01 Refresh the baseline: pass

Before init: 460 files (39 original, 341 additive, 80 scratch), 25 nested repositories (all in scratch), no reparse point and no `.git`. All 995 import destinations were checked together, case-insensitively and for escapes, before any write.

### #02 Git in place: pass

- `git init -b workshop` ran in the existing folder, with origin `https://github.com/Amalgamour/Librarian.git`. Fetches went only into this repository.
- `workshop` was set to `14676ca`, the index emptied with `read-tree --empty`, and the empty tree committed. The 1,938 inherited paths showed as staged deletions; no file was written or deleted.
- The policy was committed, then the baseline. Nothing was broad-staged: every path came from an explicit NUL-separated list.
- **Stops along the way, all kept in `evidence/step02/attempts/`:**
  - the inventory refused the new `.git`, so an explicit after-init mode was added;
  - the attribute check refused the two LF control files, so they were classified as control;
  - the capture included the step's own output file, so Pack B's labs were deferred to the evidence boundary.

### #03 Imports: pass

**The import helper** (`labs/bootstrap-establish-pass01/import_blobs.py`) passes 6 tests (`evidence/step03/import-tests.txt`). Before any write, it refuses:
- case duplicates, and a directory spelled two ways;
- `..`, drive letters, reserved names and `.git`;
- an existing destination, even with identical bytes;
- a real blob from elsewhere in history ("provenance");
- a wrong hash.

It also refuses to restart without `--resume`, refuses a resume with other rows, and resumes correctly with the same rows.

**What was imported, from Git objects only:**

| Set | Rows | Where |
|---|---|---|
| Snapshots | 890 (688 originally minimum, 202 originally later) | `imports/source-tree/` |
| Selected copies | 81 (73 reference faces, 8 runtime candidates) | into the books; each byte-identical to its snapshot row |
| P1 decisions | 22 | `imports/director-decisions/`, from archive `e8b1a99` with their original relative paths |
| Claude's pass 02 files | 2 (manifest and collisions) | from archive `fe42b01` |
| Pack copies | 36 (the Pack B package, the addendum, 4 manifests) | `0501.bootstrap/` and `0410.imports/manifests/`, from the baseline commit |

**One stop:** the first index check crashed, because 995 paths on one command line exceeded Windows' length limit (`evidence/step03/attempt1-index-CRASH.txt`). The verifier was fixed and re-gated, and the commit resumed from the verified staged state.

No snapshot is in an executable lookup. No old stamp confers local approval.

### #04 Desk, books, work records: done as drafts (hand form)

**The desk tree:**

```text
lib-build/
  .gitattributes  .gitignore  README.md  AGENTS.004.md (draft)
  app/README.md                                   reserved, nothing implemented
  00.kernel/
    00.md  00.start.md  00.readme.md  00.live.md  (00.live.md derived)
    00.00.00.syntax/   00.001.md  + 17 reference faces (01.md)
    00.00.01.law/      00.001.md  + 56 reference faces (01.md)
                       0041.handoff  0062.role-director  0063.role-prime  0064.role-colab  0065.role-builder   (01.001.md)
                       0018.seqaddr/01.011.md  0050.band.structure/01.004.md  0057.bands/01.003.md
                       0300.band.compute/01.md
                       0302.run  0303.jobs  0304.check  0305.clerk  0307.face   (02.md card + inactive candidates)
    00.00.10.work/     00.md  0010.about  0011.contents  0014.design
                       0100.band.returns  0400.band.dev  0500.band.packs  0600.band.notes
                       0401.goal (01.md, 06.01.md)  0408.seats  0409.decisions  0410.imports
                       0501.bootstrap (01.md, 05.01.md, 05.02.md, pack/, addendum-001/)  0611.findings
  imports/  labs/  notes/  packs/  returns/
```

**The work pages:**
- **Contents** (`0011`) are generated from the folders: 13 pages, each listed exactly once.
- **Seats:** Director Matthew John Fisher; Prime Codex; Colab Claude; Builder unassigned. Pack execution is recorded separately from the seat.
- **Decisions:** 11 chat entries and 83 imported items (72 replies, all verified verbatim by `check_decisions.py`; 11 blank), each tagged as approved design, packing authorization, execution release, or seat assignment.
- **`README.md`** is the provisional entry and names everything that's missing.

### #05 Role and law drafts; candidates inactive: done as drafts

**Allocation.** Checked against every law path in the repository's history, including the old kernel, Grok's candidate kernel, the solo sample and retired faces:
- `0041`, `0062`–`0065` and the titles `handoff` and `role-*` are unused.
- `0300` is also used by a `0300.band` template in Grok's candidate kernel, which is another book (B-F1).

**The drafts:**
- **`0041.handoff`** covers: declared routes; Clerk validation and recording; hash-bound review; delivery identity and idempotency; explicit wait states; and durable results that survive a failed delivery.
- **The role pages** give inputs, responsibility, authority, outputs and escalation. Builder can't approve its own output. Colab independence doesn't require a different model family.
- **The amendments** take the next version from the full history: `0018` 009 and 010 → 011; `0050` 002 and 003 → 004; `0057` 001 and 002 → 003. The 010, 003 and 002 versions are the solo sample's chains, commit `317c06b`. Each amendment starts with its notes, and gives a disposition, destination and reason for every section. `check_amendments.py` confirms every section described as unchanged is byte-identical, and every source hash is the real one.
- **The runtime door** `0300.band.compute`, and the cards for `0302`, `0303`, `0304`, `0305` and `0307`: `runs:`, `uses:` and `args:` only, each naming an active file that doesn't exist.

**The candidates** keep their names and bytes:

| Candidate | sha256 (start) |
|---|---|
| `02.run.001.py` | `af207d4d` |
| `02.jobs.010.py` | `7b393085` |
| `02.lcheck.001.py` | `35129397` |
| `02.sentinel.001.py` | `985cc2b5` |
| `02.rules.001.toml` | `b40759f7` |
| `02.moves.001.toml` | `660ee0a3` |
| `02.clerk.009.py` | `678536e2` |
| `02.face.001.py` | `6760ea78` |

The stamps that still describe the rebuild are listed on `0410.imports`, as the next pass's work: the run module's stamp says PPPP 0202, and `face` has no stamp at all.

### #06 Orientation and checks

`labs/bootstrap-establish-pass01/evidence/step06/`

- **The canonical record** is `0401.goal/06.01.md`. Its schema is on `0410.imports`: 11 required keys, a fixed state list, LF only.
- **The renderer** (`render_live.py`) builds `00.kernel/00.live.md` from the record and the selection register. It names both inputs' hashes and its own. It is deterministic and runs nothing else.

| Check | Result |
|---|---|
| 1. Original hashes retained; additive baseline accounted for; old checkouts unchanged | pass |
| 2. 995 import rows at worktree and HEAD; 81 selected copies equal their snapshots; 22 P1 files equal the preservation manifest | pass |
| 3. Case, escape, existing-destination, provenance and hash refusals before any write; restart from the journal | pass (import tests 6/6; Pack A helper 19/20, 1 skipped) |
| 4. One desk and three books; no new unversioned law or syntax face under 0100; no active runtime file; no seated loader | pass |
| 5. Links resolve; contents match the folders | pass (7 markdown links; 173 code-formatted paths scanned, and the 27 that don't resolve were all reviewed as intentional: attribute patterns, historical paths, Git refs, page-relative folders, the reserved `.librarian/`, and this return) |
| 6. Two processes render identical bytes; a tampered view is refused and repaired without changing the record; a missing or malformed record is refused | pass (4/4; the first run's failure was my malformed test case, kept) |
| 7. A fresh clone on another path verifies the records and renders the view | pass: on drive C: from the local repository, and again from GitHub, both with `autocrlf=true` set before checkout |

Historical code was never run. The renderer and the tools are development tooling.

### #07 Commit, publish, return: done

- Exact named paths only, `Model:` lines on every commit.
- **Re-checked before the push:** baselines, imports, package integrity, and the old checkouts (`evidence/old-fingerprint-prepush.json`: unchanged).
- **Pushed `workshop` only**, and verified it in an independent GitHub clone.

**The old workspaces:** `D:\Git\Librarian` (HEAD `38a037ea`, 943 status entries, 679 hashed files) and `D:\Git\Librarian-rebuild` (`de3b8ebc`, 28 and 28) are unchanged from before Pack B through the push: HEAD, status, refs, stashes, worktrees and file hashes.

## Where things are

| What | Where |
|---|---|
| The original packs, unchanged | `packs/lib-build-bootstrap-pass01-2026-10-26/`, `packs/lib-build-pack-B-addendum-001-2026-10-26/` |
| Byte copies on the work book | `00.kernel/00.00.10.work/0501.bootstrap/pack/`, `…/addendum-001/` |
| This pack's record | `0501.bootstrap/05.02.md` (Pack A's is `05.01.md`) |
| Imports, the selection register, stamps, the custody policy, the record schema | `0410.imports` |
| Findings | `0611.findings`: F01–F05, A-F1, B-F1 to B-F3, and the older returns kept separate |
| Pack B tools and evidence | `labs/bootstrap-establish-pass01/`, `labs/bootstrap-git-bytes-pass01/` |

## What a worker can and cannot do now

**Can:**
- start at `README.md` and find the assignment, the goal, the seats, the decisions, the imports and the findings;
- regenerate and check `00.live.md`;
- verify any custody set with `gitbytes.py`;
- read every source byte-exact under `imports/`.

**Cannot:**
- run any runtime module;
- use a loader;
- route work through a Clerk;
- seat, approve or lock anything;
- treat an imported face or an old boot file as an instruction.

## Not done, skipped or open

- **Not claimed:** a fresh-model cold boot. Check 7 is a filesystem and process test only.
- **Skipped:** none in Pack B's checks. Pack A's symlink test stays skipped, because Windows wouldn't allow symlink creation.
- **Open findings:**
  - **B-F1:** the `0300` address also appears in Grok's candidate kernel.
  - **B-F2:** I read the "faces under 0100 start versioned" rule as covering the work book's function pages.
  - **B-F3:** `00.md` follows law `0051`'s one-line form and also carries the pointer.
  - **F01, F04 and F05** remain open.
  - **The 25 unreviewed lines** of rebuild returns `0101`–`0106`.
- **Environment:** the clones and test repositories stay in place, ignored. The test scratch for this pack is under `labs/bootstrap-git-bytes-pass01/scratch/`.

## Proposed next pack (not packed, not released)

Adapt the explicit loader and context, and execute the candidates against fixtures only:
1. A recorded context (book plus workflow space), never inferred.
2. Development selection by explicit candidate path and hash, with a test scope.
3. Normal mode refuses a missing active module and never picks the highest version.
4. Stamps adapted to their law addresses, with the code bytes unchanged below the stamp.
5. Fixtures for every refusal.

Then a Prime and Colab review, and, separately, the Director's activation decision. The old ready packs stay pending; they don't run just because they were copied.

One thing I'd have done differently: I'd have written the evidence boundary into the inventory before the first baseline run. Pack B's own output files tripped the capture twice before I separated them.
