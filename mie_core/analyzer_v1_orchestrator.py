#!/usr/bin/env python3
"""HookLab/TIME Analyzer v1 orchestrator.

FULL_TMT_READY now requires not only source-layer gates but a populated empirical
core fingerprint. Structurally inapplicable dimensions (for example recurrence in
a song with no repeated text groups) do not fail readiness; unexplained missing
core measurements do.
"""
import argparse,json,subprocess,sys
from pathlib import Path
from data_first_guard import assert_no_manual_success_weights

def load(p): return json.loads(Path(p).read_text())
def run(cmd): subprocess.run(cmd,check=True)
def present(x): return isinstance(x,(int,float))

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
 layer_gates={
  'coverage_full':acoustic.get('coverage')=='FULL',
  'audio_not_persisted':acoustic.get('audio_persistence')=='NONE',
  'M_present':bool(acoustic.get('M_events')),
  'T_valid':acoustic.get('T_status') in {'VALID','VALID_BEAT_THIS','BEAT_THIS_VALID'},
  'T_tactus_present':bool(acoustic.get('T_tactus_times')),
  'text_present':text_present,
  'text_aligned':text_aligned
 }
 song={'schema_version':'TMT_SONG_OBJECT_v1.1','song_id':manifest.get('song_id'),'provenance':manifest,
       'genre_style':{'genre':a.genre,'style':a.style},'acoustic':acoustic,'text':text,
       'inference_status':'DESCRIPTIVE_ONLY'}
 sp=out/'song_object.json';sp.write_text(json.dumps(song,indent=2,ensure_ascii=False))
 feature_path=out/'feature_payload.json'
 if text:
  run([sys.executable,str(Path(__file__).with_name('assemble_tmt_features.py')),'--acoustic',a.acoustic,'--text',a.text,'--output',str(feature_path)])
 else:
  feature_path.write_text(json.dumps({'song_id':manifest.get('song_id'),'coverage':acoustic.get('coverage'),'global':{}},indent=2))
 feature=load(feature_path)
 fp=out/'structural_fingerprint.json';run([sys.executable,str(Path(__file__).with_name('build_structural_fingerprint.py')),str(feature_path),str(fp)])
 fingerprint=load(fp); g=feature.get('global',{}); app=feature.get('applicability',{})
 core_feature_gates={
   'M_median_midi_present':present(g.get('M_median_midi')),
   'M_range_present':present(g.get('M_range_semitones')),
   'T_tempo_present':present(g.get('T_tempo_bpm')),
   'T_near_tactus_present':present(g.get('mean_near_tactus_share_by_line')),
   'text_line_count_present':present(g.get('text_line_count')) and g.get('text_line_count')>0,
   'M_events_per_token_present':present(g.get('mean_M_events_per_text_token')),
 }
 recurrence_required=app.get('recurrence')=='APPLICABLE'
 recurrence_gate=(not recurrence_required) or present(fingerprint.get('TMT',{}).get('mean_recurrence_similarity'))
 gates={**layer_gates,**core_feature_gates,'recurrence_resolved_or_not_applicable':recurrence_gate}
 status='FULL_TMT_READY' if all(gates.values()) else ('CORE_FEATURES_PENDING' if all(layer_gates.values()) else 'INCOMPLETE')
 song['quality']={'gates':gates,'status':status,'feature_applicability':app}
 sp.write_text(json.dumps(song,indent=2,ensure_ascii=False))
 routing=None
 if a.registry and (a.genre or a.style):
  rp=out/'cohort_route.json';cmd=[sys.executable,str(Path(__file__).with_name('genre_style_router.py')),a.registry,str(rp),'--min-n','5']
  if a.genre:cmd+=['--genre',a.genre]
  if a.style:cmd+=['--style',a.style]
  run(cmd);routing=load(rp)
 report={'schema':'ANALYZER_V1_RESULT','song_id':manifest.get('song_id'),'status':status,'gates':gates,
         'feature_applicability':app,'outputs':{'song_object':str(sp),'fingerprint':str(fp),'features':str(feature_path)},'cohort_route':routing,
         'rule':'FULL_TMT_READY requires complete source-layer gates plus populated core empirical TMT features; inapplicable dimensions are explicit, never fabricated.'}
 (out/'analyzer_result.json').write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report))
if __name__=='__main__':main()
