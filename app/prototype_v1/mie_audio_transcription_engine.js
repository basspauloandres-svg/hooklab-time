(function(root,factory){
  const api=factory(root);
  if(typeof module==='object'&&module.exports)module.exports=api;
  root.HookLabMieAudioEngine=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(root){
  'use strict';
  const VERSION='HOOKLAB_MIE_AUDIO_ENGINE_v0.2';
  const SAMPLE_RATE=22050;
  const MEL_URL='https://raw.githubusercontent.com/danigb/beat-this-rs/main/models/mel_spectrogram.onnx';
  const BEAT_URL='https://raw.githubusercontent.com/danigb/beat-this-rs/main/models/beat_this_small.onnx';
  let melSession=null,beatSession=null;

  function mono(buffer){
    const y=new Float32Array(buffer.length);
    for(let channel=0;channel<buffer.numberOfChannels;channel++){
      const x=buffer.getChannelData(channel);
      for(let i=0;i<y.length;i++)y[i]+=x[i]/buffer.numberOfChannels;
    }
    return y;
  }
  function resample(x,from,to=SAMPLE_RATE){
    if(from===to)return x;
    const n=Math.floor(x.length*to/from),y=new Float32Array(n),ratio=from/to;
    for(let i=0;i<n;i++){
      const p=i*ratio,a=Math.floor(p),f=p-a;
      y[i]=x[a]*(1-f)+x[Math.min(x.length-1,a+1)]*f;
    }
    return y;
  }
  function hz(midi){return 440*Math.pow(2,(midi-69)/12);}
  function goertzel(x,start,size,midi,sampleRate){
    const f=hz(midi);let re=0,im=0,weightSum=0;
    for(let n=0;n<size;n+=2){
      const i=start+n;if(i>=x.length)break;
      const weight=.5-.5*Math.cos(2*Math.PI*n/(size-1)),value=x[i]*weight,phase=2*Math.PI*f*n/sampleRate;
      re+=value*Math.cos(phase);im-=value*Math.sin(phase);weightSum+=weight;
    }
    return Math.hypot(re,im)/Math.max(1,weightSum);
  }
  function melody(x,sampleRate=SAMPLE_RATE){
    const size=2048,hop=1024,frames=[];
    for(let start=0;start+size<x.length;start+=hop){
      let best={m:48,e:0},second=0;
      for(let midi=45;midi<=79;midi++){
        const energy=goertzel(x,start,size,midi,sampleRate);
        if(energy>best.e){second=best.e;best={m:midi,e:energy};}else if(energy>second)second=energy;
      }
      frames.push({t:start/sampleRate,m:best.m,e:best.e,ratio:best.e/(second+1e-9)});
    }
    const energies=frames.map(q=>q.e).sort((a,b)=>a-b),threshold=(energies[Math.floor(energies.length*.45)]||0)*.75;
    const events=[];let current=null;
    for(const frame of frames){
      if(frame.e<threshold||frame.ratio<1.03){if(current){events.push(current);current=null;}continue;}
      if(!current||frame.m!==current.m){if(current)events.push(current);current={on:frame.t,off:frame.t+hop/sampleRate,m:frame.m};}
      else current.off=frame.t+hop/sampleRate;
    }
    if(current)events.push(current);
    return events.filter(event=>event.off-event.on>=.07);
  }
  function harmony(x,sampleRate,beats,duration){
    const bounds=beats.length>3?beats:Array.from({length:Math.ceil(duration/.86)+1},(_,i)=>i*.86),out=[];
    for(let k=0;k<bounds.length-1;k++){
      const start=bounds[k],end=bounds[k+1];if(end-start<.15)continue;
      const size=4096,pitchClass=Array(12).fill(0),midiEnergy=Array(85).fill(0);let frames=0;
      for(let t=start;t+size/sampleRate<end;t+=2048/sampleRate){
        const offset=Math.floor(t*sampleRate);
        for(let midi=36;midi<=84;midi++){const e=goertzel(x,offset,size,midi,sampleRate);pitchClass[midi%12]+=e;midiEnergy[midi]+=e;}
        frames++;
      }
      if(!frames)continue;
      const maximum=Math.max(...pitchClass),median=[...pitchClass].sort((a,b)=>a-b)[6],candidates=[];
      for(let pc=0;pc<12;pc++)if(pitchClass[pc]>=Math.max(maximum*.18,median*1.18)){
        const bins=[];for(let midi=36;midi<=84;midi++)if(midi%12===pc)bins.push([midi,midiEnergy[midi]]);
        bins.sort((a,b)=>b[1]-a[1]);candidates.push({pc,m:bins[0][0],rel:pitchClass[pc]/(maximum||1)});
      }
      candidates.sort((a,b)=>b.rel-a.rel);let kept=candidates.filter(c=>c.rel>=.34).slice(0,4);if(kept.length<2)kept=candidates.slice(0,2);
      out.push({start,end,midi:kept.map(q=>q.m)});
    }
    return out;
  }
  async function beatThis(x,progress){
    if(!root.ort)throw new Error('ONNX Runtime no está disponible. Revisa la conexión y vuelve a intentar.');
    root.ort.env.wasm.numThreads=1;
    progress&&progress('Cargando detector Beat This…',18);
    if(!melSession)melSession=await root.ort.InferenceSession.create(MEL_URL,{executionProviders:['wasm']});
    if(!beatSession)beatSession=await root.ort.InferenceSession.create(BEAT_URL,{executionProviders:['wasm']});
    progress&&progress('Detectando pulsos…',28);
    const melOutput=await melSession.run({[melSession.inputNames[0]]:new root.ort.Tensor('float32',x,[1,x.length])});
    const spectrogram=melOutput[melSession.outputNames[0]],dims=spectrogram.dims;
    const frames=dims.length===3?dims[1]:dims[0],bands=dims.length===3?dims[2]:dims[1],flat=spectrogram.data;
    const probabilities=[],chunk=1500,overlap=12,step=chunk-2*overlap;
    for(let start=0;start<frames;start+=step){
      const count=Math.min(chunk,frames-start),data=new Float32Array(count*bands);data.set(flat.subarray(start*bands,(start+count)*bands));
      const output=await beatSession.run({[beatSession.inputNames[0]]:new root.ort.Tensor('float32',data,[1,count,bands])}),scores=output[beatSession.outputNames[0]].data;
      const left=start?overlap:0,right=start+count<frames?overlap:0;
      for(let j=left;j<count-right;j++)probabilities.push({frame:start+j,value:1/(1+Math.exp(-scores[j]))});
    }
    const peaks=[];
    for(let i=1;i<probabilities.length-1;i++)if(probabilities[i].value>=.5&&probabilities[i].value>=probabilities[i-1].value&&probabilities[i].value>probabilities[i+1].value)peaks.push({t:probabilities[i].frame*.02,s:probabilities[i].value});
    const kept=[];for(const peak of peaks.sort((a,b)=>b.s-a.s))if(!kept.some(other=>Math.abs(other.t-peak.t)<.16))kept.push(peak);
    return kept.sort((a,b)=>a.t-b.t).map(peak=>peak.t);
  }
  async function analyze(audioBuffer,sourceName,progress){
    progress&&progress('Preparando señal…',5);
    const duration=Math.min(audioBuffer.duration,60),x=resample(mono(audioBuffer),audioBuffer.sampleRate).subarray(0,Math.floor(duration*SAMPLE_RATE));
    const beats=await beatThis(x,progress);
    progress&&progress('Detectando melodía…',56);const detectedMelody=melody(x,SAMPLE_RATE);
    progress&&progress('Estimando armonía…',78);const detectedHarmony=harmony(x,SAMPLE_RATE,beats,duration);
    progress&&progress('Resultado listo.',100);
    return{schema:'MIE-AUDIO-MIDI-EXPLORER-v0.2',engine:VERSION,status:'EXPERIMENTAL_NOT_BASELINE',source:sourceName||null,duration_s:duration,prior_reference_injected:false,decoder:'top-level-mobile-safe',melody:detectedMelody,harmony:detectedHarmony,beats,scientific_d_unlocked:false};
  }
  return{VERSION,SAMPLE_RATE,mono,resample,hz,goertzel,melody,harmony,beatThis,analyze};
});
