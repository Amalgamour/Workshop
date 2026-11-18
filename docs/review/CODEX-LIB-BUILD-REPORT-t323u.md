# Codex report on the lib build (t323u)

Pasted by Matthew in chat on Wed Nov 18, 2026, about 3:08 PM EST. Text verbatim.

Security edit (Prima): every link originally pointed at commit 1f3c1fe98d2f4c0ca4a7a2e25cfa6c48486ef619, which held a live-looking token and was deleted from GitHub (t320u). To avoid republishing that commit id on a public branch, each link below is re-pointed to the clean tip cce5d257679cad8a9366cb4090483749d5800e0e (same paths). Mentions of "1f3c1fe" in the prose are his/Codex words and left as written.

---

What Survives the Handoff?

A research memoir and architectural case study of the Workshop reference workbook

Research draft 01 · November 18, 2026

Workshop direction: Matthew John Fisher · Archival review and draft: Codex

Abstract

Workshop explores how people and models can work on a problem without depending on the conversation that started it. This study samples a failed development workbook that nevertheless preserved enough evidence to reconstruct several decisions and repairs. Its sharpest result was a failed replay. Three participants reported that an assisted review could not run because its frozen bundle lacked a pinned dependency. The records also show that a revision could erase earlier wording and make an old return look current, and that a derived view could disagree with its governing records. I propose evaluating Workshop on whether a replacement worker can recover the intended work, the reasons for it, the authority to act, and the ability to verify or resume it.

The design intuition

Matthew recalled an early success in which a worker saw .002 and .003 of the same pack, understood the sequence, and continued from the third pass. His follow-up was more revealing: if drift left .003 almost empty, the worker could follow what survived in prior passes. This is a reported experience, not an independently replayed result. It motivates a stronger question. If the current handoff is incomplete, what can a replacement worker recover without asking the Director to tell the story again?

The workbook is useful precisely because it records both successful local behavior and ways the system failed. It distinguishes the work order from the lesson derived from it. It also separates the development conversation, the released work pass, and the Colab review. Those distinctions let a model consult prior work without treating every interesting idea as an instruction to act. [Reuse note](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/notes/understanding-and-reuse-2026-10-26.md) · [Three-loop discussion](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0415.prime-cycle/06.02.md)

Method and limits

I purposively sampled threads from the pinned reference snapshot at 1f3c1fe. I followed the original pass, review, and successor where present, then compared the project's own replay and orientation records. The sample includes favorable and adverse cases. Historical test outcomes are reported as claims in the archive, with independent reviews identified where available. This is an archival case study, with no new execution of the system, no representative sampling, and no causal estimate of model or human performance. It does not establish why the old project failed overall. [Reference snapshot](https://github.com/Amalgamour/Workshop/tree/cce5d257679cad8a9366cb4090483749d5800e0e)

What the workbook showed

A review can become reusable work. The app-entry fixture returned a receipt and replayed without launching its worker a second time. Prime found that a stored receipt could report successful collection even when it no longer matched the job. The next pass retained the original probe, corrected the identity checks, and documented a successful independent rerun. The acceptance stayed limited to the fixture correction. The lasting contribution is the chain from finding to repair to evidence, which a new reviewer can traverse. [Original review](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0504.app-entry/05.05.md#L115) · [Repair review](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0504.app-entry/05.06.md#L82)

Recoverability requires the old material. The desk-core review found in qualified serial probes that revised task wording could overwrite its predecessor and that a return against the earlier assignment could be reviewed as current. The work-history page separates the address of the work, the revision that was assigned, and the hash that verifies a particular write. That distinction has a plain consequence. If the system wants a worker to recover meaning carried by .002, the earlier text and its recorded relationship to .003 must survive. [Desk-core review](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0523.desk-core/05.01.md#L180) · [Work-history page](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0419.work-history/01.md)

An intact packet can still be unusable. Codex, Grok, and Claude all reported that the assisted reader lacked the same pinned adapter. The helper could verify custody, while the reader reported "no return" after it failed to observe the return. Review recording then refused the unbound result. The agreement is evidence of a shared preparation defect. Prior involvement, sequential carryover, missing historical dependencies, and incomplete measurement prevent an estimate of efficiency or an independent ranking of models. The useful finding is that a pack can preserve exact bytes while failing to carry the conditions needed to use them. [Codex](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0172.prime-replay-codex-01/return.md) · [Grok](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0173.prime-replay-grok-02/return.md) · [Claude](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0174.prime-replay-claude-03/return.md)

A desk summary can be out of date even when it comes from a renderer. The October 27 summary, November 1 assignment, and review attached to that assignment present different stages in the work. Separately, a disposable-book lab later reported rereading a held judgment and an unresolved question after restart. Taken together, the records suggest both a failure mode and a tractable first proof. Read the authoritative record after restart and surface a disagreement where the input records cannot establish a single current state. The lab reported a bounded result and no adoption of the live loop. [Summary](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.live.md) · [Assignment](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0401.goal/06.01.md) · [Review](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0511.workflow-colab/05.04.md#L128) · [Independent lab return](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0183.desk-loop-independent-lab-0501/return.md)

What I would build and test next

The first desk should support one complete passage of work: a scoped order, a return, a review requiring correction, a successor, and safe recovery of the next action after restart. Keep the work on one project page. Give the person a read-only page board that opens the actual evidence. Give the replacement model a small entry packet with the goal, current assignment and grant, relevant predecessor, and links to verification. Have compute check the bindings and whether the declared dependencies work in a fresh environment. Let the checker decide whether the result actually meets the goal. The first desk does not need to automate model launch to prove this.

The workbook suggests three cases for the trial. Use a sound successor, a successor that lost context, and a deliberate deletion backed by a recorded reason and decision. Compare a latest-only handoff with one that includes the linked predecessor and decision record. Give each fresh worker one case without the historical answer. Balance case order if the same model family is used repeatedly, keep conditions comparable, and record exposure to prior context. The old orientation return is a reminder to score understanding and compliance separately. [Orientation return](https://github.com/Amalgamour/Workshop/blob/cce5d257679cad8a9366cb4090483749d5800e0e/00.kernel/00.00.10.work/0153.prime-orientation-trial-t2/return.md)

Judge whether the worker finds the right predecessor, preserves the intended deletion, identifies what it cannot recover, cites the governing decision, and proposes a valid next action without authority it was never given. Then test one lesson on a second book on the same shelf. Record whether the new worker adapts it to the new goal and can explain the departure. Measure time to a correct next action, manual clarifications, and the cost of following links. Report incorrect continuations and unnecessary holds separately. This evaluates the handoff as well as the answer.

If We Are Right

A project could leave behind something more valuable than its output. The next book could inherit an explanation of where a choice worked, the case that broke it, and the decision that made the repair safe to reuse. A fresh model could bring that evidence to a person and ask the one question the old project could not answer for the new one. Even an unsuccessful build could improve later projects if its evidence and limitations remain findable.

The conjecture can fail. The extra records may create enough friction to outweigh recovery gains, or workers may still choose the wrong predecessor even with clear links. A trial that compares linked handoffs with ordinary handoffs would tell us which parts of the design earn their keep.

