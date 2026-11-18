# Prime use — disposable counterexample

This pass produced two views from explicit new books, plus three inspection packets on the first request. The command was:

```text
python -B labs/prime-desk-pass03/demo.py --out D:\Git\lib-build\00.kernel\00.00.10.work\0524.prime-desk\evidence\build05.03\demo-output
```

Run it from `D:\Git\lib-build` with `PYTHONDONTWRITEBYTECODE=1`. Python was 3.14.0. The same `--out` now exists, so a repeat refuses. To generate again, pass a new absolute directory.

Read these files:

- `demo-output/books.txt`
- `demo-output/view.md` and `demo-output/view.json`
- `demo-output/packet.md` and `demo-output/packet.json`
- `demo-output/view-0522.md` and `demo-output/packet-0522.md`
- `demo-output/packet-inspect-0522.json`
- `demo-output/packet-inspect-1599.json`
- `demo-output/packet-inspect-1705.json`
- `demo-output/request.json` and `demo-output/request-0522.json`
- `demo-output/live-drift.txt`

The overview before `## Packet` is 76 lines. The packet then quotes the selected task page in full.

`demo-output/book` holds a disposable assignment-record v1. Its `current_work` is `0521.return-placement/05.03.md`. The legacy selector still names `work-0522-0504`. The catalog names that same other id and was not used. Selected id is `work-0521-0503`. Rule is `assignment-record/v1`. The review path is the source page, file `matched`, judgment `unknown`. The return path is `0121.return-placement/05.03.return.md`, file `missing`, custody `pending`. The request names that return and the tool does not create it. Reporting policy `0412.prime-review/06.02.md` stays a desk dependency. The packet's review section names the source page. Its return section names the pending return. The 0521 criteria stay on that packet.

`demo-output/book-0522` keeps the frozen assignment snapshot, which names `0522.review-construction/05.04.md`. Selected id is `work-0522-0504`. Its review path is that source page. Its return path `0122.review-construction/05.04.return.md` is undeclared, so custody is `unknown`. The two canonical packets differ.

Inspection of `work-0522-0504`, `work-1599-0501`, and `work-1705-0501` against the first request leaves the selected id at `work-0521-0503`. Those packets use relation `inspection`. The 1599 return path is `1199.synth-lab/05.01.return.md`. The 1705 return and review stay on `1705.prime-desk-check`. `1599` and `1705` are disposable fixture pages in the new books.

Both canonical tool exits are 1. The inspection exits are 1. The wrapper exit is 0. Exit 1 here is the legacy disagreement, the pending or undeclared return, the open hold, the worker with no evidence file, and, for an inspection, the inspection gap. It is not acceptance. Director bytes 111:403 and model bytes 430:834 of the copied `0420.prime-desk/06.01.md` are separate spans. A supplied sentence that the worker is running stays supplied. Process activity stays unknown.

Counterexample request sha256 `35f12954ab320c4975af38c17f931f8103e029f1b3d89cd64fcbe876b4e6b475`. Fingerprint `140122b746da0cdd39e2ea8dbc99fbd238da18fc068ce2c06ba5880126af840c`. Observed `2026-11-01T18:17:42Z`. Coverage matched 23, missing 1, stale 0, changed 0.

Second book request sha256 `0c2b640eb5e22cd08237b2a66edbe5e1a49114e778dcd60a3ff822062ae4fc06`. Fingerprint `43ca41cf018bf09c5df803637d6af0ff0848e56c74b96049c1443d8d89ef46e9`. Observed `2026-11-01T18:17:45Z`. Coverage matched 23, missing 0.

## Live-read proposal — not run

This pass did not point the tool at the live book.

A later review can do that only with a new request file. Set `instance.root` to `D:\Git\lib-build\00.kernel\00.00.10.work`. Keep `tools_root` as the repository root. Point `assignment` at the live `0401.goal/06.01.md` only after a person checks its bytes. At demo time that live file still matched the pack05.02 snapshot, sha256 `a340b2cd72ed1c1ec3bc8f22b88319f171a3f270a8f31eb3b4cac1084b218806`, 595 bytes, and its `current_work` is `0522.review-construction/05.04.md`. The disposable 0521 record must not be copied onto that live file.

```text
python -B labs/prime-desk-pass03/prime_desk.py view --request ABS
python -B labs/prime-desk-pass03/prime_desk.py packet --request ABS --work-id WORK
```

`app/README.md` and `app/librarian.py` differed from the pack pins at demo time. This request does not read them. Rehashing either file is a new request written by a person. The tool will not silently refresh.

`assignment_state` stays a record field. A supplied running sentence stays supplied. Neither one is a live process check. This proposal does not seat `00.live`, register a librarian command, change the 0705 oracle, or file 0124 custody.
