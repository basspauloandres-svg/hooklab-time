#!/usr/bin/env python3
"""HookLab/TIME Analyzer v1 orchestrator.

Single deterministic entry point for resolved source layers. It does not invent missing evidence.
Acoustic/text acquisition adapters feed this orchestrator; this module validates gates,
assembles the Song Object, builds the structural fingerprint and optionally routes a genre/style cohort.
"""
import argparse,json,subprocess,sys
from pathlib import Path
from data_first_guard import assert_no_manual_success_weights

def load(p): return json.loads(Path(p).read_text())
def run(cmd): subprocess.run(cmd,check=True)

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--manifest',required=True);ap.add_argument('--acoustic',required=True)
 ap.add_argument('--text');ap.add_argument('--registry');ap.add_argument('--genre');ap.add_argument('--style')
 ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 manifest=load(a.manifest); acoustic=load(a.acoustic); text=load(a.text) if a.text else None
 assert_no_manual_success_weights(manifest)
 text_present=text is not None
 text_aligned=bool(text and text.get('alignment_status')=='ALIGNED' and float(text.get('alignment_coverage',0))>=0.95)
 gates={
  'coverage_full':acoustic.get('coverage')=='FULL',
  'audio_not_persisted':acoustic.get('audio_persistence')=='NONE',
  'M_present':bool(acoustic.get('M_events') or acoustic.get('M_structural_count')),
  'T_valid':acoustic.get('T_status') in {'VALID','VALID_BEAT_THIS','BEAT_THIS_VALID'},
  'text_present':text_present,
  'text_aligned':text_aligned
 }
 acoustic_ready=all(gates[k] for k in ('coverage_full','audio_not_persisted','M_present','T_valid'))
 status='FULL_TMT_READY' if acoustic_ready and text_present and text_aligned else ('ACOUSTIC_READY_TEXT_PENDING' if acoustic_ready else 'INCOMPLETE')
 song={'schema_version':'TMT_SONG_OBJECT_v1.0','song_id':manifest.get('song_id'),
       'provenance':manifest,'genre_style':{'genre':a.genre,'style':a.style},
       'acoustic':acoustic,'text':text,'quality':{'gates':gates,'status':status},
       'inference_status':'DESCRIPTIVE_ONLY'}
 sp=out/'song_object.json';sp.write_text(json.dumps(song,indent=2,ensure_ascii=False))
 # Normalize acoustic regression into the descriptive fields expected by the fingerprint builder.
 rr=acoustic.get('M_range_raw') or [None,None]
 feature=acoustic.get('feature_vector') or {
   'song_id':manifest.get('song_id'),'coverage':acoustic.get('coverage'),
   'global':{
      'M_event_count':acoustic.get('M_post_ornament_count') or acoustic.get('M_structural_count'),
      'M_range_semitones':(rr[1]-rr[0]) if len(rr)==2 and rr[0] is not None and rr[1] is not None else None,
      'T_tempo_bpm':acoustic.get('T_tempo_bpm_median'),'T_tactus_count':acoustic.get('T_tactus_count'),
      'text_line_count':len(text.get('units',[])) if text else None,
      'text_repetition_group_count':len(text.get('repetition_groups',[])) if text else None
   }}
 fp_in=out/'feature_payload.json';fp_in.write_text(json.dumps(feature,indent=2,ensure_ascii=False))
 fp=out/'structural_fingerprint.json';run([sys.executable,str(Path(__file__).with_name('build_structural_fingerprint.py')),str(fp_in),str(fp)])
 routing=None
 if a.registry and (a.genre or a.style):
  rp=out/'cohort_route.json';cmd=[sys.executable,str(Path(__file__).with_name('genre_style_router.py')),a.registry,str(rp),'--min-n','5']
  if a.genre:cmd+=['--genre',a.genre]
  if a.style:cmd+=['--style',a.style]
  run(cmd);routing=load(rp)
 report={'schema':'ANALYZER_V1_RESULT','song_id':manifest.get('song_id'),'status':status,'gates':gates,
         'outputs':{'song_object':str(sp),'fingerprint':str(fp)},'cohort_route':routing,
         'rule':'FULL_TMT_READY requires FULL acoustic evidence and >=95% documentary text alignment. Missing evidence is never fabricated.'}
 (out/'analyzer_result.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report))
if __name__=='__main__':main()
