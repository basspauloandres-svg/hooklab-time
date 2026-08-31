import sys
sys.path.insert(0,'mie_core')
from paired_representation_agreement import analyze
base={'identity':'PASS','reference':{'pitch_range_st':8},'candidate':{'pitch_range_st':8}}
r=analyze([dict(base,independent_reference=True) for _ in range(30)])
assert r['independent_reference'] is True
r2=analyze([dict(base,independent_reference=True) for _ in range(29)]+[dict(base)])
assert r2['independent_reference'] is False
r3=analyze([])
assert r3['independent_reference'] is False
assert r3['same_performance_or_aligned_identity'] is False
print('PASS calibration independence fail-closed')
