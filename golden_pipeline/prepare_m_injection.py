#!/usr/bin/env python3
"""Prepare, but do not audition, a controlled M substitution manifest.

The script refuses to infer alignment between a structural-probe timeline and
the historical golden interval. A caller must provide an explicit offset and
assert that the source timeline corresponds to the same recording/window.
Harmony B and Beat This remain untouched.
"""
import argparse, json
from pathlib import Path

GOLDEN_START=13.3
GOLDEN_END=40.7


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--probe',required=True)
    ap.add_argument('--offset-s',type=float,required=True,
                    help='Explicit physical-time offset mapping probe t -> historical t.')
    ap.add_argument('--same-source-confirmed',action='store_true',
                    help='Required assertion that probe audio is aligned to the historical source.')
    ap.add_argument('--output',required=True)
    args=ap.parse_args()
    if not args.same_source_confirmed:
        raise SystemExit('REFUSED: source/timeline identity has not been confirmed; alignment must not be inferred.')
    d=json.loads(Path(args.probe).read_text(encoding='utf-8'))
    pr=d.get('plane_resolution',{})
    events=pr.get('events',[])
    mapped=[]
    for e in events:
        a=float(e['start_s'])+args.offset_s
        b=float(e['end_s'])+args.offset_s
        if b < GOLDEN_START or a > GOLDEN_END:
            continue
        q={
            'id':e.get('id'),
            'start_s':max(GOLDEN_START,a),
            'end_s':min(GOLDEN_END,b),
            'midi':int(e['midi']),
            'confidence':float(e.get('confidence',0.0)),
            'state':e.get('state','LOCK'),
            'source_start_s':float(e['start_s']),
            'source_end_s':float(e['end_s']),
        }
        if q['state']=='LOCK' and q['end_s']>q['start_s']:
            mapped.append(q)
    manifest={
        'version':'MIE Golden M Injection Manifest v0.1',
        'status':'PREPARED_NOT_AUDITIONED_NOT_PROMOTED',
        'same_source_confirmed':True,
        'time_mapping':{'kind':'offset','offset_s':args.offset_s},
        'golden_window_s':[GOLDEN_START,GOLDEN_END],
        'melody_source_probe':str(args.probe),
        'melody_event_count':len(mapped),
        'melody_events':mapped,
        'H':'FROZEN Harmony B from recovered golden renderer',
        'T':'FROZEN Beat This tactus from recovered golden renderer',
        'rule':'This manifest does not alter H/T and must not be rendered until structural gate and source alignment pass.'
    }
    Path(args.output).write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({k:manifest[k] for k in ['version','status','melody_event_count','golden_window_s']},indent=2))

if __name__=='__main__':
    main()
