=== BUILDER PROMPT 90.50.10.0701.05.04 ===
You are a Workshop builder on Windows, in PowerShell. Follow these steps in order. Stop and tell
Matthew if a step fails; do not work around it.

Safety rules (always):
- Stage by path only (git add -- <path>). Never `git add -A` or `git add .`.
- Push only to the `returns` branch, and only through `wf.exe return ... --push`.
- Never push to main or packs. Never force push. Never commit secrets, tokens or keys.

Setup, once per machine (skip what is already done):
  git clone -b packs https://github.com/Amalgamour/Workshop wf-run
  git clone -b returns https://github.com/Amalgamour/Workshop wf-run\work
  cargo install --git https://github.com/Amalgamour/Workshop --branch <kit branch> --locked wf

Every pass (the first line drops your local copy of wf's page writes; they already went out with your last return):
  cd wf-run
  git checkout -- pages
  git pull --ff-only origin packs
  git -C work fetch origin
  $env:WF_ROOT = (Get-Location).Path
  $env:WF_AS = "<your builder name>"

1. Read pages/90.50.10.0701/05.04/PROMPT.md and the AGENTS.md it names (pages/...). Follow them.
2. Claim the pass:
     wf.exe claim 90.50.10.0701 04
3. Start your work from the pack's start commit:
     git -C work switch -c work/90.50.10.0701.05.04 14467f3e79e859b45d8cc5a6789ec00616db4480
4. Do the work inside work\ . Touch only: tests/lab_0423.rs
   Run the checks: cargo test --test lab_0423
5. Copy pages/90.50.10.0701/05.04/RETURN-TEMPLATE.md to work\.workshop/returns/90.50.10.0701.05.04.md and fill every line.
   The "pack:" line is this pack's hash: 6c5192505588597d9969e4030dadaac2a9549613bf5433c2813d2ef7d20b8141
   A job you cannot finish ends `need` or `blocked`, with why.
6. Commit by path:
     git -C work add -- .workshop/returns/90.50.10.0701.05.04.md <each file you changed>
     git -C work commit -m "90.50.10.0701.05.04: <what you did>"
7. Return and push (wf merges your commit into returns, records the return, and pushes):
     wf.exe return 90.50.10.0701 04 --branch returns --commit (git -C work rev-parse HEAD) --file .workshop/returns/90.50.10.0701.05.04.md --push
8. Tell Matthew: "returned 90.50.10.0701.05.04" and paste the last lines wf printed.
=== END BUILDER PROMPT ===
