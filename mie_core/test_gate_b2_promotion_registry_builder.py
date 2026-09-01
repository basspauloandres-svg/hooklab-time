from gate_b2_promotion_registry_builder import build

def rule():
 return {'rules':[{'rule_id':'R1','evidence_id':'E1','origin':'CORPUS_EMPIRICAL','musical_dimension':'TEMPO_METER','transformation':{'type':'RANGE_CONSTRAINT','lower':110,'upper':125},'validation_scope':'dance-pop robust cohort','provisional':False}]}
def test_blocks_small_seed_even_with_rule():
 out=build({'status':'MORE_ROBUST_DATA_REQUIRED','rows':5,'persistent_drift_detected':False},rule())
 assert out['decision']=='PROMOTION_BLOCKED'
 assert 'COHORT_NOT_STABLE_REFERENCE_READY' in out['rejected_rules'][0]['rejection_reasons']
def test_promotes_only_after_stable_reference():
 out=build({'status':'STABLE_REFERENCE_READY','rows':75,'persistent_drift_detected':False},rule())
 assert out['decision']=='PROMOTION_READY'
 assert out['promoted_rules'][0]['promotion_state']=='PROMOTED'
def test_provisional_rule_is_rejected():
 r=rule();r['rules'][0]['provisional']=True
 out=build({'status':'STABLE_REFERENCE_READY','rows':75,'persistent_drift_detected':False},r)
 assert out['decision']=='PROMOTION_BLOCKED'
 assert 'PROVISIONAL_RULE' in out['rejected_rules'][0]['rejection_reasons']
