import Link from "next/link";
import { get, type BookDetail, type BookSummary, type PageDetail } from "@/lib/compute";
import { Addr, Header, Hole, NotOk, Raw, SourceBadge, TailBadge } from "@/components/ui";
import { CardView } from "@/components/CardView";
import { FACE_NAMES, frontMatter, parseCards } from "@/lib/seq";
import { LOOP } from "@/lib/rules";

export const dynamic = "force-dynamic";

export default async function Desk({ params }: { params: Promise<{ dd: string }> }) {
  const { dd } = await params;
  const r = await get<BookSummary[]>("/books");
  const head = <Header title={<>Desk <code>{dd}</code></>} />;
  if (!/^\d\d$/.test(dd)) return <>{head}<Hole what={`desk ${dd}`} why="A desk number is two digits." /></>;
  if (r.kind !== "ok") return <>{head}<NotOk r={r} what="the books" /></>;
  const mine = r.data.filter((b) => b.address.startsWith(`${dd}.`));
  const deskBook = mine.find((b) => b.address === `${dd}.00.00`);
  const [door, ...details] = await Promise.all([get<PageDetail>(`/page/${dd}.00.00.0000`), ...mine.map((b) => get<BookDetail>(`/book/${b.address}`))]);
  const det = new Map(mine.map((b, i) => [b.address, details[i].kind === "ok" ? details[i].data : null]));
  const shelves = [...new Set(mine.map((b) => b.address.split(".")[1]).filter((s) => s !== "00"))].sort();
  const deskBooks = mine.filter((b) => b.address.split(".")[1] === "00" && b.address !== `${dd}.00.00`);

  // Jobs on this desk: every page with a face 05, read through the compute.
  const jobPages = mine.flatMap((b) => (det.get(b.address)?.pages ?? []).filter((p) => p.faces.includes("05")).map((p) => `${b.address}.${p.page}`));
  const jp = await Promise.all(jobPages.map((p) => get<PageDetail>(`/page/${p}`)));
  const jobs = jp.flatMap((x, i) => x.kind !== "ok" ? [] : Object.entries(x.data.faces).filter(([k]) => /^05\.\d\d$/.test(k) && k !== "05.00").map(([k, v]) => ({ page: jobPages[i], title: x.data.title, nn: k, tail: v.tail ?? "closed", card: parseCards(v.body).cards[0]?.title ?? "" })));

  const doorData = door.kind === "ok" ? door.data : null;
  const stamp = doorData ? doorData.faces["00"] ?? doorData.faces["00.draft"] : undefined;
  return (
    <>
      <Header title={<>Desk <code>{dd}</code> {deskBook?.title ?? ""}</>} lede={<>A desk is the highest working space. It has a door (its zero sequence: <code>{dd}.00.00.0000</code>), shelves, and books. {dd === "00" ? "Desk 00 is the kernel." : null}</>} />

      <div className="panel">
        <h3>The door <span className="note">(the full-zero sequence: who this desk is; Director ruling R1)</span></h3>
        <Addr a={`${dd}.00.00.0000`} link />
        {doorData ? (
          <>
            {stamp ? <div className="badges"><SourceBadge from={stamp.resolved_from} source={stamp.source} /><TailBadge tail={stamp.tail ?? "seated"} />{Object.entries(frontMatter(stamp.body)).map(([k, v]) => <span key={k} className="chip">{k}: {v}</span>)}</div> : null}
            {Object.entries(doorData.faces).filter(([k]) => !k.startsWith("00")).map(([k, v]) => (
              <div key={k}><strong>Face {k} {FACE_NAMES[k.slice(0, 2)]?.name}</strong> <TailBadge tail={v.tail ?? "seated"} />{parseCards(v.body).cards.map((c) => <CardView key={c.key} card={c} pageAddr={`${dd}.00.00.0000`} />)}</div>
            ))}
          </>
        ) : <Hole what={`the desk's door ${dd}.00.00.0000`} why="A container needs its door to be legal (seqAddr 8). Raised to you." />}
      </div>

      <div className="panel tree">
        <h3>Shelves and books</h3>
        <ul>
          {shelves.map((s) => (
            <li key={s}><span className="kind">Shelf</span> <strong><code>{dd}.{s}</code> {mine.find((b) => b.address === `${dd}.${s}.00`)?.title ?? <em className="note">7 no door book</em>}</strong>
              <ul>{mine.filter((b) => b.address.startsWith(`${dd}.${s}.`)).map((b) => (
                <li key={b.address}><span className="kind">{b.address.endsWith(".00") ? "Door" : "Book"}</span> <Link href={`/book/${b.address}`}><code>{b.address}</code> {b.title ?? "7 no title"}</Link> <span className="note">{b.pages} page(s)</span>
                  {(det.get(b.address)?.warnings ?? []).map((w) => <div key={w} className="note">⚠ {w}</div>)}</li>
              ))}</ul>
            </li>
          ))}
          {deskBooks.length ? <li><span className="kind">Desk books</span> <em className="note">owned by the desk, no shelf</em><ul>{deskBooks.map((b) => <li key={b.address}><Link href={`/book/${b.address}`}><code>{b.address}</code> {b.title}</Link></li>)}</ul></li> : null}
          {shelves.length === 0 && deskBooks.length === 0 ? <li className="note">No shelves yet.</li> : null}
        </ul>
      </div>

      <div className="panel">
        <h3>Jobs on this desk <span className="note">(every face 05 counter in its books)</span></h3>
        {jobs.length === 0 ? <p className="note">No jobs yet. Start one on any page with <Link href="/work">Work loop</Link>.</p> : (
          <div className="board">{LOOP.map((l) => (
            <div className="col" key={l.tail}><h4>{l.tail}</h4>
              {jobs.filter((j) => j.tail === l.tail).map((j) => <Link key={j.page + j.nn} href={`/work?page=${j.page}&job=${j.nn.slice(3)}`} style={{ textDecoration: "none", color: "inherit" }}><div className="job"><b>{j.title}</b> {j.nn}<div className="note">{j.card}</div></div></Link>)}
            </div>
          ))}</div>
        )}
      </div>
      <Raw data={{ books: mine, door: doorData, jobs }} url={r.url} />
    </>
  );
}
