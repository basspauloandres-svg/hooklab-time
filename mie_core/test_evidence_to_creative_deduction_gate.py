from evidence_to_creative_deduction_gate import evaluate

def base():
 return {'evidence_id':'PROTO-001','population_scope':'qualified corpus snapshot','observed_pattern':'X distribution differs across observed outcome strata','association_evidence':{'method':'prototype contrast','causal_language':False},'interpretation':'Pattern is compatible with a conditioned musical hypothesis; mechanism remains open.','alternative_explanations':['exposure','artist history','period','genre/style'],'theory_support':['scientific literature required before promotion'],'deduction':'Test X as a bounded compositional constraint, not as a success prediction.','musical_realization':{'target':'melodic MIDI prototype','parameter':'X'},'provenance':['observed corpus snapshot'],'purpose':'CREATIVE_DEDUCTION','claim_level':'ASSOCIATIVE','genre_style_role':'STRATIFICATION','source_type':'OBSERVED_DATA'}

def test_associative_deduction_passes(): assert evaluate(base())['eligible']
def test_prediction_fails():
 x=base();x['purpose']='HIT_PREDICTION';assert not evaluate(x)['eligible']
def test_industry_claim_without_support_fails():
 x=base();x['source_type']='INDUSTRY_CLAIM';assert not evaluate(x)['eligible']
def test_causal_language_without_experiment_fails():
 x=base();x['association_evidence']['causal_language']=True;assert not evaluate(x)['eligible']
