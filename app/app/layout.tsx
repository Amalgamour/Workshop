import type { ReactNode } from "react";
import "./globals.css";

export const metadata = {
  title: "Workshop",
  description: "Read one face by asking the compute.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
