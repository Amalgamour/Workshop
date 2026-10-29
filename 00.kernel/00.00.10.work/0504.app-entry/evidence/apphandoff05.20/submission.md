Did
The Director released 0504.app-entry/05.20 on 2026-10-28. Claim: Grok 4.7 (xAI), session 01a179d2-387a-7661-8702-6e53f95e96b5, 2026-10-28, HEAD aa9bf59f610e58e24067c4173ec8bce1c684bcf9. Pack manifest de83297511303a827b3ad9a2660399444153968463190c535dd9a0d4cdb1a28e matched. 0 bad. This pack has no source-provenance file. Live files matched the snapshots before the door edit. The baseline app/librarian.py was 694d44ae34739e6b41319ba1de6e84a9710fe13184d7329be769d62b71d8689a, 9268 bytes.

The door is capture-return --binding ABS in app/librarian.py. It launches the pinned labs/capture-handoff-pass01/handoff.py perform --binding ABS. It does not queue, claim, return, reserve, or launch a worker. clerk-deliver is unchanged. Code hashes: app/librarian.py cfb209e5f1cbeeada345d208d2aeea623b70969d199effdd17fe97ef2c690572, 9791 bytes; app/handoff_tools.py f1d76a517b64a82ff8e348b811a5c59dfe8870385e6737b67878e0749e705bc2, 9901 bytes; app/capture-handoff.json 9e1cdbbf89d9aa9edbb959b2c1c1944777a9420daf5551a510abe38d4f0ab854, 894 bytes; app/tests/test_handoff_tools.py 8ab810e2f2cd915364fbef507c9f1fcdd193107faad883fe8262354c1c31f597, 38476 bytes; app/README.md fd0a330d99d221b72fa237f1787903e0723cfbf0f3af4e5018abe2f3d7ed4015, 24078 bytes.

python -B app/tests/test_handoff_tools.py exited 0. evidence/apphandoff05.20/tests.txt is sha256 0d697a1e0c4430964ff07c345a0a938b65d314a682c501d22c77e52dd3f622a7, 8746 bytes. Summary: pass 6, expected-refusal 15, skip 1, fail 0. The skip is WinError 1314. The complete capture matched the direct backend aside from manifest and receipt hashes, which include captured_at. The read-only repeat matched byte for byte and printed writes none. A changed event and a changed payload were refused and the receipt bytes stayed. A partial capture was forwarded as attention, completed.json stayed absent, and the door did not resume. An unknown child exit was not turned into success, was not retried, and the wrapper did not add writes none.

python -B app/tests/test_entry.py exited 0. evidence/apphandoff05.20/entry-tests.txt is sha256 9d539694959f49bba685fbb93203d67ccd72650e893a2ca061602d35ae281b56, 2472 bytes. Summary: pass 12, expected-refusal 46, skip 1, fail 0. The skip is WinError 1314. run stays refused.

evidence/apphandoff05.20/verification.json is sha256 427d71ead6cb04b9ab144e2b7aaa4f370299fc57cd947081b412045f01994601, 5304 bytes. It hashes the captured sources and the code and does not hash itself.

Blocked
Nothing in this door slice stopped the build. File-symlink creation skipped with WinError 1314. That skip is recorded. It is not a failed check.

Need
Codex Prime review. No acceptance, acknowledgement, closure, or publication is claimed. A verified receipt is custody, not acceptance. The same-user gap between a hash read and the subprocess remains open. This door is not an operating-system sandbox. The read-only repeat is not a general exactly-once guarantee. There is no outer timeout and no automatic recovery.
