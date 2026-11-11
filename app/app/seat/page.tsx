import Link from "next/link";
import { get, withDraftReasons, type LogEntry, type PageDetail } from "@/lib/compute";
import { DraftState } from "@/components/DraftState";
import { QueueResult } from "@/components/QueueResult";
import { Addr, Header, Hole, Raw } from "@/components/ui";
import { SeatForm } from "@/components/SeatForm";
import { draftNotes } from "@/lib/drafting";
import { FACE_NAMES, torontoTime } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function Seat({ searchParams }: { searchParams: Promise<{ addr?: string; done?: string }> }) {
  const { addr, done } = await searchParams;
  const head = <Header title="Seat a face" lede={<>Seating makes a draft the live face. During this build stage it may be done without the Director&apos;s eyes, but only after a hostile trial from another view, and it is always recorded so it can be found and re-reviewed (Director ruling R2).</>} />;
  const m = /^(\d\d\.\d\d\.\d\d\.\d{4})\.(\d\d)$/.exec(addr ?? "");
  if (!m)
    return <>{head}<form className="panel" action="/seat"><div className="field"><label>Face address <small>(desk.shelf.book.page.face, like 10.11.21.1100.04)</small></label><input className="big mono" name="addr" defaultValue={addr ?? ""} /></div><button className="go">Open</button></form></>;
  const [page, face] = [m[1], m[2]];
  const [pr, hr] = await Promise.all([get<PageDetail>(`/page/${page}`), get<LogEntry[]>(`/history/${page}.${face}`)]);
  const pd = pr.kind === "ok" ? await withDraftReasons(pr.data) : null;
  const draft = pd?.faces[`${face}.draft`];
  const live = pd?.faces[face];
  const hist = hr.kind === "ok" ? hr.data : [];
  const notes = draftNotes(hist, `${page}.${face}`);
  const seats = hist.filter((e) => e.op === "promote");
  return (
    <>
      {head}
      <QueueResult id={done} />
      <div className="panel">
        <h3>Face {face} {FACE_NAMES[face]?.name} of <Link href={`/page/${page}?face=${face}`}>{pd?.title ?? page}</Link></h3>
        <Addr a={`${page}.${face}`} />
      </div>
      {!draft ? <Hole what={`a draft of face ${face}`} why="There is no draft to seat. Write one first." traceHref={`/resolve?addr=${page}.${face}`} /> : (
        <>
          <div className="cols">
            <div className="panel"><h3>Live now</h3>{live && live.resolved_from === "local" ? <pre className="body mono">{live.body}</pre> : <p className="note">Nothing live in this book yet{live ? ` (inherited from ${live.source})` : ""}.</p>}</div>
            <div className="panel"><h3>The draft that would become live</h3><DraftState state={draft.state ?? "draft"} tail={draft.tail} why={draft.why_draft} /><pre className="body mono">{draft.body}</pre><p className="note">by {draft.by}{draft.at ? `, ${torontoTime(draft.at)}` : ""}</p></div>
          </div>
          <SeatForm faceAddr={`${page}.${face}`} openNotes={notes.filter((n) => !n.struck).length} />
        </>
      )}
      {seats.length ? (
        <div className="panel"><h3>Earlier seats of this face</h3>
          <table className="log"><thead><tr><th>When</th><th>Who</th><th>Approved by</th><th>Trial</th><th>Entry</th></tr></thead>
            <tbody>{seats.map((e) => <tr key={e.n}><td>{torontoTime(e.at)}</td><td>{e.by}</td><td><b>{e["approved-by"] ?? "7 not recorded"}</b></td><td><code>{e.trial ?? "—"}</code></td><td>#{e.n}</td></tr>)}</tbody></table>
        </div>
      ) : null}
      <Raw data={{ page: pd, history: hist }} url={pr.url} />
    </>
  );
}
