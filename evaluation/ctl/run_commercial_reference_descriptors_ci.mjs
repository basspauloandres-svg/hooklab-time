import fs from 'fs';
import path from 'path';

const srcPath = path.resolve('evaluation/ctl/run_commercial_reference_descriptors.mjs');
const dstPath = path.resolve('evaluation/ctl/.run_commercial_reference_descriptors_ci.generated.mjs');
let s = fs.readFileSync(srcPath, 'utf8');

s = s.replace(
  "const m4a=path.join(outDir,`${ref.id}.m4a`),wav=path.join(outDir,`${ref.id}.wav`);",
  "const m4a=path.join(outDir,`${ref.id}.m4a`),wav=path.join(outDir,`${ref.id}.wav`),pcm=path.join(outDir,`${ref.id}.f32le`);"
);

s = s.replace(
  "execFileSync('ffmpeg',['-y','-i',m4a,'-ac','1','-ar','44100',wav],{stdio:'ignore'});",
  "execFileSync('ffmpeg',['-y','-i',m4a,'-ac','1','-ar','44100',wav],{stdio:'ignore'}); execFileSync('ffmpeg',['-y','-i',m4a,'-ac','1','-ar','22050','-f','f32le',pcm],{stdio:'ignore'});"
);

const oldBlock = "await page.setInputFiles('#f',wav); await page.click('#decode');\n    await page.waitForFunction(()=>{const s=document.querySelector('#ds')?.textContent||'';return s.includes('DECODE OK')||s.startsWith('ERROR');},null,{timeout:60000});\n    const ds=await page.textContent('#ds'); if(!ds.includes('DECODE OK'))throw new Error(`${ref.id} decode failed: ${ds}`);";

const newBlock = `await page.setInputFiles('#f',wav);\n    await page.evaluate(async (pcmUrl)=>{\n      const r=await fetch(pcmUrl); if(!r.ok) throw new Error('PCM HTTP '+r.status);\n      const ab=await r.arrayBuffer();\n      const source=new Float32Array(ab);\n      const data=new Float32Array(source.length); data.set(source);\n      buf={duration:data.length/22050,sampleRate:22050,length:data.length,numberOfChannels:1,getChannelData(c){if(c!==0)throw new Error('mono');return data;}};\n      document.querySelector('#ds').textContent='DECODE OK · DIRECT_PCM_CI · '+buf.duration.toFixed(6)+' s · 22050 Hz';\n      document.querySelector('#run').disabled=false;\n    }, 'http://127.0.0.1:8766/evaluation/ctl/commercial_reference_outputs/'+ref.id+'.f32le');\n    const ds=await page.textContent('#ds'); if(!ds.includes('DECODE OK'))throw new Error(\`${ref.id} direct PCM failed: \${ds}\`);`;

if (!s.includes(oldBlock)) throw new Error('CI adapter failed closed: decode block signature changed');
s = s.replace(oldBlock, newBlock);

s = s.replace(
  "if(p.endsWith('.wav'))res.setHeader('Content-Type','audio/wav');",
  "if(p.endsWith('.wav'))res.setHeader('Content-Type','audio/wav'); if(p.endsWith('.f32le'))res.setHeader('Content-Type','application/octet-stream');"
);

fs.writeFileSync(dstPath, s);
await import('file://' + dstPath + '?v=' + Date.now());
