const assert=require('assert');
const D=require('../app/prototype_v1/d0_engine.js');
const a=D.generate({seed:1701}),b=D.generate({seed:1701});
assert.equal(D.validate(a).status,'PASS');
assert.equal(a.stimulus_class,'D0_EXPLORATORY');
assert.equal(a.scientific_d,'BLOCKED');
assert.equal(a.variants.length,3);
assert.deepStrictEqual(a.variants,b.variants,'generation must be deterministic for same seed');
assert.deepStrictEqual(a.variants.map(x=>x.variant),['thetic','anacrustic','syncopated']);
for(const v of a.variants){
  assert(v.events.length>0);
  assert(v.tempo_bpm>=55&&v.tempo_bpm<=190);
  const bytes=D.midiBytes(v);
  assert.equal(String.fromCharCode(...bytes.slice(0,4)),'MThd');
  assert(bytes.length>50);
}
assert.equal(a.online_corpus_reanalysis,false);
assert(/NO_SOURCE_MELODY_INPUT/.test(a.copying_policy));
console.log(JSON.stringify({status:'PASS',adapter:D.VERSION,variants:a.variants.map(v=>({variant:v.variant,events:v.events.length,bpm:v.tempo_bpm,midi_bytes:D.midiBytes(v).length}))},null,2));
