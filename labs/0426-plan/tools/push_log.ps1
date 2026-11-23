# Push one page log from the run folder to returns, only if the published log is a byte prefix of the local log.
# Lead tool (Claude, 2026-11-23). Never forces. Stages by path only.
# Usage: powershell -NoProfile -File push_log.ps1 -Page 90.50.10.0416 -Message "wf: close 90.50.10.0416.05.01 failed (log)"
param([Parameter(Mandatory)][string]$Page, [Parameter(Mandatory)][string]$Message, [string]$Root = $env:WF_ROOT, [string]$Builder = "Claude")
$ErrorActionPreference = "Stop"
$work = Join-Path $Root "work"
$local = [IO.File]::ReadAllBytes((Join-Path $Root "pages\$Page\log.jsonl"))
git -C $work fetch -q origin returns
if ($LASTEXITCODE -ne 0) { throw "fetch failed" }
$rel = ".workshop/logs/$Page/log.jsonl"
$tmp = [IO.Path]::GetTempFileName()
cmd /c "git -C `"$work`" show origin/returns:$rel > `"$tmp`" 2>nul"
$remote = if ($LASTEXITCODE -eq 0) { [IO.File]::ReadAllBytes($tmp) } else { [byte[]]@() }
Remove-Item $tmp
if ($remote.Length -gt $local.Length) { throw "refused: published log ($($remote.Length) bytes) is longer than local ($($local.Length)); intake first" }
for ($i = 0; $i -lt $remote.Length; $i++) { if ($remote[$i] -ne $local[$i]) { throw "refused: published log differs from local at byte $i; not a prefix" } }
if ($remote.Length -eq $local.Length) { "nothing new to push for $Page"; exit 0 }
"prefix ok: published $($remote.Length) bytes, local $($local.Length) bytes"
git -C $work checkout -q returns
git -C $work merge --ff-only -q origin/returns
if ($LASTEXITCODE -ne 0) { throw "work clone cannot fast-forward to origin/returns" }
$dest = Join-Path $work $rel
New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
[IO.File]::WriteAllBytes($dest, $local)
git -C $work add -- $rel
# Commit only this path, so anything else already staged in the work clone is not swept in.
git -C $work commit -q -m $Message -m "Builder: $Builder" -- $rel
git -C $work push -q origin returns
if ($LASTEXITCODE -ne 0) { throw "push rejected; nothing was forced. Fetch, re-run this script (it re-checks the prefix)." }
"pushed $rel to returns ($(git -C $work rev-parse --short HEAD))"
