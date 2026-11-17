#!/usr/bin/env bash
# Hash chain limits: (a) rewrite an old line and recompute every prev -> verify says ok.
# (b) a torn last line (interrupted append) -> every command, verify --fix too, is stuck.
. "$(dirname "$0")/lib.sh"
new_env chain; L=$R/pages/$PG/log.jsonl
echo "== (a) change the 04 goal at entry 2 from 'a works' to 'REWRITTEN', then recompute the chain"
python3 - "$L" <<'PY'
import json,hashlib,sys
p=sys.argv[1]; lines=open(p).read().splitlines(); prev="0"; out=[]
for l in lines:
    v=json.loads(l)
    if v["seq"]==2: v["data"]["text"]="REWRITTEN"
    v["prev"]=prev; s=json.dumps(v,separators=(",",":")); out.append(s); prev=hashlib.sha256(s.encode()).hexdigest()
open(p,"w").write("\n".join(out)+"\n")
PY
say verify $PG; say verify $PG --fix; grep -c REWRITTEN $R/pages/$PG/04.md
echo "== (b) torn append: half a line at the end"
printf '{"seq":5,"time":"2026-11-1' >> $L
say verify $PG; say verify $PG --fix; say status $PG
