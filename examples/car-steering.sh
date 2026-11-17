#!/usr/bin/env bash
# Runs the SAMPLE-PAGE car steering example (EXAMPLE values) through wf, end to end.
# Everything under examples/pages/ is printed by wf from each page's log.jsonl.
# Usage: examples/car-steering.sh [path/to/wf]   (default: target/release/wf)
set -euo pipefail
KIT="$(cd "$(dirname "$0")/.." && pwd)"
WF="$(realpath "${1:-$KIT/target/release/wf}")"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
export WF_ROOT="$WORK" WF_NOW=1795449600   # Mon 23 Nov 2026 16:00 UTC (EXAMPLE clock)
export GIT_AUTHOR_DATE="@1795449600 +0000" GIT_COMMITTER_DATE="@1795449600 +0000"
export GIT_AUTHOR_NAME="model A" GIT_AUTHOR_EMAIL=a@example GIT_COMMITTER_NAME="model A" GIT_COMMITTER_EMAIL=a@example
wf() { WF_NOW=$((WF_NOW += 60)); export GIT_AUTHOR_DATE="@$WF_NOW +0000" GIT_COMMITTER_DATE="@$WF_NOW +0000"; echo "\$ wf $*"; "$WF" "$@"; }
try() { if wf "$@"; then echo "!! expected a refusal"; exit 1; else echo "   (refused, as the example expects)"; fi; }
G() { git -C "$WORK/driving-game" -c init.defaultBranch=main "$@" >/dev/null 2>&1; }
P=10.20.30.1201; Q=10.20.30.1211

# The work repo (EXAMPLE game). Checks are plain shell so they run anywhere.
mkdir -p "$WORK/driving-game"/{src/physics,tests}; G init
cd "$WORK/driving-game"
echo "rate = 1" > src/steer.rs; echo "raw keys" > src/input.rs; echo "grip = 1" > src/physics/grip.rs
echo "test steer_turns" > tests/steer.rs
G add .; G commit -m "game skeleton"
cd "$WORK"

# Return file for pass NN of page $1, with given job lines.
ret_file() { local page=$1 nn=$2; shift 2; local f=".workshop/returns/$page.05.$nn.md"
  local hash; hash=$(sed -n 's/^Pack hash: \([0-9a-f]*\).*/\1/p' "$WORK/pages/$page/05.$nn/PROMPT.md")
  mkdir -p "$WORK/driving-game/.workshop/returns"
  { echo "# Return $page.05.$nn"; echo "pack: $hash"; echo "done: $DONE"; echo "changed: $CHANGED"
    echo "noticed: ${NOTICED:-none}"; printf '%s\n' "$@"; echo "proof: commit on the pass branch; checks run locally"
    echo "not done: ${NOTDONE:-none}"; echo "unprompted: none"; echo "overflow: none, the job was small"; } > "$WORK/driving-game/$f"
  echo "$f"; }
# Worker: branch from start, apply edit command, add return, commit, ping.
work() { local page=$1 nn=$2 edit=$3; shift 3
  local start; start=$(sed -n 's/^start: *//p' "$WORK/pages/$page/05.$nn/PACK.md")
  G checkout -B "pass/$page.05.$nn" "$start"; (cd driving-game && eval "$edit")
  local f; f=$(ret_file "$page" "$nn" "$@"); G add -A; G commit -m "pass $page.05.$nn"
  local sha; sha=$(git -C driving-game rev-parse HEAD); G checkout main
  wf return "$page" "$nn" --branch "pass/$page.05.$nn" --commit "$sha" --file "$f" --as model-a; }
pack_file() { cat > "$WORK/pack.txt"; echo "$WORK/pack.txt"; }

echo "== Page $P: steering. Codex, then Designer, then Prima hold Prime."
wf init-page $P --title steering --person matthew --prime codex --grant "src/steer.rs,src/input.rs,tests/steer.rs" --grant-ref t300u --as matthew
wf set-prime $P designer --as matthew
wf set-prime $P prima --as matthew
wf face-write $P 04 --section goals --text "The car steers with the arrow keys; never past 30 degrees; feels smooth. Why: steering is the first thing a player feels." --as prima
wf face-write $P 01 --text $'Goal: the car turns left and right with the arrow keys.\nMax turn: 30 degrees. Turn rate: 2 per frame.\nDone when: the steer checks pass and the angle is clamped at 30.' --as prima
wf face-write $P 02 --text $'on each frame:\n  angle = angle + rate * key\n  angle = clamp(angle, -30, 30)' --as prima
wf face-write $P 08 --text $'src/steer.rs (driving-game)\ntests/steer.rs (driving-game)' --as prima
try face-write $P 04 --section responses --text "prime cannot write the person's responses" --as prima

echo "== 05.01: steer at rate 2 and clamp (passes)"
wf face-write $P 06 --text "Before 05.01: read 04 goals; no earlier pass." --as prima
wf draft $P --as prima --file "$(pack_file <<'X'
repo: driving-game
start: main
axioms: 2,8,9
outcome: arrow keys turn the car; max 30 degrees
overview: first feel of the game; see 04
w01: steer left and right at rate 2
w02: clamp the angle at 30 degrees
may touch: src/steer.rs, tests/steer.rs
checks: grep -q "rate = 2" src/steer.rs; grep -q clamp src/steer.rs
stop if: the turn needs a physics change
X
)"
wf pack $P 1 --as prima
wf claim $P 1 --as model-a
try claim $P 1 --as model-b
DONE="steer at rate 2, clamp at 30" CHANGED="modify src/steer.rs" NOTICED="a 1-frame tap gives a 2-degree twitch" \
  work $P 01 'printf "rate = 2\nclamp(-30, 30)\n" > src/steer.rs' "w01: done - rate 2" "w02: done - clamp_angle"
try check $P 1 --as model-a
wf check $P 1 --as checker-c
try signoff $P 1 --outcome passed --as designer
wf signoff $P 1 --outcome passed --as prima
wf close $P 1 --as prima
G merge --no-edit pass/$P.05.01   # accepted work goes live (wf v0 does not merge; T1 open)

echo "== 05.02: rate 3 and a dead zone (blocked; w02 needs src/input.rs)"
wf face-write $P 04 --section responses --text "feels too stiff." --as matthew
wf face-write $P 04 --section decisions --text "D-a: rate 2 to 3. Links: 05.01, the stiff response." --as prima
wf face-write $P 01 --text $'Goal: the car turns left and right with the arrow keys.\nMax turn: 30 degrees. Turn rate: 3 per frame.\nDone when: the steer checks pass and the angle is clamped at 30.' --as prima
wf face-write $P 06 --text "Before 05.02: 05.01 passed; 04 says too stiff; D-a rate 3." --as prima
wf draft $P --as prima --file "$(pack_file <<'X'
repo: driving-game
start: main
axioms: 2,8,9
outcome: steering feels less stiff; taps under 50 ms do nothing
overview: you said "feels too stiff" (04)
w01: rate 2 to 3 (decision D-a)
w02: ignore taps under 50 ms (dead zone)
may touch: src/steer.rs, tests/steer.rs
checks: grep -q "rate = 3" src/steer.rs
stop if: the tap length lives outside may touch
X
)"
wf face-write $P 04 --section responses --text "tapping still twitches." --as matthew
try pack $P 2 --as prima
wf face-write $P 06 --text "Re-read 04: tapping still twitches. Same jobs; re-pinned." --as prima
wf draft $P --pass 2 --file "$WORK/pack.txt" --as prima
wf pack $P 2 --as prima
wf claim $P 2 --as model-a
DONE="rate 3" CHANGED="modify src/steer.rs" NOTDONE="w02: tap length comes from src/input.rs" \
  work $P 02 'printf "rate = 3\nclamp(-30, 30)\n" > src/steer.rs' "w01: done - rate 3" "w02: blocked - tap length comes from src/input.rs, which is outside may touch"
wf check $P 2 --as checker-c
wf status $P
wf signoff $P 2 --outcome blocked --as prima
wf close $P 2 --as prima
G merge --no-edit pass/$P.05.02   # w01 accepted goes live
wf answer $P "$(grep -n '"kind":"elevate"' "$WORK/pages/$P/log.jsonl" | head -1 | cut -d: -f1)" --text "D-b: frame widened to src/input.rs (inside grant t300u), in 05.03" --as prima

echo "== 05.03: smoothing with the wider frame (left open, in progress)"
wf face-write $P 04 --section decisions --text "D-b: add a dead zone and input smoothing; frame widened to src/input.rs." --as prima
wf face-write $P 01 --text $'Goal: the car turns left and right with the arrow keys.\nMax turn: 30 degrees. Turn rate: 3 per frame.\nTaps under 50 ms do nothing (dead zone).\nDone when: the steer checks pass and the angle is clamped at 30.' --as prima
wf face-write $P 06 --text "Before 05.03: 05.02 blocked on src/input.rs; D-b widens the frame." --as prima
wf draft $P --as prima --file "$(pack_file <<'X'
repo: driving-game
start: main
axioms: 2,8,9
outcome: taps under 50 ms do nothing; holds feel smooth
overview: 05.02 w02 blocked; frame widened (D-b)
w01: smooth the key input in src/input.rs
w02: ignore taps under 50 ms
may touch: src/steer.rs, src/input.rs, tests/steer.rs
checks: grep -q smooth src/input.rs; grep -q "rate = 3" src/steer.rs
stop if: the turn needs a physics change
X
)"
wf pack $P 3 --as prima
wf claim $P 3 --as model-a
wf status $P
wf observe $P --as observer-o

echo "== Page $Q: the harder paths (SAMPLE-PAGE-PATHS)"
wf init-page $Q --title "steering hard paths" --person matthew --prime prima --grant "src/steer.rs,src/input.rs,tests/steer.rs" --grant-ref t300u --as matthew
wf face-write $Q 01 --text $'Goal: the turn rate eases in.\nDone when: the steer checks pass and the angle never passes 30.' --as prima
wf face-write $Q 06 --text "Before 05.01: start from live main." --as prima
cat > "$WORK/ease.txt" <<'X'
repo: driving-game
start: main
outcome: the turn rate eases in
w01: make the turn rate ease in
may touch: src/steer.rs, tests/steer.rs
checks: grep -q "clamp(-30, 30)" src/steer.rs
stop if: the turn needs a physics change
X
echo "-- Path 1: the check fails twice, Prime signs off failed, rework is a new pass"
wf draft $Q --file "$WORK/ease.txt" --as prima
wf pack $Q 1 --as prima
wf claim $Q 1 --as model-a
DONE="ease-in added" CHANGED="modify src/steer.rs" work $Q 01 'printf "rate = 3\nease_in\n" > src/steer.rs' "w01: done - ease in"
wf check $Q 1 --as checker-c || true
wf check $Q 1 --as checker-c --note "same commit, still unclamped" || true
wf answer $Q "$(grep -n '"kind":"elevate"' "$WORK/pages/$Q/log.jsonl" | tail -1 | cut -d: -f1)" --text "fail it; rework in 05.02" --as prima
wf signoff $Q 1 --outcome failed --note "clamp broken by ease-in; rework in 05.02" --as prima
wf close $Q 1 --as prima
wf face-write $Q 06 --text "Before 05.02: 05.01 failed (clamp lost). Rework keeps the clamp." --as prima
wf draft $Q --file "$WORK/ease.txt" --as prima
wf pack $Q 2 --as prima
wf claim $Q 2 --as model-a
DONE="ease-in, clamp kept" CHANGED="modify src/steer.rs" work $Q 02 'printf "rate = 3\nease_in\nclamp(-30, 30)\n" > src/steer.rs' "w01: done - ease in, clamp kept"
wf check $Q 2 --as checker-c
wf signoff $Q 2 --outcome passed --as prima
wf close $Q 2 --as prima
echo "-- Path 2: a return touches a file outside its frame and is refused"
wf face-write $Q 06 --text "Before 05.03: 05.02 passed. Next: smooth turns at speed." --as prima
sed 's/^w01:.*/w01: turns stay smooth at speed/; s/^outcome:.*/outcome: no skid on fast turns/' "$WORK/ease.txt" > "$WORK/speed.txt"
wf draft $Q --file "$WORK/speed.txt" --as prima
wf pack $Q 3 --as prima
wf claim $Q 3 --as model-a
DONE="grip tweak" CHANGED="modify src/physics/grip.rs" work $Q 03 'echo "grip = 2" > src/physics/grip.rs' "w01: done - grip tweak" || echo "   (refused, as the example expects)"
echo "-- Path 3: the worker ends need; physics is outside the grant, so it goes to Matthew"
DONE="nothing changed in code" CHANGED="create the return file only" NOTDONE="w01, needs src/physics/grip.rs" \
  work $Q 03 'true' "w01: need - grip change needed for smooth turns (src/physics/grip.rs)"
E=$(grep -n '"kind":"elevate"' "$WORK/pages/$Q/log.jsonl" | tail -1 | cut -d: -f1)
wf elevate $Q 3 --to person --item "May steering work change src/physics/grip.rs? Proposed: yes, fn grip_at_speed, for 05.04 only." --as prima
wf answer $Q "$E" --text "sent up to matthew (outside grant t300u)" --as prima
wf check $Q 3 --as checker-c
wf signoff $Q 3 --outcome needs-authority --as prima
wf close $Q 3 --as prima
E2=$(grep -n '"kind":"elevate"' "$WORK/pages/$Q/log.jsonl" | tail -1 | cut -d: -f1)
wf grant $Q --paths "src/physics/grip.rs" --ref t301u --answers "$E2" --as matthew
wf face-write $Q 06 --text "Before 05.04: t301u grants src/physics/grip.rs." --as prima
sed 's#^may touch:.*#may touch: src/steer.rs, src/physics/grip.rs#' "$WORK/speed.txt" > "$WORK/speed2.txt"
wf draft $Q --file "$WORK/speed2.txt" --as prima
wf pack $Q 4 --as prima
wf observe $Q --as observer-o --record "4 passes on one page; Prime should answer the why questions before 05.04 is claimed" 
try observe $Q --record "prime cannot file this" --as prima
wf status $Q
wf verify $P
wf verify $Q

rm -rf "$KIT/examples/pages"; mkdir -p "$KIT/examples/pages"
cp -r "$WORK/pages/$P" "$WORK/pages/$Q" "$KIT/examples/pages/"
echo "== done: examples/pages/$P and examples/pages/$Q"
