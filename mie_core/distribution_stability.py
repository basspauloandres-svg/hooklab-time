#!/usr/bin/env python3
"""Distribution stability diagnostics for the first empirical sample.

Compares successive matrix snapshots using standardized shifts in location and spread.
This is a stopping aid, not a representativeness proof. No success labels or manual
feature weights are used.
"""
import argparse,csv,json,math,statistics
from pathlib import Path

def read_csv(path):
    with open(path,encoding='utf-8') as f:return list(csv.DictReader(f))

def numeric(rows):
    out={}
    if not rows:return out
    for k in rows[0]:
        if k=='song_id':continue
        vals=[]
        for r in rows:
            try:
                v=float(r[k])
                if math.isfinite(v):vals.append(v)
            except:pass
        if vals:out[k]=vals
    return out

def stats(vals):
    return {'n':len(vals),'mean':statistics.mean(vals),'median':statistics.median(vals),'sd':statistics.stdev(vals) if len(vals)>1 else 0.0}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--previous',required=True);ap.add_argument('--current',required=True);ap.add_argument('--output',required=True);ap.add_argument('--median-shift-threshold',type=float,default=.10);ap.add_argument('--sd-shift-threshold',type=float,default=.10);a=ap.parse_args()
    p=numeric(read_csv(a.previous));c=numeric(read_csv(a.current));features=sorted(set(p)&set(c));res={};stable=0
    for k in features:
        ps,cs=stats(p[k]),stats(c[k]);scale=max(abs(ps['sd']),1e-9)
        med_shift=abs(cs['median']-ps['median'])/scale
        sd_shift=abs(cs['sd']-ps['sd'])/scale
        ok=med_shift<=a.median_shift_threshold and sd_shift<=a.sd_shift_threshold
        stable+=int(ok);res[k]={'previous':ps,'current':cs,'standardized_median_shift':med_shift,'standardized_sd_shift':sd_shift,'stable':ok}
    frac=stable/len(features) if features else 0.0
    out={'schema':'DISTRIBUTION_STABILITY_v1.0','n_features_compared':len(features),'stable_fraction':frac,'all_features_stable':bool(features) and stable==len(features),'thresholds':{'median_shift_sd_units':a.median_shift_threshold,'sd_shift_sd_units':a.sd_shift_threshold},'features':res,'interpretation_rule':'Use only as descriptive stabilization evidence; it does not establish representativeness or statistical power.'}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'stable_fraction':frac,'features':len(features)}))
if __name__=='__main__':main()
