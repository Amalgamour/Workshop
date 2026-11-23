=== BUILDER PROMPT 90.50.10.0705.05.01 ===
You are a Workshop builder on Windows, in PowerShell. Follow these steps in order. Stop and tell
Matthew if a step fails; do not work around it.

Safety rules (always):
- Stage by path only (git add -- <path>). Never `git add -A` or `git add .`.
- Push only to the `returns` branch, and only through `wf.exe return ... --push`.
- Never push to main or packs. Never force push. Never commit secrets, tokens or keys.

Setup, once per machine (skip what is already done):
  git clone -b packs https://github.com/Amalgamour/Workshop.git wf-run
  git clone -b returns https://github.com/Amalgamour/Workshop.git wf-run\work
  cargo install --git https://github.com/Amalgamour/Workshop.git --branch <kit branch> --locked wf

Every pass (the first line drops your local copy of wf's page writes; they already went out with your last return):
  cd wf-run
  git checkout -- pages
  git pull --ff-only origin packs
  git -C work fetch origin
  $env:WF_ROOT = (Get-Location).Path
  $env:WF_AS = "<your builder name>"

1. Read pages/90.50.10.0705/05.01/PROMPT.md and the AGENTS.md it names (pages/...). Follow them.
2. Claim the pass:
     wf.exe claim 90.50.10.0705 01
3. Start your work from the pack's start commit:
     git -C work switch -c work/90.50.10.0705.05.01 10abb9f2598191ebf2652b70704cddc0fe3ffd56
4. Do the work inside work\ . Touch only: labs/0705/
   Run the checks: git ls-files --error-unmatch labs/0705/DESIGN.md; git ls-files --error-unmatch labs/0705/SPEC.md; git ls-files --error-unmatch labs/0705/WORKER-SETUP.md; git ls-files --error-unmatch labs/0705/FAILURES.md; git ls-files --error-unmatch labs/0705/BUILD-PAGES.md; git ls-files --error-unmatch labs/0705/LESSONS.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0705/DESIGN.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0705/SPEC.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0705/WORKER-SETUP.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0705/FAILURES.md; git grep -q -E [#][#][[:space:]]1[.] -- labs/0705/BUILD-PAGES.md
5. Copy pages/90.50.10.0705/05.01/RETURN-TEMPLATE.md to work\.workshop/returns/90.50.10.0705.05.01.md and fill every line.
   The "pack:" line is this pack's hash: 282c4c99ba41ef309902a533950fb0849cda503c9a5ceced004d2c15b13d5b55
   A job you cannot finish ends `need` or `blocked`, with why.
6. Commit by path:
     git -C work add -- .workshop/returns/90.50.10.0705.05.01.md <each file you changed>
     git -C work commit -m "90.50.10.0705.05.01: <what you did>"
7. Return and push (wf merges your commit into returns, records the return, and pushes):
     wf.exe return 90.50.10.0705 01 --branch returns --commit (git -C work rev-parse HEAD) --file .workshop/returns/90.50.10.0705.05.01.md --push
8. Tell Matthew: "returned 90.50.10.0705.05.01" and paste the last lines wf printed.
=== END BUILDER PROMPT ===
