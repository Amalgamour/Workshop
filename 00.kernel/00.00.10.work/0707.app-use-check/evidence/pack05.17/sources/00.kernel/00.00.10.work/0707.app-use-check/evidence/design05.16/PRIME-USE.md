# PRIME-USE — N7 intake lab (0707/05.16)
**Lab only. Never pass the live book.** The commands below rebuild the evidence on fresh disposable roots.

```bash
python -B labs/n7-intake-compat-pass01/make_fixture.py --room D:/librarian/temp/n7-intake-NEW/faithful
python -B labs/n7-intake-compat-pass01/make_fixture.py --room D:/librarian/temp/n7-intake-NEW/noreview --omit-review
python -B labs/n7-intake-compat-pass01/run_flow.py --fixtures D:/librarian/temp/n7-intake-NEW --evidence D:/librarian/temp/n7-intake-NEW/evidence
python -B labs/n7-intake-compat-pass01/tests/test_n7.py --root D:/librarian/temp/n7-intake-NEW/tests --out D:/librarian/temp/n7-intake-NEW/tests.json
```

**Single calls**, where REPO is the copy root and BOOK = REPO/00.kernel/00.00.10.work:
```bash
python -B labs/n7-intake-compat-pass01/n7compat.py --repo-root REPO prepare --book BOOK --source 0707.app-use-check --pass 05.15
python -B labs/n7-intake-compat-pass01/n7compat.py --patch --repo-root REPO prepare --book BOOK --source 0707.app-use-check --pass 05.15
```

- **Without `--patch`, the behavior is the selected pass03's.**
- **With `--patch`,** the N7 grammar applies (`CONTRACT.md`).
- **Read the full inspect output before publishing,** then publish as a separate command.
