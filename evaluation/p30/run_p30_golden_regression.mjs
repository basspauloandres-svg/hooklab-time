import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { pathToFileURL } from 'url';

const root=process.cwd();
const html=path.join(root,'app-mie-p30-harmony-beat-v0.1.html');
const outDir=path.join(root,'evaluation','p30','outputs');
fs.mkdirSync(outDir,{recursive:true});
const expected='de8381ef9322e73bf295db40a9dffeb0528469502313ea949c4c9018fe9cd940';
if(!fs.existsSync(html)) throw new Error('Golden P30 renderer missing');

const browser=await chromium.launch({headless:true});
try{
  const page=await browser.newPage();
  page.on('pageerror',e=>console.error('PAGEERROR',e.message));
  await page.goto(pathToFileURL(html).href,{waitUntil:'load'});
  await page.click('#render');
  await page.waitForFunction(()=>document.querySelector('#st')?.textContent?.startsWith('LISTO'),{timeout:120000});
  const bytes=await page.evaluate(async()=>{
    const src=document.querySelector('#out')?.src;
    if(!src) throw new Error('No rendered audio src');
    const ab=await (await fetch(src)).arrayBuffer();
    return Array.from(new Uint8Array(ab));
  });
  const buf=Buffer.from(bytes);
  const wav=path.join(outDir,'P30_GOLDEN_REPRODUCED.wav');
  fs.writeFileSync(wav,buf);
  const sha=crypto.createHash('sha256').update(buf).digest('hex');
  const report={
    test:'P30_GOLDEN_REGRESSION',
    renderer:'app-mie-p30-harmony-beat-v0.1.html',
    expected_sha256:expected,
    actual_sha256:sha,
    byte_count:buf.length,
    pass:sha===expected,
    invariants:{window_s:[13.3,40.7],melody:'P30-SCORE-002',harmony:'Harmony B',beat:'Beat This v1.9.3'}
  };
  fs.writeFileSync(path.join(outDir,'P30_GOLDEN_REGRESSION.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  if(!report.pass) process.exitCode=2;
}finally{
  await browser.close();
}
