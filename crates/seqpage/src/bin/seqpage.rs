//! `seqpage export | import | check` (docs/spec/seqpage.md 12). JSON reports
//! on stdout; exit 1 on any error. Import never writes a book: it prints the
//! proposal (and, with `--books`, the core's dry-run verdict on it).

use seqaddr_core::addr::BookId;
use seqaddr_core::log::BookLog;
use seqaddr_core::{BookState, Policy, World};
use seqpage::write::derived_title;
use seqpage::{check_text, export, file_name, import, page_entries, pages_in, PageId};
use serde_json::json;
use std::process::exit;

const USAGE: &str = "usage:
  seqpage export <book-file> <DD.SS.BB.PPPP> [--out FILE | --dir DIR]
  seqpage export <book-file> --all --dir DIR
  seqpage import <file.seq> [--book BOOK-FILE] [--by NAME] [--books DIR]
  seqpage check  <file.seq> [--book BOOK-FILE]";

fn die(msg: impl std::fmt::Display) -> ! {
    println!("{}", json!({"ok": false, "error": msg.to_string()}));
    exit(1)
}

fn opt(args: &[String], name: &str) -> Option<String> {
    args.iter().position(|a| a == name).and_then(|i| args.get(i + 1).cloned())
}

fn read_book(path: &str) -> BookLog {
    seqaddr_core::log::file::read(std::path::Path::new(path)).unwrap_or_else(|e| die(format!("{path}: {e}")))
}

fn load_world(dir: &str) -> World {
    let mut w = World::new(Policy::default());
    let rd = std::fs::read_dir(dir).unwrap_or_else(|e| die(format!("{dir}: {e}")));
    for ent in rd.flatten() {
        let p = ent.path();
        if p.extension().and_then(|x| x.to_str()) == Some("book") {
            let log = seqaddr_core::log::file::read(&p).unwrap_or_else(|e| die(format!("{}: {e}", p.display())));
            let st = BookState::replay(&log, &w.policy).unwrap_or_else(|e| die(format!("{}: {e}", p.display())));
            w.insert(st);
        }
    }
    w
}

fn export_one(log: &BookLog, page: PageId, out: Option<&str>, dir: Option<&str>) -> serde_json::Value {
    let text = match export(log, page) {
        Ok(t) => t,
        Err(e) => return json!({"page": page.to_string(), "ok": false, "error": e}),
    };
    let name = file_name(page, derived_title(page, &page_entries(log, page)).as_deref());
    let path = match (out, dir) {
        (Some(o), _) => Some(o.to_string()),
        (None, Some(d)) => Some(format!("{}/{}", d.trim_end_matches('/'), name)),
        _ => None,
    };
    match path {
        Some(p) => {
            if let Err(e) = std::fs::write(&p, &text) {
                die(format!("{p}: {e}"));
            }
            json!({"page": page.to_string(), "ok": true, "file": p})
        }
        None => {
            print!("{text}");
            exit(0)
        }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let cmd = args.first().map(String::as_str).unwrap_or("");
    match cmd {
        "export" => {
            let book = args.get(1).unwrap_or_else(|| die(USAGE));
            let log = read_book(book);
            let dir = opt(&args, "--dir");
            if args.iter().any(|a| a == "--all") {
                let dir = dir.unwrap_or_else(|| die("--all needs --dir DIR"));
                let res: Vec<_> = pages_in(&log).into_iter().map(|p| export_one(&log, p, None, Some(&dir))).collect();
                let ok = res.iter().all(|r| r["ok"] == true);
                println!("{}", serde_json::to_string_pretty(&json!({"ok": ok, "pages": res})).unwrap());
                exit(if ok { 0 } else { 1 });
            }
            let page = args.get(2).unwrap_or_else(|| die(USAGE));
            let page = PageId::parse(page).unwrap_or_else(|e| die(e));
            if page.book != BookId::parse(&log.header.address).unwrap_or_else(|e| die(e)) {
                die(format!("page {page} is not in book {}", log.header.address));
            }
            let r = export_one(&log, page, opt(&args, "--out").as_deref(), dir.as_deref());
            let ok = r["ok"] == true;
            println!("{}", serde_json::to_string_pretty(&r).unwrap());
            exit(if ok { 0 } else { 1 });
        }
        "import" => {
            let file = args.get(1).unwrap_or_else(|| die(USAGE));
            let text = std::fs::read_to_string(file).unwrap_or_else(|e| die(format!("{file}: {e}")));
            let book = opt(&args, "--book").map(|b| read_book(&b));
            let by = opt(&args, "--by").unwrap_or_else(|| "user".to_string());
            match import(&text, book.as_ref(), &by) {
                Err(rep) => {
                    println!("{}", serde_json::to_string_pretty(&rep).unwrap());
                    exit(1)
                }
                Ok(imp) => {
                    let mut out = json!({"ok": true, "page": imp.page, "booked": imp.booked, "proposal": imp.proposal, "findings": imp.findings});
                    if let Some(dir) = opt(&args, "--books") {
                        let w = load_world(&dir);
                        let outcome = seqaddr_core::validate(&w, &imp.proposal, &seqaddr_core::log::now_utc());
                        out["dry_run"] = serde_json::to_value(&outcome).unwrap();
                        out["note"] = json!("dry run only: nothing was written; the compute books an approved proposal");
                    }
                    println!("{}", serde_json::to_string_pretty(&out).unwrap());
                }
            }
        }
        "check" => {
            let file = args.get(1).unwrap_or_else(|| die(USAGE));
            let text = std::fs::read_to_string(file).unwrap_or_else(|e| die(format!("{file}: {e}")));
            let book = opt(&args, "--book").map(|b| read_book(&b));
            let rep = check_text(&text, Some(file), book.as_ref());
            println!("{}", serde_json::to_string_pretty(&rep).unwrap());
            exit(if rep.ok { 0 } else { 1 });
        }
        _ => die(USAGE),
    }
}
