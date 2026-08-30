#!/usr/bin/env python3
"""Aggregate Analyzer v1 generalization outcomes and decide prototype-interface readiness.

Readiness is an engineering gate only. It does not evaluate musical quality or success.
A prototype interface becomes eligible when the analyzer demonstrates repeated strict-pass
behavior across a heterogeneous validation set without per-song tuning.
"""
import argparse,json,collections
from pathlib import Path

PASS={'STRICT_REPLAY_PASS','FULL_TMT_READY'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('inputs',nargs='+');ap.add_argument('--output',required=True)
    ap.add_argument('--min-pass',type=int,default=5);ap.add_argument('--min-genres',type=int,default=2);ap.add_argument('--min-styles',type=int,default=3)
    a=ap.parse_args(); rows=[]
    for p in a.inputs:
        d=json.loads(Path(p).read_text()); meta=d.get('metadata',{})
        status=d.get('strict_gate_status') or d.get('status') or d.get('analysis_status')
        gs=d.get('genre_style') or meta.get('genre_style') or {}
        rows.append({'source':p,'song_id':d.get('song_id') or meta.get('song_id'), 'status':status,
                     'genre':gs.get('genre') or meta.get('genre'),'style':gs.get('style') or meta.get('style'),
                     'parameter_policy':d.get('parameter_policy') or meta.get('parameter_policy','GLOBAL_FROZEN')})
    passed=[r for r in rows if r['status'] in PASS]
    failures=[r for r in rows if r['status'] not in PASS]
    genres={r['genre'] for r in passed if r['genre']}; styles={r['style'] for r in passed if r['style']}
    no_tuning=all(r['parameter_policy']=='GLOBAL_FROZEN' for r in rows)
    gates={'min_pass':len(passed)>=a.min_pass,'min_genres':len(genres)>=a.min_genres,'min_styles':len(styles)>=a.min_styles,'no_per_song_tuning':no_tuning}
    ready=all(gates.values())
    report={'schema':'ANALYZER_GENERALIZATION_REPORT_v1.0','n_total':len(rows),'n_pass':len(passed),'n_fail':len(failures),
            'genres_passed':sorted(genres),'styles_passed':sorted(styles),'gates':gates,
            'prototype_interface_status':'ELIGIBLE' if ready else 'DEFERRED',
            'rows':rows,'failures':failures,
            'rule':'Interface readiness is based on repeated analyzer generalization, not musical-quality judgement.'}
    Path(a.output).write_text(json.dumps(report,indent=2,ensure_ascii=False));print(json.dumps(report))
if __name__=='__main__': main()
