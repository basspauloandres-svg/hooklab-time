#!/usr/bin/env python3
"""Extract calibrated median_pitch_st from authorized DALI note events.

Fail-closed: no dataset/audio download, no scientific promotion, and no melody
feature other than the calibrated median_pitch_st. Writes one association-compatible
JSON evidence file per successfully parsed target plus a summary report.
"""
from __future__ import annotations
import argparse, hashlib, importlib, json, sys
from pathlib import Path
from representation_calibration_feature_extractor import features

EXPECTED_TARGET_SCHEMA='HOOKLAB_M300_DALI_TARGET_MANIFEST_v1.1'
EVIDENCE_SCHEMA='HOOKLAB_DALI_ANNOTATION_EVIDENCE_v1.0'
REPORT_SCHEMA='HOOKLAB_DALI_TARGET_EXTRACTION_REPORT_v1.0'
REPRESENTATION_ORIGIN='DALI_NOTE_EVENTS'

def _notes_from_entry(entry):
 ann=entry.annotations;typ=ann.get('type');data=ann.get('annot',{})
 if typ=='horizontal':
  notes=data.get('notes')
  if not isinstance(notes,list):raise ValueError('DALI_HORIZONTAL_NOTES_MISSING')
  return notes
 if typ=='vertical':
  from DALI.extra import unroll
  notes=unroll(data).get('notes')
  if not isinstance(notes,list):raise ValueError('DALI_VERTICAL_NOTES_MISSING')
  return notes
 raise ValueError(f'DALI_ANNOTATION_TYPE_UNSUPPORTED:{typ}')

def _event_from_note(note):
 time=note.get('time');freq=note.get('freq')
 if not isinstance(time,(list,tuple)) or len(time)!=2:raise ValueError('DALI_NOTE_TIME_INVALID')
 if isinstance(freq,(list,tuple)):
  vals=[float(x) for x in freq if x is not None and float(x)>0]
  if not vals:raise ValueError('DALI_NOTE_FREQ_INVALID')
  freq_hz=sum(vals)/len(vals)
 else:
  freq_hz=float(freq)
  if freq_hz<=0:raise ValueError('DALI_NOTE_FREQ_INVALID')
 return {'start':float(time[0]),'end':float(time[1]),'freq_hz':freq_hz}

def extract_entry(entry):
 events=[_event_from_note(n) for n in _notes_from_entry(entry)]
 f=features(events)
 if f.get('n_events',0)<2 or f.get('median_pitch_st') is None:raise ValueError('INSUFFICIENT_VALID_DALI_NOTE_EVENTS')
 return {'pitch_median_midi':float(f['median_pitch_st']),'n_note_events':int(f['n_events']),'representation_origin':REPRESENTATION_ORIGIN}

def sha256_file(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()

def locate_annotation_file(root,dali_id):
 hits=list(Path(root).rglob(f'{dali_id}.gz'))
 if len(hits)==1:return hits[0]
 if not hits:return None
 raise ValueError(f'AMBIGUOUS_DALI_ID_FILES:{dali_id}:{len(hits)}')

def load_entry(path):
 from DALI.main import get_an_entry
 return get_an_entry(str(Path(path).resolve()))

def evidence_for_target(t,entry,path):
 if str(entry.info.get('id'))!=str(t['dali_id']):raise ValueError(f'DALI_INTERNAL_ID_MISMATCH:{entry.info.get("id")}')
 x=extract_entry(entry);ncc=(entry.info.get('scores') or {}).get('NCC')
 quality='GROUND_TRUTH' if bool(entry.info.get('ground-truth')) else ('HIGH_NCC' if isinstance(ncc,(int,float)) and ncc>=.8 else 'OTHER')
 return {'schema':EVIDENCE_SCHEMA,'status':'PASS_ANNOTATION_PARSE','candidate_id':t['candidate_id'],'dali_id':t['dali_id'],'title':t['title'],'artist':t['artist'],'representation_origin':REPRESENTATION_ORIGIN,'melody_summary':{'pitch_median_midi':x['pitch_median_midi'],'n_note_events':x['n_note_events']},'quality_tier':quality,'ncc':ncc,'dataset_version':entry.info.get('dataset_version'),'ground_truth_flag':bool(entry.info.get('ground-truth')),'annotation_sha256':sha256_file(path),'scientific_promotion':False}

def build(target_manifest,dali_root,evidence_dir=None):
 if target_manifest.get('schema')!=EXPECTED_TARGET_SCHEMA:raise ValueError('TARGET_MANIFEST_SCHEMA_MISMATCH')
 if len(target_manifest.get('targets',[]))!=target_manifest.get('candidate_count'):raise ValueError('TARGET_MANIFEST_COUNT_MISMATCH')
 rows=[];audit=[];outdir=Path(evidence_dir) if evidence_dir else None
 if outdir:outdir.mkdir(parents=True,exist_ok=True)
 for t in target_manifest.get('targets',[]):
  did=t['dali_id'];p=locate_annotation_file(dali_root,did)
  if p is None:
   audit.append({'candidate_id':t['candidate_id'],'dali_id':did,'status':'ANNOTATION_FILE_MISSING'});continue
  try:
   ev=evidence_for_target(t,load_entry(p),p);rows.append(ev)
   if outdir:(outdir/f"{t['candidate_id'].replace(':','_')}__{did}.json").write_text(json.dumps(ev,indent=2,ensure_ascii=False),encoding='utf-8')
   audit.append({'candidate_id':t['candidate_id'],'dali_id':did,'status':'ANNOTATION_EXTRACTED','n_note_events':ev['melody_summary']['n_note_events']})
  except Exception as e:audit.append({'candidate_id':t['candidate_id'],'dali_id':did,'status':'ANNOTATION_REJECTED','reason':str(e)})
 expected=len(target_manifest.get('targets',[]));complete=len(rows)==expected and expected>=int(target_manifest.get('minimum_population_gate_n',30))
 return {'schema':REPORT_SCHEMA,'feature_allowlist':['median_pitch_st'],'feature_definition':'median of note-event MIDI pitches; Hz converted as 69 + 12*log2(f/440)','representation_origin':REPRESENTATION_ORIGIN,'target_manifest_schema':EXPECTED_TARGET_SCHEMA,'target_count':expected,'eligible_annotation_rows':len(rows),'status':'ANNOTATION_EVIDENCE_COMPLETE_FOR_IDENTITY_GATE' if complete else 'ANNOTATION_EVIDENCE_INCOMPLETE','audit':audit,'scientific_promotion':False,'invariants':['annotation extraction != released-recording identity PASS','annotation availability != population association support','only median_pitch_st may proceed from the calibrated melody allowlist']}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--targets',required=True);ap.add_argument('--dali-root',required=True);ap.add_argument('--dali-code-root');ap.add_argument('--evidence-dir',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 if a.dali_code_root:sys.path.insert(0,str(Path(a.dali_code_root).resolve()))
 try:importlib.import_module('DALI')
 except Exception as e:raise SystemExit(f'DALI_PROVIDER_CODE_UNAVAILABLE:{e}')
 targets=json.loads(Path(a.targets).read_text(encoding='utf-8'));out=build(targets,a.dali_root,a.evidence_dir);Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8');print(json.dumps({'status':out['status'],'eligible_annotation_rows':out['eligible_annotation_rows'],'target_count':out['target_count']}));raise SystemExit(0 if out['status']=='ANNOTATION_EVIDENCE_COMPLETE_FOR_IDENTITY_GATE' else 4)
if __name__=='__main__':main()
