# Director words, t401u (2026-11-19, 12:37 PM EST), verbatim

> Yes you are correct one shared returns branch and one packs branch.  We have another branch for the core and one for the shop manager UI.  
>
> This is construction design.  Once we have workshop functional, this will all be done by the compute.  Seamlessly queuing work, planning each step moving the goal forward.  
>
> I want to be careful we aren't getting stalled right now.  So lets get WF into a functional state.  It doesn't have to be perfect, it can be glitchy, we just need I can give you work.  YOu can plan it out, assign it.  In time you'll talk with the compute to arrange and order the work.  That is the bodyshop manager software design we are aiming for.

Plain words:
- Use one shared `returns` branch and one `packs` branch. This replaces Prima's one-branch-per-pass choice. Two more branches exist: one for the core and one for the shop manager UI.
- This is the construction setup. Later the compute will queue, plan and order all of this itself (the bodyshop manager design).
- Priority now: get WF working, even if it's glitchy, so Matthew can give Prima work and she can plan and assign it. Don't stall on polish.
