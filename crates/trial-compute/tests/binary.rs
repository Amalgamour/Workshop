//! The real `compute` binary: listen address (finding 14 + held default).
use std::io::{BufRead, BufReader};
use std::process::{Command, Stdio};
use std::time::Duration;
use trial_compute::*;

fn compute_bin() -> std::path::PathBuf {
    let st = Command::new(env!("CARGO")).args(["build", "-q", "-p", "compute", "--bin", "compute"]).current_dir(repo()).status().expect("cargo build compute");
    assert!(st.success());
    repo().join("target/debug/compute")
}

/// Start the binary and return its first stdout/stderr line.
fn first_line(args: &[&str], env: &[(&str, &str)]) -> String {
    let d = kernel_dir("bin");
    let mut cmd = Command::new(compute_bin());
    cmd.args(["--books", d.to_str().unwrap()]).args(args).env_remove("COMPUTE_LISTEN").stdout(Stdio::piped()).stderr(Stdio::piped());
    for (k, v) in env {
        cmd.env(k, v);
    }
    let mut ch = cmd.spawn().unwrap();
    let out = ch.stdout.take().unwrap();
    let err = ch.stderr.take().unwrap();
    let (tx, rx) = std::sync::mpsc::channel();
    let tx2 = tx.clone();
    std::thread::spawn(move || {
        for l in BufReader::new(out).lines().map_while(Result::ok) {
            let _ = tx.send(l);
        }
    });
    std::thread::spawn(move || {
        for l in BufReader::new(err).lines().map_while(Result::ok) {
            if !l.starts_with("warning") {
                let _ = tx2.send(l);
            }
        }
    });
    let l = rx.recv_timeout(Duration::from_secs(20)).unwrap_or_default();
    let _ = ch.kill();
    let _ = ch.wait();
    l
}

#[test]
fn held_default_listen_is_loopback() {
    // either it binds 127.0.0.1:7700, or 7700 is busy and it says so: both name loopback
    let l = first_line(&[], &[]);
    assert!(l.contains("127.0.0.1:7700"), "{l}");
}

/// Finding 14 (minor): `--listen` / COMPUTE_LISTEN take any address; the
/// compute serves unauthenticated writes on every interface without a word.
#[test]
fn f14_non_loopback_listen_accepted() {
    let a = first_line(&["--listen", "0.0.0.0:0"], &[]);
    let b = first_line(&[], &[("COMPUTE_LISTEN", "0.0.0.0:0")]);
    assert!(!a.starts_with("compute on") && !b.starts_with("compute on"), "served on all interfaces: `{a}` / `{b}`");
}
