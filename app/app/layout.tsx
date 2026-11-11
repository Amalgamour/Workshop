import "./globals.css";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = { title: "Workshop reader", description: "Read every face of every page. Trust, but verify." };

const NAV = [
  ["/", "Library", "desks, shelves, books"],
  ["/words", "Word lookup", "your special words"],
  ["/cards", "Card matching", "one card on every face"],
  ["/resolve", "Resolve trace", "how an address was found"],
] as const;

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="shell">
          <aside className="side">
            <h1>Workshop</h1>
            <p>The reader. It shows what the compute holds. It changes nothing.</p>
            <nav>{NAV.map(([href, name, small]) => <Link key={href} href={href}>{name}<small>{small}</small></Link>)}</nav>
          </aside>
          <main className="main">{children}</main>
        </div>
      </body>
    </html>
  );
}
