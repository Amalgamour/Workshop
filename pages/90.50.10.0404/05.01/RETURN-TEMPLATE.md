# Return 90.50.10.0404.05.01
pack: aa8de5e137a42f221472177de482bbb8c794ec620cffa5541a88bf43b659220c
done: <what you did, in plain words>
changed: <your summary of creates, modifies and deletes; the tool takes the list from git>
noticed: <what you noticed, or none>
w01: <done | need | blocked> - new templates/v4/return.txt: the text of templates/return.txt with one line added after the proof line and before the not done line: "design review: <the design files you compared your work against (at least docs/AXIOMS.md and docs/DESIGN.md in the kit), what matched, and any place it differs; t416u>". In src/render.rs add T_RETURN_V4 from that file, set TEMPLATE_VER to "4", and make packed_templates return (T_AGENTS_V3, T_PROMPT_V3, T_RETURN_V4) for "4". Leave "1", "2" and "3" exactly as they are. Update the render.rs unit tests that name the version.
w02: <done | need | blocked> - in src/cmd.rs, when the pass's pack entry has templates "4", parse_return also requires a filled "design review" line (present, not empty, not starting with "<"). The refusal says: "the return has no 'design review:' line filled in. t416u: novel work is reviewed against the design documents before the return is complete". It is recorded as return-refused like the other refusals. Packs on templates 1, 2 or 3 do not need the line. Unit tests in src/cmd.rs's own test module: a v4 pass without the line is refused with that message; with it, passes; a v3 pass without it passes.
proof: <commits, tests run and what they showed>
not done: <what you did not do, and why, or none>
unprompted: <anything you did that was not asked, or none>
overflow: <ideas past this job, or none>
