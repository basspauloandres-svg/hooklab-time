#!/usr/bin/env python3
"""Build Corpus Reference Model v0.1 from homogeneous TMT fingerprints.

No feature is declared important. This module estimates empirical distributions
(mean, std, median, IQR, min, max, n) for every numeric feature available across
fingerprints. These distributions can later standardize distinctions without
manual feature weights.
"""
import argparse,json,math,statistics
from pathlib import Path
from data_first_guard import assert_no_manual_success_weights

def flatten(d,p=''):
 out={}
 for k,v in d.items():
  q=f'{p}.{k}' if p else k
  if isinstance(v,dict):out.update(flatten(v,q))
  elif isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v):out[q]=float(v)
 return out

def percentile(xs,p):
 xs=sorted(xs)
 if not xs:return None
 if len(xs)==1:return xs[0]
 q=(len(xs)-1)*p;lo=int(math.floor(q));hi=int(math.ceil(q))
 return xs[lo] if lo==hi else xs[lo]+(xs[hi]-xs[lo])*(q-lo)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('output');ap.add_argument('fingerprints',nargs='+');a=ap.parse_args()
 docs=[]
 for f in a.fingerprints:
  d=json.loads(Path(f).read_text());assert_no_manual_success_weights(d);docs.append(d)
 cols={}
 for d in docs:
  for k,v in flatten(d).items(): cols.setdefault(k,[]).append(v)
 features={}
 for k,xs in sorted(cols.items()):
  if len(xs)<2:continue
  q1=percentile(xs,.25);q3=percentile(xs,.75)
  features[k]={'n':len(xs),'mean':statistics.mean(xs),'std':statistics.pstdev(xs),'median':statistics.median(xs),
               'q1':q1,'q3':q3,'iqr':q3-q1,'min':min(xs),'max':max(xs)}
 out={'schema':'TMT_CORPUS_REFERENCE_v0.1','n_fingerprints':len(docs),'features':features,
      'selection_status':'NO_FEATURE_SELECTION','weighting_status':'NO_MANUAL_WEIGHTS',
      'epistemic_guard':{'policy':'DATA_FIRST','purpose':'EMPIRICAL_STANDARDIZATION_ONLY'},
      'promotion_rule':'Predictive interpretation requires an independently defined Y and out-of-sample validation.'}
 Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps(out))
if __name__=='__main__':main()
