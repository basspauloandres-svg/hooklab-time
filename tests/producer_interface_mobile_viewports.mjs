import { chromium, webkit } from 'playwright';
import fs from 'fs';

const URL=process.env.HOOKLAB_TEST_URL||'http://127.0.0.1:8000/app/prototype_v1/index.html';
const wav=Buffer.alloc(44+22050*2); // minimal 1 s mono PCM16 WAV
wav.write('RIFF',0); wav.writeUInt32LE(wav.length-8,4); wav.write('WAVEfmt ',8); wav.writeUInt32LE(16,16); wav.writeUInt16LE(1,20); wav.writeUInt16LE(1,22); wav.writeUInt32LE(22050,24); wav.writeUInt32LE(44100,28); wav.writeUInt16LE(2,32); wav.writeUInt16LE(16,34); wav.write('data',36); wav.writeUInt32LE(wav.length-44,40);
fs.writeFileSync('/tmp/hooklab_mobile.wav',wav);

const profiles=[
  {name:'iphone_webkit',launcher:webkit,viewport:{width:390,height:844}},
  {name:'android_chromium',launcher:chromium,viewport:{width:412,height:915}}
];

const results=[];
for(const p of profiles){
  const browser=await p.launcher.launch({headless:true});
  const page=await browser.newPage({viewport:p.viewport});
  page.setDefaultTimeout(15000);
  await page.goto(URL,{waitUntil:'domcontentloaded'});
  const title=await page.title();
  if(!/Producer Interface v0\.6/.test(title)) throw new Error(`${p.name}: bad title ${title}`);
  await page.waitForSelector('#hookAssistantCard');
  const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>document.documentElement.clientWidth+2);
  if(overflow) throw new Error(`${p.name}: horizontal overflow`);
  await page.setInputFiles('#ref',{name:'mobile-test.wav',mimeType:'audio/wav',buffer:wav});
  await page.waitForFunction(()=>!document.querySelector('#analyzeRef').disabled);
  const minButton=await page.evaluate(()=>Math.min(...[...document.querySelectorAll('button')].map(b=>b.getBoundingClientRect().height)));
  if(minButton<36) throw new Error(`${p.name}: touch targets too small ${minButton}`);
  await page.click('#midiBtn');
  await page.waitForFunction(()=>document.querySelector('#buildState').textContent.includes('D0 LISTO'));
  await page.fill('#assistantIntent','reencuentro');
  await page.click('#generateHookCandidates');
  await page.waitForFunction(()=>document.querySelectorAll('.useHookCandidate').length>=3);
  const candidateCount=await page.locator('.useHookCandidate').count();
  if(candidateCount<3) throw new Error(`${p.name}: multimodal candidates missing`);
  await page.locator('.useHookCandidate').first().click();
  const selectedText=await page.inputValue('#text');
  if(!selectedText.trim()) throw new Error(`${p.name}: candidate not transferred to lyric curation`);
  await page.selectOption('#decision',{label:'Modificar'});
  await page.fill('#reason','mobile regression');
  await page.click('#save');
  const saved=await page.evaluate(()=>Object.keys(localStorage).some(k=>k.startsWith('hooklab_session_')));
  if(!saved) throw new Error(`${p.name}: session not persisted`);
  results.push({profile:p.name,title,viewport:p.viewport,min_button_height:minButton,horizontal_overflow:false,d0:true,multimodal_candidates:candidateCount,candidate_selected:true,persisted:true});
  await browser.close();
}
console.log(JSON.stringify({status:'PASS',results},null,2));
