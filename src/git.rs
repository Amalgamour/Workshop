//! The few git reads wf needs. Runs the `git` command; no library.

use crate::log::Res;
use std::path::{Path, PathBuf};
use std::process::Command;

pub fn git(repo: &Path, args: &[&str]) -> Res<String> {
    let out = Command::new("git").arg("-C").arg(repo).args(args).output().map_err(|e| format!("cannot run git: {e}"))?;
    if out.status.success() {
        Ok(String::from_utf8_lossy(&out.stdout).trim_end().to_string())
    } else {
        Err(format!("git {}: {}", args.join(" "), String::from_utf8_lossy(&out.stderr).trim()))
    }
}

/// Full SHA of a commit, or an error naming it.
pub fn commit(repo: &Path, rev: &str) -> Res<String> {
    git(repo, &["rev-parse", "--verify", "--quiet", &format!("{rev}^{{commit}}")]).map_err(|_| format!("commit {rev} not found in {}", repo.display()))
}

pub fn is_ancestor(repo: &Path, a: &str, b: &str) -> bool {
    git(repo, &["merge-base", "--is-ancestor", a, b]).is_ok()
}

/// The branch tip: local branch first, then origin/<branch>.
pub fn branch_tip(repo: &Path, branch: &str) -> Res<String> {
    commit(repo, &format!("refs/heads/{branch}"))
        .or_else(|_| commit(repo, &format!("refs/remotes/origin/{branch}")))
        .map_err(|_| format!("branch {branch} not found (fetch it first)"))
}

pub fn show(repo: &Path, sha: &str, path: &str) -> Res<String> {
    git(repo, &["show", &format!("{sha}:{path}")]).map_err(|_| format!("{path} is not in commit {sha}"))
}

/// One path from `git diff --name-status --no-renames`, with its letter (A, M, D).
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Change {
    pub letter: char,
    pub path: String,
}

impl Change {
    pub fn tag(&self) -> String {
        format!("{} {}", self.letter, self.path)
    }
}

/// Parse `git diff --name-status` output. A rename is two lines (D old, A new) when --no-renames is set.
#[cfg(test)]
pub fn parse_name_status(text: &str) -> Res<Vec<Change>> {
    let mut out = Vec::new();
    for line in text.lines().filter(|l| !l.is_empty()) {
        let (st, path) = line.split_once('\t').ok_or_else(|| format!("git name-status line has no tab: {line}"))?;
        let letter = st.chars().next().ok_or_else(|| format!("git name-status line has no status: {line}"))?;
        if path.is_empty() {
            return Err(format!("git name-status line has no path: {line}"));
        }
        out.push(Change { letter, path: path.to_string() });
    }
    Ok(out)
}

/// Parse `git diff -z --name-status` output: STATUS\\0PATH\\0, paths kept exact.
pub fn parse_name_status_z(bytes: &[u8]) -> Res<Vec<Change>> {
    let mut parts: Vec<&[u8]> = bytes.split(|b| *b == 0).collect();
    if parts.last().is_some_and(|p| p.is_empty()) {
        parts.pop();
    }
    if parts.len() % 2 != 0 {
        return Err("git name-status -z output is truncated".into());
    }
    let mut out = Vec::new();
    for chunk in parts.chunks(2) {
        let st = std::str::from_utf8(chunk[0]).map_err(|_| "git name-status status is not UTF-8".to_string())?;
        let path = std::str::from_utf8(chunk[1]).map_err(|_| "git name-status path is not UTF-8".to_string())?;
        let letter = st.chars().next().ok_or_else(|| "git name-status entry has no status".to_string())?;
        if path.is_empty() {
            return Err("git name-status entry has no path".into());
        }
        out.push(Change { letter, path: path.to_string() });
    }
    Ok(out)
}

fn git_raw(repo: &Path, args: &[&str]) -> Res<Vec<u8>> {
    let out = Command::new("git").arg("-C").arg(repo).args(args).output().map_err(|e| format!("cannot run git: {e}"))?;
    if out.status.success() {
        Ok(out.stdout)
    } else {
        Err(format!("git {}: {}", args.join(" "), String::from_utf8_lossy(&out.stderr).trim()))
    }
}

pub fn changed(repo: &Path, from: &str, to: &str) -> Res<Vec<Change>> {
    parse_name_status_z(&git_raw(repo, &["diff", "--name-status", "--no-renames", "-z", from, to])?)
}

/// Check out `sha` in a throwaway worktree, run `f` in it, then remove it.
pub fn in_worktree<T>(repo: &Path, sha: &str, f: impl FnOnce(&Path) -> T) -> Res<T> {
    let dir: PathBuf = std::env::temp_dir().join(format!("wf-check-{}-{}", std::process::id(), &sha[..8.min(sha.len())]));
    git(repo, &["worktree", "add", "--detach", "--force", &dir.to_string_lossy(), sha])?;
    let out = f(&dir);
    let _ = git(repo, &["worktree", "remove", "--force", &dir.to_string_lossy()]);
    Ok(out)
}

/// Run one check command in `dir`. Returns (passed, full output).
pub fn run(dir: &Path, cmd: &str) -> (bool, String) {
    let mut c = if cfg!(windows) { let mut c = Command::new("cmd"); c.arg("/C"); c } else { let mut c = Command::new("sh"); c.arg("-c"); c };
    match c.arg(cmd).current_dir(dir).output() {
        Ok(o) => {
            let all = format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr));
            (o.status.success(), all.trim().to_string())
        }
        Err(e) => (false, format!("could not run: {e}")),
    }
}

/// Keep at most the last `max` lines of a check command's output, and note how many were cut.
pub fn clip_check_out(out: &str, max: usize) -> String {
    let lines: Vec<&str> = out.lines().collect();
    if lines.len() <= max {
        out.to_string()
    } else {
        let cut = lines.len() - max;
        format!("({cut} lines cut)\n{}", lines[lines.len() - max..].join("\n"))
    }
}

#[cfg(test)]
mod tests {
    use super::{clip_check_out, parse_name_status, parse_name_status_z};

    #[test]
    fn parse_name_status_keeps_letters_and_splits_a_rename() {
        let text = "A\t.workshop/returns/p.md\nD\tsrc/b.rs\nA\tsrc/c.rs\nM\tsrc/a.rs\n";
        let cs = parse_name_status(text).unwrap();
        assert_eq!(
            cs.iter().map(|c| c.tag()).collect::<Vec<_>>(),
            ["A .workshop/returns/p.md", "D src/b.rs", "A src/c.rs", "M src/a.rs"]
        );
    }

    #[test]
    fn parse_name_status_rejects_a_bad_line() {
        assert!(parse_name_status("src/a.rs").unwrap_err().contains("no tab"));
    }

    #[test]
    fn clip_check_out_keeps_short_output() {
        assert_eq!(clip_check_out("a\nb\nc", 40), "a\nb\nc");
        assert_eq!(clip_check_out("", 40), "");
    }

    #[test]
    fn clip_check_out_keeps_last_40_and_notes_the_cut() {
        let src: Vec<String> = (1..=50).map(|i| format!("L{i:03}")).collect();
        let out = clip_check_out(&src.join("\n"), 40);
        assert!(out.starts_with("(10 lines cut)\nL011\n"), "{out}");
        assert!(out.ends_with("L050"), "{out}");
        assert!(!out.contains("L001") && !out.contains("L010"), "{out}");
        assert_eq!(out.lines().count(), 41);
    }

    #[test]
    fn parse_name_status_z_keeps_spaces_tabs_newlines_and_non_ascii() {
        let mut raw = Vec::new();
        for (st, path) in [
            ("A", "src/a space.rs"),
            ("A", "src/a\tb.rs"),
            ("A", "src/a\nb.rs"),
            ("M", "src/é.rs"),
        ] {
            raw.extend_from_slice(st.as_bytes());
            raw.push(0);
            raw.extend_from_slice(path.as_bytes());
            raw.push(0);
        }
        let cs = parse_name_status_z(&raw).unwrap();
        assert_eq!(
            cs.iter().map(|c| c.tag()).collect::<Vec<_>>(),
            ["A src/a space.rs", "A src/a\tb.rs", "A src/a\nb.rs", "M src/é.rs"]
        );
        assert!(parse_name_status_z(b"").unwrap().is_empty());
        assert!(parse_name_status_z(b"A").unwrap_err().contains("truncated"));
    }
}
