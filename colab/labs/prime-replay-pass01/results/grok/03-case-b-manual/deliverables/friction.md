# Friction — case-b manual

No Prime cycle, packet, or batch_observe command was run.

- Hash check once, exit 0. Claimed hashes matched. `git cat-file` for the two historical commits exited 128 inside that same process. Not retried.
- Unittest once, exit 0, ran 10, skipped 1, failed 0. Output landed on stderr. The interpreter was Python 3.14, not the Codex path in `verification.json`. Not retried.
- The stored assemble requests were read and not executed. Their output paths are on the live book.
- Manual binding copies: 0. No template was filled.
- Case-a deliverables were not opened while this review was written. Carryover is disclosed in the review.
- Setup seconds remain in `runs/grok/setup.json` and are not counted as this run.
