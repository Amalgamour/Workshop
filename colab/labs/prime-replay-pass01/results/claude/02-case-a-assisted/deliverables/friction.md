# Friction — run 02-case-a-assisted

- **Manual binding and address copies: 0** of hashes. The template binding was pre-filled; I left it as read.
  - I typed 4 absolute paths (registration, templates, journal, tool), repeated in each command line.
  - I also typed the work id `case-a` and the day date (from a directory listing).
- **Tool refusals and failures (assisted effort):**
  - read ×3 with `observation-failed`;
  - a direct reader run, exit 2 (`missing clerk_adapter.py`);
  - record refused, exit 2.
- **Diagnosis cost:** the view does not carry the reader's stderr, so I needed 1 extra wrapped command plus 2 unwrapped greps to find the cause.
- **My own correction:** a `/tmp` path in a bash pipe is not visible to Windows Python. One parse failed, and I re-read the retained operation stdout instead. Not a tool issue.
- **Misleading output:** `pass state: no-return` while custody is verified complete (packet). I did not act on it.
- **Coverage gap:** the packet holds only return.md and receipt.json, so review substance still needed direct reads (carried over from run 01).
- **Not attempted:** repairing the bundle (forbidden); `prime_review report` on a hand-built record.
- **Interruptions:** none.
