mod common;

/// Outside trial for 90.50.10.0419. The harness stays in tests/common.
/// The read of tests/page_0419.rs fails on a823ee28, where that file is absent.
/// The shell proof is run here, not by tests/page_0419.rs.

use std::path::{Path, PathBuf};
use std::process::Command;

const SAFE: &str = "git grep -q -E [#][#][[:space:]]0[.] -- heading.md";
const BARE: &str = "git grep -q -E ##[[:space:]]0[.] -- heading.md";

#[test]
fn safe_git_grep_form_holds_outside_page_0419() {
    let _harness = common::PG;

    let page_path = Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/page_0419.rs");
    let page = std::fs::read_to_string(&page_path)
        .unwrap_or_else(|_| panic!("missing tests/page_0419.rs; the 05.01 outside test is absent"));
    assert!(page.contains("[#][#][[:space:]]0[.]"), "tests/page_0419.rs lost the safe form");
    assert!(page.contains("##[[:space:]]0[.]"), "tests/page_0419.rs lost the bare form");
    assert!(page.contains("no pattern given"), "tests/page_0419.rs lost the bare-form note");

    let src = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/src/git.rs"));
    let start = src.find("/// Run one check command").expect("run docs");
    let end = src.find("pub fn clip_check_out").expect("next item");
    let body = &src[start..end];
    assert!(body.contains("[#][#][[:space:]]0[.]"), "run comment lost the [#][#] form\n{body}");
    assert!(body.contains("##[[:space:]]0[.]"), "run comment lost the bare ## form\n{body}");
    assert!(body.contains("exits 128"), "run comment lost exit 128\n{body}");
    assert!(body.contains("no pattern given"), "run comment lost no pattern given\n{body}");

    let pattern = SAFE.split_whitespace().nth(4).expect("pattern token");
    assert!(!pattern.contains('^'), "caret in {pattern}");
    assert!(!pattern.contains('"') && !pattern.contains('\''), "quotes in {pattern}");
    assert!(!pattern.contains(' '), "space in {pattern}");
    assert!(!pattern.starts_with('#'), "pattern starts with #");

    let dir = heading_repo("lab0419");
    let (code, out) = sh_c(&dir, SAFE);
    assert_eq!(code, 0, "safe form under sh -c: {out}");
    let (code, out) = sh_c(&dir, BARE);
    assert_eq!(code, 128, "bare ## under sh -c: {out}");
    assert!(out.contains("no pattern given"), "{out}");
    let _ = std::fs::remove_dir_all(&dir);
}

fn heading_repo(name: &str) -> PathBuf {
    let dir = std::env::temp_dir().join(format!("wf-lab-0419-{}-{name}", std::process::id()));
    let _ = std::fs::remove_dir_all(&dir);
    std::fs::create_dir_all(&dir).unwrap();
    let git = |args: &[&str]| {
        let out = Command::new("git").arg("-C").arg(&dir).args(args).output().expect("git");
        assert!(out.status.success(), "git {}: {}", args.join(" "), String::from_utf8_lossy(&out.stderr));
    };
    git(&["init", "-q"]);
    std::fs::write(dir.join("heading.md"), "## 0. a heading\n## 1. other\n").unwrap();
    git(&["add", "--", "heading.md"]);
    dir
}

fn sh_bin() -> PathBuf {
    if let Some(path) = std::env::var_os("PATH") {
        for dir in std::env::split_paths(&path) {
            let exe = if cfg!(windows) { dir.join("sh.exe") } else { dir.join("sh") };
            if exe.is_file() {
                return exe;
            }
        }
    }
    for candidate in [r"C:\Program Files\Git\bin\sh.exe", r"C:\Program Files\Git\usr\bin\sh.exe"] {
        let path = PathBuf::from(candidate);
        if path.is_file() {
            return path;
        }
    }
    PathBuf::from("sh")
}

fn sh_c(dir: &Path, cmd: &str) -> (i32, String) {
    let out = Command::new(sh_bin()).arg("-c").arg(cmd).current_dir(dir).output().expect("run sh -c");
    let text = format!("{}{}", String::from_utf8_lossy(&out.stdout), String::from_utf8_lossy(&out.stderr));
    (out.status.code().unwrap_or(1), text)
}
