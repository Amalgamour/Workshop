//! Page 90.50.10.0419. A git grep pattern in a pack check has no caret, no
//! quotes, and no spaces. The bare `##` form is a comment under `sh -c`.

use std::path::{Path, PathBuf};
use std::process::Command;

const SAFE: &str = "git grep -q -E [#][#][[:space:]]0[.] -- heading.md";
const BARE: &str = "git grep -q -E ##[[:space:]]0[.] -- heading.md";

fn heading_repo(name: &str) -> PathBuf {
    let dir = std::env::temp_dir().join(format!("wf-page-0419-{}-{name}", std::process::id()));
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

fn assert_pattern_is_safe(cmd: &str) {
    let pattern = cmd.split_whitespace().nth(4).expect("pattern token");
    assert!(!pattern.contains('^'), "caret in {pattern}");
    assert!(!pattern.contains('"') && !pattern.contains('\''), "quotes in {pattern}");
    assert!(!pattern.contains(' '), "space in {pattern}");
    assert!(!pattern.starts_with('#'), "sh comment token {pattern}");
}

#[test]
fn bracket_form_matches_a_heading_under_sh_c() {
    assert_pattern_is_safe(SAFE);
    let dir = heading_repo("sh-safe");
    let (code, out) = sh_c(&dir, SAFE);
    assert_eq!(code, 0, "safe form under sh -c: {out}");
    let _ = std::fs::remove_dir_all(&dir);
}

#[test]
fn bare_hash_form_is_a_sh_comment_with_no_pattern() {
    let dir = heading_repo("sh-bare");
    let (code, out) = sh_c(&dir, BARE);
    assert_eq!(code, 128, "bare ## under sh -c should exit 128: {out}");
    assert!(out.contains("no pattern given"), "{out}");
    let _ = std::fs::remove_dir_all(&dir);
}

#[test]
fn git_rs_documents_the_bare_form_and_the_safe_form() {
    let src = include_str!(concat!(env!("CARGO_MANIFEST_DIR"), "/src/git.rs"));
    let start = src.find("/// Run one check command").expect("run docs");
    let end = src.find("pub fn clip_check_out").expect("next item");
    let body = &src[start..end];
    assert!(body.contains("##[[:space:]]0[.]"), "{body}");
    assert!(body.contains("no pattern given"), "{body}");
    assert!(body.contains("exits 128"), "{body}");
    assert!(body.contains("[#][#][[:space:]]0[.]"), "{body}");
    assert!(body.contains("sh -c") && body.contains("cmd /C"), "{body}");
}

/// What a Linux box still has to show is the `sh -c` pair above. This Windows
/// process also runs the safe form the way `src/git.rs` `run` does, through
/// `cmd /C`, and checks that the pattern has no caret, no quotes, and no spaces.
#[cfg(windows)]
#[test]
fn bracket_form_matches_a_heading_under_cmd() {
    assert_pattern_is_safe(SAFE);
    let dir = heading_repo("cmd-safe");
    let out = Command::new("cmd").arg("/C").arg(SAFE).current_dir(&dir).output().expect("cmd");
    let text = format!("{}{}", String::from_utf8_lossy(&out.stdout), String::from_utf8_lossy(&out.stderr));
    assert!(out.status.success(), "safe form under cmd /C: {text}");
    let _ = std::fs::remove_dir_all(&dir);
}
