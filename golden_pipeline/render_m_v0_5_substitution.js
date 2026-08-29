#!/usr/bin/env node
'use strict';

/**
 * Guarded golden M substitution renderer v0.1.
 *
 * Experimental purpose: replace ONLY the melody event stream in the recovered
 * golden renderer. Harmony B and Beat This are extracted from the canonical
 * recovered HTML and verified against frozen hashes before rendering.
 *
 * This executable deliberately REFUSES to infer source alignment. A manifest
 * must state alignment_status=VERIFIED and same_source_confirmed=true.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const EXPECTED_RENDERER_SHA256 = '8ae79a4c6f92cea9d48a6aea5cd1cc3d4496dbd993e9cf0d229e6fcfcb4c5541';
const EXPECTED_BEATS_CANONICAL_SHA256 = '402f6870aa6ce1aac39acf09b6b2274a47b958fd1059a686156fb494b723a1e4';
const EXPECTED_H_CANONICAL_SHA256 = 'cf528e781652d4c573a8c1d818e0b78c02d6dbb7b4566088398933c11052a721';
const GOLDEN_START = 13.3;
const GOLDEN_END = 40.7;
const SR = 44100;

const rendererPath = process.argv[2] || 'app-mie-p30-harmony-beat-v0.1.html';
const manifestPath = process.argv[3];
const outputPath = process.argv[4] || 'golden_pipeline/MIE_M_V05_HB_TFROZEN_candidate.wav';
const reportPath = process.argv[5] || outputPath.replace(/\.wav$/i, '.json');
if (!manifestPath) {
  throw new Error('Usage: node render_m_v0_5_substitution.js <canonical_renderer.html> <verified_manifest.json> [output.wav] [report.json]');
}

function sha256(x) { return crypto.createHash('sha256').update(x).digest('hex'); }
function canonicalSha(obj) { return sha256(Buffer.from(JSON.stringify(obj, Object.keys(obj).sort()))); }
function deepCanonical(obj) {
  if (Array.isArray(obj)) return obj.map(deepCanonical);
  if (obj && typeof obj === 'object') {
    const out = {};
    for (const k of Object.keys(obj).sort()) out[k] = deepCanonical(obj[k]);
    return out;
  }
  return obj;
}
function canonicalHash(obj) { return sha256(Buffer.from(JSON.stringify(deepCanonical(obj)))); }

const rendererBytes = fs.readFileSync(rendererPath);
const rendererSha = sha256(rendererBytes);
if (rendererSha !== EXPECTED_RENDERER_SHA256) {
  throw new Error(`REFUSED: canonical renderer SHA mismatch: ${rendererSha}`);
}
const html = rendererBytes.toString('utf8');
const startMatch = html.match(/const START=([0-9.]+),END=([0-9.]+),SR=([0-9]+)/);
if (!startMatch) throw new Error('REFUSED: cannot extract golden geometry');
if (Number(startMatch[1]) !== GOLDEN_START || Number(startMatch[2]) !== GOLDEN_END || Number(startMatch[3]) !== SR) {
  throw new Error('REFUSED: golden geometry changed');
}
function extract(name, nextName) {
  const re = new RegExp(`const ${name}=([\\s\\S]*?);\\nconst ${nextName}=`);
  const m = html.match(re);
  if (!m) throw new Error(`REFUSED: cannot extract ${name}`);
  return Function(`\"use strict\"; return (${m[1]});`)();
}
const BEATS = extract('BEATS', 'H');
const hMatch = html.match(/const H=([\s\S]*?);\nconst \$=/);
if (!hMatch) throw new Error('REFUSED: cannot extract H');
const H = Function(`\"use strict\"; return (${hMatch[1]});`)();
const beatsHash = canonicalHash(BEATS);
const hHash = canonicalHash(H);
if (beatsHash !== EXPECTED_BEATS_CANONICAL_SHA256) throw new Error(`REFUSED: frozen Beat This changed: ${beatsHash}`);
if (hHash !== EXPECTED_H_CANONICAL_SHA256) throw new Error(`REFUSED: frozen Harmony B changed: ${hHash}`);
if (BEATS.length !== 34 || H.length !== 33) throw new Error('REFUSED: frozen H/T cardinality changed');

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
if (manifest.alignment_status !== 'VERIFIED') {
  throw new Error(`REFUSED: M alignment_status must be VERIFIED, got ${manifest.alignment_status || 'MISSING'}`);
}
if (manifest.same_source_confirmed !== true) throw new Error('REFUSED: same_source_confirmed must be true');
if (!manifest.alignment_evidence || !Array.isArray(manifest.alignment_evidence) || manifest.alignment_evidence.length === 0) {
  throw new Error('REFUSED: explicit alignment_evidence is required');
}
const M = manifest.melody_events;
if (!Array.isArray(M) || M.length === 0) throw new Error('REFUSED: no melody_events');
for (const e of M) {
  if (e.state && e.state !== 'LOCK') throw new Error(`REFUSED: non-LOCK melody event ${e.id || ''}`);
  if (!(Number.isFinite(e.start_s) && Number.isFinite(e.end_s) && Number.isFinite(e.midi))) throw new Error('REFUSED: invalid melody event');
  if (!(e.end_s > e.start_s)) throw new Error('REFUSED: non-positive melody duration');
  if (e.start_s < GOLDEN_START - 1e-9 || e.end_s > GOLDEN_END + 1e-9) throw new Error('REFUSED: melody event outside golden window');
}

function hz(m) { return 440 * Math.pow(2, (m - 69) / 12); }
function addTone(y, on, off, m, amp, kind) {
  let A = Math.max(0, Math.floor((on - GOLDEN_START) * SR));
  let B = Math.min(y.length, Math.floor((off - GOLDEN_START) * SR));
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
  const A = Math.max(0, Math.floor((t - GOLDEN_START) * SR));
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

const y = new Float32Array(Math.ceil((GOLDEN_END - GOLDEN_START) * SR));
for (const q of H) for (const m of q.midi) addTone(y, Math.max(GOLDEN_START, q.start), Math.min(GOLDEN_END, q.end), m, .038, 'harm');
for (const e of M) addTone(y, e.start_s, e.end_s, e.midi, .075, 'mel');
for (const t of BEATS) if (t >= GOLDEN_START && t <= GOLDEN_END) addClick(y, t);
const out = wav(y);
fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, out);
const report = {
  version: 'MIE Golden M v0.5 Substitution Renderer v0.1',
  status: 'RENDERED_CANDIDATE_NOT_PROMOTED',
  baseline_promoted: false,
  canonical_renderer_sha256: rendererSha,
  frozen_harmony_b_canonical_sha256: hHash,
  frozen_beat_this_canonical_sha256: beatsHash,
  harmony_units: H.length,
  beat_events_embedded: BEATS.length,
  beat_events_rendered: BEATS.filter(t => t >= GOLDEN_START && t <= GOLDEN_END).length,
  melody_events: M.length,
  alignment_status: manifest.alignment_status,
  alignment_evidence: manifest.alignment_evidence,
  output_sha256: sha256(out),
  golden_window_s: [GOLDEN_START, GOLDEN_END],
  sr: SR,
  rule: 'Only M was substituted. H/T and golden synthesis parameters were read from and verified against the recovered canonical renderer.'
};
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
