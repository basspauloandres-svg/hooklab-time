#!/usr/bin/env python3
"""Text Acquisition Adapter v0.1.

Normalizes a legally/contractually available lyric/document source into a traceable
Text Object input. The adapter does not scrape around access controls and does not
invent missing lyrics. Acquisition providers remain pluggable; this layer enforces
provenance, completeness and separation between documentary text and acoustic
alignment.
"""
import argparse,hashlib,json,re
from pathlib import Path

SECTION=re.compile(r'^\s*\[([^\]]+)\]\s*$')

def normalize_lines(raw):
    section='UNSPECIFIED';units=[]
    for line in raw.splitlines():
        x=line.strip()
        if not x: continue
        m=SECTION.match(x)
        if m: section=m.group(1).strip();continue
        units.append({'line_id':f'TXT_{len(units):03d}','section':section,'text':x,
                      'token_count':len(re.findall(r"\b[\w’'-]+\b",x,flags=re.UNICODE))})
    return units

def repetition_groups(units):
    by={}
    for u in units:
        key=re.sub(r'\s+',' ',re.sub(r'[^\w\s]','',u['text'].lower())).strip()
        if key: by.setdefault(key,[]).append(u['line_id'])
    return [ids for ids in by.values() if len(ids)>1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--song-id',required=True);ap.add_argument('--source-id',required=True)
    ap.add_argument('--source-type',required=True,choices=['LICENSED_API','USER_AUTHORIZED_CORPUS','PUBLIC_DOMAIN','RESEARCH_CORPUS'])
    ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);ap.add_argument('--expected-complete',action='store_true')
    a=ap.parse_args();raw=Path(a.input).read_text(encoding='utf-8');units=normalize_lines(raw)
    status='COMPLETE_CANDIDATE' if a.expected_complete and units else ('PARTIAL' if units else 'UNAVAILABLE')
    obj={'schema':'TMT_TEXT_OBJECT_v1.0','song_id':a.song_id,
         'provenance':{'source_id':a.source_id,'source_type':a.source_type,'sha256':hashlib.sha256(raw.encode()).hexdigest()},
         'document_status':status,'alignment_status':'UNALIGNED','units':units,
         'repetition_groups':repetition_groups(units),
         'rules':['Document text is preserved before acoustic alignment.','Missing text is never generated.','Text does not determine pitch.']}
    Path(a.output).write_text(json.dumps(obj,indent=2,ensure_ascii=False));print(json.dumps({'lines':len(units),'status':status}))
if __name__=='__main__':main()
