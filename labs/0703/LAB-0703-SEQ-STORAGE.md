# Lab 0703 | Seq storage

## 1. Options

Matthew asked, “What should be the design for the storage of it.” (t451u). Pass 05.02 revisits the three whole-page stores after Claude’s cross-check found unequal write durability, unequal tamper tests and no update workload. The earlier trial is preserved in commit `05cd58a`. Claude’s findings are recorded in the 0703 page log, entries 9–11.

- **Text with Git.** One UTF-8 `.seq` file per page. Git commits the initial batch and then the updated page. The working files serve reads. Git’s committed blobs preserve both versions.
- **Append-only SHA-256 log.** One record per version. A header holds the page address, preceding hash and byte count. The page body follows, then the SHA-256 of that header and body. Each record’s checksum lets the verifier name the edited record. The previous-hash link follows the pattern in `src/log.rs:1–3` at `c09fa60c`.
- **SQLite.** Bundled SQLite through `rusqlite`. One row per revision, keyed by page address and version. Normal writes insert a revision in a transaction and latest reads use the version key. SQLite can also update or delete a historical row.

## 2. Sample pages

The generator cycles through the shapes of the 11 examples in `docs/spec/examples/` at `8e96151dbe9ff03a55e6838168033ba6bf5f4a4a`. The shapes include short registries, a long schema page, counted tasks, draft proposals, and multiline payloads with history. Titles use lowercase words and hyphens (`docs/spec/seqAddr.md:280–281`).

The fixed seed `0x07035eed` produces 1,000 synthetic pages with **4,268,680 payload bytes**, from **231 to 29,932 bytes** per page. After the initial batch, every store receives a second version of `91.07.03.0501`. Its marker changes from `v1` to `v2`. Full and single reads must return the latest bytes, and the history check must still see both versions. The workload exercises byte storage and retrieval using the shape of the examples. It leaves grammar validation and production compressibility open.

## 3. Results

Rerun on Matthew’s PC with an AMD Ryzen 5 5600X3D (6 cores, 12 logical processors), Windows 10 Pro 22H2 (build 19045.6466), and the NTFS `D:` volume. Release build with Rust 1.99.1, Git 2.55.0.windows.3 and bundled SQLite 3.50.2.

| Store | Write all (ms) | Update one (ms) | Read all latest (ms) | Read one latest (µs) | Stored bytes after update | Write durability | Hand-readable |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Text + Git | 2,285.212 | 58.703 | 37.328 | 32.300 | 5,674,813 | OS-buffered, `core.fsync=none` | Open the working `.seq` file. Use Git for old versions. |
| Append-only SHA-256 log | 5.294 | 0.054 | 14.350 | 2,372.000 | 4,418,578 | OS-buffered, writer flushes its buffer | Search the address in the text headers and read the body. |
| SQLite | 17.876 | 1.459 | 19.322 | 160.600 | 5,951,488 | OS-buffered, `synchronous=OFF` with a DELETE rollback journal | Use a SQLite reader to extract a page and its versions. |

The common write setting acknowledges OS-buffered writes without an explicit durable flush. These timings give no power-loss guarantee. The write paths still have different transaction and crash-recovery behavior. The table takes medians over seven fresh stores per option with rotating store order. Each round writes all pages, updates one page, reads all latest pages, and opens fresh handles for 21 lookups of the updated page. Timed reads follow the writes with the OS cache left warm and exclude verification. The unindexed log scans to the end to find the latest record. Git timings include staging and commits. Stored bytes sum file lengths after the update, including working files and `.git` for Git. NTFS allocation overhead is excluded.

### Same edits, same outside reference

For each store, the trial retains the same independent SHA-256 of the chosen address and its two known versions in order. The address and version bodies are length-prefixed, and the version count is included. The audit checks stored history and checks the same sequence with the served latest page substituted. The reference stays in benchmark memory and covers the one audited page.

1. On a fresh pair of versions, change exactly one ASCII byte (`S` to `s`) in the latest version’s marker. Edit the Git working file, the log payload and the SQLite database file. All three serve the same altered page.
2. On a separate fresh pair, change the same byte in version 1 and keep version 2 unchanged. Rebuild the Git commit chain in the disposable repository and point its local ref at the replacement history. Rewrite the log and recompute its checksums and links. Update the old SQLite row.

| Store | Latest-byte edit, native check | Older version rewrite, native check | Shared outside reference |
| --- | --- | --- | --- |
| Text + Git | Working file differs from HEAD’s blob. The committed history still matches. | `git fsck --full --no-reflogs` and the working-file comparison pass on the replacement history. | Detects both edits. |
| Append-only SHA-256 log | Checksum fails at record 1001, `91.07.03.0501`. | All rebuilt checksums and links pass. | Detects both edits. |
| SQLite | `PRAGMA integrity_check` returns `ok`. | `PRAGMA integrity_check` returns `ok`. | Detects both edits. |

All three stores keep the first version when the normal update path writes a second. A writer with access to replace the stored history can also make each native check pass. The Git trial checks the active history. Reflogs and unreachable objects may still aid recovery in the disposable repository. The common external reference detects the replacement within its scope. The log tests also reject a partial final record and a removed middle record. Removing a complete suffix can leave the remaining chain valid, so auditing a whole log needs an independently retained head or equivalent checkpoint for the whole log.

## 4. Pick

**Codex proposal — carry the append-only SHA-256 log forward as the candidate for whole-page version history.** It spent the least time on both the initial batch and the single update, used the fewest bytes after the update, and exposed the raw edit at the altered record while keeping the history readable in a text editor. The latest lookup was the slowest. A rebuildable address-to-offset index is worth testing. The equal tamper comparison gives the log no advantage against a coherent rewrite. Every option needs a trusted external reference for that threat.

Git’s commit chain is a real append-only candidate if a protected writer publishes only descendants and a reader verifies against an independently trusted commit. It offers direct file reads and existing diff tools, and can version files at face granularity. In this trial Git had the fastest single-page read, but its initial and per-update costs were much higher and its history required Git tooling to inspect. SQLite remains a candidate for an indexed read view or for separately testing transactional history under a controlled writer.

Axiom 6 requires a visible new step without rewriting older steps (`docs/spec/Axioms.md:23`). Matthew’s R37 adopts one append-only source of truth and a delivery ID whose content cannot change (`docs/spec/DIRECTOR-RULINGS.md:192,195–196`). `docs/spec/WRITE-ONCE.md` §§1, 4.3 and 4.10 explain retry handling, saving the receipt alongside the change, and rebuilding receipt lookup from the history. This lab checks page versions and tamper evidence. It leaves receipt replay, durable acknowledgements and recovery for later trials.

The proposal conflicts with the storage authority in `docs/design/SEQ-FILE-PLAN.md:246` and `:251`. The plan makes small files authoritative and specifies a folder per page with a file per face or counter under R31, item 7. A whole-page log as the source of truth would change that decision. The measured workload has no face-level reads or updates and cannot settle the plan’s granularity. The next comparison under that plan would test versioned face files and face-level reads, including Git’s commit chain, under a durable write setting. Any move to an authoritative log and rebuildable face files would need Matthew’s decision.

## 5. How to rerun

Run from the `work` checkout root in PowerShell, with Rust, Git and a C toolchain for bundled SQLite.

```powershell
$env:CARGO_TARGET_DIR = Join-Path (Get-Location).Path 'labs/0703/target'
cargo test --manifest-path labs/0703/Cargo.toml
cargo run --locked --release --manifest-path labs/0703/Cargo.toml
```

The test suite covers round trips and latest-version reads for each store, both common tamper trials, and the log’s edited record, partial tail and removed middle record. The release command prints the timing and tamper results. Both commands use disposable stores under `labs/0703/target/`.
