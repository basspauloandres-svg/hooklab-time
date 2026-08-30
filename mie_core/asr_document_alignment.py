#!/usr/bin/env python3
"""ASR-assisted documentary text alignment v0.1.

Uses ASR only as acoustic timing evidence. Documentary text remains the lexical source.
The ASR hypothesis is token-aligned to documentary tokens; only matched documentary
lines receive timing windows. Unmatched text remains unaligned and is never invented.
"""
import argparse,json,re,difflib,tempfile,subprocess,os
from pathlib import Path

def norm(x):
    return re.sub(r"[^a-z0-9']+",'',x.lower().replace('’',"'"))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--audio-url',required=True);ap.add_argument('--text',required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--model',default='small');a=ap.parse_args()
    text=json.loads(Path(a.text).read_text());ram=Path('/dev/shm') if Path('/dev/shm').exists() else Path(tempfile.gettempdir())
    src=ram/f'align_{os.getpid()}.audio';wav=ram/f'align_{os.getpid()}.wav'
    try:
        subprocess.run(['curl','-L','--fail','--silent','--show-error',a.audio_url,'-o',str(src)],check=True)
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-ar','16000','-ac','1',str(wav)],check=True)
        from faster_whisper import WhisperModel
        model=WhisperModel(a.model,device='cpu',compute_type='int8')
        segments,_=model.transcribe(str(wav),word_timestamps=True,vad_filter=True)
        aw=[]
        for seg in segments:
            for w in (seg.words or []):
                t=norm(w.word)
                if t:aw.append({'token':t,'start_s':float(w.start),'end_s':float(w.end),'probability':float(w.probability or 0)})
        doc=[];line_ranges={}
        for u in text.get('units',[]):
            start=len(doc)
            for raw in re.findall(r"[\w’'-]+",u.get('text',''),flags=re.UNICODE):
                n=norm(raw)
                if n:doc.append({'token':n,'line_id':u['line_id']})
            line_ranges[u['line_id']]=(start,len(doc))
        sm=difflib.SequenceMatcher(a=[x['token'] for x in doc],b=[x['token'] for x in aw],autojunk=False)
        mapping={}
        for block in sm.get_matching_blocks():
            for k in range(block.size):mapping[block.a+k]=block.b+k
        windows=[]
        for u in text.get('units',[]):
            lo,hi=line_ranges[u['line_id']];idx=[i for i in range(lo,hi) if i in mapping]
            denom=max(hi-lo,1);coverage=len(idx)/denom
            if coverage>=0.50 and idx:
                vals=[aw[mapping[i]] for i in idx]
                windows.append({'line_id':u['line_id'],'start_s':min(x['start_s'] for x in vals),'end_s':max(x['end_s'] for x in vals),
                                'confidence':coverage,'mean_asr_probability':sum(x['probability'] for x in vals)/len(vals),
                                'evidence':'ASR_TOKEN_MATCH_TIMING_ONLY'})
        Path(a.output).write_text(json.dumps({'schema':'ASR_DOCUMENT_WINDOWS_v0.1','windows':windows,
            'document_token_count':len(doc),'asr_token_count':len(aw),'matched_document_tokens':len(mapping),
            'rule':'ASR supplies timing evidence only; documentary text supplies lexical content.'},indent=2,ensure_ascii=False))
        print(json.dumps({'windows':len(windows),'matched_document_tokens':len(mapping)}))
    finally:
        for p in (src,wav):
            try:p.unlink()
            except FileNotFoundError:pass
if __name__=='__main__':main()
