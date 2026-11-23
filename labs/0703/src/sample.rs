use std::fmt::Write;

pub const PAGE_COUNT: usize = 1_000;
pub const SEED: u64 = 0x0703_5EED;

#[derive(Debug, PartialEq, Eq)]
pub struct Page {
    pub id: String,
    pub text: String,
}

impl Page {
    pub fn filename(&self) -> String {
        format!("{}.seq", self.id)
    }

    pub fn probe(&self, version: u8) -> String {
        format!("Storage trial v{version} marker {}", self.id)
    }

    pub fn revised(&self) -> Self {
        Self {
            id: self.id.clone(),
            text: self.text.replacen(&self.probe(1), &self.probe(2), 1),
        }
    }
}

struct Shape {
    name: &'static str,
    bytes: usize,
    draft: bool,
    // Each block carries a face or counted subface and its events.
    // A leading '+' denotes a proposal event that has yet to be written.
    blocks: &'static [(&'static str, &'static [&'static str])],
}

const SHAPES: &[Shape] = &[
    Shape {
        name: "seqaddr",
        bytes: 25848,
        draft: false,
        blocks: &[
            ("00", &["put"]),
            ("01", &["put"]),
            ("02", &["put"]),
            ("04", &["put"]),
            ("06", &[]),
            ("06.01", &["put"]),
        ],
    },
    Shape {
        name: "bob",
        bytes: 2038,
        draft: false,
        blocks: &[("00", &["put"]), ("01", &["put"]), ("04", &["put"])],
    },
    Shape {
        name: "timer",
        bytes: 3440,
        draft: false,
        blocks: &[
            ("00", &["put"]),
            ("01", &["put", "copy", "note", "merge", "promote"]),
            ("04", &["put", "copy", "note"]),
            ("05", &[]),
            ("05.01", &["put", "tail", "tail", "tail", "tail"]),
            ("06", &[]),
            ("06.01", &["put"]),
        ],
    },
    Shape {
        name: "book-door",
        bytes: 473,
        draft: false,
        blocks: &[("00", &["put"])],
    },
    Shape {
        name: "dictionary",
        bytes: 824,
        draft: false,
        blocks: &[("00", &["put"]), ("03", &[]), ("03.16", &["put"])],
    },
    Shape {
        name: "dev",
        bytes: 872,
        draft: false,
        blocks: &[("00", &["put"]), ("04", &["put"])],
    },
    Shape {
        name: "ide-design",
        bytes: 1354,
        draft: false,
        blocks: &[
            ("00", &["put"]),
            ("04", &["put"]),
            ("05", &[]),
            ("05.01", &["put"]),
        ],
    },
    Shape {
        name: "cats",
        bytes: 1091,
        draft: true,
        blocks: &[("00", &["put"]), ("01", &["put"])],
    },
    Shape {
        name: "bob-proposal",
        bytes: 2335,
        draft: true,
        blocks: &[
            ("00", &["put"]),
            ("01", &["put"]),
            ("04", &["put"]),
            ("06", &[]),
            ("06.01", &["+put"]),
        ],
    },
    Shape {
        name: "cats-proposal",
        bytes: 241,
        draft: true,
        blocks: &[("00", &["+put"]), ("04", &["+put"])],
    },
    Shape {
        name: "bob-real",
        bytes: 7619,
        draft: false,
        blocks: &[
            ("00", &["put"]),
            ("01", &["put"]),
            ("05", &[]),
            ("05.01", &["put"]),
            ("05.02", &["put"]),
        ],
    },
];

pub fn pages(count: usize) -> Vec<Page> {
    let mut seed = SEED;
    (0..count)
        .map(|index| make_page(index, &SHAPES[index % SHAPES.len()], &mut seed))
        .collect()
}

fn make_page(index: usize, shape: &Shape, seed: &mut u64) -> Page {
    let id = format!("91.07.03.{:04}", index + 1);
    let mut page = Page {
        id,
        text: String::from("seqpage 1\n"),
    };
    let probe = page.probe(1);
    let state = if shape.draft { "draft" } else { "live" };
    let mut history = String::from("~ history\n");
    let mut entry = 0;
    let events = shape.blocks.iter().map(|(_, ops)| ops.len()).sum::<usize>();
    let target_bytes = shape.bytes * (85 + draw(seed, 31)) / 100;
    let body_budget = (target_bytes / events).saturating_sub(155);
    let face_names = ["registry", "law", "schema", "operate", "user", "tasks", "notes"];

    for (section, ops) in shape.blocks {
        let address = format!("{}.{}", page.id, section);
        if section.contains('.') {
            writeln!(page.text, "== {section} {address}").unwrap();
        } else {
            let name = face_names[section.parse::<usize>().unwrap()];
            writeln!(page.text, "= {section} {name} {address}").unwrap();
        }
        if *section == "00" {
            writeln!(page.text, "title := {}-sample\nstate := {state}", shape.name).unwrap();
        }
        if ops.is_empty() {
            page.text.push('\n');
        }
        for op in *ops {
            if let Some(proposal) = op.strip_prefix('+') {
                writeln!(page.text, "\n--- new {proposal} {address}").unwrap();
            } else {
                entry += 1;
                writeln!(
                    page.text,
                    "\n--- @{entry} {op} {address}\nat: 2026-11-19T20:{entry:02}:00Z\nby: storage-lab"
                )
                .unwrap();
                writeln!(history, "@{entry} {op} {address}").unwrap();
            }
            if *section == "00" {
                writeln!(page.text, "| {probe}").unwrap();
            }
            add_body(&mut page.text, body_budget, seed);
            page.text.push('\n');
        }
    }
    page.text.push_str(&history);
    page.text.push_str("~ end\n");
    page
}

// Fixed LCG and word list keep the workload stable across platforms and toolchains.
fn draw(seed: &mut u64, upper: usize) -> usize {
    *seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
    ((*seed >> 32) % upper as u64) as usize
}

fn add_body(body: &mut String, budget: usize, seed: &mut u64) {
    const WORDS: &[&str] = &[
        "address", "approve", "archive", "book", "branch", "build", "card", "check", "choice",
        "clock", "copy", "counter", "draft", "entry", "evidence", "face", "finding", "grant",
        "history", "index", "law", "lead", "lineage", "menu", "note", "order", "page", "person",
        "reason", "record", "registry", "report", "review", "rule", "sample", "schema", "slot",
        "source", "stamp", "state", "task", "text", "time", "trial", "view", "write",
    ];
    let start = body.len();
    while body.len() - start < budget {
        write!(body, "| Sample ").unwrap();
        for word in 0..(5 + draw(seed, 7)) {
            if word > 0 {
                body.push(' ');
            }
            body.push_str(WORDS[draw(seed, WORDS.len())]);
        }
        body.push_str(".\n");
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn seeded_corpus_exercises_all_shapes() {
        let corpus = pages(PAGE_COUNT);
        assert_eq!(corpus, pages(PAGE_COUNT));
        for (index, page) in corpus.iter().enumerate() {
            let shape = &SHAPES[index % SHAPES.len()];
            assert!(page.text.contains(&format!("title := {}-sample", shape.name)));
            assert!(page.text.starts_with("seqpage 1\n= 00 registry "));
            assert!(page.text.ends_with("~ end\n"));
            assert_eq!(page.text.matches(&page.probe(1)).count(), 1);
        }
    }
}
