# Friction — case-b assisted

- Read once, exit 1, `observation-failed: reader exit 2`. Wrapper stderr empty. Not run again as its own command.
- Packet once, exit 0. Custody complete. Artifact checks none.
- Hash once, exit 0. Three files match the manual route.
- The template binding was copied once into `out/decision-case-b.json`. `receipt_sha256` left null. Manual binding copies: 1.
- Record once. `end.json` exit 2. `refused: observation failed: reader exit 2`. The tool result's process code was 1; the operation file says 2. Not retried.
- Inspect once, exit 0, reviews empty.
- Day once, exit 0. Its implementation calls `read()` when `--registration` is set, so the reader ran again inside that process and was not journalled as a second read. Day was not repeated. Inspect ran in parallel and is absent from the day listing.
- No `batch_observe` command on this route. No edit of the assistance tree or the subject.
- The manual review was already saved and was not rewritten.
