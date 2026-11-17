#!/usr/bin/env bash
# P1 (init): init-page takes no lock (main.rs:90-93; cmd.rs:66-72). Two inits of one page, 50 times.
. "$(dirname "$0")/lib.sh"
R=$(mktemp -d /tmp/wf-triage-init-XXXX); export WF_ROOT=$R; bad=0; two=0
for i in $(seq 1 50); do P=7.7.7.$i
  "$WF" init-page $P --title a --person mat --prime pri --grant src/ --grant-ref t1 --as mat >/dev/null 2>&1 &
  "$WF" init-page $P --title b --person mat --prime pri2 --grant src/ --grant-ref t1 --as mat >/dev/null 2>&1 & wait
  [ "$(wc -l < $R/pages/$P/log.jsonl)" -gt 1 ] && two=$((two+1))
  "$WF" status $P >/dev/null 2>&1 || bad=$((bad+1))
done; echo "50 runs: page log got two init lines=$two, page left unreadable=$bad"
