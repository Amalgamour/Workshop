use ask::*;

fn bob() -> (Vec<QuestionCard>, Vec<BrandCard>) {
    let q = vec![
        QuestionCard { address: "10.11.21.0013.01.what-is-my-name".into(), title: "what is my name".into(), forms: ["what is my name", "whats my name", "who am i", "what do you call me", "my name?"].map(String::from).to_vec(), answer: Some("10.11.21.1001.01.bob".into()), hole: None, state: None },
        QuestionCard { address: "10.11.21.0013.01.what-time-is-it".into(), title: "what time is it".into(), forms: vec!["what time is it".into()], answer: None, hole: Some("no clock source".into()), state: None },
    ];
    let b = vec![BrandCard { address: "10.11.21.1001.01.bob".into(), title: "bob".into(), forms: vec!["Bob".into()], means: Some("the user's name".into()), state: None }];
    (q, b)
}

#[test]
fn r11_keeps_what_my_name() {
    let w: Vec<String> = words("What is my name?").into_iter().map(|w| w.norm).collect();
    assert_eq!(w, ["what", "my", "name"]);
    assert_eq!(words("whats my name")[0].norm, "what");
    assert_eq!(words("What's my name")[0].norm, "what");
}

#[test]
fn bob_variants_hit_the_bob_card() {
    let (q, b) = bob();
    for p in ["what is my name", "whats my name?", "who am I", "What do you call me?", "my name?", "um, what's my name please"] {
        let s = solve(p, &q, &b, &Config::default()).unwrap();
        match s.outcome {
            Outcome::Pieces(ps) => assert_eq!(ps[0].target.as_deref(), Some("10.11.21.1001.01.bob"), "{p}"),
            o => panic!("{p}: {o:?}"),
        }
    }
}

#[test]
fn exact_brand_form_is_a_piece_case_matters() {
    let (q, b) = bob();
    let s = solve("tell Bob hello", &q, &b, &Config::default()).unwrap();
    assert!(matches!(&s.outcome, Outcome::Pieces(p) if p[0].kind == "brand"));
    let s = solve("bob", &q, &b, &Config::default()).unwrap();
    assert!(matches!(s.outcome, Outcome::Probe { .. }), "lowercased form is below threshold");
}

#[test]
fn nonsense_probes() {
    let (q, b) = bob();
    let s = solve("purple dishwasher zebra", &q, &b, &Config::default()).unwrap();
    match s.outcome {
        Outcome::Probe { question, .. } => assert!(question.contains("purple dishwasher zebra"), "{question}"),
        o => panic!("{o:?}"),
    }
    let s = solve("?!", &q, &b, &Config::default()).unwrap();
    assert!(matches!(s.outcome, Outcome::Probe { .. }));
}

#[test]
fn near_miss_probes_with_the_near_question() {
    let (q, b) = bob();
    let s = solve("what is the weather", &q, &b, &Config::default()).unwrap();
    match s.outcome {
        Outcome::Probe { question, near } => {
            assert!(!near.is_empty());
            assert!(question.starts_with("Do you mean"), "{question}");
        }
        o => panic!("{o:?}"),
    }
}

#[test]
fn hole_is_never_a_piece() {
    let (q, b) = bob();
    let s = solve("what time is it", &q, &b, &Config::default()).unwrap();
    match s.outcome {
        Outcome::Probe { question, .. } => assert!(question.contains("nothing answers it yet"), "{question}"),
        o => panic!("{o:?}"),
    }
}

#[test]
fn r4_non_ascii_refused() {
    let (q, b) = bob();
    let e = solve("what is my n\u{e0}me", &q, &b, &Config::default()).unwrap_err();
    assert_eq!(e.rule, "R4");
    assert!(solve("tab\there", &q, &b, &Config::default()).is_err());
}

#[test]
fn score_is_written_out() {
    let (q, b) = bob();
    let s = solve("what is my name", &q, &b, &Config::default()).unwrap();
    assert_eq!(s.ranked[0].score, 1.0);
    assert_eq!(s.ranked[0].why, "2*4 / (4 + 4) = 1");
    assert_eq!(s.ranked[0].matched, ["what", "my", "name"]);
}

#[test]
fn at_most_three_pieces_one_per_target() {
    let q: Vec<QuestionCard> = (0..5).map(|i| QuestionCard { address: format!("q{i}"), title: "where is it".into(), forms: vec!["where is it".into()], answer: Some(format!("t{i}")), hole: None, state: None }).collect();
    let s = solve("where is it", &q, &[], &Config::default()).unwrap();
    assert!(matches!(&s.outcome, Outcome::Pieces(p) if p.len() == 3));
    let q2: Vec<QuestionCard> = (0..3).map(|i| QuestionCard { answer: Some("same".into()), address: format!("q{i}"), ..q[0].clone() }).collect();
    let s = solve("where is it", &q2, &[], &Config::default()).unwrap();
    assert!(matches!(&s.outcome, Outcome::Pieces(p) if p.len() == 1));
}

#[test]
fn add_form_links_a_phrasing() {
    let body = "## what is my name\ntype: question\nforms: what is my name, who am i\nanswer: x";
    let tf = |h: &str| h.to_ascii_lowercase().replace(' ', "-");
    let nb = add_form(body, "what-is-my-name", "what am i called", tf).unwrap();
    assert!(nb.contains("forms: what is my name, who am i, what am i called"));
    assert_eq!(add_form(body, "what-is-my-name", "Who am I", tf), Err("already linked"));
    assert_eq!(add_form(body, "nope", "x", tf), Err("no such card"));
}
