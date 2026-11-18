# Bounds - old and new source capacity

accepted: false

The rejecting check on the frozen 0512/05.09 record is as_list(sources) against MAX_LIST = 24 in labs/prime-review-pass02/prime_review.py. The same function still bounds holds, answers, review_passes, gaps, and the other non-source lists. strict_json still refuses a document above MAX_DOC = 262144. MAX_TEXT = 12000 still bounds prose and an inline source record. MAX_INDEX = 12 still bounds form cuts. Form can exit 0 with finding index-context-bounded while every emitted book source is still present.

| Bound | Old module | Successor |
| --- | --- | --- |
| unique generated sources, 24 | records | records, and the report matches the old module on the saved 24-source input |
| unique generated sources, 25 | refuses `limit sources` | records |
| unique generated sources, 32 | refuses `limit sources` | records |
| unique generated sources, 33 | refuses `limit sources` | refuses `limit sources: 33 sources exceeds supported limit 32; split the return so one record binds at most 32 sources` and leaves the review PENDING |
| holds, 25 | refuses `limit holds` | refuses `limit holds` |
| document bytes above 262144, with 22 sources | refuses `input: input exceeds 262144 bytes` | same message |

Measured 0512/05.09: 39 intake rows, 30 unique book paths, 29 emitted sources, pretty record 125955 bytes. Roles: book artifact 28, book artifact-manifest 1, book assignment 1, book submission 1, code artifact 8. The artifact-manifest role is the book path that is not emitted. Code-root rows are excluded by the book-root filter. Inline record text is present on 22 sources and null on 7.

Measured 0522/05.14: 31 intake rows, 21 unique book paths, 20 emitted sources, pretty record 62200 bytes. That return is inside the old source limit. The candidate recorded it. Separate publish stopped because the copied review section is already occupied.

32 is the smallest power of two above the measured 29 emitted sources. The successor does not promise an unbounded list. A later return above 32 sources, or a pretty record above 262144 bytes, stops at the matching refusal. Rollback to pass02 refuses the 29-source return at 24 again.
