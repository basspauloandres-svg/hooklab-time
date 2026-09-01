import csv,json,subprocess,sys,tempfile
from pathlib import Path
SCRIPT=Path(__file__).with_name('melodic_confidence_gate.py')

def run(rows):
 inp=Path(tempfile.mkstemp(suffix='.csv')[1]);out=Path(tempfile.mkstemp(suffix='.csv')[1])
 fields=sorted({k for r in rows for k in r})
 with inp.open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 cp=subprocess.run([sys.executable,str(SCRIPT),'--input',str(inp),'--output',str(out)],capture_output=True,text=True)
 data=list(csv.DictReader(out.open(encoding='utf-8')));summary=json.loads(out.with_suffix('.summary.json').read_text())
 for p in (inp,out,out.with_suffix('.summary.json')):
  try:p.unlink()
  except:pass
 return cp.returncode,data,summary

def high():return {'song_id':'high','melody_overlap_ratio':.02,'melody_track_coverage':.95,'melodic_range_semitones':18,'melodic_register_midi':65,'melodic_events_per_token':1.0,'melody_candidate_score':10,'text_token_count':160}
def audit():return {'song_id':'audit','melody_overlap_ratio':.12,'melody_track_coverage':.65,'melodic_range_semitones':18,'melodic_register_midi':65,'melodic_events_per_token':2.0,'melody_candidate_score':7,'text_token_count':60}
def reject():return {'song_id':'reject','melody_overlap_ratio':.42,'melody_track_coverage':.20,'melodic_range_semitones':48,'melodic_register_midi':35,'melodic_events_per_token':4.0,'melody_candidate_score':2,'text_token_count':5}

def test_high_confidence_auto_passes():
 rc,d,s=run([high()]);assert rc==0 and d[0]['melodic_confidence_decision']=='AUTO_HIGH_CONFIDENCE'
def test_ambiguous_row_is_quarantined_for_human_audit():
 rc,d,s=run([audit()]);assert d[0]['melodic_confidence_decision']=='HUMAN_AUDIT'
def test_bad_candidate_rejects_or_reanalyzes():
 rc,d,s=run([reject()]);assert d[0]['melodic_confidence_decision']=='REJECT_OR_REANALYZE'
def test_mixed_batch_does_not_block_good_rows():
 rc,d,s=run([high(),audit(),reject()]);assert s['counts']=={'AUTO_HIGH_CONFIDENCE':1,'HUMAN_AUDIT':1,'REJECT_OR_REANALYZE':1}
def test_gate_remains_triage_not_identity_proof():
 rc,d,s=run([high()]);assert s['semantics']=='TRIAGE_ONLY_NOT_INDEPENDENT_VOCAL_IDENTITY_PROOF'
def test_ambiguity_rule_is_batch_safe():
 rc,d,s=run([high(),audit()]);assert 'AMBIGUOUS_ROWS_ARE_QUARANTINED' in s['batch_rule']
