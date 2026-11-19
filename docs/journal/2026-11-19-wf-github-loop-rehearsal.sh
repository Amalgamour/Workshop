#!/usr/bin/env bash
# Rehearsal: a local bare repo stands in for GitHub; one clone is Prima (the box), one is the builder.
set -euo pipefail
WF=/workspace/workshop-build/target-wf-functional/debug/wf
R=/tmp/wfr; rm -rf $R; mkdir -p $R
export GIT_AUTHOR_NAME=x GIT_AUTHOR_EMAIL=x@example GIT_COMMITTER_NAME=x GIT_COMMITTER_EMAIL=x@example
say() { echo; echo "## $*"; }
run() { echo "\$ $*"; "$@"; }
say "GitHub stand-in: bare repo with a returns branch (code) and a packs branch (pages)"
git init -q --bare $R/origin.git
git init -q -b returns $R/seed; cd $R/seed
mkdir -p src; echo "rate = 1" > src/steer.rs; git add -- src/steer.rs; git commit -qm "code: steer"; git push -q $R/origin.git returns
git checkout -q --orphan packs; git rm -rq --cached src; rm -rf src
printf 'work/\n' > .gitignore; mkdir pages; touch pages/.keep; git add -- .gitignore pages/.keep; git commit -qm "packs: start"; git push -q $R/origin.git packs
say "Prima's run folder (box): packs checkout, with work/ = returns checkout"
git clone -q -b packs $R/origin.git $R/prima; git clone -q -b returns $R/origin.git $R/prima/work
say "Builder's run folder (stands in for Matthew's Windows machine)"
git clone -q -b packs $R/origin.git $R/builder; git clone -q -b returns $R/origin.git $R/builder/work
P=10.20.30.1301
cd $R/prima; export WF_ROOT=$R/prima WF_KIT_BRANCH=wf-functional
say "Prima: page, faces, draft, pack on the shared returns branch, publish"
run $WF init-page $P --title "steer rehearsal" --person mat --prime prima --grant src/ --grant-ref t401u --as mat
run $WF face-write $P 04 --section goals --text "steering rate doubles" --as prima
run $WF face-write $P 01 --text "Goal: steering rate is 2.
Done when: src/steer.rs says rate = 2." --as prima
run $WF face-write $P 06 --text "first loop over GitHub (t401u)" --as prima
printf 'repo: work\nstart: origin/returns\noutcome: rate = 2\nw01: set rate to 2\nmay touch: src/steer.rs\nchecks: grep -q "rate = 2" src/steer.rs\nstop if: another file must change\n' > $R/pack.txt
run $WF draft $P --file $R/pack.txt --as prima
run $WF pack $P 1 --branch returns --as prima > $R/prompt-out.txt; echo "(job box printed; BUILDER-PROMPT.md written)"
run $WF publish-pack $P 1
cd $R/builder; export WF_ROOT=$R/builder WF_AS=bob; unset WF_KIT_BRANCH
say "Builder: follows BUILDER-PROMPT.md"
run git checkout -- pages
run git pull -q --ff-only origin packs
run git -C work fetch -q origin
run $WF claim $P 1
START=$(grep -o 'switch -c work/[^ ]* [0-9a-f]*' pages/$P/05.01/BUILDER-PROMPT.md | awk '{print $4}')
run git -C work switch -q -c work/$P.05.01 $START
echo "rate = 2" > work/src/steer.rs
HASH=$(sed -n 's/^Pack hash: \([0-9a-f]*\).*/\1/p' pages/$P/05.01/PROMPT.md)
mkdir -p work/.workshop/returns
printf 'pack: %s\ndone: set rate to 2\nchanged: modify src/steer.rs\nnoticed: none\nw01: done - rate is 2\nproof: grep\nnot done: none\nunprompted: none\noverflow: none\n' "$HASH" > work/.workshop/returns/$P.05.01.md
run git -C work add -- .workshop/returns/$P.05.01.md src/steer.rs
run git -C work commit -qm "$P.05.01: rate 2"
run $WF return $P 1 --branch returns --commit "$(git -C work rev-parse HEAD)" --file .workshop/returns/$P.05.01.md --push
cd $R/prima; export WF_ROOT=$R/prima; unset WF_AS
say "Prima: intake, check (Tester's seat), signoff, close, publish"
run $WF intake
run $WF check $P 1 --as cat
run $WF signoff $P 1 --outcome passed --as prima
run $WF close $P 1 --as prima | tail -3
run $WF publish-pack $P 1
run $WF verify $P
say "Builder: next pull of packs is clean"
cd $R/builder; run git checkout -- pages; run git pull -q --ff-only origin packs; WF_ROOT=$R/builder run $WF verify $P
say "GitHub stand-in: branch logs"
run git -C $R/origin.git log --oneline returns
run git -C $R/origin.git log --oneline packs
