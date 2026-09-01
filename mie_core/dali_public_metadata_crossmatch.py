#!/usr/bin/env python3
"""Crossmatch HookLab candidates against DALI public metadata only.

This module deliberately does not assume access to DALI annotations. The public
metadata can be queried without credentials and is useful for discovery, but DALI
annotation files are access-restricted on Zenodo. A metadata hit therefore means
DALI_CANDIDATE_MATCH, never FULL_TMT_READY.

For fail-closed auditability, the best metadata candidate is retained even when it
does not pass the automatic match threshold. This does not lower that threshold or
promote an audit candidate.
"""
import argparse,json,re,urllib.request
from pathlib import Path

DALI_METADATA_URL='https://raw.githubusercontent.com/gabolsgabs/DALI/master/code/DALI/files/dali_v1_metadata.json'
ARTIST_IDENTITY_ALIASES={
    'p nk':'pink',  # audited orthographic identity: P!nk == Pink
}

def norm(s):
    return re.sub(r'[^a-z0-9]+',' ',str(s or '').lower()).strip()

def norm_artist(s):
    x=norm(s)
    return ARTIST_IDENTITY_ALIASES.get(x,x)

def score(track,artist,entry):
    tt,aa=norm(track),norm_artist(artist)
    et,ea=norm(entry.get('title')),norm_artist(entry.get('artist'))
    s=0
    if tt==et:s+=6
    elif tt and (tt in et or et in tt):s+=3
    if aa==ea:s+=4
    elif aa and ea and (aa in ea or ea in aa):s+=2
    return s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--candidates',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    candidates=json.loads(Path(a.candidates).read_text())
    if isinstance(candidates,dict):
        candidates=candidates.get('priority',candidates.get('candidates',[]))
    req=urllib.request.Request(DALI_METADATA_URL,headers={'User-Agent':'HookLabPrototype/1.0'})
    with urllib.request.urlopen(req,timeout=60) as r: dali=json.load(r)
    entries=list(dali.values());results=[]
    for c in candidates:
        title=c.get('title') or c.get('track'); artist=c.get('artist')
        ranked=sorted(((score(title,artist,e),e) for e in entries),key=lambda x:x[0],reverse=True)
        best_score,best=ranked[0]
        exact=best_score>=8
        results.append({'title':title,'artist':artist,'match_status':'DALI_CANDIDATE_MATCH' if exact else 'NO_RELIABLE_DALI_MATCH',
                        'score':best_score,'dali_id':best.get('id') if exact else None,
                        'dali_artist':best.get('artist') if exact else None,'dali_title':best.get('title') if exact else None,
                        'ground_truth':best.get('ground-truth') if exact else None,
                        'ncc':best.get('scores',{}).get('NCC') if exact else None,
                        'audio_working_flag':best.get('audio',{}).get('working') if exact else None,
                        'artist_identity_alias_applied':norm(artist)!=norm_artist(artist) or norm(best.get('artist'))!=norm_artist(best.get('artist')),
                        'audit_best_dali_id':best.get('id'),'audit_best_dali_artist':best.get('artist'),
                        'audit_best_dali_title':best.get('title'),'audit_best_ground_truth':best.get('ground-truth'),
                        'audit_best_ncc':best.get('scores',{}).get('NCC'),
                        'audit_best_release_date':(best.get('metadata') or {}).get('release_date'),
                        'audit_best_album':(best.get('metadata') or {}).get('album'),
                        'audit_semantics':'BEST_CANDIDATE_RETAINED_FOR_REVIEW_NOT_AUTOMATIC_PROMOTION',
                        'coverage_semantics':'PUBLIC_METADATA_ONLY_ANNOTATIONS_ACCESS_RESTRICTED'})
    out={'schema':'HOOKLAB_DALI_PUBLIC_CROSSMATCH_v1.2','metadata_source':DALI_METADATA_URL,
         'annotation_access':'RESTRICTED_ZENODO_REQUEST_REQUIRED',
         'automatic_match_threshold':8,
         'artist_identity_aliases':ARTIST_IDENTITY_ALIASES,
         'rule':'A public metadata match cannot satisfy M_FULL, TEXT_FULL, Matrix-X eligibility, or generation readiness by itself.',
         'results':results}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False))
    print(json.dumps({'matched':sum(x['match_status']=='DALI_CANDIDATE_MATCH' for x in results),'total':len(results)}))
if __name__=='__main__':main()
