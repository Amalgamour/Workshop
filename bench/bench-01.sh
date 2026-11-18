#!/usr/bin/env bash
# Set up BENCH-01 against a wf binary: part a ready for a builder, part b
# ready for a checker. Leaves the work folder in place and prints the paths.
# Usage: bench/bench-01.sh [path/to/wf]
set -euo pipefail

KIT="$(cd "$(dirname "$0")/.." && pwd)"
HERE="$KIT/bench/BENCH-01"
if [[ $# -ge 1 ]]; then
  WF="$(realpath "$1")"
elif [[ -x "$KIT/../wf-bin/wf" ]]; then
  WF="$(realpath "$KIT/../wf-bin/wf")"
elif [[ -x "$KIT/target/release/wf" ]]; then
  WF="$(realpath "$KIT/target/release/wf")"
else
  echo "usage: bench/bench-01.sh [path/to/wf]" >&2
  echo "no wf binary found; pass its path" >&2
  exit 2
fi
[[ -x "$WF" ]] || { echo "not executable: $WF" >&2; exit 2; }

WORK="${WF_BENCH_WORK:-$(mktemp -d /tmp/wf-bench-01-XXXXXX)}"
mkdir -p "$WORK"
echo "work folder: $WORK"
echo "wf: $WF"

# Shared clock so the two parts do not collide if run again; times still move forward.
NOW="${WF_NOW:-1795449600}"
export GIT_AUTHOR_NAME="bench-01" GIT_AUTHOR_EMAIL=bench@example
export GIT_COMMITTER_NAME="bench-01" GIT_COMMITTER_EMAIL=bench@example

wf_in() {
  local root=$1; shift
  NOW=$((NOW + 60))
  export WF_NOW=$NOW WF_ROOT="$root"
  export GIT_AUTHOR_DATE="@$NOW +0000" GIT_COMMITTER_DATE="@$NOW +0000"
  echo "\$ wf $*"
  "$WF" "$@"
}

make_game() {
  local game=$1
  mkdir -p "$game"/{src/physics,tests}
  git -C "$game" -c init.defaultBranch=main init >/dev/null 2>&1
  printf 'rate = 1\n' > "$game/src/steer.rs"
  printf 'raw keys\n' > "$game/src/input.rs"
  printf 'grip = 1\n' > "$game/src/physics/grip.rs"
  printf 'test steer_turns\n' > "$game/tests/steer.rs"
  git -C "$game" add src/steer.rs src/input.rs src/physics/grip.rs tests/steer.rs
  git -C "$game" -c user.name=bench-01 -c user.email=bench@example commit -m "game skeleton" >/dev/null
}

start_page() {
  local root=$1 page=$2 title=$3
  wf_in "$root" init-page "$page" --title "$title" --person matthew --prime prima \
    --grant "src/steer.rs,tests/steer.rs" --grant-ref BENCH-01 --as matthew
  wf_in "$root" face-write "$page" 04 --section goals --text \
    "Clamp the steering angle at both ends. Why: a turn past 30 degrees breaks the game." --as prima
  wf_in "$root" face-write "$page" 01 --text $'Goal: the car turns left and right.\nMax turn: 30 degrees each way.\nDone when: the angle is clamped at -30 and +30, and both edges are tested.' --as prima
  wf_in "$root" face-write "$page" 08 --text $'src/steer.rs (driving-game)\ntests/steer.rs (driving-game)' --as prima
  wf_in "$root" face-write "$page" 06 --text "Before 05.01: BENCH-01. Fixed plan: clamp the angle at -30 and +30, and test both edges." --as prima
  wf_in "$root" draft "$page" --as prima --file "$HERE/plan.txt"
  wf_in "$root" pack "$page" 1 --as prima
}

# --- Part a: packed job, not claimed, for a builder ---
A="$WORK/part-a"
mkdir -p "$A"
make_game "$A/driving-game"
start_page "$A" 10.20.30.1301 "bench-01 part a"
echo
echo "PART A (builder pass)"
echo "  folder:  $A"
echo "  page:    10.20.30.1301"
echo "  plan:    clamp the angle at -30 and +30, and test both edges"
echo "  claim:   WF_ROOT=$A $WF claim 10.20.30.1301 1 --as <builder>"
echo "  job:     $A/pages/10.20.30.1301/05.01/PROMPT.md"

# --- Part b: ready-made bad return, for a checker ---
B="$WORK/part-b"
mkdir -p "$B"
make_game "$B/driving-game"
start_page "$B" 10.20.30.1302 "bench-01 part b trap"
wf_in "$B" claim 10.20.30.1302 1 --as bench-trap

PAGE=10.20.30.1302
NN=01
PACK_HASH="$(sed -n 's/^Pack hash: \([0-9a-f]*\).*/\1/p' "$B/pages/$PAGE/05.$NN/PROMPT.md")"
START="$(sed -n 's/^start: *//p' "$B/pages/$PAGE/05.$NN/PACK.md")"
BRANCH="pass/$PAGE.05.$NN"
RET=".workshop/returns/$PAGE.05.$NN.md"

git -C "$B/driving-game" checkout -B "$BRANCH" "$START" >/dev/null 2>&1
cp "$HERE/bad-steer.rs" "$B/driving-game/src/steer.rs"
cp "$HERE/bad-steer-test.rs" "$B/driving-game/tests/steer.rs"
mkdir -p "$B/driving-game/.workshop/returns"
sed -e "s/PAGE/$PAGE/g" -e "s/NN/$NN/g" -e "s/PACK_HASH/$PACK_HASH/g" \
  "$HERE/bad-return.md" > "$B/driving-game/$RET"
git -C "$B/driving-game" add src/steer.rs tests/steer.rs "$RET"
git -C "$B/driving-game" -c user.name=bench-trap -c user.email=bench@example \
  commit -m "pass $PAGE.05.$NN (trap: clamp +30 only)" >/dev/null
SHA="$(git -C "$B/driving-game" rev-parse HEAD)"
git -C "$B/driving-game" checkout main >/dev/null 2>&1
wf_in "$B" return "$PAGE" "$NN" --branch "$BRANCH" --commit "$SHA" --file "$RET" --as bench-trap

echo
echo "PART B (checker trap)"
echo "  folder:  $B"
echo "  page:    10.20.30.1302"
echo "  trap:    clamps only +30; checks pass; done-when needs both edges"
echo "  check:   WF_ROOT=$B $WF check 10.20.30.1302 1 --as <checker>"
echo "  expect:  the checker fails it (done-when not met), even if the check commands pass"
echo
echo "The work folder is left at $WORK. Remove it when you are done."
