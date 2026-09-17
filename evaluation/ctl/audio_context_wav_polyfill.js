(() => {
  class HookLabAudioContext {
    async decodeAudioData(ab) {
      const v = new DataView(ab);
      const str = (o,n) => Array.from({length:n},(_,i)=>String.fromCharCode(v.getUint8(o+i))).join('');
      if (str(0,4) !== 'RIFF' || str(8,4) !== 'WAVE') throw new Error('Unsupported WAV container');
      let p=12, fmt=null, dataOff=null, dataSize=null;
      while (p+8 <= v.byteLength) {
        const id=str(p,4), size=v.getUint32(p+4,true), off=p+8;
        if (id === 'fmt ') {
          fmt={format:v.getUint16(off,true),channels:v.getUint16(off+2,true),sampleRate:v.getUint32(off+4,true),bits:v.getUint16(off+14,true)};
        } else if (id === 'data') { dataOff=off; dataSize=size; break; }
        p=off+size+(size&1);
      }
      if (!fmt || dataOff==null) throw new Error('Invalid WAV: missing fmt/data');
      if (fmt.format !== 1 || fmt.bits !== 16) throw new Error(`Unsupported WAV PCM format=${fmt.format} bits=${fmt.bits}`);
      const frames=Math.floor(dataSize/(fmt.channels*2));
      const channels=Array.from({length:fmt.channels},()=>new Float32Array(frames));
      let q=dataOff;
      for(let i=0;i<frames;i++) for(let c=0;c<fmt.channels;c++) channels[c][i]=v.getInt16(q,true)/32768, q+=2;
      return {
        duration:frames/fmt.sampleRate,
        sampleRate:fmt.sampleRate,
        length:frames,
        numberOfChannels:fmt.channels,
        getChannelData(c){return channels[c];}
      };
    }
    async close() {}
  }
  window.AudioContext=HookLabAudioContext;
  window.webkitAudioContext=HookLabAudioContext;
})();
