"""PRIME/DIRECTOR ONLY: build a disposable desk for a later cold-Prime Colab of the prime cycle (0515.prime-cycle/05.01).

  python -B build_colab_desk.py --eval-dir NEW_EMPTY_DIR

The desk is a new temporary Git repository with five registered works, built through the real CLI and real capture:
- W1: a new captured return, no review;
- W2: an accepted, finished pass whose page goal stays open;
- W3: an accepted pass, then an explicit goal completion;
- W4: a Director-input hold;
- W5: an interrupted review write (a partial), left for the candidate to recover.
Every decision is SYNTHETIC SUPPLIED. The desk path and registration are printed for the candidate. The baseline for
evaluate.py goes to --eval-dir, which must be outside the desk and is not given to the candidate. The candidate's journal
root is <desk>/journal, outside the desk repository (05.02). No model is run here.
"""
import json
import sys
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "tests"))
sys.path.insert(0, str(HERE.parent))
import fixture as F  # noqa: E402
import prime_cycle as pc  # noqa: E402

LANES = (("W1", "0591.colab-w1"), ("W2", "0592.colab-w2"), ("W3", "0593.colab-w3"), ("W4", "0594.colab-w4"), ("W5", "0595.colab-w5"))


def tree(repo: Path) -> dict:
    return {p.relative_to(repo).as_posix(): F.sha(p.read_bytes()) for p in sorted(repo.rglob("*"))
            if p.is_file() and ".git" not in p.relative_to(repo).parts}


def build(eval_dir: Path) -> dict:
    eval_dir.mkdir(parents=True, exist_ok=False)
    d = F.Desk(prefix="pcy-colab-")
    works = []
    for wid, lane in LANES:
        m = d.member(wid.lower(), lane, "05.01")
        d.page(lane, "05.01", F.page_text(m, d.receipt(m)))
        works.append(d.work(wid, lane, "05.01", m, goal_id=f"{wid.lower()}-goal",
                            statement=f"SUPPLIED FIXTURE goal for {wid}: the lane's bounded note is written and reviewed."))
    reg = d.registration(works)
    _, v = d.read(reg)
    tm = {w["work_id"]: w["template"] for w in v["works"]}
    for wid, kind in (("W2", "accept-finished-open"), ("W3", "accept-finished-open"), ("W4", "director-input")):
        code, out = pc.record(reg, d.write_decision(F.fill(tm[wid], kind), f"dec-{wid}.json"))
    _, v = d.read(reg)
    t3 = next(w["template"] for w in v["works"] if w["work_id"] == "W3")
    pc.record(reg, d.write_decision(F.fill(t3, "complete"), "dec-W3b.json"))
    real = pc.write_file

    def torn(p, data):  # interrupt the W5 write at REVIEW.md, leaving record.json and half a projection
        if p.name == "REVIEW.md":
            with open(p, "xb") as h:
                h.write(data[: len(data) // 2])
            raise OSError("colab fixture: injected interruption")
        return real(p, data)
    with mock.patch.object(pc, "write_file", torn):
        try:
            pc.record(reg, d.write_decision(F.fill(tm["W5"], "accept-finished-open"), "dec-W5.json"))
        except pc.PartialWrite:
            pass
    for f in d.tmp.glob("dec-*.json"):  # the candidate sees no prior decision files, only records on the desk
        f.unlink()
    _, view = d.read(reg)
    base = {"schema": "prime-cycle-colab-baseline/1", "desk": str(d.tmp), "registration": str(reg), "repo_tree": tree(d.repo),
            "view": {w["work_id"]: {k: w[k] for k in ("pass_state", "disposition", "pass_terminal", "goal_terminal")}
                     | {"latest": (w.get("latest_review") or {}).get("review_id"), "partial": [p["review_id"] for p in w["reviews"]["partial"]]}
                     for w in view["works"]},
            "recover_work": "W5", "journal_root": str(d.tmp / "journal"), "label": "SYNTHETIC SUPPLIED fixture; not a model benchmark"}
    (eval_dir / "baseline.json").write_text(json.dumps(base, indent=1) + "\n", encoding="utf-8", newline="\n")
    return base


if __name__ == "__main__":
    out = Path(sys.argv[sys.argv.index("--eval-dir") + 1]).resolve()
    b = build(out)
    print(f"desk: {b['desk']}\nregistration: {b['registration']}\njournal root (give to the candidate): {b['journal_root']}\n"
          f"baseline (evaluator only): {out / 'baseline.json'}")
