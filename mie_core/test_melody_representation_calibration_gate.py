from melody_representation_calibration_gate import evaluate

def good():
 feats={}
 for f in ('pitch_range_st','median_pitch_st','median_interval_st','stepwise_motion_share','pitch_repetition_share'):
  feats[f]={'n':40,'spearman_rho':.9,'median_abs_error':.2,'max_allowed_median_abs_error':1.0}
 return {'paired_items':40,'minimum_paired_items':30,'independent_reference':True,'same_performance_or_aligned_identity':True,'feature_agreement':feats}
def test_pass(): assert evaluate(good())['status']=='REPRESENTATION_CALIBRATED'
def test_small_n_blocks():
 x=good();x['paired_items']=10;assert evaluate(x)['status']=='REPRESENTATION_CALIBRATION_PENDING'
def test_identity_blocks():
 x=good();x['same_performance_or_aligned_identity']=False;assert evaluate(x)['status']=='REPRESENTATION_CALIBRATION_PENDING'
def test_unstable_blocks():
 x=good();x['feature_agreement']={};assert evaluate(x)['status']=='REPRESENTATION_CALIBRATION_PENDING'
