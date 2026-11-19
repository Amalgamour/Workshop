# Worker roles and usage balance (2026-11-19, from t465u-t466u)

Matthew's plans: Codex and Claude are about 20 a month each; Grok and Cursor are about 100 a month.
Rule (t465u): page builds go to the cheaper local workers whenever possible.

| Worker | Where | Role | Queue now |
|---|---|---|---|
| Cursor-1 | Matthew's PC, D:\Git\wf-run | Builds stage 1 pages, one at a time | 0404, 0415, then 0406-0409, 0411-0414, 0498 |
| Claude | Matthew's PC, D:\Git\claude | Deep lab work and design thinking, few big jobs | Lab 0702 seq grammar; then cross-check 0703; then an axioms lab |
| Codex | Matthew's PC, D:\Git\codex | Deep lab work and prototypes, few big jobs | Lab 0703 seq storage (waits on network setting); then cross-check 0702 |
| Cursor-C Pack | Cursor cloud | Makes and publishes packs with wf (c09fa60c) | 0404, 0415 |
| Cursor-C Design | Cursor cloud | Page and lab drafts | On call |
| Cursor-C Test | Cursor cloud | Hostile trials of designs and returns | On call |
| Prima | Grok Bot | Reviews, intake, check, signoff, close; brings Matthew only conflicts, forks and major issues | Ongoing |

Grok-1 and Grok-2 are not set up. They could later take stage 1 pages beside Cursor-1 on separate pages.
