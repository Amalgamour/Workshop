# piece agents.branch-limits

id: agents.branch-limits
version: 1
state: DRAFT (not approved). Made by Prima under t327u. Build stage only (t329u): reviewed as protection hardens.
section: Where you may push
axioms: 1
why: the grant names the branches; main is outside every grant so far.
authority: Director t267u ("use workflow and push freely"; docs/review/DIRECTOR-WORDS-t267u.md:19-21). `7`: no recorded Director words say "never merge main" outright; it is Prima's mapping of t267u.
slots:
  - push_target: one branch name from the grant, or `none`
sha256: 7cb97f0fef8a414bf2b2a4e9835560c8aca646842f6b562b208c2b79473fe443

wording:
Push only to {{push_target}}. Never merge into main. Never force push.
end wording
