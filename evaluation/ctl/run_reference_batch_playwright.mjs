import { chromium } from 'playwright';
import fs from 'fs';
import { execFileSync } from 'child_process';
import path from 'path';
import http from 'http';

const refs = [
  {id:'R03', title:'Color Esperanza', artist:'Diego Torres', url:'https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview112/v4/cb/aa/e3/cbaae307-6041-f1c3-f2e5-8d4431caf400/mzaf_12497882098216135100.plus.aac.p.m4a'},
  {id:'R02', title:'Latinoamérica', artist:'Calle 13', url:'https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview115/v4/54/aa/4c/54aa4c12-3c52-a0e8-4ad5-c98ca93f3c2d/mzaf_5496000771296428020.plus.aac.p.m4a'},
  {id:'R04', title:'Oliveira Dos Cen Anos', artist:'C. Tangana', url:'https://audio-ssl.itunes.apple.com/itunes-assets/AudioPreview126/v4/7a/a3/69/7aa369c8-8e91-9237-2488-577ff8375e07/mzaf_12014619421289819217.plus.aac.p.m4a'}
];

const root = process.cwd();
const outDir = path.join(root,'evaluation','ctl','reference_batch_outputs');
fs.mkdirSync(outDir,{recursive:true});
const appName='app-mie-unified-transcription-v0.1.1.html';
const app = path.join(root,appName);
if(!fs.existsSync(app)) throw new Error('Missing unified MIE app');

async function download(url, dest){
  const r = await fetch(url);
  if(!r.ok) throw new Error(`HTTP ${r.status} ${url}`);
  fs.writeFileSync(dest, Buffer.from(await r.arrayBuffer()));
}

const server=http.createServer((req,res)=>{
  const p=path.join(root, decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/,''));
  if(!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) {res.statusCode=404;return res.end('not found');}
  if(p.endsWith('.html')) res.setHeader('Content-Type','text/html; charset=utf-8');
  if(p.endsWith('.wav')) res.setHeader('Content-Type','audio/wav');
  res.setHeader('Access-Control-Allow-Origin','*');
  fs.createReadStream(p).pipe(res);
});
await new Promise(ok=>server.listen(8765,'127.0.0.1',ok));

const browser = await chromium.launch({headless:true,args:['--autoplay-policy=no-user-gesture-required']});
try {
  for(const ref of refs){
    const m4a=path.join(outDir,`${ref.id}.m4a`), wav=path.join(outDir,`${ref.id}.wav`);
    console.log(`DOWNLOAD ${ref.id}`);
    await download(ref.url,m4a);
    execFileSync('ffmpeg',['-y','-i',m4a,'-ac','1','-ar','44100',wav],{stdio:'ignore'});
    console.log(`WAV ${ref.id} ${fs.statSync(wav).size} bytes`);
    const page=await browser.newPage({acceptDownloads:true});
    page.on('console',m=>console.log(`[browser ${ref.id}] ${m.type()}: ${m.text()}`));
    page.on('pageerror',e=>console.log(`[pageerror ${ref.id}] ${e.message}`));
    await page.goto(`http://127.0.0.1:8765/${appName}`,{waitUntil:'load'});
    await page.setInputFiles('#f',wav);
    await page.click('#decode');
    await page.waitForFunction(()=>{const s=document.querySelector('#ds')?.textContent||'';return s.includes('DECODE OK')||s.startsWith('ERROR');},{timeout:60000});
    const ds=await page.textContent('#ds'); console.log(`DECODE ${ref.id}: ${ds}`);
    if(!ds.includes('DECODE OK')) throw new Error(`${ref.id} decode failed: ${ds}`);
    await page.click('#run');
    await page.waitForFunction(()=>{const s=document.querySelector('#st')?.textContent||'';return s.startsWith('LISTO')||s.startsWith('ERROR');},{timeout:240000});
    const st=await page.textContent('#st'); console.log(`ANALYZE ${ref.id}: ${st}`);
    if(!st.startsWith('LISTO')) throw new Error(`${ref.id} analysis failed: ${st}`);
    const result=await page.evaluate(()=>result);
    result.reference={id:ref.id,title:ref.title,artist:ref.artist,preview_url:ref.url};
    fs.writeFileSync(path.join(outDir,`${ref.id}_MIE.json`),JSON.stringify(result,null,2));
    await page.close();
  }
} finally {
  await browser.close();
  await new Promise(ok=>server.close(ok));
}
