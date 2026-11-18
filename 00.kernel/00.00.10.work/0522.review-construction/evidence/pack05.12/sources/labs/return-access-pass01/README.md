# return-access pass01

Resolves a return by source page and pass, or by one old member or submission, through pinned return-lines pass03. The legacy reader runs only against the member's actual parent. A line page is not a legacy envelope. No sentinel is installed. Pass04 is not imported.

```text
python -B labs/return-access-pass01/return_access.py status --book BOOK
python -B labs/return-access-pass01/return_access.py lookup --book BOOK --source PAGE --pass 05.NN
python -B labs/return-access-pass01/return_access.py verify --book BOOK --member OLD-MEMBER
```

The supported app entry is `app/librarian.py return-lines`. Reserve and capture go through that door to pass03, not through this file.
