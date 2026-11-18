import json, subprocess, os, hashlib
OUT="/workspace/prima/run05.01/workerA"; SRC="/workspace/prima/run05.01/source"
argv=["/usr/bin/python3","-B","labs/return-capture-pass01/return_inspect.py","inspect","--book","/workspace/prima/run05.01/source/00.kernel/00.00.10.work","--member","0182.desk-app-integration-design-0501","--json"]
def now(): return subprocess.run(["date","--iso-8601=ns"],capture_output=True,text=True).stdout.strip()
start=now()
p=subprocess.run(argv,cwd=SRC,capture_output=True)
end=now()
open(OUT+"/inspect.stdout","wb").write(p.stdout); open(OUT+"/inspect.stderr","wb").write(p.stderr)
json.dump({"argv":argv,"cwd":SRC,"start":start,"end":end,"exit":p.returncode},open(OUT+"/run.json","w"),indent=2)
print(p.returncode)
