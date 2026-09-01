#!/usr/bin/env python3
import copy
from statistical_deduction_final_gate import evaluate,promotable

def base():
 return {'ANALYSIS_ID':'X','POPULATION_SCOPE':'P','OUTCOME':'O','N_ELIGIBLE':100,'FEATURE_DOMAIN':'MUSIC_FORM','FEATURE':'f','ANALYSIS_PHASE':'CONFIRMATORY','EFFECT_SIZE_AND_UNCERTAINTY':{'effect':{'rho':.3},'uncertainty':{'ci95':[.1,.5]}},'MULTIPLICITY_CONTROL':{'method':'BH','q':.01},'ROBUSTNESS_SENSITIVITY':'PASS','REPLICATION_STATUS':'REPLICATED','THEORY_SUPPORT':'SUPPORTED_BY_PEER_REVIEWED_LITERATURE','CLAIM_LEVEL':'ASSOCIATIVE','CALIBRATION_STATUS':'NOT_APPLICABLE','DECISION':'PROMOTE_TO_CONDITIONED_DEDUCTION'}

def main():
 x=base();ok,_=promotable(x);assert ok
 y=copy.deepcopy(x);y['EFFECT_SIZE_AND_UNCERTAINTY']['uncertainty']='NOT_REPORTED_IN_SOURCE';assert not promotable(y)[0]
 y=copy.deepcopy(x);y['ANALYSIS_PHASE']='EXPLORATORY';assert not promotable(y)[0]
 y=copy.deepcopy(x);y['FEATURE_DOMAIN']='MUSIC_MELODY';y['CALIBRATION_STATUS']='NOT_CALIBRATED';assert not promotable(y)[0]
 null={'rows':[dict(base(),DECISION='NO_PROMOTION')]};o=evaluate(null);assert o['status']=='VALID_NULL_NON_PROMOTION_COMPLETION' and o['scientific_d_state']=='BLOCKED_NO_POSITIVE_ELIGIBLE_DEDUCTION'
 pending=dict(base(),ANALYSIS_ID='DALI_PENDING',FEATURE_DOMAIN='MUSIC_MELODY',CALIBRATION_STATUS='REPRESENTATION_CALIBRATED_DUAL_REFERENCE',ANALYSIS_PHASE='PRE_REGISTERED_PENDING_EXTERNAL_PROVISIONING',EFFECT_SIZE_AND_UNCERTAINTY={'effect':None,'uncertainty':'NOT_ESTIMABLE_WITHOUT_POPULATION_DATA'},DECISION='AUDIT')
 o=evaluate({'rows':[pending]});assert o['status']=='VALID_NULL_NON_PROMOTION_COMPLETION'
 print('PASS: statistical deduction gate is fail-closed')
if __name__=='__main__':main()
