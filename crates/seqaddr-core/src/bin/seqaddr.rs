//! `seqaddr`: a small tool for people to check addresses and books.
//!
//! ```text
//! seqaddr parse <addr> [--active DD.SS.BB[:PPPP,...]]
//! seqaddr validate <addr>
//! seqaddr axioms <chain>
//! seqaddr replay <book-file> [--until N]
//! seqaddr history <book-file> <addr>
//! seqaddr resolve <addr> --books <dir> [--active DD.SS.BB[:PPPP]]
//! seqaddr propose <proposal.json> --books <dir>      (dry run, writes nothing)
//! ```

use seqaddr_core::addr::{axis_role, band_of, desk_kind, page_kind, Active, Address, BookId};
use seqaddr_core::face::face_job;
use seqaddr_core::{AxiomChain, BookState, Policy, Proposal, SeqError, World};
use serde_json::{json, Value};
use std::path::Path;
use std::process::ExitCode;

fn err_json(e: &SeqError) -> Value {
    json!({"error": e.code(), "rule": e.rule(), "axiom": e.axiom(), "detail": e.detail()})
}

fn flag<'a>(args: &'a [String], name: &str) -> Option<&'a str> {
    args.iter().position(|a| a == name).and_then(|i| args.get(i + 1)).map(|s| s.as_str())
}

fn parse_active(s: &str) -> Result<Active, SeqError> {
    let (b, pages) = match s.split_once(':') {
        Some((b, p)) => (b, p.split(',').map(|x| x.parse::<u16>().map_err(|_| SeqError::invalid("A1.6", format!("bad page `{x}`")))).collect::<Result<Vec<_>, _>>()?),
        None => (s, vec![]),
    };
    Ok(Active { book: BookId::parse(b)?, pages })
}

fn load_world(dir: &str) -> Result<World, SeqError> {
    let mut w = World::new(Policy::default());
    let rd = std::fs::read_dir(dir).map_err(|e| SeqError::Io { detail: e.to_string() })?;
    for ent in rd.flatten() {
        let p = ent.path();
        if p.extension().and_then(|x| x.to_str()) == Some("book") {
            let log = seqaddr_core::log::file::read(&p)?;
            let st = BookState::replay(&log, &w.policy).map_err(|e| SeqError::Corrupt { line: 0, detail: format!("{}: {e}", p.display()) })?;
            w.insert(st);
        }
    }
    Ok(w)
}

fn describe(a: &Address) -> Value {
    match a {
        Address::Container(c) => json!({
            "kind": "container", "full": a.to_string(), "level": c.level(),
            "desk_kind": desk_kind(c.desk),
            "shelf_role": c.shelf.map(axis_role), "book_role": c.book.map(axis_role),
            "own_book": c.own_book().to_string(), "door_page": c.door_page().to_string(),
        }),
        Address::Page(p) => json!({
            "kind": "page", "written": a.to_string(), "form": p.form(), "page_kind": page_kind(p.page), "band": band_of(p.page),
            "title": p.title, "tail": p.tail(),
            "face": p.face.as_ref().map(|f| json!({"face": f.face, "job": face_job(f.face).name(), "counter": f.counter, "tail": f.tail, "card": f.card, "brand": f.brand})),
        }),
        Address::ActiveRel(f) => json!({"kind": "active_relative", "face": f.face, "job": face_job(f.face).name(), "counter": f.counter, "tail": f.tail}),
    }
}

fn run(args: &[String]) -> Result<Value, SeqError> {
    let cmd = args.first().map(|s| s.as_str()).unwrap_or("help");
    let arg = |i: usize| args.get(i).map(|s| s.as_str()).ok_or_else(|| SeqError::invalid("cli", "missing argument; run `seqaddr help`"));
    match cmd {
        "parse" | "validate" => {
            let a = Address::parse(arg(1)?)?;
            let mut out = describe(&a);
            if let Some(act) = flag(args, "--active") {
                let full = a.expand(&parse_active(act)?)?;
                out["expanded"] = json!(full.to_string());
            }
            if cmd == "validate" {
                out = json!({"ok": true, "address": out});
            }
            Ok(out)
        }
        "axioms" => {
            let c = AxiomChain::parse(arg(1)?)?;
            Ok(json!({"chain": c.to_string(), "reads": c.describe()}))
        }
        "replay" => {
            let log = seqaddr_core::log::file::read(Path::new(arg(1)?))?;
            let pol = Policy::default();
            let st = match flag(args, "--until") {
                Some(n) => BookState::replay_until(&log, n.parse().unwrap_or(u64::MAX), &pol)?,
                None => BookState::replay(&log, &pol)?,
            };
            let pages: Vec<Value> = st
                .pages
                .iter()
                .map(|(p, pg)| {
                    json!({"page": format!("{p:04}"), "title": pg.title(), "state": pg.tail(),
                    "faces": pg.faces.iter().map(|(f, fs)| json!({"face": format!("{f:02}"), "slot": fs.slot_state(),
                        "counters": fs.counters.iter().map(|(n, c)| json!({"counter": format!("{n:02}"), "tail": c.tail.board_word(), "claim": c.claim.as_ref().map(|c| c.owner.clone())})).collect::<Vec<_>>()})).collect::<Vec<_>>()})
                })
                .collect();
            Ok(json!({"book": st.book.to_string(), "title": st.title(), "entries": log.entries.len(), "dropped_partial": log.dropped_partial, "pages": pages}))
        }
        "history" => {
            let log = seqaddr_core::log::file::read(Path::new(arg(1)?))?;
            Ok(serde_json::to_value(log.history(arg(2)?)?).unwrap())
        }
        "resolve" => {
            let w = load_world(flag(args, "--books").unwrap_or("books"))?;
            let act = flag(args, "--active").map(parse_active).transpose()?;
            let r = w.resolve_str(arg(1)?, act.as_ref())?;
            Ok(serde_json::to_value(r).unwrap())
        }
        "propose" => {
            let w = load_world(flag(args, "--books").unwrap_or("books"))?;
            let text = std::fs::read_to_string(arg(1)?).map_err(|e| SeqError::Io { detail: e.to_string() })?;
            let p: Proposal = serde_json::from_str(&text).map_err(|e| SeqError::invalid("cli", e.to_string()))?;
            let out = seqaddr_core::validate(&w, &p, &seqaddr_core::log::now_utc());
            Ok(serde_json::to_value(out).unwrap())
        }
        _ => Ok(json!({"usage": [
            "seqaddr parse <addr> [--active DD.SS.BB[:PPPP,...]]",
            "seqaddr validate <addr>",
            "seqaddr axioms <chain>",
            "seqaddr replay <book-file> [--until N]",
            "seqaddr history <book-file> <addr>",
            "seqaddr resolve <addr> --books <dir> [--active DD.SS.BB[:PPPP]]",
            "seqaddr propose <proposal.json> --books <dir>   (dry run)"
        ]})),
    }
}

fn main() -> ExitCode {
    let args: Vec<String> = std::env::args().skip(1).collect();
    match run(&args) {
        Ok(v) => {
            println!("{}", serde_json::to_string_pretty(&v).unwrap());
            ExitCode::SUCCESS
        }
        Err(e) => {
            println!("{}", serde_json::to_string_pretty(&err_json(&e)).unwrap());
            ExitCode::from(1)
        }
    }
}
