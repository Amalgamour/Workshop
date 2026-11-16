# Prototype results: the .seq small-file storage

WORKING PATH by Tester, not a ruling.
A throwaway prototype of SEQ-FILE-PLAN.md at 6dbe53c.
Code: /workspace/seq-proto (not in the repo). 316 lines of Rust.
Nothing in the repo was changed.

## What it is

- One folder per page. One file per face inside it.
- Faces 00 and 01 are compact (binary records with a length).
- Face 04 is plain text (R27). It is kept the Google way (R29):
  - 04.chg: a log of small changes (replace lines a..b).
  - 04.snap: a full copy every 16 changes.
  - 04.md: the current view, for people to read.
- Face 09 (09.log) is the page log. Only the compute appends to it.
  Each line has a chain: chain = SHA-256(previous chain + line).
- signposts.log holds band and book signposts, also chained.
  - A band line holds only the changed row, and a full line every
    64 of that band's own writes (K = 64).
  - A book line holds only the changed band, full every 64 writes.
  - Each page also has a small `sig` file (the page signpost).
- Boot: takes an OS folder lock, checks every chain, checks every
  face against its fingerprint, rebuilds 04 from its change log,
  and compares the signposts with the 09 logs.
- Before each write: checks file length and last chain against
  memory. Write order: face piece, 09 line, page, band, book.

## Numbers

Machine: 8 vCPU "Intel Xeon Processor" (virtual machine).
Disk: virtio /dev/vdb, ext4, 128 GB; disk type not known.
Cold = guest page cache dropped (sync; drop_caches, with sudo).
The host may still cache; that cannot be seen from inside.
Release build. Times are best of a few runs, or p50/p99 as named.

Book sizes used:

| book | writes  | pages | files  | real size | on disk |
|------|---------|-------|--------|-----------|---------|
| 1k   | 1,000   | 250   | 1,502  | 1.1 MB    | 7.2 MB  |
| 10k  | 10,000  | 2,500 | 15,002 | 11 MB     | 72 MB   |
| 100k | 100,000 | 9,000 | 54,173 | 89 MB     | 284 MB  |

Boot (full chain check, every file read), seconds:

| book | warm (3 runs)       | cold (3 runs)       |
|------|---------------------|---------------------|
| 1k   | 0.015, 0.014, 0.012 | 0.077, 0.066, 0.137 |
| 10k  | 0.182, 0.130, 0.149 | 0.637, 0.619, 0.592 |
| 100k | 1.046, 1.058, 1.007 | 2.455, 2.483, 2.452 |

One lookup (book -> band -> page -> face), microseconds:

| book | warm p50/p99 | cold first 200 | cold single x40 | reads |
|      | (20,000)     | p50 / p99      | p50 / max       | max   |
|------|--------------|----------------|-----------------|-------|
| 1k   | 21 / 36      | 92 / 329       | 325 / 468       | 24    |
| 10k  | 31 / 63      | 100 / 573      | 622 / 5,071     | 82    |
| 100k | 49 / 90      | 215 / 1,047    | 251 / 641       | 99    |

- "Cold single": caches dropped before each one lookup.
- Most reads seen: 99. The plan's bound is 2K + 3 = 131. Holds.

Append (one face write plus log and signposts), microseconds:

| book | no fsync p50/p99 | fsync p50/p99 | after cold boot |
|      | (3,000 writes)   | (300 writes)  | no fsync p50/p99|
|------|------------------|---------------|-----------------|
| 1k   | 55 / 108         | 422 / 818     | 54 / 94         |
| 10k  | 61 / 163         | 449 / 3,055   | 65 / 102        |
| 100k | 74 / 154         | 479 / 2,081   | 80 / 150        |

- A cold append does not exist here: the boot check reads every
  file first, so the first append is already warm.
- Signposts cost about 380 bytes per write (38 MB per 100k).

## Break tests

(a) Crash in the middle of a write
- kill -9 during heavy writes, fsync on and off: boot passed.
  (kill -9 keeps the OS cache, so it is not a power cut.)
- Crash after the face piece: boot cut the orphan bytes. Good.
- Crash after the 09 line: boot saw "log ahead of signposts" and
  wrote fresh signposts. Good.
- Crash after the band line, before the book line: boot PASSED,
  but the next read raised a false alarm ("does not match its
  fingerprint"). The read walked an old book line to old rows.
- Crash after 04.md, before the 09 line: boot called it a HAND
  EDIT and parked the text as 04.pending. A false alarm.
- Cut the last signpost line by hand: cut and removed. Good.
- Cut a 09 line by hand: HALT (signposts name a later write). Good.

(b) Edits behind the compute's back
- Hand edit to 04.md: found at boot, and at read time. The logged
  version stays live; the edit is kept as 04.pending (a draft).
  Not booked: who made it is unknown.
- One byte changed in 01.dat: HALT at boot (fingerprint).
- One letter changed in 09.log: HALT at boot (chain).
- One letter changed in signposts.log: HALT at boot (chain).
- Forge: change 01 data, fix its fingerprint, re-chain 09.log:
  HALT (the page signpost disagreed).
- Same forge, then empty signposts.log and the page sig: ACCEPTED.
  Boot rebuilt every signpost and reported 250 quiet "crash"
  findings. The chain has no secret, as the plan says.

(c) Forks
- Copy the whole book, write to both: both boot fine. Nothing
  tells them apart. Only their last chains differ.
- Copy a page folder to a new page number (0009 -> 0950):
  ACCEPTED as page 0950. No file inside a page names its address.

(d) Other
- Second writer while the compute runs: REFUSED (folder lock).
- Outside tool appending to 09.log while the compute writes: the
  compute REFUSED its next write to that page. Boot then refused.
- Race between check and write: in 2 of 20 tries the compute's
  line went in after an outside line. The write was reported OK.
  It was caught only at the next write or boot. The OS lock is
  advisory: a tool that ignores it is not stopped.
- Small files: 6 files and 1 folder per page. On disk is 3 to 7
  times the real size (4 KB blocks). 9,000 pages = about 63,000
  inodes. This disk has 2,048,000; fine, but it adds up per book.

## Top findings

1. Speed is fine. 100k writes, 9,000 pages: lookup 49 us warm,
   under 1.1 ms cold (p99); append 74 us, or 479 us with fsync;
   boot 1.0 s warm, 2.5 s cold.
2. The book line must be the commit point. A crash between band
   and book lines leaves a stale path that boot does not see.
   Fix: at boot, drop band lines after the last book line, or
   write a fresh book line.
3. Write the 04 current view after the 09 line, not before.
   Otherwise a crash looks like a hand edit.
4. Pages and books do not know their own address. Copies, forks
   and a full re-chain are accepted. Fix: start each 09 chain from
   the page address (and a book birth id). Make "all signposts
   missing" a halt that asks a person, not a quiet repair.
5. The check-then-write race is real (2 of 20). The lock and the
   length check catch it late. A write can be reported OK on a
   file an outside tool has touched.

## What does not match the plan, or is undefined in it

- Chain: defined for one file. With small files there are many
  files. I chained signposts.log and each 09.log apart. A chain
  over the whole book is not defined.
- Hash: the plan's C7 says the git blob (SHA-1 or SHA-256 form,
  open); its example says "sha256:". I used SHA-256 of the bytes.
- 04 current view file (04.md): not in the plan; needed so people
  can read and edit 04. Its write order is not defined.
- Book line as commit point: not stated (Step 11).
- Small change format for 04: not designed. I used a line range.
- Full copy cadence for 04: a builder setting; I used 16.
- "New piece in a new file (or new lines)": I used new lines in
  one append-only file per face.
- Taking in a hand edit: who made it has no source. Parked only.
- Page address inside page files: not in the plan.
- Locks (R30), exports, links, and C11-C14: not built.

## Not measured

- Power loss. kill -9 is not a power cut; fsync order is not
  tested by it.
- Real cold disk: the host's cache could not be dropped.
- Disk type: virtio reports "rotational", which says nothing.
- Books over 100k writes or 10,000 pages.
- Many readers at once; the export file; git blob hashing.
