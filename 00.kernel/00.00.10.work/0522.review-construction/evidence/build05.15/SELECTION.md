# Selection and rollback — 0522/05.15

`app/librarian.py` is `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes. It still loads `review_loop_tools_v7.py`. This pack did not select the app.

An unapplied one-line swap of that load from v7 to v9 would hash to `7ee676f69fa819e02739561698e6e0a419f69b0dd59d95df1db90c6455ad8fd1`, 12204 bytes. That file was not written. It is not a selection candidate. The unfinished reporter lane also edits `app/librarian.py`. One later dispatcher has to carry this v9 pin and that reporter pin together. A capacity-lane pin, if Prime accepts one, belongs in that same coherent version.

Rollback of a future selection restores `app/librarian.py` to `c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9`, 12204 bytes, and leaves the v9 files on disk, inert. This pack does not delete them and does not archive them.

`0522/05.13` still measures `app/librarian.py` at the current hash. Selecting a later dispatcher would make a later prepare of that historical page incomplete. This pack did not edit `05.13.md`, its manifest, or its review.

The isolated 0521 absent-target repair is not in this door. The N7 disposable publish created `06.01.review.md` on that external book because the current publish path creates an absent N7 file. That is preliminary publication. `cycle.called` and `cycle.committed` stayed false.
