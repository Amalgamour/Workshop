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

pub fn changed(repo: &Path, from: &str, to: &str) -> Res<Vec<String>> {
    Ok(git(repo, &["diff", "--name-only", from, to])?.lines().map(String::from).collect())
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
    use super::clip_check_out;

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
}
