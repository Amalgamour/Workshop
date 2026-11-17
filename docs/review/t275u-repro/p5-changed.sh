#!/usr/bin/env bash
# P5: the return's 'changed:' line is free text. And git diff --name-only hides the old side of a rename.
. "$(dirname "$0")/lib.sh"
new_env p5
echo "== (a) declared 'changed' says a file that was never touched; real change is src/a.rs"
draft src/a.rs true "w01: set a"; w pack $PG 1 --as pri >/dev/null; w claim $PG 1 --as bob >/dev/null
S=$(work 01 "create src/zzz.rs, delete src/b.rs" 'echo "a = 2" > src/a.rs' "w01: done - a"); ret 01 $S
jq -c 'select(.kind=="return")|{git_changed:.data.changed, declared:(.data.text|split("\n")[]|select(startswith("changed:")))}' $R/pages/$PG/log.jsonl
echo "== (b) rename: src/b.rs (OUTSIDE may touch src/c.rs) moved to src/c.rs"
w face-write $PG 06 --text "next" --as pri; draft src/c.rs true "w01: add c"; w pack $PG 2 --as pri >/dev/null; w claim $PG 2 --as bob >/dev/null
S=$(work 02 "create src/c.rs" 'git mv src/b.rs src/c.rs' "w01: done - c"); ret 02 $S
echo "git diff --name-only (what wf uses, git.rs:37):"; G diff --name-only main $S
echo "git diff --name-status --no-renames (the full truth):"; G diff --name-status --no-renames main $S
