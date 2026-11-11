// Drives the desk working side end to end against a REAL compute and saves app/screenshots/live-2x-*.png.
// Run the compute on a COPY of the books (it writes), the app with COMPUTE_URL pointing at it, then:
//   APP_URL=http://127.0.0.1:3010 node scripts/screenshots-live-2x.mjs
import { chromium } from "playwright-core";
import { mkdirSync } from "node:fs";
const base = process.env.APP_URL ?? "http://127.0.0.1:3010";
const PAGE = process.env.DEMO_PAGE ?? "10.11.21.1100";
const out = new URL("../screenshots/", import.meta.url).pathname;
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME ?? "/usr/bin/google-chrome", args: ["--no-sandbox"] });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
let i = 0;
const shot = async (name) => { const f = `${out}live-2x-${String(++i).padStart(2, "0")}-${name}.png`; await page.waitForTimeout(400); await page.screenshot({ path: f, fullPage: true }); console.log("saved", f); };
const go = async (p) => { await page.goto(base + p, { waitUntil: "networkidle" }); };
const as = async (who) => { await page.fill("#who", who); await page.waitForTimeout(150); };
// Approved: the screen reloads with ?done=<queue id> (result read back from the compute's queue). Rejected: a red box appears in place.
const topId = () => page.evaluate(async () => (await (await fetch("/api/compute/queue")).json()).proposals?.[0]?.id ?? null);
let last = null;
// Waits until the compute's queue has a new proposal, then for the screen to settle.
const sendAndWait = async (label) => {
  const before = await topId();
  await page.getByRole("button", { name: label }).click();
  for (let t = 0; t < 100 && (await topId()) === before; t++) await page.waitForTimeout(100);
  await page.waitForLoadState("networkidle");
  await page.waitForSelector(".ok-box, .no-box", { timeout: 10000 });
  await page.waitForTimeout(500);
  last = await page.evaluate(async () => (await (await fetch("/api/compute/queue")).json()).proposals?.[0]);
};
const result = async () => `${last?.id} ${last?.by} ${last?.status} ${(last?.reasons ?? []).map((r) => r.rule).join(",")}`;

// 1. Draft a new page (door + face 04, both drafts)
await go(`/draft?page=${PAGE}&face=04`);
await as("lead-prima");
await page.fill("#t", "clock");
await page.fill("#b", "## Clock\nsource: [01 / Clock]\nwhy: Long runs need a clear end so work does not drift.\n\nA clock that counts down and records when it ends.");
await shot("draft-new-page-form");
await sendAndWait("Send the draft"); console.log(" ->", await result());
await shot("draft-new-page-approved");

// 2. Seat under R2 with a trial reference
await go(`/seat?addr=${PAGE}.04`);
await as("prima");
await page.fill("#tr", "docs/trial/app-demo.md#clock-04");
await page.check("input[type=checkbox]");
await shot("seat-r2-form");
await sendAndWait("Seat it (make it live)"); console.log(" ->", await result());
await shot("seat-r2-approved");

// 3. Change the live face: copy -> note -> merge, then a refused seat while a note is open
await go(`/draft?page=${PAGE}&face=04`);
await sendAndWait("Copy into a draft"); console.log(" ->", await result());
await shot("change-1-copied");
await page.fill("#n", "Say that the clock can be paused, because long runs get interrupted.");
await sendAndWait("Add the note"); console.log(" ->", await result());
await shot("change-2-note-added");
await go(`/seat?addr=${PAGE}.04`);
await page.fill("#tr", "docs/trial/app-demo.md#clock-04-pause");
await page.check("input[type=checkbox]");
await sendAndWait("Seat it (make it live)"); console.log(" ->", await result());
await shot("seat-refused-open-note");
await go(`/draft?page=${PAGE}&face=04`);
await page.fill("#m", "## Clock\nsource: [01 / Clock]\nwhy: Long runs need a clear end so work does not drift.\n\nA clock that counts down, can be paused, and records when it ends.");
await sendAndWait("Merge it"); console.log(" ->", await result());
await shot("change-3-merged");
await go(`/seat?addr=${PAGE}.04`);
await page.fill("#tr", "docs/trial/app-demo.md#clock-04-pause");
await page.check("input[type=checkbox]");
await sendAndWait("Seat it (make it live)"); console.log(" ->", await result());
await shot("change-4-seated");

// 4. The work loop on face 05
await go(`/work?page=${PAGE}`);
await as("lead-prima");
await sendAndWait("Write the job as a draft"); console.log(" ->", await result());
await shot("loop-1-draft");
await sendAndWait("Mark ready to run (pack)"); console.log(" ->", await result());
await as("agent-7");
await sendAndWait("Claim it (open)"); console.log(" ->", await result());
await shot("loop-2-claimed");
await as("agent-8");
await page.fill("#ret", "## w01\nresult: done\nevidence: none");
await sendAndWait("Hand in the return"); console.log(" ->", await result());
await shot("loop-3-foreign-return-refused-axiom1");
await as("agent-7");
await page.fill("#ret", "## w01\nresult: done\nevidence: npm run build passed");
await sendAndWait("Hand in the return"); console.log(" ->", await result());
await sendAndWait("Start review"); console.log(" ->", await result());
await shot("loop-4-self-review-refused-S10");
await as("reviewer-trial");
await sendAndWait("Start review"); console.log(" ->", await result());
await page.selectOption("#oc", "passed");
await sendAndWait("Close with an outcome"); console.log(" ->", await result());
await shot("loop-5-closed-passed");

// 5. Queue, page, desk
await go("/queue"); await shot("queue");
await go("/queue?show=rejected"); await shot("queue-not-written");
await go(`/page/${PAGE}?face=04`); await shot("page-with-actions");
await go(`/history/${PAGE}`); await shot("history-lineage");
await go("/desk/10"); await shot("desk-10");
await go("/desk/00"); await shot("desk-00-kernel");
await go(`/export?addr=${PAGE}`); await shot("export-seq");
await browser.close();
