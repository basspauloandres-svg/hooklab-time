import { chromium } from 'playwright';
import fs from 'node:fs';
import assert from 'node:assert/strict';
const URL='https://basspauloandres-svg.github.io/hooklab-time/producer-interface-v0.5/';
const wav='/tmp/hooklab-click120.wav';
function writeClick(path){const sr=22050,seconds=3,n=sr*seconds,b=Buffer.alloc(44+n*2);b.write('RIFF',0);b.writeUInt32LE(36+n*2,4);b.write('WAVE',8);b.write('fmt ',12);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(sr,24);b.writeUInt32LE(sr*2,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(n*2,40);for(let i=0;i<n;i++){const phase=i%(sr/2),v=phase<500?Math.round(16000*Math.sin(2*Math.PI*1000*phase/sr)*Math.exp(-phase/100)):0;b.writeInt16LE(v,44+i*2)}fs.writeFileSync(path,b)}
writeClick(wav);
const browser=await chromium.launch({headless:true,args:['--autoplay-policy=no-user-gesture-required']});
const page=await browser.newPage();
page.on('console',m=>console.log('BROWSER',m.type(),m.text()));
page.on('requestfailed',r=>console.log('REQUEST_FAILED',r.url(),r.failure()?.errorText));
await page.goto(URL,{waitUntil:'domcontentloaded',timeout:30000});
assert.match(await page.title(),/v0\.5/);
await page.locator('#ref').setInputFiles({name:'click120.wav',mimeType:'audio/wav',buffer:fs.readFileSync(wav)});
await page.waitForFunction(()=>document.querySelector('#refState')?.textContent?.includes('AUDIT_LOCAL_REFERENCE'));
const result=await page.evaluate(async()=>{
 const file=document.querySelector('#ref').files[0];
 const stages=[];
 try{
  const a=await HookLabLocalBeatThis.analyze(file,{sessionId:state.session_id,sha256:state.aesthetic_reference.sha256,onProgress:s=>{stages.push(s);console.log('HOOKLAB_STAGE',s)}});
  return {ok:true,a,stages};
 }catch(e){return {ok:false,error:String(e&&e.message||e),stages};}
});
console.log('DIRECT_RESULT',JSON.stringify(result));
if(!result.ok)throw new Error('LOCAL_ANALYZER_FAIL '+result.error+' stages='+result.stages.join('>'));
const a=result.a;
assert.equal(a.analysis_mode,'LOCAL_ON_DEVICE_ONNX');assert.equal(a.source_audio_persistence,'NONE');assert.equal(a.scientific_ingestion,false);assert.equal(a.gate_a_ingestion,false);assert(a.beat_count>1);assert(a.tempo_bpm_median>80&&a.tempo_bpm_median<160);
await browser.close();
console.log(JSON.stringify({status:'PASS',bpm:a.tempo_bpm_median,beats:a.beat_count,stages:result.stages,latency_ms:a.latency_ms},null,2));