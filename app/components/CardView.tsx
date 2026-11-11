import Link from "next/link";
import { Fragment } from "react";
import type { Card } from "@/lib/seq";

export function CardView({ card, pageAddr }: { card: Card; pageAddr?: string }) {
  return (
    <div className="card" id={card.key}>
      <h4>
        <Link href={`/cards?title=${encodeURIComponent(card.key)}${pageAddr ? `&from=${pageAddr}` : ""}`} title="See this same card on other faces">{card.title}</Link>
        <span className="chip">card key: {card.key}</span>
      </h4>
      {card.fields.length ? (
        <dl className="fields">
          {card.fields.map(([k, v], i) => (<Fragment key={i}><dt>{k}</dt><dd>{v}</dd></Fragment>))}
        </dl>
      ) : null}
      {card.body ? <p className="body">{card.body}</p> : null}
    </div>
  );
}
