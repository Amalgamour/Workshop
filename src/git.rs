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

/// Run one check command in `dir`. Returns (passed, last lines of output).
pub fn run(dir: &Path, cmd: &str) -> (bool, String) {
    let mut c = if cfg!(windows) { let mut c = Command::new("cmd"); c.arg("/C"); c } else { let mut c = Command::new("sh"); c.arg("-c"); c };
    match c.arg(cmd).current_dir(dir).output() {
        Ok(o) => {
            let all = format!("{}{}", String::from_utf8_lossy(&o.stdout), String::from_utf8_lossy(&o.stderr));
            let tail: Vec<&str> = all.lines().rev().take(3).collect();
            (o.status.success(), tail.into_iter().rev().collect::<Vec<_>>().join(" | "))
        }
        Err(e) => (false, format!("could not run: {e}")),
    }
}
