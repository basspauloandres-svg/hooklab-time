import { chromium } from 'playwright';
import fs from 'fs';
import { execFileSync } from 'child_process';
import path from 'path';

const refs = [
  {id:'R03', title:'Color Esperanza', artist:'Diego Torres', url:'https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview112/v4/cb/aa/e3/cbaae307-6041-f1c3-f2e5-8d4431caf400/mzaf_12497882098216135100.plus.aac.p.m4a'},
  {id:'R02', title:'Latinoamérica', artist:'Calle 13', url:'https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/54/aa/4c/54aa4c12-3c52-a0e8-4ad5-c98ca93f3c2d/mzaf_5496000771296428020.plus.aac.p.m4a'},
  {id:'R04', title:'Oliveira Dos Cen Anos', artist:'C. Tangana', url:'https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview126/v4/7a/a3/69/7aa369c8-8e91-9237-2488-577ff8375e07/mzaf_12014619421289819217.plus.aac.p.m4a'}
];

const root = process.cwd();
const outDir = path.join(root,'evaluation','ctl','reference_batch_outputs');
fs.mkdirSync(outDir,{recursive:true});
const app = path.join(root,'app-mie-unified-transcription-v0.1.1.html');
if(!fs.existsSync(app)) throw new Error('Missing unified MIE app');

async function download(url, dest){
  const r = await fetch(url);
  if(!r.ok) throw new Error(`HTTP ${r.status} ${url}`);
  fs.writeFileSync(dest, Buffer.from(await r.arrayBuffer()));
}

const browser = await chromium.launch({headless:true});
try {
  for(const ref of refs){
    const m4a=path.join(outDir,`${ref.id}.m4a`), wav=path.join(outDir,`${ref.id}.wav`);
    await download(ref.url,m4a);
    execFileSync('ffmpeg',['-y','-i',m4a,'-ac','1','-ar','44100',wav],{stdio:'ignore'});
    const page=await browser.newPage({acceptDownloads:true});
    await page.goto('file://'+app);
    await page.setInputFiles('#f',wav);
    await page.click('#decode');
    await page.waitForFunction(()=>document.querySelector('#ds').textContent.includes('DECODE OK'),{timeout:30000});
    await page.click('#run');
    await page.waitForFunction(()=>document.querySelector('#st').textContent.startsWith('LISTO'),{timeout:180000});
    const result=await page.evaluate(()=>result);
    result.reference={id:ref.id,title:ref.title,artist:ref.artist,preview_url:ref.url};
    fs.writeFileSync(path.join(outDir,`${ref.id}_MIE.json`),JSON.stringify(result,null,2));
    await page.close();
  }
} finally { await browser.close(); }
