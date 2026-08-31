from bimmuda_provider_admissibility_gate import evaluate

def base():
    return {
        'repository_public':True,
        'full_main_melody_midi':True,
        'section_midis':True,
        'metadata_available':True,
        'manual_transcription_quality_control':True,
        'target_population_intersection_observed':True,
        'dataset_license_status':'NO_EXPLICIT_REPOSITORY_DATASET_LICENSE_OBSERVED',
        'computational_processing_authorized':False,
    }

def test_public_repo_without_dataset_license_is_audit():
    out=evaluate(base())
    assert out['status']=='PROVIDER_AUDIT_REQUIRED'
    assert 'DATASET_FILE_LICENSE_OR_RESEARCH_PERMISSION_NOT_EXPLICIT' in out['blocking_reasons']

def test_explicit_research_permission_can_unlock_provider():
    x=base();x['dataset_license_status']='EXPLICIT_RESEARCH_PERMISSION';x['computational_processing_authorized']=True
    out=evaluate(x)
    assert out['status']=='PROVIDER_ADMISSIBLE'
    assert out['downstream_eligible'] is True
