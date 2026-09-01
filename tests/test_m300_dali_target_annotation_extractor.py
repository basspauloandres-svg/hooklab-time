#!/usr/bin/env python3
"""Software regression for DALI target extraction; synthetic data are not evidence."""
from __future__ import annotations
import math, sys, tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'mie_core'))
from m300_dali_target_annotation_extractor import extract_entry, build

class Entry:
    def __init__(self, notes):
        self.annotations={'type':'horizontal','annot':{'notes':notes}}
        self.info={'id':'synthetic','dataset_version':'TEST','ground-truth':False,'scores':{'NCC':1.0}}

# A4=440 Hz -> MIDI 69; A5=880 Hz -> MIDI 81; median = 75.
x=extract_entry(Entry([
    {'time':(0.0,0.5),'freq':[440.0,440.0]},
    {'time':(0.5,1.0),'freq':[880.0,880.0]},
]))
assert x['representation_origin']=='DALI_NOTE_EVENTS'
assert x['n_note_events']==2
assert math.isclose(x['median_pitch_st'],75.0,abs_tol=1e-9),x

# The target population must remain incomplete when annotations are not provisioned.
manifest={
 'schema':'HOOKLAB_M300_DALI_TARGET_MANIFEST_v1.1',
 'minimum_population_gate_n':30,
 'targets':[{'candidate_id':f'M300::TEST::{i:02d}','dali_id':f'id{i:02d}','title':'Synthetic','artist':'Synthetic'} for i in range(30)]
}
with tempfile.TemporaryDirectory() as d:
    out=build(manifest,d)
assert out['status']=='ANNOTATION_EVIDENCE_INCOMPLETE'
assert out['eligible_annotation_rows']==0
assert len(out['audit'])==30
assert out['scientific_promotion'] is False
assert out['feature_allowlist']==['median_pitch_st']
print('PASS: calibrated DALI extractor regression; SYNTHETIC_SOFTWARE_TEST_ONLY')
