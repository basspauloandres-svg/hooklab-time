import csv,json,random,subprocess,sys,tempfile
from pathlib import Path
SCRIPT=Path(__file__).with_name('cohort_stability_gate.py')
FIELDS=['tempo_bpm','melodic_range_semitones','melodic_events_per_token','near_tactus_share','text_line_count']

def make_rows(n,drift=False):
 rows=[]
 for i in range(n):
  shift=(i/n*35 if drift else 0)
  rows.append({'tempo_bpm':120+shift+(i%5)*.2,'melodic_range_semitones':18+(i%3),'melodic_events_per_token':1.0+(i%4)*.01,'near_tactus_share':.62+(i%3)*.005,'text_line_count':42+(i%5)})
 return rows

def run(rows):
 d=Path(tempfile.mkdtemp());m=d/'m.csv';o=d/'o.json'
 with m.open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
 cp=subprocess.run([sys.executable,str(SCRIPT),'--matrix',str(m),'--output',str(o)],capture_output=True,text=True)
 return cp.returncode,json.loads(o.read_text())

def test_small_n_never_freezes_reference():
 rc,d=run(make_rows(30));assert rc==4 and d['status']=='MORE_ROBUST_DATA_REQUIRED'
def test_stable_125_rows_pass():
 rc,d=run(make_rows(125));assert rc==0 and d['status']=='STABLE_REFERENCE_READY' and d['stable_tail_transitions']>=2
def test_drifting_distribution_fails():
 rc,d=run(make_rows(125,drift=True));assert rc==4 and d['status']=='MORE_ROBUST_DATA_REQUIRED'
def test_gate_reports_n_not_representativeness_claim():
 rc,d=run(make_rows(125));assert 'N alone does not establish representativeness' in d['rule']
