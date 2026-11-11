//! Value and body encoding (seqpage.md 6.3, 6.4). Both are exact inverses,
//! which is what makes the round trip lossless.

/// A value is written raw when it is plain; otherwise as a JSON string.
pub fn is_plain(s: &str) -> bool {
    !s.is_empty() && s.trim() == s && !s.starts_with('"') && !s.chars().any(|c| c.is_control())
}

pub fn encode_value(s: &str) -> String {
    if is_plain(s) {
        s.to_string()
    } else {
        serde_json::to_string(s).expect("string serializes")
    }
}

/// Inverse of [`encode_value`]. A raw value must itself be plain.
pub fn decode_value(raw: &str) -> Result<String, String> {
    if raw.starts_with('"') {
        let v: String = serde_json::from_str(raw).map_err(|e| format!("bad quoted value: {e}"))?;
        if let Some((_, _, c)) = first_non_r4(&v) {
            return Err(format!("quoted value holds {} (R4: plain ASCII only)", describe_char(c)));
        }
        if is_plain(&v) {
            return Err("a plain value must be written without quotes".into());
        }
        Ok(v)
    } else if is_plain(raw) {
        Ok(raw.to_string())
    } else {
        Err("value is empty or has leading/trailing space or control characters; quote it as JSON".into())
    }
}

/// Body lines: every line of the body is prefixed `| ` (an empty line is `|`).
pub fn body_lines(body: &str) -> Vec<String> {
    body.split('\n').map(|l| if l.is_empty() { "|".to_string() } else { format!("| {l}") }).collect()
}

/// One body line back to its text; `None` if the line is not a body line.
pub fn body_line(line: &str) -> Option<Result<&str, String>> {
    if line == "|" {
        Some(Ok(""))
    } else if let Some(rest) = line.strip_prefix("| ") {
        if rest.is_empty() {
            Some(Err("`| ` with nothing after it: write an empty body line as `|`".into()))
        } else {
            Some(Ok(rest))
        }
    } else if line.starts_with('|') {
        Some(Err("a body line is `|` or `| ` followed by text".into()))
    } else {
        None
    }
}

/// Director ruling R4: stored text is plain ASCII, printable 0x20-0x7E plus
/// newline 0x0A. No tab, no CR, no accents, no dashes or quotes outside ASCII.
pub fn is_r4_char(c: char) -> bool {
    c == '\n' || (' '..='~').contains(&c)
}

/// The first character that breaks R4, as (1-based line, 1-based column, char).
pub fn first_non_r4(s: &str) -> Option<(usize, usize, char)> {
    let mut line = 1;
    let mut col = 0;
    for c in s.chars() {
        col += 1;
        if !is_r4_char(c) {
            return Some((line, col, c));
        }
        if c == '\n' {
            line += 1;
            col = 0;
        }
    }
    None
}

/// Describe a character for an error message: `U+2014`, plus a name for the usual ones.
pub fn describe_char(c: char) -> String {
    let name = match c {
        '\t' => " (tab)",
        '\r' => " (carriage return)",
        '\u{2014}' => " (em dash; write -- or -)",
        '\u{2013}' => " (en dash; write -)",
        '\u{201C}' | '\u{201D}' => " (curly double quote; write \")",
        '\u{2018}' | '\u{2019}' => " (curly single quote; write ')",
        '\u{00A7}' => " (section sign; write 'section')",
        '\u{00A0}' => " (no-break space; write a space)",
        _ => "",
    };
    format!("U+{:04X}{name}", c as u32)
}

/// Every string inside a JSON value passes R4 (keys too).
pub fn json_r4(v: &serde_json::Value) -> Option<char> {
    match v {
        serde_json::Value::String(s) => first_non_r4(s).map(|x| x.2),
        serde_json::Value::Array(a) => a.iter().find_map(json_r4),
        serde_json::Value::Object(m) => m.iter().find_map(|(k, v)| first_non_r4(k).map(|x| x.2).or_else(|| json_r4(v))),
        _ => None,
    }
}
