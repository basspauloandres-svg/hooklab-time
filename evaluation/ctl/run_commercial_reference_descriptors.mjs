import { chromium } from 'playwright';
import fs from 'fs';
import { execFileSync } from 'child_process';
import path from 'path';
import http from 'http';

const TARGETS = [
  {id:'CREF01', title:'Danza Kuduro', artist:'Don Omar'},
  {id:'CREF02', title:'Despacito', artist:'Luis Fonsi'},
  {id:'CREF03', title:'Mi Gente', artist:'J Balvin'},
  {id:'CREF04', title:'Pepas', artist:'Farruko'},
  {id:'CREF05', title:'Tití Me Preguntó', artist:'Bad Bunny'},
  {id:'CREF06', title:'Papasito', artist:'KAROL G'}
];

const root = process.cwd();
const outDir = path.join(root,'evaluation','ctl','commercial_reference_outputs');
fs.mkdirSync(outDir,{recursive:true});
const appName='app-mie-unified-transcription-v0.1.1.html';
const app = path.join(root,appName);
if(!fs.existsSync(app)) throw new Error('Missing unified MIE app');

function norm(s){return String(s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim();}
function tokens(s){return new Set(norm(s).split(/\s+/).filter(Boolean));}
function overlap(a,b){const A=tokens(a),B=tokens(b); if(!A.size||!B.size)return 0; let n=0; for(const x of A)if(B.has(x))n++; return n/Math.max(A.size,B.size);}
function median(xs){if(!xs.length)return null; const z=xs.slice().sort((a,b)=>a-b),m=Math.floor(z.length/2); return z.length%2?z[m]:(z[m-1]+z[m])/2;}
function mean(xs){return xs.length?xs.reduce((a,b)=>a+b,0)/xs.length:null;}
function q(v,step=.25){return Math.round(v/step)*step;}
function histogram(xs){const m=new Map(); for(const x of xs)m.set(String(x),(m.get(String(x))||0)+1); return Object.fromEntries([...m.entries()].sort((a,b)=>b[1]-a[1]));}
function entropy(xs){if(!xs.length)return null; const h=histogram(xs),n=xs.length; let e=0; for(const c of Object.values(h)){const p=c/n;e-=p*Math.log2(p);} return +e.toFixed(4);}
function topNgrams(seq,n,top=8){const m=new Map(); for(let i=0;i+n<=seq.length;i++){const k=seq.slice(i,i+n).join('|');m.set(k,(m.get(k)||0)+1);} return [...m.entries()].sort((a,b)=>b[1]-a[1]||a[0].localeCompare(b[0])).slice(0,top).map(([pattern,count])=>({pattern,count}));}
function repeatedNgramShare(seq,n){const total=Math.max(0,seq.length-n+1); if(!total)return null; const m=new Map(); for(let i=0;i+n<=seq.length;i++){const k=seq.slice(i,i+n).join('|');m.set(k,(m.get(k)||0)+1);} let repeated=0; for(const c of m.values())if(c>1)repeated+=c; return +(repeated/total).toFixed(4);}
function longestRepeatedJoint(events,beatSec){
  if(events.length<6||!beatSec)return null;
  const units=[];
  for(let i=1;i<events.length;i++){
    const interval=events[i].m-events[i-1].m;
    const ioi=q((events[i].on-events[i-1].on)/beatSec,.25);
    units.push(`${interval}@${ioi}`);
  }
  for(let n=Math.min(10,Math.floor(units.length/2));n>=3;n--){
    const seen=new Map();
    for(let i=0;i+n<=units.length;i++){
      const k=units.slice(i,i+n).join('|');
      const arr=seen.get(k)||[]; arr.push(i); seen.set(k,arr);
    }
    for(const [pattern,positions] of seen){
      if(positions.length<2)continue;
      let nonOverlap=false;
      for(let i=0;i<positions.length;i++)for(let j=i+1;j<positions.length;j++)if(Math.abs(positions[j]-positions[i])>=n)nonOverlap=true;
      if(nonOverlap)return {length_transitions:n,events:n+1,pattern,occurrences:positions.length,positions};
    }
  }
  return null;
}
function phrases(events,beatSec){
  if(!events.length||!beatSec)return [];
  const out=[]; let start=0;
  for(let i=1;i<events.length;i++){
    const gap=(events[i].on-events[i-1].off)/beatSec;
    if(gap>=1.25){out.push(events.slice(start,i));start=i;}
  }
  out.push(events.slice(start)); return out.filter(x=>x.length>=2);
}
function descriptors(result){
  const events=(Array.isArray(result.melody)?result.melody:[]).map(e=>({on:+e.on,off:+e.off,m:Math.round(+e.m)})).filter(e=>Number.isFinite(e.on)&&Number.isFinite(e.off)&&Number.isFinite(e.m)&&e.off>e.on).sort((a,b)=>a.on-b.on);
  const beats=(Array.isArray(result.beats)?result.beats:[]).map(Number).filter(Number.isFinite).sort((a,b)=>a-b);
  const ibis=[]; for(let i=1;i<beats.length;i++){const d=beats[i]-beats[i-1];if(d>=.25&&d<=2)ibis.push(d);} const beatSec=median(ibis);
  const bpm=beatSec?60/beatSec:null;
  const intervals=[],iois=[],durations=[];
  for(let i=0;i<events.length;i++){
    durations.push(q((events[i].off-events[i].on)/(beatSec||1),.25));
    if(i){intervals.push(events[i].m-events[i-1].m);iois.push(q((events[i].on-events[i-1].on)/(beatSec||1),.25));}
  }
  const absIntervals=intervals.map(Math.abs);
  const pitchSet=[...new Set(events.map(e=>e.m))];
  const phraseList=phrases(events,beatSec);
  const phraseEvents=phraseList.map(p=>p.length), phraseBeats=phraseList.map(p=>(p[p.length-1].off-p[0].on)/(beatSec||1));
  const joint=longestRepeatedJoint(events,beatSec);
  const jointUnits=[]; for(let i=1;i<events.length;i++)jointUnits.push(`${events[i].m-events[i-1].m}@${q((events[i].on-events[i-1].on)/(beatSec||1),.25)}`);
  return {
    tempo_bpm:bpm?+bpm.toFixed(3):null,
    beat_count:beats.length,
    melodic_event_count:events.length,
    unique_pitch_count:pitchSet.length,
    melodic_range_semitones:pitchSet.length?Math.max(...pitchSet)-Math.min(...pitchSet):null,
    repeated_pitch_transition_share:intervals.length?+(intervals.filter(x=>x===0).length/intervals.length).toFixed(4):null,
    stepwise_transition_share:intervals.length?+(absIntervals.filter(x=>x<=2).length/intervals.length).toFixed(4):null,
    leap_ge5_transition_share:intervals.length?+(absIntervals.filter(x=>x>=5).length/intervals.length).toFixed(4):null,
    mean_abs_interval_semitones:absIntervals.length?+mean(absIntervals).toFixed(4):null,
    interval_entropy_bits:entropy(intervals),
    rhythm_ioi_entropy_bits:entropy(iois),
    duration_entropy_bits:entropy(durations),
    interval_histogram:histogram(intervals),
    ioi_beats_histogram:histogram(iois),
    duration_beats_histogram:histogram(durations),
    melodic_interval_trigrams:topNgrams(intervals,3),
    rhythmic_ioi_trigrams:topNgrams(iois,3),
    joint_interval_ioi_trigrams:topNgrams(jointUnits,3),
    melodic_trigram_repetition_share:repeatedNgramShare(intervals,3),
    rhythmic_trigram_repetition_share:repeatedNgramShare(iois,3),
    joint_trigram_repetition_share:repeatedNgramShare(jointUnits,3),
    longest_repeated_joint_ngram:joint,
    phrase_count:phraseList.length,
    phrase_event_count_median:phraseEvents.length?median(phraseEvents):null,
    phrase_length_beats_median:phraseBeats.length?+median(phraseBeats).toFixed(4):null,
    analysis_scope:'APPLE_MUSIC_PREVIEW_WINDOW_NOT_VERIFIED_CHORUS',
    scientific_status:'DESCRIPTIVE_REFERENCE_ONLY'
  };
}

async function resolvePreview(target){
  const term=encodeURIComponent(`${target.title} ${target.artist}`);
  const url=`https://itunes.apple.com/search?term=${term}&entity=song&limit=15&country=US`;
  const r=await fetch(url); if(!r.ok)throw new Error(`iTunes search HTTP ${r.status}`);
  const data=await r.json();
  const scored=(data.results||[]).filter(x=>x.previewUrl).map(x=>({x,score:2*overlap(target.title,x.trackName)+overlap(target.artist,x.artistName)})).sort((a,b)=>b.score-a.score);
  if(!scored.length)throw new Error(`No preview for ${target.title}`);
  const best=scored[0];
  if(best.score<1.2)throw new Error(`Low-confidence iTunes identity match for ${target.title}: ${best.x.trackName} — ${best.x.artistName}`);
  return {...target, preview_url:best.x.previewUrl, resolved_title:best.x.trackName, resolved_artist:best.x.artistName, collection:best.x.collectionName, track_id:best.x.trackId, identity_score:+best.score.toFixed(4)};
}

async function download(url,dest){const r=await fetch(url);if(!r.ok)throw new Error(`HTTP ${r.status} ${url}`);fs.writeFileSync(dest,Buffer.from(await r.arrayBuffer()));}

const server=http.createServer((req,res)=>{
  const p=path.join(root,decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/,''));
  if(!p.startsWith(root)||!fs.existsSync(p)||fs.statSync(p).isDirectory()){res.statusCode=404;return res.end('not found');}
  if(p.endsWith('.html'))res.setHeader('Content-Type','text/html; charset=utf-8');
  if(p.endsWith('.wav'))res.setHeader('Content-Type','audio/wav');
  res.setHeader('Access-Control-Allow-Origin','*');fs.createReadStream(p).pipe(res);
});
await new Promise(ok=>server.listen(8766,'127.0.0.1',ok));

const browser=await chromium.launch({headless:true,args:['--autoplay-policy=no-user-gesture-required']});
const summaries=[];
try{
  for(const target of TARGETS){
    const ref=await resolvePreview(target);
    const m4a=path.join(outDir,`${ref.id}.m4a`),wav=path.join(outDir,`${ref.id}.wav`);
    await download(ref.preview_url,m4a);
    execFileSync('ffmpeg',['-y','-i',m4a,'-ac','1','-ar','44100',wav],{stdio:'ignore'});
    const page=await browser.newPage();
    await page.goto(`http://127.0.0.1:8766/${appName}`,{waitUntil:'load'});
    await page.setInputFiles('#f',wav); await page.click('#decode');
    await page.waitForFunction(()=>{const s=document.querySelector('#ds')?.textContent||'';return s.includes('DECODE OK')||s.startsWith('ERROR');},null,{timeout:60000});
    const ds=await page.textContent('#ds'); if(!ds.includes('DECODE OK'))throw new Error(`${ref.id} decode failed: ${ds}`);
    await page.click('#run');
    await page.waitForFunction(()=>{const s=document.querySelector('#st')?.textContent||'';return s.startsWith('LISTO')||s.startsWith('ERROR');},null,{timeout:240000});
    const st=await page.textContent('#st'); if(!st.startsWith('LISTO'))throw new Error(`${ref.id} analysis failed: ${st}`);
    const result=await page.evaluate(()=>result);
    const row={reference:ref, descriptors:descriptors(result), engine:'MIE_UNIFIED_v0.1.1'};
    fs.writeFileSync(path.join(outDir,`${ref.id}_DESCRIPTORS.json`),JSON.stringify(row,null,2));
    summaries.push(row); await page.close();
  }
} finally {await browser.close();await new Promise(ok=>server.close(ok));}

function vals(key){return summaries.map(x=>x.descriptors[key]).filter(Number.isFinite);}
const aggregate={
  schema:'HOOKLAB_COMMERCIAL_REFERENCE_RHYTHM_MELODY_DESCRIPTORS_v0.1',
  status:'DESCRIPTIVE_REFERENCE_ONLY',
  n:summaries.length,
  scope:'Automated Apple Music preview windows analyzed by existing MIE unified transcription; windows are not asserted to be choruses unless independently verified.',
  references:summaries,
  aggregate:{
    tempo_bpm_median:median(vals('tempo_bpm')),
    melodic_event_count_median:median(vals('melodic_event_count')),
    unique_pitch_count_median:median(vals('unique_pitch_count')),
    melodic_range_semitones_median:median(vals('melodic_range_semitones')),
    repeated_pitch_transition_share_median:median(vals('repeated_pitch_transition_share')),
    stepwise_transition_share_median:median(vals('stepwise_transition_share')),
    leap_ge5_transition_share_median:median(vals('leap_ge5_transition_share')),
    mean_abs_interval_semitones_median:median(vals('mean_abs_interval_semitones')),
    interval_entropy_bits_median:median(vals('interval_entropy_bits')),
    rhythm_ioi_entropy_bits_median:median(vals('rhythm_ioi_entropy_bits')),
    duration_entropy_bits_median:median(vals('duration_entropy_bits')),
    melodic_trigram_repetition_share_median:median(vals('melodic_trigram_repetition_share')),
    rhythmic_trigram_repetition_share_median:median(vals('rhythmic_trigram_repetition_share')),
    joint_trigram_repetition_share_median:median(vals('joint_trigram_repetition_share')),
    phrase_event_count_median:median(vals('phrase_event_count_median')),
    phrase_length_beats_median:median(vals('phrase_length_beats_median'))
  }
};
fs.writeFileSync(path.join(outDir,'COMMERCIAL_REFERENCE_DESCRIPTORS_v0.1.json'),JSON.stringify(aggregate,null,2));
console.log(JSON.stringify(aggregate,null,2));
