=== BUILDER PROMPT 90.50.10.0702.05.02 ===
You are a Workshop builder on Windows, in PowerShell. Follow these steps in order. Stop and tell
Matthew if a step fails; do not work around it.

Safety rules (always):
- Stage by path only (git add -- <path>). Never `git add -A` or `git add .`.
- Push only to the `returns` branch, and only through `wf.exe return ... --push`.
- Never push to main or packs. Never force push. Never commit secrets, tokens or keys.

Setup, once per machine (skip what is already done):
  git clone -b packs https://github.com/Amalgamour/Workshop.git wf-run
  git clone -b returns https://github.com/Amalgamour/Workshop.git wf-run\work
  cargo install --git https://github.com/Amalgamour/Workshop.git --branch returns --locked wf

Every pass (the first line drops your local copy of wf's page writes; they already went out with your last return):
  cd wf-run
  git checkout -- pages
  git pull --ff-only origin packs
  git -C work fetch origin
  $env:WF_ROOT = (Get-Location).Path
  $env:WF_AS = "<your builder name>"

1. Read pages/90.50.10.0702/05.02/PROMPT.md and the AGENTS.md it names (pages/...). Follow them.
2. Claim the pass:
     wf.exe claim 90.50.10.0702 02
3. Start your work from the pack's start commit:
     git -C work switch -c work/90.50.10.0702.05.02 86770ec221da36d3edaed3d1399459b555a86fa3
4. Do the work inside work\ . Touch only: labs/0702/
   Run the checks: git ls-files --error-unmatch labs/0702/LAB-0702-SEQ-GRAMMAR.md; git ls-files --error-unmatch labs/0702/LESSONS.md; git grep -q -E "^##[[:space:]]0[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]1[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]2[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]3[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]4[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]5[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md; git grep -q -E "^##[[:space:]]6[.]" -- labs/0702/LAB-0702-SEQ-GRAMMAR.md
5. Copy pages/90.50.10.0702/05.02/RETURN-TEMPLATE.md to work\.workshop/returns/90.50.10.0702.05.02.md and fill every line.
   The "pack:" line is this pack's hash: e570e7a6d93e723f074d8473866d9b06c3e5e2d9f177ccfb0f1fd40b8fea86e6
   A job you cannot finish ends `need` or `blocked`, with why.
6. Commit by path:
     git -C work add -- .workshop/returns/90.50.10.0702.05.02.md <each file you changed>
     git -C work commit -m "90.50.10.0702.05.02: <what you did>"
7. Return and push (wf merges your commit into returns, records the return, and pushes):
     wf.exe return 90.50.10.0702 02 --branch returns --commit (git -C work rev-parse HEAD) --file .workshop/returns/90.50.10.0702.05.02.md --push
8. Tell Matthew: "returned 90.50.10.0702.05.02" and paste the last lines wf printed.
=== END BUILDER PROMPT ===
