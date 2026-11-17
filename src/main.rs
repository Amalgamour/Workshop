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

const HELP: &str = "wf - Workshop workflow tool (see README.md)
Every command that writes needs --as <name> (or set WF_AS).
  init-page <page> --title T --person P --prime L --grant \"src/,tests/x.rs\" --grant-ref t300u
  set-prime <page> <name>                     person or current prime
  grant <page> --paths \"a,b\" --ref t301u [--answers <entry>]   person
  face-write <page> <01|02|04|06|08> --text T | --file F [--section goals|decisions|responses]
  draft <page> --file pack.txt [--pass NN]      prime; pins 04, 06, last closed 05
  pack <page> <NN>                              prime; checks, then prints the prompt box
  claim <page> <NN>                             builder; first claim wins
  return <page> <NN> --branch B --commit SHA --file PATH   the claim holder's ping
  check <page> <NN> [--note T] [--fail T]       checker (never the builder)
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

/// One writer at a time per page.
struct Lock(PathBuf);
impl Lock {
    fn take(dir: &Path) -> log::Res<Lock> {
        let p = dir.join(".wf-lock");
        fs::OpenOptions::new().write(true).create_new(true).open(&p)
            .map_err(|_| format!("another wf command is writing this page ({} exists). If none is running, remove that file.", p.display()))?;
        Ok(Lock(p))
    }
}
impl Drop for Lock {
    fn drop(&mut self) {
        let _ = fs::remove_file(&self.0);
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
        let dir = cmd::init_page(&root, &a, &who)?;
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
    let mut p = Page::load(&dir)?;
    let edited = render::edited(&p)?;
    match c {
        "status" => return Ok(print!("{}", status::status(&p))),
        "verify" => {
            if edited.is_empty() {
                println!("ok: log chain holds ({} entries, head {}); every view matches the log", p.events.len(), log::short(&p.head));
            } else if a.flag("fix").is_some() {
                render::write(&p)?;
                println!("reprinted from the log: {}", edited.join(", "));
            } else {
                return Err(format!("hand-edited view files: {}. The log is the truth; run wf verify {addr} --fix to reprint them.", edited.join(", ")));
            }
            return Ok(());
        }
        _ => {}
    }
    if !edited.is_empty() {
        return Err(format!("refused: hand-edited page files: {}. Nobody writes page files directly. Run wf verify {addr} --fix to reprint them from the log.", edited.join(", ")));
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
        let _l = Lock::take(&dir)?;
        p.add(&who, "observer", "finding", serde_json::json!({"text": text, "evidence": found}))?;
        return render::write(&p);
    }
    need_who(&who)?;
    let _l = Lock::take(&dir)?;
    match c {
        "set-prime" => cmd::set_prime(&mut p, &a, &who),
        "grant" => cmd::grant(&mut p, &a, &who),
        "face-write" => cmd::face_write(&mut p, &a, &who),
        "draft" => cmd::draft(&mut p, &a, &who),
        "pack" => cmd::pack(&mut p, &root, &a, &who),
        "claim" => cmd::claim(&mut p, &a, &who),
        "return" => cmd::ret(&mut p, &root, &a, &who),
        "check" => cmd::check(&mut p, &root, &a, &who),
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
