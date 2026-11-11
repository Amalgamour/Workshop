import Link from "next/link";
import { Fragment } from "react";
import { get, type FaceView, type Links, type PageDetail } from "@/lib/compute";
import { Addr, Header, Hole, NotOk, Raw, SourceBadge, TailBadge } from "@/components/ui";
import { CardView } from "@/components/CardView";
import { FACE_NAMES, TAB_FACES, frontMatter, parseCards, torontoTime } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function PageView({ params, searchParams }: { params: Promise<{ addr: string }>; searchParams: Promise<{ face?: string }> }) {
  const { addr } = await params;
  const sp = await searchParams;
  const r = await get<PageDetail>(`/page/${addr}`);
  if (r.kind !== "ok") return <><Header title={<>Page <code>{addr}</code></>} /><NotOk r={r} what={`page ${addr}`} /></>;
  const p = r.data;
  const groups = new Map<string, [string, FaceView][]>();
  for (const [k, v] of Object.entries(p.faces)) {
    const f = k.slice(0, 2);
    if (!groups.has(f)) groups.set(f, []);
    groups.get(f)!.push([k, v]);
  }
  const first = TAB_FACES.find((f) => groups.has(f)) ?? "04";
  const face = sp.face && /^\d\d$/.test(sp.face) ? sp.face : first;
  const stamp = p.faces["00"];
  const sf = frontMatter(stamp?.body);
  const links = await get<Links>(`/links/${addr}`);

  return (
    <>
      <Header title={<>{p.title ?? "7 no title"}</>} lede={<>A page. Its address: <Addr a={p.address} /></>} />

      <div className="panel">
        <h3>Stamp <span className="note">(face 00: who this page is)</span></h3>
        {stamp ? (
          <>
            <div className="badges"><SourceBadge from={stamp.resolved_from} source={stamp.source} />{stamp.tail ? <TailBadge tail={stamp.tail} /> : null}</div>
            <dl className="fields">{Object.entries(sf).map(([k, v]) => <Fragment key={k}><dt>{k}</dt><dd>{v}</dd></Fragment>)}</dl>
          </>
        ) : <Hole what="the page stamp (face 00)" why="A page needs face 00. This is a defect, raised to you." />}
        <div className="row note">
          <Link href={`/history/${addr}`}>History of this page</Link>·
          <Link href={`/links/${addr}`}>Links and map</Link>·
          <Link href={`/resolve?addr=${addr}.${face}`}>How face {face} was found</Link>
          {links.kind === "ok" ? <span>· {links.data.forward.length} links out, {links.data.back.length} links in{links.data.missing.length ? <>, <b style={{ color: "var(--hole)" }}>{links.data.missing.length} missing</b></> : null}</span> : null}
        </div>
      </div>

      <nav className="tabs" aria-label="faces">
        {TAB_FACES.map((f) => (
          <Link key={f} href={`/page/${addr}?face=${f}`} className={`tab ${f === face ? "on" : ""} ${groups.has(f) ? "" : "empty"}`}>
            {f} {FACE_NAMES[f].name}<small>{groups.has(f) ? sourceSummary(groups.get(f)!) : "missing"}</small>
          </Link>
        ))}
      </nav>

      <FacePanel addr={addr} face={face} entries={groups.get(face) ?? []} />

      {p.inherited.length ? (
        <div className="panel">
          <h3>Inherited here</h3>
          <p className="note">This book does not write these itself. They come from above it.</p>
          <ul>{p.inherited.map((a) => <li key={a}><Addr a={a} link /></li>)}</ul>
        </div>
      ) : null}
      <Raw data={p} url={r.url} />
    </>
  );
}

function sourceSummary(e: [string, FaceView][]) {
  const s = new Set(e.map(([, v]) => v.resolved_from ?? "local"));
  return [...s].join(" + ");
}

function FacePanel({ addr, face, entries }: { addr: string; face: string; entries: [string, FaceView][] }) {
  const name = FACE_NAMES[face] ?? { name: `face ${face}`, plain: "" };
  if (entries.length === 0)
    return (
      <div className="panel">
        <h3>{face} {name.name} <span className="note">— {name.plain}</span></h3>
        <Hole what={`face ${face} (${name.name})`} why={`Face ${face} is not written in this book, its shelf, its desk, or the kernel. A page needs face 00 and at least one content face (seqAddr 5.2), so this can be fine.`} traceHref={`/resolve?addr=${addr}.${face}`} />
      </div>
    );
  const seated = entries.find(([k]) => k === face);
  const draft = entries.find(([k]) => k === `${face}.draft`);
  const board = entries.find(([k]) => k === `${face}.00`);
  const counters = entries.filter(([k]) => /^\d\d\.\d\d$/.test(k) && !k.endsWith(".00")).sort();
  const other = entries.filter(([k]) => k !== face && k !== `${face}.draft` && !/^\d\d\.\d\d$/.test(k));
  return (
    <div className="panel">
      <h3>{face} {name.name} <span className="note">— {name.plain}</span></h3>
      {seated ? <FaceBlock addr={addr} k={seated[0]} v={seated[1]} label="Live face" /> : null}
      {draft ? <FaceBlock addr={addr} k={draft[0]} v={draft[1]} label="Draft (not active yet)" /> : null}
      {board || counters.length ? (
        <>
          <h3 style={{ marginTop: 18 }}>Board <span className="note">(face {face}.00: every counter and its state)</span></h3>
          {!board ? <Hole what={`the board ${face}.00`} why="Counters are written but there is no board. A counter without a board is invalid (seqAddr 5.7). Raised to you." /> : null}
          <table className="log">
            <thead><tr><th>Counter</th><th>State</th><th>First card</th></tr></thead>
            <tbody>{counters.map(([k, v]) => <tr key={k}><td><a href={`#c-${k}`}><code>{k}</code></a></td><td><TailBadge tail={v.tail ?? "closed"} /></td><td>{parseCards(v.body).cards[0]?.title ?? ""}</td></tr>)}</tbody>
          </table>
          {counters.map(([k, v]) => <div key={k} id={`c-${k}`}><FaceBlock addr={addr} k={k} v={v} label={`Counter ${k}`} /></div>)}
        </>
      ) : null}
      {other.map(([k, v]) => <FaceBlock key={k} addr={addr} k={k} v={v} label={k} />)}
    </div>
  );
}

function FaceBlock({ addr, k, v, label }: { addr: string; k: string; v: FaceView; label: string }) {
  const { intro, cards } = parseCards(v.body);
  return (
    <section style={{ marginTop: 10 }}>
      <div className="row"><strong>{label}</strong> <code className="note">{addr}.{k}</code></div>
      <div className="badges">
        <SourceBadge from={v.resolved_from} source={v.source} />
        <TailBadge tail={v.tail ?? (/\.\d\d$/.test(k) ? "closed" : "seated")} />
        {v.by ? <span className="badge seated">by <b>{v.by}</b>{v.at ? ` · ${torontoTime(v.at)}` : ""}{v.n ? ` · entry ${v.n}` : ""}</span> : null}
      </div>
      {intro ? <p className="body">{intro}</p> : null}
      {cards.map((c) => <CardView key={c.key} card={c} pageAddr={addr} />)}
      {!intro && cards.length === 0 ? <p className="note">Empty body.</p> : null}
    </section>
  );
}
