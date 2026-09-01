/* HookLab Aesthetic Reference Analyzer API client v0.1 */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;root.HookLabAnalyzerAPI=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const VERSION='hooklab-analyzer-api-client-v0.1';
function normalizeBase(url){return String(url||'').replace(/\/$/,'');}
async function analyzeReference({baseUrl,audioFile,sessionId,referenceSha256,clientVersion='producer-interface-v0.4-mobile',signal}){
  if(!baseUrl) throw new Error('ANALYZER_API_NOT_CONFIGURED');
  if(!audioFile) throw new Error('AUDIO_FILE_REQUIRED');
  if(!sessionId) throw new Error('SESSION_ID_REQUIRED');
  if(!referenceSha256) throw new Error('REFERENCE_SHA256_REQUIRED');
  const form=new FormData();
  form.append('audio',audioFile,audioFile.name||'reference-audio');
  form.append('session_id',sessionId);
  form.append('reference_sha256',referenceSha256);
  form.append('client_version',clientVersion);
  const r=await fetch(normalizeBase(baseUrl)+'/v1/analyze-reference',{method:'POST',body:form,signal});
  let body=null;try{body=await r.json();}catch(_){body={status:'FAIL',reasons:['NON_JSON_RESPONSE']};}
  if(!r.ok){const e=new Error('ANALYZER_HTTP_'+r.status);e.status=r.status;e.body=body;throw e;}
  if(!body||body.schema!=='HOOKLAB_AESTHETIC_REFERENCE_ANALYSIS_v0.1')throw new Error('BAD_ANALYZER_SCHEMA');
  if(body.session_id!==sessionId)throw new Error('ANALYZER_SESSION_MISMATCH');
  if(body.reference_sha256!==referenceSha256)throw new Error('ANALYZER_SHA256_MISMATCH');
  if(body.scientific_ingestion!==false||body.gate_a_ingestion!==false||body.m300_ingestion!==false)throw new Error('ANALYZER_SCIENTIFIC_BOUNDARY_VIOLATION');
  return body;
}
return {VERSION,normalizeBase,analyzeReference};
});
