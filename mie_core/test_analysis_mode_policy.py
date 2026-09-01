import subprocess,sys,json,tempfile
from pathlib import Path
SCRIPT=Path(__file__).with_name('analysis_mode_policy.py')

def run(*args):
 p=Path(tempfile.mkstemp(suffix='.json')[1]);cp=subprocess.run([sys.executable,str(SCRIPT),*args,'--output',str(p)],capture_output=True,text=True);data=json.loads(p.read_text());p.unlink();return cp.returncode,data

def test_robust_validation_seed_is_not_analytic():
 rc,d=run('--mode','ROBUST','--n','5');assert rc==4 and d['status']=='VALIDATION_ONLY'
def test_robust_30_is_pilot_only():
 rc,d=run('--mode','ROBUST','--n','30');assert rc==4 and d['status']=='PILOT_ONLY'
def test_robust_50_passes_analytic_gate():
 rc,d=run('--mode','ROBUST','--n','50');assert rc==0 and d['status']=='PASS'
def test_robust_100_is_standard_target():
 rc,d=run('--mode','ROBUST','--n','100');assert rc==0 and d['policy']['standard_target_n']==100
def test_light_below_10_blocks():
 rc,d=run('--mode','LIGHT','--n','9','--robust-cache-ready');assert rc==4 and d['status']=='BLOCKED'
def test_light_10_to_20_requires_cache_and_passes():
 for n in (10,15,20):
  rc,d=run('--mode','LIGHT','--n',str(n),'--robust-cache-ready');assert rc==0 and d['status']=='PASS'
def test_light_above_20_blocks():
 rc,d=run('--mode','LIGHT','--n','21','--robust-cache-ready');assert rc==4 and d['status']=='BLOCKED'
def test_light_without_robust_cache_blocks():
 rc,d=run('--mode','LIGHT','--n','15');assert rc==4 and d['status']=='BLOCKED'
def test_light_never_rebuilds_master():
 rc,d=run('--mode','LIGHT','--n','15','--robust-cache-ready');assert d['policy']['rebuild_master_corpus'] is False and d['policy']['online_corpus_reanalysis'] is False
