#!/usr/bin/env python3
"""Validate selected melody proxies by agreement across independent MIDI arrangements.

This validator compares transposition-invariant melodic interval histograms and normalized
rhythmic profiles between the primary target representation and independently sourced
alternate arrangements of the same title/artist. It provides reproducibility evidence
for the melody proxy. It is not equivalent to audio ground truth and is reported as
CROSS_REPRESENTATION_PASS rather than AUDIO_REFERENCE_PASS.
"""
import argparse,csv,json,math
from pathlib import Path

def vec(s):
 try:return [float(x) for x in str(s or '').split(';') if x!='']
 except:return []
def cosine(a,b):
 if not a or not b or len(a)!=len(b):return 0.0
 d=sum(x*y for x,y in zip(a,b));na=math.sqrt(sum(x*x for x in a));nb=math.sqrt(sum(y*y for y in b));return d/max(na*nb,1e-12)
def truth(v):return str(v).lower() in {'true','1','yes','pass'}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--primary',required=True);ap.add_argument('--alternates',required=True);ap.add_argument('--output',required=True);ap.add_argument('--min-consensus',type=float,default=.72);a=ap.parse_args()
 pri=list(csv.DictReader(Path(a.primary).open(encoding='utf-8')));alt=list(csv.DictReader(Path(a.alternates).open(encoding='utf-8')))
 byp={(r.get('title','').lower(),r.get('artist','').lower()):r for r in pri}
 groups={}
 for r in alt:groups.setdefault((r.get('title','').lower(),r.get('artist','').lower()),[]).append(r)
 rows=[]
 for key,p in byp.items():
  comps=[]
  for r in groups.get(key,[]):
   if not truth(r.get('full_tmt_candidate')):continue
   ci=cosine(vec(p.get('interval_histogram')),vec(r.get('interval_histogram')));cr=cosine(vec(p.get('rhythm_ratio_histogram')),vec(r.get('rhythm_ratio_histogram')))
   score=.7*ci+.3*cr
   comps.append({'alternate_md5':r.get('md5'),'interval_cosine':round(ci,4),'rhythm_cosine':round(cr,4),'consensus_score':round(score,4),'alternate_full_tmt':True})
  best=max([x['consensus_score'] for x in comps],default=0.0)
  passed=best>=a.min_consensus
  rows.append({'title':p.get('title'),'artist':p.get('artist'),'primary_md5':p.get('md5'),'alternate_valid_n':len(comps),'best_consensus_score':round(best,4),'crossrepresentation_gate':'PASS' if passed else 'PENDING','melodic_reference_evidence_level':'CROSS_REPRESENTATION_REPRODUCIBILITY','comparisons':comps})
 out={'schema':'HOOKLAB_MELODIC_CROSSREPRESENTATION_VALIDATOR_v1.0','threshold':a.min_consensus,'rows':rows,'pass_n':sum(x['crossrepresentation_gate']=='PASS' for x in rows),'semantics':'Cross-arrangement agreement validates reproducibility of the symbolic melody proxy but is not audio-reference ground truth.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'pass_n':out['pass_n'],'evaluated_n':len(rows)}))
if __name__=='__main__':main()
