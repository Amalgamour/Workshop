# No-blanks check for the lab prompts

Run by Prima on Sat Nov 28 2026 (t599u), after the prompts were written and before they were published. Plan doc.

## What it checks

Every filled prompt must have nothing left to fill in. The check searches for these:

- angle-bracket placeholders (a less-than or greater-than sign)
- the word NN, TBD, TODO or XXX
- double curly braces
- "..." and empty brackets or parentheses
- date-stamp placeholders (YYYY, HHMM, the word "stamp")
- a field name with nothing after it (Builder, Pack, Lab folder, Job, Done when, Note)
- an empty table cell

It runs on the two prompt files, the two queue files, the Nov 30 work page, and the Grok prompt blocks P1-P4 of the week page.

Not scanned: the week page's command for Matthew (the grant command for tests/page_0407.rs). It waits for his t-number. It is a command for him, not a builder prompt. It now reads "(his t-number)" so nothing in angle brackets is left in the file.

## The command

```
bash /workspace/workshop-build/scratch/labprompts/noblanks.sh
```

The script (box only, same text as below):

```
#!/bin/bash
# no-blanks check. Prints every hit; "hits=0" means clean.
cd /workspace/workshop-build/repo
F="docs/plan/queues/CLAUDE-PROMPTS.md docs/plan/queues/CODEX-PROMPTS.md docs/plan/queues/CLAUDE-QUEUE.md docs/plan/queues/CODEX-QUEUE.md docs/plan/WORK-PAGE-2026-11-30.md"
PAT='<|>|\bNN\b|\bTBD\b|\bTODO\b|\bXXX\b|\{\{|\}\}|\.\.\.|\[\]|\(\s*\)|YYYY|HHMM|\bstamp\b|^(Builder|Pack|Lab folder|Job|Done when|Note|Why|Prompt):[[:space:]]*$|\|[[:space:]]*\|'
n=$(grep -n -E -e "$PAT" $F | tee /dev/stderr | wc -l)
# week page: only the prompt code blocks P1-P4 (from "## 11. Ready prompts" to "### P5")
awk '/^## 11. Ready prompts/{f=1} /^### P5/{f=0} f' docs/plan/WORK-PAGE-2026-11-26-WEEK.md > /tmp/weekprompts.txt
m=$(grep -n -E -e "$PAT" /tmp/weekprompts.txt | tee /dev/stderr | wc -l)
echo "hits=$((n+m))"
```

## Result

First run: 1 hit, in P1 of the week page ("w01, w02, ..." was an ellipsis). Fixed to "w01 first, then w02, and so on".
Earlier in the run, the first draft of the pattern also matched every line that ends in a colon, like "Steps:". That was the pattern, not the files, so it was narrowed to named field names.
Second run: `hits=0`.

Also checked:
- 20 Claude prompts and 20 Codex prompts. Every one starts with "Builder: Claude" or "Builder: Codex".
- Every Claude prompt names `D:\Git\claude\wf-run\work`. Every Codex prompt names `D:\Git\codex\wf-run\work`. Neither names the other's folder as its own. (catch log row 13)
- Every prompt names its pack, folder, allowed files, job and Done when, and ends with the MANUAL RETURN block.
- Every allowed file is inside the agent's own lane on the Nov 30 work page.
- No prompt has a report name that needs a time. Each has a fixed name, for example reports/lab/review-stage1-route/Claude-C2.md. (catch log row 17)
