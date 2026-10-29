# REAL-USE — colab-support-pass02 on one real source

State: the 0510/05.03 executor prepared one real-source v2 package on 2026-10-29. The 0701 investigation is a declared FIXTURE, not a live investigation. No model was called, and no return or review exists. This is the producer's own use; Prime has not used v2 yet.

## What was prepared
- **Target T01.** `00.kernel/00.00.10.work/0411.colab/evidence/exchange-layout-v2/CONTRACT.md` as a whole file. Blob 1cff00588bde14723b7058aa3698a30eb727a3632892bb8ad7029b4d049617d9, label `workshop`, commit 6896224510fe0bcebac291fce7ed311a2cd085cb.
- **Investigation (fixture).** `00.00.10.work/0701.colab-exchange-layout`, pass 05.01. hostile-read, unscored, zip-only.
- **Required sources.** exchange-layout-v2/NOTES.md, n7nn-interface-v1/CONTRACT.md and 0700.band.colabs/01.md.
- **Director replies.** Three actual quotes, copied exactly as the target contract quotes them.
- **Request.** `labs/colab-support-pass02/examples/request-exchange-layout.json`.

## Exact Prime invocation
The config is local and never packaged. Template: `labs/colab-support-pass02/examples/config.example.json`. Fill in the absolute interpreter path.
```text
python -B D:/Git/lib-build/labs/colab-support-pass02/colab_support.py preview --request D:/Git/lib-build/labs/colab-support-pass02/examples/request-exchange-layout.json --config CONFIG --json
python -B D:/Git/lib-build/labs/colab-support-pass02/colab_support.py prepare --request <same> --config CONFIG --output OUT --digest 42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184 --json
python -B D:/Git/lib-build/labs/colab-support-pass02/colab_support.py verify --output OUT --config CONFIG --json
python -B D:/Git/lib-build/labs/colab-support-pass02/handoff_check.py check --output OUT --expected-digest 42734b85… --json
```
Results, from raw exit records:

| step | exit | result |
|---|---|---|
| preview | 0 | |
| prepare | 0 | `prepared` |
| verify | 0 | `intact`; pinned assembler verify on the support projection exit 0 |
| repeat prepare | 0 | `already-prepared`; nothing written |
| `handoff_check check` | 0 | `valid` |
| `handoff_check copy` | 0 | `copied`, 17 files |

An earlier smoke preparation from the same request gave the same digest, so preparation is deterministic.

## Verified package
Package digest (`colab-package-digest/2`): **42734b859dca535dfe88b6c145fb03912d57a43636a2d7e67d5d3c7b75914184**
handoff.json 5d8d8f5115d0b9630afda61a29199f35baf43f06e5e5ac84c8d1b21c42fde755 (12279 bytes). verification.json 2a8557373a3370d27015ac6475c3c24bff991e165617e989bc2295833fe0cbf1 (5883 bytes).

| package path | role | sha256 | bytes |
|---|---|---|---|
| 05.01.pack.md | primary instruction | b46713a78cea87597d04578949d21f4539518133ff58a8c007377fb222ea5a29 | 3584 |
| 06.01.notes.md | notes | 2d7fe940fcfbd2a9b88c655ebbbd3f113c290182a18e8f875c2c10758c5349f9 | 2552 |
| ENTRY.md | entry | 1085c83d57c313844a83964e65489ebac71df7bf1f0623e74ddc35b8ba67aff7 | 4777 |
| templates/05.01.return.TEMPLATE.md | template | fcaeaa71c097b2dba66e670057597b0b2ea3f66c93998c606e420282dbd1ef8f | 1439 |
| templates/06.01.review.TEMPLATE.md | template | a6c3a88abbed4c80880b0bdca193c51e7f369e846a672253e7d9f8828eefc943 | 1008 |
| binding.json | binding | d6bfabb615200c91009deb8631bd834c52286037aae2cfb14e5827f49a1a81b1 | 642 |
| colab-request.json | request | 5778b69507ff4eadd67e0b3eb2bdb3aa7d22440110d1ddb16e09b5e5e7c0b1fa | 6270 |
| source-manifest.json | source manifest | 419d863333779d4cf723dbfc0eacf5a9622cf1ab41b1b0ddbcce660daf2a09c0 | 1109 |
| snapshots/0001.blob | T01 | 1cff00588bde14723b7058aa3698a30eb727a3632892bb8ad7029b4d049617d9 | 3776 |
| snapshots/0002.blob | required | b82b263ea18f8fe7432c3f0190671c5d9d816d4712a5c64921a0697d2ab701e5 | 434 |
| snapshots/0003.blob | required | 246189acdba7c4559c1bda5ba9a6314d60dca9bf1710b87c4eaf59cbde5f6f42 | 4489 |
| snapshots/0004.blob | required | a4231ad09ec5a14a320779f29574ca0cd8912eb0b1e8a25d2462d94c6b4dfeed | 1321 |
| support/SUPPORT.md | support declaration | 8cc3b97b405b20e3bd15710deafd95dd449b58cdbab65731b10ff85947594e38 | 574 |
| support/assembler/05.01.md | assembler support | bbc9e48853ff5720b1184734343672a1f8432612fb1397f8929ef0dcb602dd82 | 3377 |
| support/assembler/request.snapshot | assembler support | bb1d670be230884b6f47655016907133eadc0005bb9a4c166b0116e18a27c4e5 | 3581 |
| support/assembler/completion-receipt.json | assembler support | 0b51d84d96ff560148f2eec959004ec34b8838da4d155f38dbec524eec4d4170 | 2232 |

The ZIP `prepared-colab.zip` (5f77b08318a40b9329f51a9178e274637271d1cf06d4aa3e9e1ea3c354862cfe, 43099 bytes) holds exactly these 16 files. The captured `evidence/exchange05.03/prepared-colab.zip` is a byte copy.

OUT also holds `assembler-output/` (the same three support files, plus the shared manifest and snapshots), `assembler-request.json` (= support request.snapshot), `assembler-run.json` (raw, 4886 bytes), `handoff.json` and `verification.json`. There is no `05.01.return.md` or `06.01.review.md` anywhere.

## Labelled synthetic intake (disposable book)
Two members were reserved with the pinned helper:
- 0101.synthetic-layout-0701, with origin 0701.colab-exchange-layout/05.01;
- 0102.synthetic-layout-target, with origin 0411.colab/05.01, the SUBJECT page.

The return file says "SYNTHETIC FIXTURE … No model was called. Not a Colab finding."

- **0101: `captured`, exit 0.**
  - Runs: inspector 1 (reserved), capture 0, verify 0, inspector 0.
  - Receipt 7cc266af19a6a68b3effd212239d13323023887a95224f6b068f16703ac912fd; return ee9650a9…, 334 bytes.
  - The placement proposal maps the captured return.md to `00.00.10.work/0701.colab-exchange-layout/05.01.return.md`, `proposed; not written`.
- **Repeat: `already-captured`, exit 0.**
- **0102: `wrong-origin`, exit 2.** Only the inspector ran; nothing was captured.

## Mechanical steps this replaces (beyond v1)
1. Naming the exchange files from the pass, and keeping the pack as the single instruction source.
2. Producing visibly-marked return and review templates, and refusing to pre-create real ones.
3. Packaging Prime's supplied preparation notes separately from the later review.
4. A machine-readable handoff, so a consumer validates without reading prose.
5. Proposing where the exact captured return would sit, without writing it.

## Manual inputs that remain (Prime)
- The question, why, context, gaps, method, cases, permissions, stop points and preparation notes.
- The commit and target blob hash.
- Reserving the return member with the investigation origin before launch (G04 disposition).
- The release, transport, and carrying the expected digest with the ZIP (G03).
- Placing the exact return as `05.NN.return.md`, writing `06.NN.review.md`, and choosing the route. Those are workflow and Prime work, not built here.

## Friction and limits seen
- **U01.** The legacy assembler draft must still exist for custody checks. It is kept under support/ and labelled; a reader who opens support/ first still sees an instruction-shaped file, so its first instruction says it is not one.
- **U02.** Intake proposes placement only. Until a reviewed consumer exists, the return stays only in N1NN custody.
- **U03.** No time or token savings are measured or claimed.
