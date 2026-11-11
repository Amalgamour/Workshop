import Link from "next/link";
import { get, type BookDetail, type BookSummary } from "@/lib/compute";
import { Header, NotOk, Raw } from "@/components/ui";
import { FACE_NAMES } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function Library() {
  const r = await get<BookSummary[]>("/books");
  if (r.kind !== "ok") return <><Header title="Library" /><NotOk r={r} what="the library" /></>;
  const books = r.data;
  const details = await Promise.all(books.map((b) => get<BookDetail>(`/book/${b.address}`)));
  const byAddr = new Map(books.map((b, i) => [b.address, { ...b, detail: details[i].kind === "ok" ? details[i].data : null }]));

  // desk DD -> shelf DD.SS -> book DD.SS.BB. A container's own book is DD.00.00 or DD.SS.00 (seqAddr.md 1.4).
  const desks = new Map<string, Map<string, string[]>>();
  for (const b of books) {
    const [d, s, k] = b.address.split(".");
    if (!desks.has(d)) desks.set(d, new Map());
    const shelves = desks.get(d)!;
    if (s === "00" && k === "00") continue;
    if (!shelves.has(s)) shelves.set(s, []);
    if (k !== "00") shelves.get(s)!.push(b.address);
  }
  const titleOf = (a: string) => byAddr.get(a)?.title;

  return (
    <>
      <Header title="Library" lede={<>Every desk, shelf and book the compute holds. A desk holds shelves, a shelf holds books, a book holds pages. Click a page to read its faces.</>} />
      <div className="tree panel">
        <ul>
          {[...desks.entries()].sort().map(([d, shelves]) => (
            <li key={d}>
              <span className="kind">Desk</span> <strong><code>{d}</code> {titleOf(`${d}.00.00`) ?? <em className="note">7 no title (its own book is missing)</em>}</strong>
              {d === "00" ? <span className="note"> — the kernel: base rules every book inherits</span> : null}
              <BookPages a={`${d}.00.00`} detail={byAddr.get(`${d}.00.00`)?.detail} label="desk's own book" />
              <ul>
                {[...shelves.entries()].sort().map(([s, bks]) => (
                  <li key={s}>
                    <span className="kind">Shelf</span> <strong><code>{d}.{s}</code> {s === "00" ? <em className="note">desk books (no shelf)</em> : titleOf(`${d}.${s}.00`) ?? <em className="note">7 no title</em>}</strong>
                    {s !== "00" ? <BookPages a={`${d}.${s}.00`} detail={byAddr.get(`${d}.${s}.00`)?.detail} label="shelf's own book" /> : null}
                    <ul>
                      {bks.sort().map((ba) => (
                        <li key={ba}>
                          <span className="kind">Book</span> <Link href={`/book/${ba}`}><strong><code>{ba}</code> {titleOf(ba) ?? "7 no title"}</strong></Link>
                          <BookPages a={ba} detail={byAddr.get(ba)?.detail} />
                        </li>
                      ))}
                    </ul>
                  </li>
                ))}
              </ul>
            </li>
          ))}
        </ul>
      </div>
      <Raw data={books} url={r.url} />
    </>
  );
}

function BookPages({ a, detail, label }: { a: string; detail?: BookDetail | null; label?: string }) {
  if (!detail) return null;
  return (
    <ul>
      {label ? <li className="note">{label}: <Link href={`/book/${a}`}><code>{a}</code></Link></li> : null}
      {detail.pages.map((p) => (
        <li key={p.page}>
          <span className="kind">Page</span> <Link href={`/page/${a}.${p.page}`}><code>{p.page}</code> {p.title ?? <em>no title</em>}</Link>
          {p.faces.map((f) => <span key={f} className="chip" title={FACE_NAMES[f]?.plain}>{f} {FACE_NAMES[f]?.name ?? ""}</span>)}
        </li>
      ))}
    </ul>
  );
}
