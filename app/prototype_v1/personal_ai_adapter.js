/* HookLab Personal AI Adapter v0.1
 * Personal research prototype. Provider-neutral. No secrets in browser.
 */
(function(root,factory){const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;root.HookLabPersonalAI=api;})(typeof globalThis!=='undefined'?globalThis:this,function(){
'use strict';
const VERSION='hooklab-personal-ai-adapter-v0.1';
const DEFAULT_ENDPOINT='http://127.0.0.1:8787/hooklab/ai/coherence';
function contract(){return{schema:'HOOKLAB_PERSONAL_AI_ADAPTER_CONTRACT_v0.1',version:VERSION,deployment_class:'PERSONAL_RESEARCH_PROTOTYPE',commercial_mode:false,multi_user_mode:false,secrets_in_browser:false,provider_neutral:true,default_endpoint:DEFAULT_ENDPOINT};}
async function health(endpoint=DEFAULT_ENDPOINT){try{const r=await fetch(endpoint.replace(/\/coherence$/,'/health'),{method:'GET'});if(!r.ok)return{status:'AI_ADAPTER_OFFLINE',http_status:r.status};const j=await r.json();return{status:j?.status==='READY'?'AI_ADAPTER_READY':'AI_ADAPTER_NOT_READY',remote:j};}catch(e){return{status:'AI_ADAPTER_OFFLINE',reason:e.message};}}
async function reason(payload,opts={}){const endpoint=opts.endpoint||DEFAULT_ENDPOINT;const h=await health(endpoint);if(h.status!=='AI_ADAPTER_READY')return{status:'AI_REASONING_LOCKED',reason:h.status,health:h};const body={schema:'HOOKLAB_AI_REQUEST_v0.1',request_id:'AIREQ-'+Date.now(),requested_at:new Date().toISOString(),task:'COHERENCE_AND_SECTION_REALIZATION',payload};const r=await fetch(endpoint,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});if(!r.ok)return{status:'AI_REASONING_FAIL',http_status:r.status};const j=await r.json();if(!j||j.schema!=='HOOKLAB_AI_RESPONSE_v0.1')return{status:'AI_REASONING_FAIL',reason:'INVALID_RESPONSE_SCHEMA'};return j;}
return{VERSION,DEFAULT_ENDPOINT,contract,health,reason};
});