const assert=require('assert');
const B=require('../app/prototype_v1/analysis_bridge.js');
const good={schema:B.SCHEMA,status:'PASS',reasons:[],session_id:'HL-1',role:'AESTHETIC_REFERENCE_ANALYSIS',scientific_ingestion:false,gate_a_ingestion:false,m300_ingestion:false,success_evidence_ingestion:false,source_audio_persistence:'NONE',reference_sha256:'abc',tempo_bpm_median:120,beat_count:32};
assert.equal(B.validateResult(good,{sessionId:'HL-1',sha256:'abc'}).status,'PASS');
assert.equal(B.validateResult({...good,scientific_ingestion:true},{sessionId:'HL-1',sha256:'abc'}).status,'FAIL');
assert.equal(B.validateResult({...good,reference_sha256:'x'},{sessionId:'HL-1',sha256:'abc'}).status,'FAIL');
console.log('PASS analyzer bridge client contract');
