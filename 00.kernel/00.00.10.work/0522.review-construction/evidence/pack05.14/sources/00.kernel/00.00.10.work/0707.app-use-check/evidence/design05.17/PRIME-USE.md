# PRIME-USE — N5-compatible N7 intake lab (0707/05.17)
**Lab only. Never pass the live book.** Use a NEW root for every rerun. Every tool refuses a root inside the checkout.

```bash
python -B labs/n7-intake-compat-pass02/tests/test_n7v2.py --root D:/librarian/temp/n7-intake-NEW/v2 --out D:/librarian/temp/n7-intake-NEW/v2.json
python -B labs/n7-intake-compat-pass02/compat17/tests/test_n7.py --root D:/librarian/temp/n7-intake-NEW/compat17 --out D:/librarian/temp/n7-intake-NEW/compat17.json
python -B labs/n7-intake-compat-pass02/compat17/make_fixture.py --room D:/librarian/temp/n7-intake-NEW/flow/faithful
python -B labs/n7-intake-compat-pass02/compat17/make_fixture.py --room D:/librarian/temp/n7-intake-NEW/flow/noreview --omit-review
python -B labs/n7-intake-compat-pass02/run_flow2.py --fixtures D:/librarian/temp/n7-intake-NEW/flow --evidence D:/librarian/temp/n7-intake-NEW/flow/evidence
python -B labs/n7-intake-compat-pass02/n5_replay.py --room D:/librarian/temp/n7-intake-NEW/n5 --out D:/librarian/temp/n7-intake-NEW/n5.json
```

**Proposal check.** Pass the intake_ids printed by the two runs above. They depend on the copy's book path, so read them from the new outputs.
```bash
python -B labs/n7-intake-compat-pass02/proposal_check.py --faithful D:/librarian/temp/n7-intake-NEW/flow/faithful/repo --n5 D:/librarian/temp/n7-intake-NEW/n5/repo --expect-n7 ID_FROM_FLOW_R --expect-n5 ID_FROM_N5_U1 --out D:/librarian/temp/n7-intake-NEW/propcheck/out.json
```

**Single calls.** Here REPO is a copy root.
```bash
python -B labs/n7-intake-compat-pass02/n7compat2.py --repo-root REPO prepare --book REPO/00.kernel/00.00.10.work --source 0707.app-use-check --pass 05.15
python -B labs/n7-intake-compat-pass02/n7compat2.py --patch --repo-root REPO prepare --book REPO/00.kernel/00.00.10.work --source 0707.app-use-check --pass 05.15
```

- **Without `--patch`:** the pinned pass03 behaves exactly as selected.
- **With `--patch`:** the grammar is chosen by the measured kind (`CONTRACT.md`).
- **Read the full inspect output before publishing,** and publish as a separate command.
- **The `compat17` adapter** runs the historical pass01 cases (unedited copies) against pass02. Its G7 failure is the labelled K1 revision.
