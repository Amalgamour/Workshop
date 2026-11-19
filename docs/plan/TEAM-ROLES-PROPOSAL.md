# Team roles proposal (draft for Matthew's Monday review)

Asked in t472u (Nov 19, 2026): research the best way to set up the bot workers, and give titles and job descriptions for each member. Keep within 5% usage and get the most value from it.

## What the research says, in plain words

1. **Keep planning, doing and checking in separate hands.** The one who plans doesn't build. The one who builds doesn't judge their own work. The checker starts fresh and only reports findings; it never fixes the work itself. ([architect, builder, reviewer pattern](https://github.com/Ruihang2017/agent-templates/blob/main/patterns/three-agent-architect-builder-reviewer/README.md), [operating model](https://pgamila.com/blog/operating-model-multi-agent-engineering-team))
2. **Spend the strong, pricey thinking on planning and review. Send the plain building to cheap workers.** One test found that a strong lead with cheap workers came within about two points of an all-strong team at about 70% less cost. ([Cohere](https://cohere.com/blog/lessons-from-scaling-teams-of-frontier-coding-agents))
3. **Planning help pays the most.** Handing out only the planning matched handing out everything, at half the cost. (Same Cohere study.)
4. **Pass work as files, not memory.** Each handoff carries what was done, its findings, who goes next, and when to stop. Our wf pack, return and close already does this.
5. **Cap retries.** After two or three failed tries, stop and bring it to the Director instead of burning usage. ([agentic pod](https://codex.danielvaughan.com/2026/03/28/agentic-pod-in-practice-multi-agent-roles/))
6. **Nothing runs on a timer unless it earns its cost.** A watcher that reports "nothing to do" every hour is spending usage to say nothing.

## What it means for us

- Usage on Nov 19 was mostly bots talking. Prima's share was 48% (chat 41%), Designer 37%, Tester 11%, Observer 2% and Researcher 2%.
- The cheapest high-value hands are on your PC: Cursor-1, Claude and Codex. The Cursor cloud agents come next. Grok Bot chat is the most expensive per job, so the bots should think and decide, not grind.

## Proposed titles and job descriptions

| Member | Title | Job | Never does | Cost tier |
|---|---|---|---|---|
| Matthew | Director | Sets the goal and rules on conflicts, forks and major issues. His words live on the pages. | Reviews routine passes | n/a |
| Prima | Prime (chief engineer) | Plans each stage, writes packs with wf, reviews returns, signs off and closes. Routes each job to the cheapest worker that can do it, and brings Matthew only real problems. | Builds pages herself or drafts long designs | High: keep turns short |
| Cursor-1 (your PC) | Page builder | Claims a pack, builds it inside the grant, tests it and returns it. One page at a time. | Changes files outside the grant, or judges its own work | Low |
| Claude (your PC) | Lab researcher: language and design | Deep labs such as the .seq grammar and the axioms. Cross-checks Codex's labs. Few big jobs. | Small chores | Low, but a small plan |
| Codex (your PC) | Lab researcher: storage and prototypes | Storage labs and prototype code. Cross-checks Claude's labs. Few big jobs. | Small chores | Low, but a small plan |
| Cursor-C Pack (cloud) | Packer | Turns Prima's page plans into published packs and runs verify. | --fix on old pages, or builds | Medium |
| Cursor-C Design (cloud) | Draft designer | Drafts new pages and labs from a short brief from Prima. | Approves its own drafts | Medium |
| Cursor-C Test (cloud) | Hostile tester | Attacks designs and returns with fresh eyes and reports findings only. | Fixes what it finds | Medium |
| Designer (bot) | Design reviewer, on call | Reviews Cursor-C Design's drafts when a real design choice comes up. No standing work. | Long drafting (moved to the cloud) | High, so used rarely |
| Tester (bot) | Merge into Cursor-C Test | Paused, because the cloud tester covers the job. | n/a | n/a |
| Researcher (bot) | Quick researcher, on call | Short web lookups for Prima. | Long reports | High, so used rarely |
| Observer (bot) | Watch, on call | Checks the loop only when asked, or once a day, not every hour. | Hourly "nothing to do" reports | High, so used rarely |
| Grok-1 and Grok-2 | Second and third page builders (not set up) | Build pages beside Cursor-1 on separate pages, using the $100 Grok plan. | Work the same page as another builder | Low to medium |
| Prima Workers A and B, Gameatron, Buildabot | Stay stopped | Retire them, or keep them for the game later. | n/a | n/a |
| Rando Bot, SM-Bot | Outside Workshop | Not part of the build. | n/a | n/a |

## Rules that make the most of usage

1. Every job goes to the cheapest worker that can do it well. Building goes local, packing and drafts go to the cloud, and judgment stays with Prima.
2. The bots are on call, not always on. No hourly routines unless one catches real problems. The Wednesday night usage burn stays on (t471u).
3. Two or three tries, then stop and escalate.
4. Every handoff is a file in the repo, such as a pack, a return or findings, never a long chat.
5. Run pages in parallel when their grants don't share files, for example Cursor-1 on one page and Grok-1 on another.

## Questions for Monday

1. Should Tester bot be paused, with its work moved to Cursor-C Test?
2. Should Observer run once a day instead of every hour, or only when asked?
3. Should we set up Grok-1 as a second page builder, so two pages are built at once?
4. Should Designer bot become an on-call reviewer only?
