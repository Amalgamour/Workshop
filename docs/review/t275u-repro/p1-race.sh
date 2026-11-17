#!/usr/bin/env bash
# P1: two claims of the same pass. Process B is paused AFTER Page::load (main.rs:103)
# and BEFORE Lock::take (main.rs:144) by turning one view file (07.md) into a FIFO,
# which render::edited (main.rs:104) blocks on. Process A then claims and finishes.
# B is released with the right 07.md text, takes the now-free lock, and appends.
. "$(dirname "$0")/lib.sh"
new_env p1
draft src/a.rs true "w01: set a"; w pack $PG 1 --as pri >/dev/null
D=$R/pages/$PG; cp $D/07.md $R/07.real; tail -1 $D/log.jsonl | jq -c '{seq,kind}'
mv $D/07.md $R/07.keep; mkfifo $D/07.md
( "$WF" claim $PG 1 --as bob > $R/b.out 2>&1; echo "B exit $?" >> $R/b.out ) &   # B: loads, then blocks on the FIFO
sleep 1; mv $D/07.md $R/07.fifo; cp $R/07.real $D/07.md                          # B still holds the FIFO open
echo "-- A claims while B is paused:"; say claim $PG 1 --as alice
cat $R/07.real > $R/07.fifo; wait                                                 # release B
echo "-- B:"; cat $R/b.out
echo "-- last 3 log lines (seq, actor, kind, prev):"; tail -3 $D/log.jsonl | jq -c '{seq,actor,kind,prev:.prev[:12]}'
echo "-- any later command:"; say status $PG; say verify $PG
