#!/usr/bin/env bash
# SeqAddr: wf takes any label as a page id (page.rs:91-94) and numbers passes past 98.
. "$(dirname "$0")/lib.sh"
R=$(mktemp -d /tmp/wf-triage-seq-XXXX); export WF_ROOT=$R
for id in hello 1.2.3.4 10.20.30.12345 99.99.99.9999; do printf '%-16s ' $id; "$WF" init-page $id --title t --person mat --prime pri --grant src/ --grant-ref t1 --as mat 2>&1 | head -1; done
new_env seq; for i in $(seq 1 100); do draft src/a.rs true "w01: x$i"; done
w status $PG | grep -oE "05\.(01|98|99|100) " | sort -u | tr '\n' ' '; echo
ls $R/pages/$PG/05.md >/dev/null && grep -oE "^## 05\.(99|100) " $R/pages/$PG/05.md
