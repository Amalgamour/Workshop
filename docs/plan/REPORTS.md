# Worker reports

t526u (23 Nov 2026): builders should push reports to GitHub so Prima can retrieve them. GitHub is the nexus for now.

t527u: this must be built into wf. wf is taught once where reports land, then wf sends the report when the worker is done.

t528u: design it as a lab with Claude first, so it is built well. We need this before we set up more workers. Prompt boxes are for brief troubleshooting. The normal loop is packs > returns > review through GitHub, with wf controlling it.

The design lab is 90.50.10.0705. Do not pack the Grok pages that build this into wf until that lab closes. This file is the stopgap.

## Interim (until wf sends the report)

Every builder and checker writes its final report as a markdown file and pushes it to the `returns` branch (or to `prima/build` for a core page; see docs/plan/CORE-RUN.md).

Path:

    reports/<page>/05.NN/<Builder>-<kind>-<YYYYMMDD-HHMM>.md

- `kind` is one of: `build`, `check`, `setup`, `lab`, `other`.
- `page` looks like `90.50.10.0407`.
- Setup reports (no page) go at `reports/setup/<Builder>-setup-<YYYYMMDD-HHMM>.md`.
- The timestamp is the machine's local time (Matthew's PC is America/Toronto).

The file includes: builder name, page/pass, commands run, results, wf entry numbers, push commits, findings, and time taken.

Stage by path only (`git add reports/...`; never `add -A`, never `commit -a`). Commit with a `Builder: <name>` trailer. Push to `returns` (or the core branch). Never force push. If the push is rejected, fetch and rebase onto the tip, then push again, and still never force.

`reports/` lives at the root of the work clone, outside `pages/` and outside `.workshop/`. At wf `a823ee28`, `wf intake` only reads `.workshop/logs/` from the returns tip (`src/cmd.rs`, the `ls-tree` of `.workshop/logs/`). `wf verify` only compares the view files printed under `pages/<page>/`. A `reports/` tree does not break intake or verify. This was checked in a throwaway run folder with a `reports/` file on the returns tip: intake still only considered log files, and verify of an unchanged page still said ok.

## PowerShell snippet

Paste at the end of any builder or checker prompt. Fill in the report body, then run as written. Adjust `$page`, `$pass`, and `$kind`. For a core page, push `prima/build` instead of `returns`.

```powershell
# Interim report push (docs/plan/REPORTS.md). Never force push.
$builder = $env:WF_AS
$page    = "90.50.10.0407"   # or "setup"
$pass    = "05.01"           # unused when $page is setup
$kind    = "build"           # build|check|setup|lab|other
$stamp   = Get-Date -Format "yyyyMMdd-HHmm"
$work    = Join-Path $env:WF_ROOT "work"
if ($page -eq "setup") {
  $rel = "reports/setup/$builder-$kind-$stamp.md"
  $what = "setup $builder"
} else {
  $rel = "reports/$page/$pass/$builder-$kind-$stamp.md"
  $what = "$page $pass"
}
$path = Join-Path $work $rel
New-Item -ItemType Directory -Force -Path (Split-Path $path -Parent) | Out-Null
@"
# Report

- Builder: $builder
- Page/pass: $what
- Kind: $kind
- Commands run:
- Results:
- wf entry numbers:
- Push commits:
- Findings:
- Time taken:
"@ | Set-Content -Encoding utf8 $path

git -C $work add -- $rel
git -C $work commit -m "report: $builder $kind $what" -m "Builder: $builder"
git -C $work push origin returns
if ($LASTEXITCODE -ne 0) {
  git -C $work fetch origin returns
  git -C $work rebase origin/returns
  git -C $work push origin returns
  # If this is rejected again, stop and tell Prima. Never force push.
}
```

## Proper version (lab 0705, then build pages)

wf is configured once with a report destination (run-folder config: branch and path). When a worker finishes a build return, a check, setup, a lab, or troubleshooting, wf writes the report file into the page's pass, pushes it to the configured place on GitHub, and logs it in the hash chain, so reports live in pages. Prima reads them from GitHub. Lab 90.50.10.0705 designs that end to end and proposes a split into disjoint-grant build pages for Grok builders. Those pages are packed after the lab closes.
