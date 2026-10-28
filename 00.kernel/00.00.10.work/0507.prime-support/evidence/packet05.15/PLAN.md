# PLAN — recorded Prime boot packet candidate (0507.prime-support 05.15)

Author: claude-opus-5-5, Colab, packet preparation only. Date: 2026-10-28.

**Purpose (limited).** One prepared snapshot packet for *orientation at a fixed source cut*. It is not a fresh Prime boot, not an exam, not an answer set and not a current-live assignment service.
- No model is called.
- No answers, check or judge.
- The model label is `unassigned-preparation-only`.
- The real candidate's identity and the final packet cut are bound later, in a test the Director releases. They are not edited into this attempt.

## Source cuts (two, kept distinct)

| cut | commit | what it is |
|---|---|---|
| packet source | `d3b6ad3e55beb1ec0bd5acbb114e6e66fd66c4e9` | every committed ref in the packet is read at this commit |
| brief observation | `6d18d182535df8dc60b698c585b04cd276c5df85` | the accepted brief (realbrief05.14) describes the reader's observations at this earlier commit, plus Prime-supplied coordination |

At the packet cut, three of the brief's pages are byte-identical to the brief's source: 0504/05.17, 0508/05.15 and 0507/05.12. Two changed after the brief: 0504/05.18 and 0508/05.16. The packet carries 0504/05.18 at d3b6ad3, so its text may show later facts than the brief's "unknown". Both identities are kept, and neither is relabelled as current.

## Tools (accepted, pinned; no changes)

`app/librarian.py boot-prepare` and `boot-show` go through `app/boot_tools.py` with `app/prime-boot.json`. These are the pins:

| file | sha256 |
|---|---|
| prime_boot.py | `54b23484f9e0812db92a623a8588175702682ebe14f8b0b915111daf51a91534` |
| prime_support.py | `700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70` |
| clerk_adapter.py | `2f30ba751f78ec9f7d2995739bebde0e3b6509eeab35ae29a9078385ff33f8d4` |
| check_book.py | `fc16d2f68a3645050b6766ce18ce55f8169a0e2bad52d3392b4d059c629073a4` |
| return_capture.py | `8f3da5c651f6924fca6dedb0b95da7d181eb58884dc030dd9cbc3d8b6a5b15ac` |
| return_inspect.py | `947915febaa5918f56b6be03c81840c030d081fcab9a3bead2cd660973a9999b` |

The front door files have these pack hashes: librarian.py 694d44ae…, boot_tools.py 409901b1…, prime-boot.json 5f8498cd….

## Selection, inside 12 refs and 128 KiB

prime_boot orders the refs as: the four mandatory refs, then the member inspections, then `packet[]`.

| # | ref | bytes at the cut | why |
|---|---|---|---|
| 1 | `00.md` (book entry) | 98 | mandatory |
| 2 | `0011.contents/01.051.md` | 9,952 | mandatory (the contents face the entry points to) |
| 3 | `0408.seats/01.md` | 2,031 | mandatory: the role record (Prime is Codex; this candidate is not seated) |
| 4 | `0401.goal/06.01.md` | 545 | mandatory: the canonical assignment, stale (0504/05.06 `accepted`), kept as it is |
| 5 | member `0145.real-reader-brief-0514` | about 4,090 | **live** custody of the brief's capture, kept apart from commit facts |
| 6 | `realbrief05.14/brief.txt` | 1,912 | the accepted brief |
| 7 | `realbrief-input05.14/coordination-provenance.json` | 2,425 | where the brief's decisions came from: Prime-supplied interpretation, not authentication |
| 8 | `realbrief-input05.14/coordination.json` | 3,056 | the exact supplied decisions behind the held, accepted-not-terminal and unknown outcomes |
| 9 | `prime-review05.14/review.md` | 1,745 | Prime's acceptance of the brief, with its scope limits |
| 10 | `0504.app-entry/05.17.md` | 6,885 | the source of one **held** outcome |
| 11 | `0508.return-capture/05.15.md` | 6,533 | the source of the **accepted-without-terminal** outcome |
| 12 | `0504.app-entry/05.18.md` | 6,188 | the source of one **unknown** outcome as of the brief. It changed after the brief's cut. |

The estimated total is about 45.5 KB of 131,072 bytes. The tool's own counts are authoritative, and verification.json records them.

**Excluded on purpose.** These are not omissions by the tool, because they were never requested.
- `realbrief05.14/results.json` (172,747 bytes): it exceeds the cap on its own. It stays an exact external evidence link, with sha256 `d308733fa245…`, in the pack and in verification.json.
- `0507.prime-support/05.12.md`: the second held page, with the same pattern as 05.17. The brief lists it.
- `0508.return-capture/05.16.md`: the second unknown page, with the same pattern as 05.18, and also changed after the brief. The brief lists it.
- Grok-2's 0508/05.17 acceptance plan: unreviewed, so not used.

## Registry and request

- **registry.json:** `prime-support-registry` v1, with one repository and three lanes (0504, 0507, 0508). Canonical is `0401.goal/06.01.md`, bound to lane 0504.app-entry, the lane its current_work names. No Clerk jobs.
- **request.json:** `prime-boot-request/1`, with the selection above; role `Prime`; model `unassigned-preparation-only`; limits 12 and 131072.
- **Records root:** a new external temp directory, with attempt `p1`.

## Expected

- Prepare is `prepared`, with 12 refs, 0 absences and 0 omissions, inside the caps, and stable. If the outcome is `partial` or `failed`, it is kept as it is and explained.
- Prime_support's status attention and conflicts come from live repository state at run time. They are recorded as they are.
- `show` reports `prepared; awaiting answers; not oriented`. No file 20 or later exists.
