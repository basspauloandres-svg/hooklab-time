#!/usr/bin/env python3
"""Parse authorized DALI annotation records into HookLab-neutral evidence.

This parser operates on annotation JSON exported from the official DALI code.
It does not retrieve audio or use legacy YouTube helpers.
"""
from __future__ import annotations
import argparse,json,math,statistics
from pathlib import Path

def hz_to_midi(hz: float) -> float:
    if hz <= 0: raise ValueError('frequency must be > 0')
    return 69.0 + 12.0 * math.log2(hz / 440.0)

def summarize_notes(notes):
    clean=[]
    for n in notes:
        t=n.get('time');f=n.get('freq');text=n.get('text','')
        if not (isinstance(t,list) and len(t)==2 and isinstance(f,list) and len(f)==2):
            continue
        start,end=float(t[0]),float(t[1]);hz=(float(f[0])+float(f[1]))/2.0
        if end <= start or hz <= 0: continue
        clean.append({'start_s':start,'end_s':end,'duration_s':end-start,'hz':hz,'midi_float':hz_to_midi(hz),'text':text})
    if not clean:
        return {'note_count':0,'valid':False,'notes':[]}
    pitches=[x['midi_float'] for x in clean];durs=[x['duration_s'] for x in clean]
    intervals=[pitches[i]-pitches[i-1] for i in range(1,len(pitches))]
    iois=[clean[i]['start_s']-clean[i-1]['start_s'] for i in range(1,len(clean)) if clean[i]['start_s']>=clean[i-1]['start_s']]
    return {
        'valid':True,'note_count':len(clean),'notes':clean,
        'pitch_min_midi':min(pitches),'pitch_max_midi':max(pitches),'pitch_range_semitones':max(pitches)-min(pitches),
        'pitch_median_midi':statistics.median(pitches),'duration_median_s':statistics.median(durs),
        'mean_abs_interval_semitones':(sum(abs(x) for x in intervals)/len(intervals)) if intervals else 0.0,
        'stepwise_interval_share':(sum(abs(x)<=2.0 for x in intervals)/len(intervals)) if intervals else None,
        'repeated_pitch_share':(sum(abs(x)<0.5 for x in intervals)/len(intervals)) if intervals else None,
        'median_ioi_s':statistics.median(iois) if iois else None,
        'text_token_count':sum(1 for x in clean if str(x['text']).strip())
    }

def parse_entry(entry):
    info=entry.get('info') or {}
    ann=entry.get('annotations') or {}
    if ann.get('type')!='horizontal':
        return {'status':'AUDIT_FORMAT','reason':'DALI_HORIZONTAL_REQUIRED','scientific_promotion':False}
    annot=ann.get('annot') or {}; notes=annot.get('notes') or []
    sm=summarize_notes(notes)
    if not sm.get('valid'):
        return {'status':'AUDIT_ANNOTATION','reason':'NO_VALID_NOTES','scientific_promotion':False}
    scores=info.get('scores') or {};ncc=scores.get('NCC')
    gt=bool(info.get('ground-truth'))
    quality='GROUND_TRUTH' if gt else ('HIGH_NCC' if isinstance(ncc,(int,float)) and ncc>=0.8 else 'AUDIT_QUALITY')
    return {
      'schema':'HOOKLAB_DALI_ANNOTATION_EVIDENCE_v1.0','status':'PASS_ANNOTATION_PARSE' if quality!='AUDIT_QUALITY' else 'AUDIT_ANNOTATION_QUALITY',
      'provider':'DALI','dali_id':info.get('id'),'artist':info.get('artist'),'title':info.get('title'),'dataset_version':info.get('dataset_version'),
      'ground_truth':gt,'ncc':ncc,'quality_tier':quality,'metadata':info.get('metadata') or {},
      'melody_summary':{k:v for k,v in sm.items() if k!='notes'},'note_events':sm['notes'],
      'provenance':{'source':'authorized DALI annotation export','audio_retrieval_attempted':False,'legacy_youtube_helper_used':False},
      'scientific_promotion':False,
      'promotion_boundary':'Parsing success does not establish released-recording version identity or population-level rule eligibility.'
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input-json',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    out=parse_entry(json.loads(Path(a.input_json).read_text()));Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':out['status']}))
if __name__=='__main__':main()
