# Selection and rollback — proposal only

This pack did not edit `app/librarian.py`. The active command remains the v7 door.

## Intended later dispatcher delta

The accepted candidate edit is two lines in `app/librarian.py`. The unapplied candidate file is `labs/review-entry-integration-pass01/candidate/app/librarian.py`. Its declared result is sha256 `5bc43806e6189f482b9e23e924e77cd60f9921a1ce94aaf0fe0f5c9278c4ea83`, 12204 bytes.

The docstring line changes the review-loop sentence from the pinned v7 door to the pinned v8 door. The load line changes from:

`load_module(Path(__file__).resolve().parent / "review_loop_tools_v7.py", "librarian_review_loop_tools_v7")`

to:

`load_module(Path(__file__).resolve().parent / "review_loop_tools_v8.py", "librarian_review_loop_tools_v8")`

The v8 declaration already pins the staged workbook `b7b8776c0da775509b21614fadc1b51a39123a946add76d0dfcc9ad3fe3016e2`, 6508 bytes, and the current v7 door `93a89939b6e6143eaffbb75c3b7cb60c38c60ad91902bd15d0b48c5bb35c382d`, 10291 bytes. Fixture commands stay on the pinned v4 door. No pin was disabled.

## Reporter pin coordination

`0512.prime-review/06.12.md` R1 says deployment of Grok-1's reporter remains blocked. A disposable copy with that proposed dispatcher on disk measured `app/librarian.py` at 12792 bytes, sha256 `b253a89751a48b64089bb95c4fde3715de00e6dc3c61dd8bad8653051234f3fa`, against the pin of 12204 bytes, sha256 `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`.

The v8 selection and the reporter selection both change `app/librarian.py`. One later dispatcher version has to carry both the v8 review-loop load and the reporter route. Whichever lands second has to re-pin the first version's dispatcher hash. This pack did not incorporate the unfinished `0512/05.08` reporter files and did not weaken that pin.

## Historical app artifact

While this dispatcher stays at `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, prepare of `0522.review-construction/05.13` measures complete and the `app/librarian.py` artifact row matches those bytes. Applying the two-line edit changes the file the historical return declares. The next prepare then reports `artifact-hash-mismatch` and incomplete. That is a selection consequence. Restoring the v7 dispatcher bytes makes the same prepare complete again. Do not edit `0522/05.13` so that the selected hash looks neutral.

## Rollback

Restore `app/librarian.py` to `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes. Leave `app/review_loop_tools_v8.py`, `app/review-loop-v8.json`, and `labs/workbook-review-pass04/workbook.py` on disk. They are inert while the dispatcher loads v7.

Do not edit the v8 declaration in place. Do not delete the staged files as a rollback. Do not re-record a v8 review through v7 to hide the intake difference. N7 rows written through the v8 grammar are not the v7 intake. A later v7 read of that review can show the intake as stale. N5 pages whose returns do not pin app bytes keep the same parser result on both doors, which is what the two live N5 prepares showed.

No archive, migration, or source-cut cleanup was done.
