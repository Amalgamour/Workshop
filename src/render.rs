//! Views. Every file in a page folder except log.jsonl is printed here from the log.
//! Templates are fixed text built into the binary; only the tool fills them.

use crate::log::{sha, short, Res};
use crate::page::{s, Page, Pass, FACES};
use serde_json::Value;
use std::collections::BTreeMap;
use std::fs;

pub const T_PACK: &str = include_str!("../templates/pack.txt");
pub const T_PROMPT: &str = include_str!("../templates/prompt.txt");
pub const T_AGENTS: &str = include_str!("../templates/agents.txt");
pub const T_RETURN: &str = include_str!("../templates/return.txt");
pub const T_CLOSE: &str = include_str!("../templates/close.txt");
pub const AXIOMS: &str = include_str!("../docs/AXIOMS.md");
pub const DESIGN: &str = include_str!("../docs/DESIGN.md");

/// Fill `{{key}}` slots. Refuses if a slot is left empty or unknown.
pub fn fill(t: &str, vals: &[(&str, String)]) -> Res<String> {
    let mut out = t.to_string();
    for (k, v) in vals {
        out = out.replace(&format!("{{{{{k}}}}}"), v);
    }
    match out.find("{{") {
        Some(i) => Err(format!("template slot left unfilled: {}", &out[i..out[i..].find("}}").map(|j| i + j + 2).unwrap_or(out.len())])),
        None => Ok(out),
    }
}

pub fn pass_name(p: &Page, nn: u32) -> String {
    format!("{}.05.{nn:02}", p.addr)
}

pub fn jobs(f: &serde_json::Map<String, Value>) -> Vec<(String, String)> {
    f.iter().filter(|(k, _)| k.len() == 3 && k.starts_with('w')).map(|(k, v)| (k.clone(), v.as_str().unwrap_or("").to_string())).collect()
}

fn jobs_text(f: &serde_json::Map<String, Value>) -> String {
    jobs(f).iter().map(|(k, v)| format!("  {k}: {v}")).collect::<Vec<_>>().join("\n")
}

/// The values every pass template shares, read from the pack event.
fn pass_vals(p: &Page, x: &Pass) -> Vec<(&'static str, String)> {
    let pk = x.pack.as_ref().cloned().unwrap_or(Value::Null);
    let f = &x.fields;
    let g = |k: &str| f.get(k).and_then(|v| v.as_str()).unwrap_or("").to_string();
    vec![
        ("pass", pass_name(p, x.nn)),
        ("addr", p.addr.clone()),
        ("nn", format!("{:02}", x.nn)),
        ("dir", format!("pages/{}/05.{:02}", p.addr, x.nn)),
        ("pack_hash", s(&pk, "pack_hash")),
        ("seq", pk["seq"].to_string()),
        ("time", s(&pk, "time")),
        ("repo", g("repo")),
        ("start", s(&pk, "start")),
        ("branch", s(&pk, "branch")),
        ("return_file", s(&pk, "return_file")),
        ("jobs", jobs_text(f)),
        ("may_touch", g("may touch")),
        ("checks", g("checks")),
        ("stop_if", g("stop if")),
        ("axioms", g("axioms")),
        ("src01", s(&pk["sources"], "01")),
        ("src_axioms", s(&pk["sources"], "axioms")),
        ("src_design", s(&pk["sources"], "design")),
        ("face01", s(&pk, "face01")),
    ]
}

pub fn prompt(p: &Page, x: &Pass) -> Res<String> {
    fill(T_PROMPT, &pass_vals(p, x))
}

pub fn agents(p: &Page, x: &Pass) -> Res<String> {
    fill(T_AGENTS, &pass_vals(p, x))
}

pub fn return_template(p: &Page, x: &Pass) -> Res<String> {
    let mut v = pass_vals(p, x);
    let lines = jobs(&x.fields).iter().map(|(k, j)| format!("{k}: <done | need | blocked> - {j}")).collect::<Vec<_>>().join("\n");
    v.push(("job_lines", lines));
    fill(T_RETURN, &v)
}

fn face_text(p: &Page, f: &str) -> String {
    p.faces.get(f).map(|x| x.text.clone()).unwrap_or_default()
}

fn face_head(p: &Page, f: &str, name: &str) -> String {
    let v = match p.faces.get(f) {
        Some(x) => format!("v{} (entry {}, hash {})", x.version, x.seq, short(&x.hash())),
        None if ["00", "03", "05"].contains(&f) => "built fresh from the log".into(),
        None => "empty".into(),
    };
    format!("# {f} {name}: {}\nView printed by wf from log.jsonl. Do not edit. Version: {v}\n\n", p.addr)
}

fn face05(p: &Page) -> String {
    let mut o = face_head(p, "05", "work");
    for x in p.passes.values() {
        o += &format!("## 05.{:02}  tail: {}  claim: {}\n", x.nn, x.tail, x.claim.as_deref().unwrap_or("-"));
        if let Some(pk) = &x.pack {
            o += &format!("pack: {} (see 05.{:02}/PACK.md)\n", s(pk, "pack_hash"), x.nn);
        } else {
            o += "draft fields:\n";
            for (k, v) in &x.fields {
                o += &format!("  {k}: {}\n", v.as_str().unwrap_or(""));
            }
        }
        for (seq, why) in &x.refusals {
            o += &format!("return refused (entry {seq}): {why}\n");
        }
        if let Some(r) = &x.ret {
            o += &format!("return: {} at {} (hash {})\n", s(r, "file"), s(r, "commit"), short(&s(r, "hash")));
            o += &format!("```\n{}\n```\n", s(r, "text").trim_end());
        }
        if let Some((who, c)) = &x.check {
            o += &format!("check by {who}: verdict {}\n{}", s(c, "verdict"), s(c, "report"));
        }
        if let Some((who, seq, d)) = &x.signoff {
            o += &format!("signed off: {who} at entry {seq}, outcome {}\n", s(d, "outcome"));
        }
        if let Some(c) = &x.close {
            o += &format!("```\n{}```\n", s(c, "record"));
        }
        o += "\n";
    }
    o
}

fn face00(p: &Page) -> String {
    let mut o = face_head(p, "00", "stamp");
    o += &format!("title:   {}\nperson:  {}\nprime:   {} (since entry {})\nprevious primes:\n", p.title, p.person, p.prime, p.primes.last().map(|x| x.1).unwrap_or(0));
    for (n, a, b) in &p.primes[..p.primes.len().saturating_sub(1)] {
        o += &format!("  - {n}: entries {a}-{b}\n");
    }
    o += &format!("grant:   {} (from {})\n", p.grant.join(", "), p.grant_refs.join(", "));
    o += &format!("log:     {} entries, head {}\n", p.events.len(), short(&p.head));
    o
}

fn face03(p: &Page) -> String {
    let mut o = face_head(p, "03", "menu");
    let names = ["stamp", "agents card", "pseudo code", "menu", "dev space", "work", "prime notes", "labs", "connections"];
    for (i, f) in FACES.iter().enumerate() {
        let st = match *f {
            "05" => p.passes.values().map(|x| format!("05.{:02} {}", x.nn, x.tail)).collect::<Vec<_>>().join(", "),
            "00" | "03" => "printed by wf".into(),
            _ => p.faces.get(*f).map(|x| format!("v{}", x.version)).unwrap_or("empty".into()),
        };
        o += &format!("{f} {:<12} {}\n", names[i], st);
    }
    o
}

/// Every view file of the page: relative path -> text.
pub fn views(p: &Page) -> Res<BTreeMap<String, String>> {
    let mut m = BTreeMap::new();
    m.insert("00.md".into(), face00(p));
    for (f, n) in [("01", "agents card"), ("02", "pseudo code"), ("04", "dev space"), ("06", "prime notes"), ("08", "connections")] {
        m.insert(format!("{f}.md"), face_head(p, f, n) + &face_text(p, f));
    }
    m.insert("03.md".into(), face03(p));
    m.insert("05.md".into(), face05(p));
    m.insert("07.md".into(), face_head(p, "07", "labs") + "Labs are not built in wf v0.\n");
    for x in p.passes.values() {
        if let Some(pk) = &x.pack {
            let d = format!("05.{:02}/", x.nn);
            m.insert(d.clone() + "PACK.md", s(pk, "pack_text"));
            m.insert(d.clone() + "PROMPT.md", prompt(p, x)?);
            m.insert(d.clone() + "AGENTS.md", agents(p, x)?);
            m.insert(d + "RETURN-TEMPLATE.md", return_template(p, x)?);
        }
    }
    Ok(m)
}

/// Compare the view files on disk with the log. Returns the files that differ.
pub fn edited(p: &Page) -> Res<Vec<String>> {
    let mut bad = vec![];
    for (rel, text) in views(p)? {
        if let Ok(disk) = fs::read_to_string(p.dir.join(&rel)) {
            if sha(&disk) != sha(&text) {
                bad.push(rel);
            }
        }
    }
    Ok(bad)
}

pub fn write(p: &Page) -> Res<()> {
    for (rel, text) in views(p)? {
        let path = p.dir.join(&rel);
        if let Some(d) = path.parent() {
            fs::create_dir_all(d).map_err(|e| e.to_string())?;
        }
        if fs::read_to_string(&path).ok().as_deref() != Some(text.as_str()) {
            fs::write(&path, text).map_err(|e| e.to_string())?;
        }
    }
    Ok(())
}

pub fn version_of(text: &str) -> String {
    format!("hash {}", short(&sha(text)))
}

pub fn cards_text(v: &Value) -> String {
    v.as_object().map(|m| m.iter().map(|(k, v)| format!("{k} {}", v.as_str().unwrap_or(""))).collect::<Vec<_>>().join(", ")).unwrap_or_default()
}

