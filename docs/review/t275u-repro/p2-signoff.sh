#!/usr/bin/env bash
# P2: w02 is blocked, the check commands pass, an elevation is open. Prime signs off 'passed'.
. "$(dirname "$0")/lib.sh"
new_env p2
draft src/a.rs "grep -q 2 src/a.rs" "w01: set a to 2" "w02: also change b"
w pack $PG 1 --as pri >/dev/null; w claim $PG 1 --as bob >/dev/null
S=$(work 01 "modify src/a.rs" 'echo "a = 2" > src/a.rs' "w01: done - a is 2" "w02: blocked - b is outside may touch")
ret 01 $S
say check $PG 1 --as cat | grep -E "check 05|check ok|job w|exit"
echo "-- open elevations before signoff:"; jq -c 'select(.kind=="elevate"or.kind=="answer")|{seq,kind,data}' $R/pages/$PG/log.jsonl
say signoff $PG 1 --outcome passed --as pri
say close $PG 1 --as pri | grep -E "outcome|cards|w0|exit"
echo "-- signoff event:"; jq -c 'select(.kind=="signoff")|.data' $R/pages/$PG/log.jsonl
echo "-- elevation still unanswered after close:"; w status $PG | grep -iE "question|elev|w02" 
