import fs from 'node:fs';
import assert from 'node:assert/strict';
import { chromium } from 'playwright';

const AUDIO=process.env.TEST_AUDIO||'/tmp/hooklab_test.wav';
const CLI_BEATS=process.env.CLI_BEATS||'/tmp/hooklab_cli.beats';
const BASE_URL=process.env.TEST_URL||'http://127.0.0.1:8000/tests/fixtures/local_beat_this_equivalence.html';
const BPM_REL_TOL=0.03;
const BEAT_COUNT_REL_TOL=0.15;
const MEDIAN_NEAREST_TOL_S=0.10;

function median(a){const x=[...a].sort((p,q)=>p-q);if(!x.length)return null;const m=Math.floor(x.length/2);return x.length%2?x[m]:(x[m-1]+x[m])/2;}
function bpm(beats){const d=[];for(let i=1;i<beats.length;i++)if(beats[i]>beats[i-1])d.push(beats[i]-beats[i-1]);const m=median(d);return m?60/m:null;}
const cli=fs.readFileSync(CLI_BEATS,'utf8').split(/\r?\n/).map(x=>x.trim()).filter(Boolean).map(x=>Number(x.split(/\s+/)[0])).filter(Number.isFinite);
assert(cli.length>4,'CLI beat reference is empty');

const browser=await chromium.launch({headless:true});
const page=await browser.newPage();
page.setDefaultTimeout(180000);
await page.goto(BASE_URL,{waitUntil:'domcontentloaded'});
await page.setInputFiles('#audio',AUDIO);
const result=await page.evaluate(async()=>{
  const file=document.querySelector('#audio').files[0];
  const b=await file.arrayBuffer();
  const h=await crypto.subtle.digest('SHA-256',b);
  const sha=[...new Uint8Array(h)].map(x=>x.toString(16).padStart(2,'0')).join('');
  return await HookLabLocalBeatThis.analyze(file,{sessionId:'HL-EQUIV',sha256:sha});
});
await browser.close();
assert.equal(result.status,'PASS');
assert.equal(result.analysis_mode,'LOCAL_ON_DEVICE_ONNX');
const local=result.beat_times_s;
assert(local.length>4,'Browser beat result is empty');
const cliBpm=bpm(cli),localBpm=result.tempo_bpm_median;
const bpmRel=Math.abs(localBpm-cliBpm)/cliBpm;
const beatCountRel=Math.abs(local.length-cli.length)/cli.length;
const nearest=local.map(x=>Math.min(...cli.map(y=>Math.abs(x-y))));
const medNearest=median(nearest);
const report={status:'PASS',thresholds:{bpm_relative_max:BPM_REL_TOL,beat_count_relative_max:BEAT_COUNT_REL_TOL,median_nearest_beat_error_s_max:MEDIAN_NEAREST_TOL_S},observed:{cli_bpm:cliBpm,local_bpm:localBpm,bpm_relative_error:bpmRel,cli_beats:cli.length,local_beats:local.length,beat_count_relative_error:beatCountRel,median_nearest_beat_error_s:medNearest},browser_result:result};
if(bpmRel>BPM_REL_TOL||beatCountRel>BEAT_COUNT_REL_TOL||medNearest>MEDIAN_NEAREST_TOL_S)report.status='FAIL';
fs.writeFileSync('local_beat_this_equivalence_report.json',JSON.stringify(report,null,2));
console.log(JSON.stringify(report,null,2));
if(report.status!=='PASS')process.exit(2);
