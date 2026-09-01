import fs from 'node:fs';
import vm from 'node:vm';
class LS{constructor(){this.m=new Map()}getItem(k){return this.m.get(k)||null}setItem(k,v){this.m.set(k,String(v))}removeItem(k){this.m.delete(k)}}
class FD{constructor(){this.items=[]}append(...x){this.items.push(x)}}
const localStorage=new LS();
let requested=[];
const context={window:{},localStorage,FormData:FD,fetch:async(url,opts={})=>{requested.push({url,opts}); if(url.endsWith('/health')) return {ok:true,json:async()=>({status:'ok'})}; return {ok:true,json:async()=>({reference_sha256:'abc',tempo_bpm_median:120,beat_count:4})};}};
context.window=context;
vm.createContext(context);
vm.runInContext(fs.readFileSync('app/prototype_v1/online_fallback.js','utf8'),context);
const A=context.HookLabOnlineFallback;
if(A.configured()) throw new Error('must start unconfigured');
A.setEndpoint('https://api.example.test/');
if(A.endpoint()!=='https://api.example.test') throw new Error('endpoint normalize fail');
const h=await A.health(); if(h.status!=='ok') throw new Error('health fail');
const f={type:'audio/wav',name:'x.wav'};
const r=await A.analyze(f,{sessionId:'HL-1',sha256:'abc'});
if(r.analysis_mode!=='ONLINE_API_FALLBACK') throw new Error('mode fail');
if(r.scientific_ingestion!==false||r.gate_a_ingestion!==false||r.m300_ingestion!==false) throw new Error('scientific isolation fail');
if(!requested.some(x=>x.url.endsWith('/v1/analyze-reference'))) throw new Error('request missing');
console.log('PASS online fallback client contract');
