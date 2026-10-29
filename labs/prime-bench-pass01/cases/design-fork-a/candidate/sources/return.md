# Return — 05.08

## Did
- Copy never overwrites. Both designs below satisfy F1 and F2.

## Blocked
The exit code for an identical replay.

## Need
Option 1: identical replay exits 0 (idempotent; safer for retries).
Option 2: identical replay exits 2 (one meaning for every existing destination).
The workflow consumer currently treats any non-zero exit as a failure.
I implemented neither; current code still exits 2 for every existing destination, as before.
