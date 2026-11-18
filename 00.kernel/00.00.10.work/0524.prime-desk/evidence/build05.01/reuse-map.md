# Reuse map — 0524.prime-desk/05.01

Reading a README is not acceptance. These pins were the bytes loaded, and only the calls in the used column are reachable from `labs/prime-desk-pass01/prime_desk.py`. A pin mismatch loads nothing.

| Reader | Path | Pin sha256 / bytes | Used | Not called | Output on this desk | Limit |
| --- | --- | --- | --- | --- | --- | --- |
| desk-state | `labs/desk-state-pass01/desk_state.py` | `4d924bf6549fe37b229962d4f3a81924109a879a8206ea95066f4bfde11701b4` / 55144 | schema token `desk-state/1` | `validate`, `build_view`, `revise` | token match or a visible mismatch | `build_view` launches subprocesses and can write a candidate |
| prime-brief | `labs/prime-brief-pass01/prime_brief.py` | `302ed832d2fa955a591420f13d3b22ce91e4a7669c69a778d443fc82627580d7` / 22747 | `validate` | `build` | shape acceptance plus the module `AUTHORITY` string | `build` applies fixture lifecycle labels; those labels are not live facts |
| state-projection | `labs/state-projection-pass01/state_projection.py` | `b349da5cef5178296a069c354002a600ba4e168c2710aa5d87789724d4951ecb` / 20338 | `validate` | `project`, `inspect` | shape acceptance only | `project` and `inspect` produce lifecycle labels; `inspect` is a subprocess |
| prime-support | `labs/prime-support-pass01/prime_support.py` | `700d60d2e49c186d49e56a9a38058e21a722b4a5dd79d461453a305e8d904f70` / 59791 | none | import, `status`, `collect` | the limitation line only | status and collect use Git, which this request forbids |
| app-context | `app/context.py` | `5b1a31d47bb9f9b465a8492541467abbd9bd3a99ae524be7aa0dbffe2380eb9f` / 22063 | `parse_assignment` on one hash-matched assignment reference | `validate_context` | record fields `current_work`, `assignment_state`, `pack`, `updated` | `assignment_state` is a record field, not a process check. `validate_context` lists a runtime band and checks a runner |

Assumptions: `tools_root` is set and contains those relative paths; the request names every input hash; standard library only. A null `tools_root` skips module load and says so.

`app/librarian.py` (`939484f152c9227482e857f9ce88eaf40649f433a57d6c9d213a07bde16baee5` / 10463) and `app/development-workspace.json` were inspected and not edited. `prime-status` remains the pinned intake path. This desk is not registered there.

Not imported: `labs/prime-cycle-pass03`, `labs/review-loop-pass02`, `labs/review-construction-pass02`. The tool adds one operation row, `review-loop`, with executed false and the limitation `Pending. Successor modules were not imported.`
