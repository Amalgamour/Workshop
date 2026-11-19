=== BUILDER PROMPT 90.50.10.0403.05.01 ===
You are a Workshop builder on Windows, in PowerShell. Follow these steps in order. Stop and tell
Matthew if a step fails; do not work around it.

Safety rules (always):
- Stage by path only (git add -- <path>). Never `git add -A` or `git add .`.
- Push only to the `returns` branch, and only through `wf return ... --push`.
- Never push to main or packs. Never force push. Never commit secrets, tokens or keys.

Setup, once per machine (skip what is already done):
  git clone -b packs https://github.com/Amalgamour/Workshop.git wf-run
  git clone -b returns https://github.com/Amalgamour/Workshop.git wf-run\work
  cargo install --git https://github.com/Amalgamour/Workshop.git --branch wf-functional --locked wf

Every pass (the first line drops your local copy of wf's page writes; they already went out with your last return):
  cd wf-run
  git checkout -- pages
  git pull --ff-only origin packs
  git -C work fetch origin
  $env:WF_ROOT = (Get-Location).Path
  $env:WF_AS = "<your builder name>"

1. Read pages/90.50.10.0403/05.01/PROMPT.md and the AGENTS.md it names (pages/...). Follow them.
2. Claim the pass:
     wf claim 90.50.10.0403 01
3. Start your work from the pack's start commit:
     git -C work switch -c work/90.50.10.0403.05.01 60dd7e254df032a6fa02510667eb408acf4a41ee
4. Do the work inside work\ . Touch only: src/addr.rs, src/cmd.rs, src/lib.rs, tests/wf.rs
   Run the checks: cargo test --lib addr; cargo test --test wf init_page_address
5. Copy pages/90.50.10.0403/05.01/RETURN-TEMPLATE.md to work\.workshop/returns/90.50.10.0403.05.01.md and fill every line.
   The "pack:" line is this pack's hash: b2de54ce03fd3280e81acadfbef4c1f366105918625956a832c5923663ce45a9
   A job you cannot finish ends `need` or `blocked`, with why.
6. Commit by path:
     git -C work add -- .workshop/returns/90.50.10.0403.05.01.md <each file you changed>
     git -C work commit -m "90.50.10.0403.05.01: <what you did>"
7. Return and push (wf merges your commit into returns, records the return, and pushes):
     wf return 90.50.10.0403 01 --branch returns --commit (git -C work rev-parse HEAD) --file .workshop/returns/90.50.10.0403.05.01.md --push
8. Tell Matthew: "returned 90.50.10.0403.05.01" and paste the last lines wf printed.
=== END BUILDER PROMPT ===
