from dali_research_provider_adapter import resolve

def test_unprovisioned_is_reference_unavailable():
 x=resolve(None);assert x['status']=='REFERENCE_UNAVAILABLE';assert x['audio_access_attempted'] is False

def test_missing_path_is_reference_unavailable(tmp_path):
 x=resolve(str(tmp_path/'missing'));assert x['status']=='REFERENCE_UNAVAILABLE'

def test_present_dataset_stays_audit_until_schema_validation(tmp_path):
 x=resolve(str(tmp_path));assert x['status']=='AUDIT_PROVISIONED';assert x['scientific_promotion'] is False
