import { chromium } from 'playwright';
import fs from 'node:fs';
import assert from 'node:assert/strict';

const URL='https://basspauloandres-svg.github.io/hooklab-time/producer-interface-v0.4/';
const wav='/tmp/hooklab-v04.wav';
function writeWav(path){const sr=8000,samples=sr,dataSize=samples*2,b=Buffer.alloc(44+dataSize);b.write('RIFF',0);b.writeUInt32LE(36+dataSize,4);b.write('WAVE',8);b.write('fmt ',12);b.writeUInt32LE(16,16);b.writeUInt16LE(1,20);b.writeUInt16LE(1,22);b.writeUInt32LE(sr,24);b.writeUInt32LE(sr*2,28);b.writeUInt16LE(2,32);b.writeUInt16LE(16,34);b.write('data',36);b.writeUInt32LE(dataSize,40);fs.writeFileSync(path,b)}
writeWav(wav);
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({acceptDownloads:true});
page.setDefaultTimeout(12000);
let ready=false;
for(let i=0;i<12;i++){try{await page.goto(URL,{waitUntil:'domcontentloaded',timeout:15000});if(/Producer Interface v0\.4/.test(await page.title())){ready=true;break}}catch{}await new Promise(r=>setTimeout(r,5000))}
assert.equal(ready,true,'v0.4 Pages route did not become ready');
assert.equal(await page.locator('#analyzeRef').count(),1);
assert.equal(await page.locator('#analyzerEndpoint').count(),1);
await page.locator('#ref').setInputFiles({name:'synthetic.wav',mimeType:'audio/wav',buffer:fs.readFileSync(wav)});
await page.waitForFunction(()=>document.querySelector('#refState')?.textContent?.includes('AUDIT_LOCAL_REFERENCE'));
await page.locator('#analyzeRef').click();
assert.match(await page.locator('#analysisState').innerText(),/BACKEND_NOT_PROVISIONED/);
const info=await page.evaluate(()=>({sid:document.querySelector('#sessionId').textContent,sha:state.aesthetic_reference.sha256}));
await page.route('https://hooklab.test/analyze',async route=>{
  await route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({schema:'HOOKLAB_AESTHETIC_REFERENCE_ANALYSIS_v0.1',status:'PASS',reasons:[],session_id:info.sid,role:'AESTHETIC_REFERENCE_ANALYSIS',semantics:'DESCRIPTIVE_SESSION_REFERENCE_ONLY',scientific_ingestion:false,gate_a_ingestion:false,m300_ingestion:false,success_evidence_ingestion:false,source_audio_persistence:'NONE',reference_sha256:info.sha,duration_s:1,tempo_bpm_median:123.45,beat_count:2,beat_times_s:[0.1,0.58],beat_sensor:'Beat This',beat_status:'VALID',melody_event_count:0,melody_range_raw:[null,null],sensor_version:'TEST',beat_model_sha256:'test',mel_model_sha256:'test'})});
});
await page.locator('#analyzerEndpoint').fill('https://hooklab.test/analyze');
await page.locator('#saveEndpoint').click();
await page.locator('#analyzeRef').click();
await page.waitForFunction(()=>document.querySelector('#analysisState')?.textContent?.includes('ANALYSIS PASS'));
const panel=await page.locator('#analysisPanel').innerText();
assert.match(panel,/123\.45 BPM/);assert.match(panel,/Beat This/);assert.match(panel,/Persistencia audio\s*NONE/);
await page.locator('#midiBtn').click();
assert.match(await page.locator('#buildState').innerText(),/D0 LISTO/);
for(const value of ['thetic','anacrustic','syncopated']){await page.locator('#variant').selectOption(value);assert.equal(await page.locator('#downloadMidi').isEnabled(),true)}
const midPromise=page.waitForEvent('download');await page.locator('#downloadMidi').click();const mid=await midPromise;const mp=await mid.path();assert.equal(fs.readFileSync(mp).subarray(0,4).toString(),'MThd');
const manPromise=page.waitForEvent('download');await page.locator('#downloadManifest').click();const man=await manPromise;const obj=JSON.parse(fs.readFileSync(await man.path(),'utf8'));assert.equal(obj.stimulus_class,'D0_EXPLORATORY');assert.equal(obj.scientific_d,'BLOCKED');
await page.locator('#save').click();
const saved=await page.evaluate(()=>JSON.parse(localStorage.getItem('hooklab_session_'+document.querySelector('#sessionId').textContent)));
assert.equal(saved.aesthetic_reference_analysis.role,'AESTHETIC_REFERENCE_ANALYSIS');assert.equal(saved.aesthetic_reference_analysis.scientific_ingestion,false);assert.equal(saved.scientific_state.scientific_d,'BLOCKED');
await browser.close();
console.log('PASS Producer Interface v0.4 browser regression with mocked analyzer transport');
