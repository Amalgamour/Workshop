# Worker B, unit 2 findings (prima-0706-0502): episode preservation and recoverability

Scope: the frozen source room only (87 files). The room is a selected bundle, so "absent from the room" means the file can't be recovered from what was supplied. It does not prove the file is lost in the live book. Static reading plus one stdlib hash or presence check (probes/check_pointers.py, exit 0; output in probes/check_pointers.out). W = 00.kernel/00.00.10.work.

**Labels.** I keep two kinds of statement apart. *Source fact* means bytes I hashed or compared myself. *Builder/model claim* means a sentence written by the executor (Grok-1 or Grok-2 per the pages) or the reviewer (Codex Prime) that I could only read, not check.

## B2-01 The 0512 trace from 05.05 to 05.06 is recoverable from outcome to evidence, except for the two files where the finding was first written
- **fact:** The chain runs as follows. The 05.06 outcome is the review at W/0512.prime-review/05.06.md:32-61: workbook-review-id wbf38837cf0fa9c6b (:32), disposition accepted (:40), tests_passed true (:61). Its exact request is 05.06.md:9-12 ("Repair P3 from 06.08.md."). The original finding is the 05.05 review at 05.05.md:58, "P3#file-identity answered: Independent failure confirmed. Assigned bounded correction; not closed.", with the next action at :66. The correction is labs/review-report-pass03, with notes at 06.09.md:8-48. The evidence is evidence/build05.06: the known-failure fixture known-failures/identical-files-pass02.json has sha256 e72b2e2e0b8d8edb8510413eaefa6c7a07e47e442e72878680934de451eacabb, which equals the hash cited at 06.09.md:20, and the live report current-review/report.json has the counts cited at 06.09.md:44. Missing links: 06.08.md, where the request says P3 was raised, and evidence/prime-review05.05/independent-identical-files.json, the independent probe behind "Independent failure confirmed", are both absent from the room. 06.09.md:16 says both were in the 05.06 freeze manifest (evidence/pack05.06/source-manifest.json), which is also absent.
- **evidence:** 05.05.md:58, :66; 05.06.md:9-12, :32-61; 06.09.md:14-16, :20; probes/presence-0512.txt; probes/check_pointers.out.
- **method:** read; static hash check
- **severity and impact:** medium. The independent probe that turned P3 into a confirmed failure, which is Prime's reviewer evidence, can't be recovered from this room. Only the builder's own reproduction of it survives.
- **recommendation:** add 06.08.md, prime-review05.05/independent-identical-files.json and pack05.06/source-manifest.json to any preservation bundle for this episode.
- **label:** verified (presence and hashes); whether these files exist in the live book is unknown

## B2-02 The 05.05 and 05.07 artifact manifests named in the Return pointers are absent, so those episodes' evidence sets can't be checked
- **fact:** 05.05.md:34 cites build05.05/artifact-manifest.json (sha256 7e52850f…53af, 4864 bytes, 21 files). 05.07.md:31 cites build05.07/artifact-manifest.json (dfd5ea00…f4, 4977 bytes, 23 files). Neither is in the room. build05.05 holds only submission.md (its pointer hash matches), and build05.07 holds CONTRACT.md and submission.md (the submission pointer matches). The 05.05 review reason "All 21 manifest artifacts match." (05.05.md:53) and the 05.07 reasons and findings R1/R2 (05.07.md:55-56) therefore have no supporting evidence files in the room. 05.07 also names command logs, a test table and a no-write proof (05.07.md:27), and none are present. By contrast, the build05.06 manifest (14 files) and the 0521 build05.13 manifest (5 files) are present and every listed file hash-matches.
- **evidence:** probes/check_pointers.out (ABSENT for 05.05.md:34 and 05.07.md:31; MATCH for the other 6 pointers and all 19 manifest rows).
- **method:** static check
- **severity and impact:** medium for 05.05 and 05.07 recoverability. The 05.07 correction-required outcome (the dispatcher-pin blocker and the PENDING test, both already known) can be traced to its review text but not to its evidence.
- **recommendation:** supply both manifests and their listed files, or record that the room deliberately excludes them.
- **label:** verified

## B2-03 No Director quotation exists anywhere in these four episodes; "named Director invocation" is asserted but not recorded
- **fact:** Every review records "### Director text / none measured" (05.05.md:60, 05.06.md:51, 05.07.md:58, 0521/05.13.md:62). Each page header says "state: PREPARED; execute on named Director invocation" (05.05.md:6, 05.06.md:6, 05.07.md:6, 0521/05.13.md:6), but no page, submission or verification file in these episodes records the invocation itself: who, when, or the exact words. There is therefore no Director quotation to preserve here. The link from "prepared" to "invoked by the Director" is missing. The 0521 contract says explicitly that the synthetic authorization "is not a Director release and not live authority" (evidence/build05.13/CONTRACT.md:17).
- **evidence:** grep for "director" across W/0512.prime-review and W/0521.return-placement (output in this session's log, reproduced by `grep -rni director` on those folders).
- **method:** read and grep
- **severity and impact:** medium for provenance. Nothing in the room shows that execution was Director-invoked rather than self-started.
- **recommendation:** record the invocation (actor, timestamp, exact words, verbatim) on the page or in the evidence before the builder runs.
- **label:** verified (absence within the room)

## B2-04 The 05.06 live-report and suite claims are consistent with the retained evidence, but run provenance rests on builder-written files
- **fact:** Source facts: report.json and report-second.stdout are byte-identical (sha256 170028a6a6ee8817ac091d5e2c9642b8c250c32d6ac728fe89a554f526c8a06d, 29742 bytes each). report.json gives review w4c5ae945c250d823, state readable, stale false, observation coherent and stable, publication complete, disposition accepted, custody missing, authority none, 6 attention lines, declared 29 / 314945, measured 29 / 314945, addressed 31 / 329258, content 25 / 325080, physical unknown, intake 32 / 354914, hash_match 29. All of these equal the claims at 06.09.md:44 and summary.json. Builder claims: the exits (0 and 0), "empty stderr", "two processes", the Python version 3.14.0, the HEAD 960d20c5… and the branch "workshop" appear only in 06.09.md and verification.json. No stderr or exit file was retained for either process. author-suite.txt (125 bytes) holds only the unittest tail and "exit 0", with no command line, interpreter or timestamp.
- **evidence:** evidence/build05.06/current-review/*, author-suite.txt, verification.json:1-60, 06.09.md:40-44.
- **method:** static read of the JSON
- **severity and impact:** low. The content claims are verified, but the process claims rely on the builder's own records.
- **recommendation:** retain per-process stderr and exit files and the exact command line next to stdout.
- **label:** verified (content equality); builder claim (exits, stderr, interpreter, HEAD)

## B2-05 Builder-time "PENDING" and "accepted: false" statements sit beside later accepted reviews, and nothing marks them as superseded
- **fact:** 0521 evidence/build05.13/submission.md:12 and :28 say "accepted: false" and "Codex Prime review on `05.13.md` remains PENDING.", while 0521/05.13.md:48-51 records disposition accepted (review webe8f0a86f3de800). Likewise labs/review-report-pass03/PRIME-USE.md:3 says "accepted: false", yet it is a hash-matched member of the build05.06 manifest, and the 05.06 review (05.06.md:40) is "disposition: accepted". This also resolves my unit 1 B-08: the PRIME-USE statement predates the review. This is the same lifecycle pattern as the known pre-filing PENDING test assumption. I'm noting the preservation side only, not presenting it as a new test defect.
- **evidence:** paths and lines above; probes/check_pointers.out (PRIME-USE.md MATCH in the build05.06 manifest).
- **method:** read; static check
- **severity and impact:** low to medium. A reader who recovers only the evidence folder sees "accepted: false / PENDING" with nothing tying it to the later review.
- **recommendation:** keep the frozen bytes, and have the review or a pointer file name which evidence statements it supersedes.
- **label:** verified

## B2-06 The evidence for the 0521 05.13 accepted outcome lives in an external temp stamp; the in-book manifest holds only 5 files
- **fact:** The outcome is 0521/05.13.md:48-51 (disposition accepted, review webe8f0a86f3de800). Its reasons rest on "The retained child capture record says attempted true and writer_started false" (05.13.md:55) and on the N7 raw prepare (05.13.md:56). 06.26.md:35 places the official proof at `D:\librarian\temp\0521-0513\20261103T214834952429Z` (run report sha256 cf86f025…2514, 42532 bytes). 06.26.md:132 says "The child transcript is the writer-start evidence". verification.json cites a failure log (3361ed1c…) and an intent (13fc7c48…) by hash only. The in-book artifact manifest lists 5 files (06.26.md, CONTRACT.md, submission.md, verification.json, labs/connected-return-review-pass02/drive.py), and all hash-match. The run report, child transcript, failure log, raw prepare stdout and fixture roots are not among them and are not in the room. The run report's own `door_result.writer_started` is true (a sentence-presence flag, 06.26.md:86), so the retained report alone would mislead without the external transcript.
- **evidence:** 05.13.md:35, :48-56; 06.26.md:35, :86, :132; verification.json (sha256 290c4d4d…a0f6, matches the submission's citation); probes/check_pointers.out.
- **method:** read; static check
- **severity and impact:** high for recoverability. The decisive writer-start evidence is preserved only by hash, in a folder named "temp" outside the book.
- **recommendation:** copy the run report, the child transcript and failure log, and the N7 raw prepare stdout and stderr into evidence/build05.13, and add them to the manifest, before any temp cleanup.
- **label:** verified (absence and hashes in the room); builder claim (the contents of the external files)

## B2-07 The 0521 original request link (06.25.md) and the freeze manifest are absent; their content survives only as a builder paraphrase
- **fact:** 05.13.md:9 says "Finish I1/I2 on 06.25 and isolate I3" and "Verify evidence/pack05.13/source-manifest.json". Neither 06.25.md nor pack05.13/source-manifest.json is in the room. The only account of 06.25 is the builder's line at 06.26.md:23: "06.25.md was read first. It accepts the bounded native N5 proof and requires I1, I2, and an I3 diagnosis." The "earlier bare-init failure" that 05.13.md:9 tells the builder to note is evidenced only by its contract retelling (CONTRACT.md:15) and by neighbor stamps under `D:\librarian\temp\0521-0512` (06.26.md:25), which are external.
- **evidence:** paths and lines above; presence check in this session's log.
- **method:** read; presence check
- **severity and impact:** medium. The trace from outcome to request is intact, but the request to original finding hop rests on a model claim.
- **recommendation:** include 06.25.md and the pack05.13 source manifest in the preservation bundle.
- **label:** verified (absence); builder claim (06.25 content)

## B2-08 Every execution root cited across both episodes is a fixed Windows path outside the room, so no run can be re-observed from these files
- **fact:** 06.09.md:20 retains the pass02 known failure at `D:/librarian/temp/0512-0506-report/...`. A copy is in the room (build05.06/known-failures/identical-files-pass02.json), and its sha256 e72b2e2e…cabb equals the hash the page cites. That is the one external artifact I could confirm was preserved. 0521 runs use `D:\librarian\temp\0521-0513\<stamp>` (CONTRACT.md:23), and copied review launchers read fixed `D:\Git\lib-build` (06.26.md:116, :132). Per COMMON.md I did not build or simulate any D: tree. This is recorded as evidence, not retried.
- **evidence:** lines above; `sha256sum` of identical-files-pass02.json (session log).
- **method:** read; sha256sum
- **severity and impact:** medium. Replay depends on the original Windows host and its temp folders.
- **recommendation:** record, per episode, which external roots were copied into the book and which remain host-only.
- **label:** verified

## Ambiguous states (summary)
- 05.06 and 05.13 are "accepted", while their frozen evidence says "accepted: false" or "PENDING" (B2-05). Both are true at different times, but nothing links them.
- 05.13: prime_review_effective is "attention", tests_passed is true, and custody is "missing" on the page, while the submission says custody "pending" (05.13.md:44, :72-73; submission.md:20). These are two different custody vocabularies for the same pass, and the difference is unexplained in the room.
- 05.05 and 05.07 outcomes are correction-required, and their follow-up pages (06.07, 06.10, 06.11) are absent, so whether each correction closed can't be told from the room. For 05.05 (P3), closure is visible through 05.06. For 05.07 (R1/R2), it is unknown.

## Checks skipped
- I did not open labs/review-report-pass03/report.py or tests beyond the manifest hash match. That was code review, which is outside this audit.
- I did not read 06.26.md in full (lines 1-35 and the grep hits only), because of the time limit.
- I did not inspect hostile/current-changed.json content.
