//! # ask: the common-questions solver (Director ruling R11)
//!
//! "Most people only have a few important words when they write or say
//! something. We use this as how we solve." (R11)
//!
//! 1. Pull the important words out of a prompt: key words plus the small
//!    linking words (prepositions, pronouns) and question words. Filler words
//!    are dropped. Lowercased; plain ASCII only (R4).
//! 2. Match them against (a) the common-questions list: each entry is a sentence
//!    pattern with variants (`forms`), linked to what answers it, like a brand
//!    card; and (b) brand cards (a typed word equal to a brand form).
//! 3. Rank with a transparent score and say which words matched.
//! 4. Hand back 1-3 pieces, or a probe: a clarifying question for the person.
//!
//! Pure Rust, no network, no state. The word lists, weights, threshold and
//! formula are provisional (BUILD-LOG `[COMPUTE]` 7) and live in [`Config`].

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

/// Question words (R11: "what" + "name" + "my").
pub const QUESTION_WORDS: &[&str] = &["what", "who", "whom", "whose", "where", "when", "why", "how", "which"];
/// Small linking words kept as signal: prepositions, pronouns, possessives, a few auxiliaries.
pub const LINK_WORDS: &[&str] = &[
    "i", "me", "my", "mine", "myself", "you", "your", "yours", "we", "us", "our", "it", "its", "am", "do", "does", "did",
    "to", "for", "of", "in", "on", "at", "by", "with", "from", "about", "into", "over", "under", "after", "before", "up", "out", "off", "than", "as", "if",
];
/// Filler dropped before matching (7: chosen so "what is my name" keeps what + my + name, as R11 says).
pub const FILLER_WORDS: &[&str] = &[
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being", "and", "or", "but", "so", "please", "just", "um", "uh", "er", "hey", "hi", "hello", "ok", "okay", "then", "really", "very",
];
/// Contractions folded to their question word (7). The apostrophe is already gone.
pub const FOLDS: &[(&str, &str)] = &[("whats", "what"), ("whos", "who"), ("wheres", "where"), ("whens", "when"), ("hows", "how"), ("im", "i"), ("ive", "i")];

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Kind {
    Key,
    Link,
    Question,
}

/// One important word of a prompt or a phrasing.
#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct Word {
    /// As typed (case kept; brand forms are case-sensitive, brands.md).
    pub text: String,
    /// Lowercased, apostrophes removed, contraction folded.
    pub norm: String,
    pub kind: Kind,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize)]
pub struct AskError {
    pub error: &'static str,
    pub rule: &'static str,
    pub detail: String,
}

/// R4: printable ASCII 0x20-0x7E plus newline.
pub fn check_ascii(s: &str) -> Result<(), AskError> {
    for (i, b) in s.bytes().enumerate() {
        if !(b == b'\n' || (0x20..=0x7e).contains(&b)) {
            return Err(AskError { error: "invalid", rule: "R4", detail: format!("byte 0x{b:02X} at {i} is not plain ASCII (Director ruling R4); type plain letters only") });
        }
    }
    Ok(())
}

pub fn kind_of(norm: &str) -> Option<Kind> {
    if FILLER_WORDS.contains(&norm) {
        None
    } else if QUESTION_WORDS.contains(&norm) {
        Some(Kind::Question)
    } else if LINK_WORDS.contains(&norm) {
        Some(Kind::Link)
    } else {
        Some(Kind::Key)
    }
}

/// The important words, in order, without repeats (by `norm`).
pub fn words(s: &str) -> Vec<Word> {
    let mut out: Vec<Word> = Vec::new();
    for raw in s.split(|c: char| !(c.is_ascii_alphanumeric() || c == '\'')) {
        let text: String = raw.chars().filter(|c| *c != '\'').collect();
        if text.is_empty() {
            continue;
        }
        let mut norm = text.to_ascii_lowercase();
        if let Some((_, to)) = FOLDS.iter().find(|(f, _)| *f == norm) {
            norm = to.to_string();
        }
        let Some(kind) = kind_of(&norm) else { continue };
        if out.iter().any(|w| w.norm == norm) {
            continue;
        }
        out.push(Word { text, norm, kind });
    }
    out
}

/// A common question: works like a brand card (R11). `forms` are its phrasings.
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct QuestionCard {
    /// Card address, e.g. `10.11.21.0013.01.what-is-my-name`.
    pub address: String,
    pub title: String,
    pub forms: Vec<String>,
    /// Address of what answers it; `None` is a hole (7).
    pub answer: Option<String>,
    #[serde(default)]
    pub hole: Option<String>,
    #[serde(default)]
    pub state: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct BrandCard {
    pub address: String,
    pub title: String,
    /// Case-sensitive forms (brands.md "Forms and case").
    pub forms: Vec<String>,
    #[serde(default)]
    pub means: Option<String>,
    #[serde(default)]
    pub state: Option<String>,
}

/// Every tunable number and the formula, in one place (7).
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Config {
    /// A candidate must score at least this to be handed to the model.
    pub threshold: f64,
    pub weight_key: f64,
    pub weight_link: f64,
    pub weight_question: f64,
    /// Score of a typed word equal to a brand form, case and all.
    pub brand_exact: f64,
    /// Score of a typed word equal to a brand form only when lowercased (below threshold: probe, not guess).
    pub brand_folded: f64,
    pub max_pieces: usize,
    /// How many ranked candidates to show for transparency.
    pub show: usize,
}

impl Default for Config {
    fn default() -> Self {
        Config { threshold: 0.5, weight_key: 2.0, weight_link: 1.0, weight_question: 1.0, brand_exact: 1.0, brand_folded: 0.4, max_pieces: 3, show: 5 }
    }
}

impl Config {
    pub fn weight(&self, k: Kind) -> f64 {
        match k {
            Kind::Key => self.weight_key,
            Kind::Link => self.weight_link,
            Kind::Question => self.weight_question,
        }
    }
    pub fn formula(&self) -> String {
        format!(
            "question: weighted Dice = 2*w(matched) / (w(prompt words) + w(phrasing words)), best phrasing; weights key {}, link {}, question {}. brand: {} if a typed word equals a form exactly, {} if only lowercased. pieces: score >= {}, top {}, one per target.",
            self.weight_key, self.weight_link, self.weight_question, self.brand_exact, self.brand_folded, self.threshold, self.max_pieces
        )
    }
}

/// One ranked guess.
#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct Candidate {
    /// `question` or `brand`.
    pub kind: &'static str,
    /// The card that matched (question card or brand card).
    pub via: String,
    pub via_title: String,
    /// What to hand the model: the answer of a question, or the brand card itself. `None` = hole.
    pub target: Option<String>,
    /// The phrasing or form that matched best.
    pub phrasing: String,
    pub matched: Vec<String>,
    /// Important words of the prompt that did not match.
    pub unmatched: Vec<String>,
    pub score: f64,
    /// The arithmetic, written out.
    pub why: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub hole: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize)]
#[serde(rename_all = "lowercase")]
pub enum Outcome {
    /// 1-3 pieces the model may use (each one target).
    Pieces(Vec<Candidate>),
    /// Nothing cleared the threshold: ask the person.
    Probe { question: String, near: Vec<Candidate> },
}

#[derive(Debug, Clone, PartialEq, Serialize)]
pub struct Solved {
    pub heard: Vec<Word>,
    pub ranked: Vec<Candidate>,
    pub outcome: Outcome,
    pub threshold: f64,
    pub formula: String,
}

fn round3(x: f64) -> f64 {
    (x * 1000.0).round() / 1000.0
}

fn score_question(prompt: &[Word], q: &QuestionCard, cfg: &Config) -> Option<Candidate> {
    let wp: f64 = prompt.iter().map(|w| cfg.weight(w.kind)).sum();
    let mut best: Option<Candidate> = None;
    for form in &q.forms {
        let fw = words(form);
        if fw.is_empty() {
            continue;
        }
        let wf: f64 = fw.iter().map(|w| cfg.weight(w.kind)).sum();
        let matched: Vec<&Word> = prompt.iter().filter(|w| fw.iter().any(|f| f.norm == w.norm)).collect();
        if matched.is_empty() {
            continue;
        }
        let wm: f64 = matched.iter().map(|w| cfg.weight(w.kind)).sum();
        let score = round3(2.0 * wm / (wp + wf));
        if best.as_ref().map(|b| score > b.score).unwrap_or(true) {
            best = Some(Candidate {
                kind: "question",
                via: q.address.clone(),
                via_title: q.title.clone(),
                target: q.answer.clone(),
                phrasing: form.clone(),
                matched: matched.iter().map(|w| w.norm.clone()).collect(),
                unmatched: prompt.iter().filter(|w| !matched.iter().any(|m| m.norm == w.norm)).map(|w| w.norm.clone()).collect(),
                score,
                why: format!("2*{wm} / ({wp} + {wf}) = {score}"),
                hole: q.hole.clone().or_else(|| if q.answer.is_none() { Some("nothing answers this question yet (7)".into()) } else { None }),
            });
        }
    }
    best
}

fn score_brand(prompt: &[Word], b: &BrandCard, cfg: &Config) -> Option<Candidate> {
    let mut best: Option<(f64, &Word, &String)> = None;
    for w in prompt {
        for f in &b.forms {
            let s = if &w.text == f {
                cfg.brand_exact
            } else if w.norm == f.to_ascii_lowercase() {
                cfg.brand_folded
            } else {
                continue;
            };
            if best.map(|x| s > x.0).unwrap_or(true) {
                best = Some((s, w, f));
            }
        }
    }
    let (s, w, f) = best?;
    Some(Candidate {
        kind: "brand",
        via: b.address.clone(),
        via_title: b.title.clone(),
        target: Some(b.address.clone()),
        phrasing: f.clone(),
        matched: vec![w.text.clone()],
        unmatched: prompt.iter().filter(|x| x.norm != w.norm).map(|x| x.norm.clone()).collect(),
        score: s,
        why: if s == cfg.brand_exact { format!("typed `{}` equals form `{f}` exactly = {s}", w.text) } else { format!("typed `{}` equals form `{f}` only lowercased (forms are case-sensitive) = {s}", w.text) },
        hole: None,
    })
}

/// Solve one prompt. Errors only on R4 (not plain ASCII).
pub fn solve(prompt: &str, questions: &[QuestionCard], brands: &[BrandCard], cfg: &Config) -> Result<Solved, AskError> {
    check_ascii(prompt)?;
    let heard = words(prompt);
    let mut ranked: Vec<Candidate> = Vec::new();
    if !heard.is_empty() {
        ranked.extend(questions.iter().filter_map(|q| score_question(&heard, q, cfg)));
        ranked.extend(brands.iter().filter_map(|b| score_brand(&heard, b, cfg)));
    }
    // highest score first; ties: questions before brands, then by address (stable, explainable)
    ranked.sort_by(|a, b| b.score.partial_cmp(&a.score).unwrap().then(a.kind.cmp(b.kind).reverse()).then(a.via.cmp(&b.via)));
    // one piece per target
    let mut pieces: Vec<Candidate> = Vec::new();
    let mut seen: BTreeMap<String, usize> = BTreeMap::new();
    for c in ranked.iter().filter(|c| c.score >= cfg.threshold && c.target.is_some() && c.hole.is_none()) {
        let t = c.target.clone().unwrap();
        if let Some(&i) = seen.get(&t) {
            for m in &c.matched {
                if !pieces[i].matched.contains(m) {
                    pieces[i].matched.push(m.clone());
                }
            }
            continue;
        }
        if pieces.len() == cfg.max_pieces {
            break;
        }
        seen.insert(t, pieces.len());
        pieces.push(c.clone());
    }
    let outcome = if !pieces.is_empty() {
        Outcome::Pieces(pieces)
    } else {
        let near: Vec<Candidate> = ranked.iter().take(3).cloned().collect();
        Outcome::Probe { question: probe_question(&heard, &ranked, cfg), near }
    };
    ranked.truncate(cfg.show);
    Ok(Solved { heard, ranked, outcome, threshold: cfg.threshold, formula: cfg.formula() })
}

/// The clarifying question for the person (R11: "probing them for more detail").
pub fn probe_question(heard: &[Word], ranked: &[Candidate], cfg: &Config) -> String {
    let keys: Vec<&str> = heard.iter().filter(|w| w.kind == Kind::Key).map(|w| w.text.as_str()).collect();
    if heard.is_empty() {
        return "I could not pick out any words I know. What would you like to do?".into();
    }
    if let Some(h) = ranked.iter().find(|c| c.score >= cfg.threshold && c.hole.is_some()) {
        return format!("I know the question \"{}\", but nothing answers it yet. Can you tell me the answer, so I can link it?", h.via_title);
    }
    if let Some(n) = ranked.first() {
        return format!("Do you mean \"{}\"? If not, can you tell me more about what you mean{}?", n.phrasing, if keys.is_empty() { String::new() } else { format!(" by \"{}\"", keys.join(" ")) });
    }
    if keys.is_empty() {
        "Can you say a bit more about what you need?".into()
    } else {
        format!("I don't have anything on \"{}\" yet. Can you tell me more about what you mean?", keys.join(" "))
    }
}

/// Add a phrasing to a question card's `forms:` line in a face body (R11: new
/// phrasings get linked to the known question, like a new brand form).
/// Returns the whole new body. Errors: card not found, phrasing already there.
pub fn add_form(body: &str, card_key: &str, phrasing: &str, title_form: impl Fn(&str) -> String) -> Result<String, &'static str> {
    let lines: Vec<&str> = body.split('\n').collect();
    let mut out: Vec<String> = Vec::with_capacity(lines.len() + 1);
    let mut in_card = false;
    let mut done = false;
    let mut header_at = None;
    for l in lines.iter() {
        if let Some(h) = l.strip_prefix("## ") {
            if in_card && !done {
                // card had no forms line: add one before the next card
                out.insert(header_at.unwrap() + 1, format!("forms: {phrasing}"));
                done = true;
            }
            in_card = title_form(h.trim()) == card_key;
            if in_card {
                header_at = Some(out.len());
            }
            out.push(l.to_string());
            continue;
        }
        if in_card && !done {
            if let Some(v) = l.strip_prefix("forms:") {
                let have: Vec<String> = v.split(',').map(|s| s.trim().to_ascii_lowercase()).collect();
                if have.contains(&phrasing.trim().to_ascii_lowercase()) {
                    return Err("already linked");
                }
                let v = v.trim_end();
                out.push(if v.trim().is_empty() { format!("forms: {phrasing}") } else { format!("forms:{v}, {phrasing}") });
                done = true;
                continue;
            }
        }
        out.push(l.to_string());
    }
    if in_card && !done {
        out.insert(header_at.unwrap() + 1, format!("forms: {phrasing}"));
        done = true;
    }
    if !done {
        return Err("no such card");
    }
    Ok(out.join("\n"))
}
