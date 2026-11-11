//! Director ruling R5: drafts are found and inherited; the seated face wins at the same spot;
//! the answer shows the draft state and why it is a draft (R5 follow-up).
mod common;
use common::*;

#[tokio::test]
async fn r5_inherited_draft_is_found_and_marked_draft_with_why() {
    let s = Srv::start(&kernel_dir("r5a")).await;
    seed(&s).await;
    let (c, f) = s.get("/face/10.11.21.0030.01").await;
    assert_eq!(c, 200, "{f}");
    assert_eq!((f["resolved_from"].as_str(), f["state"].as_str()), (Some("kernel"), Some("draft")));
    assert_eq!(f["source"], "00.00.00.0030.01");
    assert_eq!(f["why_draft"]["has_seated"], false);
    assert_eq!(f["why_draft"]["opened_by_entry"], 6);
    let (_, p) = s.get("/page/10.11.21.0030").await;
    assert_eq!(p["faces"]["01.draft"]["resolved_from"], "kernel", "{p}");
    assert_eq!(p["faces"]["01.draft"]["state"], "draft");
    s.stop().await;
}

#[tokio::test]
async fn r5_seated_wins_over_its_draft_at_the_same_spot() {
    let s = Srv::start(&kernel_dir("r5b")).await;
    seed(&s).await;
    let (_, f) = s.get("/face/10.11.21.0020.01").await;
    assert_eq!((f["state"].as_str(), f["body"].as_str()), (Some("seated"), Some("## Route\nRoute the work.")), "{f}");
    assert!(f.get("why_draft").is_none());
    let (_, p) = s.get("/page/10.11.21.0020").await;
    assert_eq!(p["faces"]["01"]["state"], "seated");
    assert!(p["faces"].get("01.draft").is_none(), "the kernel's working draft stays in the kernel: {p}");
    // in the kernel itself both show; the draft says why (one open note)
    let (_, k) = s.get("/page/00.00.00.0020").await;
    assert_eq!(k["faces"]["01.draft"]["why_draft"]["has_seated"], true);
    assert_eq!(k["faces"]["01.draft"]["why_draft"]["open_notes"][0]["text"], "say who routes");
    s.stop().await;
}

#[tokio::test]
async fn r5_local_draft_beats_kernel_seated() {
    let s = Srv::start(&kernel_dir("r5c")).await;
    seed(&s).await;
    let (c, v) = s.post("user", serde_json::json!([put_t("10.11.21.0020.01", "draft", "## Route\nLocal draft route.")])).await;
    assert_eq!(c, 200, "{v}");
    let (_, f) = s.get("/face/10.11.21.0020.01").await;
    assert_eq!((f["resolved_from"].as_str(), f["state"].as_str()), (Some("local"), Some("draft")), "{f}");
    let (_, p) = s.get("/page/10.11.21.0020").await;
    assert!(p["faces"].get("01").is_none(), "{p}");
    assert_eq!(p["faces"]["01.draft"]["resolved_from"], "local");
    s.stop().await;
}

#[tokio::test]
async fn r5_page_why_draft_carries_the_opening_reason_like_face() {
    let s = Srv::start(&kernel_dir("r5d")).await;
    seed(&s).await;
    let mut op = put_t("10.11.21.0020.01", "draft", "## Route\nLocal draft route.");
    op["reason"] = serde_json::json!("try a local route");
    let (c, v) = s.post("user", serde_json::json!([op])).await;
    assert_eq!(c, 200, "{v}");
    let (_, f) = s.get("/face/10.11.21.0020.01").await;
    assert_eq!(f["why_draft"]["reason"], "try a local route", "{f}");
    let (_, p) = s.get("/page/10.11.21.0020").await;
    assert_eq!(p["faces"]["01.draft"]["why_draft"]["reason"], "try a local route", "{p}");
    // a draft opened with no reason has no `reason` key (not null, not empty)
    let (_, k) = s.get("/page/00.00.00.0030").await;
    assert!(k["faces"]["01.draft"]["why_draft"].get("reason").is_none(), "{k}");
    s.stop().await;
}
