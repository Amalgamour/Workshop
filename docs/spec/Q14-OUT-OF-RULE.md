# Q14 draft: a page with an out-of-order entry still loads

Build stage, no Director ruling yet (Q14). Branch `q14-draft`, from `merge-rehearsal`. Not merged, not pushed.

## Rule (the proposed answer to question 14)
- Every new write must still follow the order rules. Nothing changes there.
- An entry already in the log that breaks the order (any rule in `Page::order`) does not make the page unreadable any more. It is:
  - kept in the log, byte for byte;
  - not folded into the page state, so it cannot change what the next command sees;
  - shown as `log entry N is out of order: <rule>; the page is out of rule at entry N: only wf resume or a Prime note (face-write 06) may be written (build stage, no Director ruling yet, Q14)` on `status`, `board`, `observe` and `verify`, and on the book board line for that page.
- While a page has one, only `wf resume` and a Prime `face-write 06` note may be written. Every other write (draft, pack, claim, return, check, signoff, close, halt, grant, set-prime, other faces, answer, elevate, `observe --record`) is refused with `refused, nothing written: ...` and the same line.
- `verify --fix` still reprints views (it writes no log entry).
- Still unreadable: a broken hash chain, and a log whose entry 1 is not the init (there is no page to show).

## Where in the code
- `src/page.rs`: `Page.out_of_rule`, `out_of_rule_lines()`, `apply()` records instead of failing, `add()` gate.
- `src/lib.rs`: command gate before dispatch (so a refusal names the rule, not a missing pass part); `verify` and `observe` print the lines.
- `src/status.rs`, `src/board.rs`: the lines in status, the board's ATTENTION block and the book board.

## Tests
- 43 unit tests and 112 e2e tests pass (155 in total; there were 153 before).
- New test `q14_h4_page_loads_out_of_rule_and_takes_only_resume_or_a_prime_note` uses `tests/fixtures/h4/log.jsonl`, a copy of Tester's `scratch/tester-3001/h4` page log.
- New test `q14_clean_page_shows_no_out_of_rule_line`.
- 9 order-rule tests changed: the reads now exit 0 and show the line, instead of exit 1 and "cannot be read". Their names still say "unreadable"; I left them as they were to keep the diff small.
- The three real pages (copies) still verify ok with 85, 49 and 37 entries.

## Open for the Director
1. Should the mark ever clear (for example a Prime note that cites a ruling), or stay for good? The draft keeps it for good, so a page with one only ever takes resume or notes. That matches the proposed answer's words, but by axiom 6 it still blocks the page for good. A likely next step: a person-only `wf accept-out-of-rule <page> <N> --ref tNNNu` entry.
2. Should the out-of-rule entry be skipped (this draft) or applied? Skipping means a forged entry cannot steer the next command (axiom 1).
