# Local runner for librarian-check. Does not lint by itself.
# Finds a Python 3, then runs librarian-check\lcheck.py.
# No args: brief card on 00.00.00.kernel.draft.
# A first argument that does not start with - is the desk. The rest pass through.

$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$repo = $here
while ($repo -and -not (Test-Path (Join-Path $repo '00.00.00.kernel.draft'))) {
    $parent = Split-Path -Parent $repo
    if (-not $parent -or $parent -eq $repo) {
        Write-Error "Repo root not found from $here"
        exit 2
    }
    $repo = $parent
}
$tool = Join-Path $here 'librarian-check\lcheck.py'
$defaultDesk = Join-Path $repo '00.00.00.kernel.draft'

function Find-Python {
    $cmd = Get-Command py, python, python3 -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($cmd) { return $cmd.Source }
    $cached = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path $cached) { return $cached }
    return $null
}

if (-not (Test-Path $tool)) {
    Write-Error "lcheck.py is not at $tool"
    exit 2
}

$py = Find-Python
if (-not $py) {
    Write-Error 'No Python 3 found on PATH or in the local cache.'
    exit 2
}

$desk = $defaultDesk
$rest = @()
if ($args.Count -gt 0 -and -not $args[0].ToString().StartsWith('-')) {
    $desk = $args[0]
    if ($args.Count -gt 1) { $rest = @($args[1..($args.Count - 1)]) }
} else {
    $rest = @($args)
}
if ($rest.Count -eq 0) { $rest = @('--brief') }

& $py $tool $desk @rest
exit $LASTEXITCODE
