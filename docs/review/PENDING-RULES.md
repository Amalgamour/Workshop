# Pending rules

Rulings that belong in a spec file but cannot be written there yet, because an open pass cites that file (t381u: a rule file never changes mid pass, only after review and before a new draft starts).

## t530u  -  band N6 holds worker pages

Status: pending. Apply to `docs/spec/seqAddr.md` as a versioned note (after section 11, the lab and stage bands) once 90.50.10.0705.05.01 is closed. That pass is returned, not closed, and its face 08 cites seqAddr.md section 11. Do not edit seqAddr.md, DIRECTOR-RULINGS.md or decisions.md while it is open.

Authority: t530u, docs/review/DIRECTOR-WORDS-t530.md. Verbatim: "N6 is where worker pages should live." "One page per worker" "The title should be the worker's name." And, for numbering: "First open slot after N600."

The rules, in plain words:

1. **Worker pages have their own band, `DD.SS.BB.0600-0699` (N6).** The band head `0600` is the door (seqAddr.md section 10, rule 4). Worker pages sit on `0601-0698`. `0699` is the band's continuation, not a worker page.
2. **One page per worker.** Not a shared workers page.
3. **The title is the worker's name, lowercase.** seqAddr.md:112: titles use lowercase letters, digits and hyphens, and start with a letter. So Grok-Check is titled `grok-check`. The exact name (including its capital letters) is kept in the page stamp and in the worker config. Exact-case titles would need a further ruling.
4. **The first page is the first open slot after 0600.** Today no 06NN page exists on packs or returns, so the first open slot is 0601.

Related, not an address rule: setup reports for a new worker chain on that worker's page (t530u Q1). Lab 0705 pass 05.02 is to fold that into the report-system design.
