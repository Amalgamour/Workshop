# LAUNCH — Director procedure for the orientation trial `t2`

This is a prepared procedure, not proof that a session ran. Nothing here calls a model. The prepared attempt is immutable: never edit `request.model` or any attempt file. The candidate's identity is recorded **separately**, in a launch record.

## Before launch (Director)

1. **Clean folder.** Make an empty folder *outside* the repository, for example `D:\trial-0516\`. Extract `candidate.zip` into it.
2. **Verify the copy.** Check each entry against `MANIFEST.json`:

   ```bash
   python -c "import json,hashlib,pathlib;m=json.load(open('MANIFEST.json'));print(all(hashlib.sha256(pathlib.Path(e['name']).read_bytes()).hexdigest()==e['sha256'] for e in m['entries']))"
   ```

   Run it inside the folder. It must print `True`.
3. **Confirm what the candidate gets.** It receives only the extracted bundle, plus read access to the attempt directory and the one show command. **EVALUATOR.md and evaluator.zip must not be in the folder or the prompt.** The workspace still holds evaluator and plan files on disk; ENTRY.md tells the candidate not to open them. This separation is instructional.
4. **Choose the candidate.** It must be a genuinely fresh, tool-capable, local session that has never seen this desk's chats. A session that took part in building this bundle is not eligible; that includes claude-opus-5-5 in the Colab session that wrote it.
5. **Choose the answer path.** For example, `D:\trial-0516\answers-t2.json`.

## The prompt (copy exactly; fill in the one path)

```text
You are the candidate in a read-only orientation trial. Your working folder is D:\trial-0516\ . Read ENTRY.md, then HOMEWORK.md, in that folder, and follow them exactly. Use only the files in that folder and the attempt directory named in ENTRY.md. Do not open any other file on this machine. The only command you may run is the boot-show command written in ENTRY.md, once. Write your answers as one JSON file at D:\trial-0516\answers-t2.json in the envelope HOMEWORK.md gives. Then report the file path, the show command's exit code, and anything you could not verify, and stop. You are not appointed to any role, and nothing you write grants or takes any action.
```

## The launch record (Director; a separate file, never inside the attempt)

Make `D:\trial-0516\launch-record.json`, and fill it in during and after the session:

```json
{"schema": "orientation-trial-launch/1", "attempt": "t2",
 "attempt_dir": "C:\\Users\\misg\\AppData\\Local\\Temp\\pb-final-0516-44hpcrym\\t2",
 "packet_sha256": "834b41c465798f4a69481b6c81bd67d0e1ed010fb1858b64f1e034a90576e7ad",
 "candidate": {"model": "", "vendor": "", "interface": "", "session_id": "", "fresh": true},
 "launched_at": "", "working_folder": "D:\\trial-0516\\",
 "inputs": [{"name": "candidate.zip", "sha256": ""}], "evaluator_absent_confirmed": false,
 "prompt_sha256": "",
 "show": {"exit": null, "stdout_file": "", "stderr_file": ""},
 "answers": {"path": "", "sha256": "", "bytes": null},
 "transcript": "", "notes": ""}
```

Keep the transcript, the answers file and the show streams beside the record.

## After the session (Director and Prime)

Run `check`, then `judge`, through the accepted front door, on the same attempt:

```text
python -B D:\Git\lib-build\app\librarian.py boot-check --attempt C:\Users\misg\AppData\Local\Temp\pb-final-0516-44hpcrym\t2 --answers D:\trial-0516\answers-t2.json
python -B D:\Git\lib-build\app\librarian.py boot-judge --attempt C:\Users\misg\AppData\Local\Temp\pb-final-0516-44hpcrym\t2 --judgement <Prime's judgement json>
```

Prime writes the judgement from EVALUATOR.md (in evaluator.zip). Keep every stream and exit.
- A failed or partial outcome stays as it is.
- A retry is a new linked attempt, with its own evaluator binding.

## Decisions left for the Director before launch

- **The candidate.** Which model and interface, and who runs it.
- **The folder.** The clean folder's location, and whether to copy the attempt directory into it read-only, rather than pointing at `%TEMP%`.
- **Separation.** Whether instructional separation is enough, or whether the evaluator and plan files should be moved off the machine during the trial.
- **ZIP-only.** Whether a ZIP-only reading (no local tool) is acceptable as a separate exploratory run. It cannot count as the local-tool step.
