import "./globals.css";
import Link from "next/link";
import type { Metadata } from "next";
import { WhoAmI } from "@/components/WhoAmI";

export const metadata: Metadata = { title: "Workshop reader", description: "Read every face of every page. Trust, but verify." };

const NAV = [
  ["/ask", "Ask", "a question in your words"],
  ["/", "Library", "desks, shelves, books"],
  ["/words", "Word lookup", "your special words"],
  ["/cards", "Card matching", "one card on every face"],
  ["/resolve", "Resolve trace", "how an address was found"],
] as const;
const WORK = [
  ["/desk", "Desk", "one desk: door, shelves, jobs"],
  ["/draft", "Draft a face", "write or change, as a draft"],
  ["/work", "Work loop", "jobs: draft → … → closed"],
  ["/seat", "Seat a face", "make a draft live (R2)"],
  ["/queue", "Queue", "every proposal and its result"],
] as const;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <aside className="side">
            <h1>Workshop</h1>
            <p>Read what the compute holds. Propose changes; the compute checks and writes.</p>
            <nav><div className="navhead">Read</div>{NAV.map(([href, name, small]) => <Link key={href} href={href}>{name}<small>{small}</small></Link>)}
              <div className="navhead">Work</div>{WORK.map(([href, name, small]) => <Link key={href} href={href}>{name}<small>{small}</small></Link>)}</nav>
            <WhoAmI />
          </aside>
          <main className="main">{children}</main>
        </div>
      </body>
    </html>
  );
}
