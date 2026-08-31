from t1_observed_evidence_merger import merge

def base():
 return {'rows':[{'title':'A','artist':'X','gates':{'mass_success':'PENDING','identity':'PENDING','genre_style':'PENDING','version':'PENDING','symbolic_source':'PENDING','full_song':'PENDING','provenance':'PENDING','full_tmt':'PENDING'}}]}
def test_partial_batch_does_not_qualify():
 b={'batch_id':'B1','rows':[{'title':'A','artist':'X','gates':{'mass_success':'PASS','identity':'PASS'}}]}
 out=merge(base(),b)
 assert out['qualified_n']==0
 assert out['rows'][0]['qualification_status']=='PENDING'
def test_audit_is_not_fail():
 b={'batch_id':'B1','rows':[{'title':'A','artist':'X','gates':{'mass_success':'PASS','identity':'PASS','genre_style':'AUDIT'}}]}
 out=merge(base(),b)
 assert out['rows'][0]['qualification_status']=='AUDIT_REQUIRED'
 assert out['rejected_n']==0
def test_all_pass_qualifies():
 g={k:'PASS' for k in ('mass_success','identity','genre_style','version','symbolic_source','full_song','provenance','full_tmt')}
 out=merge(base(),{'batch_id':'B2','rows':[{'title':'A','artist':'X','gates':g}]})
 assert out['qualified_n']==1
 assert out['rows'][0]['qualification_status']=='QUALIFIED_FOR_MATRIX_X'
