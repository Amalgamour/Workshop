# Demonstration trace (protocol test worker, not a model)

delivery `demo-0001`, job `job-count-lines`, request_sha256 `357eec2d94f657668136b67f0aaab24a257ad310a1ed1ac114fead14538f96c5`

| Boundary | File | Bytes | sha256 |
|---|---|---|---|
| request (prepared) | `request.json` | 674 | `357eec2d94f657668136b67f0aaab24a257ad310a1ed1ac114fead14538f96c5` |
| request (as stored by the adapter) | `store/demo-0001/request.json` | 674 | `357eec2d94f657668136b67f0aaab24a257ad310a1ed1ac114fead14538f96c5` |
| launch record (exclusive create, before the process) | `store/demo-0001/launch.json` | 390 | `0a2b95203026d4f0f41b4ce301d3339492a0dda3127f9d079b8a0c021f9f217f` |
| input read by the worker | `input/input.txt` | 75 | `3fc5fa06cff7912cb9a707d24f0b70edf751d873a6d106576654e3f6257cd5e4` |
| artifact written by the worker | `output/result.json` | 11 | `0c07187ea6d064441225b3cba26a7b1e8bc702fcf332b457dae8e26892ba68a6` |
| worker stdout = result | `store/demo-0001/attempt/stdout.bin` | 374 | `0d764e19f29a4d615dd9556c37ed70334d185951d250e3cdc0fd1c9666962c49` |
| worker stderr | `store/demo-0001/attempt/stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| exit record | `store/demo-0001/attempt/exit.json` | 59 | `40a03363bb2a35972ef6f7a3cb392c7ec19827df0e5229cf549f240f0d86df28` |
| receipt | `store/demo-0001/receipt.json` | 814 | `7b51eebd72db25c4381a44abf694bc8c8bf008a599a2d9f1d4370a984f77a4a1` |

deliver exit 0; fresh-process status exit 0
transport `delivered`, claimed outcome `done`, collection `collected`, worker kind `protocol test worker`, review `not performed`
artifact content: `{"count":3}`
