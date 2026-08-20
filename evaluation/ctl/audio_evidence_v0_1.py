#!/usr/bin/env python3
"""Audio evidence v0.2 for MB05/MB06b/MB07.
RMS activity is normalized to the file median rather than a percentile that can
misclassify a sustained tone bed as inactive. Spectral-flux peaks are clustered
with a refractory interval to avoid double onsets from one synthetic attack.
"""
import wave, json
import numpy as np

def read_wav(path):
    with wave.open(path,'rb') as w:
        sr=w.getframerate(); n=w.getnframes(); ch=w.getnchannels(); sw=w.getsampwidth(); raw=w.readframes(n)
    if sw!=2: raise ValueError('expects 16-bit PCM')
    x=np.frombuffer(raw,dtype='<i2').astype(np.float32)/32768.0
    if ch>1:x=x.reshape(-1,ch).mean(1)
    return sr,x

def extract(path,frame_s=.0464,hop_s=.0116,refractory_s=.08):
    sr,x=read_wav(path); n=max(256,int(frame_s*sr)); hop=max(64,int(hop_s*sr)); win=np.hanning(n)
    rms=[]; flux=[]; times=[]; prev=None
    for i in range(0,max(1,len(x)-n),hop):
        f=x[i:i+n]; times.append((i+n/2)/sr); rms.append(float(np.sqrt(np.mean(f*f)+1e-12)))
        mag=np.abs(np.fft.rfft(f*win)); flux.append(0.0 if prev is None else float(np.maximum(mag-prev,0).sum())); prev=mag
    rms=np.asarray(rms); flux=np.asarray(flux); times=np.asarray(times)
    baseline=max(1e-6,float(np.median(rms)))
    activity_thr=max(1e-5,baseline*.25)
    active=rms>activity_thr
    med=float(np.median(flux)); mad=float(np.median(np.abs(flux-med)))+1e-12; onset_thr=med+5*mad
    raw=[]
    for k in range(1,len(flux)-1):
        if active[k] and flux[k]>=onset_thr and flux[k]>=flux[k-1] and flux[k]>flux[k+1]: raw.append((float(times[k]),float(flux[k])))
    peaks=[]
    for t,v in raw:
        if not peaks or t-peaks[-1][0]>=refractory_s: peaks.append([t,v])
        elif v>peaks[-1][1]: peaks[-1]=[t,v]
    return {'schema':'audio-evidence-v0.2','sr':sr,'activity_threshold':activity_thr,'rms_baseline':baseline,'active_fraction':float(active.mean()),'onsets_s':[p[0] for p in peaks],'onset_count':len(peaks),'frame_times_s':times.tolist(),'active':active.astype(int).tolist()}

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser(); ap.add_argument('wav'); ap.add_argument('--out'); a=ap.parse_args(); r=extract(a.wav); txt=json.dumps(r,indent=2)
 if a.out: open(a.out,'w').write(txt+'\n')
 else: print(txt)
