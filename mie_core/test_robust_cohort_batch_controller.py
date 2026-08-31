from robust_cohort_batch_controller import evaluate

def valid(i,prom=False):
 return {'song_id':str(i),'identity_pass':True,'version_pass':True,'full_song_pass':True,'provenance_pass':True,'full_tmt_pass':True,'mass_success_pass':True,'genre_style_pass':True,'scientific_promotion':prom}
def test_t0_points_to_t1():
 out=evaluate([valid(i) for i in range(5)])
 assert out['qualified_candidate_n']==5 and out['next_checkpoint']==30 and out['rows_needed_for_next_checkpoint']==25
def test_preview_never_counts_as_robust_row():
 r=valid(1);r['audio_scope']='PUBLIC_SHORT_PREVIEW';r['role']='PROTOTYPE_EVIDENCE_NOT_FINAL_SAMPLE'
 out=evaluate([r])
 assert out['qualified_candidate_n']==0
def test_candidate_and_scientific_promotion_are_separate():
 out=evaluate([valid(i,False) for i in range(50)])
 assert out['qualified_candidate_n']==50 and out['scientifically_promoted_n']==0
 assert out['candidate_stage']=='T2_ANALYTICAL_OR_HIGHER' and out['scientific_promotion_complete'] is False
def test_50_promoted_rows_still_need_stability_elsewhere():
 out=evaluate([valid(i,True) for i in range(50)])
 assert out['qualified_candidate_n']==50 and out['scientifically_promoted_n']==50
 assert 'N alone does not establish representativeness' in out['invariants']
