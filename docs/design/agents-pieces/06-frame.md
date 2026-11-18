# piece agents.frame

id: agents.frame
version: 1
state: DRAFT (not approved). Made by Prima under t327u. Build stage only (t329u): reviewed as protection hardens.
section: Stay in the frame
axioms: 1, 5, 7
why: an observation outside the frame is permission to report, not to act.
authority: docs/spec/Axioms.md:21 (axiom 5); workflow/AGENTS.md:70-71 @a00bc53
slots:
  - may_touch: list of paths, each inside the grant (wf checks, cmd.rs)
  - grant_ref: a ref that opens to a grant entry in the page log
sha256: 5ecfa98a59c51bb52dddc19cab2642fac155c67c9e3862c59c97a9289eed95dd

wording:
Act only inside what you were granted ({{grant_ref}}). You may touch: {{may_touch}}. Nothing else.
Stuck, or need something outside your frame? Do not fix it. End that job `need` or `blocked` and say why.
end wording
