#!/usr/bin/env bash
# P1 without any trick: two plain claims started together, 100 times on fresh pages.
. "$(dirname "$0")/lib.sh"
new_env p1loop; draft src/a.rs true "w01: set a"
broken=0; both=0; one=0; lockref=0
for i in $(seq 1 100); do
  P=9.9.9.$i; cp -r $R/pages/$PG $R/pages/$P
  w pack $P 1 --as pri >/dev/null 2>&1 || { echo "pack fail"; break; }
  "$WF" claim $P 1 --as alice >$R/a 2>&1 & "$WF" claim $P 1 --as bob >$R/b 2>&1 & wait
  n=$(grep -c "^claimed 05" $R/a $R/b | awk -F: '{s+=$2} END{print s}')
  if ! "$WF" status $P >/dev/null 2>&1; then broken=$((broken+1)); fi
  [ "$n" = 2 ] && both=$((both+1)); [ "$n" = 1 ] && one=$((one+1))
  grep -q "another wf command" $R/a $R/b && lockref=$((lockref+1))
done
echo "100 runs: one claim won=$one, BOTH claims 'won'=$both, log left broken=$broken, lock refusals seen=$lockref"
