#!/usr/bin/env python3
"""Build a cached cohort reference from FULL_TMT test-lane Matrix X rows.

The output schema matches preproduction_router.py and preproduction_constraints_compiler.py.
This is engineering evidence only; it cannot be merged into massive-hit cohort references.
"""
import argparse,csv,json,statistics
from pathlib import Path

def nums(rows,key):
    out=[]
    for r in rows:
        try:
            if str(r.get(key,'')).strip()!='': out.append(float(r[key]))
        except Exception: pass
    return out

def desc(v):
    v=sorted(v); n=len(v)
    if not v:return None
    def q(p):
        x=(n-1)*p; lo=int(x); hi=min(lo+1,n-1); f=x-lo
        return v[lo]*(1-f)+v[hi]*f
    return {'min':v[0],'q25':q(.25),'median':statistics.median(v),'q75':q(.75),'max':v[-1],'n':n}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--matrix',required=True);ap.add_argument('--output',required=True);ap.add_argument('--genre',default='lakh_lyric_test');ap.add_argument('--style',default='full_tmt_symbolic');a=ap.parse_args()
    rows=list(csv.DictReader(Path(a.matrix).open(encoding='utf-8')))
    rows=[r for r in rows if r.get('coverage')=='FULL_SONG' and 'PASS' in r.get('strict_gate','').upper() and r.get('evidence_role')=='TEST_LANE_ONLY_LAKH_LYRIC_MIDI']
    mapping={'T_tempo_bpm':'tempo_bpm','M_median_midi':'melodic_register_midi','M_range_semitones':'melodic_range_semitones','M_events_per_token':'melodic_events_per_token','T_near_tactus_share':'near_tactus_share','text_line_count':'text_line_count'}
    ref={dst:desc(nums(rows,src)) for dst,src in mapping.items()}; ref={k:v for k,v in ref.items() if v is not None}
    key=f"{a.genre.strip().lower()}::{a.style.strip().lower()}"
    out={'schema':'HOOKLAB_PRECOMPUTED_COHORT_CACHE_v1.0','evidence_boundary':'TEST_LANE_ONLY_LAKH_LYRIC_MIDI','cohorts':{key:{**ref,'cohort_n':len(rows),'coverage':'FULL_TMT','source_matrix':Path(a.matrix).name}}}
    Path(a.output).write_text(json.dumps(out,indent=2,ensure_ascii=False));print(json.dumps({'status':'FULL_TMT_TEST_COHORT_CACHE_READY','cohort_key':key,'n':len(rows),'fields':list(ref)}))
    raise SystemExit(0 if len(rows)>=3 and len(ref)==6 else 4)
if __name__=='__main__':main()
