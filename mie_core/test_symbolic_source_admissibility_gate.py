from symbolic_source_admissibility_gate import evaluate

def base():
 return {'track':'X','provider':'P','identity_resolved':True,'version_resolved':True,'full_length':True,'provenance_available':True,'computational_processing_authorized':True,'access_mode':'DATASET_AUTHORIZED','source_kind':'FULL_MIDI'}

def test_pass_requires_explicit_computational_authorization():
 r=base(); assert evaluate(r)['symbolic_source_gate']=='PASS'
 r['computational_processing_authorized']=False
 out=evaluate(r); assert out['symbolic_source_gate']=='AUDIT'; assert 'COMPUTATIONAL_PROCESSING_AUTHORIZED_NOT_CONFIRMED' in out['admissibility_reasons']

def test_preview_never_passes():
 r=base();r['source_kind']='PREVIEW'
 assert evaluate(r)['symbolic_source_gate']=='AUDIT'

def test_stream_only_never_passes():
 r=base();r['access_mode']='STREAM_ONLY';r['source_kind']='STREAM_ONLY'
 assert evaluate(r)['symbolic_source_gate']=='AUDIT'
