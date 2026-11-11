import Link from "next/link";
import { get, type LogEntry, type PageDetail } from "@/lib/compute";
import { QueueResult } from "@/components/QueueResult";
import { Addr, Header, Raw } from "@/components/ui";
import { DraftForm } from "@/components/DraftForm";
import { draftNotes } from "@/lib/drafting";
import { FACE_NAMES } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function Draft({ searchParams }: { searchParams: Promise<{ page?: string; face?: string; done?: string; override?: string }> }) {
  const sp = await searchParams;
  const head = <Header title="Draft a face" lede="Write or change one face of a page. Nothing becomes live here: a draft is checked by the compute and written as a draft. Seating it (making it live) is a separate step." />;
  if (!sp.page || !/^\d\d\.\d\d\.\d\d\.\d{4}$/.test(sp.page))
    return (
      <>{head}
        <form className="panel" action="/draft">
          <div className="field"><label>Page address <small>(full: desk.shelf.book.page, like 10.11.21.1100)</small></label><input className="big mono" name="page" defaultValue={sp.page ?? ""} placeholder="10.11.21.1100" /></div>
          <div className="field"><label>Face</label>
            <select className="big" name="face" defaultValue={sp.face ?? "04"}>{Object.entries(FACE_NAMES).filter(([f]) => f !== "00" && f !== "05").map(([f, v]) => <option key={f} value={f}>{f} {v.name} — {v.plain}</option>)}</select></div>
          <button className="go">Open</button>
          <p className="note">Jobs on face 05 have their own screen: <Link href="/work">Work loop</Link>.</p>
        </form>
      </>
    );
  const page = sp.page, face = /^\d\d$/.test(sp.face ?? "") ? sp.face! : "04";
  const [pr, hr] = await Promise.all([get<PageDetail>(`/page/${page}`), get<LogEntry[]>(`/history/${page}.${face}`)]);
  const pageData = pr.kind === "ok" ? pr.data : null;
  const live = pageData?.faces[face];
  const draft = pageData?.faces[`${face}.draft`];
  const notes = hr.kind === "ok" ? draftNotes(hr.data, `${page}.${face}`) : [];
  const mode = !pageData ? "new-page" : draft ? "draft" : live && live.resolved_from === "local" ? "seated" : live ? "inherited" : "new-face";
  return (
    <>
      {head}
      <QueueResult id={sp.done} />
      <div className="panel">
        <h3>Face {face} {FACE_NAMES[face]?.name ?? ""} <span className="note">— {FACE_NAMES[face]?.plain}</span></h3>
        <div className="row"><Addr a={`${page}.${face}`} />{pageData ? <Link href={`/page/${page}?face=${face}`}>open the page</Link> : null}</div>
      </div>
      <DraftForm override={sp.override ?? null} page={page} face={face} mode={mode} pageTitle={pageData?.title ?? null}
        live={live ? { body: live.body, source: live.source, from: live.resolved_from ?? "local" } : null}
        draft={draft ? { body: draft.body } : null} notes={notes} />
      <Raw data={{ page: pageData, history: hr.kind === "ok" ? hr.data : hr }} url={pr.url} />
    </>
  );
}
