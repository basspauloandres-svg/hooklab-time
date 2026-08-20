#!/usr/bin/env python3
from statistics import median

def _circ(x):
    x=x%1.0
    return min(x,1.0-x)

def resolve(last_pre,post,ibi,audio_active,phase_tol=.18,tempo_tol=.14,min_events=3,target_events=5):
    if not audio_active:
        return {'state':'SILENCE','confidence':'high'}
    if len(post)<min_events:
        return {'state':'UNCERTAIN','confidence':'low','reason':'insufficient_events','events':len(post)}
    p=post[:target_events]
    ints=[p[i]-p[i-1] for i in range(1,len(p))]
    folded=[]
    for x in ints:
        k=max(1,round(x/ibi)); folded.append(x/k)
    post_ibi=median(folded)
    if abs(post_ibi-ibi)/ibi>tempo_tol:
        return {'state':'UNCERTAIN','confidence':'low','reason':'tempo_incompatible','events':len(p)}
    errs=[_circ((t-last_pre)/ibi) for t in p]
    restart=sum(e>phase_tol for e in errs); cont=len(errs)-restart
    need=3 if len(p)>=5 else len(p)
    if restart>=need and restart>cont:
        return {'state':'CLOCK_STOP_RESTART','confidence':'high' if len(p)>=5 else 'medium','events':len(p),'restart_votes':restart}
    if cont>=need and cont>restart:
        return {'state':'CLOCK_CONTINUES','confidence':'high' if len(p)>=5 else 'medium','events':len(p),'continue_votes':cont}
    return {'state':'UNCERTAIN','confidence':'low','reason':'conflicting_phase_evidence','events':len(p),'restart_votes':restart,'continue_votes':cont}
