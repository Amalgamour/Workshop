# Friction — run 01-case-a-manual

- **Manual binding and address copies: 2.**
  - The page-pointer receipt sha, typed into the custody_check argument from the page output.
  - The member path, typed.
  The sha was compared by the script, not by eye.
- **Corrections:**
  - (1) custody_check.py guessed the manifest payload key (`artifacts`/`payloads`/`files`; the real key is `sources`, with `logical` and `payload`), so its payload check came back empty. I re-checked with two more wrapped commands.
  - (2) The Windows console shows the em dash as a replacement character in wrapped output. That is display only; the files are UTF-8.
- **Blocked check:** the historical suite needs absent support files (exit 5). `validate` drift is exit 1. I did not import the dependencies from lib-build, because the contract says missing dependencies remain unknown.
- **Effort without help from a tool:**
  - finding where `candidate_files` is used meant a grep and a ~75-line code read;
  - mapping F01–F04 onto the code was all my own reading.
- **Exposure:** the case B identity and goal were read before this run, for the disclosure notes (access.jsonl line 2).
- **Interruptions:** none.
