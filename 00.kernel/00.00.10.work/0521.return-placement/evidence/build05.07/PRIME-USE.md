# PRIME-USE - source and pass return access

Run these from `D:\Git\lib-build` with `python -B`. Begin with a source page and a pass. The book below is the retained disposable copy. It is not the live book. A descriptor is custody information. It is not acceptance, approval, or publication. `task_association` is `not-established`.

The clean run is `D:\librarian\temp\0521-0507\20261102T193704Z`. Its book is the path in the commands. Full stdout stays in that run's `commands` directory. Three earlier runs stay beside it: `20261102T193328Z`, `20261102T193354Z`, and `20261102T193526Z`. Each stopped on a suite assertion. They were not deleted.

Matching live custody `0121.return-placement` is still unfiled. Do not point these commands at `D:\Git\lib-build\00.kernel\00.00.10.work`.

First filing, source plus pass:

```text
python -B app/librarian.py return-lines verify --book D:\librarian\temp\0521-0507\20261102T193704Z\book --source 0521.return-placement --pass 05.01
```

The result is schema `return-access-result/1`. Read `descriptor.target_page`, `descriptor.return_path`, and `descriptor.custody_path`. They are `0121.return-placement`, `0121.return-placement/05.01.return.md`, and `0121.return-placement/05.01.custody`. The return sha256 is `74dbfd2f52cbac30e8bd6203ac018e6bbc504b3416edfc1537a53ef85db2f660`. `legacy.called` is false. The reason is `native line-pass return is not a legacy single-envelope page`.

Same line, second pass:

```text
python -B app/librarian.py return-lines verify --book D:\librarian\temp\0521-0507\20261102T193704Z\book --source 0521.return-placement --pass 05.02
```

`descriptor.return_path` is `0121.return-placement/05.02.return.md`. The return sha256 is `191012aa6b4bc682e613027541ae6f7ce1ff212ff43f9bf4c8e0aca28f3e4621`.

Historical passes on one N5NN line. The reader parent is `D:\librarian\temp\0521-0507\20261102T193704Z\retired\originals`.

```text
python -B app/librarian.py return-lines verify --book D:\librarian\temp\0521-0507\20261102T193704Z\book --source 0508.return-capture --pass 05.02
python -B app/librarian.py return-lines verify --book D:\librarian\temp\0521-0507\20261102T193704Z\book --source 0508.return-capture --pass 05.08
```

Pass `05.02` keeps member `0103.return-capture-0502` and target `0108.return-capture`. Pass `05.08` keeps member `0121.archive-resolution-0508` and the same target page with `05.08.return.md`. The occupant specimen is member `0104.app-entry-0508`, whose parent is `retired\occupants`.

Page-local tail:

```text
python -B app/librarian.py return-lines verify --book D:\librarian\temp\0521-0507\20261102T193704Z\book --source 0701.bench-method --pass 05.01
```

`descriptor.target_page` is `0701.bench-method`. `descriptor.return_path` is `0701.bench-method/05.01.return.md`.

Read-only status. It reports the layout hash, authority established false, `sentinel_policy` `not-adopted`, and `legacy_writer_closure` `not-established`. Incomplete index row `0154.colab-support-first-0501` stays incomplete.

```text
python -B app/librarian.py return-lines status --book D:\librarian\temp\0521-0507\20261102T193704Z\book
```

A live reserve is refused before launch and writes nothing:

```text
python -B app/librarian.py return-lines reserve --book D:\Git\lib-build\00.kernel\00.00.10.work
```

Stderr starts with `stop: canonical live book is refused`. Stdout is empty. Exit 2. `00.kernel\00.00.10.work\return-line-layout.json` stays absent.
