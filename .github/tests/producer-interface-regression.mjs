import { chromium } from 'playwright';
import fs from 'node:fs';
import assert from 'node:assert/strict';

const URL = process.env.HOOKLAB_URL || 'https://basspauloandres-svg.github.io/hooklab-time/';
const wavPath = '/tmp/hooklab-reference.wav';

function writeSilentWav(path, seconds=1, sampleRate=8000) {
  const samples = sampleRate * seconds;
  const dataSize = samples * 2;
  const b = Buffer.alloc(44 + dataSize);
  b.write('RIFF', 0); b.writeUInt32LE(36 + dataSize, 4); b.write('WAVE', 8);
  b.write('fmt ', 12); b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20); b.writeUInt16LE(1, 22);
  b.writeUInt32LE(sampleRate, 24); b.writeUInt32LE(sampleRate * 2, 28); b.writeUInt16LE(2, 32); b.writeUInt16LE(16, 34);
  b.write('data', 36); b.writeUInt32LE(dataSize, 40);
  fs.writeFileSync(path, b);
}

writeSilentWav(wavPath);
const browser = await chromium.launch({headless:true});
const page = await browser.newPage({acceptDownloads:true});
page.setDefaultTimeout(10000);
page.setDefaultNavigationTimeout(20000);
const failures = [];
const check = async (name, fn) => {
  try { await fn(); console.log(`PASS ${name}`); }
  catch (e) { failures.push(`${name}: ${e.message}`); console.error(`FAIL ${name}: ${e.message}`); }
};

try {
  await page.goto(URL, {waitUntil:'domcontentloaded', timeout:20000});
} catch (e) {
  console.error(`REGRESSION_FAIL navigation: ${e.message}`);
  await browser.close();
  process.exit(1);
}

await check('version/title', async()=>{
  assert.match(await page.title(), /Producer Interface v0\.2/);
  assert.equal(await page.locator('#sessionId').count(), 1);
});

await check('scientific contract visible', async()=>{
  const txt = await page.locator('body').innerText();
  assert.match(txt, /AESTHETIC_REFERENCE ≠ M300_EVIDENCE ≠ SUCCESS_EVIDENCE ≠ GATE_A_ACQUISITION/);
  assert.match(txt, /SCIENTIFIC_D bloqueado/);
});

await check('evidence panels toggle', async()=>{
  for (const id of ['evidence','limits','provenance']) {
    await page.locator(`[data-panel="${id}"]`).click();
    assert.equal(await page.locator(`#${id}`).evaluate(el=>getComputedStyle(el).display), 'block');
  }
});

await check('aesthetic reference provenance', async()=>{
  await page.locator('#ref').setInputFiles({name:'synthetic-reference.wav', mimeType:'audio/wav', buffer:fs.readFileSync(wavPath)});
  await page.waitForFunction(()=>document.querySelector('#refState')?.textContent?.includes('AUDIT_LOCAL_REFERENCE'), null, {timeout:10000});
  const meta = await page.locator('#refMeta').innerText();
  assert.match(meta, /AESTHETIC_REFERENCE/);
  assert.match(meta, /synthetic-reference\.wav/);
  assert.match(meta, /SHA-256/i);
  assert.match(meta, /Gate A\s*NO/i);
  assert.match(meta, /Ingesta científica\s*NO/i);
  const session = await page.evaluate(()=>{
    const sid = document.querySelector('#sessionId').textContent;
    return {sid, stored:localStorage.getItem('hooklab_session_id')};
  });
  assert.equal(session.sid, session.stored);
});

await check('timer start-stop-reset', async()=>{
  await page.locator('#start').click();
  await page.waitForTimeout(1300);
  assert.notEqual(await page.locator('#time').innerText(), '00:00');
  await page.locator('#stop').click();
  await page.locator('#reset').click();
  assert.equal(await page.locator('#time').innerText(), '00:00');
});

await check('D0 and scientific lock states', async()=>{
  await page.locator('#midiBtn').click();
  assert.match(await page.locator('#buildState').innerText(), /D0: interfaz preparada/);
  assert.match(await page.locator('#buildState').innerText(), /SCIENTIFIC_D permanece bloqueado/);
  await page.locator('#audioBtn').click();
  assert.match(await page.locator('#buildState').innerText(), /Audio científico no disponible/);
});

await check('save persistence', async()=>{
  await page.locator('#text').fill('Texto controlado de regresión');
  await page.locator('#intent').fill('directo');
  await page.locator('#decision').selectOption({label:'Modificar'});
  await page.locator('#reason').fill('Prueba de persistencia');
  await page.locator('#save').click();
  assert.match(await page.locator('#saveState').innerText(), /Sesión guardada localmente/);
  const saved = await page.evaluate(()=>{
    const sid = document.querySelector('#sessionId').textContent;
    return JSON.parse(localStorage.getItem('hooklab_session_'+sid));
  });
  assert.equal(saved.creative.text, 'Texto controlado de regresión');
  assert.equal(saved.producer_evaluation.decision, 'Modificar');
  assert.equal(saved.aesthetic_reference.scientific_ingestion, false);
  assert.equal(saved.aesthetic_reference.gate_a_ingestion, false);
});

await check('JSON export', async()=>{
  const downloadPromise = page.waitForEvent('download', {timeout:10000});
  await page.locator('#export').click();
  const download = await downloadPromise;
  const p = await download.path();
  const obj = JSON.parse(fs.readFileSync(p, 'utf8'));
  assert.equal(obj.version, 'producer-interface-v0.2');
  assert.equal(obj.provenance_contract, 'AESTHETIC_REFERENCE != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION');
  assert.equal(obj.scientific_state.scientific_d, 'BLOCKED');
});

await check('clear aesthetic reference', async()=>{
  await page.locator('#clearRef').click();
  assert.equal(await page.locator('#refState').innerText(), 'Sin referencia cargada.');
});

await browser.close();
if (failures.length) {
  console.error(`REGRESSION_FAIL count=${failures.length}`);
  for (const f of failures) console.error(f);
  process.exit(1);
}
console.log('REGRESSION_PASS Producer Interface v0.2');
