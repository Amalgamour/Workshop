# Shared setup for the t275u triage repros. Uses the wf built from 693e608.
set -u
WF="${WF:-/workspace/workshop-build/scratch/wf-triage/wf693}"
PG=1.2.3.4
new_env() {  # $1 name -> sets R (root), page ready with 04, 01, 06
  R=$(mktemp -d /tmp/wf-triage-$1-XXXX); export WF_ROOT=$R
  mkdir -p $R/game/src; G init -q -b main
  echo "a = 1" > $R/game/src/a.rs; echo "b = 1" > $R/game/src/b.rs
  G add .; G commit -q -m start
  w init-page $PG --title t --person mat --prime pri --grant src/ --grant-ref t1 --as mat >/dev/null
  w face-write $PG 04 --section goals --text "a works" --as pri
  w face-write $PG 01 --text $'Goal: a.\nDone when: a is 2.' --as pri
  w face-write $PG 06 --text "read 04" --as pri
}
G() { git -C $R/game -c user.name=t -c user.email=t@t "$@"; }
w() { "$WF" "$@"; }
say() { echo "\$ wf $*"; "$WF" "$@" 2>&1; echo "  [exit $?]"; }
draft() {  # $1 may touch, $2 checks, $3.. job lines
  local may=$1 checks=$2; shift 2
  { echo "repo: game"; echo "start: main"; echo "outcome: a = 2"; printf '%s\n' "$@"
    echo "may touch: $may"; echo "checks: $checks"; echo "stop if: b must change"; } > $R/pack.txt
  w draft $PG --file $R/pack.txt --as pri >/dev/null
}
hash_of() { sed -n 's/^Pack hash: \([0-9a-f]*\).*/\1/p' $R/pages/$PG/05.$1/PROMPT.md; }
# work NN "changed text" "edit cmd" job-lines...  -> prints sha
work() {
  local nn=$1 ch=$2 edit=$3; shift 3; local name=$PG.05.$nn
  G checkout -q -B pass/$name main; (cd $R/game && eval "$edit")
  mkdir -p $R/game/.workshop/returns
  { echo "pack: $(hash_of $nn)"; echo "done: work"; echo "changed: $ch"; echo "noticed: none"; printf '%s\n' "$@"
    echo "proof: tests"; echo "not done: none"; echo "unprompted: none"; echo "overflow: none"; } > $R/game/.workshop/returns/$name.md
  G add -A; G commit -q -m work; G rev-parse HEAD; G checkout -q main
}
ret() { say return $PG $1 --branch pass/$PG.05.$1 --commit $2 --file .workshop/returns/$PG.05.$1.md --as bob; }
