// Round 3 screens against a REAL compute and saves app/screenshots/live-3x-*.png.
// Run the compute on a COPY of the books (it writes) with demo tokens in that copy's books/.identities,
// the app with COMPUTE_URL pointing at it, then:
//   APP_URL=http://127.0.0.1:3020 COMPUTE=http://127.0.0.1:7720 TOKEN=tok-app-demo node scripts/screenshots-live-3x.mjs
import { chromium } from "playwright-core";
import { mkdirSync } from "node:fs";
const base = process.env.APP_URL ?? "http://127.0.0.1:3020";
const compute = process.env.COMPUTE ?? "http://127.0.0.1:7720";
const TOKEN = process.env.TOKEN ?? "tok-app-demo";
const PAGE = process.env.DEMO_PAGE ?? "10.11.21.1100";
const out = new URL("../screenshots/", import.meta.url).pathname;
mkdirSync(out, { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROME ?? "/usr/bin/google-chrome", args: ["--no-sandbox"] });
const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
let i = 0;
const shot = async (name) => { const f = `${out}live-3x-${String(++i).padStart(2, "0")}-${name}.png`; await page.waitForTimeout(500); await page.screenshot({ path: f, fullPage: true }); console.log("saved", f); };
const go = async (p) => { await page.goto(base + p, { waitUntil: "networkidle" }); };
const topId = () => page.evaluate(async () => (await (await fetch("/api/compute/queue")).json()).proposals?.[0]?.id ?? null);
// Click, wait for the compute's queue to move (a refused identity is not queued, so give up after 3 s), then for a result box.
const send = async (label) => {
  const before = await topId();
  await page.getByRole("button", { name: label }).click();
  for (let t = 0; t < 30 && (await topId()) === before; t++) await page.waitForTimeout(100);
  await page.waitForLoadState("networkidle");
  await page.waitForSelector(".ok-box, .no-box", { timeout: 10000 });
  await page.waitForTimeout(600);
  const top = await page.evaluate(async () => (await (await fetch("/api/compute/queue")).json()).proposals?.[0]);
  console.log(" ->", top?.id === before ? "(not queued)" : `${top?.id} ${top?.by} ${top?.status} ${(top?.reasons ?? []).map((r) => r.rule).join(",")}`);
};
const signIn = async (tok) => {
  await page.fill("#tok", tok);
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForSelector(".who-state", { timeout: 5000 });
  await page.waitForTimeout(800);
};

// 1-2. Ask: pieces, then the probe (no sign-in needed to ask)
await go(`/ask?q=${encodeURIComponent("what is my name")}`);
await page.waitForSelector("h3:has-text('What I found'), h3:has-text('Nothing fits')");
await shot("ask-pieces");
await go(`/ask?q=${encodeURIComponent("tell me about the weather")}`);
await page.waitForSelector("h3:has-text('Nothing fits')");
await shot("ask-probe");

// 3-4. Sign in: a token the compute does not know (401), then the demo token
await go("/ask");
await signIn("not-a-real-token-123");
await shot("signin-401-unknown-token");
await signIn(TOKEN);
await shot("signin-accepted");

// 5-6. Teach a new phrasing, then ask it again
await go(`/ask?q=${encodeURIComponent("what am i called")}`);
await page.waitForSelector("h3:has-text('What I found'), h3:has-text('Nothing fits')");
await shot("ask-link-form");
await send("Link this phrasing");
await page.getByRole("button", { name: "Ask", exact: true }).click();
await page.waitForSelector("h3:has-text('What I found')");
await shot("ask-linked-then-found");

// 7-8. Draft a page with a reason, then see the draft and why on the page view
await go(`/draft?page=${PAGE}&face=04`);
await page.fill("#t", "clock");
await page.fill("#b", "## Clock\nsource: [01 / Clock]\nwhy: Long runs need a clear end so work does not drift.\n\nA clock that counts down and records when it ends.");
await page.fill("#why", "waiting for a trial before it goes live");
await send("Send the draft");
await shot("draft-sent-with-reason");
await go(`/page/${PAGE}?face=04`);
await shot("page-draft-why");

// 9. 403: asking for the Director's approval with the app's token
await go(`/seat?addr=${PAGE}.04`);
await page.getByRole("button", { name: /The Director/ }).click();
await send("Seat it (make it live)");
await shot("seat-403-not-director");

// 10-11. Face 00 as the registry, on the page view and the desk door
await go("/page/10.11.21.1001?face=00");
await shot("page-face00-registry");
await go("/desk/10");
await shot("desk-door-registry");

// 12-15. .seq: export, check (refused and ok), import through the queue
await go("/export?addr=10.11.21.1001");
await shot("export-seq");
await go("/page/10.11.21.1001#seq");
await page.getByRole("button", { name: /Start from this page/ }).click();
await page.waitForTimeout(800);
const ex = await (await fetch(`${compute}/page.seq?addr=10.11.21.1001`)).text();
const broken = ex.replace(/^title := bob$/m, "title := bob").replace(/^\| title: bob$/m, "| title: robert");
await page.fill("textarea[aria-label='.seq text']", broken);
await page.getByRole("button", { name: /Check it/ }).click();
await page.waitForTimeout(1200);
await page.locator("#seq").scrollIntoViewIfNeeded();
await shot("import-check-refused-past-changed");
const blk = "= 06 notes 10.11.21.1001.06\n\n== 06.01 10.11.21.1001.06.01\n\n--- new put 10.11.21.1001.06.01\n| ## Session 3\n| why: the Bob test, asked on the Ask screen\n|\n| The user asked \"what is my name\". The Ask screen found the card 10.11.21.1001.01.bob: Bob.\n\n";
const k = ex.indexOf("~ history");
await page.fill("textarea[aria-label='.seq text']", ex.slice(0, k) + blk + ex.slice(k));
await page.getByRole("button", { name: /Check it/ }).click();
await page.waitForTimeout(1200);
await shot("import-check-ok");
await send(/Import through the queue/);
await shot("import-approved-queue-result");
await go("/queue");
await shot("queue");
await browser.close();
