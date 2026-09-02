const assert=require('assert');
const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const page=fs.readFileSync(path.join(root,'app-mie-audio-midi-explorer-v0.2.html'),'utf8');
const engine=require(path.join(root,'app/prototype_v1/mie_audio_transcription_engine.js'));

assert(page.includes('id="audioFile"'),'missing top-level audio input');
assert(page.includes('id="inputPreview"'),'missing input audio player');
assert(page.includes('id="outputPreview"'),'missing output audio player');
assert(!page.includes('<iframe'),'v0.2 must not use an iframe');
assert(page.includes('scientific_d_unlocked=false'),'scientific lock must be visible');
assert(page.includes("map.scientific_d_unlocked=false"),'scientific lock must be enforced');
assert.equal(engine.VERSION,'HOOKLAB_MIE_AUDIO_ENGINE_v0.2');

const sampleRate=22050,duration=.5,signal=new Float32Array(sampleRate*duration),frequency=engine.hz(60);
for(let i=0;i<signal.length;i++)signal[i]=Math.sin(2*Math.PI*frequency*i/sampleRate)*.7;
const melody=engine.melody(signal,sampleRate);
assert(melody.length>0,'synthetic tone should produce a melody event');
assert(melody.some(event=>Math.abs(event.m-60)<=1),'detected pitch should be near MIDI 60');
console.log('MIE_AUDIO_MIDI_EXPLORER_V02_PASS');
