// Takes screenshots of each screen into app/screenshots/. Needs the app (port 3000) and a compute (or the mock) running.
// CHROME=/path/to/chrome to choose the browser.
import { chromium } from "playwright-core";
import { mkdirSync } from "node:fs";
const base = process.env.APP_URL ?? "http://127.0.0.1:3000";
const out = new URL("../screenshots/", import.meta.url).pathname;
mkdirSync(out, { recursive: true });
const shots = [
  ["01-library", "/"],
  ["02-page-faces-law", "/page/10.11.21.1014?face=01"],
  ["03-page-tasks-board", "/page/10.11.21.1014?face=05"],
  ["04-page-inherited-why", "/page/10.11.21.0020?face=04"],
  ["05-page-missing-hole", "/page/10.11.21.1014?face=02"],
  ["06-page-draft", "/page/10.11.21.1523?face=01"],
  ["07-card-matching", "/cards?title=retry-policy&from=10.11.21.1014"],
  ["08-links-map", "/links/10.11.21.1014"],
  ["09-history", "/history/10.11.21.1014"],
  ["10-resolve-trace", "/resolve?addr=10.11.21.0021.04"],
  ["11-resolve-missing", "/resolve?addr=10.11.21.1777.00"],
  ["12-word-lookup", "/words"],
];
const browser = await chromium.launch({ executablePath: process.env.CHROME ?? "/usr/bin/google-chrome", args: ["--no-sandbox"] });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
for (const [name, path] of shots) {
  await page.goto(base + path, { waitUntil: "networkidle" });
  if (name === "12-word-lookup") { await page.waitForSelector("mark.brand", { timeout: 8000 }).catch(() => {}); await page.click("mark.brand >> nth=1").catch(() => {}); await page.waitForTimeout(800); }
  await page.screenshot({ path: `${out}${name}.png`, fullPage: true });
  console.log("saved", name);
}
await browser.close();
