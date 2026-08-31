from t1_qualification_matrix_builder import build,GATES

def queue():
 return {'cohort_key':'pop_rock::dance_pop','target_checkpoint':30,'existing_qualified_t0':5,'candidates':[{'title':'A','artist':'B','discovery_basis':'x'}]}
def ev(statuses):
 return {'records':[{'title':'A','artist':'B','gates':{g:{'status':statuses.get(g,'PENDING')} for g in GATES}}]}
def test_discovery_alone_never_qualifies():
 out=build(queue(),{'records':[]})
 assert out['new_rows'][0]['qualification_status']=='PENDING'
 assert out['t0_plus_new_qualified']==5
def test_all_pass_qualifies():
 out=build(queue(),ev({g:'PASS' for g in GATES}))
 assert out['new_rows'][0]['qualification_status']=='QUALIFIED_FOR_MATRIX_X'
def test_audit_distinct_from_fail():
 s={g:'PASS' for g in GATES};s['version']='AUDIT'
 out=build(queue(),ev(s));assert out['new_rows'][0]['qualification_status']=='AUDIT'
def test_fail_rejects():
 s={g:'PASS' for g in GATES};s['full_song']='FAIL'
 out=build(queue(),ev(s));assert out['new_rows'][0]['qualification_status']=='REJECTED'
