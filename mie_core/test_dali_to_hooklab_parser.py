from dali_to_hooklab_parser import parse_entry

def sample(gt=False,ncc=.91):
 return {'info':{'id':'x1','artist':'Artist','title':'Song','dataset_version':2.0,'ground-truth':gt,'scores':{'NCC':ncc},'metadata':{'language':'en','genres':['pop']}},'annotations':{'type':'horizontal','annot':{'notes':[{'text':'la','time':[0.0,.5],'freq':[440.0,440.0],'index':0},{'text':'la','time':[.5,1.0],'freq':[493.883,493.883],'index':1}]}}}

def test_high_ncc_passes_parse():
 x=parse_entry(sample());assert x['status']=='PASS_ANNOTATION_PARSE';assert round(x['melody_summary']['pitch_range_semitones'])==2;assert x['provenance']['audio_retrieval_attempted'] is False

def test_ground_truth_passes():
 x=parse_entry(sample(gt=True,ncc=.2));assert x['quality_tier']=='GROUND_TRUTH';assert x['status']=='PASS_ANNOTATION_PARSE'

def test_low_quality_is_audit():
 x=parse_entry(sample(gt=False,ncc=.5));assert x['status']=='AUDIT_ANNOTATION_QUALITY';assert x['scientific_promotion'] is False

def test_vertical_is_audit():
 x=sample();x['annotations']['type']='vertical';assert parse_entry(x)['status']=='AUDIT_FORMAT'
