wf on Windows splits a quoted check command at spaces. git grep -q -F "## 3. Results" fails as 'ambiguous argument 3.'
Until a page fixes that, every pack check must keep spaces out of the pattern. Use git grep -q -E "^##[[:space:]]3[.]" -- <file>.
This note is for that future page.
