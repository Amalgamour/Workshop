=== BUILDER PROMPT 90.50.10.0419.05.02 ===
You are a Workshop builder on Windows, in PowerShell. Follow these steps in order. Stop and tell
Matthew if a step fails; do not work around it.

Safety rules (always):
- Stage by path only (git add -- <path>). Never `git add -A` or `git add .`.
- Push only to the `pass/90.50.10.0419.05.02` branch, and only through `wf.exe return ... --push`.
- Never push to main or packs. Never force push. Never commit secrets, tokens or keys.

Setup, once per machine (skip what is already done):
  git clone -b packs https://github.com/Amalgamour/Workshop.git wf-run
  git clone -b pass/90.50.10.0419.05.02 https://github.com/Amalgamour/Workshop.git wf-run\work
  cargo install --git https://github.com/Amalgamour/Workshop.git --branch <kit branch> --locked wf

Every pass (the first line drops your local copy of wf's page writes; they already went out with your last return):
  cd wf-run
  git checkout -- pages
  git pull --ff-only origin packs
  git -C work fetch origin
  $env:WF_ROOT = (Get-Location).Path
  $env:WF_AS = "<your builder name>"

1. Read pages/90.50.10.0419/05.02/PROMPT.md and the AGENTS.md it names (pages/...). Follow them.
2. Claim the pass:
     wf.exe claim 90.50.10.0419 02
3. Start your work from the pack's start commit:
     git -C work switch -c work/90.50.10.0419.05.02 4dc2e0f076326657a7f4ac232bf8edd6733464c2
4. Do the work inside work\ . Touch only: tests/lab_0419.rs
   Run the checks: cargo test --lib; cargo test --test page_0419; cargo test --test lab_0419
5. Copy pages/90.50.10.0419/05.02/RETURN-TEMPLATE.md to work\.workshop/returns/90.50.10.0419.05.02.md and fill every line.
   The "pack:" line is this pack's hash: b1882a4544faf8fa7865d570c351f2633df21cd4e049528bf9eb073a8c1e43f6
   A job you cannot finish ends `need` or `blocked`, with why.
6. Commit by path:
     git -C work add -- .workshop/returns/90.50.10.0419.05.02.md <each file you changed>
     git -C work commit -m "90.50.10.0419.05.02: <what you did>"
7. Return and push (wf merges your commit into pass/90.50.10.0419.05.02, records the return, and pushes):
     wf.exe return 90.50.10.0419 02 --branch pass/90.50.10.0419.05.02 --commit (git -C work rev-parse HEAD) --file .workshop/returns/90.50.10.0419.05.02.md --push
8. Tell Matthew: "returned 90.50.10.0419.05.02" and paste the last lines wf printed.
=== END BUILDER PROMPT ===
