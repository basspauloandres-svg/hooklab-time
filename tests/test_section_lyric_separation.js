const A=require('../app/prototype_v1/hook_composition_assistant.js');
function ok(x,m){if(!x)throw new Error(m);}
const reference_analysis={tempo_bpm_median:107.1429,beat_count:299,analysis_mode:'LOCAL_ON_DEVICE_ONNX'};
const d0_manifest={schema:'HOOKLAB_D0_BROWSER_GENERATION_MANIFEST_v0.1',variants:[{variant:'thetic',events:Array(32).fill({})},{variant:'anacrustic',events:Array(32).fill({})},{variant:'syncopated',events:Array(32).fill({})}]};
const set=A.generateCandidates({language:'es',intention:'Verso: Traición',reference_analysis,d0_manifest,reference_sha256:'test'},3);
ok(set.section_function==='verse','SECTION_FUNCTION_NOT_SEPARATED');
ok(set.intention==='Traición','INTENTION_NOT_CLEAN');
ok(set.constraint_set.section_function==='verse','CONSTRAINT_SECTION_MISSING');
ok(set.constraint_set.target_section_bars===4,'VERSE_SECTION_PROFILE_NOT_APPLIED');
ok(!('target_hook_bars' in set.constraint_set),'LEGACY_HOOK_FIELD_LEAK');
ok(set.candidates.length===3,'THREE_CANDIDATES_REQUIRED');
for(const c of set.candidates){
  ok(c.section_function==='verse','CANDIDATE_SECTION_MISSING');
  ok(c.intention==='Traición','CANDIDATE_INTENTION_NOT_CLEAN');
  ok(!/\bverso\b/i.test(c.plain_text),'SECTION_LABEL_LEAKED_INTO_LYRIC');
}
console.log('PASS section/lyric separation');
