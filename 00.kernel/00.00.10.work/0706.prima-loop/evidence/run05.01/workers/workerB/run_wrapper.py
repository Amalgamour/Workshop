import json, subprocess, datetime, os
SRC = "/workspace/prima/run05.01/source"
OUT = "/workspace/prima/run05.01/workerB"
argv = ["/usr/bin/python3", "-B", "app/librarian.py", "review-loop", "describe-legacy",
        "--book", "/workspace/prima/run05.01/source/00.kernel/00.00.10.work",
        "--member", "0182.desk-app-integration-design-0501"]
start = datetime.datetime.now().astimezone().isoformat()
p = subprocess.run(argv, cwd=SRC, capture_output=True, shell=False)
end = datetime.datetime.now().astimezone().isoformat()
open(os.path.join(OUT, "describe.stdout"), "wb").write(p.stdout)
open(os.path.join(OUT, "describe.stderr"), "wb").write(p.stderr)
json.dump({"argv": argv, "cwd": SRC, "start": start, "end": end, "exit_code": p.returncode},
          open(os.path.join(OUT, "invocation.json"), "w"), indent=2)
print(p.returncode)
