#!/usr/bin/env python3
import json,tempfile,subprocess,sys
from pathlib import Path

hook={
 'schema':'HOOKLAB_CURATED_HOOK_PROSODY_v1.0','hook_id':'T001','language':'es','prosody_status':'CURATED_PROSODY_PASS',
 'provenance':{'source':'synthetic_regression_fixture'},
 'lines':[{'text':'Canta conmigo','words':[
   {'text':'Canta','syllables':[{'text':'Can','stressed':True},{'text':'ta','stressed':False}]},
   {'text':'conmigo','syllables':[{'text':'con','stressed':False},{'text':'mi','stressed':True},{'text':'go','stressed':False}]}
 ]}]
}
structure={
 'schema':'HOOKLAB_TMT_STRUCTURAL_GENERATION_v2.0','status':'THREE_FULL_TMT_STRUCTURAL_CANDIDATES_READY','variants':[]
}
for name,off in [('thetic',0.0),('anacrustic',0.0),('syncopated',0.25)]:
 structure['variants'].append({'variant':name,'tempo_bpm':120,'phrases':[{'events':[{'onset_s':off+i*.5,'midi':60+i%3} for i in range(7)]}]})
with tempfile.TemporaryDirectory() as td:
 p=Path(td); (p/'hook.json').write_text(json.dumps(hook)); (p/'structure.json').write_text(json.dumps(structure)); out=p/'out'
 subprocess.run([sys.executable,'mie_core/lyric_prosody_midi_bridge.py','--hook',str(p/'hook.json'),'--structure',str(p/'structure.json'),'--output-dir',str(out)],check=True)
 m=json.loads((out/'bridge_manifest.json').read_text())
 assert m['status']=='LYRIC_PROSODY_MIDI_BRIDGE_PASS'
 assert m['generation_class']=='D0_EXPLORATORY' and m['scientific_d_unlocked'] is False
 assert len(m['variants'])==3
 for v in m['variants']:
  assert (out/v['midi_file']).exists() and v['mapping_count']==7
 bad=dict(hook); bad['prosody_status']='AUTO_INFERRED'
 (p/'bad.json').write_text(json.dumps(bad))
 r=subprocess.run([sys.executable,'mie_core/lyric_prosody_midi_bridge.py','--hook',str(p/'bad.json'),'--structure',str(p/'structure.json'),'--output-dir',str(p/'badout')])
 assert r.returncode==4
print('PASS: lyric-prosody-MIDI bridge traceability and fail-closed prosody contract')
