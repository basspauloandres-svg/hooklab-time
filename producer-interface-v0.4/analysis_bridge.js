/* HookLab Producer Interface analyzer bridge client v0.1
 * Browser-side transport only. It does not analyze audio locally and does not contain secrets.
 * Expected backend response schema: HOOKLAB_AESTHETIC_REFERENCE_ANALYSIS_v0.1
 */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports) module.exports=api;
  root.HookLabAnalyzerBridge=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const VERSION='hooklab-analyzer-bridge-client-v0.1';
  const SCHEMA='HOOKLAB_AESTHETIC_REFERENCE_ANALYSIS_v0.1';
  function validateResult(d,expected={}){const reasons=[];if(!d||d.schema!==SCHEMA)reasons.push('BAD_SCHEMA');if(d&&d.role!=='AESTHETIC_REFERENCE_ANALYSIS')reasons.push('BAD_ROLE');if(d&&d.scientific_ingestion!==false)reasons.push('SCIENTIFIC_INGESTION_MUST_BE_FALSE');if(d&&d.gate_a_ingestion!==false)reasons.push('GATE_A_INGESTION_MUST_BE_FALSE');if(d&&d.m300_ingestion!==false)reasons.push('M300_INGESTION_MUST_BE_FALSE');if(d&&d.source_audio_persistence!=='NONE')reasons.push('SOURCE_AUDIO_PERSISTENCE_MUST_BE_NONE');if(expected.sessionId&&d&&d.session_id!==expected.sessionId)reasons.push('SESSION_ID_MISMATCH');if(expected.sha256&&d&&d.reference_sha256!==expected.sha256)reasons.push('REFERENCE_SHA256_MISMATCH');return{status:reasons.length?'FAIL':'PASS',reasons}}
  async function analyzeFile(file,opts={}){if(!file)throw new Error('AUDIO_FILE_REQUIRED');if(!file.type||!file.type.startsWith('audio/'))throw new Error('AUDIO_MIME_REQUIRED');if(!opts.endpoint)throw new Error('ANALYZER_ENDPOINT_NOT_CONFIGURED');if(!opts.sessionId)throw new Error('SESSION_ID_REQUIRED');if(!opts.sha256)throw new Error('REFERENCE_SHA256_REQUIRED');const fd=new FormData();fd.append('audio',file,file.name||'reference-audio');fd.append('session_id',opts.sessionId);fd.append('reference_sha256',opts.sha256);fd.append('role','AESTHETIC_REFERENCE');const fetchImpl=opts.fetchImpl||fetch,res=await fetchImpl(opts.endpoint,{method:'POST',body:fd,headers:{'X-HookLab-Contract':'AESTHETIC_REFERENCE_ANALYSIS_v0.1'}});if(!res.ok)throw new Error(`ANALYZER_HTTP_${res.status}`);const data=await res.json(),check=validateResult(data,{sessionId:opts.sessionId,sha256:opts.sha256});if(check.status!=='PASS')throw new Error('ANALYZER_CONTRACT_FAIL:'+check.reasons.join(','));return data}
  return{VERSION,SCHEMA,validateResult,analyzeFile};
});
