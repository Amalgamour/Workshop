# First demo attempt

The first `demo.py --out evidence/build05.02/demo-output` exited 2 before copying a book. Stdout was empty. Stderr was:

```text
predecessor or tool pin moved: app/README.md, app/librarian.py
```

Those two live files differ from pack05.02. This pass did not edit them and did not parse the new bytes. The demo treated every non-book pack path as a required pin. `app/README.md` and `app/librarian.py` are not read by this request. The blocker list is now the workspace, `app/context.py`, the pass01 lab, and the four pinned readers. The partial directory from this attempt was removed before the recorded demo.
