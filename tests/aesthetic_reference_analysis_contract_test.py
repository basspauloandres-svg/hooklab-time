import sys
sys.path.insert(0,'mie_core')
from aesthetic_reference_analysis_contract import normalize
sensor={'ephemeral_sha256':'abc','audio_persistence':'NONE','coverage':'FULL','duration_s':12.5,'T_sensor':'Beat This','T_status':'VALID','T_tactus_count':20,'T_tempo_bpm_median':100.0,'T_tactus_times':[0.1,0.7],'M_post_ornament_count':8,'M_range_raw':[60,72],'version':'FULL M/T Sensor Regression v0.3','T_model_sha256':'m','T_mel_model_sha256':'mel'}
r=normalize(sensor,'HL-TEST','abc')
assert r['status']=='PASS'
assert r['role']=='AESTHETIC_REFERENCE_ANALYSIS'
assert r['scientific_ingestion'] is False
assert r['gate_a_ingestion'] is False
assert r['m300_ingestion'] is False
assert r['source_audio_persistence']=='NONE'
assert r['tempo_bpm_median']==100.0
assert normalize(sensor,'HL-TEST','different')['status']=='FAIL'
print('PASS')
