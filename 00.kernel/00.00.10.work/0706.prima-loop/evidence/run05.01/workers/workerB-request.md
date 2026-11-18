# Prima -> Worker B request (prima-0706-0501, pass 01)

You are Prima Worker B for Prima (Prime Assistant to Codex Prime; Director: Matthew). Task: app route and relocation. Report back to Prima only, with SendToAgent. Do not message anyone else, do not touch Git or GitHub, do not create bots, routines or subagents, do not install anything.

Shared read-only source snapshot (API reconstruction of Amalgamour/Librarian at commit 39d86e871c86484669cafecd7d2e1a8d86e15e34, blob SHA-1 verified, no .git):
  SRC=/workspace/prima/run05.01/source
  ABS_BOOK=/workspace/prima/run05.01/source/00.kernel/00.00.10.work
Your own output directory (write ONLY here): /workspace/prima/run05.01/workerB
Do not modify, chmod, copy back into, or write anything under SRC. Do not patch or rebind code, do not create a D: directory or fake tree anywhere, do not substitute another executable, do not run the Windows-only pilot harness, any test suite, or retry a product failure.

Steps (use your own shell on this shared computer):
1. Record your identity (bot name, and your model only if you actually know it; otherwise "unknown"), the actual python on PATH (`command -v python; command -v python3; /usr/bin/python3 --version`), and the environment (`env | sort`, with any secret-looking values redacted) into workerB/environment.txt.
2. Independently read app/librarian.py and the review-loop route it uses (app/review_loop_tools_v2.py, labs/review-loop-pass02/review_loop.py, and anything they name for describe-legacy) plus any app contract/README under app/. Note file:line for the route.
3. Fingerprint before: from SRC, sha256 + byte size of every file under app/, labs/review-loop-pass02/, labs/return-capture-pass01/ and 00.kernel/00.00.10.work/0182.desk-app-integration-design-0501/ into workerB/fingerprint-before.txt. Also record `ls -la "$SRC"` so any new stray path is visible.
4. The box has no `python` command, only /usr/bin/python3; use that existing interpreter. Invoke ONCE, with cwd = SRC:
   /usr/bin/python3 -B app/librarian.py review-loop describe-legacy --book /workspace/prima/run05.01/source/00.kernel/00.00.10.work --member 0182.desk-app-integration-design-0501
   Capture exact argv (JSON list), cwd, start/end timestamps with UTC offset, exit code, stdout to workerB/describe.stdout, stderr to workerB/describe.stderr. Use a wrapper with list argv. Do not retry.
5. Fingerprint after (same method, plus `ls -la "$SRC"` again) and diff. Any change, including a created file/dir, is a finding.
6. If it failed: identify the first missing path or refusal (exact path string and code line that produced it) and propose the smallest repair, as a finding only. If it worked: compare origin and intended route with the recorded 0519/05.01 -> 0119 relationship in the book and keep placement pending.
7. Write workerB/result.json with all of the above (identity, argv, cwd, timestamps, exit, stdout/stderr sha256 + bytes, fingerprints identical or not, first blocking path, proposed repair, Windows-path assumptions you saw). Mark inference vs observed.
8. Send Prima a short SendToAgent reply: exit code, the first blocking path or outcome, your file paths. Then stop.
