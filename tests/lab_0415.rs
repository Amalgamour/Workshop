mod common;

use common::{Env, PG};

/// Outside trial for 90.50.10.0415. The harness stays in tests/common.
/// Creating a page log goes through the wf binary. The source read checks
/// sync_dir itself, so the same file fails on 3646e344, where the Windows
/// open is absent.
#[test]
fn creating_a_page_log_succeeds_and_sync_dir_keeps_both_branches() {
    let src = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/src/log.rs"));
    let body = sync_dir_body(src);
    let unix = slice_until(body, "#[cfg(unix)]", "#[cfg(windows)]");
    let windows = slice_until(body, "#[cfg(windows)]", "#[cfg(not(any(unix, windows)))]");
    let unix_open = at(unix, "fs::File::open");
    let unix_sync = at(unix, ".sync_all()");
    assert!(unix_open < unix_sync, "unix branch must open the folder and then sync_all:\n{unix}");
    let flag = at(windows, "custom_flags(FILE_FLAG_BACKUP_SEMANTICS)");
    let open = at(windows, ".open(");
    let sync = at(windows, ".sync_all()");
    assert!(
        flag < open && open < sync,
        "windows branch must open with FILE_FLAG_BACKUP_SEMANTICS and then sync_all:\n{windows}"
    );

    let e = Env::new("lab0415");
    let out = e.ok(&[
        "init-page",
        PG,
        "--title",
        "t",
        "--person",
        "mat",
        "--prime",
        "pri",
        "--grant",
        "src/",
        "--grant-ref",
        "t1",
        "--as",
        "mat",
    ]);
    assert!(!out.contains("cannot sync"), "{out}");
    assert!(!out.contains("Access is denied (os error 5)"), "{out}");
    let log = std::fs::read_to_string(e.page().join("log.jsonl")).expect("page log was created");
    assert!(log.contains("\"kind\":\"init\""), "{log}");
}

fn sync_dir_body(src: &str) -> &str {
    let start = src.find("fn sync_dir").expect("sync_dir");
    let rest = &src[start..];
    let end = rest.find("\n#[cfg(test)]").expect("end of sync_dir");
    &rest[..end]
}

fn slice_until<'a>(src: &'a str, start: &str, end: &str) -> &'a str {
    let i = src.find(start).unwrap_or_else(|| panic!("missing {start}; the Windows open is absent"));
    let rest = &src[i..];
    let j = rest.find(end).unwrap_or_else(|| panic!("missing {end} after {start}; the Windows open is absent"));
    &rest[..j]
}

fn at(hay: &str, needle: &str) -> usize {
    hay.find(needle).unwrap_or_else(|| panic!("missing {needle}; the Windows open is absent\n{hay}"))
}
