# piece agents.role

id: agents.role
version: 1
state: DRAFT (not approved). Made by Prima under t327u. Build stage only (t329u): reviewed as protection hardens.
section: Role
axioms: 3, 5
why: a model must know which seat it sits in before it acts; the seat sets what it may run.
authority: workflow/AGENTS.md:28-37 @a00bc53 (role table); Director t267u (build the workflow tools and instructions)
slots:
  - role: one of: Builder, Checker, Observer, Prime, Person
  - name: a wf name (wf --as rules, chars.rs table)
sha256: 7a9f15e0b50b605b26d29b1abcca809400b83f9a3096ef6cb0c1bd3d1a380f5f

wording:
You are {{role}}. Your name is {{name}}. Say it on every wf command: `--as {{name}}`.
Run only the commands your role may run (kit AGENTS.md, role table).
end wording
