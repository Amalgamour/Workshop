#!/usr/bin/env bash
# P3: face 01 changes after pack; check reports the NEW done-when, not the packed one.
. "$(dirname "$0")/lib.sh"
new_env p3
draft src/a.rs "grep -q 2 src/a.rs" "w01: set a to 2"
w pack $PG 1 --as pri >/dev/null; w claim $PG 1 --as bob >/dev/null
echo "-- packed done_when:"; jq -r 'select(.kind=="pack")|.data.done_when' $R/pages/$PG/log.jsonl
say face-write $PG 01 --text $'Goal: a.\nDone when: a is 3 and b is 9.' --as pri
S=$(work 01 "modify src/a.rs" 'echo "a = 2" > src/a.rs' "w01: done - a is 2"); ret 01 $S >/dev/null
say check $PG 1 --as cat | grep -E "check 05|done when|exit"
