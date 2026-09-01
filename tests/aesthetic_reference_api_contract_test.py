import hashlib, importlib.util, pathlib
from fastapi.testclient import TestClient

p=pathlib.Path('services/aesthetic_reference_api/app.py')
spec=importlib.util.spec_from_file_location('hooklab_api',p)
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def fake_run(data, filename, session_id, sha):
    assert hashlib.sha256(data).hexdigest()==sha
    return {'status':'PASS','analysis_mode':'ONLINE_API_FALLBACK','session_id':session_id,'scientific_ingestion':False,'gate_a_ingestion':False,'m300_ingestion':False,'source_audio_persistence':'NONE','tempo_bpm_median':120.0,'beat_count':8}
mod.run_analysis=fake_run
c=TestClient(mod.app)
r=c.get('/health'); assert r.status_code==200 and r.json()['role']=='ONLINE_API_FALLBACK'
data=b'RIFFfake-audio-for-contract'
sha=hashlib.sha256(data).hexdigest()
r=c.post('/v1/analyze-reference',files={'audio':('x.wav',data,'audio/wav')},data={'session_id':'HL-API-TEST','sha256':sha})
assert r.status_code==200, r.text
j=r.json(); assert j['status']=='PASS' and j['scientific_ingestion'] is False and j['source_audio_persistence']=='NONE'
r=c.post('/v1/analyze-reference',files={'audio':('x.txt',b'x','text/plain')},data={'session_id':'x','sha256':'0'*64})
assert r.status_code==415
print('PASS online fallback API HTTP contract')
