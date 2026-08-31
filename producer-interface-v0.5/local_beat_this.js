/* HookLab local Beat This analyzer v0.1
 * On-device browser inference. Audio never leaves the browser.
 * Models: danigb/beat-this-rs commit 089b509247e6fdcec666511c0dcf0d5f39c21e73
 * Scientific role: AESTHETIC_REFERENCE_ANALYSIS only.
 */
(function(root,factory){
  const api=factory();
  if(typeof module==='object'&&module.exports) module.exports=api;
  root.HookLabLocalBeatThis=api;
})(typeof globalThis!=='undefined'?globalThis:this,function(){
  'use strict';
  const VERSION='hooklab-local-beat-this-v0.1';
  const ORT_VERSION='1.29.0';
  const MODEL_COMMIT='089b509247e6fdcec666511c0dcf0d5f39c21e73';
  const BASE=`https://raw.githubusercontent.com/danigb/beat-this-rs/${MODEL_COMMIT}/models/`;
  const MEL_URL=BASE+'mel_spectrogram.onnx';
  const BEAT_URL=BASE+'beat_this_small.onnx';
  const MEL_SHA256='fdd59e65c515331308e4c8841edf99972deca646bdf6197744c2a5b7755e3de9';
  const BEAT_SHA256='a5f8d39d989f31859454ba27afe61c5317ca95e4d9373e6853e5361b8937172f';
  const SAMPLE_RATE=22050, FPS=50, CHUNK=1500, BORDER=6, STRIDE=1488;
  let sessionsPromise=null;

  async function digestHex(buf){const h=await crypto.subtle.digest('SHA-256',buf);return [...new Uint8Array(h)].map(x=>x.toString(16).padStart(2,'0')).join('')}
  async function fetchVerified(url,expected){const r=await fetch(url,{cache:'force-cache'});if(!r.ok)throw new Error(`MODEL_HTTP_${r.status}`);const b=await r.arrayBuffer(),sha=await digestHex(b);if(sha!==expected)throw new Error('MODEL_SHA256_MISMATCH');return b}
  async function loadSessions(){
    if(sessionsPromise)return sessionsPromise;
    sessionsPromise=(async()=>{
      if(typeof ort==='undefined')throw new Error('ONNXRUNTIME_WEB_NOT_LOADED');
      ort.env.wasm.numThreads=1;
      ort.env.wasm.wasmPaths=`https://cdn.jsdelivr.net/npm/onnxruntime-web@${ORT_VERSION}/dist/`;
      const [melBytes,beatBytes]=await Promise.all([fetchVerified(MEL_URL,MEL_SHA256),fetchVerified(BEAT_URL,BEAT_SHA256)]);
      const opts={executionProviders:['wasm'],graphOptimizationLevel:'all'};
      const [mel,beat]=await Promise.all([ort.InferenceSession.create(melBytes,opts),ort.InferenceSession.create(beatBytes,opts)]);
      return {mel,beat};
    })();
    try{return await sessionsPromise}catch(e){sessionsPromise=null;throw e}
  }

  async function decodeResample(file){
    const array=await file.arrayBuffer();
    const ctx=new (window.AudioContext||window.webkitAudioContext)();
    let decoded;
    try{decoded=await ctx.decodeAudioData(array.slice(0))}finally{await ctx.close()}
    const frames=Math.max(1,Math.ceil(decoded.duration*SAMPLE_RATE));
    const off=new OfflineAudioContext(1,frames,SAMPLE_RATE),src=off.createBufferSource();src.buffer=decoded;src.connect(off.destination);src.start(0);const rendered=await off.startRendering();
    return {samples:new Float32Array(rendered.getChannelData(0)),duration_s:rendered.duration};
  }

  function startsFor(n){const out=[];let p=-BORDER,limit=n-BORDER;while(p<limit){out.push(p);p+=STRIDE}if(n>STRIDE&&out.length)out[out.length-1]=n-(CHUNK-BORDER);return out}
  function extractChunk(data,fullTime,start){const nMels=128,actualStart=Math.max(start,0),actualEnd=Math.min(start+CHUNK,fullTime),padLeft=Math.max(-start,0),frames=Math.max(0,actualEnd-actualStart),padRight=Math.max(0,Math.min(BORDER,start+CHUNK-fullTime)),chunkTime=padLeft+frames+padRight,out=new Float32Array(chunkTime*nMels);for(let t=actualStart;t<actualEnd;t++){const src=t*nMels,dst=(padLeft+t-actualStart)*nMels;out.set(data.subarray(src,src+nMels),dst)}return {data:out,time:chunkTime}}
  function vectorFrom(t){return t.data instanceof Float32Array?t.data:new Float32Array(t.data)}
  async function predict(beatSession,melData,fullTime){const beatLogits=new Float32Array(fullTime);beatLogits.fill(-1000);const downLogits=new Float32Array(fullTime);downLogits.fill(-1000);const starts=startsFor(fullTime);for(let si=starts.length-1;si>=0;si--){const start=starts[si],ch=extractChunk(melData,fullTime,start),input=new ort.Tensor('float32',ch.data,[1,ch.time,128]),feeds={};feeds[beatSession.inputNames.includes('spectrogram')?'spectrogram':beatSession.inputNames[0]]=input;const out=await beatSession.run(feeds),b=vectorFrom(out.beat||out.beat_logits||out[beatSession.outputNames[0]]),d=vectorFrom(out.downbeat||out.downbeat_logits||out[beatSession.outputNames[1]]),writeStart=start+BORDER;for(let i=BORDER;i<ch.time-BORDER;i++){const dest=writeStart+(i-BORDER);if(dest>=0&&dest<fullTime){beatLogits[dest]=b[i];downLogits[dest]=d[i]}}}return {beatLogits,downLogits}}
  function dedupe(peaks){if(!peaks.length)return[];const out=[];let p=peaks[0],c=1;for(let i=1;i<peaks.length;i++){const p2=peaks[i];if(p2-p<=1){c++;p+=(p2-p)/c}else{out.push(p);p=p2;c=1}}out.push(p);return out}
  function findPeaks(logits){const peaks=[];for(let i=0;i<logits.length;i++){if(logits[i]<=0)continue;let max=true;for(let j=Math.max(0,i-3);j<Math.min(logits.length,i+4);j++){if(logits[j]>logits[i]){max=false;break}}if(max)peaks.push(i)}return dedupe(peaks)}
  function snapDownbeats(beats,downs){if(!beats.length)return downs;return [...new Set(downs.map(d=>beats.reduce((best,b)=>Math.abs(b-d)<Math.abs(best-d)?b:best,beats[0])))].sort((a,b)=>a-b)}
  function decodePeaks(b,d){const beats=findPeaks(b).map(x=>x/FPS),downs=snapDownbeats(beats,findPeaks(d).map(x=>x/FPS));return {beats,downbeats:downs}}
  function median(a){if(!a.length)return null;const x=[...a].sort((p,q)=>p-q),m=Math.floor(x.length/2);return x.length%2?x[m]:(x[m-1]+x[m])/2}
  function bpmFromBeats(beats){const ints=[];for(let i=1;i<beats.length;i++)if(beats[i]>beats[i-1])ints.push(beats[i]-beats[i-1]);const m=median(ints);return m?60/m:null}

  async function analyze(file,{sessionId,sha256}={}){
    if(!file||!file.type?.startsWith('audio/'))throw new Error('AUDIO_FILE_REQUIRED');if(!sessionId||!sha256)throw new Error('SESSION_AND_SHA_REQUIRED');
    const t0=performance.now(),{samples,duration_s}=await decodeResample(file),{mel,beat}=await loadSessions();
    const melInput=new ort.Tensor('float32',samples,[1,samples.length]),melFeeds={};melFeeds[mel.inputNames.includes('audio_pcm')?'audio_pcm':mel.inputNames[0]]=melInput;const melOut=await mel.run(melFeeds),melTensor=melOut.mel_spectrogram||melOut[mel.outputNames[0]],dims=melTensor.dims,fullTime=dims[1];if(dims.length!==3||dims[0]!==1||dims[2]!==128)throw new Error('BAD_MEL_SHAPE');
    const {beatLogits,downLogits}=await predict(beat,vectorFrom(melTensor),fullTime),decoded=decodePeaks(beatLogits,downLogits),bpm=bpmFromBeats(decoded.beats);
    return {schema:'HOOKLAB_AESTHETIC_REFERENCE_ANALYSIS_v0.1',status:'PASS',reasons:[],session_id:sessionId,role:'AESTHETIC_REFERENCE_ANALYSIS',semantics:'DESCRIPTIVE_SESSION_REFERENCE_ONLY',analysis_mode:'LOCAL_ON_DEVICE_ONNX',scientific_ingestion:false,gate_a_ingestion:false,m300_ingestion:false,success_evidence_ingestion:false,source_audio_persistence:'NONE',reference_sha256:sha256,duration_s:+duration_s.toFixed(3),tempo_bpm_median:bpm==null?null:+bpm.toFixed(4),beat_count:decoded.beats.length,beat_times_s:decoded.beats.map(x=>+x.toFixed(4)),downbeat_count:decoded.downbeats.length,downbeat_times_s:decoded.downbeats.map(x=>+x.toFixed(4)),beat_sensor:'Beat This small ONNX',beat_status:'VALID',model_source_commit:MODEL_COMMIT,beat_model_sha256:BEAT_SHA256,mel_model_sha256:MEL_SHA256,onnxruntime_web_version:ORT_VERSION,latency_ms:Math.round(performance.now()-t0),contract:'AESTHETIC_REFERENCE != M300_EVIDENCE != SUCCESS_EVIDENCE != GATE_A_ACQUISITION'};
  }
  return {VERSION,MODEL_COMMIT,MEL_SHA256,BEAT_SHA256,startsFor,findPeaks,bpmFromBeats,analyze};
});
