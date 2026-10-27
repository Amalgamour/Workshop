import json,sys,subprocess
request=json.loads(sys.stdin.buffer.read())
subprocess.Popen([sys.executable,'-c','import time; time.sleep(5)'],stdin=subprocess.DEVNULL,stdout=sys.stdout,stderr=sys.stderr)
