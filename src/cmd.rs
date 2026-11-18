//! The commands that write. Each one checks the role, then appends to the log.

use crate::chars::{self, check_text, check_text_nl};
use crate::git;
use crate::log::{sha, short, Res};
use crate::page::{check_addr, done_when_lines, face01_drift, inside, paths_overlap, s, split_list, Page, Pass};
use crate::render::{self, fill, jobs, pass_name, AXIOMS, DESIGN, T_CLOSE, T_PACK};
use crate::Args;
use serde_json::{json, Map, Value};
use std::fs;
use std::path::{Path, PathBuf};

const CARD_WORDS: [&str; 4] = ["accepted", "carried", "discarded", "candidate"];
const OUTCOMES: [&str; 4] = ["passed", "failed", "blocked", "needs-authority"];
const RETURN_KEYS: [&str; 7] = ["done", "changed", "noticed", "proof", "not done", "unprompted", "overflow"];
const REQUIRED: [&str; 6] = ["outcome", "repo", "start", "may touch", "checks", "stop if"];

fn need(ok: bool, msg: impl Into<String>) -> Res<()> {
    if ok { Ok(()) } else { Err(msg.into()) }
}

/// Text that is not empty after trimming. Used for --ref and --text, and by why_ref.
fn nonblank<'a>(text: &'a str, flag: &str) -> Res<&'a str> {
    let t = text.trim();
    need(!t.is_empty(), format!("--{flag} must have non-blank text"))?;
    check_text(text, flag)?;
    Ok(t)
}

pub(crate) fn no_ctrl(text: &str, flag: &str) -> Res<()> {
    check_text(text, flag)
}

/// A valid "<why> (ref)": both the why and the ref have non-blank text after trimming.
fn why_ref<'a>(text: &'a str, flag: &str) -> Res<&'a str> {
    no_ctrl(text, flag)?;
    let t = text.trim();
    let ok = match (t.find('('), t.rfind(')')) {
        (Some(i), Some(j)) if j > i => !t[..i].trim().is_empty() && nonblank(&t[i + 1..j], flag).is_ok(),
        _ => false,
    };
    need(ok, format!("--{flag} needs a reason and a (ref), like \"why (t275u)\""))?;
    if let (Some(i), _) = (t.find('('), t.rfind(')')) {
        check_text(t[..i].trim(), flag)?;
    }
    Ok(t)
}

fn job_word(v: &Value) -> &str {
    v.as_str().unwrap_or("").split_whitespace().next().unwrap_or("")
}

fn jobs_not_done(ret: &Value) -> Vec<String> {
    ret["jobs"]
        .as_object()
        .map(|m| m.iter().filter(|(_, v)| matches!(job_word(v), "need" | "blocked")).map(|(k, _)| k.clone()).collect())
        .unwrap_or_default()
}

fn must_be(p: &Page, who: &str, role: &str) -> Res<()> {
    let holder = if role == "prime" { &p.prime } else { &p.person };
    need(who == holder, format!("refused: only the {role} ({holder}) may do this, not {who}"))
}

/// Draft, pack and claim stop on a halted page.
fn not_halted(p: &Page) -> Res<()> {
    match &p.halt {
        Some((who, _, note, seq)) => Err(format!("refused: page {} is halted (by {who}, entry {seq}: {note}). {}", p.addr, crate::status::how_to_resume(p))),
        None => Ok(()),
    }
}

fn prime_or_person(p: &Page, who: &str) -> Res<&'static str> {
    need(who == p.prime || who == p.person, format!("refused: only Prime ({}) or the person ({}) may do this, not {who}", p.prime, p.person))?;
    Ok(if who == p.person { "person" } else { "prime" })
}

/// Stop work on the page. Refused while a pass holds files (pack, open, return or review).
pub fn halt(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let role = prime_or_person(p, who)?;
    let note = why_ref(a.flag("note").unwrap_or(""), "note")?.to_string();
    need(p.halt.is_none(), format!("refused: page {} is already halted", p.addr))?;
    if let Some(x) = p.passes.values().find(|x| x.is_open_tail()) {
        return Err(format!("refused: 05.{:02} is at '{}'; halt only when no pass is open. Next for it: {}", x.nn, x.tail, crate::status::pass_next(p, x)));
    }
    p.add(who, role, "halt", json!({"note": note}))?;
    println!("page {} halted. To go on: wf resume {} --note \"why (ref)\"", p.addr, p.addr);
    Ok(())
}

pub fn resume(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let role = prime_or_person(p, who)?;
    let note = why_ref(a.flag("note").unwrap_or(""), "note")?.to_string();
    need(p.halt.is_some(), format!("refused: page {} is not halted", p.addr))?;
    p.add(who, role, "resume", json!({"note": note}))?;
    println!("page {} resumed.", p.addr);
    Ok(())
}

/// A pass part the command needs is not in the log (a forged or wrong-order log).
fn no_part(n: u32, what: &str) -> String {
    format!("refused: 05.{n:02} has no {what} in the log; nothing was written. Run wf verify to check the log")
}

fn tail_is(x: &Pass, want: &[&str]) -> Res<()> {
    need(want.contains(&x.tail.as_str()), format!("refused: 05.{:02} is at '{}', this needs {}", x.nn, x.tail, want.join(" or ")))
}

/// Digits, or 05.NN. Refuses signed forms like +1.
pub(crate) fn parse_pass(v: &str, err: &str) -> Res<u32> {
    let v = v.strip_prefix("05.").unwrap_or(v);
    if v.is_empty() || !v.bytes().all(|b| b.is_ascii_digit()) {
        return Err(err.into());
    }
    v.parse().map_err(|_| err.to_string())
}

/// `05.NN` for a pass number in 01-98; otherwise `pass N` (never `05.100`).
fn pass_label(n: u32) -> String {
    if (1..=98).contains(&n) { format!("05.{n:02}") } else { format!("pass {n}") }
}

fn nn(a: &Args, i: usize) -> Res<u32> {
    parse_pass(a.pos.get(i).map(|s| s.as_str()).unwrap_or(""), "give the pass number, like 3 or 05.03")
}

/// Pass numbers are 01-98 (R9). 00 is not a pass; after 98 is open (QD16).
fn pass_number_ok(n: u32) -> Res<()> {
    if n == 0 {
        return Err("refused: pass 0 is not allowed (R9)".into());
    }
    if n > 98 {
        return Err("counter 98 reached: after 98 is open (QD16); ask Prime".into());
    }
    Ok(())
}

fn text_arg(a: &Args) -> Res<String> {
    match (a.flag("text"), a.flag("file")) {
        (Some(t), _) => Ok(t.to_string()),
        (_, Some(f)) => fs::read_to_string(f).map_err(|e| format!("cannot read {f}: {e}")),
        _ => Err("give --text \"...\" or --file path".into()),
    }
}

/// `key: value` lines; a line starting with spaces continues the last key.
pub fn fields(text: &str) -> Map<String, Value> {
    let mut m = Map::new();
    let mut last = String::new();
    for line in text.lines() {
        if line.starts_with(' ') && !last.is_empty() {
            let v = format!("{}\n{}", m[&last].as_str().unwrap_or(""), line.trim());
            m.insert(last.clone(), v.into());
        } else if let Some((k, v)) = line.split_once(':') {
            last = k.trim().to_lowercase();
            m.insert(last.clone(), v.trim().into());
        }
    }
    m
}

fn repo(root: &Path, x: &Pass) -> PathBuf {
    root.join(x.fields.get("repo").and_then(|v| v.as_str()).unwrap_or("."))
}

pub fn init_page(root: &Path, a: &Args, who: &str) -> Res<(PathBuf, crate::Lock)> {
    let addr = a.pos.first().ok_or("give a page address")?;
    check_addr(addr)?;
    let person = a.req("person")?;
    check_text(person, "person")?;
    need(who == person, "refused: the person starts their own page (--as must match --person)")?;
    let title = a.req("title")?;
    check_text(title, "title")?;
    let prime = a.req("prime")?;
    check_text(prime, "prime")?;
    let grant_raw = a.req("grant")?;
    check_text(grant_raw, "grant")?;
    let grant = split_list(grant_raw);
    let grant_ref = a.req("grant-ref")?;
    check_text(grant_ref, "grant-ref")?;
    let dir = root.join("pages").join(addr);
    fs::create_dir_all(&dir).map_err(|e| e.to_string())?;
    let lock = crate::Lock::take(&dir)?;
    need(!dir.join("log.jsonl").exists(), format!("refused: page {addr} already exists"))?;
    let data = json!({"address": addr, "title": title, "person": person, "prime": prime,
                      "grant": grant, "grant_ref": grant_ref});
    crate::log::append(&dir.join("log.jsonl"), "0", 1, who, "person", "init", data)?;
    Ok((dir, lock))
}

pub fn set_prime(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    need(who == p.person || who == p.prime, "refused: only the person or the current prime may set prime")?;
    let name = a.pos.get(1).ok_or("give the new prime's name")?;
    check_text(name, "name")?;
    p.add(who, "person", "prime", json!({"name": name, "ref": nonblank(a.req("ref")?, "ref")?}))
}

pub fn grant(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    must_be(p, who, "person")?;
    let ans = a.flag("answers").and_then(|x| x.parse::<u64>().ok());
    let grant_ref = nonblank(a.req("ref")?, "ref")?;
    let paths = a.req("paths")?;
    check_text(paths, "paths")?;
    p.add(who, "person", "grant", json!({"paths": split_list(paths), "ref": grant_ref}))?;
    if let Some(seq) = ans {
        p.add(who, "person", "answer", json!({"elevation": seq, "text": format!("grant {grant_ref} widened")}))?;
    }
    Ok(())
}

pub fn face_write(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let face = a.pos.get(1).map(|x| x.as_str()).unwrap_or("");
    let text = text_arg(a)?;
    if a.flag("file").is_some() {
        check_text_nl(&text, "file")?;
    } else {
        check_text_nl(&text, "text")?;
    }
    let (mode, section, role) = match (face, a.flag("section").unwrap_or("")) {
        ("01" | "02" | "08", _) => ("replace", "", "prime"),
        ("04", "responses") => ("append", "responses", "person"),
        ("04", sec @ ("goals" | "decisions")) => ("append", sec, "prime"),
        ("04", _) => return Err("face 04 needs --section goals, decisions (prime) or responses (person)".into()),
        ("06", _) => ("append", "note", "prime"),
        ("00" | "03" | "05", _) => return Err(format!("refused: face {face} is printed by wf; nobody writes it")),
        _ => return Err(format!("refused: face '{face}' cannot be written in wf v0")),
    };
    must_be(p, who, role)?;
    p.add(who, role, "face", json!({"face": face, "mode": mode, "section": section, "text": text}))
}

fn pin(p: &Page, f: &str) -> Value {
    p.faces.get(f).map(|x| json!({"entry": x.seq, "hash": x.hash()})).unwrap_or(json!("none"))
}

fn pin05(p: &Page) -> Value {
    p.last_closed().map(|x| json!({"pass": x.nn, "entry": x.last_seq})).unwrap_or(json!("none"))
}

pub fn draft(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    must_be(p, who, "prime")?;
    not_halted(p)?;
    let mut f = fields(&text_arg(a)?);
    for (k, v) in &f {
        check_text(k, "field")?;
        if let Some(s) = v.as_str() {
            check_text_nl(s, k)?;
        }
    }
    let n = match a.flag("pass") {
        Some(v) => {
            let n = parse_pass(v, "bad --pass")?;
            pass_number_ok(n)?;
            tail_is(p.pass(n)?, &["draft"])?;
            n
        }
        None => {
            let n = p.passes.keys().max().unwrap_or(&0) + 1;
            pass_number_ok(n)?;
            n
        }
    };
    let allow = overlap_ok_flag(p, a)?;
    // A pass at draft cannot be overlapped. An open pass (pack, open, return, review)
    // may, when Prime names it with --overlap-ok and a why.
    for x in p.passes.values().filter(|x| x.nn != n && x.tail != "closed") {
        if allow.as_ref().map(|(okn, _)| *okn) == Some(x.nn) {
            continue;
        }
        let redo = if x.tail == "draft" { format!(", or redraft it: wf draft {} --pass {}", p.addr, x.nn) } else { String::new() };
        return Err(format!("refused: 05.{:02} is at '{}' and not closed. Draft the next pass after it closes. Next for 05.{:02}: {}{redo}",
            x.nn, x.tail, x.nn, crate::status::pass_next(p, x)));
    }
    let since = p.last_closed().map(|x| x.last_seq).unwrap_or(0);
    need(p.faces.get("06").map(|x| x.seq > since).unwrap_or(false),
        "refused: before a draft, read 04, 06 and the last closed 05, then write a 06 note (wf face-write <page> 06)")?;
    if !f.contains_key("predecessor") {
        let pre = if n > 1 { format!("05.{:02}", n - 1) } else { "none".into() };
        f.insert("predecessor".into(), pre.into());
    }
    let pins = json!({"04": pin(p, "04"), "06": pin(p, "06"), "05": pin05(p)});
    let mut d = json!({"pass": n, "fields": f, "pins": pins});
    if let Some((okn, why)) = &allow {
        d["overlap_ok"] = json!(okn);
        d["overlap_why"] = json!(why);
    }
    p.add(who, "prime", "draft", d)?;
    println!("drafted 05.{n:02}. Next: wf pack {} {n} --as {who}", p.addr);
    Ok(())
}

fn pin_text(v: &Value) -> String {
    match v {
        Value::Object(m) if m.contains_key("pass") => {
            format!("05.{:02} closed at entry {}", m["pass"].as_u64().unwrap_or(0), m["entry"].as_u64().unwrap_or(0))
        }
        Value::Object(m) => format!("entry {}, hash {}", m["entry"], short(m["hash"].as_str().unwrap_or(""))),
        _ => "none".into(),
    }
}

fn overlap_ok_flag(p: &Page, a: &Args) -> Res<Option<(u32, String)>> {
    match a.flag("overlap-ok") {
        None => Ok(None),
        Some(v) => {
            let why = why_ref(a.req("why")?, "why")?.to_string();
            let n = parse_pass(v, "give --overlap-ok a pass number, like 3 or 05.03")?;
            match p.passes.get(&n) {
                Some(x) if x.is_open_tail() => Ok(Some((n, why))),
                Some(x) => Err(format!("refused: --overlap-ok {} is not open (tail is {})", pass_label(n), x.tail)),
                None => Err(format!("refused: --overlap-ok {} is not open (no such pass)", pass_label(n))),
            }
        }
    }
}

fn refuse_overlap(p: &Page, n: u32, mine: &[String], allow: Option<u32>) -> Res<()> {
    let mut hits = Vec::new();
    for x in p.passes.values() {
        if x.nn == n || !x.is_open_tail() || allow == Some(x.nn) {
            continue;
        }
        let theirs = split_list(x.fields.get("may touch").and_then(|v| v.as_str()).unwrap_or(""));
        let pairs: Vec<String> = mine
            .iter()
            .flat_map(|a| theirs.iter().filter(move |b| paths_overlap(a, b)).map(move |b| format!("{a} and {b}")))
            .collect();
        if !pairs.is_empty() {
            hits.push(format!("05.{:02} ({})", x.nn, pairs.join(", ")));
        }
    }
    need(hits.is_empty(), format!("refused: may touch overlaps open pass {}", hits.join("; ")))
}

pub fn pack(p: &mut Page, root: &Path, a: &Args, who: &str) -> Res<()> {
    must_be(p, who, "prime")?;
    not_halted(p)?;
    let n = nn(a, 1)?;
    let x = p.pass(n)?.clone();
    tail_is(&x, &["draft"])?;
    let f = &x.fields;
    let g = |k: &str| f.get(k).and_then(|v| v.as_str()).unwrap_or("").to_string();
    for k in REQUIRED {
        need(!g(k).is_empty(), format!("refused: pack field '{k}' is empty"))?;
    }
    need(!jobs(f).is_empty(), "refused: the pack has no jobs (w01: ...)")?;
    let mine = split_list(&g("may touch"));
    for path in &mine {
        need(inside(path, &p.grant), format!("refused: may touch '{path}' is outside the grant ({})", p.grant.join(", ")))?;
    }
    let allow = overlap_ok_flag(p, a)?;
    refuse_overlap(p, n, &mine, allow.as_ref().map(|(n, _)| *n))?;
    for (k, now) in [("04", pin(p, "04")), ("06", pin(p, "06")), ("05", pin05(p))] {
        need(x.pins[k] == now, format!("refused: stale pin {k}: drafted against {}, now {}. Write a new 06 note and redraft (wf face-write {} 06, then wf draft {} --pass {n} --file ...)",
            pin_text(&x.pins[k]), pin_text(&now), p.addr, p.addr))?;
    }
    let f01 = p.faces.get("01").ok_or("refused: face 01 (the agents card) is empty")?.clone();
    let start = git::commit(&repo(root, &x), &g("start"))?;
    let name = pass_name(p, n);
    let (branch, rfile) = (format!("pass/{name}"), format!(".workshop/returns/{name}.md"));
    let src01 = format!("v{} entry {} hash {}", f01.version, f01.seq, short(&f01.hash()));
    let (sax, sds) = (render::version_of(AXIOMS), render::version_of(DESIGN));
    let jobs_txt = jobs(f).iter().map(|(k, v)| format!("  {k}: {v}")).collect::<Vec<_>>().join("\n");
    let done_when = done_when_lines(&f01.text);
    if done_when == "none" {
        eprintln!("warning: face 01 has no done-when");
    }
    let text = fill(T_PACK, &[("pass", name.clone()), ("addr", p.addr.clone()), ("title", p.title.clone()), ("prime", p.prime.clone()),
        ("predecessor", g("predecessor")), ("repo", g("repo")), ("start", start.clone()), ("branch", branch.clone()),
        ("return_file", rfile.clone()), ("grant", format!("{} ({})", p.grant.join(", "), p.grant_refs.join(", "))),
        ("axioms", g("axioms")), ("outcome", g("outcome")), ("overview", g("overview")), ("jobs", jobs_txt),
        ("may_touch", g("may touch")), ("checks", g("checks")), ("done_when", done_when.clone()), ("stop_if", g("stop if")),
        ("pin04", pin_text(&x.pins["04"])), ("pin06", pin_text(&x.pins["06"])), ("pin05", pin_text(&x.pins["05"])),
        ("src01", src01.clone()), ("src_axioms", sax.clone()), ("src_design", sds.clone())])?;
    let seq = p.events.len() as u64 + 1;
    let mut d = json!({"pass": n, "pack_text": text, "pack_hash": sha(&text), "branch": branch, "return_file": rfile, "start": start,
        "seq": seq, "time": crate::log::iso(crate::log::now()), "face01": f01.text, "done_when": done_when,
        "templates": render::TEMPLATE_VER,
        "sources": {"01": src01, "axioms": sax, "design": sds}});
    if let Some((okn, why)) = allow {
        d["overlap_ok"] = json!(okn);
        d["overlap_why"] = json!(why);
    }
    p.add(who, "prime", "pack", d)?;
    print!("{}", render::prompt(p, p.pass(n)?)?);
    Ok(())
}

pub fn claim(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    not_halted(p)?;
    let n = nn(a, 1)?;
    let x = p.pass(n)?;
    if let Some(c) = &x.claim {
        return Err(format!("refused: 05.{n:02} is already claimed by {c} (first claim wins)"));
    }
    tail_is(x, &["pack"])?;
    p.add(who, "builder", "claim", json!({"pass": n}))?;
    println!("claimed 05.{n:02}. Read pages/{}/05.{n:02}/PROMPT.md and AGENTS.md", p.addr);
    Ok(())
}

fn ret_change_paths(r: &Value) -> Vec<String> {
    r["changed"]
        .as_array()
        .map(|a| {
            a.iter()
                .filter_map(|v| {
                    if let Some(s) = v.as_str() {
                        Some(s.to_string())
                    } else {
                        let path = s(v, "path");
                        if path.is_empty() { None } else { Some(path) }
                    }
                })
                .collect()
        })
        .unwrap_or_default()
}

/// Check a return file's text. Returns the job lines (w01 -> "done ...").
pub fn parse_return(text: &str, x: &Pass, pack_hash: &str) -> Res<Map<String, Value>> {
    let f = fields(text);
    need(f.get("pack").and_then(|v| v.as_str()) == Some(pack_hash), "the return's 'pack:' line must be this pack's hash")?;
    for k in RETURN_KEYS {
        let v = f.get(k).and_then(|v| v.as_str()).unwrap_or("");
        need(!v.is_empty() && !v.starts_with('<'), format!("the return has no '{k}:' line filled in"))?;
    }
    let mut out = Map::new();
    for (k, _) in jobs(&x.fields) {
        let v = f.get(&k).and_then(|v| v.as_str()).unwrap_or("");
        let st = v.split_whitespace().next().unwrap_or("");
        need(["done", "need", "blocked"].contains(&st), format!("job {k} must start with done, need or blocked"))?;
        out.insert(k, v.into());
    }
    Ok(out)
}

pub fn ret(p: &mut Page, root: &Path, a: &Args, who: &str) -> Res<()> {
    let n = nn(a, 1)?;
    let x = p.pass(n)?.clone();
    tail_is(&x, &["open"])?;
    need(x.claim.as_deref() == Some(who), format!("refused: only the claim holder ({}) may return", x.claim.clone().unwrap_or_default()))?;
    let pk = x.pack.clone().ok_or_else(|| no_part(n, "pack"))?;
    let (branch, file, sha_in) = (a.req("branch")?.to_string(), a.req("file")?.to_string(), a.req("commit")?.to_string());
    let checked = (|| -> Res<(String, String, Vec<git::Change>, Map<String, Value>)> {
        need(branch == s(&pk, "branch"), format!("branch must be {}", s(&pk, "branch")))?;
        need(file == s(&pk, "return_file"), format!("return file must be {}", s(&pk, "return_file")))?;
        let r = repo(root, &x);
        let c = git::commit(&r, &sha_in)?;
        let tip = git::branch_tip(&r, &branch)?;
        need(git::is_ancestor(&r, &c, &tip), format!("commit {} is not on {branch}", short(&c)))?;
        need(git::is_ancestor(&r, &s(&pk, "start"), &c), "the commit does not start from the pack's start commit")?;
        let text = git::show(&r, &c, &file)?;
        let scope = split_list(x.fields["may touch"].as_str().unwrap_or(""));
        let changed = git::changed(&r, &s(&pk, "start"), &c)?;
        let out: Vec<String> = changed.iter().filter(|ch| ch.path != file && !inside(&ch.path, &scope)).map(|ch| ch.tag()).collect();
        need(out.is_empty(), format!("{} outside may touch. Send a new commit without it, or end the job `need` and say why",
            out.join(", ")))?;
        let jobs = parse_return(&text, &x, &s(&pk, "pack_hash"))?;
        Ok((c, text, changed, jobs))
    })();
    match checked {
        Err(why) => {
            p.add("wf", "tool", "return-refused", json!({"pass": n, "by": who, "commit": sha_in, "why": why}))?;
            Err(format!("return refused (recorded): {why}"))
        }
        Ok((c, text, changed, jobs)) => {
            let git_changed: Vec<Value> = changed.iter().map(|ch| json!({"letter": ch.letter.to_string(), "path": ch.path})).collect();
            p.add(who, "builder", "return", json!({"pass": n, "branch": branch, "commit": c, "file": file, "hash": sha(&text),
                "text": text, "changed": git_changed, "jobs": jobs}))?;
            for (k, v) in &jobs {
                let v = v.as_str().unwrap_or("");
                if !v.starts_with("done") {
                    p.add("wf", "tool", "elevate", json!({"pass": n, "to": "prime", "item": format!("{k} {v}")}))?;
                }
            }
            println!("return filed on 05.{n:02}. Next: a checker runs wf check {} {n} --as <checker>", p.addr);
            Ok(())
        }
    }
}

fn refuse_passed(p: &Page, n: u32, ret: &Value, named: &[String], has_note: bool) -> Res<()> {
    let not_done = jobs_not_done(ret);
    let missing: Vec<&String> = not_done.iter().filter(|j| !named.contains(j)).collect();
    need(missing.is_empty(), format!(
        "refused: cannot sign off 'passed' while jobs not done: {}. Name each in --cards and give --note \"<why> (ref)\"",
        missing.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", ")
    ))?;
    let open: Vec<String> = p.elevs.iter()
        .filter(|e| e.pass == n && e.to == "person" && e.answer.is_none())
        .map(|e| e.seq.to_string())
        .collect();
    need(open.is_empty(), format!(
        "refused: cannot sign off 'passed' while elevation {} to person has no answer",
        open.join(", ")
    ))?;
    let drifted = face01_drift(p, p.pass(n)?.pack.as_ref().ok_or("refused: this pass has no pack")?).is_some();
    need(!drifted || has_note, "refused: cannot sign off 'passed' while face 01 has changed since pack; give --note \"<why> (ref)\"")
}

fn check_report(p: &Page, pk: &Value, r: &Value, results: &[(String, (bool, String))], frame_ok: bool, note: Option<&str>, fail: Option<&str>) -> String {
    let mut rep = String::new();
    for (c, (ok, out)) in results {
        rep += &format!("  check {}: {c}\n", if *ok { "ok" } else { "FAIL" });
        if !out.is_empty() {
            for line in out.lines() {
                rep += &format!("    {line}\n");
            }
        }
    }
    rep += &format!("  frame {}: changed {}\n", if frame_ok { "ok" } else { "FAIL" }, render::git_changed_text(r));
    for (k, v) in r["jobs"].as_object().cloned().unwrap_or_default() {
        rep += &format!("  job {k}: {}\n", chars::escape_line(v.as_str().unwrap_or("")));
    }
    let not_done = jobs_not_done(r);
    if !not_done.is_empty() {
        rep += &format!("  jobs not done: {}\n", not_done.join(", "));
    }
    let dw = s(pk, "done_when");
    if dw != "none" && !dw.is_empty() {
        for l in dw.lines() {
            rep += &format!("  done when (01): {} -> {}\n", l, if results.iter().all(|r| r.1 .0) { "checks ok; the checker judges the rest" } else { "not met" });
        }
    }
    if let Some(now) = face01_drift(p, pk) {
        rep += &format!("  drift: face 01 changed since pack (now {now})\n");
    }
    if let Some(note) = note {
        rep += &format!("  checker note: {}\n", chars::escape_line(note));
    }
    if let Some(f) = fail {
        rep += &format!("  checker fail: {}\n", chars::escape_line(f));
    }
    rep
}

pub fn check(p: &mut Page, root: &Path, a: &Args, who: &str) -> Res<()> {
    let n = nn(a, 1)?;
    if let Some(note) = a.flag("note") {
        check_text(note, "note")?;
    }
    if let Some(fail) = a.flag("fail") {
        check_text(fail, "fail")?;
    }
    let x = p.pass(n)?.clone();
    tail_is(&x, &["return", "review"])?;
    need(x.claim.as_deref() != Some(who), "refused: the builder may not check its own work")?;
    let dry = a.flag("dry-run").is_some();
    if let (false, Some((who, at, d))) = (dry, &x.signoff) {
        return Err(format!("refused: 05.{n:02} was signed off by {who} at entry {at} (outcome {}), so it cannot be checked again; nothing was written. Next: wf close {} {n}",
            s(d, "outcome"), p.addr));
    }
    if !dry {
        if let Some((_, c)) = &x.check {
            need(s(c, "verdict") == "fail", "refused: this pass already passed its check")?;
        }
    }
    let pk = x.pack.clone().ok_or_else(|| no_part(n, "pack"))?;
    let r = x.ret.clone().ok_or_else(|| no_part(n, "return"))?;
    let pack_hash = s(&pk, "pack_hash");
    let return_hash = s(&r, "hash");
    let tail0 = x.tail.clone();
    let check0 = x.check.clone();
    let commit = s(&r, "commit");
    let cmds: Vec<String> = x.fields["checks"].as_str().unwrap_or("").split(';').map(|c| c.trim().to_string()).filter(|c| !c.is_empty()).collect();
    let results = git::in_worktree(&repo(root, &x), &commit, |dir| cmds.iter().map(|c| (c.clone(), git::run(dir, c))).collect::<Vec<_>>())?;
    let scope = split_list(x.fields["may touch"].as_str().unwrap_or(""));
    let frame_ok = ret_change_paths(&r).iter().all(|f| *f == s(&r, "file") || inside(f, &scope));
    let pass = results.iter().all(|r| r.1 .0) && frame_ok && a.flag("fail").is_none();
    let verdict = if pass { "pass" } else { "fail" };
    if dry {
        let rep = check_report(p, &pk, &r, &results, frame_ok, a.flag("note"), a.flag("fail"));
        print!("check 05.{n:02}: {verdict} (dry-run: nothing written)\n{rep}");
        return Ok(());
    }
    let _l = crate::Lock::take(&p.dir)?;
    *p = Page::load(&p.dir)?;
    let edited = render::edited(p)?;
    need(edited.is_empty(), format!("refused: {}. Nobody writes page files directly. Run wf verify {} --fix to reprint missing and changed views from the log.", edited.report(), p.addr))?;
    let x2 = p.pass(n)?.clone();
    let still = x2.tail == tail0
        && x2.signoff.is_none()
        && s(x2.pack.as_ref().unwrap_or(&Value::Null), "pack_hash") == pack_hash
        && s(x2.ret.as_ref().unwrap_or(&Value::Null), "hash") == return_hash
        && x2.check == check0;
    if let Some((who, at, d)) = &x2.signoff {
        return Err(format!("refused: 05.{n:02} was signed off by {who} at entry {at} (outcome {}), so it cannot be checked again; nothing was written. Next: wf close {} {n}",
            s(d, "outcome"), p.addr));
    }
    need(still, format!("refused: 05.{n:02} changed while the checks ran (it is now at '{}', last entry {}); nothing was written. Run wf check {} {n} again",
        x2.tail, x2.last_seq, p.addr))?;
    if let Some((_, c)) = &x2.check {
        need(s(c, "verdict") == "fail", "refused: this pass already passed its check")?;
    }
    need(x2.claim.as_deref() != Some(who), "refused: the builder may not check its own work")?;
    let pk = x2.pack.as_ref().ok_or_else(|| no_part(n, "pack"))?;
    let r = x2.ret.as_ref().ok_or_else(|| no_part(n, "return"))?;
    let rep = check_report(p, pk, r, &results, frame_ok, a.flag("note"), a.flag("fail"));
    p.add(who, "checker", "check", json!({"pass": n, "commit": commit, "verdict": verdict, "report": rep,
        "results": results.iter().map(|(c, (ok, out))| json!({"cmd": c, "ok": ok, "out": git::clip_check_out(out, 40)})).collect::<Vec<_>>()}))?;
    let fails = p.events.iter().filter(|e| e.kind == "check" && e.data["pass"] == n && s(&e.data, "verdict") == "fail").count();
    if fails >= 2 {
        p.add("wf", "tool", "elevate", json!({"pass": n, "to": "prime", "item": format!("second failed check on 05.{n:02}")}))?;
    }
    print!("check 05.{n:02}: {verdict}\n{rep}");
    render::write_after_append(p)
}

pub fn signoff(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    must_be(p, who, "prime")?;
    let n = nn(a, 1)?;
    let x = p.pass(n)?.clone();
    tail_is(&x, &["review"])?;
    let outcome = a.req("outcome")?;
    need(OUTCOMES.contains(&outcome), format!("outcome must be one of {}", OUTCOMES.join(", ")))?;
    let verdict = x.check.as_ref().map(|c| s(&c.1, "verdict")).unwrap_or_default();
    need(outcome != "passed" || verdict == "pass", "refused: cannot sign off 'passed' when the check failed")?;
    let ret = x.ret.as_ref().ok_or_else(|| no_part(n, "return"))?;
    let not_done = jobs_not_done(ret);
    let named: Vec<String> = split_list(a.flag("cards").unwrap_or(""))
        .iter()
        .map(|kv| kv.split_once('=').map(|(k, _)| k.trim().to_string()).unwrap_or_default())
        .filter(|k| !k.is_empty())
        .collect();
    let drifted = face01_drift(p, x.pack.as_ref().ok_or_else(|| no_part(n, "pack"))?).is_some();
    if outcome == "passed" {
        refuse_passed(p, n, ret, &named, a.flag("note").is_some())?;
    }
    let mut cards = Map::new();
    for (k, v) in ret["jobs"].as_object().cloned().unwrap_or_default() {
        let done = v.as_str().unwrap_or("").starts_with("done");
        let w = match outcome { "passed" => "accepted", "failed" => "discarded", _ if done => "accepted", _ => "carried" };
        cards.insert(k, w.into());
    }
    let defaults = cards.clone();
    for kv in split_list(a.flag("cards").unwrap_or("")) {
        let (k, v) = kv.split_once('=').ok_or("cards look like w01=accepted,w02=carried")?;
        need(cards.contains_key(k.trim()) && CARD_WORDS.contains(&v.trim()), format!("bad card '{kv}' (words: {})", CARD_WORDS.join(", ")))?;
        cards.insert(k.trim().into(), v.trim().into());
    }
    let changed_default = cards.iter().any(|(k, v)| defaults.get(k) != Some(v));
    let need_note = (outcome == "passed" && (!not_done.is_empty() || drifted)) || changed_default;
    let note = if need_note {
        why_ref(a.flag("note").unwrap_or(""), "note")?
    } else {
        let n = a.flag("note").unwrap_or("none");
        check_text(n, "note")?;
        n
    };
    p.add(who, "prime", "signoff", json!({"pass": n, "outcome": outcome, "cards": cards, "note": note}))?;
    println!("signed off 05.{n:02} {outcome}. Next: wf close {} {n}", p.addr);
    Ok(())
}

pub fn close(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let n = nn(a, 1)?;
    let x = p.pass(n)?.clone();
    tail_is(&x, &["review"])?;
    let (signer, seq, d) = x.signoff.clone().ok_or("refused: Prime has not signed off this pass")?;
    need(p.prime_at(seq) == signer, format!("refused: {signer} was not prime at entry {seq}"))?;
    let (pk, r, (checker, c)) = (x.pack.clone().ok_or_else(|| no_part(n, "pack"))?, x.ret.clone().ok_or_else(|| no_part(n, "return"))?, x.check.clone().ok_or_else(|| no_part(n, "check"))?);
    if s(&d, "outcome") == "passed" {
        let named: Vec<String> = d["cards"].as_object().map(|m| m.keys().cloned().collect()).unwrap_or_default();
        refuse_passed(p, n, &r, &named, why_ref(&s(&d, "note"), "note").is_ok())?;
        let f01 = p.faces.get("01").map(|f| f.seq).unwrap_or(0);
        need(f01 <= seq, "refused: cannot close 'passed' while face 01 changed after the signoff entry")?;
    }
    let sum = c["results"].as_array().map(|v| v.iter().map(|r| format!("{} {}", s(r, "cmd"), if r["ok"] == true { "ok" } else { "FAIL" })).collect::<Vec<_>>().join("; ")).unwrap_or_default();
    let mut record = fill(T_CLOSE, &[("pass", pass_name(p, n)), ("pack_hash", s(&pk, "pack_hash")), ("return_hash", s(&r, "hash")),
        ("commit", s(&r, "commit")), ("branch", s(&r, "branch")), ("checker", checker), ("check_summary", format!("{} ({sum})", s(&c, "verdict"))),
        ("signer", signer), ("sign_seq", seq.to_string()), ("outcome", s(&d, "outcome")), ("cards", render::cards_text(&d["cards"])), ("note", s(&d, "note"))])?;
    let git = render::git_changed_text(&r);
    if !git.is_empty() {
        if !record.ends_with('\n') {
            record.push('\n');
        }
        record.push_str(&format!("git: {git}\n"));
    }
    p.add(who, "tool", "close", json!({"pass": n, "outcome": s(&d, "outcome"), "cards": d["cards"], "record": record, "record_hash": sha(&record)}))?;
    print!("{record}");
    Ok(())
}

pub fn elevate(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let n = nn(a, 1)?;
    p.pass(n)?;
    let to = a.req("to")?;
    need(to == "prime" || (to == "person" && who == p.prime), "refused: --to prime (anyone), or --to person (only Prime sends it up)")?;
    let item = a.req("item")?;
    no_ctrl(item, "item")?;
    p.add(who, if who == p.prime { "prime" } else { "builder" }, "elevate", json!({"pass": n, "to": to, "item": item}))
}

pub fn answer(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let seq: u64 = a.pos.get(1).and_then(|x| x.parse().ok()).ok_or("give the elevation's entry number")?;
    let e = p.elevs.iter().find(|e| e.seq == seq).ok_or(format!("no elevation at entry {seq}"))?.clone();
    must_be(p, who, &e.to)?;
    p.add(who, &e.to, "answer", json!({"elevation": seq, "text": nonblank(a.req("text")?, "text")?}))
}

#[cfg(test)]
mod tests {
    /// A pass state the log order rules now keep out of any loaded page; the commands still refuse it, not panic.
    #[test]
    fn write_commands_refuse_missing_parts_without_a_panic() {
        use crate::page::{Page, Pass};
        let dir = std::env::temp_dir().join(format!("wf-cmd-noparts-{}", std::process::id()));
        let _ = std::fs::remove_dir_all(&dir);
        std::fs::create_dir_all(&dir).unwrap();
        let mut p = Page { dir: dir.clone(), addr: "1.2.3.4".into(), prime: "pri".into(), person: "mat".into(), ..Default::default() };
        p.primes.push(("pri".into(), 1, 1));
        let a = |v: &[&str]| crate::Args::parse(&v.iter().map(|s| s.to_string()).collect::<Vec<_>>());
        p.passes.insert(1, Pass { nn: 1, tail: "open".into(), claim: Some("bob".into()), ..Default::default() });
        let err = super::ret(&mut p, &dir, &a(&["1.2.3.4", "1", "--branch", "b", "--commit", "c", "--file", "f"]), "bob").unwrap_err();
        assert!(err.contains("05.01 has no pack in the log"), "{err}");
        p.passes.insert(1, Pass { nn: 1, tail: "return".into(), ..Default::default() });
        let err = super::check(&mut p, &dir, &a(&["1.2.3.4", "1"]), "cat").unwrap_err();
        assert!(err.contains("05.01 has no pack in the log"), "{err}");
        p.passes.insert(1, Pass { nn: 1, tail: "review".into(), ..Default::default() });
        let err = super::signoff(&mut p, &a(&["1.2.3.4", "1", "--outcome", "failed"]), "pri").unwrap_err();
        assert!(err.contains("05.01 has no return in the log"), "{err}");
        p.passes.insert(1, Pass { nn: 1, tail: "review".into(), signoff: Some(("pri".into(), 1, serde_json::json!({"outcome": "failed"}))), ..Default::default() });
        let err = super::close(&mut p, &a(&["1.2.3.4", "1"]), "pri").unwrap_err();
        assert!(err.contains("05.01 has no pack in the log"), "{err}");
        assert!(!dir.join("log.jsonl").exists(), "nothing was written");
        let _ = std::fs::remove_dir_all(&dir);
    }

    #[test]
    fn fields_join_indented_lines() {
        let f = super::fields("w01: one\n  two\nChecks: a; b\n");
        assert_eq!(f["w01"], "one\ntwo");
        assert_eq!(f["checks"], "a; b");
    }

    #[test]
    fn pin_text_pads_pass_number() {
        let v = serde_json::json!({"pass": 1, "entry": 11});
        assert_eq!(super::pin_text(&v), "05.01 closed at entry 11");
    }

    #[test]
    fn why_ref_needs_a_reason_and_parenthetical() {
        assert_eq!(super::why_ref("shared files (t275u)", "why").unwrap(), "shared files (t275u)");
        assert!(super::why_ref("", "why").unwrap_err().contains("--why needs a reason and a (ref)"));
        assert!(super::why_ref("(t275u)", "note").unwrap_err().contains("--note needs a reason"));
        assert!(super::why_ref("shared files", "why").unwrap_err().contains("--why needs a reason and a (ref)"));
        assert!(super::why_ref("shared files ()", "why").is_err());
        assert!(super::why_ref("ok ( )", "why").is_err());
        assert!(super::why_ref("ok (\t)", "note").is_err());
        assert_eq!(super::nonblank(" t275u ", "ref").unwrap(), "t275u");
        assert!(super::nonblank(" ", "ref").unwrap_err().contains("--ref must have non-blank text"));
        assert!(super::nonblank("\t", "text").unwrap_err().contains("--text must have non-blank text"));
    }

    #[test]
    fn check_text_refuses_each_class_and_keeps_newlines_only_when_asked() {
        use crate::chars::{check_text, check_text_nl};
        assert!(check_text("ok name", "as").is_ok());
        assert!(check_text("wait for Matthew (t301u)", "note").is_ok());
        for (name, ch) in [
            ("C0 ESC", '\u{001B}'),
            ("C0 tab", '\t'),
            ("C0 newline", '\n'),
            ("C0 CR", '\r'),
            ("DEL", '\u{007F}'),
            ("C1 NEL", '\u{0085}'),
            ("U+2028", '\u{2028}'),
            ("U+2029", '\u{2029}'),
            ("bidi RLO", '\u{202E}'),
            ("bidi FSI", '\u{2066}'),
            ("LTR mark", '\u{200E}'),
            ("RTL mark", '\u{200F}'),
            ("ALM", '\u{061C}'),
            ("soft hyphen", '\u{00AD}'),
            ("function application", '\u{2061}'),
            ("language tag", '\u{E0001}'),
            ("Hangul filler", '\u{3164}'),
            ("zero-width space", '\u{200B}'),
            ("word joiner", '\u{2060}'),
            ("BOM", '\u{FEFF}'),
        ] {
            let s = format!("x{ch}y");
            let err = check_text(&s, "as").unwrap_err();
            assert!(err.contains("--as cannot contain control characters"), "{name}: {err}");
            if ch == '\n' {
                assert!(check_text_nl(&s, "file").is_ok(), "{name}");
            } else {
                assert!(check_text_nl(&s, "file").is_err(), "{name} should fail multiline");
            }
        }
        assert!(check_text_nl("Goal: a.\nDone when: checks pass.", "file").is_ok());
        assert!(check_text("Goal: a.\nDone when: checks pass.", "text").is_err());
        assert!(check_text("\u{0301}\u{0301}", "as").unwrap_err().contains("only combining marks"));
    }

    #[test]
    fn pass_number_ok_allows_01_to_98_and_refuses_0_and_99() {
        assert!(super::pass_number_ok(1).is_ok());
        assert!(super::pass_number_ok(98).is_ok());
        assert_eq!(super::pass_number_ok(0).unwrap_err(), "refused: pass 0 is not allowed (R9)");
        assert_eq!(
            super::pass_number_ok(99).unwrap_err(),
            "counter 98 reached: after 98 is open (QD16); ask Prime"
        );
        assert_eq!(
            super::pass_number_ok(100).unwrap_err(),
            "counter 98 reached: after 98 is open (QD16); ask Prime"
        );
    }
}
