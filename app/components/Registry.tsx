import { Fragment } from "react";
import type { FaceView } from "@/lib/compute";
import { readFace00, STAMP_FIELDS } from "@/lib/face00";
import { CardView } from "@/components/CardView";
import { DraftState } from "@/components/DraftState";
import { SourceBadge, TailBadge } from "@/components/ui";

/** Face 00 as the registry location: 1 the stamp, 2 the type, 3 the registry (docs/spec/face00.md, DRAFT). */
export function Registry({ face, pageAddr }: { face: FaceView; pageAddr: string }) {
  const f = readFace00(face.body);
  const known = new Set(STAMP_FIELDS.map(([k]) => k));
  const extra = Object.entries(f.stamp).filter(([k]) => !known.has(k));
  return (
    <>
      <div className="badges"><SourceBadge from={face.resolved_from} source={face.source} /><TailBadge tail={face.tail ?? "seated"} /></div>
      <DraftState state={face.state} tail={face.tail} why={face.why_draft} />
      <div className="reg3">
        <section>
          <h4>1 · Stamp <span className="note">who and what the page is</span></h4>
          <dl className="fields">
            {STAMP_FIELDS.map(([k, plain]) => (
              <Fragment key={k}><dt title={plain}>{k}</dt><dd>{f.stamp[k] ?? <span className="note">— not written</span>}</dd></Fragment>
            ))}
            {extra.map(([k, v]) => <Fragment key={k}><dt>{k}</dt><dd>{v}</dd></Fragment>)}
          </dl>
        </section>
        <section>
          <h4>2 · Type <span className="note">what kind of page</span></h4>
          <p className="bigtype">{f.type ?? <span className="note">not written: the band head&apos;s default applies, else general</span>}</p>
        </section>
        <section>
          <h4>3 · Registry <span className="note">fields for this type</span></h4>
          {f.registry ? (
            <>
              <dl className="fields">{f.registry.fields.map(([k, v]) => <Fragment key={k}><dt>{k}</dt><dd>{v}</dd></Fragment>)}</dl>
              {f.registry.body ? <p className="body note">{f.registry.body}</p> : null}
            </>
          ) : <p className="note"><b>7</b> no Registry card yet. Each page type will have its own fields (R19).</p>}
        </section>
      </div>
      {f.other.map((c) => <CardView key={c.key} card={c} pageAddr={pageAddr} />)}
      <p className="note">Face 00 layout follows docs/spec/face00.md, which is a DRAFT for the Director.</p>
    </>
  );
}
