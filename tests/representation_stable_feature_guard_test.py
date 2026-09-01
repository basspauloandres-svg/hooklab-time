import json,sys
sys.path.insert(0,'mie_core')
from representation_stable_feature_guard import evaluate
allow=json.load(open('config/representation_stable_features_v1.json'))
a=evaluate(['median_pitch_st'],allow)
assert a['status']=='PASS'
assert a['blocked_requested_features']==[]
b=evaluate(['pitch_range_st'],allow)
assert b['status']=='BLOCKED'
assert b['blocked_requested_features']==['pitch_range_st']
c=evaluate(['median_pitch_st','median_interval_st'],allow)
assert c['status']=='BLOCKED'
assert c['blocked_requested_features']==['median_interval_st']
print('PASS representation stable feature guard')
