//! wf: the Workshop workflow tool. One page per piece of work.
//! The log (pages/<page>/log.jsonl) is the only truth; every other page file is a view
//! printed from it. People and models never edit page files; they run wf.

mod cmd;
mod git;
mod log;
mod page;
mod render;
mod status;

use page::Page;
use std::collections::BTreeMap;
use std::fs;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

const HELP: &str = "wf - Workshop workflow tool (see README.md)
Every command that writes needs --as <name> (or set WF_AS).
  init-page <page> --title T --person P --prime L --grant \"src/,tests/x.rs\" --grant-ref t300u
  set-prime <page> <name> --ref tNNNu         person or current prime
  grant <page> --paths \"a,b\" --ref t301u [--answers <entry>]   person
  face-write <page> <01|02|04|06|08> --text T | --file F [--section goals|decisions|responses]
  draft <page> --file pack.txt [--pass NN]      prime; pins 04, 06, last closed 05
  pack <page> <NN> [--overlap-ok NN --why T]    prime; checks, then prints the prompt box
  claim <page> <NN>                             builder; first claim wins
  return <page> <NN> --branch B --commit SHA --file PATH   the claim holder's ping
  check <page> <NN> [--note T] [--fail T] [--dry-run]   checker (never the builder); --dry-run writes nothing
  signoff <page> <NN> --outcome passed|failed|blocked|needs-authority [--cards w01=accepted,..] [--note T]
  close <page> <NN>                             writes the close record
  elevate <page> <NN> --to prime|person --item T
  answer <page> <entry> --text T
  status <page>                                 now strip, board, feed (read only)
  observe <page> [--stall-hours 24] [--record T]   observer signals; --record files a finding
  verify <page> [--fix]                         check the log chain and every view file
Root folder: current folder, or WF_ROOT.";

pub struct Args {
    pub pos: Vec<String>,
    flags: BTreeMap<String, String>,
}

impl Args {
    fn parse(raw: &[String]) -> Args {
        let (mut pos, mut flags, mut i) = (vec![], BTreeMap::new(), 0);
        while i < raw.len() {
            if let Some(k) = raw[i].strip_prefix("--") {
                let v = raw.get(i + 1).filter(|v| !v.starts_with("--")).cloned();
                i += if v.is_some() { 2 } else { 1 };
                flags.insert(k.to_string(), v.unwrap_or_default());
            } else {
                pos.push(raw[i].clone());
                i += 1;
            }
        }
        Args { pos, flags }
    }
    pub fn flag(&self, k: &str) -> Option<&str> {
        self.flags.get(k).map(|s| s.as_str())
    }
    pub fn req(&self, k: &str) -> log::Res<&str> {
        self.flag(k).filter(|v| !v.is_empty()).ok_or(format!("missing --{k}"))
    }
}

/// One writer at a time per page. A lock file; `take` retries for up to 5 seconds.
#[derive(Debug)]
pub(crate) struct Lock(PathBuf);
impl Lock {
    pub(crate) fn take(dir: &Path) -> log::Res<Lock> {
        Lock::acquire(dir, Duration::from_secs(5))
    }

    fn acquire(dir: &Path, wait: Duration) -> log::Res<Lock> {
        let p = dir.join(".wf-lock");
        let start = Instant::now();
        loop {
            match fs::OpenOptions::new().write(true).create_new(true).open(&p) {
                Ok(_) => return Ok(Lock(p)),
                Err(_) if start.elapsed() < wait => std::thread::sleep(Duration::from_millis(20)),
                Err(_) => {
                    return Err(format!(
                        "another wf command is writing this page ({} exists). If none is running, remove that file.",
                        p.display()
                    ))
                }
            }
        }
    }
}
impl Drop for Lock {
    fn drop(&mut self) {
        let _ = fs::remove_file(&self.0);
    }
}

/// Commands that append to the log or reprint views. The rest only read.
fn writes(c: &str, a: &Args) -> bool {
    match c {
        "status" | "help" | "--help" => false,
        "verify" => a.flag("fix").is_some(),
        "observe" => a.flag("record").is_some(),
        "check" => false, // commands run unlocked; check takes the lock itself before it appends
        _ => true,
    }
}

fn run(raw: &[String]) -> log::Res<()> {
    let c = raw.first().map(|s| s.as_str()).unwrap_or("help");
    let a = Args::parse(&raw[1.min(raw.len())..]);
    let root = std::env::var("WF_ROOT").map(PathBuf::from).unwrap_or_else(|_| PathBuf::from("."));
    let who = a.flag("as").map(String::from).or_else(|| std::env::var("WF_AS").ok()).unwrap_or_default();
    if c == "help" || c == "--help" {
        println!("{HELP}");
        return Ok(());
    }
    if c == "init-page" {
        need_who(&who)?;
        let (dir, _l) = cmd::init_page(&root, &a, &who)?;
        render::write(&Page::load(&dir)?)?;
        println!("page {} started. Next: Prime writes 01 and 04 goals.", a.pos[0]);
        return Ok(());
    }
    let addr = a.pos.first().ok_or("give the page address")?;
    page::check_addr(addr)?;
    let dir = root.join("pages").join(addr);
    if !dir.join("log.jsonl").exists() {
        return Err(format!("no page {addr} under {}", dir.display()));
    }
    let _l = if writes(c, &a) { Some(Lock::take(&dir)?) } else { None };
    let mut p = Page::load(&dir)?;
    let edited = render::edited(&p)?;
    match c {
        "status" => return Ok(print!("{}", status::status(&p))),
        "verify" => {
            if edited.is_empty() {
                println!("ok: log chain holds ({} entries, head {}); every view matches the log", p.events.len(), log::short(&p.head));
            } else if a.flag("fix").is_some() {
                render::write_except(&p, &edited.unreadable)?;
                let mut reprinted = edited.missing.clone();
                reprinted.extend(edited.changed.iter().cloned());
                if !reprinted.is_empty() {
                    println!("reprinted from the log: {}", reprinted.join(", "));
                }
                if !edited.unreadable.is_empty() {
                    return Err(format!(
                        "unreadable view files: {}. Make them readable, then run wf verify {addr} --fix if they still differ.",
                        edited.unreadable.join(", ")
                    ));
                }
            } else {
                return Err(format!("{}. The log is the truth; run wf verify {addr} --fix to reprint missing and changed views.", edited.report()));
            }
            return Ok(());
        }
        _ => {}
    }
    if !edited.is_empty() {
        return Err(format!(
            "refused: {}. Nobody writes page files directly. Run wf verify {addr} --fix to reprint missing and changed views from the log.",
            edited.report()
        ));
    }
    if c == "check" {
        need_who(&who)?;
        return cmd::check(&mut p, &root, &a, &who);
    }
    if c == "observe" {
        let found = status::observe(&p, a.flag("stall-hours").and_then(|h| h.parse().ok()).unwrap_or(24));
        println!("observer view of {addr} (prime: {})", p.prime);
        found.iter().for_each(|f| println!("  - {f}"));
        if found.is_empty() {
            println!("  findings: none");
        }
        let Some(text) = a.flag("record") else { return Ok(()) };
        need_who(&who)?;
        if who == p.prime {
            return Err("refused: the observer watches Prime, so Prime cannot file observer findings".into());
        }
        p.add(&who, "observer", "finding", serde_json::json!({"text": text, "evidence": found}))?;
        return render::write(&p);
    }
    need_who(&who)?;
    match c {
        "set-prime" => cmd::set_prime(&mut p, &a, &who),
        "grant" => cmd::grant(&mut p, &a, &who),
        "face-write" => cmd::face_write(&mut p, &a, &who),
        "draft" => cmd::draft(&mut p, &a, &who),
        "pack" => cmd::pack(&mut p, &root, &a, &who),
        "claim" => cmd::claim(&mut p, &a, &who),
        "return" => cmd::ret(&mut p, &root, &a, &who),
        "signoff" => cmd::signoff(&mut p, &a, &who),
        "close" => cmd::close(&mut p, &a, &who),
        "elevate" => cmd::elevate(&mut p, &a, &who),
        "answer" => cmd::answer(&mut p, &a, &who),
        _ => Err(format!("unknown command '{c}'. Run wf help")),
    }
    .and(Ok(()))
    .map_err(|e| {
        let _ = render::write(&p);
        e
    })?;
    render::write(&p)
}

fn need_who(who: &str) -> log::Res<()> {
    if who.is_empty() { Err("say who you are: --as <name> (or set WF_AS)".into()) } else { Ok(()) }
}

fn main() {
    let raw: Vec<String> = std::env::args().skip(1).collect();
    if let Err(e) = run(&raw) {
        eprintln!("wf: {e}");
        std::process::exit(1);
    }
}

#[cfg(test)]
mod lock_tests {
    use super::*;

    fn tmp(name: &str) -> PathBuf {
        let d = std::env::temp_dir().join(format!("wf-lock-{}-{name}", std::process::id()));
        let _ = fs::remove_dir_all(&d);
        fs::create_dir_all(&d).unwrap();
        d
    }

    #[test]
    fn acquire_succeeds_when_free() {
        let d = tmp("free");
        let l = Lock::acquire(&d, Duration::from_secs(1)).unwrap();
        assert!(d.join(".wf-lock").exists());
        drop(l);
        assert!(!d.join(".wf-lock").exists());
        let _ = fs::remove_dir_all(&d);
    }

    #[test]
    fn acquire_waits_then_succeeds() {
        let d = tmp("wait");
        fs::write(d.join(".wf-lock"), "").unwrap();
        let dir = d.clone();
        let h = std::thread::spawn(move || {
            std::thread::sleep(Duration::from_millis(40));
            fs::remove_file(dir.join(".wf-lock")).unwrap();
        });
        let start = Instant::now();
        let l = Lock::acquire(&d, Duration::from_millis(400)).unwrap();
        assert!(start.elapsed() >= Duration::from_millis(40));
        drop(l);
        h.join().unwrap();
        let _ = fs::remove_dir_all(&d);
    }

    #[test]
    fn acquire_refuses_after_the_wait() {
        let d = tmp("busy");
        fs::write(d.join(".wf-lock"), "").unwrap();
        let start = Instant::now();
        let err = Lock::acquire(&d, Duration::from_millis(60)).unwrap_err();
        assert!(start.elapsed() >= Duration::from_millis(60));
        assert!(err.contains("another wf command is writing"));
        let _ = fs::remove_dir_all(&d);
    }
}
