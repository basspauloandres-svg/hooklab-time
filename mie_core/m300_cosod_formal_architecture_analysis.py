#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json,re,unicodedata,zipfile,math
from pathlib import Path
from collections import defaultdict,Counter
from scipy.stats import spearmanr

def norm(s):
 s=unicodedata.normalize('NFKD',str(s or '')).encode('ascii','ignore').decode().lower();s=re.sub(r'\([^)]*\)|\[[^]]*\]',' ',s);return ' '.join(re.sub(r'[^a-z0-9]+',' ',s).split())
def toks(s):return {x for x in norm(s).split() if x not in {'the','and','with','feat','featuring','ft','x'}}
def ov(a,b):
 A=toks(a);B=toks(b);return len(A&B)/max(1,min(len(A),len(B)))
def csvrows(path):
 with zipfile.ZipFile(path) as z:
  for name in z.namelist():
   if '__MACOSX/' in name or not name.lower().endswith('.csv'):continue
   for row in csv.reader(z.read(name).decode('utf-8-sig','replace').splitlines()):
    if row and any(str(c).strip() for c in row):yield row

def md(path):
 out={}
 for r in csvrows(path):
  if len(r)!=9:continue
  try:i=int(r[0]);y=int(r[1]);pos=int(r[2])
  except:continue
  out[i]={'cosod_index':i,'year':y,'cosod_year_end_position':pos,'title':r[3].strip(),'artist':r[4].strip(),'collaboration_type_gender':r[7].strip(),'musicbrainz_url':r[8].strip()}
 return out

def canonical_section(s):
 x=norm(s)
 if 'pre chorus' in x:return 'pre_chorus'
 if 'post chorus' in x:return 'post_chorus'
 if 'dance chorus' in x:return 'dance_chorus'
 if x in {'chorus','hook','refrain'}:return x
 if 'verse' in x:return 'verse'
 if 'intro' in x or 'introduction' in x:return 'intro'
 if 'bridge' in x:return 'bridge'
 if 'outro' in x:return 'outro'
 if 'link' in x:return 'link'
 return x or 'other'

def architecture(path):
 raw=defaultdict(list)
 for r in csvrows(path):
  if len(r)!=15:continue
  try:i=int(r[0]);t=float(r[1])
  except:continue
  raw[i].append((t,canonical_section(r[2])))
 out={}
 hook_family={'chorus','hook','refrain','dance_chorus','post_chorus'}
 for i,events in raw.items():
  # collapse duplicate timestamps/labels if provider exports repeated analytic rows
  seq=[]
  for t,s in sorted(set(events),key=lambda x:(x[0],x[1])):
   if not seq or seq[-1]!=(t,s):seq.append((t,s))
  labels=[s for _,s in seq];n=len(labels)
  if not n:continue
  c=Counter(labels);bigrams=list(zip(labels,labels[1:]));bc=Counter(bigrams)
  unique=len(c);recurrent=sum(v for v in c.values() if v>1)
  hook_times=[t for t,s in seq if s in hook_family]
  gaps=[b-a for a,b in zip(hook_times,hook_times[1:]) if b>a]
  entropy=-sum((v/n)*math.log2(v/n) for v in c.values()) if n>1 else 0.0
  entropy_norm=entropy/math.log2(unique) if unique>1 else 0.0
  out[i]={
   'formal_section_count':n,
   'formal_unique_section_count':unique,
   'formal_recurrent_event_ratio':recurrent/n,
   'formal_dominant_section_share':max(c.values())/n,
   'formal_entropy_norm':entropy_norm,
   'formal_transition_reuse_ratio':(1-len(bc)/len(bigrams)) if bigrams else 0.0,
   'hook_family_count':len(hook_times),
   'hook_family_share':len(hook_times)/n,
   'hook_return_count':max(0,len(hook_times)-1),
   'median_hook_gap_s':sorted(gaps)[len(gaps)//2] if gaps else None,
   'provider_sequence':labels
  }
 return out

def bh(ps):
 m=len(ps);o=sorted(range(m),key=lambda i:ps[i]);q=[1.]*m;prev=1.
 for rank,i in reversed(list(enumerate(o,1))):prev=min(prev,ps[i]*m/rank);q[i]=prev
 return q

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--m300',required=True);ap.add_argument('--cosod-metadata',required=True);ap.add_argument('--cosod-analysis',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 m=json.loads(Path(a.m300).read_text());M=md(a.cosod_metadata);A=architecture(a.cosod_analysis);by={}
 for _,r in M.items():by.setdefault((r['year'],norm(r['title'])),[]).append(r)
 rows=[];aud=[]
 for c in m['candidates']:
  hits=sorted([(ov(c['artist'],x['artist']),x) for x in by.get((int(c['chart_year']),norm(c['title'])),[])],reverse=True,key=lambda z:z[0])
  if hits and hits[0][0]>=.5 and hits[0][1]['cosod_index'] in A:
   s,r=hits[0];rows.append({**c,**r,**A[r['cosod_index']],'artist_overlap':s,'m300_rank_strength':16-int(c['rank']),'log10_spotify_playcount':math.log10(max(1,int(c.get('spotify_playcount_observed') or 0)))})
  elif hits:aud.append({'candidate_id':c['candidate_id'],'reason':'IDENTITY_AUDIT'})
 feats=['formal_unique_section_count','formal_recurrent_event_ratio','formal_dominant_section_share','formal_entropy_norm','formal_transition_reuse_ratio','hook_family_count','hook_family_share','hook_return_count','median_hook_gap_s']
 outs=['m300_rank_strength','log10_spotify_playcount'];tests=[]
 for f in feats:
  for o in outs:
   pairs=[(r.get(f),r.get(o)) for r in rows if r.get(f) is not None and r.get(o) is not None]
   if len(pairs)<30:continue
   xs=[x for x,_ in pairs];ys=[y for _,y in pairs]
   if len(set(xs))<2 or len(set(ys))<2:continue
   rho,p=spearmanr(xs,ys);tests.append({'feature':f,'outcome':o,'n':len(pairs),'rho':round(float(rho),4),'p':float(p)})
 qs=bh([x['p'] for x in tests]) if tests else []
 for x,q in zip(tests,qs):x['q_bh']=q;x['supported_for_interpretation']=bool(x['n']>=30 and abs(x['rho'])>=.2 and q<.05)
 supported=[x for x in tests if x['supported_for_interpretation']]
 out={'schema':'HOOKLAB_M300_COSOD_FORMAL_ARCHITECTURE_ANALYSIS_v1.0','population_scope':'Exact licensed M300 x CoSoD collaboration subcohort, 2010-2019','eligible_rows':len(rows),'audit_rows':len(aud),'feature_semantics':'Observable provider-annotated formal-section recurrence and hook-family organization only; no claim of listener salience, causality, or compositional optimality.','gate':{'n_min':30,'abs_spearman_rho_min':0.2,'bh_q_max':0.05},'tests':tests,'supported_for_interpretation':supported,'decision':'FORMAL_ARCHITECTURE_ASSOCIATION_AVAILABLE' if supported else 'NO_FORMAL_ARCHITECTURE_ASSOCIATION_PASSED_GATE','scientific_promotion':False,'midi_rule_eligible':False,'boundary':'CoSoD is collaboration-specific. Outcomes remain observational and exposure/context, text, genre/style and artist-history layers remain separate.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'eligible_rows':len(rows),'tests':len(tests),'supported':supported,'decision':out['decision']}))
if __name__=='__main__':main()
