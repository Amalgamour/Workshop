# Return lines, pass 01

Canonical line/pass reserve, capture, verify, lookup, and two-phase migration.
The contract is `00.kernel/00.00.10.work/0521.return-placement/evidence/build05.03/CONTRACT.md`.

This lab loads the pinned placement route and the pinned `return-capture/1` reader by path.
It does not call the sequential allocator. It does not edit those pinned files.
Mutating commands refuse the live work book and any book that still contains `0100.band.returns`.

New passes use schema `return-line-capture/1`. Historical packages stay `return-capture/1` and are described as `legacy-relocated/1` after adoption. A receipt is a byte check. It is not acceptance.

## Commands

Run from the repository root:

```text
python -B labs/return-lines-pass01/return_lines.py init --book BOOK --name 00.00.10.work
python -B labs/return-lines-pass01/return_lines.py reserve --book BOOK --page PAGE --batch 05.NN --submission ID --output LOGICAL --submitter NAME --reviewer NAME --release TEXT
python -B labs/return-lines-pass01/return_lines.py capture --book BOOK --page PAGE --batch 05.NN --submission ID --return-file FILE --artifact LOGICAL FILE
python -B labs/return-lines-pass01/return_lines.py verify --book BOOK --page PAGE --batch 05.NN
python -B labs/return-lines-pass01/return_lines.py lookup --book BOOK --member MEMBER
python -B labs/return-lines-pass01/return_lines.py lookup --book BOOK --page PAGE --batch 05.NN
python -B labs/return-lines-pass01/return_lines.py descriptor --book BOOK --page PAGE --batch 05.NN
python -B labs/return-lines-pass01/return_lines.py stage --book BOOK --backup BACKUP --audit AUDIT
python -B labs/return-lines-pass01/return_lines.py stage-resume --book BOOK --backup BACKUP --audit AUDIT
python -B labs/return-lines-pass01/return_lines.py adopt --book BOOK --backup BACKUP --audit AUDIT
python -B labs/return-lines-pass01/return_lines.py rollback-stage --book BOOK --backup BACKUP
python -B labs/return-lines-pass01/return_lines.py rollback-adopt --book BOOK --backup BACKUP
python -B labs/return-lines-pass01/return_lines.py plan --book BOOK --audit AUDIT --out FILE
```

`--interrupt-after N` stops a stage or adopt before the phase marker. Exit 0 is a finished command of that kind. Exit 1 means reserved or incomplete. Exit 2 is a refusal or a byte conflict. Exit 3 is an interrupted phase.

`app/return_line_tools.py` is the development pin and forwarder. It is not kernel law.

## Tests

```text
python -B -m unittest -v labs.return-lines-pass01.tests.test_return_lines
```

`rehearse.py` copies the audited capture set to a disposable book outside the live work book, then stages, adopts, rolls back, and files one synthetic pass. It does not modify the live captures.
