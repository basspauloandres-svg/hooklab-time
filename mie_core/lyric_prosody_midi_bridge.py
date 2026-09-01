#!/usr/bin/env python3
"""Traceable Lyric→Prosody→MIDI bridge for HookLab D0 exploratory generation.

This module binds explicitly curated syllables/stress to an existing TMT structural
candidate. It does not infer prosody automatically and it does not promote a
scientific deduction. The output remains D0_EXPLORATORY unless a future, separately
validated scientific deduction contract explicitly authorizes otherwise.
"""
from __future__ import annotations
import argparse,json,math
from pathlib import Path


def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def validate_hook(h):
    reasons=[]
    if h.get('schema') != 'HOOKLAB_CURATED_HOOK_PROSODY_v1.0': reasons.append('INVALID_HOOK_SCHEMA')
    if h.get('prosody_status') != 'CURATED_PROSODY_PASS': reasons.append('PROSODY_NOT_CURATED_PASS')
    if not h.get('hook_id'): reasons.append('MISSING_HOOK_ID')
    if not h.get('language'): reasons.append('MISSING_LANGUAGE')
    if not h.get('provenance'): reasons.append('MISSING_PROVENANCE')
    lines=h.get('lines') or []
    if not lines: reasons.append('NO_LINES')
    for li,line in enumerate(lines,1):
        words=line.get('words') or []
        if not words: reasons.append(f'LINE_{li}_NO_WORDS'); continue
        for wi,w in enumerate(words,1):
            sylls=w.get('syllables') or []
            if not sylls: reasons.append(f'LINE_{li}_WORD_{wi}_NO_SYLLABLES')
            if not any(bool(s.get('stressed')) for s in sylls):
                reasons.append(f'LINE_{li}_WORD_{wi}_NO_STRESS_DECLARED')
            for si,s in enumerate(sylls,1):
                if not str(s.get('text','')).strip(): reasons.append(f'LINE_{li}_WORD_{wi}_SYLL_{si}_EMPTY')
    return reasons


def flatten_line(line):
    out=[]
    for wi,w in enumerate(line.get('words',[])):
        word=str(w.get('text','')).strip()
        for si,s in enumerate(w.get('syllables',[])):
            out.append({'word_index':wi,'word':word,'syllable_index_in_word':si,'syllable':str(s['text']).strip(),'stressed':bool(s.get('stressed'))})
    return out


def bind_variant(variant,hook):
    phrases=variant.get('phrases') or []
    lines=hook.get('lines') or []
    if len(phrases) < len(lines):
        raise ValueError(f'INSUFFICIENT_PHRASES:{len(phrases)}<{len(lines)}')
    mappings=[]
    for li,line in enumerate(lines):
        sylls=flatten_line(line); events=phrases[li].get('events') or []
        if len(events) < len(sylls):
            raise ValueError(f'INSUFFICIENT_EVENTS_LINE_{li+1}:{len(events)}<{len(sylls)}')
        nE,nS=len(events),len(sylls)
        for si,sy in enumerate(sylls):
            a=math.floor(si*nE/nS); b=math.floor((si+1)*nE/nS)
            if b<=a: b=a+1
            assigned=events[a:b]
            for ni,e in enumerate(assigned):
                mappings.append({
                    'line_index':li+1,
                    'word_index':sy['word_index']+1,
                    'word':sy['word'],
                    'syllable_index_in_word':sy['syllable_index_in_word']+1,
                    'syllable':sy['syllable'],
                    'stressed':sy['stressed'],
                    'melisma_note_index':ni+1,
                    'onset_s':float(e['onset_s']),
                    'pitch_midi':int(e['midi'])
                })
    return mappings


def write_midi(path,variant,mappings):
    import mido
    bpm=float(variant.get('tempo_bpm',120.0)); tempo=mido.bpm2tempo(bpm); tpb=480
    mid=mido.MidiFile(ticks_per_beat=tpb); tr=mido.MidiTrack(); mid.tracks.append(tr)
    tr.append(mido.MetaMessage('track_name',name='HookLab Lyric Prosody Bridge',time=0))
    tr.append(mido.MetaMessage('set_tempo',tempo=tempo,time=0))
    events=[]
    beat=60.0/bpm
    for m in mappings:
        tick=max(0,round(mido.second2tick(m['onset_s'],tpb,tempo)))
        dur=max(1,round(mido.second2tick(beat*0.8,tpb,tempo)))
        if m['melisma_note_index']==1:
            events.append((tick,0,mido.MetaMessage('lyrics',text=m['syllable'],time=0)))
        events.append((tick,1,mido.Message('note_on',note=m['pitch_midi'],velocity=84,time=0)))
        events.append((tick+dur,2,mido.Message('note_off',note=m['pitch_midi'],velocity=0,time=0)))
    events.sort(key=lambda x:(x[0],x[1])); prev=0
    for tick,_,msg in events:
        msg.time=max(0,tick-prev); tr.append(msg); prev=tick
    mid.save(path)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--hook',required=True); ap.add_argument('--structure',required=True); ap.add_argument('--output-dir',required=True); a=ap.parse_args()
    h=load_json(a.hook); reasons=validate_hook(h)
    if reasons:
        print(json.dumps({'status':'AUDIT_PROSODY_CONTRACT','blocking_reasons':reasons})); raise SystemExit(4)
    s=load_json(a.structure)
    if s.get('status')!='THREE_FULL_TMT_STRUCTURAL_CANDIDATES_READY':
        raise SystemExit('STRUCTURAL_CANDIDATES_NOT_READY')
    outdir=Path(a.output_dir); outdir.mkdir(parents=True,exist_ok=True); manifest=[]
    for v in s.get('variants',[]):
        mappings=bind_variant(v,h); name=str(v.get('variant','variant'))
        midi_path=outdir/f'{h["hook_id"]}_{name}.mid'; write_midi(midi_path,v,mappings)
        item={'variant':name,'midi_file':midi_path.name,'mapping_count':len(mappings),'mapping':mappings}
        (outdir/f'{h["hook_id"]}_{name}_mapping.json').write_text(json.dumps(item,indent=2,ensure_ascii=False),encoding='utf-8')
        manifest.append(item)
    result={
      'schema':'HOOKLAB_LYRIC_PROSODY_MIDI_BRIDGE_v1.0',
      'status':'LYRIC_PROSODY_MIDI_BRIDGE_PASS',
      'generation_class':'D0_EXPLORATORY',
      'scientific_d_unlocked':False,
      'hook_id':h['hook_id'],'language':h['language'],'prosody_status':h['prosody_status'],
      'traceability_chain':['WORD','SYLLABLE','STRESS','ONSET','DURATION_POLICY','PITCH','MIDI','HUMAN_EVALUATION'],
      'mapping_policy':'MONOTONIC_SYLLABLE_TO_EXISTING_EVENTS; EXTRA_EVENTS_FORM_EXPLICIT_MELISMA',
      'prosody_policy':'CURATED_INPUT_REQUIRED; NO_AUTOMATIC_STRESS_OR_SYLLABIFICATION_INFERENCE',
      'source_structure_schema':s.get('schema'),'variants':[{'variant':x['variant'],'midi_file':x['midi_file'],'mapping_count':x['mapping_count']} for x in manifest],
      'provenance':h.get('provenance')
    }
    (outdir/'bridge_manifest.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'status':result['status'],'variants':len(manifest),'generation_class':result['generation_class']}))

if __name__=='__main__': main()
