# Integration proposal - 0512.prime-review/05.07

accepted: false
applied: false
state: unapplied exact diff

## Staged command

```
python -B app/review_report_tools_v1.py --book ABS --source PAGE --pass 05.NN
```

This command is the connector shipped by this pack. It does not require a dispatcher edit.

## Proposed command

```
python -B app/librarian.py review-report --book ABS --source PAGE --pass 05.NN
```

The proposal is not selected. On-disk app/librarian.py stays sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes.

## Exact diff

```diff
diff --git a/app/librarian.py b/app/librarian.py
--- a/app/librarian.py
+++ b/app/librarian.py
@@ -8,6 +8,7 @@
 prime-status calls the pinned read-only Prime status tool on a caller-supplied registry.
 prime-review, prime-guard, and prime-check-next call the pinned read-only Prime review tool on one explicit input.
 review-loop forwards workbook prepare, form, record, inspect, publish, read, and recover to the pinned v7 door. The v4 fixture commands stay on the pinned v4 door. reproduce is not an app command.
+review-report forwards one selected read-only report to the pinned pass03 reporter. It does not record, publish, or approve. Exit 0 is not a release.
 authoring forwards form, start, add-note, add-item, revise, inspect, review, and freeze to the pinned authoring v2 door.
 return-lines forwards status, lookup, and verify to the pinned return-access adapter, and reserve and capture to the pinned pass03 door.
 boot-prepare, boot-check, boot-judge, and boot-show forward explicit arguments to the pinned recorded-boot tool.
@@ -92,6 +93,7 @@
         "boot-show",
         "batch-observe",
         "capture-return",
+        "review-report",
         "review-loop",
         "authoring",
         "return-lines",
@@ -107,6 +109,15 @@
             stop(str(exc))
         if type(code) is not int:
             stop("pinned review loop returned no exit code")
+        raise SystemExit(code)
+    if command == "review-report":
+        door = load_module(Path(__file__).resolve().parent / "review_report_tools_v1.py", "librarian_review_report_tools_v1")
+        try:
+            code = door.perform(args, code_root)
+        except door.Refuse as exc:
+            stop(str(exc))
+        if type(code) is not int:
+            stop("pinned review report returned no exit code")
         raise SystemExit(code)
     if command == "authoring":
         door = load_module(Path(__file__).resolve().parent / "authoring_tools_v2.py", "librarian_authoring_tools_v2")
```

## Rollback

Restore app/librarian.py to sha256 c3a5be3b612c021d95effaa5da4a151bf89026422b94f4cad98331014c7f0cd9, 12204 bytes. The reverse diff is:

```diff
diff --git a/app/librarian.py b/app/librarian.py
--- a/app/librarian.py
+++ b/app/librarian.py
@@ -8,7 +8,6 @@
 prime-status calls the pinned read-only Prime status tool on a caller-supplied registry.
 prime-review, prime-guard, and prime-check-next call the pinned read-only Prime review tool on one explicit input.
 review-loop forwards workbook prepare, form, record, inspect, publish, read, and recover to the pinned v7 door. The v4 fixture commands stay on the pinned v4 door. reproduce is not an app command.
-review-report forwards one selected read-only report to the pinned pass03 reporter. It does not record, publish, or approve. Exit 0 is not a release.
 authoring forwards form, start, add-note, add-item, revise, inspect, review, and freeze to the pinned authoring v2 door.
 return-lines forwards status, lookup, and verify to the pinned return-access adapter, and reserve and capture to the pinned pass03 door.
 boot-prepare, boot-check, boot-judge, and boot-show forward explicit arguments to the pinned recorded-boot tool.
@@ -93,7 +92,6 @@
         "boot-show",
         "batch-observe",
         "capture-return",
-        "review-report",
         "review-loop",
         "authoring",
         "return-lines",
@@ -109,15 +107,6 @@
             stop(str(exc))
         if type(code) is not int:
             stop("pinned review loop returned no exit code")
-        raise SystemExit(code)
-    if command == "review-report":
-        door = load_module(Path(__file__).resolve().parent / "review_report_tools_v1.py", "librarian_review_report_tools_v1")
-        try:
-            code = door.perform(args, code_root)
-        except door.Refuse as exc:
-            stop(str(exc))
-        if type(code) is not int:
-            stop("pinned review report returned no exit code")
         raise SystemExit(code)
     if command == "authoring":
         door = load_module(Path(__file__).resolve().parent / "authoring_tools_v2.py", "librarian_authoring_tools_v2")
```

## Pin consequence

Applying the forward diff changes app/librarian.py. labs/review-report-pass01/report.py check_pins and app/review_report_tools_v1.py then refuse `app/librarian.py`. This pack does not update that pin and does not update any other worker file. The dispatcher diff is the shared-command text. A later reviewed change has to carry the new librarian.py hash before the shared command can pass the pin check. Until that review, callers use the staged tool command. Rollback is the reverse diff above.
