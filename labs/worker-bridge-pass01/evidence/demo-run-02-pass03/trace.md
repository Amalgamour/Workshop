# Demonstration trace (protocol test worker, not a model)

delivery `demo-0001`, job `job-count-lines`, request_sha256 `8ce51a0d346ef32877af410315c58646e0d9c6b3d6ca9cb373060dfc640d0715`

| Boundary | File | Bytes | sha256 |
|---|---|---|---|
| request (prepared) | `request.json` | 688 | `8ce51a0d346ef32877af410315c58646e0d9c6b3d6ca9cb373060dfc640d0715` |
| request (as stored by the adapter) | `store/demo-0001/request.json` | 688 | `8ce51a0d346ef32877af410315c58646e0d9c6b3d6ca9cb373060dfc640d0715` |
| launch record (exclusive create, before the process) | `store/demo-0001/launch.json` | 390 | `956f947a6feba62d94c9c1081947d051bcaf03539ac2a554f688a6a18cb57875` |
| input read by the worker | `input/input.txt` | 75 | `3fc5fa06cff7912cb9a707d24f0b70edf751d873a6d106576654e3f6257cd5e4` |
| artifact written by the worker | `output/result.json` | 11 | `0c07187ea6d064441225b3cba26a7b1e8bc702fcf332b457dae8e26892ba68a6` |
| worker stdout = result | `store/demo-0001/attempt/stdout.bin` | 374 | `4be2f977bdc6e7db32b43f61c58ce5eb719c2af93e5e07b41dfd01f1589e6cd9` |
| worker stderr | `store/demo-0001/attempt/stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| exit record | `store/demo-0001/attempt/exit.json` | 129 | `86fb05f852c2f1a4a822d2ab7ebcd20eec682a47fcba9cbfb2bd760e5b15bade` |
| receipt | `store/demo-0001/receipt.json` | 884 | `81e3db7a117fe83a0681a9da7f0bf032ebce4df3b6fb8904ab2812dae16679af` |

deliver exit 0; fresh-process status exit 0
transport `delivered`, claimed outcome `done`, collection `collected`, worker kind `protocol test worker`, review `not performed`
artifact content: `{"count":3}`
