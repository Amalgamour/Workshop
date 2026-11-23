# Lab 0703 | Seq storage

## 1. Options

Matthew asked, “What should be the design for the storage of it.” (t451u). This trial stores the same complete `.seq` page bytes three ways.

1. **Text with Git.** Store one UTF-8 `.seq` file per address. Stage the named files and save a snapshot in a fresh local Git repository. Reads open the working files directly. The committed blob gives a comparison point for a working-file edit.
2. **Append-only SHA-256 log.** Write one UTF-8 record per page. Each record starts with a line containing the address, the previous record’s SHA-256 and the body byte count. The body is the original multiline `.seq` text. The link hashes the exact preceding header and body. Verification starts from the zero genesis hash and compares the computed final hash with a separately retained trusted head, held in memory for this trial. This follows the previous-hash pattern in `wf`’s `src/log.rs:1–3` at `c09fa60c`.
3. **SQLite.** Store each address and its UTF-8 text in a primary-keyed table using bundled SQLite through `rusqlite`. Write all rows in one transaction with a rollback journal and `synchronous=FULL`. Read a page by its primary key.

## 2. Sample pages

The generator cycles through the 11 example shapes at `8e96151dbe9ff03a55e6838168033ba6bf5f4a4a` under `docs/spec/examples/`. It uses the SeqAddr law, Bob and timer examples, the five `face00/` files, the two `proposals/` files and `real/10.11.21.1001.bob.seq`. The shapes carry each example’s face and subface layout, event kinds and approximate byte size. They include a short registry, a long schema page, counted tasks, draft proposals, and multiline bodies followed by history.

The fixed seed `0x07035eed` varies target lengths and synthetic body text. The 1,000 pages have distinct synthetic addresses and total **4,265,680 payload bytes**, ranging from **228 to 29,929 bytes** per page. Every store receives the same bytes in the same order. The samples exercise storage and byte-for-byte retrieval. Grammar validity and production compressibility are outside the trial.

## 3. Results

Measured on Matthew’s PC with an AMD Ryzen 5 5600X3D (6 cores, 12 logical processors), Windows 10 Pro 22H2 (build 19045.6466), and the local NTFS `D:` volume. Release build with Rust 1.99.1, Git 2.55.0.windows.3 and bundled SQLite 3.50.2.

| Store | Write all (ms) | Read all (ms) | Read one (µs) | Stored bytes | Hand-readable | One-byte change | Write-once fit |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| Text + Git | 2,358.637 | 39.175 | 33.500 | 5,643,536 | Yes. Open the named `.seq` file in a plain editor. | The raw working-file blob hash differed from the committed blob at the same path. | Working files are editable. A retained trusted commit and controlled commit history give edits a trace. |
| Append-only SHA-256 log | 5.473 | 10.106 | 1,113.400 | 4,349,466 | Yes. Search the address in the plain-text headers and read the multiline page below it. | The chain failed at the next record, `91.07.03.0502`. A separate test found an edit to the last record by comparing against the trusted head. | Appending preserves prior records. Verification against a trusted head reveals changes to existing records and a missing suffix. |
| SQLite | 32.837 | 5.684 | 157.900 | 5,935,104 | Requires a SQLite reader to extract a page by address. | `PRAGMA integrity_check` returned `ok`. Comparing the retrieved payload’s SHA-256 with the retained original detected the edit. | A primary key rejects duplicate inserts. Normal updates and deletes can change history without a trace unless the writer records and protects it. |

The table uses medians over seven fresh stores per option. The store order rotates by round. A round times the initial write, one full read, then 21 fresh-handle reads of address `91.07.03.0501`, halfway through the log. Single-read latency is the median of all 147 lookups per option. Git write time includes initializing, creating files, staging and committing. The log writes via a buffered append handle. These write paths have different durability guarantees. Read times follow the writes with the OS cache left in place. Integrity checks run separately from the read timings. The log scans from the beginning for the selected address. SQLite opens a fresh read-only connection per read.

Stored bytes sum logical file lengths after the write. The Git count includes the working files and `.git` with loose objects. SQLite’s journal is gone after closing the committed database. The trusted comparison values used for the log and SQLite tamper checks are held outside the measured files. The counts exclude filesystem allocation overhead.

The tamper trial uses a separate fresh set of stores. It changes the same single ASCII byte in the middle page’s body in each case. Git compares it with the saved blob. The log recomputes its links and checks the saved head. SQLite reads back the changed text successfully, so an external content comparison is what exposes that edit.

## 4. Pick

**Codex proposal — use the append-only SHA-256 log as the authoritative store.** Axiom 6 asks for a visible new step whenever something changes while preserving the earlier steps. An append-only log keeps those steps in order with their original page bytes, and the check caught the edited record. Keeping a trusted head outside the file matters. Someone able to replace both the log and its trusted head can present a different history. The measured cost of a direct lookup is also higher in the unindexed log. A rebuildable address-to-offset index is a Codex proposal for a later trial. The authority and lineage rationale comes from `docs/spec/Axioms.md:23` at `8e96151d`.

`docs/spec/WRITE-ONCE.md` §§1, 4.3 and 4.10 give a separate requirement for retries. Matthew’s R37 rulings establish one append-only source of truth and a delivery ID whose content cannot change. Codex’s proposed fit is for the compute gate to save the writer-scoped delivery ID and the change together in one record, rebuild the receipt index on restart, return the first answer on a matching resend, and refuse a different payload under the same writer and ID. The bench tests storage and detectable edits. Recovery, concurrency, receipt replay and checkpoint custody need their own trials.

Use text with Git for browsable exports and review diffs. Use SQLite for indexed reads or a rebuildable view where primary-key lookups and transactions help.

## 5. How to rerun

From the `work` checkout root in PowerShell, with Rust, Git and a C toolchain for bundled SQLite on PATH.

```powershell
$env:CARGO_TARGET_DIR = Join-Path (Get-Location).Path 'labs/0703/target'
cargo test --manifest-path labs/0703/Cargo.toml
cargo run --locked --release --manifest-path labs/0703/Cargo.toml
```

The release command prints the corpus sizes, timing table and one-byte outcomes. Tests and benchmark use disposable directories under `labs/0703/target/`. A checker can rerun the tests without comparing timings across machines.
