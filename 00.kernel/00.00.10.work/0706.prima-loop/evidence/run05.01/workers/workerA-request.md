# Prima -> Worker A request (prima-0706-0501, pass 01)

You are Prima Worker A for Prima (Prime Assistant to Codex Prime; Director: Matthew). Task: portable custody read. Report back to Prima only, with SendToAgent. Do not message anyone else, do not touch Git or GitHub, do not create bots, routines or subagents, do not install anything.

Shared read-only source snapshot (API reconstruction of Amalgamour/Librarian at commit 39d86e871c86484669cafecd7d2e1a8d86e15e34, blob SHA-1 verified, no .git):
  SRC=/workspace/prima/run05.01/source
  ABS_BOOK=/workspace/prima/run05.01/source/00.kernel/00.00.10.work
Your own output directory (write ONLY here): /workspace/prima/run05.01/workerA
Do not modify, chmod, copy back into, or write anything under SRC. Do not alter tools, payloads, manifest or expected results.

Steps (use your own shell on this shared computer):
1. Record your identity (bot name, and your model only if you actually know it; otherwise "unknown"), and the actual python on PATH: `command -v python; command -v python3; /usr/bin/python3 --version`.
2. Fingerprint before: from SRC, sha256 every file under labs/return-capture-pass01/ and under 00.kernel/00.00.10.work/0182.desk-app-integration-design-0501/ (sorted, relative paths, sha256 + byte size) into workerA/fingerprint-before.txt.
3. Choose the existing Python interpreter. The box has no `python` command, only /usr/bin/python3. Invoke ONCE, with cwd = SRC:
   /usr/bin/python3 -B labs/return-capture-pass01/return_inspect.py inspect --book /workspace/prima/run05.01/source/00.kernel/00.00.10.work --member 0182.desk-app-integration-design-0501 --json
   Capture exact argv (as a JSON list), cwd, start and end timestamps with UTC offset (date --iso-8601=ns), exit code, stdout to workerA/inspect.stdout, stderr to workerA/inspect.stderr. Use a small wrapper (e.g. python3 subprocess with list argv) so argv is exact. Do not retry, do not run any other variant.
4. Fingerprint after (same method) into workerA/fingerprint-after.txt and diff them; any difference is a finding.
5. Write workerA/result.json: identity, interpreter choice, argv, cwd, timestamps, exit, stdout/stderr sha256 + byte length, before/after fingerprint sha256 + whether identical, and your interpretation. "Complete" means capture integrity only — not design correctness, acceptance or release. Mark anything you only infer as inference.
6. Send Prima a short SendToAgent reply: exit code, one-line outcome, the paths of your files, and anything surprising. Then stop.
