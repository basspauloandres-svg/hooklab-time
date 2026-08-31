#!/usr/bin/env python3
"""Gate A automatic recording/version identity resolver using MusicBrainz metadata.

This component resolves *recording identity only*. It does not acquire or authorize audio.
The downstream recording_reference_resolver remains the authority for computational-access rights.

Resolution order:
1. exact ISRC lookup when target registry already contains an ISRC;
2. MusicBrainz recording search by title + artist;
3. conservative scoring using title, artist, duration and first-release year;
4. explicit VERIFIED / AUDIT / UNRESOLVED outcome with provenance.
"""
from __future__ import annotations
import argparse, json, re, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

MB='https://musicbrainz.org/ws/2'
UA='HookLab-TIME-MIE/1.0 (scientific research; recording identity resolver)'
VERSION='HOOKLAB_RECORDING_IDENTITY_RESOLVER_v1.0'

def norm(s): return re.sub(r'[^a-z0-9]+',' ',str(s or '').lower()).strip()
def _get(path, params=None):
    url=f'{MB}/{path}'
    if params: url += '?' + urllib.parse.urlencode(params)
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=30) as r: return json.load(r),url

def _artist(rec):
    return ''.join(x.get('name','') + x.get('joinphrase','') for x in rec.get('artist-credit',[])).strip()
def _year(rec):
    d=rec.get('first-release-date') or ''
    try:return int(d[:4])
    except:return None

def score(target,rec):
    s=0; reasons=[]
    if norm(target.get('title'))==norm(rec.get('title')): s+=40; reasons.append('TITLE_EXACT')
    elif norm(target.get('title')) in norm(rec.get('title')) or norm(rec.get('title')) in norm(target.get('title')): s+=20; reasons.append('TITLE_PARTIAL')
    if norm(target.get('artist'))==norm(_artist(rec)): s+=35; reasons.append('ARTIST_EXACT')
    elif norm(target.get('artist')) in norm(_artist(rec)) or norm(_artist(rec)) in norm(target.get('artist')): s+=18; reasons.append('ARTIST_PARTIAL')
    td=target.get('duration_ms'); rd=rec.get('length')
    if td and rd:
        delta=abs(int(td)-int(rd)); reasons.append(f'DURATION_DELTA_MS={delta}')
        if delta<=2000:s+=15
        elif delta<=5000:s+=10
        elif delta<=15000:s+=3
        else:s-=15
    ty=target.get('release_year'); ry=_year(rec)
    if ty and ry:
        dy=abs(int(ty)-int(ry)); reasons.append(f'YEAR_DELTA={dy}')
        if dy==0:s+=10
        elif dy==1:s+=5
        elif dy>=3:s-=5
    return s,reasons

def resolve(target):
    provenance=[]; candidates=[]
    if target.get('isrc'):
        data,url=_get(f"isrc/{target['isrc']}",{'fmt':'json','inc':'artist-credits+isrcs'})
        provenance.append(url); candidates=data.get('recordings',[])
        method='ISRC_LOOKUP'
    else:
        q=f'recording:"{target.get("title","")}" AND artist:"{target.get("artist","")}"'
        data,url=_get('recording/',{'query':q,'fmt':'json','limit':10})
        provenance.append(url); candidates=data.get('recordings',[])
        method='TITLE_ARTIST_SEARCH'
    ranked=[]
    for r in candidates:
        sc,why=score(target,r)
        ranked.append({'score':sc,'reasons':why,'mbid':r.get('id'),'title':r.get('title'),'artist':_artist(r),'duration_ms':r.get('length'),'first_release_date':r.get('first-release-date'),'isrcs':r.get('isrcs',[])})
    ranked.sort(key=lambda x:x['score'],reverse=True)
    best=ranked[0] if ranked else None; second=ranked[1] if len(ranked)>1 else None
    margin=(best['score']-second['score']) if best and second else (best['score'] if best else 0)
    # Conservative: metadata search is VERIFIED only with strong exact metadata and separation.
    if best and best['score']>=80 and margin>=10: status='VERIFIED'
    elif best and best['score']>=60: status='AUDIT'
    else: status='UNRESOLVED'
    return {'schema':VERSION,'song_id':target.get('song_id'),'resolution_method':method,'version_identity_status':status,'selected_recording':best if status!='UNRESOLVED' else None,'candidate_rank':ranked,'provenance':provenance,'resolved_at':datetime.now(timezone.utc).isoformat(),'boundary':'Recording/version identity only. This result does not authorize audio access or establish melodic validity.'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
    p=json.loads(Path(a.input).read_text(encoding='utf-8'))
    targets=p.get('targets',[p]) if isinstance(p,dict) else p
    out={'schema':VERSION,'results':[resolve(t) for t in targets]}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps({'verified':sum(x['version_identity_status']=='VERIFIED' for x in out['results']),'audit':sum(x['version_identity_status']=='AUDIT' for x in out['results']),'total':len(out['results'])}))
if __name__=='__main__':main()
