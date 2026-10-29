# Candidate identity and transcript note — trial t2

- Model: Claude Opus 5.5 (`claude-opus-5-5`), vendor Anthropic.
- Interface: Claude Code, Claude desktop app (Code tab), Windows.
- Session id: not exposed directly; the session scratchpad path contains `2c19315e-118c-4c89-bbde-d177d3a541c1`, which appears to be the session id.
- Date: 2026-10-29.
- Role: orientation-trial candidate only. Not appointed, not Prime.

## Inputs read
- LAUNCH-PROMPT.txt, candidate/ENTRY.md, candidate/HOMEWORK.md, candidate/MANIFEST.json.
- candidate/attempt/t2/ files 00-10 and 19 (07.status.json read in part, plus a search for every `conflicts` key; both are `[]`).
- The bundle was present as an extracted folder; no `candidate.zip` was found there. I did not open the prepared attempt folder under Temp directly; only the show command read it.

## Command (run once)
`& "C:\Users\misg\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -B "D:\Git\lib-build\app\librarian.py" boot-show --attempt "C:\Users\misg\AppData\Local\Temp\pb-final-0516-44hpcrym\t2" --json`
(via PowerShell Start-Process with separate stream redirection)
- stdout: show-t2.stdout (556 bytes; stage awaiting-answers, "prepared; awaiting answers; not oriented", authority none)
- stderr: show-t2.stderr (0 bytes)
- exit: 0 (show-t2.exit)

## Deviations and limitations
- Claude Code automatically loaded the user's memory file for D:\librarian (a working-rules note about zip-only colab work) into context at session start, and I opened it once before starting. It contains no trial content, and I did not use it in the answers.
- I printed the ten small attempt files (00-06, 08, 10) with one read-only Bash `cat`, and created the output folder with PowerShell `New-Item`. These were read-only or output-folder-only operations, but they are shell commands that the launch prompt's "normal file-reading tools" rule did not allow.
- I did not hash any file. The bundle against MANIFEST.json, the bundle copy against the prepared attempt, and the packet ref sha256 values against their texts are all unverified. I compared the HOMEWORK table with 09.packet.json by reading them: ids, paths, sha256 and bytes match, and the byte total is 52,701.
- I did not run prepare, check or judge, and ran no Git.
