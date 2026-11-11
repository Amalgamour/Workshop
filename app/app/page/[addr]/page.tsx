import Link from "next/link";
import { get, withDraftReasons, type FaceView, type Links, type PageDetail } from "@/lib/compute";
import { Registry } from "@/components/Registry";
import { DraftState } from "@/components/DraftState";
import { SeqTools } from "@/components/SeqTools";
import { QueueResult } from "@/components/QueueResult";
import { Addr, Header, Hole, NotOk, Raw, SourceBadge, TailBadge } from "@/components/ui";
import { CardView } from "@/components/CardView";
import { FACE_NAMES, TAB_FACES, parseCards, torontoTime } from "@/lib/seq";

export const dynamic = "force-dynamic";

export default async function PageView({ params, searchParams }: { params: Promise<{ addr: string }>; searchParams: Promise<{ face?: string; done?: string }> }) {
  const { addr } = await params;
  const sp = await searchParams;
  const r = await get<PageDetail>(`/page/${addr}`);
  if (r.kind !== "ok") return <><Header title={<>Page <code>{addr}</code></>} /><NotOk r={r} what={`page ${addr}`} /></>;
  const p = await withDraftReasons(r.data);
  const groups = new Map<string, [string, FaceView][]>();
  for (const [k, v] of Object.entries(p.faces)) {
    const f = k.slice(0, 2);
    if (!groups.has(f)) groups.set(f, []);
    groups.get(f)!.push([k, v]);
  }
  const first = TAB_FACES.find((f) => groups.has(f)) ?? "04";
  const face = sp.face && /^\d\d$/.test(sp.face) ? sp.face : first;
  const stamp = p.faces["00"] ?? p.faces["00.draft"]; // compute: an unseated stamp is keyed 00.draft
  const links = await get<Links>(`/links/${addr}`);

  return (
    <>
      <Header title={<>{p.title ?? "7 no title"}</>} lede={<>A page. Its address: <Addr a={p.address} /></>} />

      <div className="panel">
        <h3>Face 00 · Registry <span className="note">(who this page is: stamp, type, registry — R10, R19)</span></h3>
        {stamp ? (
          <Registry face={stamp} pageAddr={addr} />
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

      <FacePanel addr={addr} face={face} entries={groups.get(face) ?? []} board={p.boards?.[face]} />

      <QueueResult id={sp.done} />
      <SeqTools addr={addr} />

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

function FacePanel({ addr, face, entries, board: derived }: { addr: string; face: string; entries: [string, FaceView][]; board?: { counter: string; tail: string | null }[] }) {
  const name = FACE_NAMES[face] ?? { name: `face ${face}`, plain: "" };
  if (entries.length === 0)
    return (
      <div className="panel">
        <h3>{face} {name.name} <span className="note">— {name.plain}</span></h3>
        <Actions addr={addr} face={face} hasDraft={entries.some(([k]) => k === `${face}.draft`)} />
        <Hole what={`face ${face} (${name.name})`} why={`Face ${face} is not written in this book, its shelf, its desk, or the kernel. A page needs face 00 and at least one content face (seqAddr 5.2), so this can be fine.`} traceHref={`/resolve?addr=${addr}.${face}`} />
      </div>
    );
  const seated = entries.find(([k]) => k === face);
  const draft = entries.find(([k]) => k === `${face}.draft`);
  const board = derived ?? entries.find(([k]) => k === `${face}.00`);
  const counters = entries.filter(([k]) => /^\d\d\.\d\d$/.test(k) && !k.endsWith(".00")).sort();
  const other = entries.filter(([k]) => k !== face && k !== `${face}.draft` && !/^\d\d\.\d\d$/.test(k));
  return (
    <div className="panel">
      <h3>{face} {name.name} <span className="note">— {name.plain}</span></h3>
        <Actions addr={addr} face={face} hasDraft={entries.some(([k]) => k === `${face}.draft`)} />
      {seated ? <FaceBlock addr={addr} k={seated[0]} v={seated[1]} label="Live face" /> : null}
      {draft ? <FaceBlock addr={addr} k={draft[0]} v={draft[1]} label="Draft (not active yet)" /> : null}
      {board || counters.length ? (
        <>
          <h3 style={{ marginTop: 18 }}>Board <span className="note">(every counter and its state; a view derived by the compute, R9)</span></h3>
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
      <DraftState state={v.state} tail={v.tail} why={v.why_draft} />
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

function Actions({ addr, face, hasDraft }: { addr: string; face: string; hasDraft: boolean }) {
  return (
    <div className="row" style={{ margin: "0 0 10px" }}>
      {face === "05" ? <Link className="tab" href={`/work?page=${addr}`}>Work the job loop →</Link> : <Link className="tab" href={`/draft?page=${addr}&face=${face}`}>{hasDraft ? "Work on the draft →" : "Draft this face →"}</Link>}
      {hasDraft ? <Link className="tab" href={`/seat?addr=${addr}.${face}`}>Seat the draft (R2) →</Link> : null}
    </div>
  );
}
