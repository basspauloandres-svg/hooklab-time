#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,math
from pathlib import Path
from collections import defaultdict
from scipy.stats import spearmanr

def parse_ann(p):
 lines=p.read_text(encoding='utf-8',errors='replace').splitlines(); times=[]; named=[]; chords=[]; hi=[]
 for line in lines:
  if not line or line.startswith('#'): continue
  m=re.match(r'^([0-9.]+)\s+(.*)$',line)
  if not m: continue
  times.append(float(m.group(1))); body=m.group(2)
  pre=body.split('|',1)[0]
  for tok in [x.strip() for x in pre.split(',') if x.strip()]:
   low=tok.lower()
   if re.match(r"^[A-Z](?:'+)?$",tok): hi.append(tok)
   elif any(k in low for k in ('verse','chorus','bridge','intro','outro','refrain','pre-chorus','prechorus','solo','instrumental')): named.append((float(m.group(1)),low))
  for bar in re.findall(r'\|([^|]+)\|',body):
   for c in re.split(r'[\s.]+',bar.strip()):
    if c and c not in {'&pause','*'}: chords.append(c)
 duration=max(times) if times else None
 chor=[t for t,n in named if 'chorus' in n or 'refrain' in n]
 return {'duration_s':duration,'first_chorus_ratio':(min(chor)/duration if chor and duration and duration>0 else None),'named_section_events':len(named),'unique_named_sections':len(set(n for _,n in named)),'high_level_section_events':len(hi),'chord_tokens':len(chords),'unique_chords':len(set(chords)),'chord_vocab_ratio':(len(set(chords))/len(chords) if chords else None)}

def bh(ps):
 m=len(ps); order=sorted(range(m),key=lambda i:ps[i]); q=[1.0]*m; prev=1.0
 for rank,i in reversed(list(enumerate(order,1))): prev=min(prev,ps[i]*m/rank);q[i]=prev
 return q

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True);ap.add_argument('--output',required=True);a=ap.parse_args();root=Path(a.repo)
 idx=list(csv.DictReader((root/'billboard-2.0-index.csv').open(encoding='utf-8-sig'))); rows=[];seen=set()
 for r in idx:
  if not r.get('id') or not r.get('title') or not r.get('artist') or not r.get('weeks_on_chart') or not r.get('peak_rank'): continue
  key=(r['title'].strip().lower(),r['artist'].strip().lower())
  if key in seen: continue
  p=root/'billboard-2.0-salami_chords'/str(int(r['id'])).zfill(4)/'salami_chords.txt'
  if not p.exists(): continue
  seen.add(key); f=parse_ann(p); f.update({'id':r['id'],'title':r['title'],'artist':r['artist'],'chart_date':r['chart_date'],'weeks_on_chart':int(r['weeks_on_chart']),'peak_strength':101-int(r['peak_rank'])});rows.append(f)
 feats=['duration_s','first_chorus_ratio','named_section_events','unique_named_sections','high_level_section_events','chord_tokens','unique_chords','chord_vocab_ratio']; tests=[]
 for outcome in ('weeks_on_chart','peak_strength'):
  for feat in feats:
   pairs=[(x[feat],x[outcome]) for x in rows if x.get(feat) is not None]
   if len(pairs)<30: continue
   rho,p=spearmanr([x for x,_ in pairs],[y for _,y in pairs]);tests.append({'feature':feat,'outcome':outcome,'n':len(pairs),'rho':round(float(rho),4),'p':float(p)})
 qs=bh([x['p'] for x in tests])
 for x,q in zip(tests,qs): x['q_bh']=q;x['exploratory_supported']=bool(x['n']>=100 and abs(x['rho'])>=.15 and q<.05)
 supported=[x for x in tests if x['exploratory_supported']];supported.sort(key=lambda x:abs(x['rho']),reverse=True)
 out={'schema':'HOOKLAB_MCGILL_BILLBOARD_DEDUCTION_CALIBRATION_v1.0','provider':'McGill Billboard Project / CC0 annotations','role':'HISTORICAL_METHOD_CALIBRATION_NOT_CONTEMPORARY_TARGET_POPULATION','eligible_unique_song_rows':len(rows),'tests':tests,'supported_exploratory_associations':supported,'strongest_supported':supported[0] if supported else None,'deduction_state':'CANDIDATE_FOR_THEORY_MATCHING' if supported else 'NO_EXPLORATORY_ASSOCIATION_PASSED_GATE','scientific_promotion':False,'boundary':'Association in 1958-1991 Billboard songs is not a contemporary universal success rule; genre/style and exposure are not controlled here. This run validates the evidence-to-deduction machinery and identifies hypotheses for theory matching.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'rows':len(rows),'supported':len(supported),'strongest':out['strongest_supported']}))
if __name__=='__main__':main()
