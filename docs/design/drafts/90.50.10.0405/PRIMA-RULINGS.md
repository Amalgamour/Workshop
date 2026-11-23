# Prima's rulings on the 0405 questions

Nov 23, applied by Cursor-C (Pack). The page is held. Not published.

1. 0405 joins wave 4 beside 0407 and 0408. It may change tests/wf.rs and tests/page_0405.rs only. No shared file with 0407 or 0408.
2. The proof line pastes the Windows cargo test --test wf output. A Linux run of that command must also pass. A Linux run alone is not the proof.
3. The Windows stand-in is Windows PowerShell 5.1, powershell -NoProfile -Command, the host that ships with Windows 10. Not pwsh. A script file uses powershell -NoProfile -File under that same host.

Face 01 names the builder Grok-1 for now. Cursor-1 may take the pass if free first.
Start: a823ee284574be3d9f6247925b9088137a27a539. Template 4. Kit branch returns.
Pack hash: ad8b0e5728ecf91587bfd1e8e48a2d1809aa34992bb19cab0a3ab6e1fe0d6702
Grant: tests/wf.rs, tests/page_0405.rs (t461u)
Design's pack file sha256 before these rulings: 0893a08f98b7778bd4a47111fec5ba766038bb96d12ed8401b74e67c2ce358c3
