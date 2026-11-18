# Worker A, unit 2 (optional second wave): dependency inventory
Read ../COMMON.md first; it applies in full, except that your folder is /workspace/prima/run0502/workers/A2/. Unit 1's files stay untouched.

## Purpose
From the frozen, selected v7 declaration, build a dependency inventory from the actual import and pin references.

## Where to look (in /workspace/prima/run0502/source-room)
- app/review-loop-v7.json
- app/review_loop_tools_v7.py
- whatever those reference: other app/ files, labs/ passes, and design05.17 evidence

## Output
1. **dependencies.json** plus a short summary in findings.md. List the exact nodes, with path, sha256 and bytes for each.
2. For the edges, show declared edges against discovered edges, with evidence lines.
3. List dynamic or fixed-root references that can't be resolved (such as D:\ paths) as unresolved.
4. Keep three kinds of dependency separate:
   - code execution dependencies
   - source-data dependencies
   - historical context

## Limits
- No new registry or app code.
- No readiness claims you haven't established.
- Static reading and AST only.
- 25-minute maximum, with a checkpoint as you go.
