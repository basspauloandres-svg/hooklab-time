from manual_reference_audio_contract import build

def valid():
 return {'reference_id':'REF001','purpose':'PRIVATE_RESEARCH_PREPRODUCTION','user_supplied':True,'publish_or_redistribute':False,'corpus_population_evidence':False,'raw_audio_repository_retention':False,'sha256':'abc123','identity':{'title':'User declared reference'}}
def test_reference_is_admissible_but_never_matrix_x():
 out=build(valid())
 assert out['status']=='REFERENCE_ANALYSIS_ADMISSIBLE'
 assert out['evidence_class']=='MANUAL_REFERENCE_AUDIO'
 assert out['matrix_x_eligible'] is False
 assert out['corpus_population_evidence'] is False
def test_blocks_corpus_contamination():
 m=valid();m['corpus_population_evidence']=True
 out=build(m)
 assert out['status']=='REFERENCE_ANALYSIS_BLOCKED'
 assert 'CORPUS_CONTAMINATION_RISK' in out['blocking_reasons']
def test_blocks_raw_audio_repository_retention():
 m=valid();m['raw_audio_repository_retention']=True
 out=build(m)
 assert out['status']=='REFERENCE_ANALYSIS_BLOCKED'
 assert 'RAW_AUDIO_RETENTION_NOT_DISABLED' in out['blocking_reasons']
