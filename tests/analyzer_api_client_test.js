const assert=require('assert');
const API=require('../app/prototype_v1/analyzer_api_client.js');
(async()=>{
  const file=new Blob(['abc'],{type:'audio/wav'});file.name='x.wav';
  const expected={schema:'HOOKLAB_AESTHETIC_REFERENCE_ANALYSIS_v0.1',status:'PASS',session_id:'HL-1',reference_sha256:'abc123',scientific_ingestion:false,gate_a_ingestion:false,m300_ingestion:false,tempo_bpm_median:120,beat_count:4,duration_s:2};
  let called='';
  global.fetch=async(url,opt)=>{called=url;assert.equal(opt.method,'POST');assert(opt.body instanceof FormData);return {ok:true,status:200,json:async()=>expected};};
  const r=await API.analyzeReference({baseUrl:'https://api.example.test/',audioFile:file,sessionId:'HL-1',referenceSha256:'abc123'});
  assert.equal(called,'https://api.example.test/v1/analyze-reference');
  assert.equal(r.tempo_bpm_median,120);
  global.fetch=async()=>({ok:true,status:200,json:async()=>({...expected,session_id:'WRONG'})});
  await assert.rejects(()=>API.analyzeReference({baseUrl:'https://x',audioFile:file,sessionId:'HL-1',referenceSha256:'abc123'}),/ANALYZER_SESSION_MISMATCH/);
  console.log('PASS');
})().catch(e=>{console.error(e);process.exit(1)});
