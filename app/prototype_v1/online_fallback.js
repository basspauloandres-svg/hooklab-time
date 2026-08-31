(function(g){
  'use strict';
  const KEY='hooklab_fallback_endpoint';
  function endpoint(){
    const v=(localStorage.getItem(KEY)||g.HOOKLAB_FALLBACK_ENDPOINT||'').trim();
    return v.replace(/\/$/,'');
  }
  function configured(){ return !!endpoint(); }
  function setEndpoint(url){
    if(!url){ localStorage.removeItem(KEY); return; }
    localStorage.setItem(KEY,String(url).replace(/\/$/,''));
  }
  async function health(){
    if(!configured()) return {status:'UNCONFIGURED'};
    const r=await fetch(endpoint()+'/health',{method:'GET'});
    if(!r.ok) throw new Error('FALLBACK_HEALTH_'+r.status);
    return r.json();
  }
  async function analyze(file,{sessionId,sha256}={}){
    if(!configured()) throw new Error('ONLINE_FALLBACK_UNCONFIGURED');
    if(!file || !file.type || !file.type.startsWith('audio/')) throw new Error('AUDIO_MIME_REQUIRED');
    if(!sessionId || !sha256) throw new Error('SESSION_ID_AND_SHA_REQUIRED');
    const fd=new FormData();
    fd.append('audio',file,file.name||'reference.wav');
    fd.append('session_id',sessionId);
    fd.append('sha256',sha256);
    const r=await fetch(endpoint()+'/v1/analyze-reference',{method:'POST',body:fd});
    let body={}; try{body=await r.json()}catch(_e){}
    if(!r.ok) throw new Error(body.detail||('ONLINE_FALLBACK_HTTP_'+r.status));
    if(body.reference_sha256 && body.reference_sha256!==sha256) throw new Error('SHA256_SESSION_MISMATCH');
    body.analysis_mode='ONLINE_API_FALLBACK';
    body.scientific_ingestion=false;
    body.gate_a_ingestion=false;
    body.m300_ingestion=false;
    body.success_evidence_ingestion=false;
    return body;
  }
  g.HookLabOnlineFallback={configured,setEndpoint,endpoint,health,analyze};
})(window);
