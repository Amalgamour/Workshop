import Link from "next/link";
import { COMPUTE_URL } from "@/lib/compute";
import { Addr, Header, Hole, Raw } from "@/components/ui";

export const dynamic = "force-dynamic";

export default async function Export({ searchParams }: { searchParams: Promise<{ addr?: string }> }) {
  const { addr } = await searchParams;
  const head = <Header title="Export page as .seq" lede="A .seq file holds one page with all its faces. The book stays the real copy; the .seq file is a view of it (Director ruling R3). Bringing one back in goes through the normal queue." />;
  if (!addr || !/^\d\d\.\d\d\.\d\d\.\d{4}$/.test(addr))
    return <>{head}<form className="panel" action="/export"><div className="field"><label>Page address <small>(desk.shelf.book.page)</small></label><input className="big mono" name="addr" defaultValue={addr ?? ""} /></div><button className="go">Show it</button></form></>;
  const url = `${COMPUTE_URL}/page.seq?addr=${addr}`;
  let status = 0, text = "", json: unknown = null, name = `${addr}.seq`;
  try {
    const res = await fetch(url, { cache: "no-store" });
    status = res.status; text = await res.text();
    try { json = JSON.parse(text); } catch { /* plain .seq text */ }
    const cd = res.headers.get("content-disposition"); const m = cd ? /filename="([^"]+)"/.exec(cd) : null; if (m) name = m[1];
  } catch (err) { text = String((err as Error).message); }
  const j = json as { error?: string; axiom?: string; detail?: string; rule?: string } | null;
  return (
    <>
      {head}
      <div className="panel row"><Addr a={addr} /> <Link href={`/page/${addr}`}>open the page</Link></div>
      {status === 200 && !j ? (
        <div className="panel">
          <div className="row"><h3 style={{ margin: 0 }}>{name}</h3><a className="go" style={{ textDecoration: "none", padding: "10px 18px", borderRadius: 12, background: "var(--accent)", color: "#fff" }} href={`/api/seq?addr=${addr}`} download={name}>Download {name}</a></div>
          <p className="note">This is exactly what the compute exported. Plain characters only (R4).</p>
          <pre className="body mono card" style={{ fontSize: "0.85rem" }}>{text}</pre>
        </div>
      ) : j?.error === "route" ? (
        <Hole what="the .seq export in this compute" why="This compute does not serve GET /page.seq yet. The route is proposed in CONTRACT.md (SEQPAGE addendum) and waits for the compute lane. Nothing is faked here." />
      ) : j?.error === "missing" ? (
        <Hole what={`page ${addr}`} why={j.detail ?? "The page has no entries."} traceHref={`/resolve?addr=${addr}.00`} />
      ) : (
        <div className="no-box"><div className="big-word">✗ Could not export</div><p>{j?.detail ?? text}</p>{j?.rule ? <span className="badge seated">rule <b>{j.rule}</b></span> : null}</div>
      )}
      <Raw data={{ status, body: j ?? text }} url={url} />
    </>
  );
}
