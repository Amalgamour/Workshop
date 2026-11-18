# Bounds - 05.11

| Check | Bound | Result |
| --- | --- | --- |
| historical sources | 24 | 24 records; 25 refuses `refused: limit sources` |
| pass01 sources | 32 | 32 records; 33 and the 44-source return refuse with the split sentence |
| pass02 sources | 64 | 33, 44, and 64 pass the count check; 65 refuses with the keep-every-source sentence |
| holds | 24 | 25 refuses `refused: limit holds` |
| answers | 24 | 25 refuses `refused: limit answers` |
| prime-input document | 262144 | the 05.10 prime-input is 137328 bytes |
| source content_bytes | 262144 | over-document.json is 276423 and refuses `limit sources[24].content_bytes` |
| inline hostile document | 262144 | 40 sources inside the count bound, 502359 bytes, refuse `input: input exceeds 262144 bytes` |

The 704-byte gap between Prime's frozen 136624-byte figure and this regeneration's 137328-byte figure is recorded in 06.19.md.
Both figures are under 262144. The content_bytes refusal is a different check.
