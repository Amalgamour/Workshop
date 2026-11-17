#!/usr/bin/env bash
# P4: delete a face file and a pack file; make one unreadable. verify still says every view matches.
. "$(dirname "$0")/lib.sh"
new_env p4
draft src/a.rs true "w01: set a"; w pack $PG 1 --as pri >/dev/null
D=$R/pages/$PG
rm $D/01.md $D/05.01/PACK.md; chmod 000 $D/04.md
echo "-- after rm 01.md, rm 05.01/PACK.md, chmod 000 04.md:"; ls $D $D/05.01 | tr '\n' ' '; echo
say verify $PG
echo "-- a write command is not refused either, and quietly reprints only what it can:"
say face-write $PG 06 --text "note" --as pri
ls $D/01.md $D/05.01/PACK.md 2>&1; chmod 600 $D/04.md
echo "-- for contrast, an edited file IS caught:"; echo x >> $D/02.md; say verify $PG
echo "-- the failed face-write still wrote its log entry (the event landed, the print did not):"
wc -l < $D/log.jsonl; tail -1 $D/log.jsonl | jq -c '{seq,kind}'
