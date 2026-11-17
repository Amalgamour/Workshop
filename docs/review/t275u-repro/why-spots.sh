#!/usr/bin/env bash
# Why-required: consequential choices that take no reason.
. "$(dirname "$0")/lib.sh"
new_env why
draft src/a.rs true "w01: a"; w pack $PG 1 --as pri >/dev/null
draft src/a.rs true "w01: a again"
say pack $PG 2 --overlap-ok 1 --as pri | grep -E "Pack hash|exit"
say set-prime $PG other --as mat
jq -c 'select(.kind=="pack" and .data.pass==2)|.data|{pass,overlap_ok}' $R/pages/$PG/log.jsonl; jq -c 'select(.kind=="prime")|.data' $R/pages/$PG/log.jsonl
