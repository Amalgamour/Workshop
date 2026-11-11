// Screenshots of the reader running on the REAL compute and real books -> app/screenshots/live-*.png
// Needs the compute (7700) and the app (3000) up. CHROME=/path to choose the browser.
import { createRequire } from "node:module";
import { mkdirSync } from "node:fs";
const require = createRequire(new URL("../app/package.json", import.meta.url));
const { chromium } = require("playwright-core");
const base = process.env.APP_URL ?? "http://127.0.0.1:3000";
const out = new URL("../app/screenshots/", import.meta.url).pathname;
mkdirSync(out, { recursive: true });
const shots = [
  ["live-01-library", "/"],
  ["live-02-kernel-seqaddr-law", "/page/00.00.00.0051?face=01"],
  ["live-03-kernel-workflow-loop", "/page/00.00.00.0057?face=01"],
  ["live-04-bob-brand-cards", "/page/10.11.21.1001?face=01"],
  ["live-05-local-override-why", "/page/10.11.21.0056?face=04"],
  ["live-06-dictionary-counters", "/page/10.11.21.0012?face=03"],
  ["live-07-card-matching-bob", "/cards?title=bob&from=10.11.21.1001"],
  ["live-08-links", "/links/10.11.21.1001"],
  ["live-09-history", "/history/10.11.21.1001"],
  ["live-10-resolve-trace", "/resolve?addr=10.11.21.0056.01"],
  ["live-11-resolve-missing", "/resolve?addr=10.11.21.1777.00"],
  ["live-12-word-lookup-bob", "/words"],
];
const browser = await chromium.launch({ executablePath: process.env.CHROME ?? "/usr/bin/google-chrome", args: ["--no-sandbox"] });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
for (const [name, path] of shots) {
  await page.goto(base + path, { waitUntil: "networkidle" });
  if (name === "live-12-word-lookup-bob") {
    await page.fill("textarea", "My name is Bob and I like cats");
    await page.waitForSelector("mark.brand", { timeout: 8000 }).catch(() => console.log("no brand lit up"));
    await page.waitForTimeout(1200);
  }
  await page.screenshot({ path: `${out}${name}.png`, fullPage: true });
  console.log("saved", name);
}
await browser.close();
