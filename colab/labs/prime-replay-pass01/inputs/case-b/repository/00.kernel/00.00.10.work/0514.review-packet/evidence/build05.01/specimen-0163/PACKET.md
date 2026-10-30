# Review packet

Assembly: complete
Member: 0163.prime-bench-harness-0501
Book: D:\Git\lib-build\00.kernel\00.00.10.work

## Custody observation

Status: complete
Inspector exit: 0
Helper verify exit: 0
Problems: none

A verified receipt is custody, not acceptance.

Helper verify text, stored exact:

reservation 04e5152c777ff175da3a35f621f04d6b6d270f79c98e6cd426662327e0ccb47a
manifest 39d9404e159b8d04a865387724b1e4f8cae62c5261f81b5347987f7b89d37a6a
receipt 7efb07af0f08d3cbaf1b490e97889bb3caa601b932762fcf32820854e45f7e4f
payload 0001.blob 537480d4c5d8035014d5c68df46b604bdf83348a9a1579af37295307240bbbb3
payload 0002.blob 68add992c3b3769e6f89286f358138970302d0361884421cf5378d3afc434b3e
payload 0003.blob d9c2fd4e9a700d13aede26976d4f8ae4a11a9fed50e21564f3a40608ada895d6
payload 0004.blob 26235db45d4cf00fdfcef6be8e80523ab532e601676c6078a2ce09cf2d4c4627
payload 0005.blob da06ab6cfdee15497c1d19394fb9e22433e5c1db6623a3fd8462d20749274634
payload 0006.blob dcd33eb45b8c2397b9dd2577e636992b2c980a30c669281ed5acca72eb2f0d78
result complete
not approved
not accepted
not published

## Builder-reported claims

Return claims remain claims even when a hash matches.
- return-text: status present; sha256 742beefbf856429ce3dfcf59e675a06f618c1b75b74f8f09b87c67dc6575198e; bytes 6655; snapshot sources/0001-return-text.blob

## Artifact checks

### artifact-manifest

Schema result: checked
Observed schema: artifact-manifest/1
Rows interpreted: true
Keys not interpreted: batch, note
- labs/prime-bench-pass01/bench.json: classification changed-live-working-copy; historical match sha256 f00c6f29f35edd27465b2bbf5e4023323d8f028c4c6d8291ef1fe85db39fe9d1 bytes 12713; live differs sha256 ba17e1218eb27316d209784d51ba8e236a80967bdd6faa29b64f7161d82146db bytes 14320
- labs/prime-bench-pass01/cases/complete-a/candidate/sources/pack.md: classification historical-match; historical match sha256 26cf677ace1a54e6e0b796465fdae8d1ea638ace441b7f3a59aef7ac0daee70f bytes 354; live match sha256 26cf677ace1a54e6e0b796465fdae8d1ea638ace441b7f3a59aef7ac0daee70f bytes 354
- labs/prime-bench-pass01/cases/complete-a/candidate/sources/return.md: classification historical-match; historical match sha256 90014925ebb102724d9a201a1b80997c902557291a5753e9c4a78aa8f05c0cb7 bytes 257; live match sha256 90014925ebb102724d9a201a1b80997c902557291a5753e9c4a78aa8f05c0cb7 bytes 257
- labs/prime-bench-pass01/cases/complete-a/candidate/sources/test-log.txt: classification historical-match; historical match sha256 704e75e2945b18a83322002201a7393c6a9e3966f98197479fc06fc88000aa5b bytes 345; live match sha256 704e75e2945b18a83322002201a7393c6a9e3966f98197479fc06fc88000aa5b bytes 345
- labs/prime-bench-pass01/cases/complete-a/candidate/sources/verify.txt: classification historical-match; historical match sha256 f471c289f040cc2292239a029c0e7de8d0de468735198ea6d6d3a54505e8eae4 bytes 138; live match sha256 f471c289f040cc2292239a029c0e7de8d0de468735198ea6d6d3a54505e8eae4 bytes 138
- labs/prime-bench-pass01/cases/complete-a/candidate/TASK.md: classification historical-match; historical match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784; live match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784
- labs/prime-bench-pass01/cases/complete-a/coordinator/meta.json: classification changed-live-working-copy; historical match sha256 abd371d0545131b849d1c9d183b541d7ee53dd62624c467c5642f95723480241 bytes 943; live differs sha256 5b1bd5f58d07160c6b5911590d28e53de5a22975a3f707e30292e616d5f68574 bytes 943
- labs/prime-bench-pass01/cases/complete-a/evaluator/key.json: classification changed-live-working-copy; historical match sha256 2a0b84d03e331cbc0215edd2c618188fb79aa4339f80c2f4decb1b312fd44842 bytes 368; live differs sha256 0f51f62c16b67f7d7c83408c85af4601e019b465d079105a6ca417f300dc3f0b bytes 368
- labs/prime-bench-pass01/cases/complete-a/evaluator/rubric.json: classification changed-live-working-copy; historical match sha256 6daccf8f1dd3eca8705bfc5170ad99e6108936bc73b74587cde928096dcdb7ae bytes 832; live differs sha256 34ab02b6ebcafdf69a959921e1da5120d59dd54dfd47e6340c21ac08a612a63d bytes 832
- labs/prime-bench-pass01/cases/complete-b/candidate/sources/example-run.txt: classification historical-match; historical match sha256 8b42f2df23fbb255d1a13079e6b13022b9f03ac42eff49d768ccc38b46b442b3 bytes 103; live match sha256 8b42f2df23fbb255d1a13079e6b13022b9f03ac42eff49d768ccc38b46b442b3 bytes 103
- labs/prime-bench-pass01/cases/complete-b/candidate/sources/pack.md: classification historical-match; historical match sha256 932f84242de6cd272b5ddb01b3cfa04a8af7c52ceca7d4956d4b258ad4adaea8 bytes 356; live match sha256 932f84242de6cd272b5ddb01b3cfa04a8af7c52ceca7d4956d4b258ad4adaea8 bytes 356
- labs/prime-bench-pass01/cases/complete-b/candidate/sources/README-excerpt.md: classification historical-match; historical match sha256 0c875d189130562bea533d658dcf558cadf6ad7889bca45fede40c67ebb49d6f bytes 108; live match sha256 0c875d189130562bea533d658dcf558cadf6ad7889bca45fede40c67ebb49d6f bytes 108
- labs/prime-bench-pass01/cases/complete-b/candidate/sources/return.md: classification historical-match; historical match sha256 69a1db6e49bbc947cfd4d49738113fc92a94974747703747e0882ef3eacdd084 bytes 258; live match sha256 69a1db6e49bbc947cfd4d49738113fc92a94974747703747e0882ef3eacdd084 bytes 258
- labs/prime-bench-pass01/cases/complete-b/candidate/TASK.md: classification historical-match; historical match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784; live match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784
- labs/prime-bench-pass01/cases/complete-b/coordinator/meta.json: classification changed-live-working-copy; historical match sha256 1fd546394562e2fbb3a90c64445a1021890b70443c4142abe5413d681365ec1e bytes 917; live differs sha256 4672165000dcc98117b84bd04f9f4b7f512cc2bd981e70391b4e16662692e71e bytes 917
- labs/prime-bench-pass01/cases/complete-b/evaluator/key.json: classification changed-live-working-copy; historical match sha256 56fb8055b12f9dfc7cc885080e2fbc1dad13e2e72bc1127711bfb39cff87b0e1 bytes 331; live differs sha256 698df3255b5903c49488ec5056c0171eaee1e368b20147d39de0603d8ab70b76 bytes 331
- labs/prime-bench-pass01/cases/complete-b/evaluator/rubric.json: classification changed-live-working-copy; historical match sha256 19bcd134f6737c435225c080336ad67171f2c173132e4e40763065c783235aa9 bytes 832; live differs sha256 783eb69bc448dc8f4739c0d3e2534e660e859732d7fb533803ca70fe4ce579c8 bytes 832
- labs/prime-bench-pass01/cases/correction-a/candidate/sources/pack.md: classification historical-match; historical match sha256 127508c0e30640e339d0caf8a489089ca91f82afc469c5e22224925decce4765 bytes 304; live match sha256 127508c0e30640e339d0caf8a489089ca91f82afc469c5e22224925decce4765 bytes 304
- labs/prime-bench-pass01/cases/correction-a/candidate/sources/return.md: classification historical-match; historical match sha256 fa7fdfd698605c5a085757875d355e3e07b5193839b1e16242915efb28f45414 bytes 165; live match sha256 fa7fdfd698605c5a085757875d355e3e07b5193839b1e16242915efb28f45414 bytes 165
- labs/prime-bench-pass01/cases/correction-a/candidate/sources/tally_limit.py: classification historical-match; historical match sha256 906cc98fffe063163fb1b2712a7eb5a223861c9d13de6c6d1ff3d5f8987bcd42 bytes 195; live match sha256 906cc98fffe063163fb1b2712a7eb5a223861c9d13de6c6d1ff3d5f8987bcd42 bytes 195
- labs/prime-bench-pass01/cases/correction-a/candidate/sources/test-log.txt: classification historical-match; historical match sha256 6d3adda6ac44e34ff0cc91b46bed21c0988cd8e351bc12a7ce22576fa4ff33c2 bytes 293; live match sha256 6d3adda6ac44e34ff0cc91b46bed21c0988cd8e351bc12a7ce22576fa4ff33c2 bytes 293
- labs/prime-bench-pass01/cases/correction-a/candidate/TASK.md: classification historical-match; historical match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784; live match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784
- labs/prime-bench-pass01/cases/correction-a/coordinator/meta.json: classification changed-live-working-copy; historical match sha256 db227f5591dbb9cfe8cbbb0d3d8b3abe8d3f5a0714eb4a6dd44b3d287ef7b8dd bytes 1029; live differs sha256 0bf1aead407b0b89d666cf15d55b1440b75cfcfae0f9690f192ee25e514cea8e bytes 1029
- labs/prime-bench-pass01/cases/correction-a/evaluator/key.json: classification changed-live-working-copy; historical match sha256 9064a0e8826ca88a8b17809cbd14b12715fe44119e3a13c7f7ea6a9529a520c2 bytes 411; live differs sha256 f154787ec60dd98fa1498f397f4f0c326dc25fbdcf78d203937a94258ba30fea bytes 411
- labs/prime-bench-pass01/cases/correction-a/evaluator/rubric.json: classification changed-live-working-copy; historical match sha256 cef2f8053bf8114c27e3c0d74072be77dec1b3fc26d4c3844586123c4d184d70 bytes 834; live differs sha256 6487ce55f0e2eaa4b3c67d51512ad40a616ca2cf6558941dc4dbf99a27093a22 bytes 834
- labs/prime-bench-pass01/cases/correction-b/candidate/sources/export_root.py: classification historical-match; historical match sha256 6cacad91f8250ed8fc447918eeacc2de48ad99cc9b09b1c04950599e9a3367e1 bytes 164; live match sha256 6cacad91f8250ed8fc447918eeacc2de48ad99cc9b09b1c04950599e9a3367e1 bytes 164
- labs/prime-bench-pass01/cases/correction-b/candidate/sources/pack.md: classification historical-match; historical match sha256 2c3b493d602a2a12ef6ae6af8139909c1984b44f900ca0056e9d11db807608b6 bytes 323; live match sha256 2c3b493d602a2a12ef6ae6af8139909c1984b44f900ca0056e9d11db807608b6 bytes 323
- labs/prime-bench-pass01/cases/correction-b/candidate/sources/return.md: classification historical-match; historical match sha256 5107884aa64fec34c6f4867a15f770576b9605a5df41643eac49da8b15cba07d bytes 173; live match sha256 5107884aa64fec34c6f4867a15f770576b9605a5df41643eac49da8b15cba07d bytes 173
- labs/prime-bench-pass01/cases/correction-b/candidate/sources/test-log.txt: classification historical-match; historical match sha256 a951bf2ec2222bbbad54581d237562d9a68c8c4a8033c98724c337a1cb7941fb bytes 225; live match sha256 a951bf2ec2222bbbad54581d237562d9a68c8c4a8033c98724c337a1cb7941fb bytes 225
- labs/prime-bench-pass01/cases/correction-b/candidate/TASK.md: classification historical-match; historical match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784; live match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784
- labs/prime-bench-pass01/cases/correction-b/coordinator/meta.json: classification changed-live-working-copy; historical match sha256 a10b8a652b153f4b5ce9e68d759f95bf350786a3d2c77acbfecb1f510c473725 bytes 998; live differs sha256 2e33d0ac2abe0519ffdfa706478b0a48950f7ff20308d649d5cfb5f2fdc119ca bytes 998
- labs/prime-bench-pass01/cases/correction-b/evaluator/key.json: classification changed-live-working-copy; historical match sha256 1ebf2e5999217a7c70bd503a26b7114f6dc1ad7e6172b37c2000ba87e0edb944 bytes 353; live differs sha256 7f5a416a34602838da893a84f86f49806aeb525626608709168cd6e885c63084 bytes 353
- labs/prime-bench-pass01/cases/correction-b/evaluator/rubric.json: classification changed-live-working-copy; historical match sha256 7b521ff2045e6642b8ba453ac4391dd04970eaeb8b79b58ba62c39c1690df051 bytes 834; live differs sha256 2a01c1144648a7a2ac3859b66c9e747183bab61bce9c52ef98d5d1b87434eb15 bytes 834
- labs/prime-bench-pass01/cases/design-fork-a/candidate/sources/consumer-note.md: classification historical-match; historical match sha256 af648a6c022b9665b413d5252ac5ed0360db2fe3fd6031a7ca8ed62a7055e645 bytes 91; live match sha256 af648a6c022b9665b413d5252ac5ed0360db2fe3fd6031a7ca8ed62a7055e645 bytes 91
- labs/prime-bench-pass01/cases/design-fork-a/candidate/sources/pack.md: classification historical-match; historical match sha256 cf63e03c4cc5c76ee21cba65b3a20cb77c2e2acbff5149ea0d49e795916f0c2d bytes 326; live match sha256 cf63e03c4cc5c76ee21cba65b3a20cb77c2e2acbff5149ea0d49e795916f0c2d bytes 326
- labs/prime-bench-pass01/cases/design-fork-a/candidate/sources/return.md: classification historical-match; historical match sha256 c48fc6abd4874c68b0ae0119b22fb75788e26adb770d3df0ff601c233d1fa825 bytes 463; live match sha256 c48fc6abd4874c68b0ae0119b22fb75788e26adb770d3df0ff601c233d1fa825 bytes 463
- labs/prime-bench-pass01/cases/design-fork-a/candidate/TASK.md: classification historical-match; historical match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784; live match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784
- labs/prime-bench-pass01/cases/design-fork-a/coordinator/meta.json: classification changed-live-working-copy; historical match sha256 ffdd8d7bfae7e10e9e85310b5945c6716bc3a4d42c11a34cb44d6742316e6133 bytes 1033; live differs sha256 f6c9919e107bccf9b71f8153f915b437bb19388b3dd9eade775052b92efa2b67 bytes 1033
- labs/prime-bench-pass01/cases/design-fork-a/evaluator/key.json: classification changed-live-working-copy; historical match sha256 9769154ae951f4edbc5af033ee480e667829f2172f9e1d3ad331cb064027ee1a bytes 441; live differs sha256 09e5728b9fc7d91c91e6a7db55ba343e709a4287fca83048e566ea7042936347 bytes 441
- labs/prime-bench-pass01/cases/design-fork-a/evaluator/rubric.json: classification changed-live-working-copy; historical match sha256 eded2752863d0e2faa7334f39140d7241e48a6557f28ab4f93427e6cc7a5a2ba bytes 835; live differs sha256 f4d370ded691d2eea39e4263f8dcbd35940138238dbc45e5d86f2cc9a43818db bytes 835
- labs/prime-bench-pass01/cases/design-fork-b/candidate/sources/pack.md: classification historical-match; historical match sha256 606d73f254e73333935fe3a2c0c83b9d011f93677e832c26cf58ef966a280d80 bytes 326; live match sha256 606d73f254e73333935fe3a2c0c83b9d011f93677e832c26cf58ef966a280d80 bytes 326
- labs/prime-bench-pass01/cases/design-fork-b/candidate/sources/return.md: classification historical-match; historical match sha256 313f3b93465e0d738ab2f155205fc4ad6e8c98a1089e221f01f4700086f0b799 bytes 467; live match sha256 313f3b93465e0d738ab2f155205fc4ad6e8c98a1089e221f01f4700086f0b799 bytes 467
- labs/prime-bench-pass01/cases/design-fork-b/candidate/TASK.md: classification historical-match; historical match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784; live match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784
- labs/prime-bench-pass01/cases/design-fork-b/coordinator/meta.json: classification changed-live-working-copy; historical match sha256 35ff533aa3954ed254966544267f5d293c5d69a7e28e96796d3ca6d706d6fd3e bytes 1020; live differs sha256 69523f34b8f91e938d12a2a8343b5aebddbf3d0d267b0320defce929f880be79 bytes 1020
- labs/prime-bench-pass01/cases/design-fork-b/evaluator/key.json: classification changed-live-working-copy; historical match sha256 051932573fa222e0f3a8fcd1326c0912ee7efa0cb7032871e79bb5a8cc5e5002 bytes 482; live differs sha256 d6371f6fcd6cfb024d36d6f4b078363a88cfc4cc60b3e2cac9fbd29e68c1cf97 bytes 482
- labs/prime-bench-pass01/cases/design-fork-b/evaluator/rubric.json: classification changed-live-working-copy; historical match sha256 7ea333be1dd042d26ca5d807edfbbe014bc94a8fc940610a1fd73f1a74ee70f3 bytes 835; live differs sha256 5d02ea8eb62d3c64499ef51bd2adc531bf3651785415ac503f53f3af66a27191 bytes 835
- labs/prime-bench-pass01/cases/false-completion-a/candidate/sources/pack.md: classification historical-match; historical match sha256 7879cca412c85a0fb24248f8f02f6c4f9c921a3cf35300cbdb883b3330ed6370 bytes 269; live match sha256 7879cca412c85a0fb24248f8f02f6c4f9c921a3cf35300cbdb883b3330ed6370 bytes 269
- labs/prime-bench-pass01/cases/false-completion-a/candidate/sources/return.md: classification historical-match; historical match sha256 1df66eeaec345782cf30548b43b6507457ba72ebfb8bc2efa110d111012cf891 bytes 168; live match sha256 1df66eeaec345782cf30548b43b6507457ba72ebfb8bc2efa110d111012cf891 bytes 168
- labs/prime-bench-pass01/cases/false-completion-a/candidate/sources/verify.txt: classification historical-match; historical match sha256 0d9fe0e129a06b1a0f85a1d504506b248a3d557dd31acd8d144c9892d56f1497 bytes 211; live match sha256 0d9fe0e129a06b1a0f85a1d504506b248a3d557dd31acd8d144c9892d56f1497 bytes 211
- labs/prime-bench-pass01/cases/false-completion-a/candidate/TASK.md: classification historical-match; historical match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784; live match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784
- labs/prime-bench-pass01/cases/false-completion-a/coordinator/meta.json: classification changed-live-working-copy; historical match sha256 d857c7ea3089412d5892c574124016ee9a27e7b610dadc03a28423e927ac8930 bytes 1012; live differs sha256 aa8230d4866d9e113ff7cdfc1f5f88e26a59135f93ce08143551ddf6b2352a57 bytes 1012
- labs/prime-bench-pass01/cases/false-completion-a/evaluator/key.json: classification changed-live-working-copy; historical match sha256 8aa7116c4e9f2fa26d1da526615274ad7e279b1c065037daaf91aae90fe0dd3c bytes 402; live differs sha256 04b911ed94b3bd8fdba4a5dd65630c5b66adaaaebb746d9dd66132b7ebe607d2 bytes 402
- labs/prime-bench-pass01/cases/false-completion-a/evaluator/rubric.json: classification changed-live-working-copy; historical match sha256 5a2eb4249dff1b9e17195246494d68e4015077b810a81d3361f82e3b3283dff6 bytes 840; live differs sha256 9cc5a60c285fef850b441f982396636d02af5028eace137e13d2225d0fec86ce bytes 840
- labs/prime-bench-pass01/cases/false-completion-b/candidate/sources/artifact-manifest.json: classification historical-match; historical match sha256 bc7e9916fbf63f24570c530b7575be21a440570b5318728aeac9ddfb00db4d89 bytes 437; live match sha256 bc7e9916fbf63f24570c530b7575be21a440570b5318728aeac9ddfb00db4d89 bytes 437
- labs/prime-bench-pass01/cases/false-completion-b/candidate/sources/pack.md: classification historical-match; historical match sha256 e09f9ee28fa8523ab7e782a32d37d48f7747f12f89aa204579826cc4b5edfb01 bytes 286; live match sha256 e09f9ee28fa8523ab7e782a32d37d48f7747f12f89aa204579826cc4b5edfb01 bytes 286
- labs/prime-bench-pass01/cases/false-completion-b/candidate/sources/return.md: classification historical-match; historical match sha256 09b8147742409938cf385146fbf558db2ed8cfbd47ec239661fcf6bc869e97c4 bytes 172; live match sha256 09b8147742409938cf385146fbf558db2ed8cfbd47ec239661fcf6bc869e97c4 bytes 172
- labs/prime-bench-pass01/cases/false-completion-b/candidate/TASK.md: classification historical-match; historical match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784; live match sha256 28ba483bdbbbc1e592df44a365e0b7b0cffc4866f38f5e9bdf272e8120e2f74b bytes 784
- labs/prime-bench-pass01/cases/false-completion-b/coordinator/meta.json: classification changed-live-working-copy; historical match sha256 746cc194941a426150d0d97e3effab8b9b5cffaa749a6ff7e5949d85df6cbb28 bytes 1033; live differs sha256 61a2f23208a24a127fabf0a3d059b48982d77f03a7d253628b69e9d4c4f12d48 bytes 1033
- labs/prime-bench-pass01/cases/false-completion-b/evaluator/key.json: classification changed-live-working-copy; historical match sha256 e5062637775861d496d1440f615e2623f5e7178f8444624bd84f4054f77b15c7 bytes 324; live differs sha256 aea12934881fd435815e3935b2cb31dd2f7a402f8210d3b0738de698fee9f966 bytes 324
- labs/prime-bench-pass01/cases/false-completion-b/evaluator/rubric.json: classification changed-live-working-copy; historical match sha256 59b0c3670817ca234ccfd2a784b1fed9dcdb083ad89d4f5194d6db8ca71d6378 bytes 840; live differs sha256 89ccd723f571583ffa7e5a2137bd6b036fbdcb34c8739dffdd12774dee6f2498 bytes 840
- labs/prime-bench-pass01/conditions.json: classification historical-match; historical match sha256 d04a656ea912154db0237c3dcba2fee8e07567fa80bb3dccd3cb1de8a3c92753 bytes 788; live match sha256 d04a656ea912154db0237c3dcba2fee8e07567fa80bb3dccd3cb1de8a3c92753 bytes 788
- labs/prime-bench-pass01/prime_bench.py: classification changed-live-working-copy; historical match sha256 258727eef76693583ab0b88813c1b5afbded0009561f43c9bb61797b9d4dd650 bytes 68800; live differs sha256 a6dc98b8b6dbcaa8e080903a3ec537381e511b2b94206b259bb5c723c0696fe3 bytes 106951
- labs/prime-bench-pass01/README.md: classification changed-live-working-copy; historical match sha256 4c076720efaba038d3ebb609079f8be3fa6f97f6ac3434b048ce2605ee9a8b81 bytes 4664; live differs sha256 f2580bba642b3a71446cf590e9a33f0290ccb31bf9e8fb982dc8096213933a0b bytes 6022
- labs/prime-bench-pass01/tests/test_prime_bench.py: classification changed-live-working-copy; historical match sha256 5c125c3b4cc8ff5a72838fd83f0f7d88e55903f34b558f5deece187d4ca09ec9 bytes 42700; live differs sha256 2616b2ce2f36eb759129071c12a817964aa04414b98489591ee29e5f42449345 bytes 48650
- 00.kernel/00.00.10.work/0513.bench-build/06.01.md: classification historical-match; historical match sha256 537480d4c5d8035014d5c68df46b604bdf83348a9a1579af37295307240bbbb3 bytes 10070; live match sha256 537480d4c5d8035014d5c68df46b604bdf83348a9a1579af37295307240bbbb3 bytes 10070
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/CONTRACT.md: classification historical-match; historical match sha256 68add992c3b3769e6f89286f358138970302d0361884421cf5378d3afc434b3e bytes 10806; live match sha256 68add992c3b3769e6f89286f358138970302d0361884421cf5378d3afc434b3e bytes 10806
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/RUN-GUIDE.md: classification historical-match; historical match sha256 26235db45d4cf00fdfcef6be8e80523ab532e601676c6078a2ce09cf2d4c4627 bytes 4732; live match sha256 26235db45d4cf00fdfcef6be8e80523ab532e601676c6078a2ce09cf2d4c4627 bytes 4732
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/sample-report.md: classification historical-match; historical match sha256 dcd33eb45b8c2397b9dd2577e636992b2c980a30c669281ed5acca72eb2f0d78 bytes 6028; live match sha256 dcd33eb45b8c2397b9dd2577e636992b2c980a30c669281ed5acca72eb2f0d78 bytes 6028
- 00.kernel/00.00.10.work/0513.bench-build/evidence/build05.01/verification.json: classification historical-match; historical match sha256 d9c2fd4e9a700d13aede26976d4f8ae4a11a9fed50e21564f3a40608ada895d6 bytes 130259; live match sha256 d9c2fd4e9a700d13aede26976d4f8ae4a11a9fed50e21564f3a40608ada895d6 bytes 130259

## Absent, conflicting, and unverified

- absent or rejected source manifest-at-claimed-head: git blob is absent, live file was not read
- artifact labs/prime-bench-pass01/bench.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/complete-a/coordinator/meta.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/complete-a/evaluator/key.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/complete-a/evaluator/rubric.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/complete-b/coordinator/meta.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/complete-b/evaluator/key.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/complete-b/evaluator/rubric.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/correction-a/coordinator/meta.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/correction-a/evaluator/key.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/correction-a/evaluator/rubric.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/correction-b/coordinator/meta.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/correction-b/evaluator/key.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/correction-b/evaluator/rubric.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/design-fork-a/coordinator/meta.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/design-fork-a/evaluator/key.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/design-fork-a/evaluator/rubric.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/design-fork-b/coordinator/meta.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/design-fork-b/evaluator/key.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/design-fork-b/evaluator/rubric.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/false-completion-a/coordinator/meta.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/false-completion-a/evaluator/key.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/false-completion-a/evaluator/rubric.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/false-completion-b/coordinator/meta.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/false-completion-b/evaluator/key.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/cases/false-completion-b/evaluator/rubric.json: changed-live-working-copy
- artifact labs/prime-bench-pass01/prime_bench.py: changed-live-working-copy
- artifact labs/prime-bench-pass01/README.md: changed-live-working-copy
- artifact labs/prime-bench-pass01/tests/test_prime_bench.py: changed-live-working-copy

## Director quotations

None.
These quotations are source bytes. They do not confer authority.

## Limits

A verified receipt is custody, not acceptance. Return claims remain claims even when a hash matches. These checks are not an OS sandbox or a same-user race guarantee.
This packet does not accept, approve, publish, seat, or name a next task.
