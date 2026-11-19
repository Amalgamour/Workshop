//! Views. Every file in a page folder except log.jsonl is printed here from the log.
//! Templates are fixed text built into the binary; only the tool fills them.

use crate::chars::{escape_line, escape_text};
use crate::log::{sha, short, Res};
use crate::page::{s, Page, Pass, FACES};
use serde_json::Value;
use std::collections::BTreeMap;
use std::fs;
use std::io::Write;
use std::path::Path;

pub const T_PACK: &str = include_str!("../templates/pack.txt");
pub const T_PROMPT: &str = include_str!("../templates/prompt.txt");
pub const T_AGENTS: &str = include_str!("../templates/agents.txt");
pub const T_RETURN: &str = include_str!("../templates/return.txt");
pub const T_CLOSE: &str = include_str!("../templates/close.txt");
/// v1: the 8eb1fdb text, used when a pack entry has no template version.
pub const T_PROMPT_V1: &str = include_str!("../templates/v1/prompt.txt");
pub const T_AGENTS_V1: &str = include_str!("../templates/v1/agents.txt");
pub const T_RETURN_V1: &str = include_str!("../templates/v1/return.txt");
/// Version written into new pack entries. Missing or "1" means v1 (8eb1fdb).
pub const TEMPLATE_VER: &str = "2";
pub const AXIOMS: &str = include_str!("../docs/AXIOMS.md");
pub const DESIGN: &str = include_str!("../docs/DESIGN.md");

/// Agents, prompt and return templates for one pack.
/// Only a missing field or the string "1" mean v1; only the string "2" means v2.
/// Any other value is refused, and the message names the page and the pack entry.
pub fn packed_templates(pk: &Value, addr: &str) -> Res<(&'static str, &'static str, &'static str)> {
    let seq = pk.get("seq").and_then(|v| v.as_u64());
    let loc = match seq {
        Some(n) => format!(" (page {addr}, entry {n})"),
        None => format!(" (page {addr})"),
    };
    match pk.as_object().and_then(|m| m.get("templates")) {
        None => Ok((T_AGENTS_V1, T_PROMPT_V1, T_RETURN_V1)),
        Some(Value::String(s)) if s == "1" => Ok((T_AGENTS_V1, T_PROMPT_V1, T_RETURN_V1)),
        Some(Value::String(s)) if s == "2" => Ok((T_AGENTS, T_PROMPT, T_RETURN)),
        Some(v) => Err(format!("unknown template version {v}{loc}")),
    }
}

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
        ("done_when", s(&pk, "done_when")),
        ("axioms", g("axioms")),
        ("src01", s(&pk["sources"], "01")),
        ("src_axioms", s(&pk["sources"], "axioms")),
        ("src_design", s(&pk["sources"], "design")),
        ("face01", s(&pk, "face01")),
    ]
}

pub fn prompt(p: &Page, x: &Pass) -> Res<String> {
    let pk = x.pack.as_ref().cloned().unwrap_or(Value::Null);
    let (_, tmpl, _) = packed_templates(&pk, &p.addr)?;
    fill(tmpl, &pass_vals(p, x))
}

pub fn agents(p: &Page, x: &Pass) -> Res<String> {
    let pk = x.pack.as_ref().cloned().unwrap_or(Value::Null);
    let (tmpl, _, _) = packed_templates(&pk, &p.addr)?;
    fill(tmpl, &pass_vals(p, x))
}

pub fn return_template(p: &Page, x: &Pass) -> Res<String> {
    let pk = x.pack.as_ref().cloned().unwrap_or(Value::Null);
    let (_, _, tmpl) = packed_templates(&pk, &p.addr)?;
    let mut v = pass_vals(p, x);
    let lines = jobs(&x.fields).iter().map(|(k, j)| format!("{k}: <done | need | blocked> - {j}")).collect::<Vec<_>>().join("\n");
    v.push(("job_lines", lines));
    fill(tmpl, &v)
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
            o += &format!("return refused (entry {seq}): {}\n", escape_line(&why));
        }
        if let Some(r) = &x.ret {
            o += &format!("return: {} at {} (hash {})\n", s(r, "file"), s(r, "commit"), short(&s(r, "hash")));
            let git = git_changed_text(r);
            if !git.is_empty() {
                o += &format!("git: {git}\n");
            }
            o += &format!("```\n{}\n```\n", escape_text(s(r, "text").trim_end()));
        }
        if let Some((who, c)) = &x.check {
            o += &format!("check by {who}: verdict {}\n{}", s(c, "verdict"), escape_text(&s(c, "report")));
        }
        if let Some((who, seq, d)) = &x.signoff {
            o += &format!("signed off: {who} at entry {seq}, outcome {}\n", s(d, "outcome"));
        }
        if let Some(c) = &x.close {
            o += &format!("```\n{}```\n", escape_text(&s(c, "record")));
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

/// Pass views whose released text is pinned by a sha256 in the pack entry (Director t373u).
pub const HASHED: [(&str, &str); 2] = [("AGENTS.md", "agents_hash"), ("PROMPT.md", "prompt_hash")];

/// The hash a pack entry recorded for one released file. None: the entry has no such
/// field (packed before t373u). A field that is not a string can match no text.
pub fn recorded_hash(pk: &Value, key: &str) -> Option<String> {
    pk.as_object().and_then(|m| m.get(key)).map(|v| v.as_str().unwrap_or("").to_string())
}

/// The first 12 characters of a recorded hash, escaped (a forged field may hold anything).
pub fn hash12(h: &str) -> String {
    escape_line(&h.chars().take(12).collect::<String>())
}

fn hash_invalid(file: &str, nn: u32, detail: String) -> String {
    format!("{file} for pass 05.{nn:02} is invalid: hash mismatch ({detail})")
}

/// Released files this wf would print differently from the hash recorded at pack
/// (a template changed after release). Built from the log only. Every view reprint is
/// refused while one is listed: wf never rewrites what a worker was given.
pub fn hash_faults(p: &Page) -> Res<Vec<String>> {
    let mut out = Vec::new();
    for x in p.passes.values() {
        let Some(pk) = &x.pack else { continue };
        for (file, key) in HASHED {
            let Some(want) = recorded_hash(pk, key) else { continue };
            let text = if file == "AGENTS.md" { agents(p, x)? } else { prompt(p, x)? };
            let got = sha(&text);
            if got != want {
                out.push(hash_invalid(file, x.nn, format!(
                    "pack entry {} recorded {}, this wf would print {}; the released text is not reprinted",
                    pk["seq"], hash12(&want), short(&got)
                )));
            }
        }
    }
    Ok(out)
}

/// One line per packed pass for verify: does the log pin its released files?
pub fn hash_notes(p: &Page) -> Vec<String> {
    let mut out = Vec::new();
    for x in p.passes.values() {
        let Some(pk) = &x.pack else { continue };
        let parts: Vec<String> = HASHED
            .iter()
            .map(|(file, key)| match recorded_hash(pk, key) {
                Some(h) => format!("{file} hash {} holds", hash12(&h)),
                None => format!("{file} no hash recorded (before t373u)"),
            })
            .collect();
        out.push(format!("05.{:02}: {}", x.nn, parts.join("; ")));
    }
    out
}

/// Views on disk that do not match the log, split by kind.
#[derive(Default, Debug, PartialEq, Eq)]
pub struct ViewDiff {
    pub missing: Vec<String>,
    pub unreadable: Vec<String>,
    pub changed: Vec<String>,
    /// Released files (AGENTS.md, PROMPT.md) that do not match their recorded hash.
    pub invalid: Vec<String>,
}

impl ViewDiff {
    pub fn is_empty(&self) -> bool {
        self.missing.is_empty() && self.unreadable.is_empty() && self.changed.is_empty() && self.invalid.is_empty()
    }

    /// "<invalid>; missing view files: a; unreadable view files: b; view files differ from the log (hand edit or a failed reprint): c"
    pub fn report(&self) -> String {
        let mut parts = self.invalid.clone();
        if !self.missing.is_empty() {
            parts.push(format!("missing view files: {}", self.missing.join(", ")));
        }
        if !self.unreadable.is_empty() {
            parts.push(format!("unreadable view files: {}", self.unreadable.join(", ")));
        }
        if !self.changed.is_empty() {
            parts.push(format!(
                "view files differ from the log (hand edit or a failed reprint): {}",
                self.changed.join(", ")
            ));
        }
        parts.join("; ")
    }
}

/// The first symlink on `rel` below `dir`, as a path relative to `dir`.
/// Missing components are not links. Does not follow any symlink it finds.
fn symlink_on_path(dir: &Path, rel: &str) -> std::io::Result<Option<String>> {
    let mut cur = dir.to_path_buf();
    let mut acc = String::new();
    for part in Path::new(rel).components() {
        let std::path::Component::Normal(name) = part else {
            continue;
        };
        cur.push(name);
        if !acc.is_empty() {
            acc.push('/');
        }
        acc.push_str(&name.to_string_lossy());
        match fs::symlink_metadata(&cur) {
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => return Ok(None),
            Err(e) => return Err(e),
            Ok(meta) if meta.file_type().is_symlink() => return Ok(Some(acc)),
            Ok(_) => {}
        }
    }
    Ok(None)
}

/// Write `text` to a temp file in the same folder, sync it, then rename over `path`.
/// A hard-linked or symlinked view is replaced; the other name or target is left alone.
fn write_atomic(path: &Path, text: &str) -> Res<()> {
    let dir = path.parent().ok_or_else(|| format!("no parent for {}", path.display()))?;
    let name = path.file_name().ok_or_else(|| format!("no name for {}", path.display()))?;
    let tmp = dir.join(format!(".{}.wf-tmp", name.to_string_lossy()));
    let _ = fs::remove_file(&tmp);
    let write = (|| -> std::io::Result<()> {
        let mut f = fs::OpenOptions::new().write(true).create_new(true).open(&tmp)?;
        f.write_all(text.as_bytes())?;
        f.sync_all()?;
        fs::rename(&tmp, path)?;
        Ok(())
    })();
    if write.is_err() {
        let _ = fs::remove_file(&tmp);
    }
    write.map_err(|e| format!("cannot write {}: {e}", path.display()))
}

/// Compare the view files on disk with the log.
pub fn edited(p: &Page) -> Res<ViewDiff> {
    let mut d = ViewDiff::default();
    d.invalid = hash_faults(p)?;
    let pinned = pinned_files(p);
    for (rel, text) in views(p)? {
        let path = p.dir.join(&rel);
        match symlink_on_path(&p.dir, &rel) {
            Ok(Some(_)) => {
                d.changed.push(rel);
                continue;
            }
            Err(_) => {
                d.unreadable.push(rel);
                continue;
            }
            Ok(None) => {}
        }
        match fs::read_to_string(&path) {
            Ok(disk) => {
                let got = sha(&disk);
                if let Some((nn, file, want)) = pinned.get(&rel) {
                    if &got != want {
                        d.invalid.push(hash_invalid(file, *nn, format!("the copy on disk hashes to {}, the log recorded {}", short(&got), hash12(want))));
                    }
                }
                if got != sha(&text) {
                    d.changed.push(rel);
                }
            }
            Err(e) if e.kind() == std::io::ErrorKind::NotFound => d.missing.push(rel),
            Err(_) => d.unreadable.push(rel),
        }
    }
    Ok(d)
}

/// Relative path -> (pass, file, recorded hash) for every released file the log pins.
fn pinned_files(p: &Page) -> BTreeMap<String, (u32, &'static str, String)> {
    let mut m = BTreeMap::new();
    for x in p.passes.values() {
        let Some(pk) = &x.pack else { continue };
        for (file, key) in HASHED {
            if let Some(h) = recorded_hash(pk, key) {
                m.insert(format!("05.{:02}/{file}", x.nn), (x.nn, file, h));
            }
        }
    }
    m
}

pub fn write(p: &Page) -> Res<()> {
    write_except(p, &[])
}

/// Reprint views after the log was appended. If the reprint fails, name the
/// new log entry so a retry is not mistaken for a no-op (and does not double-log).
pub fn write_after_append(p: &Page) -> Res<()> {
    write(p).map_err(|e| {
        let n = p.events.last().map(|ev| ev.seq).unwrap_or(0);
        format!("logged as entry {n}; views not reprinted ({e}); run wf verify {} --fix", p.addr)
    })
}

/// Reprint views from the log, skipping the named relative paths.
pub fn write_except(p: &Page, skip: &[String]) -> Res<()> {
    let faults = hash_faults(p)?;
    if !faults.is_empty() {
        return Err(format!("refused to reprint: {}; nothing was changed (Director t373u: a released file that does not match its hash is invalid)", faults.join("; ")));
    }
    let all = views(p)?;
    let mut linked = Vec::new();
    for rel in all.keys() {
        if skip.iter().any(|s| s == rel) {
            continue;
        }
        match symlink_on_path(&p.dir, rel) {
            Ok(Some(link)) if link != *rel => {
                if !linked.contains(&link) {
                    linked.push(link);
                }
            }
            Err(e) => {
                return Err(format!("cannot read {}: {e}", p.dir.join(rel).display()));
            }
            _ => {}
        }
    }
    if !linked.is_empty() {
        return Err(format!(
            "linked folder{}: {}; nothing was changed",
            if linked.len() == 1 { "" } else { "s" },
            linked.join(", ")
        ));
    }
    for (rel, text) in all {
        if skip.iter().any(|s| s == &rel) {
            continue;
        }
        let path = p.dir.join(&rel);
        if let Some(d) = path.parent() {
            fs::create_dir_all(d).map_err(|e| e.to_string())?;
        }
        write_atomic(&path, &text)?;
    }
    Ok(())
}

/// The return event's git change list, as "A path, M path, D path".
/// Paths that came from the builder are escaped when they contain a refused character.
pub fn git_changed_text(r: &Value) -> String {
    r["changed"]
        .as_array()
        .map(|a| {
            a.iter()
                .filter_map(|v| {
                    if let Some(s) = v.as_str() {
                        Some(escape_line(s))
                    } else {
                        let letter = s(v, "letter");
                        let path = s(v, "path");
                        if path.is_empty() { None } else { Some(format!("{letter} {}", escape_line(&path))) }
                    }
                })
                .collect::<Vec<_>>()
                .join(", ")
        })
        .unwrap_or_default()
}

pub fn version_of(text: &str) -> String {
    format!("hash {}", short(&sha(text)))
}

pub fn cards_text(v: &Value) -> String {
    v.as_object().map(|m| m.iter().map(|(k, v)| format!("{k} {}", v.as_str().unwrap_or(""))).collect::<Vec<_>>().join(", ")).unwrap_or_default()
}


#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    #[test]
    fn missing_or_v1_selects_the_8eb1fdb_text() {
        for pk in [json!({}), json!({"templates": "1"})] {
            let (a, p, _) = packed_templates(&pk, "1.2.3.4").unwrap();
            assert!(a.contains("- docs/AXIOMS.md: {{src_axioms}}"), "{a}");
            assert!(!a.contains("kit folder"), "{a}");
            assert!(p.contains("Read first: {{dir}}/AGENTS.md, docs/AXIOMS.md, docs/DESIGN.md"), "{p}");
            assert!(!p.contains("kit folder"), "{p}");
        }
    }

    #[test]
    fn v2_selects_the_current_text() {
        let (a, p, _) = packed_templates(&json!({"templates": "2"}), "1.2.3.4").unwrap();
        assert!(a.contains("kit folder") && a.contains("cargo clean -p wf"), "{a}");
        assert!(p.contains("kit folder"), "{p}");
    }

    #[test]
    fn unknown_version_names_the_page_and_entry() {
        for pk in [
            json!({"templates": "9", "seq": 6}),
            json!({"templates": 2, "seq": 6}),
            json!({"templates": true, "seq": 6}),
            json!({"templates": null, "seq": 6}),
        ] {
            let err = packed_templates(&pk, "90.10.00.0001").unwrap_err();
            assert!(err.contains("unknown template version"), "{err}");
            assert!(err.contains("page 90.10.00.0001"), "{err}");
            assert!(err.contains("entry 6"), "{err}");
        }
    }
}
