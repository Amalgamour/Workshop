import Link from "next/link";
import { get, type CardHit } from "@/lib/compute";
import { Addr, Header, Hole, NotOk, Raw, TailBadge } from "@/components/ui";
import { FACE_NAMES } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function Cards({ searchParams }: { searchParams: Promise<{ title?: string; from?: string }> }) {
  const { title, from } = await searchParams;
  const form = (
    <form className="row" action="/cards" style={{ marginBottom: 22 }}>
      <input className="big" style={{ flex: 1 }} name="title" defaultValue={title ?? ""} placeholder="Card title, for example: Retry Policy" aria-label="card title" />
      <button className="go">Match</button>
    </form>
  );
  const head = <Header title="Card matching" lede="The same card key on two faces is the same card. Type a card title, or click a card title on any page, to see it on every face that has it." />;
  if (!title) return <>{head}{form}</>;
  const r = await get<CardHit[]>(`/cards?title=${encodeURIComponent(title)}`);
  if (r.kind !== "ok") return <>{head}{form}<NotOk r={r} what={`card ${title}`} /></>;
  const byPage = new Map<string, CardHit[]>();
  for (const c of r.data) { const p = c.face.split(".").slice(0, 4).join("."); if (!byPage.has(p)) byPage.set(p, []); byPage.get(p)!.push(c); }
  const order = from && byPage.has(from) ? [from, ...[...byPage.keys()].filter((k) => k !== from)] : [...byPage.keys()];
  return (
    <>
      {head}{form}
      {r.data.length === 0 ? <Hole what={`a card called "${title}"`} why="No face holds a card with this key." /> : null}
      {order.map((p) => {
        const hits = byPage.get(p)!;
        const faces = new Set(hits.map((h) => h.face.split(".")[4]));
        const needs04 = (faces.has("01") || faces.has("02")) && !faces.has("04");
        return (
          <div className="panel" key={p}>
            <h3><Link href={`/page/${p}`}>{hits[0].page_title ?? "page"}</Link> <span className="note">{p === from ? "(the page you came from)" : ""}</span></h3>
            <Addr a={p} />
            <div className="cols" style={{ marginTop: 14 }}>
              {hits.map((h) => {
                const f = h.face.split(".").slice(4).join(".");
                const fn = f.slice(0, 2);
                return (
                  <div className="card" key={h.address} style={{ margin: 0 }}>
                    <h4><Link href={`/page/${p}?face=${fn}#${h.key}`}>Face {f} {FACE_NAMES[fn]?.name ?? ""}</Link></h4>
                    <div className="badges"><TailBadge tail={h.tail ?? "seated"} /></div>
                    <dl className="fields">{Object.entries(h.fields).map(([k, v]) => <div key={k} style={{ display: "contents" }}><dt>{k}</dt><dd>{v}</dd></div>)}</dl>
                    <p className="body">{h.body}</p>
                  </div>
                );
              })}
            </div>
            {needs04 ? <div style={{ marginTop: 12 }}><Hole what="the face 04 why for this card" why="Every 01 or 02 card needs a 04 card with the same key on its page (seqAddr 5.4). It may be inherited; open the page to check." /></div> : null}
          </div>
        );
      })}
      <Raw data={r.data} url={r.url} />
    </>
  );
}
