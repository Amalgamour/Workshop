# Lab report · X3

Builder: Codex.

Pack: X3. [Work page line 113](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L113)

## What I did

- Refreshed all 24 Stage 1 rows. Both published log trees were checked. The 0407 and 0423 closes now show as failed. The 0419.05.02 passing close remains recorded. [Evidence table](#log-evidence)
- 0407.05.01 accepted both cards and carried the separate lab trial. [0407 close, entry 12](https://github.com/Amalgamour/Workshop/blob/bbb7d9565551c2bbbe9d64bc5ff3c3d08fba22f6/.workshop/logs/90.50.10.0407/log.jsonl#L12)
- 0423.05.03 carried w02 to a later 05.04. It needs a grant covering tests/page_0407.rs. The Unix-only fixture failure is listed with the Windows failures. [0423 entries 29–33](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/.workshop/logs/90.50.10.0423/log.jsonl#L29-L33) · [Catch log row 16](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/quality/CATCH-LOG.md#L38)
- Added “code on returns” as the last column. Its yes or no is the Git ancestry result for the returned commit of the latest closed pass. Six are yes and two are no. The eight checks are listed below. Open pages have a blank cell.
- The 0403 row keeps both facts. Its returns log ends at the elevation, while packs has the passing close. Its returned code is on returns. [0403 returns entry 9](https://github.com/Amalgamour/Workshop/blob/c09fa60c92ac2e4cde39c73a061166ebc2fac0e0/.workshop/logs/90.50.10.0403/log.jsonl#L9) · [0403 packs entry 12](https://github.com/Amalgamour/Workshop/blob/3313938cf8ef9d752bd54eef435bf3c4d51d4442/pages/90.50.10.0403/log.jsonl#L12)

## Files touched

- [PAGES.csv](../../../labs/stage1-route/PAGES.csv)
- reports/lab/stage1-route/Codex-X3.md, this report.

## Log evidence

Pins: [returns a82a0488](https://github.com/Amalgamour/Workshop/commit/a82a04887fdcdbf71628c72f835c08a12448101d), [packs c697e035](https://github.com/Amalgamour/Workshop/commit/c697e0353c34e41a46ebf029f7b417479e5485fa) and [prima/build 5d26b448](https://github.com/Amalgamour/Workshop/commit/5d26b4484067c776dfcf2e58f8255847d2385755).

The links point to the entry and the commit that last changed its log.

A missing returns log is shown as absent. Packs is shown when it supplies evidence.

Entry numbers, SHA-256 links and byte prefixes were checked from the Git blobs.

| Page | Latest returns entry | Latest packs entry |
| --- | --- | --- |
| 0403 | [returns e9 at c09fa60c](https://github.com/Amalgamour/Workshop/blob/c09fa60c92ac2e4cde39c73a061166ebc2fac0e0/.workshop/logs/90.50.10.0403/log.jsonl#L9) | [packs e12 at 3313938c](https://github.com/Amalgamour/Workshop/blob/3313938cf8ef9d752bd54eef435bf3c4d51d4442/pages/90.50.10.0403/log.jsonl#L12) |
| 0404 | [returns e22 at 411a014e](https://github.com/Amalgamour/Workshop/blob/411a014ee2f363dad22fe5904eb70d9e745d5146/.workshop/logs/90.50.10.0404/log.jsonl#L22) | [packs e22 at 2508512c](https://github.com/Amalgamour/Workshop/blob/2508512c1fc68ec82615597a3504e10ac3a0c233/pages/90.50.10.0404/log.jsonl#L22) |
| 0407 | [returns e12 at bbb7d956](https://github.com/Amalgamour/Workshop/blob/bbb7d9565551c2bbbe9d64bc5ff3c3d08fba22f6/.workshop/logs/90.50.10.0407/log.jsonl#L12) | [packs e12 at b111fd1d](https://github.com/Amalgamour/Workshop/blob/b111fd1de9e26f5a7c322a98db3eb9b3a578ed1f/pages/90.50.10.0407/log.jsonl#L12) |
| 0408 | [returns e11 at 21be13b9](https://github.com/Amalgamour/Workshop/blob/21be13b902a6ed2104b3316c64093f4556f1ff3a/.workshop/logs/90.50.10.0408/log.jsonl#L11) | [packs e11 at 7450d7a4](https://github.com/Amalgamour/Workshop/blob/7450d7a4836c6e41c7c59bd1838a0d536b8f6893/pages/90.50.10.0408/log.jsonl#L11) |
| 0415 | [returns e11 at 4dc2e0f0](https://github.com/Amalgamour/Workshop/blob/4dc2e0f076326657a7f4ac232bf8edd6733464c2/.workshop/logs/90.50.10.0415/log.jsonl#L11) | [packs e11 at 912ae002](https://github.com/Amalgamour/Workshop/blob/912ae002db9a6db494afc14dd019dd821584a407/pages/90.50.10.0415/log.jsonl#L11) |
| 0416 | [returns e12 at 49654b6a](https://github.com/Amalgamour/Workshop/blob/49654b6a8d51b57f94eb7888745eb5e39ee7f048/.workshop/logs/90.50.10.0416/log.jsonl#L12) | [packs e12 at b30ff68b](https://github.com/Amalgamour/Workshop/blob/b30ff68ba550f2f79faf9c212f05a3a5847ea218/pages/90.50.10.0416/log.jsonl#L12) |
| 0418 | Absent | [packs e6 at 98324515](https://github.com/Amalgamour/Workshop/blob/98324515d0a38ab6f3ce07d734752457dab3ea52/pages/90.50.10.0418/log.jsonl#L6) |
| 0419 | [returns e22 at ee40448d](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0419/log.jsonl#L22) | [packs e22 at a72be090](https://github.com/Amalgamour/Workshop/blob/a72be090d97bd51c038a919283db3f79c5f621ac/pages/90.50.10.0419/log.jsonl#L22) |
| 0422 | Absent | [packs e5 at dcc23879](https://github.com/Amalgamour/Workshop/blob/dcc2387983e04e2cedbcb01298877868b7a05ed9/pages/90.50.10.0422/log.jsonl#L5) |
| 0423 | [returns e33 at ec78461d](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/.workshop/logs/90.50.10.0423/log.jsonl#L33) | [packs e33 at c697e035](https://github.com/Amalgamour/Workshop/blob/c697e0353c34e41a46ebf029f7b417479e5485fa/pages/90.50.10.0423/log.jsonl#L33) |
| 0424 | [returns e7 at a0c08c1f](https://github.com/Amalgamour/Workshop/blob/a0c08c1f4e393a006b5806cf3cc0115b99dc64d5/.workshop/logs/90.50.10.0424/log.jsonl#L7) | [packs e7 at b4980927](https://github.com/Amalgamour/Workshop/blob/b4980927de634edc1e69856f98f73eef75efce00/pages/90.50.10.0424/log.jsonl#L7) |
| 0701, supporting lab | [returns e42 at 3090160d](https://github.com/Amalgamour/Workshop/blob/3090160d406968e2e1152ce8d636102632aa6755/.workshop/logs/90.50.10.0701/log.jsonl#L42) | [packs e42 at 07fe4d5f](https://github.com/Amalgamour/Workshop/blob/07fe4d5f82d4ec08f53bbc39762405b112b66970/pages/90.50.10.0701/log.jsonl#L42) |

The other 13 addresses have no log in either pinned tree.

They are 0405, 0406, 0409–0414, 0417, 0420, 0421, 0425 and 0498. [Returns log tree](https://github.com/Amalgamour/Workshop/tree/a82a04887fdcdbf71628c72f835c08a12448101d/.workshop/logs) · [Packs page tree](https://github.com/Amalgamour/Workshop/tree/c697e0353c34e41a46ebf029f7b417479e5485fa/pages)

The prior CSV supplies the unchanged planning fields and their citations. [Prior CSV, lines 1–25](https://github.com/Amalgamour/Workshop/blob/a82a04887fdcdbf71628c72f835c08a12448101d/labs/stage1-route/PAGES.csv#L1-L25) · [Original source key, lines 136–157](https://github.com/Amalgamour/Workshop/blob/a82a04887fdcdbf71628c72f835c08a12448101d/labs/stage1-route/README.md#L136-L157)

Current planning notes used for the refresh are the [X3–X6 rows](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L113-L116), the [held-pack question](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L165), and [Catch log rows 17–18](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/quality/CATCH-LOG.md#L39-L40). The 0701 outcome is cited in its row above.

## Code on returns

| Closed pass | Return entry | Exact commit on returns |
| --- | --- | --- |
| 0403.05.01 | [returns e8 at c09fa60c](https://github.com/Amalgamour/Workshop/blob/c09fa60c92ac2e4cde39c73a061166ebc2fac0e0/.workshop/logs/90.50.10.0403/log.jsonl#L8) | yes · [d9110934](https://github.com/Amalgamour/Workshop/commit/d91109344cfda1281cc87280889c0c1a6087b287) |
| 0404.05.02 | [returns e19 at 411a014e](https://github.com/Amalgamour/Workshop/blob/411a014ee2f363dad22fe5904eb70d9e745d5146/.workshop/logs/90.50.10.0404/log.jsonl#L19) | yes · [954ba76a](https://github.com/Amalgamour/Workshop/commit/954ba76a2e730c76f8279c92e63279a6ccf6547e) |
| 0407.05.01 | [returns e8 at bbb7d956](https://github.com/Amalgamour/Workshop/blob/bbb7d9565551c2bbbe9d64bc5ff3c3d08fba22f6/.workshop/logs/90.50.10.0407/log.jsonl#L8) | yes · [38a9b7f1](https://github.com/Amalgamour/Workshop/commit/38a9b7f1814c0a0abb5f8b68d641abfd13011eec) |
| 0408.05.01 | [returns e8 at 21be13b9](https://github.com/Amalgamour/Workshop/blob/21be13b902a6ed2104b3316c64093f4556f1ff3a/.workshop/logs/90.50.10.0408/log.jsonl#L8) | yes · [e2140ad8](https://github.com/Amalgamour/Workshop/commit/e2140ad843f76906dff2b2fc068b1b66cb4c8605) |
| 0415.05.01 | [returns e8 at 4dc2e0f0](https://github.com/Amalgamour/Workshop/blob/4dc2e0f076326657a7f4ac232bf8edd6733464c2/.workshop/logs/90.50.10.0415/log.jsonl#L8) | yes · [0e7708d3](https://github.com/Amalgamour/Workshop/commit/0e7708d3439b4896c2262812275bf4b3a6507591) |
| 0416.05.01 | [returns e9 at 49654b6a](https://github.com/Amalgamour/Workshop/blob/49654b6a8d51b57f94eb7888745eb5e39ee7f048/.workshop/logs/90.50.10.0416/log.jsonl#L9) | no · [c5bde1e2](https://github.com/Amalgamour/Workshop/commit/c5bde1e29c11ef1aa23ea219dbd7845c07820bfd) |
| 0419.05.02 | [returns e19 at ee40448d](https://github.com/Amalgamour/Workshop/blob/ee40448dde492f8dadb89eb164338a4f8604bc05/.workshop/logs/90.50.10.0419/log.jsonl#L19) | yes · [fa82cf29](https://github.com/Amalgamour/Workshop/commit/fa82cf29b9e7278263640645f605cbe54b92eb89) |
| 0423.05.03 | [returns e29 at ec78461d](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/.workshop/logs/90.50.10.0423/log.jsonl#L29) | no · [f1e2481a](https://github.com/Amalgamour/Workshop/commit/f1e2481a05a95cb506c3f22dec2e35326dbb437a) |

The 0416 and 0423.05.03 return commits are reachable from their recorded pass-branch tips. Both fail the ancestry check against the returns pin above. [0416 pass tip](https://github.com/Amalgamour/Workshop/commit/e07cf4261a9081aabdb00f3edf4a67d9622187d2) · [0423.05.03 pass tip](https://github.com/Amalgamour/Workshop/commit/d8d047d7ec2d4af3e483e97dbfe29a5744bc8d7d)

The 0423.05.02 passing code is already on returns. The column uses 05.03 because it is the latest closed pass on that page. [0423 return and close entries 19–22](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/.workshop/logs/90.50.10.0423/log.jsonl#L19-L22) · [05.02 code](https://github.com/Amalgamour/Workshop/commit/bf5207807781cbf16f52f7270dc0f09d8a3a175e)

## Questions for Matthew

- Should the authorized publisher also record the 0403 passing close on returns? Today its packs and returns tails differ. [0403 in the log table](#log-evidence)
- Which approved route should carry the accepted 0423.05.03 helper changes into 05.04? The failed close accepted that work and carried only w02. [0423 close entry 33](https://github.com/Amalgamour/Workshop/blob/ec78461d00a9d4e0f74a188e6056043f91943eb4/.workshop/logs/90.50.10.0423/log.jsonl#L33)

## Stop rules

No stop rule halted the refresh. The two publication questions stay open. [Work page rules and lane](https://github.com/Amalgamour/Workshop/blob/5d26b4484067c776dfcf2e58f8255847d2385755/docs/plan/WORK-PAGE-2026-11-30.md#L34-L73)
