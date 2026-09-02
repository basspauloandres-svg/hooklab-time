(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.HookLabMieMidiExplorer=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const VERSION='HOOKLAB_MIE_AUDIO_MIDI_EXPLORER_v0.1';
  const PPQ=480;

  function clamp(n,a,b){return Math.max(a,Math.min(b,n));}
  function median(xs){
    if(!xs.length)return null;
    const z=xs.slice().sort((a,b)=>a-b),m=Math.floor(z.length/2);
    return z.length%2?z[m]:(z[m-1]+z[m])/2;
  }
  function bpmFromBeats(beats){
    const ibi=[];
    for(let i=1;i<beats.length;i++){
      const d=beats[i]-beats[i-1];
      if(Number.isFinite(d)&&d>=.25&&d<=2)ibi.push(d);
    }
    const m=median(ibi);
    return m?clamp(60/m,30,240):120;
  }
  function vlq(n){
    n=Math.max(0,Math.round(n));
    let out=[n&0x7f];
    while((n>>=7))out.unshift((n&0x7f)|0x80);
    return out;
  }
  function be16(n){return[(n>>>8)&255,n&255];}
  function be32(n){return[(n>>>24)&255,(n>>>16)&255,(n>>>8)&255,n&255];}
  function textBytes(s){return Array.from(new TextEncoder().encode(String(s)));}
  function chunk(tag,data){return[...textBytes(tag),...be32(data.length),...data];}
  function track(events){
    events.sort((a,b)=>a.tick-b.tick||a.order-b.order);
    let data=[],last=0;
    for(const e of events){data.push(...vlq(e.tick-last),...e.bytes);last=e.tick;}
    data.push(0,0xff,0x2f,0);
    return chunk('MTrk',data);
  }
  function validResult(result){
    return !!(result&&Array.isArray(result.melody)&&Array.isArray(result.beats));
  }
  function nearestBeat(time,beats){
    if(!beats.length)return{beat_index:null,beat_time_s:null,deviation_ms:null};
    let k=0,d=Math.abs(time-beats[0]);
    for(let i=1;i<beats.length;i++){
      const q=Math.abs(time-beats[i]);
      if(q<d){d=q;k=i;}
    }
    return{beat_index:k,beat_time_s:+beats[k].toFixed(5),deviation_ms:+((time-beats[k])*1000).toFixed(2)};
  }
  function normalizedMelody(result){
    return result.melody.map((e,index)=>({
      event_index:index,
      onset_s:+e.on,
      offset_s:+e.off,
      duration_s:+Math.max(0,e.off-e.on).toFixed(5),
      midi:clamp(Math.round(e.m),0,127),
      ...nearestBeat(+e.on,result.beats)
    })).filter(e=>Number.isFinite(e.onset_s)&&Number.isFinite(e.offset_s)&&e.offset_s>e.onset_s);
  }
  function buildMidi(result){
    if(!validResult(result))throw new Error('Resultado MIE incompleto');
    const bpm=bpmFromBeats(result.beats),ticksPerSecond=bpm*PPQ/60;
    const micros=Math.round(60000000/bpm);
    const conductor=[
      {tick:0,order:0,bytes:[0xff,0x03,VERSION.length,...textBytes(VERSION)]},
      {tick:0,order:1,bytes:[0xff,0x51,0x03,(micros>>>16)&255,(micros>>>8)&255,micros&255]},
      {tick:0,order:2,bytes:[0xff,0x58,0x04,0x04,0x02,0x18,0x08]}
    ];
    const melody=[{tick:0,order:0,bytes:[0xc0,0]}];
    for(const e of normalizedMelody(result)){
      const on=Math.round(e.onset_s*ticksPerSecond),off=Math.max(on+1,Math.round(e.offset_s*ticksPerSecond));
      melody.push({tick:on,order:2,bytes:[0x90,e.midi,92]},{tick:off,order:1,bytes:[0x80,e.midi,0]});
    }
    const pulse=[];
    for(const t of result.beats){
      if(!Number.isFinite(t)||t<0)continue;
      const on=Math.round(t*ticksPerSecond),off=on+Math.max(1,Math.round(.045*ticksPerSecond));
      pulse.push({tick:on,order:2,bytes:[0x99,37,76]},{tick:off,order:1,bytes:[0x89,37,0]});
    }
    return new Uint8Array([
      ...textBytes('MThd'),...be32(6),...be16(1),...be16(3),...be16(PPQ),
      ...track(conductor),...track(melody),...track(pulse)
    ]);
  }
  function mapping(result,source,midiSha256){
    if(!validResult(result))throw new Error('Resultado MIE incompleto');
    return{
      schema:VERSION,
      status:'EXPERIMENTAL_NOT_BASELINE',
      source:{name:source&&source.name||result.source||null,size_bytes:source&&source.size||null,sha256:source&&source.sha256||null},
      engine_source:'app-mie-unified-transcription-v0.1.1.html',
      analysis_class:'EXPLORATORY_LISTENING_TEST',
      scientific_d_unlocked:false,
      midi:{format:1,ppq:PPQ,tracks:['conductor','detected_melody','detected_pulse'],sha256:midiSha256||null},
      tempo_bpm:+bpmFromBeats(result.beats).toFixed(4),
      melody_events:normalizedMelody(result),
      beat_events_s:result.beats.map(t=>+t.toFixed(5)),
      harmony_windows:Array.isArray(result.harmony)?result.harmony:[],
      limitations:[
        'Blind experimental output; it does not modify the frozen Luis Miguel reference.',
        'Detected melody remains an experimental front end and requires producer listening.',
        'MIDI timing preserves physical seconds through one estimated tempo map; source events remain authoritative in JSON.'
      ]
    };
  }
  function buildAuditionWav(result,sampleRate=44100){
    if(!validResult(result))throw new Error('Resultado MIE incompleto');
    const melody=normalizedMelody(result),lastNote=melody.reduce((m,e)=>Math.max(m,e.offset_s),0);
    const lastBeat=result.beats.reduce((m,t)=>Number.isFinite(t)?Math.max(m,t):m,0);
    const duration=Math.max(.25,Math.min(600,Math.max(Number(result.duration_s)||0,lastNote+.25,lastBeat+.25)));
    const count=Math.ceil(duration*sampleRate),pcm=new Float32Array(count);
    function addTone(start,end,frequency,amplitude,harmonic){
      const a=Math.max(0,Math.floor(start*sampleRate)),b=Math.min(count,Math.ceil(end*sampleRate));
      for(let i=a;i<b;i++){
        const t=(i-a)/sampleRate,remaining=(b-i)/sampleRate;
        const envelope=Math.min(1,t/.008,remaining/.035)*Math.exp(-t*(harmonic?1.2:.25));
        pcm[i]+=amplitude*envelope*(Math.sin(2*Math.PI*frequency*t)+(harmonic?.16*Math.sin(4*Math.PI*frequency*t):0));
      }
    }
    for(const e of melody)addTone(e.onset_s,e.offset_s,440*Math.pow(2,(e.midi-69)/12),.24,true);
    for(let i=0;i<result.beats.length;i++){
      const t=+result.beats[i];
      if(Number.isFinite(t)&&t>=0&&t<duration)addTone(t,Math.min(duration,t+.045),i%4===0?1500:950,.11,false);
    }
    let peak=0;for(const x of pcm)peak=Math.max(peak,Math.abs(x));
    const gain=.9/Math.max(peak,1e-9),dataBytes=count*2,buffer=new ArrayBuffer(44+dataBytes),view=new DataView(buffer);let p=0;
    function str(s){for(const c of s)view.setUint8(p++,c.charCodeAt(0));}
    function u32(n){view.setUint32(p,n,true);p+=4;}
    function u16(n){view.setUint16(p,n,true);p+=2;}
    str('RIFF');u32(36+dataBytes);str('WAVE');str('fmt ');u32(16);u16(1);u16(1);u32(sampleRate);u32(sampleRate*2);u16(2);u16(16);str('data');u32(dataBytes);
    for(const x of pcm){const y=clamp(x*gain,-1,1);view.setInt16(p,y<0?Math.round(y*32768):Math.round(y*32767),true);p+=2;}
    return new Uint8Array(buffer);
  }
  return{VERSION,PPQ,bpmFromBeats,validResult,normalizedMelody,buildMidi,buildAuditionWav,mapping};
});
