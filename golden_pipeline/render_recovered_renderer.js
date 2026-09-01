#!/usr/bin/env node
'use strict';

const fs = require('fs');
const crypto = require('crypto');

const rendererPath = process.argv[2] || 'app-mie-p30-harmony-beat-v0.1.html';
const outputPath = process.argv[3] || 'golden_pipeline/recovered_renderer_output.wav';
const html = fs.readFileSync(rendererPath, 'utf8');

function extractConst(name, nextName) {
  const re = new RegExp(`const ${name}=([\\s\\S]*?);\\nconst ${nextName}=`);
  const m = html.match(re);
  if (!m) throw new Error(`Cannot extract ${name}`);
  return Function(`"use strict"; return (${m[1]});`)();
}

const startMatch = html.match(/const START=([0-9.]+),END=([0-9.]+),SR=([0-9]+)/);
if (!startMatch) throw new Error('Cannot extract START/END/SR');
const START = Number(startMatch[1]);
const END = Number(startMatch[2]);
const SR = Number(startMatch[3]);
const P30 = extractConst('P30', 'BEATS');
const BEATS = extractConst('BEATS', 'H');
const hMatch = html.match(/const H=([\s\S]*?);\nconst \$=/);
if (!hMatch) throw new Error('Cannot extract H');
const H = Function(`"use strict"; return (${hMatch[1]});`)();

function hz(m) { return 440 * Math.pow(2, (m - 69) / 12); }
function addTone(y, on, off, m, amp, kind) {
  let A = Math.max(0, Math.floor((on - START) * SR));
  let B = Math.min(y.length, Math.floor((off - START) * SR));
  if (B <= A) return;
  const f = hz(m);
  for (let i = A; i < B; i++) {
    const t = (i - A) / SR, d = (B - A) / SR;
    let en;
    if (kind === 'mel') en = (1 - Math.exp(-t / .006)) * Math.min(1, (d - t) / .025) * .95;
    else en = (1 - Math.exp(-t / .004)) * (.56 * Math.exp(-t / .9) + .30 * Math.exp(-t / 2.3) + .14 * Math.exp(-t / 5));
    let v = Math.sin(2 * Math.PI * f * t);
    if (kind === 'harm') v += .34 * Math.sin(4 * Math.PI * f * t) + .13 * Math.sin(6 * Math.PI * f * t);
    else v += .12 * Math.sin(4 * Math.PI * f * t);
    y[i] += amp * en * v;
  }
}
function addClick(y, t) {
  const A = Math.max(0, Math.floor((t - START) * SR));
  const B = Math.min(y.length, A + Math.floor(.035 * SR));
  for (let i = A; i < B; i++) {
    const q = (i - A) / SR, en = Math.exp(-q * 90);
    const v = Math.sin(2 * Math.PI * 1450 * q) + .35 * Math.sin(2 * Math.PI * 2200 * q);
    y[i] += .12 * en * v;
  }
}
function wav(y) {
  let mx = 0;
  for (const v of y) mx = Math.max(mx, Math.abs(v));
  const g = .92 / Math.max(mx, 1e-9);
  const ab = new ArrayBuffer(44 + y.length * 2), dv = new DataView(ab);
  let p = 0;
  const S = s => { for (const c of s) dv.setUint8(p++, c.charCodeAt(0)); };
  const U = n => { dv.setUint32(p, n, true); p += 4; };
  const W = n => { dv.setUint16(p, n, true); p += 2; };
  S('RIFF'); U(36 + y.length * 2); S('WAVEfmt '); U(16); W(1); W(1); U(SR); U(SR * 2); W(2); W(16); S('data'); U(y.length * 2);
  for (let x of y) {
    x = Math.max(-1, Math.min(1, x * g));
    dv.setInt16(p, x < 0 ? x * 32768 : x * 32767, true); p += 2;
  }
  return Buffer.from(ab);
}

const y = new Float32Array(Math.ceil((END - START) * SR));
for (const q of H) for (const m of q.midi) addTone(y, Math.max(START, q.start), Math.min(END, q.end), m, .038, 'harm');
for (const q of P30) if (q[1] >= START && q[0] <= END) addTone(y, Math.max(START, q[0]), Math.min(END, q[1]), q[2], .075, 'mel');
for (const t of BEATS) if (t >= START && t <= END) addClick(y, t);

const out = wav(y);
fs.mkdirSync(require('path').dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, out);
const sha256 = crypto.createHash('sha256').update(out).digest('hex');
console.log(JSON.stringify({renderer: rendererPath, output: outputPath, sha256, start_s: START, end_s: END, sr: SR, samples: y.length, p30_events: P30.length, harmony_units: H.length, rendered_tactus: BEATS.filter(t => t >= START && t <= END).length}, null, 2));
