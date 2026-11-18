# return-lines pass03

Successor to frozen `labs/return-lines-pass02`. It loads that tool by pin and does not edit it. Reconstruction publishes corrected return pages, then retires colliding occupants into `retired/occupants` and every remaining audited old member into `retired/originals`. Retirement is the whole audited set.

The canonical live book is refused with check `live execution`. An ordinary door-marked copy still uses the synthetic fixture `return-line-authorization/1`. A copy marked by the in-process seam `designate_live` can use `return-line-recorded-release/1`, which pins an external `return-line-director-release/1` file. `return-line-release-candidate/1` is not authority. `preflight` checks a record and writes nothing.

```text
python -B labs/return-lines-pass03/return_lines.py preflight --book BOOK --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
python -B labs/return-lines-pass03/return_lines.py plan --book BOOK --audit AUDIT --out PLAN
python -B labs/return-lines-pass03/return_lines.py init --book BOOK --name 00.00.10.work --authorization AUTH --audit AUDIT --plan PLAN --backup BACKUP --staging STAGING --retired RETIRED
```

The other pass02 commands use the same arguments. There is no `--force` and no `--allow-live`. `designate_live` is not a CLI flag.

See `00.kernel/00.00.10.work/0521.return-placement/evidence/build05.05/CONTRACT.md`.

This tool does not edit app modules, callers, pass01, pass02, or the band door. It does not install a sentinel.
