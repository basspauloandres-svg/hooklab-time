(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.HookLabMieRecognitionBridge=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const SCHEMA='HOOKLAB_MIE_RECOGNITION_v0.3';
  function validate(result,expected={}){
    const reasons=[],tx=result&&result.transcription||{};
    if(!result||result.schema!==SCHEMA)reasons.push('BAD_SCHEMA');
    if(result&&result.status!=='PASS')reasons.push('STATUS_NOT_PASS');
    if(result&&result.scientific_d_unlocked!==false)reasons.push('SCIENTIFIC_D_MUST_REMAIN_LOCKED');
    if(result&&result.scientific_ingestion!==false)reasons.push('SCIENTIFIC_INGESTION_MUST_BE_FALSE');
    if(result&&result.source_audio_persistence!=='NONE')reasons.push('SOURCE_AUDIO_PERSISTENCE_MUST_BE_NONE');
    if(expected.sessionId&&result&&result.session_id!==expected.sessionId)reasons.push('SESSION_ID_MISMATCH');
    if(expected.sha256&&result&&result.reference_sha256!==expected.sha256)reasons.push('REFERENCE_SHA256_MISMATCH');
    if(!Array.isArray(tx.melody_events)||!tx.melody_events.length)reasons.push('MELODY_REQUIRED');
    if(!Array.isArray(tx.harmony_states)||!tx.harmony_states.length)reasons.push('HARMONY_REQUIRED');
    if(!Array.isArray(tx.beat_events)||!tx.beat_events.length)reasons.push('BEAT_REQUIRED');
    if(!result||!result.audition_wav_base64)reasons.push('AUDIBLE_MHT_REQUIRED');
    return{status:reasons.length?'FAIL':'PASS',reasons};
  }
  function base64Blob(base64,mime='audio/wav'){
    const raw=atob(base64),bytes=new Uint8Array(raw.length);
    for(let i=0;i<raw.length;i++)bytes[i]=raw.charCodeAt(i);
    return new Blob([bytes],{type:mime});
  }
  async function analyze(file,options={}){
    if(!file)throw new Error('AUDIO_FILE_REQUIRED');
    if(!options.endpoint)throw new Error('ANALYZER_ENDPOINT_REQUIRED');
    if(!options.sessionId||!options.sha256)throw new Error('SESSION_AND_SHA_REQUIRED');
    const body=new FormData();body.append('audio',file,file.name||'audio');body.append('session_id',options.sessionId);body.append('reference_sha256',options.sha256);
    const headers={'X-HookLab-Contract':SCHEMA};if(options.token)headers.Authorization='Bearer '+options.token;
    const response=await (options.fetchImpl||fetch)(options.endpoint.replace(/\/$/,'')+'/v1/analyze-reference',{method:'POST',body,headers,signal:options.signal});
    if(!response.ok)throw new Error('ANALYZER_HTTP_'+response.status+':'+await response.text());
    const result=await response.json(),check=validate(result,{sessionId:options.sessionId,sha256:options.sha256});
    if(check.status!=='PASS')throw new Error('MIE_RECOGNITION_CONTRACT_FAIL:'+check.reasons.join(','));
    return result;
  }
  return{SCHEMA,validate,base64Blob,analyze};
});
