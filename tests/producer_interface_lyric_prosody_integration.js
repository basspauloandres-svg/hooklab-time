const assert=require('assert');
const fs=require('fs');
const D=require('../app/prototype_v1/d0_engine.js');
const L=require('../app/prototype_v1/lyric_prosody_ui_bridge.js');

const bad={schema:'HOOKLAB_CURATED_HOOK_PROSODY_v1.0',hook_id:'H0',language:'es',prosody_status:'AUTO',lines:[],provenance:{source:'test'}};
assert.equal(L.validateHook(bad).status,'AUDIT_PROSODY_CONTRACT');
assert(L.validateHook(bad).reasons.includes('PROSODY_NOT_CURATED_PASS'));

const hook={
 schema:'HOOKLAB_CURATED_HOOK_PROSODY_v1.0',hook_id:'HOOK-TEST-001',language:'es',prosody_status:'CURATED_PROSODY_PASS',
 lines:[{words:[
  {text:'hoy',syllables:[{text:'hoy',stressed:true}]},
  {text:'vuelvo',syllables:[{text:'vuel',stressed:true},{text:'vo',stressed:false}]},
  {text:'a',syllables:[{text:'a',stressed:true}]},
  {text:'ti',syllables:[{text:'ti',stressed:true}]}
 ]}],provenance:{source:'PRODUCER_CURATED_TEST',automatic_syllabification:false,automatic_stress_inference:false}
};
assert.equal(L.validateHook(hook).status,'PASS');
const d0=D.generate({seed:1701});
const r=L.build(d0,hook);
assert.equal(r.status,'LYRIC_PROSODY_MIDI_BRIDGE_PASS');
assert.equal(r.generation_class,'D0_EXPLORATORY');
assert.equal(r.scientific_d_unlocked,false);
assert.equal(r.hook_id,'HOOK-TEST-001');
assert.equal(r.variants.length,3);
for(const v of r.variants){
 assert(v.mapping_count>=5);
 assert(v.mapping.some(x=>x.word==='vuelvo'&&x.syllable==='vuel'&&x.stressed===true));
 const b=v.midi_bytes;
 assert.equal(String.fromCharCode(...b.slice(0,4)),'MThd');
 assert(b.includes(0xff)&&b.includes(0x05),'MIDI must contain lyric meta events');
}
const html=fs.readFileSync(require('path').join(__dirname,'../app/prototype_v1/index.html'),'utf8');
for(const id of ['hookId','hookLanguage','prosodyNotation','bindLyrics','downloadLyricMidi','downloadLyricManifest']) assert(html.includes(`id="${id}"`),`missing UI ${id}`);
assert(html.includes('hooklab_eval_${state.session_id}_${ev.hook_id}_${ev.variant_id}'),'evaluation must be keyed to session+hook+variant');
assert(html.includes("stimulus_class:'D0_EXPLORATORY'"));
assert(html.includes('scientific_d_unlocked:false'));
console.log(JSON.stringify({status:'PASS',adapter:L.VERSION,hook_id:r.hook_id,variants:r.variants.map(x=>({variant:x.variant,mapping_count:x.mapping_count,midi_bytes:x.midi_bytes.length}))},null,2));
