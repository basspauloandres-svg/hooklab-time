#!/usr/bin/env python3
"""Fail-closed guard for melody features entering population association testing."""
import argparse, json
from pathlib import Path

DEFAULT_ALLOWLIST=Path('config/representation_stable_features_v1.json')

def evaluate(requested, allowlist):
    allowed=set(allowlist.get('allowed_for_population_association_testing',[]))
    requested=list(dict.fromkeys(requested))
    blocked=[f for f in requested if f not in allowed]
    return {
      'schema':'HOOKLAB_REPRESENTATION_STABLE_FEATURE_GUARD_v1.0',
      'status':'PASS' if requested and not blocked else 'BLOCKED',
      'requested_features':requested,
      'allowed_features':sorted(allowed),
      'blocked_requested_features':blocked,
      'scientific_d':'BLOCKED',
      'semantics':'REPRESENTATION_CALIBRATION_AUTHORIZES_ASSOCIATION_TESTING_ONLY'
    }

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--features',nargs='+',required=True); ap.add_argument('--allowlist',default=str(DEFAULT_ALLOWLIST)); ap.add_argument('--output'); a=ap.parse_args()
    out=evaluate(a.features,json.loads(Path(a.allowlist).read_text()))
    if a.output: Path(a.output).write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
    raise SystemExit(0 if out['status']=='PASS' else 4)
if __name__=='__main__': main()
