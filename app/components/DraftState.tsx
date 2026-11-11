import type { DraftWhy } from "@/lib/compute";

/** R5: a draft is found, and it shows why it is a draft. */
export function DraftState({ state, tail, why }: { state?: string; tail?: string; why?: DraftWhy }) {
  const isDraft = state === "draft" || tail === "draft";
  if (!isDraft) return null;
  const open = why?.open_notes ?? [];
  return (
    <div className="draftbox">
      <div><span className="badge tail"><b>Draft</b> not live yet</span> <b>Why it is a draft:</b>{" "}
        {why?.reason ? <span>{why.reason}</span> : open[0] ? <span>{open[0].text} <span className="note">(first open note)</span></span> : <span className="note"><b>7</b> no reason was recorded when it was opened</span>}
      </div>
      {why ? (
        <div className="note" style={{ marginTop: 4 }}>
          {why.has_seated ? "A working copy of a live face. " : "There is no live face here yet. "}
          {open.length ? `${open.length} note(s) still to merge. ` : "No notes waiting. "}
          {why.merged_notes ? `${why.merged_notes} merged. ` : ""}
          {why.opened_by_entry ? `Opened by entry #${why.opened_by_entry}.` : ""}
        </div>
      ) : null}
      {open.length ? <ul className="note" style={{ margin: "4px 0 0" }}>{open.map((n) => <li key={n.n}>#{n.n} {n.by}: {n.text}</li>)}</ul> : null}
    </div>
  );
}
