//! The commands that write. Each one checks the role, then appends to the log.

use crate::git;
use crate::log::{sha, short, Res};
use crate::page::{check_addr, done_when_lines, face01_drift, inside, list, paths_overlap, s, split_list, Page, Pass};
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

/// A required why: a reason plus a parenthetical ref, e.g. "shared files (t275u)".
fn why_ref<'a>(text: &'a str, flag: &str) -> Res<&'a str> {
    let t = text.trim();
    let ok = match (t.find('('), t.rfind(')')) {
        (Some(i), Some(j)) if j > i + 1 => !t[..i].trim().is_empty(),
        _ => false,
    };
    need(ok, format!("--{flag} needs a reason and a (ref), like \"why (t275u)\""))?;
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

fn tail_is(x: &Pass, want: &[&str]) -> Res<()> {
    need(want.contains(&x.tail.as_str()), format!("refused: 05.{:02} is at '{}', this needs {}", x.nn, x.tail, want.join(" or ")))
}

fn nn(a: &Args, i: usize) -> Res<u32> {
    a.pos.get(i).and_then(|x| x.trim_start_matches("05.").parse().ok()).ok_or("give the pass number, like 3 or 05.03".into())
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
    need(who == person, "refused: the person starts their own page (--as must match --person)")?;
    let title = a.req("title")?;
    let prime = a.req("prime")?;
    let grant = split_list(a.req("grant")?);
    let grant_ref = a.req("grant-ref")?;
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
    p.add(who, "person", "prime", json!({"name": name, "ref": a.req("ref")?}))
}

pub fn grant(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    must_be(p, who, "person")?;
    let ans = a.flag("answers").and_then(|x| x.parse::<u64>().ok());
    p.add(who, "person", "grant", json!({"paths": split_list(a.req("paths")?), "ref": a.req("ref")?}))?;
    if let Some(seq) = ans {
        p.add(who, "person", "answer", json!({"elevation": seq, "text": format!("grant {} widened", a.req("ref")?)}))?;
    }
    Ok(())
}

pub fn face_write(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let face = a.pos.get(1).map(|x| x.as_str()).unwrap_or("");
    let text = text_arg(a)?;
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
    let mut f = fields(&text_arg(a)?);
    let since = p.last_closed().map(|x| x.last_seq).unwrap_or(0);
    need(p.faces.get("06").map(|x| x.seq > since).unwrap_or(false),
        "refused: before a draft, read 04, 06 and the last closed 05, then write a 06 note (wf face-write <page> 06)")?;
    let n = match a.flag("pass") {
        Some(v) => {
            let n: u32 = v.trim_start_matches("05.").parse().map_err(|_| "bad --pass".to_string())?;
            tail_is(p.pass(n)?, &["draft"])?;
            n
        }
        None => p.passes.keys().max().unwrap_or(&0) + 1,
    };
    if !f.contains_key("predecessor") {
        let pre = if n > 1 { format!("05.{:02}", n - 1) } else { "none".into() };
        f.insert("predecessor".into(), pre.into());
    }
    let pins = json!({"04": pin(p, "04"), "06": pin(p, "06"), "05": pin05(p)});
    p.add(who, "prime", "draft", json!({"pass": n, "fields": f, "pins": pins}))?;
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
            let n: u32 = v.trim_start_matches("05.").parse()
                .map_err(|_| "give --overlap-ok a pass number, like 3 or 05.03".to_string())?;
            match p.passes.get(&n) {
                Some(x) if x.is_open_tail() => Ok(Some((n, why))),
                Some(x) => Err(format!("refused: --overlap-ok 05.{n:02} is not open (tail is {})", x.tail)),
                None => Err(format!("refused: --overlap-ok 05.{n:02} is not open (no such pass)")),
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
    let pk = x.pack.clone().unwrap();
    let (branch, file, sha_in) = (a.req("branch")?.to_string(), a.req("file")?.to_string(), a.req("commit")?.to_string());
    let checked = (|| -> Res<(String, String, Vec<String>, Map<String, Value>)> {
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
        let out: Vec<&String> = changed.iter().filter(|f| **f != file && !inside(f, &scope)).collect();
        need(out.is_empty(), format!("{} outside may touch. Send a new commit without it, or end the job `need` and say why",
            out.iter().map(|s| s.as_str()).collect::<Vec<_>>().join(", ")))?;
        let jobs = parse_return(&text, &x, &s(&pk, "pack_hash"))?;
        Ok((c, text, changed, jobs))
    })();
    match checked {
        Err(why) => {
            p.add("wf", "tool", "return-refused", json!({"pass": n, "by": who, "commit": sha_in, "why": why}))?;
            Err(format!("return refused (recorded): {why}"))
        }
        Ok((c, text, changed, jobs)) => {
            p.add(who, "builder", "return", json!({"pass": n, "branch": branch, "commit": c, "file": file, "hash": sha(&text),
                "text": text, "changed": changed, "jobs": jobs}))?;
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

pub fn check(p: &mut Page, root: &Path, a: &Args, who: &str) -> Res<()> {
    let n = nn(a, 1)?;
    let x = p.pass(n)?.clone();
    tail_is(&x, &["return", "review"])?;
    need(x.claim.as_deref() != Some(who), "refused: the builder may not check its own work")?;
    let dry = a.flag("dry-run").is_some();
    if !dry {
        if let Some((_, c)) = &x.check {
            need(s(c, "verdict") == "fail", "refused: this pass already passed its check")?;
        }
    }
    let pk = x.pack.clone().unwrap();
    let r = x.ret.clone().unwrap();
    let pack_hash = s(&pk, "pack_hash");
    let return_hash = s(&r, "hash");
    let tail0 = x.tail.clone();
    let check0 = x.check.clone();
    let commit = s(&r, "commit");
    let cmds: Vec<String> = x.fields["checks"].as_str().unwrap_or("").split(';').map(|c| c.trim().to_string()).filter(|c| !c.is_empty()).collect();
    let results = git::in_worktree(&repo(root, &x), &commit, |dir| cmds.iter().map(|c| (c.clone(), git::run(dir, c))).collect::<Vec<_>>())?;
    let scope = split_list(x.fields["may touch"].as_str().unwrap_or(""));
    let frame_ok = list(&r["changed"]).iter().all(|f| *f == s(&r, "file") || inside(f, &scope));
    let mut rep = String::new();
    for (c, (ok, out)) in &results {
        rep += &format!("  check {}: {c}\n", if *ok { "ok" } else { "FAIL" });
        if !out.is_empty() {
            for line in out.lines() {
                rep += &format!("    {line}\n");
            }
        }
    }
    rep += &format!("  frame {}: changed {}\n", if frame_ok { "ok" } else { "FAIL" }, list(&r["changed"]).join(", "));
    for (k, v) in r["jobs"].as_object().cloned().unwrap_or_default() {
        rep += &format!("  job {k}: {}\n", v.as_str().unwrap_or(""));
    }
    let not_done = jobs_not_done(&r);
    if !not_done.is_empty() {
        rep += &format!("  jobs not done: {}\n", not_done.join(", "));
    }
    let dw = s(&pk, "done_when");
    if dw != "none" && !dw.is_empty() {
        for l in dw.lines() {
            rep += &format!("  done when (01): {} -> {}\n", l, if results.iter().all(|r| r.1 .0) { "checks ok; the checker judges the rest" } else { "not met" });
        }
    }
    if let Some(now) = face01_drift(p, &pk) {
        rep += &format!("  drift: face 01 changed since pack (now {now})\n");
    }
    if let Some(note) = a.flag("note") {
        rep += &format!("  checker note: {note}\n");
    }
    let pass = results.iter().all(|r| r.1 .0) && frame_ok && a.flag("fail").is_none();
    if let Some(f) = a.flag("fail") {
        rep += &format!("  checker fail: {f}\n");
    }
    let verdict = if pass { "pass" } else { "fail" };
    if dry {
        print!("check 05.{n:02}: {verdict} (dry-run: nothing written)\n{rep}");
        return Ok(());
    }
    let _l = crate::Lock::take(&p.dir)?;
    *p = Page::load(&p.dir)?;
    let edited = render::edited(p)?;
    need(edited.is_empty(), format!("refused: hand-edited page files: {}. Nobody writes page files directly. Run wf verify {} --fix to reprint them from the log.", edited.join(", "), p.addr))?;
    let x2 = p.pass(n)?.clone();
    let still = x2.tail == tail0
        && x2.signoff.is_none()
        && s(x2.pack.as_ref().unwrap_or(&Value::Null), "pack_hash") == pack_hash
        && s(x2.ret.as_ref().unwrap_or(&Value::Null), "hash") == return_hash
        && x2.check == check0;
    need(still, format!("refused: 05.{n:02} is no longer in return with the same pack and return"))?;
    if let Some((_, c)) = &x2.check {
        need(s(c, "verdict") == "fail", "refused: this pass already passed its check")?;
    }
    need(x2.claim.as_deref() != Some(who), "refused: the builder may not check its own work")?;
    p.add(who, "checker", "check", json!({"pass": n, "commit": commit, "verdict": verdict, "report": rep,
        "results": results.iter().map(|(c, (ok, out))| json!({"cmd": c, "ok": ok, "out": git::clip_check_out(out, 40)})).collect::<Vec<_>>()}))?;
    let fails = p.events.iter().filter(|e| e.kind == "check" && e.data["pass"] == n && s(&e.data, "verdict") == "fail").count();
    if fails >= 2 {
        p.add("wf", "tool", "elevate", json!({"pass": n, "to": "prime", "item": format!("second failed check on 05.{n:02}")}))?;
    }
    print!("check 05.{n:02}: {verdict}\n{rep}");
    render::write(p)
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
    let ret = x.ret.as_ref().unwrap();
    let not_done = jobs_not_done(ret);
    let named: Vec<String> = split_list(a.flag("cards").unwrap_or(""))
        .iter()
        .map(|kv| kv.split_once('=').map(|(k, _)| k.trim().to_string()).unwrap_or_default())
        .filter(|k| !k.is_empty())
        .collect();
    let drifted = face01_drift(p, x.pack.as_ref().unwrap()).is_some();
    if outcome == "passed" {
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
        if drifted && a.flag("note").is_none() {
            return Err("refused: cannot sign off 'passed' while face 01 has changed since pack; give --note \"<why> (ref)\"".into());
        }
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
        a.flag("note").unwrap_or("none")
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
    let (pk, r, (checker, c)) = (x.pack.clone().unwrap(), x.ret.clone().unwrap(), x.check.clone().unwrap());
    let sum = c["results"].as_array().map(|v| v.iter().map(|r| format!("{} {}", s(r, "cmd"), if r["ok"] == true { "ok" } else { "FAIL" })).collect::<Vec<_>>().join("; ")).unwrap_or_default();
    let record = fill(T_CLOSE, &[("pass", pass_name(p, n)), ("pack_hash", s(&pk, "pack_hash")), ("return_hash", s(&r, "hash")),
        ("commit", s(&r, "commit")), ("branch", s(&r, "branch")), ("checker", checker), ("check_summary", format!("{} ({sum})", s(&c, "verdict"))),
        ("signer", signer), ("sign_seq", seq.to_string()), ("outcome", s(&d, "outcome")), ("cards", render::cards_text(&d["cards"])), ("note", s(&d, "note"))])?;
    p.add(who, "tool", "close", json!({"pass": n, "outcome": s(&d, "outcome"), "cards": d["cards"], "record": record, "record_hash": sha(&record)}))?;
    print!("{record}");
    Ok(())
}

pub fn elevate(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let n = nn(a, 1)?;
    p.pass(n)?;
    let to = a.req("to")?;
    need(to == "prime" || (to == "person" && who == p.prime), "refused: --to prime (anyone), or --to person (only Prime sends it up)")?;
    p.add(who, if who == p.prime { "prime" } else { "builder" }, "elevate", json!({"pass": n, "to": to, "item": a.req("item")?}))
}

pub fn answer(p: &mut Page, a: &Args, who: &str) -> Res<()> {
    let seq: u64 = a.pos.get(1).and_then(|x| x.parse().ok()).ok_or("give the elevation's entry number")?;
    let e = p.elevs.iter().find(|e| e.seq == seq).ok_or(format!("no elevation at entry {seq}"))?.clone();
    must_be(p, who, &e.to)?;
    p.add(who, &e.to, "answer", json!({"elevation": seq, "text": a.req("text")?}))
}

#[cfg(test)]
mod tests {
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
    }
}
