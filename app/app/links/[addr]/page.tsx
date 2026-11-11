import Link from "next/link";
import { get, type Links, type PageDetail } from "@/lib/compute";
import { Addr, Header, Hole, NotOk, Raw } from "@/components/ui";
import { CardView } from "@/components/CardView";
import { parseCards } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function LinksView({ params }: { params: Promise<{ addr: string }> }) {
  const { addr } = await params;
  const [r, pr] = await Promise.all([get<Links>(`/links/${addr}`), get<PageDetail>(`/page/${addr}`)]);
  const title = pr.kind === "ok" ? pr.data.title : null;
  const head = <Header title={<>Links and map: <Link href={`/page/${addr}`}>{title ?? addr}</Link></>} lede={<>Axiom 8: a connection is lawful only when it is written, linked both ways. <Addr a={addr} /></>} />;
  if (r.kind !== "ok") return <>{head}<NotOk r={r} what={`links for ${addr}`} /></>;
  const l = r.data;
  const missing = new Set(l.missing);
  const back = new Set(l.back);
  const map = pr.kind === "ok" ? pr.data.faces["08"] : undefined;
  return (
    <>
      {head}
      <div className="cols">
        <div className="panel">
          <h3>Links out <span className="note">(this page points to)</span></h3>
          {l.forward.length === 0 ? <p className="note">None written.</p> : null}
          <ul>{l.forward.map((a) => (
            <li key={a} style={{ marginBottom: 8 }}>
              <Addr a={a} link={!missing.has(a)} />{" "}
              {missing.has(a) ? <span className="badge missing"><b>7.8</b> cannot be opened</span> : back.has(a) ? <span className="badge local">links back</span> : (l.one_way ?? []).includes(a) ? <span className="badge tail"><b>one-way</b> no back-link</span> : null}
            </li>
          ))}</ul>
        </div>
        <div className="panel">
          <h3>Links in <span className="note">(pages that point here)</span></h3>
          {l.back.length === 0 ? <p className="note">None found.</p> : null}
          <ul>{l.back.map((a) => <li key={a} style={{ marginBottom: 8 }}><Addr a={a} link /></li>)}</ul>
        </div>
      </div>
      {l.missing.length ? (
        <div className="panel">
          <h3>Missing links</h3>
          {l.missing.map((a) => <div key={a} style={{ marginBottom: 10 }}><Hole what={`the page ${a}`} why="Face 08 points here, but nothing is written there. A connection that cannot be opened is missing (7.8). Do not repair it from memory." traceHref={`/resolve?addr=${a}.00`} /></div>)}
        </div>
      ) : null}
      {(l.one_way ?? []).length ? <p className="note">One-way: the target exists but its face 08 does not point back. Spec 7: a one-way link is invalid. Raised, not fixed.</p> : null}
      <div className="panel">
        <h3>Face 08 Map, as written</h3>
        {map ? parseCards(map.body).cards.map((c) => <CardView key={c.key} card={c} pageAddr={addr} />) : <Hole what="face 08 (Map)" />}
      </div>
      <Raw data={l} url={r.url} />
    </>
  );
}
