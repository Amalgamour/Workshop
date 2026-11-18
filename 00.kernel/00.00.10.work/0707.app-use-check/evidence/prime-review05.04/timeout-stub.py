import time,sys
print("partial stdout retained",flush=True)
print("partial stderr retained",file=sys.stderr,flush=True)
time.sleep(10)
