# PACKET-ENTRY — how to read this prepared snapshot (0507.prime-support 05.15)

**What this is.** A *prepared* recorded-boot packet candidate for orientation at one fixed source cut. It was prepared by the accepted prime_boot, through the app front door. Nobody has booted from it.

**What this is not.**
- It contains no answers, no grades and no evaluator text.
- It grants no work authority, release, acceptance or seat.
- Its model label is `unassigned-preparation-only`. The actual candidate, and the final packet cut, are bound later in a test the Director releases.

## 1. Find the packet

The attempt directory is `p1` under the external records root recorded in `records.json` (`provenance.records_root`). The packet is `09.packet.json`.
- It holds 12 refs and 45,460 raw bytes, inside 12 refs and 131,072 bytes.
- It has 0 absences and 0 omissions.
- `19.prepare-outcome.json` says `prepared`, and `10.stability.json` says `stable: true`.
- Every file is also kept in `records.json` as base64, with its sha256 and bytes.

## 2. Identify the source cut

- **Committed refs.** Every `commit-blob` ref (R01-R04 and R06-R12) is the exact text of that path at commit `d3b6ad3e55beb1ec0bd5acbb114e6e66fd66c4e9`. Each ref's `sha256` binds its bytes.
- **The workspace moved on.** At prepare time, HEAD was `b4f3048…`, not the cut (`04.git.json`: head_is_commit false). A ref's `live` field compares the worktree file now: R01 `00.md` *differs*, and the rest are `same`. Live bytes are never in the packet text.

## 3. Find the brief, and its own, earlier cut

- **The brief.** R06 is the accepted brief, `realbrief05.14/brief.txt`.
- **The brief's earlier cut.** It describes reader observations at commit `6d18d182535df8dc60b698c585b04cd276c5df85`, not at d3b6ad3. Its held, accepted-not-terminal and unknown states come from the Prime-supplied coordination in R08, whose provenance is R07: "Prime-supplied interpretation for a read-only rehearsal, not authentication or Director approval". Its acceptance, and the limits on it, are in R09.
- **Pages behind the brief:**
  - R10, 0504/05.17: held;
  - R11, 0508/05.15: accepted without terminal;
  - R12, 0504/05.18: unknown as of the brief.
  R10 and R11 are byte-identical to the brief's sources. **R12 changed after the brief's cut** (commit c1a11dc), so its text may show later facts than the brief's "unknown". Read the brief as being *as of 6d18d18*.
- **Kept out of the packet.**
  - `realbrief05.14/results.json` is 172,747 bytes, over the cap. It is an exact external link: sha256 `d308733fa245…`, in pack05.15 and in verification.json.
  - The brief's other two pages, 0507/05.12 and 0508/05.16, were left out to stay inside the caps. 0508/05.16 also changed after the brief.

## 4. Live custody versus source facts

- **Live custody.** R05 (`live-inspection`, `member:0145.real-reader-brief-0514`) is the pinned inspector's report, read **at prepare time**. It is not a commit blob. It shows status `complete`, with receipt `62a745580ba75f601b24530ca93f2a887b1b99d31653fcfeea705197cc6cfc5d`, and stage 10 read the same thing again. Custody is not approval.
- **Live status.** `07.status.json` is prime_support's view of the *live* repository at prepare time. It is not the cut. It shows 69 attention items (unsupported legacy headings, unbound reviews and review-needed) and **no conflicts**.

## 5. Unresolved, on purpose (gaps, not resolutions)

1. **The canonical record is stale.** R04, `0401.goal/06.01.md`, still names `0504.app-entry/05.06.md` as `accepted`, waiting on 0506/05.04. The registry binds it to lane 0504, the lane it names, and in that binding status reports no conflict. **That doesn't make the record current.** The desk-versus-parallel-lane question (05.11 DEC-1 and DEC-5) is still undecided.
2. **Brief versus packet cut.** The brief is as of 6d18d18, and two of its pages changed after it. A reader must not treat the brief as current live work.
3. **The brief's unknowns stay unknown.** 0504/05.18 and 0508/05.16 had release and claim unknown at the brief's cut. Nothing here resolves them.
4. **Nothing is completed.** The accepted-without-terminal item (R11) and the held items stay open. A review saying "accepted" is not a terminal decision.
5. **Seats.** R03 seats Codex as Prime. This candidate holds no seat. The exercise label `Prime` is a request field, not an appointment.
6. **Pending dependency.** Grok-2's cold-Prime acceptance plan (0508/05.17) is unreviewed and is not used here. The final exam will be reconciled with it after Prime reviews it.
7. **Not yet bound.** The candidate's identity, its session, the final cut, and whether a later packet rebuild is needed.
