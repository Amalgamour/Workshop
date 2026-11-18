# app-dependencies-pass03

Read-only preflight for the accepted K, G, I, and L pieces. The contract is 00.kernel/00.00.10.work/0525.app-dependencies/06.05.md.

The reader is labs/module-dependencies-pass02/depdecl.py and stays unchanged. reader-pin.json is the measured pin. This wrapper does not import declared modules.

```
python -B labs/app-dependencies-pass03/preflight.py --set D:\Git\lib-build\labs\app-dependencies-pass03\set.json
```

Exit 0 means the report was written and the measured fixture rows match, with the disclosed reporter pin difference left visible. activation_ready is false. Combined workbook W and reporter-on-W stay pending. Exit 0 is not activation, closure, or release.
