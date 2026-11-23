# Director words: t526u, t527u, t528u (2026-11-23, late morning EST)

Matthew, verbatim, on worker reports and how work moves through GitHub.

## t526u

> Going forward they should be pushing reports to you on Github.  We need a wf space for those to land in pages.  So you can retrieve and see the reports there.  We use github as our nexus for information for now.

## t527u

> That needs to be built into wf so when the worker is done, the wf sending the report once it is taught where it should land them.

## t528u

> We should get claude to work on this as a lab so we can get it built well. Take all I said above plan it out.  message me when your ready.  So I can see you need me.  We need this before we can setup more workers.  For brief fast messages like we are trouble shooting.  prompt boxes are good.  But for normal wf loops we use packs > returns > review through github with WF controlling it.

Effect: until wf itself sends reports, builders push a markdown report to GitHub (interim convention in docs/plan/REPORTS.md) so Prima can retrieve it there. GitHub is the nexus for now. The proper version is built into wf: wf is taught once where reports land, and when a worker is done, wf writes and pushes the report so it lands on the page and in the hash chain. That design is lab 90.50.10.0705, for Claude (`D:\Git\claude`), grant labs/0705/. Checker is Grok-Check. Do not pack the Grok implementation pages until this lab closes. Prompt boxes stay for brief troubleshooting. The normal loop is packs > returns > review through GitHub, with wf controlling it. We need this before setting up more workers.
