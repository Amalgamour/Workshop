from pathlib import Path
import json,sys,subprocess,importlib.util

R=Path(r'D:\Git\lib-build');L=Path(__file__).parent
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
mode=sys.argv[1]
if mode=='workflow':
 p=subprocess.run([sys.executable,'-B',str(R/'labs/colab-workflow-pass03/tests/run_suite.py')],cwd=R,capture_output=True)
 (L/'workflow-tests.stdout').write_bytes(p.stdout);(L/'workflow-tests.stderr').write_bytes(p.stderr)
 (L/'workflow-tests.exit').write_text(str(p.returncode))
 print(json.dumps({'mode':mode,'exit':p.returncode,'stdout_tail':p.stdout.decode('utf-8','replace').splitlines()[-5:],'stderr_tail':p.stderr.decode('utf-8','replace').splitlines()[-5:]}))
elif mode=='harness':
 lab=R/'colab/labs/0707.app-use-check/pass04'
 m=load('harness_selftest_prime',lab/'selftest.py')
 cfg=json.loads((lab/'candidate.config.json').read_text());cfg['interpreter']={'path':sys.executable,'version':'.'.join(str(x) for x in sys.version_info[:3])}
 cp=L/'native-harness-config.json';cp.write_text(json.dumps(cfg))
 m.REAL_CONFIG=cp;m.OUT=L/'harness-selftest';m.SCRATCH=L/'harness-scratch'
 code=m.main();print(json.dumps({'mode':mode,'exit':code}))
elif mode=='timeout':
 lab=R/'colab/labs/0707.app-use-check/pass04';sys.path.insert(0,str(lab));h=load('harness_timeout_prime',lab/'harness.py')
 stub=L/'timeout-stub.py';stub.write_text('import time,sys\nprint("partial stdout retained",flush=True)\nprint("partial stderr retained",file=sys.stderr,flush=True)\ntime.sleep(10)\n')
 cfg=json.loads((lab/'candidate.config.json').read_text());out=L/'timeout-fixtures';out.mkdir()
 cfg.update(kind='stub',output_root=str(out),timeout_seconds=1,interpreter={'path':sys.executable,'version':'.'.join(map(str,sys.version_info[:3]))})
 run=h.Run(cfg,h.dump(cfg),'stub',L/'timeout-evidence');case=run.dir/'case';case.mkdir()
 d=run.call(case,'timeout',[sys.executable,'-B',str(stub)])
 data={'timed_out':d['timed_out'],'stdout_bytes':next((case/'calls').glob('*.stdout')).stat().st_size,'stderr_bytes':next((case/'calls').glob('*.stderr')).stat().st_size,'killed':d['killed']}
 (L/'timeout-check.json').write_text(json.dumps(data,indent=2));print(json.dumps(data))
